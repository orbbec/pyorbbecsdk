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
G300 series device discovery and basic information tests.

Covers: Gemini 330 / 335 / 335L / 335Le / 335Lg / 336 / 336L / 330L / 305 / 345
and all their variants.

Tests verify:
- Device enumeration and identity (name, VID, PID, serial number)
- Firmware and hardware version completeness
- Sensor availability (Depth, Color, IR mandatory for all G300 models)
- Physical properties (temperature, calibration parameters)
- USB connection
"""

import re

import pytest

from pyorbbecsdk import OBError, OBSensorType

pytestmark = [pytest.mark.hardware, pytest.mark.g300_series, pytest.mark.functional]


class TestG300DeviceDiscovery:
    """Verify the device is found and correctly identified as G300 series."""

    def test_device_found(self, g300_series_device):
        assert g300_series_device is not None

    def test_device_name_is_g300(self, device_info):
        """Device name must identify it as a Gemini 3xx series camera."""
        name = device_info.get_name()
        assert name is not None and len(name) > 0
        g300_prefixes = [
            "Gemini 330",
            "Gemini 335",
            "Gemini 336",
            "Gemini 305",
            "Gemini 345",
        ]
        assert any(p in name for p in g300_prefixes), f"Device name '{name}' is not a recognized G300 series model"

    def test_vid_is_orbbec(self, device_info):
        """Vendor ID must be Orbbec (0x2BC5)."""
        vid = device_info.get_vid()
        assert vid == 0x2BC5, f"Expected VID=0x2BC5, got 0x{vid:04X}"

    def test_pid_is_nonzero(self, device_info):
        pid = device_info.get_pid()
        assert pid is not None and pid > 0

    def test_serial_number_nonempty(self, device_info):
        sn = device_info.get_serial_number()
        assert sn is not None and len(sn.strip()) > 0

    def test_connection_type_is_usb(self, device_info):
        """All G300 series cameras connect via USB."""
        conn = device_info.get_connection_type()
        assert conn is not None
        assert "usb" in str(conn).lower(), f"Expected USB connection, got: '{conn}'"


class TestG300FirmwareInfo:

    def test_firmware_version_nonempty(self, device_info):
        fw = device_info.get_firmware_version()
        assert fw is not None and len(fw.strip()) > 0

    def test_firmware_version_format(self, device_info):
        """Firmware version must follow a numeric dotted pattern (e.g. 1.6.00)."""
        fw = device_info.get_firmware_version()
        assert re.search(r"v?\d+\.\d+\.[\w\.]+", fw), f"Firmware version '{fw}' does not match expected format"

    def test_hardware_version_nonempty(self, device_info):
        hw = device_info.get_hardware_version()
        assert hw is not None and len(hw.strip()) > 0

    def test_device_type_nonempty(self, device_info):
        assert device_info.get_device_type() is not None


class TestG300SensorList:
    """All G300 series models must expose Depth, Color, and at least one IR sensor."""

    def test_sensor_list_nonempty(self, g300_series_device):
        sl = g300_series_device.get_sensor_list()
        assert sl is not None and sl.get_count() > 0

    def test_depth_sensor_present(self, g300_series_device):
        sl = g300_series_device.get_sensor_list()
        types = [sl.get_sensor_by_index(i).get_type() for i in range(sl.get_count())]
        assert OBSensorType.DEPTH_SENSOR in types, "Depth sensor not found"

    def test_color_sensor_present(self, g300_series_device):
        sl = g300_series_device.get_sensor_list()
        types = [sl.get_sensor_by_index(i).get_type() for i in range(sl.get_count())]
        assert OBSensorType.COLOR_SENSOR in types, "Color sensor not found"

    def test_ir_sensor_present(self, g300_series_device):
        """G300 cameras use a single IR sensor or stereo left/right IR."""
        sl = g300_series_device.get_sensor_list()
        types = [sl.get_sensor_by_index(i).get_type() for i in range(sl.get_count())]
        has_ir = (
            OBSensorType.IR_SENSOR in types
            or OBSensorType.LEFT_IR_SENSOR in types
            or OBSensorType.RIGHT_IR_SENSOR in types
        )
        assert has_ir, "No IR sensor found"

    def test_all_sensors_have_valid_type(self, g300_series_device):
        sl = g300_series_device.get_sensor_list()
        for i in range(sl.get_count()):
            s = sl.get_sensor_by_index(i)
            assert s is not None and s.get_type() is not None


class TestG300PhysicalProperties:

    def test_temperature_readable(self, g300_series_device):
        temp = g300_series_device.get_temperature()
        assert temp is not None

    def test_temperature_in_range(self, g300_series_device):
        """Operating temperature should be within -10°C to 95°C."""
        temp = g300_series_device.get_temperature()
        import re as _re

        values = [float(v) for v in _re.findall(r"[-+]?\d*\.?\d+", str(temp))]
        if values:
            for val in values:
                assert -10.0 <= val <= 95.0, f"Temperature {val}°C is outside expected range"

    def test_calibration_params_available(self, g300_series_device):
        calib = g300_series_device.get_calibration_camera_param_list()
        assert calib is not None and calib.get_count() > 0
