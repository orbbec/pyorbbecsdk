#!/bin/bash
# package_all_whl.sh - Create wheels for Python 3.8-3.13

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
echo "  pyorbbecsdk Multi-Version Wheel Packager"
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

# Clean dist directory
DIST_DIR="$PROJECT_ROOT/dist"
rm -rf "$DIST_DIR"
mkdir -p "$DIST_DIR"

echo -e "${BLUE}Building wheels for all Python versions${NC}"
echo ""

for entry in "${PYTHON_VERSIONS[@]}"; do
    ver="${entry%%:*}"
    py="${entry#*:}"

    if [ ! -f "$py" ]; then
        echo -e "${RED}Skipping Python $ver (not found)${NC}"
        continue
    fi

    # Check if .so file exists
    SO_PATTERN="cpython-${ver//./}"
    SO_FILE=$(find "$PROJECT_ROOT/install/lib" -name "*${SO_PATTERN}*.so" 2>/dev/null | head -n1)
    if [ -z "$SO_FILE" ]; then
        echo -e "${RED}Skipping Python $ver (.so file not found)${NC}"
        continue
    fi

    echo -e "${YELLOW}Building wheel for Python $ver...${NC}"

    # Create a temporary build directory
    TMP_DIR="$PROJECT_ROOT/build/whl_py${ver}"
    rm -rf "$TMP_DIR"
    mkdir -p "$TMP_DIR"

    # Create temporary install/lib with only the correct .so file
    TMP_LIB="$TMP_DIR/install/lib"
    mkdir -p "$TMP_LIB"

    # Copy the specific .so file
    cp "$SO_FILE" "$TMP_LIB/"

    # Copy dylib files
    cp "$PROJECT_ROOT/install/lib/"*.dylib "$TMP_LIB/" 2>/dev/null || true

    # Create temporary src directory with __init__.py
    TMP_SRC="$TMP_DIR/src/pyorbbecsdk"
    mkdir -p "$TMP_SRC"

    # Copy Python source files
    if [ -d "$PROJECT_ROOT/src/pyorbbecsdk" ]; then
        cp "$PROJECT_ROOT/src/pyorbbecsdk/"*.py "$TMP_SRC/" 2>/dev/null || true
    fi

    # Copy setup.py and other necessary files
    cp "$PROJECT_ROOT/setup.py" "$TMP_DIR/"
    cp "$PROJECT_ROOT/README.md" "$TMP_DIR/" 2>/dev/null || true

    # Build wheel from temp directory
    cd "$TMP_DIR"

    # Install wheel if needed
    $py -m pip install wheel --quiet 2>/dev/null || true

    # Build the wheel
    $py setup.py bdist_wheel 2>&1 | grep -v "running\|reading\|writing\|creating\|copying\|adding" || true

    # Copy wheel to main dist directory
    if ls "$TMP_DIR/dist/"*.whl 1> /dev/null 2>&1; then
        cp "$TMP_DIR/dist/"*.whl "$DIST_DIR/"
        WHEEL_NAME=$(ls "$DIST_DIR/"*cp${ver//./}*.whl 2>/dev/null | head -n1 | xargs basename)
        echo -e "${GREEN}✓ Wheel created for Python $ver: $WHEEL_NAME${NC}"
    else
        echo -e "${RED}✗ Failed to create wheel for Python $ver${NC}"
    fi

    cd "$PROJECT_ROOT"
done

echo ""
echo -e "${BLUE}Summary${NC}"
echo "=========================================="
echo "Wheels created in $DIST_DIR:"
ls -la "$DIST_DIR/"*.whl 2>/dev/null || echo "No wheels found"
echo "=========================================="