# ******************************************************************************
#  Copyright (c) 2024 Orbbec 3D Technology, Inc
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
# ******************************************************************************
"""
YOLOv5 Object Detection with Orbbec Depth Camera (Software D2C Alignment).

Runs YOLOv5s (ONNX) on the colour stream and overlays per-object median
depth measured from the aligned depth stream.

Controls:
    ESC / Q  -  Quit

Usage:
    python object_detection.py
    python object_detection.py --color_width 640 --color_height 480
    python object_detection.py --model models/yolov5s.onnx
"""

import argparse
import os
import sys
import time

import cv2
import numpy as np
import onnxruntime as ort

# ---------------------------------------------------------------------------
# Resolve paths relative to *this* script so CWD doesn't matter
# ---------------------------------------------------------------------------
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# examples/utils.py is two levels up: applications/object_detection -> examples
sys.path.insert(0, os.path.abspath(os.path.join(_SCRIPT_DIR, "..", "..")))

from utils import frame_to_bgr_image  # noqa: E402

from pyorbbecsdk import Config  # type: ignore  # noqa: E402
from pyorbbecsdk import AlignFilter, OBFormat, OBSensorType, OBStreamType, Pipeline

# ---------------------------------------------------------------------------
# Default Paths (relative to script, not CWD)
# ---------------------------------------------------------------------------
DEFAULT_MODEL_PATH = os.path.join(_SCRIPT_DIR, "models", "yolov5s.onnx")
DEFAULT_LABELS_PATH = os.path.join(_SCRIPT_DIR, "coco.names")

# ---------------------------------------------------------------------------
# Camera Resolution (None = use device default)
# ---------------------------------------------------------------------------
COLOR_CAMERA_WIDTH = None  # e.g. 640
COLOR_CAMERA_HEIGHT = None  # e.g. 480
DEPTH_CAMERA_WIDTH = None  # e.g. 640
DEPTH_CAMERA_HEIGHT = None  # e.g. 480

# ---------------------------------------------------------------------------
# YOLOv5 Inference Parameters
# ---------------------------------------------------------------------------
INPUT_WIDTH, INPUT_HEIGHT = 640, 640
SCORE_THRESHOLD = 0.5
NMS_THRESHOLD = 0.45
CONFIDENCE_THRESHOLD = 0.5
MAX_DISPLAY_BOXES = 5

# ---------------------------------------------------------------------------
# Depth Parameters (mm)
# ---------------------------------------------------------------------------
MIN_DEPTH_MM = 20  # ignore depth < 20 mm
MAX_DEPTH_MM = 10000  # ignore depth > 10 000 mm
DEPTH_OUTLIER_RATIO = 0.2  # +/-20 % around median

# ---------------------------------------------------------------------------
# Drawing Constants
# ---------------------------------------------------------------------------
ESC_KEY = 27
FONT_FACE = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.5
THICKNESS = 1
BLACK = (0, 0, 0)
RED = (0, 0, 255)

PALETTE = [
    (255, 255, 255),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 0, 255),
    (0, 255, 255),
    (128, 128, 0),
    (128, 0, 128),
    (0, 128, 128),
    (128, 128, 128),
]


# ===========================================================================
# Helper Functions
# ===========================================================================


def draw_label(img, label, x, y, color, extra_line=None):
    """Draw one or two lines of text with a filled background rectangle."""
    lines = [label] if extra_line is None else [label, extra_line]
    y_offset = 0
    for text in lines:
        (tw, th), baseline = cv2.getTextSize(text, FONT_FACE, FONT_SCALE, THICKNESS)
        if y + y_offset + th + baseline > img.shape[0]:
            break
        cv2.rectangle(
            img,
            (x, y + y_offset),
            (x + tw, y + y_offset + th + baseline),
            BLACK,
            cv2.FILLED,
        )
        cv2.putText(
            img,
            text,
            (x, y + y_offset + th),
            FONT_FACE,
            FONT_SCALE,
            color,
            THICKNESS,
            cv2.LINE_AA,
        )
        y_offset += th + baseline


# Map ONNX element type strings to numpy dtypes
_ONNX_DTYPE_MAP = {
    "tensor(float)": np.float32,
    "tensor(float16)": np.float16,
    "tensor(double)": np.float64,
}


def pre_process(img, dtype=np.float32):
    """Resize + normalise BGR image -> (1, 3, 640, 640) tensor.

    *dtype* should match the ONNX model's input type (float32 or float16).
    """
    blob = cv2.resize(img, (INPUT_WIDTH, INPUT_HEIGHT))
    blob = cv2.cvtColor(blob, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
    blob = np.transpose(blob, (2, 0, 1))[np.newaxis, ...]
    return blob.astype(dtype)


def filter_depth_outliers(values, ratio=DEPTH_OUTLIER_RATIO):
    """Keep depth values within +/-*ratio* of the median."""
    if values.size == 0:
        return values
    med = np.median(values)
    lo, hi = med * (1 - ratio), med * (1 + ratio)
    return values[(values >= lo) & (values <= hi)]


def extract_depth_map(depth_frame):
    """Extract a uint16 depth map (mm) from an Orbbec depth frame."""
    try:
        data = np.frombuffer(depth_frame.get_data(), dtype=np.uint16).reshape(
            depth_frame.get_height(), depth_frame.get_width()
        )
    except ValueError:
        print("[Warn] Failed to reshape depth data")
        return None
    data = (data.astype(np.float32) * depth_frame.get_depth_scale()).astype(np.uint16)
    data = np.where((data > MIN_DEPTH_MM) & (data < MAX_DEPTH_MM), data, 0)
    return data


def post_process(img, depth_data, predictions, classes):
    """Apply NMS, draw bounding boxes and depth labels. Returns annotated image."""
    preds = np.squeeze(predictions[0])  # shape: (N, 85)
    boxes, confidences, class_ids = [], [], []
    img_h, img_w = img.shape[:2]
    x_factor = img_w / INPUT_WIDTH
    y_factor = img_h / INPUT_HEIGHT

    for row in preds:
        obj_conf = row[4]
        if obj_conf < CONFIDENCE_THRESHOLD:
            continue
        cls_scores = row[5:]
        cid = int(np.argmax(cls_scores))
        if cls_scores[cid] * obj_conf < SCORE_THRESHOLD:
            continue
        cx, cy, w, h = row[:4]
        left = int((cx - w / 2) * x_factor)
        top = int((cy - h / 2) * y_factor)
        boxes.append([left, top, int(w * x_factor), int(h * y_factor)])
        confidences.append(float(obj_conf))
        class_ids.append(cid)

    indices = cv2.dnn.NMSBoxes(boxes, confidences, CONFIDENCE_THRESHOLD, NMS_THRESHOLD)
    if len(indices) == 0:
        return img

    for i in indices.flatten()[:MAX_DISPLAY_BOXES]:
        left, top, bw, bh = boxes[i]
        # Clamp ROI to depth map bounds
        x0 = max(0, left)
        y0 = max(0, top)
        x1 = min(left + bw, depth_data.shape[1])
        y1 = min(top + bh, depth_data.shape[0])

        roi = depth_data[y0:y1, x0:x1].flatten()
        valid = roi[roi > 0]
        filtered = filter_depth_outliers(valid)

        depth_label = f"depth:{int(np.median(filtered))}mm" if filtered.size > 0 else "depth:N/A"

        color = PALETTE[class_ids[i] % len(PALETTE)]
        cv2.rectangle(img, (left, top), (left + bw, top + bh), color, 2)

        label = f"{classes[class_ids[i]]}:{confidences[i]:.2f}"
        lx = max(2, min(left + 2, img_w - 102))
        ly = max(37, min(top + bh - 5, img_h - 2))
        draw_label(img, label, lx, ly - 35, color, depth_label)

    return img


# ===========================================================================
# Camera Configuration
# ===========================================================================


def _find_profile(profiles, width, height, fmt=None):
    """Return the first matching stream profile, or None."""
    for p in profiles:
        if p.get_width() == width and p.get_height() == height:
            if fmt is None or p.get_format() == fmt:
                return p
    return None


def build_config(pipeline, color_w=None, color_h=None, depth_w=None, depth_h=None):
    """Build a Pipeline Config with optional resolution overrides.

    Resolution priority: CLI args > global constants > device default.
    """
    cw = color_w or COLOR_CAMERA_WIDTH
    ch = color_h or COLOR_CAMERA_HEIGHT
    dw = depth_w or DEPTH_CAMERA_WIDTH
    dh = depth_h or DEPTH_CAMERA_HEIGHT

    config = Config()
    try:
        color_profiles = pipeline.get_stream_profile_list(OBSensorType.COLOR_SENSOR)
        depth_profiles = pipeline.get_stream_profile_list(OBSensorType.DEPTH_SENSOR)

        # -- Colour stream --
        color_profile = None
        if cw and ch:
            color_profile = _find_profile(color_profiles, cw, ch, OBFormat.RGB)
            if color_profile:
                print(f"[Config] Color: {cw}x{ch}")
            else:
                print(f"[Config] Color {cw}x{ch} not found, using default")
        if color_profile is None:
            color_profile = color_profiles.get_default_video_stream_profile()
            print(f"[Config] Color: {color_profile.get_width()}x" f"{color_profile.get_height()} (default)")
        config.enable_stream(color_profile)

        # -- Depth stream --
        depth_profile = None
        if dw and dh:
            depth_profile = _find_profile(depth_profiles, dw, dh)
            if depth_profile:
                print(f"[Config] Depth: {dw}x{dh}")
            else:
                print(f"[Config] Depth {dw}x{dh} not found, using default")
        if depth_profile is None:
            depth_profile = depth_profiles.get_default_video_stream_profile()
            print(f"[Config] Depth: {depth_profile.get_width()}x" f"{depth_profile.get_height()} (default)")
        config.enable_stream(depth_profile)

    except Exception as e:
        print(f"[Config] Failed: {e}")
        return None

    return config


# ===========================================================================
# Main
# ===========================================================================


def main():
    parser = argparse.ArgumentParser(description="YOLOv5 object detection with Orbbec depth camera")
    parser.add_argument(
        "--model",
        type=str,
        default=DEFAULT_MODEL_PATH,
        help="Path to YOLOv5s ONNX model",
    )
    parser.add_argument(
        "--labels",
        type=str,
        default=DEFAULT_LABELS_PATH,
        help="Path to class labels file (coco.names)",
    )
    parser.add_argument("--color_width", type=int, default=None, help="Color camera width")
    parser.add_argument("--color_height", type=int, default=None, help="Color camera height")
    parser.add_argument("--depth_width", type=int, default=None, help="Depth camera width")
    parser.add_argument("--depth_height", type=int, default=None, help="Depth camera height")
    args = parser.parse_args()

    # ---- Validate model & labels ----
    if not os.path.isfile(args.model):
        print(f"[Error] Model not found: {args.model}")
        print(f"  Run  python {os.path.join(_SCRIPT_DIR, 'setup_model.py')}  to download it.")
        return 1
    if not os.path.isfile(args.labels):
        print(f"[Error] Labels file not found: {args.labels}")
        return 1

    with open(args.labels, "r") as f:
        classes = f.read().strip().split("\n")
    print(f"[Model] {os.path.basename(args.model)}  ({len(classes)} classes)")

    # ---- ONNX Runtime session ----
    providers = ort.get_available_providers()
    print(f"[ONNX]  Providers: {providers}")
    session = ort.InferenceSession(args.model, providers=providers)
    input_meta = session.get_inputs()[0]
    input_name = input_meta.name
    input_dtype = _ONNX_DTYPE_MAP.get(input_meta.type, np.float32)
    print(f"[ONNX]  Input: {input_name}  dtype={input_meta.type}")

    # ---- Camera pipeline ----
    pipeline = Pipeline()
    config = build_config(
        pipeline,
        args.color_width,
        args.color_height,
        args.depth_width,
        args.depth_height,
    )
    if config is None:
        print("[Error] Could not configure camera streams.")
        return 1

    pipeline.start(config)
    align_filter = AlignFilter(align_to_stream=OBStreamType.COLOR_STREAM)
    print("[Camera] Pipeline started.  Press ESC or Q to quit.\n")

    # Create a resizable window for the object detection visualization
    cv2.namedWindow("YOLOv5 + Orbbec Depth", cv2.WINDOW_NORMAL)

    prev_time = time.time()
    try:
        while True:
            frames = pipeline.wait_for_frames(1000)
            if not frames:
                continue
            frames = align_filter.process(frames)
            if not frames:
                continue

            color_frame = frames.get_color_frame()
            depth_frame = frames.get_depth_frame()
            if not color_frame or not depth_frame:
                continue

            img_bgr = frame_to_bgr_image(color_frame)
            if img_bgr is None:
                continue

            # Inference
            t0 = time.time()
            outputs = session.run(None, {input_name: pre_process(img_bgr, input_dtype)})
            infer_ms = (time.time() - t0) * 1000

            # Depth map
            depth_data = extract_depth_map(depth_frame)
            if depth_data is None:
                continue

            # Post-process & draw
            result = post_process(img_bgr.copy(), depth_data, outputs, classes)

            # OSD: inference time + FPS
            now = time.time()
            fps = 1.0 / max(now - prev_time, 1e-6)
            prev_time = now
            cv2.putText(
                result,
                f"Infer: {infer_ms:.1f}ms | FPS: {fps:.1f}",
                (10, 20),
                FONT_FACE,
                FONT_SCALE,
                RED,
                THICKNESS,
                cv2.LINE_AA,
            )

            cv2.imshow("YOLOv5 + Orbbec Depth", result)
            if cv2.waitKey(1) in (ESC_KEY, ord("q"), ord("Q")):
                break

    except KeyboardInterrupt:
        print("\n[Info] Interrupted by user.")
    finally:
        cv2.destroyAllWindows()
        pipeline.stop()

    return 0


if __name__ == "__main__":
    sys.exit(main())
