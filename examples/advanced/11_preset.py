# ******************************************************************************
#  pyorbbecsdk Advanced Example 11 — Named Depth Presets
#
#  What you will learn:
#    1. Query the device for all available named depth presets
#    2. Load and apply a preset by name (e.g., Default, Hand, High Accuracy)
#    3. Switch between presets at runtime without restarting the pipeline
#    4. Observe how different presets affect depth range, fill rate, and noise
#
#  Device requirement: Gemini 330 series
#
#  Run:
#    python examples/advanced/11_preset.py
# ******************************************************************************
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pyorbbecsdk as ob


def main():
    # Check if device is connected
    ctx = ob.Context()
    device_list = ctx.query_devices()
    if device_list.get_count() == 0:
        print("Device Not Found! Please connect an Orbbec camera and try again.")
        return

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
