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
#
#  pyorbbecsdk Quick Start — RGB-D Viewer in ~30 Lines
#
#  What this example demonstrates:
#    1. How to use Pipeline with zero-config — the SDK loads the default stream
#       configuration from  config/OrbbecSDKConfig.xml  automatically.
#    2. How to retrieve synchronized Color + Depth frames.
#    3. How to convert the raw depth data (uint16, mm) into a colour-mapped
#       visualisation using OpenCV.
#    4. How to display Color and Depth side-by-side in a single window.
#
#  Default configuration:
#    When pipeline.start() is called without a Config object, the SDK reads
#    config/OrbbecSDKConfig.xml in the working directory.  That XML file
#    defines default stream profiles (resolution, FPS, format) per device
#    model under the <Pipeline><Stream> and <Device> sections.
#
#    To customise the defaults without changing code, edit OrbbecSDKConfig.xml:
#      - <Depth>  / <Color> : Width, Height, FPS, Format
#      - <UseDefaultStreamProfile>false</UseDefaultStreamProfile>
#    See config/OrbbecSDKConfig.md for the full reference.
#
#  Prerequisites:
#    pip install pyorbbecsdk2 opencv-python numpy
#    Connect an Orbbec camera via USB before running.
#
#  Run:
#    python examples/quick_start.py
#
#  Controls:
#    ESC / Q  —  Quit
# ******************************************************************************

import cv2
import numpy as np

from pyorbbecsdk import *
from utils import frame_to_bgr_image

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
ESC_KEY = 27
MIN_DEPTH = 20      # mm — ignore noisy near-range readings
MAX_DEPTH = 10000   # mm — ignore far-range readings

WINDOW_NAME = "QuickStart Viewer"
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720


def main():
    # ------------------------------------------------------------------
    # Step 1: Create a Pipeline and start with the default configuration.
    #
    #   No Config object is passed, so the SDK loads settings from
    #   config/OrbbecSDKConfig.xml (stream profiles, filters, etc.).
    #   This is the simplest way to get RGBD data flowing.
    # ------------------------------------------------------------------
    pipeline = Pipeline()
    pipeline.start()
    print("Pipeline started (default config). Press 'Q' or ESC to exit.")

    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(WINDOW_NAME, WINDOW_WIDTH, WINDOW_HEIGHT)

    while True:
        try:
            # ----------------------------------------------------------
            # Step 2: Wait for a synchronized set of frames (Color + Depth).
            # ----------------------------------------------------------
            frames = pipeline.wait_for_frames(1000)
            if frames is None:
                continue

            # ----------------------------------------------------------
            # Step 3: Get the Color frame and convert to BGR for OpenCV.
            # ----------------------------------------------------------
            color_frame = frames.get_color_frame()
            if color_frame is None:
                continue
            color_image = frame_to_bgr_image(color_frame)

            # ----------------------------------------------------------
            # Step 4: Get the Depth frame and apply scale + range filter.
            # ----------------------------------------------------------
            depth_frame = frames.get_depth_frame()
            if depth_frame is None:
                continue
            if depth_frame.get_format() != OBFormat.Y16:
                print("Depth format is not Y16, skipping frame.")
                continue

            width = depth_frame.get_width()
            height = depth_frame.get_height()
            scale = depth_frame.get_depth_scale()

            depth_data = np.frombuffer(depth_frame.get_data(), dtype=np.uint16)
            depth_data = depth_data.reshape((height, width))
            depth_data = (depth_data.astype(np.float32) * scale).astype(np.uint16)
            depth_data = np.where(
                (depth_data > MIN_DEPTH) & (depth_data < MAX_DEPTH), depth_data, 0
            )

            # ----------------------------------------------------------
            # Step 5: Visualise — normalise depth to 0-255 and apply a
            #         colour map, then display side-by-side with colour.
            # ----------------------------------------------------------
            depth_image = cv2.normalize(depth_data, None, 0, 255,
                                        cv2.NORM_MINMAX, dtype=cv2.CV_8U)
            depth_image = cv2.applyColorMap(depth_image, cv2.COLORMAP_JET)

            half_w = WINDOW_WIDTH // 2
            color_resized = cv2.resize(color_image, (half_w, WINDOW_HEIGHT))
            depth_resized = cv2.resize(depth_image, (half_w, WINDOW_HEIGHT))
            combined = np.hstack((color_resized, depth_resized))

            cv2.imshow(WINDOW_NAME, combined)

            if cv2.waitKey(1) in (ord('q'), ord('Q'), ESC_KEY):
                break

        except KeyboardInterrupt:
            break

    # ------------------------------------------------------------------
    # Step 6: Clean up.
    # ------------------------------------------------------------------
    cv2.destroyAllWindows()
    pipeline.stop()
    print("Pipeline stopped.")


if __name__ == "__main__":
    main()
