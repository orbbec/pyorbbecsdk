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

#include "filter.hpp"

#include "error.hpp"
#include "utils.hpp"

namespace pyorbbecsdk {
void define_filter(const py::object& m) {
  py::class_<ob::Filter, std::shared_ptr<ob::Filter>>(m, "Filter")
      .def(py::init<>())
      .def(
          "reset",
          [](std::shared_ptr<ob::Filter>& self) {
            CHECK_NULLPTR(self);
            OB_TRY_CATCH({ self->reset(); });
          },
          py::call_guard<py::gil_scoped_release>())
      .def("enable",
           [](std::shared_ptr<ob::Filter>& self, bool enable) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ self->enable(enable); });
           })
      .def("is_enabled",
           [](std::shared_ptr<ob::Filter>& self) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ return self->isEnabled(); });
           })
      .def(
          "process",
          [](std::shared_ptr<ob::Filter>& self,
             std::shared_ptr<ob::Frame> frame) {
            CHECK_NULLPTR(self);
            OB_TRY_CATCH({ return self->process(frame); });
          },
          py::call_guard<py::gil_scoped_release>())
      .def(
          "push_frame",
          [](std::shared_ptr<ob::Filter>& self,
             std::shared_ptr<ob::Frame> frame) {
            CHECK_NULLPTR(self);
            OB_TRY_CATCH({ self->pushFrame(frame); });
          },
          py::call_guard<py::gil_scoped_release>())
      .def("set_callback",
           [](std::shared_ptr<ob::Filter>& self, py::function& callback) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({
               self->setCallBack([callback](std::shared_ptr<ob::Frame> frame) {
                 py::gil_scoped_acquire acquire;
                 callback(frame);
               });
             });
           })
      .def("get_name",
           [](std::shared_ptr<ob::Filter>& self) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ return std::string(self->type()); });
           })
      .def("is_hdr_merge_filter", &ob::Filter::is<ob::HdrMerge>)
      .def("is_sequence_id_filter", &ob::Filter::is<ob::SequenceIdFilter>)
      .def("is_threshold_filter", &ob::Filter::is<ob::ThresholdFilter>)
      .def("is_disparity_transform_filter",
           &ob::Filter::is<ob::DisparityTransform>)
      .def("is_noise_removal_filter", &ob::Filter::is<ob::NoiseRemovalFilter>)
      .def("is_spatial_advanced_filter",
           &ob::Filter::is<ob::SpatialAdvancedFilter>)
      .def("is_temporal_filter", &ob::Filter::is<ob::TemporalFilter>)
      .def("is_hole_filling_filter", &ob::Filter::is<ob::HoleFillingFilter>)
      .def("is_decimation_filter", &ob::Filter::is<ob::DecimationFilter>)
      .def("is_point_cloud_filter", &ob::Filter::is<ob::PointCloudFilter>)
      .def("is_compression_filter", &ob::Filter::is<ob::CompressionFilter>)
      .def("is_decompression_filter", &ob::Filter::is<ob::DecompressionFilter>)
      .def("is_format_converter", &ob::Filter::is<ob::FormatConvertFilter>)
      .def("is_align_filter", &ob::Filter::is<ob::Align>)
      .def("is_edge_noise_removal_filter",
           &ob::Filter::is<ob::EdgeNoiseRemovalFilter>);
}

void define_point_cloud_filter(const py::object& m) {
  py::class_<ob::PointCloudFilter, ob::Filter,
             std::shared_ptr<ob::PointCloudFilter>>(m, "PointCloudFilter")
      .def(py::init<>())
      .def("set_create_point_format",
           [](std::shared_ptr<ob::PointCloudFilter>& self, OBFormat format) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ return self->setCreatePointFormat(format); });
           })
      .def("set_camera_param",
           [](std::shared_ptr<ob::PointCloudFilter>& self,
              const OBCameraParam& param) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ self->setCameraParam(param); });
           })
      .def("set_frame_align_state",
           [](std::shared_ptr<ob::PointCloudFilter>& self, bool state) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ self->setFrameAlignState(state); });
           })
      .def("set_position_data_scaled",
           [](std::shared_ptr<ob::PointCloudFilter>& self, float scale) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ self->setPositionDataScaled(scale); });
           })
      .def("set_color_data_normalization",
           [](std::shared_ptr<ob::PointCloudFilter>& self, bool state) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ self->setColorDataNormalization(state); });
           })
      .def("calculate", [](std::shared_ptr<ob::PointCloudFilter>& self,
                           std::shared_ptr<ob::Frame> frame) {
        CHECK_NULLPTR(self);
        CHECK_NULLPTR(frame);
        auto format = frame->format();
        if (format != OBFormat::OB_FORMAT_RGB_POINT &&
            format != OBFormat::OB_FORMAT_POINT) {
          std::cerr << "Is not a point cloud frame, do you call process first?"
                    << std::endl;
          throw std::runtime_error(
              "Is not a point cloud frame, do you call process first?");
        }
        if (format == OBFormat::OB_FORMAT_RGB_POINT) {
          auto data = frame->data();
          auto data_size = frame->dataSize();
          uint32_t num_of_points = data_size / sizeof(OBColorPoint);
          auto points = reinterpret_cast<OBColorPoint*>(data);
          // Convert to py::array
          py::array::ShapeContainer shape({num_of_points, 6});
          py::array::StridesContainer strides(
              {6 * sizeof(float), sizeof(float)});
          py::dtype dtype("float");
          py::array array(dtype, shape, strides);
          py::array_t<float> result = py::cast<py::array_t<float>>(array);
          py::buffer_info buf_info = result.request();
          auto* ptr = static_cast<float*>(buf_info.ptr);
          for (long i = 0; i < num_of_points; ++i) {
            auto point = points[i];
            size_t index = i * 6;
            ptr[index] = point.x;
            ptr[index + 1] = point.y;
            ptr[index + 2] = point.z;
            ptr[index + 3] = point.r;
            ptr[index + 4] = point.g;
            ptr[index + 5] = point.b;
          }
          return result;
        } else {
          auto data = frame->data();
          auto data_size = frame->dataSize();
          uint32_t num_of_points = data_size / sizeof(OBPoint);
          auto points = reinterpret_cast<OBPoint*>(data);
          // Convert to py::array
          py::array::ShapeContainer shape({num_of_points, 3});
          py::array::StridesContainer strides(
              {3 * sizeof(float), sizeof(float)});
          py::dtype dtype("float");
          py::array array(dtype, shape, strides);
          py::array_t<float> result = py::cast<py::array_t<float>>(array);
          py::buffer_info buf_info = result.request();
          auto* ptr = static_cast<float*>(buf_info.ptr);
          for (long i = 0; i < num_of_points; ++i) {
            auto point = points[i];
            size_t index = i * 3;
            ptr[index] = point.x;
            ptr[index + 1] = point.y;
            ptr[index + 2] = point.z;
          }
          return result;
        }
      });
}

void define_format_covert_filter(const py::object& m) {
  py::class_<ob::FormatConvertFilter, ob::Filter,
             std::shared_ptr<ob::FormatConvertFilter>>(m, "FormatConvertFilter")
      .def(py::init<>())
      .def(
          "set_format_convert_format",
          [](std::shared_ptr<ob::FormatConvertFilter>& self,
             OBConvertFormat format) {
            CHECK_NULLPTR(self);
            OB_TRY_CATCH({ self->setFormatConvertType(format); });
          },
          "Set the format to convert to");
}

void define_hole_filling_filter(const py::object& m) {
  py::class_<ob::HoleFillingFilter, ob::Filter,
             std::shared_ptr<ob::HoleFillingFilter>>(m, "HoleFillingFilter")
      .def(py::init<>())
      .def(
          "set_filling_mode",
          [](std::shared_ptr<ob::HoleFillingFilter>& self,
             OBHoleFillingMode mode) {
            CHECK_NULLPTR(self);
            OB_TRY_CATCH({ self->setFilterMode(mode); });
          },
          "Set the filling mode")
      .def("get_filling_mode",
           [](std::shared_ptr<ob::HoleFillingFilter>& self) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ return self->getFilterMode(); });
           });
}

void define_temporal_filter(const py::object& m) {
  py::class_<ob::TemporalFilter, ob::Filter,
             std::shared_ptr<ob::TemporalFilter>>(m, "TemporalFilter")
      .def(py::init<>())
      .def(
          "get_diff_scale_range",
          [](std::shared_ptr<ob::TemporalFilter>& self) {
            CHECK_NULLPTR(self);
            OB_TRY_CATCH({ return self->getDiffScaleRange(); });
          },
          "get diff scale range")
      .def(
          "set_diff_scale",
          [](std::shared_ptr<ob::TemporalFilter>& self, float value) {
            CHECK_NULLPTR(self);
            OB_TRY_CATCH({ self->setDiffScale(value); });
          },
          "set diff scale")
      .def(
          "get_weight_range",
          [](std::shared_ptr<ob::TemporalFilter>& self) {
            CHECK_NULLPTR(self);
            OB_TRY_CATCH({ return self->getWeightRange(); });
          },
          "get weight range")
      .def("set_weight",
           [](std::shared_ptr<ob::TemporalFilter>& self, float value) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ self->setWeight(value); });
           });
}

void define_spatial_advanced_filter(const py::object& m) {
  py::class_<ob::SpatialAdvancedFilter, ob::Filter,
             std::shared_ptr<ob::SpatialAdvancedFilter>>(
      m, "SpatialAdvancedFilter")
      .def(py::init<>())
      .def(
          "get_alpha_range",
          [](std::shared_ptr<ob::SpatialAdvancedFilter>& self) {
            OB_TRY_CATCH({ return self->getAlphaRange(); });
          },
          "get alpha range")
      .def("get_disp_diff_range",
           [](std::shared_ptr<ob::SpatialAdvancedFilter>& self) {
             OB_TRY_CATCH({ return self->getDispDiffRange(); });
           })
      .def("get_radius_range",
           [](std::shared_ptr<ob::SpatialAdvancedFilter>& self) {
             OB_TRY_CATCH({ return self->getRadiusRange(); });
           })
      .def("get_magnitude_range",
           [](std::shared_ptr<ob::SpatialAdvancedFilter>& self) {
             OB_TRY_CATCH({ return self->getMagnitudeRange(); });
           })
      .def("get_filter_params",
           [](std::shared_ptr<ob::SpatialAdvancedFilter>& self) {
             OB_TRY_CATCH({ return self->getFilterParams(); });
           })
      .def("set_filter_params",
           [](std::shared_ptr<ob::SpatialAdvancedFilter>& self,
              const OBSpatialAdvancedFilterParams& params) {
             OB_TRY_CATCH({ return self->setFilterParams(params); });
           });
}

void define_disparity_transform(const py::object& m) {
  py::class_<ob::DisparityTransform, ob::Filter,
             std::shared_ptr<ob::DisparityTransform>>(m, "DisparityTransform")
      .def(py::init<bool>(), py::arg("depth_to_disparity") = false);
}

void define_HDR_merge_filter(const py::object& m) {
  py::class_<ob::HdrMerge, ob::Filter, std::shared_ptr<ob::HdrMerge>>(
      m, "HDRMergeFilter")
      .def(py::init<>());
}

void define_align_filter(const py::object& m) {
  py::class_<ob::Align, ob::Filter, std::shared_ptr<ob::Align>>(m,
                                                                "AlignFilter")
      .def(py::init<OBStreamType>(), py::arg("align_to_stream"))
      .def("get_align_to_stream_type", [](std::shared_ptr<ob::Align>& self) {
        CHECK_NULLPTR(self);
        OB_TRY_CATCH({ return self->getAlignToStreamType(); });
      });
}

void define_threshold_filter(const py::object& m) {
  py::class_<ob::ThresholdFilter, ob::Filter,
             std::shared_ptr<ob::ThresholdFilter>>(m, "ThresholdFilter")
      .def(py::init<>())
      .def("get_min_range",
           [](std::shared_ptr<ob::ThresholdFilter>& self) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ return self->getMinRange(); });
           })
      .def("get_max_range",
           [](std::shared_ptr<ob::ThresholdFilter>& self) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ return self->getMaxRange(); });
           })
      .def("set_value_range", [](std::shared_ptr<ob::ThresholdFilter>& self,
                                 uint16_t min, uint16_t max) {
        CHECK_NULLPTR(self);
        OB_TRY_CATCH({ return self->setValueRange(min, max); });
      });
}

void define_sequence_id_filter(const py::object& m) {
  py::class_<ob::SequenceIdFilter, ob::Filter,
             std::shared_ptr<ob::SequenceIdFilter>>(m, "SequenceIdFilter")
      .def(py::init<>())
      .def("select_sequence_id",
           [](std::shared_ptr<ob::SequenceIdFilter>& self, int sequence_id) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ self->selectSequenceId(sequence_id); });
           })
      .def("get_select_sequence_id",
           [](std::shared_ptr<ob::SequenceIdFilter>& self) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ return self->getSelectSequenceId(); });
           })
      .def("get_sequence_id_list",
           [](std::shared_ptr<ob::SequenceIdFilter>& self) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({
               auto list_size = self->getSequenceIdListSize();
               auto list = self->getSequenceIdList();
               py::list result;
               for (int i = 0; i < list_size; ++i) {
                 result.append(py::cast(list[i]));
               }
               return result;
             });
           })
      .def("get_sequence_id_list_size",
           [](std::shared_ptr<ob::SequenceIdFilter>& self) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ return self->getSequenceIdListSize(); });
           });
}

void define_noise_removal_filter(const py::object& m) {
  py::class_<ob::NoiseRemovalFilter, ob::Filter,
             std::shared_ptr<ob::NoiseRemovalFilter>>(m, "NoiseRemovalFilter")
      .def(py::init<>())
      .def("set_filter_params",
           [](std::shared_ptr<ob::NoiseRemovalFilter>& self,
              const OBNoiseRemovalFilterParams& params) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ self->setFilterParams(params); });
           })
      .def("get_filter_params",
           [](std::shared_ptr<ob::NoiseRemovalFilter>& self) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ return self->getFilterParams(); });
           })
      .def("get_disp_diff_range",
           [](std::shared_ptr<ob::NoiseRemovalFilter>& self) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ return self->getDispDiffRange(); });
           })
      .def("get_max_size_range",
           [](std::shared_ptr<ob::NoiseRemovalFilter>& self) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ return self->getMaxSizeRange(); });
           });
}

void define_decimation_filter(const py::object& m) {
  py::class_<ob::DecimationFilter, ob::Filter,
             std::shared_ptr<ob::DecimationFilter>>(m, "DecimationFilter")
      .def(py::init<>())
      .def("set_scale_value",
           [](std::shared_ptr<ob::DecimationFilter>& self, uint8_t value) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ self->setScaleValue(value); });
           })
      .def("get_scale_value",
           [](std::shared_ptr<ob::DecimationFilter>& self) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ return self->getScaleValue(); });
           })
      .def("get_scale_range", [](std::shared_ptr<ob::DecimationFilter>& self) {
        CHECK_NULLPTR(self);
        OB_TRY_CATCH({ return self->getScaleRange(); });
      });
}

void define_edge_noise_removal_filter(const py::object& m) {
  py::class_<ob::EdgeNoiseRemovalFilter, ob::Filter,
             std::shared_ptr<ob::EdgeNoiseRemovalFilter>>(
      m, "EdgeNoiseRemovalFilter")
      .def(py::init<>())
      .def("set_filter_params",
           [](std::shared_ptr<ob::EdgeNoiseRemovalFilter>& self,
              const OBEdgeNoiseRemovalFilterParams& params) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ self->setFilterParams(params); });
           })
      .def("get_filter_params",
           [](std::shared_ptr<ob::EdgeNoiseRemovalFilter>& self) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ return self->getFilterParams(); });
           })
      .def("get_margin_left_th_range",
           [](std::shared_ptr<ob::EdgeNoiseRemovalFilter>& self) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ return self->getMarginLeftThRange(); });
           })
      .def("get_margin_right_th_range",
           [](std::shared_ptr<ob::EdgeNoiseRemovalFilter>& self) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ return self->getMarginRightThRange(); });
           })
      .def("get_margin_top_th_range",
           [](std::shared_ptr<ob::EdgeNoiseRemovalFilter>& self) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ return self->getMarginTopThRange(); });
           })
      .def("get_margin_bottom_th_range",
           [](std::shared_ptr<ob::EdgeNoiseRemovalFilter>& self) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ return self->getMarginBottomThRange(); });
           });
}

}  // namespace pyorbbecsdk
