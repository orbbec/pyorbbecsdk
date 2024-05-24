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

save_points_dir = os.path.join(os.getcwd(), "point_clouds")
if not os.path.exists(save_points_dir):
    os.mkdir(save_points_dir)


def save_points_to_ply(points, file_name) -> int:
    # save numpy array to ply file
    if points is None:
        return 0
    num_points = len(points)
    if num_points == 0:
        return 0
    # if has color, save as color point cloud
    if len(points[0]) == 6:
        vertices = np.zeros(num_points, dtype=[('x', 'f4'), ('y', 'f4'), ('z', 'f4'),
                                               ('red', 'u1'), ('green', 'u1'), ('blue', 'u1')])
    else:
        vertices = np.zeros(num_points, dtype=[('x', 'f4'), ('y', 'f4'), ('z', 'f4')])

    for i in range(num_points):
        vertices[i] = tuple(points[i])
    el = PlyElement.describe(vertices, 'vertex')
    PlyData([el], text=True).write(file_name)

    return 1


def main():
    pipeline = Pipeline()
    config = Config()
    depth_profile_list = pipeline.get_stream_profile_list(OBSensorType.DEPTH_SENSOR)
    if depth_profile_list is None:
        print("No proper depth profile, can not generate point cloud")
        return
    depth_profile = depth_profile_list.get_default_video_stream_profile()
    config.enable_stream(depth_profile)
    has_color_sensor = False
    try:
        profile_list = pipeline.get_stream_profile_list(OBSensorType.COLOR_SENSOR)
        if profile_list is not None:
            color_profile = profile_list.get_default_video_stream_profile()
            config.enable_stream(color_profile)
            has_color_sensor = True
    except OBError as e:
        print(e)
    pipeline.enable_frame_sync()
    pipeline.start(config)
    camera_param = pipeline.get_camera_param()
    align_filter = AlignFilter(align_to_stream=OBStreamType.COLOR_STREAM)
    point_cloud_filter = PointCloudFilter()
    point_cloud_filter.set_camera_param(camera_param)
    while True:
        frames = pipeline.wait_for_frames(100)
        if frames is None:
            continue
        depth_frame = frames.get_depth_frame()
        if depth_frame is None:
            continue
        color_frame = frames.get_color_frame()
        if has_color_sensor and color_frame is None:
            continue
        frame = align_filter.process(frames)
        scale = depth_frame.get_depth_scale()
        point_cloud_filter.set_position_data_scaled(scale)

        point_cloud_filter.set_create_point_format(
            OBFormat.RGB_POINT if has_color_sensor and color_frame is not None else OBFormat.POINT)
        point_cloud_frame = point_cloud_filter.process(frame)
        points = point_cloud_filter.calculate(point_cloud_frame)
        save_points_to_ply(points, os.path.join(save_points_dir, "point_cloud.ply"))
        print("point cloud saved to: ", os.path.join(save_points_dir, "point_cloud.ply"))
        break

    pipeline.stop()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
