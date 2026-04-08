# ******************************************************************************
#  pyorbbecsdk Beginner Example 07 — IMU Data Stream
#
#  What you will learn:
#    1. How to enable the accelerometer (ACCEL) and gyroscope (GYRO) sensors
#    2. How to read IMU frames: timestamp, temperature, and 3-axis values
#    3. How to display accelerometer (m/s^2) and gyroscope (rad/s) data in real time
#
#  Keyboard: ESC or 'q' to quit
#
#  Device requirement: All
#
#  Run:
#    python examples/beginner/07_imu.py
# ******************************************************************************
import cv2

from pyorbbecsdk import OBError  # type: ignore
from pyorbbecsdk import (
    Config,
    Context,
    OBFrameAggregateOutputMode,
    OBFrameType,
    OBSensorType,
    Pipeline,
)

ESC_KEY = 27


def print_imu_value(value, frame_index, timestamp_us, temperature, frame_type, unit_str):
    """Print IMU frame value in formatted style similar to C++ example."""
    type_str = "ACCEL" if frame_type == OBFrameType.ACCEL_FRAME else "GYRO"

    print(f"frame index: {frame_index}")
    print(f"{type_str} Frame: ")
    print("{")
    print(f"  tsp = {timestamp_us}")
    print(f"  temperature = {temperature}")
    print(f"  {type_str}.x = {value.x}{unit_str}")
    print(f"  {type_str}.y = {value.y}{unit_str}")
    print(f"  {type_str}.z = {value.z}{unit_str}")
    print("}")
    print()


def main():
    # Check if device is connected
    ctx = Context()
    device_list = ctx.query_devices()
    if device_list.get_count() == 0:
        print("Device Not Found! Please connect an Orbbec camera and try again.")
        return

    config = Config()
    pipeline = Pipeline()
    device = pipeline.get_device()

    try:
        device.get_sensor(OBSensorType.ACCEL_SENSOR)
        device.get_sensor(OBSensorType.GYRO_SENSOR)
    except Exception as e:
        print(f"Device does not support Accel or Gyro sensor: {e}")
        return

    config.enable_accel_stream()
    config.enable_gyro_stream()
    config.set_frame_aggregate_output_mode(OBFrameAggregateOutputMode.FULL_FRAME_REQUIRE)
    try:
        pipeline.start(config)
    except OBError as e:
        print(f"Error: {e}")
        print("Please connect an Orbbec camera and try again.")
        return

    accel_count = 0
    gyro_count = 0

    print("IMU stream started. Press 'q' or ESC to exit.")
    print()

    while True:
        try:
            key = cv2.waitKey(1)
            if key == ord("q") or key == ESC_KEY:
                break

            frames = pipeline.wait_for_frames(100)
            if frames is None:
                continue

            accel_frame = frames.get_accel_frame()
            if accel_frame is not None:
                if accel_count % 50 == 0:  # Print every 50 frames
                    print_imu_value(
                        accel_frame.get_value(),
                        accel_frame.get_index(),
                        accel_frame.get_timestamp_us(),
                        accel_frame.get_temperature(),
                        accel_frame.get_type(),
                        "m/s^2",
                    )
                accel_count += 1

            gyro_frame = frames.get_gyro_frame()
            if gyro_frame is not None:
                if gyro_count % 50 == 0:  # Print every 50 frames
                    print_imu_value(
                        gyro_frame.get_value(),
                        gyro_frame.get_index(),
                        gyro_frame.get_timestamp_us(),
                        gyro_frame.get_temperature(),
                        gyro_frame.get_type(),
                        "rad/s",
                    )
                gyro_count += 1

        except KeyboardInterrupt:
            break

    pipeline.stop()


if __name__ == "__main__":
    main()
