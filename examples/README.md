# pyorbbecsdk examples

* [depth_viewer.py](depth_viewer.py) - Displays the depth stream from the camera.
* [depth_viewer_callback.py](depth_viewer_callback.py) - Displays the depth stream from the camera using a callback.
* [color_viewer.py](color_viewer.py) - Displays the color stream from the camera.
* [depth_work_mode.py](depth_work_mode.py) - Demonstrates how to set the depth work mode.
* [depth_color_sync.py](depth_color_sync_align_viewer.py) - Demonstrates how to synchronize the depth and color streams.
* [hello_orbbec.py](hello_orbbec.py) - Demonstrates how to get the device information.
* [hot_plug.py](hot_plug.py) - Demonstrates how to detect hot plug events.
* [imu_reader.py](imu_reader.py) - Demonstrates how to read the IMU data.
* [infrared_viewer.py](infrared_viewer.py) - Displays the infrared stream from the camera.(Gemini 2 XL does not support this sample. Please refer to double_infrared_viewer.py)
* [multi_device.py](multi_device.py) - Demonstrates how to use multiple devices.
* [recorder.py](recorder.py) - Demonstrates how to record the depth and color streams to a file.
* [net_device.py](net_device.py) - Demonstrates how to use the network device.
* [playback.py](playback.py) - Demonstrates how to play back the recorded streams.
* [save_image_to_disk](save_image_to_disk.py) - Demonstrates how to save the depth and color streams to disk.
* [save_pointcloud_to_disk.py](save_pointcloud_to_disk.py) - Demonstrates how to save the pointcloud to disk.
* [double_infrared_viewer.py](double_infrared_viewer.py) - Demonstrates how to display the double infrared stream.(Gemini 2 XL support)
* [net_device.py](net_device.py) - Demonstrate how to use network functions. Femto Mega and Gemini 2 XL support network functions. Notes：1. Femto Mega firemware version 1.1.5 network not support color MJPEG. 2. Femto Mega (firmware version 1.1.7) and Gemini 2 XL does not support DHCP . It is necessary to connect to the device using an IP address. You can view the device's IP address using the OrbbecViewer tool on a PC. Under USB connection, configure the IP address and the host computer in the same network segment, and verify using the ping command. It should be able to ping （Default IP address of the device: 192.168.1.10）. 