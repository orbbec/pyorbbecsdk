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
import os
import threading
from pyorbbecsdk import *
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import is_lidar_device

# Get valid .bag file path from user input
def get_rosbag_path():
    while True:
        print("Please input the path of the Rosbag file (.bag) to playback: ")
        path = input("Path: ").strip()
        
        if (path.startswith("'") and path.endswith("'")) or (path.startswith('"') and path.endswith('"')):
            path = path[1:-1]
            
        if path.lower().endswith(".bag") and os.path.exists(path):
            print(f"Playback file confirmed: {path}\n")
            return path
        
        print("Invalid file or format. Please provide an existing .bag file.\n")

class PlaybackApp:
    def __init__(self, file_path):
        self.exited = False
        self.file_path = file_path
        self.frame_count = 0
        
        # Create a playback device with a Rosbag file
        self.playback = PlaybackDevice(file_path)
        # Create a pipeline with the playback device
        self.pipe = Pipeline(self.playback)
        # Enable all recording streams from the playback device
        self.config = Config()
        
        print(f"Duration: {self.playback.get_duration()}ms")
        
        self.replay_condition = threading.Condition()
        self.play_status = OBPlaybackStatus.STOPPED

        # Set playback status change callback, when the playback stops, start the pipeline again with the same config
        self.playback.set_playback_status_change_callback(self.on_playback_status_change)

        sensor_list = self.playback.get_sensor_list()
        for i in range(sensor_list.get_count()):
            sensor_type = sensor_list.get_sensor_by_index(i).get_type()
            self.config.enable_stream(sensor_type)
        
        self.config.set_frame_aggregate_output_mode(OBFrameAggregateOutputMode.ANY_SITUATION)

    def on_playback_status_change(self, status):
        with self.replay_condition:
            self.play_status = status
            print(f"Playback status changed to: {status}")
            self.replay_condition.notify_all()

    def on_new_frame(self, frame_set):
        if self.frame_count % 20 == 0:
            for i in range(frame_set.get_count()):
                frame = frame_set.get_frame_by_index(i)
                if frame:
                    fmt = frame.get_format()
                    print(f"frame index: {frame.get_index()}, tsp: {frame.get_timestamp_us()}, format: {fmt}")
        self.frame_count += 1

    def monitor_replay(self):
        while not self.exited:
            with self.replay_condition:
                self.replay_condition.wait_for(lambda: self.exited or self.play_status == OBPlaybackStatus.STOPPED)
                
                if self.exited:
                    break
                
                if self.play_status == OBPlaybackStatus.STOPPED:
                    print("End of file reached. Replaying in 1s...")
                    self.pipe.stop()

                    # wait 1s and play again
                    self.replay_condition.wait(1.0)
                    if self.exited:
                        break
                        
                    self.play_status = OBPlaybackStatus.UNKNOWN
                    print("Replay again")
                    self.pipe.start(self.config, self.on_new_frame)

    def run(self):
        monitor_thread = threading.Thread(target=self.monitor_replay)
        monitor_thread.start()

        # Start the pipeline with the config
        self.pipe.start(self.config, self.on_new_frame)

        print("\nControls:")
        print("Press 'p' or 'P' to pause/resume.")
        print("Press 'q' or 'Ctrl+C' to exit.")

        try:
            while not self.exited:
                key = input(">> (p: Pause/Resume, q: Quit): ").strip().lower()
                
                if key == 'q':  # 'q' key to exit.
                    break
                elif key == 'p':  # 'p' or 'P' key to pause/resume playback.
                    status = self.playback.get_playback_status()
                    if status == OBPlaybackStatus.PLAYING:
                        self.playback.pause()
                        print("Playback paused")
                    elif status == OBPlaybackStatus.PAUSED:
                        self.playback.resume()
                        print("Playback resumed")
        except KeyboardInterrupt:
            pass

        # stop
        self.exited = True
        self.pipe.stop()
        with self.replay_condition:
            self.replay_condition.notify_all()
        monitor_thread.join()
        print("exit")

def main():
    try:
        file_path = get_rosbag_path()
        app = PlaybackApp(file_path)
        app.run()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()