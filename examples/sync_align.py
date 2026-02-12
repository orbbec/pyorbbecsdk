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
from utils import frame_to_bgr_image

# --- Configuration Constants ---
ESC_KEY = 27
MIN_DEPTH = 20    # Minimum valid depth distance in mm
MAX_DEPTH = 10000 # Maximum valid depth distance in mm

def main():
    window_name = "SyncAlignViewer"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, 1280, 720)

    # Initialize the pipeline and configuration objects
    pipeline = Pipeline()
    config = Config()

    # Default settings for synchronization and alignment mode
    enable_sync = False
    align_mode = 0 # 0: Depth to Color (D2C), 1: Color to Depth (C2D)
    
    try:
        # 1. Setup Color Stream Profile
        profile_list = pipeline.get_stream_profile_list(OBSensorType.COLOR_SENSOR)
        color_profile = profile_list.get_video_stream_profile(0, 0, OBFormat.RGB, 0)
        config.enable_stream(color_profile)
        
        # 2. Setup Depth Stream Profile
        profile_list = pipeline.get_stream_profile_list(OBSensorType.DEPTH_SENSOR)
        depth_profile = profile_list.get_default_video_stream_profile()
        config.enable_stream(depth_profile)
        
        # 3. Ensure pipeline waits for a full frameset (Color + Depth) before outputting
        config.set_frame_aggregate_output_mode(OBFrameAggregateOutputMode.FULL_FRAME_REQUIRE)
    except Exception as e:
        print(f"Stream configuration error: {e}")
        return

    # Enable hardware-level frame synchronization if requested
    if enable_sync:
        try:
            pipeline.enable_frame_sync()
        except Exception as e:
            print(f"Sync error: {e}")

    try:
        pipeline.start(config)
    except Exception as e:
        print(f"Pipeline start error: {e}")
        return

    # Initialize the alignment filter. D2C is the most common use case (overlaying depth on RGB).
    align_filter = AlignFilter(align_to_stream=OBStreamType.COLOR_STREAM)
    
    print("\nControls:")
    print("'t' or 'T': Switch Align Mode (D2C <-> C2D)")
    print("'f' or 'F': Toggle Frame Sync (ON / OFF)")
    print("'q' or ESC: Exit program\n")

    while True:
        try:
            # Retrieve a frameset with a 100ms timeout
            frames = pipeline.wait_for_frames(1000)
            if not frames:
                continue
                
            color_frame = frames.get_color_frame()
            depth_frame = frames.get_depth_frame()
            
            if not color_frame or not depth_frame:
                continue

            # --- Spatial Alignment ---
            # Transforms one stream to the coordinate system/FOV of the other
            frames = align_filter.process(frames)
            if not frames:
                continue
            
            frames = frames.as_frame_set()
            color_frame = frames.get_color_frame()
            depth_frame = frames.get_depth_frame()
            
            if not color_frame or not depth_frame:
                continue

            # Convert raw color frame to BGR for OpenCV rendering
            color_image = frame_to_bgr_image(color_frame)
            if color_image is None:
                print("Failed to convert color frame")
                continue
                
            # --- Depth Image Processing ---
            try:
                # Convert raw buffer to 2D numpy array
                depth_data = np.frombuffer(depth_frame.get_data(), dtype=np.uint16).reshape(
                    (depth_frame.get_height(), depth_frame.get_width()))
            except ValueError:
                print("Failed to reshape depth data")
                continue
                
            # Apply depth scale to get actual distance in mm and filter by range
            depth_data = depth_data.astype(np.float32) * depth_frame.get_depth_scale()
            depth_data = np.where((depth_data > MIN_DEPTH) & (depth_data < MAX_DEPTH), depth_data, 0)
            
            # Normalize and colormap for visualization
            depth_data = depth_data.astype(np.uint16)
            depth_image = cv2.normalize(depth_data, None, 0, 255, cv2.NORM_MINMAX)
            depth_image = cv2.applyColorMap(depth_image.astype(np.uint8), cv2.COLORMAP_JET)
            
            # --- Blended Visualization ---
            # Alpha-blending of Color and Depth images to check alignment accuracy
            overlay_image = cv2.addWeighted(color_image, 0.5, depth_image, 0.5, 0)

            # UI Text Overlay
            mode_text = "D2C (Depth to Color)" if align_mode == 0 else "C2D (Color to Depth)"
            sync_text = "Sync: ON" if enable_sync else "Sync: OFF"
            cv2.putText(overlay_image, f"{mode_text} | {sync_text}", (20, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        
            cv2.imshow(window_name, overlay_image)
            
            # Handle Keyboard Input
            key = cv2.waitKey(1)
            if key in [ord('q'), ESC_KEY]:
                break
            elif key in [ord('f'), ord('F')]:
                # Toggle Frame Synchronization logic
                enable_sync = not enable_sync
                if enable_sync:
                    pipeline.enable_frame_sync()
                    print("Sync: Enabled")
                else:
                    pipeline.disable_frame_sync()
                    print("Sync: Disabled")
                
            elif key in [ord('t'), ord('T')]:
                # Toggle Alignment Mode logic
                align_mode = (align_mode + 1) % 2
                if align_mode == 0:
                    align_filter = AlignFilter(align_to_stream=OBStreamType.COLOR_STREAM)
                    print("Changed Mode: Depth to Color")
                else:
                    align_filter = AlignFilter(align_to_stream=OBStreamType.DEPTH_STREAM)
                    print("Changed Mode: Color to Depth")
                    
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Runtime error: {e}")
            continue
        
    # Clean up resources
    cv2.destroyAllWindows()
    pipeline.stop()

if __name__ == "__main__":
    main()