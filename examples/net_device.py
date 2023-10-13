import cv2
import ffmpeg
import numpy as np
from pyorbbecsdk import (Pipeline, FrameSet, Context, Config, OBSensorType,
                         OBFormat, OBError, VideoStreamProfile)
from utils import frame_to_bgr_image

ESC_KEY = 27


def get_stream_profile(pipeline, sensor_type, width, height, fmt, fps):
    profile_list = pipeline.get_stream_profile_list(sensor_type)
    try:
        profile = profile_list.get_video_stream_profile(width, height, fmt, fps)
    except OBError:
        profile = profile_list.get_default_video_stream_profile()
    return profile


def decode_h265_frame(color_frame):
    color_format = 'h265' if color_frame.get_format() == OBFormat.H265 else 'h264'
    in_proc = ffmpeg.input('pipe:', format=color_format).output('pipe:', format='rawvideo', pix_fmt='bgr24').run(
        capture_stdout=True, capture_stderr=True, input=color_frame.get_data())
    decoded_frame = np.frombuffer(in_proc[0], dtype=np.uint8).reshape(color_frame.get_height(), color_frame.get_width(),
                                                                      3)
    return decoded_frame


def main():
    ctx = Context()
    ip = input("Enter the ip address of the device (default: 192.168.1.10): ") or "192.168.1.10"
    device = ctx.create_net_device(ip, 8090)
    if device is None:
        print("Failed to create net device")
        return

    config = Config()
    pipeline = Pipeline(device)

    # Setup color stream
    color_profile = get_stream_profile(pipeline, OBSensorType.COLOR_SENSOR, 640, 0, OBFormat.H265, 30)
    config.enable_stream(color_profile)

    # Setup depth stream
    depth_profile = get_stream_profile(pipeline, OBSensorType.DEPTH_SENSOR, 640, 0, OBFormat.Y16, 30)
    config.enable_stream(depth_profile)

    pipeline.start(config)

    try:
        while True:
            frames = pipeline.wait_for_frames(100)
            if not frames:
                continue

            color_frame = frames.get_color_frame()
            depth_frame = frames.get_depth_frame()

            if color_frame and color_frame.get_format() in [OBFormat.H265, OBFormat.H264]:
                color_image = decode_h265_frame(color_frame)
            elif color_frame:
                color_image = frame_to_bgr_image(color_frame)
            else:
                color_image = None

            if depth_frame:
                depth_data = np.frombuffer(depth_frame.get_data(), dtype=np.uint16).reshape(depth_frame.get_height(),
                                                                                            depth_frame.get_width())
                scale = depth_frame.get_depth_scale()
                depth_data = (depth_data * scale).astype(np.uint16)
                depth_image = cv2.normalize(depth_data, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
                depth_image = cv2.applyColorMap(depth_image, cv2.COLORMAP_JET)
            else:
                depth_image = None

            if color_image is not None or depth_image is not None:
                images_to_show = [img for img in [color_image, depth_image] if img is not None]
                cv2.imshow("net_device", np.hstack(images_to_show))

            key = cv2.waitKey(1)
            if key in [ord('q'), ESC_KEY]:
                break
    except KeyboardInterrupt:
        pass
    finally:
        pipeline.stop()


if __name__ == "__main__":
    main()
