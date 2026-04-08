# ******************************************************************************
#  pyorbbecsdk Advanced Example 02 — Bag File Playback
#
#  What you will learn:
#    1. How to open a recorded .bag file with PlaybackDevice
#    2. How to retrieve and display all recorded streams (color, depth, IR, IMU)
#    3. How to monitor OBPlaybackStatus and auto-loop when the file ends
#    4. How to display a dynamic multi-stream grid from the recorded data
#
#  Keyboard: Q/ESC to quit
#
#  Device requirement: All
#
#  Run:
#    python examples/advanced/02_playback.py
# ******************************************************************************
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import threading
import time

import cv2
import numpy as np
from utils import frame_to_bgr_image

import pyorbbecsdk as ob
from pyorbbecsdk import OBFrameType  # type: ignore
from pyorbbecsdk import (
    Config,
    OBFormat,
    OBPlaybackStatus,
    OBSensorType,
    Pipeline,
    PlaybackDevice,
)


# Global state to share data between the processing callback and the UI thread
class GlobalState:
    def __init__(self):
        self.frame_mutex = threading.Lock()
        self.status_mutex = threading.Lock()
        self.stop_rendering = False
        self.exited = False
        self.playback_status = None
        self.enabled_sensor_types = []
        # cached frames for better visualization
        self.cached_frames = {
            "color": None,
            "depth": None,
            "left_ir": None,
            "right_ir": None,
            "ir": None,
            "confidence": None,
            "left_color": None,
            "right_color": None,
            "accel": None,
            "gyro": None,
        }


state = GlobalState()
pipeline = None
config = None
playback = None


def setup_camera(playback_device):
    """Setup camera and stream configuration"""
    global pipeline, config
    pipeline = Pipeline(playback_device)
    config = Config()
    device = pipeline.get_device()

    # Try to enable all possible sensors
    sensors = [
        OBSensorType.COLOR_SENSOR,
        OBSensorType.DEPTH_SENSOR,
        OBSensorType.IR_SENSOR,
        OBSensorType.LEFT_IR_SENSOR,
        OBSensorType.RIGHT_IR_SENSOR,
        OBSensorType.CONFIDENCE_SENSOR,
        OBSensorType.LEFT_COLOR_SENSOR,
        OBSensorType.RIGHT_COLOR_SENSOR,
        OBSensorType.ACCEL_SENSOR,
        OBSensorType.GYRO_SENSOR,
    ]

    sensor_list = playback_device.get_sensor_list()
    for sensor in range(len(sensor_list)):
        try:
            sensor_type = sensor_list[sensor].get_type()
            if sensor_type in sensors:
                config.enable_stream(sensor_type)
                state.enabled_sensor_types.append(sensor_type)
        except:
            continue

    # Set frame aggregate output mode if available - reduces latency
    try:
        config.set_frame_aggregate_output_mode(ob.OBFrameAggregateOutputMode.OB_FRAME_AGGREGATE_OUTPUT_ANY_SITUATION)
    except AttributeError:
        # OBFrameAggregateOutputMode not available in this SDK version
        pass

    return pipeline, config


def process_color(frame):
    """Process color image"""
    if frame is None:
        return None
    return frame_to_bgr_image(frame)


def process_depth(frame):
    """Process depth image"""
    if frame is None:
        return None
    try:
        depth_data = np.frombuffer(frame.get_data(), dtype=np.uint16)
        depth_data = depth_data.reshape(frame.get_height(), frame.get_width())
        depth_image = cv2.normalize(depth_data, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        return cv2.applyColorMap(depth_image, cv2.COLORMAP_JET)
    except ValueError:
        return None


def process_ir(ir_frame):
    """Process IR frame (left, right, or mono) to RGB image"""
    if ir_frame is None:
        return None
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


def process_confidence(frame):
    """Process confidence image"""
    if frame is None:
        return None
    try:
        confidence_data = np.frombuffer(frame.get_data(), dtype=np.uint8)
        confidence_data = confidence_data.reshape(frame.get_height(), frame.get_width())
        confidence_image = cv2.normalize(confidence_data, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        return cv2.cvtColor(confidence_image, cv2.COLOR_GRAY2RGB)
    except ValueError:
        return None


def create_single_imu_panel(imu_frame, title, w=480, h=240):
    """Create a panel displaying IMU data - pre-render to reduce UI overhead"""
    p = np.zeros((h, w, 3), dtype=np.uint8)
    if not imu_frame:
        return p

    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.6
    thickness = 1
    color = (255, 255, 255)

    unit = "rad/s" if title == "GYRO" else "m/s^2"
    lines = [
        f"{title}:",
        f" Time: {imu_frame.get_timestamp_us()}us",
        f" X: {imu_frame.get_x():.6f}{unit}",
        f" Y: {imu_frame.get_y():.6f}{unit}",
        f" Z: {imu_frame.get_z():.6f}{unit}",
    ]

    line_height = 30
    total_height = len(lines) * line_height
    start_y = (h - total_height) // 2

    for i, line in enumerate(lines):
        text_size = cv2.getTextSize(line, font, font_scale, thickness)[0]
        text_x = (w - text_size[0]) // 2
        text_y = start_y + i * line_height + text_size[1]
        cv2.putText(p, line, (text_x, text_y), font, font_scale, color, thickness, cv2.LINE_AA)
    return p


def video_frame_callback(frames):
    """Callback function triggered when a new FrameSet arrives - async processing"""
    if frames is None:
        return
    with state.frame_mutex:
        # Process color image
        color_frame = frames.get_color_frame()
        if color_frame:
            state.cached_frames["color"] = process_color(color_frame)

        # Process depth image
        depth_frame = frames.get_depth_frame()
        if depth_frame:
            state.cached_frames["depth"] = process_depth(depth_frame)

        # Process left IR
        left_ir = frames.get_left_ir_frame()
        if left_ir:
            state.cached_frames["left_ir"] = process_ir(left_ir)

        # Process right IR
        right_ir = frames.get_right_ir_frame()
        if right_ir:
            state.cached_frames["right_ir"] = process_ir(right_ir)

        # Process mono IR
        ir_frame = frames.get_ir_frame()
        if ir_frame:
            state.cached_frames["ir"] = process_ir(ir_frame)

        # Process confidence
        confidence = frames.get_confidence_frame()
        if confidence:
            try:
                state.cached_frames["confidence"] = process_confidence(confidence)
            except:
                pass

        # Process left color
        left_color = frames.get_left_color_frame()
        if left_color:
            try:
                state.cached_frames["left_color"] = process_color(left_color)
            except:
                pass

        # Process right color
        right_color = frames.get_right_color_frame()
        if right_color:
            try:
                state.cached_frames["right_color"] = process_color(right_color)
            except:
                pass

        # Process IMU data - pre-render as images
        accel = frames.get_accel_frame()
        if accel:
            state.cached_frames["accel"] = create_single_imu_panel(accel, "ACCEL")

        gyro = frames.get_gyro_frame()
        if gyro:
            state.cached_frames["gyro"] = create_single_imu_panel(gyro, "GYRO")


def on_playback_status_change(status):
    """Callback for playback status changes"""
    with state.status_mutex:
        state.playback_status = status
    print(f"[Callback] Playback status changed: {status}")


def replay_monitor():
    """Monitor playback status and auto-replay when stopped"""
    global pipeline, config
    while not state.exited:
        with state.status_mutex:
            status = state.playback_status

        if status == OBPlaybackStatus.STOPPED:
            print("Replay again")
            try:
                pipeline.stop()
            except:
                pass
            time.sleep(1.0)

            if state.exited:
                break

            # Clear frames cache for fresh start
            with state.frame_mutex:
                for key in state.cached_frames:
                    state.cached_frames[key] = None

            with state.status_mutex:
                state.playback_status = None

            try:
                pipeline.start(config, video_frame_callback)
            except Exception as e:
                print(f"Failed to restart playback: {e}")
        else:
            time.sleep(0.1)


def create_display(width=1280, height=720):
    """Create display window with correct dynamic layout"""
    sensor_type_to_name = {
        OBSensorType.COLOR_SENSOR: "color",
        OBSensorType.DEPTH_SENSOR: "depth",
        OBSensorType.LEFT_IR_SENSOR: "left_ir",
        OBSensorType.RIGHT_IR_SENSOR: "right_ir",
        OBSensorType.IR_SENSOR: "ir",
        OBSensorType.CONFIDENCE_SENSOR: "confidence",
        OBSensorType.LEFT_COLOR_SENSOR: "left_color",
        OBSensorType.RIGHT_COLOR_SENSOR: "right_color",
    }

    with state.frame_mutex:
        # Get enabled video keys based on sensor types
        video_keys = []
        for sensor_type in state.enabled_sensor_types:
            if sensor_type in sensor_type_to_name:
                video_keys.append(sensor_type_to_name[sensor_type])

        # Get video frames
        video_frames = []
        for k in video_keys:
            img = state.cached_frames.get(k)
            if img is not None:
                video_frames.append(img)

        # Get IMU panels (already pre-rendered)
        imu_frames = {}
        for key in ["accel", "gyro"]:
            img = state.cached_frames.get(key)
            if img is not None:
                imu_frames[key] = img

    num_videos = len(video_frames)
    total_elements = num_videos + len(imu_frames)

    if total_elements == 0:
        return np.zeros((height, width, 3), dtype=np.uint8)

    if total_elements == 1:
        grid_cols, grid_rows = 1, 1
    elif total_elements <= 2:
        grid_cols, grid_rows = 2, 1
    elif total_elements <= 4:
        grid_cols, grid_rows = 2, 2
    elif total_elements <= 6:
        grid_cols, grid_rows = 3, 2
    elif total_elements <= 9:
        grid_cols, grid_rows = 3, 3
    else:
        grid_cols, grid_rows = 3, 3

    cell_w = width // grid_cols
    cell_h = height // grid_rows

    display = np.zeros((cell_h * grid_rows, cell_w * grid_cols, 3), dtype=np.uint8)

    # Render video frames
    for idx, frame in enumerate(video_frames):
        row = idx // grid_cols
        col = idx % grid_cols
        x_start = col * cell_w
        y_start = row * cell_h
        if frame is not None:
            if total_elements == 1:
                resized = cv2.resize(frame, (width, height))
                display = resized
            else:
                resized = cv2.resize(frame, (cell_w, cell_h))
                display[y_start : y_start + cell_h, x_start : x_start + cell_w] = resized

    # Render IMU panels
    for i, (key, img) in enumerate(imu_frames.items()):
        current_idx = num_videos + i
        row = current_idx // grid_cols
        col = current_idx % grid_cols
        x_start = col * cell_w
        y_start = row * cell_h
        if total_elements == 1:
            display = cv2.resize(img, (width, height))
        else:
            resized = cv2.resize(img, (cell_w, cell_h))
            display[y_start : y_start + cell_h, x_start : x_start + cell_w] = resized

    return display


def render_frames():
    """Main UI loop to display the frames - runs at display refresh rate"""
    WINDOW_NAME = "MultiStream Playback(.bag) Viewer"
    DISPLAY_WIDTH = 1280
    DISPLAY_HEIGHT = 720

    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(WINDOW_NAME, DISPLAY_WIDTH, DISPLAY_HEIGHT)

    while not state.stop_rendering:
        display = create_display(DISPLAY_WIDTH, DISPLAY_HEIGHT)

        cv2.imshow(WINDOW_NAME, display)

        # Check exit key
        key = cv2.waitKey(1) & 0xFF
        if key in [ord("q"), 27]:  # q or ESC
            break


def main():
    global playback, pipeline, config

    # Get file path from user
    file_path = input("Enter output filename (.bag) and press Enter to start playbacking: ")

    try:
        # Initialize playback
        playback = PlaybackDevice(file_path)

        # Setup camera
        pipeline, config = setup_camera(playback)

        # Set playback status callback
        playback.set_playback_status_change_callback(on_playback_status_change)

        # Start pipeline with callback - async mode
        pipeline.start(config, video_frame_callback)

        # Start replay monitor thread
        monitor_thread = threading.Thread(target=replay_monitor, daemon=True)
        monitor_thread.start()

        # Start rendering (main thread)
        try:
            render_frames()
        except KeyboardInterrupt:
            state.stop_rendering = True

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Signal exit
        state.exited = True
        state.stop_rendering = True

        # Stop pipeline
        try:
            if pipeline:
                pipeline.stop()
        except:
            pass

        # Cleanup
        playback = None
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
