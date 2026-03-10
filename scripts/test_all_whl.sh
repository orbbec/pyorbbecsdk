#!/bin/bash
# test_all_whl.sh - Test wheel installation for Python 3.8-3.13

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
echo "  pyorbbecsdk Wheel Installation Test"
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

DIST_DIR="$PROJECT_ROOT/dist"
TEST_DIR="$PROJECT_ROOT/test_install"

echo -e "${BLUE}Testing wheel installation for all Python versions${NC}"
echo ""

for entry in "${PYTHON_VERSIONS[@]}"; do
    ver="${entry%%:*}"
    py="${entry#*:}"

    if [ ! -f "$py" ]; then
        echo -e "${RED}Skipping Python $ver (Python not found)${NC}"
        continue
    fi

    # Find the wheel for this version
    PY_TAG="cp${ver//./}"
    WHEEL=$(ls "$DIST_DIR/"*${PY_TAG}*.whl 2>/dev/null | head -n1)
    if [ -z "$WHEEL" ]; then
        echo -e "${RED}Skipping Python $ver (wheel not found)${NC}"
        continue
    fi

    echo -e "${YELLOW}Testing Python $ver...${NC}"
    echo "  Wheel: $(basename $WHEEL)"

    # Create test virtual environment
    VENV_DIR="$TEST_DIR/venv_py${ver}"
    rm -rf "$VENV_DIR"
    $py -m venv "$VENV_DIR" 2>/dev/null || {
        echo -e "${RED}  ✗ Failed to create venv for Python $ver${NC}"
        continue
    }

    # Activate and install
    source "$VENV_DIR/bin/activate"

    # Install the wheel
    pip install "$WHEEL" --quiet 2>/dev/null || {
        echo -e "${RED}  ✗ Failed to install wheel for Python $ver${NC}"
        deactivate
        continue
    }

    # Test import
    python -c "import pyorbbecsdk; print('  Version:', pyorbbecsdk.__version__ if hasattr(pyorbbecsdk, '__version__') else 'N/A')" 2>/dev/null || {
        # Try alternative import
        python -c "import pyorbbecsdk; print('  Module imported successfully')" 2>/dev/null || {
            echo -e "${RED}  ✗ Failed to import pyorbbecsdk for Python $ver${NC}"
            deactivate
            continue
        }
    }

    echo -e "${GREEN}  ✓ Python $ver: Installation and import successful${NC}"

    deactivate
done

echo ""
echo -e "${BLUE}Summary${NC}"
echo "=========================================="
echo "Test environments created in: $TEST_DIR"
echo "=========================================="