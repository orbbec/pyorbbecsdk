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

import cv2
import numpy as np

from pyorbbecsdk import *
from utils import frame_to_bgr_image

ESC_KEY = 27

# 回放状态回调函数
def playback_state_callback(state):
    # 播放开始
    if state == OBMediaState.OB_MEDIA_BEGIN:
        print("Bag player stopped")
    # 播放结束
    elif state == OBMediaState.OB_MEDIA_END:
        print("Bag player playing")
    # 播放暂停
    elif state == OBMediaState.OB_MEDIA_PAUSED:
        print("Bag player paused")

# 获取彩色图像的函数
def get_color_frame(frames):
    color_frame = frames.get_color_frame()
    if color_frame is None:
        return None
    color_image = frame_to_bgr_image(color_frame)
    if color_image is None:
        print("failed to convert frame to image")
        return None
    return color_image


def main():
    # 加载 .bag 文件
    pipeline = Pipeline("./test.bag")
    playback = pipeline.get_playback()
    # 注册播放状态回调
    playback.set_playback_state_callback(playback_state_callback)

    # 打印设备与相机参数
    device_info = playback.get_device_info()
    print("Device info: ", device_info)
    camera_param = pipeline.get_camera_param()
    print("Camera param: ", camera_param)

    # 启动管道并播放
    pipeline.start()
    try:
        while True:
            # 等待一帧数据到来（最大延迟 100 毫秒）
            frames = pipeline.wait_for_frames(100)
            if frames is None:
                continue

            # 提取深度帧数据并转换
            depth_frame = frames.get_depth_frame()
            if depth_frame is None:
                continue
            images = []
            width = depth_frame.get_width()
            height = depth_frame.get_height()
            scale = depth_frame.get_depth_scale()

            depth_data = np.frombuffer(depth_frame.get_data(), dtype=np.uint16)
            depth_data = depth_data.reshape((height, width))
            depth_data = depth_data.astype(np.float32) * scale
            depth_image = cv2.normalize(depth_data, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
            depth_image = cv2.applyColorMap(depth_image, cv2.COLORMAP_JET)

            # 获取彩色图像
            color_image = get_color_frame(frames)
            # if you want to add IR frame, it's the same as color
            if depth_image is not None:
                images.append(depth_image)
            if color_image is not None:
                images.append(color_image)
            if len(images) > 0:
                images_to_show = []
                for img in images:
                    # 图像统一缩放为 640x480
                    img = cv2.resize(img, (640, 480))
                    images_to_show.append(img)
                # 使用 np.hstack 横向拼接图像
                cv2.imshow("playbackViewer", np.hstack(images_to_show))
            key = cv2.waitKey(1)
            if key == ord('q') or key == ESC_KEY:
                break
    except KeyboardInterrupt:
        # 退出与清理
        if pipeline:
            pipeline.stop()
        sys.exit(0)


if __name__ == "__main__":
    main()
