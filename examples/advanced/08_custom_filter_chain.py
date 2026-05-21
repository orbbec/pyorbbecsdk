# ******************************************************************************
#  pyorbbecsdk Advanced Example 08 — Custom Filter Chain
#
#  What you will learn:
#    1. How to chain multiple post-processing filters in sequence
#    2. What each filter does and when to use it
#    3. How to compare before/after filter effects side-by-side
#    4. How to tune filter parameters via keyboard
#
#  Filter chain applied:
#    Raw Depth → [Temporal] → [Spatial] → [HoleFill] → [Threshold] → Display
#
#  Note: On Linux the depth stream may use RLE compression. The example
#  checks the frame format and only processes uncompressed frames (Y16,
#  Z16, Y12C4), mirroring the C++ SDK behaviour.
#
#  Keyboard controls (while window is focused):
#    T  — toggle TemporalFilter on/off
#    S  — toggle SpatialFilter on/off
#    H  — toggle HoleFillingFilter on/off
#    +  — increase threshold max depth by 500mm
#    -  — decrease threshold max depth by 500mm
#    q  — quit
#
#  Run:
#    python examples/advanced/08_custom_filter_chain.py
# ******************************************************************************
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import sys

import cv2
import numpy as np

from pyorbbecsdk import (
    Config,
    Context,
    HoleFillingFilter,
    OBFormat,
    OBError,
    OBLogLevel,
    OBSensorType,
    OBStreamType,
    Pipeline,
    SpatialAdvancedFilter,
    TemporalFilter,
    ThresholdFilter,
)

# Pixel formats that contain raw uncompressed 16-bit depth values.
_RAW_DEPTH_FORMATS = {OBFormat.Y16, OBFormat.Z16, OBFormat.Y12C4}


def _get_depth_array(depth_frame):
    """Return a (height, width) uint16 numpy array, or None if unsupported.

    On Linux the depth stream may deliver RLE-compressed frames which cannot
    be reshaped directly.  We skip those frames, matching the C++ behaviour
    in ``utils_opencv.cpp``.
    """
    if depth_frame.get_format() not in _RAW_DEPTH_FORMATS:
        return None
    raw = np.frombuffer(depth_frame.get_data(), dtype=np.uint16)
    try:
        return raw.reshape(depth_frame.get_height(), depth_frame.get_width())
    except ValueError:
        return None

ESC_KEY = 27
MIN_DEPTH_MM = 100
MAX_DEPTH_MM = 4000  # adjustable with +/-


def depth_to_colormap(depth_frame, min_mm, max_mm):
    """Convert a raw depth frame to a color-mapped BGR image."""
    w = depth_frame.get_width()
    h = depth_frame.get_height()
    scale = depth_frame.get_depth_scale()
    raw = _get_depth_array(depth_frame)
    if raw is None:
        return None
    mm = raw.astype(np.float32) * scale
    valid = np.where((mm >= min_mm) & (mm <= max_mm), mm, 0).astype(np.uint16)
    norm = cv2.normalize(valid, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
    return cv2.applyColorMap(norm, cv2.COLORMAP_JET)


def add_label(img, text, color=(0, 255, 0)):
    cv2.putText(img, text, (8, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.65, color, 2)
    return img


def main():
    global MAX_DEPTH_MM

    # Check if device is connected
    ctx = Context()
    device_list = ctx.query_devices()
    if device_list.get_count() == 0:
        print("Device Not Found! Please connect an Orbbec camera and try again.")
        return

    ctx.set_logger_level(OBLogLevel.WARNING)

    pipeline = Pipeline()
    config = Config()

    try:
        config.enable_stream(OBStreamType.DEPTH_STREAM)
    except OBError as e:
        print(f"ERROR: {e}")
        sys.exit(1)

    pipeline.start(config)

    # ----- Filter objects -----
    temporal = TemporalFilter()
    spatial = SpatialAdvancedFilter()
    hole_fill = HoleFillingFilter()
    threshold = ThresholdFilter()
    threshold.set_value_range(MIN_DEPTH_MM, MAX_DEPTH_MM)

    # ----- Filter enable flags -----
    use_temporal = True
    use_spatial = True
    use_hole_fill = True

    print("Filter Chain Demo")
    print("  T = toggle Temporal filter")
    print("  S = toggle Spatial filter")
    print("  H = toggle HoleFill filter")
    print("  +/- = adjust max depth")
    print("  q/ESC = quit\n")

    try:
        while True:
            frame_set = pipeline.wait_for_frames(1000)
            if frame_set is None:
                continue

            raw_frame = frame_set.get_depth_frame()
            if raw_frame is None:
                continue

            # Skip compressed frames (RLE etc.) — the filter chain
            # requires uncompressed pixel data (Y16 / Z16 / Y12C4).
            if raw_frame.get_format() not in _RAW_DEPTH_FORMATS:
                continue

            # ---- Apply filter chain ----
            filtered = raw_frame

            if use_temporal:
                out = temporal.process(filtered)
                if out is not None:
                    filtered = out

            if use_spatial:
                out = spatial.process(filtered)
                if out is not None:
                    filtered = out

            if use_hole_fill:
                out = hole_fill.process(filtered)
                if out is not None:
                    filtered = out

            threshold.set_value_range(MIN_DEPTH_MM, MAX_DEPTH_MM)
            out = threshold.process(filtered)
            if out is not None:
                filtered = out

            # ---- Build display panels ----
            raw_vis = depth_to_colormap(raw_frame, MIN_DEPTH_MM, MAX_DEPTH_MM)
            if raw_vis is None:
                continue
            filtered = filtered.as_depth_frame()
            flt_vis = depth_to_colormap(filtered, MIN_DEPTH_MM, MAX_DEPTH_MM)
            if flt_vis is None:
                continue

            # Active filter labels
            active = []
            if use_temporal:
                active.append("Temporal")
            if use_spatial:
                active.append("Spatial")
            if use_hole_fill:
                active.append("HoleFill")
            active.append(f"Threshold(<{MAX_DEPTH_MM}mm)")
            filter_str = "+".join(active) if active else "None"

            add_label(raw_vis.copy(), "RAW DEPTH")
            add_label(flt_vis, f"FILTERED: {filter_str}")

            display = np.hstack([raw_vis, flt_vis])
            cv2.imshow("Filter Chain  |  T/S/H/+/- keys", display)

            key = cv2.waitKey(1) & 0xFF
            if key in (ord("q"), ESC_KEY):
                break
            elif key == ord("t"):
                use_temporal = not use_temporal
                print(f"Temporal filter: {'ON' if use_temporal else 'OFF'}")
            elif key == ord("s"):
                use_spatial = not use_spatial
                print(f"Spatial filter: {'ON' if use_spatial else 'OFF'}")
            elif key == ord("h"):
                use_hole_fill = not use_hole_fill
                print(f"HoleFill filter: {'ON' if use_hole_fill else 'OFF'}")
            elif key in (ord("+"), ord("=")):
                MAX_DEPTH_MM = min(MAX_DEPTH_MM + 500, 10000)
                print(f"Max depth: {MAX_DEPTH_MM}mm")
            elif key == ord("-"):
                MAX_DEPTH_MM = max(MAX_DEPTH_MM - 500, MIN_DEPTH_MM + 500)
                print(f"Max depth: {MAX_DEPTH_MM}mm")

    finally:
        pipeline.stop()
        cv2.destroyAllWindows()
        print("Stopped.")


if __name__ == "__main__":
    main()
