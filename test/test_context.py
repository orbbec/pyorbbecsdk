import unittest
from pyorbbecsdk import *


def on_device_connected_callback(_: DeviceList):
    print("on_device_connected_callback")


def on_device_disconnected_callback(_: DeviceList):
    print("on_device_disconnected_callback")


def on_set_device_changed_callback(disconn_list: DeviceList, conn_list: DeviceList):
    on_device_disconnected_callback(disconn_list)
    on_device_connected_callback(conn_list)


class ContextTest(unittest.TestCase):

    def setUp(self) -> None:
        self.context = Context()

    def tearDown(self) -> None:
        self.context = None

    def test_get_device_list(self):
        device_list = self.context.query_devices()
        self.assertIsNotNone(device_list)
        self.assertGreater(device_list.get_count(), 0)

    def test_setup_logger_level(self):
        self.context.set_logger_level(OBLogLevel.DEBUG)
        self.context.set_logger_level(OBLogLevel.INFO)
        self.context.set_logger_level(OBLogLevel.WARNING)
        self.context.set_logger_level(OBLogLevel.ERROR)
        self.context.set_logger_level(OBLogLevel.FATAL)
        self.context.set_logger_level(OBLogLevel.NONE)

    def test_set_device_changed_callback(self):
        self.context.set_device_changed_callback(on_set_device_changed_callback)

    def test_enable_multi_device_sync(self):
        self.context.enable_multi_device_sync(100)

    def test_set_logger_to_console(self):
        self.context.set_logger_to_console(OBLogLevel.DEBUG)

    def test_set_logger_to_file(self):
        self.context.set_logger_to_file(OBLogLevel.DEBUG, "test.log")


if __name__ == '__main__':
    print("Start test Context interface, Please make sure you have connected a device to your computer.")
    unittest.main()
