import unittest
from pyorbbecsdk import *


class DeviceTest(unittest.TestCase):
    def setUp(self) -> None:
        self.context = Context()
        device_list = self.context.query_devices()
        self.assertIsNotNone(device_list)
        self.assertGreater(device_list.get_count(), 0)
        self.device = device_list.get_device_by_index(0)
        self.assertIsNotNone(self.device)

    def tearDown(self) -> None:
        self.device = None
        self.context = None

    def test_get_device_info(self):
        device_info = self.device.get_device_info()
        self.assertIsNotNone(device_info)
        self.assertIsNotNone(device_info.get_name())
        self.assertIsNotNone(device_info.get_pid())
        self.assertIsNotNone(device_info.get_vid())
        self.assertIsNotNone(device_info.get_serial_number())
        self.assertIsNotNone(device_info.get_firmware_version())
        self.assertIsNotNone(device_info.get_hardware_version())
        self.assertIsNotNone(device_info.get_connection_type())
        self.assertIsNotNone(device_info.get_device_type())
        print("Device info: ", device_info)

    def test_get_sensor_list(self):
        sensor_list = self.device.get_sensor_list()
        self.assertIsNotNone(sensor_list)
        self.assertGreater(sensor_list.get_count(), 0)
        for i in range(sensor_list.get_count()):
            sensor = sensor_list.get_sensor_by_index(i)
            self.assertIsNotNone(sensor)
            self.assertIsNotNone(sensor.get_type())
            print(sensor)

    def test_get_depth_work_mode_list(self):
        if not self.device.is_property_supported(OBPropertyID.OB_STRUCT_CURRENT_DEPTH_ALG_MODE,
                                                 OBPermissionType.PERMISSION_READ_WRITE):
            print("Current device not support depth work mode!")
            return
        current_depth_work_mode = self.device.get_depth_work_mode()
        self.assertIsNotNone(current_depth_work_mode)
        print("Current depth work mode: ", current_depth_work_mode)
        depth_work_mode_list = self.device.get_depth_work_mode_list()
        self.assertIsNotNone(depth_work_mode_list)
        self.assertGreater(depth_work_mode_list.get_count(), 0)
        select_depth_work_mode = None
        for i in range(depth_work_mode_list.get_count()):
            depth_work_mode = depth_work_mode_list.get_depth_work_mode_by_index(i)
            self.assertIsNotNone(depth_work_mode)
            print(depth_work_mode)
            if depth_work_mode != current_depth_work_mode:
                select_depth_work_mode = depth_work_mode
        if select_depth_work_mode is not None:
            self.device.set_depth_work_mode(select_depth_work_mode)
            self.assertEqual(select_depth_work_mode, self.device.get_depth_work_mode())
            self.device.set_depth_work_mode(current_depth_work_mode)
            self.assertEqual(current_depth_work_mode, self.device.get_depth_work_mode())

        self.device.set_depth_work_mode(current_depth_work_mode)

    def test_get_calib_camera_params(self):
        calib_camera_params_list = self.device.get_calibration_camera_param_list()
        self.assertIsNotNone(calib_camera_params_list)
        self.assertGreater(calib_camera_params_list.get_count(), 0)
        for i in range(calib_camera_params_list.get_count()):
            calib_camera_params = calib_camera_params_list.get_camera_param(i)
            self.assertIsNotNone(calib_camera_params)
            print(calib_camera_params)


if __name__ == '__main__':
    print("Start test Device interface, Please make sure you have connected a device to your computer.")
    unittest.main()
