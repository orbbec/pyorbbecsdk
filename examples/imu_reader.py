from pyorbbecsdk import *
import time
from threading import Lock

console_lock = Lock()
stop_gyro = False
stop_accel = False


def on_gyro_frame_callback(frame: Frame):
    if frame is None:
        return
    global stop_gyro
    if stop_gyro:
        return
    with console_lock:
        gyro_frame: GyroFrame = frame.as_gyro_frame()
        if gyro_frame is not None:
            print("GyroFrame: ts={}".format(gyro_frame.get_timestamp()))
            print("GyroFrame: x={}, y={}, z={}".format(gyro_frame.get_x(), gyro_frame.get_y(),
                                                       gyro_frame.get_z()))


def on_accel_frame_callback(frame: Frame):
    if frame is None:
        return
    global stop_accel
    if stop_accel:
        return
    with console_lock:
        accel_frame: AccelFrame = frame.as_accel_frame()
        if accel_frame is not None:
            print("AccelFrame: ts={}".format(accel_frame.get_timestamp()))
            print("AccelFrame: x={}, y={}, z={}".format(accel_frame.get_x(), accel_frame.get_y(),
                                                        accel_frame.get_z()))


def main():
    ctx: Context = Context()
    device_list: DeviceList = ctx.query_devices()
    if device_list.get_count() == 0:
        print("No device connected")
        return
    device: Device = device_list.get_device_by_index(0)
    sensor_list: SensorList = device.get_sensor_list()
    try:
        gyro_senor = sensor_list.get_sensor_by_type(OBSensorType.GYRO_SENSOR)
        if gyro_senor is None:
            print("No gyro sensor")
            return
        gyro_profile_list: StreamProfileList = gyro_senor.get_stream_profile_list()
        gyro_profile: StreamProfile = gyro_profile_list.get_stream_profile_by_index(0)
        assert gyro_profile is not None
        gyro_senor.start(gyro_profile, on_gyro_frame_callback)
    except OBError as e:
        print(e)
        return
    try:
        accel_sensor = sensor_list.get_sensor_by_type(OBSensorType.ACCEL_SENSOR)
        if accel_sensor is None:
            print("No accel sensor")
            return
        accel_profile_list: StreamProfileList = accel_sensor.get_stream_profile_list()
        accel_profile: StreamProfile = accel_profile_list.get_stream_profile_by_index(0)
        assert accel_profile is not None
        accel_sensor.start(accel_profile, on_accel_frame_callback)
    except OBError as e:
        print(e)
        return
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            # Don't forget to stop the sensor
            global stop_accel, stop_gyro
            stop_accel = True
            stop_gyro = True
            time.sleep(0.01)
            if gyro_senor is not None:
                gyro_senor.stop()
            if accel_sensor is not None:
                accel_sensor.stop()
            break


if __name__ == "__main__":
    main()
