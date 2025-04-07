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

# 用于控制打印频率
import time

# OpenCV，用于图像显示
import cv2
# 用于处理深度图数据
import numpy as np

# 3D 相机交互
from pyorbbecsdk import Config
from pyorbbecsdk import OBSensorType
from pyorbbecsdk import Pipeline

ESC_KEY = 27
PRINT_INTERVAL = 1  # seconds
MIN_DEPTH = 20  # 20mm
MAX_DEPTH = 10000  # 10000mm

# 时间滤波器
# 一阶指数滤波器
class TemporalFilter:
    def __init__(self, alpha):
        # 滤波强度
        self.alpha = alpha
        self.previous_frame = None

    def process(self, frame):
        if self.previous_frame is None:
            result = frame
        else:
            # 加权平均当前帧与上一帧
            result = cv2.addWeighted(frame, self.alpha, self.previous_frame, 1 - self.alpha, 0)
        self.previous_frame = result
        return result


def main():
    # 初始化相机配置
    config = Config()
    pipeline = Pipeline()
    temporal_filter = TemporalFilter(alpha=0.5)
    try:
        # 配置深度图像流
        profile_list = pipeline.get_stream_profile_list(OBSensorType.DEPTH_SENSOR)
        assert profile_list is not None
        depth_profile = profile_list.get_default_video_stream_profile()
        assert depth_profile is not None
        print("depth profile: ", depth_profile)
        config.enable_stream(depth_profile)
    except Exception as e:
        print(e)
        return
    pipeline.start(config)
    last_print_time = time.time()
    while True:
        try:
            # 等待并获取深度帧
            frames = pipeline.wait_for_frames(100)
            if frames is None:
                continue
            depth_frame = frames.get_depth_frame()
            if depth_frame is None:
                continue
            # 获取帧数据与尺寸
            width = depth_frame.get_width()
            height = depth_frame.get_height()
            scale = depth_frame.get_depth_scale()

            # 将缓冲区转换为 NumPy 图像矩阵
            # 原始深度数据为 uint16
            depth_data = np.frombuffer(depth_frame.get_data(), dtype=np.uint16)
            # 乘以 scale 将单位从整数转换为毫米
            depth_data = depth_data.reshape((height, width))

            depth_data = depth_data.astype(np.float32) * scale
            # 屏蔽掉不合法的深度值
            depth_data = np.where((depth_data > MIN_DEPTH) & (depth_data < MAX_DEPTH), depth_data, 0)
            depth_data = depth_data.astype(np.uint16)
            # Apply temporal filtering
            # depth_data = temporal_filter.process(depth_data)

            # # 获取中心点距离
            # center_y = int(height / 2)
            # center_x = int(width / 2)
            # center_distance = depth_data[center_y, center_x]

            # # 每隔 1s 打印一次
            # current_time = time.time()
            # if current_time - last_print_time >= PRINT_INTERVAL:
            #     print("center distance: ", center_distance)
            #     last_print_time = current_time

            # 将深度值归一化到 0~255
            depth_image = cv2.normalize(depth_data, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
            # 将单通道图像转为伪彩色
            depth_image = cv2.applyColorMap(depth_image, cv2.COLORMAP_JET)

            # 显示图像
            cv2.imshow("Depth Viewer", depth_image)
            key = cv2.waitKey(1)
            if key == ord('q') or key == ESC_KEY:
                break
        except KeyboardInterrupt:
            break
    pipeline.stop()


if __name__ == "__main__":
    main()
