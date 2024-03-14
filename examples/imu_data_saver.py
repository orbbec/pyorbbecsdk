from pyorbbecsdk import *
import time
from threading import Lock
import csv
from pathlib import Path
import os
console_lock = Lock()
stop_gyro = False
stop_accel = False

csv_file = open(os.path.join(Path(__file__).parent, 'imu_data.csv'), 'w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['timestamp', 'type', 'x', 'y', 'z'])

def on_gyro_frame_callback(frame: Frame):
    if frame is None:
        return
    global stop_gyro
    if stop_gyro:
        return
    with console_lock:
        gyro_frame: GyroFrame = frame.as_gyro_frame()
        if gyro_frame is not None:
            # write the gyroscope data to the CSV
            csv_writer.writerow([gyro_frame.get_timestamp(), 'gyro', gyro_frame.get_x(), gyro_frame.get_y(), gyro_frame.get_z()])

def on_accel_frame_callback(frame: Frame):
    if frame is None:
        return
    global stop_accel
    if stop_accel:
        return
    with console_lock:
        accel_frame: AccelFrame = frame.as_accel_frame()
        if accel_frame is not None:
            # write the acceleration data to the CSV
            csv_writer.writerow([accel_frame.get_timestamp(), 'accel', accel_frame.get_x(), accel_frame.get_y(), accel_frame.get_z()])

def main():
    ctx: Context = Context()
    device_list: DeviceList = ctx.query_devices()
    if device_list.get_count() == 0:
        print("No device connected")
        return
    device: Device = device_list.get_device_by_index(0)
    sensor_list: SensorList = device.get_sensor_list()
    try:
        gyro_sensor = sensor_list.get_sensor_by_type(OBSensorType.GYRO_SENSOR)
        if gyro_sensor is None:
            print("No gyro sensor")
            return
        gyro_profile_list: StreamProfileList = gyro_sensor.get_stream_profile_list()
        gyro_profile: StreamProfile = gyro_profile_list.get_stream_profile_by_index(0)
        assert gyro_profile is not None
        gyro_sensor.start(gyro_profile, on_gyro_frame_callback)
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
            global stop_accel, stop_gyro
            stop_accel = True
            stop_gyro = True
            time.sleep(0.01)
            if gyro_sensor is not None:
                gyro_sensor.stop()
            if accel_sensor is not None:
                accel_sensor.stop()
            break

    # close the csv file
    csv_file.close()

if __name__ == "__main__":
    main()
