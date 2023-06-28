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
