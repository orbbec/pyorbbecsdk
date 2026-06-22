# ******************************************************************************
#  pyorbbecsdk Beginner Example 06 — Multi-Stream Viewer
#
#  What you will learn:
#    1. How to enable all available streams (color, depth, IR, IMU) simultaneously
#    2. How to use async callbacks to receive frames without blocking the main thread
#    3. How to display multiple streams in a dynamic grid layout
#    4. How to handle dual-IR and dual-color sensors automatically
#
#  Keyboard: ESC or Q to quit
#
#  Dependencies: numpy, opencv-python, utils.py
#
#  Device requirement: All
#
#  Run:
#    python examples/beginner/06_multi_streams.py
# ******************************************************************************

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import math
import threading

import cv2
import numpy as np
from utils import frame_to_bgr_image, is_astra_mini_device, is_gemini305g_device

from pyorbbecsdk import OBFormat  # type: ignore
from pyorbbecsdk import Config, Context, OBError, OBFrameType, OBSensorType, Pipeline


class GlobalState:
    def __init__(self):
        self.frame_mutex = threading.Lock()
        self.imu_mutex = threading.Lock()
        self.stop_rendering = False
        self.support_dual_ir = False
        self.support_imu = False
        self.support_dual_rgb = False
        # cached frames for better visualization
        self.cached_frames = {
            "color": None,
            "depth": None,
            "left_ir": None,
            "right_ir": None,
            "ir": None,
            "confidence": None,
            "accel": None,
            "gyro": None,
            "left_color": None,
            "right_color": None,
        }


state = GlobalState()


def setup_camera():
    """Setup camera and stream configuration"""
    pipeline = Pipeline()
    config = Config()
    device = pipeline.get_device()
    device_info = device.get_device_info()

    # Try to enable all possible sensors
    video_sensors = [
        OBSensorType.COLOR_SENSOR,
        OBSensorType.DEPTH_SENSOR,
        OBSensorType.IR_SENSOR,
        OBSensorType.LEFT_IR_SENSOR,
        OBSensorType.RIGHT_IR_SENSOR,
        OBSensorType.CONFIDENCE_SENSOR,
        OBSensorType.LEFT_COLOR_SENSOR,
        OBSensorType.RIGHT_COLOR_SENSOR,
    ]
    sensor_list = device.get_sensor_list()
    for sensor in range(len(sensor_list)):
        sensor_type = sensor_list[sensor].get_type()
        if sensor_type in [OBSensorType.LEFT_IR_SENSOR, OBSensorType.RIGHT_IR_SENSOR]:
            state.support_dual_ir = True
        if sensor_type in [
            OBSensorType.LEFT_COLOR_SENSOR,
            OBSensorType.RIGHT_COLOR_SENSOR,
        ]:
            state.support_dual_rgb = True
        if sensor_type in [OBSensorType.ACCEL_SENSOR, OBSensorType.GYRO_SENSOR]:
            state.support_imu = True
            continue
        if sensor_type in video_sensors:
            if (
                is_astra_mini_device(device_info.get_vid(), device_info.get_pid())
                and sensor_type == OBSensorType.IR_SENSOR
            ):
                continue
        try:
            config.enable_stream(sensor_type)
        except:
            continue

    if is_gemini305g_device(device_info.get_vid(), device_info.get_pid(), device_info.get_connection_type()):
        config.disable_stream(OBSensorType.LEFT_IR_SENSOR)

    try:
        pipeline.start(config, video_frame_callback)
    except OBError as e:
        print(f"Error: {e}")
        print("Please connect an Orbbec camera and try again.")
        return None
    return pipeline


def setup_imu():
    """Setup IMU configuration"""
    if not state.support_imu:
        return None
    pipeline = Pipeline()
    config = Config()
    config.enable_accel_stream()
    config.enable_gyro_stream()
    try:
        pipeline.start(config, imu_frame_callback)
    except OBError as e:
        print(f"Error: {e}")
        print("Please connect an Orbbec camera and try again.")
        return None
    return pipeline


def process_color(frame):
    """Process color image"""
    if frame is None:
        return state.cached_frames["color"]
    return frame_to_bgr_image(frame)


def process_depth(frame):
    """Process depth image"""
    if frame is None:
        return state.cached_frames["depth"]
    try:
        depth_data = np.frombuffer(frame.get_data(), dtype=np.uint16)
        depth_data = depth_data.reshape(frame.get_height(), frame.get_width())
        depth_image = cv2.normalize(depth_data, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        return cv2.applyColorMap(depth_image, cv2.COLORMAP_JET)
    except ValueError:
        return None


def process_ir(ir_frame):
    """Process IR frame (left or right) to RGB image"""
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
        return state.cached_frames["confidence"]
    try:
        confidence_data = np.frombuffer(frame.get_data(), dtype=np.uint8)
        confidence_data = confidence_data.reshape(frame.get_height(), frame.get_width())
        confidence_image = cv2.normalize(confidence_data, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        return cv2.cvtColor(confidence_image, cv2.COLOR_GRAY2RGB)
    except ValueError:
        return None


def create_single_imu_panel(imu_frame, title, w=480, h=240):
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
    if frames is None:
        return None
    with state.frame_mutex:
        if frames:
            state.cached_frames["color"] = process_color(frames.get_color_frame())
            state.cached_frames["depth"] = process_depth(frames.get_depth_frame())

            if state.support_dual_ir:
                left_ir = frames.get_left_ir_frame()
                right_ir = frames.get_right_ir_frame()
                if left_ir:
                    state.cached_frames["left_ir"] = process_ir(left_ir)
                if right_ir:
                    state.cached_frames["right_ir"] = process_ir(right_ir)
            else:
                ir_frame = frames.get_ir_frame()
                if ir_frame:
                    state.cached_frames["ir"] = process_ir(ir_frame)

            confidence = frames.get_confidence_frame()
            if confidence:
                try:
                    state.cached_frames["confidence"] = process_confidence(confidence)
                except:
                    pass

            if state.support_dual_rgb:
                left_color = frames.get_left_color_frame()
                right_color = frames.get_right_color_frame()
                if left_color and right_color:
                    try:
                        state.cached_frames["left_color"] = process_color(left_color)
                        state.cached_frames["right_color"] = process_color(right_color)
                    except:
                        pass


def imu_frame_callback(imu_frames):
    if imu_frames is None:
        return None

    with state.imu_mutex:
        if imu_frames:
            accel = imu_frames.get_accel_frame()
            gyro = imu_frames.get_gyro_frame()
            if accel:
                state.cached_frames["accel"] = create_single_imu_panel(accel, "ACCEL")
            if gyro:
                state.cached_frames["gyro"] = create_single_imu_panel(gyro, "GYRO")


def create_display(blocks, width=1280, height=720):
    """
    Composite multiple image blocks into a single grid display.

    :param blocks: List of numpy arrays (images) to be displayed.
    :param width: Width of the output canvas.
    :param height: Height of the output canvas.
    :return: A single composite image with all blocks arranged in a grid.
    """
    if not blocks:
        return np.zeros((height, width, 3), dtype=np.uint8)

    count = len(blocks)
    cols = min(3, math.ceil(math.sqrt(count)))
    rows = math.ceil(count / cols)

    display = np.zeros((height, width, 3), dtype=np.uint8)
    cw, ch = width // cols, height // rows

    for i, imgs in enumerate(blocks):
        r, c = i // cols, i % cols
        x1, y1 = c * cw, r * ch

        h_orig, w_orig = imgs.shape[:2]
        scale = min(cw / w_orig, ch / h_orig)
        nw, nh = int(w_orig * scale), int(h_orig * scale)
        res = cv2.resize(imgs, (nw, nh))

        dx = (cw - nw) // 2
        dy = (ch - nh) // 2
        display[y1 + dy : y1 + dy + nh, x1 + dx : x1 + dx + nw] = res

    return display


def render_frames():
    # Window settings
    WINDOW_NAME = "MultiStream Viewer"
    DISPLAY_WIDTH = 1280
    DISPLAY_HEIGHT = 720

    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(WINDOW_NAME, DISPLAY_WIDTH, DISPLAY_HEIGHT)

    while not state.stop_rendering:
        blocks = []
        check_keys = [
            "color",
            "depth",
            "left_ir",
            "right_ir",
            "ir",
            "confidence",
            "accel",
            "gyro",
            "left_color",
            "right_color",
        ]
        with state.frame_mutex, state.imu_mutex:
            # create display
            for key in check_keys:
                img = state.cached_frames.get(key)
                if img is not None:
                    blocks.append(img)

        if not blocks:
            if cv2.waitKey(5) & 0xFF in [ord("q"), 27]:
                break
            continue

        display = create_display(blocks, DISPLAY_WIDTH, DISPLAY_HEIGHT)
        cv2.imshow(WINDOW_NAME, display)

        # check exit key
        key = cv2.waitKey(1) & 0xFF
        if key in [ord("q"), 27]:  # q or ESC
            break


def main():
    # Check if device is connected
    ctx = Context()
    device_list = ctx.query_devices()
    if device_list.get_count() == 0:
        print("Device Not Found! Please connect an Orbbec camera and try again.")
        return

    pipeline = None
    imu_pipeline = None
    try:
        # Initialize camera
        pipeline = setup_camera()
        imu_pipeline = setup_imu()

        # Start rendering frames
        try:
            render_frames()
        except KeyboardInterrupt:
            state.stop_rendering = True

    except Exception as e:
        print(f"Error: {str(e)}")

    # Clean up
    if pipeline:
        pipeline.stop()
    if imu_pipeline:
        imu_pipeline.stop()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
