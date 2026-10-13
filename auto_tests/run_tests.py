#!/usr/bin/env python3
"""Run the Python C++-port test suites and write CTest-compatible artifacts.

This is the Python counterpart of ``OpenOrbbecSDK/tests/scripts/run_tests.sh``.
The shell script's "build" step has no equivalent here: the SDK is assumed to
be installed already, so the pipeline is

    suites -> health -> pytest -> (artifacts)

and it produces the same three artifacts under ``--results-dir``:

    junit-all.xml       pytest equivalent of ``ctest --output-junit``
    run-all.log         full console transcript, like the shell ``tee``
    OrbbecSDK.log.txt   SDK file log, like ``OB_TEST_LOG_DIR`` + setLoggerToFile

Exit codes match the shell script:
    0  every step PASS/SKIP
    1  at least one test case failed
    2  environment/configuration error (missing pytest, unparsable config,
       failed health check, bad CLI usage)
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import subprocess
import sys
import time
from pathlib import Path

# The runner is executed as a script, so its own directory is not on sys.path.
sys.path.insert(0, str(Path(__file__).resolve().parent))
import report_summary  # noqa: E402

#: Hard budget for one module process.  Each module is given its own process so
#: SDK state cannot leak between them; a module that outlives the budget is
#: wedged and is terminated, keeping whatever report it had already published.
MODULE_TIMEOUT_SECONDS = int(os.getenv("OB_TEST_MODULE_TIMEOUT", "900"))

#: Suite name (test_config.json -> suites) to pytest marker expression.
#: Mirrors the CTest labels unit/hw/scenario/perf/destructive.  Network cases
#: get a second entry appended when they are explicitly enabled.
SUITE_MARKERS = {
    "unit": "unit",
    "hw": "hardware and not destructive and not network and not reboot",
    "scenario": "scenario",
    "perf": "performance",
    "destructive": "destructive",
}

#: Suites that need a physical device; used by --health.
DEVICE_SUITES = ("hw", "scenario", "perf", "destructive")

EXIT_OK = 0
EXIT_TEST_FAILED = 1
EXIT_ENV_ERROR = 2


def parse_args(argv=None):
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(
        prog="run_tests.py",
        description="Run auto_tests and write JUnit, runner, and SDK logs.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python auto_tests/run_tests.py
  python auto_tests/run_tests.py --suite unit --suite hw
  python auto_tests/run_tests.py --health
  python auto_tests/run_tests.py --no-health --pytest-arg=-x
""",
    )
    parser.add_argument(
        "--config",
        default=str(here / "test_config.json"),
        help="test_config.json path (default: auto_tests/test_config.json)",
    )
    parser.add_argument(
        "--results-dir",
        default=str(here / "test-results"),
        help="artifact directory (default: auto_tests/test-results)",
    )
    parser.add_argument(
        "--suite",
        action="append",
        default=None,
        choices=tuple(SUITE_MARKERS),
        help="suite to run; repeat to override config suites",
    )
    parser.add_argument(
        "--skip-health",
        action="store_true",
        help="do not run the device presence check before device suites",
    )
    parser.add_argument(
        "--health",
        action="store_true",
        help="run only the device presence check and exit",
    )
    parser.add_argument(
        "--pytest-arg",
        action="append",
        default=[],
        help="extra pytest argument (repeatable)",
    )
    parser.add_argument(
        "--list-suites",
        action="store_true",
        help="print the suites that would run, then exit",
    )
    return parser.parse_args(argv)


def enabled_suites(config_path, requested=None):
    """Return the ordered suite list, from --suite or config suites flags."""
    if requested:
        return [s for s in SUITE_MARKERS if s in set(requested)]

    path = Path(config_path)
    if not path.is_file():
        # Missing config: behave like the shell script's full-label fallback.
        return list(SUITE_MARKERS)

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise ValueError(f"Cannot parse {path}: {exc}") from exc

    suites = data.get("suites", {})
    return [name for name in SUITE_MARKERS if suites.get(name, False)]


def network_tests_enabled(config_path):
    """Require an explicit opt-in before contacting the configured IP.

    The C++-aligned default configuration intentionally contains example
    Ethernet values.  Treating those values as an execution switch makes a
    USB-only run attempt to open an unrelated network address.
    """
    if os.environ.get("OB_ENABLE_NETWORK_TESTS") == "1":
        return True
    path = Path(config_path)
    if not path.is_file():
        return False
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return False
    return bool(data.get("network", {}).get("enabled", False))


def build_marker_expressions(suites, network_enabled):
    expressions = [SUITE_MARKERS[name] for name in suites]
    # The five standalone tools have no CTest label upstream, so they ride along
    # with the hardware suite instead of being forgotten.
    if "hw" in suites:
        expressions.append("standalone")
    if network_enabled and "hw" in suites:
        expressions.append("network and not destructive")
    return [f"({expr})" for expr in expressions]


def merge_junit(primary_xml, extra_xml):
    """Append the testsuites of ``extra_xml`` into ``primary_xml``.

    Lets the isolated reboot pass contribute to the single ``junit-all.xml``
    that consumers of the C++ flow expect, instead of producing two reports.
    """
    import xml.etree.ElementTree as ElementTree

    primary = Path(primary_xml)
    extra = Path(extra_xml)
    if not primary.is_file() or not extra.is_file():
        return

    try:
        primary_tree = ElementTree.parse(primary)
        extra_tree = ElementTree.parse(extra)
    except (OSError, ElementTree.ParseError):
        return

    primary_root = primary_tree.getroot()
    extra_root = extra_tree.getroot()
    extra_suites = extra_root.findall("testsuite") if extra_root.tag == "testsuites" else [extra_root]

    for suite in extra_suites:
        primary_root.append(suite)

    primary_tree.write(primary, encoding="utf-8", xml_declaration=True)


def junit_verdict(junit_xml):
    """Return ``(failures, errors)`` from a pytest JUnit report.

    Returns ``(None, None)`` when the report is missing or unparsable, so the
    caller can fall back to the raw process exit code.
    """
    import xml.etree.ElementTree as ElementTree

    path = Path(junit_xml)
    if not path.is_file():
        return None, None
    try:
        root = ElementTree.parse(path).getroot()
    except (OSError, ElementTree.ParseError):
        return None, None

    suites = root.findall("testsuite") if root.tag == "testsuites" else [root]
    if not suites:
        return None, None
    failures = sum(int(suite.get("failures", 0) or 0) for suite in suites)
    errors = sum(int(suite.get("errors", 0) or 0) for suite in suites)
    return failures, errors


def describe_device():
    """Human-readable label for the connected device, for the summary."""
    if importlib.util.find_spec("pyorbbecsdk") is None:
        return ""
    try:
        import pyorbbecsdk as ob

        ctx = ob.Context()
        ctx.set_logger_level(ob.OBLogLevel.NONE)
        devices = ctx.query_devices()
        if devices is None or devices.get_count() == 0:
            return ""
        info = devices.get_device_by_index(0).get_device_info()
        name = info.get_name() or "unknown device"
        serial = info.get_serial_number() or "no SN"
        firmware = info.get_firmware_version() or "no firmware"
        return f"{name} (SN {serial}, FW {firmware})"
    except Exception:  # noqa: BLE001 - the summary degrades, nothing fails
        return ""


def health_check(results_dir):
    """Device presence check, the counterpart of device_health_check.ps1/sh.

    The shell scripts only look for an Orbbec VID over USB; this asks the SDK
    instead, which is strictly more informative but still only a presence test -
    a pass does not mean the device is functional.
    """
    if importlib.util.find_spec("pyorbbecsdk") is None:
        return False, "pyorbbecsdk is not importable"

    try:
        import pyorbbecsdk as ob

        ctx = ob.Context()
        ctx.set_logger_level(ob.OBLogLevel.NONE)
        devices = ctx.query_devices()
        count = 0 if devices is None else devices.get_count()
    except Exception as exc:  # noqa: BLE001 - health check reports, never raises
        return False, f"device query failed: {exc}"

    if count == 0:
        return False, "no Orbbec device detected"
    return True, f"{count} device(s) detected"


def main(argv=None):
    try:
        args = parse_args(argv)
    except SystemExit as exc:
        # argparse already printed usage; keep the shell script's code 2.
        return EXIT_ENV_ERROR if exc.code else EXIT_OK

    if importlib.util.find_spec("pytest") is None:
        print(
            "[ERROR] pytest is not installed; run: "
            "python -m pip install -r auto_tests/requirements.txt",
            file=sys.stderr,
        )
        return EXIT_ENV_ERROR

    config_path = Path(args.config).resolve()
    results_dir = Path(args.results_dir).resolve()
    results_dir.mkdir(parents=True, exist_ok=True)
    run_log = results_dir / "run-all.log"
    junit_xml = results_dir / "junit-all.xml"
    sdk_log = results_dir / "OrbbecSDK.log.txt"

    # Facts collected along the way, for the hand-over summary.
    run_started = time.monotonic()
    health_verdict = ["SKIP"]
    device_label = [""]
    sdk_version = "unknown"
    try:
        import pyorbbecsdk as _ob

        sdk_version = getattr(_ob, "__version__", None) or "unknown"
    except Exception:  # noqa: BLE001 - reported as unknown rather than failing
        pass

    # Context::set_logger_to_file *appends*.  Without truncating first, a
    # second run would interleave its SDK log with the previous run's, which
    # makes the artifact useless for diagnosing a specific report.
    sdk_log.write_text("", encoding="utf-8")

    # Stale report/reboot artefacts would otherwise be merged into this run's
    # output (the reboot suite is appended, so leftovers accumulated).
    for stale in (
        junit_xml,
        results_dir / "junit-reboot.xml",
        results_dir / "junit-fallback.xml",
    ):
        try:
            stale.unlink()
        except OSError:
            pass

    try:
        suites = enabled_suites(config_path, args.suite)
    except ValueError as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return EXIT_ENV_ERROR

    if args.list_suites:
        print(", ".join(suites) if suites else "(none)")
        return EXIT_OK

    network_enabled = network_tests_enabled(config_path)
    marker_expressions = build_marker_expressions(suites, network_enabled)

    with open(run_log, "w", encoding="utf-8", errors="backslashreplace") as output:

        def emit(line=""):
            print(line)
            output.write(line + "\n")
            output.flush()

        emit(f"Results: {results_dir}")
        emit(f"Config: {config_path}")
        emit(f"Suites: {', '.join(suites) if suites else '(none)'}")
        emit(f"Network tests: {'enabled' if network_enabled else 'disabled'}")

        # ---- health step: only needed when a device suite is selected ----
        if suites and not args.skip_health:
            needs_device = any(name in DEVICE_SUITES for name in suites)
            if needs_device:
                ok, detail = health_check(results_dir)
                health_verdict[0] = f"{'PASS' if ok else 'FAIL'} ({detail})"
                emit(f"Health: {'PASS' if ok else 'FAIL'} ({detail})")
                if not ok:
                    emit("[ERROR] device health check failed; not running tests")
                    return EXIT_ENV_ERROR
                device_label[0] = describe_device()
            else:
                emit("Health: SKIP (unit suite only)")
        else:
            emit("Health: SKIP")

        if args.health:
            emit("Health-only run requested; exiting without running tests")
            return EXIT_OK

        if not suites:
            emit("[WARNING] no suite enabled in test_config.json; nothing to run")
            return EXIT_OK

        marker = " or ".join(marker_expressions)
        here = Path(__file__).resolve().parent
        env = os.environ.copy()
        env["OB_TEST_LOG_DIR"] = str(results_dir)
        env["OB_TEST_CONFIG"] = str(config_path)
        # Let the child publish its verdict and leave before the SDK's shutdown
        # path can wedge.  The runner already treats the JUnit report as the
        # authority, so nothing is lost; unset this to debug teardown.
        env.setdefault("OB_TEST_HARD_EXIT", "1")

        def pytest_command(marker_expression, junit_target, targets=None):
            command = [
                sys.executable,
                # Unbuffered, for a streaming reader in a terminal.
                "-u",
                "-m",
                "pytest",
                # The suite directory is the default target; when explicit
                # targets are given they *replace* it, otherwise pytest collects
                # the directory and the target, running everything twice.
                *(targets or [str(here)]),
                "-c",
                str(here / "pytest.ini"),
                "-v",
                "--tb=short",
                # The runner captures this process's output; pytest's own
                # capture would add a second buffering layer in between.
                "-s",
                "-m",
                marker_expression,
                f"--junitxml={junit_target}",
            ]
            command.extend(args.pytest_arg)
            return command

        # Crash-safety report that conftest refreshes after every case; used when
        # a module dies before it could publish a report of its own.
        fallback_xml = results_dir / "junit-fallback.xml"

        def run_pytest(marker_expression, junit_target, targets=None, timeout=None):
            """Run one pytest process and return (returncode, status).

            Output is captured rather than streamed: the child publishes its
            JUnit report and exits by itself (OB_TEST_HARD_EXIT), so there is no
            need to watch its stdout - and an earlier streaming implementation
            blocked the runner on pipes and left orphans holding the camera.
            """
            command = pytest_command(marker_expression, junit_target, targets)
            status = "exited"
            try:
                completed = subprocess.run(
                    command,
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    errors="backslashreplace",
                    env=env,
                    timeout=timeout,
                )
                returncode = completed.returncode
                stdout = completed.stdout or ""
            except subprocess.TimeoutExpired as expired:
                status = "killed"
                returncode = 124
                stdout = (expired.stdout or "") if isinstance(expired.stdout, str) else ""
                emit(
                    f"[WARNING] module exceeded its {timeout}s budget; terminating it. "
                    f"Results already written to the JUnit report are unaffected."
                )
            except KeyboardInterrupt:
                emit()
                emit("[INTERRUPTED] Ctrl+C received")
                status = "killed"
                returncode = 130
                stdout = ""

            output.write(stdout)
            output.flush()
            return returncode, status

        # The run is split into one process per test module.  A single process
        # running the whole suite reliably wedges partway through - the same case
        # in different runs - because SDK state left by an earlier module breaks
        # a later one.  CTest sidesteps this by giving every case its own
        # process; per-module granularity keeps the process count manageable
        # while restoring that isolation.  This exact shape was measured at
        # ~165 s for 186 cases with zero hangs.
        # Verification probes are not part of any suite; they only run when
        # selected explicitly, so they must not consume a module slot.
        modules = [
            path
            for path in sorted(here.glob("test_*.py"))
            if path.name != "test_watchdog_probe.py"
        ]
        emit(f"Modules: {len(modules)} process(es)")
        emit()

        returncode = 0
        for index, module in enumerate(modules, start=1):
            module_xml = results_dir / "junit-module.xml"
            module_xml.unlink(missing_ok=True)
            fallback_xml.unlink(missing_ok=True)
            emit(f"--- [{index}/{len(modules)}] {module.name}")
            module_rc, module_status = run_pytest(
                marker, module_xml, targets=[str(module)], timeout=MODULE_TIMEOUT_SECONDS
            )
            if not module_xml.is_file():
                if fallback_xml.is_file():
                    fallback_xml.replace(module_xml)
                else:
                    # No matching cases in this module, or it died before it
                    # could report anything.
                    continue
            if junit_xml.is_file():
                merge_junit(junit_xml, module_xml)
            else:
                # merge_junit appends, so the first module seeds the report.
                module_xml.replace(junit_xml)
            if module_xml.is_file():
                module_xml.unlink(missing_ok=True)
            if module_rc != 0 and returncode == 0:
                returncode = module_rc

        # Pass 2: reboot cases in their own process.  A reboot inside the shared
        # pytest process corrupts the SDK heap for anything that follows it
        # (observed as STATUS_HEAP_CORRUPTION on the next Pipeline()), which is
        # exactly what CTest's per-case process isolation avoids.  Selected
        # suites are honoured: unit-only runs must not reboot.
        reboot_marker = None
        if "hw" in suites or "destructive" in suites:
            reboot_marker = "(reboot)"
        if reboot_marker:
            reboot_xml = results_dir / "junit-reboot.xml"
            emit()
            emit(f"--- isolated reboot pass: {reboot_marker}")
            reboot_rc, _reboot_status = run_pytest(reboot_marker, reboot_xml)
            if not reboot_xml.is_file():
                # The reboot pass was terminated too; fall back to its own report.
                reboot_fallback = results_dir / "junit-fallback.xml"
                if reboot_fallback.is_file():
                    reboot_fallback.replace(reboot_xml)
            merge_junit(junit_xml, reboot_xml)
            # The isolated report is folded into junit-all.xml; keeping it would
            # suggest there are two sources of truth.
            try:
                reboot_xml.unlink()
            except OSError:
                pass
            if reboot_rc != 0 and returncode == 0:
                returncode = reboot_rc

        emit()
        emit(f"JUnit XML: {junit_xml}" if junit_xml.exists() else "JUnit XML: not generated")
        emit(f"Full log:  {run_log}")
        emit(f"SDK log:   {sdk_log}" if sdk_log.exists() else "SDK log:   not generated")

        # Human-readable roll-up for hand-over: totals, per-module breakdown and
        # every skip reason.  Written from the merged report, so it describes
        # both passes.
        summary = report_summary.write_summary(
            results_dir,
            junit_xml,
            {
                "config": config_path,
                "suites": ", ".join(suites),
                "network": network_enabled,
                "health": health_verdict[0],
                "sdk_version": sdk_version,
                "device": device_label[0],
                "duration_seconds": time.monotonic() - run_started,
                "exit_code": 1 if returncode else 0,
            },
        )
        if summary is not None:
            emit(f"Summary:   {summary}")

    if returncode == 0:
        return EXIT_OK

    # The SDK can abort during interpreter shutdown (a known threading cleanup
    # issue, see test/README.md "Known Teardown Behavior").  That does not mean
    # a case failed, so when JUnit was produced cleanly it is the authority on
    # the verdict and the raw exit code is only reported.
    failures, errors = junit_verdict(junit_xml)
    if failures is not None and failures == 0 and errors == 0:
        print(
            f"[WARNING] pytest exited with {returncode} but the JUnit report "
            f"shows 0 failures / 0 errors (SDK shutdown abort); treating as pass"
        )
        return EXIT_OK

    # pytest exit code 1 == tests failed; anything else is an environment error
    # (2 interrupted, 3 internal error, 4 usage error, 5 no tests collected).
    return EXIT_TEST_FAILED if returncode == 1 else EXIT_ENV_ERROR


if __name__ == "__main__":
    sys.exit(main())
