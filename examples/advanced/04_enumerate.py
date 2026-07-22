# ******************************************************************************
#  pyorbbecsdk Advanced Example 04 - Device and Sensor Enumeration
#
#  What you will learn:
#    1. How to list all connected devices with PID, VID, serial, and connection type
#    2. How to enumerate every sensor and its supported stream profiles
#    3. How to read format, resolution, and FPS for each profile interactively
#    4. How to enumerate repeatedly: 'q' at the sensor level goes back to device
#       selection, 'q' at the device level exits the program
#
#  Device requirement: All
#
#  Run:
#    python examples/advanced/04_enumerate.py
# ******************************************************************************
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pyorbbecsdk import (  # type: ignore
    Context,
    convert_format_to_string,
    convert_sensor_type_to_string,
)

QUIT_KEY = "q"


def get_input_option():
    """Get user input option, return -1 to exit (press 'q')"""
    while True:
        option = input("Please enter an option (or press 'q' to exit): ")
        if option.lower() == QUIT_KEY:
            return -1
        try:
            return int(option)
        except ValueError:
            print("Invalid input, please enter a number!")


def print_video_profile(profile, index, sensor_type):
    """Print video stream profile information, including sensor type"""
    # Check if VideoStreamProfile has the required methods
    if all(hasattr(profile, attr) for attr in ["get_format", "get_width", "get_height", "get_fps"]):
        format_name = convert_format_to_string(profile.get_format())
        width = profile.get_width()
        height = profile.get_height()
        fps = profile.get_fps()
        print(
            f"Sensor type: {convert_sensor_type_to_string(sensor_type)} | {index}. format: {format_name}, width: {width}, height: {height}, fps: {fps}"
        )
    else:
        print(f"{index}. VideoStreamProfile is missing expected methods")


def enumerate_stream_profiles(sensor):
    """List stream profiles based on sensor type"""
    try:
        stream_profile_list = sensor.get_stream_profile_list()
    except Exception as e:
        print(f"Unable to get StreamProfileList: {e}")
        return

    sensor_type = sensor.get_type()
    print("Available stream profiles:")
    for index in range(stream_profile_list.get_count()):
        try:
            profile = stream_profile_list.get_stream_profile_by_index(index)
            print(f"Profile #{index} type: {type(profile).__name__}")
            if profile.is_video_stream_profile():
                print_video_profile(profile, index, sensor_type)
            elif profile.is_accel_stream_profile():
                accel_profile = profile.as_accel_stream_profile()
                print(
                    f"{index}. AccelStreamProfile: full_scale_range: {accel_profile.get_full_scale_range()}, sample_rate: {accel_profile.get_sample_rate()}"
                )
            elif profile.is_gyro_stream_profile():
                gyro_profile = profile.as_gyro_stream_profile()
                print(
                    f"{index}. GyroStreamProfile: full_scale_range: {gyro_profile.get_full_scale_range()}, sample_rate: {gyro_profile.get_sample_rate()}"
                )
            elif profile.is_lidar_stream_profile():
                lidar_profile = profile.as_lidar_stream_profile()
                print(f"{index}. LiDARStreamProfile: scan_rate: {lidar_profile.get_scan_rate()}")
            else:
                print(f"{index}. Unknown stream profile type")
        except Exception as e:
            print(f"Unable to retrieve stream profile: {e}")


def enumerate_sensors(device):
    """List device sensor information and allow user to select a sensor repeatedly"""
    while True:
        sensor_list = device.get_sensor_list()
        print("Available sensor list:")
        for index in range(sensor_list.get_count()):
            sensor_type = sensor_list.get_type_by_index(index)
            print(f" - {index}. Sensor type: {convert_sensor_type_to_string(sensor_type)}")

        print("Select a sensor to enumerate its streams (input sensor index or 'q' to back to device):")
        sensor_selected = get_input_option()
        if sensor_selected == -1:
            # 'q' -> back to device selection
            return
        if sensor_selected >= sensor_list.get_count() or sensor_selected < 0:
            print("\nInvalid input, please reselect the sensor!\n")
            continue

        sensor = sensor_list.get_sensor_by_index(sensor_selected)
        print(f"Selected sensor type: {convert_sensor_type_to_string(sensor.get_type())}")
        enumerate_stream_profiles(sensor)
        # Loop back to let the user pick another sensor of the same device


def main():
    context = Context()
    while True:
        device_list = context.query_devices()
        if device_list.get_count() < 1:
            print("No device found! Please connect a supported device and retry this program.")
            return

        print("Enumerated devices:")
        for index in range(device_list.get_count()):
            device = device_list[index]
            device_info = device.get_device_info()
            print(
                f" - {index}. Device name: {device_info.get_name()}, PID: {device_info.get_pid()}, Serial Number: {device_info.get_serial_number()}, Connection Type: {device_info.get_connection_type()}"
            )

        print("Select a device to enumerate its sensors (input device index or 'q' to exit program):")
        device_selected = get_input_option()
        if device_selected == -1:
            # 'q' -> exit the program
            print("Exiting...")
            return
        if device_selected >= device_list.get_count() or device_selected < 0:
            print("\nInvalid input, please reselect the device!\n")
            continue

        selected_device = device_list[device_selected]
        enumerate_sensors(selected_device)
        # Loop back to let the user pick another device (or exit)


if __name__ == "__main__":
    main()
