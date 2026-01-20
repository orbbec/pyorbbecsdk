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
import time
import threading
from pyorbbecsdk import *
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import is_lidar_device

# Select a device: the name, vid, pid, uid, and sn of the device will be printed.
# The corresponding device object will be returned after selection.
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

def main():
    try:
        # Create a context for getting devices and sensors
        ctx = Context()
        
        # Query the list of connected devices
        device_list = ctx.query_devices()
        if device_list.get_count() < 1:
            print("No device found! Please connect a supported device and retry.")
            return

        # Select device: default to the first one if only one is connected
        if device_list.get_count() == 1:
            device = device_list.get_device_by_index(0)
        else:
            device = select_device(device_list)

        # Check if the selected device is a LiDAR device
        if not is_lidar_device(device):
            print("Invalid device, please connect a LiDAR device!")
            return

        print("\n" + "-" * 72)
        # Get output filename from user
        file_path = input("Please enter the output filename (with .bag extension): ").strip()
        if not file_path.endswith(".bag"):
            file_path += ".bag"

        # Create a pipeline for the specified device
        pipe = Pipeline(device)
        
        # Create a config and enable all available streams
        config = Config()
        sensor_list = device.get_sensor_list()
        
        for i in range(sensor_list.get_count()):
            sensor = sensor_list.get_sensor_by_index(i)
            sensor_type = sensor.get_type()
            # Enable stream based on the sensor type
            config.enable_stream(sensor_type)

        # Mutex and map for thread-safe frame counting
        frame_mutex = threading.Lock()
        frame_count_map = {}

        # Callback function for new frame sets
        def on_new_frame(frame_set):
            if frame_set is None:
                return
            with frame_mutex:
                for i in range(frame_set.get_count()):
                    frame = frame_set.get_frame_by_index(i)
                    if frame:
                        f_type = frame.get_type()
                        # Increment count for each frame type
                        frame_count_map[f_type] = frame_count_map.get(f_type, 0) + 1

        # Initialize the recording device with the output file path
        record_device = RecordDevice(device, file_path)
        
        # Start the pipeline with the configuration and callback
        pipe.start(config, on_new_frame)

        # Operation prompts
        print("Streams and recorder have started!")
        print("Press Ctrl+C to stop recording and exit safely.")
        print("IMPORTANT: Always exit safely to avoid bag file corruption.\n")

        start_time = time.time() * 1000  # Time in milliseconds
        wait_interval = 1000 # Initial statistics interval (1s)

        try:
            while True:
                time.sleep(0.05)
                current_time = time.time() * 1000
                
                # Periodically calculate and print FPS for each stream
                if current_time > start_time + wait_interval:
                    temp_count_map = {}
                    duration = 0
                    
                    with frame_mutex:
                        current_time = time.time() * 1000
                        duration = current_time - start_time
                        if frame_count_map:
                            start_time = current_time
                            wait_interval = 2000 # Change to 2s interval for subsequent prints
                            temp_count_map = frame_count_map.copy()
                            # Reset counts for the next interval
                            for k in frame_count_map:
                                frame_count_map[k] = 0

                    if not temp_count_map:
                        print("Recording... Current FPS: 0")
                    else:
                        fps_info = []
                        for f_type, count in temp_count_map.items():
                            rate = count / (duration / 1000.0)
                            fps_info.append(f"{f_type.name}={rate:.2f}")
                        print(f"Recording... Current FPS: {', '.join(fps_info)}")

        except KeyboardInterrupt:
            # Catch Ctrl+C to allow for clean shutdown
            print("\nStopping recording...")

        # Stop the pipeline
        pipe.stop()
        
        # Release the RecordDevice to flush and save the file
        record_device = None 
        print("Recording saved safely.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()