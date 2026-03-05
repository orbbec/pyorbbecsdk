#!/bin/bash
# build_all_wheels.sh - Build wheel packages for Python 3.8-3.13
# This script builds wheels for all available Python versions

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
echo "  pyorbbecsdk Multi-Version Wheel Builder"
echo "=========================================="
echo ""

# Python versions to build for (version:python_path)
PYTHON_VERSIONS=(
    "3.8:$HOME/.pyenv/versions/3.8.20/bin/python3.8"
    "3.9:/opt/homebrew/bin/python3.9"
    "3.10:/opt/homebrew/bin/python3.10"
    "3.11:/opt/homebrew/bin/python3.11"
    "3.12:/opt/homebrew/bin/python3.12"
    "3.13:/opt/homebrew/bin/python3.13"
)

# Create dist directory
mkdir -p "$PROJECT_ROOT/dist"

# Build for each version
SUCCESS_COUNT=0
FAIL_COUNT=0

for entry in "${PYTHON_VERSIONS[@]}"; do
    ver="${entry%%:*}"
    py="${entry#*:}"

    # Check if Python exists
    if [ ! -f "$py" ]; then
        echo -e "${YELLOW}  [${ver}] Python not found, skipping${NC}"
        continue
    fi

    # Check if .so file exists for this version
    # Convert 3.8 -> 38, 3.9 -> 39, etc.
    ver_num="${ver//.}"
    SO_FILE=$(ls "$PROJECT_ROOT/install/lib"/pyorbbecsdk.cpython-${ver_num}-darwin.so 2>/dev/null)

    if [ -z "$SO_FILE" ]; then
        echo -e "${RED}  [${ver}] .so file not found in install/lib, skipping${NC}"
        continue
    fi

    echo -n "  [${ver}] Building wheel... "

    # Clean only build directory, keep dist
    rm -rf "$PROJECT_ROOT/build"

    # Build wheel using this Python version
    if "$py" setup.py bdist_wheel > /tmp/wheel_build_${ver}.log 2>&1; then
        # Find the generated wheel file (cp39, cp310, etc.)
        WHEEL=$(ls "$PROJECT_ROOT/dist"/pyorbbecsdk2-*cp${ver_num}*.whl 2>/dev/null | head -n1)
        if [ -n "$WHEEL" ]; then
            echo -e "${GREEN}✓ $(basename $WHEEL)${NC}"
            ((SUCCESS_COUNT++))
        else
            echo -e "${RED}✗ wheel not found${NC}"
            ((FAIL_COUNT++))
        fi
    else
        echo -e "${RED}✗ build failed${NC}"
        tail -3 /tmp/wheel_build_${ver}.log 2>/dev/null || true
        ((FAIL_COUNT++))
    fi
done

echo ""
echo "=========================================="
echo -e "${BLUE}  Build Summary${NC}"
echo "=========================================="
echo -e "Success: ${GREEN}$SUCCESS_COUNT${NC}"
echo -e "Failed:  ${RED}$FAIL_COUNT${NC}"
echo ""
echo "Generated wheel files:"
ls -lh "$PROJECT_ROOT/dist"/pyorbbecsdk2-*.whl 2>/dev/null || echo "No wheel files found"
echo "=========================================="