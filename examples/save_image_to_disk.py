from pyorbbecsdk import *
import cv2
import numpy as np
from utils import frame_to_rgb_frame


def save_depth_frame(frame: DepthFrame, index):
    width = frame.get_width()
    height = frame.get_height()
    timestamp = frame.get_timestamp()
    data = frame.get_data()
    filename = "depth_{}x{}_{}_{}.png".format(width, height, index, timestamp)
    image = np.asanyarray(data)
    cv2.imwrite(filename, image)


def save_color_frame(frame: ColorFrame, index):
    width = frame.get_width()
    height = frame.get_height()
    timestamp = frame.get_timestamp()
    data = frame.get_data()
    filename = "color_{}x{}_{}_{}.png".format(width, height, index, timestamp)
    image = np.asanyarray(data)
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
                color_frame = frame_to_rgb_frame(color_frame)
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
