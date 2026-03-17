import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Add the scripts directory to the path so we can import auto_update_firmware
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'scripts'))
import auto_update_firmware

class TestAutoUpdateFirmware(unittest.TestCase):

    @patch('auto_update_firmware.urllib.request.urlretrieve')
    @patch('auto_update_firmware.Context')
    @patch('auto_update_firmware.load_config')
    @patch('builtins.input', return_value='y')
    def test_firmware_update_flow(self, mock_input, mock_load_config, MockContext, mock_urlretrieve):
        # 1. Mock the configuration
        mock_load_config.return_value = {
            "devices": [
                {
                    "products": ["MockDevice"],
                    "recommended_version": "2.0.0",
                    "download_url": "http://example.com/mock_firmware.bin"
                }
            ]
        }

        # 2. Mock the Orbbec SDK context and device
        mock_ctx = MockContext.return_value
        mock_device_list = MagicMock()
        mock_ctx.query_devices.return_value = mock_device_list
        mock_device_list.get_count.return_value = 1

        mock_device = MagicMock()
        mock_device_list.get_device_by_index.return_value = mock_device

        mock_info = MagicMock()
        mock_device.get_device_info.return_value = mock_info
        mock_info.get_name.return_value = "MockDevice"
        mock_info.get_serial_number.return_value = "SN123456"
        mock_info.get_firmware_version.return_value = "1.0.0" # Needs update

        # 3. Run the main function
        try:
            auto_update_firmware.main()
        except SystemExit:
            pass # main() calls sys.exit(0) on success, or sys.exit(1) on failure

        # 4. Verify the flow
        
        # Verify download was called with correct URL
        mock_urlretrieve.assert_called_once()
        self.assertEqual(mock_urlretrieve.call_args[0][0], "http://example.com/mock_firmware.bin")
        
        # Get the temp file path that was used
        temp_file_path = mock_urlretrieve.call_args[0][1]

        # Verify firmware update was called on the device
        mock_device.update_firmware.assert_called_once()
        # args are (path, callback, async_update)
        update_args = mock_device.update_firmware.call_args[0]
        self.assertEqual(update_args[0], temp_file_path)
        self.assertEqual(update_args[2], False) # async_update is False

if __name__ == '__main__':
    unittest.main()
