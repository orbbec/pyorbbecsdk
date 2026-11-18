
[English](readme.md) | **中文**

<a id="yolov5s-onnx-model"></a>

# YOLOv5s ONNX 模型

将 `yolov5s.onnx` 放在此目录中。

<a id="automatic-download-recommended"></a>

## 自动下载（推荐）

```bash
cd ..
python setup_model.py
```

<a id="manual-export"></a>

## 手动导出

```bash
git clone --depth 1 --branch v7.0 https://github.com/ultralytics/yolov5.git
cd yolov5
pip install -r requirements.txt && pip install onnx
python export.py --weights yolov5s.pt --include onnx --opset 12 --imgsz 640
```

然后将生成的 `yolov5s.onnx` 复制到此 `models/` 目录中。
