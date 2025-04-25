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
#pragma once

#include <pybind11/pybind11.h>

#include <atomic>
#include <libobsensor/ObSensor.hpp>
namespace py = pybind11;
namespace pyorbbecsdk {

class Pipeline {
 public:
  Pipeline();

  explicit Pipeline(std::shared_ptr<ob::Device> device);

  ~Pipeline() noexcept;

  void start(std::shared_ptr<ob::Config> config);

  void start(std::shared_ptr<ob::Config> config, const py::function &callback);

  void stop();

  std::shared_ptr<ob::Config> get_config();

  std::shared_ptr<ob::FrameSet> wait_for_frames(uint32_t timeout) const;

  std::shared_ptr<ob::Device> get_device() const;

  std::shared_ptr<ob::StreamProfileList> get_stream_profile_list(
      OBSensorType sensor_type) const;

  void enable_frame_sync() const;

  void disable_frame_sync() const;

  OBCameraParam get_camera_param() const;

  std::shared_ptr<ob::StreamProfileList> get_d2c_depth_profile_list(
      std::shared_ptr<ob::StreamProfile> color_profile,
      OBAlignMode align_mode) const;

 private:
  std::shared_ptr<ob::Pipeline> impl_;
  std::atomic<bool> is_started_{false};
};

void define_pipeline(py::object &m);

void define_pipeline_config(py::object &m);

}  // namespace pyorbbecsdk
