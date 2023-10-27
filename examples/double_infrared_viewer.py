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
from pyorbbecsdk import *
import cv2
import numpy as np

ESC_KEY = 27
#Notes: Demonstrates how to display the double infrared stream,Currently, only Gemini 2 XL supports simultaneous output of double IR

def process_ir_frame(ir_frame):
    if ir_frame is None:
        return None

    ir_data = np.asanyarray(ir_frame.get_data())
    width = ir_frame.get_width()
    height = ir_frame.get_height()
    ir_format = ir_frame.get_format()

    if ir_format == OBFormat.Y8:
        ir_data = np.resize(ir_data, (height, width, 1))
        data_type = np.uint8
        image_dtype = cv2.CV_8UC1
        max_data = 255
    elif ir_format == OBFormat.MJPG:
        ir_data = cv2.imdecode(ir_data, cv2.IMREAD_UNCHANGED)
        data_type = np.uint8
        image_dtype = cv2.CV_8UC1
        max_data = 255
        if ir_data is None:
            print("decode mjpeg failed")
            return None
        ir_data = np.resize(ir_data, (height, width, 1))
    else:
        ir_data = np.frombuffer(ir_data, dtype=np.uint16)
        data_type = np.uint16
        image_dtype = cv2.CV_16UC1
        max_data = 65535
        ir_data = np.resize(ir_data, (height, width, 1))

    cv2.normalize(ir_data, ir_data, 0, max_data, cv2.NORM_MINMAX, dtype=image_dtype)
    ir_data = ir_data.astype(data_type)
    ir_image = cv2.cvtColor(ir_data, cv2.COLOR_GRAY2RGB)
    return ir_image


def main():
    config = Config()
    pipeline = Pipeline()

    # Configure both LEFT and RIGHT IR streams
    left_profile_list = pipeline.get_stream_profile_list(OBSensorType.LEFT_IR_SENSOR)
    right_profile_list = pipeline.get_stream_profile_list(OBSensorType.RIGHT_IR_SENSOR)
    # Get the default video stream profile from config/OrbbecSDKConfig_v1.0.xml
    left_ir_profile = left_profile_list.get_default_video_stream_profile()
    right_ir_profile = right_profile_list.get_default_video_stream_profile()
    config.enable_stream(left_ir_profile)
    config.enable_stream(right_ir_profile)
    pipeline.start(config)

    while True:
        try:
            frames = pipeline.wait_for_frames(100)
            if frames:
                left_ir_frame = frames.get_frame(OBFrameType.LEFT_IR_FRAME)
                right_ir_frame = frames.get_frame(OBFrameType.RIGHT_IR_FRAME)

                left_ir_image = process_ir_frame(left_ir_frame)
                right_ir_image = process_ir_frame(right_ir_frame)

                if left_ir_image is not None and right_ir_image is not None:
                    combined_ir_image = np.hstack((left_ir_image, right_ir_image))
                    cv2.imshow("Infrared Viewer", combined_ir_image)

                key = cv2.waitKey(1)
                if key == ord('q') or key == ESC_KEY:
                    break

        except KeyboardInterrupt:
            break

    pipeline.stop()


if __name__ == "__main__":
    main()
