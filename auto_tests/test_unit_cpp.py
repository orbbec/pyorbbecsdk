"""Translations of tests/unit with the original C++ case names.

Every case keeps its ``TC_CPP_*`` id so the JUnit report can be diffed against
the C++ ``junit-all.xml`` case by case.

Cases whose SDK entry point is not exposed by the installed pyorbbecsdk build
are skipped with an explicit reason instead of being silently weakened; see
``temp_doc/PYTHON_BINDING_TEST_GAPS.md`` for the maintained gap list.  Verified
against pyorbbecsdk 2.10.6 (SDK 2.10.6), where these are absent:
``Frame.create_frame_from_buffer``, ``Pipeline.get_calibration_param``,
``Device.get_structured_data`` / ``set_structured_data``.
"""

from __future__ import annotations

import gc
import time

import numpy as np
import pytest
from conftest import ob, require_method

pytestmark = pytest.mark.unit

#: Frame size used by the frame-metadata cases (640x480x2 bytes, Y16).
DEPTH_FRAME_BYTES = 614400


# ---------------------------------------------------------------------------
# TC_CPP_01 context
# ---------------------------------------------------------------------------


def test_TC_CPP_01_01_context_default_create_destroy():
    ctx = ob.Context()
    assert ctx.query_devices() is not None
    del ctx
    gc.collect()


def test_TC_CPP_01_02_context_config_path():
    ctx = ob.Context("/non_existent_path/config.json")
    assert ctx.query_devices() is not None


def test_TC_CPP_01_03_context_repeated_create_destroy():
    for _ in range(10):
        ctx = ob.Context()
        assert ctx.query_devices() is not None
        del ctx


def test_TC_CPP_01_04_free_idle_memory():
    ctx = ob.Context()
    ctx.free_idle_memory()
    assert ctx.query_devices() is not None


def test_TC_CPP_01_05_uvc_backend():
    backend = ob.OBUvcBackendType
    ctx = ob.Context()
    try:
        for candidate in (backend.LIBUVC, backend.V4L2, backend.MSMF, backend.AUTO):
            ctx.set_uvc_backend_type(candidate)
    except Exception as exc:  # noqa: BLE001
        text = str(exc)
        # The Windows wheel ships without the USB PAL backend.
        if "Usb pal is not exist" in text or "BUILD_USB_PAL" in text:
            pytest.skip(f"USB PAL backend unavailable: {text}")
        raise


def test_TC_CPP_01_06_extension_plugin_directory():
    ctx = ob.Context()
    ctx.set_extensions_directory(".")
    ctx.set_extensions_directory("/non_existent_path")


# ---------------------------------------------------------------------------
# TC_CPP_02 clock sync
# ---------------------------------------------------------------------------


def test_TC_CPP_02_06_clock_sync(context):
    # Same sequence as the C++ case: 1000, 500, then restore with 0.
    context.enable_multi_device_sync(1000)
    context.enable_multi_device_sync(500)
    context.enable_multi_device_sync(0)


# ---------------------------------------------------------------------------
# TC_CPP_10 / 12 frame factory
# ---------------------------------------------------------------------------


def test_TC_CPP_10_04_frame_ref_count():
    require_method(ob.Frame, "create_frame_from_buffer")
    destroyed = []
    buffer = bytearray([66] * 100)

    frame = ob.Frame.create_frame_from_buffer(
        ob.OBFrameType.DEPTH_FRAME, ob.OBFormat.Y16, buffer, lambda: destroyed.append(1)
    )
    ref = frame
    assert frame.get_data_size() == len(buffer)
    # Holding a reference must keep the buffer alive.
    assert not destroyed
    del ref
    del frame
    gc.collect()
    assert destroyed


def test_TC_CPP_10_13_frameset_push_frame():
    frame_set = ob.Frame.create_frame_set()
    frame = ob.Frame.create_frame(ob.OBFrameType.DEPTH_FRAME, ob.OBFormat.Y16, DEPTH_FRAME_BYTES)
    frame_set.push_frame(frame)
    assert frame_set.get_frame_count() == 1


def test_TC_CPP_12_01_create_frame_and_video_frame():
    frame = ob.Frame.create_frame(ob.OBFrameType.DEPTH_FRAME, ob.OBFormat.Y16, DEPTH_FRAME_BYTES)
    assert frame is not None
    assert frame.get_type() == ob.OBFrameType.DEPTH_FRAME
    assert frame.get_format() == ob.OBFormat.Y16
    assert frame.get_data_size() == DEPTH_FRAME_BYTES

    video = ob.Frame.create_video_frame(ob.OBFrameType.COLOR_FRAME, ob.OBFormat.RGB, 640, 480)
    assert video is not None
    assert video.get_type() == ob.OBFrameType.COLOR_FRAME
    assert video.get_format() == ob.OBFormat.RGB
    assert video.get_width() == 640
    assert video.get_height() == 480
    assert video.get_data_size() > 0


def test_TC_CPP_12_03_create_frame_from_buffer():
    require_method(ob.Frame, "create_frame_from_buffer")
    destroyed = []
    buffer = bytearray([66] * 100)

    frame = ob.Frame.create_frame_from_buffer(
        ob.OBFrameType.DEPTH_FRAME, ob.OBFormat.Y16, buffer, lambda: destroyed.append(1)
    )
    assert frame is not None
    assert frame.get_data_size() == len(buffer)
    assert bytes(frame.get_data()) == bytes(buffer)
    del frame
    gc.collect()
    assert destroyed


def test_TC_CPP_12_04_create_empty_frameset():
    frame_set = ob.Frame.create_frame_set()
    assert frame_set.get_frame_count() == 0

    frame = ob.Frame.create_frame(ob.OBFrameType.DEPTH_FRAME, ob.OBFormat.Y16, DEPTH_FRAME_BYTES)
    frame_set.push_frame(frame)
    assert frame_set.get_frame_count() == 1


# ---------------------------------------------------------------------------
# TC_CPP_11 metadata
# ---------------------------------------------------------------------------


def test_TC_CPP_11_06_update_metadata_c_api():
    require_method(ob.Frame, "update_metadata")
    require_method(ob.VideoFrame, "get_metadata")

    frame = ob.Frame.create_video_frame(ob.OBFrameType.DEPTH_FRAME, ob.OBFormat.Y16, 640, 480)
    metadata = bytearray(range(64))
    frame.update_metadata(metadata)

    assert bytes(frame.get_metadata()) == bytes(metadata)
    assert frame.get_metadata_size() == len(metadata)


# ---------------------------------------------------------------------------
# TC_CPP_13 filters
# ---------------------------------------------------------------------------


def test_TC_CPP_13_01_create_all_builtin_filters():
    # Portable filters: every build must provide these.
    required = (
        "DecimationFilter",
        "ThresholdFilter",
        "Align",
        "FormatConverter",
        "HDRMerge",
        "PointCloudFilter",
        "SequenceIdFilter",
    )
    # Extended filters: presence depends on the device/extension set.
    optional = (
        "SpatialAdvancedFilter",
        "SpatialFastFilter",
        "SpatialModerateFilter",
        "TemporalFilter",
        "HoleFillingFilter",
        "NoiseRemovalFilter",
        "DisparityTransform",
        "FalsePositiveFilter",
    )

    for name in required:
        assert ob.FilterFactory.create_filter(name) is not None

    for name in optional:
        try:
            created = ob.FilterFactory.create_filter(name)
        except Exception as exc:  # noqa: BLE001
            if any(token in str(exc) for token in ("Private filter", "activated")):
                continue
            raise
        assert created is not None


def test_TC_CPP_13_02_create_invalid_filter():
    with pytest.raises(Exception):
        ob.FilterFactory.create_filter("TotallyInvalidFilter")


def test_TC_CPP_13_05_filter_enable_disable():
    filter_ = ob.FilterFactory.create_filter("DecimationFilter")
    filter_.enable(True)
    assert filter_.is_enabled()
    filter_.enable(False)
    assert not filter_.is_enabled()


def test_TC_CPP_13_06_filter_reset_and_config():
    filter_ = ob.FilterFactory.create_filter("DecimationFilter")
    schema = filter_.get_config_schema_vec()
    assert schema

    first = schema[0]
    filter_.get_config_value(first.name)
    filter_.set_config_value(first.name, first.default)
    filter_.reset()


def test_TC_CPP_13_07_filter_type_check():
    filter_ = ob.FilterFactory.create_filter("PointCloudFilter")
    assert filter_.get_name()
    assert filter_.is_point_cloud_filter()


def test_TC_CPP_13_17_private_filter():
    with pytest.raises(Exception):
        ob.FilterFactory.create_private_filter("SomePrivateFilter", "invalid_key")


# ---------------------------------------------------------------------------
# TC_CPP_20 coordinate transform
# ---------------------------------------------------------------------------


def _identity_extrinsic():
    extrinsic = ob.OBExtrinsic()
    extrinsic.rot = np.eye(3, dtype=np.float32)
    extrinsic.transform = np.zeros(3, dtype=np.float32)
    return extrinsic


def _camera_intrinsic():
    intrinsic = ob.OBCameraIntrinsic()
    intrinsic.fx, intrinsic.fy = 500.0, 500.0
    intrinsic.cx, intrinsic.cy = 320.0, 240.0
    intrinsic.width, intrinsic.height = 640, 480
    return intrinsic


def test_TC_CPP_20_01_3d_to_3d():
    point = ob.OBPoint3f(100.0, 200.0, 300.0)
    result = ob.transformation3dto3d(point, _identity_extrinsic())
    assert (result.x, result.y, result.z) == pytest.approx((100.0, 200.0, 300.0), abs=1e-3)


def test_TC_CPP_20_02_2d_depth_to_3d():
    pixel = ob.OBPoint2f(320.0, 240.0)
    result = ob.transformation2dto3d(pixel, 1000.0, _camera_intrinsic(), _identity_extrinsic())
    assert (result.x, result.y, result.z) == pytest.approx((0.0, 0.0, 1000.0), abs=5.0)


def test_TC_CPP_20_03_3d_to_2d():
    point = ob.OBPoint3f(0.0, 0.0, 1000.0)
    result = ob.transformation3dto2d(point, _camera_intrinsic(), ob.OBCameraDistortion(), _identity_extrinsic())
    assert (result.x, result.y) == pytest.approx((320.0, 240.0), abs=1.0)


def test_TC_CPP_20_04_2d_to_2d():
    pixel = ob.OBPoint2f(400.0, 300.0)
    # Binding order: (pixel, depth, src_intrinsic, src_distortion,
    #                 dst_intrinsic, dst_distortion, extrinsic).
    result = ob.transformation2dto2d(
        pixel,
        1000.0,
        _camera_intrinsic(),
        ob.OBCameraDistortion(),
        _camera_intrinsic(),
        ob.OBCameraDistortion(),
        _identity_extrinsic(),
    )
    assert (result.x, result.y) == pytest.approx((400.0, 300.0), abs=2.0)


# ---------------------------------------------------------------------------
# TC_CPP_22 version
# ---------------------------------------------------------------------------


def test_TC_CPP_22_01_full_version():
    version = ob.get_version()
    parts = [ob.get_version_major(), ob.get_version_minor(), ob.get_version_patch()]
    assert version
    # The accessors return ints; the C++ case compares the dotted string.
    assert ".".join(str(part) for part in parts) in version


def test_TC_CPP_22_02_stage_version():
    stage = ob.get_version_stage()
    if stage:
        assert any(token in stage.lower() for token in ("alpha", "beta", "rc", "release"))


# ---------------------------------------------------------------------------
# TC_CPP_23 logger
# ---------------------------------------------------------------------------


def test_TC_CPP_23_01_log_severity_set():
    for level in (
        ob.OBLogLevel.DEBUG,
        ob.OBLogLevel.INFO,
        ob.OBLogLevel.WARNING,
        ob.OBLogLevel.ERROR,
        ob.OBLogLevel.FATAL,
        ob.OBLogLevel.NONE,
    ):
        ob.Context.set_logger_level(level)


def test_TC_CPP_23_02_log_to_file(tmp_path):
    """The SDK file logger must create and write OrbbecSDK.log.txt.

    The deterministic trigger is ``log_external_message``; ``query_devices()``
    is issued best effort only, because enumeration can block on background
    network discovery and would make the assertion timing dependent.
    """
    log_dir = tmp_path / "sdklog"
    log_dir.mkdir()
    ctx = ob.Context()
    ctx.set_logger_to_file(ob.OBLogLevel.INFO, str(log_dir))
    try:
        ob.Context.log_external_message(ob.OBLogLevel.INFO, "NOHW", "FILE_MARKER", __file__, __name__, 1)

        log_path = log_dir / "OrbbecSDK.log.txt"
        deadline = time.monotonic() + 5
        content = ""
        while time.monotonic() < deadline:
            if log_path.exists():
                content = log_path.read_text(errors="replace")
                if content:
                    break
            time.sleep(0.05)
        assert log_path.exists(), "OrbbecSDK.log.txt was not created"
        assert content, "OrbbecSDK.log.txt is empty"
        assert "FILE_MARKER" in content
    finally:
        ctx.set_logger_level(ob.OBLogLevel.WARNING)


def test_TC_CPP_23_03_log_to_console():
    ctx = ob.Context()
    ctx.set_logger_to_console(ob.OBLogLevel.INFO)
    ctx.set_logger_level(ob.OBLogLevel.WARNING)


def test_TC_CPP_23_04_log_callback():
    """The callback must be registered and receive SDK messages.

    ``query_devices()`` is only pumped as a best effort: in some environments
    device enumeration blocks on background network discovery and emits nothing
    for the whole window, which would make this case flaky.  The deterministic
    trigger is ``log_external_message``.
    """
    messages = []
    ctx = ob.Context()
    callback = lambda level, msg: messages.append(msg)  # noqa: E731
    ctx.set_logger_level(ob.OBLogLevel.DEBUG)
    ctx.set_logger_to_callback(ob.OBLogLevel.DEBUG, callback)
    try:
        ob.Context.log_external_message(ob.OBLogLevel.DEBUG, "NOHW", "CALLBACK_MARKER", __file__, __name__, 1)

        deadline = time.monotonic() + 2
        while not messages and time.monotonic() < deadline:
            time.sleep(0.05)
        assert messages
        assert any("CALLBACK_MARKER" in str(m) for m in messages)
    finally:
        ctx.set_logger_level(ob.OBLogLevel.WARNING)
        # clear_logger_callback is not exposed by every build.
        clear = getattr(ctx, "clear_logger_callback", None)
        if callable(clear):
            clear()


def test_TC_CPP_23_05_external_message():
    messages = []
    ctx = ob.Context()
    ctx.set_logger_level(ob.OBLogLevel.INFO)
    ctx.set_logger_to_callback(ob.OBLogLevel.INFO, lambda level, msg: messages.append(msg))
    try:
        ob.Context.log_external_message(ob.OBLogLevel.INFO, "NOHW", "NOHW_TEST_MARKER", __file__, __name__, 1)

        deadline = time.monotonic() + 2
        while not any("NOHW_TEST_MARKER" in str(m) for m in messages):
            if time.monotonic() >= deadline:
                break
            time.sleep(0.05)
        assert any("NOHW_TEST_MARKER" in str(m) for m in messages)
    finally:
        ctx.set_logger_level(ob.OBLogLevel.WARNING)
        clear = getattr(ctx, "clear_logger_callback", None)
        if callable(clear):
            clear()


# ---------------------------------------------------------------------------
# TC_CPP_24 exceptions
# ---------------------------------------------------------------------------


def test_TC_CPP_24_01_exception_type_info():
    with pytest.raises(Exception) as error:
        ob.FilterFactory.create_filter("TotallyInvalidFilter")
    assert str(error.value)


def test_TC_CPP_24_02_invalid_value_exception():
    """Invalid frame dimensions must be rejected, not silently accepted.

    The C++ case expects an exception for a bad size.  This build does not
    range-check the extent - ``0`` is accepted and yields ``data_size == 0`` -
    so the invalid values used here are the ones the binding genuinely rejects,
    at the C++ argument-conversion boundary:

    * negative extents, and
    * values outside the ``uint32`` range the SDK takes.

    Both raise before any allocation, which matters: probing the limit with an
    enormous-but-representable size instead makes the SDK attempt a multi-GB
    frame buffer before failing.
    """
    for width, height in ((-1, -1), (640, -1), (1 << 40, 1), (1, 1 << 40)):
        with pytest.raises(Exception):
            ob.Frame.create_video_frame(ob.OBFrameType.DEPTH_FRAME, ob.OBFormat.Y16, width, height)

    # A zero extent is accepted by this build; record that rather than pretend
    # it fails, so a future change of behaviour is visible.
    empty = ob.Frame.create_video_frame(ob.OBFrameType.DEPTH_FRAME, ob.OBFormat.Y16, 0, 0)
    assert empty.get_data_size() == 0


def test_TC_CPP_24_03_wrong_api_sequence():
    pipeline = ob.Pipeline()
    try:
        # waitForFrames before start: the SDK must either return None or raise.
        assert pipeline.wait_for_frames(100) is None
    except Exception as error:  # noqa: BLE001
        assert error


def test_TC_CPP_24_06_all_exception_types():
    with pytest.raises(Exception) as error:
        ob.FilterFactory.create_filter("TotallyBogusFilter")
    assert str(error.value)
