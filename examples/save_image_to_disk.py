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
import os

import cv2
import numpy as np

from pyorbbecsdk import *
from utils import frame_to_bgr_image


def save_depth_frame(frame: DepthFrame, index):
    if frame is None:
        return
    width = frame.get_width()
    height = frame.get_height()
    timestamp = frame.get_timestamp()
    scale = frame.get_depth_scale()
    depth_format = frame.get_format()
    if depth_format != OBFormat.Y16:
        print("depth format is not Y16")
        return
    data = np.frombuffer(frame.get_data(), dtype=np.uint16)
    data = data.reshape((height, width))
    data = data.astype(np.float32) * scale
    data = data.astype(np.uint16)
    save_image_dir = os.path.join(os.getcwd(), "depth_images")
    if not os.path.exists(save_image_dir):
        os.mkdir(save_image_dir)
    filename = save_image_dir + "/depth_{}x{}_{}_{}.png".format(width, height, index, timestamp)
    params = [cv2.IMWRITE_PNG_COMPRESSION, 0]
    cv2.imwrite(filename, data, params)
    print(f"Depth saved: {filename}")

def save_color_frame(frame: ColorFrame, index):
    if frame is None:
        return
    width = frame.get_width()
    height = frame.get_height()
    timestamp = frame.get_timestamp()
    save_image_dir = os.path.join(os.getcwd(), "color_images")
    if not os.path.exists(save_image_dir):
        os.mkdir(save_image_dir)
    filename = save_image_dir + "/color_{}x{}_{}_{}.png".format(width, height, index, timestamp)
    image = frame_to_bgr_image(frame)
    if image is None:
        print("failed to convert frame to image")
        return
    cv2.imwrite(filename, image)
    print(f"Color saved: {filename}")

def main():
    pipeline = Pipeline()
    config = Config()
    saved_color_cnt: int = 0
    saved_depth_cnt: int = 0
    has_color_sensor = False
    try:
        profile_list = pipeline.get_stream_profile_list(OBSensorType.COLOR_SENSOR)
        if profile_list is not None:
            color_profile: VideoStreamProfile = profile_list.get_default_video_stream_profile()
            config.enable_stream(color_profile)
            has_color_sensor = True
        depth_profile_list = pipeline.get_stream_profile_list(OBSensorType.DEPTH_SENSOR)
        if depth_profile_list is not None:
            depth_profile = depth_profile_list.get_default_video_stream_profile()
            config.enable_stream(depth_profile)
        config.set_frame_aggregate_output_mode(OBFrameAggregateOutputMode.FULL_FRAME_REQUIRE)
    except OBError as e:
        print(e)
    pipeline.start(config)
    
    print("Waiting for sensor to stabilize...")
    for _ in range(15):
        pipeline.wait_for_frames(1000)
        
    frame_index = 0
    try:
        while True:
            frames = pipeline.wait_for_frames(1000)
            if frames is None:
                continue
            frame_index += 1
            if frame_index >= 5:
                print("The demo is over!")
                break
            
            color_frame = frames.get_color_frame()
            depth_frame = frames.get_depth_frame()
            
            if color_frame:
                save_color_frame(color_frame, frame_index)
            if depth_frame:
                save_depth_frame(depth_frame, frame_index)
    except KeyboardInterrupt:
        pass
    except OBError as e:
        print(e)
    finally:
        pipeline.stop()
        print("Pipeline stopped.")
        
if __name__ == "__main__":
    main()
