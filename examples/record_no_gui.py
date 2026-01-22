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

import cv2
import time
from threading import Lock

from pyorbbecsdk import *
from utils import is_astra_mini_device

class GlobalState:
    def __init__(self):
        self.recorder = None
state = GlobalState()

frame_mutex = Lock()
counts = {}

def sync_callback(frameset):
    with frame_mutex:
        for i in range(frameset.get_count()):
            f = frameset.get_frame_by_index(i)
            t = f.get_type()
            counts[t] = counts.get(t, 0) + 1

def setup_camera(file_path):
    """Setup camera and stream configuration"""
    pipeline = Pipeline()
    config = Config()
    device = pipeline.get_device()
    try:
        device.timer_sync_with_host()
    except OBError as e:
        print(e)
    
    state.recorder = RecordDevice(device, file_path)
    print("Streams and recorder have started!")
    print("Press 'Ctrl + C' to stop and save.")
    
    device_info = device.get_device_info()

    # Try to enable all possible sensors
    sensor_list = device.get_sensor_list()
    for sensor in range(len(sensor_list)):
            sensor_type = sensor_list[sensor].get_type()
            if is_astra_mini_device(device_info.get_vid(), device_info.get_pid()) and sensor_type == OBSensorType.IR_SENSOR:
                continue
            try: 
                config.enable_stream(sensor_type)
            except: 
                continue

    pipeline.start(config, sync_callback)
    return pipeline
  
def main(): 
    file_path = input("Enter output filename (.bag) and press Enter to start recording: ")
    try:  
        # Initialize camera
        pipeline = setup_camera(file_path)
        last_time = time.time()
        
        while True:
            time.sleep(2) 
            with frame_mutex:
                curr_time = time.time()
                duration = curr_time - last_time
                for f_type, count in counts.items():
                    print(f"{f_type}: {count/duration:.2f} FPS", end=" ")
                    print()
                print()
                counts.clear()
                last_time = curr_time
    
    except KeyboardInterrupt:
        print("Stopping recording...")
    except Exception as e:
        print(f"Error: {str(e)}")
    # Clean up
    finally:
        if state.recorder:
            state.recorder = None
        pipeline.stop()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
