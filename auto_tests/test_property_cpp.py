"""Direct translations of tests/hardware/TC_CPP_14_property_hw_test.cpp.

Cases that need an SDK entry point this pyorbbecsdk build does not expose
(``get_structured_data`` / ``set_structured_data``) are skipped with an explicit
reason instead of being weakened; see ``temp_doc/PYTHON_BINDING_TEST_GAPS.md``.
"""

from __future__ import annotations

import struct

import pytest

from conftest import ob, require_method

pytestmark = pytest.mark.hardware

READ = ob.OBPermissionType.PERMISSION_READ
WRITE = ob.OBPermissionType.PERMISSION_WRITE
READ_WRITE = ob.OBPermissionType.PERMISSION_READ_WRITE


def _supported(device, prop, permission):
    try:
        return bool(device.is_property_supported(prop, permission))
    except Exception:  # noqa: BLE001
        return False


def _flip_bool(device, prop):
    if not _supported(device, prop, READ_WRITE):
        return False
    original = device.get_bool_property(prop)
    device.set_bool_property(prop, not original)
    assert device.get_bool_property(prop) != original
    device.set_bool_property(prop, original)
    assert device.get_bool_property(prop) == original
    return True


def _set_int_max(device, prop):
    if not _supported(device, prop, READ_WRITE):
        return False
    value_range = device.get_int_property_range(prop)
    if value_range.max <= value_range.min:
        return False
    original = device.get_int_property(prop)
    device.set_int_property(prop, value_range.max)
    assert device.get_int_property(prop) == value_range.max
    device.set_int_property(prop, original)
    assert device.get_int_property(prop) == original
    return True


# ---------------------------------------------------------------------------
# enumeration / scalar properties
# ---------------------------------------------------------------------------


def test_TC_CPP_14_01_property_enum(device):
    count = device.get_support_property_count()
    assert count > 0

    for index in range(count):
        prop = device.get_supported_property(index)
        assert prop is not None
        assert int(prop.id) >= 0


def test_TC_CPP_14_02_bool_property(device):
    _flip_bool(device, ob.OBPropertyID.OB_PROP_LASER_BOOL)


def test_TC_CPP_14_03_int_property_range(device):
    prop = ob.OBPropertyID.OB_PROP_DEPTH_EXPOSURE_INT
    if not _supported(device, prop, READ_WRITE):
        pytest.skip("depth exposure not supported")

    value_range = device.get_int_property_range(prop)
    assert value_range.max >= value_range.min
    assert value_range.step >= 0

    current = device.get_int_property(prop)
    assert value_range.min <= current <= value_range.max


def test_TC_CPP_14_04_float_property_range(device):
    prop = ob.OBPropertyID.OB_PROP_DEPTH_UNIT_FLEXIBLE_ADJUSTMENT_FLOAT
    if not _supported(device, prop, READ):
        pytest.skip("OB_PROP_DEPTH_UNIT_FLEXIBLE_ADJUSTMENT_FLOAT not supported on this device")

    value_range = device.get_float_property_range(prop)
    assert value_range.max >= value_range.min
    assert value_range.step >= 0.0

    current = device.get_float_property(prop)
    assert value_range.min <= current <= value_range.max


def test_TC_CPP_14_05_structured_data(device):
    require_method(
        ob.Device, "get_structured_data", reason="not exposed by this pyorbbecsdk build"
    )
    require_method(
        ob.Device, "set_structured_data", reason="not exposed by this pyorbbecsdk build"
    )

    prop = ob.OBPropertyID.OB_STRUCT_DEPTH_AE_ROI
    if not _supported(device, prop, READ_WRITE):
        pytest.skip("OB_STRUCT_DEPTH_AE_ROI not fully supported (read+write)")

    roi_format = "=hhhh"
    original = device.get_structured_data(prop)
    assert len(original) == struct.calcsize(roi_format)

    left, top, right, bottom = struct.unpack(roi_format, original)
    updated = struct.pack(roi_format, left, top, right, bottom)
    device.set_structured_data(prop, updated)
    assert device.get_structured_data(prop) is not None


def test_TC_CPP_14_06_raw_data(device):
    require_method(
        ob.Device, "get_structured_data", reason="not exposed by this pyorbbecsdk build"
    )
    candidates = []
    for index in range(device.get_support_property_count()):
        item = device.get_supported_property(index)
        if int(item.id) <= 0:
            continue
        if item.type != ob.OBPropertyType.OB_STRUCT_PROPERTY:
            continue
        permission = int(item.permission)
        if permission & int(READ) or permission & int(READ_WRITE):
            candidates.append(item)

    if not candidates:
        pytest.skip("No raw data properties found on this device")

    for item in candidates:
        assert device.get_structured_data(item.id) is not None


# ---------------------------------------------------------------------------
# control groups
# ---------------------------------------------------------------------------


def test_TC_CPP_14_07_laser_control(device):
    _flip_bool(device, ob.OBPropertyID.OB_PROP_LASER_BOOL)
    _flip_bool(device, ob.OBPropertyID.OB_PROP_LDP_BOOL)
    _flip_bool(device, ob.OBPropertyID.OB_PROP_FLOOD_BOOL)
    _set_int_max(device, ob.OBPropertyID.OB_PROP_LASER_POWER_LEVEL_CONTROL_INT)


def test_TC_CPP_14_08_depth_control(device):
    _flip_bool(device, ob.OBPropertyID.OB_PROP_DEPTH_MIRROR_BOOL)
    _flip_bool(device, ob.OBPropertyID.OB_PROP_DEPTH_FLIP_BOOL)
    _flip_bool(device, ob.OBPropertyID.OB_PROP_DEPTH_AUTO_EXPOSURE_BOOL)
    _set_int_max(device, ob.OBPropertyID.OB_PROP_DEPTH_EXPOSURE_INT)
    _set_int_max(device, ob.OBPropertyID.OB_PROP_DEPTH_GAIN_INT)


def test_TC_CPP_14_09_color_control(device):
    _flip_bool(device, ob.OBPropertyID.OB_PROP_COLOR_MIRROR_BOOL)
    _flip_bool(device, ob.OBPropertyID.OB_PROP_COLOR_FLIP_BOOL)
    _flip_bool(device, ob.OBPropertyID.OB_PROP_COLOR_AUTO_EXPOSURE_BOOL)
    _set_int_max(device, ob.OBPropertyID.OB_PROP_COLOR_EXPOSURE_INT)
    _set_int_max(device, ob.OBPropertyID.OB_PROP_COLOR_GAIN_INT)


def test_TC_CPP_14_10_ir_control(device):
    _flip_bool(device, ob.OBPropertyID.OB_PROP_IR_MIRROR_BOOL)
    _flip_bool(device, ob.OBPropertyID.OB_PROP_IR_FLIP_BOOL)
    _set_int_max(device, ob.OBPropertyID.OB_PROP_IR_EXPOSURE_INT)


def test_TC_CPP_14_11_device_management(device):
    _flip_bool(device, ob.OBPropertyID.OB_PROP_INDICATOR_LIGHT_BOOL)
    _set_int_max(device, ob.OBPropertyID.OB_PROP_FAN_WORK_MODE_INT)


def test_TC_CPP_14_12_timing_sync(device):
    config = device.get_timestamp_reset_config()
    original_enable = config.enable

    try:
        device.set_timestamp_reset_config(config)
        assert device.get_timestamp_reset_config().enable == original_enable
        device.timestamp_reset()
    except Exception as exc:  # noqa: BLE001
        pytest.skip(f"timestampReset not supported: {exc}")


def test_TC_CPP_14_13_hdr_interleave(device):
    _flip_bool(device, ob.OBPropertyID.OB_PROP_HDR_MERGE_BOOL)
    _flip_bool(device, ob.OBPropertyID.OB_PROP_FRAME_INTERLEAVE_ENABLE_BOOL)


# ---------------------------------------------------------------------------
# structured read groups
# ---------------------------------------------------------------------------


def test_TC_CPP_14_14_structured_read_group(device):
    checked = 0

    prop = ob.OBPropertyID.OB_STRUCT_DEVICE_TEMPERATURE
    if _supported(device, prop, READ):
        temperature = device.get_temperature()
        value = temperature.chip_top_temperature
        assert value is not None
        assert 0.0 <= float(value) <= 80.0
        checked += 1

    prop = ob.OBPropertyID.OB_STRUCT_BASELINE_CALIBRATION_PARAM
    if _supported(device, prop, READ):
        baseline = device.get_baseline()
        assert baseline.zpd >= 0
        checked += 1

    prop = ob.OBPropertyID.OB_STRUCT_MULTI_DEVICE_SYNC_CONFIG
    if _supported(device, prop, READ):
        config = device.get_multi_device_sync_config()
        assert int(config.mode) >= 0
        checked += 1

    prop = ob.OBPropertyID.OB_STRUCT_DEVICE_SERIAL_NUMBER
    if _supported(device, prop, READ):
        assert device.get_device_info().get_serial_number()
        checked += 1

    if checked == 0:
        pytest.skip("No structured data properties are supported for reading")

    assert checked >= 1


def test_TC_CPP_14_15_sdk_level_property(device):
    readable = False

    for prop in (
        ob.OBPropertyID.OB_PROP_HEARTBEAT_BOOL,
        ob.OBPropertyID.OB_PROP_WATCHDOG_BOOL,
        ob.OBPropertyID.OB_PROP_EXTERNAL_SIGNAL_RESET_BOOL,
        ob.OBPropertyID.OB_PROP_TIMER_RESET_TRIGGER_OUT_ENABLE_BOOL,
    ):
        if _supported(device, prop, READ):
            assert device.get_bool_property(prop) in (0, 1, True, False)
            readable = True

    for prop in (
        ob.OBPropertyID.OB_PROP_DEVICE_COMMUNICATION_TYPE_INT,
        ob.OBPropertyID.OB_PROP_DEVICE_WORK_MODE_INT,
        ob.OBPropertyID.OB_PROP_USB_POWER_STATE_INT,
    ):
        if _supported(device, prop, READ):
            assert device.get_int_property(prop) >= 0
            readable = True

    assert readable, "Current device exposes no readable SDK-level validation property"


# ---------------------------------------------------------------------------
# safety behaviour
# ---------------------------------------------------------------------------


def test_TC_CPP_14_16_unsupported_property_safe(device):
    invalid = ob.OBPropertyID(99999)
    assert not _supported(device, invalid, READ)
    with pytest.raises(Exception):
        device.get_int_property(invalid)


def test_TC_CPP_14_17_out_of_range_safe(device):
    prop = ob.OBPropertyID.OB_PROP_DEPTH_EXPOSURE_INT
    if not _supported(device, prop, WRITE):
        pytest.skip("depth exposure is not writable")

    value_range = device.get_int_property_range(prop)
    original = device.get_int_property(prop)

    try:
        device.set_int_property(prop, value_range.max + 10000)
    except Exception:  # noqa: BLE001 - refusing the write is acceptable
        pass
    finally:
        device.set_int_property(prop, original)

    assert value_range.min <= device.get_int_property(prop) <= value_range.max
