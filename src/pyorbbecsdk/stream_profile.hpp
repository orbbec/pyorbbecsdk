#include <pybind11/pybind11.h>

#include <libobsensor/ObSensor.hpp>

#include "types.hpp"

namespace py = pybind11;

namespace pyorbbecsdk {
void define_stream_profile(const py::object& m);

void define_video_stream_profile(const py::object& m);

void define_accel_stream_profile(const py::object& m);

void define_gyro_stream_profile(const py::object& m);

void define_stream_profile_list(const py::object& m);

}  // namespace pyorbbecsdk
