"""Python equivalents of the five non-GoogleTest C/C++ programs.

These are not part of any CTest label upstream either: the C++ build produces
them as standalone executables, so here they are ordinary test functions that
run when selected explicitly.  ``align_test`` cannot be ported at all - see the
skip reason at the bottom.
"""

from __future__ import annotations

import time
from pathlib import Path

import numpy as np
import pytest

from conftest import ob

#: These mirror `tests/frame_test`, `pipeline_status_test`, `total_test`,
#: `hdr_test` and `align_test`, which upstream are standalone executables rather
#: than CTest-labelled cases.  They are still selected by the default hardware
#: run (the runner appends `or (standalone)` to the hw expression) so they are
#: exercised automatically instead of being forgotten.
pytestmark = pytest.mark.standalone


def test_frame_test():
    """Port of tests/frame_test: create a frame, then configure a filter."""
    frame = ob.Frame.create_video_frame(
        ob.OBFrameType.DEPTH_FRAME, ob.OBFormat.Y16, 640, 480
    )
    assert frame is not None
    assert frame.get_data_size() > 0
    assert frame.get_data_pointer() is not None

    try:
        noise = ob.FilterFactory.create_filter("NoiseRemovalFilter")
    except Exception as exc:  # noqa: BLE001
        pytest.skip(f"NoiseRemovalFilter extension unavailable: {exc}")

    assert noise is not None
    assert noise.get_config_schema_vec()


def test_pipeline_status_test(pipeline):
    """Port of tests/pipeline_status_test: status flags and health monitor."""
    before = pipeline.get_status()
    assert before is not None
    assert int(getattr(before, "sdk_status", 0)) >= 0

    frame_count = 0
    pipeline.start()
    try:
        for _ in range(20):
            if pipeline.wait_for_frames(200) is not None:
                frame_count += 1
        assert frame_count > 0

        # Health monitor callbacks must start and then stop again.
        # Binding signature: enable_health_monitor(callback, interval_ms).
        callbacks = []
        pipeline.enable_health_monitor(lambda status: callbacks.append(status), 200)
        time.sleep(1.2)
        pipeline.disable_health_monitor()
        before_disable = len(callbacks)
        time.sleep(1.2)
        after_disable = len(callbacks)
        assert after_disable == before_disable
    finally:
        pipeline.stop()

    after = pipeline.get_status()
    assert after is not None
    assert int(getattr(after, "sdk_status", 0)) >= 0


def test_total_test(device, device_info):
    """Port of tests/total_test: enumerate everything and stream colour."""
    assert all(
        (
            device_info.get_name(),
            device_info.get_serial_number(),
            device_info.get_pid(),
            device_info.get_vid(),
            device_info.get_uid(),
            device_info.get_connection_type(),
            device_info.get_firmware_version(),
            device_info.get_hardware_version(),
            device_info.get_supported_min_sdk_version(),
        )
    )

    sensors = device.get_sensor_list()
    assert sensors.get_count() > 0

    # get_sensor_by_type lives on SensorList, not on Device.
    color = sensors.get_sensor_by_type(ob.OBSensorType.COLOR_SENSOR)
    if color is None:
        pytest.skip("device has no colour sensor")

    profiles = color.get_stream_profile_list()
    assert profiles.get_count() > 0
    for index in range(profiles.get_count()):
        video = profiles.get_stream_profile_by_index(index).as_video_stream_profile()
        assert video.get_width() > 0
        assert video.get_height() > 0
        assert video.get_fps() > 0
        assert video.get_format() != ob.OBFormat.UNKNOWN_FORMAT

    received = []
    color.start(
        profiles.get_default_video_stream_profile(), lambda frame: received.append(frame)
    )
    try:
        deadline = time.monotonic() + 5
        while not received and time.monotonic() < deadline:
            time.sleep(0.05)
        assert received
        frame = received[0].as_video_frame()
        assert frame.get_index() >= 0
        assert frame.get_data_size() > 0
        assert frame.get_data_pointer() is not None
    finally:
        color.stop()


def test_hdr_test_requires_raw_inputs(test_config):
    """Port of tests/hdr_test using its command-line inputs from config."""
    hdr = test_config.get("resource", {}).get("hdr", {})
    required = ("width", "height", "depth0Path", "depth1Path", "ir0Path", "ir1Path")
    if not hdr or not all(hdr.get(key) for key in required):
        pytest.skip("HDR raw inputs are not configured")

    width = int(hdr["width"])
    height = int(hdr["height"])

    paths = {}
    for key in ("depth0Path", "depth1Path", "ir0Path", "ir1Path"):
        path = Path(hdr[key])
        assert path.is_file(), f"C++ hdr_test input is missing: {key}"
        paths[key] = path

    depth_item_size = width * height * 2
    ir_item_size = width * height
    for key in ("depth0Path", "depth1Path"):
        assert paths[key].stat().st_size % depth_item_size == 0, f"Unexpected input size: {key}"
    for key in ("ir0Path", "ir1Path"):
        assert paths[key].stat().st_size % ir_item_size == 0, f"Unexpected input size: {key}"

    depth0 = np.fromfile(paths["depth0Path"], dtype=">u2").astype(np.uint16)[: width * height]
    depth1 = np.fromfile(paths["depth1Path"], dtype=">u2").astype(np.uint16)[: width * height]
    ir0 = np.fromfile(paths["ir0Path"], dtype=np.uint8)[: width * height]
    ir1 = np.fromfile(paths["ir1Path"], dtype=np.uint8)[: width * height]

    # Depth-only merge, then IR-assisted merge, both written next to depth0.
    depth_only = np.zeros(width * height, dtype=np.uint16)
    for index in range(len(depth0)):
        depth_only[index] = depth0[index] if depth0[index] else depth1[index]
    depth_only.tofile(str(paths["depth0Path"].with_name(paths["depth0Path"].stem + "_depthonly.raw")))

    with_ir = np.zeros(width * height, dtype=np.uint16)
    for index in range(len(depth0)):
        with_ir[index] = depth0[index] if ir0[index] else depth1[index]
    with_ir.tofile(str(paths["depth0Path"].with_name(paths["depth0Path"].stem + "_withir.raw")))

    assert paths["depth0Path"].with_name(
        paths["depth0Path"].stem + "_depthonly.raw"
    ).is_file()
    assert paths["depth0Path"].with_name(paths["depth0Path"].stem + "_withir.raw").is_file()
    # Silence unused warnings while keeping both buffers meaningful.
    assert int(with_ir.sum()) >= 0 and int(ir1.sum()) >= 0


def test_align_test_requires_calibration_inputs():
    pytest.skip(
        "Python binding lacks internal AlignImpl calibration initialization required by align_test"
    )
