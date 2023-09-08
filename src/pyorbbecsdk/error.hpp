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

#define OB_TRY_CATCH(code_block)         \
  do {                                   \
    try {                                \
      code_block                         \
    } catch (const ob::Error &error) {   \
      throw pyorbbecsdk::OBError(error); \
    }                                    \
  } while (false)

namespace pyorbbecsdk {

class OBError : public std::exception {
 public:
  OBError(std::string message, OBExceptionType type, std::string name,
          std::string args) noexcept
      : message_(std::move(message)),
        type_(type),
        name_(std::move(name)),
        args_(std::move(args)) {}

  explicit OBError(const ob::Error &error)
      : message_(error.getMessage()),
        type_(error.getExceptionType()),
        name_(error.getName()),
        args_(error.getArgs()) {}

  const char *what() const noexcept override { return message_.c_str(); }
  OBExceptionType get_type() const noexcept { return type_; }
  const char *get_name() const noexcept { return name_.c_str(); }

 private:
  std::string message_;
  OBExceptionType type_;
  std::string name_;
  std::string args_;
};

void define_orbbec_error(const py::object &m);
}  // namespace pyorbbecsdk
