import unittest
from pyorbbecsdk import *


class PipelineTest(unittest.TestCase):

    def setUp(self) -> None:
        self.context = Context()
        device_list = self.context.query_devices()
        self.assertIsNotNone(device_list)
        self.assertGreater(device_list.get_count(), 0)
        self.device = device_list.get_device_by_index(0)
        self.assertIsNotNone(self.device)
        self.pipeline = Pipeline(self.device)
        self.assertIsNotNone(self.pipeline)

    def tearDown(self) -> None:
        self.pipeline = None
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

    def test_get_camera_param(self):
        camera_param = self.pipeline.get_camera_param()
        self.assertIsNotNone(camera_param)
        print(camera_param.depth_intrinsic)
        print(camera_param.rgb_intrinsic)
        print(camera_param.depth_distortion)
        print(camera_param.rgb_distortion)
        print(camera_param.transform)


if __name__ == '__main__':
    print("Start test Pipeline interface, Please make sure you have connected a device to your computer.")
    unittest.main()
