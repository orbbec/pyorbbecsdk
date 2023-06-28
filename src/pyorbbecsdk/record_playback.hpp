#include <pybind11/pybind11.h>

#include <libobsensor/ObSensor.hpp>
namespace py = pybind11;

namespace pyorbbecsdk {
void define_recorder(const py::object& m);

void define_playback(const py::object& m);
}  // namespace pyorbbecsdk
