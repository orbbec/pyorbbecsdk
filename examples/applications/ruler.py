# ******************************************************************************
#  pyorbbecsdk Application Example — Depth Ruler
#
#  What you will learn:
#    1. How to align depth to color so every color pixel has a valid depth value
#    2. How to read per-pixel depth (mm) from the aligned depth frame
#    3. How to back-project a 2D image point to 3D using camera intrinsics
#    4. How to compute the real-world Euclidean distance between two 3D points
#    5. How to build an interactive OpenCV mouse-driven measurement overlay
#
#  Usage:
#    Left-click and drag on the color image to draw a measurement line.
#    Release to finalize — the 3D distance (mm) is shown on the line.
#    Press 'C' to clear all measurements.
#    Press 'Q' or ESC to quit.
#
#  How it works:
#    For each endpoint (u, v) the tool reads depth_mm[v, u] from the aligned
#    depth frame, then back-projects to 3D:
#      Z  = depth_mm
#      X  = (u - cx) * Z / fx
#      Y  = (v - cy) * Z / fy
#    Distance = ||P2 - P1||_2  (Euclidean norm, in mm)
#
#  Run:
#    python examples/applications/ruler.py
# ******************************************************************************

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from typing import Optional

import cv2
import numpy as np
from utils import frame_to_bgr_image

from pyorbbecsdk import (
    AlignFilter,
    Config,
    Context,
    OBError,
    OBSensorType,
    OBStreamType,
    Pipeline,
)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
MIN_DEPTH_MM = 100  # ignore depth values below this (mm)
MAX_DEPTH_MM = 8000  # ignore depth values above this (mm)
ESC_KEY = 27
WINDOW_TITLE = "Depth Ruler  |  Drag to measure  |  C = clear  |  Q/ESC = quit"

# ---------------------------------------------------------------------------
# Global mouse state
# ---------------------------------------------------------------------------
_drawing = False  # True while left button is held
_pt_start = None  # (x, y) where drag started
_pt_end = None  # (x, y) current drag position (updated on move)
_segments = []  # finished segments: list of (pt_start, pt_end, dist_mm)
_depth_mm = None  # latest aligned depth array (float32, shape H×W)
_cam_param = None  # OBCameraParam (filled after pipeline starts)


def _pixel_to_3d(u: int, v: int, depth_arr: np.ndarray, intr) -> Optional[np.ndarray]:
    """
    Back-project pixel (u, v) to a 3D point using the color camera intrinsics.

    Returns a numpy array [X, Y, Z] in mm, or None if depth is invalid.

    The formula is the standard pinhole back-projection:
        Z = depth_arr[v, u]
        X = (u - cx) * Z / fx
        Y = (v - cy) * Z / fy
    """
    h, w = depth_arr.shape[:2]
    if not (0 <= u < w and 0 <= v < h):
        return None

    z = float(depth_arr[v, u])
    if not (MIN_DEPTH_MM <= z <= MAX_DEPTH_MM):
        return None

    x = (u - intr.cx) * z / intr.fx
    y = (v - intr.cy) * z / intr.fy
    return np.array([x, y, z], dtype=np.float64)


def _mouse_callback(event, x, y, flags, param):
    """OpenCV mouse callback — tracks drag gestures."""
    global _drawing, _pt_start, _pt_end, _segments, _depth_mm, _cam_param

    if event == cv2.EVENT_LBUTTONDOWN:
        _drawing = True
        _pt_start = (x, y)
        _pt_end = (x, y)

    elif event == cv2.EVENT_MOUSEMOVE and _drawing:
        _pt_end = (x, y)

    elif event == cv2.EVENT_LBUTTONUP and _drawing:
        _drawing = False
        _pt_end = (x, y)

        # Compute 3D distance if depth data is available
        if _depth_mm is not None and _cam_param is not None:
            intr = _cam_param.rgb_intrinsic  # color intrinsics (aligned frame)
            p1 = _pixel_to_3d(_pt_start[0], _pt_start[1], _depth_mm, intr)
            p2 = _pixel_to_3d(_pt_end[0], _pt_end[1], _depth_mm, intr)

            if p1 is not None and p2 is not None:
                dist_mm = float(np.linalg.norm(p2 - p1))
                _segments.append((_pt_start, _pt_end, dist_mm))
            else:
                # At least one endpoint has invalid depth — store as "?"
                _segments.append((_pt_start, _pt_end, None))
        else:
            _segments.append((_pt_start, _pt_end, None))

        _pt_start = None
        _pt_end = None


def _draw_overlay(canvas: np.ndarray) -> np.ndarray:
    """
    Draw all finished segments and the current in-progress drag line
    on top of the color image.
    """
    out = canvas.copy()

    # --- Finished segments ---
    for seg_start, seg_end, dist in _segments:
        color = (0, 220, 0)  # green for valid distance
        if dist is None:
            color = (0, 80, 220)  # orange-ish for invalid depth

        cv2.line(out, seg_start, seg_end, color, 2)
        cv2.circle(out, seg_start, 5, color, -1)
        cv2.circle(out, seg_end, 5, color, -1)

        # Label at midpoint
        mx = (seg_start[0] + seg_end[0]) // 2
        my = (seg_start[1] + seg_end[1]) // 2
        label = f"{dist:.1f} mm" if dist is not None else "no depth"
        # Black outline for readability
        cv2.putText(out, label, (mx + 4, my - 4), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 3)
        cv2.putText(
            out,
            label,
            (mx + 4, my - 4),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            1,
        )

    # --- In-progress drag line ---
    if _drawing and _pt_start and _pt_end:
        cv2.line(out, _pt_start, _pt_end, (255, 200, 0), 1)
        cv2.circle(out, _pt_start, 4, (255, 200, 0), -1)

    # --- Help text (bottom) ---
    h = out.shape[0]
    hint = "Drag to measure | C = clear | Q/ESC = quit"
    cv2.putText(out, hint, (8, h - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 0), 2)
    cv2.putText(out, hint, (8, h - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (220, 220, 220), 1)

    return out


def main():
    global _depth_mm, _cam_param, _segments

    ctx = Context()

    # --- Step 1: Start pipeline with color + depth ---
    pipeline = Pipeline()
    config = Config()

    for sensor_type in (OBSensorType.DEPTH_SENSOR, OBSensorType.COLOR_SENSOR):
        try:
            profile_list = pipeline.get_stream_profile_list(sensor_type)
            profile = profile_list.get_default_video_stream_profile()
            config.enable_stream(profile)
        except OBError as e:
            print(f"ERROR: Cannot configure {sensor_type.name}: {e}")
            sys.exit(1)

    pipeline.start(config)
    print("Pipeline started. Waiting for first frame …")

    # --- Step 2: Retrieve camera parameters (after first frame) ---
    #   get_camera_param() requires the pipeline to be running and at least
    #   one frame to have been delivered so the active profiles are resolved.
    for _ in range(30):
        fs = pipeline.wait_for_frames(1000)
        if fs is not None:
            _cam_param = pipeline.get_camera_param()
            print(
                f"Color intrinsics: fx={_cam_param.rgb_intrinsic.fx:.2f}  "
                f"fy={_cam_param.rgb_intrinsic.fy:.2f}  "
                f"cx={_cam_param.rgb_intrinsic.cx:.2f}  "
                f"cy={_cam_param.rgb_intrinsic.cy:.2f}"
            )
            break

    if _cam_param is None:
        print("ERROR: Could not retrieve camera parameters.")
        pipeline.stop()
        sys.exit(1)

    # --- Step 3: Set up AlignFilter (depth → color) ---
    #   The AlignFilter reprojects the depth frame into the color camera's
    #   coordinate system so that depth[v, u] corresponds to color[v, u].
    align_filter = AlignFilter(OBStreamType.COLOR_STREAM)

    # --- Step 4: OpenCV window with mouse callback ---
    cv2.namedWindow(WINDOW_TITLE, cv2.WINDOW_NORMAL)
    cv2.setMouseCallback(WINDOW_TITLE, _mouse_callback)

    print("Ready. Drag on the image to measure distance.")
    print("Press 'C' to clear  |  'Q'/ESC to quit.\n")

    try:
        while True:
            frame_set = pipeline.wait_for_frames(1000)
            if frame_set is None:
                continue

            # Apply alignment filter
            aligned_set = align_filter.process(frame_set)
            if aligned_set is None:
                continue
            aligned_set = aligned_set.as_frame_set()

            # --- Extract color frame ---
            color_frame = aligned_set.get_color_frame()
            if color_frame is None:
                continue
            color_img = frame_to_bgr_image(color_frame)
            if color_img is None:
                continue

            # --- Extract aligned depth frame ---
            depth_frame = aligned_set.get_depth_frame()
            if depth_frame is None:
                continue

            w = depth_frame.get_width()
            h = depth_frame.get_height()
            scale = depth_frame.get_depth_scale()
            raw = np.frombuffer(depth_frame.get_data(), dtype=np.uint16)
            _depth_mm = raw.reshape(h, w).astype(np.float32) * scale  # mm

            # --- Draw overlay and show ---
            display = _draw_overlay(color_img)
            cv2.imshow(WINDOW_TITLE, display)

            key = cv2.waitKey(1) & 0xFF
            if key in (ord("q"), ESC_KEY):
                break
            elif key == ord("c"):
                _segments.clear()
                print("Measurements cleared.")

    finally:
        pipeline.stop()
        cv2.destroyAllWindows()
        print("Stopped.")


if __name__ == "__main__":
    main()
