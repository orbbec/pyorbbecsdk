# V2 New Features

This document highlights the new features, capabilities, and architectural evolution introduced in the **v2-main** branch (SDK v2.x series).

---

## Overview

The v2-main branch represents a full rewrite of the Python bindings targeting
**Orbbec SDK v2.7.6+**, which itself is a major architectural evolution from the v1.x SDK.
The key difference is that SDK v2.x uses the UVC protocol for newer devices, whereas
v1.x used the proprietary OpenNI protocol.

> For the v1.x changelog, refer to the [main branch](https://github.com/orbbec/pyorbbecsdk/tree/main).

### Dependencies

- Requires **Orbbec SDK v2.7.6** or newer (precompiled libraries bundled in `sdk/lib/`)
- pybind11 2.11.0 or newer

### Added

#### Core API Classes
- `Context` — SDK entry point; device enumeration and lifecycle management
- `Pipeline` / `Config` — stream configuration and frame acquisition loop
- `Device` / `DeviceList` / `DeviceInfo` — device identity, firmware info, property access
- `Sensor` / `SensorList` — sensor enumeration (depth, color, IR, IMU, etc.)
- `StreamProfile` / `VideoStreamProfile` / `AccelStreamProfile` / `GyroStreamProfile` — stream resolution, FPS, and format configuration

#### Frame Types
- `Frame`, `VideoFrame` — base frame class with timestamp, metadata, and data buffer access
- `DepthFrame` — depth data with scale factor (convert raw `uint16` to millimeters)
- `ColorFrame` — RGB / MJPEG / Y8 color frames
- `IRFrame` — infrared frames (left and right IR for stereo cameras)
- `PointsFrame` — 3D point cloud data
- `AccelFrame` / `GyroFrame` — IMU accelerometer and gyroscope frames
- `FrameSet` — multi-stream frame container from `Pipeline.wait_for_frames()`

#### Post-Processing Filters
- `AlignFilter` — software depth-to-color (or color-to-depth) alignment
- `TemporalFilter` — reduces depth noise by averaging across consecutive frames
- `SpatialAdvancedFilter` — edge-preserving spatial smoothing
- `HoleFillingFilter` — fills invalid depth pixels using neighbor interpolation
- `ThresholdFilter` — clips depth values to a min/max range
- `DecimationFilter` — reduces resolution while preserving depth validity
- `FormatConvertFilter` — converts between frame formats
- `NoiseRemovalFilter` — removes isolated noisy depth pixels
- `PointCloudFilter` — generates colored 3D point clouds from depth + color frames
- `HDRMergeFilter` — merges alternating-exposure frames for extended dynamic range
- `SequenceIdFilter` — selects frames from a specific sequence (e.g., for HDR)

#### Calibration and Geometry
- `OBCameraIntrinsic` — focal length, principal point, image dimensions
- `OBCameraDistortion` — radial and tangential distortion coefficients
- `OBExtrinsic` — rotation matrix and translation vector between sensor frames
- `OBCalibrationParam` — full calibration parameter set for all sensors
- `CoordinateTransformHelper` — utilities for 2D ↔ 3D ↔ depth ↔ color coordinate transforms

#### Device Features
- IMU streaming — accelerometer and gyroscope via `OBSensorType.ACCEL` / `GYRO`
- Multi-device support — open and stream from multiple cameras simultaneously
- Hot-plug detection — register callbacks for device connect/disconnect events
- Network camera support — connect to Femto Mega and Gemini 2 XL over Ethernet
- HDR merge — high dynamic range depth (Gemini 330 series)
- Hardware D2C alignment — depth-to-color alignment processed on-device
- Depth work mode switching — High Accuracy, High Density, etc. (select devices)
- Device preset management — load/save named depth presets (Gemini 330 series)
- Device firmware update — OTA firmware upgrade via `device_firmware_update.py`
- Recording and playback — record streams to bag files; replay offline

#### Developer Experience
- Comprehensive type stubs (`stubs/pyorbbecsdk.pyi`, 3600+ lines) for full IDE autocompletion
- Pre-built wheels for Windows x64, Linux x64, and Linux ARM64 (Python 3.8–3.13)
- Beginner example series (`examples/beginner/`):
  - `01_hello_camera.py` — device discovery and info display
  - `02_depth_visualization.py` — depth streaming with OpenCV colormap
  - `03_color_and_depth_aligned.py` — multi-stream with AlignFilter
- Advanced example series (`examples/advanced/`):
  - `high_performance_pipeline.py` — async callback with bounded frame queue and FPS meter
  - `custom_filter_chain.py` — filter chain with live keyboard tuning
- 25+ additional standalone examples covering every major SDK feature
- pytest test suite:
  - Device, controls, streams, filters, calibration, and performance test modules
  - `conftest.py` with session-scoped fixtures and automatic hardware skip
  - HTML report generation via `test/generate_report.py`

### Supported Platforms

| Platform | Architecture | OS |
|----------|--------------|----|
| Windows | x64 | Windows 10+ |
| Linux | x64 | Ubuntu 18.04, 20.04, 22.04 |
| Linux | ARM64 | Ubuntu 18.04, 20.04, 22.04 |
| macOS | x64 | macOS (experimental, CI only) |

### Supported Python Versions

Python 3.8, 3.9, 3.10, 3.11, 3.12, 3.13

### Supported Devices

See the [device support matrix](README.md#device-support) in README.md.

Notable device families supported in v2-main:
- **Gemini 435Le**
- **Gemini 330 series** (335, 335L, 335Le, 335Lg, 336, 336L, 330, 330L)
- **Gemini 2 series** (Gemini 2, 2L, 215, 210)
- **Femto series** (Femto Bolt, Femto Mega, Femto Mega I)
- **Astra 2**, **Astra Mini Pro/S Pro**
- **Gemini 305**, **Gemini 345**, **Gemini 345Lg**
- **Pulsar SL450**, **Pulsar ME450**
