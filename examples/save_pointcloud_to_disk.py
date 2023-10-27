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
import os

save_points_dir = os.path.join(os.getcwd(), "point_clouds")
if not os.path.exists(save_points_dir):
    os.mkdir(save_points_dir)


def save_points_to_ply(frames: FrameSet, camera_param: OBCameraParam) -> int:
    if frames is None:
        return 0
    depth_frame = frames.get_depth_frame()
    if depth_frame is None:
        return 0
    points = frames.convert_to_points(camera_param)
    if points is None or len(points) == 0:
        print("no depth points")
        return 0
    global save_points_dir
    points_filename = save_points_dir + "/points_{}.ply".format(depth_frame.get_timestamp())
    with open(points_filename, "w") as f:
        f.write("ply\n")
        f.write("format ascii 1.0\n")
        f.write("element vertex {}\n".format(len(points)))
        f.write("property float x\n")
        f.write("property float y\n")
        f.write("property float z\n")
        f.write("end_header\n")
        for point in points:
            f.write("{} {} {}\n".format(point.x, point.y, point.z))
    return 1


def save_color_points_to_ply(frames: FrameSet, camera_param: OBCameraParam) -> int:
    if frames is None:
        return 0
    depth_frame = frames.get_depth_frame()
    if depth_frame is None:
        return 0
    points = frames.convert_to_color_points(camera_param)
    if points is None or len(points) == 0:
        print("no color points")
        return 0
    global save_points_dir
    points_filename = save_points_dir + "/color_points_{}.ply".format(depth_frame.get_timestamp())
    with open(points_filename, "w") as f:
        f.write("ply\n")
        f.write("format ascii 1.0\n")
        f.write("element vertex {}\n".format(len(points)))
        f.write("property float x\n")
        f.write("property float y\n")
        f.write("property float z\n")
        f.write("property uchar red\n")
        f.write("property uchar green\n")
        f.write("property uchar blue\n")
        f.write("end_header\n")
        for point in points:
            f.write(
                "{} {} {} {} {} {}\n".format(point.x, point.y, point.z, point.r, point.g, point.b))

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
                #Femto Mega does not support hardware D2C, and it is changed to software D2C
               config.set_align_mode(OBAlignMode.SW_MODE)
            else:
               config.set_align_mode(OBAlignMode.HW_MODE)
            has_color_sensor = True
    except OBError as e:
        config.set_align_mode(OBAlignMode.DISABLE)
        print(e)

    pipeline.start(config)
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
