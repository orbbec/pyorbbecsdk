
# Object-Detection-using-YOLOv5-in-Python
This repository aims to integrate the Orbbec Depth Sensing Camera with the YOLOv5 object detection algorithm for enhanced object detection accuracy and performance. By incorporating depth information, the project strives to improve object localization and recognition in real-world environments.
## Features
* Integration of the Orbbec Depth Sensing Camera with YOLOv5
* Utilizes depth information for more precise object localization
* Improved accuracy and robustness in object detection
* Real-time object detection and depth visualization
## Support Platforms
* Linux: 20.04/22.04/24.04 (x64)
* Arm64: Ubuntu 20.04/22.04
## Prerequisites
* Python 3.8.0 and above
* PyTorch 1.8 and above
* OpenCV 4.5.5 and above
* Python Bindings for Orbbec SDK
* Other necessary dependencies (listed in requirements.txt)
## Installation
1.Python Bindings for Orbbec SDK
Refer to [UserGuide](https://orbbec.github.io/pyorbbecsdk/index.html) for detailed documentation.
2..YOLOv5 model conversion
```
cd pyorbbecsdk
git clone https://github.com/ultralytics/yolov5
export PYTHONPATH=$PYTHONPATH:$(pwd)/install/lib/
source venv/bin/activate
cd yolov5/
pip install -r requirements.txt
pip install onnx onnxruntime
python export.py --weights yolov5s.pt --include onnx --opset 12
cp  yolov5s.onnx ../examples/object_detection/models/
```
3.Run the examples
```
cd pyorbbecsdk
export PYTHONPATH=$PYTHONPATH:$(pwd)/install/lib/
source venv/bin/activate
cd examples/object_detection/
python3 object_detection_sw_align.py
```
