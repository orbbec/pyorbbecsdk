from pyorbbecsdk import Pipeline, FrameSet
from pyorbbecsdk import Config
from pyorbbecsdk import OBSensorType
import cv2
import numpy as np
from queue import Queue

depth_frames_queue = Queue()
MAX_QUEUE_SIZE = 5
ESC_KEY = 27


def on_new_frame_callback(frame: FrameSet):
    if frame is None:
        return
    depth_frame = frame.get_depth_frame()
    if depth_frame is None:
        return
    if depth_frames_queue.qsize() >= MAX_QUEUE_SIZE:
        depth_frames_queue.get()
    depth_frames_queue.put(depth_frame)


def rendering_frames():
    global depth_frames_queue
    while True:
        depth_frame = None
        if not depth_frames_queue.empty():
            depth_frame = depth_frames_queue.get()
        if depth_frame is None:
            continue
        height = depth_frame.get_height()
        width = depth_frame.get_width()
        data_size = depth_frame.get_data_size()
        if data_size != width * height * 2:
            print("Invalid data size: ", data_size)
            continue
        depth_data = np.frombuffer(depth_frame.get_data(), dtype=np.uint16)
        depth_data = depth_data.reshape((height, width))
        scale = depth_frame.get_depth_scale()

        depth_data = depth_data.astype(np.float32) * scale
        center_y = int(height / 2)
        center_x = int(width / 2)
        center_distance = depth_data[center_y, center_x]
        print("center distance: ", center_distance)

        depth_image = cv2.normalize(depth_data, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        depth_image = cv2.applyColorMap(depth_image, cv2.COLORMAP_JET)

        cv2.imshow("Depth Viewer", depth_image)
        key = cv2.waitKey(1)
        if key == ord('q') or key == ESC_KEY:
            break


def main():
    config = Config()
    pipeline = Pipeline()
    try:
        profile_list = pipeline.get_stream_profile_list(OBSensorType.DEPTH_SENSOR)
        assert profile_list is not None
        depth_profile = profile_list.get_default_video_stream_profile()
        assert depth_profile is not None
        print("depth profile: ", type(depth_profile))
        config.enable_stream(depth_profile)
    except Exception as e:
        print(e)
        return
    pipeline.start(config, lambda frames: on_new_frame_callback(frames))
    while True:
        try:
            rendering_frames()
        except KeyboardInterrupt:
            break
    pipeline.stop()


if __name__ == "__main__":
    main()
