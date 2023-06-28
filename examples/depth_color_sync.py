from pyorbbecsdk import *
import cv2
import numpy as np
from utils import frame_to_bgr_image

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
        print("color profile : {}x{}@{}_{}".format(color_profile.get_width(), color_profile.get_height(),
                                                   color_profile.get_fps(), color_profile.get_format()))
        print("depth profile : {}x{}@{}_{}".format(depth_profile.get_width(), depth_profile.get_height(),
                                                   depth_profile.get_fps(), depth_profile.get_format()))
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
            color_image = frame_to_bgr_image(color_frame)
            if color_image is None:
                print("failed to convert frame to image")
                continue
            depth_frame = frames.get_depth_frame()
            if depth_frame is None:
                continue
            height = depth_frame.get_height()
            width = depth_frame.get_width()
            scale = depth_frame.get_depth_scale()
            depth_data = np.asanyarray(depth_frame.get_data())
            depth_data = np.resize(depth_data, (height, width, 2))
            depth_data = depth_data * scale
            channel0 = depth_data[:, :, 0]
            channel1 = depth_data[:, :, 1]
            channel0_norm = cv2.normalize(channel0, None, 0, 255, cv2.NORM_MINMAX)
            channel1_norm = cv2.normalize(channel1, None, 0, 255, cv2.NORM_MINMAX)
            depth_image = np.zeros((height, width, 3), dtype=np.uint8)
            depth_image[:, :, 0] = channel0_norm
            depth_image[:, :, 1] = channel1_norm
            depth_image = cv2.applyColorMap(depth_image, cv2.COLORMAP_JET)
            # overlay color image on depth image
            depth_image = cv2.addWeighted(color_image, 0.5, depth_image, 0.5, 0)
            cv2.imshow("SyncAlignViewer ", depth_image)
            key = cv2.waitKey(1)
            if key == ord('q') or key == ESC_KEY:
                break
        except KeyboardInterrupt:
            break
    pipeline.stop()


if __name__ == "__main__":
    main()
