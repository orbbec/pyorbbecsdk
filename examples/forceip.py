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

def get_ip_config():
    """Get the new IP configuration from user input"""
    cfg = OBDeviceIpAddrConfig()
    cfg.dhcp = 0  # Static IP configuration

    print("Please enter the network configuration information:")

    # Get and validate IP address
    while True:
        val = input("Enter IP address: ")
        parts = val.split(".")
        if len(parts) == 4 and all(p.isdigit() and 0 <= int(p) <= 255 for p in parts):
            cfg.address = val
            break
        print("Invalid format.")

    # Get and validate Subnet Mask
    while True:
        val = input("Enter Subnet Mask: ")
        parts = val.split(".")
        if len(parts) == 4 and all(p.isdigit() and 0 <= int(p) <= 255 for p in parts):
            cfg.netmask = val
            break
        print("Invalid format.")

    # Get and validate Gateway address
    while True:
        val = input("Enter Gateway address: ")
        parts = val.split(".")
        if len(parts) == 4 and all(p.isdigit() and 0 <= int(p) <= 255 for p in parts):
            cfg.gateway = val
            break
        print("Invalid format.")

    return cfg

def select_device(device_list):
    """Select a device to operate, specifically filtering for Ethernet devices"""
    device_count = device_list.get_count()
    if device_count == 0:
        print("No devices found.")
        return -1

    index_list = []
    ethernet_dev_num = 0

    print("Ethernet device list:")
    for i in range(device_count):
        conn_type = device_list.get_device_connection_type_by_index(i)
        # Only show and allow selection of Ethernet-connected devices
        if conn_type != "Ethernet":
            continue

        print(f"{ethernet_dev_num}. Name: {device_list.get_device_name_by_index(i)}, "
              f"Mac: 0x{device_list.get_device_uid_by_index(i)}, "
              f"Serial Number: {device_list.get_device_serial_number_by_index(i)}, "
              f"IP: {device_list.get_device_ip_address_by_index(i)}, "
              f"Subnet Mask: {device_list.get_device_subnet_mask_by_index(i)}, "
              f"Gateway: {device_list.get_device_gateway_by_index(i)}")
        index_list.append(i)
        ethernet_dev_num += 1

    if not index_list:
        print("No network devices found.")
        return -1

    # User input loop for device selection
    while True:
        try:
            choice = int(input("Enter your choice: "))
            if 0 <= choice < len(index_list):
                return index_list[choice]
            else:
                print("Invalid input, please enter a valid index number.")
        except ValueError:
            print("Invalid input, please enter a number.")
    return -1

def main():
    try:
        # Create a Context object to interact with Orbbec devices
        context = Context()
        # Query the list of connected devices
        device_list = context.query_devices()
        
        # Select a device to operate
        device_number = select_device(device_list)
        
        if device_number != -1:
            # Get the new IP configuration from user input
            config = get_ip_config()
            
            # Change device IP configuration (Force IP)
            # This is typically used when the device is on a different subnet
            device_uid = device_list.get_device_uid_by_index(device_number)
            device_status = context.ob_force_ip_config(device_uid, config)
            
            if device_status is not True:
                print("Failed to apply the new IP configuration.")
            else:
                print("The new IP configuration has been successfully applied to the device.")
                
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()