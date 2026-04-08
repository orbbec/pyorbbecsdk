#!/usr/bin/env python3
"""
test_device.py - Device enumeration test for pyorbbecsdk on macOS

This test verifies that pyorbbecsdk can enumerate connected Orbbec devices.

Usage:
    python tests/test_device.py

Note: Requires an Orbbec camera to be connected for full testing.
"""

import platform
import sys


def test_context_creation():
    """Test creating a Context object"""
    print("=" * 50)
    print("Context Creation Test")
    print("=" * 50)

    try:
        import pyorbbecsdk

        ctx = pyorbbecsdk.Context()
        print(f"✓ Context created successfully")
        print(f"  Context object: {ctx}")

        return ctx
    except Exception as e:
        print(f"✗ Context creation failed: {e}")
        return None


def test_device_enumeration(ctx):
    """Test enumerating connected devices"""
    print()
    print("=" * 50)
    print("Device Enumeration Test")
    print("=" * 50)

    if ctx is None:
        print("✗ Skipped (no context)")
        return False, []

    try:
        devices = ctx.query_devices()
        device_count = devices.get_count() if devices else 0

        print(f"✓ Device query completed")
        print(f"  Devices found: {device_count}")

        if device_count == 0:
            print("  Note: No devices connected (this is OK for testing)")
            return True, []

        # List devices
        device_list = []
        for i in range(device_count):
            try:
                device = devices.get_device_by_index(i)
                device_list.append(device)
                # Get device info for name
                try:
                    device_info = device.get_device_info()
                    name = device_info.get_name()
                except:
                    name = "<no device info>"
                print(f"  Device {i + 1}: {name}")
            except Exception as e:
                print(f"  Device {i + 1}: <unknown> ({e})")

        return True, device_list
    except Exception as e:
        print(f"✗ Device enumeration failed: {e}")
        return False, []


def test_device_info(ctx, devices):
    """Test getting device information"""
    print()
    print("=" * 50)
    print("Device Information Test")
    print("=" * 50)

    if not devices:
        print("  Skipped (no devices)")
        return True

    try:
        device = devices[0] if isinstance(devices, list) else devices.get_device_by_index(0)
        device_info = device.get_device_info()

        # Try to get various device info
        info_tests = [
            ("Name", lambda: device_info.get_name()),
            ("Serial Number", lambda: device_info.get_serial_number()),
            ("Firmware Version", lambda: device_info.get_firmware_version()),
            ("USB Bandwidth", lambda: str(device.get_usb_bandwidth())),
        ]

        for name, getter in info_tests:
            try:
                value = getter()
                print(f"✓ {name}: {value}")
            except Exception as e:
                print(f"  {name}: <not available> ({type(e).__name__})")

        return True
    except Exception as e:
        print(f"✗ Device info test failed: {e}")
        return False


def test_sensor_enumeration(ctx, devices):
    """Test enumerating device sensors"""
    print()
    print("=" * 50)
    print("Sensor Enumeration Test")
    print("=" * 50)

    if not devices:
        print("  Skipped (no devices)")
        return True

    try:
        device = devices[0] if isinstance(devices, list) else devices.get_device_by_index(0)
        sensors = device.get_sensor_list()
        sensor_count = sensors.get_count() if sensors else 0

        print(f"✓ Sensor query completed")
        print(f"  Sensors found: {sensor_count}")

        if sensor_count == 0:
            print("  Note: No sensors found")
            return True

        # List sensors
        for i in range(sensor_count):
            try:
                sensor = sensors.get_sensor_by_index(i)
                sensor_type = sensor.get_type()
                print(f"  Sensor {i + 1}: {sensor_type}")
            except Exception as e:
                print(f"  Sensor {i + 1}: <unknown> ({e})")

        return True
    except Exception as e:
        print(f"✗ Sensor enumeration failed: {e}")
        return False


def test_cleanup(ctx):
    """Test proper cleanup"""
    print()
    print("=" * 50)
    print("Cleanup Test")
    print("=" * 50)

    try:
        if ctx:
            del ctx
        print("✓ Cleanup completed")
        return True
    except Exception as e:
        print(f"✗ Cleanup failed: {e}")
        return False


def main():
    """Run all tests"""
    print()
    print("╔" + "=" * 48 + "╗")
    print("║  pyorbbecsdk macOS Device Test Suite        ║")
    print("╚" + "=" * 48 + "╝")
    print()

    results = []

    # Test context creation
    ctx = test_context_creation()
    results.append(("Context Creation", ctx is not None))

    # Test device enumeration
    enum_success, devices = test_device_enumeration(ctx)
    results.append(("Device Enumeration", enum_success))

    # Test device info
    info_success = test_device_info(ctx, devices)
    results.append(("Device Information", info_success))

    # Test sensor enumeration
    sensor_success = test_sensor_enumeration(ctx, devices)
    results.append(("Sensor Enumeration", sensor_success))

    # Test cleanup
    cleanup_success = test_cleanup(ctx)
    results.append(("Cleanup", cleanup_success))

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
