# ******************************************************************************
#  Copyright (c) 2024 Orbbec 3D Technology, Inc
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
import time
import cv2
import numpy as np
from pyorbbecsdk import *

ESC_KEY = 27

def main():
    config = Config()
    pipeline = Pipeline()
    config.enable_accel_stream()
    config.enable_gyro_stream()
    config.set_frame_aggregate_output_mode(OBFrameAggregateOutputMode.FULL_FRAME_REQUIRE)
    pipeline.start(config)
    while True:
        try:
            frames = pipeline.wait_for_frames(100)
            if frames is None:
                continue
            
            accel_frame = frames.get_frame(OBFrameType.ACCEL_FRAME)
            accel_frame = accel_frame.as_accel_frame()
            
            if accel_frame is not None:
                accel_index = accel_frame.get_index()
                if accel_index % 50 == 0:
                    print("AccelFrame: ts={}".format(accel_frame.get_timestamp()))
                    print("AccelFrame: x={}, y={}, z={}".format(accel_frame.get_x(), accel_frame.get_y(),accel_frame.get_z()))    

            gyro_frame = frames.get_frame(OBFrameType.GYRO_FRAME)
            gyro_frame = gyro_frame.as_gyro_frame()
            if gyro_frame is not None:
                gyro_index = gyro_frame.get_index()
                if gyro_index % 50 == 0:
                    print("GyroFrame: ts={}".format(gyro_frame.get_timestamp()))
                    print("GyroFrame: x={}, y={}, z={}".format(gyro_frame.get_x(), gyro_frame.get_y(),gyro_frame.get_z()))  

            key = cv2.waitKey(1)
            if key == ord('q') or key == ESC_KEY:
                break            
        except KeyboardInterrupt:
            break           

if __name__ == "__main__":
    main()
