# pyorbbecsdk Examples

A curated collection of examples organized by difficulty level — from connecting your first camera to building production-grade streaming pipelines.

---

## Prerequisites

**All examples require:**

1. A connected Orbbec camera (see the [device support matrix](../README.md#device-support))
2. pyorbbecsdk installed:
   ```bash
   pip install pyorbbecsdk2
   ```
3. Python dependencies:
   ```bash
   pip install -r examples/requirements.txt
   ```

**One-time OS setup (required before running any example):**

- **Linux:** Install udev rules so the OS grants USB access:
  ```bash
  cd scripts/env_setup
  sudo chmod +x install_udev_rules.sh && sudo ./install_udev_rules.sh
  sudo udevadm control --reload && sudo udevadm trigger
  ```
- **Windows:** Register frame metadata (required for correct timestamps):
  ```powershell
  # Run PowerShell as Administrator
  cd scripts\env_setup
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  .\obsensor_metadata_win10.ps1 -op install_all
  ```

**Running an example (from the repository root):**
```bash
python examples/beginner/01_hello_camera.py
python examples/depth.py
```

---

## Level 1 — Beginner (Start Here ⭐)

Three annotated tutorials designed for first-time users. Each file is heavily commented, teaches one concept at a time, and requires no prior Orbbec SDK knowledge. **Run them in order: 01 → 02 → 03.**

| Script | What You Learn | Extra Dependencies |
|--------|---------------|--------------------|
| `beginner/01_hello_camera.py` | Discover connected devices, print device name, firmware version, and sensor list | none |
| `beginner/02_depth_visualization.py` | Configure a depth stream, convert raw `uint16` data to millimeters, display with an OpenCV colormap | numpy, opencv-python |
| `beginner/03_color_and_depth_aligned.py` | Enable multiple streams simultaneously, use `AlignFilter` to project depth into the color camera view | numpy, opencv-python |

> **Tip:** After running all three, try `quick_start.py` for a self-contained color + depth side-by-side viewer.

---

## Level 2 — Intermediate (⭐⭐)

Single-feature scripts you can run independently. Each demonstrates one aspect of the SDK with minimal boilerplate.

### Device & System

| Script | Description | Device Notes |
|--------|-------------|--------------|
| `enumerate.py` | List all connected devices, sensors, stream profiles, and supported formats | All |
| `hot_plug.py` | Detect camera connect/disconnect events at runtime via callbacks | All |
| `logger.py` | Set the SDK log level (`DEBUG` / `INFO` / `WARNING` / `ERROR`); redirect logs to a custom file path | All |
| `control.py` | Read and write device properties: exposure, gain, white balance, mirror, flood, laser, etc. | All |

### Streaming

| Script | Description | Device Notes |
|--------|-------------|--------------|
| `quick_start.py` | Color + depth side-by-side viewer; the simplest full-featured example | All |
| `color.py` | Color-only stream viewer with format display | All |
| `depth.py` | Depth-only stream viewer with min/max range overlay | All |
| `infrared.py` | IR stream viewer | All |
| `imu.py` | Read accelerometer and gyroscope data; display timestamp, temperature, and values | All |
| `callback.py` | Receive frames via async callback (non-blocking pipeline mode) | All |
| `multi_streams.py` | Enable all available streams at once in a single pipeline | All |
| `multi_device.py` | Open and stream from two or more cameras simultaneously | All |
| `net_device.py` | Connect to a network-attached camera via IP address | Femto Mega, Gemini 2 XL |

### Data Capture

| Script | Description | Device Notes |
|--------|-------------|--------------|
| `metadata.py` | Read per-frame metadata: exposure time, gain, timestamp, sensor temperature | All |
| `save_image_to_disk.py` | Capture a single frame and save as PNG (color) or PGM (depth) to disk | All |
| `recorder.py` | Record a live stream to a `.bag` file for offline replay | All |
| `playback.py` | Replay a previously recorded `.bag` file | All |
| `record_no_gui.py` | Record a stream without opening any display window (headless mode) | All |

---

## Level 3 — Advanced (⭐⭐⭐)

These scripts combine multiple SDK features or require domain knowledge of depth sensing.

### Post-Processing & Alignment

| Script | Description | Device Notes |
|--------|-------------|--------------|
| `advanced/custom_filter_chain.py` | Chain `TemporalFilter` + `SpatialAdvancedFilter` + `HoleFillingFilter` + `ThresholdFilter`; use keyboard shortcuts to tune parameters live | All |
| `sync_align.py` | Software `AlignFilter` — align depth to color in Python, configurable target stream | All |
| `hw_d2c_align.py` | Hardware D2C alignment — depth-to-color projection done on-device (lower CPU overhead) | Select devices |
| `post_processing.py` | Compare before/after applying the full post-processing filter stack | Gemini 330 series |

### Performance & Architecture

| Script | Description | Device Notes |
|--------|-------------|--------------|
| `advanced/high_performance_pipeline.py` | Async callback pipeline with bounded frame queue, FPS meter, and end-to-end latency measurement | All |

### 3D & Geometry

| Script | Description | Device Notes |
|--------|-------------|--------------|
| `point_cloud.py` | Generate a colored 3D point cloud using `PointCloudFilter`; save to `.ply` for open3d visualization | All |
| `coordinate_transform.py` | Transform between 2D image, 3D depth, and color coordinate systems using the calibration API | All |

### Device-Specific Features

| Script | Description | Device Notes |
|--------|-------------|--------------|
| `hdr.py` | HDR merge: combine alternating-exposure frames for extended dynamic range depth | Gemini 330 series |
| `preset.py` | Load and apply named depth presets (e.g., `Default`, `Hand`, `High Accuracy`) | Gemini 330 series |
| `depth_work_mode.py` | Switch depth work modes at runtime: High Accuracy, High Density, Medium Density, etc. | Gemini 2, Gemini 2L, Astra 2, Gemini 2 XL |
| `two_devices_sync.py` | Hardware-level frame synchronization between two cameras (primary/secondary trigger) | All |
| `device_firmware_update.py` | Perform an OTA firmware upgrade by reading a `.bin` file and flashing the device | All |
| `device_optional_depth_presets_update.py` | Update optional depth preset profiles on the device | Gemini 330 series |
| `laser_interleave.py` | Enable laser interleave mode to reduce multi-camera interference | Select devices |
| `confidence.py` | Access depth confidence data alongside the depth frame | Select devices |
| `forceip.py` | Assign a static IP address to a network-attached camera | Femto Mega, Gemini 2 XL |

---

## Specialized — LiDAR (⭐⭐⭐)

Examples for Orbbec LiDAR devices. Located in `examples/lidar_examples/`.

| Script | Description |
|--------|-------------|
| `lidar_quick_start.py` | Minimal LiDAR streaming example — first stop for LiDAR users |
| `lidar_stream.py` | Full LiDAR stream viewer with visualization |
| `lidar_device_control.py` | Read and set LiDAR-specific device properties |
| `lidar_record.py` | Record LiDAR data to a `.bag` file |
| `lidar_playback.py` | Replay a recorded LiDAR session |

---

## Specialized — Object Detection (⭐⭐⭐)

Computer vision examples using depth + color together. Located in `examples/object_detection/`.

| Script | Description |
|--------|-------------|
| `object_detection_sw_align.py` | Real-time YOLO object detection with software-aligned depth overlay; shows detected object distance in meters |

> **Requires:** `pip install open3d` for point cloud examples; model files are included in `object_detection/models/`.

---

## Utilities

| File | Purpose |
|------|---------|
| `utils.py` | Shared helpers used across multiple examples (e.g., `frame_to_bgr_image`, colormap conversion) |
| `requirements.txt` | All Python dependencies for the example suite |

---

## Learning Path Summary

```
New to Orbbec?     →  beginner/01 → 02 → 03 → quick_start.py
Need a specific    →  Pick any Level 2 script by feature
feature?
Building a real    →  advanced/high_performance_pipeline.py
application?              + advanced/custom_filter_chain.py
Working with 3D?   →  point_cloud.py + coordinate_transform.py
Using a LiDAR?     →  lidar_examples/lidar_quick_start.py
```
