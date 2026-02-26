# ******************************************************************************
#  pyorbbecsdk Beginner Example 03 — Color and Aligned Depth
#
#  What you will learn:
#    1. How to enable multiple streams simultaneously (Color + Depth)
#    2. What "frame synchronization" means and how to enable it
#    3. How to use AlignFilter to project depth into the color camera view
#    4. How to display both streams side-by-side with OpenCV
#
#  When depth is aligned to color:
#    - Each color pixel (u, v) has a corresponding depth value at the same (u, v)
#    - This is essential for tasks like 3D object detection and point cloud coloring
#
#  Press 'q' or ESC to quit.
#
#  Run:
#    python examples/beginner/03_color_and_depth_aligned.py
# ******************************************************************************

import sys
import numpy as np
import cv2

from pyorbbecsdk import (
    Pipeline, Config, AlignFilter,
    OBSensorType, OBStreamType, OBLogLevel, Context, OBError,
)
from pyorbbecsdk import FormatConvertFilter, OBFormat, OBConvertFormat

ESC_KEY = 27
MIN_DEPTH_MM = 100
MAX_DEPTH_MM = 5000


def color_frame_to_bgr(color_frame):
    """Convert a color VideoFrame to a BGR numpy array for OpenCV display."""
    width  = color_frame.get_width()
    height = color_frame.get_height()
    fmt    = color_frame.get_format()
    data   = np.frombuffer(color_frame.get_data(), dtype=np.uint8)

    if fmt == OBFormat.RGB:
        img = data.reshape(height, width, 3)
        return cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    elif fmt == OBFormat.BGR:
        return data.reshape(height, width, 3)
    elif fmt == OBFormat.MJPG:
        return cv2.imdecode(data, cv2.IMREAD_COLOR)
    elif fmt in (OBFormat.YUYV, OBFormat.UYVY):
        # Use the SDK's FormatConvertFilter for YUV formats
        convert_filter = FormatConvertFilter()
        convert_filter.set_format_convert_format(
            OBConvertFormat.YUYV_TO_RGB888
            if fmt == OBFormat.YUYV
            else OBConvertFormat.UYVY_TO_RGB888
        )
        rgb_frame = convert_filter.process(color_frame)
        if rgb_frame is None:
            return None
        rgb_data = np.frombuffer(rgb_frame.get_data(), dtype=np.uint8)
        img = rgb_data.reshape(height, width, 3)
        return cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    else:
        print(f"Unsupported color format: {fmt}")
        return None


def depth_to_colormap(depth_frame):
    """Convert a depth frame to a color-mapped BGR image."""
    width  = depth_frame.get_width()
    height = depth_frame.get_height()
    scale  = depth_frame.get_depth_scale()
    raw    = np.frombuffer(depth_frame.get_data(), dtype=np.uint16)
    depth_mm = raw.reshape(height, width).astype(np.float32) * scale
    clipped  = np.where(
        (depth_mm >= MIN_DEPTH_MM) & (depth_mm <= MAX_DEPTH_MM), depth_mm, 0
    ).astype(np.uint16)
    normalized = cv2.normalize(clipped, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
    return cv2.applyColorMap(normalized, cv2.COLORMAP_JET)


def main():
    ctx = Context()
    ctx.set_logger_level(OBLogLevel.WARNING)

    pipeline = Pipeline()
    config   = Config()

    # --- Enable Color stream ---
    try:
        color_profiles = pipeline.get_stream_profile_list(OBSensorType.COLOR_SENSOR)
        config.enable_stream(color_profiles.get_default_video_stream_profile())
        print("Color stream enabled.")
    except OBError as e:
        print(f"WARNING: Color stream unavailable: {e}")

    # --- Enable Depth stream ---
    try:
        depth_profiles = pipeline.get_stream_profile_list(OBSensorType.DEPTH_SENSOR)
        config.enable_stream(depth_profiles.get_default_video_stream_profile())
        print("Depth stream enabled.")
    except OBError as e:
        print(f"ERROR: Depth stream unavailable: {e}")
        sys.exit(1)

    # --- Enable frame synchronization ---
    # This aligns the timestamps of Color and Depth frames so they come from
    # the same moment in time. Without sync, you may get frames from different
    # instants, causing visible ghosting artifacts when they are overlaid.
    pipeline.enable_frame_sync()
    print("Frame sync enabled.")

    # --- Create AlignFilter ---
    # AlignFilter reprojects the depth image into the color camera coordinate
    # system, making each pixel in the output depth map correspond to the
    # same spatial point as the color image pixel at the same (x, y).
    align_filter = AlignFilter(align_to_stream=OBStreamType.COLOR_STREAM)

    pipeline.start(config)
    print("\nStreaming... Press 'q' or ESC to quit.\n")

    try:
        while True:
            frame_set = pipeline.wait_for_frames(1000)
            if frame_set is None:
                continue

            # Apply alignment — this reprojects depth into color space
            aligned = align_filter.process(frame_set)
            if aligned is None:
                continue

            color_frame = aligned.get_color_frame()
            depth_frame = aligned.get_depth_frame()

            panels = []

            if color_frame is not None:
                bgr = color_frame_to_bgr(color_frame)
                if bgr is not None:
                    panels.append(bgr)

            if depth_frame is not None:
                depth_vis = depth_to_colormap(depth_frame)

                # Overlay a semi-transparent depth on color for intuitive alignment check
                if panels:
                    # Ensure both images have the same size before blending
                    h_d, w_d = depth_vis.shape[:2]
                    h_c, w_c = panels[0].shape[:2]
                    if (h_d, w_d) != (h_c, w_c):
                        depth_vis = cv2.resize(depth_vis, (w_c, h_c))
                    blended = cv2.addWeighted(panels[0], 0.6, depth_vis, 0.4, 0)
                    panels.append(blended)
                else:
                    panels.append(depth_vis)

            if not panels:
                continue

            # Stack color | blend side by side
            display = np.hstack(panels) if len(panels) > 1 else panels[0]

            # Add labels
            h, w = display.shape[:2]
            half_w = w // len(panels)
            cv2.putText(display, "Color", (10, 25),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            if len(panels) > 1:
                cv2.putText(display, "Color + Aligned Depth", (half_w + 10, 25),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            cv2.imshow("Color + Aligned Depth  |  Press 'q' to quit", display)
            if cv2.waitKey(1) in (ord("q"), ESC_KEY):
                break

    finally:
        pipeline.stop()
        cv2.destroyAllWindows()
        print("Stopped.")


if __name__ == "__main__":
    main()
