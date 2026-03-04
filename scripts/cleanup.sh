#!/bin/bash
# cleanup.sh - Clean build artifacts and temporary files
# Use this to reset the build environment

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

echo "=========================================="
echo "  pyorbbecsdk Cleanup Script"
echo "=========================================="
echo ""

# Colors
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m'

# Ask for confirmation
echo -e "${YELLOW}This will remove all build artifacts and temporary files.${NC}"
read -p "Continue? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cleanup cancelled."
    exit 0
fi

# Remove build directories
echo "Removing build directories..."
rm -rf "$PROJECT_ROOT/build"
rm -rf "$PROJECT_ROOT/dist"
rm -rf "$PROJECT_ROOT/*.egg-info"
rm -rf "$PROJECT_ROOT/src/*.egg-info"

# Remove compiled Python files
echo "Removing Python cache..."
find "$PROJECT_ROOT" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find "$PROJECT_ROOT" -type f -name "*.pyc" -delete 2>/dev/null || true
find "$PROJECT_ROOT" -type f -name "*.pyo" -delete 2>/dev/null || true

# Remove shared object files
echo "Removing compiled extensions..."
find "$PROJECT_ROOT/src" -type f -name "*.so" -delete 2>/dev/null || true
find "$PROJECT_ROOT" -type f -name "*.dylib" -delete 2>/dev/null || true

# Remove test virtual environment
echo "Removing test environments..."
rm -rf "$PROJECT_ROOT/test_venv"
rm -rf "$PROJECT_ROOT/.venv"

# Remove macOS specific files
echo "Removing macOS artifacts..."
rm -f "$PROJECT_ROOT/.DS_Store"
rm -rf "$PROJECT_ROOT/Log"

# Keep sdk directory but clean build artifacts
if [ -d "$PROJECT_ROOT/sdk/lib/macOS" ]; then
    echo "Keeping SDK library directory..."
fi

echo ""
echo -e "${GREEN}Cleanup complete!${NC}"
echo ""
echo "To rebuild, run: ./scripts/build_macos.sh"
