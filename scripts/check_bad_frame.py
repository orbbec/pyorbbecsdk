from pyorbbecsdk import *
import numpy as np
import cv2
import time
import os
import sys
import yaml
from typing import *
import logging

lower_purple = np.array([130, 50, 90])
upper_purple = np.array([170, 255, 255])
magnitude_spectrum_upper = 2000
save_all_images = False
max_duration = 10
max_purple_ratio = 0.1
all_images_dir = "all_images"
bad_images_dir = "bad_images"


def determine_convert_format(frame: VideoFrame):
    if frame.get_format() == OBFormat.I420:
        return OBConvertFormat.I420_TO_RGB888
    elif frame.get_format() == OBFormat.MJPG:
        return OBConvertFormat.MJPG_TO_RGB888
    elif frame.get_format() == OBFormat.YUYV:
        return OBConvertFormat.YUYV_TO_RGB888
    elif frame.get_format() == OBFormat.NV21:
        return OBConvertFormat.NV21_TO_RGB888
    elif frame.get_format() == OBFormat.NV12:
        return OBConvertFormat.NV12_TO_RGB888
    elif frame.get_format() == OBFormat.UYVY:
        return OBConvertFormat.UYVY_TO_RGB888
    else:
        return None


def frame_to_bgr_image(frame: VideoFrame) -> Union[Optional[np.array], Any]:
    width = frame.get_width()
    height = frame.get_height()
    color_format = frame.get_format()
    data = np.asanyarray(frame.get_data())
    image = np.zeros((height, width, 3), dtype=np.uint8)
    if color_format == OBFormat.RGB:
        image = np.resize(data, (height, width, 3))
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    elif color_format == OBFormat.BGR:
        image = np.resize(data, (height, width, 3))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    elif color_format == OBFormat.YUYV:
        image = np.resize(data, (height, width, 2))
        image = cv2.cvtColor(image, cv2.COLOR_YUV2BGR_YUYV)
    elif color_format == OBFormat.MJPG:
        image = cv2.imdecode(data, cv2.IMREAD_COLOR)
    elif color_format == OBFormat.I420:
        image = np.resize(data, (height, width * 3 // 2))
        image = cv2.cvtColor(image, cv2.COLOR_YUV2BGR_I420)
        image = image[:, :width, :]
    elif color_format == OBFormat.NV12:
        image = np.resize(data, (height, width * 3 // 2))
        image = cv2.cvtColor(image, cv2.COLOR_YUV2BGR_NV12)
        image = image[:, :width, :]
    elif color_format == OBFormat.NV21:
        image = np.resize(data, (height, width * 3 // 2))
        image = cv2.cvtColor(image, cv2.COLOR_YUV2BGR_NV21)
        image = image[:, :width, :]
    elif color_format == OBFormat.UYVY:
        image = np.resize(data, (height, width * 2))
        image = cv2.cvtColor(image, cv2.COLOR_YUV2BGR_UYVY)
    else:
        logging.error("Unsupported color format: {}".format(color_format))
        return None
    return image


def read_config(config_file: str) -> Dict[str, Any]:
    if not os.path.exists(config_file):
        logging.error("Config file not found: {}".format(config_file))
        sys.exit(1)
    with open(config_file, "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    return config


def check_ir_frame(frame: VideoFrame):
    if frame is None:
        return
    ir_data = np.asanyarray(frame.get_data())
    width = frame.get_width()
    height = frame.get_height()
    ir_format = frame.get_format()
    if ir_format == OBFormat.Y8:
        ir_data = np.resize(ir_data, (height, width, 1))
    else:
        ir_data = np.resize(ir_data, (height, width, 2))
        ir_data = ir_data[:, :, 0]
    gray = ir_data
    image = gray
    f = np.fft.fft2(gray)
    fshift = np.fft.fftshift(f)
    magnitude_spectrum = 20 * np.log(np.abs(fshift))
    timestamp = frame.get_system_timestamp()
    image_format = frame.get_format()
    bad_ir_image_dir = os.path.join(bad_images_dir, "ir")
    os.path.exists(bad_ir_image_dir) or os.makedirs(bad_ir_image_dir)
    bad_image_file_name = os.path.join(bad_ir_image_dir,
                                       "{}_{}_{}_{}_bad.jpg".format(width, height, image_format,
                                                                    timestamp))
    max_magnitude_spectrum = np.max(magnitude_spectrum)
    print("max_magnitude_spectrum: {}".format(max_magnitude_spectrum))
    global magnitude_spectrum_upper
    if max_magnitude_spectrum > magnitude_spectrum_upper:
        cv2.imwrite(bad_image_file_name, image)
        logging.info("Save bad image: {}".format(bad_image_file_name))
    if save_all_images:
        all_ir_image_dir = os.path.join(all_images_dir, "ir")
        os.path.exists(all_ir_image_dir) or os.makedirs(all_ir_image_dir)
        all_image_file_name = os.path.join(all_ir_image_dir,
                                           "{}_{}_{}_{}.jpg".format(width, height, image_format,
                                                                    timestamp))
        cv2.imwrite(all_image_file_name, image)
        logging.info("Save all image: {}".format(all_image_file_name))


def check_color_frame(frame: VideoFrame):
    if frame is None:
        return
    image = frame_to_bgr_image(frame)
    if image is None:
        logging.error("Convert frame to bgr image failed")
        return
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_purple, upper_purple)
    purple_ratio = 0 if mask.shape[0] * mask.shape[1] == 0 else mask.sum() / (
            mask.shape[0] * mask.shape[1])
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    f = np.fft.fft2(gray)
    fshift = np.fft.fftshift(f)
    magnitude_spectrum = 20 * np.log(np.abs(fshift))
    width = frame.get_width()
    height = frame.get_height()
    image_format = frame.get_format()
    timestamp = frame.get_system_timestamp()
    bad_color_image_dir = os.path.join(bad_images_dir, "color")
    os.path.exists(bad_color_image_dir) or os.makedirs(bad_color_image_dir)

    bad_image_file_name = os.path.join(bad_color_image_dir,
                                       "{}_{}_{}_{}_bad.jpg".format(width, height, image_format,
                                                                    timestamp))
    max_magnitude_spectrum = np.max(magnitude_spectrum)
    if max_magnitude_spectrum > magnitude_spectrum_upper:
        logging.error(
            "Bad color frame, {}x{}, format: {}, timestamp: {}, magnitude spectrum:{}".format(width,
                                                                                              height,
                                                                                              image_format,
                                                                                              timestamp,
                                                                                              magnitude_spectrum.max()))
        cv2.imwrite(bad_image_file_name, image)
    elif purple_ratio > max_purple_ratio:
        logging.error(
            "Bad color frame, {}x{}, format: {}, timestamp: {}, purple ratio:{}".format(width,
                                                                                        height,
                                                                                        image_format,
                                                                                        timestamp,
                                                                                        purple_ratio))
        cv2.imwrite(bad_image_file_name, image)
    print("max_magnitude_spectrum: {}".format(max_magnitude_spectrum))
    print("purple_ratio: {}".format(purple_ratio))

    if save_all_images:
        color_image_dir = os.path.join(all_images_dir, "color")
        os.path.exists(color_image_dir) or os.makedirs(color_image_dir)
        image_file_name = os.path.join(color_image_dir,
                                       "{}_{}_{}_{}.jpg".format(width, height, image_format,
                                                                timestamp))
        cv2.imwrite(image_file_name, image)


def check_depth_frame(frame: VideoFrame):
    if frame is None:
        return
    width = frame.get_width()
    height = frame.get_height()
    scale = frame.get_depth_scale()
    depth_data = np.frombuffer(frame.get_data(), dtype=np.uint16)
    depth_data = depth_data.reshape((height, width))
    depth_data = depth_data.astype(np.float32) * scale
    image = cv2.normalize(depth_data, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    f = np.fft.fft2(image)
    fshift = np.fft.fftshift(f)
    magnitude_spectrum = 20 * np.log(np.abs(fshift))
    image_format = frame.get_format()
    timestamp = frame.get_system_timestamp()
    bad_depth_image_dir = os.path.join(bad_images_dir, "depth")
    os.path.exists(bad_depth_image_dir) or os.makedirs(bad_depth_image_dir)

    bad_image_file_name = os.path.join(bad_depth_image_dir,
                                       "{}_{}_{}_{}_bad.jpg".format(width, height, image_format,
                                                                    timestamp))
    max_magnitude_spectrum = np.max(magnitude_spectrum)
    if max_magnitude_spectrum > magnitude_spectrum_upper:
        logging.error(
            "Bad depth frame, {}x{}, format: {}, timestamp: {}, magnitude spectrum:{}".format(width,
                                                                                              height,
                                                                                              image_format,
                                                                                              timestamp,
                                                                                              max_magnitude_spectrum))
        cv2.imwrite(bad_image_file_name, image)

    if save_all_images:
        depth_image_dir = os.path.join(all_images_dir, "depth")
        os.path.exists(depth_image_dir) or os.makedirs(depth_image_dir)
        image_file_name = os.path.join(depth_image_dir,
                                       "{}_{}_{}_{}.jpg".format(width, height, image_format,
                                                                timestamp))
        cv2.imwrite(image_file_name, image)


def main():
    global lower_purple, upper_purple, magnitude_spectrum_upper
    global max_duration, save_all_images, max_purple_ratio
    if os.path.exists("config.yaml"):
        config = read_config("config.yaml")
        lower_purple = np.array(config["lower_purple"])
        upper_purple = np.array(config["upper_purple"])
        magnitude_spectrum_upper = config["magnitude_spectrum_upper"]
        max_duration = config["max_duration"]
        save_all_images = config["save_all_images"]
        max_purple_ratio = config["max_purple_ratio"]
    else:
        logging.warning("Config file not found, use default values")
    context = Context()
    context.set_logger_level(OBLogLevel.NONE)
    device_list = context.query_devices()
    if device_list.get_count() == 0:
        logging.error("No device connected")
        return
    device = device_list.get_device_by_index(0)
    pipeline = Pipeline(device)
    sensor_types = [OBSensorType.COLOR_SENSOR, OBSensorType.DEPTH_SENSOR, OBSensorType.IR_SENSOR]
    check_bad_frame = {OBFrameType.COLOR_FRAME: check_color_frame,
                       OBFrameType.DEPTH_FRAME: check_depth_frame,
                       OBFrameType.IR_FRAME: check_ir_frame}
    stream_types = {OBFrameType.COLOR_FRAME: "color",
                    OBFrameType.DEPTH_FRAME: "depth",
                    OBFrameType.IR_FRAME: "ir"}
    for sensor_type in sensor_types:
        profile_list = pipeline.get_stream_profile_list(sensor_type)
        for i in range(profile_list.get_count()):
            profile = profile_list.get_stream_profile_by_index(i).as_video_stream_profile()
            config = Config()
            config.enable_stream(profile)
            start_time = time.time()
            duration = 0
            last_frame_time = 0
            width = profile.get_width()
            height = profile.get_height()
            image_format = profile.get_format()
            expected_fps = profile.get_fps()
            pipeline.start(config)
            frame_count = 0
            print("stream type: {}, width: {}, height: {}, format: {}, fps: {}".format(
                stream_types[sensor_type],
                width, height,
                image_format,
                expected_fps))
            while duration < max_duration:
                frames = pipeline.wait_for_frames(100)
                if frames is None:
                    continue
                if sensor_type == OBSensorType.COLOR_SENSOR:
                    frame = frames.get_color_frame()
                elif sensor_type == OBSensorType.DEPTH_SENSOR:
                    frame = frames.get_depth_frame()
                else:
                    frame = frames.get_ir_frame()
                if frame is None:
                    continue
                # compute fps
                frame_time = frame.get_system_timestamp()  # in ms
                frame_count += 1
                if frame_count % expected_fps == 0:
                    fps = 1000.0 / (frame_time - last_frame_time) * expected_fps
                    last_frame_time = frame_time
                    # check bad frame fps
                    if fps < expected_fps * 0.9:
                        print(
                            " Low fps, {} : {} {}x{}@{}fps, fps: {}".format(
                                stream_types[sensor_type], image_format, width,
                                height,
                                expected_fps,
                                fps))

                elif last_frame_time == 0:
                    last_frame_time = frame_time
                # check bad frame
                frame_type = frame.get_type()
                check_bad_frame[frame_type](frame)
                duration = time.time() - start_time
            pipeline.stop()


if __name__ == '__main__':
    time_str = time.strftime("%Y%m%d_%H%M%S")
    if not os.path.exists("log"):
        os.makedirs("log")
    filename = "log/" + time_str + ".log"
    logging.basicConfig(filename=filename, level=logging.INFO)
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Keyboard interrupt")
