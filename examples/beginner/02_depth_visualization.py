# ******************************************************************************
#  pyorbbecsdk Beginner Example 02 — Depth Visualization
#
#  What you will learn:
#    1. How to configure and start a depth stream
#    2. How to convert raw uint16 depth data to millimeters
#    3. How to clip depth to a fixed range (avoids flickering normalization)
#    4. How to add gamma correction for better near-field depth gradients
#    5. How to apply surface-normal lighting (Scharr gradient) for 3D relief
#    6. How to overlay center distance and a depth range legend
#
#  Rendering pipeline (based on ui.py):
#    raw uint16  →  mm float  →  clip [MIN, MAX]  →  gamma 0.8  →  8-bit
#    →  Scharr gradient  →  diffuse lighting  →  COLORMAP_TURBO  →  display
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
MIN_DEPTH_MM = 100    # Clip depth closer than this (mm)
MAX_DEPTH_MM = 10000  # Clip depth farther than this (mm)
WINDOW_TITLE = "Depth Viewer  |  C = next colormap  |  Q/ESC = quit"
ESC_KEY = 27

# Press 'C' during playback to cycle through these options.
# Each entry: (cv2 colormap constant, display name)
COLORMAPS = [
    (cv2.COLORMAP_TURBO,   "TURBO"),    # warm→cool, high perceptual separation
    (cv2.COLORMAP_MAGMA,   "MAGMA"),    # dark→light, great for low-light scenes
    (cv2.COLORMAP_PLASMA,  "PLASMA"),   # purple→yellow, uniform brightness
    (cv2.COLORMAP_INFERNO, "INFERNO"),  # deep black→bright yellow, dramatic
    (cv2.COLORMAP_VIRIDIS, "VIRIDIS"),  # scientific standard, colorblind-safe
    (cv2.COLORMAP_JET,     "JET"),      # classic rainbow, familiar look
    (cv2.COLORMAP_HOT,     "HOT"),      # black→red→yellow→white, heat-map style
    (cv2.COLORMAP_OCEAN,   "OCEAN"),    # dark blue→white, underwater aesthetic
]
_cmap_index = 0   # current selection


def _render_depth_3d(depth_mm: np.ndarray) -> np.ndarray:
    """
    Convert a float32 depth-in-mm array into a 3D-looking BGR image.

    Steps (mirrors ui.py _on_depth_frame):
      1. Clip to [MIN_DEPTH_MM, MAX_DEPTH_MM] — fixed range keeps colors stable
      2. Gamma correction (0.8) — stretches near-field gradient for better detail
      3. Map to 8-bit
      4. Scharr gradient → simplified diffuse lighting from top-left
      5. Apply COLORMAP_TURBO
      6. Multiply color by per-pixel lighting (gives relief / 3D feel)
      7. Draw corner frame markers
    """
    # --- 1. Clip to fixed range ---
    depth_clipped = np.clip(depth_mm, MIN_DEPTH_MM, MAX_DEPTH_MM)

    # --- 2. Normalize [0, 1] then apply gamma ---
    depth_norm = (depth_clipped - MIN_DEPTH_MM) / (MAX_DEPTH_MM - MIN_DEPTH_MM)
    depth_gamma = np.power(depth_norm, 0.8)          # γ < 1 → brighten near-field

    # --- 3. Map to uint8 ---
    depth_8bit = (depth_gamma * 255).astype(np.uint8)

    # --- 4. Surface-normal lighting via Scharr gradient ---
    #   Scharr gives a more isotropic gradient than Sobel.
    #   grad_x, grad_y are the x/y slopes of the depth surface.
    #   Light direction: top-left (-0.707, -0.707, 0).
    #   Diffuse term: dot(normal, light) ≈ -(grad_x + grad_y) / magnitude
    grad_x = cv2.Scharr(depth_8bit, cv2.CV_32F, 1, 0)
    grad_y = cv2.Scharr(depth_8bit, cv2.CV_32F, 0, 1)
    mag    = cv2.magnitude(grad_x, grad_y) + 1.0      # +1 avoids divide-by-zero

    # Diffuse coefficient: 0.15 (subtle); ambient: 0.85 (keeps dark areas visible)
    lighting = -0.707 * (grad_x + grad_y) / mag
    lighting = lighting * 0.15 + 0.85
    np.clip(lighting, 0.7, 1.0, out=lighting)         # floor at 70% brightness

    # --- 5. Apply colormap (current selection from COLORMAPS list) ---
    colormap, cmap_name = COLORMAPS[_cmap_index]
    depth_colored = cv2.applyColorMap(depth_8bit, colormap)

    # --- 6. Multiply color by lighting (broadcast over 3 channels) ---
    depth_colored = (depth_colored * lighting[..., np.newaxis]).astype(np.uint8)

    # --- 7. Corner frame markers (subtle 3D-frame feel) ---
    h, w    = depth_colored.shape[:2]
    clen    = 20
    ccol    = (200, 200, 200)
    cv2.line(depth_colored, (5, 5),         (5 + clen, 5),     ccol, 1)
    cv2.line(depth_colored, (5, 5),         (5, 5 + clen),     ccol, 1)
    cv2.line(depth_colored, (w-6, 5),       (w-6-clen, 5),     ccol, 1)
    cv2.line(depth_colored, (w-6, 5),       (w-6, 5+clen),     ccol, 1)
    cv2.line(depth_colored, (5, h-6),       (5+clen, h-6),     ccol, 1)
    cv2.line(depth_colored, (5, h-6),       (5, h-6-clen),     ccol, 1)
    cv2.line(depth_colored, (w-6, h-6),     (w-6-clen, h-6),   ccol, 1)
    cv2.line(depth_colored, (w-6, h-6),     (w-6, h-6-clen),   ccol, 1)

    # --- 8. Colormap name (top-right, press C to cycle) ---
    label_size, _ = cv2.getTextSize(cmap_name, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
    cv2.putText(depth_colored, cmap_name,
                (w - label_size[0] - 8, 25),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    return depth_colored


def main():
    # Suppress SDK info messages; set DEBUG for diagnostics
    ctx = Context()
    ctx.set_logger_level(OBLogLevel.WARNING)

    # --- Step 1: Create pipeline and configure depth stream ---
    pipeline = Pipeline()

    config = Config()
    try:
        profile_list  = pipeline.get_stream_profile_list(OBSensorType.DEPTH_SENSOR)
        depth_profile = profile_list.get_default_video_stream_profile()
        print(f"Depth profile: {depth_profile}")
        config.enable_stream(depth_profile)
    except OBError as e:
        print(f"ERROR: Cannot configure depth stream: {e}")
        sys.exit(1)

    pipeline.start(config)
    print(f"Depth stream started. Range: {MIN_DEPTH_MM} – {MAX_DEPTH_MM} mm")
    print("Press 'q' or ESC to quit.\n")

    try:
        while True:
            # --- Step 2: Wait for the next frame set (up to 1 second) ---
            frame_set = pipeline.wait_for_frames(1000)
            if frame_set is None:
                continue

            depth_frame = frame_set.get_depth_frame()
            if depth_frame is None:
                continue

            # --- Step 3: Convert raw uint16 to float32 millimeters ---
            width  = depth_frame.get_width()
            height = depth_frame.get_height()
            scale  = depth_frame.get_depth_scale()   # e.g. 0.1 → 1 unit = 0.1 mm

            raw      = np.frombuffer(depth_frame.get_data(), dtype=np.uint16)
            depth_mm = raw.reshape(height, width).astype(np.float32) * scale

            # --- Step 4: Render with 3D lighting effect ---
            display = _render_depth_3d(depth_mm)

            # --- Step 5: Overlay center-point distance ---
            cy, cx       = height // 2, width // 2
            center_dist  = depth_mm[cy, cx]
            in_range     = MIN_DEPTH_MM <= center_dist <= MAX_DEPTH_MM
            dist_label   = f"{center_dist:.0f} mm" if in_range else "out of range"

            cv2.circle(display, (cx, cy), 5, (255, 255, 255), -1)
            cv2.putText(display, dist_label,
                        (cx + 8, cy + 6),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            # --- Step 6: Depth range legend (top-left) ---
            cv2.putText(display, f"{MIN_DEPTH_MM}-{MAX_DEPTH_MM} mm",
                        (10, 25),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

            cv2.imshow(WINDOW_TITLE, display)
            key = cv2.waitKey(1)
            if key in (ord("q"), ESC_KEY):
                break
            elif key == ord("c"):
                # Cycle to next colormap
                global _cmap_index
                _cmap_index = (_cmap_index + 1) % len(COLORMAPS)
                print(f"Colormap → {COLORMAPS[_cmap_index][1]}")

    finally:
        pipeline.stop()
        cv2.destroyAllWindows()
        print("Stopped.")


if __name__ == "__main__":
    main()
