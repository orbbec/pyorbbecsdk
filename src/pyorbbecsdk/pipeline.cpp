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

#include "pipeline.hpp"

#include "error.hpp"
#include "utils.hpp"

namespace pyorbbecsdk {

Pipeline::Pipeline() : impl_(std::make_shared<ob::Pipeline>()) {}

Pipeline::Pipeline(std::shared_ptr<ob::Device> device)
    : impl_(std::make_shared<ob::Pipeline>(std::move(device))) {}

Pipeline::Pipeline(const std::string &bag_path)
    : impl_(std::make_shared<ob::Pipeline>(bag_path.c_str())) {}

Pipeline::~Pipeline() {
  if (impl_) {
    impl_->stop();
  }
}

void Pipeline::start(std::shared_ptr<ob::Config> config) {
  CHECK_NULLPTR(impl_);
  // CHECK_NULLPTR(config);
  OB_TRY_CATCH({ impl_->start(std::move(config)); });
}

void Pipeline::start(std::shared_ptr<ob::Config> config,
                     const py::function &callback) {
  CHECK_NULLPTR(impl_);
  CHECK_NULLPTR(config);
  OB_TRY_CATCH({
    impl_->start(std::move(config),
                 [callback](std::shared_ptr<ob::FrameSet> fs) {
                   py::gil_scoped_acquire acquire;
                   callback(fs);
                 });
  });
}

void Pipeline::stop() {
  CHECK_NULLPTR(impl_);
  impl_->stop();
}

std::shared_ptr<ob::Config> Pipeline::get_config() {
  CHECK_NULLPTR(impl_);
  OB_TRY_CATCH({ return impl_->getConfig(); });
}

std::shared_ptr<ob::FrameSet> Pipeline::wait_for_frames(uint32_t timeout) {
  CHECK_NULLPTR(impl_);
  OB_TRY_CATCH({ return impl_->waitForFrames(timeout); });
}

std::shared_ptr<ob::Playback> Pipeline::get_playback() {
  CHECK_NULLPTR(impl_);
  OB_TRY_CATCH({ return impl_->getPlayback(); });
}

std::shared_ptr<ob::Device> Pipeline::get_device() {
  OB_TRY_CATCH({ return impl_->getDevice(); });
}

std::shared_ptr<ob::StreamProfileList> Pipeline::get_stream_profile_list(
    OBSensorType sensor_type) {
  CHECK_NULLPTR(impl_);
  OB_TRY_CATCH({ return impl_->getStreamProfileList(sensor_type); });
}

void Pipeline::enable_frame_sync() {
  CHECK_NULLPTR(impl_);
  OB_TRY_CATCH({ impl_->enableFrameSync(); });
}

void Pipeline::disable_frame_sync() {
  CHECK_NULLPTR(impl_);
  OB_TRY_CATCH({ impl_->disableFrameSync(); });
}

OBCameraParam Pipeline::get_camera_param() {
  CHECK_NULLPTR(impl_);

  OB_TRY_CATCH({ return impl_->getCameraParam(); });
}

OBRect Pipeline::get_d2c_valid_area(uint32_t minimum_z, uint32_t maximum_z) {
  CHECK_NULLPTR(impl_);
  OB_TRY_CATCH({ return impl_->getD2CValidArea(minimum_z, maximum_z); });
}

void Pipeline::switch_config(std::shared_ptr<ob::Config> config) {
  CHECK_NULLPTR(impl_);
  CHECK_NULLPTR(config);
  OB_TRY_CATCH({ impl_->switchConfig(std::move(config)); });
}

void Pipeline::start_recording(const std::string &file_path) {
  CHECK_NULLPTR(impl_);
  OB_TRY_CATCH({ impl_->startRecord(file_path.c_str()); });
}

void Pipeline::stop_recording() {
  OB_TRY_CATCH({ impl_->stopRecord(); });
}

void define_pipeline(py::object &m) {
  py::class_<Pipeline>(m, "Pipeline")
      .def(py::init<>())
      .def(py::init<std::shared_ptr<ob::Device>>())
      .def(py::init<const std::string &>())
      .def("start",
           [](Pipeline &self, std::shared_ptr<ob::Config> config) {
             self.start(std::move(config));
           })
      .def("start",
           [](Pipeline &self, std::shared_ptr<ob::Config> config,
              const py::function &callback) {
             self.start(std::move(config), callback);
           })
      .def("start", [](Pipeline &self) { self.start(nullptr); })
      .def(
          "stop", [](Pipeline &self) { self.stop(); },
          py::call_guard<py::gil_scoped_release>())
      .def(
          "get_config", [](Pipeline &self) { return self.get_config(); },
          py::call_guard<py::gil_scoped_release>())
      .def(
          "wait_for_frames",
          [](Pipeline &self, uint32_t timeout) {
            return self.wait_for_frames(timeout);
          },
          py::call_guard<py::gil_scoped_release>())
      .def(
          "get_playback", [](Pipeline &self) { return self.get_playback(); },
          py::call_guard<py::gil_scoped_release>())
      .def(
          "get_device", [](Pipeline &self) { return self.get_device(); },
          py::call_guard<py::gil_scoped_release>())
      .def(
          "get_stream_profile_list",
          [&](Pipeline &self, OBSensorType sensor_type) {
            return self.get_stream_profile_list(sensor_type);
          },
          py::call_guard<py::gil_scoped_release>())
      .def(
          "enable_frame_sync", [](Pipeline &self) { self.enable_frame_sync(); },
          py::call_guard<py::gil_scoped_release>())
      .def(
          "disable_frame_sync",
          [](Pipeline &self) { self.disable_frame_sync(); },
          py::call_guard<py::gil_scoped_release>())
      .def(
          "get_camera_param",
          [](Pipeline &self) { return self.get_camera_param(); },
          py::call_guard<py::gil_scoped_release>())
      .def(
          "get_d2c_valid_area",
          [](Pipeline &self, uint32_t minimum_z, uint32_t maximum_z) {
            return self.get_d2c_valid_area(minimum_z, maximum_z);
          },
          py::call_guard<py::gil_scoped_release>())
      .def(
          "switch_config",
          [](Pipeline &self, std::shared_ptr<ob::Config> config) {
            self.switch_config(std::move(config));
          },
          py::call_guard<py::gil_scoped_release>())
      .def(
          "start_recording",
          [](Pipeline &self, const std::string &file_path) {
            self.start_recording(file_path);
          },
          py::call_guard<py::gil_scoped_release>())
      .def(
          "stop_recording", [](Pipeline &self) { self.stop_recording(); },
          py::call_guard<py::gil_scoped_release>());
}

void define_pipeline_config(py::object &m) {
  py::class_<ob::Config, std::shared_ptr<ob::Config>>(m, "Config")
      .def(py::init<>())
      .def("enable_stream",
           [](std::shared_ptr<ob::Config> &self,
              const std::shared_ptr<ob::StreamProfile> &stream_profile) {
             OB_TRY_CATCH({ self->enableStream(stream_profile); });
           })
      .def("enable_all_stream",
           [](std::shared_ptr<ob::Config> &self) { self->enableAllStream(); })
      .def("disable_stream",
           [](std::shared_ptr<ob::Config> &self, OBStreamType stream_type) {
             OB_TRY_CATCH({ self->disableStream(stream_type); });
           })
      .def("disable_all_stream",
           [](std::shared_ptr<ob::Config> &self) {
             OB_TRY_CATCH({ self->disableAllStream(); });
           })
      .def("set_align_mode",
           [](std::shared_ptr<ob::Config> &self, OBAlignMode align_mode) {
             OB_TRY_CATCH({ self->setAlignMode(align_mode); });
           })
      .def(
          "set_depth_scale_require",
          [](std::shared_ptr<ob::Config> &self, bool depth_scale_required) {
            OB_TRY_CATCH({ self->setDepthScaleRequire(depth_scale_required); });
          })
      .def("set_d2c_target_resolution", [](std::shared_ptr<ob::Config> &self,
                                           uint32_t width, uint32_t height) {
        OB_TRY_CATCH({ self->setD2CTargetResolution(width, height); });
      });
}

}  // namespace pyorbbecsdk
