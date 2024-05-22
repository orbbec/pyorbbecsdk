# ******************************************************************************
#  Copyright (c) 2023 Orbbec 3D Technology, Inc
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


def get_precision_level(value):
    if value == OBDepthPrecisionLevel.ONE_MM:
        return "1mm"
    elif value == OBDepthPrecisionLevel.ZERO_POINT_EIGHT_MM:
        return "0.8mm"
    elif value == OBDepthPrecisionLevel.ZERO_POINT_FOUR_MM:
        return "0.4mm"
    elif value == OBDepthPrecisionLevel.ZERO_POINT_TWO_MM:
        return "0.2mm"
    elif value == OBDepthPrecisionLevel.ZERO_POINT_ONE_MM:
        return "0.1mm"
    else:
        return "Unknown"


def set_depth_unit(device):
    level = device.get_int_property(OBPropertyID.OB_PROP_DEPTH_PRECISION_LEVEL_INT)
    print("Current depth precision level: ", get_precision_level(level))
    #  auto isHwD2DMode = device->getBoolProperty(OB_PROP_DISPARITY_TO_DEPTH_BOOL);
    is_hw_d2d_mode = device.get_bool_property(OBPropertyID.OB_PROP_DISPARITY_TO_DEPTH_BOOL)
    if is_hw_d2d_mode:
        print("Current depth unit is hardware disparity to depth mode.")
        return
    precision_support_list = device.get_depth_precision_support_list()
    print("Supported depth precision level: ")
    for i in range(len(precision_support_list)):
        print("{} . {}".format(i, get_precision_level(precision_support_list[i])))

    index = int(input("Please input depth precision level index: "))
    if index < 0 or index >= len(precision_support_list):
        print("Invalid input!")
        return
    device.set_int_property(OBPropertyID.OB_PROP_DEPTH_PRECISION_LEVEL_INT, precision_support_list[index])
    # get value after set
    level = device.get_int_property(OBPropertyID.OB_PROP_DEPTH_PRECISION_LEVEL_INT)
    print("Set depth precision level to {} success!".format(get_precision_level(level)))


def set_depth_unit_float(device):
    # auto current = device->getFloatProperty(OB_PROP_DEPTH_UNIT_FLEXIBLE_ADJUSTMENT_FLOAT)
    current_value = device.get_float_property(OBPropertyID.OB_PROP_DEPTH_UNIT_FLEXIBLE_ADJUSTMENT_FLOAT)
    value_range = device.get_float_property_range(OBPropertyID.OB_PROP_DEPTH_UNIT_FLEXIBLE_ADJUSTMENT_FLOAT)
    print("Current depth unit: ", current_value)
    print("Supported depth unit range: ", value_range.min, value_range.max)
    index = float(input("Please input depth unit value: "))
    if index < value_range.min or index > value_range.max:
        print("Invalid input!")
        return
    device.set_float_property(OBPropertyID.OB_PROP_DEPTH_UNIT_FLEXIBLE_ADJUSTMENT_FLOAT, index)
    # get value after set
    current_value = device.get_float_property(OBPropertyID.OB_PROP_DEPTH_UNIT_FLEXIBLE_ADJUSTMENT_FLOAT)
    print("Set depth unit to {} success!".format(current_value))


def main():
    ctx = Context()
    device_list = ctx.query_devices()
    if device_list.get_count() == 0:
        print("No device connected")
        return
    device = device_list.get_device_by_index(0)
    if device.is_property_supported(OBPropertyID.OB_PROP_DEPTH_PRECISION_LEVEL_INT,
                                    OBPermissionType.PERMISSION_READ_WRITE):
        print("Set depth precision level.")
        set_depth_unit(device)
    elif device.is_property_supported(OBPropertyID.OB_PROP_DEPTH_UNIT_FLEXIBLE_ADJUSTMENT_FLOAT,
                                      OBPermissionType.PERMISSION_READ_WRITE):
        print("Set depth unit.")
        set_depth_unit_float(device)
    else:
        print("Current device not support depth unit setting!")


if __name__ == "__main__":
    main()
