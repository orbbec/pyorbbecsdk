#!/bin/bash
# build_all_versions.sh - Build pyorbbecsdk for Python 3.8-3.13

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo "=========================================="
echo "  pyorbbecsdk Multi-Version Builder"
echo "=========================================="
echo ""

# Python versions and executables
PYTHON_VERSIONS=(
    "3.8:$HOME/.pyenv/versions/3.8.20/bin/python3.8"
    "3.9:/opt/homebrew/bin/python3.9"
    "3.10:/opt/homebrew/bin/python3.10"
    "3.11:/opt/homebrew/bin/python3.11"
    "3.12:/opt/homebrew/bin/python3.12"
    "3.13:/opt/homebrew/bin/python3.13"
)

# Check and install pybind11 for each version
echo -e "${BLUE}Step 1: Installing pybind11 for all Python versions${NC}"
for entry in "${PYTHON_VERSIONS[@]}"; do
    ver="${entry%%:*}"
    py="${entry#*:}"
    if [ ! -f "$py" ]; then
        echo -e "${RED}Python $ver not found at $py${NC}"
        continue
    fi
    echo -e "${YELLOW}Installing pybind11 for Python $ver...${NC}"
    $py -m pip install pybind11 2>&1 | tail -1 || {
        echo -e "${RED}Failed to install pybind11 for Python $ver${NC}"
        continue
    }
    echo -e "${GREEN}✓ pybind11 installed for Python $ver${NC}"
done

echo ""
echo -e "${BLUE}Step 2: Building for all Python versions${NC}"

# Clean previous builds
rm -rf "$PROJECT_ROOT/install/lib"/*.so 2>/dev/null || true

# Build for each version
for entry in "${PYTHON_VERSIONS[@]}"; do
    ver="${entry%%:*}"
    py="${entry#*:}"
    if [ ! -f "$py" ]; then
        echo -e "${RED}Skipping Python $ver (not found)${NC}"
        continue
    fi

    echo ""
    echo -e "${YELLOW}Building for Python $ver...${NC}"

    # Get pybind11 cmake directory
    PYBIND11_DIR=$($py -c "import pybind11; print(pybind11.get_cmake_dir())" 2>/dev/null)
    if [ -z "$PYBIND11_DIR" ]; then
        echo -e "${RED}✗ Could not find pybind11 cmake dir for Python $ver${NC}"
        continue
    fi

    BUILD_DIR="$PROJECT_ROOT/build/build_py${ver}"

    # Clean build directory
    rm -rf "$BUILD_DIR"
    mkdir -p "$BUILD_DIR"

    cd "$BUILD_DIR"

    # Configure with CMake - add pybind11_DIR
    cmake "$PROJECT_ROOT" \
        -DPython3_EXECUTABLE="$py" \
        -Dpybind11_DIR="$PYBIND11_DIR" \
        -DCMAKE_BUILD_TYPE=Release \
        -DCMAKE_INSTALL_PREFIX="$PROJECT_ROOT/install" \
        > /tmp/cmake_output_${ver}.log 2>&1 || {
        echo -e "${RED}✗ CMake configuration failed for Python $ver${NC}"
        cat /tmp/cmake_output_${ver}.log | tail -20
        cd "$PROJECT_ROOT"
        continue
    }

    # Build
    make -j$(sysctl -n hw.ncpu) > /tmp/make_output_${ver}.log 2>&1 || {
        echo -e "${RED}✗ Build failed for Python $ver${NC}"
        cat /tmp/make_output_${ver}.log | tail -10
        cd "$PROJECT_ROOT"
        continue
    }

    # Install
    make install > /tmp/install_output_${ver}.log 2>&1 || {
        echo -e "${RED}✗ Install failed for Python $ver${NC}"
        cd "$PROJECT_ROOT"
        continue
    }

    # Verify .so file
    SO_PATTERN="cpython-${ver//./}"
    SO_FILE=$(find "$PROJECT_ROOT/install/lib" -name "*${SO_PATTERN}*.so" 2>/dev/null | head -n1)
    if [ -n "$SO_FILE" ]; then
        echo -e "${GREEN}✓ Built successfully for Python $ver${NC}"
        echo "  Output: $(basename $SO_FILE)"
    else
        echo -e "${YELLOW}⚠ Python $ver: .so file not found${NC}"
    fi

    cd "$PROJECT_ROOT"
done

echo ""
echo -e "${BLUE}Step 3: Summary${NC}"
echo "=========================================="
echo "Built .so files:"
ls -la "$PROJECT_ROOT/install/lib/"*.so 2>/dev/null || echo "No .so files found"
echo "=========================================="