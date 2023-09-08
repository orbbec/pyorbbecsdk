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
import sys

from pyorbbecsdk import *
import time
import cv2
import numpy as np

from queue import Queue

depth_frames_queue = Queue()
MAX_QUEUE_SIZE = 5
ESC_KEY = 27
stop_rendering = False


def playback_state_callback(state):
    if state == OBMediaState.OB_MEDIA_BEGIN:
        print("Bag player stopped")
    elif state == OBMediaState.OB_MEDIA_END:
        print("Bag player playing")
    elif state == OBMediaState.OB_MEDIA_PAUSED:
        print("Bag player paused")


def frame_playback_callback(frame):
    global depth_frames_queue
    depth_frame = frame.as_depth_frame()
    if depth_frame is None:
        return
    if depth_frames_queue.qsize() >= MAX_QUEUE_SIZE:
        depth_frames_queue.get()
    depth_frames_queue.put(depth_frame)


def rendering_frames():
    global depth_frames_queue, stop_rendering
    while not stop_rendering:
        depth_frame = None
        if not depth_frames_queue.empty():
            depth_frame = depth_frames_queue.get()
        if depth_frame is None:
            continue
        width = depth_frame.get_width()
        height = depth_frame.get_height()
        scale = depth_frame.get_depth_scale()
        depth_data = np.frombuffer(depth_frame.get_data(), dtype=np.uint16)
        depth_data = depth_data.reshape((height, width))
        depth_data = depth_data.astype(np.float32) * scale
        depth_image = cv2.normalize(depth_data, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        depth_image = cv2.applyColorMap(depth_image, cv2.COLORMAP_JET)
        cv2.imshow("Depth Viewer", depth_image)
        key = cv2.waitKey(1)
        if key == ord('q') or key == ESC_KEY:
            break


def main():
    pipeline = Pipeline("./test.bag")
    playback = pipeline.get_playback()
    playback.set_playback_state_callback(playback_state_callback)
    device_info = playback.get_device_info()
    print("Device info: ", device_info)
    camera_param = pipeline.get_camera_param()
    print("Camera param: ", camera_param)
    global stop_rendering
    playback.start(frame_playback_callback)
    try:
        rendering_frames()
    except KeyboardInterrupt:
        stop_rendering = True
        sys.exit(0)


if __name__ == "__main__":
    main()
