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
#include "types.hpp"

#include "utils.hpp"
namespace pyorbbecsdk {

void define_orbbec_types(const py::object &m) {
  py::enum_<OBPermissionType>(m, "OBPermissionType")
      .value("PERMISSION_DENY", OB_PERMISSION_DENY)
      .value("PERMISSION_READ", OB_PERMISSION_READ)
      .value("PERMISSION_WRITE", OB_PERMISSION_WRITE)
      .value("PERMISSION_READ_WRITE", OB_PERMISSION_READ_WRITE);

  py::enum_<OBStatus>(m, "OBStatus")
      .value("STATUS_OK", OB_STATUS_OK)
      .value("STATUS_ERROR", OB_STATUS_ERROR);

  py::enum_<OBLogSeverity>(m, "OBLogLevel")
      .value("DEBUG", OB_LOG_SEVERITY_DEBUG)
      .value("INFO", OB_LOG_SEVERITY_INFO)
      .value("WARNING", OB_LOG_SEVERITY_WARN)
      .value("ERROR", OB_LOG_SEVERITY_ERROR)
      .value("FATAL", OB_LOG_SEVERITY_FATAL)
      .value("NONE", OB_LOG_SEVERITY_NONE);

  py::enum_<OBExceptionType>(m, "OBException")
      .value("UNKNOWN", OB_EXCEPTION_TYPE_UNKNOWN)
      .value("CAMERA_DISCONNECTED", OB_EXCEPTION_TYPE_CAMERA_DISCONNECTED)
      .value("PLATFORM", OB_EXCEPTION_TYPE_PLATFORM)
      .value("INVALID_VALUE", OB_EXCEPTION_TYPE_INVALID_VALUE)
      .value("WRONG_API_CALL_SEQUENCE",
             OB_EXCEPTION_TYPE_WRONG_API_CALL_SEQUENCE)
      .value("NOT_IMPLEMENTED", OB_EXCEPTION_TYPE_NOT_IMPLEMENTED)
      .value("IO_ERROR", OB_EXCEPTION_TYPE_IO);

  py::enum_<OBSensorType>(m, "OBSensorType")
      .value("UNKNOWN_SENSOR", OB_SENSOR_UNKNOWN)
      .value("IR_SENSOR", OB_SENSOR_IR)
      .value("COLOR_SENSOR", OB_SENSOR_COLOR)
      .value("DEPTH_SENSOR", OB_SENSOR_DEPTH)
      .value("ACCEL_SENSOR", OB_SENSOR_ACCEL)
      .value("GYRO_SENSOR", OB_SENSOR_GYRO)
      .value("LEFT_IR_SENSOR", OB_SENSOR_IR_LEFT)
      .value("RIGHT_IR_SENSOR", OB_SENSOR_IR_RIGHT);

  py::enum_<OBStreamType>(m, "OBStreamType")
      .value("UNKNOWN_STREAM", OB_STREAM_UNKNOWN)
      .value("VIDEO_STREAM", OB_STREAM_VIDEO)
      .value("IR_STREAM", OB_STREAM_IR)
      .value("COLOR_STREAM", OB_STREAM_COLOR)
      .value("DEPTH_STREAM", OB_STREAM_DEPTH)
      .value("ACCEL_STREAM", OB_STREAM_ACCEL)
      .value("GYRO_STREAM", OB_STREAM_GYRO)
      .value("LEFT_IR_STREAM", OB_STREAM_IR_LEFT)
      .value("RIGHT_IR_STREAM", OB_STREAM_IR_RIGHT);

  py::enum_<OBFrameType>(m, "OBFrameType")
      .value("UNKNOWN_FRAME", OB_FRAME_UNKNOWN)
      .value("VIDEO_FRAME", OB_FRAME_VIDEO)
      .value("IR_FRAME", OB_FRAME_IR)
      .value("COLOR_FRAME", OB_FRAME_COLOR)
      .value("DEPTH_FRAME", OB_FRAME_DEPTH)
      .value("ACCEL_FRAME", OB_FRAME_ACCEL)
      .value("GYRO_FRAME", OB_FRAME_GYRO)
      .value("LEFT_IR_FRAME", OB_FRAME_IR_LEFT)
      .value("RIGHT_IR_FRAME", OB_FRAME_IR_RIGHT)
      .value("FRAME_SET", OB_FRAME_SET);

  py::enum_<OBFormat>(m, "OBFormat")
      .value("UNKNOWN_FORMAT", OB_FORMAT_UNKNOWN)
      .value("YUYV", OB_FORMAT_YUYV)
      .value("YUY2", OB_FORMAT_YUY2)
      .value("UYVY", OB_FORMAT_UYVY)
      .value("NV12", OB_FORMAT_NV12)
      .value("NV21", OB_FORMAT_NV21)
      .value("MJPG", OB_FORMAT_MJPG)
      .value("H264", OB_FORMAT_H264)
      .value("H265", OB_FORMAT_H265)
      .value("Y16", OB_FORMAT_Y16)
      .value("Y8", OB_FORMAT_Y8)
      .value("Y10", OB_FORMAT_Y10)
      .value("Y11", OB_FORMAT_Y11)
      .value("Y12", OB_FORMAT_Y12)
      .value("GRAY", OB_FORMAT_GRAY)
      .value("HEVC", OB_FORMAT_HEVC)
      .value("I420", OB_FORMAT_I420)
      .value("ACCEL", OB_FORMAT_ACCEL)
      .value("GYRO", OB_FORMAT_GYRO)
      .value("POINT", OB_FORMAT_POINT)
      .value("RGB_POINT", OB_FORMAT_RGB_POINT)
      .value("RLE", OB_FORMAT_RLE)
      .value("RGB", OB_FORMAT_RGB)
      .value("BGR", OB_FORMAT_BGR)
      .value("Y14", OB_FORMAT_Y14)
      .value("BGRA", OB_FORMAT_BGRA)
      .value("COMPRESSED", OB_FORMAT_COMPRESSED)
      .value("RVL", OB_FORMAT_RVL);

  py::enum_<OBUpgradeState>(m, "OBUpgradeState")
      .value("FILE_TRANSFER", STAT_FILE_TRANSFER)
      .value("DONE", STAT_DONE)
      .value("IN_PROGRESS", STAT_IN_PROGRESS)
      .value("START", STAT_START)
      .value("VERIFY_IMAGE", STAT_VERIFY_IMAGE)
      .value("VERIFY_ERROR", ERR_VERIFY)
      .value("PROGRAM_ERROR", ERR_PROGRAM)
      .value("ERASE_ERROR", ERR_ERASE)
      .value("FLASH_TYPE_ERROR", ERR_FLASH_TYPE)
      .value("IMAGE_SIZE_ERROR", ERR_IMAGE_SIZE)
      .value("OTHER_ERROR", ERR_OTHER)
      .value("DDR_ERROR", ERR_DDR)
      .value("TIMEOUT_ERROR", ERR_TIMEOUT);

  py::enum_<OBFileTranState>(m, "OBFileTranState")
      .value("TRANSFER", FILE_TRAN_STAT_TRANSFER)
      .value("DONE", FILE_TRAN_STAT_DONE)
      .value("PREPARING", FILE_TRAN_STAT_PREPAR)
      .value("DDR_ERROR", FILE_TRAN_ERR_DDR)
      .value("NOT_ENOUGH_SPACE_ERROR", FILE_TRAN_ERR_NOT_ENOUGH_SPACE)
      .value("PATH_NOT_WRITABLE_ERROR", FILE_TRAN_ERR_PATH_NOT_WRITABLE)
      .value("MD5_ERROR", FILE_TRAN_ERR_MD5_ERROR)
      .value("WRITE_FLASH_ERROR", FILE_TRAN_ERR_WRITE_FLASH_ERROR)
      .value("TIMEOUT_ERROR", FILE_TRAN_ERR_TIMEOUT);

  py::enum_<OBDataTranState>(m, "OBDataTranState")
      .value("STOPPED", DATA_TRAN_STAT_STOPPED)
      .value("DONE", DATA_TRAN_STAT_DONE)
      .value("VERIFYING", DATA_TRAN_STAT_VERIFYING)
      .value("TRANSFERRING", DATA_TRAN_STAT_TRANSFERRING)
      .value("BUSY", DATA_TRAN_ERR_BUSY)
      .value("UNSUPPORTED_ERROR", DATA_TRAN_ERR_UNSUPPORTED)
      .value("TRANSFER_FAILED", DATA_TRAN_ERR_TRAN_FAILED)
      .value("VERIFY_FAILED", DATA_TRAN_ERR_VERIFY_FAILED)
      .value("OTHER_ERROR", DATA_TRAN_ERR_OTHER);

  py::class_<OBIntPropertyRange>(m, "OBIntPropertyRange")
      .def(py::init<>())
      .def_readwrite("current", &OBIntPropertyRange::cur)
      .def_readwrite("min", &OBIntPropertyRange::min)
      .def_readwrite("max", &OBIntPropertyRange::max)
      .def_readwrite("step", &OBIntPropertyRange::step)
      .def_readwrite("default_value", &OBIntPropertyRange::def);

  py::class_<OBFloatPropertyRange>(m, "OBFloatPropertyRange")
      .def(py::init<>())
      .def_readwrite("current", &OBFloatPropertyRange::cur)
      .def_readwrite("min", &OBFloatPropertyRange::min)
      .def_readwrite("max", &OBFloatPropertyRange::max)
      .def_readwrite("step", &OBFloatPropertyRange::step)
      .def_readwrite("default_value", &OBFloatPropertyRange::def);

  py::class_<OBCameraIntrinsic>(m, "OBCameraIntrinsic")
      .def(py::init<>())
      .def_readwrite("fx", &OBCameraIntrinsic::fx)
      .def_readwrite("fy", &OBCameraIntrinsic::fy)
      .def_readwrite("cx", &OBCameraIntrinsic::cx)
      .def_readwrite("cy", &OBCameraIntrinsic::cy)
      .def_readwrite("width", &OBCameraIntrinsic::width)
      .def_readwrite("height", &OBCameraIntrinsic::height)
      .def("__repr__", [](const OBCameraIntrinsic &a) {
        return "<OBCameraIntrinsic fx=" + std::to_string(a.fx) +
               " fy=" + std::to_string(a.fy) + " cx=" + std::to_string(a.cx) +
               " cy=" + std::to_string(a.cy) +
               " width=" + std::to_string(a.width) +
               " height=" + std::to_string(a.height) + ">";
      });

  py::class_<OBCameraDistortion>(m, "OBCameraDistortion")
      .def(py::init<>())
      .def_readwrite("k1", &OBCameraDistortion::k1)
      .def_readwrite("k2", &OBCameraDistortion::k2)
      .def_readwrite("k3", &OBCameraDistortion::k3)
      .def_readwrite("k4", &OBCameraDistortion::k4)
      .def_readwrite("k5", &OBCameraDistortion::k5)
      .def_readwrite("k6", &OBCameraDistortion::k6)
      .def_readwrite("p1", &OBCameraDistortion::p1)
      .def_readwrite("p2", &OBCameraDistortion::p2)
      .def("__repr__", [](const OBCameraDistortion &a) {
        return "<OBCameraDistortion k1=" + std::to_string(a.k1) +
               " k2=" + std::to_string(a.k2) + " k3=" + std::to_string(a.k3) +
               " k4=" + std::to_string(a.k4) + " k5=" + std::to_string(a.k5) +
               " k6=" + std::to_string(a.k6) + " p1=" + std::to_string(a.p1) +
               " p2=" + std::to_string(a.p2) + ">";
      });

  py::class_<OBD2CTransform>(m, "OBD2CTransform")
      .def(py::init<>())
      .def_property(
          "rot",
          [](const OBD2CTransform &self) -> py::array_t<float> {
            py::array_t<float> result({3, 3});
            std::memcpy(result.mutable_data(), self.rot, 3 * 3 * sizeof(float));
            return result;
          },
          [](OBD2CTransform &self, const py::array_t<float> &value) {
            if (value.ndim() != 2 || value.shape(0) != 3 || value.shape(1) != 3)
              throw std::runtime_error("rot must be a 3x3 array");
            std::memcpy(self.rot, value.data(), 9 * sizeof(float));
          })
      .def_property(
          "transform",
          [](const OBD2CTransform &self) -> py::array_t<float> {
            py::array_t<float> result(3);
            std::memcpy(result.mutable_data(), self.trans, 3 * sizeof(float));
            return result;
          },
          [](OBD2CTransform &self, const py::array_t<float> &value) {
            if (value.ndim() != 1 || value.shape(0) != 3)
              throw std::runtime_error(
                  "transform must be a 1D array with 3 elements");
            std::memcpy(self.trans, value.data(), 3 * sizeof(float));
          })
      .def("__repr__", [](OBD2CTransform &transform) {
        std::ostringstream oss;
        oss << "<OBD2CTransform rot=[";
        for (int i = 0; i < 9; i++) {
          oss << transform.rot[i];
          if (i != 8) {
            oss << ", ";
          }
        }
        oss << "]" << std::endl;
        oss << "transform=[";
        oss << transform.trans[0] << ", " << transform.trans[1] << ", "
            << transform.trans[2] << "]";
        return oss.str();
      });

  py::class_<OBCameraParam>(m, "OBCameraParam")
      .def(py::init<>())
      .def_readwrite("depth_intrinsic", &OBCameraParam::depthIntrinsic)
      .def_readwrite("depth_distortion", &OBCameraParam::depthDistortion)
      .def_readwrite("rgb_intrinsic", &OBCameraParam::rgbIntrinsic)
      .def_readwrite("rgb_distortion", &OBCameraParam::rgbDistortion)
      .def_readwrite("transform", &OBCameraParam::transform);

  py::enum_<OBAlignMode>(m, "OBAlignMode")
      .value("DISABLE", OBAlignMode::ALIGN_DISABLE)
      .value("HW_MODE", OBAlignMode::ALIGN_D2C_HW_MODE)
      .value("SW_MODE", OBAlignMode::ALIGN_D2C_SW_MODE);

  py::class_<OBRect>(m, "OBRect")
      .def(py::init<>())
      .def_readwrite("x", &OBRect::x)
      .def_readwrite("y", &OBRect::y)
      .def_readwrite("width", &OBRect::width)
      .def_readwrite("height", &OBRect::height);

  py::enum_<OBConvertFormat>(m, "OBConvertFormat")
      .value("YUYV_TO_RGB888", OBConvertFormat::FORMAT_YUYV_TO_RGB888)
      .value("I420_TO_RGB888", OBConvertFormat::FORMAT_I420_TO_RGB888)
      .value("NV21_TO_RGB888", OBConvertFormat::FORMAT_NV21_TO_RGB888)
      .value("NV12_TO_RGB888", OBConvertFormat::FORMAT_NV12_TO_RGB888)
      .value("MJPG_TO_I420", OBConvertFormat::FORMAT_MJPG_TO_I420)
      .value("RGB888_TO_BGR", OBConvertFormat::FORMAT_RGB888_TO_BGR)
      .value("MJPG_TO_NV21", OBConvertFormat::FORMAT_MJPG_TO_NV21)
      .value("MJPG_TO_RGB888", OBConvertFormat::FORMAT_MJPG_TO_RGB888)
      .value("MJPG_TO_BGR888", OBConvertFormat::FORMAT_MJPG_TO_BGR888)
      .value("MJPG_TO_BGRA", OBConvertFormat::FORMAT_MJPG_TO_BGRA)
      .value("UYVY_TO_RGB888", OBConvertFormat::FORMAT_UYVY_TO_RGB888)
      .value("BGR_TO_RGB", OBConvertFormat::FORMAT_BGR_TO_RGB);

  py::enum_<OBGyroSampleRate>(m, "OBGyroSampleRate")
      .value("SAMPLE_RATE_1_5625_HZ",
             OBGyroSampleRate::OB_SAMPLE_RATE_1_5625_HZ)
      .value("SAMPLE_RATE_3_125_HZ", OBGyroSampleRate::OB_SAMPLE_RATE_3_125_HZ)
      .value("SAMPLE_RATE_6_25_HZ", OBGyroSampleRate::OB_SAMPLE_RATE_6_25_HZ)
      .value("SAMPLE_RATE_12_5_HZ", OBGyroSampleRate::OB_SAMPLE_RATE_12_5_HZ)
      .value("SAMPLE_RATE_25_HZ", OBGyroSampleRate::OB_SAMPLE_RATE_25_HZ)
      .value("SAMPLE_RATE_50_HZ", OBGyroSampleRate::OB_SAMPLE_RATE_50_HZ)
      .value("SAMPLE_RATE_100_HZ", OBGyroSampleRate::OB_SAMPLE_RATE_100_HZ)
      .value("SAMPLE_RATE_200_HZ", OBGyroSampleRate::OB_SAMPLE_RATE_200_HZ)
      .value("SAMPLE_RATE_500_HZ", OBGyroSampleRate::OB_SAMPLE_RATE_500_HZ)
      .value("SAMPLE_RATE_1_KHZ", OBGyroSampleRate::OB_SAMPLE_RATE_1_KHZ)
      .value("SAMPLE_RATE_2_KHZ", OBGyroSampleRate::OB_SAMPLE_RATE_2_KHZ)
      .value("SAMPLE_RATE_4_KHZ", OBGyroSampleRate::OB_SAMPLE_RATE_4_KHZ)
      .value("SAMPLE_RATE_8_KHZ", OBGyroSampleRate::OB_SAMPLE_RATE_8_KHZ)
      .value("SAMPLE_RATE_16_KHZ", OBGyroSampleRate::OB_SAMPLE_RATE_16_KHZ)
      .value("SAMPLE_RATE_32_KHZ", OBGyroSampleRate::OB_SAMPLE_RATE_32_KHZ);

  py::enum_<OBAccelFullScaleRange>(m, "OBAccelFullScaleRange")
      .value("ACCEL_FS_2g", OBAccelFullScaleRange::OB_ACCEL_FS_2g)
      .value("ACCEL_FS_4g", OBAccelFullScaleRange::OB_ACCEL_FS_4g)
      .value("ACCEL_FS_8g", OBAccelFullScaleRange::OB_ACCEL_FS_8g)
      .value("ACCEL_FS_16g", OBAccelFullScaleRange::OB_ACCEL_FS_16g);

  py::class_<OBAccelValue>(m, "OBAccelValue")
      .def(py::init<>())
      .def_readwrite("x", &OBAccelValue::x)
      .def_readwrite("y", &OBAccelValue::y)
      .def_readwrite("z", &OBAccelValue::z)
      .def("__repr__", [](const OBAccelValue &a) {
        return "<OBAccelValue x=" + std::to_string(a.x) +
               ", y=" + std::to_string(a.y) + ", z=" + std::to_string(a.z) +
               ">";
      });

  py::class_<OBDeviceTemperature>(m, "OBDeviceTemperature")
      .def(py::init<>())
      .def_readwrite("cpu_temperature", &OBDeviceTemperature::cpuTemp)
      .def_readwrite("ir_temperature", &OBDeviceTemperature::irTemp)
      .def_readwrite("laser_temperature", &OBDeviceTemperature::ldmTemp)
      .def_readwrite("main_board_temperature",
                     &OBDeviceTemperature::mainBoardTemp)
      .def_readwrite("tec_temperature", &OBDeviceTemperature::tecTemp)
      .def_readwrite("imu_temperature", &OBDeviceTemperature::imuTemp)
      .def_readwrite("rgb_temperature", &OBDeviceTemperature::rgbTemp)
      .def_readwrite("ir_left_temperature", &OBDeviceTemperature::irLeftTemp)
      .def_readwrite("ir_right_temperature", &OBDeviceTemperature::irRightTemp)
      .def_readwrite("chip_top_temperature", &OBDeviceTemperature::chipTopTemp)
      .def_readwrite("chip_bottom_temperature",
                     &OBDeviceTemperature::chipBottomTemp);

  py::enum_<OBDepthCroppingMode>(m, "OBDepthCroppingMode")
      .value("AUTO", OBDepthCroppingMode::DEPTH_CROPPING_MODE_AUTO)
      .value("CLOSE", OBDepthCroppingMode::DEPTH_CROPPING_MODE_CLOSE)
      .value("OPEN", OBDepthCroppingMode::DEPTH_CROPPING_MODE_OPEN);

  py::enum_<OBDeviceType>(m, "OBDeviceType")
      .value("LIGHT_MONOCULAR",
             OBDeviceType::OB_STRUCTURED_LIGHT_MONOCULAR_CAMERA)
      .value("LIGHT_BINOCULAR",
             OBDeviceType::OB_STRUCTURED_LIGHT_BINOCULAR_CAMERA)
      .value("TIME_OF_FLIGHT", OBDeviceType::OB_TOF_CAMERA);

  py::enum_<OBMediaType>(m, "OBMediaType")
      .value("DEPTH", OBMediaType::OB_MEDIA_DEPTH_STREAM)
      .value("COLOR", OBMediaType::OB_MEDIA_COLOR_STREAM)
      .value("IR", OBMediaType::OB_MEDIA_IR_STREAM)
      .value("GYRO", OBMediaType::OB_MEDIA_GYRO_STREAM)
      .value("ACCEL", OBMediaType::OB_MEDIA_ACCEL_STREAM)
      .value("CAMERA_PARAM", OBMediaType::OB_MEDIA_CAMERA_PARAM)
      .value("DEVICE_INFO", OBMediaType::OB_MEDIA_DEVICE_INFO)
      .value("STREAM_INFO", OBMediaType::OB_MEDIA_STREAM_INFO)
      .value("LEFT_IR", OBMediaType::OB_MEDIA_IR_LEFT_STREAM)
      .value("RIGHT_IR", OBMediaType::OB_MEDIA_IR_RIGHT_STREAM);

  py::enum_<OBMediaState>(m, "OBMediaState")
      .value("OB_MEDIA_BEGIN", OBMediaState::OB_MEDIA_BEGIN)
      .value("OB_MEDIA_PAUSE", OBMediaState::OB_MEDIA_PAUSE)
      .value("OB_MEDIA_RESUME", OBMediaState::OB_MEDIA_PAUSE)
      .value("OB_MEDIA_END", OBMediaState::OB_MEDIA_END);

  py::enum_<OBDepthPrecisionLevel>(m, "OBDepthPrecisionLevel")
      .value("ONE_MM", OBDepthPrecisionLevel::OB_PRECISION_1MM)
      .value("ZERO_POINT_EIGHT_MM", OBDepthPrecisionLevel::OB_PRECISION_0MM8)
      .value("ZERO_POINT_FOUR_MM", OBDepthPrecisionLevel::OB_PRECISION_0MM4)
      .value("ZERO_POINT_TWO_MM", OBDepthPrecisionLevel::OB_PRECISION_0MM2)
      .value("ZERO_POINT_ONE_MM", OBDepthPrecisionLevel::OB_PRECISION_0MM1);

  py::enum_<OBTofFilterRange>(m, "OBTofFilterRange")
      .value("CLOSE", OBTofFilterRange::OB_TOF_FILTER_RANGE_CLOSE)
      .value("MIDDLE", OBTofFilterRange::OB_TOF_FILTER_RANGE_MIDDLE)
      .value("FAR", OBTofFilterRange::OB_TOF_FILTER_RANGE_LONG)
      .value("DEBUG", OBTofFilterRange::OB_TOF_FILTER_RANGE_DEBUG);

  py::class_<OBPoint>(m, "OBPoint")
      .def(py::init<>())
      .def_readwrite("x", &OBPoint::x)
      .def_readwrite("y", &OBPoint::y)
      .def_readwrite("z", &OBPoint::z)
      .def("__repr__", [](const OBPoint &p) {
        return "(" + std::to_string(p.x) + ", " + std::to_string(p.y) + ", " +
               std::to_string(p.z) + ")";
      });

  py::class_<OBColorPoint>(m, "OBColorPoint")
      .def(py::init<>())
      .def_readwrite("x", &OBColorPoint::x)
      .def_readwrite("y", &OBColorPoint::y)
      .def_readwrite("z", &OBColorPoint::z)
      .def_property(
          "r", [](const OBColorPoint &p) { return static_cast<int>(p.r); },
          [](OBColorPoint &p, int r) { p.r = static_cast<float>(r); })
      .def_property(
          "g", [](const OBColorPoint &p) { return static_cast<int>(p.g); },
          [](OBColorPoint &p, int g) { p.g = static_cast<float>(g); })
      .def_property(
          "b", [](const OBColorPoint &p) { return static_cast<int>(p.b); },
          [](OBColorPoint &p, int b) { p.b = static_cast<float>(b); })
      .def("__repr__", [](const OBColorPoint &p) {
        return "(" + std::to_string(p.x) + ", " + std::to_string(p.y) + ", " +
               std::to_string(p.z) + ", " + std::to_string(p.r) + ", " +
               std::to_string(p.g) + ", " + std::to_string(p.b) + ")";
      });

  py::enum_<OBCompressionMode>(m, "OBCompressionMode")
      .value("LOSSLESS", OBCompressionMode::OB_COMPRESSION_LOSSLESS)
      .value("LOSSY", OBCompressionMode::OB_COMPRESSION_LOSSY);

  py::class_<OBCompressionParams>(m, "OBCompressionParams")
      .def(py::init<>())
      .def_readwrite("threshold", &OBCompressionParams::threshold);

  py::class_<OBTofExposureThresholdControl>(m, "OBTofExposureThresholdControl")
      .def(py::init<>())
      .def_readwrite("upper", &OBTofExposureThresholdControl::upper)
      .def_readwrite("lower", &OBTofExposureThresholdControl::lower);

  py::enum_<OBSyncMode>(m, "OBSyncMode")
      .value("CLOSE", OBSyncMode::OB_SYNC_MODE_CLOSE)
      .value("STANDALONE", OBSyncMode::OB_SYNC_MODE_STANDALONE)
      .value("PRIMARY", OBSyncMode::OB_SYNC_MODE_PRIMARY)
      .value("SECONDARY", OBSyncMode::OB_SYNC_MODE_SECONDARY)
      .value("PRIMARY_MCU_TRIGGER",
             OBSyncMode::OB_SYNC_MODE_PRIMARY_MCU_TRIGGER)
      .value("PRIMARY_IR_TRIGGER", OBSyncMode::OB_SYNC_MODE_PRIMARY_IR_TRIGGER)
      .value("PRIMARY_SOFT_TRIGGER",
             OBSyncMode::OB_SYNC_MODE_PRIMARY_SOFT_TRIGGER)
      .value("SECONDARY_SOFT_TRIGGER",
             OBSyncMode::OB_SYNC_MODE_SECONDARY_SOFT_TRIGGER)
      .value("UNKNOWN", OBSyncMode::OB_SYNC_MODE_UNKNOWN);

  py::enum_<OBPowerLineFreqMode>(m, "OBPowerLineFreqMode")
      .value("FREQUENCY_50HZ",
             OBPowerLineFreqMode::OB_POWER_LINE_FREQ_MODE_50HZ)
      .value("FREQUENCY_60HZ",
             OBPowerLineFreqMode::OB_POWER_LINE_FREQ_MODE_60HZ)
      .value("FREQUENCY_CLOSE",
             OBPowerLineFreqMode::OB_POWER_LINE_FREQ_MODE_CLOSE);

  py::class_<OBDeviceSyncConfig>(m, "OBDeviceSyncConfig")
      .def(py::init<>())
      .def_readwrite("mode", &OBDeviceSyncConfig::syncMode)
      .def_readwrite("ir_trigger_signal_delay",
                     &OBDeviceSyncConfig::irTriggerSignalInDelay)
      .def_readwrite("rgb_trigger_signal_delay",
                     &OBDeviceSyncConfig::rgbTriggerSignalInDelay)
      .def_readwrite("device_trigger_signal_out_delay",
                     &OBDeviceSyncConfig::deviceTriggerSignalOutDelay)
      .def_readwrite("device_trigger_signal_out_polarity",
                     &OBDeviceSyncConfig::deviceTriggerSignalOutPolarity)
      .def_readwrite("mcu_trigger_frequency",
                     &OBDeviceSyncConfig::mcuTriggerFrequency)
      .def_readwrite("device_index", &OBDeviceSyncConfig::deviceId);

  py::class_<OBDepthWorkMode>(m, "OBDepthWorkMode")
      .def(py::init<>())
      .def_property(
          "checksum",
          [](const OBDepthWorkMode &mode) -> py::array_t<uint8_t> {
            py::array_t<uint8_t> arr(16);
            std::memcpy(arr.mutable_data(), mode.checksum, 16);
            return arr;
          },
          [](OBDepthWorkMode &mode, const py::array_t<uint8_t> &arr) {
            std::memcpy(mode.checksum, arr.data(), 16);
          })
      .def_property(
          "name",
          [](const OBDepthWorkMode &mode) -> std::string { return mode.name; },
          [](OBDepthWorkMode &mode, const std::string &str) {
            std::strncpy(mode.name, str.c_str(), 31);
            mode.name[31] = '\0';  // ensure null-termination
          })
      .def("__repr__",
           [](const OBDepthWorkMode &mode) { return std::string(mode.name); })
      .def("__eq__",
           [](const OBDepthWorkMode &mode1, const OBDepthWorkMode &mode2) {
             return std::memcmp(mode1.name, mode2.name, 32) == 0;
           });

  py::class_<OBDeviceIpAddrConfig>(m, "OBDeviceIpAddrConfig")
      .def(py::init<>())
      .def_readwrite("dhcp", &OBDeviceIpAddrConfig::dhcp)
      .def_property(
          "address",
          [](const OBDeviceIpAddrConfig &config) -> std::string {
            std::string addr = std::to_string(config.address[0]) + "." +
                               std::to_string(config.address[1]) + "." +
                               std::to_string(config.address[2]) + "." +
                               std::to_string(config.address[3]);
            return addr;
          },
          [](OBDeviceIpAddrConfig &config, const std::string &str) {
            auto addr = split(str, ".");

            if (addr.size() != 4) {
              throw std::runtime_error("Invalid IP address");
            }
            for (int i = 0; i < 4; i++) {
              config.address[i] = std::stoi(addr[i]);
            }
          })
      .def_property(
          "netmask",
          [](const OBDeviceIpAddrConfig &config) -> std::string {
            std::string addr = std::to_string(config.mask[0]) + "." +
                               std::to_string(config.mask[1]) + "." +
                               std::to_string(config.mask[2]) + "." +
                               std::to_string(config.mask[3]);
            return addr;
          },
          [](OBDeviceIpAddrConfig &config, const std::string &str) {
            auto addr = split(str, ".");

            if (addr.size() != 4) {
              throw std::runtime_error("Invalid IP address");
            }
            for (int i = 0; i < 4; i++) {
              config.mask[i] = std::stoi(addr[i]);
            }
          })
      .def_property(
          "gateway",
          [](const OBDeviceIpAddrConfig &config) -> std::string {
            std::string addr = std::to_string(config.gateway[0]) + "." +
                               std::to_string(config.gateway[1]) + "." +
                               std::to_string(config.gateway[2]) + "." +
                               std::to_string(config.gateway[3]);
            return addr;
          },
          [](OBDeviceIpAddrConfig &config, const std::string &str) {
            auto addr = split(str, ".");
            if (addr.size() != 4) {
              throw std::runtime_error("Invalid IP address");
            }
            for (int i = 0; i < 4; i++) {
              config.gateway[i] = std::stoi(addr[i]);
            }
          });

  py::enum_<OBCommunicationType>(m, "OBCommunicationType")
      .value("USB", OBCommunicationType::OB_COMM_USB)
      .value("ETHERNET", OBCommunicationType::OB_COMM_NET);

  py::enum_<OBUSBPowerState>(m, "OBUSBPowerState")
      .value("OFF", OBUSBPowerState::OB_USB_POWER_NO_PLUGIN)
      .value("POWER_5V_0A9", OBUSBPowerState::OB_USB_POWER_5V_0A9)
      .value("POWER_5V_1A5", OBUSBPowerState::OB_USB_POWER_5V_1A5)
      .value("POWER_5V_3A0", OBUSBPowerState::OB_USB_POWER_5V_3A0);

  py::enum_<OBDCPowerState>(m, "OBDCPowerState")
      .value("OFF", OBDCPowerState::OB_DC_POWER_NO_PLUGIN)
      .value("ON", OBDCPowerState::OB_DC_POWER_PLUGIN);

  py::enum_<OBRotateDegreeType>(m, "OBRotateDegreeType")
      .value("ROTATE_0", OBRotateDegreeType::OB_ROTATE_DEGREE_0)
      .value("ROTATE_90", OBRotateDegreeType::OB_ROTATE_DEGREE_90)
      .value("ROTATE_180", OBRotateDegreeType::OB_ROTATE_DEGREE_180)
      .value("ROTATE_270", OBRotateDegreeType::OB_ROTATE_DEGREE_270);

  py::class_<OBProtocolVersion>(m, "OBProtocolVersion")
      .def(py::init<>())
      .def_readwrite("major", &OBProtocolVersion::major)
      .def_readwrite("minor", &OBProtocolVersion::minor)
      .def_readwrite("patch", &OBProtocolVersion::patch);

  py::enum_<OBCmdVersion>(m, "OBCmdVersion")
      .value("V0", OBCmdVersion::OB_CMD_VERSION_V0)
      .value("V1", OBCmdVersion::OB_CMD_VERSION_V1)
      .value("V2", OBCmdVersion::OB_CMD_VERSION_V2)
      .value("V3", OBCmdVersion::OB_CMD_VERSION_V3)
      .value("NONE", OBCmdVersion::OB_CMD_VERSION_NOVERSION)
      .value("INVALID", OBCmdVersion::OB_CMD_VERSION_INVALID);

  py::class_<OBDataBundle>(m, "OBDataBundle")
      .def(py::init<>())
      .def_readwrite("cmd_version", &OBDataBundle::cmdVersion)
      .def_readwrite("data_size", &OBDataBundle::dataSize)
      .def_readwrite("item_type_size", &OBDataBundle::itemTypeSize)
      .def_readwrite("item_count", &OBDataBundle::itemCount)
      .def("get_data",
           [](const OBDataBundle &b) -> py::array {
             // FIXME: copy data to result array
             py::array_t<uint8_t> arr(b.dataSize);
             std::memcpy(arr.mutable_data(), b.data, b.dataSize);
             return arr;
           })
      .def(
          "set_data",
          [](OBDataBundle &b, const py::array_t<uint8_t> &arr) {
            if (arr.itemsize() != static_cast<long>(b.itemTypeSize) ||
                arr.size() != static_cast<long>(b.itemCount)) {
              throw py::value_error("Invalid array size or item size");
            }
            std::memcpy(b.data, arr.data(), arr.nbytes());
          },
          py::arg("data"));

  py::enum_<OBFrameAggregateOutputMode>(m, "OBFrameAggregateOutputMode")
      .value("FULL_FRAME_REQUIRE",
             OBFrameAggregateOutputMode::
                 OB_FRAME_AGGREGATE_OUTPUT_FULL_FRAME_REQUIRE)
      .value("COLOR_FRAME_REQUIRE",
             OBFrameAggregateOutputMode::
                 OB_FRAME_AGGREGATE_OUTPUT_COLOR_FRAME_REQUIRE)
      .value(
          "ANY_SITUATION",
          OBFrameAggregateOutputMode::OB_FRAME_AGGREGATE_OUTPUT_ANY_SITUATION);
}
}  // namespace pyorbbecsdk
