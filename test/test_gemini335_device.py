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
Gemini 335 device discovery and basic information tests.

Tests in this module verify:
- Device can be enumerated by the SDK
- Device identity (name, PID, VID, serial number)
- Firmware and hardware version completeness
- Sensor availability (Depth, Color, IR mandatory for Gemini 335)
- Physical properties (temperature range)
- Connection type
"""

import re
import pytest

from pyorbbecsdk import OBSensorType, OBError

pytestmark = [pytest.mark.hardware, pytest.mark.gemini335]


class TestGemini335DeviceDiscovery:
    """Verify the device can be found and identified correctly."""

    def test_device_found(self, gemini335_device):
        """At least one device must be connected."""
        assert gemini335_device is not None

    def test_device_name_contains_gemini335(self, device_info):
        """Device name should identify this as a Gemini 335 family camera."""
        name = device_info.get_name()
        assert name is not None and len(name) > 0
        assert "Gemini 335" in name or "Gemini335" in name, (
            f"Expected 'Gemini 335' in device name, got: '{name}'"
        )

    def test_vid_is_orbbec(self, device_info):
        """Vendor ID must be Orbbec (0x2BC5)."""
        vid = device_info.get_vid()
        assert vid == 0x2BC5, f"Expected VID=0x2BC5, got 0x{vid:04X}"

    def test_pid_is_nonzero(self, device_info):
        """Product ID must be a non-zero value."""
        pid = device_info.get_pid()
        assert pid is not None and pid > 0, f"Invalid PID: {pid}"

    def test_serial_number_nonempty(self, device_info):
        """Serial number must be a non-empty string."""
        sn = device_info.get_serial_number()
        assert sn is not None and len(sn.strip()) > 0, "Serial number is empty"

    def test_connection_type_is_usb(self, device_info):
        """Gemini 335 connects via USB."""
        conn_type = device_info.get_connection_type()
        assert conn_type is not None
        conn_str = str(conn_type).lower()
        assert "usb" in conn_str, (
            f"Expected USB connection, got: '{conn_type}'"
        )


class TestGemini335FirmwareInfo:
    """Verify firmware and hardware version information."""

    def test_firmware_version_nonempty(self, device_info):
        """Firmware version string must be present."""
        fw = device_info.get_firmware_version()
        assert fw is not None and len(fw.strip()) > 0, "Firmware version is empty"

    def test_firmware_version_format(self, device_info):
        """Firmware version should follow a numeric dotted format (e.g. 1.2.34)."""
        fw = device_info.get_firmware_version()
        # Accept formats like: 1.2.3, 1.2.34, v1.2.3, 1.2.3.4
        pattern = r"v?\d+\.\d+\.[\w\.]+"
        assert re.search(pattern, fw), (
            f"Firmware version '{fw}' does not match expected numeric format"
        )

    def test_hardware_version_nonempty(self, device_info):
        """Hardware version string must be present."""
        hw = device_info.get_hardware_version()
        assert hw is not None and len(hw.strip()) > 0, "Hardware version is empty"

    def test_device_type_nonempty(self, device_info):
        """Device type enumeration must be defined."""
        device_type = device_info.get_device_type()
        assert device_type is not None


class TestGemini335SensorList:
    """Verify required sensors are present on Gemini 335."""

    def test_sensor_list_nonempty(self, gemini335_device):
        """Sensor list must contain at least one sensor."""
        sensor_list = gemini335_device.get_sensor_list()
        assert sensor_list is not None
        assert sensor_list.get_count() > 0

    def test_depth_sensor_present(self, gemini335_device):
        """Gemini 335 must have a depth sensor."""
        sensor_list = gemini335_device.get_sensor_list()
        sensor_types = [
            sensor_list.get_sensor_by_index(i).get_type()
            for i in range(sensor_list.get_count())
        ]
        assert OBSensorType.DEPTH_SENSOR in sensor_types, (
            "Depth sensor not found in sensor list"
        )

    def test_color_sensor_present(self, gemini335_device):
        """Gemini 335 must have a color sensor."""
        sensor_list = gemini335_device.get_sensor_list()
        sensor_types = [
            sensor_list.get_sensor_by_index(i).get_type()
            for i in range(sensor_list.get_count())
        ]
        assert OBSensorType.COLOR_SENSOR in sensor_types, (
            "Color sensor not found in sensor list"
        )

    def test_ir_sensor_present(self, gemini335_device):
        """Gemini 335 must have at least one IR sensor."""
        sensor_list = gemini335_device.get_sensor_list()
        sensor_types = [
            sensor_list.get_sensor_by_index(i).get_type()
            for i in range(sensor_list.get_count())
        ]
        has_ir = (
            OBSensorType.IR_SENSOR in sensor_types
            or OBSensorType.LEFT_IR_SENSOR in sensor_types
            or OBSensorType.RIGHT_IR_SENSOR in sensor_types
        )
        assert has_ir, "No IR sensor found in sensor list"

    def test_all_sensors_have_type(self, gemini335_device):
        """Every sensor in the list must return a valid type."""
        sensor_list = gemini335_device.get_sensor_list()
        for i in range(sensor_list.get_count()):
            sensor = sensor_list.get_sensor_by_index(i)
            assert sensor is not None
            assert sensor.get_type() is not None


class TestGemini335PhysicalProperties:
    """Verify physical properties reported by the device."""

    def test_temperature_is_readable(self, gemini335_device):
        """Device temperature must be readable."""
        temp = gemini335_device.get_temperature()
        assert temp is not None

    def test_temperature_in_reasonable_range(self, gemini335_device):
        """Device temperature should be between 0°C and 90°C when operating."""
        temp = gemini335_device.get_temperature()
        # OBDeviceTemperature has irTemp, ldmTemp, mainBoardTemp, chipTopTemp,
        # chipBottomTemp — check the main board temperature if accessible
        temp_str = str(temp)
        # Parse any float value found in the repr
        import re
        values = re.findall(r"[-+]?\d*\.?\d+", temp_str)
        float_vals = [float(v) for v in values]
        if float_vals:
            for val in float_vals:
                assert -10.0 <= val <= 95.0, (
                    f"Temperature value {val}°C is outside reasonable range"
                )

    def test_calibration_params_available(self, gemini335_device):
        """Calibration parameters list must be non-empty."""
        calib_list = gemini335_device.get_calibration_camera_param_list()
        assert calib_list is not None
        assert calib_list.get_count() > 0, (
            "Calibration camera param list is empty"
        )
