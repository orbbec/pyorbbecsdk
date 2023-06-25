from pyorbbecsdk import *
import time
import cv2
import numpy as np


def main():
    pipeline = Pipeline
    config = Config()
    try:
        profile_list = pipeline.get_stream_profile_list(OBSensorType.COLOR_SENSOR)
        if profile_list is None:
            print("No depth sensor found")
            return
        profile = profile_list.get_default_video_stream_profile()
        config.enable_stream(profile)
    except Exception as e:
        print(e)
        return
    pipeline.start(config)
    pipeline.start_recording("test.bag")
    while True:
        try:
            frames = pipeline.wait_for_frames(100)
            if frames is None:
                continue
            depth_frame = frames.get_depth_frame()
            if depth_frame is None:
                continue
            depth_image = np.asanyarray(depth_frame.get_data())
            cv2.normalize(depth_image, depth_image, 0, 255, cv2.NORM_MINMAX)
            depth_image = depth_image.astype(np.uint8)
            depth_image = cv2.applyColorMap(depth_image, cv2.COLORMAP_JET)
            cv2.imshow("Depth Viewer", depth_image)
            key = cv2.waitKey(1)
            if key == ord('q'):
                pipeline.stop_recording()
                break
        except KeyboardInterrupt:
            pipeline.stop_recording()
            break


if __name__ == "__main__":
    main()
