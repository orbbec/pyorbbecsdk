import pytest

from pyorbbecsdk import (
    Context,
    DeviceList,
    OBLogLevel,
)

pytestmark = [pytest.mark.hardware, pytest.mark.functional]


def on_device_connected(device_list: DeviceList):
    pass  # callback stub for testing


def on_device_disconnected(device_list: DeviceList):
    pass  # callback stub for testing


def on_device_changed(disconn_list: DeviceList, conn_list: DeviceList):
    on_device_disconnected(disconn_list)
    on_device_connected(conn_list)


class TestContext:

    def test_query_devices_returns_list(self, context):
        device_list = context.query_devices()
        assert device_list is not None

    def test_query_devices_has_device(self, context):
        """Requires a physical device. Skipped automatically if none connected."""
        device_list = context.query_devices()
        assert device_list.get_count() > 0, (
            "Expected at least one device — ensure USB camera is connected"
        )

    def test_set_logger_level_all_levels(self, context):
        for level in [
            OBLogLevel.DEBUG,
            OBLogLevel.INFO,
            OBLogLevel.WARNING,
            OBLogLevel.ERROR,
            OBLogLevel.FATAL,
            OBLogLevel.NONE,
        ]:
            context.set_logger_level(level)

    def test_set_device_changed_callback(self, context):
        context.set_device_changed_callback(on_device_changed)

    def test_enable_multi_device_sync(self, context):
        context.enable_multi_device_sync(100)

    def test_set_logger_to_console(self, context):
        context.set_logger_to_console(OBLogLevel.WARNING)

    def test_set_logger_to_file(self, context, tmp_path):
        log_file = str(tmp_path / "test.log")
        context.set_logger_to_file(OBLogLevel.WARNING, log_file)
