"""Fixtures matching tests/common/test_fixtures.hpp.

Reconstructed to the same public surface as the reference Python port:
session-scoped ``context``/``device``/``device_info``, an autouse
``hardware_identity_guard`` that mirrors the C++ TearDown check, a per-test
``pipeline`` fixture, and the shared helpers
``wait_for_frameset_with_retry`` / ``reboot_and_reconnect`` /
``open_test_device``.
"""

from __future__ import annotations

import json
import os
import signal
import sys
import threading
import time
from pathlib import Path

import pytest

ob = pytest.importorskip("pyorbbecsdk")

#: Set once the first Ctrl+C has been seen, so a second one escalates.
_CTRL_C_REQUESTED = threading.Event()
_PREVIOUS_SIGINT_HANDLER = None
_SDK_LOG_DIR: Path | None = None


def ctrl_c_requested() -> bool:
    """Return whether the test session received Ctrl+C."""
    return _CTRL_C_REQUESTED.is_set()


def pytest_sessionstart(session):
    """Record Ctrl+C before delegating to pytest's normal interrupt handling."""
    global _PREVIOUS_SIGINT_HANDLER, _SDK_LOG_DIR

    log_dir = os.getenv("OB_TEST_LOG_DIR")
    if log_dir:
        _SDK_LOG_DIR = Path(log_dir)
        _SDK_LOG_DIR.mkdir(parents=True, exist_ok=True)
        # Mirrors test_utils::setupTestLogger() -> ob::Context::setLoggerToFile.
        # These are *instance* methods in the pybind11 binding, not statics.
        ctx = ob.Context()
        ctx.set_logger_to_file(ob.OBLogLevel.DEBUG, str(_SDK_LOG_DIR))
        ob.Context.log_external_message(
            ob.OBLogLevel.INFO, "AUTO_TEST", "pytest session started", __file__, __name__, 0
        )

    def handle_sigint(signum, frame):
        if _CTRL_C_REQUESTED.is_set():
            # Second Ctrl+C: let Python abort the interpreter.
            signal.default_int_handler(signum, frame)
        _CTRL_C_REQUESTED.set()
        previous = _PREVIOUS_SIGINT_HANDLER
        if callable(previous):
            previous(signum, frame)
            return
        raise KeyboardInterrupt

    _PREVIOUS_SIGINT_HANDLER = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, handle_sigint)


#: nodeid -> {"outcome", "duration", "message"}, for the JUnit report.
_RECORDS: dict[str, dict] = {}
#: nodeids pytest selected, so unexecuted cases still appear in the report.
_SELECTED: list[str] = []
#: Crash-safety copy, refreshed after every case.
_FALLBACK_TARGET: Path | None = None
#: The path pytest itself was told to write (--junitxml).
_JUNIT_TARGET: Path | None = None


def pytest_collection_finish(session):
    """Remember what was selected, for cases that never reach a report."""
    global _SELECTED
    _SELECTED = [item.nodeid for item in getattr(session, "items", []) or []]


def pytest_configure(config):
    global _FALLBACK_TARGET, _JUNIT_TARGET
    for arg in getattr(config, "invocation_params", None).args or []:
        if isinstance(arg, str) and arg.startswith("--junitxml="):
            _JUNIT_TARGET = Path(arg.split("=", 1)[1])
            _FALLBACK_TARGET = _JUNIT_TARGET.with_name("junit-fallback.xml")
            break


def pytest_runtest_logreport(report):
    """Track each case's outcome and keep a rolling report on disk.

    pytest writes ``--junitxml`` only after the whole session finishes, and the
    SDK can wedge in shutdown before that - so when ``OB_TEST_HARD_EXIT`` is set
    the report must already exist.  Recording from the native reports (rather
    than re-parsing text) keeps pass/fail/**skip** and durations intact.
    """
    global _RECORDS
    if report.when == "call":
        # The call phase carries the real duration and verdict, so it replaces
        # whatever the setup phase provisionally recorded.
        _RECORDS[report.nodeid] = {
            "outcome": "failed" if report.failed else "skipped" if report.skipped else "passed",
            "duration": report.duration,
            "message": _report_message(report),
        }
    elif report.when == "setup":
        if report.failed:
            _RECORDS[report.nodeid] = {
                "outcome": "error",
                "duration": report.duration,
                "message": _report_message(report),
            }
        elif report.skipped:
            _RECORDS[report.nodeid] = {
                "outcome": "skipped",
                "duration": report.duration,
                "message": _report_message(report),
            }
        else:
            # Listed so the case appears even if it never reaches "call", but
            # keep setup's time too: with --collect-only the call phase never
            # happens and this is all the timing there is.
            _RECORDS.setdefault(
                report.nodeid,
                {"outcome": "passed", "duration": report.duration, "message": ""},
            )
    else:
        return

    _write_junit(_JUNIT_TARGET)
    _write_junit(_FALLBACK_TARGET)


def _report_message(report):
    """Best-effort longrepr text for a report."""
    try:
        text = str(report.longrepr) if report.longrepr is not None else ""
    except Exception:  # noqa: BLE001
        text = ""
    return text


def _write_junit(target):
    """Write a JUnit report from the recorded outcomes; never raises."""
    if target is None or not (_RECORDS or _SELECTED):
        return
    try:
        import xml.etree.ElementTree as ElementTree

        # Collected-but-unexecuted cases (a --collect-only run, or a case that
        # never started) are listed with an empty verdict so the report still
        # describes the selection instead of looking truncated.
        outcomes = [(nodeid, _RECORDS[nodeid]) for nodeid in _RECORDS]
        for nodeid in _SELECTED:
            if nodeid not in _RECORDS:
                outcomes.append((nodeid, {"outcome": "", "duration": 0.0, "message": ""}))

        counts = {"passed": 0, "skipped": 0, "failed": 0, "error": 0}
        for _, record in outcomes:
            counts[record["outcome"]] = counts.get(record["outcome"], 0) + 1

        suite = ElementTree.Element(
            "testsuite",
            {
                "name": "pytest",
                "tests": str(len(outcomes)),
                "failures": str(counts["failed"]),
                "errors": str(counts["error"]),
                "skipped": str(counts["skipped"]),
                "time": f"{sum(r['duration'] for _, r in outcomes):.3f}",
            },
        )
        for nodeid, record in outcomes:
            classname, _, name = nodeid.partition("::")
            node = ElementTree.SubElement(
                suite,
                "testcase",
                {
                    "classname": classname.replace("\\", ".").replace("/", "."),
                    "name": name,
                    "time": f"{record['duration']:.3f}",
                },
            )
            if record["outcome"] == "skipped":
                ElementTree.SubElement(node, "skipped", {"message": record["message"][:200]})
            elif record["outcome"] == "failed":
                failure = ElementTree.SubElement(node, "failure", {"message": record["message"][:200]})
                failure.text = record["message"]
            elif record["outcome"] == "error":
                error = ElementTree.SubElement(node, "error", {"message": record["message"][:200]})
                error.text = record["message"]

        root = ElementTree.Element("testsuites")
        root.append(suite)
        # Write beside the target and replace, so a reader never sees a partial
        # report (the runner may read it the moment the process dies).
        staging = target.with_suffix(target.suffix + ".part")
        ElementTree.ElementTree(root).write(staging, encoding="utf-8", xml_declaration=True)
        staging.replace(target)
    except Exception:  # noqa: BLE001 - never let reporting break the session
        pass


def pytest_sessionfinish(session, exitstatus):
    """Publish the verdict and, when asked, exit without SDK teardown.

    pytest normally writes ``--junitxml`` after every plugin has finished, and
    the SDK can wedge in interpreter shutdown before that happens - which cost
    minutes per module and left orphaned native threads holding the device.
    So when ``OB_TEST_HARD_EXIT=1`` the JUnit report is written here and the
    process leaves immediately with the right status, skipping the teardown that
    wedges.

    The env var is deliberately opt-in: unset it to get normal interpreter
    shutdown and full pytest reporting while debugging.
    """
    # Refresh the rolling crash-safety report, then publish the authoritative
    # one to the path pytest was asked for.
    _write_junit(_FALLBACK_TARGET)
    _write_junit(_JUNIT_TARGET)

    if os.getenv("OB_TEST_HARD_EXIT") == "1":
        try:
            sys.stdout.flush()
            sys.stderr.flush()
        except Exception:  # noqa: BLE001
            pass
        failed = bool(getattr(session, "testsfailed", 0)) or exitstatus not in (
            0,
            pytest.ExitCode.NO_TESTS_COLLECTED,
        )
        os._exit(1 if failed else 0)

    if _PREVIOUS_SIGINT_HANDLER is not None:
        signal.signal(signal.SIGINT, _PREVIOUS_SIGINT_HANDLER)


#: Per-case watchdog, in seconds; 0 disables it.  A wedged SDK call would
#: otherwise hang the whole run with no indication of the culprit, which is
#: exactly what a long hardware regression cannot afford.
_CASE_TIMEOUT_SECONDS = int(os.getenv("OB_TEST_CASE_TIMEOUT", "0"))


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_call(item):
    """Fail a case that exceeds ``OB_TEST_CASE_TIMEOUT`` seconds.

    ``signal.SIGALRM`` does not exist on Windows, so this uses a ``Timer``
    thread that raises into the main thread.  It cannot interrupt a wedged
    native call, but it does turn "the run stopped producing output" into a
    named failure, which is what matters for locating a hang.
    """
    if _CASE_TIMEOUT_SECONDS <= 0:
        yield
        return

    timed_out = threading.Event()

    def _on_timeout():
        timed_out.set()
        _thread.interrupt_main()

    timer = threading.Timer(_CASE_TIMEOUT_SECONDS, _on_timeout)
    timer.daemon = True
    timer.start()
    try:
        yield
    except KeyboardInterrupt:
        if timed_out.is_set():
            pytest.fail(f"case exceeded OB_TEST_CASE_TIMEOUT={_CASE_TIMEOUT_SECONDS}s")
        raise
    finally:
        timer.cancel()


def _load_config():
    path = Path(os.getenv("OB_TEST_CONFIG", "test_config.json"))
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


@pytest.fixture(scope="session")
def test_config():
    return _load_config()


@pytest.fixture(scope="session")
def context():
    ctx = ob.Context()
    ctx.set_logger_level(ob.OBLogLevel.WARNING)
    yield ctx
    del ctx


@pytest.fixture(scope="session")
def device(context, test_config):
    devices = context.query_devices()
    if devices is None or devices.get_count() == 0:
        pytest.skip("No connected device")

    serial = test_config.get("device", {}).get("serial", "")
    if serial:
        try:
            return devices.get_device_by_serial_number(serial)
        except Exception as exc:
            pytest.skip(f"Configured device is unavailable: {exc}")

    try:
        return devices.get_device_by_index(0)
    except Exception as exc:
        pytest.skip(f"Connected device cannot be opened: {exc}")


@pytest.fixture(scope="session")
def device_info(device):
    return device.get_device_info()


@pytest.fixture(autouse=True)
def hardware_identity_guard(request):
    """Fail when a case leaves the device PID/name changed (C++ TearDown rule)."""
    if "hardware" not in request.node.keywords:
        yield
        return

    # Cases that reboot on purpose cannot be checked against a stale handle.
    if "destructive" in request.node.keywords or "reboot" in request.node.keywords:
        yield
        return

    device = request.getfixturevalue("device")
    before = device.get_device_info()
    before_pid, before_name = before.get_pid(), before.get_name()
    yield
    after = device.get_device_info()
    assert after.get_pid() == before_pid
    assert after.get_name() == before_name


@pytest.fixture
def pipeline(device):
    pipe = ob.Pipeline(device)
    yield pipe
    try:
        pipe.stop()
    except Exception:
        pass


def first_profile(pipeline, sensor_type):
    return pipeline.get_stream_profile_list(sensor_type).get_default_video_stream_profile()


@pytest.fixture
def capture(pipeline, sensor_type=ob.OBSensorType.DEPTH_SENSOR, count=5, timeout=1000):
    """Poll ``count`` frames of ``sensor_type`` with a 10 s overall deadline."""
    config = ob.Config()
    config.enable_stream(first_profile(pipeline, sensor_type))
    pipeline.start(config)

    frame_type = {
        ob.OBSensorType.DEPTH_SENSOR: ob.OBFrameType.DEPTH_FRAME,
        ob.OBSensorType.COLOR_SENSOR: ob.OBFrameType.COLOR_FRAME,
        ob.OBSensorType.IR_SENSOR: ob.OBFrameType.IR_FRAME,
    }[sensor_type]
    result = []
    deadline = time.monotonic() + 10
    while len(result) < count and time.monotonic() < deadline:
        frame_set = pipeline.wait_for_frames(timeout)
        if frame_set is not None:
            frame = frame_set.get_frame_by_type(frame_type)
            if frame is not None:
                result.append(frame)
    return result


def wait_for_frameset_with_retry(pipeline, retries=15, timeout=1000):
    """Match tests/common/test_utils.hpp::waitForFramesetWithRetry."""
    for _ in range(retries):
        frameset = pipeline.wait_for_frames(timeout)
        if frameset is not None:
            return frameset
    return None


def require_destructive():
    if os.getenv("OB_ALLOW_DESTRUCTIVE") != "1":
        pytest.skip("Destructive test disabled; set OB_ALLOW_DESTRUCTIVE=1")


def has_method(class_or_obj, name):
    """Report whether a pybind11 class exposes a method.

    Resolved through ``getattr`` so static/class slots behave the same as
    instance methods: pybind11 turns a staticmethod slot into a plain function
    attribute, and a missing slot raises AttributeError.

    The set of available methods is *not* uniform across SDK builds (e.g.
    ``Frame.create_frame_from_buffer`` and ``Context.enable_multi_device_sync``
    exist only in some wheels), so cases that need one must skip rather than
    error out.
    """
    try:
        getattr(class_or_obj, name)
    except AttributeError:
        return False
    return True


def require_method(class_or_obj, name, reason=None):
    """Skip unless ``name`` exists on ``class_or_obj``."""
    if not has_method(class_or_obj, name):
        owner = getattr(class_or_obj, "__name__", class_or_obj)
        detail = reason or "not exposed by this pyorbbecsdk build"
        pytest.skip(f"{owner}.{name} {detail}")


#: Substrings that mean "this filter exists in the binding but its
#: implementation is not available in this build".
_FILTER_UNAVAILABLE_MARKERS = (
    "Private filter library not activated",
    "Private filter",
    "activated",
)


def make_filter(name, required=False):
    """Create a filter by name without risking a native crash.

    Extended filters are implemented in a private library.  In a build where
    that library is absent, ``FilterFactory.create_filter(name)`` raises a
    catchable error, while the concrete classes of the same name abort the
    process (STATUS_ACCESS_VIOLATION) when constructed - so instantiating
    ``SpatialAdvancedFilter()`` etc. directly must never be done unconditionally.

    Returns ``None`` when the filter is unavailable and ``required`` is false;
    skips when it is required.
    """
    try:
        return ob.FilterFactory.create_filter(name)
    except Exception as exc:  # noqa: BLE001
        text = str(exc)
        if any(marker in text for marker in _FILTER_UNAVAILABLE_MARKERS):
            if required:
                pytest.skip(f"{name} not available: {text}")
            return None
        raise


def open_test_device(ctx, test_config):
    devices = ctx.query_devices()
    if devices is None or devices.get_count() == 0:
        pytest.skip("No connected device")

    serial = test_config.get("device", {}).get("serial", "")
    try:
        if serial:
            return devices.get_device_by_serial_number(serial)
        return devices.get_device_by_index(0)
    except Exception as exc:
        pytest.skip(f"Configured device is unavailable: {exc}")


def reboot_and_reconnect(ctx, device, serial=None, timeout_seconds=90):
    """Match hw_test_helpers.hpp::rebootAndReconnect."""
    try:
        device.reboot()
    except Exception:
        pass
    del device

    time.sleep(2)
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        try:
            devices = ctx.query_devices()
            if devices is not None and devices.get_count() > 0:
                candidate = devices.get_device_by_serial_number(serial) if serial else devices.get_device_by_index(0)
                if candidate is not None and candidate.get_device_info() is not None:
                    return candidate
        except Exception:
            pass
        time.sleep(1)

    pytest.fail(f"Device {serial or '<first device>'} did not reconnect within {timeout_seconds} s")
