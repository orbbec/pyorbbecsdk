#!/bin/bash
# package_macos_wheel.sh - Package pyorbbecsdk wheel for macOS using venv
# Usage: Activate your venv first, then run this script
#   source venv/bin/activate
#   ./scripts/package_macos_wheel.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

echo "=========================================="
echo "  pyorbbecsdk macOS Wheel Packaging"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running in a virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    echo -e "${YELLOW}Warning: No virtual environment detected!${NC}"
    echo "Please activate your venv first:"
    echo "  source venv/bin/activate"
    echo ""
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Use Python from virtual environment or system
if [ -n "$VIRTUAL_ENV" ]; then
    PYTHON_BIN="$VIRTUAL_ENV/bin/python"
    PIP_BIN="$VIRTUAL_ENV/bin/pip"
else
    PYTHON_BIN="python3"
    PIP_BIN="pip3"
fi

# Check Python exists
if [ ! -f "$PYTHON_BIN" ]; then
    echo -e "${RED}Error: Python not found at $PYTHON_BIN${NC}"
    exit 1
fi

# Get Python version
PYTHON_VERSION=$("$PYTHON_BIN" --version 2>&1 | cut -d' ' -f2)
echo -e "${GREEN}Using Python: $PYTHON_VERSION${NC}"
echo -e "Python path: $PYTHON_BIN"

# Check pybind11 is installed
echo ""
echo "Checking pybind11..."
if ! "$PYTHON_BIN" -c "import pybind11" 2>/dev/null; then
    echo -e "${YELLOW}pybind11 not found, installing...${NC}"
    "$PIP_BIN" install pybind11
fi
PYBIND11_VERSION=$("$PYTHON_BIN" -c "import pybind11; print(pybind11.__version__)")
echo -e "pybind11 version: $PYBIND11_VERSION"

# Check Xcode Command Line Tools
echo ""
echo "Checking Xcode Command Line Tools..."
if ! xcode-select -v &> /dev/null; then
    echo -e "${YELLOW}Warning: Xcode Command Line Tools not found${NC}"
    echo "Install with: xcode-select --install"
else
    echo -e "${GREEN}Xcode Command Line Tools: $(xcode-select -v)${NC}"
fi

# Check for required directories
echo ""
echo "Checking build environment..."
if [ ! -d "install/lib" ]; then
    echo -e "${RED}Error: install/lib directory not found${NC}"
    echo "Please run build first or ensure SDK libraries are in install/lib"
    exit 1
fi

if [ ! -d "extensions" ]; then
    echo -e "${RED}Error: extensions directory not found${NC}"
    exit 1
fi

echo -e "${GREEN}Build directories OK${NC}"

# Clean previous build
echo ""
echo "Cleaning previous build..."
rm -rf build/ dist/ *.egg-info

# Build wheel package
echo ""
echo "Building wheel package..."
"$PYTHON_BIN" setup.py bdist_wheel

# Verify wheel was created
WHEEL_FILE=$(ls -1 dist/*.whl 2>/dev/null | head -1)
if [ -z "$WHEEL_FILE" ]; then
    echo -e "${RED}Error: Wheel package not created${NC}"
    exit 1
fi

echo ""
echo "=========================================="
echo -e "${GREEN}  Build Successful!${NC}"
echo "=========================================="
echo ""
echo "Wheel file: $WHEEL_FILE"
echo ""

# Show wheel contents
echo "Wheel contents:"
unzip -l "$WHEEL_FILE" | grep -E "(pyorbbecsdk|extensions)" | head -20

echo ""
echo "To install locally:"
echo "  pip install $WHEEL_FILE --force-reinstall"
echo ""
echo "To upload to PyPI:"
echo "  twine upload dist/*.whl"
echo "=========================================="