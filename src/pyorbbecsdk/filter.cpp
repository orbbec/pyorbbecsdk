#include "filter.hpp"

#include "error.hpp"

namespace pyorbbecsdk {
void define_filter(const py::object& m) {
  py::class_<ob::Filter, std::shared_ptr<ob::Filter>>(m, "Filter")
      .def("reset",
           [](const std::shared_ptr<ob::Filter>& self) {
             OB_TRY_CATCH({ self->reset(); });
           })
      .def("process",
           [](const std::shared_ptr<ob::Filter>& self,
              const std::shared_ptr<ob::Frame>& frame) {
             OB_TRY_CATCH({ self->process(frame); });
           })
      .def("push_frame",
           [](const std::shared_ptr<ob::Filter>& self,
              const std::shared_ptr<ob::Frame>& frame) {
             OB_TRY_CATCH({ self->pushFrame(frame); });
           })
      .def("set_callback",
           [](const std::shared_ptr<ob::Filter>& self, py::function& callback) {
             OB_TRY_CATCH({
               self->setCallBack([callback](std::shared_ptr<ob::Frame> frame) {
                 py::gil_scoped_acquire acquire;
                 callback(frame);
               });
             });
           });
}

void define_point_cloud_filter(const py::object& m) {
  py::class_<ob::PointCloudFilter, ob::Filter,
             std::shared_ptr<ob::PointCloudFilter>>(m, "PointCloudFilter")
      .def("set_create_point_format",
           [](const std::shared_ptr<ob::PointCloudFilter>& self,
              OBFormat format) {
             OB_TRY_CATCH({ return self->setCreatePointFormat(format); });
           })
      .def("set_camera_param",
           [](const std::shared_ptr<ob::PointCloudFilter>& self,
              const OBCameraParam& param) {
             OB_TRY_CATCH({ self->setCameraParam(param); });
           })
      .def("set_frame_align_state",
           [](const std::shared_ptr<ob::PointCloudFilter>& self, bool state) {
             OB_TRY_CATCH({ self->setFrameAlignState(state); });
           })
      .def("set_position_data_scaled",
           [](const std::shared_ptr<ob::PointCloudFilter>& self, float scale) {
             OB_TRY_CATCH({ self->setPositionDataScaled(scale); });
           })
      .def("set_color_data_normalization",
           [](const std::shared_ptr<ob::PointCloudFilter>& self, bool state) {
             OB_TRY_CATCH({ self->setColorDataNormalization(state); });
           });
}

void define_format_covert_filter(const py::object& m) {
  py::class_<ob::FormatConvertFilter, ob::Filter,
             std::shared_ptr<ob::FormatConvertFilter>>(m, "FormatConvertFilter")
      .def(
          "set_format_convert_format",
          [](const std::shared_ptr<ob::FormatConvertFilter>& self,
             OBConvertFormat format) {
            OB_TRY_CATCH({ self->setFormatConvertType(format); });
          },
          "Set the format to convert to");
}

}  // namespace pyorbbecsdk
