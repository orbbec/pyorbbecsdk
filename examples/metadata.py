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

from pyorbbecsdk import *

ESC_KEY = 27

def main():
    # Initialize Pipeline
    pipeline = Pipeline()
    # Start Pipeline
    pipeline.start()
    print("Pipeline started. Press Ctrl+C to exit.")

    frame_counter = 0  # Add frame counter
    
    while True:
        try:
            # Get frameSet from Pipeline
            frame_set = pipeline.wait_for_frames(1000)
            if frame_set is None:
                continue

            frame_counter += 1  # Increment counter
            
            # Only print metadata every 30 frames
            if frame_counter % 30 == 0:
                for i in range(len(frame_set)):
                    frame = frame_set[i]

                    # Print frame metadata
                    print(f"Frame type: {frame.get_type()}")
                    metadata_types = [getattr(OBFrameMetadataType, attr) for attr in dir(OBFrameMetadataType) 
                                    if not attr.startswith('__') and isinstance(getattr(OBFrameMetadataType, attr), OBFrameMetadataType)]
                    
                    for metadata_type in metadata_types:
                        if frame.has_metadata(metadata_type):
                            metadata_value = frame.get_metadata_value(metadata_type)
                            print(f"  Metadata type: {metadata_type.name}, value: {metadata_value}")

        except KeyboardInterrupt:
            break
        except Exception as e:
            print("An error occurred:", e)
            break

    pipeline.stop()
    print("Pipeline stopped.")

if __name__ == "__main__":
    main()
