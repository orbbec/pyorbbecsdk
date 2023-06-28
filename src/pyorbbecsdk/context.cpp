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
        [callback](std::shared_ptr<ob::DeviceList> removedList,
                   std::shared_ptr<ob::DeviceList> addedList) {
          py::gil_scoped_acquire acquire;
          callback(removedList, addedList);
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
      .def("enable_multi_device_sync",
           [](Context &self, uint64_t repeat_interval) {
             self.enable_multi_device_sync(repeat_interval);
           })
      .def_static("set_logger_level",
                  [](OBLogSeverity level) { Context::set_logger_level(level); })
      .def_static(
          "set_logger_to_console",
          [](OBLogSeverity level) { Context::set_logger_to_console(level); })
      .def_static("set_logger_to_file",
                  [](OBLogSeverity level, const std::string &file_path) {
                    Context::set_logger_to_file(level, file_path);
                  });
}
}  // namespace pyorbbecsdk
