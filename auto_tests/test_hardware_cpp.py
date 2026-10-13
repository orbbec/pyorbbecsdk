"""Hardware translations of the non-destructive C++ hardware cases.

Covers ``tests/hardware/TC_CPP_02`` ~ ``TC_CPP_04`` enumeration cases.  The
remaining TC_CPP_02..05 cases (network, access modes, destructive) live in
``test_discovery_deviceinfo_access_cpp.py``.
"""

from __future__ import annotations

import pytest

from conftest import ob

pytestmark = pytest.mark.hardware


def test_TC_CPP_02_01_usb_device_enum(context):
    devices = context.query_devices()
    assert devices is not None
    assert devices.get_count() > 0


def test_TC_CPP_03_01_count_and_index(context):
    devices = context.query_devices()
    assert devices.get_count() > 0

    for index in range(devices.get_count()):
        device = devices.get_device_by_index(index)
        assert device is not None
        assert devices.get_device_name_by_index(index)
        assert devices.get_device_pid_by_index(index) > 0


def test_TC_CPP_03_02_access_mode(context):
    # Every access mode must be able to address the connected device; the SDK
    # rejects the mode itself when the device does not support it.
    devices = context.query_devices()
    for index in range(devices.get_count()):
        serial = devices.get_device_serial_number_by_index(index)
        for mode in (
            ob.OBDeviceAccessMode.OB_DEVICE_DEFAULT_ACCESS,
            ob.OBDeviceAccessMode.OB_DEVICE_CONTROL_ACCESS,
        ):
            assert devices.get_device_by_serial_number(serial, mode) is not None


def test_TC_CPP_03_03_get_by_sn_uid(context):
    devices = context.query_devices()
    assert devices.get_count() > 0

    index = 0
    info = devices.get_device_by_index(index).get_device_info()
    serial = devices.get_device_serial_number_by_index(index)

    assert devices.get_device_by_serial_number(serial) is not None
    assert devices.get_device_by_uid(devices.get_device_uid_by_index(index)) is not None
    assert info.get_serial_number() == serial

    with pytest.raises(Exception):
        devices.get_device_by_serial_number("NON_EXISTENT_SN_12345")
    with pytest.raises(Exception):
        devices.get_device_by_uid("NON_EXISTENT_UID_12345")


def test_TC_CPP_04_01_basic_info(device_info):
    assert device_info.get_name()
    assert device_info.get_serial_number()
    assert device_info.get_firmware_version()
