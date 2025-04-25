/*******************************************************************************
 * Copyright (c) 2024 Orbbec 3D Technology, Inc
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
  m.def("transformation3dto3d",
        [](const OBPoint3f source, const OBExtrinsic& extrinsic) {
          OBPoint3f result;
          OB_TRY_CATCH({
            ob::CoordinateTransformHelper::transformation3dto3d(
                source, extrinsic, &result);
          });
          return result;
        })
      .def("transformation3dto2d",
           [](const OBPoint3f source, const OBCameraIntrinsic& target_intrinsic,
              const OBCameraDistortion& target_distortion,
              const OBExtrinsic& extrinsic) {
             OBPoint2f result;
             OB_TRY_CATCH({
               ob::CoordinateTransformHelper::transformation3dto2d(
                   source, target_intrinsic, target_distortion, extrinsic,
                   &result);
             });
             return result;
           })
      .def("transformation2dto2d",
           [](const OBPoint2f source, const float depth,
              const OBCameraIntrinsic source_intrinsic,
              const OBCameraDistortion source_distortion,
              const OBCameraIntrinsic target_intrinsic,
              const OBCameraDistortion target_distortion,
              OBExtrinsic extrinsic) {
             OBPoint2f result;
             OB_TRY_CATCH({
               ob::CoordinateTransformHelper::transformation2dto2d(
                   source, depth, source_intrinsic, source_distortion,
                   target_intrinsic, target_distortion, extrinsic, &result);
             });
             return result;
           })
      .def("transformation2dto3d",
           [](const OBPoint2f source, const float depth,
              const OBCameraIntrinsic intrinsic, OBExtrinsic extrinsic) {
             OBPoint3f result;
             OB_TRY_CATCH({
               ob::CoordinateTransformHelper::transformation2dto3d(
                   source, depth, intrinsic, extrinsic, &result);
             });
             return result;
           });
}

void define_point_cloud_helper(py::module& m) {
  m.def(
      "save_point_cloud_to_ply",
      [](const char* file_name, std::shared_ptr<ob::Frame> frame,
         bool save_binary, bool use_mesh, float mesh_threshold) {
        OB_TRY_CATCH({
          ob::PointCloudHelper::savePointcloudToPly(
              file_name, frame, save_binary, use_mesh, mesh_threshold);
        });
      },
      py::arg("file_name"), py::arg("frame"), py::arg("save_binary") = false,
      py::arg("use_mesh") = false, py::arg("mesh_threshold") = 50.0f);
}

}  // namespace pyorbbecsdk
