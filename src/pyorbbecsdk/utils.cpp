#include "utils.hpp"
namespace pyorbbecsdk {
std::vector<std::string> split(const std::string& s, const std::string& delim) {
  std::vector<std::string> elems;
  size_t pos = 0;
  size_t len = s.length();
  size_t delim_len = delim.length();
  if (delim_len == 0) return elems;
  while (pos < len) {
    size_t find_pos = s.find(delim, pos);
    if (find_pos == std::string::npos) {
      elems.push_back(s.substr(pos, len - pos));
      break;
    }
    elems.push_back(s.substr(pos, find_pos - pos));
    pos = find_pos + delim_len;
  }
  return elems;
}

std::string ob_format_to_string(OBFormat format) {
  switch (format) {
    case OBFormat::OB_FORMAT_YUYV:
      return "YUYV";
    case OBFormat::OB_FORMAT_YUY2:
      return "YUY2";
    case OBFormat::OB_FORMAT_UYVY:
      return "UYVY";
    case OBFormat::OB_FORMAT_NV12:
      return "NV12";
    case OBFormat::OB_FORMAT_NV21:
      return "NV21";
    case OBFormat::OB_FORMAT_MJPG:
      return "MJPG";
    case OBFormat::OB_FORMAT_H264:
      return "H264";
    case OBFormat::OB_FORMAT_H265:
      return "H265";
    case OBFormat::OB_FORMAT_Y16:
      return "Y16";
    case OBFormat::OB_FORMAT_Y8:
      return "Y8";
    case OBFormat::OB_FORMAT_Y10:
      return "Y10";
    case OBFormat::OB_FORMAT_Y11:
      return "Y11";
    case OBFormat::OB_FORMAT_Y12:
      return "Y12";
    case OBFormat::OB_FORMAT_GRAY:
      return "GRAY";
    case OBFormat::OB_FORMAT_HEVC:
      return "HEVC";
    case OBFormat::OB_FORMAT_I420:
      return "I420";
    case OBFormat::OB_FORMAT_ACCEL:
      return "ACCEL";
    case OBFormat::OB_FORMAT_GYRO:
      return "GYRO";
    case OBFormat::OB_FORMAT_POINT:
      return "POINT";
    case OBFormat::OB_FORMAT_RGB_POINT:
    case OBFormat::OB_FORMAT_RLE:
      return "RLE";
    case OBFormat::OB_FORMAT_RGB:
      return "RGB";
    case OBFormat::OB_FORMAT_BGR:
      return "BGR";
    case OBFormat::OB_FORMAT_Y14:
      return "Y14";
    case OBFormat::OB_FORMAT_BGRA:
      return "BGRA";
    case OBFormat::OB_FORMAT_COMPRESSED:
      return "COMPRESSED";
    case OBFormat::OB_FORMAT_RVL:
      return "RVL";
    default:
      return "UNKNOWN";
  }
}
}  // namespace pyorbbecsdk
