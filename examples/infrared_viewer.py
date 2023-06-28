from pyorbbecsdk import Pipeline
from pyorbbecsdk import Config
from pyorbbecsdk import OBSensorType, OBFormat
from pyorbbecsdk import OBError
import cv2
import numpy as np


def main():
    config = Config()
    pipeline = Pipeline()
    try:
        profile_list = pipeline.get_stream_profile_list(OBSensorType.IR_SENSOR)
        try:
            ir_profile = profile_list.get_video_stream_profile(640, 0, OBFormat.Y16, 30)
        except OBError as e:
            print(e)
            ir_profile = profile_list.get_default_video_stream_profile()
        config.enable_stream(ir_profile)
    except Exception as e:
        print(e)
        return
    pipeline.start(config)
    while True:
        try:
            frames = pipeline.wait_for_frames(100)
            if frames is None:
                continue
            ir_frame = frames.get_ir_frame()
            if ir_frame is None:
                continue
            ir_data = np.asanyarray(ir_frame.get_data())
            width = ir_frame.get_width()
            height = ir_frame.get_height()
            ir_format = ir_frame.get_format()
            if ir_format == OBFormat.Y8:
                ir_data = np.resize(ir_data, (height, width, 1))
            else:
                ir_data = np.resize(ir_data, (height, width, 2))
            ir_image = np.zeros((height, width, 3), dtype=np.uint8)
            ir_image[:, :, 0] = ir_data[:, :, 0]
            ir_image[:, :, 1] = ir_data[:, :, 0] if ir_format == OBFormat.Y8 else ir_data[:, :, 1]
            cv2.normalize(ir_image, ir_image, 0, 255, cv2.NORM_MINMAX)
            ir_image = ir_image.astype(np.uint8)
            ir_image = cv2.cvtColor(ir_image, cv2.COLORMAP_HOT)
            cv2.imshow("Infrared Viewer", ir_image)
            key = cv2.waitKey(1)
            if key == ord('q'):
                break
        except KeyboardInterrupt:
            break
    pipeline.stop()


if __name__ == "__main__":
    main()
