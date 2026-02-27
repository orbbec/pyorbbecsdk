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
- [Device Support](#device-support)
- [Hardware & Firmware Requirements](#hardware-products-supported-by-python-sdk)
- [Supported Platforms](#supported-platforms)
- [Supported Python Versions](#supported-python-versions)
- [Environment Setup](#environment-setup)
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

```bash
pip install pyorbbecsdk2
```

> **Package name note:** The PyPI package is `pyorbbecsdk2`, but the Python import name is `pyorbbecsdk`:
> ```python
> import pyorbbecsdk   # correct import name
> ```

Pre-built wheels are available for:
- **Windows x64:** Python 3.8–3.13 (online and offline)
- **Linux x64:** Python 3.9–3.13 (online), 3.8–3.13 (offline)
- **ARM64:** Python 3.8–3.13 (offline packages only)

For offline installation packages or building from source, see the [installation documentation](https://orbbec.github.io/pyorbbecsdk/source/2_installation/install_the_package.html).

---

## Quick Start

### Step 1 — Verify your camera is detected

```python
from pyorbbecsdk import Context, OBLogLevel

ctx = Context()
ctx.set_logger_level(OBLogLevel.WARNING)

device_list = ctx.query_devices()
if device_list.get_count() == 0:
    print("No device found. Check USB connection and environment setup.")
else:
    device = device_list.get_device_by_index(0)
    info = device.get_device_info()
    print(f"Connected : {info.get_name()}")
    print(f"Firmware  : {info.get_firmware_version()}")
    print(f"Serial    : {info.get_serial_number()}")
```

### Step 2 — Read one depth frame

```python
from pyorbbecsdk import Pipeline, Config, OBSensorType
import numpy as np

pipeline = Pipeline()
config   = Config()

profile_list = pipeline.get_stream_profile_list(OBSensorType.DEPTH_SENSOR)
config.enable_stream(profile_list.get_default_video_stream_profile())
pipeline.start(config)

frame_set = pipeline.wait_for_frames(2000)   # wait up to 2 s
if frame_set:
    depth_frame = frame_set.get_depth_frame()
    if depth_frame:
        w, h  = depth_frame.get_width(), depth_frame.get_height()
        scale = depth_frame.get_depth_scale()
        data  = np.frombuffer(depth_frame.get_data(), dtype=np.uint16)
        depth_mm = data.reshape(h, w) * scale
        cx, cy   = w // 2, h // 2
        print(f"Center pixel depth: {depth_mm[cy, cx]:.0f} mm")

pipeline.stop()
```

For visual display, alignment, point clouds, IMU, and more — see the [Examples](#examples) section.

---

## Device Support

> [!IMPORTANT]
> Before using this SDK, verify that your device is supported in the `v2-main` branch (v2.x column below).

<table border="1" style="border-collapse: collapse; text-align: left; width: 100%;">
  <thead>
    <tr style="background-color: #1f4e78; color: white; text-align: center;">
      <th>Product Series</th>
      <th>Product</th>
      <th><a href="https://github.com/orbbec/pyorbbecsdk/tree/main" style="color: white; text-decoration: none;">Branch main (v1.x)</a></th>
      <th><a href="https://github.com/orbbec/pyorbbecsdk/tree/v2-main" style="color: white; text-decoration: none;">Branch v2-main (v2.x)</a></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align: center; font-weight: bold;">Gemini 435Le</td>
      <td>Gemini 435Le</td>
      <td>not supported</td>
      <td>recommended for new designs</td>
    </tr>
    <tr>
      <td rowspan="8" style="text-align: center; font-weight: bold;">Gemini 330</td>
      <td>Gemini 335Le</td>
      <td>not supported</td>
      <td>recommended for new designs</td>
    </tr>
    <tr>
      <td>Gemini 335</td>
      <td>full maintenance</td>
      <td>recommended for new designs</td>
    </tr>
    <tr>
      <td>Gemini 336</td>
      <td>full maintenance</td>
      <td>recommended for new designs</td>
    </tr>
    <tr>
      <td>Gemini 330</td>
      <td>full maintenance</td>
      <td>recommended for new designs</td>
    </tr>
    <tr>
      <td>Gemini 335L</td>
      <td>full maintenance</td>
      <td>recommended for new designs</td>
    </tr>
    <tr>
      <td>Gemini 336L</td>
      <td>full maintenance</td>
      <td>recommended for new designs</td>
    </tr>
    <tr>
      <td>Gemini 330L</td>
      <td>full maintenance</td>
      <td>recommended for new designs</td>
    </tr>
    <tr>
      <td>Gemini 335Lg</td>
      <td>not supported</td>
      <td>recommended for new designs</td>
    </tr>
    <tr>
      <td rowspan="5" style="text-align: center; font-weight: bold;">Gemini 2</td>
      <td>Gemini 2</td>
      <td>full maintenance</td>
      <td>recommended for new designs</td>
    </tr>
    <tr>
      <td>Gemini 2 L</td>
      <td>full maintenance</td>
      <td>recommended for new designs</td>
    </tr>
    <tr>
      <td>Gemini 2 XL</td>
      <td>recommended for new designs</td>
      <td>to be supported</td>
    </tr>
    <tr>
      <td>Gemini 215</td>
      <td>not supported</td>
      <td>recommended for new designs</td>
    </tr>
    <tr>
      <td>Gemini 210</td>
      <td>not supported</td>
      <td>recommended for new designs</td>
    </tr>
    <tr>
      <td rowspan="3" style="text-align: center; font-weight: bold;">Femto</td>
      <td>Femto Bolt</td>
      <td>full maintenance</td>
      <td>recommended for new designs</td>
    </tr>
    <tr>
      <td>Femto Mega</td>
      <td>full maintenance</td>
      <td>recommended for new designs</td>
    </tr>
    <tr>
      <td>Femto Mega I</td>
      <td>full maintenance</td>
      <td>recommended for new designs</td>
    </tr>
    <tr>
      <td rowspan="3" style="text-align: center; font-weight: bold;">Astra</td>
      <td>Astra 2</td>
      <td>full maintenance</td>
      <td>recommended for new designs</td>
    </tr>
    <tr>
      <td>Astra+</td>
      <td>limited maintenance</td>
      <td>not supported</td>
    </tr>
    <tr>
      <td>Astra Pro Plus</td>
      <td>limited maintenance</td>
      <td>not supported</td>
    </tr>
    <tr>
      <td style="text-align: center; font-weight: bold;">Astra Mini</td>
      <td>Astra Mini (S) Pro</td>
      <td>full maintenance</td>
      <td>recommended for new designs</td>
    </tr>
  </tbody>
</table>

**Notes:**
- If you do not find your device, please contact our FAE or sales representative for help.
- Starting from October 2025 (Orbbec SDK v2.5.5), devices using the OpenNI protocol will be upgraded to UVC protocol. See [the upgrade document](https://github.com/orbbec/OrbbecSDK_v2?tab=readme-ov-file#12-upgrading-from-openni-protocol-to-uvc-protocol) for details.

**Maintenance status definitions:**

| Status | Meaning |
|--------|---------|
| recommended for new designs | Full support: new features, bug fixes, and performance optimization |
| full maintenance | Bug fix support |
| limited maintenance | Critical bug fix support only |
| not supported | Not supported in this branch/version |
| to be supported | Support planned for a future release |

---

## Hardware Products Supported by Python SDK

| **Product** | **Minimum Firmware** | **Recommended Firmware** |
|-------------|----------------------|--------------------------|
| Gemini 305        | 1.0.30  | 1.0.30  |
| Gemini 345        | 1.7.04  | 1.9.03  |
| Gemini 345Lg      | 1.7.04  | 1.9.03  |
| Gemini 435Le      | 1.2.4   | 1.3.6   |
| Gemini 335Le      | 1.5.31  | 1.6.00  |
| Gemini 330        | 1.2.20  | 1.6.00  |
| Gemini 330L       | 1.2.20  | 1.6.00  |
| Gemini 335        | 1.2.20  | 1.6.00  |
| Gemini 335L       | 1.2.20  | 1.6.00  |
| Gemini 336        | 1.2.20  | 1.6.00  |
| Gemini 336L       | 1.2.20  | 1.6.00  |
| Gemini 335Lg      | 1.3.46  | 1.6.00  |
| Femto Bolt        | 1.1.2   | 1.1.3   |
| Femto Mega        | 1.3.0   | 1.3.1   |
| Femto Mega I      | 2.0.4   | 2.0.4   |
| Astra 2           | 2.8.20  | 2.8.20  |
| Gemini 2 L        | 1.4.53  | 1.5.2   |
| Gemini 2          | 1.4.92  | 1.4.98  |
| Gemini 215        | 1.0.9   | 1.0.9   |
| Gemini 210        | 1.0.9   | 1.0.9   |
| Astra Mini Pro    | 2.0.03  | 2.0.03  |
| Astra Mini S Pro  | 2.0.03  | 2.0.03  |
| Pulsar SL450      | 2.2.4.5 | 2.2.4.5 |
| Pulsar ME450      | 1.0.0.6 | 1.0.0.6 |

---

## Supported Platforms

| Platform | Architecture | OS Version |
|----------|-------------|------------|
| Windows  | x64         | Windows 10+ |
| Linux    | x64         | Ubuntu 18.04 / 20.04 / 22.04 |
| Linux    | ARM64       | Ubuntu 18.04 / 20.04 / 22.04 |
| macOS    | x64         | Experimental (CI build only) |

---

## Supported Python Versions

Python **3.8** through **3.13**

| Platform | Online install | Offline install |
|----------|---------------|-----------------|
| Windows x64  | 3.8–3.13 | 3.8–3.13 |
| Linux x64    | 3.9–3.13 | 3.8–3.13 |
| Linux ARM64  | —        | 3.8–3.13 |

---

## Environment Setup

The SDK requires a one-time OS-level configuration before the camera can be opened.

### Windows — Metadata Registration

Frame timestamps and frame synchronization rely on Windows metadata. Without this step, timestamps will be incorrect and frame sync will fail.

1. Connect the device and confirm it appears in Device Manager.
2. Open **PowerShell as Administrator**.
3. Navigate to the setup script:
   ```powershell
   cd pyorbbecsdk\scripts\env_setup
   ```
4. Allow script execution:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```
   If the above fails, try:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope CurrentUser
   ```
5. Run the installer:
   ```powershell
   .\obsensor_metadata_win10.ps1 -op install_all
   ```

*If metadata is not registered, device timestamps will be abnormal and the SDK's internal frame synchronization functionality will be affected.*

### Linux — udev Rules

Without udev rules, opening the device will fail due to USB permission issues.

```bash
cd pyorbbecsdk/scripts/env_setup
sudo chmod +x ./install_udev_rules.sh
sudo ./install_udev_rules.sh
sudo udevadm control --reload && sudo udevadm trigger
```

### ARM64 (Linux)

Follow the same Linux udev rules steps above. ARM64 pre-built wheels are available as offline packages — see the [installation documentation](https://orbbec.github.io/pyorbbecsdk/source/2_installation/install_the_package.html).

---

## Examples

The [examples/](examples/) directory is organized by difficulty level:

| Level | Location | Description |
|-------|----------|-------------|
| ⭐ Beginner | `examples/beginner/` | 3 annotated tutorials: hello camera → depth visualization → color+depth alignment |
| ⭐⭐ Intermediate | `examples/*.py` | 20+ single-feature scripts: streaming, IMU, callbacks, multi-device, recording |
| ⭐⭐⭐ Advanced | `examples/advanced/` | Async pipeline with FPS meter; filter chain with live keyboard tuning |
| Specialized | `examples/lidar_examples/` `examples/object_detection/` | LiDAR streaming; depth-fused object detection |

See [examples/README.md](examples/README.md) for the full list with descriptions and device compatibility notes.

**Learning path:**
```
New user?          →  examples/beginner/01_hello_camera.py
Need depth data?   →  examples/beginner/02_depth_visualization.py
Building an app?   →  examples/advanced/high_performance_pipeline.py
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
- Ensure metadata registration was completed (see [Environment Setup](#environment-setup)).
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

Check the [Hardware Products table](#hardware-products-supported-by-python-sdk) and [examples/README.md](examples/README.md) for per-feature device notes.

---

### Firmware version below the required minimum

Check your current firmware version:
```python
info = device.get_device_info()
print(info.get_firmware_version())
```
Compare against the [Hardware Products table](#hardware-products-supported-by-python-sdk). Contact Orbbec support for firmware upgrade assistance.

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
