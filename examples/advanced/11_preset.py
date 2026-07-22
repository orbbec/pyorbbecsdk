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
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pyorbbecsdk as ob

SETTLE_SEC = 1.5
CONFIRM_TIMEOUT_SEC = 5.0
MAX_RETRIES = 5
RETRY_BACKOFF_SEC = 2.0


def wait_preset_confirmed(device, preset_name, timeout_sec=CONFIRM_TIMEOUT_SEC):
    """Wait until the device reports `preset_name` as its current preset."""
    deadline = time.monotonic() + timeout_sec
    last = ""
    while time.monotonic() < deadline:
        try:
            last = device.get_current_preset_name() or ""
        except Exception:
            last = ""
        if last == preset_name:
            return
        time.sleep(0.2)
    raise RuntimeError(f"preset read-back mismatch: expected '{preset_name}', got '{last}'")


def switch_preset(device, preset_name, retries=MAX_RETRIES):
    """Load a preset and wait for the device to confirm it took effect."""
    last_err = None
    for attempt in range(1, retries + 1):
        try:
            device.load_preset(preset_name)
            time.sleep(SETTLE_SEC)
            wait_preset_confirmed(device, preset_name)
            return
        except Exception as e:
            last_err = e
            if attempt < retries:
                time.sleep(RETRY_BACKOFF_SEC)
    raise RuntimeError(f"failed to load preset '{preset_name}' after {retries} tries: {last_err}")


def main():
    pipe = None
    try:
        pipe = ob.Pipeline()
        device = pipe.get_device()
    except Exception as e:
        print("Device Not Found! Please connect an Orbbec camera and try again.")
        print(f"  ({e})")
        if pipe is not None:
            pipe.stop()
        return

    try:
        while True:
            preset_list = device.get_available_preset_list()
            if len(preset_list) == 0:
                print("The current device does not support preset mode")
                break

            print("\nAvailable Presets:")
            for index in range(len(preset_list)):
                print(f" - {index}. {preset_list[index]}")

            print(f"\nCurrent PresetName: {device.get_current_preset_name()}")

            try:
                input_option = int(input("\nEnter index of preset to load (or -1 to exit): "))
                if input_option == -1:
                    break
            except ValueError:
                print("Invalid input. Please enter a valid index.")
                continue

            preset_list = device.get_available_preset_list()
            if input_option < 0 or input_option >= len(preset_list):
                print("Invalid input. Please enter a valid index.")
                continue
            preset_name = preset_list.get_name_by_index(input_option)

            switch_preset(device, preset_name)

            print(f"\nPreset loaded. Current PresetName: {device.get_current_preset_name()}")

    except ob.OBError as e:
        print(f"Error: {str(e)}")
    except RuntimeError as e:
        print(f"Error: {str(e)}")
    finally:
        pipe.stop()


if __name__ == "__main__":
    main()
