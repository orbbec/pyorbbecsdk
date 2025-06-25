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
# Import Libraries
import cv2
import time
import argparse
import numpy as np
import onnxruntime as ort
from pyorbbecsdk import *

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))

from utils import frame_to_bgr_image

# Global Parameters
# Users can directly set the camera resolution here. If set to None, the default profile will be used
COLOR_CAMERA_WIDTH = None  # for example 640
COLOR_CAMERA_HEIGHT = None  # for example 400
DEPTH_CAMERA_WIDTH = None  # for example 640
DEPTH_CAMERA_HEIGHT = None  # for example 400

ESC_KEY = 27
INPUT_WIDTH, INPUT_HEIGHT = 640, 640
SCORE_THRESHOLD = 0.5
NMS_THRESHOLD = 0.45
CONFIDENCE_THRESHOLD = 0.5
MAX_DISPLAY_BOXES = 5

# Temporal filter for smoothing depth data over time
MIN_DEPTH = 20  # 20mm
MAX_DEPTH = 10000  # 10000mm

# Font and Colors
FONT_FACE = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.5
THICKNESS = 1
BLACK, RED = (0, 0, 0), (0, 0, 255)

# Color cycle for object recognition frames
PALETTE = [(255, 255, 255), (0, 255, 0), (0, 0, 255), (255, 255, 0),
           (255, 0, 255), (0, 255, 255), (128, 128, 0),
           (128, 0, 128), (0, 128, 128), (128, 128, 128)]

# Draw YOLOv5 Inference Label
def draw_label(img, label, x, y, color, extra_line=None):
    # Draw labels on the image (supports two lines: class name+confidence, depth information)
    lines = [label] if extra_line is None else [label, extra_line]
    y_offset = 0
    for text in lines:
        # Get text size
        ts, bs = cv2.getTextSize(text, FONT_FACE, FONT_SCALE, THICKNESS)
        w, h = ts
        if y + y_offset + h + bs > img.shape[0]:
            break
        # Use text size to create a BLACK rectangle
        cv2.rectangle(img, (x, y + y_offset), (x + w, y + y_offset + h + bs), BLACK, cv2.FILLED)
        # Display text inside the rectangle
        cv2.putText(img, text, (x, y + y_offset + h), FONT_FACE, FONT_SCALE, color, THICKNESS, cv2.LINE_AA)
        y_offset += h + bs

# PRE-PROCESSING YOLOv5 Model
def pre_process(img):
    # Preprocess images for ONNX model input
    blob = cv2.resize(img, (INPUT_WIDTH, INPUT_HEIGHT))
    blob = cv2.cvtColor(blob, cv2.COLOR_BGR2RGB)
    blob = blob.astype(np.float32) / 255.0
    blob = np.transpose(blob, (2, 0, 1))[np.newaxis, ...] # (1, 3, 640, 640)
    return blob

# Depth anomaly filtering, taking the median depth
def filter_depth_outliers(depth_values, threshold=0.2):
    # Filter depth outliers: Keep data within a certain range near the median
    if depth_values.size == 0:
        return depth_values
    median = np.median(depth_values)
    lower = median * (1 - threshold)
    upper = median * (1 + threshold)
    return depth_values[(depth_values >= lower) & (depth_values <= upper)]

# POST-PROCESSING YOLOv5 Prediction Output YOLOv5
def post_process(img, depth_frame, outs):
    # Process model output+NMS+plotting+depth median calculation
    predictions = np.squeeze(outs[0]) # shape: (N, 85)
    boxes, confidences, class_ids = [], [], []
    img_h, img_w = img.shape[:2]
    x_factor, y_factor = img_w / INPUT_WIDTH, img_h / INPUT_HEIGHT
    # Obtain depth data (in millimeters)
    """
    depth_data = np.frombuffer(depth_frame.get_data(), dtype=np.uint16).reshape(
        (depth_frame.get_height(), depth_frame.get_width())
    )
    """
    try:
        depth_data = np.frombuffer(depth_frame.get_data(), dtype=np.uint16).reshape(
            (depth_frame.get_height(), depth_frame.get_width()))
    except ValueError:
        print("Failed to reshape depth data")

    depth_data = depth_data.astype(np.float32) * depth_frame.get_depth_scale()
    depth_data = np.where((depth_data > MIN_DEPTH) & (depth_data < MAX_DEPTH), depth_data, 0)
    depth_data = depth_data.astype(np.uint16)


    for row in predictions:
        conf = row[4]
        if conf < CONFIDENCE_THRESHOLD:
            continue
        cls_scores = row[5:]
        class_id = np.argmax(cls_scores)
        if cls_scores[class_id] * conf < SCORE_THRESHOLD:
            continue
        cx, cy, w, h = row[0:4]
        left = int((cx - w/2) * x_factor)
        top = int((cy - h/2) * y_factor)
        width = int(w * x_factor)
        height = int(h * y_factor)
        boxes.append([left, top, width, height])
        confidences.append(float(conf))
        class_ids.append(class_id)

    indices = cv2.dnn.NMSBoxes(boxes, confidences, CONFIDENCE_THRESHOLD, NMS_THRESHOLD)
    if len(indices) == 0:
        return img

    for i in indices.flatten()[:MAX_DISPLAY_BOXES]:
        left, top, width, height = boxes[i]
        right = min(left + width, depth_data.shape[1])
        bottom = min(top + height, depth_data.shape[0])
        depth_roi = depth_data[top:bottom, left:right] # Depth area within the frame
        depth_values = depth_roi.flatten()
        valid_depths = depth_values[depth_values > 0] # Remove the value of 0
        filtered_depths = filter_depth_outliers(valid_depths) # Remove Outliers

        if filtered_depths.size > 0:
            depth_at_center = int(np.median(filtered_depths))
            depth_label = f"depth:{depth_at_center}mm"
        else:
            depth_label = "depth:N/A"

        box_color = PALETTE[class_ids[i] % len(PALETTE)]
        cv2.rectangle(img, (left, top), (left + width, top + height), box_color, 2)
        
        label = f"{classes[class_ids[i]]}:{confidences[i]:.2f}"
        label_x = max(2, min(left + 2, img.shape[1] - 100 - 2))
        label_y = max(2 + 35, min(top + height - 5, img.shape[0] - 2))
        draw_label(img, label, label_x, label_y - 35, box_color, depth_label)
    return img

# Orbbec 3D Camera D2C Data Stream
def get_sw_align_config(pipeline, color_req_width=None, color_req_height=None, depth_req_width=None, depth_req_height=None):
    """
    Use software alignment to configure the flow.
    Priority should be given to using the command-line parameters color_req_width/color_req_height and depth_req_width/depth_req_height
    If not provided, use global COLOR_CAMERA_WIDTH/COLOR_CAMERA_HEIGHT and DEPTH_CAMERA_WIDTH/DEPTH_CAMERA_HEIGHT
    If the final resolution exists and matches the profile, use the specified resolution; otherwise, use the default profile and print the prompt.
    """
    # Determine final resolution: prioritize command line, then global
    cw = color_req_width if color_req_width is not None else COLOR_CAMERA_WIDTH
    ch = color_req_height if color_req_height is not None else COLOR_CAMERA_HEIGHT
    dw = depth_req_width if depth_req_width is not None else DEPTH_CAMERA_WIDTH
    dh = depth_req_height if depth_req_height is not None else DEPTH_CAMERA_HEIGHT

    config = Config()
    try:
        color_profiles = pipeline.get_stream_profile_list(OBSensorType.COLOR_SENSOR)
        depth_profiles = pipeline.get_stream_profile_list(OBSensorType.DEPTH_SENSOR)

        # Select color profile
        color_profile = None
        if cw and ch:
            for cp in color_profiles:
                if cp.get_format() == OBFormat.RGB and cp.get_width() == cw and cp.get_height() == ch:
                    color_profile = cp
                    print(f"Use specified color resolution profile: {cw}x{ch}")
                    break
            if color_profile is None:
                print(f"No matching color profile found {cw}x{ch}, Use default profile")
        if color_profile is None:
            color_profile = color_profiles.get_default_video_stream_profile()
            print(f"Use default color profile: {color_profile.get_width()}x{color_profile.get_height()}")
        config.enable_stream(color_profile)

        # Select depth profile
        depth_profile = None
        if dw and dh:
            for dp in depth_profiles:
                if dp.get_width() == dw and dp.get_height() == dh:
                    depth_profile = dp
                    print(f"Use specified depth resolution profile: {dw}x{dh}")
                    break
            if depth_profile is None:
                print(f"No matching depth profile found {dw}x{dh}, Use default profile")
        if depth_profile is None:
            depth_profile = depth_profiles.get_default_video_stream_profile()
            print(f"Use default depth profile: {depth_profile.get_width()}x{depth_profile.get_height()}")
        config.enable_stream(depth_profile)

    except Exception as e:
        print(f"Failed to get software align config: {e}")
        return None

    return config

if __name__ == '__main__':
    # Example of executed commands：python object_detection_sw_align.py --color_width 640 --color_height 480 --depth_width 640 --depth_height 480
    parser = argparse.ArgumentParser()
    parser.add_argument('--color_width', type=int, default=None, help="Expected color camera resolution width")
    parser.add_argument('--color_height', type=int, default=None, help="Expected color camera resolution height")
    parser.add_argument('--depth_width', type=int, default=None, help="Expected depth camera resolution width")
    parser.add_argument('--depth_height', type=int, default=None, help="Expected depth camera resolution height")
    args = parser.parse_args()

    # Load category labels
    with open('coco.names', 'rt') as f:
        classes = f.read().strip().split('\n')

    # Initialize ONNX Runtime
    ort_session = ort.InferenceSession('models/yolov5s.onnx')
    input_name = ort_session.get_inputs()[0].name

    # Start the camera
    pipeline = Pipeline()
    config = get_sw_align_config(pipeline, args.color_width, args.color_height, args.depth_width, args.depth_height)
    if config is None:
        print("No suitable stream profile found.")
        exit(1)

    pipeline.start(config)
    align_filter = AlignFilter(align_to_stream=OBStreamType.COLOR_STREAM)
    prev_time = time.time()

    while True:
        # Get aligned frames
        frames = pipeline.wait_for_frames(100)
        if not frames:
            continue

        frames = align_filter.process(frames)
        if not frames:
            continue
        frames = frames.as_frame_set()

        color_frame = frames.get_color_frame()
        depth_frame = frames.get_depth_frame()
        if not color_frame or not depth_frame:
            continue

        # Process image
        img_bgr = frame_to_bgr_image(color_frame)
        if img_bgr is None:
            print("Failed to convert frame to image")
            continue

        # Inference
        input_tensor = pre_process(img_bgr)
        start_infer = time.time()
        outputs = ort_session.run(None, {input_name: input_tensor})
        inference_time_ms = (time.time() - start_infer) * 1000

        # Inference result processing
        result = post_process(img_bgr.copy(), depth_frame, outputs)

        # Display frame rate and time consumption
        curr_time = time.time()
        frame_time_ms = (curr_time - prev_time) * 1000
        fps = 1000.0 / frame_time_ms
        prev_time = curr_time

        cv2.putText(result, f"Inference time:{inference_time_ms:.2f}ms", (10, 20),
                    FONT_FACE, FONT_SCALE, RED, THICKNESS, cv2.LINE_AA)

        """ 
        cv2.putText(result, f"FPS:{fps:.2f}  Frame:{frame_time_ms:.2f}ms", (10, 40),
                    FONT_FACE, FONT_SCALE, RED, THICKNESS, cv2.LINE_AA)
        """
        
        cv2.imshow('Output', result)
        if cv2.waitKey(1) in (ESC_KEY, ord('q')):
            break

    cv2.destroyAllWindows()
    pipeline.stop()
