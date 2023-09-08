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
#include <pybind11/pybind11.h>

#include <libobsensor/ObSensor.hpp>

#include "context.hpp"
#include "device.hpp"
#include "error.hpp"
#include "filter.hpp"
#include "frame.hpp"
#include "pipeline.hpp"
#include "properties.hpp"
#include "record_playback.hpp"
#include "sensor.hpp"
#include "stream_profile.hpp"
#include "types.hpp"
#include "utils.hpp"
namespace py = pybind11;

PYBIND11_MODULE(pyorbbecsdk, m) {
  m.doc() = "OrbbecSDK python binding";
  // version
  m.def("get_version", []() {
    auto major = ob::Version::getMajor();
    auto minor = ob::Version::getMinor();
    auto patch = ob::Version::getPatch();
    return std::to_string(major) + "." + std::to_string(minor) + "." +
           std::to_string(patch);
  });
  m.def("get_stage_version", []() { return ob::Version::getStageVersion(); });
  // context
  pyorbbecsdk::define_orbbec_types(m);
  pyorbbecsdk::define_context(m);

  // device
  pyorbbecsdk::define_device_info(m);
  pyorbbecsdk::define_device_list(m);
  pyorbbecsdk::define_depth_work_mode_list(m);
  pyorbbecsdk::define_device(m);
  pyorbbecsdk::define_camera_list(m);

  // error
  pyorbbecsdk::define_orbbec_error(m);

  // filter
  pyorbbecsdk::define_filter(m);
  pyorbbecsdk::define_point_cloud_filter(m);
  pyorbbecsdk::define_format_covert_filter(m);

  // frame
  pyorbbecsdk::define_frame(m);
  pyorbbecsdk::define_video_frame(m);
  pyorbbecsdk::define_color_frame(m);
  pyorbbecsdk::define_depth_frame(m);
  pyorbbecsdk::define_ir_frame(m);
  pyorbbecsdk::define_points_frame(m);
  pyorbbecsdk::define_frame_set(m);
  pyorbbecsdk::define_accel_frame(m);
  pyorbbecsdk::define_gyro_frame(m);

  // pipeline
  pyorbbecsdk::define_pipeline(m);
  pyorbbecsdk::define_pipeline_config(m);

  // properties
  pyorbbecsdk::define_properties(m);

  // record_playback
  pyorbbecsdk::define_recorder(m);
  pyorbbecsdk::define_playback(m);

  // sensor
  pyorbbecsdk::define_sensor(m);
  pyorbbecsdk::define_sensor_list(m);
  // stream_profile
  pyorbbecsdk::define_stream_profile(m);
  pyorbbecsdk::define_video_stream_profile(m);
  pyorbbecsdk::define_accel_stream_profile(m);
  pyorbbecsdk::define_gyro_stream_profile(m);
  pyorbbecsdk::define_stream_profile_list(m);
}
