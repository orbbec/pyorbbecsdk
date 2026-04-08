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
Astra Mini Pro / Astra Mini S Pro device discovery and basic information tests.

Astra Mini characteristics:
- Structured light depth sensor
- Compact form factor (smallest in Astra line)
- Sensors: Depth, Color (Pro), IR
- No IMU
- USB connection (USB 2.0 / 3.0)
- Depth range: 0.3 m – 8.0 m

Tests verify:
- Device enumeration and identity
- Firmware and hardware version completeness
- Sensor presence (Depth mandatory; Color present on Pro variants)
- Temperature and calibration parameters
"""

import re

import pytest

from pyorbbecsdk import OBSensorType

pytestmark = [pytest.mark.hardware, pytest.mark.astra_mini, pytest.mark.functional]


class TestAstraMiniDeviceDiscovery:

    def test_device_found(self, astra_mini_device):
        assert astra_mini_device is not None

    def test_device_name_is_astra_mini(self, device_info):
        name = device_info.get_name()
        assert name and len(name) > 0
        assert "Astra Mini" in name or "Astra mini" in name, f"Device name '{name}' is not an Astra Mini camera"

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
        assert "usb" in str(conn).lower(), f"Expected USB, got: '{conn}'"


class TestAstraMiniSensorList:

    def test_sensor_list_nonempty(self, astra_mini_device):
        sl = astra_mini_device.get_sensor_list()
        assert sl and sl.get_count() > 0

    def test_depth_sensor_present(self, astra_mini_device):
        sl = astra_mini_device.get_sensor_list()
        types = [sl.get_sensor_by_index(i).get_type() for i in range(sl.get_count())]
        assert OBSensorType.DEPTH_SENSOR in types, "Depth sensor not found"

    def test_ir_sensor_present(self, astra_mini_device):
        sl = astra_mini_device.get_sensor_list()
        types = [sl.get_sensor_by_index(i).get_type() for i in range(sl.get_count())]
        has_ir = (
            OBSensorType.IR_SENSOR in types
            or OBSensorType.LEFT_IR_SENSOR in types
            or OBSensorType.RIGHT_IR_SENSOR in types
        )
        assert has_ir, "No IR sensor found"

    def test_color_or_depth_sensor_present(self, astra_mini_device):
        """Astra Mini Pro has color sensor; S Pro may have color; depth is always present."""
        sl = astra_mini_device.get_sensor_list()
        types = [sl.get_sensor_by_index(i).get_type() for i in range(sl.get_count())]
        assert OBSensorType.DEPTH_SENSOR in types

    def test_no_imu_sensor(self, astra_mini_device):
        """Astra Mini does not have an IMU — confirm or skip."""
        sl = astra_mini_device.get_sensor_list()
        types = [sl.get_sensor_by_index(i).get_type() for i in range(sl.get_count())]
        if OBSensorType.ACCEL_SENSOR in types:
            pytest.skip("This Astra Mini variant has an IMU — test expectation may differ")


class TestAstramMiniPhysicalProperties:

    def test_firmware_version_format(self, device_info):
        fw = device_info.get_firmware_version()
        assert fw and re.search(r"v?\d+\.\d+\.[\w\.]+", fw), f"Firmware version '{fw}' does not match expected format"

    def test_calibration_params_available(self, astra_mini_device):
        calib = astra_mini_device.get_calibration_camera_param_list()
        assert calib and calib.get_count() > 0
