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

import threading
import time
from typing import Optional

from pyorbbecsdk import *

# Global variables
device: Optional[Device] = None
pipeline: Optional[Pipeline] = None
device_lock = threading.Lock()

def print_device_list(prompt: str, device_list: DeviceList):
    count = len(device_list)
    if count == 0:
        return

    print(f"{count} device(s) {prompt}:")
    for i in range(count):
        try:
            uid = device_list.get_device_uid_by_index(i)
            vid = device_list.get_device_vid_by_index(i)
            pid = device_list.get_device_pid_by_index(i)
            sn  = device_list.get_device_serial_number_by_index(i)
            conn = device_list.get_device_connection_type_by_index(i)

            print(
                f" - uid: {uid}, "
                f"vid: 0x{vid:04x}, "
                f"pid: 0x{pid:04x}, "
                f"serial number: {sn}, "
                f"connection: {conn}"
            )
        except Exception as e:
            print(f" - failed to read device list info: {e}")
    print("")


def on_device_changed_callback(removed_list: DeviceList, added_list: DeviceList):
    print_device_list("added", added_list)
    print_device_list("removed", removed_list)


def main():
    print("Create Context")
    ctx = Context()

    print("Register device changed callback")
    ctx.set_device_changed_callback(on_device_changed_callback)

    print("Query current device list")
    current_list = ctx.query_devices()
    print_device_list("connected", current_list)

    print("Press Ctrl+C to exit.")
    print("You can manually unplug / plugin device to trigger callbacks.\n")

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nExit.")


if __name__ == "__main__":
    main()
