# ******************************************************************************
#  pyorbbecsdk Beginner Example 01 — Hello Camera
#
#  What you will learn:
#    1. How to discover connected Orbbec cameras
#    2. How to print device information (name, firmware, serial number)
#    3. How to list available sensors (Depth, Color, IR)
#    4. How to safely release resources when done
#
#  Prerequisites:
#    pip install pyorbbecsdk2
#    Connect an Orbbec camera via USB before running.
#
#  Run:
#    python examples/beginner/01_hello_camera.py
# ******************************************************************************

from pyorbbecsdk import Context, OBLogLevel

# ---------------------------------------------------------------------------
# Step 1: Create a Context
#   The Context is the entry point to the SDK. It manages device discovery
#   and global logging. One Context is usually enough for the entire program.
# ---------------------------------------------------------------------------
ctx = Context()

# Reduce log noise — set to OBLogLevel.DEBUG to see everything
ctx.set_logger_level(OBLogLevel.WARNING)

# ---------------------------------------------------------------------------
# Step 2: Find connected devices
#   query_devices() returns a DeviceList snapshot.
#   The list is valid until you call query_devices() again.
# ---------------------------------------------------------------------------
device_list = ctx.query_devices()

if device_list.get_count() == 0:
    print("ERROR: No Orbbec device found.")
    print("  - Check that the camera is plugged in via USB.")
    print("  - On Linux, ensure your user is in the 'plugdev' group:")
    print("      sudo usermod -aG plugdev $USER  (then log out and back in)")
    raise SystemExit(1)

print(f"Found {device_list.get_count()} device(s):\n")

# ---------------------------------------------------------------------------
# Step 3: Open each device and print its information
# ---------------------------------------------------------------------------
for i in range(device_list.get_count()):
    # get_device_by_index() opens the device exclusively.
    # Only one process should open a device at a time.
    device = device_list.get_device_by_index(i)

    info = device.get_device_info()
    print(f"  Device #{i + 1}")
    print(f"    Name           : {info.get_name()}")
    print(f"    Serial Number  : {info.get_serial_number()}")
    print(f"    Firmware       : {info.get_firmware_version()}")
    print(f"    Hardware       : {info.get_hardware_version()}")
    print(f"    USB PID / VID  : 0x{info.get_pid():04X} / 0x{info.get_vid():04X}")
    print(f"    Connection     : {info.get_connection_type()}")

    # Step 3b: List available sensors
    sensor_list = device.get_sensor_list()
    sensor_names = [
        str(sensor_list.get_sensor_by_index(j).get_type())
        for j in range(sensor_list.get_count())
    ]
    print(f"    Sensors        : {', '.join(sensor_names)}")
    print()

    # Step 3c: Read device temperature (useful for thermal monitoring)
    try:
        temp = device.get_temperature()
        print(f"    Temperature    : {temp}")
    except Exception:
        pass  # Not all devices support temperature reading

# ---------------------------------------------------------------------------
# Step 4: Resources are automatically released
#   Python's garbage collector frees the Device and Context when they go out
#   of scope. For explicit control, set them to None or use a context manager.
# ---------------------------------------------------------------------------
print("Done! Resources released automatically.")
