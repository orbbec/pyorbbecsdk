from pyorbbecsdk import *
import cv2
import numpy as np
from utils import frame_to_bgr_image
import os


def save_depth_frame(frame: DepthFrame, index):
    if frame is None:
        return
    width = frame.get_width()
    height = frame.get_height()
    timestamp = frame.get_timestamp()
    scale = frame.get_value_scale()
    data = np.asanyarray(frame.get_data())
    data = data * scale
    save_image_dir = os.path.join(os.getcwd(), "depth_images")
    if not os.path.exists(save_image_dir):
        os.mkdir(save_image_dir)
    png_filename = save_image_dir + "/depth_{}x{}_{}_{}.png".format(width, height, index, timestamp)
    raw_filename = save_image_dir + "/depth_{}x{}_{}_{}.raw".format(width, height, index, timestamp)
    if frame.get_format() == OBFormat.Y8:
        data = data * 16
    data = np.resize(data, (height, width, 2))
    depth_image = np.zeros((height, width, 3), dtype=np.uint8)
    depth_image[:, :, 0] = data[:, :, 0]
    depth_image[:, :, 1] = data[:, :, 1]
    depth_image.astype(np.uint16)
    cv2.imwrite(png_filename, depth_image)
    depth_image.tofile(raw_filename)


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


def main():
    pipeline = Pipeline()
    config = Config()
    saved_color_cnt: int = 0
    saved_depth_cnt: int = 0
    try:
        profile_list = pipeline.get_stream_profile_list(OBSensorType.COLOR_SENSOR)
        if profile_list is not None:
            color_profile: VideoStreamProfile = profile_list.get_default_video_stream_profile()
            config.enable_stream(color_profile)
    except OBError as e:
        print(e)
    depth_profile_list = pipeline.get_stream_profile_list(OBSensorType.DEPTH_SENSOR)
    if depth_profile_list is not None:
        depth_profile = depth_profile_list.get_default_video_stream_profile()
        config.enable_stream(depth_profile)
    pipeline.start(config)
    frame_cnt = 0
    while True:
        try:
            frames = pipeline.wait_for_frames(100)
            if frames is None:
                continue
            if frame_cnt > 5:
                break
            frame_cnt += 1
            color_frame = frames.get_color_frame()
            if color_frame is not None:
                save_color_frame(color_frame, saved_color_cnt)
                saved_color_cnt += 1
            depth_frame = frames.get_depth_frame()
            if depth_frame is not None:
                save_depth_frame(depth_frame, saved_depth_cnt)
                saved_depth_cnt += 1
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    main()
