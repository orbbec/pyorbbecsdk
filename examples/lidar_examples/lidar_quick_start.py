# ******************************************************************************
#  Copyright (c) 2024 Orbbec 3D Technology, Inc
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
# ******************************************************************************
import os
import sys

from pyorbbecsdk import *

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import is_lidar_device

ESC_KEY = 27

save_points_dir = os.path.join(os.getcwd(), "point_clouds")
if not os.path.exists(save_points_dir):
    os.mkdir(save_points_dir)

def main():
    # Create a pipeline.
    pipeline = Pipeline()
    
    # Get the device from pipeline.
    device = pipeline.get_device()
    
    # Check LiDAR device
    if not is_lidar_device(device):
        print("Invalid device, please connect a LiDAR device!")
        return

    # Start the pipeline with default config.
    # Modify the default configuration by the configuration file: "*SDKConfig.xml"
    pipeline.start()
    
    print("LiDAR stream is started!")
    print("Press 'r' or 'R' to create LiDAR PointCloud and save to ply file! ")
    print("Press 'q' or 'Q' to exit! ")
    
    try:
        while True:
            # Wait for user input
            key = input("Wating for command:")
            if key.lower() == 'q':
                break
            
            # Press 'r' or 'R' to save LiDAR point cloud to ply file
            if key.lower() == 'r':
                print("Save LiDAR PointCloud to ply file, this will take some time...")
                
                # Wait for frameSet from the pipeline, the default timeout is 1000ms.
                frames = pipeline.wait_for_frames(1000)
                if frames is None:
                    print("No frame data, please try again!")
                    continue
            
                # Get LiDAR point cloud frame
                frame = frames.get_frame(OBFrameType.LIDAR_POINTS_FRAME)
                if frame is None:
                    print("No LiDAR frame found!")
                    continue
                
                # Save point cloud data to ply file
                save_path = os.path.join(save_points_dir, "LiDARPoints.ply")
                save_lidar_point_cloud_to_ply(save_path, frame.as_lidar_points_frame(), False)
                print(f"LiDARPoints.ply Saved at: {os.path.abspath(save_path)}")
    
    except KeyboardInterrupt:
        pass
    except OBError as e:
        print(e)
    finally:
        # Stop the Pipeline, no frame data will be generated
        pipeline.stop()

if __name__ == "__main__":
    main()