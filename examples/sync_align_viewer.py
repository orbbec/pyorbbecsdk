from pyorbbecsdk import *
import cv2
import numpy as np
from utils import frame_to_rgb_frame

ESC_KEY = 27


def main():
    pipeline = Pipeline()
    config = Config()
    try:
        profile_list = pipeline.get_stream_profile_list(OBSensorType.COLOR_SENSOR)
        try:
            color_profile: VideoStreamProfile = profile_list.get_video_stream_profile(1280, 0, OBFormat.RGB, 30)
        except OBError as e:
            print(e)
            color_profile = profile_list.get_default_video_stream_profile()
        config.enable_stream(color_profile)
        profile_list = pipeline.get_stream_profile_list(OBSensorType.DEPTH_SENSOR)
        assert profile_list is not None
        depth_profile = profile_list.get_default_video_stream_profile()
        assert depth_profile is not None
        config.enable_stream(depth_profile)
    except Exception as e:
        print(e)
        return
    config.set_align_mode(OBAlignMode.HW_MODE)
    try:
        pipeline.start(config)
    except Exception as e:
        print(e)
        return
    while True:
        try:
            frames: FrameSet = pipeline.wait_for_frames(100)
            if frames is None:
                continue
            color_frame = frames.get_color_frame()
            if color_frame is None:
                continue
            # covert to RGB format
            color_frame = frame_to_rgb_frame(color_frame)
            if color_frame is None:
                continue
            color_image = np.asanyarray(color_frame.get_data())
            depth_frame = frames.get_depth_frame()
            if depth_frame is None:
                continue
            depth_image = np.asanyarray(depth_frame.get_data())
            cv2.normalize(depth_image, depth_image, 0, 255, cv2.NORM_MINMAX)
            depth_image = depth_image.astype(np.uint8)
            depth_image = cv2.applyColorMap(depth_image, cv2.COLORMAP_JET)
            # overlay color image on depth image
            depth_image = cv2.addWeighted(color_image, 0.5, depth_image, 0.5, 0)
            cv2.imshow("SyncAlignViewer ", depth_image)
            key = cv2.waitKey(1)
            if key == ord('q') or key == ESC_KEY:
                break
        except KeyboardInterrupt:
            break
