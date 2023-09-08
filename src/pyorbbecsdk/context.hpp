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
class Context {
 public:
  Context() noexcept;

  explicit Context(const std::string &config_file_path) noexcept;

  ~Context() = default;

  std::shared_ptr<ob::DeviceList> query_devices();

  std::shared_ptr<ob::Device> create_net_device(const std::string &ip,
                                              uint16_t port);

  void set_device_changed_callback(const py::function &callback);

  void enable_multi_device_sync(uint64_t repeat_interval);

  static void set_logger_level(OBLogSeverity level);

  static void set_logger_to_console(OBLogSeverity level);

  static void set_logger_to_file(OBLogSeverity level,
                                 const std::string &file_path);

 private:
  std::shared_ptr<ob::Context> impl_;
};

void define_context(py::object &m);
}  // namespace pyorbbecsdk
