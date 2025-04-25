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
#include "record_playback.hpp"

#include "error.hpp"
#include "libobsensor/h/ObTypes.h"
#include "utils.hpp"

namespace pyorbbecsdk {
void define_record(py::object &m) {
  py::class_<ob::RecordDevice, std::shared_ptr<ob::RecordDevice>>(
      m, "RecordDevice")
      .def(py::init<std::shared_ptr<ob::Device>, const std::string &, bool>(),
           py::arg("device"), py::arg("file"), py::arg("compression") = true)
      .def(
          "pause", [](ob::RecordDevice &self) { self.pause(); },
          py::call_guard<py::gil_scoped_release>())

      .def(
          "resume", [](ob::RecordDevice &self) { self.resume(); },
          py::call_guard<py::gil_scoped_release>());
}

void define_playback(py::object &m) {
  py::enum_<OBPlaybackStatus>(m, "PlaybackStatus")
      .value("Stopped", OB_PLAYBACK_STOPPED)
      .value("Playing", OB_PLAYBACK_PLAYING)
      .value("Paused", OB_PLAYBACK_PAUSED)
      .export_values();

  py::class_<ob::PlaybackDevice, ob::Device,
             std::shared_ptr<ob::PlaybackDevice>>(m, "PlaybackDevice")
      .def(py::init<const std::string &>(), py::arg("file"))
      .def(
          "pause", [](ob::PlaybackDevice &self) { self.pause(); },
           py::call_guard<py::gil_scoped_release>())
      .def(
          "resume", [](ob::PlaybackDevice &self) { self.resume(); },
           py::call_guard<py::gil_scoped_release>())
      .def(
          "seek", [](ob::PlaybackDevice &self,const int64_t timestamp) { self.seek(timestamp); }, 
           py::call_guard<py::gil_scoped_release>(), py::arg("timestamp"))
      .def(
          "set_playback_rate",
          [](ob::PlaybackDevice &self, const float rate) {
            self.setPlaybackRate(rate);
          }, 
           py::call_guard<py::gil_scoped_release>(), py::arg("rate"))
      .def("set_playback_status_change_callback",
           [](ob::PlaybackDevice &self, py::function cb) {
             self.setPlaybackStatusChangeCallback([cb](OBPlaybackStatus s) {
               py::gil_scoped_acquire g;
               cb(s);
             });
           })
      .def(
          "get_playback_status",
          [](ob::PlaybackDevice &self) { return self.getPlaybackStatus(); }, 
          py::call_guard<py::gil_scoped_release>()
          )
      .def(
          "get_position",
          [](ob::PlaybackDevice &self) { return self.getPosition(); }, 
          py::call_guard<py::gil_scoped_release>()
          )
      .def(
          "get_duration", [](ob::PlaybackDevice &self) {return  self.getDuration(); },
          py::call_guard<py::gil_scoped_release>()
      );
}
}  // namespace pyorbbecsdk