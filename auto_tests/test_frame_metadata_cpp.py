"""Direct translations of TC_CPP_10 through TC_CPP_12 hardware cases.

The ``TEST_P`` IMU cases (``10_09``/``10_10``) are one parametrised function
with the original case ids as parameter ids, so the JUnit names stay diffable
against the C++ report.
"""

from __future__ import annotations

import time

import numpy as np
import pytest
from conftest import first_profile, make_filter, ob, wait_for_frameset_with_retry

pytestmark = pytest.mark.hardware


def _capture(device, sensor_type=ob.OBSensorType.DEPTH_SENSOR, count=5, timeout=1000):
    """Collect up to ``count`` frames of ``sensor_type``; returns (frames, framesets).

    Frames are converted to their concrete subclass, because the type-specific
    accessors (``get_depth_scale``, ``get_metadata_size``, ``get_x`` ...) live
    on ``DepthFrame`` / ``VideoFrame`` / ``AccelFrame``, not on ``Frame``.
    ``get_frame_by_type`` hands out the base ``Frame`` view.
    """
    pipeline = ob.Pipeline(device)
    try:
        config = ob.Config()
        config.enable_stream(first_profile(pipeline, sensor_type))
        pipeline.start(config)

        frames = []
        framesets = []
        for _ in range(count):
            frameset = pipeline.wait_for_frames(timeout)
            if frameset is None:
                frameset = wait_for_frameset_with_retry(pipeline)
            if frameset is not None:
                framesets.append(frameset)
                frame = _typed_frame(frameset, sensor_type)
                if frame is not None:
                    frames.append(frame)
        return frames, framesets
    finally:
        try:
            pipeline.stop()
        except Exception:
            pass


def _typed_frame(frameset, sensor_type):
    """Return the concrete frame subclass for ``sensor_type``, or None."""
    if sensor_type == ob.OBSensorType.DEPTH_SENSOR:
        return frameset.get_depth_frame()
    if sensor_type == ob.OBSensorType.COLOR_SENSOR:
        return frameset.get_color_frame()
    if sensor_type == ob.OBSensorType.IR_SENSOR:
        return frameset.get_ir_frame()
    if sensor_type == ob.OBSensorType.ACCEL_SENSOR:
        return frameset.get_accel_frame()
    if sensor_type == ob.OBSensorType.GYRO_SENSOR:
        return frameset.get_gyro_frame()
    frame = frameset.get_frame_by_type(_frame_type(sensor_type))
    return frame


def _frame_type(sensor_type):
    return {
        ob.OBSensorType.DEPTH_SENSOR: ob.OBFrameType.DEPTH_FRAME,
        ob.OBSensorType.COLOR_SENSOR: ob.OBFrameType.COLOR_FRAME,
        ob.OBSensorType.IR_SENSOR: ob.OBFrameType.IR_FRAME,
        ob.OBSensorType.ACCEL_SENSOR: ob.OBFrameType.ACCEL_FRAME,
        ob.OBSensorType.GYRO_SENSOR: ob.OBFrameType.GYRO_FRAME,
    }[sensor_type]


# ---------------------------------------------------------------------------
# TC_CPP_10 frame properties
# ---------------------------------------------------------------------------


def test_TC_CPP_10_01_frame_basic_properties(device):
    frames, _ = _capture(device, ob.OBSensorType.DEPTH_SENSOR)
    assert frames
    depth = frames[0]

    assert depth.get_type() == ob.OBFrameType.DEPTH_FRAME
    assert depth.get_format() != ob.OBFormat.UNKNOWN_FORMAT
    assert depth.get_data_pointer() is not None
    assert depth.get_data_size() > 0
    assert depth.get_index() >= 0


def test_TC_CPP_10_02_timestamp_monotonicity(device):
    pipeline = ob.Pipeline(device)
    try:
        config = ob.Config()
        config.enable_stream(first_profile(pipeline, ob.OBSensorType.DEPTH_SENSOR))
        pipeline.start(config)

        stamps = []
        for _ in range(5):
            frameset = pipeline.wait_for_frames(1000)
            if frameset is not None and frameset.get_depth_frame() is not None:
                stamps.append(frameset.get_depth_frame().get_system_timestamp_us())
    finally:
        try:
            pipeline.stop()
        except Exception:
            pass

    assert stamps
    assert stamps == sorted(stamps)


def test_TC_CPP_10_03_frame_associated_info(device):
    frames, _ = _capture(device, ob.OBSensorType.DEPTH_SENSOR)
    assert frames
    depth = frames[0]

    assert depth.get_stream_profile() is not None
    assert depth.get_sensor() is not None
    assert depth.get_device() is not None


def test_TC_CPP_10_05_video_frame_properties(device):
    frames, _ = _capture(device, ob.OBSensorType.DEPTH_SENSOR)
    assert frames
    video = frames[0].as_video_frame()

    assert video.get_width() > 0
    assert video.get_height() > 0
    assert video.get_pixel_available_bit_size() > 0


def test_TC_CPP_10_06_depth_frame_scale(device):
    scale = None
    values = []
    for _ in range(5):
        frames, _ = _capture(device, ob.OBSensorType.DEPTH_SENSOR, count=1)
        if not frames:
            continue
        depth = frames[0]
        scale = depth.get_depth_scale()
        data = np.frombuffer(depth.get_data(), dtype="<u2")
        if data.size:
            values = [float(v) for v in data[:16]]
            break

    assert scale
    assert values
    assert all(value >= 0.0 for value in values)
    # millimetres; the C++ case tolerates a small non-zero scale.
    assert scale > 0.01


def test_TC_CPP_10_07_color_ir_data_valid(device):
    frames, _ = _capture(device, ob.OBSensorType.COLOR_SENSOR)
    if not frames:
        frames, _ = _capture(device, ob.OBSensorType.IR_SENSOR)
    assert frames, "no color or IR frames"

    for frame in frames:
        data = frame.get_data()
        assert frame.as_video_frame() is not None
        assert np.any(np.frombuffer(data, dtype=np.uint8)), "Frame is all zeros"


def test_TC_CPP_10_08_points_frame(device):
    frames, _ = _capture(device, ob.OBSensorType.DEPTH_SENSOR)
    assert frames

    if make_filter("PointCloudFilter") is None:
        pytest.skip("PointCloudFilter not available")
    cloud = ob.FilterFactory.create_filter("PointCloudFilter")

    result = cloud.process(frames[0])
    assert result is not None
    points = result.as_points_frame()
    assert points is not None
    assert points.get_position_value_scale() > 0.0


@pytest.mark.parametrize(
    "sensor_type,frame_method",
    [
        (ob.OBSensorType.ACCEL_SENSOR, "as_accel_frame"),
        (ob.OBSensorType.GYRO_SENSOR, "as_gyro_frame"),
    ],
    ids=["TC_CPP_10_09_accel_frame", "TC_CPP_10_10_gyro_frame"],
)
def test_TC_CPP_10_imu_frames(device, sensor_type, frame_method):
    try:
        sensor = device.get_sensor(sensor_type)
    except Exception:  # noqa: BLE001
        pytest.skip(f"No {sensor_type.name.lower()} sensor")
    assert sensor is not None

    profiles = sensor.get_stream_profile_list()
    if profiles is None or profiles.get_count() == 0:
        pytest.skip("No IMU profiles available")

    pipeline = ob.Pipeline(device)
    try:
        config = ob.Config()
        config.enable_stream(profiles.get_stream_profile_by_index(0))
        pipeline.start(config)

        received = []
        deadline = time.monotonic() + 5
        while not received and time.monotonic() < deadline:
            frameset = pipeline.wait_for_frames(1000)
            if frameset is not None:
                frame = (
                    frameset.get_accel_frame()
                    if sensor_type == ob.OBSensorType.ACCEL_SENSOR
                    else frameset.get_gyro_frame()
                )
                if frame is not None:
                    received.append(frame)
            time.sleep(0.05)
    finally:
        try:
            pipeline.stop()
        except Exception:
            pass

    assert received, "No IMU frame received"
    frame = received[0]
    magnitude = (frame.get_x() ** 2 + frame.get_y() ** 2 + frame.get_z() ** 2) ** 0.5

    if sensor_type == ob.OBSensorType.ACCEL_SENSOR:
        assert magnitude == pytest.approx(9.8, abs=4.0)
    else:
        assert magnitude == pytest.approx(0.0, abs=80.0)
    assert frame.get_temperature() >= 0.0


def test_TC_CPP_10_11_frameset_count_extract(device):
    frames, framesets = _capture(device, ob.OBSensorType.DEPTH_SENSOR)
    assert framesets
    frameset = framesets[0]

    assert frameset.get_count() >= 1
    assert frameset.get_depth_frame() is not None or frameset.get_color_frame() is not None


def test_TC_CPP_10_12_frameset_by_type_index(device):
    frames, framesets = _capture(device, ob.OBSensorType.DEPTH_SENSOR)
    assert framesets
    frameset = framesets[0]

    assert frameset.get_frame(ob.OBFrameType.DEPTH_FRAME) is not None
    for index in range(frameset.get_count()):
        frame = frameset.get_frame_by_index(index)
        assert frame is not None
        assert frame.get_type() != ob.OBFrameType.UNKNOWN_FRAME


def test_TC_CPP_10_14_frameset_sync(device):
    try:
        if device.get_sensor(ob.OBSensorType.COLOR_SENSOR) is None:
            pytest.skip("Current device has no color sensor")
    except Exception:  # noqa: BLE001
        pytest.skip("Current device has no color sensor")

    pipeline = ob.Pipeline(device)
    try:
        pipeline.enable_frame_sync()
        frames, _ = _capture(device, ob.OBSensorType.DEPTH_SENSOR)
        assert frames
    finally:
        try:
            pipeline.disable_frame_sync()
        except Exception:
            pass


# ---------------------------------------------------------------------------
# TC_CPP_11 metadata
# ---------------------------------------------------------------------------


def _depth_frame(device):
    frames, _ = _capture(device, ob.OBSensorType.DEPTH_SENSOR)
    assert frames, "no depth frames"
    return frames[0]


def test_TC_CPP_11_01_metadata_basic_read(device):
    depth = _depth_frame(device)
    assert depth.has_metadata(ob.OBFrameMetadataType.TIMESTAMP)
    assert depth.get_metadata_value(ob.OBFrameMetadataType.TIMESTAMP) >= 0


def test_TC_CPP_11_02_frame_number_fps(device):
    pipeline = ob.Pipeline(device)
    try:
        config = ob.Config()
        config.enable_stream(first_profile(pipeline, ob.OBSensorType.DEPTH_SENSOR))
        pipeline.start(config)

        numbers = []
        last = None
        for _ in range(10):
            frameset = pipeline.wait_for_frames(1000)
            if frameset is None or frameset.get_depth_frame() is None:
                continue
            depth = frameset.get_depth_frame()
            if depth.has_metadata(ob.OBFrameMetadataType.FRAME_NUMBER):
                value = depth.get_metadata_value(ob.OBFrameMetadataType.FRAME_NUMBER)
                if last is None or value != last:
                    numbers.append(value)
                last = value
    finally:
        try:
            pipeline.stop()
        except Exception:
            pass

    if len(numbers) >= 2:
        assert numbers == sorted(numbers)


def test_TC_CPP_11_03_exposure_gain_laser(device):
    for _ in range(5):
        depth = _depth_frame(device)
        if depth.has_metadata(ob.OBFrameMetadataType.EXPOSURE):
            value = depth.get_metadata_value(ob.OBFrameMetadataType.EXPOSURE)
            assert value >= 0
            break
    else:
        pytest.skip("no depth frame carried EXPOSURE metadata")

    depth = _depth_frame(device)
    if depth.has_metadata(ob.OBFrameMetadataType.GAIN):
        assert depth.get_metadata_value(ob.OBFrameMetadataType.GAIN) >= 0


def test_TC_CPP_11_04_raw_metadata_buffer(device):
    depth = _depth_frame(device)
    video = depth.as_video_frame()
    assert video is not None
    assert video.get_metadata_size() > 0
    assert video.get_metadata() is not None


def test_TC_CPP_11_05_unsupported_field_safe(device):
    depth = _depth_frame(device)
    unsupported = ob.OBFrameMetadataType(9999)
    assert not depth.has_metadata(unsupported)


def test_TC_CPP_12_02_clone_frame(device):
    depth = _depth_frame(device)
    clone = ob.Frame.create_frame_from_other_frame(depth, True)

    assert clone is not None
    assert clone.get_data_size() == depth.get_data_size()
    assert clone.get_format() == depth.get_format()
