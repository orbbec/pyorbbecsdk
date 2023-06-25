#include <pybind11/pybind11.h>

#include <libobsensor/ObSensor.hpp>
namespace py = pybind11;

namespace pyorbbecsdk {
void define_filter(const py::object& m);

void define_point_cloud_filter(const py::object& m);

void define_format_covert_filter(const py::object& m);

}  // namespace pyorbbecsdk
