
#include <pybind11/pybind11.h>

#include <libobsensor/ObSensor.hpp>
namespace py = pybind11;
namespace pyorbbecsdk {
void define_properties(const py::object& m);
}
