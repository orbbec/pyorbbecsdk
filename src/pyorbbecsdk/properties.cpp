/*******************************************************************************
 * Copyright (c) 2023 Orbbec 3D Technology, Inc
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *******************************************************************************/
#include "properties.hpp"

namespace pyorbbecsdk {
void define_properties(const py::object& m) {
  py::enum_<OBPropertyID>(m, "OBPropertyID")
      .value("OB_PROP_LDP_BOOL", OBPropertyID::OB_PROP_LDP_BOOL, "LDP switch")
      .value("OB_PROP_LASER_BOOL", OBPropertyID::OB_PROP_LASER_BOOL,
             "Laser switch")
      .value("OB_PROP_LASER_PULSE_WIDTH_INT",
             OBPropertyID::OB_PROP_LASER_PULSE_WIDTH_INT, "laser pulse width")
      .value("OB_PROP_LASER_CURRENT_FLOAT",
             OBPropertyID::OB_PROP_LASER_CURRENT_FLOAT,
             "Laser current (uint: mA)")
      .value("OB_PROP_FLOOD_BOOL", OBPropertyID::OB_PROP_FLOOD_BOOL,
             "IR flood switch")
      .value("OB_PROP_FLOOD_LEVEL_INT", OBPropertyID::OB_PROP_FLOOD_LEVEL_INT,
             "IR flood level")
      .value("OB_PROP_DEPTH_MIRROR_BOOL",
             OBPropertyID::OB_PROP_DEPTH_MIRROR_BOOL, "Depth mirror")
      .value("OB_PROP_DEPTH_FLIP_BOOL", OBPropertyID::OB_PROP_DEPTH_FLIP_BOOL,
             "Depth flip")
      .value("OB_PROP_DEPTH_POSTFILTER_BOOL",
             OBPropertyID::OB_PROP_DEPTH_POSTFILTER_BOOL, "Depth Post filter")
      .value("OB_PROP_DEPTH_HOLEFILTER_BOOL",
             OBPropertyID::OB_PROP_DEPTH_HOLEFILTER_BOOL, "Depth Hole filter")
      .value("OB_PROP_IR_MIRROR_BOOL", OBPropertyID::OB_PROP_IR_MIRROR_BOOL,
             "IR mirror")
      .value("OB_PROP_IR_FLIP_BOOL", OBPropertyID::OB_PROP_IR_FLIP_BOOL,
             "IR flip")
      .value("OB_PROP_MIN_DEPTH_INT", OBPropertyID::OB_PROP_MIN_DEPTH_INT,
             "Minimum depth threshold")
      .value("OB_PROP_MAX_DEPTH_INT", OBPropertyID::OB_PROP_MAX_DEPTH_INT,
             "Maximum depth threshold")
      .value("OB_PROP_DEPTH_SOFT_FILTER_BOOL",
             OBPropertyID::OB_PROP_DEPTH_SOFT_FILTER_BOOL,
             "Software filter switch")
      .value("OB_PROP_LDP_STATUS_BOOL", OBPropertyID::OB_PROP_LDP_STATUS_BOOL,
             "LDP status")
      .value("OB_PROP_DEPTH_MAX_DIFF_INT",
             OBPropertyID::OB_PROP_DEPTH_MAX_DIFF_INT,
             "soft filter max diff param")
      .value("OB_PROP_DEPTH_MAX_SPECKLE_SIZE_INT",
             OBPropertyID::OB_PROP_DEPTH_MAX_SPECKLE_SIZE_INT,
             "soft filter maxSpeckleSize")
      .value("OB_PROP_DEPTH_ALIGN_HARDWARE_BOOL",
             OBPropertyID::OB_PROP_DEPTH_ALIGN_HARDWARE_BOOL,
             "Hardware d2c is on")
      .value("OB_PROP_TIMESTAMP_OFFSET_INT",
             OBPropertyID::OB_PROP_TIMESTAMP_OFFSET_INT, "Timestamp adjustment")
      .value("OB_PROP_HARDWARE_DISTORTION_SWITCH_BOOL",
             OBPropertyID::OB_PROP_HARDWARE_DISTORTION_SWITCH_BOOL,
             " Hardware distortion switch Rectify")
      .value("OB_PROP_FAN_WORK_MODE_INT",
             OBPropertyID::OB_PROP_FAN_WORK_MODE_INT, "Fan mode switch")
      .value("OB_PROP_DEPTH_ALIGN_HARDWARE_MODE_INT",
             OBPropertyID::OB_PROP_DEPTH_ALIGN_HARDWARE_MODE_INT,
             "Multi-resolution D2C mode")
      .value("OB_PROP_ANTI_COLLUSION_ACTIVATION_STATUS_BOOL",
             OBPropertyID::OB_PROP_ANTI_COLLUSION_ACTIVATION_STATUS_BOOL,
             "Anti_collusion activation status")
      .value("OB_PROP_DEPTH_PRECISION_LEVEL_INT",
             OBPropertyID::OB_PROP_DEPTH_PRECISION_LEVEL_INT,
             "he depth precision level, which may change the depth frame data "
             "unit, needs to be confirmed through the ValueScale interface of "
             "DepthFrame")
      .value("OB_PROP_TOF_FILTER_RANGE_INT",
             OBPropertyID::OB_PROP_TOF_FILTER_RANGE_INT,
             "tof filter range configuration")
      .value("OB_PROP_LASER_MODE_INT", OBPropertyID::OB_PROP_LASER_MODE_INT,
             "laser mode, the firmware terminal currently only return 1: IR "
             "Drive, 2: Torch")
      .value("OB_PROP_RECTIFY2_BOOL", OBPropertyID::OB_PROP_RECTIFY2_BOOL,
             "brt2r-rectify function switch (brt2r is a special module on "
             "mx6600), 0: Disable, 1: Rectify Enable")
      .value("OB_PROP_COLOR_MIRROR_BOOL",
             OBPropertyID::OB_PROP_COLOR_MIRROR_BOOL, "Color mirror")
      .value("OB_PROP_COLOR_FLIP_BOOL", OBPropertyID::OB_PROP_COLOR_FLIP_BOOL,
             "Color flip")
      .value("OB_PROP_INDICATOR_LIGHT_BOOL",
             OBPropertyID::OB_PROP_INDICATOR_LIGHT_BOOL,
             "Indicator switch, 0: Disable, 1: Enable")
      .value("OB_PROP_DISPARITY_TO_DEPTH_BOOL",
             OBPropertyID::OB_PROP_DISPARITY_TO_DEPTH_BOOL,
             "Disparity to depth switch, 0: off, the depth stream outputs the "
             "disparity map; 1. On, the depth stream outputs the depth map.")
      .value("OB_PROP_BRT_BOOL", OBPropertyID::OB_PROP_BRT_BOOL,
             "BRT function switch (anti-background interference), 0: Disable, "
             "1: Enable")
      .value("OB_PROP_WATCHDOG_BOOL", OBPropertyID::OB_PROP_WATCHDOG_BOOL,
             "Watchdog function switch, 0: Disable, 1: Enable")
      .value("OB_PROP_EXTERNAL_SIGNAL_RESET_BOOL",
             OBPropertyID::OB_PROP_EXTERNAL_SIGNAL_RESET_BOOL,
             "External signal reset function switch, 0: Disable, 1: Enable")
      .value("OB_PROP_HEARTBEAT_BOOL", OBPropertyID::OB_PROP_HEARTBEAT_BOOL,
             "Heartbeat monitoring function switch, 0: Disable, 1: Enable")
      .value("OB_PROP_DEPTH_CROPPING_MODE_INT",
             OBPropertyID::OB_PROP_DEPTH_CROPPING_MODE_INT,
             "Depth cropping mode device: OB_DEPTH_CROPPING_MODE")
      .value("OB_PROP_D2C_PREPROCESS_BOOL",
             OBPropertyID::OB_PROP_D2C_PREPROCESS_BOOL,
             "D2C preprocessing switch (such as RGB cropping), 0: off, 1: on")
      .value("OB_PROP_RGB_CUSTOM_CROP_BOOL",
             OBPropertyID::OB_PROP_RGB_CUSTOM_CROP_BOOL,
             "Custom RGB cropping switch, 0 is off, 1 is on custom cropping, "
             "and the ROI cropping area is issued")
      .value("OB_PROP_DEVICE_WORK_MODE_INT",
             OBPropertyID::OB_PROP_DEVICE_WORK_MODE_INT,
             "Device operating mode (power consumption)")
      .value("OB_PROP_DEVICE_COMMUNICATION_TYPE_INT",
             OBPropertyID::OB_PROP_DEVICE_COMMUNICATION_TYPE_INT,
             "Device communication type, 0: USB; 1: Ethernet(RTSP)")
      .value(
          "OB_PROP_SWITCH_IR_MODE_INT",
          OBPropertyID::OB_PROP_SWITCH_IR_MODE_INT,
          "Switch infrared imaging mode, 0: active IR mode, 1: passive IR mode")
      .value("OB_PROP_LASER_POWER_LEVEL_CONTROL_INT",
             OBPropertyID::OB_PROP_LASER_POWER_LEVEL_CONTROL_INT,
             "Laser power level")
      .value("OB_PROP_LASER_ENERGY_LEVEL_INT",
             OBPropertyID::OB_PROP_LASER_ENERGY_LEVEL_INT, "Laser energy level")
      .value("OB_PROP_LDP_MEASURE_DISTANCE_INT",
             OBPropertyID::OB_PROP_LDP_MEASURE_DISTANCE_INT,
             "LDP's measure distance, unit: mm")
      .value("OB_PROP_TIMER_RESET_SIGNAL_BOOL",
             OBPropertyID::OB_PROP_TIMER_RESET_SIGNAL_BOOL,
             "Reset device time to zero")
      .value("OB_PROP_TIMER_RESET_TRIGGER_OUT_ENABLE_BOOL",
             OBPropertyID::OB_PROP_TIMER_RESET_TRIGGER_OUT_ENABLE_BOOL,
             "Enable send reset device time signal to other device. true: "
             "enable, false: disable")
      .value("OB_PROP_TIMER_RESET_DELAY_US_INT",
             OBPropertyID::OB_PROP_TIMER_RESET_DELAY_US_INT,
             "Delay to reset device time, unit: us")
      .value("OB_PROP_CAPTURE_IMAGE_SIGNAL_BOOL",
             OBPropertyID::OB_PROP_CAPTURE_IMAGE_SIGNAL_BOOL)
      .value("OB_PROP_IR_RIGHT_MIRROR_BOOL",
             OBPropertyID::OB_PROP_IR_RIGHT_MIRROR_BOOL,
             "Signal to capture image")
      .value("OB_PROP_CAPTURE_IMAGE_FRAME_NUMBER_INT",
             OBPropertyID::OB_PROP_CAPTURE_IMAGE_FRAME_NUMBER_INT,
             "Number frame to capture once a "
             "OB_PROP_CAPTURE_IMAGE_SIGNAL_BOOL' effect. range: [1, 255]")
      .value("OB_PROP_IR_RIGHT_FLIP_BOOL",
             OBPropertyID::OB_PROP_IR_RIGHT_FLIP_BOOL,
             "Right IR sensor flip state. true: flip image, false: origin, "
             "default: false")
      .value("OB_PROP_COLOR_ROTATE_INT", OBPropertyID::OB_PROP_COLOR_ROTATE_INT,
             "Color sensor rotation, angle{0, 90, 180, 270}")
      .value("OB_PROP_IR_ROTATE_INT", OBPropertyID::OB_PROP_IR_ROTATE_INT,
             "IR/Left-IR sensor rotation, angle{0, 90, 180, 270}")
      .value("OB_PROP_IR_RIGHT_ROTATE_INT",
             OBPropertyID::OB_PROP_IR_RIGHT_ROTATE_INT,
             "Right IR sensor rotation, angle{0, 90, 180, 270}")
      .value("OB_PROP_DEPTH_ROTATE_INT", OBPropertyID::OB_PROP_DEPTH_ROTATE_INT,
             "Depth sensor rotation, angle{0, 90, 180, 270}")
      .value(
          "OB_PROP_LASER_HW_ENERGY_LEVEL_INT",
          OBPropertyID::OB_PROP_LASER_HW_ENERGY_LEVEL_INT,
          "Get hardware laser energy level which real state of laser element. "
          "OB_PROP_LASER_ENERGY_LEVEL_INT(99)will effect this command"
          " which it setting and changed the hardware laser energy level.")
      .value("OB_PROP_USB_POWER_STATE_INT",
             OBPropertyID::OB_PROP_USB_POWER_STATE_INT, "USB's power state")
      .value("OB_PROP_DC_POWER_STATE_INT",
             OBPropertyID::OB_PROP_DC_POWER_STATE_INT, "DC's power state")
      .value("OB_PROP_DEVICE_DEVELOPMENT_MODE_INT",
             OBPropertyID::OB_PROP_DEVICE_DEVELOPMENT_MODE_INT,
             "Device development mode switch")
      .value(
          "OB_PROP_SYNC_SIGNAL_TRIGGER_OUT_BOOL",
          OBPropertyID::OB_PROP_SYNC_SIGNAL_TRIGGER_OUT_BOOL,
          " Multi-DeviceSync synchronized signal trigger out is enable state")
      .value("OB_PROP_RESTORE_FACTORY_SETTINGS_BOOL",
             OBPropertyID::OB_PROP_RESTORE_FACTORY_SETTINGS_BOOL,
             "Restore factory settings and factory parameters")
      .value("OB_PROP_BOOT_INTO_RECOVERY_MODE_BOOL",
             OBPropertyID::OB_PROP_BOOT_INTO_RECOVERY_MODE_BOOL,
             "Enter recovery mode (flashing mode) when boot the device")
      .value("OB_PROP_DEVICE_IN_RECOVERY_MODE_BOOL",
             OBPropertyID::OB_PROP_DEVICE_IN_RECOVERY_MODE_BOOL,
             "Query whether the current device is running in recovery mode"
             "(read-only)")
      .value("OB_PROP_CAPTURE_INTERVAL_MODE_INT",
             OBPropertyID::OB_PROP_CAPTURE_INTERVAL_MODE_INT,
             "Capture interval mode, 0:time interval, 1:number interval")
      .value("OB_PROP_CAPTURE_IMAGE_TIME_INTERVAL_INT",
             OBPropertyID::OB_PROP_CAPTURE_IMAGE_TIME_INTERVAL_INT,
             "Capture time interval")
      .value("OB_PROP_CAPTURE_IMAGE_NUMBER_INTERVAL_INT",
             OBPropertyID::OB_PROP_CAPTURE_IMAGE_NUMBER_INTERVAL_INT,
             "Capture number interval")
      .value("OB_PROP_TIMER_RESET_ENABLE_BOOL",
             OBPropertyID::OB_PROP_TIMER_RESET_ENABLE_BOOL,
             "OB_PROP_TIMER_RESET_ENABLE_BOOL")
      .value("OB_PROP_DEVICE_USB3_REPEAT_IDENTIFY_BOOL",
             OBPropertyID::OB_PROP_DEVICE_USB3_REPEAT_IDENTIFY_BOOL,
             "Enable or disable the device to retry USB2.0 re-identification "
             "when the device is connected to a USB2.0 port.")
      .value("OB_PROP_DEVICE_REBOOT_DELAY_INT",
             OBPropertyID::OB_PROP_DEVICE_REBOOT_DELAY_INT,
             "Reboot device delay mode. Delay time unit: ms, range: [0, 8000).")
      .value("OB_PROP_LASER_OVERCURRENT_PROTECTION_STATUS_BOOL",
             OBPropertyID::OB_PROP_LASER_OVERCURRENT_PROTECTION_STATUS_BOOL,
             "Query the status of laser overcurrent protection (read-only)")
      .value("OB_PROP_LASER_PULSE_WIDTH_PROTECTION_STATUS_BOOL",
             OBPropertyID::OB_PROP_LASER_PULSE_WIDTH_PROTECTION_STATUS_BOOL,
             "Query the status of laser pulse width protection (read-only)")
      .value("OB_PROP_LASER_ALWAYS_ON_BOOL",
             OBPropertyID::OB_PROP_LASER_ALWAYS_ON_BOOL,
             " Laser always on, true: always on, false: off, laser will be "
             "turned off when out of exposure time")
      .value("OB_PROP_LASER_ON_OFF_PATTERN_INT",
             OBPropertyID::OB_PROP_LASER_ON_OFF_PATTERN_INT,
             "Laser on/off alternate mode, 0: off, 1: on-off alternate, 2: "
             "off-on alternate")
      .value("OB_PROP_DEPTH_UNIT_FLEXIBLE_ADJUSTMENT_FLOAT",
             OBPropertyID::OB_PROP_DEPTH_UNIT_FLEXIBLE_ADJUSTMENT_FLOAT,
             "Depth unit flexible adjustment,This property allows continuous "
             "adjustment of the depth unit")
      .value("OB_PROP_LASER_CONTROL_INT",
             OBPropertyID::OB_PROP_LASER_CONTROL_INT,
             "Laser control, 0: off, 1: on, 2: auto")
      .value("OB_PROP_IR_BRIGHTNESS_INT",
             OBPropertyID::OB_PROP_IR_BRIGHTNESS_INT,
             "IR brightness")
      .value("OB_STRUCT_BASELINE_CALIBRATION_PARAM",
             OBPropertyID::OB_STRUCT_BASELINE_CALIBRATION_PARAM,
             "Baseline calibration parameters")
      .value("OB_STRUCT_DEVICE_TEMPERATURE",
             OBPropertyID::OB_STRUCT_DEVICE_TEMPERATURE,
             "Device temperature information")
      .value("OB_STRUCT_TOF_EXPOSURE_THRESHOLD_CONTROL",
             OBPropertyID::OB_STRUCT_TOF_EXPOSURE_THRESHOLD_CONTROL
             ,"TOF exposure threshold range")
      .value("OB_STRUCT_DEVICE_SERIAL_NUMBER",
             OBPropertyID::OB_STRUCT_DEVICE_SERIAL_NUMBER)
      .value("OB_STRUCT_DEVICE_TIME", OBPropertyID::OB_STRUCT_DEVICE_TIME)
      .value("OB_STRUCT_MULTI_DEVICE_SYNC_CONFIG",
             OBPropertyID::OB_STRUCT_MULTI_DEVICE_SYNC_CONFIG)
      .value("OB_STRUCT_RGB_CROP_ROI", OBPropertyID::OB_STRUCT_RGB_CROP_ROI)
      .value("OB_STRUCT_DEVICE_IP_ADDR_CONFIG",
             OBPropertyID::OB_STRUCT_DEVICE_IP_ADDR_CONFIG)
      .value("OB_STRUCT_CURRENT_DEPTH_ALG_MODE",
             OBPropertyID::OB_STRUCT_CURRENT_DEPTH_ALG_MODE)
      .value("OB_STRUCT_DEPTH_PRECISION_SUPPORT_LIST",
             OBPropertyID::OB_STRUCT_DEPTH_PRECISION_SUPPORT_LIST)
      .value("OB_STRUCT_DEVICE_STATIC_IP_CONFIG_RECORD",
             OBPropertyID::OB_STRUCT_DEVICE_STATIC_IP_CONFIG_RECORD)
      .value("OB_STRUCT_DEPTH_HDR_CONFIG",
             OBPropertyID::OB_STRUCT_DEPTH_HDR_CONFIG)
      .value("OB_STRUCT_COLOR_AE_ROI", OBPropertyID::OB_STRUCT_COLOR_AE_ROI)
      .value("OB_STRUCT_DEPTH_AE_ROI", OBPropertyID::OB_STRUCT_DEPTH_AE_ROI)
      .value("OB_STRUCT_ASIC_SERIAL_NUMBER",
             OBPropertyID::OB_STRUCT_ASIC_SERIAL_NUMBER)
      .value("OB_PROP_COLOR_AUTO_EXPOSURE_BOOL",
             OBPropertyID::OB_PROP_COLOR_AUTO_EXPOSURE_BOOL)
      .value("OB_PROP_COLOR_EXPOSURE_INT",
             OBPropertyID::OB_PROP_COLOR_EXPOSURE_INT)
      .value("OB_PROP_COLOR_GAIN_INT", OBPropertyID::OB_PROP_COLOR_GAIN_INT)
      .value("OB_PROP_COLOR_AUTO_WHITE_BALANCE_BOOL",
             OBPropertyID::OB_PROP_COLOR_AUTO_WHITE_BALANCE_BOOL)
      .value("OB_PROP_COLOR_WHITE_BALANCE_INT",
             OBPropertyID::OB_PROP_COLOR_WHITE_BALANCE_INT)
      .value("OB_PROP_COLOR_BRIGHTNESS_INT",
             OBPropertyID::OB_PROP_COLOR_BRIGHTNESS_INT)
      .value("OB_PROP_COLOR_SHARPNESS_INT",
             OBPropertyID::OB_PROP_COLOR_SHARPNESS_INT)
      .value("OB_PROP_COLOR_SHUTTER_INT",
             OBPropertyID::OB_PROP_COLOR_SHUTTER_INT)
      .value("OB_PROP_COLOR_SATURATION_INT",
             OBPropertyID::OB_PROP_COLOR_SATURATION_INT)
      .value("OB_PROP_COLOR_CONTRAST_INT",
             OBPropertyID::OB_PROP_COLOR_CONTRAST_INT)
      .value("OB_PROP_COLOR_GAMMA_INT", OBPropertyID::OB_PROP_COLOR_GAMMA_INT)
      .value("OB_PROP_COLOR_ROLL_INT", OBPropertyID::OB_PROP_COLOR_ROLL_INT)
      .value("OB_PROP_COLOR_AUTO_EXPOSURE_PRIORITY_INT",
             OBPropertyID::OB_PROP_COLOR_AUTO_EXPOSURE_PRIORITY_INT)
      .value("OB_PROP_COLOR_BACKLIGHT_COMPENSATION_INT",
             OBPropertyID::OB_PROP_COLOR_BACKLIGHT_COMPENSATION_INT)
      .value("OB_PROP_COLOR_HUE_INT", OBPropertyID::OB_PROP_COLOR_HUE_INT)
      .value("OB_PROP_COLOR_POWER_LINE_FREQUENCY_INT",
             OBPropertyID::OB_PROP_COLOR_POWER_LINE_FREQUENCY_INT)
      .value("OB_PROP_DEPTH_AUTO_EXPOSURE_BOOL",
             OBPropertyID::OB_PROP_DEPTH_AUTO_EXPOSURE_BOOL)
      .value("OB_PROP_DEPTH_EXPOSURE_INT",
             OBPropertyID::OB_PROP_DEPTH_EXPOSURE_INT)
      .value("OB_PROP_DEPTH_GAIN_INT", OBPropertyID::OB_PROP_DEPTH_GAIN_INT)
      .value("OB_PROP_IR_AUTO_EXPOSURE_BOOL",
             OBPropertyID::OB_PROP_IR_AUTO_EXPOSURE_BOOL)
      .value("OB_PROP_IR_EXPOSURE_INT", OBPropertyID::OB_PROP_IR_EXPOSURE_INT)
      .value("OB_PROP_IR_GAIN_INT", OBPropertyID::OB_PROP_IR_GAIN_INT)
      .value("OB_PROP_IR_CHANNEL_DATA_SOURCE_INT",
             OBPropertyID::OB_PROP_IR_CHANNEL_DATA_SOURCE_INT)
      .value("OB_PROP_DEPTH_RM_FILTER_BOOL",
             OBPropertyID::OB_PROP_DEPTH_RM_FILTER_BOOL)
      .value("OB_PROP_COLOR_MAXIMAL_GAIN_INT",
             OBPropertyID::OB_PROP_COLOR_MAXIMAL_GAIN_INT)
      .value("OB_PROP_COLOR_MAXIMAL_SHUTTER_INT",
             OBPropertyID::OB_PROP_COLOR_MAXIMAL_SHUTTER_INT)
      .value("OB_PROP_IR_SHORT_EXPOSURE_BOOL",
             OBPropertyID::OB_PROP_IR_SHORT_EXPOSURE_BOOL)
      .value("OB_PROP_COLOR_HDR_BOOL", OBPropertyID::OB_PROP_COLOR_HDR_BOOL)
      .value("OB_PROP_IR_LONG_EXPOSURE_BOOL",
             OBPropertyID::OB_PROP_IR_LONG_EXPOSURE_BOOL)
      .value("OB_PROP_SKIP_FRAME_BOOL", OBPropertyID::OB_PROP_SKIP_FRAME_BOOL)
      .value("OB_PROP_HDR_MERGE_BOOL", OBPropertyID::OB_PROP_HDR_MERGE_BOOL)
      .value("OB_PROP_COLOR_FOCUS_INT", OBPropertyID::OB_PROP_COLOR_FOCUS_INT)
      .value("OB_PROP_SDK_DISPARITY_TO_DEPTH_BOOL",
             OBPropertyID::OB_PROP_SDK_DISPARITY_TO_DEPTH_BOOL)
      .value("OB_PROP_SDK_DEPTH_FRAME_UNPACK_BOOL",
             OBPropertyID::OB_PROP_SDK_DEPTH_FRAME_UNPACK_BOOL)
      .value("OB_PROP_SDK_IR_FRAME_UNPACK_BOOL",
             OBPropertyID::OB_PROP_SDK_IR_FRAME_UNPACK_BOOL)
      .value("OB_PROP_SDK_ACCEL_FRAME_TRANSFORMED_BOOL",
             OBPropertyID::OB_PROP_SDK_ACCEL_FRAME_TRANSFORMED_BOOL,
             "Accel data conversion function switch (on by default)")
      .value("OB_PROP_SDK_GYRO_FRAME_TRANSFORMED_BOOL",
             OBPropertyID::OB_PROP_SDK_GYRO_FRAME_TRANSFORMED_BOOL,
             "Gyro data conversion function switch (on by default)")
      .value("OB_PROP_SDK_IR_LEFT_FRAME_UNPACK_BOOL",
             OBPropertyID::OB_PROP_SDK_IR_LEFT_FRAME_UNPACK_BOOL,
             "Left IR frame data unpacking function switch (each current will "
             "be turned on by default, support RLE/Y10/Y11/Y12/Y14 format)")
      .value("OB_PROP_SDK_IR_RIGHT_FRAME_UNPACK_BOOL",
             OBPropertyID::OB_PROP_SDK_IR_RIGHT_FRAME_UNPACK_BOOL,
             "Right IR frame data unpacking function switch (each current will "
             "be turned on by default, support RLE/Y10/Y11/Y12/Y14 format)")
      .value("OB_RAW_DATA_CAMERA_CALIB_JSON_FILE",
             OBPropertyID::OB_RAW_DATA_CAMERA_CALIB_JSON_FILE,
             "Calibration JSON file read from device (Femto Mega, read only)")
      .value("OB_PROP_DEPTH_NOISE_REMOVAL_FILTER_BOOL",
             OBPropertyID::OB_PROP_DEPTH_NOISE_REMOVAL_FILTER_BOOL,
             "depth noise removal filter")
      .value("OB_PROP_SDK_DEPTH_RECTIFY_MG_FILTER_BOOL",
             OBPropertyID::OB_PROP_SDK_DEPTH_RECTIFY_MG_FILTER_BOOL,
             "depth Margin Filter");

  py::enum_<OBPropertyType>(m, "OBPropertyType")
      .value("OB_BOOL_PROPERTY", OBPropertyType::OB_BOOL_PROPERTY,
             "Boolean property")
      .value("OB_INT_PROPERTY", OBPropertyType::OB_INT_PROPERTY,
             "Integer property")
      .value("OB_FLOAT_PROPERTY", OBPropertyType::OB_FLOAT_PROPERTY,
             "Float property")
      .value("OB_STRUCT_PROPERTY", OBPropertyType::OB_STRUCT_PROPERTY,
             "Struct property");

  py::class_<OBPropertyItem>(m, "OBPropertyItem")
      .def(py::init<>())
      .def_readwrite("id", &OBPropertyItem::id, "Property ID ")
      .def_readwrite("name", &OBPropertyItem::name, "Property name")
      .def_readwrite("type", &OBPropertyItem::type, "Property type")
      .def_readwrite("permission", &OBPropertyItem::permission,
                     "Property permission");
}
}  // namespace pyorbbecsdk
