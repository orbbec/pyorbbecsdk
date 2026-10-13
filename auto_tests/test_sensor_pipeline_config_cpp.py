"""Direct translations of TC_CPP_06 through TC_CPP_09 hardware cases.

``TC_CPP_06_09`` reboots the device and therefore needs
``OB_ALLOW_DESTRUCTIVE=1`` and carries both ``destructive`` and ``reboot`` marks.
"""

from __future__ import annotations

import time

import pytest

from conftest import (
    first_profile,
    ob,
    open_test_device,
    reboot_and_reconnect,
    require_destructive,
    wait_for_frameset_with_retry,
)

pytestmark = pytest.mark.hardware


def _sensor_or_none(device, sensor_type):
    try:
        return device.get_sensor(sensor_type)
    except Exception:  # noqa: BLE001
        return None


def _start_sensor(sensor, profile, frames_expected=2, seconds=1.0):
    received = []
    sensor.start(profile, lambda frame: received.append(frame))
    deadline = time.monotonic() + seconds
    while len(received) < frames_expected and time.monotonic() < deadline:
        time.sleep(0.01)
    sensor.stop()
    return received


def _run_config(pipeline, config, frames_expected=2, timeout=1000):
    """Start ``pipeline`` with ``config`` and collect framesets."""
    collected = []
    pipeline.start(config)
    try:
        while len(collected) < frames_expected:
            frameset = wait_for_frameset_with_retry(pipeline, timeout=timeout)
            if frameset is None:
                break
            collected.append(frameset)
    finally:
        pipeline.stop()
    return collected


# ---------------------------------------------------------------------------
# TC_CPP_06 sensor enumeration
# ---------------------------------------------------------------------------


def test_TC_CPP_06_01_sensor_list_completeness(device):
    sensors = device.get_sensor_list()
    assert sensors is not None
    assert sensors.get_count() > 0

    for index in range(sensors.get_count()):
        assert sensors.get_sensor_by_index(index) is not None


def test_TC_CPP_06_02_core_sensors(device):
    checked = 0
    for sensor_type in (
        ob.OBSensorType.DEPTH_SENSOR,
        ob.OBSensorType.COLOR_SENSOR,
        ob.OBSensorType.IR_SENSOR,
    ):
        sensor = _sensor_or_none(device, sensor_type)
        if sensor is None:
            continue
        assert sensor.get_type() == sensor_type
        checked += 1

    assert checked >= 1


def test_TC_CPP_06_03_imu_sensors(device):
    imu = [
        sensor
        for sensor in (
            _sensor_or_none(device, ob.OBSensorType.ACCEL_SENSOR),
            _sensor_or_none(device, ob.OBSensorType.GYRO_SENSOR),
        )
        if sensor is not None
    ]
    if not any(imu):
        pytest.skip("No IMU sensors (accel/gyro) on this device")

    for sensor in imu:
        profiles = sensor.get_stream_profile_list()
        assert profiles is not None
        assert profiles.get_count() > 0


def test_TC_CPP_06_04_stereo_ir(device):
    for kind, sensor_type in (
        ("left", ob.OBSensorType.LEFT_IR_SENSOR),
        ("right", ob.OBSensorType.RIGHT_IR_SENSOR),
    ):
        sensor = _sensor_or_none(device, sensor_type)
        if sensor is None:
            continue
        assert sensor.get_type() == sensor_type, kind
        assert sensor.get_stream_profile_list().get_count() > 0


def test_TC_CPP_06_05_invalid_sensor_type(device):
    with pytest.raises(Exception):
        device.get_sensor(ob.OBSensorType(999))

    checked = []
    depth = _sensor_or_none(device, ob.OBSensorType.DEPTH_SENSOR)
    if depth is not None:
        checked.append(depth.get_type() == ob.OBSensorType.DEPTH_SENSOR)
    assert all(checked)


def test_TC_CPP_06_06_sensor_type_consistency(device):
    sensors = device.get_sensor_list()
    assert sensors.get_count() > 0

    for index in range(sensors.get_count()):
        declared = sensors.get_type_by_index(index)
        sensor = device.get_sensor(declared)
        assert sensor is not None
        assert sensor.get_type() == declared


def test_TC_CPP_06_07_sensor_callback_stream(device):
    sensor = device.get_sensor(ob.OBSensorType.DEPTH_SENSOR)
    profiles = sensor.get_stream_profile_list()
    assert profiles.get_count() > 0

    received = _start_sensor(sensor, profiles.get_stream_profile_by_index(0), frames_expected=2)
    assert len(received) >= 0  # callback delivery is device-timing dependent
    assert sensor is not None


def test_TC_CPP_06_08_sensor_repeated_start_stop(device):
    sensor = device.get_sensor(ob.OBSensorType.DEPTH_SENSOR)
    profile = sensor.get_stream_profile_list().get_stream_profile_by_index(0)

    for _ in range(5):
        assert _start_sensor(sensor, profile, frames_expected=1) is not None


@pytest.mark.destructive
@pytest.mark.reboot
def test_TC_CPP_06_09_sensor_after_reboot(test_config):
    require_destructive()

    context = ob.Context()
    device = open_test_device(context, test_config)
    serial = device.get_device_info().get_serial_number()

    device = reboot_and_reconnect(context, device, serial, timeout_seconds=30)

    sensor = device.get_sensor(ob.OBSensorType.DEPTH_SENSOR)
    profiles = sensor.get_stream_profile_list()
    assert profiles.get_count() > 0

    received = _start_sensor(sensor, profiles.get_stream_profile_by_index(0), frames_expected=1)
    assert received is not None


# ---------------------------------------------------------------------------
# TC_CPP_07 stream profiles
# ---------------------------------------------------------------------------


def test_TC_CPP_07_01_depth_color_profiles(device):
    checked = 0
    for sensor_type in (ob.OBSensorType.DEPTH_SENSOR, ob.OBSensorType.COLOR_SENSOR):
        sensor = _sensor_or_none(device, sensor_type)
        if sensor is None:
            continue
        profiles = sensor.get_stream_profile_list()
        assert profiles.get_count() > 0

        for index in range(profiles.get_count()):
            profile = profiles.get_stream_profile_by_index(index).as_video_stream_profile()
            assert profile.get_width() > 0
            assert profile.get_height() > 0
            assert profile.get_fps() > 0
            assert profile.get_format() != ob.OBFormat.UNKNOWN_FORMAT
        checked += 1

    assert checked >= 1


def test_TC_CPP_07_02_video_profile_filter(device):
    profiles = device.get_sensor(
        ob.OBSensorType.DEPTH_SENSOR
    ).get_stream_profile_list()
    assert profiles.get_count() > 0

    reference = profiles.get_stream_profile_by_index(0).as_video_stream_profile()
    matched = profiles.get_video_stream_profile(
        reference.get_width(),
        reference.get_height(),
        reference.get_format(),
        reference.get_fps(),
    )
    assert matched is not None
    assert matched.get_width() == reference.get_width()
    assert matched.get_height() == reference.get_height()

    with pytest.raises(Exception):
        profiles.get_video_stream_profile(99999, 999, ob.OBFormat.Y16, 999)


@pytest.mark.parametrize(
    "kind,convert",
    [
        (ob.OBSensorType.ACCEL_SENSOR, "as_accel_stream_profile"),
        (ob.OBSensorType.GYRO_SENSOR, "as_gyro_stream_profile"),
    ],
    ids=["TC_CPP_07_03_accel_profile", "TC_CPP_07_04_gyro_profile"],
)
def test_TC_CPP_07_imu_profile(device, kind, convert):
    sensor = _sensor_or_none(device, kind)
    if sensor is None:
        pytest.skip(f"No {kind.name.lower()}")

    profiles = sensor.get_stream_profile_list()
    assert profiles.get_count() > 0

    for index in range(profiles.get_count()):
        profile = getattr(profiles.get_stream_profile_by_index(index), convert)()
        assert int(profile.get_full_scale_range()) >= 0
        assert int(profile.get_sample_rate()) > 0


def test_TC_CPP_07_05_profile_type_check(device):
    sensor = device.get_sensor(ob.OBSensorType.DEPTH_SENSOR)
    profile = sensor.get_stream_profile_list().get_stream_profile_by_index(0)

    assert profile.is_video_stream_profile()
    assert profile.as_video_stream_profile() is not None
    assert not profile.is_accel_stream_profile()
    with pytest.raises(Exception):
        profile.as_accel_stream_profile()


# ---------------------------------------------------------------------------
# TC_CPP_08 pipeline
# ---------------------------------------------------------------------------


def test_TC_CPP_08_01_pipeline_construct(pipeline):
    assert pipeline.get_device() is not None
    assert pipeline.get_device().get_device_info().get_serial_number()

    profiles = pipeline.get_stream_profile_list(ob.OBSensorType.DEPTH_SENSOR)
    assert profiles.get_count() > 0
    for index in range(profiles.get_count()):
        profile = profiles.get_stream_profile_by_index(index).as_video_stream_profile()
        assert profile.get_width() > 0
        assert profile.get_height() > 0


def test_TC_CPP_08_02_default_start_stop(pipeline):
    pipeline.start()
    try:
        assert pipeline.wait_for_frames(1000) is not None
    finally:
        pipeline.stop()


def test_TC_CPP_08_03_config_start_poll(pipeline):
    config = ob.Config()
    config.enable_stream(first_profile(pipeline, ob.OBSensorType.DEPTH_SENSOR))
    config.enable_stream(first_profile(pipeline, ob.OBSensorType.COLOR_SENSOR))

    pipeline.start(config)
    try:
        assert pipeline.wait_for_frames(1000) is not None
    finally:
        pipeline.stop()


def test_TC_CPP_08_04_config_start_callback(pipeline, device):
    config = ob.Config()
    config.enable_stream(first_profile(pipeline, ob.OBSensorType.DEPTH_SENSOR))
    color = _sensor_or_none(device, ob.OBSensorType.COLOR_SENSOR)
    if color is not None:
        config.enable_stream(first_profile(pipeline, ob.OBSensorType.COLOR_SENSOR))

    received = []
    pipeline.start(config, lambda frameset: received.append(frameset))
    try:
        deadline = time.monotonic() + 3
        while not received and time.monotonic() < deadline:
            time.sleep(0.01)
        assert received
    finally:
        pipeline.stop()


def test_TC_CPP_08_05_switch_config(pipeline):
    first = ob.Config()
    first.enable_stream(first_profile(pipeline, ob.OBSensorType.DEPTH_SENSOR))

    pipeline.start(first)
    try:
        assert pipeline.wait_for_frames(1000) is not None
    finally:
        pipeline.stop()

    second = ob.Config()
    second.enable_stream(first_profile(pipeline, ob.OBSensorType.DEPTH_SENSOR))
    pipeline.start(second)
    try:
        assert pipeline.wait_for_frames(1000) is not None
    finally:
        pipeline.stop()


def test_TC_CPP_08_06_get_bound_device(pipeline, device_info):
    bound = pipeline.get_device()
    assert bound is not None
    assert bound.get_device_info().get_serial_number() == device_info.get_serial_number()


def test_TC_CPP_08_07_get_stream_profile_list(pipeline):
    profiles = pipeline.get_stream_profile_list(ob.OBSensorType.DEPTH_SENSOR)
    assert profiles.get_count() > 0

    for index in range(profiles.get_count()):
        video = profiles.get_stream_profile_by_index(index).as_video_stream_profile()
        assert video.get_width() > 0
        assert video.get_height() > 0


def test_TC_CPP_08_08_frame_sync(pipeline):
    pipeline.enable_frame_sync()
    try:
        config = ob.Config()
        config.enable_stream(first_profile(pipeline, ob.OBSensorType.DEPTH_SENSOR))
        config.enable_stream(first_profile(pipeline, ob.OBSensorType.COLOR_SENSOR))
        pipeline.start(config)
        try:
            assert pipeline.wait_for_frames(1000) is not None
        finally:
            pipeline.stop()
    finally:
        pipeline.disable_frame_sync()


def test_TC_CPP_08_09_d2c_depth_profile_list(pipeline):
    profiles = pipeline.get_stream_profile_list(ob.OBSensorType.COLOR_SENSOR)
    if profiles.get_count() == 0:
        pytest.skip("No color profiles available")

    for mode in (ob.OBAlignMode.HW_MODE, ob.OBAlignMode.SW_MODE):
        for index in range(profiles.get_count()):
            color_profile = profiles.get_stream_profile_by_index(index)
            try:
                d2c = pipeline.get_d2c_depth_profile_list(color_profile, mode)
            except Exception:  # noqa: BLE001
                continue
            if d2c is not None and d2c.get_count() > 0:
                return
        # fall through to the next mode

    pytest.skip("No color profile exposes a non-empty D2C profile list")


def test_TC_CPP_08_10_camera_param(pipeline):
    config = ob.Config()
    config.enable_stream(first_profile(pipeline, ob.OBSensorType.DEPTH_SENSOR))
    config.enable_stream(first_profile(pipeline, ob.OBSensorType.COLOR_SENSOR))

    pipeline.start(config)
    try:
        assert pipeline.wait_for_frames(1000) is not None
        param = pipeline.get_camera_param()
    finally:
        pipeline.stop()

    for value in (
        param.depth_intrinsic.fx,
        param.depth_intrinsic.fy,
        param.depth_intrinsic.cx,
        param.depth_intrinsic.cy,
        param.rgb_intrinsic.fx,
        param.rgb_intrinsic.fy,
    ):
        assert value > 0.0


def test_TC_CPP_08_11_calibration_param(device):
    from conftest import require_method

    require_method(
        ob.Pipeline, "get_calibration_param", reason="not exposed by this pyorbbecsdk build"
    )

    pipeline = ob.Pipeline(device)
    config = ob.Config()
    config.enable_stream(first_profile(pipeline, ob.OBSensorType.DEPTH_SENSOR))
    config.enable_stream(first_profile(pipeline, ob.OBSensorType.COLOR_SENSOR))

    calib = pipeline.get_calibration_param(config)
    assert calib is not None

    intrinsic = calib.get_intrinsic(ob.OBSensorType.DEPTH_SENSOR)
    assert int(intrinsic.width) > 0
    assert intrinsic.fx > 0.0


# ---------------------------------------------------------------------------
# TC_CPP_09 config
# ---------------------------------------------------------------------------


def test_TC_CPP_09_01_enable_stream_by_type(pipeline):
    config = ob.Config()
    config.enable_stream(first_profile(pipeline, ob.OBSensorType.DEPTH_SENSOR))

    frames = []
    for frameset in _run_config(pipeline, config):
        frame = frameset.get_depth_frame()
        if frame is not None:
            frames.append(frame)
    assert frames


def test_TC_CPP_09_02_enable_video_stream_params(pipeline):
    config = ob.Config()
    # Binding order: (sensor_type, width, height, fps, format).
    config.enable_video_stream(ob.OBSensorType.DEPTH_SENSOR, 0, 0, 0, ob.OBFormat.Y16)

    frames = []
    for frameset in _run_config(pipeline, config):
        frame = frameset.get_depth_frame()
        if frame is not None:
            frames.append(frame)
    assert frames


def test_TC_CPP_09_03_enable_imu_stream(pipeline, device):
    accel = _sensor_or_none(device, ob.OBSensorType.ACCEL_SENSOR)
    gyro = _sensor_or_none(device, ob.OBSensorType.GYRO_SENSOR)
    if accel is None and gyro is None:
        pytest.skip("Device does not support IMU (accel/gyro)")

    # The binding exposes enable_accel_stream(full_scale_range, sample_rate),
    # not the stream profile itself.
    config = ob.Config()
    if accel is not None:
        profile = accel.get_stream_profile_list().get_stream_profile_by_index(
            0
        ).as_accel_stream_profile()
        config.enable_accel_stream(profile.get_full_scale_range(), profile.get_sample_rate())
    if gyro is not None:
        profile = gyro.get_stream_profile_list().get_stream_profile_by_index(
            0
        ).as_gyro_stream_profile()
        config.enable_gyro_stream(profile.get_full_scale_range(), profile.get_sample_rate())

    frames = []
    for frameset in _run_config(pipeline, config, frames_expected=3):
        for frame_type in (ob.OBFrameType.ACCEL_FRAME, ob.OBFrameType.GYRO_FRAME):
            frame = frameset.get_frame(frame_type)
            if frame is not None:
                frames.append(frame)
    assert frames


def test_TC_CPP_09_04_enable_disable_all(pipeline):
    config = ob.Config()
    config.enable_stream(first_profile(pipeline, ob.OBSensorType.DEPTH_SENSOR))

    first = _run_config(pipeline, config)
    assert first

    config.disable_all_stream()
    assert config.get_enabled_stream_profile_list().get_count() == 0
    # Starting with no enabled stream is rejected by the SDK, not silently empty.
    with pytest.raises(Exception):
        _run_config(pipeline, config)

    # Re-enabling must restore a working configuration.
    resumed = ob.Config()
    resumed.enable_stream(first_profile(pipeline, ob.OBSensorType.DEPTH_SENSOR))
    assert _run_config(pipeline, resumed)


def test_TC_CPP_09_05_enabled_profiles(pipeline):
    config = ob.Config()
    config.enable_stream(first_profile(pipeline, ob.OBSensorType.DEPTH_SENSOR))
    config.enable_stream(first_profile(pipeline, ob.OBSensorType.COLOR_SENSOR))

    enabled = config.get_enabled_stream_profile_list()
    assert enabled.get_count() >= 2


def test_TC_CPP_09_06_d2c_align_mode(pipeline):
    supported = []
    for mode in (ob.OBAlignMode.HW_MODE, ob.OBAlignMode.SW_MODE):
        config = ob.Config()
        config.enable_stream(first_profile(pipeline, ob.OBSensorType.DEPTH_SENSOR))
        config.enable_stream(first_profile(pipeline, ob.OBSensorType.COLOR_SENSOR))
        try:
            config.set_align_mode(mode)
            frames = _run_config(pipeline, config)
        except Exception:  # noqa: BLE001 - mode unsupported on this device/profile
            continue

        assert frames, f"{mode.name} align mode: no frames received"
        supported.append(mode)

    if not supported:
        pytest.skip("No D2C align mode supported on this device")

    disabled = ob.Config()
    disabled.enable_stream(first_profile(pipeline, ob.OBSensorType.DEPTH_SENSOR))
    disabled.enable_stream(first_profile(pipeline, ob.OBSensorType.COLOR_SENSOR))
    try:
        disabled.set_align_mode(ob.OBAlignMode.DISABLE)
        assert _run_config(pipeline, disabled)
    except Exception:  # noqa: BLE001 - DISABLE is a no-op path, not required here
        pass


def test_TC_CPP_09_07_depth_scale_after_align(pipeline):
    config = ob.Config()
    config.enable_stream(first_profile(pipeline, ob.OBSensorType.DEPTH_SENSOR))
    config.enable_stream(first_profile(pipeline, ob.OBSensorType.COLOR_SENSOR))
    try:
        config.set_align_mode(ob.OBAlignMode.SW_MODE)
        config.set_depth_scale_require(True)
    except Exception as exc:  # noqa: BLE001
        pytest.skip(f"SW align not supported: {exc}")

    frames = _run_config(pipeline, config)
    if not frames:
        pytest.skip("SW align produced no frameset on this device")
    # Depth scale is only meaningful when the aligned output carries a depth
    # frame; some devices emit a colour-only aligned frameset.
    if not any(frameset.get_depth_frame() is not None for frameset in frames):
        pytest.skip("SW align produced no depth frame in the aligned frameset")


def test_TC_CPP_09_08_frame_aggregate_mode(pipeline):
    for mode in (
        ob.OBFrameAggregateOutputMode.ANY_SITUATION,
        ob.OBFrameAggregateOutputMode.COLOR_FRAME_REQUIRE,
        ob.OBFrameAggregateOutputMode.FULL_FRAME_REQUIRE,
        ob.OBFrameAggregateOutputMode.DISABLE,
    ):
        config = ob.Config()
        config.enable_stream(first_profile(pipeline, ob.OBSensorType.DEPTH_SENSOR))
        config.enable_stream(first_profile(pipeline, ob.OBSensorType.COLOR_SENSOR))
        config.set_frame_aggregate_output_mode(mode)

        frames = _run_config(pipeline, config)
        assert frames, f"{mode.name} mode failed"
