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
import cv2
import numpy as np
from pyorbbecsdk import *

ESC_KEY = 27

def main():
    # Initialize the Pipeline and Config objects for stream management
    config = Config()
    pipeline = Pipeline()
    
    # Get the device object to check for sensor availability
    device = pipeline.get_device()
    try:
        # Verify if the connected device supports a confidence sensor
        device.get_sensor(OBSensorType.CONFIDENCE_SENSOR)
    except:
        print("This sample requires a device with a confidence sensor.")
        return
    
    # Enable the Depth stream first as it is often tied to confidence data
    config.enable_video_stream(OBStreamType.DEPTH_STREAM)
    
    # Match Confidence stream configuration with the Depth stream settings
    enable_profiles = config.get_enabled_stream_profile_list()
    if enable_profiles:
        for i in range(0, enable_profiles.get_count()):
            profile = enable_profiles.get_stream_profile_by_index(i)
            if profile.get_type() == OBStreamType.DEPTH_STREAM:
                # Cast to VideoStreamProfile to access resolution and FPS
                depth_profile = profile.as_video_stream_profile()
                if depth_profile:
                    # Enable Confidence stream using same width, height, and FPS as Depth
                    config.enable_video_stream(
                        OBStreamType.CONFIDENCE_STREAM, 
                        depth_profile.get_width(), 
                        depth_profile.get_height(), 
                        depth_profile.get_fps()
                    )
                break
    
    # Start the pipeline with the specific configuration
    pipeline.start(config)
    
    while True:
        try:
            # Wait for a new set of frames (timeout set to 100ms)
            frames = pipeline.wait_for_frames(1000)
            if frames is None:
                continue
            
            # Extract the Confidence frame from the frameset
            confidence_frame = frames.get_frame(OBFrameType.CONFIDENCE_FRAME)
            if confidence_frame is None:
                continue
            
            # Cast the generic frame to a specialized ConfidenceFrame
            confidence_frame = confidence_frame.as_confidence_frame()
            
            try:
                # Convert raw frame data into a NumPy buffer (unsigned 8-bit integers)
                confidence_data = np.frombuffer(confidence_frame.get_data(), dtype=np.uint8)
                # Reshape the 1D buffer into a 2D image based on frame dimensions
                confidence_data = confidence_data.reshape(
                    confidence_frame.get_height(), 
                    confidence_frame.get_width()
                )
                
                # Normalize the data values to the 0-255 range for visualization
                confidence_image = cv2.normalize(
                    confidence_data, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U
                )
                # Convert the grayscale normalized image to RGB for display purposes
                confidence_image = cv2.cvtColor(confidence_image, cv2.COLOR_GRAY2RGB)
            except ValueError:
                return None
            
            # Display the processed confidence map in an OpenCV window
            cv2.imshow("Confidence", confidence_image)
            
            # Check for exit input ('q' or ESC key)
            key = cv2.waitKey(1)
            if key == ord('q') or key == ESC_KEY:
                break
        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            break
    
    # Clean up: close windows and stop the camera pipeline
    cv2.destroyAllWindows()
    pipeline.stop()

if __name__ == "__main__":
    main()