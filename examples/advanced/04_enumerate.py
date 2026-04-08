# ******************************************************************************
#  pyorbbecsdk Advanced Example 04 — Device and Sensor Enumeration
#
#  What you will learn:
#    1. How to list all connected devices with PID, VID, serial, and connection type
#    2. How to enumerate every sensor and its supported stream profiles
#    3. How to read format, resolution, and FPS for each profile interactively
#
#  Device requirement: All
#
#  Run:
#    python examples/advanced/04_enumerate.py
# ******************************************************************************
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pyorbbecsdk import Context  # type: ignore

ESC_KEY = "q"


def get_input_option():
    """Get user input option, return -1 to exit"""
    option = input("Please enter an option (or press 'q' to exit): ")
    if option.lower() == ESC_KEY:
        return -1
    try:
        return int(option)
    except ValueError:
        print("Invalid input, please enter a number!")
        return get_input_option()


def print_video_profile(profile, index, sensor_type):
    """Print video stream profile information, including sensor type"""
    # Check if VideoStreamProfile has the required methods
    if all(hasattr(profile, attr) for attr in ["get_format", "get_width", "get_height", "get_fps"]):
        format_name = profile.get_format()
        width = profile.get_width()
        height = profile.get_height()
        fps = profile.get_fps()
        print(
            f"Sensor type: {sensor_type} | {index}. format: {format_name}, width: {width}, height: {height}, fps: {fps}"
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
            profile_type = type(profile).__name__
            print(f"Profile #{index} type: {profile_type}")
            if profile_type == "VideoStreamProfile":
                print_video_profile(profile, index, sensor_type)
            else:
                print(f"{index}. Unknown video stream profile type")
        except Exception as e:
            print(f"Unable to retrieve stream profile: {e}")


def enumerate_sensors(device):
    """List device sensor information and allow user to select a sensor"""
    sensor_list = device.get_sensor_list()
    print("Available sensor list:")
    for index in range(sensor_list.get_count()):
        sensor_type = sensor_list.get_type_by_index(index)
        print(f" - {index}. Sensor type: {sensor_type}")

    # Prompt user to select a sensor
    sensor_selected = get_input_option()
    if sensor_selected == -1:
        return
    if sensor_selected >= sensor_list.get_count() or sensor_selected < 0:
        print("Invalid input, please select again!")
        return enumerate_sensors(device)

    sensor = sensor_list.get_sensor_by_index(sensor_selected)
    print(f"Selected sensor type: {sensor.get_type()}")
    enumerate_stream_profiles(sensor)


def main():
    context = Context()
    device_list = context.query_devices()
    if device_list.get_count() < 1:
        print("No device found, please connect a device and try again.")
        return

    print("Enumerated devices:")
    for index in range(device_list.get_count()):
        device = device_list[index]
        device_info = device.get_device_info()
        print(
            f" - {index}. Device name: {device_info.get_name()}, PID: {device_info.get_pid()}, Serial Number: {device_info.get_serial_number()}, Connection Type: {device_info.get_connection_type()}"
        )

    # Default to selecting the first device
    print(f"Please select a device, show between 0 and {device_list.get_count() - 1}")
    device_selected = get_input_option()
    if device_selected == -1:
        print("Exiting...")
        return
    selected_device = device_list[device_selected]
    enumerate_sensors(selected_device)


if __name__ == "__main__":
    main()
