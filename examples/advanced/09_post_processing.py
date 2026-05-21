# ******************************************************************************
#  pyorbbecsdk Advanced Example 09 — Post-Processing Filter Stack
#
#  What you will learn:
#    1. Build a full post-processing pipeline (decimation, spatial, temporal, hole-fill)
#    2. Apply the filter chain to raw depth frames in real time
#    3. Display raw depth and filtered depth side by side for direct comparison
#    4. Tune individual filter parameters to balance quality and performance
#
#  Device requirement: Gemini 330 series
#
#  Run:
#    python examples/advanced/09_post_processing.py
# ******************************************************************************
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import sys
import time
from threading import Thread

import cv2
import numpy as np

from pyorbbecsdk import OBSensorType, OBFormat, OBStreamType  # type: ignore
from pyorbbecsdk import Config, Context, DisparityTransform, OBError, Pipeline

# Pixel formats that contain raw uncompressed 16-bit depth values.
_RAW_DEPTH_FORMATS = {OBFormat.Y16, OBFormat.Z16, OBFormat.Y12C4}


def _get_depth_array(depth_frame):
    """Return a (height, width) uint16 numpy array, or None if unsupported."""
    if depth_frame.get_format() not in _RAW_DEPTH_FORMATS:
        return None
    raw = np.frombuffer(depth_frame.get_data(), dtype=np.uint16)
    try:
        return raw.reshape(depth_frame.get_height(), depth_frame.get_width())
    except ValueError:
        return None

# --- Configuration Constants ---
ESC_KEY = 27
WINDOW_NAME = "PostProcessing (Left: Original, Right: Processed)"
MIN_DEPTH = 20  # Minimum depth value in mm
MAX_DEPTH = 10000  # Maximum depth value in mm

# Global control flag to synchronize program exit across threads
quit_program = False


def _has_config_schema_api(f):
    """Check whether get_config_schema_vec / get_config_value / set_config_value are available."""
    return hasattr(f, "get_config_schema_vec")


def print_filters_info(filters):
    """
    Print information about recommended filters, including their current status
    and configuration schema (parameters, ranges, and defaults).
    """
    print(f"{len(filters)} post processing filters recommended:")
    for filter in filters:
        status = "enabled" if filter.is_enabled() else "disabled"
        print(f" - {filter.get_name()}: {status}")
        if _has_config_schema_api(filter):
            config_schema_vec = filter.get_config_schema_vec()
            for config_schema in config_schema_vec:
                # Print detailed schema for each parameter of the filter
                print(
                    f" - {{{config_schema.name}, {config_schema.type}, {config_schema.min}, {config_schema.max}, {config_schema.step}, {config_schema.default}, {config_schema.desc}}}"
                )
        # Disable optional filters by default — user enables them via CLI.
        # Keep DisparityTransform and ThresholdFilter enabled: they form the
        # baseline pipeline that decompresses RLE-encoded depth frames and
        # clips values to a valid range. Without them the raw RLE data cannot
        # be interpreted as pixel values on Linux.
        if not filter.is_disparity_transform_filter() and not filter.is_threshold_filter():
            filter.enable(False)


def filter_control(filter_list):
    """
    CLI Control Thread: Allows users to interactively enable/disable filters
    and modify parameter values via the terminal while the video runs.
    """
    global quit_program

    def print_help():
        print("Available commands:")
        print("- Enter `[Filter]` to list the current config values for the filter")
        print("- Enter `[Filter] on` or `[Filter] off` to enable/disable the filter")
        print("- Enter `[Filter] list` to list the config schema for the filter")
        print("- Enter `[Filter] [Config]` to show the config values for the filter")
        print("- Enter `[Filter] [Config] [Value]` to set a config value")
        print("- Enter `L` or `l` to list all available filters")
        print("- Enter `H` or `h` to print this help message")
        print("- Enter `Q` or `q` to quit")

    print_help()

    while not quit_program:
        print("---------------------------")
        # Use strip() to clean up whitespace from user input
        try:
            user_input = input("Enter your input (h for help): ").strip()
        except EOFError:
            # stdin is not available (e.g., running non-interactively or
            # piped input). Wait for the main thread to signal quit.
            time.sleep(0.5)
            continue

        if not user_input:
            continue

        if user_input.lower() == "q":
            quit_program = True
            break
        elif user_input.lower() == "l":
            print_filters_info(filter_list)
            continue
        elif user_input.lower() == "h":
            print_help()
            continue

        # Split input into tokens for command parsing
        tokens = user_input.split()
        if not tokens:
            continue

        target_filter_name = tokens[0]
        found_filter = None

        # Search for the requested filter in the recommended list
        for f in filter_list:
            if f.get_name() == target_filter_name:
                found_filter = f
                break

        if found_filter:
            if not _has_config_schema_api(found_filter):
                # Only on/off toggle is available without config schema API
                if len(tokens) == 2 and tokens[1].lower() in ["on", "off"]:
                    is_on = tokens[1].lower() == "on"
                    found_filter.enable(is_on)
                    status = "enabled" if found_filter.is_enabled() else "disabled"
                    print(f"Success: Filter {found_filter.get_name()} is now {status}")
                elif len(tokens) == 1:
                    status = "enabled" if found_filter.is_enabled() else "disabled"
                    print(f" - {found_filter.get_name()}: {status} (config schema API not available)")
                else:
                    print(
                        f"Error: Config schema API not available for this build. Only on/off is supported.",
                        file=sys.stderr,
                    )
            # Case 1: [Filter] -> Show all current parameter values
            elif len(tokens) == 1:
                print(f"Config values for {found_filter.get_name()}:")
                schema_vec = found_filter.get_config_schema_vec()
                for schema in schema_vec:
                    val = found_filter.get_config_value(schema.name)
                    print(f" - {schema.name}: {val}")

            # Case 2: [Filter] on/off -> Toggle filter state
            elif len(tokens) == 2 and tokens[1].lower() in ["on", "off"]:
                is_on = tokens[1].lower() == "on"
                found_filter.enable(is_on)
                status = "enabled" if found_filter.is_enabled() else "disabled"
                print(f"Success: Filter {found_filter.get_name()} is now {status}")

            # Case 3: [Filter] list -> Show technical schema details
            elif len(tokens) == 2 and tokens[1].lower() == "list":
                print(f"Config schema for {found_filter.get_name()}:")
                schema_vec = found_filter.get_config_schema_vec()
                for s in schema_vec:
                    print(f" - {{{s.name}, {s.type}, {s.min}, {s.max}, {s.step}, {s.default}, {s.desc}}}")

            # Case 4: [Filter] [Config Name] -> Get specific parameter value
            elif len(tokens) == 2:
                schema_vec = found_filter.get_config_schema_vec()
                target_config = tokens[1]
                found_config = False
                for s in schema_vec:
                    if s.name == target_config:
                        val = found_filter.get_config_value(s.name)
                        print(f"Config values for {found_filter.get_name()}@{s.name}: {val}")
                        found_config = True
                        break
                if not found_config:
                    print(
                        f"Error: Config {target_config} not found for filter {target_filter_name}",
                        file=sys.stderr,
                    )

            # Case 5: [Filter] [Config Name] [Value] -> Set parameter value
            elif len(tokens) == 3:
                try:
                    config_name = tokens[1]
                    value = float(tokens[2])
                    found_filter.set_config_value(config_name, value)
                    print(
                        f"Success: Config value of {config_name} for filter {target_filter_name} is set to {tokens[2]}"
                    )
                except ValueError:
                    print(f"Error: '{tokens[2]}' is not a valid number", file=sys.stderr)
                except Exception as e:
                    print(f"Error: {e}", file=sys.stderr)
        else:
            print(f"Error: Filter {target_filter_name} not found", file=sys.stderr)

        # Brief sleep to prevent high CPU usage in the input loop
        time.sleep(0.5)


def main():
    global quit_program
    pipeline = None
    try:
        # Check if device is connected
        ctx = Context()
        device_list = ctx.query_devices()
        if device_list.get_count() == 0:
            print("Device Not Found! Please connect an Orbbec camera and try again.")
            return

        # Initialize the Orbbec pipeline and stream configuration
        pipeline = Pipeline()
        config = Config()

        # Access the depth sensor and retrieve device-recommended filters (Decimation, Hole-filling, etc.)
        device = pipeline.get_device()
        sensor = device.get_sensor(OBSensorType.DEPTH_SENSOR)
        filters = sensor.get_recommended_filters()

        # Separate the baseline filter (DisparityTransform) from optional filters.
        # DisparityTransform decompresses RLE-encoded depth into raw pixel data
        # and must always be applied. On Windows / uncompressed streams it is a
        # near-identity transform.
        disparity_filter = None
        optional_filters = []
        for f in filters:
            if f.is_disparity_transform_filter():
                disparity_filter = f
                f.enable(True)  # always on
            else:
                optional_filters.append(f)

        # Show initial filters information
        print_filters_info(filters)

        # Enable depth stream and start the pipeline
        config.enable_stream(OBStreamType.DEPTH_STREAM)
        pipeline.start(config)

        # Start the background control thread for terminal input (pass full list
        # so the user can toggle any filter, including DisparityTransform)
        control_thread = Thread(target=filter_control, args=(filters,))
        control_thread.daemon = True
        control_thread.start()

        print("Press 'ESC' on the window to exit.")

        # Create window once outside the loop
        cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
        window_initialized = False

        while not quit_program:
            # Wait for frameset from the pipeline
            frames = pipeline.wait_for_frames(1000)
            if frames is None:
                continue
            depth_frame = frames.get_depth_frame()
            if depth_frame is None:
                continue

            # Skip compressed frames — the filter chain requires
            # uncompressed pixel data (Y16 / Z16 / Y12C4).
            if depth_frame.get_format() not in _RAW_DEPTH_FORMATS:
                continue

            # ---- Pre-process: decompress RLE → raw depth (baseline) ----
            baseline_frame = disparity_filter.process(depth_frame)
            if baseline_frame is None:
                continue

            # ---- Apply optional filters on top of the baseline ----
            processed_frame = baseline_frame
            for f in optional_filters:
                if f.is_enabled():
                    processed_frame = f.process(processed_frame)

            if processed_frame is None:
                continue

            # --- Display Original (baseline after DisparityTransform) ---
            depth_data = _get_depth_array(baseline_frame)
            if depth_data is None:
                continue
            # Normalize 16-bit depth to 8-bit for visualization
            depth_image = cv2.normalize(depth_data, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
            depth_image = cv2.applyColorMap(depth_image, cv2.COLORMAP_JET)

            # --- Process Filtered Frame for Display ---
            processed_data = _get_depth_array(processed_frame)
            if processed_data is None:
                continue
            processed_image = cv2.normalize(processed_data, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
            processed_image = cv2.applyColorMap(processed_image, cv2.COLORMAP_JET)

            # --- Render Side-by-Side View ---
            combined_view = np.hstack((depth_image, processed_image))

            # Fix for macOS: ensure array is contiguous in memory before displaying
            # macOS OpenCV backend requires contiguous array to display correctly
            combined_view = np.ascontiguousarray(combined_view)

            # Initialize window size on first frame based on actual image dimensions
            if not window_initialized:
                height, width = combined_view.shape[:2]
                cv2.resizeWindow(WINDOW_NAME, width, height)
                window_initialized = True

            cv2.imshow(WINDOW_NAME, combined_view)

            # Listen for escape or quit keys in the UI window
            key = cv2.waitKey(1)
            if key in [ord("q"), ESC_KEY]:
                break

    except OBError as e:
        print(f"SDK Error: {e}")
    finally:
        # Cleanup: Signal threads to stop, stop the pipeline, and close windows
        quit_program = True
        if pipeline is not None:
            pipeline.stop()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
