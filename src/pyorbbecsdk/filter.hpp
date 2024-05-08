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
void define_filter(const py::object& m);

void define_point_cloud_filter(const py::object& m);

void define_format_covert_filter(const py::object& m);

void define_hole_filling_filter(const py::object& m);

void define_temporal_filter(const py::object& m);

void define_spatial_advanced_filter(const py::object& m);

void define_disparity_transform(const py::object& m);

void define_HDR_merge_filter(const py::object& m);

void define_align_filter(const py::object& m);

void define_threshold_filter(const py::object& m);

void define_sequence_id_filter(const py::object& m);

void define_noise_removal_filter(const py::object& m);

void define_decimation_filter(const py::object& m);

void define_edge_noise_removal_filter(const py::object& m);

}  // namespace pyorbbecsdk
