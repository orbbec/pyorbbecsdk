/*******************************************************************************
* Copyright (c) 2023 Orbbec 3D Technology, Inc
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
*     http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
*******************************************************************************/
#pragma once

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
