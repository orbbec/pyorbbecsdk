#!/bin/bash
# package_whl.sh - Create Python wheel for pyorbbecsdk macOS
# This script packages the built extension into a distributable wheel

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

echo "=========================================="
echo "  pyorbbecsdk macOS Wheel Packager"
echo "=========================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check if build exists
echo "Checking build artifacts..."
if [ ! -d "$PROJECT_ROOT/src/pyorbbecsdk" ]; then
    echo -e "${RED}Error: Source directory not found${NC}"
    echo "Run ./scripts/build_macos.sh first"
    exit 1
fi

# Check for .so files
SO_FILES=$(find "$PROJECT_ROOT/src/pyorbbecsdk" -name "*.so" 2>/dev/null | wc -l)
if [ "$SO_FILES" -eq 0 ]; then
    echo -e "${RED}Error: No .so files found${NC}"
    echo "Run ./scripts/build_macos.sh first"
    exit 1
fi
echo -e "${GREEN}Found $SO_FILES shared object file(s)${NC}"

# Install wheel package if needed
echo ""
echo "Checking wheel package..."
if ! python3 -m pip show wheel &> /dev/null; then
    echo "Installing wheel package..."
    python3 -m pip install wheel --user
fi

# Install setuptools if needed
if ! python3 -m pip show setuptools &> /dev/null; then
    echo "Installing setuptools..."
    python3 -m pip install setuptools --user
fi

# Clean dist directory
DIST_DIR="$PROJECT_ROOT/dist"
rm -rf "$DIST_DIR"
mkdir -p "$DIST_DIR"
echo ""
echo "Output directory: $DIST_DIR"

# Get version from setup.py
VERSION=$(grep -o "version='[^']*'" setup.py | cut -d"'" -f2)
if [ -z "$VERSION" ]; then
    VERSION=$(grep -o 'version="[^"]*"' setup.py | cut -d'"' -f2)
fi
echo "Version: $VERSION"

# Get Python version info
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
PYTHON_TAG="cp${PYTHON_VERSION//./}"
echo "Python tag: $PYTHON_TAG"

# Get macOS version
MACOS_VERSION=$(sw_vers -productVersion | cut -d'.' -f1,2)
MACOS_TAG=$(echo $MACOS_VERSION | tr '.' '_')
echo "macOS tag: $MACOS_TAG"

# Get architecture
ARCH=$(uname -m)
if [ "$ARCH" = "arm64" ]; then
    ARCH_TAG="arm64"
else
    ARCH_TAG="x86_64"
fi
echo "Architecture: $ARCH_TAG"

# Build wheel
echo ""
echo "Building wheel..."
cd "$PROJECT_ROOT"
python3 setup.py bdist_wheel

# Verify wheel was created
WHEEL_FILE=$(find "$DIST_DIR" -name "*.whl" | head -n1)
if [ -z "$WHEEL_FILE" ]; then
    echo -e "${RED}Error: Wheel file not created${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}Wheel created successfully!${NC}"
echo "File: $WHEEL_FILE"

# Verify wheel contents
echo ""
echo "Wheel contents:"
unzip -l "$WHEEL_FILE" | head -30

# Test wheel installation (optional)
echo ""
read -p "Test install wheel in virtual environment? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    TEST_VENV="$PROJECT_ROOT/test_venv"
    rm -rf "$TEST_VENV"
    python3 -m venv "$TEST_VENV"
    source "$TEST_VENV/bin/activate"
    pip install "$WHEEL_FILE"
    python -c "import pyorbbecsdk; print('Import successful!')"
    deactivate
    echo -e "${GREEN}Test passed!${NC}"
fi

# Print summary
echo ""
echo "=========================================="
echo "  Packaging Summary"
echo "=========================================="
echo "Wheel file: $WHEEL_FILE"
echo "Version: $VERSION"
echo "Python: $PYTHON_TAG"
echo "Platform: macosx_${MACOS_TAG}_${ARCH_TAG}"
echo ""
echo "To install: pip install $WHEEL_FILE"
echo "To upload: twine upload $WHEEL_FILE"
echo "=========================================="
