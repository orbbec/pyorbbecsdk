import time
import sys
from pyorbbecsdk import *

# Callback function to display update progress
def preset_update_callback(first_call, state, message, percent):
    if not first_call:
        sys.stdout.write("\033[3F")  # Move cursor up 3 lines
    sys.stdout.write("\033[K")  # Clear the current line
    print(f"Progress: {percent}%")
    sys.stdout.write("\033[K")
    print(f"Status  : {state}")
    sys.stdout.write("\033[K")
    print(f"Message : {message}\n", end='')

# Helper function to return the update state message
# def get_update_status(state):
#     if state == OBFwUpdateState.STAT_VERIFY_SUCCESS:
#         return "Image file verification success"
#     elif state == OBFwUpdateState.STAT_FILE_TRANSFER:
#         return "File transfer in progress"
#     elif state == OBFwUpdateState.STAT_DONE:
#         return "Update completed"
#     elif state == OBFwUpdateState.STAT_DONE_WITH_DUPLICATES:
#         return "Update completed, duplicated presets have been ignored"
#     elif state == OBFwUpdateState.STAT_IN_PROGRESS:
#         return "Update in progress"
#     elif state == OBFwUpdateState.STAT_START:
#         return "Starting the update"
#     elif state == OBFwUpdateState.STAT_VERIFY_IMAGE:
#         return "Verifying image file"
#     else:
#         return "Unknown status or error"

# Function to simulate input of preset file paths
def get_preset_paths():
    paths = []
    print("Please input the file paths of the optional depth preset file (.bin):")
    print(" - Press 'Enter' to finish this input")
    print(" - Press 'Q' or 'q' to exit the program")
    while len(paths) < 10:
        path = input("Enter Path: ")
        if path.lower() == 'q':
            return None
        if path == '':
            if len(paths) == 0:
                print("You didn't input any file paths")
                continue
            break
        if path.endswith(".bin"):
            paths.append(path)
        else:
            print("Invalid file format. Please provide a .bin file.")
    return paths

# Main loop to simulate device selection, preset update, and handling
def main():
      # Assuming `devices` is a list of `Device` objects that you've already gathered
      devices = []
      context = Context()
      device_list = context.query_devices()

      if device_list.get_count() == 0:
            print("No device found. Please connect a device first!")
            input("Press Enter to exit...")
            return

      for i in range(device_list.get_count()):
            devices.append(device_list[i])

      print("Devices found:")
      print_device_list(devices)
    
      while True:
        device = select_device(devices)  # User selects a device
        
        if not device:
            break
        
        preset_paths = get_preset_paths()
        if not preset_paths:
            break
        
        print("Start to update optional depth preset, please wait a moment...\n")
        
        # Pass the paths list to the update function and update via callback
        try:
            device.update_optional_depth_presets(
                preset_paths,
                lambda state, message, percent: preset_update_callback(True, state, message, percent)
            )
        except Exception as e:
            print(f"\nThe update was interrupted! An error occurred: {str(e)}")
            break

        print("\nUpdate completed successfully!")
        # Assuming `print_preset(device)` will show the updated preset information
        print_preset(device)

        if not should_continue():
            break

# Function to print device list (similar to the C++ printDeviceList function)
def print_device_list(devices):
    for i, device in enumerate(devices):
        print(f"[{i}] Device: {device.get_device_info().get_name()} | "
              f"SN: {device.get_device_info().get_serial_number()} | "
              f"Firmware version: {device.get_device_info().get_firmware_version()}")

# Function to let the user select a device
def select_device(devices):
    while True:
        device_index = input("Please select a device by index, or press 'q' to quit: ")
        if device_index.lower() == 'q':
            return None
        try:
            index = int(device_index)
            if 0 <= index < len(devices):
                return devices[index]
            else:
                print("Invalid index. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

# Function to check if the user wants to continue
def should_continue():
    input_str = input("Enter 'Q' or 'q' to quit, or any other key to continue: ")
    return input_str.lower() != 'q'

# Placeholder function to retrieve devices, implement this to match your system setup
def get_devices():
    # Example: Returning a list of Device objects.
    # In real usage, you'll need to query connected devices.
    return []

# Placeholder function to print preset info after the update, implement as needed
def print_preset(device):
    print(f"Updated preset for device {device.get_device_info().get_name()}")

# Run the program
if __name__ == "__main__":
    main()
