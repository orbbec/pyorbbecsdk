from pyorbbecsdk import *
import time
import cv2
import numpy as np
from threading import Lock
from typing import List, Optional
from queue import Queue

frame_lock = Lock()
stop_rendering = False

MAX_DEVICES = 2
WINDOW_SIZE = (640, 480)

color_frames_queue: List[Queue] = [Queue() for _ in range(MAX_DEVICES)]
depth_frames_queue: List[Queue] = [Queue() for _ in range(MAX_DEVICES)]


def on_new_frame_callback(frame: FrameSet, index: int):
    assert index < MAX_DEVICES
    color_frame = frame.get_color_frame()
    depth_frame = frame.get_depth_frame()
    if color_frame is not None:
        color_frames_queue[index].put(color_frame)
    if depth_frame is not None:
        depth_frames_queue[index].put(depth_frame)


def rendering_thread():
    global stop_rendering
    while stop_rendering is False:
        for i in range(MAX_DEVICES):
            color_frame = color_frames_queue[i].get_nowait()
            depth_frame = depth_frames_queue[i].get_nowait()
            if color_frame is None or depth_frame is None:
                continue
            color_image = np.asanyarray(color_frame.get_data())
            depth_image = np.asanyarray(depth_frame.get_data())
            cv2.normalize(depth_image, depth_image, 0, 255, cv2.NORM_MINMAX)
            depth_image = depth_image.astype(np.uint8)
            depth_image = cv2.applyColorMap(depth_image, cv2.COLORMAP_JET)
            # resize to fit the window
            color_image = cv2.resize(color_image, WINDOW_SIZE)
            depth_image = cv2.resize(depth_image, WINDOW_SIZE)
            image_stack = np.hstack((color_image, depth_image))
            window_name = "Device " + str(i)
            cv2.imshow(window_name, image_stack)


def start_streams(pipelines: List[Pipeline], configs: List[Config]):
    index = 0
    for pipeline, config in zip(pipelines, configs):
        pipeline.start(config, lambda frame_set: on_new_frame_callback(frame_set, index))
        index += 1


def stop_streams(pipelines: List[Pipeline]):
    for pipeline in pipelines:
        pipeline.stop()


def main():
    ctx = Context()
    device_list = ctx.query_devices()
    if device_list.get_count() == 0:
        print("No device connected")
        return
    if device_list.get_count() > MAX_DEVICES:
        print("Too many devices connected")
        return
    pipelines: List[Pipeline] = []
    configs: List[Config] = []
    for i in range(device_list.get_count()):
        device = device_list.get_device_by_index(i)
        pipeline = Pipeline(device)
        config = Config()
        profile_list = pipeline.get_stream_profile_list(OBSensorType.COLOR_SENSOR)
        try:
            color_profile: VideoStreamProfile = profile_list.get_video_stream_profile(1280, 0, OBFormat.RGB, 30)
            config.enable_stream(color_profile)
        except OBError as e:
            print(e)
            color_profile = profile_list.get_default_video_stream_profile()
            config.enable_stream(color_profile)
        profile_list = pipeline.get_stream_profile_list(OBSensorType.DEPTH_SENSOR)
        try:
            depth_profile: VideoStreamProfile = profile_list.get_video_stream_profile(640, 0, OBFormat.Y16, 30)
            config.enable_stream(depth_profile)
        except OBError as e:
            print(e)
            depth_profile = profile_list.get_default_video_stream_profile()
            config.enable_stream(depth_profile)
        pipelines.append(pipeline)
        configs.append(config)

    start_streams(pipelines, configs)
    rendering_thread()
    stop_streams(pipelines)


if __name__ == "__main__":
    main()
