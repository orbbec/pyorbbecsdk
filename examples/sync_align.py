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
import argparse
import sys

import cv2
import numpy as np

from pyorbbecsdk import *
from utils import frame_to_bgr_image

ESC_KEY = 27

MIN_DEPTH = 20  # 20mm
MAX_DEPTH = 10000  # 10000mm
# Temporal filter for smoothing depth data over time

def main(argv):
    pipeline = Pipeline()
    config = Config()
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--enable_sync", help="enable sync", type=bool, default=True)
    args = parser.parse_args(argv)

    enable_sync = args.enable_sync
    try:
        profile_list = pipeline.get_stream_profile_list(OBSensorType.COLOR_SENSOR)
        color_profile = profile_list.get_default_video_stream_profile()
        config.enable_stream(color_profile)
        profile_list = pipeline.get_stream_profile_list(OBSensorType.DEPTH_SENSOR)
        depth_profile = profile_list.get_default_video_stream_profile()
        config.enable_stream(depth_profile)
    except Exception as e:
        print(e)
        return

    if enable_sync:
        try:
            pipeline.enable_frame_sync()
        except Exception as e:
            print(e)

    try:
        pipeline.start(config)
    except Exception as e:
        print(e)
        return

    align_filter = AlignFilter(align_to_stream=OBStreamType.COLOR_STREAM)

    while True:
        try:
            frames = pipeline.wait_for_frames(100)
            if not frames:
                continue
            color_frame = frames.get_color_frame()
            depth_frame = frames.get_depth_frame()
            if not color_frame or not depth_frame:
                continue
            frames = align_filter.process(frames)
            if not frames:
                continue
            frames  = frames.as_frame_set()
            color_frame = frames.get_color_frame()
            depth_frame = frames.get_depth_frame()
            if not color_frame or not depth_frame:
                continue

            color_image = frame_to_bgr_image(color_frame)
            if color_image is None:
                print("Failed to convert frame to image")
                continue
            try:
                depth_data = np.frombuffer(depth_frame.get_data(), dtype=np.uint16).reshape(
                    (depth_frame.get_height(), depth_frame.get_width()))
            except ValueError:
                print("Failed to reshape depth data")
                continue
            depth_data = depth_data.astype(np.float32) * depth_frame.get_depth_scale()
            depth_data = np.where((depth_data > MIN_DEPTH) & (depth_data < MAX_DEPTH), depth_data, 0)
            depth_data = depth_data.astype(np.uint16)
            depth_image = cv2.normalize(depth_data, None, 0, 255, cv2.NORM_MINMAX)
            depth_image = cv2.applyColorMap(depth_image.astype(np.uint8), cv2.COLORMAP_JET)
            depth_image = cv2.addWeighted(color_image, 0.5, depth_image, 0.5, 0)

            cv2.imshow("SyncAlignViewer", depth_image)
            if cv2.waitKey(1) in [ord('q'), ESC_KEY]:
                break
        except KeyboardInterrupt:
            break
    cv2.destroyAllWindows()
    pipeline.stop()


if __name__ == "__main__":
    main(sys.argv[1:])
