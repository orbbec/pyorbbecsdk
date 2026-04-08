# ******************************************************************************
#  pyorbbecsdk Beginner Example 03 — Color and Depth Aligned Streams
#
#  What you will learn:
#    1. How to enable color and depth streams simultaneously
#    2. How to use software AlignFilter to project depth into the color camera view
#    3. How to enable hardware D2C alignment via pipeline config (--hw flag)
#    4. How to convert raw uint16 depth data to a color-mapped overlay
#    5. How to blend aligned depth and color for visual verification
#
#  Keyboard (software mode, default):
#    T       — Toggle align direction: Depth→Color (D2C) ↔ Color→Depth (C2D)
#    F       — Toggle hardware frame synchronization ON / OFF
#    Q / ESC — Quit
#
#  Keyboard (hardware D2C mode, --hw):
#    T       — Toggle hardware D2C ON / OFF
#    + / -   — Adjust depth overlay transparency
#    Q / ESC — Quit
#
#  Dependencies: numpy, opencv-python, utils.py
#
#  Device requirement: All
#
#  Run:
#    python examples/beginner/03_color_and_depth_aligned.py          # software align (default)
#    python examples/beginner/03_color_and_depth_aligned.py --hw     # hardware D2C
# ******************************************************************************

import argparse
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import cv2
import numpy as np
from utils import frame_to_bgr_image

from pyorbbecsdk import OBAlignMode  # type: ignore
from pyorbbecsdk import (
    AlignFilter,
    Config,
    Context,
    OBFormat,
    OBFrameAggregateOutputMode,
    OBSensorType,
    OBStreamType,
    Pipeline,
)

# --- Configuration Constants ---
ESC_KEY = 27
MIN_DEPTH = 20  # Minimum valid depth distance in mm
MAX_DEPTH = 10000  # Maximum valid depth distance in mm


# ---------------------------------------------------------------------------
# Hardware D2C helpers (used only with --hw)
# ---------------------------------------------------------------------------


def get_hw_stream_config(pipeline: Pipeline):
    """
    Build a Config that enables hardware D2C alignment.

    Iterates color profiles until it finds one with RGB format and a matching
    hardware-aligned depth profile, then sets OBAlignMode.HW_MODE.
    Returns a Config on success, or None if hardware D2C is not supported.
    """
    config = Config()
    try:
        profile_list = pipeline.get_stream_profile_list(OBSensorType.COLOR_SENSOR)
        for i in range(len(profile_list)):
            color_profile = profile_list[i]
            if color_profile.get_format() != OBFormat.RGB:
                continue
            hw_depth_list = pipeline.get_d2c_depth_profile_list(color_profile, OBAlignMode.HW_MODE)
            if len(hw_depth_list) == 0:
                continue
            config.enable_stream(hw_depth_list[0])
            config.enable_stream(color_profile)
            config.set_align_mode(OBAlignMode.HW_MODE)
            return config
    except Exception as e:
        print(f"HW D2C config error: {e}")
    return None


def switch_hw_d2c(pipeline: Pipeline, config: Config, enable: bool):
    """Stop the pipeline, flip the HW D2C align mode, and restart."""
    pipeline.stop()
    time.sleep(0.1)
    config.set_align_mode(OBAlignMode.HW_MODE if enable else OBAlignMode.DISABLE)
    print(f"Hardware D2C: {'Enabled' if enable else 'Disabled'}")
    pipeline.start(config)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    # Check if device is connected
    ctx = Context()
    device_list = ctx.query_devices()
    if device_list.get_count() == 0:
        print("Device Not Found! Please connect an Orbbec camera and try again.")
        return

    parser = argparse.ArgumentParser(description="Color + Depth aligned viewer")
    parser.add_argument(
        "--hw",
        action="store_true",
        help="Use hardware D2C alignment instead of software AlignFilter",
    )
    args = parser.parse_args()

    window_name = "Color + Depth Aligned  |  Q/ESC = quit"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, 1280, 720)

    pipeline = Pipeline()
    config = None

    # ------------------------------------------------------------------
    # Stream setup — differs between SW and HW mode
    # ------------------------------------------------------------------
    if args.hw:
        # ---- Hardware D2C mode ----
        try:
            pipeline.enable_frame_sync()
        except Exception as e:
            print(f"Frame sync warning: {e}")

        config = get_hw_stream_config(pipeline)
        if config is None:
            print("ERROR: Hardware D2C is not supported on this device. Try without --hw.")
            return

        enable_hw_d2c = True
        alpha = 0.5
        alpha_step = 0.1

        print("\n========== Hardware D2C Align ==========")
        print("T       : Enable / Disable HW D2C")
        print("+ / -   : Adjust depth overlay transparency")
        print("Q / ESC : Quit")
        print("========================================\n")

    else:
        # ---- Software AlignFilter mode ----
        config = Config()
        align_mode = 0  # 0 = D2C, 1 = C2D
        enable_sync = False

        try:
            profile_list = pipeline.get_stream_profile_list(OBSensorType.COLOR_SENSOR)
            color_profile = profile_list.get_video_stream_profile(0, 0, OBFormat.RGB, 0)
            config.enable_stream(color_profile)

            profile_list = pipeline.get_stream_profile_list(OBSensorType.DEPTH_SENSOR)
            depth_profile = profile_list.get_default_video_stream_profile()
            config.enable_stream(depth_profile)

            config.set_frame_aggregate_output_mode(OBFrameAggregateOutputMode.FULL_FRAME_REQUIRE)
        except Exception as e:
            print(f"Stream configuration error: {e}")
            return

        align_filter = AlignFilter(align_to_stream=OBStreamType.COLOR_STREAM)

        print("\nControls:")
        print("  T       — Toggle align direction  (D2C ↔ C2D)")
        print("  F       — Toggle frame sync        (ON / OFF)")
        print("  Q / ESC — Quit\n")

    # ------------------------------------------------------------------
    # Start pipeline
    # ------------------------------------------------------------------
    try:
        pipeline.start(config)
    except Exception as e:
        print(f"Pipeline start error: {e}")
        return

    # ------------------------------------------------------------------
    # Frame loop
    # ------------------------------------------------------------------
    while True:
        try:
            frames = pipeline.wait_for_frames(1000)
            if not frames:
                continue

            color_frame = frames.get_color_frame()
            depth_frame = frames.get_depth_frame()
            if not color_frame or not depth_frame:
                continue

            # -- Software alignment (SW mode only) --
            if not args.hw:
                frames = align_filter.process(frames)
                if not frames:
                    continue
                color_frame = frames.get_color_frame()
                depth_frame = frames.get_depth_frame()
                if not color_frame or not depth_frame:
                    continue

            # -- Convert color frame --
            color_image = frame_to_bgr_image(color_frame)
            if color_image is None:
                continue

            # -- Convert depth frame --
            try:
                depth_data = np.frombuffer(depth_frame.get_data(), dtype=np.uint16).reshape(
                    (depth_frame.get_height(), depth_frame.get_width())
                )
            except ValueError:
                continue

            depth_data = depth_data.astype(np.float32) * depth_frame.get_depth_scale()

            if args.hw:
                depth_data = np.clip(depth_data, MIN_DEPTH, MAX_DEPTH)
            else:
                depth_data = np.where((depth_data > MIN_DEPTH) & (depth_data < MAX_DEPTH), depth_data, 0)

            depth_image = cv2.normalize(depth_data, None, 0, 255, cv2.NORM_MINMAX)
            depth_image = cv2.applyColorMap(depth_image.astype(np.uint8), cv2.COLORMAP_JET)

            # Resize depth to match color dimensions (needed when HW D2C is disabled)
            h, w = color_image.shape[:2]
            if depth_image.shape[:2] != (h, w):
                depth_image = cv2.resize(depth_image, (w, h), interpolation=cv2.INTER_NEAREST)

            # -- Blend and display --
            blend_alpha = alpha if args.hw else 0.5
            overlay = cv2.addWeighted(color_image, 1 - blend_alpha, depth_image, blend_alpha, 0)

            # Status text
            if args.hw:
                status = f"HW D2C: {'ON' if enable_hw_d2c else 'OFF'}  alpha={blend_alpha:.1f}"
            else:
                mode_str = "D2C (Depth To Color)" if align_mode == 0 else "C2D (Color To Depth)"
                sync_str = "Sync: ON" if enable_sync else "Sync: OFF"
                status = f"{mode_str} | {sync_str}"

            cv2.putText(
                overlay,
                status,
                (20, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 255),
                2,
            )
            cv2.imshow(window_name, overlay)

            # -- Keyboard input --
            key = cv2.waitKey(1) & 0xFF
            if key in (ord("q"), ESC_KEY):
                break

            if args.hw:
                if key in (ord("t"), ord("T")):
                    enable_hw_d2c = not enable_hw_d2c
                    switch_hw_d2c(pipeline, config, enable_hw_d2c)
                elif key in (ord("+"), ord("=")):
                    alpha = min(1.0, alpha + alpha_step)
                    print(f"Alpha: {alpha:.2f}")
                elif key in (ord("-"), ord("_")):
                    alpha = max(0.0, alpha - alpha_step)
                    print(f"Alpha: {alpha:.2f}")
            else:
                if key in (ord("t"), ord("T")):
                    align_mode = (align_mode + 1) % 2
                    if align_mode == 0:
                        align_filter = AlignFilter(align_to_stream=OBStreamType.COLOR_STREAM)
                        print("Mode: Depth To Color")
                    else:
                        align_filter = AlignFilter(align_to_stream=OBStreamType.DEPTH_STREAM)
                        print("Mode: Color To Depth")
                elif key in (ord("f"), ord("F")):
                    enable_sync = not enable_sync
                    if enable_sync:
                        pipeline.enable_frame_sync()
                        print("Frame sync: ON")
                    else:
                        pipeline.disable_frame_sync()
                        print("Frame sync: OFF")

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Runtime error: {e}")
            continue

    cv2.destroyAllWindows()
    pipeline.stop()


if __name__ == "__main__":
    main()
