# ******************************************************************************
#  pyorbbecsdk Beginner Example 01 — Hello Camera
#
#  What you will learn:
#    1. How to configure SDK logging (console level + optional log file)
#    2. How to discover connected Orbbec cameras
#    3. How to print device information (name, firmware, serial number)
#    4. How to enumerate default stream configurations for every sensor
#       (Depth, Color)
#    5. How to read the active depth preset and available preset list
#    6. How to safely release resources when done
#
#  Prerequisites:
#    pip install pyorbbecsdk2
#    Connect an Orbbec camera via USB before running.
#
#  Run:
#    python examples/beginner/01_hello_camera.py
# ******************************************************************************

from pyorbbecsdk import (  # type: ignore  # compiled extension; stubs in stubs/pyorbbecsdk.pyi
    Context,
    OBError,
    OBSensorType,
    Pipeline,
)

# ---------------------------------------------------------------------------
# Step 1: Create a Context
#   The Context is the entry point to the SDK. It manages device discovery.
#   One Context is usually enough for the entire program.
# ---------------------------------------------------------------------------
ctx = Context()

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
# Step 3: Open each device, print identity and enumerate default configs
# ---------------------------------------------------------------------------
for i in range(device_list.get_count()):
    # get_device_by_index() opens the device exclusively.
    # Only one process should open a device at a time.
    device = device_list.get_device_by_index(i)

    info = device.get_device_info()
    print(f"Device #{i + 1}")
    print(f"  Name           : {info.get_name()}")
    print(f"  Serial Number  : {info.get_serial_number()}")
    print(f"  Firmware       : {info.get_firmware_version()}")
    print(f"  Hardware       : {info.get_hardware_version()}")
    print(f"  USB PID / VID  : 0x{info.get_pid():04X} / 0x{info.get_vid():04X}")
    print(f"  Connection     : {info.get_connection_type()}")
    print()

    # ------------------------------------------------------------------
    # Step 3a: Default video stream configs (Depth, Color, IR)
    #   Pipeline.get_stream_profile_list(sensor_type) returns all
    #   supported profiles for a sensor.
    #   get_default_video_stream_profile() picks the recommended one.
    # ------------------------------------------------------------------
    pipeline = Pipeline(device)

    VIDEO_SENSORS = [
        (OBSensorType.DEPTH_SENSOR, "Depth"),
        (OBSensorType.COLOR_SENSOR, "Color"),
    ]

    print("  Default stream configurations:")
    for sensor_type, label in VIDEO_SENSORS:
        try:
            profiles = pipeline.get_stream_profile_list(sensor_type)
            p = profiles.get_default_video_stream_profile()
            print(
                f"    {label:<10} : {p.get_width()}x{p.get_height()} " f"@ {p.get_fps()} fps  format={p.get_format()}"
            )
        except OBError:
            pass  # sensor not present on this device

    # ------------------------------------------------------------------
    # Step 3b: Depth preset
    #   Presets bundle a named set of depth processing parameters
    #   (e.g. "Default", "Hand", "High Accuracy").
    #   get_current_preset_name() returns the active preset.
    #   get_available_preset_list() lists all presets on the device.
    # ------------------------------------------------------------------
    print()
    print("  Depth preset:")
    try:
        current = device.get_current_preset_name()
        print(f"    Active preset  : {current}")
        preset_list = device.get_available_preset_list()
        names = [preset_list[j] for j in range(len(preset_list))]
        print(f"    Available      : {', '.join(names)}")
    except OBError:
        print("    (preset not supported on this device)")

    print()

# ---------------------------------------------------------------------------
# Step 4: Resources are automatically released
#   Python's garbage collector frees the Device and Context when they go out
#   of scope. For explicit control, set them to None or use a context manager.
# ---------------------------------------------------------------------------
print("Done! Resources released automatically.")
