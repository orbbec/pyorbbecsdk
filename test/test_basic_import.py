#!/usr/bin/env python3
"""
test_import.py - Basic import test for pyorbbecsdk on macOS

This test verifies that the pyorbbecsdk module can be imported successfully
and that all required libraries are loaded correctly.

Usage:
    python tests/test_import.py
"""

import platform
import sys


def test_platform():
    """Verify we're running on macOS"""
    print("=" * 50)
    print("Platform Information")
    print("=" * 50)
    print(f"System: {platform.system()}")
    print(f"Release: {platform.release()}")
    print(f"Version: {platform.version()}")
    print(f"Machine: {platform.machine()}")
    print(f"Python: {platform.python_version()}")
    print(f"Python Implementation: {platform.python_implementation()}")
    print()

    assert platform.system() == "Darwin", "This test is designed for macOS"
    return True


def test_import():
    """Test basic import of pyorbbecsdk"""
    print("=" * 50)
    print("Import Test")
    print("=" * 50)

    try:
        import pyorbbecsdk

        print(f"✓ pyorbbecsdk imported successfully")
        print(f"  Module location: {pyorbbecsdk.__file__}")

        if hasattr(pyorbbecsdk, "__version__"):
            print(f"  Version: {pyorbbecsdk.__version__}")

        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False


def test_module_attributes():
    """Test that expected module attributes exist"""
    print()
    print("=" * 50)
    print("Module Attributes Test")
    print("=" * 50)

    try:
        import pyorbbecsdk

        expected_attrs = [
            "Context",
            "Device",
            "Pipeline",
            "Config",
            "FrameSet",
            "Frame",
            "StreamProfile",
            "StreamProfileList",
        ]

        missing = []
        for attr in expected_attrs:
            if hasattr(pyorbbecsdk, attr):
                print(f"✓ {attr}")
            else:
                print(f"✗ {attr} (missing)")
                missing.append(attr)

        if missing:
            print(f"\nWarning: Missing attributes: {', '.join(missing)}")
            return False

        return True
    except Exception as e:
        print(f"✗ Error checking attributes: {e}")
        return False


def test_library_loading():
    """Test that native libraries are loaded correctly"""
    print()
    print("=" * 50)
    print("Library Loading Test")
    print("=" * 50)

    try:
        import ctypes

        import pyorbbecsdk

        # Try to get the module file path
        module_file = pyorbbecsdk.__file__
        print(f"✓ Module file: {module_file}")

        # Check if it's a shared library
        if module_file.endswith(".so") or module_file.endswith(".dylib"):
            print(f"✓ Native extension detected")
        else:
            print(f"  Note: Module is not a direct shared library")

        return True
    except Exception as e:
        print(f"✗ Library loading test failed: {e}")
        return False


def main():
    """Run all tests"""
    print()
    print("╔" + "=" * 48 + "╗")
    print("║  pyorbbecsdk macOS Import Test Suite        ║")
    print("╚" + "=" * 48 + "╝")
    print()

    results = []

    # Run tests
    results.append(("Platform", test_platform()))
    results.append(("Import", test_import()))
    results.append(("Attributes", test_module_attributes()))
    results.append(("Library Loading", test_library_loading()))

    # Summary
    print()
    print("=" * 50)
    print("Test Summary")
    print("=" * 50)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")

    print()
    print(f"Total: {passed}/{total} tests passed")

    if passed == total:
        print("\n✓ All tests passed!")
        return 0
    else:
        print(f"\n✗ {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
