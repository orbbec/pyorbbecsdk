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
#include "device.hpp"

#include <sstream>

#include "error.hpp"

namespace pyorbbecsdk {
void define_device_info(const py::object &m) {
  py::class_<ob::DeviceInfo, std::shared_ptr<ob::DeviceInfo>>(m, "DeviceInfo")
      .def(
          "get_name",
          [](const std::shared_ptr<ob::DeviceInfo> &self) {
            return std::string(self->name());
          },
          "Get device name")
      .def(
          "get_pid",
          [](const std::shared_ptr<ob::DeviceInfo> &self) {
            return self->pid();
          },
          "Get device pid")
      .def(
          "get_vid",
          [](const std::shared_ptr<ob::DeviceInfo> &self) {
            return self->vid();
          },
          "Get device vid")
      .def(
          "get_uid",
          [](const std::shared_ptr<ob::DeviceInfo> &self) {
            return std::string(self->uid());
          },
          "Get system assigned uid for distinguishing between different "
          "devices")
      .def(
          "get_serial_number",
          [](const std::shared_ptr<ob::DeviceInfo> &self) {
            return std::string(self->serialNumber());
          },
          "Get the serial number of the device")
      .def(
          "get_firmware_version",
          [](const std::shared_ptr<ob::DeviceInfo> &self) {
            return std::string(self->firmwareVersion());
          },
          "Get the version number of the firmware")
      .def(
          "get_connection_type",
          [](const std::shared_ptr<ob::DeviceInfo> &self) {
            return std::string(self->connectionType());
          },
          "Get the connection type of the device")
      .def(
          "get_hardware_version",
          [](const std::shared_ptr<ob::DeviceInfo> &self) {
            return std::string(self->hardwareVersion());
          },
          "Get the version number of the hardware")
      .def(
          "get_supported_min_sdk_version",
          [](const std::shared_ptr<ob::DeviceInfo> &self) {
            return std::string(self->supportedMinSdkVersion());
          },
          "Get the minimum version number of the SDK supported by the device")
      .def(
          "get_device_type",
          [](const std::shared_ptr<ob::DeviceInfo> &self) {
            return self->deviceType();
          },
          "Get the device type")
      .def("__repr__", [](const std::shared_ptr<ob::DeviceInfo> &self) {
        std::ostringstream oss;
        oss << "DeviceInfo(name=" << self->name() << std::endl
            << ", pid=" << self->pid() << std::endl
            << ", vid=" << self->vid() << ", uid=" << self->uid() << std::endl
            << ", serial_number=" << self->serialNumber() << std::endl
            << ", firmware_version=" << self->firmwareVersion() << std::endl
            << ", connection_type=" << self->connectionType() << std::endl
            << ", hardware_version=" << self->hardwareVersion() << std::endl
            << ", supported_min_sdk_version=" << self->supportedMinSdkVersion()
            << std::endl
            << ", device_type=" << self->deviceType() << ")";
        return oss.str();
      });
}

void define_camera_list(const py::object &m) {
  py::class_<ob::CameraParamList, std::shared_ptr<ob::CameraParamList>>(
      m, "CameraParamList")
      .def(
          "get_count",
          [](const std::shared_ptr<ob::CameraParamList> &self) {
            return self->count();
          },
          "Get the number of devices in the list")
      .def(
          "get_camera_param",
          [](const std::shared_ptr<ob::CameraParamList> &self, int index) {
            return self->getCameraParam(index);
          },
          "Get the camera parameters for the specified index")
      .def("__len__", [](const std::shared_ptr<ob::CameraParamList> &self) {
        return self->count();
      });
}

void define_depth_work_mode_list(const py::object &m) {
  py::class_<ob::OBDepthWorkModeList, std::shared_ptr<ob::OBDepthWorkModeList>>(
      m, "OBDepthWorkModeList")
      .def(
          "get_count",
          [](const std::shared_ptr<ob::OBDepthWorkModeList> &self) {
            return self->count();
          },
          "Get the number of OBDepthWorkMode objects in the list")
      .def(
          "get_depth_work_mode_by_index",
          [](const std::shared_ptr<ob::OBDepthWorkModeList> &self, int index) {
            return self->getOBDepthWorkMode(index);
          },
          "Get the OBDepthWorkMode object at the specified index")
      .def(
          "get_name_by_index",
          [](const std::shared_ptr<ob::OBDepthWorkModeList> &self, int index) {
            return self->getName(index);
          },
          "Get the name of the depth work mode at the specified index")
      .def("__len__", [](const std::shared_ptr<ob::OBDepthWorkModeList> &self) {
        return self->count();
      });
}

void define_device(const py::object &m) {
  py::class_<ob::Device, std::shared_ptr<ob::Device>>(m, "Device")
      .def("get_device_info",
           [](const std::shared_ptr<ob::Device> &self) {
             return self->getDeviceInfo();
           })
      .def("get_sensor_list",
           [](const std::shared_ptr<ob::Device> &self) {
             return self->getSensorList();
           })
      .def("get_sensor",
           [](const std::shared_ptr<ob::Device> &self, OBSensorType type) {
             return self->getSensor(type);
           })
      .def("set_int_property",
           [](const std::shared_ptr<ob::Device> &self, OBPropertyID property_id,
              int value) {
             OB_TRY_CATCH({ return self->setIntProperty(property_id, value); });
           })
      .def("get_int_property",
           [](const std::shared_ptr<ob::Device> &self,
              OBPropertyID property_id) {
             OB_TRY_CATCH({ return self->getIntProperty(property_id); });
           })
      .def("set_float_property",
           [](const std::shared_ptr<ob::Device> &self, OBPropertyID property_id,
              float value) {
             OB_TRY_CATCH(
                 { return self->setFloatProperty(property_id, value); });
           })
      .def("get_float_property",
           [](const std::shared_ptr<ob::Device> &self,
              OBPropertyID property_id) {
             OB_TRY_CATCH({ return self->getFloatProperty(property_id); });
           })
      .def(
          "set_bool_property",
          [](const std::shared_ptr<ob::Device> &self, OBPropertyID property_id,
             bool value) {
            OB_TRY_CATCH({ return self->setBoolProperty(property_id, value); });
          })
      .def("get_bool_property",
           [](const std::shared_ptr<ob::Device> &self,
              OBPropertyID property_id) {
             OB_TRY_CATCH({ return self->getBoolProperty(property_id); });
           })
      .def("get_int_property_range",
           [](const std::shared_ptr<ob::Device> &self,
              OBPropertyID property_id) {
             OB_TRY_CATCH({ return self->getIntPropertyRange(property_id); });
           })
      .def("get_float_property_range",
           [](const std::shared_ptr<ob::Device> &self,
              OBPropertyID property_id) {
             OB_TRY_CATCH({ return self->getFloatPropertyRange(property_id); });
           })
      .def("get_bool_property_range",
           [](const std::shared_ptr<ob::Device> &self,
              OBPropertyID property_id) {
             OB_TRY_CATCH({ return self->getBoolPropertyRange(property_id); });
           })
      .def("get_support_property_count",
           [](const std::shared_ptr<ob::Device> &self) {
             return self->getSupportedPropertyCount();
           })
      .def("get_supported_property",
           [](const std::shared_ptr<ob::Device> &self, int index) {
             return self->getSupportedProperty(index);
           })
      .def("is_property_supported",
           [](const std::shared_ptr<ob::Device> &self, OBPropertyID property_id,
              OBPermissionType permission_type) {
             OB_TRY_CATCH({
               return self->isPropertySupported(property_id, permission_type);
             });
           })
      .def("get_device_state",
           [](const std::shared_ptr<ob::Device> &self) {
             return self->getDeviceState();
           })
      .def("set_device_state_changed_callback",
           [](const std::shared_ptr<ob::Device> &self,
              const py::function &callback) {
             OB_TRY_CATCH({ self->setDeviceStateChangedCallback(callback); });
           })
      .def("active_authorization",
           [](const std::shared_ptr<ob::Device> &self, const std::string &key) {
             OB_TRY_CATCH({ return self->activateAuthorization(key.c_str()); });
           })
      .def("get_calibration_camera_param_list",
           [](const std::shared_ptr<ob::Device> &self) {
             OB_TRY_CATCH({ return self->getCalibrationCameraParamList(); });
           })
      .def("get_depth_work_mode",
           [](const std::shared_ptr<ob::Device> &self) {
             OB_TRY_CATCH({ return self->getCurrentDepthWorkMode(); });
           })
      .def("set_depth_work_mode",
           [](const std::shared_ptr<ob::Device> &self, OBDepthWorkMode mode) {
             OB_TRY_CATCH({ return self->switchDepthWorkMode(mode); });
           })
      .def("get_depth_work_mode_list",
           [](const std::shared_ptr<ob::Device> &self) {
             OB_TRY_CATCH({ return self->getDepthWorkModeList(); });
           })
      .def("reboot",
           [](const std::shared_ptr<ob::Device> &self) { self->reboot(); })
      .def("get_baseline",
           [](const std::shared_ptr<ob::Device> &self) {
             OB_TRY_CATCH({
               OBBaselineCalibrationParam param;
               uint32_t size = sizeof(param);
               self->getStructuredData(OB_STRUCT_BASELINE_CALIBRATION_PARAM,
                                       &param, &size);
               return param;
             });
           })
      .def("__eq__", [](const std::shared_ptr<ob::Device> &self,
                        const std::shared_ptr<ob::Device> &other) {
        std::string device_uid = self->getDeviceInfo()->uid();
        std::string other_device_uid = other->getDeviceInfo()->uid();
        return device_uid == other_device_uid;
      });
}

void define_device_list(const py::object &m) {
  py::class_<ob::DeviceList, std::shared_ptr<ob::DeviceList>>(m, "DeviceList")
      .def("get_count",
           [](const std::shared_ptr<ob::DeviceList> &self) {
             return self->deviceCount();
           })
      .def("get_device_pid_by_index",
           [](const std::shared_ptr<ob::DeviceList> &self, int index) {
             return self->pid(index);
           })
      .def("get_device_vid_by_index",
           [](const std::shared_ptr<ob::DeviceList> &self, int index) {
             return self->vid(index);
           })
      .def("get_device_serial_number_by_index",
           [](const std::shared_ptr<ob::DeviceList> &self,
              int index) -> std::string { return self->serialNumber(index); })
      .def("get_device_uid_by_index",
           [](const std::shared_ptr<ob::DeviceList> &self,
              int index) -> std::string { return self->uid(index); })
      .def("get_device_by_index",
           [](const std::shared_ptr<ob::DeviceList> &self, int index) {
             OB_TRY_CATCH({ return self->getDevice(index); });
           })
      .def("get_device_by_serial_number",
           [](const std::shared_ptr<ob::DeviceList> &self,
              const std::string &serial_number) {
             OB_TRY_CATCH(
                 { return self->getDeviceBySN(serial_number.c_str()); });
           })
      .def("get_device_by_uid",
           [](const std::shared_ptr<ob::DeviceList> &self,
              const std::string &uid) {
             OB_TRY_CATCH({ return self->getDeviceByUid(uid.c_str()); });
           })
      .def("__len__", [](const std::shared_ptr<ob::DeviceList> &self) {
        return self->deviceCount();
      });
}
}  // namespace pyorbbecsdk
