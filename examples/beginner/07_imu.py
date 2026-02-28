# ******************************************************************************
#  pyorbbecsdk Beginner Example 07 — IMU Data Stream
#
#  What you will learn:
#    1. How to enable the accelerometer (ACCEL) and gyroscope (GYRO) sensors
#    2. How to read IMU frames: timestamp, temperature, and 3-axis values
#    3. How to display accelerometer (m/s²) and gyroscope (dps) data in real time
#
#  Keyboard: Ctrl+C to quit
#
#  Device requirement: All
#
#  Run:
#    python examples/beginner/07_imu.py
# ******************************************************************************
import cv2
from pyorbbecsdk import *

ESC_KEY = 27

def main():
    config = Config()
    pipeline = Pipeline()
    device = pipeline.get_device()
    
    try:
        device.get_sensor(OBSensorType.ACCEL_SENSOR)
        device.get_sensor(OBSensorType.GYRO_SENSOR)
    except:
        print("Device does not support Accel or Gyro sensor.")
        return
    
    config.enable_accel_stream()
    config.enable_gyro_stream()
    config.set_frame_aggregate_output_mode(OBFrameAggregateOutputMode.FULL_FRAME_REQUIRE)
    pipeline.start(config)

    frame_counter = 0

    while True:
        try:
            frames = pipeline.wait_for_frames(100)
            if frames is None:
                continue
            frame_counter += 1
            accel_frame = frames.get_frame(OBFrameType.ACCEL_FRAME)
            accel_frame = accel_frame.as_accel_frame()

            if accel_frame is not None and frame_counter % 50 == 0:
                print("AccelFrame: ts={}".format(accel_frame.get_timestamp()))
                print("AccelFrame: x={}, y={}, z={}".format(accel_frame.get_x(), accel_frame.get_y(), accel_frame.get_z()))

            gyro_frame = frames.get_frame(OBFrameType.GYRO_FRAME)
            gyro_frame = gyro_frame.as_gyro_frame()

            if gyro_frame is not None and frame_counter % 50 == 0:
                print("GyroFrame: ts={}".format(gyro_frame.get_timestamp()))
                print("GyroFrame: x={}, y={}, z={}".format(gyro_frame.get_x(), gyro_frame.get_y(), gyro_frame.get_z()))

            key = cv2.waitKey(1)
            if key == ord('q') or key == ESC_KEY:
                break
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()
