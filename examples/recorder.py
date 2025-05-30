# ******************************************************************************
#  Copyright (c) 2024 Orbbec 3D Technology, Inc
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http:# www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
# ******************************************************************************

import cv2
import numpy as np
from pyorbbecsdk import *
from utils import frame_to_bgr_image

is_paused = False
# cached frames for better visualization
cached_frames = {
    'color': None,
    'depth': None,
    'left_ir': None,
    'right_ir': None,
    'ir': None
}

def setup_camera():
    """Setup camera and stream configuration"""
    pipeline = Pipeline()
    config = Config()
    device = pipeline.get_device()

    # Try to enable all possible sensors
    video_sensors = [
        OBSensorType.COLOR_SENSOR,
        OBSensorType.DEPTH_SENSOR,
        OBSensorType.IR_SENSOR,
        OBSensorType.LEFT_IR_SENSOR,
        OBSensorType.RIGHT_IR_SENSOR
    ]
    sensor_list = device.get_sensor_list()
    for sensor in range(len(sensor_list)):
        try:
            sensor_type = sensor_list[sensor].get_type()
            if sensor_type in video_sensors:
                config.enable_stream(sensor_type)
        except:
            continue

    pipeline.start(config)
    return pipeline

def setup_imu():
    """Setup IMU configuration"""
    pipeline = Pipeline()   
    config = Config()
    config.enable_accel_stream()
    config.enable_gyro_stream()
    pipeline.start(config)
    return pipeline

def process_color(frame):
    """Process color image"""
    frame = frame if frame else cached_frames['color']
    cached_frames['color'] = frame
    return frame_to_bgr_image(frame) if frame else None


def process_depth(frame):
    """Process depth image"""
    frame = frame if frame else cached_frames['depth']
    cached_frames['depth'] = frame
    if not frame:
        return None
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
    ir_frame = ir_frame.as_video_frame()
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

def get_imu_text(frame, name):
    """Format IMU data"""
    if not frame:
        return []
    return [
        f"{name} x: {frame.get_x():.2f}",
        f"{name} y: {frame.get_y():.2f}",
        f"{name} z: {frame.get_z():.2f}"
    ]


def create_display(frames, width=1280, height=720):
    """Create display window"""
    display = np.zeros((height, width, 3), dtype=np.uint8)
    h, w = height // 2, width // 2

    # Process video frames
    if 'color' in frames and frames['color'] is not None:
        display[0:h, 0:w] = cv2.resize(frames['color'], (w, h))

    if 'depth' in frames and frames['depth'] is not None:
        display[0:h, w:] = cv2.resize(frames['depth'], (w, h))

    if 'ir' in frames and frames['ir'] is not None:
        display[h:, 0:w] = cv2.resize(frames['ir'], (w, h))

    # Display IMU data
    if 'imu' in frames:
        y_offset = h + 20
        for data_type in ['accel', 'gyro']:
            text_lines = get_imu_text(frames['imu'].get(data_type), data_type.title())
            for i, line in enumerate(text_lines):
                cv2.putText(display, line, (w + 10, y_offset + i * 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            y_offset += 80

    return display


def main():
    # Window settings
    WINDOW_NAME = "MultiStream Record Viewer"
    file_path = input("Enter output filename (.bag) and press Enter to start recording: ")

    DISPLAY_WIDTH = 1280
    DISPLAY_HEIGHT = 720

    # Initialize camera
    pipeline = setup_camera()
    device = pipeline.get_device()
    #synchronize the timer of the device with the host
    device.timer_sync_with_host();
    # initialize recording
    recorder = RecordDevice(device, file_path)
    imu_pipeline = setup_imu()
    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(WINDOW_NAME, DISPLAY_WIDTH, DISPLAY_HEIGHT)
    while True:
        # Get all frames
        frames = pipeline.wait_for_frames(100)
        if not frames:
            continue
        # Process different frame types
        processed_frames = {'color': process_color(frames.get_color_frame()),
                            'depth': process_depth(frames.get_depth_frame())}

        # Process IR image: try stereo IR first, fallback to mono if unavailable
        try:
            left = process_ir(frames.get_frame(OBFrameType.LEFT_IR_FRAME).as_video_frame())
            right = process_ir(frames.get_frame(OBFrameType.RIGHT_IR_FRAME).as_video_frame())
            if left is not None and right is not None:
                processed_frames['ir'] = np.hstack((left, right))
        except:
            ir_frame = frames.get_ir_frame()
            if ir_frame:
                processed_frames['ir'] = process_ir(ir_frame.as_video_frame())

        # Process IMU data
        imu_frames = imu_pipeline.wait_for_frames(100)
        if not imu_frames:
            continue
        accel = imu_frames.get_frame(OBFrameType.ACCEL_FRAME)
        gyro = imu_frames.get_frame(OBFrameType.GYRO_FRAME)
        if accel and gyro:
            processed_frames['imu'] = {
                'accel': accel.as_accel_frame(),
                'gyro': gyro.as_gyro_frame()
            }

        # create display
        display = create_display(processed_frames, DISPLAY_WIDTH, DISPLAY_HEIGHT)
        cv2.imshow(WINDOW_NAME, display)

        # check exit key
        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):
            global is_paused
            if not is_paused:
                recorder.pause()
                is_paused = True
                print("[PAUSED] Recording paused")
            else:
                recorder.resume()
                is_paused = False
                print("[RESUMED] Recording resumed")
        if key in (ord('q'), 27):
            break

    pipeline.stop()
    recorder = None 
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
