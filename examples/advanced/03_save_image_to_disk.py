# ******************************************************************************
#  pyorbbecsdk Advanced Example 03 — Save Frames to Disk
#
#  What you will learn:
#    1. How to capture a single color frame and save it as a PNG file
#    2. How to capture a depth frame and save it as a 16-bit PNG with the depth scale
#    3. How to limit capture to a fixed number of frames and stop automatically
#
#  Device requirement: All
#
#  Run:
#    python examples/advanced/03_save_image_to_disk.py
# ******************************************************************************
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import os

import cv2
import numpy as np
from utils import frame_to_bgr_image

from pyorbbecsdk import Context  # type: ignore
from pyorbbecsdk import (
    ColorFrame,
    Config,
    DepthFrame,
    OBError,
    OBFormat,
    OBFrameAggregateOutputMode,
    OBSensorType,
    Pipeline,
    VideoStreamProfile,
)


def save_depth_frame(frame: DepthFrame, index):
    if frame is None:
        return
    width = frame.get_width()
    height = frame.get_height()
    timestamp = frame.get_timestamp()
    scale = frame.get_depth_scale()
    depth_format = frame.get_format()
    if depth_format != OBFormat.Y16:
        print("depth format is not Y16")
        return
    data = np.frombuffer(frame.get_data(), dtype=np.uint16)
    data = data.reshape((height, width))
    data = data.astype(np.float32) * scale
    data = data.astype(np.uint16)
    save_image_dir = os.path.join(os.getcwd(), "depth_images")
    if not os.path.exists(save_image_dir):
        os.mkdir(save_image_dir)
    filename = save_image_dir + "/depth_{}x{}_{}_{}.png".format(width, height, index, timestamp)
    params = [cv2.IMWRITE_PNG_COMPRESSION, 0]
    cv2.imwrite(filename, data, params)
    print(f"Depth saved: {filename}")


def save_color_frame(frame: ColorFrame, index):
    if frame is None:
        return
    width = frame.get_width()
    height = frame.get_height()
    timestamp = frame.get_timestamp()
    save_image_dir = os.path.join(os.getcwd(), "color_images")
    if not os.path.exists(save_image_dir):
        os.mkdir(save_image_dir)
    filename = save_image_dir + "/color_{}x{}_{}_{}.png".format(width, height, index, timestamp)
    image = frame_to_bgr_image(frame)
    if image is None:
        print("failed to convert frame to image")
        return
    cv2.imwrite(filename, image)
    print(f"Color saved: {filename}")


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
        profile_list = pipeline.get_stream_profile_list(OBSensorType.COLOR_SENSOR)
        if profile_list is not None:
            color_profile: VideoStreamProfile = profile_list.get_default_video_stream_profile()
            config.enable_stream(color_profile)
        depth_profile_list = pipeline.get_stream_profile_list(OBSensorType.DEPTH_SENSOR)
        if depth_profile_list is not None:
            depth_profile = depth_profile_list.get_default_video_stream_profile()
            config.enable_stream(depth_profile)
        config.set_frame_aggregate_output_mode(OBFrameAggregateOutputMode.FULL_FRAME_REQUIRE)
    except OBError as e:
        print(f"Error: {e}")
        print("Please connect an Orbbec camera and try again.")
        return

    try:
        pipeline.start(config)
    except OBError as e:
        print(f"Error: {e}")
        print("Please connect an Orbbec camera and try again.")
        return

    print("Waiting for sensor to stabilize...")
    for _ in range(15):
        pipeline.wait_for_frames(1000)

    frame_index = 0
    try:
        while True:
            frames = pipeline.wait_for_frames(1000)
            if frames is None:
                continue
            frame_index += 1
            if frame_index >= 5:
                print("The demo is over!")
                break

            color_frame = frames.get_color_frame()
            depth_frame = frames.get_depth_frame()

            if color_frame:
                save_color_frame(color_frame, frame_index)
            if depth_frame:
                save_depth_frame(depth_frame, frame_index)
    except KeyboardInterrupt:
        pass
    except OBError as e:
        print(e)
    finally:
        pipeline.stop()
        print("Pipeline stopped.")


if __name__ == "__main__":
    main()
