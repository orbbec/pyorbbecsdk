import pytest

from pyorbbecsdk import (
    OBPropertyID,
    OBPermissionType,
)

pytestmark = pytest.mark.hardware


class TestDeviceInfo:

    def test_device_info_not_none(self, device_info):
        assert device_info is not None

    def test_device_name_nonempty(self, device_info):
        assert device_info.get_name() is not None and len(device_info.get_name()) > 0

    def test_pid_not_none(self, device_info):
        assert device_info.get_pid() is not None

    def test_vid_not_none(self, device_info):
        assert device_info.get_vid() is not None

    def test_serial_number_nonempty(self, device_info):
        sn = device_info.get_serial_number()
        assert sn is not None and len(sn.strip()) > 0

    def test_firmware_version_nonempty(self, device_info):
        fw = device_info.get_firmware_version()
        assert fw is not None and len(fw.strip()) > 0

    def test_hardware_version_nonempty(self, device_info):
        hw = device_info.get_hardware_version()
        assert hw is not None and len(hw.strip()) > 0

    def test_connection_type_not_none(self, device_info):
        assert device_info.get_connection_type() is not None

    def test_device_type_not_none(self, device_info):
        assert device_info.get_device_type() is not None


class TestSensorList:

    def test_sensor_list_not_none(self, device):
        sensor_list = device.get_sensor_list()
        assert sensor_list is not None

    def test_sensor_list_nonempty(self, device):
        sensor_list = device.get_sensor_list()
        assert sensor_list.get_count() > 0

    def test_all_sensors_have_type(self, device):
        sensor_list = device.get_sensor_list()
        for i in range(sensor_list.get_count()):
            sensor = sensor_list.get_sensor_by_index(i)
            assert sensor is not None
            assert sensor.get_type() is not None


class TestDepthWorkMode:

    def test_depth_work_mode_get_set(self, device):
        prop = OBPropertyID.OB_STRUCT_CURRENT_DEPTH_ALG_MODE
        if not device.is_property_supported(prop, OBPermissionType.PERMISSION_READ_WRITE):
            pytest.skip("Device does not support depth work mode")

        current = device.get_depth_work_mode()
        assert current is not None

        mode_list = device.get_depth_work_mode_list()
        assert mode_list is not None
        assert mode_list.get_count() > 0

        other_mode = None
        for i in range(mode_list.get_count()):
            m = mode_list.get_depth_work_mode_by_index(i)
            if m != current:
                other_mode = m
                break

        if other_mode is not None:
            device.set_depth_work_mode(other_mode)
            assert device.get_depth_work_mode() == other_mode
            device.set_depth_work_mode(current)
            assert device.get_depth_work_mode() == current


class TestCalibrationAndTemperature:

    def test_calibration_param_list_nonempty(self, device):
        params = device.get_calibration_camera_param_list()
        assert params is not None
        assert params.get_count() > 0

    def test_calibration_params_accessible(self, device):
        params = device.get_calibration_camera_param_list()
        for i in range(params.get_count()):
            p = params.get_camera_param(i)
            assert p is not None

    def test_temperature_readable(self, device):
        temp = device.get_temperature()
        assert temp is not None
