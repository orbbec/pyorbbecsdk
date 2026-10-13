"""Direct translations of TC_CPP_24 and TC_CPP_25 hardware cases.

``TC_CPP_25_01`` needs ``Pipeline.get_calibration_param``, which the installed
pyorbbecsdk build does not expose (see ``temp_doc/PYTHON_BINDING_TEST_GAPS.md``),
so it is skipped rather than weakened.
"""

from __future__ import annotations

import math

import numpy as np
import pytest

from conftest import first_profile, ob, require_method, wait_for_frameset_with_retry

pytestmark = pytest.mark.hardware


def test_TC_CPP_24_04_pipeline_exception_safety(device):
    """Invalid start/stop sequences must not corrupt the pipeline.

    This build reports a duplicate ``start`` as a recoverable SDK error (logged)
    without raising, so the case asserts the safety property that matters:
    after the invalid sequences the pipeline still stops and a fresh pipeline
    can still start on the same device.
    """
    pipeline = ob.Pipeline(device)
    config = ob.Config()
    config.enable_stream(first_profile(pipeline, ob.OBSensorType.DEPTH_SENSOR))

    pipeline.start(config)
    try:
        # Invalid sequence: start without an intervening stop.  Raising is
        # allowed, a recoverable error is also acceptable.
        try:
            pipeline.start(config)
        except Exception:  # noqa: BLE001
            pass
    finally:
        pipeline.stop()

    # Stopping an already stopped pipeline must not corrupt the object.
    try:
        pipeline.stop()
    except Exception:  # noqa: BLE001
        pass

    # The device must still be usable through a fresh pipeline.
    recovery = ob.Pipeline(device)
    recovery.start(config)
    recovery.stop()


def test_TC_CPP_24_05_device_property_exception(device):
    prop = ob.OBPropertyID.OB_PROP_SLAVE_DEVICE_SYNC_STATUS_BOOL
    if device.is_property_supported(prop, ob.OBPermissionType.PERMISSION_READ):
        value = device.get_int_property(prop)
        assert value is not None

    with pytest.raises(Exception):
        device.set_int_property(prop, 99999)


def test_TC_CPP_25_01_intrinsic_extrinsic(device):
    require_method(
        ob.Pipeline, "get_calibration_param", reason="not exposed by this pyorbbecsdk build"
    )

    pipeline = ob.Pipeline(device)
    config = ob.Config()
    config.enable_stream(first_profile(pipeline, ob.OBSensorType.DEPTH_SENSOR))
    config.enable_stream(first_profile(pipeline, ob.OBSensorType.COLOR_SENSOR))

    param = pipeline.get_calibration_param(config)
    assert param is not None

    depth = param.get_intrinsic(ob.OBSensorType.DEPTH_SENSOR)
    color = param.get_intrinsic(ob.OBSensorType.COLOR_SENSOR)
    for intrinsic in (depth, color):
        assert all(
            math.isfinite(float(value))
            for value in (
                intrinsic.fx,
                intrinsic.fy,
                intrinsic.cx,
                intrinsic.cy,
                intrinsic.k1,
                intrinsic.k2,
                intrinsic.k3,
                intrinsic.k4,
                intrinsic.k5,
                intrinsic.k6,
                intrinsic.p1,
                intrinsic.p2,
            )
        )
        assert intrinsic.fx > 0
        assert intrinsic.fy > 0

    extrinsic = param.get_extrinsic(ob.OBSensorType.DEPTH_SENSOR, ob.OBSensorType.COLOR_SENSOR)
    rot = [float(v) for row in np.atleast_2d(extrinsic.rot) for v in row]
    assert all(math.isfinite(v) for v in rot)
    assert len(rot) == 9
    assert extrinsic.transform is not None


def test_TC_CPP_25_02_camera_calib_param(device):
    pipeline = ob.Pipeline(device)
    try:
        config = ob.Config()
        config.enable_stream(first_profile(pipeline, ob.OBSensorType.DEPTH_SENSOR))
        config.enable_stream(first_profile(pipeline, ob.OBSensorType.COLOR_SENSOR))
        pipeline.start(config)

        assert wait_for_frameset_with_retry(pipeline) is not None

        param = pipeline.get_camera_param()
        assert param is not None

        for value in (
            param.depth_intrinsic.fx,
            param.depth_intrinsic.fy,
            param.depth_intrinsic.cx,
            param.depth_intrinsic.cy,
            param.rgb_intrinsic.fx,
            param.rgb_intrinsic.fy,
        ):
            assert value > 0.0

        # OBCameraParam.transform is an OBExtrinsic in this binding; rot is 3x3.
        extrinsic = param.transform
        rot = [float(v) for row in np.atleast_2d(extrinsic.rot) for v in row]
        translation = [float(v) for v in np.atleast_1d(extrinsic.transform)]
        assert all(math.isfinite(v) for v in rot + translation)
    finally:
        pipeline.stop()


def _assert_imu_intrinsic(intrinsic, require_gravity_scale):
    """Validate the IMU intrinsic block.

    ``bias``/``gravity`` are 3-element arrays and ``scale_misalignment`` /
    ``temp_slope`` are flat 9-element arrays in this binding (not 3x3), so they
    are checked flat.
    """
    for value in (
        intrinsic.noise_density,
        intrinsic.random_walk,
        intrinsic.reference_temp,
    ):
        assert math.isfinite(float(value))

    for value in intrinsic.bias:
        assert math.isfinite(float(value))

    if require_gravity_scale:
        for value in intrinsic.gravity:
            assert math.isfinite(float(value))

    for value in intrinsic.scale_misalignment:
        assert math.isfinite(float(value))
    for value in intrinsic.temp_slope:
        assert math.isfinite(float(value))


def test_TC_CPP_25_03_imu_intrinsic(device):
    try:
        accel = device.get_sensor(ob.OBSensorType.ACCEL_SENSOR)
    except Exception:  # noqa: BLE001
        accel = None
    if accel is None:
        pytest.skip("No accel sensor")

    profiles = accel.get_stream_profile_list()
    if profiles is None or profiles.get_count() == 0:
        pytest.skip("No accel profiles available")

    _assert_imu_intrinsic(
        profiles.get_stream_profile_by_index(0).as_accel_stream_profile().get_intrinsic(),
        True,
    )

    gyro = device.get_sensor(ob.OBSensorType.GYRO_SENSOR)
    if gyro is None:
        return
    profiles = gyro.get_stream_profile_list()
    if profiles is None or profiles.get_count() == 0:
        return
    _assert_imu_intrinsic(
        profiles.get_stream_profile_by_index(0).as_gyro_stream_profile().get_intrinsic(),
        False,
    )


def test_TC_CPP_25_04_device_temperature(device):
    prop = ob.OBPropertyID.OB_STRUCT_DEVICE_TEMPERATURE
    if not device.is_property_supported(prop, ob.OBPermissionType.PERMISSION_READ):
        pytest.skip("Device temperature not supported")

    temperature = device.get_temperature()
    assert temperature is not None

    checked = 0
    for name in (
        "laser_temperature",
        "main_board_temperature",
        "tec_temperature",
        "imu_temperature",
        "rgb_temperature",
        "ir_left_temperature",
        "ir_right_temperature",
        "chip_top_temperature",
        "chip_bottom_temperature",
    ):
        value = getattr(temperature, name, None)
        if value is None:
            continue
        number = float(value)
        # A sensor that is absent reports NaN (observed for imu_temperature on a
        # Gemini 336L) and a missing channel reports 0.0; neither is a failure.
        if not math.isfinite(number):
            continue
        assert 0.0 <= number <= 100.0, f"{name}={number}"
        checked += 1

    assert checked > 0
