#include "filter.hpp"

#include "error.hpp"

namespace pyorbbecsdk {
void define_filter(const py::object& m) {
  py::class_<ob::Filter>(m, "Filter")
      .def(py::init<>())
      .def(
          "reset", [](ob::Filter& self) { OB_TRY_CATCH({ self.reset(); }); },
          py::call_guard<py::gil_scoped_release>())
      .def(
          "process",
          [](ob::Filter& self, std::shared_ptr<ob::Frame> frame) {
            OB_TRY_CATCH({ self.process(frame); });
          },
          py::call_guard<py::gil_scoped_release>())
      .def(
          "push_frame",
          [](ob::Filter& self, std::shared_ptr<ob::Frame> frame) {
            OB_TRY_CATCH({ self.pushFrame(frame); });
          },
          py::call_guard<py::gil_scoped_release>())
      .def("set_callback", [](ob::Filter& self, py::function& callback) {
        OB_TRY_CATCH({
          self.setCallBack([callback](std::shared_ptr<ob::Frame> frame) {
            py::gil_scoped_acquire acquire;
            callback(frame);
          });
        });
      });
}

void define_point_cloud_filter(const py::object& m) {
  py::class_<ob::PointCloudFilter, ob::Filter>(m, "PointCloudFilter")
      .def(py::init<>())
      .def("set_create_point_format",
           [](ob::PointCloudFilter& self, OBFormat format) {
             OB_TRY_CATCH({ return self.setCreatePointFormat(format); });
           })
      .def("set_camera_param",
           [](ob::PointCloudFilter& self, const OBCameraParam& param) {
             OB_TRY_CATCH({ self.setCameraParam(param); });
           })
      .def("set_frame_align_state",
           [](ob::PointCloudFilter& self, bool state) {
             OB_TRY_CATCH({ self.setFrameAlignState(state); });
           })
      .def("set_position_data_scaled",
           [](ob::PointCloudFilter& self, float scale) {
             OB_TRY_CATCH({ self.setPositionDataScaled(scale); });
           })
      .def("set_color_data_normalization",
           [](ob::PointCloudFilter& self, bool state) {
             OB_TRY_CATCH({ self.setColorDataNormalization(state); });
           });
}

void define_format_covert_filter(const py::object& m) {
  py::class_<ob::FormatConvertFilter, ob::Filter>(m, "FormatConvertFilter")
      .def(py::init<>())
      .def(
          "set_format_convert_format",
          [](ob::FormatConvertFilter& self, OBConvertFormat format) {
            OB_TRY_CATCH({ self.setFormatConvertType(format); });
          },
          "Set the format to convert to");
}

}  // namespace pyorbbecsdk
