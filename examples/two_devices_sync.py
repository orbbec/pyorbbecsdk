# ******************************************************************************
#  Copyright (c) 2023 Orbbec 3D Technology, Inc
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http:# www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
# ******************************************************************************
import json
import os
from queue import Queue
from typing import List

import cv2
import numpy as np

from pyorbbecsdk import *
from utils import frame_to_bgr_image

MAX_DEVICES = 2
curr_device_cnt = 0

MAX_QUEUE_SIZE = 5
ESC_KEY = 27

color_frames_queue: List[Queue] = [Queue() for _ in range(MAX_DEVICES)]
depth_frames_queue: List[Queue] = [Queue() for _ in range(MAX_DEVICES)]
has_color_sensor: List[bool] = [False for _ in range(MAX_DEVICES)]
stop_rendering = False
multi_device_sync_config = {}
# config_file_path current file path
config_file_path = os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    "../config/multi_device_sync_config.json",
)


def sync_mode_from_str(sync_mode_str: str) -> OBMultiDeviceSyncMode:
    # to lower case
    sync_mode_str = sync_mode_str.upper()
    if sync_mode_str == "FREE_RUN":
        return OBMultiDeviceSyncMode.FREE_RUN
    elif sync_mode_str == "STANDALONE":
        return OBMultiDeviceSyncMode.STANDALONE
    elif sync_mode_str == "PRIMARY":
        return OBMultiDeviceSyncMode.PRIMARY
    elif sync_mode_str == "SECONDARY":
        return OBMultiDeviceSyncMode.SECONDARY
    elif sync_mode_str == "SECONDARY_SYNCED":
        return OBMultiDeviceSyncMode.SECONDARY_SYNCED
    elif sync_mode_str == "SOFTWARE_TRIGGERING":
        return OBMultiDeviceSyncMode.SOFTWARE_TRIGGERING
    elif sync_mode_str == "HARDWARE_TRIGGERING":
        return OBMultiDeviceSyncMode.HARDWARE_TRIGGERING
    else:
        raise ValueError(f"Invalid sync mode: {sync_mode_str}")


def on_new_frame_callback(frames: FrameSet, index: int):
    global color_frames_queue, depth_frames_queue
    global MAX_QUEUE_SIZE
    assert index < MAX_DEVICES
    color_frame = frames.get_color_frame()
    depth_frame = frames.get_depth_frame()
    if color_frame is not None:
        if color_frames_queue[index].qsize() >= MAX_QUEUE_SIZE:
            color_frames_queue[index].get()
        color_frames_queue[index].put(color_frame)
    if depth_frame is not None:
        if depth_frames_queue[index].qsize() >= MAX_QUEUE_SIZE:
            depth_frames_queue[index].get()
        depth_frames_queue[index].put(depth_frame)


def rendering_frames():
    global color_frames_queue, depth_frames_queue
    global curr_device_cnt
    global stop_rendering
    while not stop_rendering:
        for i in range(curr_device_cnt):
            color_frame = None
            depth_frame = None
            if not color_frames_queue[i].empty():
                color_frame = color_frames_queue[i].get()
            if not depth_frames_queue[i].empty():
                depth_frame = depth_frames_queue[i].get()
            if color_frame is None and depth_frame is None:
                continue
            color_image = None
            depth_image = None
            color_width, color_height = 0, 0
            if color_frame is not None:
                color_width, color_height = (
                    color_frame.get_width(),
                    color_frame.get_height(),
                )
                color_image = frame_to_bgr_image(color_frame)
            if depth_frame is not None:
                width = depth_frame.get_width()
                height = depth_frame.get_height()
                scale = depth_frame.get_depth_scale()

                depth_data = np.frombuffer(depth_frame.get_data(), dtype=np.uint16)
                depth_data = depth_data.reshape((height, width))

                depth_data = depth_data.astype(np.float32) * scale

                depth_image = cv2.normalize(
                    depth_data, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U
                )
                depth_image = cv2.applyColorMap(depth_image, cv2.COLORMAP_JET)

            if color_image is not None and depth_image is not None:
                window_size = (color_width // 2, color_height // 2)
                color_image = cv2.resize(color_image, window_size)
                depth_image = cv2.resize(depth_image, window_size)
                image = np.hstack((color_image, depth_image))
            elif depth_image is not None and not has_color_sensor[i]:
                image = depth_image
            else:
                continue
            cv2.imshow("Device {}".format(i), image)
            key = cv2.waitKey(1)
            if key == ord("q") or key == ESC_KEY:
                return


def start_streams(pipelines: List[Pipeline], configs: List[Config]):
    index = 0
    for pipeline, config in zip(pipelines, configs):
        pipeline.start(
            config,
            lambda frame_set, curr_index=index: on_new_frame_callback(
                frame_set, curr_index
            ),
        )
        index += 1


def stop_streams(pipelines: List[Pipeline]):
    for pipeline in pipelines:
        pipeline.stop()


def read_config(config_file: str):
    global multi_device_sync_config
    with open(config_file, "r") as f:
        config = json.load(f)
    for device in config["devices"]:
        multi_device_sync_config[device["serial_number"]] = device
        print(f"Device {device['serial_number']}: {device['config']['mode']}")


def main():
    global config_file_path
    read_config(config_file_path)
    ctx = Context()
    device_list = ctx.query_devices()
    global curr_device_cnt
    curr_device_cnt = device_list.get_count()
    if curr_device_cnt == 0:
        print("No device connected")
        return
    if curr_device_cnt > MAX_DEVICES:
        print("Too many devices connected")
        return
    pipelines: List[Pipeline] = []
    configs: List[Config] = []
    global has_color_sensor
    for i in range(device_list.get_count()):
        device = device_list.get_device_by_index(i)
        pipeline = Pipeline(device)
        config = Config()
        serial_number = device.get_device_info().get_serial_number()
        sync_config_json = multi_device_sync_config[serial_number]
        sync_config = device.get_multi_device_sync_config()
        sync_config.mode = sync_mode_from_str(sync_config_json["config"]["mode"])
        sync_config.color_delay_us = sync_config_json["config"]["color_delay_us"]
        sync_config.depth_delay_us = sync_config_json["config"]["depth_delay_us"]
        sync_config.trigger_out_enable = sync_config_json["config"]["trigger_out_enable"]
        sync_config.trigger_out_delay_us = sync_config_json["config"]["trigger_out_delay_us"]
        sync_config.frames_per_trigger = sync_config_json["config"]["frames_per_trigger"]
        print(f"Device {serial_number} sync config: {sync_config}")
        device.set_multi_device_sync_config(sync_config)
        try:
            profile_list = pipeline.get_stream_profile_list(OBSensorType.COLOR_SENSOR)
            color_profile: VideoStreamProfile = (
                profile_list.get_default_video_stream_profile()
            )
            config.enable_stream(color_profile)
            has_color_sensor[i] = True
        except OBError as e:
            print(e)
            has_color_sensor[i] = False
        profile_list = pipeline.get_stream_profile_list(OBSensorType.DEPTH_SENSOR)
        depth_profile = profile_list.get_default_video_stream_profile()
        config.enable_stream(depth_profile)
        config.enable_stream(depth_profile)
        pipelines.append(pipeline)
        configs.append(config)
    global stop_rendering
    start_streams(pipelines, configs)
    try:
        rendering_frames()
        stop_streams(pipelines)
    except KeyboardInterrupt:
        stop_rendering = True
        stop_streams(pipelines)


if __name__ == "__main__":
    main()
