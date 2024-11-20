# ******************************************************************************
#  Copyright (c) 2024 Orbbec 3D Technology, Inc
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
# ******************************************************************************

from queue import Queue
import cv2
import numpy as np
from pyorbbecsdk import *
from utils import frame_to_bgr_image

# Global variables
frames_queue = Queue()
MAX_QUEUE_SIZE = 1
ESC_KEY = 27
stop_rendering = False

# Define sensor types we want to enable
video_sensor_types = [
    OBSensorType.DEPTH_SENSOR,
    OBSensorType.LEFT_IR_SENSOR,
    OBSensorType.RIGHT_IR_SENSOR,
    OBSensorType.IR_SENSOR,
    OBSensorType.COLOR_SENSOR
]
# cached frames for better visualization
cached_frames = {
    'color': None,
    'depth': None,
    'left_ir': None,
    'right_ir': None,
    'ir': None
}

def on_new_frame_callback(frame: FrameSet):
    """Callback function to handle new frames"""
    if frame is None:
        return
    if frames_queue.qsize() >= MAX_QUEUE_SIZE:
        frames_queue.get()
    frames_queue.put(frame)


def process_color(frame):
    """Process color frame to BGR image"""
    if not frame:
        return None
    color_frame = frame.get_color_frame()
    color_frame = color_frame if color_frame else cached_frames['color']
    if not color_frame:
        return None
    try:
        cached_frames['color'] = color_frame
        return frame_to_bgr_image(color_frame)
    except ValueError:
        print("Error processing color frame")
        return None


def process_depth(frame):
    """Process depth frame to colorized depth image"""
    if not frame:
        return None
    depth_frame = frame.get_depth_frame()
    depth_frame = depth_frame if depth_frame else cached_frames['depth']
    if not depth_frame:
        return None
    try:
        depth_data = np.frombuffer(depth_frame.get_data(), dtype=np.uint16)
        depth_data = depth_data.reshape(depth_frame.get_height(), depth_frame.get_width())
        depth_image = cv2.normalize(depth_data, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        cached_frames['depth'] = depth_frame
        return cv2.applyColorMap(depth_image, cv2.COLORMAP_JET)
    except ValueError:
        print("Error processing depth frame")
        return None


def process_ir(frame, frame_type):
    if frame is None:
        return None
    ir_frame = frame.get_frame(frame_type)
    frame_name = 'ir' if frame_type == OBFrameType.IR_FRAME else 'left_ir' if frame_type == OBFrameType.LEFT_IR_FRAME else 'right_ir'
    ir_frame = ir_frame if ir_frame else cached_frames[frame_name]
    if not ir_frame:
        return None
    ir_frame = ir_frame.as_video_frame()
    cached_frames[frame_name] = ir_frame
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



def create_display(processed_frames, width=1280, height=720):
    """Create display window with all processed frames
    Layout:
    2x2 grid when both left and right IR are present:
    [Color] [Depth]
    [L-IR] [R-IR]

    2x2 grid with single IR:
    [Color] [Depth]
    [  IR  ][     ]
    """
    display = np.zeros((height, width, 3), dtype=np.uint8)
    h, w = height // 2, width // 2

    # Helper function for safe image resizing
    def safe_resize(img, target_size):
        if img is None:
            return None
        try:
            return cv2.resize(img, target_size)
        except:
            return None

    # Process frames with consistent error handling
    def place_frame(img, x1, y1, x2, y2):
        if img is not None:
            try:
                h_section = y2 - y1
                w_section = x2 - x1
                resized = safe_resize(img, (w_section, h_section))
                if resized is not None:
                    display[y1:y2, x1:x2] = resized
            except:
                pass

    # Always show color and depth in top row if available
    place_frame(processed_frames.get('color'), 0, 0, w, h)
    place_frame(processed_frames.get('depth'), w, 0, width, h)

    # Handle IR display in bottom row
    has_left_ir = processed_frames.get('left_ir') is not None
    has_right_ir = processed_frames.get('right_ir') is not None
    has_single_ir = processed_frames.get('ir') is not None

    if has_left_ir and has_right_ir:
        # Show stereo IR in bottom row
        place_frame(processed_frames['left_ir'], 0, h, w, height)
        place_frame(processed_frames['right_ir'], w, h, width, height)
    elif has_single_ir:
        # Show single IR in bottom-left quadrant
        place_frame(processed_frames['ir'], 0, h, w, height)

    # Add labels to identify each stream
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.8
    font_color = (255, 255, 255)
    font_thickness = 2

    # Helper function for adding labels
    def add_label(text, x, y):
        cv2.putText(display, text, (x + 10, y + 30), font, font_scale,
                   font_color, font_thickness)

    # Add labels for each quadrant
    add_label("Color", 0, 0)
    add_label("Depth", w, 0)

    if has_left_ir and has_right_ir:
        add_label("Left IR", 0, h)
        add_label("Right IR", w, h)
    elif has_single_ir:
        add_label("IR", 0, h)

    return display

def rendering_frames():
    """Main rendering loop for processing and displaying frames"""
    global frames_queue, stop_rendering

    # Create and configure display window
    cv2.namedWindow("Orbbec Camera Viewer", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Orbbec Camera Viewer", 1280, 720)

    while not stop_rendering:
        if frames_queue.empty():
            continue

        frame_set = frames_queue.get()
        if frame_set is None:
            continue

        # Process all available frames
        processed_frames = {
            'color': process_color(frame_set),
            'depth': process_depth(frame_set),
        }

        # Process IR frames with better error handling
        try:
            left_ir = process_ir(frame_set, OBFrameType.LEFT_IR_FRAME)
            right_ir = process_ir(frame_set, OBFrameType.RIGHT_IR_FRAME)
            if left_ir is not None and right_ir is not None:
                processed_frames['left_ir'] = left_ir
                processed_frames['right_ir'] = right_ir
            else:
                # Try single IR if stereo IR is not available
                ir = process_ir(frame_set, OBFrameType.IR_FRAME)
                if ir is not None:
                    processed_frames['ir'] = ir
        except:
            # Fallback to single IR in case of any error
            try:
                ir = process_ir(frame_set, OBFrameType.IR_FRAME)
                if ir is not None:
                    processed_frames['ir'] = ir
            except:
                pass

        # Create and display the combined view
        display = create_display(processed_frames)
        cv2.imshow("Orbbec Camera Viewer", display)

        # Check for exit key
        key = cv2.waitKey(1)
        if key in [ord('q'), ESC_KEY]:
            return

def main():
    """Main function to initialize and run the camera viewer"""
    global stop_rendering
    config = Config()
    pipeline = Pipeline()

    try:
        # Initialize pipeline and config


        # Get device and sensor information
        device = pipeline.get_device()
        sensor_list = device.get_sensor_list()

        # Enable all available video streams
        for sensor in range(len(sensor_list)):
            sensor_type = sensor_list[sensor].get_type()
            if sensor_type in video_sensor_types:
                try:
                    print(f"Enabling sensor type: {sensor_type}")
                    config.enable_stream(sensor_type)
                except:
                    print(f"Failed to enable sensor type: {sensor_type}")
                    continue

        # Start pipeline with callback
        pipeline.start(config, lambda frames: on_new_frame_callback(frames))

        # Start rendering frames
        try:
            rendering_frames()
        except KeyboardInterrupt:
            stop_rendering = True

    except Exception as e:
        print(f"Error: {str(e)}")

        # Cleanup
    stop_rendering = True
    pipeline.stop()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
