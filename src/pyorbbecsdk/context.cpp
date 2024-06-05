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
#include "context.hpp"

#include "error.hpp"
#include "utils.hpp"
namespace pyorbbecsdk {
Context::Context() noexcept { impl_ = std::make_shared<ob::Context>(); }

Context::Context(const std::string &config_file_path) noexcept {
  impl_ = std::make_shared<ob::Context>(config_file_path.c_str());
}

std::shared_ptr<ob::DeviceList> Context::query_devices() {
  CHECK_NULLPTR(impl_);
  OB_TRY_CATCH({ return impl_->queryDeviceList(); });
}

std::shared_ptr<ob::Device> Context::create_net_device(const std::string &ip,
                                                       uint16_t port) {
  CHECK_NULLPTR(impl_);
  OB_TRY_CATCH({ return impl_->createNetDevice(ip.c_str(), port); });
}

void Context::set_device_changed_callback(const py::function &callback) {
  CHECK_NULLPTR(impl_);
  OB_TRY_CATCH({
    impl_->setDeviceChangedCallback(
        [callback](std::shared_ptr<ob::DeviceList> removed_list,
                   std::shared_ptr<ob::DeviceList> added_list) {
          py::gil_scoped_acquire acquire;
          callback(removed_list, added_list);
        });
  });
}

void Context::enable_multi_device_sync(uint64_t repeat_interval) {
  CHECK_NULLPTR(impl_);
  OB_TRY_CATCH({ impl_->enableMultiDeviceSync(repeat_interval); });
}

void Context::set_logger_level(OBLogSeverity level) {
  OB_TRY_CATCH({ ob::Context::setLoggerSeverity(level); });
}

void Context::set_logger_to_console(OBLogSeverity level) {
  OB_TRY_CATCH({ ob::Context::setLoggerToConsole(level); });
}

void Context::set_logger_to_file(OBLogSeverity level,
                                 const std::string &file_path) {
  OB_TRY_CATCH({ ob::Context::setLoggerToFile(level, file_path.c_str()); });
}

void Context::enable_net_device_enumeration(bool enable) {
  OB_TRY_CATCH({ impl_->enableNetDeviceEnumeration(enable); });
}

void define_context(py::object &m) {
  py::class_<Context>(m, "Context")
      .def(py::init<>())
      .def(py::init<const std::string &>())
      .def("query_devices", &Context::query_devices, "Query devices")
      .def(
          "create_net_device",
          [](Context &self, const std::string &ip, uint16_t port) {
            return self.create_net_device(ip, port);
          },
          "Create net device")
      .def(
          "set_device_changed_callback",
          [](Context &self, const py::function &callback) {
            self.set_device_changed_callback(callback);
          },
          "Set device changed callback, callback will be called when device "
          "changed")
      .def(
          "enable_multi_device_sync",
          [](Context &self, uint64_t repeat_interval) {
            self.enable_multi_device_sync(repeat_interval);
          },
          "Activates the multi-device synchronization function to synchronize "
          "the clock of the created device (the device needs to support this "
          "function)."
          "repeat_interval: The synchronization time interval (unit: ms; if "
          "repeatInterval=0, it means that it will only be synchronized once "
          "and will not be executed regularly).")
      .def("enable_net_device_enumeration",
           [](Context &self, bool enable) {
             self.enable_net_device_enumeration(enable);
           })
      .def_static("set_logger_level",
                  [](OBLogSeverity level) { Context::set_logger_level(level); })
      .def_static(
          "set_logger_to_console",
          [](OBLogSeverity level) { Context::set_logger_to_console(level); },
          "Set logger to console")
      .def_static(
          "set_logger_to_file",
          [](OBLogSeverity level, const std::string &file_path) {
            Context::set_logger_to_file(level, file_path);
          },
          "Set logger to file");
}
}  // namespace pyorbbecsdk
