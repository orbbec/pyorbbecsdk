import platform
import subprocess

import cv2
import numpy as np

from pyorbbecsdk import (Pipeline, Context, Config, OBSensorType,
                         OBFormat, OBError)
from utils import frame_to_bgr_image

ESC_KEY = 27

# Only Femto Mega and Gemini2 XL support this sample

def get_stream_profile(pipeline, sensor_type, width, height, fmt, fps):
    profile_list = pipeline.get_stream_profile_list(sensor_type)
    try:
        profile = profile_list.get_video_stream_profile(width, height, fmt, fps)
    except OBError:
        profile = profile_list.get_default_video_stream_profile()
    return profile


def decode_h265_frame(color_frame, color_format='hevc'):
    # This function is only supported on Linux.
    # and requires ffmpeg to be installed.
    if color_format == 'h265':
        color_format = 'hevc'
    elif color_format == 'h264':
        color_format = 'h264'  # Actually, this remains unchanged but added for clarity.

    cmd_in = [
        'ffmpeg',
        '-f', color_format,
        '-i', 'pipe:',
        '-f', 'rawvideo',
        '-pix_fmt', 'bgr24',
        'pipe:'
    ]

    byte_data = color_frame.get_data().tobytes()

    proc = subprocess.Popen(cmd_in, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate(input=byte_data)

    if proc.returncode != 0:
        raise ValueError(f'FFmpeg did not run successfully: {err.decode()}')
    if len(out) == 0:
        return None
    decoded_frame = np.frombuffer(out, dtype=np.uint8).reshape(color_frame.get_height(), color_frame.get_width(), 3)
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
    color_profile = get_stream_profile(pipeline, OBSensorType.COLOR_SENSOR, 1280, 0, OBFormat.MJPG, 10)
    config.enable_stream(color_profile)

    # Setup depth stream
    depth_profile = get_stream_profile(pipeline, OBSensorType.DEPTH_SENSOR, 640, 0, OBFormat.Y16, 10)
    config.enable_stream(depth_profile)

    pipeline.start(config)
    warning_printed = False

    try:
        while True:
            frames = pipeline.wait_for_frames(100)
            if not frames:
                continue

            color_frame = frames.get_color_frame()
            depth_frame = frames.get_depth_frame()

            if color_frame and color_frame.get_format() in [OBFormat.H265, OBFormat.H264]:
                if platform.system() == 'Linux':
                    color_format = 'h265' if color_frame.get_format() == OBFormat.H265 else 'h264'
                    color_image = decode_h265_frame(color_frame, color_format)
                else:
                    if not warning_printed:
                        print("H264 and H265 are not supported on this system.")
                        warning_printed = True
                    color_image = None
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

            if color_image is not None and depth_image is not None:
                target_size = (640, 480)
                images_to_show = [img for img in [color_image, depth_image] if img is not None]
                # Resize each image to 640x480
                images_to_show = [cv2.resize(img, target_size) for img in images_to_show]

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
