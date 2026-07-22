# ******************************************************************************
#  pyorbbecsdk Advanced Example 10 — HDR Depth Merge
#
#  What you will learn:
#    1. Enable HDR mode on the device to capture alternating-exposure depth frames
#    2. Use HdrMergeFilter to combine the exposure pair into a single HDR depth frame
#    3. Visualize the merged depth output with extended dynamic range
#    4. Compare HDR depth quality against standard single-exposure depth
#
#  Device requirement: devices with Frame Interleave HDR mode or OB_STRUCT_DEPTH_HDR_CONFIG property
#
#  Run:
#    python examples/advanced/10_hdr.py
# ******************************************************************************
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import cv2
import numpy as np
from utils import resize_to_fit

from pyorbbecsdk import HDRMergeFilter  # type: ignore
from pyorbbecsdk import (
    Config,
    Context,
    OBFrameAggregateOutputMode,
    OBHdrConfig,
    OBPermissionType,
    OBPropertyID,
    OBSensorType,
    Pipeline,
)

ESC_KEY = 27
PRINT_INTERVAL = 1  # seconds
MIN_DEPTH = 20  # 20mm
MAX_DEPTH = 10000  # 10000mm


def add_text_to_image(image, text, position):
    """
    Add text to an image at the specified position
    Args:
        image: Input image
        text: Text to add
        position: Tuple of (x, y) coordinates
    Returns:
        Image with text added
    """
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.8
    color = (255, 255, 255)  # White color
    thickness = 2

    # Add black background for better visibility
    (text_width, text_height), _ = cv2.getTextSize(text, font, font_scale, thickness)
    cv2.rectangle(
        image,
        (position[0], position[1] - text_height - 5),
        (position[0] + text_width, position[1] + 5),
        (0, 0, 0),
        -1,
    )

    return cv2.putText(image, text, position, font, font_scale, color, thickness)


def enhance_contrast(image, clip_limit=3.0, tile_grid_size=(8, 8)):
    """
    Enhance image contrast using CLAHE
    """
    if len(image.shape) == 3:
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
        l = clahe.apply(l)
        lab = cv2.merge((l, a, b))
        return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    else:
        clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
        return clahe.apply(image)


def main():
    # Check if device is connected
    ctx = Context()
    device_list = ctx.query_devices()
    if device_list.get_count() == 0:
        print("Device Not Found! Please connect an Orbbec camera and try again.")
        return

    pipeline = Pipeline()
    config = Config()

    try:
        # Enable depth stream
        profile_list = pipeline.get_stream_profile_list(OBSensorType.DEPTH_SENSOR)
        depth_profile = profile_list.get_default_video_stream_profile()
        config.enable_stream(depth_profile)

        # Enable IR streams
        left_profile_list = pipeline.get_stream_profile_list(OBSensorType.LEFT_IR_SENSOR)
        right_profile_list = pipeline.get_stream_profile_list(OBSensorType.RIGHT_IR_SENSOR)
        left_ir_profile = left_profile_list.get_default_video_stream_profile()
        right_ir_profile = right_profile_list.get_default_video_stream_profile()
        config.enable_stream(left_ir_profile)
        config.enable_stream(right_ir_profile)
        config.set_frame_aggregate_output_mode(OBFrameAggregateOutputMode.FULL_FRAME_REQUIRE)
    except Exception as e:
        print(e)
        return

    # Configure HDR BEFORE pipeline.start() to ensure alternating
    # exposure is active when streaming begins.
    device = pipeline.get_device()

    if device.isFrameInterleaveSupported():
        # Disable auto exposure first; auto exposure would override
        # the interleave exposure values and prevent HDR from working.
        try:
            device.set_bool_property(OBPropertyID.OB_PROP_DEPTH_AUTO_EXPOSURE_BOOL, False)
        except Exception:
            pass
        device.loadFrameInterleave("Depth from HDR")
        device.set_bool_property(OBPropertyID.OB_PROP_FRAME_INTERLEAVE_ENABLE_BOOL, True)
    elif device.is_property_supported(OBPropertyID.OB_STRUCT_DEPTH_HDR_CONFIG, OBPermissionType.PERMISSION_READ_WRITE):
        hdr_config = OBHdrConfig()
        hdr_config.enable = True
        hdr_config.exposure_1 = 7500
        hdr_config.gain_1 = 24
        hdr_config.exposure_2 = 100
        hdr_config.gain_2 = 16
        device.set_hdr_config(hdr_config)
    else:
        print("Current default device does not support HDR merge")
        return

    hdr_filter = HDRMergeFilter()

    try:
        pipeline.start(config)
    except Exception as e:
        print(e)
        return

    # Create window for visualization
    cv2.namedWindow("HDR Merge Viewer", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("HDR Merge Viewer", 1280, 960)  # Adjusted for 2x2 layout

    while True:
        try:
            frames = pipeline.wait_for_frames(1000)
            if not frames:
                print("No frames received")
                continue

            # Get all frames
            depth_frame = frames.get_depth_frame()
            left_ir_frame = frames.get_left_ir_frame()
            right_ir_frame = frames.get_right_ir_frame()

            if not all([depth_frame, left_ir_frame, right_ir_frame]):
                print("Not All frames received")
                continue

            # Process with HDR merge
            merged_frame = hdr_filter.process(frames)
            if not merged_frame:
                continue

            merged_depth_frame = merged_frame.get_depth_frame()
            # Convert frames to displayable images
            depth_image = create_depth_image(depth_frame)
            merged_depth_image = create_depth_image(merged_depth_frame)
            ir_left_image = create_ir_image(left_ir_frame)
            ir_right_image = create_ir_image(right_ir_frame)

            # Enhance contrast for all images
            depth_image = enhance_contrast(depth_image, clip_limit=4.0)
            ir_left_image = enhance_contrast(ir_left_image, clip_limit=4.0)
            ir_right_image = enhance_contrast(ir_right_image, clip_limit=4.0)
            merged_depth_image = enhance_contrast(merged_depth_image, clip_limit=4.0)

            # Fit all images into a common cell (depth's resolution) for the
            # 2x2 grid, preserving each one's aspect ratio with black borders.
            h, w = depth_image.shape[:2]
            ir_left_image = resize_to_fit(ir_left_image, w, h)
            ir_right_image = resize_to_fit(ir_right_image, w, h)
            merged_depth_image = resize_to_fit(merged_depth_image, w, h)

            # Add text annotations to images
            ir_left_image = add_text_to_image(ir_left_image, "Left IR (HDR)", (10, 30))
            ir_right_image = add_text_to_image(ir_right_image, "Right IR (HDR)", (10, 30))
            depth_image = add_text_to_image(depth_image, "Original Depth (HDR)", (10, 30))
            merged_depth_image = add_text_to_image(merged_depth_image, "HDR Merged Depth", (10, 30))

            # Create 2x2 layout
            top_row = np.hstack((ir_left_image, ir_right_image))
            bottom_row = np.hstack((depth_image, merged_depth_image))
            display_image = np.vstack((top_row, bottom_row))

            cv2.imshow("HDR Merge Viewer", display_image)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q") or key == ESC_KEY:
                break

        except KeyboardInterrupt:
            break

    cv2.destroyAllWindows()
    pipeline.stop()
    if device.isFrameInterleaveSupported():
        device.set_bool_property(OBPropertyID.OB_PROP_FRAME_INTERLEAVE_ENABLE_BOOL, False)
    else:
        hdr_config = OBHdrConfig()
        hdr_config.enable = False
        device.set_hdr_config(hdr_config)


def create_depth_image(depth_frame):
    """Convert depth frame to colorized image"""
    width = depth_frame.get_width()
    height = depth_frame.get_height()
    scale = depth_frame.get_depth_scale()

    depth_data = np.frombuffer(depth_frame.get_data(), dtype=np.uint16)
    depth_data = depth_data.reshape((height, width))
    depth_data = depth_data.astype(np.float32) * scale
    depth_data = np.where((depth_data > MIN_DEPTH) & (depth_data < MAX_DEPTH), depth_data, 0)
    depth_data = depth_data.astype(np.uint16)

    depth_image = cv2.normalize(depth_data, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    return cv2.applyColorMap(depth_image, cv2.COLORMAP_JET)


def create_ir_image(ir_frame):
    """Convert IR frame to displayable image with enhanced contrast"""
    width = ir_frame.get_width()
    height = ir_frame.get_height()

    ir_data = np.frombuffer(ir_frame.get_data(), dtype=np.uint8)
    ir_data = ir_data.reshape((height, width))

    ir_image = cv2.normalize(ir_data, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    return cv2.cvtColor(ir_image, cv2.COLOR_GRAY2BGR)


if __name__ == "__main__":
    main()
