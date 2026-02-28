# ******************************************************************************
#  pyorbbecsdk Beginner Example 05 — 3D Point Cloud
#
#  What you will learn:
#    1. How to enable PointCloudFilter to generate a 3D point cloud
#    2. How to use AlignFilter to get a colored point cloud (RGB + XYZ)
#    3. How to save the point cloud to a .ply file for visualization
#    4. How to open the result in Open3D or MeshLab
#
#  Keyboard: press any key to capture and save one frame, Q/ESC to quit
#
#  Device requirement: All
#
#  Run:
#    python examples/beginner/05_point_cloud.py
# ******************************************************************************

import os

from pyorbbecsdk import *

save_points_dir = os.path.join(os.getcwd(), "point_clouds")
if not os.path.exists(save_points_dir):
    os.mkdir(save_points_dir)

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
        frames = pipeline.wait_for_frames(1000)
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
        if point_cloud_frame is None:
            continue
        #save point cloud
        save_point_cloud_to_ply(os.path.join(save_points_dir, "point_cloud.ply"), point_cloud_frame)
        #save mesh to point cloud
        #save_point_cloud_to_ply(os.path.join(save_points_dir, "point_cloud.ply"), point_cloud_frame, False, True, 50)        
        break
    print("stop pipeline")
    pipeline.stop()


if __name__ == "__main__":
    main()
