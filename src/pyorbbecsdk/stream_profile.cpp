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
#include "stream_profile.hpp"

#include "error.hpp"
#include "utils.hpp"

namespace pyorbbecsdk {
void define_stream_profile(const py::object &m) {
  py::class_<ob::StreamProfile, std::shared_ptr<ob::StreamProfile>>(
      m, "StreamProfile")
      .def("get_format",
           [](const std::shared_ptr<ob::StreamProfile> &self) {
             OB_TRY_CATCH({ return self->format(); });
           })
      .def("get_type",
           [](const std::shared_ptr<ob::StreamProfile> &self) {
             OB_TRY_CATCH({ return self->type(); });
           })
      .def("is_video_stream_profile",
           [](const std::shared_ptr<ob::StreamProfile> &self) {
             OB_TRY_CATCH({ return self->is<ob::VideoStreamProfile>(); });
           })
      .def("is_accel_stream_profile",
           [](const std::shared_ptr<ob::StreamProfile> &self) {
             OB_TRY_CATCH({ return self->is<ob::AccelStreamProfile>(); });
           })
      .def("is_gyro_stream_profile",
           [](const std::shared_ptr<ob::StreamProfile> &self) {
             OB_TRY_CATCH({ return self->is<ob::GyroStreamProfile>(); });
           })
      .def("as_video_stream_profile",
           [](std::shared_ptr<ob::StreamProfile> &self) {
             OB_TRY_CATCH({
               if (!self->is<ob::VideoStreamProfile>()) {
                 throw std::invalid_argument("Not a video stream profile");
               }
               return self->as<ob::VideoStreamProfile>();
             });
           })
      .def("as_accel_stream_profile",
           [](std::shared_ptr<ob::StreamProfile> &self) {
             OB_TRY_CATCH({
               if (!self->is<ob::AccelStreamProfile>()) {
                 throw std::invalid_argument("Not an accel stream profile");
               }
               return self->as<ob::AccelStreamProfile>();
             });
           })
      .def("as_gyro_stream_profile",
           [](std::shared_ptr<ob::StreamProfile> &self) {
             OB_TRY_CATCH({
               if (!self->is<ob::GyroStreamProfile>()) {
                 throw std::invalid_argument("Not a gyro stream profile");
               }
               return self->as<ob::GyroStreamProfile>();
             });
           })
      .def("as_lidar_stream_profile",
           [](std::shared_ptr<ob::StreamProfile> &self) {
             OB_TRY_CATCH({
               if (!self->is<ob::LiDARStreamProfile>()) {
                 throw std::invalid_argument("Not a lidar stream profile");
               }
               return self->as<ob::LiDARStreamProfile>();
             });
           })
      .def("bind_extrinsic_to",
           [](const std::shared_ptr<ob::StreamProfile> &self,
              std::shared_ptr<ob::StreamProfile> &target,
              const OBExtrinsic &extrinsic) {
             OB_TRY_CATCH({ return self->bindExtrinsicTo(target, extrinsic); });
           })
      .def("bind_extrinsic_to",
           [](const std::shared_ptr<ob::StreamProfile> &self,
              const OBStreamType &targetStreamType,
              const OBExtrinsic &extrinsic) {
             OB_TRY_CATCH({
               return self->bindExtrinsicTo(targetStreamType, extrinsic);
             });
           })
      .def("get_extrinsic_to",
           [](const std::shared_ptr<ob::StreamProfile> &self,
              const std::shared_ptr<ob::StreamProfile> &target) {
             OB_TRY_CATCH({ return self->getExtrinsicTo(target); });
           });
}

void define_video_stream_profile(const py::object &m) {
  py::class_<ob::VideoStreamProfile, ob::StreamProfile,
             std::shared_ptr<ob::VideoStreamProfile>>(m, "VideoStreamProfile")
      .def("get_width",
           [](const std::shared_ptr<ob::VideoStreamProfile> &self) {
             OB_TRY_CATCH({ return self->width(); });
           })
      .def("get_height",
           [](const std::shared_ptr<ob::VideoStreamProfile> &self) {
             OB_TRY_CATCH({ return self->height(); });
           })
      .def("get_fps",
           [](const std::shared_ptr<ob::VideoStreamProfile> &self) {
             OB_TRY_CATCH({ return self->fps(); });
           })
      .def("get_intrinsic",
           [](const std::shared_ptr<ob::VideoStreamProfile> &self) {
             OB_TRY_CATCH({ return self->getIntrinsic(); });
           })
      .def("get_distortion",
           [](const std::shared_ptr<ob::VideoStreamProfile> &self) {
             OB_TRY_CATCH({ return self->getDistortion(); });
           })
      .def("get_decimation_config",
           [](const std::shared_ptr<ob::VideoStreamProfile> &self) {
             OB_TRY_CATCH({ return self->getDecimationConfig(); });
           })
      .def("__repr__", [](const std::shared_ptr<ob::VideoStreamProfile> &self) {
        OB_TRY_CATCH({
          return "<VideoStreamProfile: " + std::to_string(self->width()) + "x" +
                 std::to_string(self->height()) + "@" +
                 std::to_string(self->fps()) + ">";
        });
      });
}

void define_accel_stream_profile(const py::object &m) {
  py::class_<ob::AccelStreamProfile, ob::StreamProfile,
             std::shared_ptr<ob::AccelStreamProfile>>(m, "AccelStreamProfile")
      .def("get_full_scale_range",
           [](const std::shared_ptr<ob::AccelStreamProfile> &self) {
             OB_TRY_CATCH({ return self->fullScaleRange(); });
           })
      .def("get_sample_rate",
           [](const std::shared_ptr<ob::AccelStreamProfile> &self) {
             OB_TRY_CATCH({ return self->sampleRate(); });
           })
      .def("get_intrinsic",
           [](const std::shared_ptr<ob::AccelStreamProfile> &self) {
             OB_TRY_CATCH({ return self->getIntrinsic(); });
           })
      .def("__repr__", [](const std::shared_ptr<ob::AccelStreamProfile> &self) {
        OB_TRY_CATCH({
          return "<AccelStreamProfile: " +
                 std::to_string(self->fullScaleRange()) + ">";
        });
      });
}

void define_gyro_stream_profile(const py::object &m) {
  py::class_<ob::GyroStreamProfile, ob::StreamProfile,
             std::shared_ptr<ob::GyroStreamProfile>>(m, "GyroStreamProfile")
      .def("get_full_scale_range",
           [](const std::shared_ptr<ob::GyroStreamProfile> &self) {
             OB_TRY_CATCH({ return self->fullScaleRange(); });
           })
      .def("get_sample_rate",
           [](const std::shared_ptr<ob::GyroStreamProfile> &self) {
             OB_TRY_CATCH({ return self->sampleRate(); });
           })
      .def("get_intrinsic",
           [](const std::shared_ptr<ob::GyroStreamProfile> &self) {
             OB_TRY_CATCH({ return self->getIntrinsic(); });
           })
      .def("__repr__", [](const std::shared_ptr<ob::GyroStreamProfile> &self) {
        OB_TRY_CATCH({
          return "<GyroStreamProfile: " + std::to_string(self->fullScaleRange()) +
                 ">";
        });
      });
}

void define_lidar_stream_profile(const py::object &m) {
  py::class_<ob::LiDARStreamProfile, ob::StreamProfile,
             std::shared_ptr<ob::LiDARStreamProfile>>(m, "LiDARStreamProfile")
      .def("get_scan_rate",
           [](const std::shared_ptr<ob::LiDARStreamProfile> &self) {
             OB_TRY_CATCH({ return self->getScanRate(); });
           });
}

void define_stream_profile_list(const py::object &m) {
  py::class_<ob::StreamProfileList, std::shared_ptr<ob::StreamProfileList>>(
      m, "StreamProfileList")
      .def("get_count",
           [](const std::shared_ptr<ob::StreamProfileList> &self) {
             OB_TRY_CATCH({ return self->count(); });
           })
      .def("get_stream_profile_by_index",
           [](const std::shared_ptr<ob::StreamProfileList> &self, int index) {
             OB_TRY_CATCH({ return self->getProfile(index); });
           })
      .def(
          "get_video_stream_profile",
          [](const std::shared_ptr<ob::StreamProfileList> &self, int width,
             int height, OBFormat format, int fps) {
            OB_TRY_CATCH({
              return self->getVideoStreamProfile(width, height, format, fps);
            });
          },
          py::arg("width") = OB_WIDTH_ANY, py::arg("height") = OB_HEIGHT_ANY,
          py::arg("format") = OB_FORMAT_ANY, py::arg("fps") = OB_FPS_ANY)
      .def(
          "get_video_stream_profile",
          [](const std::shared_ptr<ob::StreamProfileList> &self,
             OBHardwareDecimationConfig decimation_config, OBFormat format,
             int fps) {
            OB_TRY_CATCH({
              return self->getVideoStreamProfile(decimation_config, format,
                                                 fps);
            });
          },
          py::arg("decimation_config"), py::arg("format") = OB_FORMAT_ANY,
          py::arg("fps") = OB_FPS_ANY)
      .def("get_accel_stream_profile",
           [](const std::shared_ptr<ob::StreamProfileList> &self,
              OBAccelFullScaleRange full_scale_range,
              OBAccelSampleRate sample_rate) {
             OB_TRY_CATCH({
               return self->getAccelStreamProfile(full_scale_range,
                                                  sample_rate);
             });
           })
      .def("get_gyro_stream_profile",
           [](const std::shared_ptr<ob::StreamProfileList> &self,
              OBGyroFullScaleRange full_scale_range,
              OBGyroSampleRate sample_rate) {
             OB_TRY_CATCH({
               return self->getGyroStreamProfile(full_scale_range, sample_rate);
             });
           })
      .def("get_lidar_stream_profile",
           [](const std::shared_ptr<ob::StreamProfileList> &self,
              OBLiDARScanRate scan_rate, OBFormat format) {
             OB_TRY_CATCH(
                 { return self->getLiDARStreamProfile(scan_rate, format); });
           })
      .def("get_default_video_stream_profile",
           [](const std::shared_ptr<ob::StreamProfileList> &self)
               -> std::shared_ptr<ob::VideoStreamProfile> {
             OB_TRY_CATCH({
               auto default_profile = self->getProfile(0);
               CHECK_NULLPTR(default_profile);
               return default_profile->as<ob::VideoStreamProfile>();
             });
           })
      .def("__len__",
           [](const std::shared_ptr<ob::StreamProfileList> &self) {
             OB_TRY_CATCH({ return self->count(); });
           })
      .def("__getitem__",
           [](const std::shared_ptr<ob::StreamProfileList> &self, int index) {
             OB_TRY_CATCH({ return self->getProfile(index); });
           });
}

}  // namespace pyorbbecsdk
