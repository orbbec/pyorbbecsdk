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

#include "pipeline.hpp"

#include "error.hpp"
#include "utils.hpp"

namespace pyorbbecsdk {

Pipeline::Pipeline() : impl_(std::make_shared<ob::Pipeline>()) {}

Pipeline::Pipeline(std::shared_ptr<ob::Device> device)
    : impl_(std::make_shared<ob::Pipeline>(std::move(device))) {}

Pipeline::~Pipeline() noexcept {
  try {
    if (impl_ && is_started_) {
      impl_->stop();
    }
  } catch (const ob::Error &e) {
    std::cerr << "Error stopping pipeline: " << e.getMessage() << std::endl;
  } catch (const std::exception &e) {
    std::cerr << "Error stopping pipeline: " << e.what() << std::endl;
  } catch (...) {
    std::cerr << "Unknown error stopping pipeline" << std::endl;
  }
}

void Pipeline::start(std::shared_ptr<ob::Config> config) {
  CHECK_NULLPTR(impl_);
  OB_TRY_CATCH({ impl_->start(std::move(config)); });
  is_started_ = true;
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
  is_started_ = true;
}

void Pipeline::stop() {
  try {
    if (impl_) {
      impl_->stop();
      is_started_ = false;
    }
  } catch (const ob::Error &e) {
    std::cerr << "Error stopping pipeline: " << e.getMessage() << std::endl;
  } catch (const std::exception &e) {
    std::cerr << "Error stopping pipeline: " << e.what() << std::endl;
  } catch (...) {
    std::cerr << "Unknown error stopping pipeline" << std::endl;
  }
}

std::shared_ptr<ob::Config> Pipeline::get_config() {
  CHECK_NULLPTR(impl_);
  OB_TRY_CATCH({ return impl_->getConfig(); });
}

std::shared_ptr<ob::FrameSet> Pipeline::wait_for_frames(
    uint32_t timeout) const {
  CHECK_NULLPTR(impl_);
  OB_TRY_CATCH({ return impl_->waitForFrames(timeout); });
}

std::shared_ptr<ob::Device> Pipeline::get_device() const {
  OB_TRY_CATCH({ return impl_->getDevice(); });
}

std::shared_ptr<ob::StreamProfileList> Pipeline::get_stream_profile_list(
    OBSensorType sensor_type) const {
  CHECK_NULLPTR(impl_);
  OB_TRY_CATCH({ return impl_->getStreamProfileList(sensor_type); });
}

void Pipeline::enable_frame_sync() const {
  CHECK_NULLPTR(impl_);
  OB_TRY_CATCH({ impl_->enableFrameSync(); });
}

void Pipeline::disable_frame_sync() const {
  CHECK_NULLPTR(impl_);
  OB_TRY_CATCH({ impl_->disableFrameSync(); });
}

OBCameraParam Pipeline::get_camera_param() const {
  CHECK_NULLPTR(impl_);

  OB_TRY_CATCH({ return impl_->getCameraParam(); });
}

std::shared_ptr<ob::StreamProfileList> Pipeline::get_d2c_depth_profile_list(
    std::shared_ptr<ob::StreamProfile> color_profile,
    OBAlignMode align_mode) const {
  CHECK_NULLPTR(impl_);
  OB_TRY_CATCH(
      { return impl_->getD2CDepthProfileList(color_profile, align_mode); });
}

void define_pipeline(py::object &m) {
  py::class_<Pipeline>(m, "Pipeline")
      .def(py::init<>())
      .def(py::init<std::shared_ptr<ob::Device>>())
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
          "get_d2c_depth_profile_list",
          [](Pipeline &self, std::shared_ptr<ob::StreamProfile> color_profile,
             OBAlignMode align_mode) {
            return self.get_d2c_depth_profile_list(color_profile, align_mode);
          },
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
      .def("enable_stream",
           [](std::shared_ptr<ob::Config> &self, OBStreamType stream_type) {
             OB_TRY_CATCH({ self->enableStream(stream_type); });
           })
      .def("enable_stream",
           [](std::shared_ptr<ob::Config> &self, OBSensorType sensor_type) {
             OB_TRY_CATCH({ self->enableStream(sensor_type); });
           })
      .def(
          "enable_video_stream",
          [](std::shared_ptr<ob::Config> &self, OBStreamType stream_type,
             int width, int height, int fps, OBFormat format) {
            OB_TRY_CATCH({
              self->enableVideoStream(stream_type, width, height, fps, format);
            });
          },
          py::arg("stream_type"), py::arg("width") = OB_WIDTH_ANY,
          py::arg("height") = OB_HEIGHT_ANY, py::arg("fps") = 30,
          py::arg("format") = OB_FORMAT_ANY)
      .def(
          "enable_video_stream",
          [](std::shared_ptr<ob::Config> &self, OBSensorType sensor_type,
             int width, int height, int fps, OBFormat format) {
            OB_TRY_CATCH({
              self->enableVideoStream(sensor_type, width, height, fps, format);
            });
          },
          py::arg("sensor_type"), py::arg("width") = OB_WIDTH_ANY,
          py::arg("height") = OB_HEIGHT_ANY, py::arg("fps") = 30,
          py::arg("format") = OB_FORMAT_ANY)
      .def(
          "enable_accel_stream",
          [](std::shared_ptr<ob::Config> &self,
             OBAccelFullScaleRange full_scale_range,
             OBAccelSampleRate sample_rate) {
            OB_TRY_CATCH(
                { self->enableAccelStream(full_scale_range, sample_rate); });
          },
          py::arg("full_scale_range") =
              OBAccelFullScaleRange::OB_ACCEL_FS_UNKNOWN,
          py::arg("sample_rate") = OBAccelSampleRate::OB_SAMPLE_RATE_UNKNOWN)
      .def(
          "enable_gyro_stream",
          [](std::shared_ptr<ob::Config> &self,
             OBGyroFullScaleRange full_scale_range,
             OBGyroSampleRate sample_rate) {
            OB_TRY_CATCH(
                { self->enableGyroStream(full_scale_range, sample_rate); });
          },
          py::arg("full_scale_range") =
              OBGyroFullScaleRange::OB_GYRO_FS_UNKNOWN,
          py::arg("sample_rate") = OBGyroSampleRate::OB_SAMPLE_RATE_UNKNOWN)
      .def("enable_all_stream",
           [](std::shared_ptr<ob::Config> &self) { self->enableAllStream(); })
      .def("disable_stream",
           [](std::shared_ptr<ob::Config> &self, OBStreamType stream_type) {
             OB_TRY_CATCH({ self->disableStream(stream_type); });
           })
      .def("disable_stream",
           [](std::shared_ptr<ob::Config> &self, OBSensorType sensor_type) {
             OB_TRY_CATCH({ self->disableStream(sensor_type); });
           })
      .def("disable_all_stream",
           [](std::shared_ptr<ob::Config> &self) {
             OB_TRY_CATCH({ self->disableAllStream(); });
           })
      .def("set_align_mode",
           [](std::shared_ptr<ob::Config> &self, OBAlignMode align_mode) {
             OB_TRY_CATCH({ self->setAlignMode(align_mode); });
           })
      .def("set_frame_aggregate_output_mode",
           [](std::shared_ptr<ob::Config> &self,
              OBFrameAggregateOutputMode mode) {
             OB_TRY_CATCH({ self->setFrameAggregateOutputMode(mode); });
           })

      .def("set_depth_scale_require", [](std::shared_ptr<ob::Config> &self,
                                         bool depth_scale_required) {
        OB_TRY_CATCH({ self->setDepthScaleRequire(depth_scale_required); });
      });
}

}  // namespace pyorbbecsdk
