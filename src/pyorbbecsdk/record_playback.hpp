#include <pybind11/pybind11.h>

#include <libobsensor/ObSensor.hpp>
namespace py = pybind11;

namespace pyorbbecsdk {
void define_bag_recorder(const py::object& m);

void define_bag_player(const py::object& m);
}  // namespace pyorbbecsdk
