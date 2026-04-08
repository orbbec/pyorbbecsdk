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
Femto Bolt / Femto Mega device discovery and basic information tests.

Femto family characteristics:
- Time-of-Flight (ToF) depth sensor (not structured light)
- Depth range: 0.3 m – 8.0 m (300 – 8000 mm)
- Sensors: Depth, Color, Left IR, Right IR, Accelerometer, Gyroscope
- Femto Bolt: USB 3.0 only
- Femto Mega / Femto Mega I: USB 3.0 + Ethernet

Tests verify:
- Device enumeration and identity
- Firmware and hardware version completeness
- Mandatory sensor presence (Depth, Color, IR, IMU)
- Physical properties (temperature, calibration)
- IMU sensor availability
"""

import re

import pytest

from pyorbbecsdk import OBSensorType

pytestmark = [pytest.mark.hardware, pytest.mark.femto, pytest.mark.functional]


class TestFemtoDeviceDiscovery:

    def test_device_found(self, femto_device):
        assert femto_device is not None

    def test_device_name_is_femto(self, device_info):
        name = device_info.get_name()
        assert name and len(name) > 0
        assert "Femto" in name or "femto" in name, f"Device name '{name}' is not a Femto family camera"

    def test_vid_is_orbbec(self, device_info):
        vid = device_info.get_vid()
        assert vid == 0x2BC5, f"Expected VID=0x2BC5, got 0x{vid:04X}"

    def test_pid_is_nonzero(self, device_info):
        assert device_info.get_pid() > 0

    def test_serial_number_nonempty(self, device_info):
        sn = device_info.get_serial_number()
        assert sn and len(sn.strip()) > 0


class TestFemtoFirmwareInfo:

    def test_firmware_version_nonempty(self, device_info):
        fw = device_info.get_firmware_version()
        assert fw and len(fw.strip()) > 0

    def test_firmware_version_format(self, device_info):
        fw = device_info.get_firmware_version()
        assert re.search(r"v?\d+\.\d+\.[\w\.]+", fw), f"Firmware version '{fw}' does not match expected format"

    def test_hardware_version_nonempty(self, device_info):
        hw = device_info.get_hardware_version()
        assert hw and len(hw.strip()) > 0


class TestFemtoSensorList:
    """Femto cameras must expose Depth, Color, Left IR, Right IR, and IMU sensors."""

    def test_sensor_list_nonempty(self, femto_device):
        sl = femto_device.get_sensor_list()
        assert sl and sl.get_count() > 0

    def test_depth_sensor_present(self, femto_device):
        sl = femto_device.get_sensor_list()
        types = [sl.get_sensor_by_index(i).get_type() for i in range(sl.get_count())]
        assert OBSensorType.DEPTH_SENSOR in types, "Depth sensor not found"

    def test_color_sensor_present(self, femto_device):
        sl = femto_device.get_sensor_list()
        types = [sl.get_sensor_by_index(i).get_type() for i in range(sl.get_count())]
        assert OBSensorType.COLOR_SENSOR in types, "Color sensor not found"

    def test_ir_sensors_present(self, femto_device):
        """Femto ToF cameras use Left IR + Right IR for depth computation."""
        sl = femto_device.get_sensor_list()
        types = [sl.get_sensor_by_index(i).get_type() for i in range(sl.get_count())]
        has_ir = (
            OBSensorType.IR_SENSOR in types
            or OBSensorType.LEFT_IR_SENSOR in types
            or OBSensorType.RIGHT_IR_SENSOR in types
        )
        assert has_ir, "No IR sensor found on Femto device"

    def test_imu_sensors_present(self, femto_device):
        """Femto cameras include an IMU (accelerometer + gyroscope)."""
        sl = femto_device.get_sensor_list()
        types = [sl.get_sensor_by_index(i).get_type() for i in range(sl.get_count())]
        has_accel = OBSensorType.ACCEL_SENSOR in types
        has_gyro = OBSensorType.GYRO_SENSOR in types
        assert has_accel, "Accelerometer sensor not found on Femto device"
        assert has_gyro, "Gyroscope sensor not found on Femto device"


class TestFemtoPhysicalProperties:

    def test_temperature_readable(self, femto_device):
        temp = femto_device.get_temperature()
        assert temp is not None

    def test_temperature_in_range(self, femto_device):
        import re as _re

        temp = femto_device.get_temperature()
        values = [float(v) for v in _re.findall(r"[-+]?\d*\.?\d+", str(temp))]
        if values:
            for val in values:
                assert -10.0 <= val <= 95.0, f"Temperature {val}°C out of range"

    def test_calibration_params_available(self, femto_device):
        calib = femto_device.get_calibration_camera_param_list()
        assert calib and calib.get_count() > 0
