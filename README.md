# pyorbbecsdk — Python Bindings for Orbbec SDK v2.x

[![Build](https://img.shields.io/badge/build-GitHub%20Actions-blue?logo=github)](https://github.com/orbbec/pyorbbecsdk/actions/workflows/build.yaml)
[![PyPI](https://img.shields.io/pypi/v/pyorbbecsdk2)](https://pypi.org/project/pyorbbecsdk2/)
[![Python](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20ARM64-lightgrey)](#supported-platforms)
[![License](https://img.shields.io/badge/license-Apache%202.0-green)](LICENSE)

**pyorbbecsdk** is the official Python wrapper for the [Orbbec SDK v2.x](https://github.com/orbbec/OrbbecSDK_v2), enabling Python developers to interface with Orbbec RGB-D cameras (Gemini, Femto, Astra series) through a clean, Pythonic API backed by native C++ performance via pybind11.

> **China users:** The Gitee mirror is at [gitee.com/orbbecdeveloper/pyorbbecsdk](https://gitee.com/orbbecdeveloper/pyorbbecsdk)

> **Branch note:** This is the `v2-main` branch (SDK v2.x). For the legacy v1.x branch, see [main](https://github.com/orbbec/pyorbbecsdk/tree/main). The differences between SDK v1.x and v2.x are described in the [OrbbecSDK_v2 README](https://github.com/orbbec/OrbbecSDK_v2).

---

## Table of Contents

- [Key Features](#key-features)
- [Quick Installation](#quick-installation)
- [Quick Start](#quick-start)
- [Supported Devices & Firmware](#supported-devices--firmware)
- [Supported Platforms](#supported-platforms)
- [Supported Python Versions](#supported-python-versions)
- [Examples](#examples)
- [Documentation](#documentation)
- [Troubleshooting / FAQ](#troubleshooting--faq)
- [Contributing](#contributing)
- [Community & Support](#community--support)
- [License](#license)

---

## Key Features

- **RGB-D streaming** — depth, color, and infrared streams with configurable resolution and FPS
- **Post-processing filters** — Temporal, Spatial (Advanced), HoleFilling, Threshold, Decimation, Noise Removal
- **Depth-color alignment** — software `AlignFilter` and hardware D2C alignment
- **Point cloud generation** — colored 3D point clouds via `PointCloudFilter`
- **Camera calibration** — intrinsics, distortion coefficients, and extrinsic transforms
- **IMU support** — accelerometer and gyroscope streaming
- **Multi-device** — open and stream from multiple cameras simultaneously
- **Hot-plug detection** — detect camera connect/disconnect events at runtime
- **HDR merge** — high dynamic range depth imaging (Gemini 330 series)
- **Network cameras** — connect to Femto Mega / Gemini 2 XL over Ethernet
- **Recording & playback** — record to `.bag` files; replay offline
- **Type stubs** — full `stubs/pyorbbecsdk.pyi` for IDE autocompletion (PyCharm, VSCode)
- **Pre-built wheels** — no compilation required for Windows x64, Linux x64, and ARM64

---

## Quick Installation

### Step 1 — Install the package

**Option A — From PyPI (recommended):**

```bash
pip install pyorbbecsdk2
```

**Option B — From GitHub Release:**

Download the `.whl` file for your platform and Python version from the [Releases page](https://github.com/orbbec/pyorbbecsdk/releases), then install locally:

```bash
# Example: Windows x64, Python 3.10
pip install pyorbbecsdk2-2.0.18-cp310-cp310-win_amd64.whl
```

> **Package name note:** The PyPI package is `pyorbbecsdk2`, but the Python import name is `pyorbbecsdk`:
> ```python
> import pyorbbecsdk   # correct import name
> ```

Pre-built wheels are available for:
- **Windows x64:** Python 3.8–3.13
- **Linux x64:** Python 3.8–3.13
- **ARM64:** Python 3.8–3.13

For building from source, see [CONTRIBUTING.md](CONTRIBUTING.md#building-from-source).

### Step 2 — Environment Setup (one-time)

The camera requires a one-time OS-level configuration. Connect your device, then run the setup script:

```bash
# Windows (PowerShell — will auto-request Administrator)
python scripts/env_setup/setup_env.py

# Linux (will auto-request sudo)
python3 scripts/env_setup/setup_env.py
```

That's it! The script auto-detects your OS and applies the correct configuration:
- **Windows** — registers UVC metadata in the registry (required for correct timestamps and frame sync)
- **Linux** — installs udev rules for USB device access

You can verify the setup later with `python scripts/env_setup/setup_env.py --check`.

<details>
<summary><strong>Manual setup (if you prefer not to use the script)</strong></summary>

**Windows** — register frame metadata (run PowerShell as Administrator):
```powershell
cd scripts\env_setup
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\obsensor_metadata_win10.ps1 -op install_all
```
See [obsensor_metadata_win10.md](scripts/env_setup/obsensor_metadata_win10.md) for details.

**Linux** — install udev rules:
```bash
cd scripts/env_setup
sudo chmod +x ./install_udev_rules.sh
sudo ./install_udev_rules.sh
sudo udevadm control --reload && sudo udevadm trigger
```

</details>

---

## Quick Start

With **just 3 lines of core code**, you can get RGB-D data streaming:

```python
from pyorbbecsdk import *

pipeline = Pipeline()
pipeline.start()                        # uses default config from OrbbecSDKConfig.xml
frames = pipeline.wait_for_frames(1000)  # get synchronized Color + Depth frames
```

The complete [`examples/quick_start.py`](examples/quick_start.py) adds visualisation in ~30 lines:

```python
import cv2
import numpy as np
from pyorbbecsdk import *
from utils import frame_to_bgr_image

pipeline = Pipeline()
pipeline.start()
cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
cv2.resizeWindow(WINDOW_NAME, WINDOW_WIDTH, WINDOW_HEIGHT)

while True:
    try:
        frames = pipeline.wait_for_frames(1000)
        if frames is None:
            continue

        color_frame = frames.get_color_frame()
        color_image = frame_to_bgr_image(color_frame)

        depth_frame = frames.get_depth_frame()

        width = depth_frame.get_width()
        height = depth_frame.get_height()
        scale = depth_frame.get_depth_scale()

        depth_data = np.frombuffer(depth_frame.get_data(), dtype=np.uint16)
        depth_data = depth_data.reshape((height, width))
        depth_mm = depth_data.astype(np.float32) * scale

        depth_image = render_depth_3d(depth_mm)

        half_w = WINDOW_WIDTH // 2
        color_resized = cv2.resize(color_image, (half_w, WINDOW_HEIGHT))
        depth_resized = cv2.resize(depth_image, (half_w, WINDOW_HEIGHT))
        combined = np.hstack((color_resized, depth_resized))
        cv2.imshow(WINDOW_NAME, combined)
        if cv2.waitKey(1) in (ord('q'), ord('Q'), ESC_KEY):
            break

    except KeyboardInterrupt:
        break

cv2.destroyAllWindows()
pipeline.stop()
```

> **Default configuration:** When `pipeline.start()` is called without a `Config` object, the SDK automatically reads [`config/OrbbecSDKConfig.xml`](config/OrbbecSDKConfig.xml). You can customise stream resolution, FPS, and format in that XML file without modifying any code —  see [`config/OrbbecSDKConfig.md`](config/OrbbecSDKConfig.md) for the full reference.

For alignment, point clouds, IMU, recording, and more — see the [Examples](#examples) section.

**Running result:**

![quick_start_result](docs/_images/quick_start_result.png)

---

## Supported Devices & Firmware

The table below lists all devices supported by this SDK (v2.x branch), along with the minimum and recommended firmware versions.

| **Product Series** | **Product** | **Min Firmware** | **Recommended Firmware** |
|--------------------|-------------|------------------|--------------------------|
| **Gemini 435Le** | Gemini 435Le      | 1.2.4   | 1.3.6   |
| **Gemini 330**   | Gemini 305        | 1.0.30  | 1.0.30  |
|                  | Gemini 345        | 1.7.04  | 1.9.03  |
|                  | Gemini 345Lg      | 1.7.04  | 1.9.03  |
|                  | Gemini 335Le      | 1.5.31  | 1.6.00  |
|                  | Gemini 330        | 1.2.20  | 1.6.00  |
|                  | Gemini 330L       | 1.2.20  | 1.6.00  |
|                  | Gemini 335        | 1.2.20  | 1.6.00  |
|                  | Gemini 335L       | 1.2.20  | 1.6.00  |
|                  | Gemini 336        | 1.2.20  | 1.6.00  |
|                  | Gemini 336L       | 1.2.20  | 1.6.00  |
|                  | Gemini 335Lg      | 1.3.46  | 1.6.00  |
| **Gemini 2**     | Gemini 2          | 1.4.92  | 1.4.98  |
|                  | Gemini 2 L        | 1.4.53  | 1.5.2   |
|                  | Gemini 215        | 1.0.9   | 1.0.9   |
|                  | Gemini 210        | 1.0.9   | 1.0.9   |
| **Femto**        | Femto Bolt        | 1.1.2   | 1.1.3   |
|                  | Femto Mega        | 1.3.0   | 1.3.1   |
|                  | Femto Mega I      | 2.0.4   | 2.0.4   |
| **Astra**        | Astra 2           | 2.8.20  | 2.8.20  |
|                  | Astra Mini Pro    | 2.0.03  | 2.0.03  |
|                  | Astra Mini S Pro  | 2.0.03  | 2.0.03  |
| **Pulsar**       | Pulsar SL450      | 2.2.4.5 | 2.2.4.5 |
|                  | Pulsar ME450      | 1.0.0.6 | 1.0.0.6 |

> **Check your firmware:** `device.get_device_info().get_firmware_version()`
>
> If your firmware is below the minimum version, contact Orbbec support for upgrade assistance.

**Notes:**
- If your device is not listed, please contact our FAE or sales representative.
- Starting from October 2025 (Orbbec SDK v2.5.5), devices using the OpenNI protocol will be upgraded to UVC protocol. See [the upgrade document](https://github.com/orbbec/OrbbecSDK_v2?tab=readme-ov-file#12-upgrading-from-openni-protocol-to-uvc-protocol) for details.
- For v1.x device support (Astra+, Astra Pro Plus, Gemini 2 XL), use the [main branch](https://github.com/orbbec/pyorbbecsdk/tree/main).

---

## Supported Platforms

| Platform | Architecture | OS Version |
|----------|-------------|------------|
| Windows  | x64         | Windows 10+ |
| Linux    | x64         | Ubuntu 18.04 / 20.04 / 22.04 |
| Linux    | ARM64       | Ubuntu 18.04 / 20.04 / 22.04 |

---

## Supported Python Versions

Python **3.8** through **3.13**

| Platform | Online install | Offline install |
|----------|---------------|-----------------|
| Windows x64  | 3.8–3.13 | 3.8–3.13 |
| Linux x64    | 3.9–3.13 | 3.8–3.13 |
| Linux ARM64  | —        | 3.8–3.13 |

---

## Examples

The [examples/](examples/) directory contains **35+ scripts** organized by difficulty:

| Level | Location | Scripts | Highlights |
|-------|----------|---------|------------|
| Quick Start | `examples/quick_start.py` | 1 | Zero-config RGBD viewer — first thing to run |
| ⭐ Beginner | `examples/beginner/` | 9 | Numbered 01–09: hello camera → depth viz → alignment → calibration → point cloud → multi-stream → IMU → network camera → firmware update |
| ⭐⭐ Advanced | `examples/advanced/` | 19 | Recording & playback, device control, filter chains, HDR, presets, depth work modes, multi-device sync, coordinate transforms, high-performance pipeline |
| ⭐⭐⭐ Applications | `examples/applications/` | 2 | YOLO object detection with depth overlay; interactive depth ruler |
| LiDAR | `examples/lidar_examples/` | 5 | LiDAR streaming, control, recording, playback |

See [examples/README.md](examples/README.md) for the full list with per-script descriptions and device compatibility.

**Learning path:**
```
First time?           →  examples/quick_start.py                        (30s to first frame)
Learn the basics      →  examples/beginner/01 → 02 → 03 → 04 → 05
Specific SDK feature  →  examples/advanced/ (pick by category)
Building an app       →  examples/applications/ruler.py
                          examples/applications/object_detection/
High performance      →  examples/advanced/15_high_performance_pipeline.py
LiDAR device          →  examples/lidar_examples/lidar_quick_start.py
```

---

## Documentation

The **[Orbbec SDK V2 Python Wrapper User Guide](https://orbbec.github.io/pyorbbecsdk/index.html)** covers:

- Architecture and SDK concepts
- Installation (online and offline wheel packages, build from source)
- Python API quick-starts and usage guides
- Frequently asked questions

---

## Troubleshooting / FAQ

### Device not found (`get_count()` returns 0)

**Windows:**
- Confirm the device appears in Device Manager.
- Ensure metadata registration was completed (see [Quick Installation — Step 2](#step-2--environment-setup-one-time)).
- Try a different USB 3.0 port or cable.

**Linux:**
- Run `lsusb` and verify an Orbbec device (VID `2bc5`) appears.
- Ensure udev rules are installed and reloaded.
- Add your user to the `plugdev` group and log out/in:
  ```bash
  sudo usermod -aG plugdev $USER
  ```

---

### Timestamps incorrect / frame sync fails (Windows)

Caused by missing metadata registration.

**Fix:** Open PowerShell as administrator and run:
```powershell
.\scripts\env_setup\obsensor_metadata_win10.ps1 -op install_all
```
The camera must be connected before running the script.

---

### `import pyorbbecsdk` fails with `ModuleNotFoundError`

After a source build, the compiled module is in `install/lib/`, not on the system path.

**Fix:**
```bash
# Linux / macOS
source env.sh

# Windows (PowerShell)
$env:PYTHONPATH = "$PWD\install\lib;$env:PYTHONPATH"
```

---

### numpy version conflict / `module compiled against API version` error

numpy 2.x introduced breaking C API changes. Pin numpy to a compatible version:

```bash
pip install "numpy<2.0"
```

See [issue #47](https://github.com/orbbec/pyorbbecsdk/issues/47) for details.

---

### `Fatal Python error: Aborted` after tests end

This is a known SDK threading cleanup issue that occurs during interpreter shutdown. It does **not** indicate test failures — all test results logged before this message are valid.

---

### Device-specific feature not working (HDR, depth work mode, presets…)

Some features are model-specific:

| Feature | Required Device |
|---------|----------------|
| HDR merge | Gemini 330 series |
| Depth work mode | Gemini 2, Gemini 2L, Astra 2, Gemini 2 XL |
| Presets | Gemini 330 series |
| Network connect | Femto Mega, Gemini 2 XL |
| Hardware D2C | Select devices |

Check the [Supported Devices table](#supported-devices--firmware) and [examples/README.md](examples/README.md) for per-feature device notes.

---

### Firmware version below the required minimum

Check your current firmware version:
```python
info = device.get_device_info()
print(info.get_firmware_version())
```
Compare against the [Supported Devices table](#supported-devices--firmware). Contact Orbbec support for firmware upgrade assistance.

---

## Contributing

Contributions are welcome — bug reports, feature requests, documentation improvements, and code patches are all appreciated.

- **Report a bug:** [Open a bug report](https://github.com/orbbec/pyorbbecsdk/issues/new?template=bug_report.md)
- **Request a feature:** [Open a feature request](https://github.com/orbbec/pyorbbecsdk/issues/new?template=feature_request.md)
- **Submit a PR:** Read [CONTRIBUTING.md](CONTRIBUTING.md) for build instructions, code style, and the PR process.

---

## Community & Support

| Resource | Link |
|----------|------|
| GitHub Issues | [github.com/orbbec/pyorbbecsdk/issues](https://github.com/orbbec/pyorbbecsdk/issues) |
| Full Documentation | [orbbec.github.io/pyorbbecsdk](https://orbbec.github.io/pyorbbecsdk/index.html) |
| Orbbec SDK v2 (C++) | [github.com/orbbec/OrbbecSDK_v2](https://github.com/orbbec/OrbbecSDK_v2) |
| China Mirror (Gitee) | [gitee.com/orbbecdeveloper/pyorbbecsdk](https://gitee.com/orbbecdeveloper/pyorbbecsdk) |

---

## License

This project is licensed under the [Apache License 2.0](LICENSE).

The bundled Orbbec SDK native libraries in `sdk/lib/` are proprietary binaries distributed by Orbbec. See [sdk/lib/README.md](sdk/lib/README.md) for details.
