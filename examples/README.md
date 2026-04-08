# pyorbbecsdk Examples

A curated collection of examples organized by difficulty — from connecting your first camera to building complete depth-sensing applications.

---

## Quick Start 

Connect your camera, then run:

```bash
python examples/quick_start.py
```

This opens a color + depth side-by-side viewer immediately, no configuration needed.
Once it works, follow the **Learning Path** below.

---

## Prerequisites

1. Install pyorbbecsdk:
   ```bash
   pip install pyorbbecsdk2
   pip install -r examples/requirements.txt
   ```

2. **One-time OS setup:**

   - **Linux** — grant USB access via udev rules:
     ```bash
     cd scripts/env_setup
     sudo chmod +x install_udev_rules.sh && sudo ./install_udev_rules.sh
     sudo udevadm control --reload && sudo udevadm trigger
     ```
   - **Windows** — register frame metadata (run PowerShell as Administrator):
     ```powershell
     cd scripts\env_setup
     Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
     .\obsensor_metadata_win10.ps1 -op install_all
     ```

---

## Level 1 — Beginner ⭐

Nine numbered tutorials, designed to be **run in order: 01 → 02 → … → 09**.
Each script is heavily commented, teaches one concept, and builds on the previous.

| # | Script | What You Learn | Dependencies |
|---|--------|---------------|--------------|
| 01 | `beginner/01_hello_camera.py` | SDK logging setup; discover devices; print name, firmware, serial; enumerate default stream configs; read depth presets | none |
| 02 | `beginner/02_depth_visualization.py` | Depth stream; uint16 → mm conversion; gamma correction; Scharr-gradient 3D lighting; press **C** to cycle 8 colormaps | numpy, opencv |
| 03 | `beginner/03_color_and_depth_aligned.py` | Color + depth streams; software `AlignFilter` (default) or hardware D2C (`--hw`); blended overlay; toggle direction / transparency | numpy, opencv |
| 04 | `beginner/04_camera_calibration.py` | Read `OBCameraParam`: intrinsics (fx, fy, cx, cy), distortion coefficients, depth→color extrinsic (R\|t); build OpenCV K matrix | numpy |
| 05 | `beginner/05_point_cloud.py` | `PointCloudFilter` + `AlignFilter` to generate a colored 3D point cloud; save to `.ply` for Open3D / MeshLab | numpy |
| 06 | `beginner/06_multi_streams.py` | All streams simultaneously (color, depth, IR, IMU) via async callbacks; dynamic grid display | numpy, opencv |
| 07 | `beginner/07_imu.py` | Enable ACCEL + GYRO; read timestamp, temperature, and 3-axis values in real time | none |
| 08 | `beginner/08_net_device.py` | Connect to a network camera; decode H.264 / MJPG with PyAV; display via pygame | av, pygame |
| 09 | `beginner/09_device_firmware_update.py` | OTA firmware upgrade from a `.bin` file; progress callback; safe upgrade practices | none |

```bash
# Run any beginner example from the repo root:
python examples/beginner/01_hello_camera.py
python examples/beginner/03_color_and_depth_aligned.py        # software align
python examples/beginner/03_color_and_depth_aligned.py --hw   # hardware D2C
```

---

## Level 2 — Advanced ⭐⭐

Single-feature scripts that each go deeper into one area of the SDK.

### Recording & Playback

| Script | Description | Notes |
|--------|-------------|-------|
| `advanced/01_recorder.py` | Record all streams to `.bag`; GUI preview (default) or headless with `--no-gui`; pause/resume | All |
| `advanced/02_playback.py` | Replay a `.bag` file; auto-loop; dynamic multi-stream grid | All |
| `advanced/03_save_image_to_disk.py` | Capture a fixed number of frames and save as PNG / 16-bit PNG | All |

### Device & System

| Script | Description | Notes |
|--------|-------------|-------|
| `advanced/04_enumerate.py` | List all devices, sensors, and every supported stream profile interactively | All |
| `advanced/05_hot_plug.py` | Register a callback to detect camera connect / disconnect events | All |
| `advanced/06_control.py` | Enumerate all device properties (bool/int/float), check permissions, get/set values | All |
| `advanced/07_metadata.py` | Read per-frame metadata: exposure time, gain, timestamp, sensor temperature | All |

### Depth Processing & Alignment

| Script | Description | Notes |
|--------|-------------|-------|
| `advanced/08_custom_filter_chain.py` | Chain Temporal + Spatial + HoleFilling + Threshold filters; tune live with keyboard | All |
| `advanced/09_post_processing.py` | Full post-processing stack; raw vs. filtered side-by-side comparison | Gemini 330 |
| `advanced/10_hdr.py` | HDR merge: combine alternating-exposure frames with `HdrMergeFilter` | Gemini 330 |
| `advanced/11_preset.py` | Load named depth presets (`Default`, `Hand`, `High Accuracy`); switch at runtime | Gemini 330 |
| `advanced/12_depth_work_mode.py` | Switch depth work modes (High Accuracy, High Density, …) at runtime | Gemini 2 series |
| `advanced/13_confidence.py` | Access depth confidence map; visualize and threshold per-pixel confidence | Select devices |

### Multi-Device & Network

| Script | Description | Notes |
|--------|-------------|-------|
| `advanced/14_two_devices_sync.py` | Two cameras simultaneously; hardware frame sync via JSON config | All |
| `advanced/15_high_performance_pipeline.py` | Async callback pipeline; bounded frame queue; FPS + latency measurement | All |
| `advanced/16_coordinate_transform.py` | 2D↔2D, 2D↔3D, 3D↔3D, 3D↔2D transforms using calibration API; press 1–4 | All |
| `advanced/17_laser_interleave.py` | Laser interleave mode to reduce multi-camera IR interference | Select devices |
| `advanced/18_forceip.py` | Assign a static IP to a network camera | Femto Mega, Gemini 2 XL |
| `advanced/19_device_optional_depth_presets_update.py` | Write optional depth preset profiles to device | Gemini 330 |

```bash
python examples/advanced/01_recorder.py              # with live preview
python examples/advanced/01_recorder.py --no-gui     # headless, prints FPS
python examples/advanced/08_custom_filter_chain.py
```

---

## Level 3 — Applications ⭐⭐⭐

Complete working applications that combine multiple SDK features.

| Script | Description | Dependencies |
|--------|-------------|--------------|
| `applications/object_detection.py` | Real-time YOLO object detection on the aligned color stream; depth overlay per detected object | onnxruntime, opencv |
| `applications/ruler.py` | **Interactive depth ruler** — drag to draw a line on the color image; computes the real 3D Euclidean distance (mm) using back-projection; press **C** to clear | numpy, opencv |

```bash
python examples/applications/ruler.py
python examples/applications/object_detection.py
```

> **How the ruler works:** For each endpoint (u, v) the app reads the aligned depth value Z, then computes `X = (u−cx)·Z/fx`, `Y = (v−cy)·Z/fy`. Distance = ‖P2 − P1‖₂ in mm.

---

## Specialized — LiDAR ⭐⭐⭐

For Orbbec LiDAR devices. Located in `examples/lidar_examples/`.

| Script | Description |
|--------|-------------|
| `lidar_quick_start.py` | Minimal LiDAR streaming — first stop for LiDAR users |
| `lidar_stream.py` | Continuous LiDAR point cloud viewer with live stats |
| `lidar_device_control.py` | Read and set LiDAR-specific properties; enable scan + IMU |
| `lidar_record.py` | Record LiDAR data to a `.bag` file |
| `lidar_playback.py` | Replay a recorded LiDAR session |

---

## Utilities

| File | Purpose |
|------|---------|
| `utils.py` | Shared helpers: `frame_to_bgr_image()`, format converters, device type checks |
| `requirements.txt` | All Python dependencies for the example suite |

---

## Learning Path

```
First time?           →  quick_start.py  (30 seconds to first frame)
                          then beginner/01 → 02 → 03 → 04 → 05

Want a specific       →  Pick any Level 2 script by category
SDK feature?

Building an app?      →  applications/ruler.py
                          applications/object_detection.py

Multi-device / sync?  →  advanced/14_two_devices_sync.py
High performance?     →  advanced/15_high_performance_pipeline.py

Using a LiDAR?        →  lidar_examples/lidar_quick_start.py
```
