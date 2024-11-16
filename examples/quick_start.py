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

import cv2
import numpy as np
import time

from pyorbbecsdk import *
from utils import frame_to_bgr_image

ESC_KEY = 27
MIN_DEPTH = 20  # 20mm
MAX_DEPTH = 10000  # 10000mm

def main():
    pipeline = Pipeline()

    pipeline.start()
    print("Pipeline started successfully. Press 'q' or ESC to exit.")

    # Set window size
    window_width = 1280
    window_height = 720
    cv2.namedWindow("QuickStart Viewer", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("QuickStart Viewer", window_width, window_height)

    while True:
        try:
            frames = pipeline.wait_for_frames(100)
            if frames is None:
                continue

            # Get color frame
            color_frame = frames.get_color_frame()
            if color_frame is None:
                continue
            color_image = frame_to_bgr_image(color_frame)

            # Get depth frame
            depth_frame = frames.get_depth_frame()
            if depth_frame is None:
                continue
            if depth_frame.get_format() != OBFormat.Y16:
                print("Depth format is not Y16")
                continue

            # Process depth data
            width = depth_frame.get_width()
            height = depth_frame.get_height()
            scale = depth_frame.get_depth_scale()
            
            depth_data = np.frombuffer(depth_frame.get_data(), dtype=np.uint16).reshape((height, width))
            depth_data = depth_data.astype(np.float32) * scale
            depth_data = np.where((depth_data > MIN_DEPTH) & (depth_data < MAX_DEPTH), depth_data, 0).astype(np.uint16)

            # Create depth visualization
            depth_image = cv2.normalize(depth_data, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
            depth_image = cv2.applyColorMap(depth_image, cv2.COLORMAP_JET)

            # Resize and combine images
            color_image_resized = cv2.resize(color_image, (window_width // 2, window_height))
            depth_image_resized = cv2.resize(depth_image, (window_width // 2, window_height))
            combined_image = np.hstack((color_image_resized, depth_image_resized))
            
            cv2.imshow("QuickStart Viewer", combined_image)

            if cv2.waitKey(1) in [ord('q'), ESC_KEY]:
                break
        except KeyboardInterrupt:
            break

    cv2.destroyAllWindows()
    pipeline.stop()
    print("Pipeline stopped and all windows closed.")

if __name__ == "__main__":
    main()
