from pyorbbecsdk import *
import time
import cv2
import numpy as np


def playback_state_callback(state):
    if state == OBMediaState.OB_MEDIA_BEGIN:
        print("Bag player stopped")
    elif state == OBMediaState.OB_MEDIA_END:
        print("Bag player playing")
    elif state == OBMediaState.OB_MEDIA_PAUSED:
        print("Bag player paused")


def frame_playback_callback(frame):
    depth_frame = frame.as_depth_frame()
    depth_image = np.asanyarray(depth_frame.get_data())
    cv2.normalize(depth_image, depth_image, 0, 255, cv2.NORM_MINMAX)
    depth_image = depth_image.astype(np.uint8)
    depth_image = cv2.applyColorMap(depth_image, cv2.COLORMAP_JET)
    cv2.imshow("Depth Viewer", depth_image)


def main():
    pipeline = Pipeline("./test.bag")
    playback = pipeline.get_playback()
    playback.set_playback_state_callback(playback_state_callback)
    device_info = pipeline.get_device_info()
    print("Device info: ", device_info)
    camera_param = pipeline.get_camera_param()
    print("Camera param: ", camera_param)
    playback.start(frame_playback_callback)
    time.sleep(5)
    while True:
        if playback.get_playback_state() == OBMediaState.OB_MEDIA_END:
            break
        time.sleep(1)
    playback.stop()
    pipeline.stop()


if __name__ == "__main__":
    main()
