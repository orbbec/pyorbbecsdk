from pyorbbecsdk import Pipeline
from pyorbbecsdk import Config
from pyorbbecsdk import OBSensorType, OBFormat
from pyorbbecsdk import OBError
import cv2
import numpy as np

ESC_KEY = 27


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
            elif ir_format == OBFormat.MJPG:
                ir_data = cv2.imdecode(ir_data, cv2.IMREAD_UNCHANGED)
                if ir_data is None:
                    print("decode mjpeg failed")
                    continue
                ir_data = np.resize(ir_data, (height, width, 1))
            else:
                ir_data = np.frombuffer(ir_data, dtype=np.uint16)
                ir_data = np.resize(ir_data, (height, width, 1))
            cv2.normalize(ir_data, ir_data, 0, 255, cv2.NORM_MINMAX)
            ir_data = ir_data.astype(np.uint8)
            ir_image = cv2.cvtColor(ir_data, cv2.COLOR_GRAY2RGB)
            cv2.imshow("Infrared Viewer", ir_image)
            key = cv2.waitKey(1)
            if key == ord('q') or key == ESC_KEY:
                break
        except KeyboardInterrupt:
            break
    pipeline.stop()


if __name__ == "__main__":
    main()
