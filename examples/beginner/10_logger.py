# Copyright (c) 2024 Orbbec 3D Technology, Inc
# Licensed under the Apache License, Version 2.0

import os
import time

from pyorbbecsdk import Config, Context, OBLogLevel, OBSensorType, Pipeline


def main():
    """
    Logger Configuration Example

    This example demonstrates how to configure SDK logging.

    See LOG_CONFIGURATION.md for detailed documentation on log levels and configuration options.
    """
    # Check if device is connected
    ctx = Context()
    device_list = ctx.query_devices()
    if device_list.get_count() == 0:
        print("Device Not Found! Please connect an Orbbec camera and try again.")
        return

    # Set console logger (INFO level)
    # To disable console logging, use OBLogLevel.NONE
    Context.set_logger_to_console(OBLogLevel.INFO)

    # Set file logger (DEBUG level)
    log_path = "Log/Custom/"
    os.makedirs(log_path, exist_ok=True)
    Context.set_logger_to_file(OBLogLevel.DEBUG, log_path)

    # Configure streams
    config = Config()
    pipeline = Pipeline()

    # Get and enable depth stream
    depth_profiles = pipeline.get_stream_profile_list(OBSensorType.DEPTH_SENSOR)
    depth_profile = depth_profiles.get_default_video_stream_profile()
    config.enable_stream(depth_profile)

    # Start pipeline
    pipeline.start(config)
    time.sleep(1)
    pipeline.stop()

    print(f"\nLogs saved to: {os.path.abspath(log_path)}")
    print("Press any key to exit.")
    input()


if __name__ == "__main__":
    main()
