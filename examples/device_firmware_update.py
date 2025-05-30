# ******************************************************************************
#  Copyright (c) 2024 Orbbec 3D Technology, Inc
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http:# www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
# ******************************************************************************

import os
import sys
from pyorbbecsdk import *

devices = []
first_call = True


def get_firmware_path():
    """Prompt user for the firmware file path with improved Windows compatibility."""
    while True:
        firmware_path = input("Please input the path of the firmware file (.bin) to be updated (or 'q' to quit): ")

        if firmware_path.lower() == 'q':
            sys.exit("Exiting...")

        # Clean up the input path
        firmware_path = firmware_path.strip().strip("'").strip('"')  # Remove quotes and extra spaces

        # Normalize path separators for Windows compatibility
        firmware_path = os.path.normpath(firmware_path)

        try:
            # Convert to absolute path with proper handling of relative paths
            firmware_path = os.path.abspath(os.path.expanduser(firmware_path))

            # Verify the file exists and has .bin extension
            if os.path.isfile(firmware_path):
                # Try to open the file to verify access permissions
                try:
                    with open(firmware_path, 'rb') as f:
                        pass
                    print(f"Firmware file confirmed: {firmware_path}\n")
                    return firmware_path
                except PermissionError:
                    print("Error: Permission denied. Cannot access the specified file.\n")
                except Exception as e:
                    print(f"Error accessing file: {str(e)}\n")
            else:
                print("Invalid file format or path. Please provide a valid .bin file.\n")
        except Exception as e:
            print(f"Error processing path: {str(e)}\n")
            print("Please provide a valid file path.\n")


def print_device_list():
    """Print the list of connected devices."""
    print("--------------------------------------------------------------------------------")
    for i, device in enumerate(devices):
        device_info = device.get_device_info()
        print(
            f"[{i}] Device: {device_info.get_name()} | SN: {device_info.get_serial_number()} | Firmware version: {device_info.get_firmware_version()}")
    print("--------------------------------------------------------------------------------")


def select_device():
    """Allow user to select a device by index."""
    while True:
        choice = input(
            "Please select a device to update the firmware, enter 'l' to list devices, or 'q' to quit: \n").strip()

        if choice.lower() == 'q':
            return None

        if choice.lower() == 'l':
            print_device_list()
            continue

        try:
            index = int(choice)
            if 0 <= index < len(devices):
                print()
                return index
            else:
                print("Invalid index. Please select a valid device index.")
        except ValueError:
            print("Invalid input. Please enter a numeric index.")


def firmware_update_callback(state, message, percent):
    """Callback function to report firmware update progress."""
    global first_call
    if first_call:
        first_call = False
    else:
        print("\033[F\033[F", end="")  # Move up two lines to overwrite previous output

    print(f"Progress: {percent}%")
    print(f"Status  : {state}")
    print(f"Message : {message}\n")


def main():
    global first_call
    try:
        context = Context()
        device_list = context.query_devices()

        if device_list.get_count() == 0:
            print("No device found. Please connect a device first!")
            input("Press Enter to exit...")
            return

        for i in range(device_list.get_count()):
            devices.append(device_list[i])

        print("Devices found:")
        print_device_list()

        while True:
            first_call = True
            device_index = select_device()

            if device_index is None:
                break

            firmware_path = get_firmware_path()

            print("Upgrading device firmware, please wait...\n")
            try:
                devices[device_index].update_firmware(firmware_path, firmware_update_callback, async_update=False)
                print("Firmware update completed successfully! Please reboot the device.")
            except Exception as e:
                print("\nThe upgrade was interrupted! An error occurred!")
                print(f"Error message: {str(e)}")
                input("Press Enter to exit...")
                break

            if input("Enter 'q' to quit, or any other key to continue: ").lower() == 'q':
                break

    except Exception as e:
        print(f"Error: {str(e)}")
        input("Press Enter to exit.")
        sys.exit(1)


if __name__ == "__main__":
    main()
