# ******************************************************************************
#  pyorbbecsdk Beginner Example 02 — Depth Visualization
#
#  What you will learn:
#    1. How to configure and start a depth stream
#    2. How to convert raw uint16 depth data to millimeters
#    3. How to clip depth to a fixed range (avoids flickering normalization)
#    4. How to toggle between 2D simple and 3D relief rendering modes
#    5. How to add gamma correction and surface-normal lighting for 3D mode
#    6. How to overlay center distance and a depth range legend
#
#  Rendering modes:
#    2D mode: raw uint16 → mm float → clip [MIN, MAX] → normalize → colormap
#    3D mode: raw uint16 → mm float → clip [MIN, MAX] → gamma 0.8 → 8-bit
#             → Scharr gradient → diffuse lighting → colormap → display
#
#  Controls:
#    M        —  Toggle 2D/3D rendering mode (default: 3D)
#    C        —  Cycle colormap
#    Q / ESC  —  Quit
#
#  Run:
#    python examples/beginner/02_depth_visualization.py
# ******************************************************************************

import sys

import cv2
import numpy as np

from pyorbbecsdk import Config, Context, OBError, OBSensorType, Pipeline

# ---------------------------------------------------------------------------
# Configuration — adjust these for your scene
# ---------------------------------------------------------------------------
MIN_DEPTH_MM = 100  # Clip depth closer than this (mm)
MAX_DEPTH_MM = 5000  # Clip depth farther than this (mm)
WINDOW_TITLE = "Depth Viewer  |  M = 2D/3D  |  C = colormap  |  Q/ESC = quit"
ESC_KEY = 27

# Press 'C' to cycle through these colormaps.
# Each entry: (cv2 colormap constant, display name)
COLORMAPS = [
    (cv2.COLORMAP_JET, "JET"),  # classic rainbow, familiar look (default)
    (cv2.COLORMAP_TURBO, "TURBO"),  # warm→cool, high perceptual separation
    (cv2.COLORMAP_VIRIDIS, "VIRIDIS"),  # perceptually uniform, colorblind-friendly
    (cv2.COLORMAP_MAGMA, "MAGMA"),  # dark→light, great for low-light scenes
    (cv2.COLORMAP_INFERNO, "INFERNO"),  # warm tones, high contrast
    (cv2.COLORMAP_BONE, "BONE"),  # grayscale-like with blue tint
    (cv2.COLORMAP_OCEAN, "OCEAN"),  # blue gradient
    (-1, "GRAY"),  # pure grayscale (special case)
]
_cmap_index = 0  # current selection (JET)
_use_3d_mode = True  # True = 3D relief lighting, False = 2D simple


def _render_depth_2d(depth_mm: np.ndarray) -> np.ndarray:
    """
    Simple 2D depth rendering: normalize + colormap.

    Steps:
      1. Clip to [MIN_DEPTH_MM, MAX_DEPTH_MM]
      2. Normalize to [0, 255]
      3. Apply selected colormap
    """
    depth_clipped = np.clip(depth_mm, MIN_DEPTH_MM, MAX_DEPTH_MM)
    depth_clipped = np.where(depth_clipped > MIN_DEPTH_MM, depth_clipped, 0)

    depth_norm = cv2.normalize(depth_clipped, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)

    # Apply selected colormap
    colormap, cmap_name = COLORMAPS[_cmap_index]
    if colormap == -1:  # GRAY (special case)
        depth_colored = cv2.cvtColor(depth_norm, cv2.COLOR_GRAY2BGR)
    else:
        depth_colored = cv2.applyColorMap(depth_norm, colormap)

    # Corner frame markers
    h, w = depth_colored.shape[:2]
    clen = 20
    ccol = (200, 200, 200)
    cv2.line(depth_colored, (5, 5), (5 + clen, 5), ccol, 1)
    cv2.line(depth_colored, (5, 5), (5, 5 + clen), ccol, 1)
    cv2.line(depth_colored, (w - 6, 5), (w - 6 - clen, 5), ccol, 1)
    cv2.line(depth_colored, (w - 6, 5), (w - 6, 5 + clen), ccol, 1)
    cv2.line(depth_colored, (5, h - 6), (5 + clen, h - 6), ccol, 1)
    cv2.line(depth_colored, (5, h - 6), (5, h - 6 - clen), ccol, 1)
    cv2.line(depth_colored, (w - 6, h - 6), (w - 6 - clen, h - 6), ccol, 1)
    cv2.line(depth_colored, (w - 6, h - 6), (w - 6, h - 6 - clen), ccol, 1)

    # Mode + colormap label (top-right)
    label = f"2D - {cmap_name}"
    label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
    cv2.putText(
        depth_colored,
        label,
        (w - label_size[0] - 8, 25),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (255, 255, 255),
        1,
    )

    return depth_colored


def _render_depth_3d(depth_mm: np.ndarray) -> np.ndarray:
    """
    3D relief depth rendering: gamma correction + Scharr gradient lighting.

    Steps (mirrors ui.py _on_depth_frame):
      1. Clip to [MIN_DEPTH_MM, MAX_DEPTH_MM] — fixed range keeps colors stable
      2. Gamma correction (0.8) — stretches near-field gradient for better detail
      3. Map to 8-bit
      4. Scharr gradient → simplified diffuse lighting from top-left
      5. Apply selected colormap
      6. Multiply color by per-pixel lighting (gives relief / 3D feel)
      7. Draw corner frame markers
    """
    # --- 1. Clip to fixed range ---
    depth_clipped = np.clip(depth_mm, MIN_DEPTH_MM, MAX_DEPTH_MM)

    # --- 2. Normalize [0, 1] then apply gamma ---
    depth_norm = (depth_clipped - MIN_DEPTH_MM) / (MAX_DEPTH_MM - MIN_DEPTH_MM)
    depth_gamma = np.power(depth_norm, 0.8)  # γ < 1 → brighten near-field

    # --- 3. Map to uint8 ---
    depth_8bit = (depth_gamma * 255).astype(np.uint8)

    # --- 4. Surface-normal lighting via Scharr gradient ---
    #   Scharr gives a more isotropic gradient than Sobel.
    #   grad_x, grad_y are the x/y slopes of the depth surface.
    #   Light direction: top-left (-0.707, -0.707, 0).
    #   Diffuse term: dot(normal, light) ≈ -(grad_x + grad_y) / magnitude
    grad_x = cv2.Scharr(depth_8bit, cv2.CV_32F, 1, 0)
    grad_y = cv2.Scharr(depth_8bit, cv2.CV_32F, 0, 1)
    mag = cv2.magnitude(grad_x, grad_y) + 1.0  # +1 avoids divide-by-zero

    # Diffuse coefficient: 0.15 (subtle); ambient: 0.85 (keeps dark areas visible)
    lighting = -0.707 * (grad_x + grad_y) / mag
    lighting = lighting * 0.15 + 0.85
    np.clip(lighting, 0.7, 1.0, out=lighting)  # floor at 70% brightness

    # --- 5. Apply colormap (current selection from COLORMAPS list) ---
    colormap, cmap_name = COLORMAPS[_cmap_index]
    if colormap == -1:  # GRAY (special case)
        depth_colored = cv2.cvtColor(depth_8bit, cv2.COLOR_GRAY2BGR)
    else:
        depth_colored = cv2.applyColorMap(depth_8bit, colormap)

    # --- 6. Multiply color by lighting (broadcast over 3 channels) ---
    depth_colored = (depth_colored * lighting[..., np.newaxis]).astype(np.uint8)

    # --- 7. Corner frame markers (subtle 3D-frame feel) ---
    h, w = depth_colored.shape[:2]
    clen = 20
    ccol = (200, 200, 200)
    cv2.line(depth_colored, (5, 5), (5 + clen, 5), ccol, 1)
    cv2.line(depth_colored, (5, 5), (5, 5 + clen), ccol, 1)
    cv2.line(depth_colored, (w - 6, 5), (w - 6 - clen, 5), ccol, 1)
    cv2.line(depth_colored, (w - 6, 5), (w - 6, 5 + clen), ccol, 1)
    cv2.line(depth_colored, (5, h - 6), (5 + clen, h - 6), ccol, 1)
    cv2.line(depth_colored, (5, h - 6), (5, h - 6 - clen), ccol, 1)
    cv2.line(depth_colored, (w - 6, h - 6), (w - 6 - clen, h - 6), ccol, 1)
    cv2.line(depth_colored, (w - 6, h - 6), (w - 6, h - 6 - clen), ccol, 1)

    # --- 8. Mode + colormap name (top-right, press C to cycle) ---
    label = f"3D - {cmap_name}"
    label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
    cv2.putText(
        depth_colored,
        label,
        (w - label_size[0] - 8, 25),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (255, 255, 255),
        1,
    )

    return depth_colored


def main():
    # Check if device is connected
    ctx = Context()
    device_list = ctx.query_devices()
    if device_list.get_count() == 0:
        print("Device Not Found! Please connect an Orbbec camera and try again.")
        return

    # --- Step 1: Create pipeline and configure depth stream ---
    pipeline = Pipeline()

    config = Config()
    try:
        profile_list = pipeline.get_stream_profile_list(OBSensorType.DEPTH_SENSOR)
        depth_profile = profile_list.get_default_video_stream_profile()
        print(f"Depth profile: {depth_profile}")
        config.enable_stream(depth_profile)
    except OBError as e:
        print(f"ERROR: Cannot configure depth stream: {e}")
        sys.exit(1)

    pipeline.start(config)
    print(f"Depth stream started. Range: {MIN_DEPTH_MM} – {MAX_DEPTH_MM} mm")
    print("Press 'M' to toggle 2D/3D, 'C' to change colormap, 'Q' or ESC to quit.\n")

    try:
        # Create a resizable window for the depth visualization
        cv2.namedWindow(WINDOW_TITLE, cv2.WINDOW_NORMAL)

        while True:
            # --- Step 2: Wait for the next frame set (up to 1 second) ---
            frame_set = pipeline.wait_for_frames(1000)
            if frame_set is None:
                continue

            depth_frame = frame_set.get_depth_frame()
            if depth_frame is None:
                continue

            # --- Step 3: Convert raw uint16 to float32 millimeters ---
            width = depth_frame.get_width()
            height = depth_frame.get_height()
            scale = depth_frame.get_depth_scale()  # e.g. 0.1 → 1 unit = 0.1 mm

            raw = np.frombuffer(depth_frame.get_data(), dtype=np.uint16)
            depth_mm = raw.reshape(height, width).astype(np.float32) * scale

            # --- Step 4: Render depth (2D or 3D mode, toggle with 'M') ---
            global _use_3d_mode
            if _use_3d_mode:
                display = _render_depth_3d(depth_mm)
            else:
                display = _render_depth_2d(depth_mm)

            # --- Step 5: Overlay center-point distance ---
            cy, cx = height // 2, width // 2
            center_dist = depth_mm[cy, cx]
            in_range = MIN_DEPTH_MM <= center_dist <= MAX_DEPTH_MM
            dist_label = f"{center_dist:.0f} mm" if in_range else "out of range"

            cv2.circle(display, (cx, cy), 5, (255, 255, 255), -1)
            cv2.putText(
                display,
                dist_label,
                (cx + 8, cy + 6),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2,
            )

            # --- Step 6: Depth range legend (top-left) ---
            cv2.putText(
                display,
                f"{MIN_DEPTH_MM}-{MAX_DEPTH_MM} mm",
                (10, 25),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),
                1,
            )

            cv2.imshow(WINDOW_TITLE, display)
            key = cv2.waitKey(1)
            if key in (ord("q"), ord("Q"), ESC_KEY):
                break
            elif key in (ord("m"), ord("M")):
                # Toggle 2D/3D rendering mode
                _use_3d_mode = not _use_3d_mode
                mode_str = "3D relief" if _use_3d_mode else "2D simple"
                print(f"Depth rendering mode → {mode_str}")
            elif key in (ord("c"), ord("C")):
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
