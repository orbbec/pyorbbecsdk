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

#include "filter.hpp"

#include "error.hpp"
#include "utils.hpp"
#include <pybind11/stl.h>
#include <pybind11/functional.h>
#include <pybind11/chrono.h>
#include <pybind11/complex.h>
namespace pyorbbecsdk {
void define_filter(const py::object& m) {
  py::class_<ob::Filter, std::shared_ptr<ob::Filter>>(m, "Filter")
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
      .def("process",
           [](std::shared_ptr<ob::Filter>& self,
              std::shared_ptr<ob::Frame> frame) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({
               auto out = self->process(frame);
               if (!out) {
                 return py::object(py::none());
               } else if (out->is<ob::FrameSet>()) {
                 return py::cast(out->as<ob::FrameSet>());
               } else if (out->is<ob::ColorFrame>()) {
                 return py::cast(out->as<ob::ColorFrame>());
               } else if (out->is<ob::DepthFrame>()) {
                 return py::cast(out->as<ob::DepthFrame>());
               } else if (out->is<ob::IRFrame>()) {
                 return py::cast(out->as<ob::IRFrame>());
               } else if (out->is<ob::ConfidenceFrame>()) {
                 return py::cast(out->as<ob::ConfidenceFrame>());
               } else if (out->is<ob::PointsFrame>()) {
                 return py::cast(out->as<ob::PointsFrame>());
               }
               return py::cast(out);
             });
           })
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
      .def("get_config_schema_vec",
           [](std::shared_ptr<ob::Filter>& self) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ return self->getConfigSchemaVec(); });
           })
      .def("get_config_value",
           [](std::shared_ptr<ob::Filter>& self,
              const std::string& config_name) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ return self->getConfigValue(config_name.c_str()); });
           })
      .def(
          "set_config_value",
          [](std::shared_ptr<ob::Filter>& self, const std::string& config_name,
             double value) {
            CHECK_NULLPTR(self);
            OB_TRY_CATCH({ self->setConfigValue(config_name.c_str(), value); });
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
      .def("is_format_converter", &ob::Filter::is<ob::FormatConvertFilter>)
      .def("is_align_filter", &ob::Filter::is<ob::Align>)
      .def("is_edge_noise_removal_filter",
           &ob::Filter::is<ob::EdgeNoiseRemovalFilter>)
      .def("is_undistortion_filter",
           &ob::Filter::is<ob::UnDistortionFilter>)
      .def("is_mgc_noise_removal_filter",
           &ob::Filter::is<ob::MgcNoiseRemovalFilter>)
      .def("is_lut_noise_removal_filter",
           &ob::Filter::is<ob::LutNoiseRemovalFilter>)
      .def("is_enhanced_depth_filter",
           &ob::Filter::is<ob::EnhancedDepthFilter>)
      .def("is_spatial_fast_filter",
           &ob::Filter::is<ob::SpatialFastFilter>)
      .def("is_spatial_moderate_filter",
           &ob::Filter::is<ob::SpatialModerateFilter>)
      .def("is_false_positive_filter",
           &ob::Filter::is<ob::FalsePositiveFilter>);
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
      .def("set_decimation_factor",
           [](std::shared_ptr<ob::PointCloudFilter>& self, int value) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ self->setDecimationFactor(value); });
           })
      .def("get_decimation_factor_range",
           [](std::shared_ptr<ob::PointCloudFilter>& self) {
             CHECK_NULLPTR(self);
             OBIntPropertyRange range;
             OB_TRY_CATCH({ range = self->getDecimationFactorRange(); });
             return range;
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
      .def("set_coordinate_data_scaled",
           [](std::shared_ptr<ob::PointCloudFilter>& self, float scale) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ self->setCoordinateDataScaled(scale); });
           })
      .def("set_coordinate_system",
           [](std::shared_ptr<ob::PointCloudFilter>& self,
              OBCoordinateSystemType system) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ self->setCoordinateSystem(system); });
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
        OB_TRY_CATCH({
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
            auto points = static_cast<OBColorPoint*>(data);
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
      .def(py::init<const std::string&>(), py::arg("activationKey") = "");
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
      })
      .def("set_match_target_resolution",
           [](std::shared_ptr<ob::Align>& self, bool enable) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ self->setMatchTargetResolution(enable); });
           })
      .def("set_align_to_stream_profile",
           [](std::shared_ptr<ob::Align>& self,
              std::shared_ptr<const ob::StreamProfile> profile) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ self->setAlignToStreamProfile(profile); });
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
      .def(py::init<const std::string&>(), py::arg("activation_key") = "")
      .def("get_margin_x_th_range",
           [](std::shared_ptr<ob::EdgeNoiseRemovalFilter>& self) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ return self->getMarginXthRange(); });
           })
      .def("get_margin_y_th_range",
           [](std::shared_ptr<ob::EdgeNoiseRemovalFilter>& self) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ return self->getMarginYthRange(); });
           })
      .def("get_limit_x_th_range",
           [](std::shared_ptr<ob::EdgeNoiseRemovalFilter>& self) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ return self->getLimitXthRange(); });
           })
      .def("get_limit_y_th_range",
           [](std::shared_ptr<ob::EdgeNoiseRemovalFilter>& self) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ return self->getLimitYthRange(); });
           })
      .def("get_vertical_direction_enable_range",
           [](std::shared_ptr<ob::EdgeNoiseRemovalFilter>& self) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ return self->getVerticalDirectionEnableRange(); });
           })
      .def("get_width_range",
           [](std::shared_ptr<ob::EdgeNoiseRemovalFilter>& self) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ return self->getWidthRange(); });
           })
      .def("get_height_range",
           [](std::shared_ptr<ob::EdgeNoiseRemovalFilter>& self) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ return self->getHeightRange(); });
           })
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
           });
}

// MgcNoiseRemovalFilter for SDK v2.8.1
void define_mgc_noise_removal_filter(const py::object& m) {
  py::class_<ob::MgcNoiseRemovalFilter, ob::Filter,
             std::shared_ptr<ob::MgcNoiseRemovalFilter>>(
      m, "MgcNoiseRemovalFilter")
      .def(py::init<const std::string&>(), py::arg("activation_key") = "")
      .def("set_filter_params",
           [](std::shared_ptr<ob::MgcNoiseRemovalFilter>& self,
              const OBMgcNoiseRemovalFilterParams& params) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ self->setFilterParams(params); });
           })
      .def("get_filter_params",
           [](std::shared_ptr<ob::MgcNoiseRemovalFilter>& self) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ return self->getFilterParams(); });
           })
      .def("get_max_width_left_range",
           [](std::shared_ptr<ob::MgcNoiseRemovalFilter>& self) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ return self->getMaxWidthLeftRange(); });
           })
      .def("get_max_width_right_range",
           [](std::shared_ptr<ob::MgcNoiseRemovalFilter>& self) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ return self->getMaxWidthRightRange(); });
           })
      .def("get_max_radius_range",
           [](std::shared_ptr<ob::MgcNoiseRemovalFilter>& self) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ return self->getMaxRadiusRange(); });
           })
      .def("get_margin_x_th_range",
           [](std::shared_ptr<ob::MgcNoiseRemovalFilter>& self) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ return self->getMarginXthRange(); });
           })
      .def("get_margin_y_th_range",
           [](std::shared_ptr<ob::MgcNoiseRemovalFilter>& self) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ return self->getMarginYthRange(); });
           })
      .def("get_limit_x_th_range",
           [](std::shared_ptr<ob::MgcNoiseRemovalFilter>& self) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ return self->getLimitXthRange(); });
           })
      .def("get_limit_y_th_range",
           [](std::shared_ptr<ob::MgcNoiseRemovalFilter>& self) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ return self->getLimitYthRange(); });
           })
      .def("get_width_range",
           [](std::shared_ptr<ob::MgcNoiseRemovalFilter>& self) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ return self->getWidthRange(); });
           })
      .def("get_height_range",
           [](std::shared_ptr<ob::MgcNoiseRemovalFilter>& self) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ return self->getHeightRange(); });
           });
}

// LutNoiseRemovalFilter for SDK v2.8.1
void define_lut_noise_removal_filter(const py::object& m) {
  py::class_<ob::LutNoiseRemovalFilter, ob::Filter,
             std::shared_ptr<ob::LutNoiseRemovalFilter>>(
      m, "LutNoiseRemovalFilter")
      .def(py::init<const std::string&>(), py::arg("activation_key") = "")
      .def("set_filter_params",
           [](std::shared_ptr<ob::LutNoiseRemovalFilter>& self,
              const OBLutNoiseRemovalFilterParams& params) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ self->setFilterParams(params); });
           })
      .def("get_filter_params",
           [](std::shared_ptr<ob::LutNoiseRemovalFilter>& self) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ return self->getFilterParams(); });
           })
      .def("get_max_lut_range",
           [](std::shared_ptr<ob::LutNoiseRemovalFilter>& self, int index) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ return self->getMaxLutRange(index); });
           })
      .def("get_min_diff_range",
           [](std::shared_ptr<ob::LutNoiseRemovalFilter>& self) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ return self->getMinDiffRange(); });
           })
      .def("get_width_range",
           [](std::shared_ptr<ob::LutNoiseRemovalFilter>& self) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ return self->getWidthRange(); });
           })
      .def("get_height_range",
           [](std::shared_ptr<ob::LutNoiseRemovalFilter>& self) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ return self->getHeightRange(); });
           });
}

// UnDistortionFilter for SDK v2.9.0
void define_undistortion_filter(const py::object& m) {
  py::class_<ob::UnDistortionFilter, ob::Filter,
             std::shared_ptr<ob::UnDistortionFilter>>(
      m, "UnDistortionFilter")
      .def(py::init<OBStreamType>(), py::arg("stream_type") = OB_STREAM_COLOR)
      .def("set_stream_type",
           [](std::shared_ptr<ob::UnDistortionFilter>& self,
              OBStreamType stream_type) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ self->setStreamType(stream_type); });
           })
      .def("get_stream_type",
           [](std::shared_ptr<ob::UnDistortionFilter>& self) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ return self->getStreamType(); });
           })
      .def("set_new_camera_matrix",
           [](std::shared_ptr<ob::UnDistortionFilter>& self,
              const OBCameraIntrinsic& depth_intrinsic) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ self->setNewCameraMatrix(depth_intrinsic); });
           })
      .def("clear_new_camera_matrix",
           [](std::shared_ptr<ob::UnDistortionFilter>& self) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ self->clearNewCameraMatrix(); });
           });
}

// EnhancedDepthFilter for SDK v2.9.3
// Enhanced depth filter that requires a device for activation. Constructed with
// a device (bound to it) and an optional inference model path.
void define_enhanced_depth_filter(const py::object& m) {
  py::class_<ob::EnhancedDepthFilter, ob::Filter,
             std::shared_ptr<ob::EnhancedDepthFilter>>(
      m, "EnhancedDepthFilter")
      .def(py::init<std::shared_ptr<ob::Device>, const std::string &>(),
           py::arg("device"), py::arg("model_path") = "")
      .def_static(
          "get_supported_resolutions",
          []() {
            // Return a list of (width, height) tuples to avoid exposing a
            // std::pair caster at the Python boundary.
            const auto &res =
                ob::EnhancedDepthFilter::getSupportedResolutions();
            py::list lst;
            for (const auto &p : res) {
              lst.append(py::make_tuple(p.first, p.second));
            }
            return lst;
          },
          "Get the list of supported {width, height} pairs for the "
          "constrained (aligned-to) stream")
      .def_static(
          "get_supported_formats",
          [](OBStreamType stream_type) {
            const auto fmts =
                ob::EnhancedDepthFilter::getSupportedFormats(stream_type);
            py::list lst;
            for (auto f : fmts) {
              lst.append(f);
            }
            return lst;
          },
          py::arg("stream_type"),
          "Get the list of supported frame formats for the given stream "
          "type (color: RGB; depth: Y10/Y11/Y12/Y14/Y16/Z16). Empty for "
          "unsupported stream types")
      .def_static(
          "is_supported_resolution",
          [](OBStreamType source_stream_type, OBStreamType align_to_stream_type,
             uint32_t width, uint32_t height) {
            return ob::EnhancedDepthFilter::isSupportedResolution(
                source_stream_type, align_to_stream_type, width, height);
          },
          py::arg("source_stream_type"), py::arg("align_to_stream_type"),
          py::arg("width"), py::arg("height"),
          "Check whether a resolution is supported for the given stream "
          "alignment pair")
      .def_static(
          "is_supported_format",
          [](OBStreamType stream_type, OBFormat format) {
            return ob::EnhancedDepthFilter::isSupportedFormat(stream_type,
                                                              format);
          },
          py::arg("stream_type"), py::arg("format"),
          "Check whether a frame format is supported for the given stream "
          "type")
      .def("set_resolution",
           [](std::shared_ptr<ob::EnhancedDepthFilter>& self, uint32_t width,
              uint32_t height) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ self->setResolution(width, height); });
           },
           py::arg("width"), py::arg("height"),
           "Set the working resolution of the enhanced depth filter")
      .def("get_current_width",
           [](std::shared_ptr<ob::EnhancedDepthFilter>& self) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ return self->getCurrentWidth(); });
           },
           "Get the current configured frame width")
      .def("get_current_height",
           [](std::shared_ptr<ob::EnhancedDepthFilter>& self) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ return self->getCurrentHeight(); });
           },
           "Get the current configured frame height")
      .def("set_confidence_threshold",
           [](std::shared_ptr<ob::EnhancedDepthFilter>& self, uint32_t value) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ self->setConfidenceThreshold(value); });
           },
           py::arg("value"), "Set the confidence threshold for depth values")
      .def("get_confidence_threshold_range",
           [](std::shared_ptr<ob::EnhancedDepthFilter>& self) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ return self->getConfidenceThresholdRange(); });
           },
           "Get the property range of the confidence threshold");
}

void define_filter_factory(const py::object& m) {
  py::class_<ob::FilterFactory>(m, "FilterFactory")
      .def_static("create_filter",
                  [](const std::string& name) {
                    OB_TRY_CATCH({ return ob::FilterFactory::createFilter(name); });
                  },
                  py::arg("name"), "Create a filter by name")
      .def_static("create_private_filter",
                  [](const std::string& name, const std::string& activation_key) {
                    OB_TRY_CATCH({
                      return ob::FilterFactory::createPrivateFilter(name,
                                                                   activation_key);
                    });
                  },
                  py::arg("name"), py::arg("activation_key") = "",
                  "Create a private filter by name and activation key")
      .def_static("get_filter_vendor_specific_code",
                  [](const std::string& name) {
                    OB_TRY_CATCH({
                      return ob::FilterFactory::getFilterVendorSpecificCode(name);
                    });
                  },
                  py::arg("name"),
                  "Get the vendor specific code of a filter by name");
}

void define_spatial_fast_filter(const py::object& m) {
  py::class_<ob::SpatialFastFilter, ob::Filter,
             std::shared_ptr<ob::SpatialFastFilter>>(m, "SpatialFastFilter")
      .def(py::init<const std::string&>(), py::arg("activation_key") = "")
      .def("get_radius_range",
           [](std::shared_ptr<ob::SpatialFastFilter>& self) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ return self->getRadiusRange(); });
           })
      .def("get_filter_params",
           [](std::shared_ptr<ob::SpatialFastFilter>& self) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ return self->getFilterParams(); });
           })
      .def("set_filter_params",
           [](std::shared_ptr<ob::SpatialFastFilter>& self,
              const OBSpatialFastFilterParams& params) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ self->setFilterParams(params); });
           });
}

void define_spatial_moderate_filter(const py::object& m) {
  py::class_<ob::SpatialModerateFilter, ob::Filter,
             std::shared_ptr<ob::SpatialModerateFilter>>(
      m, "SpatialModerateFilter")
      .def(py::init<const std::string&>(), py::arg("activation_key") = "")
      .def("get_magnitude_range",
           [](std::shared_ptr<ob::SpatialModerateFilter>& self) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ return self->getMagnitudeRange(); });
           })
      .def("get_radius_range",
           [](std::shared_ptr<ob::SpatialModerateFilter>& self) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ return self->getRadiusRange(); });
           })
      .def("get_disp_diff_range",
           [](std::shared_ptr<ob::SpatialModerateFilter>& self) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ return self->getDispDiffRange(); });
           })
      .def("get_filter_params",
           [](std::shared_ptr<ob::SpatialModerateFilter>& self) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ return self->getFilterParams(); });
           })
      .def("set_filter_params",
           [](std::shared_ptr<ob::SpatialModerateFilter>& self,
              const OBSpatialModerateFilterParams& params) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ self->setFilterParams(params); });
           });
}

void define_false_positive_filter(const py::object& m) {
  py::class_<ob::FalsePositiveFilter, ob::Filter,
             std::shared_ptr<ob::FalsePositiveFilter>>(m, "FalsePositiveFilter")
      .def(py::init<const std::string&>(), py::arg("activation_key") = "")
      // fpEdgeBleed group
      .def("get_fp_edge_bleed_filter_enable_range",
           [](std::shared_ptr<ob::FalsePositiveFilter>& self) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ return self->getfpEdgeBleedFilterEnableRange(); });
           })
      // fpebfROI group
      .def("get_fpebf_roi_min_x_ratio_range",
           [](std::shared_ptr<ob::FalsePositiveFilter>& self) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ return self->getfpebfROIMinXRatioRange(); });
           })
      .def("get_fpebf_roi_max_x_ratio_range",
           [](std::shared_ptr<ob::FalsePositiveFilter>& self) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ return self->getfpebfROIMaxXRatioRange(); });
           })
      .def("get_fpebf_roi_min_y_ratio_range",
           [](std::shared_ptr<ob::FalsePositiveFilter>& self) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ return self->getfpebfROIMinYRatioRange(); });
           })
      .def("get_fpebf_roi_max_y_ratio_range",
           [](std::shared_ptr<ob::FalsePositiveFilter>& self) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ return self->getfpebfROIMaxYRatioRange(); });
           })
      .def("get_fpebf_min_bleed_length_range",
           [](std::shared_ptr<ob::FalsePositiveFilter>& self) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ return self->getfpebfMinBleedLengthRange(); });
           })
      // fpTextureSparsity group
      .def("get_fp_texture_sparsity_filter_enable_range",
           [](std::shared_ptr<ob::FalsePositiveFilter>& self) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ return self->getfpTextureSparsityFilterEnableRange(); });
           })
      // fptsfROI group
      .def("get_fptsf_roi_min_x_ratio_range",
           [](std::shared_ptr<ob::FalsePositiveFilter>& self) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ return self->getfptsfROIMinXRatioRange(); });
           })
      .def("get_fptsf_roi_max_x_ratio_range",
           [](std::shared_ptr<ob::FalsePositiveFilter>& self) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ return self->getfptsfROIMaxXRatioRange(); });
           })
      .def("get_fptsf_roi_min_y_ratio_range",
           [](std::shared_ptr<ob::FalsePositiveFilter>& self) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ return self->getfptsfROIMinYRatioRange(); });
           })
      .def("get_fptsf_roi_max_y_ratio_range",
           [](std::shared_ptr<ob::FalsePositiveFilter>& self) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ return self->getfptsfROIMaxYRatioRange(); });
           })
      .def("get_fptsf_max_noise_level_range",
           [](std::shared_ptr<ob::FalsePositiveFilter>& self) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ return self->getfptsfMaxNoiseLevelRange(); });
           })
      .def("get_fptsf_max_speckle_size_range",
           [](std::shared_ptr<ob::FalsePositiveFilter>& self) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ return self->getfptsfMaxSpeckleSizeRange(); });
           })
      // fpPatternAmbiguity group
      .def("get_fp_pattern_ambiguity_filter_enable_range",
           [](std::shared_ptr<ob::FalsePositiveFilter>& self) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({
              return self->getfpPatternAmbiguityFilterEnableRange();
            });
           })
      // fppafROI group
      .def("get_fppaf_roi_min_x_ratio_range",
           [](std::shared_ptr<ob::FalsePositiveFilter>& self) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ return self->getfppafROIMinXRatioRange(); });
           })
      .def("get_fppaf_roi_max_x_ratio_range",
           [](std::shared_ptr<ob::FalsePositiveFilter>& self) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ return self->getfppafROIMaxXRatioRange(); });
           })
      .def("get_fppaf_roi_min_y_ratio_range",
           [](std::shared_ptr<ob::FalsePositiveFilter>& self) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ return self->getfppafROIMinYRatioRange(); });
           })
      .def("get_fppaf_roi_max_y_ratio_range",
           [](std::shared_ptr<ob::FalsePositiveFilter>& self) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ return self->getfppafROIMaxYRatioRange(); });
           })
      .def("get_fppaf_max_noise_level_range",
           [](std::shared_ptr<ob::FalsePositiveFilter>& self) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ return self->getfppafMaxNoiseLevelRange(); });
           })
      .def("get_fppaf_max_speckle_size_range",
           [](std::shared_ptr<ob::FalsePositiveFilter>& self) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ return self->getfppafMaxSpeckleSizeRange(); });
           })
      .def("get_fppaf_max_width_ratio_range",
           [](std::shared_ptr<ob::FalsePositiveFilter>& self) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ return self->getfppafMaxWidthRatioRange(); });
           })
      .def("get_fppaf_max_height_ratio_range",
           [](std::shared_ptr<ob::FalsePositiveFilter>& self) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ return self->getfppafMaxHeightRatioRange(); });
           })
      .def("get_fppaf_tolerance_range",
           [](std::shared_ptr<ob::FalsePositiveFilter>& self) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ return self->getfppafToleranceRange(); });
           })
      .def("get_fppaf_score_range",
           [](std::shared_ptr<ob::FalsePositiveFilter>& self) {
             CHECK_NULLPTR(self);
             OB_TRY_CATCH({ return self->getfppafScoreRange(); });
           });
}

}  // namespace pyorbbecsdk
