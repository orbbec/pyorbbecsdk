<h1 align="center">
  pyorbbecsdk
  <br>
</h1>

<p align="center">
  Python Bindings for Orbbec SDK v2.x
  <br />
  The official Python wrapper enabling developers to interface with Orbbec RGB-D cameras (Gemini, Femto, Astra series) through a clean, Pythonic API backed by native C++ performance via pybind11.
</p>

<p align="center">
  <a href="https://orbbec.github.io/pyorbbecsdk/index.html">Documentation</a>
  ·
  <a href="https://pypi.org/project/pyorbbecsdk2/">PyPI Package</a>
  ·
  <a href="https://github.com/orbbec/pyorbbecsdk/issues">Community</a>
  ·
  <a href="https://github.com/orbbec/OrbbecSDK_v2">OrbbecSDK v2</a>
  ·
  <a href="https://gitee.com/orbbecdeveloper/pyorbbecsdk">Gitee Mirror</a>
</p>

<p align="center">
  <a href="https://github.com/orbbec/pyorbbecsdk/actions/workflows/build.yaml"><img src="https://img.shields.io/badge/build-GitHub%20Actions-blue?logo=github" alt="Build"></a>
  <a href="https://pypi.org/project/pyorbbecsdk2/"><img src="https://img.shields.io/pypi/v/pyorbbecsdk2" alt="PyPI"></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue" alt="Python"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-Apache%202.0-green" alt="License"></a>
</p>

---

> **Branch note:** This is the `v2-main` branch (SDK v2.x). For the legacy v1.x branch, see [main](https://github.com/orbbec/pyorbbecsdk/tree/main). The differences between SDK v1.x and v2.x are described in the [OrbbecSDK_v2 README](https://github.com/orbbec/OrbbecSDK_v2).

## Table of Contents

- [Supported Devices](#supported-devices)
- [Why pyorbbecsdk?](#why-pyorbbecsdk)
- [Getting started](#getting-started)
- [Samples](#samples)
- [Supported platforms](#supported-platforms)
- [Automated Firmware Update](#automated-firmware-update)
- [Community](#community)
- [License](#license)

## Supported Devices

> **Important:** 
> - Most new devices come with compatible firmware pre-installed and work out-of-the-box.
> - Starting from October 2025 (Orbbec SDK v2.5.5), devices using the OpenNI protocol will be upgraded to UVC protocol. See [the upgrade document](https://github.com/orbbec/OrbbecSDK_v2?tab=readme-ov-file#12-upgrading-from-openni-protocol-to-uvc-protocol) for details.
> - For legacy v1.x device support (Astra+, Astra Pro Plus, Gemini 2 XL), use the [main branch](https://github.com/orbbec/pyorbbecsdk/tree/main).

Here is the simplified device support list comparing the `v2-main` branch (v2.x) with the legacy `main` branch (v1.x):

| Camera Family | `v2-main` (SDK v2.x) | `main` (SDK v1.x) |
| :--- | :---: | :---: |
| **Gemini 330 Series** (335, 336, 330, L/Le/Lg) <br> **Gemini 435Le** | ✅ **Recommended** | ⚠️ Maintenance / None |
| **Gemini 2 Series** (2, 2 L, 210, 215) | ✅ **Recommended** | ⚠️ Maintenance / None |
| **Gemini 2 XL** | ⏳ *Planned* | ✅ Recommended |
| **Femto Series** (Bolt, Mega, Mega I) | ✅ **Recommended** | ⚠️ Maintenance |
| **Astra 2, Astra Mini (S) Pro** | ✅ **Recommended** | ⚠️ Maintenance |
| **Legacy Astra** (+, Pro Plus) | ❌ Not Supported | ⚠️ Maintenance |

*Note: "Recommended" means full support with new features. "Maintenance" means bug fixes only. "None" means not supported in that branch.*

## Why pyorbbecsdk?

- 📷 **RGB-D streaming** — Depth, color, and infrared streams with configurable resolution and FPS.
- 🛠️ **Post-processing filters** — Temporal, Spatial (Advanced), HoleFilling, Threshold, Decimation, Noise Removal.
- 🎯 **Depth-color alignment** — Software `AlignFilter` and hardware D2C alignment.
- ☁️ **Point cloud generation** — Colored 3D point clouds via `PointCloudFilter`.
- 📐 **Camera calibration** — Intrinsics, distortion coefficients, and extrinsic transforms.
- ⚡ **Real-time performance** — Backed by native C++ performance via pybind11.
- 🌐 **Network cameras** — Connect to Femto Mega / Gemini 2 XL over Ethernet.
- 📦 **Pre-built wheels** — No compilation required for Windows x64, Linux x64, and ARM64.

## Getting started

The pyorbbecsdk contains all the libraries that power your camera along with tools that let you experiment with its features and settings.

To get started:
- **Install the package** via PyPI (recommended) or from GitHub Release:
  ```bash
  pip install pyorbbecsdk2
  ```
- **Setup the environment** (one-time OS-level configuration for metadata and udev rules):
  ```bash
  # Windows (PowerShell — will auto-request Administrator)
  python scripts/env_setup/setup_env.py
  
  # Linux (will auto-request sudo)
  python3 scripts/env_setup/setup_env.py
  ```
- **Start experimenting** with the SDK's Quick Start code:

  ```python
  from pyorbbecsdk import *
  
  pipeline = Pipeline()
  pipeline.start()                        # uses default config from OrbbecSDKConfig.xml
  frames = pipeline.wait_for_frames(1000) # get synchronized Color + Depth frames
  ```

For full visualisation, check out [`examples/quick_start.py`](examples/quick_start.py). 
**Running result:**

![quick_start_result](docs/_images/quick_start_result.png)

## Samples

The [examples/](examples/) directory contains **35+ scripts** organized by difficulty to start using the pyorbbecsdk with only a few lines of code.

* [**Quick Start**](examples/quick_start.py) - Zero-config RGBD viewer — first thing to run.
* [**Beginner**](examples/beginner/) - Hello camera, depth viz, alignment, calibration, point cloud, multi-stream, IMU, network camera, and firmware update.
* [**Advanced**](examples/advanced/) - Recording & playback, device control, filter chains, HDR, presets, depth work modes, multi-device sync, coordinate transforms, high-performance pipeline.
* [**Applications**](examples/applications/) - YOLO object detection with depth overlay; interactive depth ruler.
* [**LiDAR**](examples/lidar_examples/) - LiDAR streaming, control, recording, and playback.

See [examples/README.md](examples/README.md) for the full list with per-script descriptions and device compatibility.

## Supported platforms

Here is the list of all supported operating systems for the pyorbbecsdk. Pre-built wheels are available for all of them.

| <div align="center"><img src="https://user-images.githubusercontent.com/32394882/230619282-fe2f84fb-2130-4164-a193-db2893b58272.png" width="40%" alt="Windows" /></div> | <div align="center"><img src="https://user-images.githubusercontent.com/32394882/230619268-bdf66472-8bf5-41e7-9efa-ca3698ff271a.png" width="40%" alt="Linux x64" /></div> | <div align="center"><img src="https://user-images.githubusercontent.com/32394882/230619273-feeee52b-209b-48da-b990-06630cabe323.png" width="40%" alt="Linux ARM" /></div> |
| :---: | :---: | :---: |
| **Windows (x64)** | **Linux (x64)** | **Linux (ARM64)** |
| Windows 10+ | Ubuntu 18.04 / 20.04 / 22.04 | Ubuntu 18.04 / 20.04 / 22.04 |

Supported Python versions: **Python 3.8 to 3.13**

## Automated Firmware Update

If you encounter errors related to firmware version mismatch, please use the automated update assistant:

```bash
python scripts/auto_update_firmware.py
```

This script will check your current device firmware version, guide you to download the correct firmware, and perform the firmware update safely.

## Community

Join the conversation and connect with other pyorbbecsdk users to share ideas, solve problems, and help make the SDK awesome. 

- **GitHub Issues** If you come across a bug or want to request a feature, please raise an issue in this [**GitHub repository**](https://github.com/orbbec/pyorbbecsdk/issues).
- **Documentation** The comprehensive [Orbbec SDK V2 Python Wrapper User Guide](https://orbbec.github.io/pyorbbecsdk/index.html) covers architecture, API quick-starts, and usage guides.
- **Contributing** Contributions are welcome — read [CONTRIBUTING.md](CONTRIBUTING.md) for build instructions, code style, and the PR process.

## License

This project is licensed under the [Apache License 2.0](LICENSE).

The bundled Orbbec SDK native libraries in `sdk/lib/` are proprietary binaries distributed by Orbbec. See [sdk/lib/README.md](sdk/lib/README.md) for details.
