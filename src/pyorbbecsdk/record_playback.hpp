#pragma once

#include <pybind11/functional.h>
#include <pybind11/pybind11.h>

#include <atomic>
#include <libobsensor/ObSensor.hpp>
namespace py = pybind11;
namespace pyorbbecsdk {
void define_record(py::object &m);
void define_playback(py::object &m);
}  // namespace pyorbbecsdk
