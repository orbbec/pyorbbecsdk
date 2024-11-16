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

import os
from pyorbbecsdk import *
import time

def main():
    # Set console logger (INFO level)
    # if you DO NOT want to see the log message in console, you can set the log level to OBLogLevel.NONE
    Context.set_logger_to_console(OBLogLevel.INFO)

    # Set file logger (DEBUG level)
    log_path = "Log/Custom/"
    os.makedirs(log_path, exist_ok=True)  # Ensure log directory exists
    Context.set_logger_to_file(OBLogLevel.INFO, log_path)


    # Configure streams
    config = Config()
    pipeline = Pipeline()
    # Get and enable depth stream configuration
    depth_profiles = pipeline.get_stream_profile_list(OBSensorType.DEPTH_SENSOR)
    depth_profile = depth_profiles.get_default_video_stream_profile()
    config.enable_stream(depth_profile)

    # Get and enable color stream configuration
    color_profiles = pipeline.get_stream_profile_list(OBSensorType.COLOR_SENSOR)
    color_profile = color_profiles.get_default_video_stream_profile()
    config.enable_stream(color_profile)

    # Start pipeline
    pipeline.start(config)
    time.sleep(1)
    # Stop pipeline
    pipeline.stop()

    print("\nPress any key to exit.")
    input()  # Wait for user input to exit

if __name__ == "__main__":
    main()
