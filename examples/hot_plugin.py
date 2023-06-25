from pyorbbecsdk import *
import time
from typing import Optional

device: Optional[Device] = None
pipeline: Optional[Pipeline] = None


def start_stream():
    global device
    global pipeline
    if device is None:
        print("No device connected")
        return
    if pipeline is not None:
        print("Pipeline is already started")
        return
    pipeline = Pipeline()
    config = Config()
    try:
        profile_list = pipeline.get_stream_profile_list(OBSensorType.COLOR_SENSOR)
        try:
            color_profile: VideoStreamProfile = profile_list.get_video_stream_profile(1280, 0, OBFormat.RGB, 30)
        except OBError as e:
            print(e)
            color_profile = profile_list.get_default_video_stream_profile()
        config.enable_stream(color_profile)
    except Exception as e:
        print(e)
    try:
        profile_list = pipeline.get_stream_profile_list(OBSensorType.DEPTH_SENSOR)
        try:
            depth_profile: VideoStreamProfile = profile_list.get_video_stream_profile(640, 0, OBFormat.Y16, 30)
        except OBError as e:
            print(e)
            depth_profile = profile_list.get_default_video_stream_profile()
        config.enable_stream(depth_profile)
    except Exception as e:
        print(e)

    pipeline.start(config)


def stop_stream():
    global pipeline
    if pipeline is None:
        print("Pipeline is not started")
        return
    pipeline.stop()
    pipeline = None


def on_device_connected_callback(device_list: DeviceList):
    if device_list.get_count() == 0:
        return
    global device
    if device is not None:
        print("Device is already connected")
        return
    device = device_list.get_device_by_index(0)
    start_stream()


def on_device_disconnected_callback(device_list: DeviceList):
    global device
    if device_list.get_count() == 0:
        stop_stream()
        device = None
        return
    for i in range(device_list.get_count()):
        if device_list.get_device_by_index(i) == device:
            stop_stream()
            device = None
            break


def on_new_frame_callback(frame: Frame):
    print("{} frame, width={}, height={}, format={}, timestamp={}".format(frame.get_ype(),
                                                                          frame.get_width(),
                                                                          frame.get_height(),
                                                                          frame.get_format(),
                                                                          frame.get_timestamp()))


def main():
    ctx = Context()
    ctx.set_devices_changed_callback(on_device_connected_callback, on_device_disconnected_callback)
    device_list = ctx.query_devices()
    on_device_connected_callback(device_list)
    global pipeline, device
    while True:
        try:
            if pipeline is not None and device is not None:
                frames: FrameSet = pipeline.wait_for_frames(100)
                if frames is None:
                    time.sleep(0.001)
                    continue
                color_frame = frames.get_color_frame()
                depth_frame = frames.get_depth_frame()
                on_new_frame_callback(color_frame)
                on_new_frame_callback(depth_frame)
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    main()
