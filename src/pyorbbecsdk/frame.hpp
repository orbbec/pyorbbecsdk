#include <pybind11/pybind11.h>

#include <libobsensor/ObSensor.hpp>
namespace py = pybind11;

namespace pyorbbecsdk {
void define_frame(const py::object& m);

void define_video_frame(const py::object& m);

void define_color_frame(const py::object& m);

void define_depth_frame(const py::object& m);

void define_ir_frame(const py::object& m);

void define_points_frame(const py::object& m);

void define_frame_set(const py::object& m);

void define_accel_frame(const py::object& m);

void define_gyro_frame(const py::object& m);


}  // namespace pyorbbecsdk
