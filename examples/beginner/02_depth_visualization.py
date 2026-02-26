# ******************************************************************************
#  pyorbbecsdk Beginner Example 02 — Depth Visualization
#
#  What you will learn:
#    1. How to configure and start a depth stream
#    2. How to convert raw uint16 depth data to millimeters
#    3. How to filter depth to a useful range (MIN_DEPTH to MAX_DEPTH)
#    4. How to display depth as a color-mapped image using OpenCV
#    5. How to overlay actual distance (mm) at the frame center
#
#  Press 'q' or ESC to quit.
#
#  Run:
#    python examples/beginner/02_depth_visualization.py
# ******************************************************************************

import sys
import numpy as np
import cv2

from pyorbbecsdk import (
    Pipeline, Config, OBSensorType, OBLogLevel, Context, OBError
)

# ---------------------------------------------------------------------------
# Configuration — adjust these for your scene
# ---------------------------------------------------------------------------
MIN_DEPTH_MM = 100    # Ignore depth closer than this (mm) — avoids noise
MAX_DEPTH_MM = 5000   # Ignore depth farther than this (mm) — avoids clutter
WINDOW_TITLE  = "Depth Viewer  |  Press 'q' to quit"
ESC_KEY = 27


def main():
    # Suppress SDK info messages; set DEBUG for diagnostics
    ctx = Context()
    ctx.set_logger_level(OBLogLevel.WARNING)

    # --- Step 1: Create pipeline and configure depth stream ---
    pipeline = Pipeline()

    config = Config()
    try:
        profile_list = pipeline.get_stream_profile_list(OBSensorType.DEPTH_SENSOR)
        # get_default_video_stream_profile() picks the sensor's preferred mode
        depth_profile = profile_list.get_default_video_stream_profile()
        print(f"Depth profile: {depth_profile}")
        config.enable_stream(depth_profile)
    except OBError as e:
        print(f"ERROR: Cannot configure depth stream: {e}")
        sys.exit(1)

    pipeline.start(config)
    print(f"Depth stream started. Range: {MIN_DEPTH_MM}mm – {MAX_DEPTH_MM}mm")
    print("Press 'q' or ESC to quit.\n")

    try:
        while True:
            # --- Step 2: Wait for the next frame set (up to 1 second) ---
            frame_set = pipeline.wait_for_frames(1000)
            if frame_set is None:
                # Timeout — camera may be initialising, just retry
                continue

            depth_frame = frame_set.get_depth_frame()
            if depth_frame is None:
                continue

            # --- Step 3: Convert raw depth to millimeters ---
            width  = depth_frame.get_width()
            height = depth_frame.get_height()
            scale  = depth_frame.get_depth_scale()   # e.g. 0.001 → 1 unit = 1 mm

            # get_data() returns a bytes-like object; interpret as uint16 pixels
            raw = np.frombuffer(depth_frame.get_data(), dtype=np.uint16)
            depth_mm = raw.reshape(height, width).astype(np.float32) * scale

            # --- Step 4: Clip to useful range, zero out-of-range pixels ---
            depth_valid = np.where(
                (depth_mm >= MIN_DEPTH_MM) & (depth_mm <= MAX_DEPTH_MM),
                depth_mm,
                0,
            ).astype(np.uint16)

            # --- Step 5: Normalize to 0-255 and apply colormap ---
            # cv2.NORM_MINMAX maps the min valid depth → 0, max → 255
            display = cv2.normalize(
                depth_valid, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U
            )
            display = cv2.applyColorMap(display, cv2.COLORMAP_JET)

            # --- Step 6: Show distance at frame center ---
            cy, cx = height // 2, width // 2
            center_dist = depth_mm[cy, cx]
            label = (
                f"{center_dist:.0f} mm"
                if MIN_DEPTH_MM <= center_dist <= MAX_DEPTH_MM
                else "out of range"
            )
            cv2.circle(display, (cx, cy), 4, (255, 255, 255), -1)
            cv2.putText(
                display, label,
                (cx + 8, cy + 6),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2,
            )

            cv2.imshow(WINDOW_TITLE, display)
            key = cv2.waitKey(1)
            if key in (ord("q"), ESC_KEY):
                break

    finally:
        # Always stop the pipeline — this releases USB bandwidth
        pipeline.stop()
        cv2.destroyAllWindows()
        print("Stopped.")


if __name__ == "__main__":
    main()
