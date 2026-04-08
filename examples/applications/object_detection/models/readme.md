# YOLOv5s ONNX Model

Place `yolov5s.onnx` in this directory.

## Automatic Download (recommended)

```bash
cd ..
python setup_model.py
```

## Manual Export

```bash
git clone --depth 1 --branch v7.0 https://github.com/ultralytics/yolov5.git
cd yolov5
pip install -r requirements.txt && pip install onnx
python export.py --weights yolov5s.pt --include onnx --opset 12 --imgsz 640
```

Then copy the resulting `yolov5s.onnx` into this `models/` directory.
