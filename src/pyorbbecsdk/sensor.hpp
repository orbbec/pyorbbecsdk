#include <pybind11/pybind11.h>

#include <libobsensor/ObSensor.hpp>
namespace py = pybind11;

namespace pyorbbecsdk {
void define_sensor(const py::object& m);

void define_sensor_list(const py::object& m);

}  // namespace pyorbbecsdk
