from pyorbbecsdk import *
import cv2
import numpy as np


def save_points_to_ply(frame: FrameSet, camera_param: OBCameraParam):
    # FIXME:
    points = frame.covert_to_points(camera_param)
    if points is None:
        print("no depth points")
        return
    with open("points.ply", "w") as f:
        f.write("ply\n")
        f.write("format ascii 1.0\n")
        f.write("element vertex {}\n".format(len(points)))
        f.write("property float x\n")
        f.write("property float y\n")
        f.write("property float z\n")
        f.write("end_header\n")
        for point in points:
            f.write("{} {} {}\n".format(point.x, point.y, point.z))


def save_color_points_to_ply(frame: FrameSet, camera_param: OBCameraParam):
    # FIXME
    points = frame.get_color_points(camera_param)
    if points is None:
        print("no color points")
        return
    with open("color_points.ply", "w") as f:
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
            f.write("{} {} {} {} {} {}\n".format(point.x, point.y, point.z, point.r, point.g, point.b))


def main():
    pipeline = Pipeline()
    config = Config()
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
            config.set_align_mode(OBAlignMode.ALIGN_D2C_HW_MODE)

    except OBError as e:
        config.set_align_mode(OBAlignMode.ALIGN_D2C_DISABLE)
        print(e)

    pipeline.start(config)
    frame_cnt = 0
    while True:
        try:
            frames = pipeline.wait_for_frames(100)
            if frames is None:
                continue
            if frame_cnt > 1:
                break
            frame_cnt += 1
            camera_param = pipeline.get_camera_param()
            save_points_to_ply(frames, camera_param)
            save_color_points_to_ply(frames, camera_param)
        except OBError as e:
            print(e)
            break


if __name__ == "__main__":
    main()
