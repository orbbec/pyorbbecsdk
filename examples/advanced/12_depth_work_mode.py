# ******************************************************************************
#  pyorbbecsdk Advanced Example 12 — Depth Work Mode Switching
#
#  What you will learn:
#    1. List all depth work modes supported by the connected device
#    2. Select and apply a work mode (High Accuracy, High Density, Medium Density)
#    3. Switch work modes at runtime and restart the pipeline to apply changes
#    4. Understand the trade-offs between accuracy, density, and frame rate
#
#  Device requirement: Gemini 2, Gemini 2L, Astra 2, Gemini 2 XL
#
#  Run:
#    python examples/advanced/12_depth_work_mode.py
# ******************************************************************************
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from pyorbbecsdk import Context, OBPermissionType, OBPropertyID, Pipeline  # type: ignore

ESC = 27


def main():
    # Check if device is connected
    ctx = Context()
    device_list = ctx.query_devices()
    if device_list.get_count() == 0:
        print("Device Not Found! Please connect an Orbbec camera and try again.")
        return

    pipeline = Pipeline()
    assert pipeline is not None
    device = pipeline.get_device()
    assert device is not None
    if not device.is_property_supported(
        OBPropertyID.OB_STRUCT_CURRENT_DEPTH_ALG_MODE,
        OBPermissionType.PERMISSION_READ_WRITE,
    ):
        print("Current device not support depth work mode!")
        return
    current_depth_work_mode = device.get_depth_work_mode()
    assert current_depth_work_mode is not None
    print("Current depth work mode: ", current_depth_work_mode)
    depth_work_mode_list = device.get_depth_work_mode_list()
    assert depth_work_mode_list is not None
    for i in range(depth_work_mode_list.get_count()):
        depth_work_mode = depth_work_mode_list.get_depth_work_mode_by_index(i)
        assert depth_work_mode is not None
        print("{}. {}".format(i, depth_work_mode))
    if depth_work_mode_list.get_count() > 1:
        try:
            index = int(input("Please input depth work mode index: "))
        except ValueError:
            print("Invalid input: Please enter an integer.")
            return
        if depth_work_mode_list.get_count() > index >= 0:
            select_depth_work_mode = depth_work_mode_list.get_depth_work_mode_by_index(index)
            assert select_depth_work_mode is not None
            device.set_depth_work_mode(select_depth_work_mode.name)
            current_depth_work_mode = device.get_depth_work_mode()
            if current_depth_work_mode.name != select_depth_work_mode.name:
                print("Set depth work mode failed!")
            else:
                print("Set depth work mode to {} success!".format(select_depth_work_mode))
        else:
            print("Invalid input: index is out of range!")


if __name__ == "__main__":
    main()
