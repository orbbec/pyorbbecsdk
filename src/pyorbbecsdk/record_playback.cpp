#include "record_playback.hpp"

#include "error.hpp"

namespace pyorbbecsdk {
void define_recorder(const py::object& m) {
  py::class_<ob::Recorder, std::shared_ptr<ob::Recorder>>(m, "Recorder")
      .def("start",
           [](const std::shared_ptr<ob::Recorder>& self,
              const std::string& path) {
             OB_TRY_CATCH({ return self->start(path.c_str()); });
           })
      .def("stop",
           [](const std::shared_ptr<ob::Recorder>& self) {
             OB_TRY_CATCH({ return self->stop(); });
           })
      .def("write", [](const std::shared_ptr<ob::Recorder>& self,
                       const std::shared_ptr<ob::Frame>& frame) {
        OB_TRY_CATCH({ return self->write(frame); });
      });
}

void define_playback(const py::object& m) {
  py::class_<ob::Playback, std::shared_ptr<ob::Playback>>(m, "Playback")
      .def("start",
           [](const std::shared_ptr<ob::Playback>& self,
              const py::function& callback, OBMediaType media_type) {
             OB_TRY_CATCH({
               return self->start(
                   [callback](std::shared_ptr<ob::Frame> frame) {
                     py::gil_scoped_acquire acquire;
                     callback(frame);
                   },
                   media_type);
             });
           })
      .def("stop",
           [](const std::shared_ptr<ob::Playback>& self) {
             OB_TRY_CATCH({ return self->stop(); });
           })
      .def("get_device_info",
           [](const std::shared_ptr<ob::Playback>& self) {
             OB_TRY_CATCH({ return self->getDeviceInfo(); });
           })
      .def("get_camera_param", [](const std::shared_ptr<ob::Playback>& self) {
        OB_TRY_CATCH({ return self->getCameraParam(); });
      });
}
}  // namespace pyorbbecsdk
