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
#include "frame.hpp"

#include <pybind11/numpy.h>

#include "error.hpp"

namespace pyorbbecsdk {
void define_frame(const py::object& m) {
  py::class_<ob::Frame, std::shared_ptr<ob::Frame>>(m, "Frame")
      .def("get_type",
           [](const std::shared_ptr<ob::Frame>& self) { return self->type(); })
      .def(
          "get_format",
          [](const std::shared_ptr<ob::Frame>& self) { return self->format(); })
      .def("get_index",
           [](const std::shared_ptr<ob::Frame>& self) { return self->index(); })
      .def("get_data",
           [](const std::shared_ptr<ob::Frame>& self) -> py::array_t<uint8_t> {
             auto data_size = self->dataSize();
             auto data = self->data();
             py::array_t<uint8_t> result(data_size);
             std::memcpy(result.mutable_data(), data, data_size);
             return result;
           })
      .def(
          "get_data_pointer",
          [](const std::shared_ptr<ob::Frame>& self) {
            auto ptr = self->data();
            return py::capsule(ptr, "frame_data_pointer");
          },
          py::return_value_policy::reference)
      .def("get_data_size",
           [](const std::shared_ptr<ob::Frame>& self) {
             return self->dataSize();
           })
      .def(
          "get_timestamp",
          [](const std::shared_ptr<ob::Frame>& self) {
            return self->timeStamp();
          },
          "Get the hardware timestamp of the frame in milliseconds")
      .def("get_timestamp_us",
           [](const std::shared_ptr<ob::Frame>& self) {
             return self->timeStampUs();
           })
      .def("get_system_timestamp",
           [](const std::shared_ptr<ob::Frame>& self) {
             return self->systemTimeStamp();
           })
      .def("get_system_timestamp_us",
           [](const std::shared_ptr<ob::Frame>& self) {
             return self->systemTimeStampUs();
           })
      .def("get_global_timestamp_us",
           [](const std::shared_ptr<ob::Frame>& self) {
             return self->globalTimeStampUs();
           })
      .def("has_metadata",
           [](const std::shared_ptr<ob::Frame>& self,
              OBFrameMetadataType type) { return self->hasMetadata(type); })
      .def(
          "get_metadata_value",
          [](const std::shared_ptr<ob::Frame>& self, OBFrameMetadataType type) {
            return self->getMetadataValue(type);
          })
      .def("as_video_frame",
           [](const std::shared_ptr<ob::Frame>& self) {
             if (!self->is<ob::VideoFrame>()) {
               throw std::runtime_error("Frame is not a VideoFrame");
             }
             OB_TRY_CATCH({ return std::make_shared<ob::VideoFrame>(*self); });
           })
      .def("as_color_frame",
           [](const std::shared_ptr<ob::Frame>& self) {
             if (!self->is<ob::ColorFrame>()) {
               throw std::runtime_error("Frame is not a ColorFrame");
             }
             OB_TRY_CATCH({ return std::make_shared<ob::ColorFrame>(*self); });
           })
      .def("as_depth_frame",
           [](const std::shared_ptr<ob::Frame>& self) {
             if (!self->is<ob::DepthFrame>()) {
               throw std::runtime_error("Frame is not a DepthFrame");
             }
             OB_TRY_CATCH({ return std::make_shared<ob::DepthFrame>(*self); });
           })
      .def("as_ir_frame",
           [](const std::shared_ptr<ob::Frame>& self) {
             if (!self->is<ob::IRFrame>()) {
               throw std::runtime_error("Frame is not an IRFrame");
             }
             OB_TRY_CATCH({ return std::make_shared<ob::IRFrame>(*self); });
           })
      .def("as_frame_set",
           [](const std::shared_ptr<ob::Frame>& self) {
             if (!self->is<ob::FrameSet>()) {
               throw std::runtime_error("Frame is not a FrameSet");
             }
             OB_TRY_CATCH({ return std::make_shared<ob::FrameSet>(*self); });
           })
      .def("as_accel_frame",
           [](const std::shared_ptr<ob::Frame>& self) {
             if (!self->is<ob::AccelFrame>()) {
               throw std::runtime_error("Frame is not an AccelFrame");
             }
             OB_TRY_CATCH({ return std::make_shared<ob::AccelFrame>(*self); });
           })
      .def("as_gyro_frame",
           [](const std::shared_ptr<ob::Frame>& self) {
             if (!self->is<ob::GyroFrame>()) {
               throw std::runtime_error("Frame is not an GyroFrame");
             }
             OB_TRY_CATCH({ return std::make_shared<ob::GyroFrame>(*self); });
           })
      .def("as_points_frame",
           [](const std::shared_ptr<ob::Frame>& self) {
             if (!self->is<ob::PointsFrame>()) {
               throw std::runtime_error("Frame is not a PointsFrame");
             }
             OB_TRY_CATCH({ return std::make_shared<ob::PointsFrame>(*self); });
           })
      .def("__repr__", [](const std::shared_ptr<ob::Frame>& self) {
        std::ostringstream oss;
        oss << "<Frame type=" << self->type() << " format=" << self->format()
            << " index=" << self->index() << " data_size=" << self->dataSize()
            << " timestamp=" << self->timeStamp()
            << " timestamp_us=" << self->timeStampUs()
            << " system_timestamp=" << self->systemTimeStamp() << ">";
      });
}

void define_video_frame(const py::object& m) {
  py::class_<ob::VideoFrame, ob::Frame, std::shared_ptr<ob::VideoFrame>>(
      m, "VideoFrame")
      .def(py::init<ob::Frame&>())
      .def("get_width",
           [](const std::shared_ptr<ob::VideoFrame>& self) {
             return self->width();
           })
      .def("get_height",
           [](const std::shared_ptr<ob::VideoFrame>& self) {
             return self->height();
           })
      .def("get_metadata",
           [](const std::shared_ptr<ob::VideoFrame>& self)
               -> py::array_t<uint8_t> {
             auto meta_data_size = self->metadataSize();
             auto meta_data = self->metadata();
             py::array_t<uint8_t> result(meta_data_size);
             std::memcpy(result.mutable_data(), meta_data, meta_data_size);
             return result;
           })
      .def("get_metadata_size",
           [](const std::shared_ptr<ob::VideoFrame>& self) {
             return self->metadataSize();
           })
      .def("get_pixel_available_bit_size",
           [](const std::shared_ptr<ob::VideoFrame>& self) {
             return self->pixelAvailableBitSize();
           })
      .def("as_color_frame",
           [](const std::shared_ptr<ob::VideoFrame>& self) {
             OB_TRY_CATCH({ return self->as<ob::ColorFrame>(); });
           })
      .def("as_depth_frame",
           [](const std::shared_ptr<ob::VideoFrame>& self) {
             OB_TRY_CATCH({ return self->as<ob::DepthFrame>(); });
           })
      .def("as_ir_frame",
           [](const std::shared_ptr<ob::VideoFrame>& self) {
             OB_TRY_CATCH({ return self->as<ob::IRFrame>(); });
           })
      .def("as_points_frame",
           [](const std::shared_ptr<ob::VideoFrame>& self) {
             OB_TRY_CATCH({ return self->as<ob::PointsFrame>(); });
           })
      .def("__repr__", [](const std::shared_ptr<ob::VideoFrame>& self) {
        std::ostringstream oss;
        oss << "<VideoFrame type=" << self->type()
            << " format=" << self->format() << " index=" << self->index()
            << " data_size=" << self->dataSize()
            << " timestamp=" << self->timeStamp()
            << " timestamp_us=" << self->timeStampUs()
            << " system_timestamp=" << self->systemTimeStamp()
            << " width=" << self->width() << " height=" << self->height()
            << ">";
      });
}

void define_color_frame(const py::object& m) {
  py::class_<ob::ColorFrame, ob::VideoFrame, std::shared_ptr<ob::ColorFrame>>(
      m, "ColorFrame")
      .def(py::init<ob::Frame&>());
}

void define_depth_frame(const py::object& m) {
  py::class_<ob::DepthFrame, ob::VideoFrame, std::shared_ptr<ob::DepthFrame>>(
      m, "DepthFrame")
      .def(py::init<ob::Frame&>())
      .def("get_depth_scale", [](const std::shared_ptr<ob::DepthFrame>& self) {
        return self->getValueScale();
      });
}

void define_ir_frame(const py::object& m) {
  py::class_<ob::IRFrame, ob::VideoFrame, std::shared_ptr<ob::IRFrame>>(
      m, "IRFrame")
      .def(py::init<ob::Frame&>())
      .def("get_data_source", [](const std::shared_ptr<ob::IRFrame>& self) {
        return self->getDataSource();
      });
}

void define_points_frame(const py::object& m) {
  py::class_<ob::PointsFrame, ob::Frame, std::shared_ptr<ob::PointsFrame>>(
      m, "PointsFrame")
      .def("get_position_value_scale",
           [](const std::shared_ptr<ob::PointsFrame>& self) {
             return self->getPositionValueScale();
           });
}

void define_frame_set(const py::object& m) {
  py::class_<ob::FrameSet, ob::Frame, std::shared_ptr<ob::FrameSet>>(m,
                                                                     "FrameSet")
      .def("get_frame_count",
           [](const std::shared_ptr<ob::FrameSet>& self) {
             return self->frameCount();
           })
      .def("get_depth_frame",
           [](const std::shared_ptr<ob::FrameSet>& self) {
             return self->depthFrame();
           })
      .def("get_color_frame",
           [](const std::shared_ptr<ob::FrameSet>& self) {
             return self->colorFrame();
           })
      .def("get_ir_frame",
           [](const std::shared_ptr<ob::FrameSet>& self) {
             return self->irFrame();
           })
      .def("get_points_frame",
           [](const std::shared_ptr<ob::FrameSet>& self) {
             return self->pointsFrame();
           })
      .def("get_frame_by_type",
           [](const std::shared_ptr<ob::FrameSet>& self, OBFrameType type) {
             return self->getFrame(type);
           })
      .def("get_frame", [](const std::shared_ptr<ob::FrameSet>& self,
                           OBFrameType type) { return self->getFrame(type); })
      .def("get_frame_by_index",
           [](const std::shared_ptr<ob::FrameSet>& self, int index) {
             return self->getFrame(index);
           })
      .def("convert_to_points",
           [](const std::shared_ptr<ob::FrameSet>& self,
              const OBCameraParam& param) -> py::list {
             try {
               ob::PointCloudFilter filter;
               filter.setCameraParam(param);
               filter.setCreatePointFormat(OB_FORMAT_POINT);

               auto depth_frame = self->depthFrame();
               if (!depth_frame) {
                 std::cerr << "depth frame not exists" << std::endl;
                 return py::list();
               }
               auto frame = filter.process(self);
               if (!frame) {
                 std::cerr << "point cloud filter process failed" << std::endl;
                 return py::list();
               }
               auto points_size =
                   static_cast<size_t>(frame->dataSize() / sizeof(OBPoint));
               auto scale = depth_frame->getValueScale();
               auto points = reinterpret_cast<OBPoint*>(frame->data());
               if (!points) {
                 std::cerr << "cast points failed" << std::endl;
                 return py::list();
               }
               py::list result;
               for (size_t i = 0; i < points_size; ++i) {
                 auto point = points[i];
                 point.x *= scale;
                 point.y *= scale;
                 point.z *= scale;
                 result.append(py::cast(point));
               }
               return result;
             } catch (const ob::Error& e) {
               throw OBError(e);
             }
           })
      .def("convert_to_color_points",
           [](const std::shared_ptr<ob::FrameSet>& self,
              const OBCameraParam& param) -> py::list {
             try {
               ob::PointCloudFilter filter;
               filter.setCameraParam(param);
               filter.setCreatePointFormat(OB_FORMAT_RGB_POINT);

               auto depth_frame = self->depthFrame();
               auto color_frame = self->colorFrame();
               if (!depth_frame || !color_frame) {
                 std::cerr << "depth or color frame not exists" << std::endl;
                 return py::list();
               }
               auto frame = filter.process(self);
               if (!frame) {
                 return py::list();
               }
               auto points_size = static_cast<size_t>(frame->dataSize() /
                                                      sizeof(OBColorPoint));
               auto scale = depth_frame->getValueScale();
               auto points = reinterpret_cast<OBColorPoint*>(frame->data());
               if (!points) {
                 std::cerr << "cast points failed" << std::endl;
                 return py::list();
               }
               py::list result;
               for (size_t i = 0; i < points_size; ++i) {
                 auto point = points[i];
                 point.x *= scale;
                 point.y *= scale;
                 point.z *= scale;
                 result.append(py::cast(point));
               }
               return result;
             } catch (const ob::Error& e) {
               throw OBError(e);
             }
           })
      .def("get_point_cloud",
           [](const std::shared_ptr<ob::FrameSet>& self,
              const OBCameraParam& param) -> py::array_t<float> {
             try {
               ob::PointCloudFilter filter;
               filter.setCameraParam(param);
               filter.setCreatePointFormat(OB_FORMAT_POINT);

               auto depth_frame = self->depthFrame();
               if (!depth_frame) {
                 std::cerr << "depth frame not exists" << std::endl;
                 return {};
               }
               auto frame = filter.process(self);
               if (!frame) {
                 std::cerr << "point cloud filter process failed" << std::endl;
                 return {};
               }
               long points_size =
                   static_cast<long>(frame->dataSize() / sizeof(OBPoint));
               auto scale = depth_frame->getValueScale();
               auto points = reinterpret_cast<OBPoint*>(frame->data());
               if (!points) {
                 std::cerr << "cast points failed" << std::endl;
                 return {};
               }

               py::array::ShapeContainer shape({points_size, 3});
               py::array::StridesContainer strides(
                   {3 * sizeof(float), sizeof(float)});
               py::dtype dtype("float");

               py::array array(dtype, shape, strides);
               py::array_t<float> result = py::cast<py::array_t<float>>(array);
               py::buffer_info buf_info = result.request();
               auto* ptr = static_cast<float*>(buf_info.ptr);
               for (long i = 0; i < points_size; ++i) {
                 auto point = points[i];
                 point.x *= scale;
                 point.y *= scale;
                 point.z *= scale;
                 size_t index = i * 3;
                 ptr[index] = point.x;
                 ptr[index + 1] = point.y;
                 ptr[index + 2] = point.z;
               }
               return result;
             } catch (const ob::Error& e) {
               throw OBError(e);
             }
           })
      .def("get_color_point_cloud",
           [](const std::shared_ptr<ob::FrameSet>& self,
              const OBCameraParam& param) -> py::array_t<float> {
             try {
               ob::PointCloudFilter filter;
               filter.setCameraParam(param);
               filter.setCreatePointFormat(OB_FORMAT_RGB_POINT);

               auto depth_frame = self->depthFrame();
               auto color_frame = self->colorFrame();
               if (!depth_frame || !color_frame) {
                 std::cerr << "depth or color frame not exists" << std::endl;
                 return {};
               }
               auto frame = filter.process(self);
               if (!frame) {
                 return {};
               }
               long points_size =
                   static_cast<long>(frame->dataSize() / sizeof(OBColorPoint));
               auto scale = depth_frame->getValueScale();
               auto points = reinterpret_cast<OBColorPoint*>(frame->data());
               if (!points) {
                 std::cerr << "cast points failed" << std::endl;
                 return {};
               }
               py::array::ShapeContainer shape({points_size, 6});
               py::array::StridesContainer strides(
                   {6 * sizeof(float), sizeof(float)});
               py::dtype dtype("float");
               py::array array(dtype, shape, strides);
               py::array_t<float> result = py::cast<py::array_t<float>>(array);
               py::buffer_info buf_info = result.request();
               auto* ptr = static_cast<float*>(buf_info.ptr);
               for (long i = 0; i < points_size; ++i) {
                 auto point = points[i];
                 point.x *= scale;
                 point.y *= scale;
                 point.z *= scale;
                 size_t index = i * 6;
                 ptr[index] = point.x;
                 ptr[index + 1] = point.y;
                 ptr[index + 2] = point.z;
                 ptr[index + 3] = point.r;
                 ptr[index + 4] = point.g;
                 ptr[index + 5] = point.b;
               }
               return result;
             } catch (const ob::Error& e) {
               throw OBError(e);
             }
           })
      .def("__repr__", [](const std::shared_ptr<ob::FrameSet>& self) {
        std::ostringstream oss;
        oss << "<FrameSet type=" << self->type() << " format=" << self->format()
            << " index=" << self->index() << " data_size=" << self->dataSize()
            << " timestamp=" << self->timeStamp()
            << " timestamp_us=" << self->timeStampUs()
            << " system_timestamp=" << self->systemTimeStamp()
            << " frame_count=" << self->frameCount() << ">";
      });
}

void define_accel_frame(const py::object& m) {
  py::class_<ob::AccelFrame, ob::Frame, std::shared_ptr<ob::AccelFrame>>(
      m, "AccelFrame")
      .def(py::init<ob::Frame&>())
      .def("get_x",
           [](const std::shared_ptr<ob::AccelFrame>& self) {
             return self->value().x;
           })
      .def("get_y",
           [](const std::shared_ptr<ob::AccelFrame>& self) {
             return self->value().y;
           })
      .def("get_z",
           [](const std::shared_ptr<ob::AccelFrame>& self) {
             return self->value().z;
           })
      .def("get_temperature",
           [](const std::shared_ptr<ob::AccelFrame>& self) {
             return self->temperature();
           })
      .def("get_value",
           [](const std::shared_ptr<ob::AccelFrame>& self) {
             return self->value();
           })
      .def("__repr__", [](const std::shared_ptr<ob::AccelFrame>& self) {
        std::ostringstream oss;
        oss << "<AccelFrame x=" << self->value().x << " y=" << self->value().y
            << " z=" << self->value().z
            << " temperature=" << self->temperature() << ">";
      });
}

void define_gyro_frame(const py::object& m) {
  py::class_<ob::GyroFrame, ob::Frame, std::shared_ptr<ob::GyroFrame>>(
      m, "GyroFrame")
      .def(py::init<ob::Frame&>())
      .def("get_x",
           [](const std::shared_ptr<ob::GyroFrame>& self) {
             return self->value().x;
           })
      .def("get_y",
           [](const std::shared_ptr<ob::GyroFrame>& self) {
             return self->value().y;
           })
      .def("get_z",
           [](const std::shared_ptr<ob::GyroFrame>& self) {
             return self->value().z;
           })
      .def("get_temperature",
           [](const std::shared_ptr<ob::GyroFrame>& self) {
             return self->temperature();
           })
      .def("get_value",
           [](const std::shared_ptr<ob::GyroFrame>& self) {
             return self->value();
           })
      .def("__repr__", [](const std::shared_ptr<ob::GyroFrame>& self) {
        std::ostringstream oss;
        oss << "<GyroFrame x=" << self->value().x << " y=" << self->value().y
            << " z=" << self->value().z
            << " temperature=" << self->temperature() << ">";
      });
}

}  // namespace pyorbbecsdk
