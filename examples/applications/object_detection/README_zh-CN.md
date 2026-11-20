
[English](README.md) | **中文**

<a id="yolov5-object-detection-with-orbbec-depth-camera"></a>

# 使用 Orbbec 深度相机进行 YOLOv5 目标检测

在 Orbbec RGB-D 相机上使用 YOLOv5s（ONNX）进行实时目标检测。每个检测目标都会标注类别、置信度，以及从软件对齐的深度流中测得的**深度中位数（mm）**。

![pipeline](https://img.shields.io/badge/Pipeline-Color%20%2B%20Depth%20(SW%20Align)-blue)
![model](https://img.shields.io/badge/Model-YOLOv5s%20ONNX-orange)

<a id="features"></a>

## 功能

- 通过 ONNX Runtime 进行 YOLOv5s 推理（CPU / CUDA / TensorRT）。
- 软件深度到彩色对齐（`AlignFilter`）。
- 对每个目标计算深度中位数，并过滤异常值。
- 通过命令行配置相机分辨率。
- 一键下载模型（`setup_model.py`）。

<a id="supported-platforms"></a>

## 支持的平台

| 操作系统 | 架构 |
|---|---|
| Windows 10 / 11 | x64 |
| Ubuntu 20.04 / 22.04 / 24.04 | x64 |
| Ubuntu 20.04 / 22.04 | ARM64 |

<a id="quick-start"></a>

## 快速入门

<a id="1-one-click-setup-recommended"></a>

### 1. 一键配置（推荐）

```bash
# Install dependencies + download YOLOv5s ONNX model automatically
python setup_model.py
```

该脚本将：

- 安装运行依赖（`onnxruntime`、`opencv-python`、`numpy`）。
- 将 YOLOv5s ONNX 模型下载到 `models/yolov5s.onnx`。

<a id="2-run"></a>

### 2. 运行

```bash
python object_detection.py
```

自定义分辨率：

```bash
python object_detection.py --color_width 640 --color_height 480 --depth_width 640 --depth_height 480
```

<a id="controls"></a>

### 按键控制

| 按键 | 操作 |
|---|---|
| `ESC` / `Q` | 退出 |

<a id="manual-setup-alternative"></a>

## 手动配置（备选方式）

如果 `setup_model.py` 执行失败，或希望手动配置：

<a id="install-dependencies"></a>

### 安装依赖

```bash
pip install numpy opencv-python onnxruntime
```

<a id="export-yolov5s-onnx-model"></a>

### 导出 YOLOv5s ONNX 模型

```bash
git clone --depth 1 https://github.com/ultralytics/yolov5.git /tmp/yolov5
cd /tmp/yolov5
pip install -r requirements.txt
pip install onnx
python export.py --weights yolov5s.pt --include onnx --opset 12 --imgsz 640
cp yolov5s.onnx <path_to>/object_detection/models/
```

<a id="cli-arguments"></a>

## 命令行参数

| 参数 | 默认值 | 说明 |
|---|---|---|
| `--model` | `models/yolov5s.onnx` | ONNX 模型路径 |
| `--labels` | `coco.names` | 类别标签文件路径 |
| `--color_width` | 设备默认值 | 彩色流宽度 |
| `--color_height` | 设备默认值 | 彩色流高度 |
| `--depth_width` | 设备默认值 | 深度流宽度 |
| `--depth_height` | 设备默认值 | 深度流高度 |

<a id="project-structure"></a>

## 项目结构

```
object_detection/
  ├── setup_model.py                   # One-click setup: deps + model download
  ├── object_detection.py     # Main detection script
  ├── coco.names                       # COCO 80-class label file
  ├── README.md
  └── models/
      └── yolov5s.onnx                # YOLOv5s model (after setup)
```

<a id="prerequisites"></a>

## 前置条件

- Python >= 3.8。
- 已安装 Orbbec SDK Python 绑定（`pyorbbecsdk`）。
- 已连接 Orbbec RGB-D 相机（Gemini、Femto、Astra 等）。
