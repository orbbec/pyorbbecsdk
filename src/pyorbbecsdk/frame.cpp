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
#include "frame.hpp"

#include <pybind11/numpy.h>

#include "error.hpp"

namespace pyorbbecsdk {
void define_frame(const py::object& m) {
  py::class_<ob::Frame, std::shared_ptr<ob::Frame>>(m, "Frame")
      .def("get_type",
           [](const std::shared_ptr<ob::Frame>& self) {
             OB_TRY_CATCH({ return self->type(); });
           })
      .def("get_format",
           [](const std::shared_ptr<ob::Frame>& self) {
             OB_TRY_CATCH({ return self->format(); });
           })
      .def("get_index",
           [](const std::shared_ptr<ob::Frame>& self) {
             OB_TRY_CATCH({ return self->index(); });
           })
      .def("get_data",
           [](const std::shared_ptr<ob::Frame>& self) -> py::array_t<uint8_t> {
             OB_TRY_CATCH({
               auto data_size = self->dataSize();
               auto data = self->data();
               py::array_t<uint8_t> result(data_size);
               std::memcpy(result.mutable_data(), data, data_size);
               return result;
             });
           })
      .def(
          "get_data_pointer",
          [](const std::shared_ptr<ob::Frame>& self) {
            OB_TRY_CATCH({
              auto ptr = self->data();
              return py::capsule(ptr, "frame_data_pointer");
            });
          },
          py::return_value_policy::reference)
      .def("get_data_size",
           [](const std::shared_ptr<ob::Frame>& self) {
             OB_TRY_CATCH({ return self->dataSize(); });
           })
      .def(
          "get_timestamp",
          [](const std::shared_ptr<ob::Frame>& self) {
            OB_TRY_CATCH({ return self->timeStamp(); });
          },
          "Get the hardware timestamp of the frame in milliseconds")
      .def("get_timestamp_us",
           [](const std::shared_ptr<ob::Frame>& self) {
             OB_TRY_CATCH({ return self->timeStampUs(); });
           })
      .def("get_system_timestamp",
           [](const std::shared_ptr<ob::Frame>& self) {
             OB_TRY_CATCH({ return self->systemTimeStamp(); });
           })
      .def("get_system_timestamp_us",
           [](const std::shared_ptr<ob::Frame>& self) {
             OB_TRY_CATCH({ return self->systemTimeStampUs(); });
           })
      .def("get_global_timestamp_us",
           [](const std::shared_ptr<ob::Frame>& self) {
             OB_TRY_CATCH({ return self->globalTimeStampUs(); });
           })
      .def(
          "has_metadata",
          [](const std::shared_ptr<ob::Frame>& self, OBFrameMetadataType type) {
            OB_TRY_CATCH({ return self->hasMetadata(type); });
          })
      .def(
          "get_metadata_value",
          [](const std::shared_ptr<ob::Frame>& self, OBFrameMetadataType type) {
            OB_TRY_CATCH({ return self->getMetadataValue(type); });
          })
      .def("as_video_frame",
           [](const std::shared_ptr<ob::Frame>& self) {
             if (!self->is<ob::VideoFrame>()) {
               throw std::runtime_error("Frame is not a VideoFrame");
             }
             OB_TRY_CATCH({ return self->as<ob::VideoFrame>(); });
           })
      .def("as_color_frame",
           [](const std::shared_ptr<ob::Frame>& self) {
             if (!self->is<ob::ColorFrame>()) {
               throw std::runtime_error("Frame is not a ColorFrame");
             }
             OB_TRY_CATCH({ return self->as<ob::ColorFrame>(); });
           })
      .def("as_depth_frame",
           [](const std::shared_ptr<ob::Frame>& self) {
             if (!self->is<ob::DepthFrame>()) {
               throw std::runtime_error("Frame is not a DepthFrame");
             }
             OB_TRY_CATCH({ return self->as<ob::DepthFrame>(); });
           })
      .def("as_ir_frame",
           [](const std::shared_ptr<ob::Frame>& self) {
             if (!self->is<ob::IRFrame>()) {
               throw std::runtime_error("Frame is not an IRFrame");
             }
             OB_TRY_CATCH({ return self->as<ob::IRFrame>(); });
           })
      .def("as_frame_set",
           [](const std::shared_ptr<ob::Frame>& self) {
             if (!self->is<ob::FrameSet>()) {
               throw std::runtime_error("Frame is not a FrameSet");
             }
             OB_TRY_CATCH({ return self->as<ob::FrameSet>(); });
           })
      .def("as_accel_frame",
           [](const std::shared_ptr<ob::Frame>& self) {
             if (!self->is<ob::AccelFrame>()) {
               throw std::runtime_error("Frame is not an AccelFrame");
             }
             OB_TRY_CATCH({ return self->as<ob::AccelFrame>(); });
           })
      .def("as_gyro_frame",
           [](const std::shared_ptr<ob::Frame>& self) {
             if (!self->is<ob::GyroFrame>()) {
               throw std::runtime_error("Frame is not an GyroFrame");
             }
             OB_TRY_CATCH({ return self->as<ob::GyroFrame>(); });
           })
      .def("as_confidence_frame",
           [](const std::shared_ptr<ob::Frame>& self) {
             if (!self->is<ob::ConfidenceFrame>()) {
               throw std::runtime_error("Frame is not a ConfidenceFrame");
             }
             OB_TRY_CATCH({ return self->as<ob::ConfidenceFrame>(); });
           })
      .def("as_points_frame",
           [](const std::shared_ptr<ob::Frame>& self) {
             if (!self->is<ob::PointsFrame>()) {
               throw std::runtime_error("Frame is not a PointsFrame");
             }
             OB_TRY_CATCH({ return self->as<ob::PointsFrame>(); });
           })
      .def("as_lidar_points_frame",
           [](const std::shared_ptr<ob::Frame>& self) {
             if (!self->is<ob::LiDARPointsFrame>()) {
               throw std::runtime_error("Frame is not a LiDARPointsFrame");
             }
             OB_TRY_CATCH({ return self->as<ob::LiDARPointsFrame>(); });
           })
      .def("get_stream_profile",
           [](const std::shared_ptr<ob::Frame>& self) {
             OB_TRY_CATCH({ return self->getStreamProfile(); });
           })
      .def("get_sensor",
           [](const std::shared_ptr<ob::Frame>& self) {
             OB_TRY_CATCH({ return self->getSensor(); });
           })
      .def("get_device",
           [](const std::shared_ptr<ob::Frame>& self) {
             OB_TRY_CATCH({ return self->getDevice(); });
           })
      .def("copy_frame_info",
           [](const std::shared_ptr<ob::Frame>& self,
              std::shared_ptr<const ob::Frame> srcFrame) {
             OB_TRY_CATCH({ self->copyFrameInfo(srcFrame); });
           })
      .def("set_system_timestamp_us",
           [](const std::shared_ptr<ob::Frame>& self,
              uint64_t system_timestamp_us) {
             OB_TRY_CATCH({ self->setSystemTimestampUs(system_timestamp_us); });
           })
      .def("update_data",
           [](const std::shared_ptr<ob::Frame>& self, py::buffer buffer) {
             auto data = buffer.request();
             if (data.ndim != 1) {
               throw std::runtime_error("update_data expects 1D buffer");
             }
             if (data.size > std::numeric_limits<uint32_t>::max()) {
               throw std::runtime_error("update_data: buffer too large");
             }
             uint32_t data_size = static_cast<uint32_t>(data.size);
             if (data_size != self->getDataSize()) {
               throw std::runtime_error("update_data: buffer size mismatch");
             }
             OB_TRY_CATCH({
               self->updateData(static_cast<const uint8_t*>(data.ptr), data_size);
             });
           })
      .def("update_metadata",
           [](const std::shared_ptr<ob::Frame>& self, py::buffer buffer) {
             auto metadata = buffer.request();

             if (metadata.ndim != 1) {
               throw std::runtime_error("update_metadata expects 1D buffer");
             }
             if (metadata.size > std::numeric_limits<uint32_t>::max()) {
               throw std::runtime_error("update_metadata: buffer too large");
             }
             uint32_t metadata_size = static_cast<uint32_t>(metadata.size);
             OB_TRY_CATCH({
               self->updateMetadata(static_cast<const uint8_t*>(metadata.ptr),
                                    metadata_size);
             });
           })
      .def("set_stream_profile",
           [](const std::shared_ptr<ob::Frame>& self,
              std::shared_ptr<const ob::StreamProfile> profile) {
             OB_TRY_CATCH({ self->setStreamProfile(profile); });
           })
      .def("__repr__", [](const std::shared_ptr<ob::Frame>& self) {
        OB_TRY_CATCH({
          std::ostringstream oss;
          oss << "<Frame type=" << self->type() << " format=" << self->format()
              << " index=" << self->index() << " data_size=" << self->dataSize()
              << " timestamp=" << self->timeStamp()
              << " timestamp_us=" << self->timeStampUs()
              << " system_timestamp=" << self->systemTimeStamp() << ">";
          return oss.str();
        });
      });
}

void define_video_frame(const py::object& m) {
  py::class_<ob::VideoFrame, ob::Frame, std::shared_ptr<ob::VideoFrame>>(
      m, "VideoFrame")
      .def("get_width",
           [](const std::shared_ptr<ob::VideoFrame>& self) {
             OB_TRY_CATCH({ return self->width(); });
           })
      .def("get_height",
           [](const std::shared_ptr<ob::VideoFrame>& self) {
             OB_TRY_CATCH({ return self->height(); });
           })
      .def("get_pixel_type",
           [](const std::shared_ptr<ob::VideoFrame>& self) {
             OB_TRY_CATCH({ return self->getPixelType(); });
           })
      .def("get_pixel_available_bit_size",
           [](const std::shared_ptr<ob::VideoFrame>& self) {
             OB_TRY_CATCH({ return self->getPixelAvailableBitSize(); });
           })
      .def("set_pixel_type",
           [](const std::shared_ptr<ob::VideoFrame>& self,
              OBPixelType pixel_type) {
             OB_TRY_CATCH({ self->setPixelType(pixel_type); });
           })
      .def("set_pixel_available_bit_size",
           [](const std::shared_ptr<ob::VideoFrame>& self, uint8_t bit_size) {
             OB_TRY_CATCH({ self->setPixelAvailableBitSize(bit_size); });
           })
      .def("get_metadata",
           [](const std::shared_ptr<ob::VideoFrame>& self)
               -> py::array_t<uint8_t> {
             OB_TRY_CATCH({
               auto meta_data_size = self->metadataSize();
               auto meta_data = self->metadata();
               py::array_t<uint8_t> result(meta_data_size);
               std::memcpy(result.mutable_data(), meta_data, meta_data_size);
               return result;
             });
           })
      .def("get_metadata_size",
           [](const std::shared_ptr<ob::VideoFrame>& self) {
             OB_TRY_CATCH({ return self->metadataSize(); });
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
      .def("as_confidence_frame",
           [](const std::shared_ptr<ob::VideoFrame>& self) {
             OB_TRY_CATCH({ return self->as<ob::ConfidenceFrame>(); });
           })
      .def("as_points_frame",
           [](const std::shared_ptr<ob::VideoFrame>& self) {
             OB_TRY_CATCH({ return self->as<ob::PointsFrame>(); });
           })
      .def("__repr__", [](const std::shared_ptr<ob::VideoFrame>& self) {
        OB_TRY_CATCH({
          std::ostringstream oss;
          oss << "<VideoFrame type=" << self->type()
              << " format=" << self->format() << " index=" << self->index()
              << " data_size=" << self->dataSize()
              << " timestamp=" << self->timeStamp()
              << " timestamp_us=" << self->timeStampUs()
              << " system_timestamp=" << self->systemTimeStamp()
              << " width=" << self->width() << " height=" << self->height()
              << ">";
          return oss.str();
        });
      });
}

void define_color_frame(const py::object& m) {
  py::class_<ob::ColorFrame, ob::VideoFrame, std::shared_ptr<ob::ColorFrame>>(
      m, "ColorFrame");
}

void define_depth_frame(const py::object& m) {
  py::class_<ob::DepthFrame, ob::VideoFrame, std::shared_ptr<ob::DepthFrame>>(
      m, "DepthFrame")
      .def("get_depth_scale",
           [](const std::shared_ptr<ob::DepthFrame>& self) {
             OB_TRY_CATCH({ return self->getValueScale(); });
           })
      .def("set_value_scale",
           [](const std::shared_ptr<ob::DepthFrame>& self, float value_scale) {
             OB_TRY_CATCH({ self->setValueScale(value_scale); });
           });
}

void define_ir_frame(const py::object& m) {
  py::class_<ob::IRFrame, ob::VideoFrame, std::shared_ptr<ob::IRFrame>>(
      m, "IRFrame");
}

void define_confidence_frame(const py::object& m) {
  py::class_<ob::ConfidenceFrame, ob::VideoFrame,
             std::shared_ptr<ob::ConfidenceFrame>>(m, "ConfidenceFrame");
}

void define_points_frame(const py::object& m) {
  py::class_<ob::PointsFrame, ob::Frame, std::shared_ptr<ob::PointsFrame>>(
      m, "PointsFrame")
      .def("get_position_value_scale",
           [](const std::shared_ptr<ob::PointsFrame>& self) {
             OB_TRY_CATCH({ return self->getPositionValueScale(); });
           })
      .def("get_width",
           [](const std::shared_ptr<ob::PointsFrame>& self) {
             OB_TRY_CATCH({ return self->getWidth(); });
           })
      .def("get_height", [](const std::shared_ptr<ob::PointsFrame>& self) {
        OB_TRY_CATCH({ return self->getHeight(); });
      });
}

void define_frame_set(const py::object& m) {
  py::class_<ob::FrameSet, ob::Frame, std::shared_ptr<ob::FrameSet>>(m,
                                                                     "FrameSet")
      .def("get_frame_count",
           [](const std::shared_ptr<ob::FrameSet>& self) {
             OB_TRY_CATCH({ return self->frameCount(); });
           })
      .def("get_depth_frame",
           [](const std::shared_ptr<ob::FrameSet>& self) {
             OB_TRY_CATCH({ return self->getDepthFrame(); });
           })
      .def("get_color_frame",
           [](const std::shared_ptr<ob::FrameSet>& self) {
             OB_TRY_CATCH({ return self->getColorFrame(); });
           })
      .def("get_ir_frame",
           [](const std::shared_ptr<ob::FrameSet>& self) {
             OB_TRY_CATCH({ return self->getIrFrame(); });
           })
      .def("get_points_frame",
           [](const std::shared_ptr<ob::FrameSet>& self) {
             OB_TRY_CATCH({ return self->getPointsFrame(); });
           })
      .def("get_frame_by_type",
           [](const std::shared_ptr<ob::FrameSet>& self, OBFrameType type) {
             OB_TRY_CATCH({ return self->getFrame(type); });
           })
      .def("get_frame", [](const std::shared_ptr<ob::FrameSet>& self,
                           OBFrameType type) {
        OB_TRY_CATCH({ return self->getFrame(type); });
      })
      .def("get_frame_by_index",
           [](const std::shared_ptr<ob::FrameSet>& self, int index) {
             OB_TRY_CATCH({ return self->getFrame(index); });
           })
      .def("push_frame",
           [](const std::shared_ptr<ob::FrameSet>& self,
              const std::shared_ptr<ob::Frame>& frame) {
             OB_TRY_CATCH({ self->pushFrame(frame); });
           })
      .def("__getitem__", [](const std::shared_ptr<ob::FrameSet>& self,
                             int index) {
        OB_TRY_CATCH({ return self->getFrame(index); });
      })
      .def("get_count",
           [](const std::shared_ptr<ob::FrameSet>& self) {
             OB_TRY_CATCH({ return self->frameCount(); });
           })
      .def("__len__",
           [](const std::shared_ptr<ob::FrameSet>& self) {
             OB_TRY_CATCH({ return self->frameCount(); });
           })
      .def("__repr__", [](const std::shared_ptr<ob::FrameSet>& self) {
        OB_TRY_CATCH({
          std::ostringstream oss;
          oss << "<FrameSet type=" << self->type() << " format=" << self->format()
              << " index=" << self->index() << " data_size=" << self->dataSize()
              << " timestamp=" << self->timeStamp()
              << " timestamp_us=" << self->timeStampUs()
              << " system_timestamp=" << self->systemTimeStamp()
              << " frame_count=" << self->frameCount() << ">";
          return oss.str();
        });
      });
}

void define_accel_frame(const py::object& m) {
  py::class_<ob::AccelFrame, ob::Frame, std::shared_ptr<ob::AccelFrame>>(
      m, "AccelFrame")
      .def("get_x",
           [](const std::shared_ptr<ob::AccelFrame>& self) {
             OB_TRY_CATCH({ return self->value().x; });
           })
      .def("get_y",
           [](const std::shared_ptr<ob::AccelFrame>& self) {
             OB_TRY_CATCH({ return self->value().y; });
           })
      .def("get_z",
           [](const std::shared_ptr<ob::AccelFrame>& self) {
             OB_TRY_CATCH({ return self->value().z; });
           })
      .def("get_temperature",
           [](const std::shared_ptr<ob::AccelFrame>& self) {
             OB_TRY_CATCH({ return self->temperature(); });
           })
      .def("get_value",
           [](const std::shared_ptr<ob::AccelFrame>& self) {
             OB_TRY_CATCH({ return self->value(); });
           })
      .def("__repr__", [](const std::shared_ptr<ob::AccelFrame>& self) {
        OB_TRY_CATCH({
          std::ostringstream oss;
          oss << "<AccelFrame x=" << self->value().x << " y=" << self->value().y
              << " z=" << self->value().z
              << " temperature=" << self->temperature() << ">";
          return oss.str();
        });
      });
}

void define_gyro_frame(const py::object& m) {
  py::class_<ob::GyroFrame, ob::Frame, std::shared_ptr<ob::GyroFrame>>(
      m, "GyroFrame")
      .def("get_x",
           [](const std::shared_ptr<ob::GyroFrame>& self) {
             OB_TRY_CATCH({ return self->value().x; });
           })
      .def("get_y",
           [](const std::shared_ptr<ob::GyroFrame>& self) {
             OB_TRY_CATCH({ return self->value().y; });
           })
      .def("get_z",
           [](const std::shared_ptr<ob::GyroFrame>& self) {
             OB_TRY_CATCH({ return self->value().z; });
           })
      .def("get_temperature",
           [](const std::shared_ptr<ob::GyroFrame>& self) {
             OB_TRY_CATCH({ return self->temperature(); });
           })
      .def("get_value",
           [](const std::shared_ptr<ob::GyroFrame>& self) {
             OB_TRY_CATCH({ return self->value(); });
           })
      .def("__repr__", [](const std::shared_ptr<ob::GyroFrame>& self) {
        OB_TRY_CATCH({
          std::ostringstream oss;
          oss << "<GyroFrame x=" << self->value().x << " y=" << self->value().y
              << " z=" << self->value().z
              << " temperature=" << self->temperature() << ">";
          return oss.str();
        });
      });
}

void define_lidar_points_frame(const py::object& m) {
  py::class_<ob::LiDARPointsFrame, ob::Frame,
             std::shared_ptr<ob::LiDARPointsFrame>>(m, "LiDARPointsFrame");
}

}  // namespace pyorbbecsdk
