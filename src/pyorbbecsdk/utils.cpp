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

#include "utils.hpp"

#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>

#include <libobsensor/hpp/Utils.hpp>


#include "error.hpp"
namespace py = pybind11;
namespace pyorbbecsdk {
std::vector<std::string> split(const std::string& s, const std::string& delim) {
  std::vector<std::string> elems;
  size_t pos = 0;
  size_t len = s.length();
  size_t delim_len = delim.length();
  if (delim_len == 0) return elems;
  while (pos < len) {
    size_t find_pos = s.find(delim, pos);
    if (find_pos == std::string::npos) {
      elems.push_back(s.substr(pos, len - pos));
      break;
    }
    elems.push_back(s.substr(pos, find_pos - pos));
    pos = find_pos + delim_len;
  }
  return elems;
}

void define_coordinate_transform_helper(py::module& m) {
  m.def("calibration_3d_to_3d",
        [](const OBCalibrationParam calibrationParam,
           const OBPoint3f sourcePoint3f, const OBSensorType sourceSensorType,
           const OBSensorType targetSensorType) {
          OBPoint3f result;
          OB_TRY_CATCH({
            ob::CoordinateTransformHelper::calibration3dTo3d(
                calibrationParam, sourcePoint3f, sourceSensorType,
                targetSensorType, &result);
          });
          return result;
        });
  m.def("calibration_3d_to_2d",
        [](const OBCalibrationParam calibrationParam,
           const OBPoint3f sourcePoint3f, const OBSensorType sourceSensorType,
           const OBSensorType targetSensorType) {
          OBPoint2f result;
          OB_TRY_CATCH({
            ob::CoordinateTransformHelper::calibration3dTo2d(
                calibrationParam, sourcePoint3f, sourceSensorType,
                targetSensorType, &result);
          });
          return result;
        });
  m.def("calibration_2d_to_3d",
        [](const OBCalibrationParam calibrationParam,
           const OBPoint2f sourcePoint2f, const float depth,
           const OBSensorType sourceSensorType,
           const OBSensorType targetSensorType) {
          OBPoint3f result;
          OB_TRY_CATCH({
            ob::CoordinateTransformHelper::calibration2dTo3d(
                calibrationParam, sourcePoint2f, depth, sourceSensorType,
                targetSensorType, &result);
          });
          return result;
        });
  m.def("calibration_2d_to_3d_undistortion",
        [](const OBCalibrationParam calibrationParam,
           const OBPoint2f sourcePoint2f, const float depth,
           const OBSensorType sourceSensorType,
           const OBSensorType targetSensorType) {
          OBPoint3f result;
          OB_TRY_CATCH({
            ob::CoordinateTransformHelper::calibration2dTo3dUndistortion(
                calibrationParam, sourcePoint2f, depth, sourceSensorType,
                targetSensorType, &result);
          });
          return result;
        });
  m.def("calibration_3d_to_2d",
        [](const OBCalibrationParam calibrationParam,
           const OBPoint3f sourcePoint3f, const OBSensorType sourceSensorType,
           const OBSensorType targetSensorType) {
          OBPoint2f result;
          OB_TRY_CATCH({
            ob::CoordinateTransformHelper::calibration3dTo2d(
                calibrationParam, sourcePoint3f, sourceSensorType,
                targetSensorType, &result);
          });
          return result;
        });
}
}  // namespace pyorbbecsdk
