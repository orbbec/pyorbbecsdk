#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>
#define PYBIND11_NO_ASSERT_GIL_HELD_INCREF_DECREF

#include <libobsensor/ObSensor.hpp>
namespace py = pybind11;

namespace pyorbbecsdk {

void define_orbbec_types(const py::object& m);
}
