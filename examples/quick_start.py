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
#    3. How to render depth with 3D relief lighting (gamma + Scharr gradient).
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
from utils import frame_to_bgr_image, resize_to_fit

from pyorbbecsdk import OBError, OBFormat, Pipeline  # type: ignore

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
ESC_KEY = 27
MIN_DEPTH = 20  # mm — ignore noisy near-range readings
MAX_DEPTH = 5000  # mm — ignore far-range readings

WINDOW_NAME = "QuickStart Viewer"
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720


def render_depth_3d(depth_mm: np.ndarray) -> np.ndarray:
    """
    Convert a float32 depth-in-mm array into a 3D-looking BGR image.

    Pipeline:
      clip [MIN, MAX] → gamma 0.8 → uint8 → Scharr gradient lighting → colormap
    """
    # 1. Clip to fixed range (keeps colors stable across frames)
    depth_clipped = np.clip(depth_mm, MIN_DEPTH, MAX_DEPTH)

    # 2. Normalize to [0, 1] then apply gamma correction
    #    γ < 1 stretches near-field gradients for better detail
    depth_norm = (depth_clipped - MIN_DEPTH) / (MAX_DEPTH - MIN_DEPTH + 1e-6)
    depth_gamma = np.power(depth_norm, 0.8)

    # 3. Map to uint8
    depth_8bit = (depth_gamma * 255).astype(np.uint8)

    # 4. Surface-normal lighting via Scharr gradient
    #    Simulates a directional light from top-left for 3D relief
    grad_x = cv2.Scharr(depth_8bit, cv2.CV_32F, 1, 0)
    grad_y = cv2.Scharr(depth_8bit, cv2.CV_32F, 0, 1)
    mag = cv2.magnitude(grad_x, grad_y) + 1.0

    lighting = -0.707 * (grad_x + grad_y) / mag  # diffuse term
    lighting = lighting * 0.15 + 0.85  # ambient 85% + diffuse 15%
    np.clip(lighting, 0.7, 1.0, out=lighting)

    # 5. Apply colormap then multiply by lighting
    depth_colored = cv2.applyColorMap(depth_8bit, cv2.COLORMAP_JET)
    depth_colored = (depth_colored * lighting[..., np.newaxis]).astype(np.uint8)

    return depth_colored


def main():
    # ------------------------------------------------------------------
    # Step 1: Create a Pipeline and start with the default configuration.
    #
    #   No Config object is passed, so the SDK loads settings from
    #   config/OrbbecSDKConfig.xml (stream profiles, filters, etc.).
    #   This is the simplest way to get RGBD data flowing.
    # ------------------------------------------------------------------
    try:
        pipeline = Pipeline()
        pipeline.start()
    except OBError as e:
        print(f"Error: {e}")
        print("Please connect an Orbbec camera and try again.")
        return

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

            width = depth_frame.get_width()
            height = depth_frame.get_height()
            scale = depth_frame.get_depth_scale()

            depth_data = np.frombuffer(depth_frame.get_data(), dtype=np.uint16)
            depth_data = depth_data.reshape((height, width))
            depth_mm = depth_data.astype(np.float32) * scale

            # ----------------------------------------------------------
            # Step 5: Render depth with 3D relief lighting.
            #
            #   Uses gamma correction + Scharr surface-normal lighting
            #   for a more visually informative depth display.
            # ----------------------------------------------------------
            depth_image = render_depth_3d(depth_mm)

            half_w = WINDOW_WIDTH // 2
            color_resized = resize_to_fit(color_image, half_w, WINDOW_HEIGHT)
            depth_resized = resize_to_fit(depth_image, half_w, WINDOW_HEIGHT)
            combined = np.hstack((color_resized, depth_resized))

            cv2.imshow(WINDOW_NAME, combined)

            if cv2.waitKey(1) in (ord("q"), ord("Q"), ESC_KEY):
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
