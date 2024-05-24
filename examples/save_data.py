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

import os

import cv2
import numpy as np
from plyfile import PlyData, PlyElement

from pyorbbecsdk import *
from utils import frame_to_bgr_image

# Directories for saving point clouds and images
save_points_dir = os.path.join(os.getcwd(), "point_clouds")
save_depth_image_dir = os.path.join(os.getcwd(), "depth_images")
save_color_image_dir = os.path.join(os.getcwd(), "color_images")

# Ensure directories exist
for dir_path in [save_points_dir, save_depth_image_dir, save_color_image_dir]:
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)


# Function to save point cloud data to PLY files
def save_points_to_ply(frames: FrameSet, camera_param: OBCameraParam, timestamp) -> int:
    points = frames.get_point_cloud(camera_param)
    if len(points) == 0:
        print("no depth points")
        return 0
    points_array = np.array([tuple(point) for point in points], dtype=[('x', 'f4'), ('y', 'f4'), ('z', 'f4')])
    points_filename = os.path.join(save_points_dir, f"points_{timestamp}.ply")
    el = PlyElement.describe(points_array, 'vertex')
    PlyData([el], text=True).write(points_filename)
    return 1


# Functions to save depth and color frames as image files
def save_depth_frame(frame: DepthFrame, index, timestamp):
    data = np.frombuffer(frame.get_data(), dtype=np.uint16).reshape((frame.get_height(), frame.get_width()))
    data = (data * frame.get_depth_scale()).astype(np.uint16)
    raw_filename = os.path.join(save_depth_image_dir,
                                f"depth_{frame.get_width()}x{frame.get_height()}_{index}_{timestamp}.raw")
    data.tofile(raw_filename)


def save_color_frame(frame: ColorFrame, index, timestamp):
    image = frame_to_bgr_image(frame)
    if image is None:
        print("failed to convert frame to image")
        return
    filename = os.path.join(save_color_image_dir,
                            f"color_{frame.get_width()}x{frame.get_height()}_{index}_{timestamp}.png")
    cv2.imwrite(filename, image)


# Main function to orchestrate saving point clouds and images
def main():
    pipeline = Pipeline()
    device = pipeline.get_device()
    config = Config()
    has_color_sensor = False
    # Configure pipeline
    try:
        depth_profile_list = pipeline.get_stream_profile_list(OBSensorType.DEPTH_SENSOR)
        if depth_profile_list:
            depth_profile = depth_profile_list.get_default_video_stream_profile()
            config.enable_stream(depth_profile)

        color_profile_list = pipeline.get_stream_profile_list(OBSensorType.COLOR_SENSOR)
        if color_profile_list:
            color_profile = color_profile_list.get_default_video_stream_profile()
            config.enable_stream(color_profile)
            has_color_sensor = True
        pipeline.start(config)
        pipeline.enable_frame_sync()
    except OBError as e:
        print(e)
        return

    # Data acquisition loop
    saved_color_cnt = saved_depth_cnt = 0
    try:
        while True:
            frames = pipeline.wait_for_frames(100)
            if frames is None:
                continue

            depth_frame = frames.get_depth_frame()
            color_frame = frames.get_color_frame() if has_color_sensor else None
            camera_param = pipeline.get_camera_param()

            if depth_frame and saved_depth_cnt < 1:
                timestamp = depth_frame.get_timestamp()
                saved_depth_cnt += save_points_to_ply(frames, camera_param, timestamp)
                save_depth_frame(depth_frame, saved_depth_cnt, timestamp)

            if color_frame and saved_color_cnt < 1:
                save_color_frame(color_frame, saved_color_cnt, color_frame.get_timestamp())
                saved_color_cnt += 1

            if saved_depth_cnt >= 1 and (not has_color_sensor or saved_color_cnt >= 1):
                break
    except KeyboardInterrupt:
        print("Interrupted by user")
    finally:
        pipeline.stop()


if __name__ == "__main__":
    main()
