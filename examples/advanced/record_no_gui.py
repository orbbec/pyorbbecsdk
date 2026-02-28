# ******************************************************************************
#  pyorbbecsdk Advanced Example — Headless Recorder (No GUI)
#
#  What you will learn:
#    1. How to record all streams to a .bag file without any display window
#    2. How to count frames per stream type using lightweight callbacks
#    3. How to calculate and print per-stream FPS during recording
#
#  Keyboard: Ctrl+C to stop
#
#  Device requirement: All
#
#  Run:
#    python examples/advanced/record_no_gui.py
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
