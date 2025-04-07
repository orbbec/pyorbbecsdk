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

# OpenCV，用于图像显示
import cv2

# 3D 相机交互
from pyorbbecsdk import Config
from pyorbbecsdk import OBError
from pyorbbecsdk import OBSensorType, OBFormat
from pyorbbecsdk import Pipeline, FrameSet
from pyorbbecsdk import VideoStreamProfile

# 工具函数
from utils import frame_to_bgr_image

ESC_KEY = 27


def main():
    # 创建相机配置对象
    config = Config()
    # 创建管道对象，用于连接传感器流
    pipeline = Pipeline()
    try:
        # 获取彩色传感器可用的视频流配置列表
        profile_list = pipeline.get_stream_profile_list(OBSensorType.COLOR_SENSOR)
        try:
            # 尝试获取分辨率 640px，帧率 30fps，格式为RGB的配置
            color_profile: VideoStreamProfile = profile_list.get_video_stream_profile(640, 0, OBFormat.RGB, 30)
        # 如果失败，获取异常并使用默认配置
        except OBError as e:
            print(e)
            color_profile = profile_list.get_default_video_stream_profile()
            print("color profile: ", color_profile)
        # 启用彩色图像流
        config.enable_stream(color_profile)
    except Exception as e:
        print(e)
        return
    # 启动管道
    pipeline.start(config)
    while True:
        try:
            # 每 100ms 等待帧数据
            frames: FrameSet = pipeline.wait_for_frames(100)
            if frames is None:
                continue
            # 获取彩色帧
            color_frame = frames.get_color_frame()
            if color_frame is None:
                continue
            # covert to RGB format
            color_image = frame_to_bgr_image(color_frame)
            if color_image is None:
                print("failed to convert frame to image")
                continue
            # 显示图像
            cv2.imshow("Color Viewer", color_image)
            key = cv2.waitKey(1)
            if key == ord('q') or key == ESC_KEY:
                break
        except KeyboardInterrupt:
            break
    pipeline.stop()


if __name__ == "__main__":
    main()
