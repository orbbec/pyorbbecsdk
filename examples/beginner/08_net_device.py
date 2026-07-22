# ******************************************************************************
#  pyorbbecsdk Beginner Example 08 — Network Camera (Net Device)
#
#  What you will learn:
#    1. How to connect to an Orbbec camera over a network (Ethernet / Wi-Fi)
#    2. How to stream H.264 or MJPG color video and decode it with PyAV
#    3. How to display the live network stream using pygame
#
#  Device requirement: Gemini 335Le / Gemini 435Le (network-capable models)
#
#  Run:
#    python examples/beginner/08_net_device.py
# ******************************************************************************

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import threading
import time

import av
import cv2
import pygame
from utils import frame_to_bgr_image, resize_to_fit

from pyorbbecsdk import Config, Context, OBError, OBFormat, OBSensorType, Pipeline

ESC_KEY = 27
# Gemini 335Le
GEMINI_335LE_PRODUCT_ID = 0x080E
# Gemini 435Le
GEMINI_435LE_PRODUCT_ID = 0x0815


def get_stream_profile(pipeline, sensor_type, width, height, fmt, fps):
    profile_list = pipeline.get_stream_profile_list(sensor_type)
    try:
        profile = profile_list.get_video_stream_profile(width, height, fmt, fps)
    except OBError:
        profile = profile_list.get_default_video_stream_profile()
    return profile


def decode_h26x_frame(decoder, byte_data):
    try:
        packet = av.Packet(byte_data)
        frames = decoder.decode(packet)
        for frame in frames:
            return frame.to_ndarray(format="bgr24")
    except av.AVError as e:
        print(f"Decoding error: {e}")
    return None


class FrameProcessor(threading.Thread):
    def __init__(self, decoder, display_width, display_height):
        super().__init__()
        self.decoder = decoder
        self.latest_frame = None
        self.processed_frame = None
        self.lock = threading.Lock()
        self.running = True
        self.daemon = True
        self.display_width = display_width
        self.display_height = display_height

    def run(self):
        while self.running:
            with self.lock:
                if self.latest_frame is not None:
                    color_image = decode_h26x_frame(self.decoder, self.latest_frame)
                    if color_image is not None:
                        # Resize to fit the display, preserving aspect ratio
                        resized_image = resize_to_fit(color_image, self.display_width, self.display_height)
                        rgb_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
                        self.processed_frame = rgb_image
                    self.latest_frame = None
            time.sleep(0.001)

    def update_frame(self, frame):
        with self.lock:
            self.latest_frame = frame

    def get_processed_frame(self):
        with self.lock:
            return self.processed_frame

    def stop(self):
        self.running = False


def main():
    ctx = Context()
    ip = input("Enter the IP address of the device (default: 192.168.1.10): ") or "192.168.1.10"
    device = ctx.create_net_device(ip, 8090)
    if device is None:
        print("Failed to create net device")
        return

    config = Config()
    pipeline = Pipeline(device)

    device_info = device.get_device_info()
    # Gemini 335Le, Gemini 435Le
    SUPPORTED_PIDS = {GEMINI_435LE_PRODUCT_ID, GEMINI_335LE_PRODUCT_ID}
    if device_info.get_pid() in SUPPORTED_PIDS:
        # Set up 1280*800 capture
        print("Current device is GEMINI 435Le or GEMINI 335Le, use OBFormat.MJPG")
        color_profile = get_stream_profile(pipeline, OBSensorType.COLOR_SENSOR, 1280, 800, OBFormat.MJPG, 10)
    else:
        # Set up 4K capture
        color_profile = get_stream_profile(pipeline, OBSensorType.COLOR_SENSOR, 3840, 2160, OBFormat.H264, 25)

    config.enable_stream(color_profile)
    pipeline.start(config)

    # Choose the correct decoder based on the format
    if color_profile.get_format() == OBFormat.H264:
        color_codec_name = "h264"
    elif color_profile.get_format() == OBFormat.MJPG:
        color_codec_name = "mjpeg"
    else:
        color_codec_name = "hevc"

    try:
        decoder = av.codec.CodecContext.create(color_codec_name, "r")
    except av.AVError as e:
        print(f"Failed to create decoder for {color_codec_name}: {e}")
        pipeline.stop()
        return

    # Set display resolution to 720p
    display_width, display_height = 1280, 720
    frame_processor = FrameProcessor(decoder, display_width, display_height)
    frame_processor.start()

    pygame.init()
    screen = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption("4K Net Device Viewer (720p Display)")
    clock = pygame.time.Clock()

    running = True
    try:
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

            if not running:
                break

            frames = pipeline.wait_for_frames(1000)
            if frames:
                color_frame = frames.get_color_frame()
                if color_frame:
                    byte_data = color_frame.get_data()
                    if len(byte_data) > 0:
                        frame_processor.update_frame(byte_data)

            processed_frame = frame_processor.get_processed_frame()
            if processed_frame is not None:
                surf = pygame.surfarray.make_surface(processed_frame.swapaxes(0, 1))
                screen.blit(surf, (0, 0))
                pygame.display.flip()

            clock.tick(30)  # Limit to 30 FPS

    finally:
        print("Stopping frame processor...")
        frame_processor.stop()
        print("Stopping pipeline...")
        pipeline.stop()
        print("Exiting the program...")
        os._exit(0)


if __name__ == "__main__":
    main()
