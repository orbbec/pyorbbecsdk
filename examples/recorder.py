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

ESC_KEY = 27


def main():
    pipeline = Pipeline()
    config = Config()
    # enable depth stream
    try:
        profile_list = pipeline.get_stream_profile_list(OBSensorType.DEPTH_SENSOR)
        if profile_list is None:
            print("No depth sensor found")
            return
        profile = profile_list.get_default_video_stream_profile()
        config.enable_stream(profile)
    except Exception as e:
        print(e)
        return
    # enable color stream
    try:
        profile_list = pipeline.get_stream_profile_list(OBSensorType.COLOR_SENSOR)
        if profile_list is None:
            print("No color sensor found")
            return
        profile = profile_list.get_default_video_stream_profile()
        config.enable_stream(profile)
    except Exception as e:
        print(e)

    pipeline.start(config)
    pipeline.start_recording("./test.bag")
    while True:
        try:
            frames = pipeline.wait_for_frames(100)
            if frames is None:
                continue
            depth_frame = frames.get_depth_frame()
            if depth_frame is None:
                continue
            width = depth_frame.get_width()
            height = depth_frame.get_height()
            scale = depth_frame.get_depth_scale()

            depth_data = np.frombuffer(depth_frame.get_data(), dtype=np.uint16)
            depth_data = depth_data.reshape((height, width))
            depth_data = depth_data.astype(np.float32) * scale
            depth_image = cv2.normalize(depth_data, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
            depth_image = cv2.applyColorMap(depth_image, cv2.COLORMAP_JET)
            cv2.imshow("Depth Viewer", depth_image)
            key = cv2.waitKey(1)
            if key == ord('q') or key == ESC_KEY:
                pipeline.stop_recording()
                break
        except KeyboardInterrupt:
            pipeline.stop_recording()
            break
    pipeline.stop()


if __name__ == "__main__":
    main()
