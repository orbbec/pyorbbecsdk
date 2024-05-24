# ******************************************************************************
#  Copyright (c) 2023 Orbbec 3D Technology, Inc
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

device: Optional[Device] = None
pipeline: Optional[Pipeline] = None

device_lock = threading.Lock()


def start_stream():
    global device
    global pipeline
    config = Config()
    if device is None:
        print("No device connected")
        return
    pipeline = Pipeline(device)
    print("try to enable stream")
    try:
        profile_list = pipeline.get_stream_profile_list(OBSensorType.COLOR_SENSOR)
        try:
            color_profile: VideoStreamProfile = profile_list.get_video_stream_profile(1280, 0, OBFormat.RGB, 30)
        except OBError as e:
            print(e)
            color_profile = profile_list.get_default_video_stream_profile()
        config.enable_stream(color_profile)
    except Exception as e:
        print(e)
    try:
        profile_list = pipeline.get_stream_profile_list(OBSensorType.DEPTH_SENSOR)
        try:
            depth_profile: VideoStreamProfile = profile_list.get_video_stream_profile(640, 0, OBFormat.Y16, 30)
        except OBError as e:
            print(e)
            depth_profile = profile_list.get_default_video_stream_profile()
        config.enable_stream(depth_profile)
    except Exception as e:
        print(e)
    print("try to start stream")
    pipeline.start(config)


def stop_stream():
    global pipeline
    if pipeline is None:
        print("Pipeline is not started")
        return
    pipeline.stop()
    pipeline = None


def on_device_connected_callback(device_list: DeviceList):
    if device_list.get_count() == 0:
        return
    global device
    print("Device connected")
    with device_lock:
        if device is not None:
            print("Device is already connected")
            return
        print("Try to get device")
        device = device_list.get_device_by_index(0)
        start_stream()


def on_device_disconnected_callback(device_list: DeviceList):
    global device, pipeline
    if device_list.get_count() == 0:
        return
    print("Device disconnected")
    with device_lock:
        device = None
        pipeline = None


def on_new_frame_callback(frame: Frame):
    if frame is None:
        return
    print("{} frame, width={}, height={}, format={}, timestamp={}us".format(frame.get_type(),
                                                                            frame.get_width(),
                                                                            frame.get_height(),
                                                                            frame.get_format(),
                                                                            frame.get_timestamp_us()))


def on_device_changed_callback(disconn_device_list: DeviceList, conn_device_list: DeviceList):
    on_device_connected_callback(conn_device_list)
    on_device_disconnected_callback(disconn_device_list)


def main():
    ctx = Context()
    ctx.set_device_changed_callback(on_device_changed_callback)
    device_list = ctx.query_devices()
    on_device_connected_callback(device_list)
    global pipeline, device

    while True:
        try:
            with device_lock:
                if pipeline is not None and device is not None:
                    frames: FrameSet = pipeline.wait_for_frames(100)
                else:
                    continue
            if frames is None:
                time.sleep(0.001)
                continue
            color_frame = frames.get_color_frame()
            depth_frame = frames.get_depth_frame()
            on_new_frame_callback(color_frame)
            on_new_frame_callback(depth_frame)
        except KeyboardInterrupt:
            break
    if pipeline is not None:
        pipeline.stop()


if __name__ == "__main__":
    main()
