# YOLOv5 Object Detection with Orbbec Depth Camera

Real-time object detection using YOLOv5s (ONNX) on an Orbbec RGB-D camera. Each
detected object is annotated with its class, confidence and **median depth (mm)**
measured from the software-aligned depth stream.

![pipeline](https://img.shields.io/badge/Pipeline-Color%20%2B%20Depth%20(SW%20Align)-blue)
![model](https://img.shields.io/badge/Model-YOLOv5s%20ONNX-orange)

## Features

- YOLOv5s inference via ONNX Runtime (CPU / CUDA / TensorRT)
- Software Depth-to-Color alignment (`AlignFilter`)
- Per-object median depth with outlier filtering
- Configurable camera resolution via CLI
- One-click model download (`setup_model.py`)

## Supported Platforms

| OS | Architecture |
|---|---|
| Windows 10 / 11 | x64 |
| Ubuntu 20.04 / 22.04 / 24.04 | x64 |
| Ubuntu 20.04 / 22.04 | ARM64 |

## Quick Start

### 1. One-Click Setup (recommended)

```bash
# Install dependencies + download YOLOv5s ONNX model automatically
python setup_model.py
```

This will:
- Install runtime dependencies (`onnxruntime`, `opencv-python`, `numpy`)
- Download the YOLOv5s ONNX model to `models/yolov5s.onnx`

### 2. Run

```bash
python object_detection.py
```

With custom resolution:

```bash
python object_detection.py --color_width 640 --color_height 480 --depth_width 640 --depth_height 480
```

### Controls

| Key | Action |
|---|---|
| `ESC` / `Q` | Quit |

## Manual Setup (alternative)

If `setup_model.py` fails or you prefer manual control:

### Install Dependencies

```bash
pip install numpy opencv-python onnxruntime
```

### Export YOLOv5s ONNX Model

```bash
git clone --depth 1 https://github.com/ultralytics/yolov5.git /tmp/yolov5
cd /tmp/yolov5
pip install -r requirements.txt
pip install onnx
python export.py --weights yolov5s.pt --include onnx --opset 12 --imgsz 640
cp yolov5s.onnx <path_to>/object_detection/models/
```

## CLI Arguments

| Argument | Default | Description |
|---|---|---|
| `--model` | `models/yolov5s.onnx` | Path to ONNX model |
| `--labels` | `coco.names` | Path to class label file |
| `--color_width` | Device default | Color stream width |
| `--color_height` | Device default | Color stream height |
| `--depth_width` | Device default | Depth stream width |
| `--depth_height` | Device default | Depth stream height |

## Project Structure

```
object_detection/
  ├── setup_model.py                   # One-click setup: deps + model download
  ├── object_detection.py     # Main detection script
  ├── coco.names                       # COCO 80-class label file
  ├── README.md
  └── models/
      └── yolov5s.onnx                # YOLOv5s model (after setup)
```

## Prerequisites

- Python >= 3.8
- Orbbec SDK Python bindings (`pyorbbecsdk`) installed
- Orbbec RGB-D camera connected (Gemini, Femto, Astra, etc.)

