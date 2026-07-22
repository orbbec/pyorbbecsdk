# ******************************************************************************
#  pyorbbecsdk Advanced Example 17 — Laser Interleave Mode
#
#  What you will learn:
#    1. Detect which connected devices support the laser interleave property
#    2. Enable laser interleave mode to reduce multi-camera IR interference
#    3. Configure interleave timing parameters for coordinated frame capture
#    4. Stream depth frames with interleave active and verify reduced crosstalk
#
#  Device requirement: Devices with laser interleave support
#
#  Run:
#    python examples/advanced/17_laser_interleave.py
# ******************************************************************************
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import sys
import threading

import cv2
import numpy as np
from utils import resize_to_fit

from pyorbbecsdk import OBFormat  # type: ignore
from pyorbbecsdk import (
    Config,
    Context,
    OBError,
    OBFrameAggregateOutputMode,
    OBFrameType,
    OBPropertyID,
    OBSensorType,
    Pipeline,
    SequenceIdFilter,
)

cached_frames = {"depth": None, "left_ir": None, "right_ir": None, "ir": None}

stream_sequence_id = {
    "depth": -1,  # -1 means all frames
    "left_ir": -1,
    "right_ir": -1,
    "ir": -1,
}

running = True

postDepthFilter = SequenceIdFilter()
postLeftInfraredFilter = SequenceIdFilter()
postRightInfraredFilter = SequenceIdFilter()


def setup_camera():
    # Initialize camera pipeline and configuration
    pipeline = Pipeline()
    config = Config()
    device = pipeline.get_device()

    # Check if device supports frame interleave
    if not device.isFrameInterleaveSupported():
        print("Current default device does not support frame interleave")
        print("Press any key to exit...")
        input("Press Enter to exit.")
        sys.exit(1)

    # Define video sensor types to enable
    video_sensor = [
        OBSensorType.DEPTH_SENSOR,
        OBSensorType.IR_SENSOR,
        OBSensorType.LEFT_IR_SENSOR,
        OBSensorType.RIGHT_IR_SENSOR,
    ]
    sensor_list = device.get_sensor_list()
    for sensor in range(len(sensor_list)):
        try:
            sensor_type = sensor_list[sensor].get_type()
            if sensor_type in video_sensor:
                config.enable_stream(sensor_type)
        except:
            continue

    # Configure frame aggregation mode
    config.set_frame_aggregate_output_mode(OBFrameAggregateOutputMode.FULL_FRAME_REQUIRE)

    # Load and enable frame interleave
    device.loadFrameInterleave("Laser On-Off")
    device.set_bool_property(OBPropertyID.OB_PROP_FRAME_INTERLEAVE_ENABLE_BOOL, True)

    try:
        pipeline.start(config)
    except OBError as e:
        print(f"Error: {e}")
        print("Please connect an Orbbec camera and try again.")
        sys.exit(1)
    return pipeline


def set_filter_value(frame):
    # Apply sequence ID filter to the frame
    global postDepthFilter
    global postLeftInfraredFilter
    global postRightInfraredFilter

    frame_type = frame.get_type()
    if frame_type == OBFrameType.DEPTH_FRAME:
        frame = postDepthFilter.process(frame)
    if frame_type == OBFrameType.LEFT_IR_FRAME:
        frame = postLeftInfraredFilter.process(frame)
    if frame_type == OBFrameType.RIGHT_IR_FRAME:
        frame = postRightInfraredFilter.process(frame)
    if frame_type == OBFrameType.IR_FRAME:
        frame = postLeftInfraredFilter.process(frame)

    return frame


def process_depth(frame):
    # Process depth frame and convert to color map
    frame = set_filter_value(frame)
    frame = frame if frame else cached_frames["depth"]
    cached_frames["depth"] = frame
    if not frame:
        return None
    try:
        depth_data = np.frombuffer(frame.get_data(), dtype=np.uint16)
        depth_data = depth_data.reshape(frame.get_height(), frame.get_width())
        depth_image = cv2.normalize(depth_data, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        return cv2.applyColorMap(depth_image, cv2.COLORMAP_JET)
    except ValueError:
        return None


def process_ir(frame):
    # Process IR frame and normalize
    if frame is None:
        return None

    ir_frame = set_filter_value(frame)
    ir_data = np.asanyarray(ir_frame.get_data())
    width = ir_frame.get_width()
    height = ir_frame.get_height()
    ir_format = ir_frame.get_format()

    if ir_format == OBFormat.Y8:
        ir_data = np.resize(ir_data, (height, width, 1))
        data_type = np.uint8
        image_dtype = cv2.CV_8UC1
        max_data = 255
    elif ir_format == OBFormat.MJPG:
        ir_data = cv2.imdecode(ir_data, cv2.IMREAD_UNCHANGED)
        data_type = np.uint8
        image_dtype = cv2.CV_8UC1
        max_data = 255
        if ir_data is None:
            print("decode mjpeg failed")
            return None
        ir_data = np.resize(ir_data, (height, width, 1))
    else:
        ir_data = np.frombuffer(ir_data, dtype=np.uint16)
        data_type = np.uint16
        image_dtype = cv2.CV_16UC1
        max_data = 255
        ir_data = np.resize(ir_data, (height, width, 1))

    cv2.normalize(ir_data, ir_data, 0, max_data, cv2.NORM_MINMAX, dtype=image_dtype)
    ir_data = ir_data.astype(data_type)
    return cv2.cvtColor(ir_data, cv2.COLOR_GRAY2RGB)


def create_display(frames, width=1280, height=720):
    # Create a composite display of all frames
    display = np.zeros((height, width, 3), dtype=np.uint8)
    h, w = height // 2, width // 2

    if "depth" in frames and frames["depth"] is not None:
        display[0:h, 0:w] = resize_to_fit(frames["depth"], w, h)

    if "ir" in frames and frames["ir"] is not None:
        display[0:h, w:] = resize_to_fit(frames["ir"], w, h)

    if "left_ir" in frames and frames["left_ir"] is not None:
        display[0:h, w:] = resize_to_fit(frames["left_ir"], w, h)

    if "right_ir" in frames and frames["right_ir"] is not None:
        display[h:, 0:w] = resize_to_fit(frames["right_ir"], w, h)

    return display


def input_command_handler():
    """Command line interface for sequence_id control"""
    global running
    global postDepthFilter
    global postLeftInfraredFilter
    global postRightInfraredFilter
    global stream_sequence_id

    print("\nAvailable commands:")
    print("  depth all/0/1       - Set sequence id for depth stream")
    print("  left_ir all/0/1     - Set sequence id for left IR stream or IR stream(Monocular camera)")
    print("  right_ir all/0/1    - Set sequence id for right IR stream")
    print("  q                   - Quit program")

    while running:
        try:
            cmd = input("\nEnter command>> ").strip().lower()
            if not cmd:
                continue

            parts = cmd.split()
            if cmd in ("q", "quit"):
                running = False
                return False

            elif len(parts) == 2:
                stream_name, param = parts

                filter_map = {
                    "depth": postDepthFilter,
                    "left_ir": postLeftInfraredFilter,
                    "right_ir": postRightInfraredFilter,
                }

                if stream_name not in filter_map:
                    print("Invalid stream name, please use depth, left_ir or right_ir")
                    continue

                if param == "all":
                    seq_id = -1
                elif param == "0":
                    seq_id = 0
                elif param == "1":
                    seq_id = 1
                else:
                    print("Invalid parameter, please use all, 0 or 1")
                    continue

                try:
                    filter_map[stream_name].select_sequence_id(seq_id)
                    print(f"Successfully set {stream_name} sequence id to {seq_id}")
                except Exception as e:
                    print(f"Failed to set sequence id: {e}")

            else:
                print("Invalid command, type 'status' for help")

        except Exception as e:
            print(f"Command processing error: {e}")

    return True


def main():
    global running
    global postDepthFilter
    global postLeftInfraredFilter
    global postRightInfraredFilter

    # Check if device is connected
    ctx = Context()
    device_list = ctx.query_devices()
    if device_list.get_count() == 0:
        print("Device Not Found! Please connect an Orbbec camera and try again.")
        return

    WINDOW_NAME = "Viewer"
    DISPLAY_WIDTH = 1280
    DISPLAY_HEIGHT = 720

    pipeline = setup_camera()

    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(WINDOW_NAME, DISPLAY_WIDTH, DISPLAY_HEIGHT)

    # Initialize filters to accept all frames
    postDepthFilter.select_sequence_id(-1)
    postLeftInfraredFilter.select_sequence_id(-1)
    postRightInfraredFilter.select_sequence_id(-1)

    # Start command input thread
    input_thread = threading.Thread(target=input_command_handler)
    input_thread.daemon = True
    input_thread.start()

    while running:
        frames = pipeline.wait_for_frames(1000)
        if frames is None:
            continue

        depth = process_depth(frames.get_depth_frame())
        processed_frames = {"depth": depth}

        # Try to get separate left/right IR frames
        left = frames.get_left_ir_frame()
        right = frames.get_right_ir_frame()

        if left and right:
            processed_frames["left_ir"] = process_ir(left)
            processed_frames["right_ir"] = process_ir(right)
        else:
            # Fall back to monocular IR frame if separate frames not available
            ir = frames.get_ir_frame()
            if ir:
                processed_frames["ir"] = process_ir(ir)

        display = create_display(processed_frames, DISPLAY_WIDTH, DISPLAY_HEIGHT)
        cv2.imshow(WINDOW_NAME, display)

        key = cv2.waitKey(1)
        if key in [ord("q"), 27]:  # Exit on 'q' or ESC
            break

    cv2.destroyAllWindows()
    pipeline.stop()


if __name__ == "__main__":
    main()
