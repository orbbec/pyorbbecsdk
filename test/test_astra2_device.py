# ******************************************************************************
#  Copyright (c) 2024 Orbbec 3D Technology, Inc
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
# ******************************************************************************
"""
Astra 2 device discovery and basic information tests.

Astra 2 characteristics:
- Structured light depth sensor (wider range than Astra Mini)
- Sensors: Depth, Color, IR
- Supports depth work mode switching (unique within Astra family)
- No IMU
- USB connection
- Depth range: 0.3 m – 10.0 m (wider than Astra Mini)
- Firmware: 2.8.20+

Tests verify:
- Device identity and enumeration
- Firmware version format
- Sensor presence (Depth, Color, IR mandatory)
- Calibration parameters accessible
- Depth work mode API (if supported)
"""

import re

import pytest

from pyorbbecsdk import OBError, OBSensorType

pytestmark = [pytest.mark.hardware, pytest.mark.astra2, pytest.mark.functional]


class TestAstra2DeviceDiscovery:

    def test_device_found(self, astra2_device):
        assert astra2_device is not None

    def test_device_name_is_astra2(self, device_info):
        name = device_info.get_name()
        assert name and ("Astra 2" in name or "Astra2" in name), f"Device name '{name}' is not an Astra 2 camera"

    def test_vid_is_orbbec(self, device_info):
        vid = device_info.get_vid()
        assert vid == 0x2BC5, f"Expected VID=0x2BC5, got 0x{vid:04X}"

    def test_pid_is_nonzero(self, device_info):
        assert device_info.get_pid() > 0

    def test_serial_number_nonempty(self, device_info):
        sn = device_info.get_serial_number()
        assert sn and len(sn.strip()) > 0

    def test_connection_type_is_usb(self, device_info):
        conn = device_info.get_connection_type()
        assert "usb" in str(conn).lower()


class TestAstra2FirmwareInfo:

    def test_firmware_version_nonempty(self, device_info):
        fw = device_info.get_firmware_version()
        assert fw and len(fw.strip()) > 0

    def test_firmware_version_format(self, device_info):
        fw = device_info.get_firmware_version()
        assert re.search(r"v?\d+\.\d+\.[\w\.]+", fw), f"Firmware version '{fw}' does not match expected format"

    def test_hardware_version_nonempty(self, device_info):
        hw = device_info.get_hardware_version()
        assert hw and len(hw.strip()) > 0


class TestAstra2SensorList:

    def test_sensor_list_nonempty(self, astra2_device):
        sl = astra2_device.get_sensor_list()
        assert sl and sl.get_count() > 0

    def test_depth_sensor_present(self, astra2_device):
        sl = astra2_device.get_sensor_list()
        types = [sl.get_sensor_by_index(i).get_type() for i in range(sl.get_count())]
        assert OBSensorType.DEPTH_SENSOR in types

    def test_color_sensor_present(self, astra2_device):
        sl = astra2_device.get_sensor_list()
        types = [sl.get_sensor_by_index(i).get_type() for i in range(sl.get_count())]
        assert OBSensorType.COLOR_SENSOR in types

    def test_ir_sensor_present(self, astra2_device):
        sl = astra2_device.get_sensor_list()
        types = [sl.get_sensor_by_index(i).get_type() for i in range(sl.get_count())]
        has_ir = (
            OBSensorType.IR_SENSOR in types
            or OBSensorType.LEFT_IR_SENSOR in types
            or OBSensorType.RIGHT_IR_SENSOR in types
        )
        assert has_ir, "No IR sensor found"


class TestAstra2PhysicalProperties:

    def test_temperature_readable(self, astra2_device):
        temp = astra2_device.get_temperature()
        assert temp is not None

    def test_calibration_params_available(self, astra2_device):
        calib = astra2_device.get_calibration_camera_param_list()
        assert calib and calib.get_count() > 0


class TestAstra2DepthWorkMode:
    """
    Astra 2 supports depth work mode switching (unique in the Astra family).
    If not supported, tests skip gracefully.
    """

    def test_depth_work_mode_get(self, astra2_device):
        try:
            mode = astra2_device.get_depth_work_mode()
            assert mode is not None
        except OBError as e:
            pytest.skip(f"Depth work mode not accessible: {e}")

    def test_depth_work_mode_list_nonempty(self, astra2_device):
        try:
            modes = astra2_device.get_depth_work_mode_list()
            assert modes and len(modes) > 0, "Depth work mode list is empty"
        except OBError as e:
            pytest.skip(f"Depth work mode list not available: {e}")

    def test_depth_work_mode_set_and_restore(self, astra2_device):
        """Switch to an alternate depth work mode and restore the original."""
        try:
            modes = astra2_device.get_depth_work_mode_list()
            if not modes or len(modes) < 2:
                pytest.skip("Fewer than 2 depth work modes available — cannot switch")
            original = astra2_device.get_depth_work_mode()
            # Pick a mode different from the current one
            target = next((m for m in modes if m.name != original.name), None)
            if target is None:
                pytest.skip("All modes have the same name — cannot distinguish")
            astra2_device.set_depth_work_mode(target.name)
            current = astra2_device.get_depth_work_mode()
            assert current.name == target.name
            astra2_device.set_depth_work_mode(original.name)
        except OBError as e:
            pytest.skip(f"Depth work mode switch not supported: {e}")
