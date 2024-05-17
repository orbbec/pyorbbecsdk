# ******************************************************************************
#  Copyright (c) 2023 Orbbec 3D Technology, Inc
#  
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.  
#  You may obtain a copy of the License at
#  
#      http:# www.apache.org/licenses/LICENSE-2.0
#  
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
# ******************************************************************************
from pyorbbecsdk import *
import time
from threading import Lock
import csv

console_lock = Lock()
stop_gyro = False
stop_accel = False
last_gyro_ts = 0
last_gyro_global_ts = 0

last_accel_ts = 0
last_accel_global_ts = 0

gyro_csv_file = open('gyro_data.csv', 'w', newline='')
gyro_writer = csv.writer(gyro_csv_file)
gyro_writer.writerow(['Index', 'Timestamp','Global Timestamp', 'Timestamp Difference', 'Global Timestamp Difference'])

accel_csv_file = open('accel_data.csv', 'w', newline='')
accel_writer = csv.writer(accel_csv_file)
accel_writer.writerow(['Index', 'Timestamp', 'Global Timestamp','Timestamp Difference', 'Global Timestamp Difference'])

def on_gyro_frame_callback(frame: Frame):
    if frame is None:
        return
    global stop_gyro, last_gyro_ts, last_gyro_global_ts
    if stop_gyro:
        return
    gyro_frame: GyroFrame = frame.as_gyro_frame()
    if gyro_frame is not None:
        timestamp = gyro_frame.get_timestamp_us()
        global_timestamp = gyro_frame.get_global_timestamp_us()
        index = gyro_frame.get_index()
        timestamp_diff = timestamp - last_gyro_ts if last_gyro_ts != 0 else 0
        global_timestamp_diff = global_timestamp - last_gyro_global_ts if last_gyro_global_ts != 0 else 0
        gyro_writer.writerow([index, timestamp,  global_timestamp, timestamp_diff, global_timestamp_diff])
        last_gyro_ts = timestamp
        last_gyro_global_ts = global_timestamp

def on_accel_frame_callback(frame: Frame):
    if frame is None:
        return
    global stop_accel, last_accel_ts, last_accel_global_ts
    if stop_accel:
        return
    accel_frame: AccelFrame = frame.as_accel_frame()
    if accel_frame is not None:
        timestamp = accel_frame.get_timestamp_us()
        global_timestamp = accel_frame.get_global_timestamp_us()
        index = accel_frame.get_index()
        timestamp_diff = timestamp - last_accel_ts if last_accel_ts != 0 else 0
        global_timestamp_diff = global_timestamp - last_accel_global_ts if last_accel_global_ts != 0 else 0
        accel_writer.writerow([index, timestamp,global_timestamp, timestamp_diff, global_timestamp_diff])
        last_accel_ts = timestamp
        last_accel_global_ts = global_timestamp

def main():
    ctx: Context = Context()
    device_list: DeviceList = ctx.query_devices()
    if device_list.get_count() == 0:
        print("No device connected")
        gyro_csv_file.close()
        accel_csv_file.close()
        return
    device: Device = device_list.get_device_by_index(0)
    sensor_list: SensorList = device.get_sensor_list()
    try:
        gyro_senor = sensor_list.get_sensor_by_type(OBSensorType.GYRO_SENSOR)
        if gyro_senor is None:
            print("No gyro sensor")
            gyro_csv_file.close()
            accel_csv_file.close()
            return
        gyro_profile_list: StreamProfileList = gyro_senor.get_stream_profile_list()
        gyro_profile: StreamProfile = gyro_profile_list.get_stream_profile_by_index(0)
        assert gyro_profile is not None
        gyro_senor.start(gyro_profile, on_gyro_frame_callback)
        gyro_profile = gyro_profile.as_gyro_stream_profile()
        print("Gyro profile: sample rate: ", gyro_profile.get_sample_rate())
        print("Gyro profile: full scale range: ", gyro_profile.get_full_scale_range())
    except OBError as e:
        print(e)
        gyro_csv_file.close()
        accel_csv_file.close()
        return
    try:
        accel_sensor = sensor_list.get_sensor_by_type(OBSensorType.ACCEL_SENSOR)
        if accel_sensor is None:
            print("No accel sensor")
            gyro_csv_file.close()
            accel_csv_file.close()
            return
        accel_profile_list: StreamProfileList = accel_sensor.get_stream_profile_list()
        accel_profile: StreamProfile = accel_profile_list.get_stream_profile_by_index(0)
        assert accel_profile is not None
        accel_sensor.start(accel_profile, on_accel_frame_callback)
        accel_profile = accel_profile.as_accel_stream_profile()
        print("Accel profile: sample rate: ", accel_profile.get_sample_rate())
        print("Accel profile: full scale range: ", accel_profile.get_full_scale_range())
    except OBError as e:
        print(e)
        gyro_csv_file.close()
        accel_csv_file.close()
        return
    pipeline = Pipeline(device)
    config = Config()

    try:
        profile_list = pipeline.get_stream_profile_list(OBSensorType.COLOR_SENSOR)
        color_profile = profile_list.get_default_video_stream_profile()
        config.enable_stream(color_profile)
        profile_list = pipeline.get_stream_profile_list(OBSensorType.DEPTH_SENSOR)
        depth_profile = profile_list.get_default_video_stream_profile()
        config.enable_stream(depth_profile)
    except Exception as e:
        print(e)
        return

    pipeline.start(config)
    pipeline.enable_frame_sync()

    last_time = time.time()
    while True:
        try:
            frames = pipeline.wait_for_frames(100)
            if not frames:
                continue
            color_frame = frames.get_color_frame()
            depth_frame = frames.get_depth_frame()
            if not color_frame or not depth_frame:
                continue
            if time.time() - last_time > 5.0:
                print("get color and depth frame")
                print("color frame timestamp: ", color_frame.get_timestamp())
                print("depth frame timestamp: ", depth_frame.get_timestamp())
                last_time = time.time()

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
            gyro_csv_file.close()
            accel_csv_file.close()
            break

if __name__ == "__main__":
    main()
