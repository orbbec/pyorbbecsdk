# ******************************************************************************
#  Copyright (c) 2023 Orbbec 3D Technology, Inc
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
# ******************************************************************************

import json
import os
import time
from queue import Queue
from threading import Lock
from typing import List

import cv2
import numpy as np
import open3d as o3d

from pyorbbecsdk import *
from utils import frame_to_bgr_image

frames_queue_lock = Lock()

# Configuration settings
MAX_DEVICES = 2
MAX_QUEUE_SIZE = 5
ESC_KEY = 27
save_points_dir = os.path.join(os.getcwd(), "point_clouds")
save_depth_image_dir = os.path.join(os.getcwd(), "depth_images")
save_color_image_dir = os.path.join(os.getcwd(), "color_images")

frames_queue: List[Queue] = [Queue() for _ in range(MAX_DEVICES)]
stop_processing = False
curr_device_cnt = 0

# Load config file for multiple devices
config_file_path = os.path.join(os.path.dirname(__file__), "../config/multi_device_sync_config.json")
multi_device_sync_config = {}


def convert_to_o3d_point_cloud(points, colors=None):
    """
    Converts numpy arrays of points and colors (if provided) into an Open3D point cloud object.
    """
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    if colors is not None:
        pcd.colors = o3d.utility.Vector3dVector(colors / 255.0)  # Assuming colors are in [0, 255]
    return pcd


def read_config(config_file: str):
    global multi_device_sync_config
    with open(config_file, "r") as f:
        config = json.load(f)
    for device in config["devices"]:
        multi_device_sync_config[device["serial_number"]] = device
        print(f"Device {device['serial_number']}: {device['config']['mode']}")


def sync_mode_from_str(sync_mode_str: str) -> OBMultiDeviceSyncMode:
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


# Frame processing and saving
def process_frames(pipelines):
    global frames_queue
    global stop_processing
    global curr_device_cnt, save_points_dir, save_depth_image_dir, save_color_image_dir
    while not stop_processing:
        now = time.time()
        for device_index in range(curr_device_cnt):
            with frames_queue_lock:
                frames = frames_queue[device_index].get() if not frames_queue[device_index].empty() else None
            if frames is None:
                continue
            color_frame = frames.get_color_frame() if frames else None
            depth_frame = frames.get_depth_frame() if frames else None
            pipeline = pipelines[device_index]
            print(f"Device {device_index} frames")

            if color_frame:
                color_image = frame_to_bgr_image(color_frame)
                color_filename = os.path.join(save_color_image_dir,
                                              f"color_{device_index}_{color_frame.get_timestamp()}.png")
                cv2.imwrite(color_filename, color_image)

            if depth_frame:
                timestamp = depth_frame.get_timestamp()
                width = depth_frame.get_width()
                height = depth_frame.get_height()
                timestamp = depth_frame.get_timestamp()
                scale = depth_frame.get_depth_scale()
                data = np.frombuffer(depth_frame.get_data(), dtype=np.uint16)
                data = data.reshape((height, width))
                data = data.astype(np.float32) * scale
                data = data.astype(np.uint16)
                if not os.path.exists(save_depth_image_dir):
                    os.mkdir(save_depth_image_dir)
                raw_filename = save_depth_image_dir + "/depth_{}x{}_device_{}_{}.raw".format(width, height,
                                                                                             device_index, timestamp)
                data.tofile(raw_filename)
                camera_param = pipeline.get_camera_param()
                points = frames.get_point_cloud(camera_param)
                if len(points) == 0:
                    print("no depth points")
                    continue
                points_array = np.array([tuple(point) for point in points],
                                        dtype=[('x', 'f4'), ('y', 'f4'), ('z', 'f4')])
                if not os.path.exists(save_points_dir):
                    os.mkdir(save_points_dir)
                points_filename = os.path.join(save_points_dir, f"points_device_{device_index}_{timestamp}.ply")
                pcd = convert_to_o3d_point_cloud(np.array(points))
                o3d.io.write_point_cloud(points_filename, pcd)
        print(f"Processing time: {time.time() - now:.3f}s")


def on_new_frame_callback(frames: FrameSet, index: int):
    global frames_queue
    global MAX_QUEUE_SIZE
    assert index < MAX_DEVICES
    with frames_queue_lock:
        if frames_queue[index].qsize() >= MAX_QUEUE_SIZE:
            frames_queue[index].get()
        frames_queue[index].put(frames)


def start_streams(pipelines: List[Pipeline], configs: List[Config]):
    index = 0
    for pipeline, config in zip(pipelines, configs):
        print(f"Starting device {index}")
        pipeline.start(
            config,
            lambda frame_set, curr_index=index: on_new_frame_callback(
                frame_set, curr_index
            ),
        )
        pipeline.enable_frame_sync()
        index += 1


def stop_streams(pipelines: List[Pipeline]):
    index = 0
    for pipeline in pipelines:
        print(f"Stopping device {index}")
        pipeline.stop()
        index += 1


# Main function for setup and teardown
def main():
    global curr_device_cnt
    read_config(config_file_path)
    ctx = Context()
    device_list = ctx.query_devices()
    if device_list.get_count() == 0:
        print("No device connected")
        return
    pipelines = []
    configs = []
    curr_device_cnt = device_list.get_count()
    for i in range(min(device_list.get_count(), MAX_DEVICES)):
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
        device.set_multi_device_sync_config(sync_config)
        print(f"Device {serial_number} sync config: {sync_config}")

        profile_list = pipeline.get_stream_profile_list(OBSensorType.COLOR_SENSOR)
        color_profile = profile_list.get_default_video_stream_profile()
        config.enable_stream(color_profile)
        print(f"Device {serial_number} color profile: {color_profile}")

        profile_list = pipeline.get_stream_profile_list(OBSensorType.DEPTH_SENSOR)
        depth_profile = profile_list.get_default_video_stream_profile()
        print(f"Device {serial_number} depth profile: {depth_profile}")
        config.enable_stream(depth_profile)
        pipelines.append(pipeline)
        configs.append(config)
    start_streams(pipelines, configs)
    global stop_processing
    try:
        process_frames(pipelines)
    except KeyboardInterrupt:
        print("Interrupted by user")
        stop_processing = True
    finally:
        print("===============Stopping pipelines====")
        stop_streams(pipelines)


if __name__ == "__main__":
    main()
