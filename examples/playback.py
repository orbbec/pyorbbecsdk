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

# cached frames for better visualization
cached_frames = {
    'color': None,
    'depth': None,
    'left_ir': None,
    'right_ir': None,
    'ir': None
}

def setup_camera(playback):
    """Setup camera and stream configuration"""
    pipeline = Pipeline(playback)
    config = Config()
    device = pipeline.get_device()

    # Try to enable all possible sensors
    video_sensors = [
        OBSensorType.COLOR_SENSOR,
        OBSensorType.DEPTH_SENSOR,
        OBSensorType.IR_SENSOR,
        OBSensorType.LEFT_IR_SENSOR,
        OBSensorType.RIGHT_IR_SENSOR,
        OBSensorType.ACCEL_SENSOR, 
        OBSensorType.GYRO_SENSOR, 
    ]
    enabled_sensor_types = []  

    sensor_list = device.get_sensor_list()
    for sensor in range(len(sensor_list)):
        try:
            sensor_type = sensor_list[sensor].get_type()
            if sensor_type in video_sensors:
                config.enable_stream(sensor_type)
                enabled_sensor_types.append(sensor_type)
        except:
            continue
    return pipeline, config, enabled_sensor_types

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


def process_ir(ir_frame, key):
    """Process IR frame (left, right, or mono) with cache"""  
    ir_frame = ir_frame if ir_frame else cached_frames[key]
    cached_frames[key] = ir_frame
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



def create_display(frames, enabled_sensor_types, width=1280, height=720):
    """Create display window with correct dynamic layout"""
    sensor_type_to_name = {
        OBSensorType.COLOR_SENSOR: 'color',
        OBSensorType.DEPTH_SENSOR: 'depth',
        OBSensorType.LEFT_IR_SENSOR: 'left_ir',
        OBSensorType.RIGHT_IR_SENSOR: 'right_ir',
        OBSensorType.IR_SENSOR: 'ir'
    }
    video_keys = []
    for sensor_type in enabled_sensor_types:
        if sensor_type in sensor_type_to_name:
            video_keys.append(sensor_type_to_name[sensor_type])

    video_frames = [frames.get(k) for k in video_keys]
    has_imu = 'imu' in frames
    num_videos = len(video_frames)

    total_elements = num_videos + (1 if has_imu else 0)

    if total_elements == 1:
        grid_cols, grid_rows = 1, 1
    elif total_elements <= 2:
        grid_cols, grid_rows = 2, 1
    elif total_elements <= 4:
        grid_cols, grid_rows = 2, 2
    elif total_elements <= 5:
        grid_cols, grid_rows = 2, 3
    else:
        raise ValueError("Too many elements! Maximum supported is 5.")

    cell_w = width // grid_cols
    cell_h = height // grid_rows

    display = np.zeros((cell_h * grid_rows, cell_w * grid_cols, 3), dtype=np.uint8)

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
                display[y_start:y_start + cell_h, x_start:x_start + cell_w] = resized
        else:
            cv2.rectangle(display, (x_start, y_start), (x_start + cell_w, y_start + cell_h), (0, 0, 0), -1)

    if has_imu:
        imu_idx = num_videos
        row = imu_idx // grid_cols
        col = imu_idx % grid_cols
        x_start = col * cell_w
        y_start = row * cell_h
        cv2.rectangle(display, (x_start, y_start), (x_start + cell_w, y_start + cell_h), (50, 50, 50), -1)

        y_offset = y_start + 30
        for data_type in ['accel', 'gyro']:
            text_lines = get_imu_text(frames['imu'].get(data_type), data_type.title())
            for i, line in enumerate(text_lines):
                cv2.putText(display, line, (x_start + 10, y_offset + i * 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)
            y_offset += 100

    return display



def main():
    # Window settings
    WINDOW_NAME = "MultiStream Playback(.bag) Viewer"
    file_path = input("Enter output filename (.bag) and press Enter to start playbacking: ")

    DISPLAY_WIDTH = 1280
    DISPLAY_HEIGHT = 720
    # initialize playback
    playback  = PlaybackDevice(file_path)
    # Initialize camera
    pipeline, config, enabled_sensor_types = setup_camera(playback)
    device = pipeline.get_device()
    def on_status_change(status):
        print(f"[Callback] status changed: {status}")
        if status == PlaybackStatus.Stopped:
            pipeline.stop()
            pipeline.start(config)
    playback.set_playback_status_change_callback(on_status_change)

    pipeline.start(config)

    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(WINDOW_NAME, DISPLAY_WIDTH, DISPLAY_HEIGHT)
    processed_frames = {}
    while True:
        # Get all frames
        frames = pipeline.wait_for_frames(100)
        if not frames:
            continue

        # Process color image        
        color_frame = frames.get_frame(OBFrameType.COLOR_FRAME)
        if color_frame:
            processed_frames['color'] = process_color(color_frame.as_video_frame())
        # Process depth image
        depth_frame = frames.get_frame(OBFrameType.DEPTH_FRAME)
        if depth_frame:
            processed_frames['depth'] = process_depth(depth_frame.as_video_frame())       
        # Process left IR
        left_ir_frame = frames.get_frame(OBFrameType.LEFT_IR_FRAME)
        processed_frames['left_ir'] = process_ir(left_ir_frame, 'left_ir')

        # Process right IR
        right_ir_frame = frames.get_frame(OBFrameType.RIGHT_IR_FRAME)
        processed_frames['right_ir'] = process_ir(right_ir_frame, 'right_ir')

        # Process mono IR
        ir_frame = frames.get_ir_frame()
        processed_frames['ir'] = process_ir(ir_frame, 'ir')

        # Process IMU data
        accel = frames.get_frame(OBFrameType.ACCEL_FRAME)
        gyro = frames.get_frame(OBFrameType.GYRO_FRAME)
        if accel and gyro:
            processed_frames['imu'] = {
                'accel': accel.as_accel_frame(),
                'gyro': gyro.as_gyro_frame()
            }

        # create display
        display = create_display(processed_frames, enabled_sensor_types, DISPLAY_WIDTH, DISPLAY_HEIGHT)
        cv2.imshow(WINDOW_NAME, display)

        # check exit key
        key = cv2.waitKey(1) & 0xFF
        if key in (ord('q'), 27):
            break

    pipeline.stop()
    playback  = None 
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
