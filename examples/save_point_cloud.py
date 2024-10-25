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
import numpy as np
import open3d as o3d

from pyorbbecsdk import *

save_points_dir = os.path.join(os.getcwd(), "point_clouds")
if not os.path.exists(save_points_dir):
    os.mkdir(save_points_dir)


def convert_to_o3d_point_cloud(points, colors=None):
    """
    Converts numpy arrays of points and colors (if provided) into an Open3D point cloud object.
    """
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    if colors is not None:
        pcd.colors = o3d.utility.Vector3dVector(colors / 255.0)  # Normalize colors to range [0, 1]
    return pcd


def save_points_to_ply(points, colors, file_name) -> int:
    """
    Save numpy array points to PLY file using Open3D.
    """
    if points is None or len(points) == 0:
        print("No points to save.")
        return 0

    # Convert points and colors (if available) to Open3D point cloud object
    pcd = convert_to_o3d_point_cloud(points, colors)
    
    # Save the point cloud in PLY format
    o3d.io.write_point_cloud(file_name, pcd)
    print(f"Point cloud saved to: {file_name}")
    
    return 1


def main():
    pipeline = Pipeline()
    config = Config()
    
    # Configure depth stream
    depth_profile_list = pipeline.get_stream_profile_list(OBSensorType.DEPTH_SENSOR)
    if depth_profile_list is None:
        print("No proper depth profile, cannot generate point cloud")
        return
    depth_profile = depth_profile_list.get_default_video_stream_profile()
    config.enable_stream(depth_profile)

    has_color_sensor = False
    try:
        # Configure color stream if available
        profile_list = pipeline.get_stream_profile_list(OBSensorType.COLOR_SENSOR)
        if profile_list is not None:
            color_profile = profile_list.get_default_video_stream_profile()
            config.enable_stream(color_profile)
            has_color_sensor = True
    except OBError as e:
        print(e)

    pipeline.enable_frame_sync()
    pipeline.start(config)
    
    #camera_param = pipeline.get_camera_param()
    align_filter = AlignFilter(align_to_stream=OBStreamType.COLOR_STREAM)
    point_cloud_filter = PointCloudFilter()
    #point_cloud_filter.set_camera_param(camera_param)

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
        #scale = depth_frame.get_depth_scale()
        #point_cloud_filter.set_position_data_scaled(scale)

        point_format = OBFormat.RGB_POINT if has_color_sensor and color_frame is not None else OBFormat.POINT
        point_cloud_filter.set_create_point_format(point_format)

        point_cloud_frame = point_cloud_filter.process(frame)
        points = point_cloud_filter.calculate(point_cloud_frame)
        
        # Prepare points and colors (if available)
        points_array = np.array([p[:3] for p in points])  # XYZ points
        colors_array = np.array([p[3:6] for p in points]) if has_color_sensor else None  # RGB colors if available
        
        # Save the point cloud data to PLY
        save_points_to_ply(points_array, colors_array, os.path.join(save_points_dir, "point_cloud.ply"))
        break
    print("stop pipeline")
    pipeline.stop()


if __name__ == "__main__":
    main()
