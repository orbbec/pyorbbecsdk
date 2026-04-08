# Contributing to pyorbbecsdk

Thank you for your interest in contributing! Whether you're fixing a bug, adding a feature, improving documentation, or reporting an issue — all contributions are appreciated.

Please read this guide before submitting changes, and ensure you follow the [Code of Conduct](CODE_OF_CONDUCT.md).

---

## Table of Contents

- [Development Prerequisites](#development-prerequisites)
- [Getting the Source Code](#getting-the-source-code)
- [Building from Source](#building-from-source)
- [Environment Setup](#environment-setup)
- [Running the Test Suite](#running-the-test-suite)
- [Code Style](#code-style)
- [Submitting Changes](#submitting-changes)
- [Reporting Issues](#reporting-issues)

---

## Development Prerequisites

### Required Tools

| Tool | Minimum Version | Notes |
|------|----------------|-------|
| CMake | 3.15 | |
| Python | 3.8+ | 3.10 recommended for running the full test suite |
| pybind11 | 2.12.0 | Required for numpy 2.x compatibility. Install via pip: `pip install pybind11==2.12.0 pybind11-global==2.12.0` |
| C++ compiler | C++14-capable | See compiler requirements below |
| Git | any recent | |

### Compiler Requirements

- **Windows:** Visual Studio 2019 or newer (MSVC 14.x+)
- **Linux / macOS:** GCC 7+ or Clang 6+

### Runtime Dependencies

```bash
pip install --upgrade pyorbbecsdk2
```

For running the object detection example:
```bash
pip install onnxruntime
```

> **NumPy Compatibility Note:**
>
> The SDK has specific NumPy version requirements based on Python version:
> - **Python 3.8-3.11**: Use `numpy<2.0.0`
> - **Python 3.12+**: Use `numpy>=2.1.0`
>
> pybind11>=2.12.0 is required to support NumPy 2.x (needed for Python 3.12+).

---

## Getting the Source Code

1. **Fork** the repository on GitHub.

2. **Clone** your fork:

   ```bash
   git clone https://github.com/<your-username>/pyorbbecsdk.git
   cd pyorbbecsdk
   ```

3. **Add the upstream remote:**

   ```bash
   git remote add upstream https://github.com/orbbec/pyorbbecsdk.git
   ```

> **Branch note:** Development happens on `v2-main` (SDK v2.x). The `main` branch is the legacy v1.x branch. Always base your work on `v2-main`.

---

## Building from Source

We provide two ways to build from source:

1. **UV build (Recommended)** — Fast, reproducible builds with automatic Python version management
2. **Traditional CMake build** — Manual setup with pip and virtual environments

### Option 1: UV Build (Recommended)

UV is a fast Python package manager that provides 10-100x faster dependency resolution than pip, automatic Python version management, and unified build scripts across platforms.

#### Prerequisites for UV Build

- **uv**: Follow the [official uv installation guide](https://docs.astral.sh/uv/getting-started/installation/)
  ```bash
  # Linux/macOS
  curl -LsSf https://astral.sh/uv/install.sh | sh

  # Windows PowerShell
  powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```
- **CMake** 3.15+ and platform compiler (same as traditional build)

#### Quick UV Build

```bash
# Linux
chmod +x scripts/build_whl/build-whl-uv.sh
./scripts/build_whl/build-whl-uv.sh  # Build for Python 3.10 (default)
./scripts/build_whl/build-whl-uv.sh 3.11  # Build for Python 3.11
./scripts/build_whl/build-whl-uv.sh all   # Build all supported versions (3.8-3.13)

# macOS
chmod +x scripts/build_whl/build-whl-uv-macos.sh
./scripts/build_whl/build-whl-uv-macos.sh

# Windows PowerShell
.\scripts\build_whl\build-whl-uv.ps1
```

Wheels are output to `wheel/` directory.

> See [Build with UV](https://orbbec.github.io/pyorbbecsdk/source/4_Package/build_with_uv.html) for detailed instructions including offline builds, script options, and troubleshooting.

---

### Option 2: Traditional CMake Build

Building is a two-stage process: first CMake compiles the C++ pybind11 bindings, then Python packages the result into a wheel.

#### Stage 1: CMake Build

```bash
cmake -S . -B build -DPYBIND11_PYTHON_VERSION=3.12
cmake --build build --config Release
cmake --install build
```

After install, compiled `.pyd` / `.so` files and the Orbbec SDK native libraries are placed in `install/lib/`.

#### Stage 2: Python Wheel

```bash
python setup.py bdist_wheel
```

Output wheel: `dist/pyorbbecsdk2-2.1.0-*.whl`

#### Setting PYTHONPATH (required to run examples after source build)

```bash
# Linux / macOS
source env.sh

# Windows (PowerShell)
$env:PYTHONPATH = "$PWD\install\lib;$env:PYTHONPATH"

# Windows (cmd)
set PYTHONPATH=%CD%\install\lib;%PYTHONPATH%
```

---

## Environment Setup

The Orbbec SDK requires a one-time OS-level configuration before the camera can be opened. Connect your device, then run:

```bash
# Windows (PowerShell — will auto-request Administrator)
python scripts/env_setup/setup_env.py

# Linux (will auto-request sudo)
python3 scripts/env_setup/setup_env.py
```

The script auto-detects your OS and applies the correct configuration:
- **Windows** — registers UVC metadata in the registry (required for correct timestamps and frame sync)
- **Linux** — installs udev rules for USB device access

You can verify the setup with `--check` or remove it with `--uninstall`:

```bash
python scripts/env_setup/setup_env.py --check      # verify status
python scripts/env_setup/setup_env.py --uninstall   # remove configuration
```

> **Linux tip:** Also add yourself to the `plugdev` group (log out and back in after):
> ```bash
> sudo usermod -aG plugdev $USER
> ```

<details>
<summary><strong>Manual setup (if you prefer not to use the script)</strong></summary>

**Windows** — register frame metadata (run PowerShell as Administrator):
```powershell
cd scripts\env_setup
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\obsensor_metadata_win10.ps1 -op install_all
```

**Linux** — install udev rules:
```bash
cd scripts/env_setup
sudo chmod +x ./install_udev_rules.sh
sudo ./install_udev_rules.sh
sudo udevadm control --reload && sudo udevadm trigger
```

</details>

---

## Running the Test Suite

### Test Markers

| Marker | Meaning |
|--------|---------|
| `hardware` | Requires a physical Orbbec camera (auto-skipped if none connected) |
| `gemini335` | Requires a Gemini 335 specifically |
| `performance` | Long-running benchmarks (60+ seconds each) |

### Common Test Commands

```bash
# No camera needed (CI-safe)
python -m pytest test/ -m "not hardware" -v

# Core tests (device, controls, calibration) — ~2 min with camera
python -m pytest \
  test/test_gemini335_device.py \
  test/test_gemini335_controls.py \
  test/test_gemini335_calib.py \
  test/test_context.py \
  test/test_device.py -v

# Full Gemini 335 test suite (camera must be connected)
python -m pytest test/test_gemini335_*.py -v

# Skip long performance benchmarks
python -m pytest test/ -m "not performance" -v
```

### Generating HTML Reports

```bash
python test/generate_report.py --quick   # quick suite
python test/generate_report.py          # full suite (saved to reports/)
```

> **Known teardown behavior:** The Orbbec SDK may print `Fatal Python error: Aborted` after the test session ends. This is a known SDK threading cleanup issue and does **not** indicate test failures — all test results logged before this message are valid.

---

## Code Style

### C++ Code

C++ code uses **clang-format** with Google style (configured in `.clang-format`).

Format before committing:

```bash
clang-format -i src/pyorbbecsdk/*.cpp src/pyorbbecsdk/*.hpp
```

### Python Code

Python code follows **PEP 8** conventions.

When modifying the public API (adding or changing C++ binding signatures), update the type stubs in `stubs/pyorbbecsdk.pyi` to keep IDE autocompletion accurate.

---

## Submitting Changes

1. **Sync with upstream** before creating a branch:

   ```bash
   git fetch upstream
   git checkout -b my-feature upstream/v2-main
   ```

2. **Make your changes** following the code style guidelines above.

3. **Add or update tests** in the `test/` directory when adding new functionality.

4. **Run the test suite** (at minimum the non-hardware tests):

   ```bash
   python -m pytest test/ -m "not hardware" -v
   ```

5. **Open a Pull Request** against the `v2-main` branch of `orbbec/pyorbbecsdk`:
   - Fill in the [pull request template](PULL_REQUEST_TEMPLATE.md) completely.
   - Link related issues using `Fixes #NNN` or `Related to #NNN`.
   - If you changed the public API, confirm `stubs/pyorbbecsdk.pyi` is updated.

---

## Reporting Issues

Before opening an issue, please check:

- The existing [issues list](https://github.com/orbbec/pyorbbecsdk/issues) for duplicates.
- The [FAQ / Troubleshooting](https://orbbec.github.io/pyorbbecsdk/index.html) in the documentation.
- Your device firmware meets the minimum version in [README.md — Automated Firmware Update](../README.md#automated-firmware-update).
- On Linux: udev rules are installed.
- On Windows: metadata registration was completed.

Use the [bug report template](ISSUE_TEMPLATE/bug_report.md) when filing a new issue.
