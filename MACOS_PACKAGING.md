# pyorbbecsdk macOS WHL Packaging Guide

This document describes the complete process for building and packaging pyorbbecsdk for macOS.

## Overview

The packaging process creates a Python wheel (.whl) file that includes:
- Python bindings for Orbbec SDK
- macOS dynamic libraries (.dylib)
- SDK configuration files
- Extension modules

## Prerequisites

- macOS 10.15 or later
- Python 3.8+ (tested with Python 3.11)
- Xcode Command Line Tools
- CMake 3.15+
- pip >= 20.0

## Directory Structure

```
pyorbbecsdk/
├── scripts/
│   ├── build_macos.sh          # Main build script
│   ├── package_whl.sh          # Wheel packaging script
│   └── cleanup.sh              # Cleanup build artifacts
├── tests/
│   ├── test_import.py          # Basic import test
│   ├── test_device.py          # Device enumeration test
│   └── test_capture.py         # Frame capture test
├── src/
│   ├── pyorbbecsdk/            # Python package source
│   └── libOrbbecSDK.dylib      # macOS SDK library
├── sdk/lib/macOS/              # SDK libraries for distribution
├── extensions/                 # Extension modules
├── setup.py                    # Python package setup
└── MACOS_PACKAGING.md          # This file
```

## Build Process

### Step 1: Clone and Prepare

```bash
git clone https://github.com/orbbec/pyorbbecsdk.git
cd pyorbbecsdk
git checkout macos
```

### Step 2: Run Build Script

```bash
chmod +x scripts/build_macos.sh
./scripts/build_macos.sh
```

This script will:
1. Check system requirements
2. Build C extensions
3. Copy required libraries
4. Generate configuration files

### Step 3: Package Wheel

```bash
chmod +x scripts/package_whl.sh
./scripts/package_whl.sh
```

Output: `dist/pyorbbecsdk-<version>-cp<py>-cp<py>-macosx_<arch>.whl`

### Step 4: Verify Package

```bash
pip install dist/pyorbbecsdk-*.whl
python -c "import pyorbbecsdk; print(pyorbbecsdk.__version__)"
```

## Testing

Run the test suite after installation:

```bash
python tests/test_import.py
python tests/test_device.py
```

## Troubleshooting

### Library Loading Issues

If you encounter errors loading libraries:

```bash
# Check library dependencies
otool -L $(python -c "import pyorbbecsdk; print(pyorbbecsdk.__file__)")

# Fix library paths if needed
install_name_tool -change ...
```

### Permission Errors

Ensure all libraries have correct permissions:

```bash
chmod 755 src/libOrbbecSDK.dylib
chmod 755 extensions/**/*.dylib
```

## Distribution

Upload to PyPI (requires twine):

```bash
pip install twine
twine upload dist/pyorbbecsdk-*.whl
```

## Version Management

Update version in:
- `setup.py` (version field)
- `src/pyorbbecsdk/__init__.py` (__version__)
- `OrbbecSDKVersion.cmake`

## Support

For issues, please open a GitHub issue at:
https://github.com/orbbec/pyorbbecsdk/issues
