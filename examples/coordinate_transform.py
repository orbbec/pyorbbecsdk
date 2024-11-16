# ******************************************************************************
#  Copyright (c) 2024 Orbbec 3D Technology, Inc
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

import numpy as np

import pyorbbecsdk as ob

ESC_KEY = 27


def print_help():
    print("Supported commands:")
    print("Press '1' to transform 2D point to 2D point")
    print("Press '2' to transform 2D point to 3D point")
    print("Press '3' to transform 3D point to 3D point")
    print("Press '4' to transform 3D point to 2D point")
    print("--------------------------------------------")
    print("Press Ctrl+C to exit the program")


def get_frame_data(color_frame, depth_frame):
    color_frame = color_frame.as_video_frame()
    depth_frame = depth_frame.as_video_frame()

    depth_width = depth_frame.get_width()
    depth_height = depth_frame.get_height()

    color_profile = color_frame.get_stream_profile()
    depth_profile = depth_frame.get_stream_profile()
    print("video profile:", color_profile.as_video_stream_profile())
    color_intrinsics = color_profile.as_video_stream_profile().get_intrinsic()
    color_distortion = color_profile.as_video_stream_profile().get_distortion()
    depth_intrinsics = depth_profile.as_video_stream_profile().get_intrinsic()
    depth_distortion = depth_profile.as_video_stream_profile().get_distortion()

    extrinsic = depth_profile.get_extrinsic_to(color_profile)

    depth_data = np.frombuffer(depth_frame.get_data(), dtype=np.uint16).reshape(depth_height, depth_width)

    return (color_intrinsics, color_distortion, depth_intrinsics, depth_distortion,
            extrinsic, depth_data, depth_width, depth_height)


def transform_points(transform_func, color_frame, depth_frame, dimension):
    (color_intrinsics, color_distortion, depth_intrinsics, depth_distortion,
     extrinsic, depth_data, depth_width, depth_height) = get_frame_data(color_frame, depth_frame)

    convert_width, convert_height = 3, 3
    for i in range(depth_width // 2, depth_width // 2 + convert_width):
        for j in range(depth_height // 2, depth_height // 2 + convert_height):
            depth = depth_data[j, i]
            x, y = float(i), float(j)
            original_point = (x, y, depth)
            if depth > 0:
                if dimension == "2d_to_2d":
                    res = transform_func(ob.OBPoint2f(x, y), depth, depth_intrinsics, depth_distortion,
                                         color_intrinsics, color_distortion, extrinsic)
                elif dimension == "2d_to_3d":
                    res = transform_func(ob.OBPoint2f(x, y), depth, depth_intrinsics, extrinsic)
                elif dimension == "3d_to_3d":
                    res = transform_func(ob.OBPoint3f(x, y, depth), extrinsic)
                elif dimension == "3d_to_2d":
                    res = transform_func(ob.OBPoint3f(x, y, depth), color_intrinsics, color_distortion, extrinsic)
                print(f"\n--- {dimension.replace('_', ' to ')} Point Transformation ---")
                print(f"Original point: {original_point}")
                print(f"Transformed point: {res}")
                print(f"--------------------------------------------")
            else:
                print("Depth is 0")


from pynput import keyboard

# Global variable to track the key that was pressed
key_pressed = None


def on_press(key):
    global key_pressed
    try:
        # Try to get the character key that was pressed
        key_pressed = key.char
    except AttributeError:
        # Handle special keys like 'ESC'
        if key == keyboard.Key.esc:
            key_pressed = 'esc'


def main():
    print_help()  # Display help menu
    config = ob.Config()  # Initialize the config for the pipeline
    pipeline = ob.Pipeline()  # Create the pipeline object

    try:
        # Enable depth and color sensors
        for sensor_type in [ob.OBSensorType.DEPTH_SENSOR, ob.OBSensorType.COLOR_SENSOR]:
            profile_list = pipeline.get_stream_profile_list(sensor_type)
            assert profile_list is not None
            profile = profile_list.get_default_video_stream_profile()
            assert profile is not None
            print(f"{sensor_type} profile:", profile)
            config.enable_stream(profile)  # Enable the stream for the sensor
    except Exception as e:
        print(e)
        return

    print("start pipeline")
    pipeline.start(config)  # Start the pipeline with the config

    # Dictionary mapping key input to transformation functions and dimension types
    transform_functions = {
        '1': (ob.transformation2dto2d, "2d_to_2d"),
        '2': (ob.transformation2dto3d, "2d_to_3d"),
        '3': (ob.transformation3dto3d, "3d_to_3d"),
        '4': (ob.transformation3dto2d, "3d_to_2d")
    }

    # Start the keyboard listener to capture key presses
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    while True:
        try:
            # Wait for frames from the pipeline (with a timeout of 100 ms)
            frames = pipeline.wait_for_frames(100)
            if frames is None:
                continue

            # Get depth and color frames from the captured frames
            depth_frame = frames.get_depth_frame()
            color_frame = frames.get_color_frame()

            # Skip iteration if depth or color frame is not available
            if depth_frame is None or color_frame is None:
                continue

            # check depth frame data size, if not match, print error
            depth_width = depth_frame.get_width()
            depth_height = depth_frame.get_height()
            depth_data_size = depth_frame.get_data_size()
            if depth_data_size != depth_width * depth_height * 2:
                print("Error: depth frame data size does not match")
                continue

            # Check if a key was pressed
            global key_pressed
            if key_pressed:
                # Convert the pressed key to lowercase
                key = key_pressed.lower()
                key_pressed = None  # Reset key_pressed after handling it

                # Check if the key corresponds to a transformation function
                if key in transform_functions:
                    print("Transforming points...")
                    transform_func, dimension = transform_functions[key]
                    transform_points(transform_func, color_frame, depth_frame, dimension)
                elif key in ['q', 'esc']:  # Exit if 'q' or 'esc' is pressed
                    break
                elif key == 'h':  # Display help if 'h' is pressed
                    print_help()

        except KeyboardInterrupt:
            break

    # Stop the pipeline and keyboard listener
    pipeline.stop()
    listener.stop()


if __name__ == "__main__":
    main()
