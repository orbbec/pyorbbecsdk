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

import threading
import time
from typing import Optional

from pyorbbecsdk import *

# Global variables
device: Optional[Device] = None
pipeline: Optional[Pipeline] = None
device_lock = threading.Lock()

def start_stream(device: Device):
    """Starts the stream for both color and depth sensors."""
    global pipeline
    if device is None:
        print("No device connected")
        return
   
    config = Config()
    print("Try to reset pipeline")
    pipeline = Pipeline(device)
    print("Try to enable color stream")
    # Enable color stream
    try:
        profile_list = pipeline.get_stream_profile_list(OBSensorType.COLOR_SENSOR)
        color_profile = profile_list.get_default_video_stream_profile()
        config.enable_stream(color_profile)
    except Exception as e:
        print(f"Failed to enable color stream: {e}")
    
    # Enable depth stream
    try:
        profile_list = pipeline.get_stream_profile_list(OBSensorType.DEPTH_SENSOR)
        depth_profile = profile_list.get_default_video_stream_profile()
        config.enable_stream(depth_profile)
    except Exception as e:
        print(f"Failed to enable depth stream: {e}")
    
    print("Starting the stream...")
    pipeline.start(config)

def stop_stream():
    """Stops the pipeline if it is running."""
    global pipeline
    if pipeline is None:
        print("Pipeline is not started")
        return
    pipeline.stop()
    pipeline = None

def on_device_connected_callback(device_list: DeviceList):
    """Callback when a new device is connected."""
    global device
    if len(device_list) == 0:
        return
    
    print("Device connected")
    with device_lock:
        if device is not None:
            print("Device is already connected")
            return
        
        # Get the first available device and start the stream
        print("Try to get device")
        device = device_list[0]
        print("Try to start stream")
        start_stream(device)
        print("Start stream successfully")

def on_device_disconnected_callback(device_list: DeviceList):
    """Callback when a device is disconnected."""
    global device, pipeline
    if len(device_list) == 0:
        return
    
    print("Device disconnected")
    try:
        with device_lock:
            print("reset device ...")
            device = None
            print("reset device successfully")
    except OBError as e:
        print(e)
    print("Device disconnected successfully")

def on_new_frame_callback(frame: Frame):
    """Handles new frames captured by the sensors."""
    if frame is None:
        return
    print(f"{frame.get_type()} frame, width={frame.get_width()}, height={frame.get_height()}, format={frame.get_format()}, timestamp={frame.get_timestamp_us()}us")

def on_device_changed_callback(disconn_device_list: DeviceList, conn_device_list: DeviceList):
    """Handles device changes by invoking appropriate connect/disconnect callbacks."""
    on_device_connected_callback(conn_device_list)
    on_device_disconnected_callback(disconn_device_list)

def main():
    """Main program loop to handle device connection and frame processing."""
    ctx = Context()
    
    # Set callback for device changes (connect/disconnect)
    ctx.set_device_changed_callback(on_device_changed_callback)
    
    # Check for currently connected devices
    device_list = ctx.query_devices()
    on_device_connected_callback(device_list)
    
    global pipeline, device

    while True:
        try:
            with device_lock:
                if pipeline is not None and device is not None:
                    # Wait for a new set of frames
                    frames: FrameSet = pipeline.wait_for_frames(100)
                else:
                    continue
            if frames is None:
                time.sleep(0.001)  # Avoid busy waiting
                continue
            
            # Get color and depth frames
            color_frame = frames.get_color_frame()
            depth_frame = frames.get_depth_frame()
            
            # Process each frame
            on_new_frame_callback(color_frame)
            on_new_frame_callback(depth_frame)
        except KeyboardInterrupt:
            break
        except OBError as e:
            print(f"Error during frame capture: {e}")
            continue
    
    # Stop the pipeline on exit
    print("Stopping the pipeline...")
    try:
        if pipeline is not None:
            pipeline.stop()
    except OBError as e:
        print(f"Error during pipeline stop: {e}")

if __name__ == "__main__":
    main()
