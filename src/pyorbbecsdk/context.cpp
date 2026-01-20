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

std::shared_ptr<ob::Device> Context::create_net_device(
    const std::string &address, uint16_t port,
    const OBDeviceAccessMode access_mode) {
  CHECK_NULLPTR(impl_);
  OB_TRY_CATCH(
      { return impl_->createNetDevice(address.c_str(), port, access_mode); });
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

uint64_t Context::register_device_changed_callback(
    const py::function &callback) {
  CHECK_NULLPTR(impl_);
  uint64_t id = 0;
  OB_TRY_CATCH({
    id = impl_->registerDeviceChangedCallback(
        [callback](std::shared_ptr<ob::DeviceList> removed_list,
                   std::shared_ptr<ob::DeviceList> added_list) {
          py::gil_scoped_acquire acquire;
          callback(removed_list, added_list);
        });
  });
  return id;
}

void Context::unregister_device_changed_callback(const uint64_t id) {
  CHECK_NULLPTR(impl_);
  OB_TRY_CATCH({ impl_->unregisterDeviceChangedCallback(id); });
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

void Context::set_logger_to_callback(OBLogSeverity level,
                                     const py::function &callback) {
  OB_TRY_CATCH({
    ob::Context::setLoggerToCallback(
        level, [callback](OBLogSeverity level, const std::string log_msg) {
          py::gil_scoped_acquire acquire;
          callback(level, log_msg.c_str());
        });
  });
}

void Context::set_logger_file_name(const std::string &file_name) {
  OB_TRY_CATCH({ ob::Context::setLoggerFileName(file_name.c_str()); });
}

void Context::log_external_message(OBLogSeverity level,
                                   const std::string &module,
                                   const std::string &message,
                                   const std::string &file,
                                   const std::string &func, int line) {
  OB_TRY_CATCH({
    ob::Context::logExternalMessage(level, module.c_str(), message.c_str(),
                                    file.c_str(), func.c_str(), line);
  });
}

void Context::enable_net_device_enumeration(bool enable) {
  OB_TRY_CATCH({ impl_->enableNetDeviceEnumeration(enable); });
}

bool Context::ob_force_ip_config(const std::string device_uid,
                                 const OBDeviceIpAddrConfig &config) {
  OB_TRY_CATCH({ return impl_->forceIp(device_uid.c_str(), config); });
}

void define_context(py::object &m) {
  py::class_<Context>(m, "Context")
      .def(py::init<>())
      .def(py::init<const std::string &>())
      .def("query_devices", &Context::query_devices, "Query devices")
      .def(
          "create_net_device",
          [](Context &self, const std::string &address, uint16_t port,
             const OBDeviceAccessMode access_mode) {
            return self.create_net_device(address, port, access_mode);
          },
          py::arg("address"), py::arg("port"),
          py::arg("access_mode") = OB_DEVICE_DEFAULT_ACCESS,
          "Create net device")
      .def(
          "set_device_changed_callback",
          [](Context &self, const py::function &callback) {
            self.set_device_changed_callback(callback);
          },
          "Set device changed callback, callback will be called when device "
          "changed")
      .def("register_device_changed_callback",
           [](Context &self, const py::function &callback) -> uint64_t {
             return self.register_device_changed_callback(callback);
           })
      .def("unregister_device_changed_callback",
           [](Context &self, const uint64_t id) {
             self.unregister_device_changed_callback(id);
           })
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
      .def(
          "ob_force_ip_config",
          [](Context &self, const std::string device_uid,
             const OBDeviceIpAddrConfig &config) {
            return self.ob_force_ip_config(device_uid, config);
          },
          "Change the IP configuration")
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
          "Set logger to file")
      .def_static(
          "set_logger_to_callback",
          [](OBLogSeverity level, const py::function &callback) {
            Context::set_logger_to_callback(level, callback);
          },
          "Set logger to callback")
      .def_static(
          "set_logger_file_name",
          [](const std::string &file_name) {
            Context::set_logger_file_name(file_name);
          },
          "Set logger file name")
      .def_static("log_external_message",
                  [](OBLogSeverity level, const std::string &module,
                     const std::string &message, const std::string &file,
                     const std::string &func, int line) {
                    Context::log_external_message(level, module, message, file,
                                                  func, line);
                  });
}
}  // namespace pyorbbecsdk
