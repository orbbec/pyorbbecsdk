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
#pragma once

#include <pybind11/pybind11.h>

#include <libobsensor/ObSensor.hpp>
namespace py = pybind11;
namespace pyorbbecsdk {

class Pipeline {
 public:
  Pipeline();

  explicit Pipeline(std::shared_ptr<ob::Device> device);

  explicit Pipeline(const std::string &bag_path);

  ~Pipeline();

  void start(std::shared_ptr<ob::Config> config);

  void start(std::shared_ptr<ob::Config> config, const py::function &callback);

  void stop();

  std::shared_ptr<ob::Config> get_config();

  std::shared_ptr<ob::FrameSet> wait_for_frames(uint32_t timeout);

  std::shared_ptr<ob::Playback> get_playback();

  std::shared_ptr<ob::Device> get_device();

  std::shared_ptr<ob::StreamProfileList> get_stream_profile_list(
      OBSensorType sensor_type);

  void enable_frame_sync();

  void disable_frame_sync();

  OBCameraParam get_camera_param();

  OBRect get_d2c_valid_area(uint32_t minimum_z, uint32_t maximum_z);

  void switch_config(std::shared_ptr<ob::Config> config);

  void start_recording(const std::string &file_path);

  void stop_recording();

 private:
  std::shared_ptr<ob::Pipeline> impl_;
};

void define_pipeline(py::object &m);

void define_pipeline_config(py::object &m);

}  // namespace pyorbbecsdk
