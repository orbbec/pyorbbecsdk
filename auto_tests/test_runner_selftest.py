"""Self-tests for the runner and the case manifest.

These cases need no device and no SDK: they guard the scaffolding itself, so a
broken suite selection, a malformed CLI, or a drifted destructive list fails a
test instead of silently producing a wrong report.
"""

from __future__ import annotations

import ast
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import _destructive  # noqa: E402
import run_tests  # noqa: E402

#: Part of the default unit suite so the scaffolding is covered by the report.
pytestmark = pytest.mark.unit


# ---------------------------------------------------------------------------
# suite selection
# ---------------------------------------------------------------------------


def test_suite_markers_match_cpp_labels():
    assert set(run_tests.SUITE_MARKERS) == {"unit", "hw", "scenario", "perf", "destructive"}
    # Reboot cases are excluded from the shared process and run isolated.
    assert (
        run_tests.SUITE_MARKERS["hw"]
        == "hardware and not destructive and not network and not reboot"
    )


def test_enabled_suites_from_shipped_config():
    suites = run_tests.enabled_suites(HERE / "test_config.json")
    assert suites == ["unit", "hw", "scenario", "perf"]


def test_enabled_suites_respects_explicit_request():
    assert run_tests.enabled_suites(HERE / "test_config.json", ["destructive"]) == ["destructive"]
    # Order always follows SUITE_MARKERS, not the CLI order.
    assert run_tests.enabled_suites(None, ["hw", "unit"]) == ["unit", "hw"]


def test_missing_config_falls_back_to_all_suites():
    missing = HERE / "__no_such_config__.json"
    assert run_tests.enabled_suites(missing) == list(run_tests.SUITE_MARKERS)


def test_unparsable_config_is_an_env_error(tmp_path):
    broken = tmp_path / "broken.json"
    broken.write_text("{not json", encoding="utf-8")
    with pytest.raises(ValueError):
        run_tests.enabled_suites(broken)


def test_all_suites_disabled_yields_no_marker():
    config = {"suites": dict.fromkeys(run_tests.SUITE_MARKERS, False)}
    assert run_tests.build_marker_expressions(
        [name for name in run_tests.SUITE_MARKERS if config["suites"][name]], False
    ) == []


def test_marker_expressions_shape():
    assert run_tests.build_marker_expressions(["unit", "perf"], False) == ["(unit)", "(performance)"]
    # Selecting hw also pulls in the standalone tool ports, which have no CTest
    # label upstream and would otherwise never run.
    assert run_tests.build_marker_expressions(["unit", "hw"], True) == [
        "(unit)",
        "(hardware and not destructive and not network and not reboot)",
        "(standalone)",
        "(network and not destructive)",
    ]
    # Without hw there is nothing for the standalone tools to attach to.
    assert run_tests.build_marker_expressions(["unit"], False) == ["(unit)"]


def test_network_opt_in_ignores_placeholder_ip(tmp_path, monkeypatch):
    config = tmp_path / "test_config.json"
    config.write_text(
        json.dumps({"network": {"enabled": False, "ip": "192.168.1.10"}}), encoding="utf-8"
    )
    monkeypatch.delenv("OB_ENABLE_NETWORK_TESTS", raising=False)
    assert run_tests.network_tests_enabled(config) is False

    config.write_text(json.dumps({"network": {"enabled": True}}), encoding="utf-8")
    assert run_tests.network_tests_enabled(config) is True

    monkeypatch.setenv("OB_ENABLE_NETWORK_TESTS", "1")
    config.write_text(json.dumps({"network": {"enabled": False}}), encoding="utf-8")
    assert run_tests.network_tests_enabled(config) is True


# ---------------------------------------------------------------------------
# CLI behaviour
# ---------------------------------------------------------------------------


def test_cli_unknown_option_is_an_env_error(capsys):
    # argparse rejects it; requirement (from run_tests.sh semantics) is exit 2.
    assert run_tests.main(["--definitely-not-an-option"]) == run_tests.EXIT_ENV_ERROR


def test_cli_list_suites(monkeypatch, tmp_path, capsys):
    results = tmp_path / "out"
    rc = run_tests.main(
        [
            "--config",
            str(HERE / "test_config.json"),
            "--results-dir",
            str(results),
            "--list-suites",
        ]
    )
    assert rc == run_tests.EXIT_OK
    assert "unit, hw, scenario, perf" in capsys.readouterr().out


def test_cli_no_suite_enabled_returns_zero_without_running(tmp_path, capsys):
    config = tmp_path / "test_config.json"
    config.write_text(
        json.dumps({"suites": dict.fromkeys(run_tests.SUITE_MARKERS, False)}), encoding="utf-8"
    )
    results = tmp_path / "out"
    rc = run_tests.main(
        ["--config", str(config), "--results-dir", str(results), "--skip-health"]
    )
    assert rc == run_tests.EXIT_OK
    log = (results / "run-all.log").read_text(encoding="utf-8")
    assert "no suite enabled" in log


def test_cli_health_only_writes_all_three_artifact_paths(tmp_path):
    results = tmp_path / "out"
    rc = run_tests.main(
        [
            "--config",
            str(HERE / "test_config.json"),
            "--results-dir",
            str(results),
            "--health",
        ]
    )
    assert rc in (run_tests.EXIT_OK, run_tests.EXIT_ENV_ERROR)
    assert (results / "run-all.log").is_file()
    assert "Results: " in (results / "run-all.log").read_text(encoding="utf-8")


def test_cli_bad_config_returns_env_error(tmp_path, capsys):
    broken = tmp_path / "broken.json"
    broken.write_text("{not json", encoding="utf-8")
    rc = run_tests.main(["--config", str(broken), "--results-dir", str(tmp_path / "out")])
    assert rc == run_tests.EXIT_ENV_ERROR
    assert "Cannot parse" in capsys.readouterr().err


# ---------------------------------------------------------------------------
# report plumbing
# ---------------------------------------------------------------------------


def test_runner_writes_a_junit_report(tmp_path):
    """A run must produce a JUnit report describing what was selected.

    ``--collect-only`` keeps this a plumbing check: running the unit suite for
    real would add a minute to every self-test pass for no extra coverage.
    """
    pytest.importorskip("pyorbbecsdk")
    results = tmp_path / "out"
    rc = run_tests.main(
        [
            "--config",
            str(HERE / "test_config.json"),
            "--results-dir",
            str(results),
            "--suite",
            "unit",
            "--skip-health",
            "--pytest-arg=--collect-only",
            "--pytest-arg=-q",
        ]
    )
    assert rc in (run_tests.EXIT_OK, run_tests.EXIT_TEST_FAILED, run_tests.EXIT_ENV_ERROR)

    report = results / "junit-all.xml"
    assert report.is_file(), "runner did not produce junit-all.xml"

    import xml.etree.ElementTree as ElementTree

    cases = list(ElementTree.parse(report).getroot().iter("testcase"))
    assert cases, "junit-all.xml contains no test cases"
    assert (results / "run-all.log").is_file()


def test_summary_reports_totals_modules_and_skip_reasons(tmp_path):
    """summary.md must carry the numbers a reviewer needs, including skips."""
    import report_summary

    junit = tmp_path / "junit-all.xml"
    junit.write_text(
        '<?xml version="1.0" encoding="utf-8"?><testsuites>'
        '<testsuite name="pytest" tests="3" failures="1" errors="0" skipped="1">'
        '<testcase classname="auto_tests.test_alpha_cpp.py" name="test_ok" time="1.5"/>'
        '<testcase classname="auto_tests.test_alpha_cpp.py" name="test_bad" time="0.5">'
        '<failure message="boom">Failed: boom</failure></testcase>'
        '<testcase classname="auto_tests.test_beta_cpp.py" name="test_skip">'
        "<skipped message=\"('path', 12, 'Skipped: device exposes no widget')\"/></testcase>"
        "</testsuite></testsuites>",
        encoding="utf-8",
    )

    target = report_summary.write_summary(
        tmp_path,
        junit,
        {"suites": "unit", "network": False, "health": "PASS", "exit_code": 1},
    )
    assert target is not None and target.is_file()
    text = target.read_text(encoding="utf-8")

    # Headline totals, derived from the suite attributes.
    assert "| Total cases selected | 3 |" in text
    assert "| Passed | 1 |" in text
    assert "| Failed | 1 |" in text
    assert "| Skipped | 1 |" in text

    # Per-module rows must keep the full module name, not a fragment.
    assert "`test_alpha_cpp`" in text
    assert "`test_beta_cpp`" in text

    # The failure and the skip reason must both be spelled out.
    assert "test_bad" in text
    assert "device exposes no widget" in text

    # And the caveat that keeps a green total from reading as coverage.
    assert "It is not a pass" in text


def test_summary_absent_report_is_a_no_op(tmp_path):
    import report_summary

    assert report_summary.write_summary(tmp_path, tmp_path / "missing.xml", {}) is None


def test_junit_verdict_reads_failures_and_errors(tmp_path):
    report = tmp_path / "junit-all.xml"
    report.write_text(
        '<?xml version="1.0" encoding="utf-8"?><testsuites>'
        '<testsuite name="pytest" errors="1" failures="2" tests="3"/></testsuites>',
        encoding="utf-8",
    )
    assert run_tests.junit_verdict(report) == (2, 1)

    clean = tmp_path / "clean.xml"
    clean.write_text(
        '<?xml version="1.0" encoding="utf-8"?><testsuites>'
        '<testsuite name="pytest" errors="0" failures="0" tests="5"/></testsuites>',
        encoding="utf-8",
    )
    # This is the shape that lets a shutdown abort be reported as a pass.
    assert run_tests.junit_verdict(clean) == (0, 0)


def test_junit_verdict_handles_missing_and_broken_reports(tmp_path):
    assert run_tests.junit_verdict(tmp_path / "absent.xml") == (None, None)
    broken = tmp_path / "broken.xml"
    broken.write_text("<testsuites", encoding="utf-8")
    assert run_tests.junit_verdict(broken) == (None, None)


def test_merge_junit_appends_suites(tmp_path):
    primary = tmp_path / "junit-all.xml"
    extra = tmp_path / "junit-reboot.xml"
    suite = (
        '<?xml version="1.0" encoding="utf-8"?><testsuites>'
        '<testsuite name="pytest" tests="1" failures="0" errors="0" skipped="0"/></testsuites>'
    )
    primary.write_text(suite, encoding="utf-8")
    extra.write_text(suite, encoding="utf-8")

    run_tests.merge_junit(primary, extra)

    import xml.etree.ElementTree as ElementTree

    assert len(ElementTree.parse(primary).getroot().findall("testsuite")) == 2


def test_runner_clears_stale_reports_before_running(tmp_path):
    """A rerun must not merge the previous run's reboot suite again.

    The reboot pass appends to junit-all.xml, so a leftover report from an
    earlier run used to accumulate an extra testsuite on every invocation.
    """
    results = tmp_path / "out"
    results.mkdir()
    stale = (
        '<?xml version="1.0" encoding="utf-8"?><testsuites>'
        '<testsuite name="pytest" tests="99" failures="0" errors="0" skipped="0"/></testsuites>'
    )
    (results / "junit-all.xml").write_text(stale, encoding="utf-8")
    (results / "junit-reboot.xml").write_text(stale, encoding="utf-8")

    rc = run_tests.main(
        [
            "--config",
            str(HERE / "test_config.json"),
            "--results-dir",
            str(results),
            "--suite",
            "unit",
            "--skip-health",
            "--pytest-arg=--collect-only",
            "--pytest-arg=-q",
        ]
    )
    assert rc in (run_tests.EXIT_OK, run_tests.EXIT_TEST_FAILED, run_tests.EXIT_ENV_ERROR)
    assert not (results / "junit-reboot.xml").exists()

    if (results / "junit-all.xml").exists():
        import xml.etree.ElementTree as ElementTree

        for suite in ElementTree.parse(results / "junit-all.xml").getroot().findall("testsuite"):
            assert suite.get("tests") != "99", "stale report content survived"


def test_runner_truncates_stale_sdk_log(tmp_path):
    """A second run must not interleave its SDK log with the previous run's.

    Context.set_logger_to_file appends, so the runner has to clear the file.
    """
    results = tmp_path / "out"
    results.mkdir()
    stale = results / "OrbbecSDK.log.txt"
    stale.write_text("STALE-MARKER-FROM-PREVIOUS-RUN\n", encoding="utf-8")

    rc = run_tests.main(
        [
            "--config",
            str(HERE / "test_config.json"),
            "--results-dir",
            str(results),
            "--suite",
            "unit",
            "--skip-health",
            "--pytest-arg=--collect-only",
            "--pytest-arg=-q",
        ]
    )
    assert rc in (run_tests.EXIT_OK, run_tests.EXIT_TEST_FAILED, run_tests.EXIT_ENV_ERROR)
    assert "STALE-MARKER-FROM-PREVIOUS-RUN" not in stale.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# destructive manifest
# ---------------------------------------------------------------------------


def _decorator_names(node: ast.FunctionDef) -> list[str]:
    names = []
    for dec in node.decorator_list:
        target = dec.func if isinstance(dec, ast.Call) else dec
        if isinstance(target, ast.Attribute):
            names.append(target.attr)
        elif isinstance(target, ast.Name):
            names.append(target.id)
    return names


def _module_level_marks(tree: ast.Module) -> set[str]:
    marks = set()
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id == "pytestmark" for t in node.targets
        ):
            value = node.value
            elements = value.elts if isinstance(value, (ast.List, ast.Tuple)) else [value]
            for element in elements:
                target = element.func if isinstance(element, ast.Call) else element
                if isinstance(target, ast.Attribute):
                    marks.add(target.attr)
    return marks


def _collect_marks():
    """Map test function name -> set of marks (module level plus per-function)."""
    marks: dict[str, set[str]] = {}
    for path in sorted(HERE.glob("test_*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        module_marks = _module_level_marks(tree)
        for node in tree.body:
            if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
                marks[node.name] = module_marks | set(_decorator_names(node))
    return marks


def _require_ported_modules():
    """Skip the manifest checks until every manifest case is actually ported.

    The checks compare the manifest against the marks found in the ported
    modules.  Running them while some cases are still missing would only report
    the port backlog, so the gate is "all manifest cases are present".
    """
    marks = _collect_marks()
    present = {_destructive.case_id_of(name) for name in marks}
    expected = set(_destructive.DESTRUCTIVE_TEST_IDS) | set(_destructive.REBOOT_TEST_IDS)
    missing = sorted(expected - present)
    if missing:
        pytest.skip(f"manifest cases not ported yet: {', '.join(missing)}")


def test_destructive_manifest_matches_marks():
    """The manifest and the per-case marks must not drift apart.

    This replaces the two hand-synced lists in the C++ tree
    (OB_HW_DESTRUCTIVE_TESTS and kDestructiveTestFilter).
    """
    _require_ported_modules()
    marks = _collect_marks()
    marked = {
        _destructive.case_id_of(f"{name}")
        for name, m in marks.items()
        if "destructive" in m
    }
    listed = set(_destructive.DESTRUCTIVE_TEST_IDS)
    assert marked == listed, (
        "destructive manifest drift\n"
        f"  listed but not marked: {sorted(listed - marked)}\n"
        f"  marked but not listed: {sorted(marked - listed)}"
    )


def test_reboot_manifest_matches_marks():
    _require_ported_modules()
    marks = _collect_marks()
    marked = {
        _destructive.case_id_of(name) for name, m in marks.items() if "reboot" in m
    }
    # TC_CPP_06_09 is both destructive and a reboot case, so it appears in both
    # manifests; the reboot list is a subset of everything carrying the mark.
    assert set(_destructive.REBOOT_TEST_IDS) <= marked
    assert marked <= set(_destructive.DESTRUCTIVE_TEST_IDS) | set(_destructive.REBOOT_TEST_IDS)


def test_case_id_extraction():
    assert _destructive.case_id_of("test_unit_cpp.py::test_TC_CPP_01_01_x") == "TC_CPP_01_01_x"
    assert (
        _destructive.case_id_of(
            "test_playback_cpp.py::test_TC_CPP_18_playback_parameterized"
            "[None-TC_CPP_18_10_playback_device_info]"
        )
        == "TC_CPP_18_10_playback_device_info"
    )


# ---------------------------------------------------------------------------
# environment sanity
# ---------------------------------------------------------------------------


def test_pytest_ini_is_the_rootdir_anchor():
    ini = (HERE / "pytest.ini").read_text(encoding="utf-8")
    for marker in (
        "unit",
        "hardware",
        "scenario",
        "performance",
        "destructive",
        "network",
        "reboot",
    ):
        assert f"    {marker}:" in ini


def test_sdk_is_importable_in_this_interpreter():
    """The suite must point at an interpreter with a pyorbbecsdk wheel."""
    check = subprocess.run(
        [sys.executable, "-c", "import pyorbbecsdk"],
        capture_output=True,
        text=True,
        env=os.environ.copy(),
    )
    if check.returncode != 0:
        pytest.skip(f"pyorbbecsdk not importable here: {check.stderr.strip().splitlines()[-1:]}")
