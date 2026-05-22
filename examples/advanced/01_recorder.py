# ******************************************************************************
#  pyorbbecsdk Advanced Example 01 — Multi-Stream Recorder
#
#  What you will learn:
#    1. How to use RecordDevice to record all available streams to a .bag file
#    2. How to enumerate and enable dual-IR, dual-color, and IMU streams
#    3. How to use frame callbacks with threading for smooth GUI recording
#    4. How to pause and resume recording without stopping the pipeline
#    5. How to run in headless mode (no display) with per-stream FPS output
#
#  Keyboard (GUI mode, default):
#    S       — Pause / Resume recording
#    Q / ESC — Stop and save
#
#  Keyboard (headless mode, --no-gui):
#    Ctrl+C  — Stop and save
#
#  Device requirement: All
#
#  Run:
#    python examples/advanced/01_recorder.py              # with live preview
#    python examples/advanced/01_recorder.py --no-gui     # headless, prints FPS
# ******************************************************************************
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import argparse
import math
import threading
import time
from threading import Lock

import cv2
import numpy as np
from utils import frame_to_bgr_image, is_astra_mini_device, is_gemini305g_device

from pyorbbecsdk import OBFormat  # type: ignore
from pyorbbecsdk import (
    Config,
    Context,
    OBError,
    OBFrameType,
    OBSensorType,
    Pipeline,
    RecordDevice,
)


class GlobalState:
    def __init__(self):
        self.frame_mutex = threading.Lock()
        self.imu_mutex = threading.Lock()
        self.recorder = None
        self.is_paused = False
        self.stop_rendering = False
        self.support_dual_ir = False
        self.support_imu = False
        self.support_dual_rgb = False
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

# --- Headless mode globals ---
_frame_mutex = Lock()
_counts: dict = {}


# ---------------------------------------------------------------------------
# Camera / IMU setup  (shared by both modes)
# ---------------------------------------------------------------------------


def setup_camera(file_path: str):
    """Initialize device, create RecordDevice, enable all available streams."""
    pipeline = Pipeline()
    config = Config()
    device = pipeline.get_device()

    try:
        device.timer_sync_with_host()
    except OBError as e:
        print(e)

    state.recorder = RecordDevice(device, file_path)
    device_info = device.get_device_info()

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
    for i in range(len(sensor_list)):
        sensor_type = sensor_list[i].get_type()
        if sensor_type in (OBSensorType.LEFT_IR_SENSOR, OBSensorType.RIGHT_IR_SENSOR):
            state.support_dual_ir = True
        if sensor_type in (
            OBSensorType.LEFT_COLOR_SENSOR,
            OBSensorType.RIGHT_COLOR_SENSOR,
        ):
            state.support_dual_rgb = True
        if sensor_type in (OBSensorType.ACCEL_SENSOR, OBSensorType.GYRO_SENSOR):
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
        except Exception:
            continue

    if is_gemini305g_device(
        device_info.get_vid(), device_info.get_pid(), device_info.get_connection_type()
    ):
        config.disable_stream(OBSensorType.LEFT_IR_SENSOR)

    pipeline.start(config, _gui_frame_callback)
    return pipeline


def setup_imu():
    """Initialize a separate pipeline for ACCEL + GYRO streams (if supported)."""
    if not state.support_imu:
        return None
    pipeline = Pipeline()
    config = Config()
    config.enable_accel_stream()
    config.enable_gyro_stream()
    pipeline.start(config, _imu_frame_callback)
    return pipeline


# ---------------------------------------------------------------------------
# Frame processing helpers (GUI mode)
# ---------------------------------------------------------------------------


def _process_color(frame):
    if frame is None:
        return state.cached_frames["color"]
    return frame_to_bgr_image(frame)


def _process_depth(frame):
    if frame is None:
        return state.cached_frames["depth"]
    try:
        d = np.frombuffer(frame.get_data(), dtype=np.uint16).reshape(frame.get_height(), frame.get_width())
        img = cv2.normalize(d, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        return cv2.applyColorMap(img, cv2.COLORMAP_JET)
    except ValueError:
        return None


def _process_ir(ir_frame):
    if ir_frame is None:
        return None
    ir_data = np.asanyarray(ir_frame.get_data())
    w, h = ir_frame.get_width(), ir_frame.get_height()
    fmt = ir_frame.get_format()

    if fmt == OBFormat.Y8:
        ir_data = np.resize(ir_data, (h, w, 1))
        dtype = np.uint8
        cv_dtype = cv2.CV_8UC1
        max_val = 255
    elif fmt == OBFormat.MJPG:
        ir_data = cv2.imdecode(ir_data, cv2.IMREAD_UNCHANGED)
        if ir_data is None:
            return None
        dtype = np.uint8
        cv_dtype = cv2.CV_8UC1
        max_val = 255
        ir_data = np.resize(ir_data, (h, w, 1))
    else:
        ir_data = np.frombuffer(ir_data, dtype=np.uint16)
        dtype = np.uint16
        cv_dtype = cv2.CV_16UC1
        max_val = 255
        ir_data = np.resize(ir_data, (h, w, 1))

    cv2.normalize(ir_data, ir_data, 0, max_val, cv2.NORM_MINMAX, dtype=cv_dtype)
    return cv2.cvtColor(ir_data.astype(dtype), cv2.COLOR_GRAY2RGB)


def _process_confidence(frame):
    if frame is None:
        return state.cached_frames["confidence"]
    try:
        d = np.frombuffer(frame.get_data(), dtype=np.uint8).reshape(frame.get_height(), frame.get_width())
        img = cv2.normalize(d, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        return cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    except ValueError:
        return None


def _create_imu_panel(imu_frame, title, w=480, h=240):
    panel = np.zeros((h, w, 3), dtype=np.uint8)
    if not imu_frame:
        return panel
    unit = "rad/s" if title == "GYRO" else "m/s^2"
    lines = [
        f"{title}:",
        f"  Time: {imu_frame.get_timestamp_us()} us",
        f"  X: {imu_frame.get_x():.6f} {unit}",
        f"  Y: {imu_frame.get_y():.6f} {unit}",
        f"  Z: {imu_frame.get_z():.6f} {unit}",
    ]
    font = cv2.FONT_HERSHEY_SIMPLEX
    lh = 30
    start_y = (h - len(lines) * lh) // 2
    for i, line in enumerate(lines):
        sz = cv2.getTextSize(line, font, 0.6, 1)[0]
        cv2.putText(
            panel,
            line,
            ((w - sz[0]) // 2, start_y + i * lh + sz[1]),
            font,
            0.6,
            (255, 255, 255),
            1,
            cv2.LINE_AA,
        )
    return panel


# ---------------------------------------------------------------------------
# Callbacks
# ---------------------------------------------------------------------------


def _gui_frame_callback(frames):
    """GUI mode: cache processed images for render_frames()."""
    if frames is None:
        return
    with state.frame_mutex:
        state.cached_frames["color"] = _process_color(frames.get_color_frame())
        state.cached_frames["depth"] = _process_depth(frames.get_depth_frame())

        if state.support_dual_ir:
            left = frames.get_left_ir_frame()
            right = frames.get_right_ir_frame()
            if left:
                state.cached_frames["left_ir"] = _process_ir(left)
            if right:
                state.cached_frames["right_ir"] = _process_ir(right)
        else:
            ir = frames.get_ir_frame()
            if ir:
                state.cached_frames["ir"] = _process_ir(ir)

        conf = frames.get_confidence_frame()
        if conf:
            try:
                state.cached_frames["confidence"] = _process_confidence(conf)
            except Exception:
                pass

        if state.support_dual_rgb:
            lc = frames.get_left_color_frame()
            rc = frames.get_right_color_frame()
            if lc and rc:
                try:
                    state.cached_frames["left_color"] = _process_color(lc)
                    state.cached_frames["right_color"] = _process_color(rc)
                except Exception:
                    pass


def _headless_frame_callback(frameset):
    """Headless mode: count frames per type for FPS display."""
    with _frame_mutex:
        for i in range(frameset.get_count()):
            f = frameset.get_frame_by_index(i)
            t = f.get_type()
            _counts[t] = _counts.get(t, 0) + 1


def _imu_frame_callback(imu_frames):
    if imu_frames is None:
        return
    with state.imu_mutex:
        accel = imu_frames.get_accel_frame()
        gyro = imu_frames.get_gyro_frame()
        if accel:
            state.cached_frames["accel"] = _create_imu_panel(accel, "ACCEL")
        if gyro:
            state.cached_frames["gyro"] = _create_imu_panel(gyro, "GYRO")


# ---------------------------------------------------------------------------
# GUI rendering
# ---------------------------------------------------------------------------


def _create_display(blocks, width=1280, height=720):
    if not blocks:
        return np.zeros((height, width, 3), dtype=np.uint8)
    count = len(blocks)
    cols = min(3, math.ceil(math.sqrt(count)))
    rows = math.ceil(count / cols)
    canvas = np.zeros((height, width, 3), dtype=np.uint8)
    cw, ch = width // cols, height // rows
    for i, img in enumerate(blocks):
        r, c = i // cols, i % cols
        x1, y1 = c * cw, r * ch
        ho, wo = img.shape[:2]
        scale = min(cw / wo, ch / ho)
        nw, nh = int(wo * scale), int(ho * scale)
        resized = cv2.resize(img, (nw, nh))
        dx, dy = (cw - nw) // 2, (ch - nh) // 2
        canvas[y1 + dy : y1 + dy + nh, x1 + dx : x1 + dx + nw] = resized
    return canvas


def render_frames():
    WINDOW = "MultiStream Record Viewer"
    W, H = 1280, 720
    cv2.namedWindow(WINDOW, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(WINDOW, W, H)

    KEYS = [
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

    while not state.stop_rendering:
        with state.frame_mutex, state.imu_mutex:
            blocks = [state.cached_frames[k] for k in KEYS if state.cached_frames.get(k) is not None]

        if not blocks:
            if cv2.waitKey(5) & 0xFF in (ord("q"), 27):
                break
            continue

        cv2.imshow(WINDOW, _create_display(blocks, W, H))
        key = cv2.waitKey(1) & 0xFF
        if key == ord("s"):
            state.is_paused = not state.is_paused
            if state.is_paused:
                state.recorder.pause()
                print("[PAUSED]")
            else:
                state.recorder.resume()
                print("[RESUMED]")
        elif key in (ord("q"), 27):
            break


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main():
    # Check if device is connected
    ctx = Context()
    device_list = ctx.query_devices()
    if device_list.get_count() == 0:
        print("Device Not Found! Please connect an Orbbec camera and try again.")
        return

    parser = argparse.ArgumentParser(description="Multi-stream recorder")
    parser.add_argument(
        "--no-gui",
        action="store_true",
        help="Headless mode: record without display, print FPS every 2 s",
    )
    args = parser.parse_args()

    file_path = input("Enter output filename (.bag) and press Enter to start recording: ")

    try:
        if args.no_gui:
            # ---- Headless mode ----
            pipeline = Pipeline()
            config = Config()
            device = pipeline.get_device()
            try:
                device.timer_sync_with_host()
            except OBError as e:
                print(e)
            state.recorder = RecordDevice(device, file_path)
            device_info = device.get_device_info()
            sensor_list = device.get_sensor_list()
            for i in range(len(sensor_list)):
                sensor_type = sensor_list[i].get_type()
                if (
                    is_astra_mini_device(device_info.get_vid(), device_info.get_pid())
                    and sensor_type == OBSensorType.IR_SENSOR
                ):
                    continue
                try:
                    config.enable_stream(sensor_type)
                except Exception:
                    continue

            if is_gemini305g_device(
                device_info.get_vid(), device_info.get_pid(), device_info.get_connection_type()
            ):
                config.disable_stream(OBSensorType.LEFT_IR_SENSOR)

            pipeline.start(config, _headless_frame_callback)
            print("Recording started (headless). Press Ctrl+C to stop and save.")

            last_time = time.time()
            while True:
                time.sleep(2)
                with _frame_mutex:
                    now = time.time()
                    duration = now - last_time
                    for ftype, cnt in _counts.items():
                        print(f"{ftype}: {cnt / duration:.2f} FPS", end="  ")
                    print()
                    _counts.clear()
                    last_time = now

        else:
            # ---- GUI mode ----
            pipeline = setup_camera(file_path)
            imu_pipeline = setup_imu()
            try:
                render_frames()
            except KeyboardInterrupt:
                state.stop_rendering = True
            if imu_pipeline:
                imu_pipeline.stop()

    except KeyboardInterrupt:
        print("\nStopping recording…")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        state.recorder = None
        try:
            pipeline.stop()
        except (NameError, UnboundLocalError):
            pass
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
