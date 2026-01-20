# ******************************************************************************
#  Copyright (c) 2024 Orbbec 3D Technology, Inc
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
# ******************************************************************************
import os
import sys
import time
import numpy as np

from pyorbbecsdk import *
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import is_lidar_device

ESC_KEY = 27
frame_count = 0

# Select a device from the list; prints device details and returns the selected device object
def select_device(device_list):
    dev_count = device_list.get_count()
    print("Device list: ")
    for i in range(dev_count):
        print(f"{i}. name: {device_list.get_device_name_by_index(i)}, "
              f"vid: 0x{hex(device_list.get_device_vid_by_index(i))}, "
              f"pid: 0x{hex(device_list.get_device_pid_by_index(i))}, "
              f"sn: {device_list.get_device_serial_number_by_index(i)}")
    
    while True:
        try:
            input_str = input("Select a device index: ")
            dev_index = int(input_str)
            if 0 <= dev_index < dev_count:
                return device_list.get_device_by_index(dev_index)
        except ValueError:
            pass
        print("Invalid selection, please reselect.")

# Select sensors to enable from the device sensor list
def select_sensors(device):
    selected_sensors = []
    while True:
        print("Sensor list: ")
        sensor_list = device.get_sensor_list()
        count = sensor_list.get_count()
        for index in range(0, count):
            sensor_type = sensor_list.get_sensor_by_index(index).get_type()
            print(f" - {index}.sensor type: {sensor_type}")
            
        print(f" - {count}.all sensors")
        print(f"Select a sensor to enable (input sensor index, '{count}' to select all sensors): ")
        
        try:
            sensor_selected = int(input())
        except:
            print("Invalid input, please enter a number!")
            continue
        
        if sensor_selected > count or sensor_selected < 0:
            if sensor_selected == -1:
                break
            else:
                print("Invalid input, please reselect the sensor!")
                continue
        
        # Add all sensors if selected, otherwise add specific sensor
        if sensor_selected == count:
            for index in range(0, count):
                sensor = sensor_list.get_sensor_by_index(index)
                selected_sensors.append(sensor)
        else:
            sensor = sensor_list.get_sensor_by_index(sensor_selected)
            selected_sensors.append(sensor)
        break
    
    return selected_sensors
    
# Print IMU (Accel/Gyro) data values, timestamp, and temperature
def print_imu_value(frame, unit_str):
    data = frame.get_value()
    frame_type = frame.get_type()
    type_str = "Accel" if frame_type == OBFrameType.ACCEL_FRAME else "Gyro"
    
    print(f"frame index: {frame.get_index()}")
    print(f"{type_str} Frame: \n{{\n"
          f"  tsp = {frame.get_timestamp_us()}\n"
          f"  temperature = {frame.get_temperature()}\n"
          f"  {type_str}.x = {data.x}{unit_str}\n"
          f"  {type_str}.y = {data.y}{unit_str}\n"
          f"  {type_str}.z = {data.z}{unit_str}\n"
          f"}}\n")

# Process and print LiDAR point cloud frame info based on the frame format
def print_lidar_point_cloud_info(frame):
    point_format = frame.get_format()
    # Check for valid LiDAR point formats
    if point_format not in [OBFormat.LIDAR_SPHERE_POINT, OBFormat.LIDAR_POINT, OBFormat.LIDAR_SCAN]:
        print("LiDAR point cloud format invalid")
        return

    min_point_value = 1e-6
    valid_point_count = 0
    data = frame.get_data()

    # Case: Sphere coordinates (distance, theta, phi)
    if point_format == OBFormat.LIDAR_SPHERE_POINT:
        points = np.frombuffer(data, dtype=[('distance', 'f4'), ('theta', 'f4'), ('phi', 'f4'), ('reflectivity', 'u1'), ('tag', 'u1')])
        
        dist = points['distance']
        theta_rad = np.radians(points['theta'])
        phi_rad = np.radians(points['phi'])
        
        cos_phi = np.cos(phi_rad)
        x = dist * np.cos(theta_rad) * cos_phi
        y = dist * np.sin(theta_rad) * cos_phi
        z = dist * np.sin(phi_rad)
        
        mask = (dist >= min_point_value) & np.isfinite(x) & np.isfinite(y) & np.isfinite(z)
        valid_point_count = np.sum(mask)

    # Case: Standard Cartesian coordinates (x, y, z)
    elif point_format == OBFormat.LIDAR_POINT:
        points = np.frombuffer(data, dtype=[
            ('x', 'f4'), ('y', 'f4'), ('z', 'f4'), 
            ('reflectivity', 'u1'), ('tag', 'u1')
        ])
        x, y, z = points['x'], points['y'], points['z']
        mask = (np.abs(z) >= min_point_value) & np.isfinite(x) & np.isfinite(y) & np.isfinite(z)
        valid_point_count = np.sum(mask)
                
    # Case: 2D Laser Scan (angle, distance)
    elif point_format == OBFormat.LIDAR_SCAN:
        points = np.frombuffer(data, dtype=[('angle', 'f4'), ('distance', 'f4'), ('intensity', 'u2')])
        
        dist = points['distance']
        angle_rad = np.radians(points['angle'])
            
        x = dist * np.cos(angle_rad)
        y = dist * np.sin(angle_rad)
        
        mask = (dist >= min_point_value) & np.isfinite(x) & np.isfinite(y)
        valid_point_count = np.sum(mask)

    if valid_point_count == 0:
        print("LiDAR point cloud vertices is zero")
        return

    print(f"frame index: {frame.get_index()}")
    print(f"LiDAR PointCloud Frame: \n{{\n"
          f"  tsp = {frame.get_timestamp_us()}\n"
          f"  format = {point_format}\n"
          f"  valid point count = {valid_point_count}\n"
          f"}}\n")

# Select and configure stream profiles for the selected sensors
def select_streams(device, config):
    selected_sensors = select_sensors(device)
    if not selected_sensors:
        print("No sensor selected")
        return
    
    for sensor in selected_sensors:
        stream_profile_list = sensor.get_stream_profile_list()
        count = stream_profile_list.get_count()
        if count == 0:
            print(f"No stream profile found for sensor: {sensor.get_type()}")
    
        print(f"Stream profile list for sensor: {sensor.get_type()}")
        for index in range(0, count):
            profile = stream_profile_list.get_stream_profile_by_index(index)
            # Differentiate profiles based on sensor type
            if sensor.get_type() == OBSensorType.ACCEL_SENSOR:
                acc_profile = profile.as_accel_stream_profile()
                acc_rate = acc_profile.get_sample_rate()
                print(f" - {index}.acc rate: {acc_rate}")
                
            elif sensor.get_type() == OBSensorType.GYRO_SENSOR:
                gyro_profile = profile.as_gyro_stream_profile()
                gyro_rate = gyro_profile.get_sample_rate()
                print(f" - {index}.gyro rate: {gyro_rate}")
    
            elif sensor.get_type() == OBSensorType.LIDAR_SENSOR:
                lidar_profile = profile.as_lidar_stream_profile()
                format_name = lidar_profile.get_format()
                scan_rate = lidar_profile.get_scan_rate()
                print(f" - {index}.format: {format_name}, scan rate: {scan_rate}")
                
            else:
                continue
            
        print("Select a stream profile to enable (input stream profile index): ")
        while True:
            stream_profile_selected = int(input())
            if stream_profile_selected >= count or stream_profile_selected < -1:
                print("Invalid input, please reselect the stream profile!")
                continue
            if stream_profile_selected == -1:
                break
            
            # Enable the selected stream profile in the config
            selected_stream_profile = stream_profile_list.get_stream_profile_by_index(stream_profile_selected)
            config.enable_stream(selected_stream_profile)
            break

# Callback function to process new FrameSets from the Pipeline
def on_new_frame_set(frames):
    global frame_count
    if frames is None:
        return

    for i in range(frames.get_count()):
        frame = frames.get_frame_by_index(i)
        if frame is None: 
            continue

        # Print frame information every 50 frames to avoid spamming the console
        if frame_count % 50 == 0:
            f_type = frame.get_type()
            if f_type == OBFrameType.LIDAR_POINTS_FRAME:
                print_lidar_point_cloud_info(frame.as_lidar_points_frame())
            elif f_type == OBFrameType.ACCEL_FRAME:
                print_imu_value(frame.as_accel_frame(), "m/s^2")
            elif f_type == OBFrameType.GYRO_FRAME:
                print_imu_value(frame.as_gyro_frame(), "rad/s")

    frame_count += 1

def main():
    try:
        pipe = None
        # Create context and query connected devices
        ctx = Context()
        device_list = ctx.query_devices()
        
        if device_list.get_count() <= 0:
            print("Device Not Found")
            return

        # Select a device (default to the first one if only one exists)
        device = None
        if device_list.get_count() == 1:
            device = device_list.get_device_by_index(0)
        else:
            device = select_device(device_list)

        # Validate that the device is a LiDAR device
        if not is_lidar_device(device):
            print("Invalid device, please connect a LiDAR device!")
            return

        # Create Pipeline and Config
        pipe = Pipeline(device)
        config = Config()

        # Display current device information
        dev_info = device.get_device_info()
        print("-" * 50)
        print(f"Current Device: name: {dev_info.get_name()}, VID: {hex(dev_info.get_vid())}, PID: {hex(dev_info.get_pid())}, "
              f"UID: {dev_info.get_uid()}, Serial Number: {dev_info.get_serial_number()}, Connection Type: {dev_info.get_connection_type()}")

        # Attempt to read the LiDAR IP Address
        try:
            ip_address = device.get_device_info().get_device_ip_address()
            print(f"LiDAR IP Address: {ip_address}")
        except:
            print("Could not read LiDAR IP Address")

        # Set specific LiDAR property (Tail Filter Level)
        device.set_int_property(OBPropertyID.OB_PROP_LIDAR_TAIL_FILTER_LEVEL_INT, 0)

        # Let user select sensors and stream profiles
        select_streams(device, config)

        # Ensure that FrameSets output contain all required frame types
        config.set_frame_aggregate_output_mode(OBFrameAggregateOutputMode.FULL_FRAME_REQUIRE)
        
        # Start the pipeline with the selected config and frame callback
        pipe.start(config, on_new_frame_set)

        print("The stream is started!")
        print("Press Ctrl+C to exit!\n")

        # Keep the main thread alive
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nStopping...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Properly stop the pipeline on exit
        if pipe is not None:
            pipe.stop()

if __name__ == "__main__":
    main()