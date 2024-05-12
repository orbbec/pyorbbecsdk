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
#include <pybind11/numpy.h>

#include <string>
#include <vector>
#include <pybind11/pybind11.h>
#include <libobsensor/ObSensor.hpp>


namespace py = pybind11;
#define CHECK_NULLPTR(ptr)                                                  \
  do {                                                                      \
    if ((ptr) == nullptr) {                                                 \
      std::ostringstream oss;                                               \
      oss << "Null pointer exception in file " << __FILE__ << ", function " \
          << __FUNCTION__ << ", line " << __LINE__;                         \
      throw std::runtime_error(oss.str());                                  \
    }                                                                       \
  } while (false)

#define CHECK_LE(a, b)                                               \
  do {                                                               \
    if ((a) > (b)) {                                                 \
      std::ostringstream oss;                                        \
      oss << "Invalid argument exception in file " << __FILE__       \
          << ", function " << __FUNCTION__ << ", line " << __LINE__; \
      throw std::invalid_argument(oss.str());                        \
    }                                                                \
  } while (false)

#define CHECK_GE(a, b)                                               \
  do {                                                               \
    if ((a) < (b)) {                                                 \
      std::ostringstream oss;                                        \
      oss << "Invalid argument exception in file " << __FILE__       \
          << ", function " << __FUNCTION__ << ", line " << __LINE__; \
      throw std::invalid_argument(oss.str());                        \
    }                                                                \
  } while (false)

namespace pyorbbecsdk {
std::vector<std::string> split(const std::string& s, const std::string& delim);

void define_coordinate_transform_helper( py::module & m);
}  // namespace pyorbbecsdk

