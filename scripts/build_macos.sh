#!/bin/bash
# build_macos.sh - Build pyorbbecsdk for macOS
# This script builds the Python bindings and prepares all required libraries

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

echo "=========================================="
echo "  pyorbbecsdk macOS Build Script"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python version
echo "Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
echo -e "${GREEN}Python version: $PYTHON_VERSION${NC}"

# Check if Python is 3.8+
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 8 ]); then
    echo -e "${RED}Error: Python 3.8+ is required${NC}"
    exit 1
fi

# Check for Xcode Command Line Tools
echo "Checking Xcode Command Line Tools..."
if ! xcode-select -v &> /dev/null; then
    echo -e "${YELLOW}Warning: Xcode Command Line Tools not found${NC}"
    echo "Install with: xcode-select --install"
fi

# Check for CMake
echo "Checking CMake..."
if ! command -v cmake &> /dev/null; then
    echo -e "${RED}Error: CMake is required${NC}"
    echo "Install with: brew install cmake"
    exit 1
fi
CMAKE_VERSION=$(cmake --version | head -n1)
echo -e "${GREEN}$CMAKE_VERSION${NC}"

# Create build directory
BUILD_DIR="$PROJECT_ROOT/build"
mkdir -p "$BUILD_DIR"
echo ""
echo "Build directory: $BUILD_DIR"

# Clean previous build
echo ""
echo "Cleaning previous build..."
rm -rf "$BUILD_DIR"/*
rm -rf "$PROJECT_ROOT/src/pyorbbecsdk"/*.so
rm -rf "$PROJECT_ROOT/src/pyorbbecsdk"/*.pyc
rm -rf "$PROJECT_ROOT/src/pyorbbecsdk"/__pycache__

# Build C extensions
echo ""
echo "Building C extensions..."
cd "$PROJECT_ROOT"
python3 setup.py build_ext --inplace

# Verify build
echo ""
echo "Verifying build..."
if [ -f "$PROJECT_ROOT/src/pyorbbecsdk/pyorbbecsdk.so" ] || [ -f "$PROJECT_ROOT/src/pyorbbecsdk"/*.cpython-*.so ]; then
    echo -e "${GREEN}Build successful!${NC}"
else
    echo -e "${RED}Build failed: No .so files found${NC}"
    exit 1
fi

# Copy libraries to sdk directory
echo ""
echo "Organizing libraries..."
SDK_LIB_DIR="$PROJECT_ROOT/sdk/lib/macOS"
mkdir -p "$SDK_LIB_DIR"

# Copy main SDK library
if [ -f "$PROJECT_ROOT/libOrbbecSDK.dylib" ]; then
    cp "$PROJECT_ROOT/libOrbbecSDK.dylib" "$SDK_LIB_DIR/"
    cp "$PROJECT_ROOT/libOrbbecSDK.2.dylib" "$SDK_LIB_DIR/" 2>/dev/null || true
    cp "$PROJECT_ROOT/libOrbbecSDK.2.7.6.dylib" "$SDK_LIB_DIR/" 2>/dev/null || true
    echo -e "${GREEN}SDK libraries copied to $SDK_LIB_DIR${NC}"
fi

# Copy extensions
if [ -d "$PROJECT_ROOT/extensions" ]; then
    mkdir -p "$SDK_LIB_DIR/extensions"
    cp -r "$PROJECT_ROOT/extensions"/* "$SDK_LIB_DIR/extensions/" 2>/dev/null || true
    echo -e "${GREEN}Extensions copied${NC}"
fi

# Set permissions
echo ""
echo "Setting permissions..."
find "$PROJECT_ROOT/src/pyorbbecsdk" -name "*.so" -exec chmod 755 {} \;
find "$SDK_LIB_DIR" -name "*.dylib" -exec chmod 755 {} \; 2>/dev/null || true

# Print build summary
echo ""
echo "=========================================="
echo "  Build Summary"
echo "=========================================="
echo "Python version: $PYTHON_VERSION"
echo "Build directory: $BUILD_DIR"
echo "Output: $PROJECT_ROOT/src/pyorbbecsdk/"
echo ""
echo "Next step: Run ./scripts/package_whl.sh to create wheel"
echo "=========================================="
