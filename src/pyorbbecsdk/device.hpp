#include <pybind11/pybind11.h>

#include <libobsensor/ObSensor.hpp>
namespace py = pybind11;

namespace pyorbbecsdk {

void define_device_info(const py::object &m);

void define_camera_list(const py::object &m);

void define_depth_work_mode_list(const py::object &m);

void define_device(const py::object &m);

void define_device_list(const py::object &m);
}  // namespace pyorbbecsdk
