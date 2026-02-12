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
from pyorbbecsdk import *

def permission_type_to_string(permission):
    """Convert permission type to display string (e.g., R/W)"""
    if permission == OBPermissionType.PERMISSION_READ:
        return "R/_"
    elif permission == OBPermissionType.PERMISSION_WRITE:
        return "_/W"
    elif permission == OBPermissionType.PERMISSION_READ_WRITE:
        return "R/W"
    else:
        return "_/_"

# Select a device, the name, pid, vid, uid of the device will be printed here, 
# and the corresponding device object will be returned after selection
def select_device(device_list):
    dev_count = device_list.get_count()
    print("Device list: ")
    for i in range(dev_count):
        print(f"{i}. name: {device_list.get_device_name_by_index(i)}, "
              f"vid: 0x{device_list.get_device_vid_by_index(i):X}, "
              f"pid: 0x{device_list.get_device_pid_by_index(i):04X}, "
              f"uid: 0x{device_list.get_device_uid_by_index(i)}, "
              f"sn: {device_list.get_device_serial_number_by_index(i)}")
    
    while True:
        try:
            dev_index = int(input("Select a device index: "))
            if 0 <= dev_index < dev_count:
                return device_list.get_device_by_index(dev_index)
        except ValueError:
            pass
        print("Your selection is out of range, please reselect.")

# Get property list
def get_property_list(device):
    property_vec = []
    size = device.get_support_property_count()
    for i in range(size):
        item = device.get_supported_property(i)
        # Filter for primary property types
        if item.type in [OBPropertyType.OB_BOOL_PROPERTY, 
                         OBPropertyType.OB_INT_PROPERTY, 
                         OBPropertyType.OB_FLOAT_PROPERTY]:
            if item.permission != OBPermissionType.PERMISSION_DENY:
                property_vec.append(item)
    return property_vec

# Print a list of supported properties
def print_property_list(device, property_list):
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
                r = device.get_int_property_range(item.id)
                str_range = f"Int value(min:{r.min}, max:{r.max}, step:{r.step})"
            elif item.type == OBPropertyType.OB_FLOAT_PROPERTY:
                r = device.get_float_property_range(item.id)
                str_range = f"Float value(min:{r.min:.2f}, max:{r.max:.2f}, step:{r.step:.2f})"
        except Exception:
            str_range = "get range failed"

        permission_str = permission_type_to_string(item.permission)
        print(f"{i:02d}. {item.name}({int(item.id)}), permission={permission_str}, range={str_range}")
    print("-" * 72)
    print('Input "?" to get all properties, or "exit" to quit.' + "\n")

def main():
    try:
        # Create a Context.
        ctx = Context()
        
        # Query the list of connected devices
        device_list = ctx.query_devices()

        while True:
            # select a device to operate
            if device_list.get_count() > 0:
                if device_list.get_count() == 1:
                    # If a single device is plugged in, the first one is selected by default
                    device = device_list.get_device_by_index(0)
                else:
                    device = select_device(device_list)
                
                info = device.get_device_info()
                print("\n" + "-" * 72)
                print(f"Current Device: name: {info.get_name()}, vid: 0x{info.get_vid():X}, "
                      f"pid: 0x{info.get_pid():04X}, uid: 0x{info.get_uid()}")
            else:
                print("Device Not Found")
                break

            print('Input "?" to get all properties, or "exit" to quit.')
            
            # Fetch and sort properties by ID
            property_list = get_property_list(device)
            property_list.sort(key=lambda x: x.id.value)

            while True:
                choice = input().strip()
                if not choice:
                    continue
                
                # exit the program
                if choice == "exit":
                    return

                if choice == "?":
                    print_property_list(device, property_list)
                    print("Please select property: (Usage: [index] [get/set] [value])")
                    continue

                # Check if it matches the input format
                control_vec = choice.split()
                if len(control_vec) < 2 or control_vec[1] not in ["get", "set"]:
                    print("Property control usage: [property index] [get] or [property index] [set] [value]")
                    continue

                try:
                    select_idx = int(control_vec[0])
                    if select_idx >= len(property_list):
                        print("Your selection is out of range, please reselect.")
                        continue
                    
                    item = property_list[select_idx]
                    is_get = control_vec[1] == "get"

                    if is_get:
                        # get property value
                        if item.type == OBPropertyType.OB_BOOL_PROPERTY:
                            val = int(device.get_bool_property(item.id))
                        elif item.type == OBPropertyType.OB_INT_PROPERTY:
                            val = device.get_int_property(item.id)
                        elif item.type == OBPropertyType.OB_FLOAT_PROPERTY:
                            val = device.get_float_property(item.id)
                        print(f"property name: {item.name}, get value: {val}")
                    else:
                        # set property value
                        if len(control_vec) < 3:
                            print("Please provide a value to set.")
                            continue
                        str_val = control_vec[2]
                        if item.type == OBPropertyType.OB_BOOL_PROPERTY:
                            device.set_bool_property(item.id, bool(int(str_val)))
                        elif item.type == OBPropertyType.OB_INT_PROPERTY:
                            device.set_int_property(item.id, int(str_val))
                        elif item.type == OBPropertyType.OB_FLOAT_PROPERTY:
                            device.set_float_property(item.id, float(str_val))
                        print(f"property name: {item.name}, set value success: {str_val}")

                except Exception as e:
                    print(f"Operation failed: {e}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()