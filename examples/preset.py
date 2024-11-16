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

import pyorbbecsdk as ob

def main():
    # Create a pipeline with default device
    pipe = ob.Pipeline()

    # Get the device from the pipeline
    device = pipe.get_device()

    try:
        while True:
            # Get preset list from device
            preset_list = device.get_available_preset_list()
            if len(preset_list) == 0:
                print("The current device does not support preset mode")
                break

            print("\nAvailable Presets:")
            for index in range(len(preset_list)):
                print(f" - {index}. {preset_list[index]}")

            # Print current preset name
            print(f"\nCurrent PresetName: {device.get_current_preset_name()}")

            # Select preset to load
            try:
                input_option = int(input("\nEnter index of preset to load (or -1 to exit): "))
                if input_option == -1:
                    break
                if input_option < 0 or input_option >= len(preset_list):
                    raise ValueError("Invalid index")
            except ValueError:
                print("Invalid input. Please enter a valid index.")
                continue

            preset_name = preset_list[input_option]

            # Load preset
            device.load_preset(preset_name)

            # Print current preset name
            print(f"\nPreset loaded. Current PresetName: {device.get_current_preset_name()}")

    except ob.OBError as e:
        print(f"Error: {str(e)}")
    finally:
        # Stop Pipeline
        pipe.stop()

if __name__ == "__main__":
    main()
