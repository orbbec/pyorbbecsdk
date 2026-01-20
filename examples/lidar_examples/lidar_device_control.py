# ******************************************************************************
#  Copyright (c) 2024 Orbbec 3D Technology, Inc
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
# ******************************************************************************
import sys
import os
from pyorbbecsdk import *
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import is_lidar_device

# Select a device, the name, pid, vid, uid of the device will be printed here, 
# and the corresponding device object will be created after selection
def select_device(device_list):
    dev_count = device_list.get_count()
    print("Device list: ")
    for i in range(dev_count):
        print(f"{i}. name: {device_list.get_device_name_by_index(i)}, "
              f"vid: 0x{hex(device_list.get_device_vid_by_index(i))}, "
              f"pid: 0x{hex(device_list.get_device_pid_by_index(i))}, "
              f"uid: {device_list.get_device_uid_by_index(i)}, "
              f"sn: {device_list.get_device_serial_number_by_index(i)}")
    
    while True:
        try:
            dev_index = int(input("Select a device index: "))
            if 0 <= dev_index < dev_count:
                return device_list.get_device_by_index(dev_index)
        except ValueError:
            pass
        print("Invalid selection, please reselect.")

# Convert permission type to string
def permission_type_to_string(permission):
    if permission == OBPermissionType.PERMISSION_READ:
        return "R/_"
    elif permission == OBPermissionType.PERMISSION_WRITE:
        return "_/W"
    elif permission == OBPermissionType.PERMISSION_READ_WRITE:
        return "R/W"
    return "_/_"

# Check if the property is a primary type (Int, Float, or Bool)
def is_primary_type_property(property_item):
    return property_item.type in [OBPropertyType.OB_INT_PROPERTY, OBPropertyType.OB_FLOAT_PROPERTY, OBPropertyType.OB_BOOL_PROPERTY]

# Get property list
def get_property_list(device):
    property_vec = []
    size = device.get_support_property_count()
    for i in range(size):
        item = device.get_supported_property(i)
        if is_primary_type_property(item) and item.permission != OBPermissionType.PERMISSION_DENY:
            property_vec.append(item)
    return property_vec

# Print a list of supported properties
def printf_property_list(device, property_list):
    print(f"size: {len(property_list)}")
    if not property_list:
        print("No supported property!")
        return
    print("\n" + "-" * 72)
    for i, item in enumerate(property_list):
        str_range = ""
        try:
            if item.type == OBPropertyType.OB_BOOL_PROPERTY:
                str_range = "Bool value(min:0, max:1, step:1)"
            elif item.type == OBPropertyType.OB_INT_PROPERTY:
                if item.permission & OBPermissionType.PERMISSION_READ:
                    int_range = device.get_int_property_range(item.id)
                    str_range = f"Int value(min:{int_range.min}, max:{int_range.max}, step:{int_range.step})"
                else:
                    str_range = "Int value"
            elif item.type == OBPropertyType.OB_FLOAT_PROPERTY:
                float_range = device.get_float_property_range(item.id)
                str_range = f"Float value(min:{float_range.min:.2f}, max:{float_range.max:.2f}, step:{float_range.step:.2f})"
        except Exception:
            str_range = "get range failed"

        print(f"{i:02d}. {item.name}({int(item.id)}), "
              f"permission={permission_type_to_string(item.permission)}, "
              f"range={str_range}")
    print("-" * 72 + "\n")

# Get property value
def get_property_value(device, item):
    try:
        val = None
        if item.type == OBPropertyType.OB_BOOL_PROPERTY:
            val = device.get_bool_property(item.id)
        elif item.type == OBPropertyType.OB_INT_PROPERTY:
            val = device.get_int_property(item.id)
        elif item.type == OBPropertyType.OB_FLOAT_PROPERTY:
            val = device.get_float_property(item.id)
        print(f"property name: {item.name}, get value: {val}")
    except Exception as e:
        print(f"get property failed: {item.name}, error: {e}")

# Set properties
def set_property_value(device, item, str_value):
    try:
        val = None
        if item.type == OBPropertyType.OB_BOOL_PROPERTY:
            val = int(str_value)
            device.set_bool_property(item.id, bool(val))
        elif item.type == OBPropertyType.OB_INT_PROPERTY:
            val = int(str_value)
            device.set_int_property(item.id, val)
        elif item.type == OBPropertyType.OB_FLOAT_PROPERTY:
            val = float(str_value)
            device.set_float_property(item.id, val)
        print(f"property name: {item.name}, set value: {val} success")
    except Exception as e:
        print(f"set property failed: {item.name}, error: {e}")

def main():
    try:
        # Create a Context.
        ctx = Context()

        # Query the list of connected devices
        device_list = ctx.query_devices()

        # Found no device
        if device_list.get_count() <= 0:
            print("Device Not Found")
            return

        # If a single device is plugged in, the first one is selected by default
        # Otherwise, select a device from the list
        device = select_device(device_list) if device_list.get_count() > 1 else device_list.get_device_by_index(0)

        # Check LiDAR device
        if not is_lidar_device(device):
            print("Invalid device, please connect a LiDAR device!")
            return

        # Get and print device information
        info = device.get_device_info()
        print("\n" + "-" * 72)
        print(f"Current Device: name: {info.get_name()}, vid: 0x{info.get_vid():x}, pid: 0x{info.get_pid():04x}, uid: {info.get_uid()}")

        # Enter property control loop
        print("Input '?' to get all properties.")
        print("Input 'exit' to exit the program.")

        # Get property list
        property_list = get_property_list(device)
        # Sort property list by ID
        property_list.sort(key=lambda x: x.id.value)

        while True:
            choice = input("\n>> ").strip()
            if not choice:
                continue

            # Exit the program
            if choice == "exit":
                break
            
            # Show all properties
            if choice == "?":
                printf_property_list(device, property_list)
                print("Please select property. (Usage: [index] [set/get] [value])")
                continue

            # Parse input and check if it matches the input format
            parts = choice.split()
            try:
                idx = int(parts[0])
                if idx >= len(property_list):
                    print("Your selection is out of range, please reselect.")
                    continue
                
                item = property_list[idx]
                cmd = parts[1].lower()

                if cmd == "get":
                    # get property value
                    get_property_value(device, item)
                elif cmd == "set" and len(parts) >= 3:
                    # set property value
                    set_property_value(device, item, parts[2])
                else:
                    print("Property control usage: [property index] [set] [property value] or [property index] [get]")
            except (ValueError, IndexError):
                print("Invalid input format.")

    except Exception as e:
        print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    main()