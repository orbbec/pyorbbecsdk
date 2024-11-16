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

from pyorbbecsdk import *
import cv2
import numpy as np
from utils import frame_to_bgr_image

def get_stream_config(pipeline: Pipeline):
    """
    Gets the stream configuration for the pipeline.

    Args:
        pipeline (Pipeline): The pipeline object.

    Returns:
        Config: The stream configuration.
    """
    config = Config()
    try:
        # Get the list of color stream profiles
        profile_list = pipeline.get_stream_profile_list(OBSensorType.COLOR_SENSOR)
        assert profile_list is not None
        
        # Iterate through the color stream profiles
        for i in range(len(profile_list)):
            color_profile = profile_list[i]
            
            # Check if the color format is RGB
            if color_profile.get_format() != OBFormat.RGB:
                continue
            
            # Get the list of hardware aligned depth-to-color profiles
            hw_d2c_profile_list = pipeline.get_d2c_depth_profile_list(color_profile, OBAlignMode.HW_MODE)
            if len(hw_d2c_profile_list) == 0:
                continue
            
            # Get the first hardware aligned depth-to-color profile
            hw_d2c_profile = hw_d2c_profile_list[0]
            print("hw_d2c_profile: ", hw_d2c_profile)
            
            # Enable the depth and color streams
            config.enable_stream(hw_d2c_profile)
            config.enable_stream(color_profile)
            
            # Set the alignment mode to hardware alignment
            config.set_align_mode(OBAlignMode.HW_MODE)
            return config
    except Exception as e:
        print(e)
        return None
    return None

def main():
    # Create a pipeline object
    pipeline = Pipeline()
    
    # Get the stream configuration
    config = get_stream_config(pipeline)
    if config is None:
        return
    
    # Start the pipeline
    pipeline.start(config)
    
    # Set the depth range
    min_depth = 20  # Minimum depth value, keep closer depths
    max_depth = 10000  # Maximum depth value, allow far depths to be lost

    while True:
        # Wait for frames
        frames = pipeline.wait_for_frames(100)
        if frames is None:
            continue
        
        # Get the color and depth frames
        color_frame = frames.get_color_frame()
        depth_frame = frames.get_depth_frame()
        if not color_frame or not depth_frame:
            continue
        depth_format = depth_frame.get_format()
        if depth_format != OBFormat.Y16:
            print("depth format is not Y16")
            continue

        # Convert the color frame to a BGR image
        color_image = frame_to_bgr_image(color_frame)
        if color_image is None:
            print("Failed to convert frame to image")
            continue

        # Get the depth data
        depth_data = np.frombuffer(depth_frame.get_data(), dtype=np.uint16).reshape(
            (depth_frame.get_height(), depth_frame.get_width()))
        
        # Convert depth data to float32 and apply depth scale
        depth_data = depth_data.astype(np.float32) * depth_frame.get_depth_scale()
        
        # Apply custom depth range, clip depth data
        depth_data = np.clip(depth_data, min_depth, max_depth)
        
        # Normalize depth data for display
        depth_image = cv2.normalize(depth_data, None, 0, 255, cv2.NORM_MINMAX)
        depth_image = cv2.applyColorMap(depth_image.astype(np.uint8), cv2.COLORMAP_JET)

        # Blend the depth and color images
        blended_image = cv2.addWeighted(color_image, 0.5, depth_image, 0.5, 0)

        #resize the window
        cv2.namedWindow("HW D2C Align Viewer", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("HW D2C Align Viewer", 640, 480)
        
        # Display the result
        cv2.imshow("HW D2C Align Viewer", blended_image)
        if cv2.waitKey(1) in [ord('q'), 27]:  # 27 is the ESC key
            break

    # Stop the pipeline
    pipeline.stop()

if __name__ == "__main__":
    main()
