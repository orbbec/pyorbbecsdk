import cv2
import numpy as np
from pyorbbecsdk import *
from utils import frame_to_bgr_image


def setup_camera():
    """Setup camera and stream configuration"""
    pipeline = Pipeline()
    config = Config()

    # Try to enable all possible sensors
    sensors = [
        OBSensorType.COLOR_SENSOR,
        OBSensorType.DEPTH_SENSOR,
        OBSensorType.IR_SENSOR,
        OBSensorType.LEFT_IR_SENSOR,
        OBSensorType.RIGHT_IR_SENSOR
    ]

    for sensor in sensors:
        try:
            profile_list = pipeline.get_stream_profile_list(sensor)
            profile = profile_list.get_default_video_stream_profile()
            config.enable_stream(profile)
        except:
            continue

    # Try to enable IMU
    try:
        config.enable_accel_stream()
        config.enable_gyro_stream()
        config.set_frame_aggregate_output_mode(OBFrameAggregateOutputMode.FULL_FRAME_REQUIRE)
    except:
        pass

    pipeline.start(config)
    return pipeline


def process_color(frame):
    """Process color image"""
    return frame_to_bgr_image(frame) if frame else None


def process_depth(frame):
    """Process depth image"""
    if not frame:
        return None
    depth_data = np.frombuffer(frame.get_data(), dtype=np.uint16)
    depth_data = depth_data.reshape(frame.get_height(), frame.get_width())
    depth_image = cv2.normalize(depth_data, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    return cv2.applyColorMap(depth_image, cv2.COLORMAP_JET)


def process_ir(frame):
    """Process IR image"""
    if not frame:
        return None
    ir_data = np.frombuffer(frame.get_data(), dtype=np.uint8)
    ir_data = ir_data.reshape(frame.get_height(), frame.get_width())
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
    WINDOW_NAME = "MultiStream Viewer"
    DISPLAY_WIDTH = 1280
    DISPLAY_HEIGHT = 720

    # Initialize camera
    pipeline = setup_camera()
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
        accel = frames.get_frame(OBFrameType.ACCEL_FRAME)
        gyro = frames.get_frame(OBFrameType.GYRO_FRAME)
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
        if key in [ord('q'), 27]:  # q or ESC
            break

    pipeline.stop()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
