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

from pyorbbecsdk import *
import cv2
import numpy as np
from utils import frame_to_bgr_image

def get_stream_config(pipeline: Pipeline):
    config = Config()
    try:
        profile_list = pipeline.get_stream_profile_list(OBSensorType.COLOR_SENSOR)
        assert profile_list is not None
        for i in range(len(profile_list)):
            color_profile = profile_list[i]
            if color_profile.get_format() != OBFormat.RGB:
                continue
            hw_d2c_profile_list = pipeline.get_d2c_depth_profile_list(color_profile, OBAlignMode.HW_MODE)
            if len(hw_d2c_profile_list) == 0:
                continue
            hw_d2c_profile = hw_d2c_profile_list[0]
            print("hw_d2c_profile: ", hw_d2c_profile)
            config.enable_stream(hw_d2c_profile)
            config.enable_stream(color_profile)
            config.set_align_mode(OBAlignMode.HW_MODE)
            return config
    except Exception as e:
        print(e)
        return None
    return None

def main():
    pipeline = Pipeline()
    config = get_stream_config(pipeline)
    if config is None:
        return
    pipeline.start(config)
    
    while True:
        frames = pipeline.wait_for_frames(100)
        if frames is None:
            continue
        
        color_frame = frames.get_color_frame()
        depth_frame = frames.get_depth_frame()
        if not color_frame or not depth_frame:
            continue

        color_image = frame_to_bgr_image(color_frame)
        if color_image is None:
            print("Failed to convert frame to image")
            continue

        depth_data = np.frombuffer(depth_frame.get_data(), dtype=np.uint16).reshape(
            (depth_frame.get_height(), depth_frame.get_width()))
        depth_data = depth_data.astype(np.float32) * depth_frame.get_depth_scale()
        depth_image = cv2.normalize(depth_data, None, 0, 10000, cv2.NORM_MINMAX)
        depth_image = cv2.applyColorMap(depth_image.astype(np.uint8), cv2.COLORMAP_JET)
        depth_image = cv2.addWeighted(color_image, 0.5, depth_image, 0.5, 0)

        cv2.imshow("HW D2C Align Viewer", depth_image)
        if cv2.waitKey(1) in [ord('q'), 27]:  # 27 is the ESC key
            break

    pipeline.stop()

if __name__ == "__main__":
    main()