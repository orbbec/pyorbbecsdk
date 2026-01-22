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

import cv2
import numpy as np
from pyorbbecsdk import *
from utils import frame_to_bgr_image, is_astra_mini_device
import threading
import math

# Global state to share data between the processing callback and the UI thread
class GlobalState:
    def __init__(self):
        self.frame_mutex = threading.Lock()
        self.stop_rendering = False
        self.support_dual_ir = False
        self.support_dual_rgb = False
        # Storage for processed images to ensure smooth visualization
        self.cached_frames = {
            'color': None, 
            'depth': None, 
            'left_ir': None, 
            'right_ir': None, 
            'ir': None, 
            'confidence': None,
            'left_color': None,
            'right_color': None
        }
state = GlobalState()

def setup_camera():
    """Initialize the pipeline and configure available sensor streams"""
    pipeline = Pipeline()
    config = Config()
    device = pipeline.get_device()
    device_info = device.get_device_info()

    # Define sensors we want to attempt to enable
    video_sensors = [
        OBSensorType.COLOR_SENSOR,
        OBSensorType.DEPTH_SENSOR,
        OBSensorType.IR_SENSOR,
        OBSensorType.LEFT_IR_SENSOR,
        OBSensorType.RIGHT_IR_SENSOR,
        OBSensorType.CONFIDENCE_SENSOR,
        OBSensorType.LEFT_COLOR_SENSOR,
        OBSensorType.RIGHT_COLOR_SENSOR
    ]
    
    sensor_list = device.get_sensor_list()
    for sensor in range(len(sensor_list)):
        sensor_type = sensor_list[sensor].get_type()
        
        # Check if the device hardware supports Dual IR (Left/Right)
        if sensor_type in [OBSensorType.LEFT_IR_SENSOR, OBSensorType.RIGHT_IR_SENSOR]:
            state.support_dual_ir = True
        
        if sensor_type in [OBSensorType.LEFT_COLOR_SENSOR, OBSensorType.RIGHT_COLOR_SENSOR]:
            state.support_dual_rgb = True
            
        if sensor_type in video_sensors:
            # Special handling: Astra Mini IR sensor might conflict with specific configs
            if is_astra_mini_device(device_info.get_vid(), device_info.get_pid()) and sensor_type == OBSensorType.IR_SENSOR:
                continue
            try: 
                config.enable_stream(sensor_type)
            except: 
                # Skip sensors that fail to enable (unsupported resolutions/formats)
                continue

    # Start pipeline with a callback function for asynchronous frame handling
    pipeline.start(config, video_frame_callback)
    return pipeline

def process_color(frame):
    """Convert raw color frame to BGR for OpenCV display"""
    if frame is None:
        return state.cached_frames['color']
    return frame_to_bgr_image(frame)

def process_depth(frame):
    """Normalize 16-bit depth data and apply a JET colormap for visualization"""
    if frame is None:
        return state.cached_frames['depth']
    try:
        depth_data = np.frombuffer(frame.get_data(), dtype=np.uint16)
        depth_data = depth_data.reshape(frame.get_height(), frame.get_width())
        # Convert 16-bit depth to 8-bit for colormap application
        depth_image = cv2.normalize(depth_data, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        return cv2.applyColorMap(depth_image, cv2.COLORMAP_JET)
    except ValueError:
        return None

def process_ir(ir_frame):
    """Process various IR formats (Y8, Y16, MJPG) into standard RGB images"""
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

    # Normalize intensity to ensure the IR image is visible
    cv2.normalize(ir_data, ir_data, 0, max_data, cv2.NORM_MINMAX, dtype=image_dtype)
    ir_data = ir_data.astype(data_type)
    return cv2.cvtColor(ir_data, cv2.COLOR_GRAY2RGB)

def process_confidence(frame):
    """Convert confidence map to an RGB grayscale representation"""
    if frame is None:
        return state.cached_frames['confidence']
    try:
        confidence_data = np.frombuffer(frame.get_data(), dtype=np.uint8)
        confidence_data = confidence_data.reshape(frame.get_height(), frame.get_width())
        confidence_image = cv2.normalize(confidence_data, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        return cv2.cvtColor(confidence_image, cv2.COLOR_GRAY2RGB)
    except ValueError:
        return None
    
def video_frame_callback(frames):
    """Callback function triggered when a new FrameSet arrives"""
    if frames is None:
        return None
    with state.frame_mutex:
        if frames:
            state.cached_frames['color'] = process_color(frames.get_color_frame())
            state.cached_frames['depth'] = process_depth(frames.get_depth_frame())

            if state.support_dual_ir:
                left_ir = frames.get_frame(OBFrameType.LEFT_IR_FRAME)
                right_ir = frames.get_frame(OBFrameType.RIGHT_IR_FRAME)
                if left_ir and right_ir:
                    state.cached_frames['left_ir'] = process_ir(left_ir)
                    state.cached_frames['right_ir'] = process_ir(right_ir)
            else:
                ir_frame = frames.get_ir_frame()
                if ir_frame:
                    state.cached_frames['ir'] = process_ir(ir_frame)
            
            confidence = frames.get_frame(OBFrameType.CONFIDENCE_FRAME)
            if confidence:
                try:
                    state.cached_frames['confidence'] = process_confidence(confidence.as_confidence_frame())
                except:
                    pass
                
            if state.support_dual_rgb:
                left_color = frames.get_frame(OBFrameType.LEFT_COLOR_FRAME)
                right_color = frames.get_frame(OBFrameType.RIGHT_COLOR_FRAME)
                if left_color and right_color:
                    try:
                        state.cached_frames['left_color'] = process_color(left_color.as_video_frame())
                        state.cached_frames['right_color'] = process_color(right_color.as_video_frame())
                    except:
                        pass

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
    """Main UI loop to process and display the frames"""
    WINDOW_NAME = "Callback Viewer"
    DISPLAY_WIDTH, DISPLAY_HEIGHT = 1280, 720
    
    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(WINDOW_NAME, DISPLAY_WIDTH, DISPLAY_HEIGHT)
    
    while not state.stop_rendering:
        blocks = []
        check_keys = ['color', 'depth', 'left_ir', 'right_ir', 'ir', 'confidence', 'left_color', 'right_color']           
        with state.frame_mutex: 
            # create display
            for key in check_keys:
                img = state.cached_frames.get(key)
                if img is not None:
                    blocks.append(img)   
                    
        if not blocks:
            if cv2.waitKey(5) & 0xFF in [ord('q'), 27]:
                break
            continue
            
        display = create_display(blocks, DISPLAY_WIDTH, DISPLAY_HEIGHT)
        cv2.imshow(WINDOW_NAME, display)
        
        # check exit key
        key = cv2.waitKey(1) & 0xFF
        if key in [ord('q'), 27]:  # q or ESC
            break
        
def main():  
    try:  
        # Initialize camera and streams
        pipeline = setup_camera()

        # Enter visualization loop
        try:
            render_frames()
        except KeyboardInterrupt:
            state.stop_rendering = True
    
    except Exception as e:
        print(f"Error: {str(e)}")
        
    # Resources cleanup
    pipeline.stop()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()