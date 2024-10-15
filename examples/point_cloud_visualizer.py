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

import cv2
import numpy as np
import open3d as o3d
from pyorbbecsdk import *
import threading

def create_visualizer():
    vis = o3d.visualization.Visualizer()
    vis.create_window()
    return vis

def update_visualizer(vis, pcd, points):
    # Update the point cloud with new points and colors (if available)
    pcd.points = o3d.utility.Vector3dVector(points[:, :3])
    if points.shape[1] == 6:
        pcd.colors = o3d.utility.Vector3dVector(points[:, 3:6] / 255.0)
    vis.update_geometry(pcd)
    vis.poll_events()
    vis.update_renderer()

def main():
    # Create context and pipeline for capturing depth data
    context = Context()
    pipeline = Pipeline()
    config = Config()
    
    # Get depth profile list and check if available
    depth_profile_list = pipeline.get_stream_profile_list(OBSensorType.DEPTH_SENSOR)
    if depth_profile_list is None:
        print("No proper depth profile, cannot generate point cloud")
        return
    depth_profile = depth_profile_list.get_default_video_stream_profile()
    config.enable_stream(depth_profile)
    
    # Check if color sensor is available
    has_color_sensor = False
    try:
        profile_list = pipeline.get_stream_profile_list(OBSensorType.COLOR_SENSOR)
        if profile_list is not None:
            color_profile = profile_list.get_default_video_stream_profile()
            config.enable_stream(color_profile)
            has_color_sensor = True
    except OBError as e:
        print(e)
    
    # Enable frame synchronization and start the pipeline
    pipeline.enable_frame_sync()
    pipeline.start(config)
    camera_param = pipeline.get_camera_param()
    
    # Initialize filters for aligning and generating point clouds
    align_filter = AlignFilter(align_to_stream=OBStreamType.COLOR_STREAM)
    point_cloud_filter = PointCloudFilter()
    point_cloud_filter.set_camera_param(camera_param)
    
    # Create a visualizer and point cloud object to display the data
    vis = create_visualizer()
    pcd = o3d.geometry.PointCloud()  # Reuse the PointCloud object
    context.set_logger_level(OBLogLevel.NONE)
    print("Start showing point cloud, press 'ctrl+c' to exit")

    def process_frames():
        try:
            while running:
                # Capture frames from the pipeline
                frames = pipeline.wait_for_frames(100)
                if frames is None:
                    continue
                depth_frame = frames.get_depth_frame()
                if depth_frame is None:
                    continue
                color_frame = frames.get_color_frame()
                if has_color_sensor and color_frame is None:
                    continue
                
                # Align frames if necessary
                frame = align_filter.process(frames)
                scale = depth_frame.get_depth_scale()
                point_cloud_filter.set_position_data_scaled(scale)

                # Set the format for creating the point cloud (RGB if color is available)
                point_cloud_filter.set_create_point_format(
                    OBFormat.RGB_POINT if has_color_sensor and color_frame is not None else OBFormat.POINT)
                point_cloud_frame = point_cloud_filter.process(frame)
                points = point_cloud_filter.calculate(point_cloud_frame)

                # Update the visualizer with the new point cloud data
                update_visualizer(vis, pcd, np.array(points))

        except Exception as e:
            print(e)

        finally:
            # Stop the pipeline and close visualizer window
            pipeline.stop()
            vis.destroy_window()
            cv2.destroyAllWindows()

    # Run the frame processing in a separate thread
    process_thread = threading.Thread(target=process_frames)
    process_thread.start()

    # Main thread for rendering
    try:
        while running:
            vis.poll_events()
            vis.update_renderer()

    except KeyboardInterrupt:
        # Handle user interruption (Ctrl+C)
        running = False
    process_thread.join()

if __name__ == "__main__":
    running = True
    main()
