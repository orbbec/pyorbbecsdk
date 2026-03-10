#!/bin/bash
# macOS USB Access Solution for pyorbbecsdk
#
# On macOS, libusb requires either:
# 1. Root privilege (sudo) - or -
# 2. Valid code signing with com.apple.vm.device-access entitlement
#
# Since ad-hoc signing doesn't work for privileged entitlements,
# this script creates a wrapper that runs Python with sudo when needed.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$(dirname "$SCRIPT_DIR"))"

echo "=== macOS USB Device Access Setup ==="
echo ""
echo "On macOS, accessing USB devices requires elevated privileges."
echo ""
echo "Option 1: Run with sudo (recommended, works immediately)"
echo "  sudo python examples/multi_streams.py"
echo ""
echo "Option 2: Create an alias for convenience"
echo "  Add to your ~/.zshrc:"
echo "  alias spython='sudo python'"
echo "  Then use: spython examples/multi_streams.py"
echo ""
echo "Option 3: For development without sudo, you need:"
echo "  - Apple Developer ID certificate"
echo "  - Sign your app bundle with the entitlements"
echo "  - This is complex and not practical for scripts"
echo ""
echo "=========================================="
echo ""
echo "Quick solution: Run your command with sudo"
echo ""
echo "Example:"
echo "  cd $PROJECT_DIR"
echo "  source venv-py310/bin/activate"
echo "  sudo python examples/multi_streams.py"
echo ""