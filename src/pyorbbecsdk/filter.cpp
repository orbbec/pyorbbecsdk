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

namespace pyorbbecsdk {
void define_filter(const py::object& m) {
  py::class_<ob::Filter, std::shared_ptr<ob::Filter>>(m, "Filter")
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
      .def("set_callback",
           [](ob::Filter& self, py::function& callback) {
             OB_TRY_CATCH({
               self.setCallBack([callback](std::shared_ptr<ob::Frame> frame) {
                 py::gil_scoped_acquire acquire;
                 callback(frame);
               });
             });
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
  py::class_<ob::FormatConvertFilter, ob::Filter,
             std::shared_ptr<ob::FormatConvertFilter>>(m, "FormatConvertFilter")
      .def(py::init<>())
      .def(
          "set_format_convert_format",
          [](ob::FormatConvertFilter& self, OBConvertFormat format) {
            OB_TRY_CATCH({ self.setFormatConvertType(format); });
          },
          "Set the format to convert to");
}

void define_hole_filling_filter(const py::object& m) {
  py::class_<ob::HoleFillingFilter, ob::Filter,
             std::shared_ptr<ob::HoleFillingFilter>>(m, "HoleFillingFilter")
      .def(py::init<>())
      .def(
          "set_filling_mode",
          [](ob::HoleFillingFilter& self, OBHoleFillingMode mode) {
            OB_TRY_CATCH({ self.setFilterMode(mode); });
          },
          "Set the  filling mode")
      .def("get_filling_mode", [](ob::HoleFillingFilter& self) {
        OB_TRY_CATCH({ return self.getFilterMode(); });
      });
}

void define_temporal_filter(const py::object& m) {
  py::class_<ob::TemporalFilter, ob::Filter,
             std::shared_ptr<ob::TemporalFilter>>(m, "TemporalFilter")
      .def(py::init<>())
      .def(
          "get_diff_scale_range",
          [](ob::TemporalFilter& self) {
            OB_TRY_CATCH({ return self.getDiffScaleRange(); });
          },
          "get diff scale range")
      .def(
          "set_diff_scale",
          [](ob::TemporalFilter& self, float value) {
            OB_TRY_CATCH({ self.setDiffScale(value); });
          },
          "set diff scale")
      .def(
          "get_weight_range",
          [](ob::TemporalFilter& self) {
            OB_TRY_CATCH({ return self.getWeightRange(); });
          },
          "get weight range")
      .def("set_weight", [](ob::TemporalFilter& self, float value) {
        OB_TRY_CATCH({ self.setWeight(value); });
      });
}

void define_spatial_advanced_filter(const py::object& m) {
  py::class_<ob::SpatialAdvancedFilter, ob::Filter,
             std::shared_ptr<ob::SpatialAdvancedFilter>>(
      m, "SpatialAdvancedFilter")
      .def(py::init<>())
      .def(
          "get_alpha_range",
          [](ob::SpatialAdvancedFilter& self) {
            OB_TRY_CATCH({ return self.getAlphaRange(); });
          },
          "get alpha range")
      .def("get_disp_diff_range",
           [](ob::SpatialAdvancedFilter& self) {
             OB_TRY_CATCH({ return self.getDispDiffRange(); });
           })
      .def("get_radius_range",
           [](ob::SpatialAdvancedFilter& self) {
             OB_TRY_CATCH({ return self.getRadiusRange(); });
           })
      .def("get_magnitude_range",
           [](ob::SpatialAdvancedFilter& self) {
             OB_TRY_CATCH({ return self.getMagnitudeRange(); });
           })
      .def("get_filter_params",
           [](ob::SpatialAdvancedFilter& self) {
             OB_TRY_CATCH({ return self.getFilterParams(); });
           })
      .def("set_filter_params",
           [](ob::SpatialAdvancedFilter& self,
              const OBSpatialAdvancedFilterParams& params) {
             OB_TRY_CATCH({ self.setFilterParams(params); });
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
  py::class_<ob::Align, ob::Filter, std::shared_ptr<ob::Align>>(m, "Align")
      .def(py::init<OBStreamType>(), py::arg("align_to_stream"))
      .def("get_align_to_stream_type", [](ob::Align& self) {
        OB_TRY_CATCH({ return self.getAlignToStreamType(); });
      });
}

void define_threshold_filter(const py::object& m) {
  py::class_<ob::ThresholdFilter, ob::Filter,
             std::shared_ptr<ob::ThresholdFilter>>(m, "ThresholdFilter")
      .def(py::init<>())
      .def("get_min_range",
           [](ob::ThresholdFilter& self) {
             OB_TRY_CATCH({ return self.getMinRange(); });
           })
      .def("get_max_range",
           [](ob::ThresholdFilter& self) {
             OB_TRY_CATCH({ return self.getMaxRange(); });
           })
      .def("set_value_range",
           [](ob::ThresholdFilter& self, uint16_t min, uint16_t max) {
             OB_TRY_CATCH({ return self.setValueRange(min, max); });
           });
}

void define_sequence_id_filter(const py::object& m) {
  py::class_<ob::SequenceIdFilter, ob::Filter,
             std::shared_ptr<ob::SequenceIdFilter>>(m, "SequenceIdFilter")
      .def(py::init<>())
      .def("select_sequence_id",
           [](ob::SequenceIdFilter& self, int sequence_id) {
             OB_TRY_CATCH({ self.selectSequenceId(sequence_id); });
           })
      .def("get_select_sequence_id",
           [](ob::SequenceIdFilter& self) {
             OB_TRY_CATCH({ return self.getSelectSequenceId(); });
           })
      .def("get_sequence_id_list",
           [](ob::SequenceIdFilter& self) {
             OB_TRY_CATCH({
               auto list_size = self.getSequenceIdListSize();
               auto list = self.getSequenceIdList();
               py::list result;
               for (int i = 0; i < list_size; ++i) {
                 result.append(py::cast(list[i]));
               }
               return result;
             });
           })
      .def("get_sequence_id_list_size", [](ob::SequenceIdFilter& self) {
        OB_TRY_CATCH({ return self.getSequenceIdListSize(); });
      });
}

void define_noise_removal_filter(const py::object& m) {
  py::class_<ob::NoiseRemovalFilter, ob::Filter,
             std::shared_ptr<ob::NoiseRemovalFilter>>(m, "NoiseRemovalFilter")
      .def(py::init<>())
      .def("set_filter_params",
           [](ob::NoiseRemovalFilter& self,
              const OBNoiseRemovalFilterParams& params) {
             OB_TRY_CATCH({ self.setFilterParams(params); });
           })
      .def("get_filter_params",
           [](ob::NoiseRemovalFilter& self) {
             OB_TRY_CATCH({ return self.getFilterParams(); });
           })
      .def("get_disp_diff_range",
           [](ob::NoiseRemovalFilter& self) {
             OB_TRY_CATCH({ return self.getDispDiffRange(); });
           })
      .def("get_max_size_range", [](ob::NoiseRemovalFilter& self) {
        OB_TRY_CATCH({ return self.getMaxSizeRange(); });
      });
}

void define_decimation_filter(const py::object& m) {
  py::class_<ob::DecimationFilter, ob::Filter,
             std::shared_ptr<ob::DecimationFilter>>(m, "DecimationFilter")
      .def(py::init<>())
      .def("set_scale_value",
           [](ob::DecimationFilter& self, uint8_t value) {
             OB_TRY_CATCH({ self.setScaleValue(value); });
           })
      .def("get_scale_value",
           [](ob::DecimationFilter& self) {
             OB_TRY_CATCH({ return self.getScaleValue(); });
           })
      .def("get_scale_range", [](ob::DecimationFilter& self) {
        OB_TRY_CATCH({ return self.getScaleRange(); });
      });
}

void define_edge_noise_removal_filter(const py::object& m) {
  py::class_<ob::EdgeNoiseRemovalFilter, ob::Filter,
             std::shared_ptr<ob::EdgeNoiseRemovalFilter>>(
      m, "EdgeNoiseRemovalFilter")
      .def(py::init<>())
      .def("set_filter_params",
           [](ob::EdgeNoiseRemovalFilter& self,
              const OBEdgeNoiseRemovalFilterParams& params) {
             OB_TRY_CATCH({ self.setFilterParams(params); });
           })
      .def("get_filter_params",
           [](ob::EdgeNoiseRemovalFilter& self) {
             OB_TRY_CATCH({ return self.getFilterParams(); });
           })
      .def("get_margin_left_th_range",
           [](ob::EdgeNoiseRemovalFilter& self) {
             OB_TRY_CATCH({ return self.getMarginLeftThRange(); });
           })
      .def("get_margin_right_th_range",
           [](ob::EdgeNoiseRemovalFilter& self) {
             OB_TRY_CATCH({ return self.getMarginRightThRange(); });
           })
      .def("get_margin_top_th_range",
           [](ob::EdgeNoiseRemovalFilter& self) {
             OB_TRY_CATCH({ return self.getMarginTopThRange(); });
           })
      .def("get_margin_bottom_th_range", [](ob::EdgeNoiseRemovalFilter& self) {
        OB_TRY_CATCH({ return self.getMarginBottomThRange(); });
      });
}

}  // namespace pyorbbecsdk
