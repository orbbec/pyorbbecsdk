// Payload layouts and error bit definitions follow Orbbec SDK InternalTypes.hpp
// (Copyright (c) Orbbec Inc., MIT license) and the supplied protocol reference.
#pragma once

#include <libobsensor/ObSensor.hpp>
#include <pybind11/pybind11.h>
#include <cstring>
#include <cstddef>
#include <string>
#include <type_traits>

namespace pyorbbecsdk {
namespace structured {

// Binding-local copies of documented SDK-internal payloads. Do not include
// headers from an external SDK checkout in a distributable Python binding.
#pragma pack(push, 1)
struct VersionInfo {
  char firmwareVersion[16];
  char hardwareVersion[16];
  char sdkVersion[16];
  char depthChip[16];
  char systemChip[16];
  char serialNumber[16];
  int32_t deviceType;
  char deviceName[16];
  char subSystemVersion[16];
  char reserved[32];
};
struct DeviceTime { uint64_t time; uint64_t rtt; };
struct DeviceErrorState { uint64_t errorCode; };
struct DepthWorkModeInternal {
  uint8_t checksum[16];
  char name[32];
  uint32_t optionCode;
};
struct ImuPresetList {
  uint32_t count;
  int32_t values[16];
};
#pragma pack(pop)

static_assert(sizeof(VersionInfo) == 164, "Invalid version payload layout");
static_assert(sizeof(DeviceTime) == 16, "Invalid time payload layout");
static_assert(sizeof(DeviceErrorState) == 8, "Invalid error payload layout");
static_assert(sizeof(DepthWorkModeInternal) == 52, "Invalid depth mode layout");
static_assert(sizeof(ImuPresetList) == 68, "Invalid IMU preset layout");

enum OBDeviceErrorCode : uint64_t {
    // bit 0~31: error code
    DEVICE_ERROR_RGB_SENSOR     = 1 << 0,   // RGB sensor error
    DEVICE_ERROR_IRL_SENSOR     = 1 << 1,   // IR left sensor error
    DEVICE_ERROR_IRR_SENSOR     = 1 << 2,   // IR right sensor error
    DEVICE_ERROR_IMU_SENSOR     = 1 << 3,   // IMU sensor error
    DEVICE_ERROR_LASER_MODULE   = 1 << 4,   // Laser module error
    DEVICE_ERROR_FLOOD_MODULE   = 1 << 5,   // Flood module error
    DEVICE_ERROR_LDP_SENSOR     = 1 << 6,   // LDP sensor error
    DEVICE_ERROR_M_ADC_CHIP     = 1 << 7,   // M_ADC chip error
    DEVICE_ERROR_S_ADC_CHIP     = 1 << 8,   // S_ADC chip error
    DEVICE_ERROR_EEPROM_SENSOR  = 1 << 9,   // EEPROM sensor error
    DEVICE_ERROR_CFG_PARAM      = 1 << 10,  // Configuration parameter error
    DEVICE_ERROR_CALIB_PARAM    = 1 << 11,  // Calibration parameter error
    DEVICE_ERROR_TEC_FUN        = 1 << 12,  // TEC function error
    DEVICE_ERROR_MCU_FUN        = 1 << 13,  // MCU function error
    DEVICE_ERROR_DSP_MODULE     = 1 << 14,  // DSP module error
    DEVICE_ERROR_OVER_LOAD      = 1 << 15,  // Overload error
    DEVICE_ERROR_ISP_MODULE     = 1 << 16,  // ISP sensor error
    DEVICE_ERROR_TRB_EXHAUSTION = 1 << 17,  // TRB exhaustion
    DEVICE_ERROR_OVF_MODULE     = 1 << 18,  // Overflow error
    DEVICE_ERROR_RGB_STREAM     = 1 << 19,  // RGB pipeline data stream failure
    DEVICE_ERROR_IRL_STREAM     = 1 << 20,  // IRL pipeline data stream failure
    DEVICE_ERROR_IRR_STREAM     = 1 << 21,  // IRR pipeline data stream failure
    DEVICE_ERROR_DEP_STREAM     = 1 << 22,  // Depth pipeline data stream failure
    DEVICE_ERROR_IRL_SNS_STREAM = 1 << 23,  // IRL sensor data stream failure
    DEVICE_ERROR_IRR_SNS_STREAM = 1 << 24,  // IRR sensor data stream failure

    // bit 32~63: warning
    DEVICE_WARNING_PERMISSION        = 1ULL << 32,  // Permission warning
    DEVICE_WARNING_IR_TEMPERATURE    = 1ULL << 33,  // IR temperature warning
    DEVICE_WARNING_RGB_TEMPERATURE   = 1ULL << 34,  // RGB temperature warning
    DEVICE_WARNING_LASER_TEMPERATURE = 1ULL << 35,  // Laser temperature warning
    DEVICE_WARNING_CPU_TEMPERATURE   = 1ULL << 36,  // CPU temperature warning
    DEVICE_WARNING_RES_MISMATCH      = 1ULL << 37,  // Resolution mismatch warning
    DEVICE_WARNING_FPS_MISMATCH      = 1ULL << 38,  // FPS mismatch warning
    DEVICE_WARNING_D2C_UNSPPOURT     = 1ULL << 39,  // D2C unsupported warning

    DEVICE_WARNING_USB_LOG      = 1ULL << 62,  // USB log warning
    DEVICE_WARNING_LOG_OVERFLOW = 1ULL << 63,  // State info cache flag
};

enum Property : uint32_t {
  VERSION = 1000,
  GYRO_ODR = 1031,
  ACCEL_ODR = 1032,
  GYRO_FULL_SCALE = 1033,
  ACCEL_FULL_SCALE = 1034,
  DEVICE_ERROR_STATE = 5524
};

template <typename T> pybind11::bytes to_bytes(const T &value) {
  static_assert(std::is_trivially_copyable<T>::value,
                "Only flat SDK payloads may be serialized");
  return pybind11::bytes(reinterpret_cast<const char *>(&value), sizeof(T));
}

template <typename T> T from_bytes(pybind11::bytes payload) {
  const std::string data = payload;
  if (data.size() != sizeof(T)) {
    throw pybind11::value_error("payload length must equal " +
                               std::to_string(sizeof(T)) + " bytes");
  }
  // A C++ bool must not be populated with an arbitrary byte representation.
  if (std::is_same<T, OBMultiDeviceSyncConfig>::value &&
      static_cast<unsigned char>(data[offsetof(OBMultiDeviceSyncConfig, triggerOutEnable)]) > 1) {
    throw pybind11::value_error("trigger_out_enable byte must be 0 or 1");
  }
  T value{};
  std::memcpy(&value, data.data(), sizeof(T));
  return value;
}

// Strings are bounded even when all bytes in a fixed char array are occupied.
template <size_t N> std::string read_text(const char (&data)[N]) {
  size_t size = 0;
  while (size < N && data[size] != '\0') ++size;
  return std::string(data, size);
}
template <size_t N> void write_text(char (&data)[N], const std::string &value) {
  if (value.size() > N || value.find('\0') != std::string::npos) {
    throw pybind11::value_error("text must fit in " + std::to_string(N) +
                               " UTF-8 bytes without embedded NUL");
  }
  std::memset(data, 0, N);
  std::memcpy(data, value.data(), value.size());
}

template <typename T>
void bind_bytes(const pybind11::object &m, const char *name) {
  auto cls = pybind11::reinterpret_borrow<pybind11::class_<T>>(m.attr(name));
  cls.def("to_bytes", &to_bytes<T>, "Copy the native packed SDK layout.")
      .def_static("from_bytes", &from_bytes<T>,
                  pybind11::arg("data").noconvert(),
                  "Decode an exact-size native packed SDK payload.");
}

}  // namespace structured
}  // namespace pyorbbecsdk
