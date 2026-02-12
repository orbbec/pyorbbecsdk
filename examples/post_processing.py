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
import sys
import cv2
import time
import numpy as np
from threading import Thread
from pyorbbecsdk import *

# --- Configuration Constants ---
ESC_KEY = 27
WINDOW_NAME = "PostProcessing (Left: Original, Right: Processed)"
MIN_DEPTH = 20      # Minimum depth value in mm
MAX_DEPTH = 10000   # Maximum depth value in mm

# Global control flag to synchronize program exit across threads
quit_program = False

def print_filters_info(filters):
    """
    Print information about recommended filters, including their current status
    and configuration schema (parameters, ranges, and defaults).
    """
    print(f"{len(filters)} post processing filters recommended:")
    for filter in filters:
        status = "enabled" if filter.is_enabled() else "disabled"
        print(f" - {filter.get_name()}: {status}")
        config_schema_vec = filter.get_config_schema_vec()
        for config_schema in config_schema_vec:
            # Print detailed schema for each parameter of the filter
            print(f" - {{{config_schema.name}, {config_schema.type}, {config_schema.min}, {config_schema.max}, {config_schema.step}, {config_schema.default}, {config_schema.desc}}}") 
        # By default, disable filters to allow user to enable them manually
        filter.enable(False)

def filter_control(filter_list):
    """
    CLI Control Thread: Allows users to interactively enable/disable filters 
    and modify parameter values via the terminal while the video runs.
    """
    global quit_program
    def print_help():
        print("Available commands:")
        print("- Enter `[Filter]` to list the current config values for the filter")
        print("- Enter `[Filter] on` or `[Filter] off` to enable/disable the filter")
        print("- Enter `[Filter] list` to list the config schema for the filter")
        print("- Enter `[Filter] [Config]` to show the config values for the filter")
        print("- Enter `[Filter] [Config] [Value]` to set a config value")
        print("- Enter `L` or `l` to list all available filters")
        print("- Enter `H` or `h` to print this help message")
        print("- Enter `Q` or `q` to quit")

    print_help()
    
    while not quit_program:
        print("---------------------------")
        # Use strip() to clean up whitespace from user input
        user_input = input("Enter your input (h for help): ").strip()
        
        if not user_input:
            continue
            
        if user_input.lower() == 'q':
            quit_program = True
            break
        elif user_input.lower() == 'l':
            print_filters_info(filter_list)
            continue
        elif user_input.lower() == 'h':
            print_help()
            continue

        # Split input into tokens for command parsing
        tokens = user_input.split()
        if not tokens:
            continue

        target_filter_name = tokens[0]
        found_filter = None
        
        # Search for the requested filter in the recommended list
        for f in filter_list:
            if f.get_name() == target_filter_name:
                found_filter = f
                break
        
        if found_filter:
            # Case 1: [Filter] -> Show all current parameter values
            if len(tokens) == 1:
                print(f"Config values for {found_filter.get_name()}:")
                schema_vec = found_filter.get_config_schema_vec()
                for schema in schema_vec:
                    val = found_filter.get_config_value(schema.name)
                    print(f" - {schema.name}: {val}")
            
            # Case 2: [Filter] on/off -> Toggle filter state
            elif len(tokens) == 2 and tokens[1].lower() in ["on", "off"]:
                is_on = tokens[1].lower() == "on"
                found_filter.enable(is_on)
                status = "enabled" if found_filter.is_enabled() else "disabled"
                print(f"Success: Filter {found_filter.get_name()} is now {status}")
            
            # Case 3: [Filter] list -> Show technical schema details
            elif len(tokens) == 2 and tokens[1].lower() == "list":
                print(f"Config schema for {found_filter.get_name()}:")
                schema_vec = found_filter.get_config_schema_vec()
                for s in schema_vec:
                    print(f" - {{{s.name}, {s.type}, {s.min}, {s.max}, {s.step}, {s.default}, {s.desc}}}")
            
            # Case 4: [Filter] [Config Name] -> Get specific parameter value
            elif len(tokens) == 2:
                schema_vec = found_filter.get_config_schema_vec()
                target_config = tokens[1]
                found_config = False
                for s in schema_vec:
                    if s.name == target_config:
                        val = found_filter.get_config_value(s.name)
                        print(f"Config values for {found_filter.get_name()}@{s.name}: {val}")
                        found_config = True
                        break
                if not found_config:
                    print(f"Error: Config {target_config} not found for filter {target_filter_name}", file=sys.stderr)
            
            # Case 5: [Filter] [Config Name] [Value] -> Set parameter value
            elif len(tokens) == 3:
                try:
                    config_name = tokens[1]
                    value = float(tokens[2])
                    found_filter.set_config_value(config_name, value)
                    print(f"Success: Config value of {config_name} for filter {target_filter_name} is set to {tokens[2]}")
                except ValueError:
                    print(f"Error: '{tokens[2]}' is not a valid number", file=sys.stderr)
                except Exception as e:
                    print(f"Error: {e}", file=sys.stderr)
        else:
            print(f"Error: Filter {target_filter_name} not found", file=sys.stderr)
        
        # Brief sleep to prevent high CPU usage in the input loop
        time.sleep(0.5)

def main():
    global quit_program
    try:
        # Initialize the Orbbec pipeline and stream configuration
        pipeline = Pipeline()
        config = Config()
        
        # Access the depth sensor and retrieve device-recommended filters (Decimation, Hole-filling, etc.)
        device = pipeline.get_device()
        sensor = device.get_sensor(OBSensorType.DEPTH_SENSOR)
        filters = sensor.get_recommended_filters()
        
        # Show initial filters information
        print_filters_info(filters)
        
        # Enable depth stream and start the pipeline
        config.enable_stream(OBStreamType.DEPTH_STREAM)
        pipeline.start(config)
        
        # Start the background control thread for terminal input
        control_thread = Thread(target=filter_control, args=(filters,))
        control_thread.daemon = True
        control_thread.start()
        
        print("Press 'ESC' on the window to exit.")
        
        while not quit_program:
            # Wait for frameset from the pipeline
            frames = pipeline.wait_for_frames(1000)
            if frames is None:
                continue
            depth_frame = frames.get_depth_frame()
            if depth_frame is None:
                continue
            
            # Apply enabled filters sequentially (Filter Chain)
            processed_frame = depth_frame
            for f in filters:
                if f.is_enabled():
                    processed_frame = f.process(processed_frame)
            
            if processed_frame is None:
                continue
            
            # Re-cast processed result back to depth frame format
            processed_frame = processed_frame.as_depth_frame()                    
            
            # --- Process Original Frame for Display ---
            depth_data = np.frombuffer(depth_frame.get_data(), dtype=np.uint16)
            depth_data = depth_data.reshape(depth_frame.get_height(), depth_frame.get_width())
            # Normalize 16-bit depth to 8-bit for visualization
            depth_image = cv2.normalize(depth_data, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
            depth_image = cv2.applyColorMap(depth_image, cv2.COLORMAP_JET)
            
            # --- Process Filtered Frame for Display ---
            processed_data = np.frombuffer(processed_frame.get_data(), dtype=np.uint16)
            processed_data = processed_data.reshape(processed_frame.get_height(), processed_frame.get_width())
            processed_image = cv2.normalize(processed_data, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
            processed_image = cv2.applyColorMap(processed_image, cv2.COLORMAP_JET)
            
            # --- Render Side-by-Side View ---
            combined_view = np.hstack((depth_image, processed_image))
            cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
            cv2.resizeWindow(WINDOW_NAME, 1280, 720)
            cv2.imshow(WINDOW_NAME, combined_view)
            
            # Listen for escape or quit keys in the UI window
            key = cv2.waitKey(1)
            if key in [ord('q'), ESC_KEY]:
                break
                
    except OBError as e:
        print(f"SDK Error: {e}")
    finally:
        # Cleanup: Signal threads to stop, stop the pipeline, and close windows
        quit_program = True
        pipeline.stop()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()