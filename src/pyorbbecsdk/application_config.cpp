/*******************************************************************************
 * Copyright (c) 2024 Orbbec 3D Technology, Inc
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
#include "application_config.hpp"

#include "error.hpp"
#include "utils.hpp"
#include <pybind11/stl.h>

namespace pyorbbecsdk {

void define_application_sensor_config(const py::object& m) {
  py::class_<ob::ApplicationSensorConfig,
             std::shared_ptr<ob::ApplicationSensorConfig>>(
      m, "ApplicationSensorConfig")
      .def(py::init<OBSensorType>(), py::arg("sensor_type"))
      .def("sensor_type",
           &ob::ApplicationSensorConfig::sensorType,
           "Get the sensor type")
      .def("enable_stream",
           &ob::ApplicationSensorConfig::enableStream,
           py::arg("enabled"),
           "Enable or disable the stream")
      .def("is_stream_enabled",
           &ob::ApplicationSensorConfig::isStreamEnabled,
           "Check if the stream is enabled")
      .def("set_stream_profile",
           &ob::ApplicationSensorConfig::setStreamProfile,
           py::arg("profile"),
           "Set the stream profile")
      .def("stream_profile",
           &ob::ApplicationSensorConfig::streamProfile,
           "Get the stream profile")
      .def("enable_undistortion",
           &ob::ApplicationSensorConfig::enableUndistortion,
           py::arg("enabled"),
           "Enable or disable undistortion")
      .def("is_undistortion_enabled",
           &ob::ApplicationSensorConfig::isUndistortionEnabled,
           "Check if undistortion is enabled");
}

void define_application_point_cloud_config(const py::object& m) {
  py::class_<ob::ApplicationPointCloudConfig,
             std::shared_ptr<ob::ApplicationPointCloudConfig>>(
      m, "ApplicationPointCloudConfig")
      .def(py::init<>())
      .def("enable",
           &ob::ApplicationPointCloudConfig::enable,
           py::arg("enabled"),
           "Enable or disable point cloud output")
      .def("is_enabled",
           &ob::ApplicationPointCloudConfig::isEnabled,
           "Check if point cloud is enabled")
      .def("set_format",
           &ob::ApplicationPointCloudConfig::setFormat,
           py::arg("format"),
           "Set the point cloud output format")
      .def("format",
           &ob::ApplicationPointCloudConfig::format,
           "Get the point cloud output format")
      .def("set_decimation_factor",
           &ob::ApplicationPointCloudConfig::setDecimationFactor,
           py::arg("factor"),
           "Set the point cloud decimation factor")
      .def("decimation_factor",
           &ob::ApplicationPointCloudConfig::decimationFactor,
           "Get the point cloud decimation factor")
      .def("set_align_mode",
           &ob::ApplicationPointCloudConfig::setAlignMode,
           py::arg("mode"),
           "Set the align mode")
      .def("align_mode",
           &ob::ApplicationPointCloudConfig::alignMode,
           "Get the align mode")
      .def("enable_frame_sync",
           &ob::ApplicationPointCloudConfig::enableFrameSync,
           py::arg("enabled"),
           "Enable or disable frame sync")
      .def("is_frame_sync_enabled",
           &ob::ApplicationPointCloudConfig::isFrameSyncEnabled,
           "Check if frame sync is enabled")
      .def("set_all_frame_type_required",
           &ob::ApplicationPointCloudConfig::setAllFrameTypeRequired,
           py::arg("enabled"),
           "Set whether all frame types are required")
      .def("is_all_frame_type_required",
           &ob::ApplicationPointCloudConfig::isAllFrameTypeRequired,
           "Check if all frame types are required")
      .def("enable_match_target_resolution",
           &ob::ApplicationPointCloudConfig::enableMatchTargetResolution,
           py::arg("enabled"),
           "Enable or disable match target resolution")
      .def("is_match_target_resolution_enabled",
           &ob::ApplicationPointCloudConfig::isMatchTargetResolutionEnabled,
           "Check if match target resolution is enabled");
}

void define_application_hdr_merge_config(const py::object& m) {
  py::class_<ob::ApplicationHDRMergeConfig,
             std::shared_ptr<ob::ApplicationHDRMergeConfig>>(
      m, "ApplicationHDRMergeConfig")
      .def(py::init<>())
      .def("enable",
           &ob::ApplicationHDRMergeConfig::enable,
           py::arg("enabled"),
           "Enable or disable HDR merge")
      .def("is_enabled",
           &ob::ApplicationHDRMergeConfig::isEnabled,
           "Check if HDR merge is enabled")
      .def("enable_ir",
           &ob::ApplicationHDRMergeConfig::enableIR,
           py::arg("enabled"),
           "Enable or disable IR for HDR merge")
      .def("is_ir_enabled",
           &ob::ApplicationHDRMergeConfig::isIREnabled,
           "Check if IR is enabled for HDR merge");
}

void define_application_dev_decimation_config(const py::object& m) {
  py::class_<ob::ApplicationDevDecimationConfig,
             std::shared_ptr<ob::ApplicationDevDecimationConfig>>(
      m, "ApplicationDevDecimationConfig")
      .def(py::init<>())
      .def("enable",
           &ob::ApplicationDevDecimationConfig::enable,
           py::arg("enabled"),
           "Enable or disable device-level decimation")
      .def("is_enabled",
           &ob::ApplicationDevDecimationConfig::isEnabled,
           "Check if device-level decimation is enabled")
      .def("set_preset_resolution_config",
           &ob::ApplicationDevDecimationConfig::setPresetResolutionConfig,
           py::arg("config"),
           "Set the preset resolution configuration")
      .def("preset_resolution_config",
           &ob::ApplicationDevDecimationConfig::presetResolutionConfig,
           py::return_value_policy::reference_internal,
           "Get the preset resolution configuration");
}

void define_application_config(const py::object& m) {
  py::class_<ob::ApplicationConfig,
             std::shared_ptr<ob::ApplicationConfig>>(
      m, "ApplicationConfig")
      .def_static("is_supported",
                  &ob::ApplicationConfig::isSupported,
                  py::arg("device"),
                  "Check whether the device supports application runtime "
                  "configuration import/export")
      .def_static("get",
                  static_cast<std::shared_ptr<ob::ApplicationConfig> (*)(
                      const std::shared_ptr<ob::Device> &)>(
                      &ob::ApplicationConfig::get),
                  py::arg("device"),
                  py::keep_alive<0, 1>(),
                  "Get the application runtime configuration cache for the "
                  "device")
      .def_static(
          "get_by_preset",
          static_cast<std::shared_ptr<ob::ApplicationConfig> (*)(
              const std::shared_ptr<ob::Device> &, const std::string &)>(
              &ob::ApplicationConfig::get),
          py::arg("device"),
          py::arg("preset_name"),
          py::keep_alive<0, 1>(),
          "Get the application config carried by an externally imported "
          "preset, by preset name. Returns None for built-in presets or "
          "presets that carry no application config")
      .def("reset",
           &ob::ApplicationConfig::reset,
           "Reset the application configuration to default values")
      .def("sensors",
           &ob::ApplicationConfig::sensors,
           "Get the list of sensor configurations")
      .def("set_sensors",
           &ob::ApplicationConfig::setSensors,
           py::arg("sensors"),
           "Set the list of sensor configurations")
      .def("set_sensor",
           &ob::ApplicationConfig::setSensor,
           py::arg("sensor"),
           "Set a single sensor configuration")
      .def("device_decimation",
           &ob::ApplicationConfig::deviceDecimation,
           "Get the device decimation configuration")
      .def("set_device_decimation",
           &ob::ApplicationConfig::setDeviceDecimation,
           py::arg("config"),
           "Set the device decimation configuration")
      .def("point_cloud",
           &ob::ApplicationConfig::pointCloud,
           "Get the point cloud configuration")
      .def("set_point_cloud",
           &ob::ApplicationConfig::setPointCloud,
           py::arg("config"),
           "Set the point cloud configuration")
      .def("hdr_merge",
           &ob::ApplicationConfig::hdrMerge,
           "Get the HDR merge configuration")
      .def("set_hdr_merge",
           &ob::ApplicationConfig::setHDRMerge,
           py::arg("config"),
           "Set the HDR merge configuration");
}

}  // namespace pyorbbecsdk
