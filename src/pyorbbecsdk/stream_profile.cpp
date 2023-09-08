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
#include "stream_profile.hpp"

#include "error.hpp"
#include "utils.hpp"

namespace pyorbbecsdk {
void define_stream_profile(const py::object &m) {
  py::class_<ob::StreamProfile, std::shared_ptr<ob::StreamProfile>>(
      m, "StreamProfile")
      .def("get_format",
           [](const std::shared_ptr<ob::StreamProfile> &self) {
             return self->format();
           })
      .def("get_type",
           [](const std::shared_ptr<ob::StreamProfile> &self) {
             return self->type();
           })
      .def("is_video_stream_profile",
           [](const std::shared_ptr<ob::StreamProfile> &self) {
             return self->is<ob::VideoStreamProfile>();
           })
      .def("is_accel_stream_profile",
           [](const std::shared_ptr<ob::StreamProfile> &self) {
             return self->is<ob::AccelStreamProfile>();
           })
      .def("is_gyro_stream_profile",
           [](const std::shared_ptr<ob::StreamProfile> &self) {
             return self->is<ob::GyroStreamProfile>();
           })
      .def("as_video_stream_profile",
           [](std::shared_ptr<ob::StreamProfile> &self) {
             OB_TRY_CATCH({
               if (!self->is<ob::VideoStreamProfile>()) {
                 throw std::invalid_argument("Not a video stream profile");
               }
               return std::make_shared<ob::VideoStreamProfile>(*self);
             });
           })
      .def("as_accel_stream_profile",
           [](std::shared_ptr<ob::StreamProfile> &self) {
             OB_TRY_CATCH({
               if (!self->is<ob::AccelStreamProfile>()) {
                 throw std::invalid_argument("Not an accel stream profile");
               }
               return std::make_shared<ob::AccelStreamProfile>(*self);
             });
           })
      .def("as_gyro_stream_profile",
           [](std::shared_ptr<ob::StreamProfile> &self) {
             OB_TRY_CATCH({
                 if (!self->is<ob::GyroStreamProfile>()) {
                   throw std::invalid_argument("Not a gyro stream profile");
                 }
                 return std::make_shared<ob::GyroStreamProfile>(*self);
             });
           });
}

void define_video_stream_profile(const py::object &m) {
  py::class_<ob::VideoStreamProfile, ob::StreamProfile,
             std::shared_ptr<ob::VideoStreamProfile>>(m, "VideoStreamProfile")
      .def(py::init<ob::StreamProfile &>())
      .def("get_width",
           [](const std::shared_ptr<ob::VideoStreamProfile> &self) {
             return self->width();
           })
      .def("get_height",
           [](const std::shared_ptr<ob::VideoStreamProfile> &self) {
             return self->height();
           })
      .def("get_fps",
           [](const std::shared_ptr<ob::VideoStreamProfile> &self) {
             return self->fps();
           })
      .def("__repr__", [](const std::shared_ptr<ob::VideoStreamProfile> &self) {
        return "<VideoStreamProfile: " + std::to_string(self->width()) + "x" +
               std::to_string(self->height()) + "@" +
               std::to_string(self->fps()) + ">";
      });
}

void define_accel_stream_profile(const py::object &m) {
  py::class_<ob::AccelStreamProfile, ob::StreamProfile,
             std::shared_ptr<ob::AccelStreamProfile>>(m, "AccelStreamProfile")
      .def(py::init<ob::StreamProfile &>())
      .def("get_full_scale_range",
           [](const std::shared_ptr<ob::AccelStreamProfile> &self) {
             return self->fullScaleRange();
           })
      .def("get_sample_rate",
           [](const std::shared_ptr<ob::AccelStreamProfile> &self) {
             return self->sampleRate();
           })
      .def("__repr__", [](const std::shared_ptr<ob::AccelStreamProfile> &self) {
        return "<AccelStreamProfile: " +
               std::to_string(self->fullScaleRange()) + ">";
      });
}

void define_gyro_stream_profile(const py::object &m) {
  py::class_<ob::GyroStreamProfile, ob::StreamProfile,
             std::shared_ptr<ob::GyroStreamProfile>>(m, "GyroStreamProfile")
      .def(py::init<ob::StreamProfile &>())
      .def("get_full_scale_range",
           [](const std::shared_ptr<ob::GyroStreamProfile> &self) {
             return self->fullScaleRange();
           })
      .def("get_sample_rate",
           [](const std::shared_ptr<ob::GyroStreamProfile> &self) {
             return self->sampleRate();
           })
      .def("__repr__", [](const std::shared_ptr<ob::GyroStreamProfile> &self) {
        return "<GyroStreamProfile: " + std::to_string(self->fullScaleRange()) +
               ">";
      });
}

void define_stream_profile_list(const py::object &m) {
  py::class_<ob::StreamProfileList, std::shared_ptr<ob::StreamProfileList>>(
      m, "StreamProfileList")
      .def("get_count",
           [](const std::shared_ptr<ob::StreamProfileList> &self) {
             return self->count();
           })
      .def("get_stream_profile_by_index",
           [](const std::shared_ptr<ob::StreamProfileList> &self, int index) {
             OB_TRY_CATCH({ return self->getProfile(index); });
           })
      .def("get_video_stream_profile",
           [](const std::shared_ptr<ob::StreamProfileList> &self, int width,
              int height, OBFormat format, int fps) {
             OB_TRY_CATCH({
               return self->getVideoStreamProfile(width, height, format, fps);
             });
           })
      .def("get_default_video_stream_profile",
           [](const std::shared_ptr<ob::StreamProfileList> &self)
               -> std::shared_ptr<ob::VideoStreamProfile> {
             auto default_profile = self->getProfile(0);
             CHECK_NULLPTR(default_profile);
             OB_TRY_CATCH(
                 { return std::make_shared<ob::VideoStreamProfile>(*default_profile); });
           })
      .def("__len__", [](const std::shared_ptr<ob::StreamProfileList> &self) {
        return self->count();
      });
}

}  // namespace pyorbbecsdk
