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
os.makedirs(save_points_dir, exist_ok=True)


def convert_to_o3d_point_cloud(points, colors=None):
    """
    Converts numpy arrays of points and colors (if provided) into an Open3D point cloud object.
    """
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    if colors is not None:
        pcd.colors = o3d.utility.Vector3dVector(colors / 255.0)  # Assuming colors are in [0, 255]
    return pcd


def save_points_to_ply(frames: FrameSet, camera_param: OBCameraParam):
    """
    Saves the point cloud data to a PLY file using Open3D.
    """
    if frames is None:
        return 0
    depth_frame = frames.get_depth_frame()
    if depth_frame is None:
        return 0
    points = frames.get_point_cloud(camera_param)
    if points is None or len(points) == 0:
        print("No points to save.")
        return 0
    # Convert points to Open3D point cloud
    pcd = convert_to_o3d_point_cloud(np.array(points))
    points_filename = os.path.join(save_points_dir, f"points_{depth_frame.get_timestamp()}.ply")
    # Save to PLY file
    o3d.io.write_point_cloud(points_filename, pcd)
    return 1


def save_color_points_to_ply(frames: FrameSet, camera_param: OBCameraParam):
    """
    Saves the color point cloud data to a PLY file using Open3D.
    """
    if frames is None:
        return 0
    depth_frame = frames.get_depth_frame()
    if depth_frame is None:
        return 0
    points = frames.get_color_point_cloud(camera_param)
    if points is None or len(points) == 0:
        print("No color points to save.")
        return 0
    # Assuming the color information is included in the points array
    # This part might need to be adjusted based on the actual format of the points array
    xyz = np.array(points[:, :3])
    colors = np.array(points[:, 3:], dtype=np.uint8)
    pcd = convert_to_o3d_point_cloud(xyz, colors)
    points_filename = os.path.join(save_points_dir, f"color_points_{depth_frame.get_timestamp()}.ply")
    # Save to PLY file
    o3d.io.write_point_cloud(points_filename, pcd)
    return 1


def main():
    pipeline = Pipeline()
    device = pipeline.get_device()
    device_info = device.get_device_info()
    device_pid = device_info.get_pid()
    config = Config()
    has_color_sensor = False
    depth_profile_list = pipeline.get_stream_profile_list(OBSensorType.DEPTH_SENSOR)
    if depth_profile_list is None:
        print("No proper depth profile, can not generate point cloud")
        return
    depth_profile = depth_profile_list.get_default_video_stream_profile()
    config.enable_stream(depth_profile)
    try:
        profile_list = pipeline.get_stream_profile_list(OBSensorType.COLOR_SENSOR)
        if profile_list is not None:
            color_profile: VideoStreamProfile = profile_list.get_default_video_stream_profile()
            config.enable_stream(color_profile)
            if device_pid == 0x066B:
                # Femto Mega does not support hardware D2C, and it is changed to software D2C
                config.set_align_mode(OBAlignMode.SW_MODE)
            else:
                config.set_align_mode(OBAlignMode.HW_MODE)
            has_color_sensor = True
    except OBError as e:
        config.set_align_mode(OBAlignMode.DISABLE)
        print(e)

    pipeline.start(config)
    pipeline.enable_frame_sync()
    saved_color_cnt: int = 0
    saved_depth_cnt: int = 0
    while True:
        try:
            frames = pipeline.wait_for_frames(100)
            if frames is None:
                continue
            camera_param = pipeline.get_camera_param()
            saved_depth_cnt += save_points_to_ply(frames, camera_param)
            if has_color_sensor:
                saved_color_cnt += save_color_points_to_ply(frames, camera_param)
            if has_color_sensor:
                if saved_color_cnt >= 5 and saved_depth_cnt >= 5:
                    break
            elif saved_depth_cnt >= 5:
                break
        except OBError as e:
            print(e)
            break


if __name__ == "__main__":
    main()
