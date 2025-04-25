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
#include <pybind11/pybind11.h>

#include <iostream>
#include <libobsensor/ObSensor.hpp>
#include <string>

#include "context.hpp"
#include "device.hpp"
#include "error.hpp"
#include "filter.hpp"
#include "frame.hpp"
#include "pipeline.hpp"
#include "properties.hpp"
#include "record_playback.hpp"
#include "sensor.hpp"
#include "stream_profile.hpp"
#include "types.hpp"
#include "utils.hpp"

#if defined(__linux__) || defined(__APPLE__)
#include <dlfcn.h>
#endif

#ifdef _WIN32
#include <windows.h>
#endif

#include <cstring>
#include <iostream>
#include <string>
// #include <Python.h>

namespace py = pybind11;
namespace pyorbbecsdk2 = pyorbbecsdk;

std::string get_site_packages_path() {
  Py_Initialize();  // Initialize the Python interpreter

  // Get the site module, which provides the correct user-specific site-packages
  // path
  PyObject *site = PyImport_ImportModule("site");
  if (!site) {
    PyErr_Print();
    return "";
  }

  // Call site.getsitepackages() to get the list of site-packages paths
  PyObject *getsitepackages_func =
      PyObject_GetAttrString(site, "getsitepackages");
  if (!getsitepackages_func || !PyCallable_Check(getsitepackages_func)) {
    PyErr_Print();
    return "";
  }

  // Call site.getsitepackages() to get all site-packages paths
  PyObject *site_packages = PyObject_CallObject(getsitepackages_func, NULL);
  if (!site_packages) {
    PyErr_Print();
    return "";
  }

  // The result is a list, so extract the first entry (user-specific
  // site-packages)
  if (PyList_Check(site_packages) && PyList_Size(site_packages) > 0) {
    PyObject *path =
        PyList_GetItem(site_packages, 0);  // First entry in the list
    if (path && PyUnicode_Check(path)) {
      std::string site_packages_path = PyUnicode_AsUTF8(path);
      Py_Finalize();
      return site_packages_path;
    }
  }

  Py_Finalize();
  return "";
}

std::string get_extensions_path() {
  std::string library_path;

#if defined(__linux__) || defined(__APPLE__)

  // std::string site_packages_path = get_site_packages_path();

  Dl_info dl_info;

  // if (!site_packages_path.empty()) {
  //     std::cout << "Found python site-packages path: " << site_packages_path
  //     << std::endl;
  // }

  // pass the address of ob_create_context function to dladdr
  if (dladdr(reinterpret_cast<void *>(&ob_create_context), &dl_info)) {
    if (dl_info.dli_fname) {
      library_path = std::string(dl_info.dli_fname);
    } else {
      std::cerr << "Failed to get library filename using dladdr" << std::endl;
    }
  } else {
    std::cerr << "dladdr failed to retrieve library info" << std::endl;
  }

#endif

#if defined(_WIN32)
  HMODULE hModule = nullptr;

  // Get a handle to the module containing `ob_create_context`
  if (GetModuleHandleEx(GET_MODULE_HANDLE_EX_FLAG_FROM_ADDRESS |
                            GET_MODULE_HANDLE_EX_FLAG_UNCHANGED_REFCOUNT,
                        reinterpret_cast<LPCSTR>(&ob_create_context),
                        &hModule)) {
    char path[MAX_PATH];
    // Get the full path of the module
    if (GetModuleFileNameA(hModule, path, MAX_PATH)) {
      library_path = std::string(path);
    } else {
      std::cerr << "GetModuleFileName failed: " << GetLastError() << std::endl;
    }
  } else {
    std::cerr << "GetModuleHandleEx failed: " << GetLastError() << std::endl;
  }
#endif

  if (!library_path.empty()) {
    // Find the last directory separator
    size_t pos = library_path.find_last_of("/\\");
    if (pos != std::string::npos) {
      // Extract the directory path
      std::string dir_path = library_path.substr(0, pos);
      // Construct the extensions path
      std::string extensions_path = dir_path + "/extensions";
      return extensions_path;
    }
  }

  // Return a default path if unable to get the library path
  return "";
}

PYBIND11_MODULE(pyorbbecsdk, m) {
  m.doc() = "OrbbecSDK python binding";
  // version
  m.def("get_version", []() {
    auto major = ob::Version::getMajor();
    auto minor = ob::Version::getMinor();
    auto patch = ob::Version::getPatch();
    return std::to_string(major) + "." + std::to_string(minor) + "." +
           std::to_string(patch);
  });
  // test set extensions
  auto extensions_path = get_extensions_path();
  if (!extensions_path.empty()) {
    std::cout << "load extensions from " << extensions_path << std::endl;
    ob::Context::setExtensionsDirectory(extensions_path.c_str());
  }
  // context
  pyorbbecsdk::define_orbbec_types(m);
  pyorbbecsdk::define_context(m);

  // device
  pyorbbecsdk::define_device_info(m);
  pyorbbecsdk::define_device_list(m);
  pyorbbecsdk::define_device_preset_list(m);
  pyorbbecsdk::define_depth_work_mode_list(m);
  pyorbbecsdk::define_device(m);
  pyorbbecsdk::define_camera_list(m);

  // error
  pyorbbecsdk::define_orbbec_error(m);

  // filter
  pyorbbecsdk::define_filter(m);
  pyorbbecsdk::define_point_cloud_filter(m);
  pyorbbecsdk::define_format_covert_filter(m);
  pyorbbecsdk::define_hole_filling_filter(m);
  pyorbbecsdk::define_temporal_filter(m);
  pyorbbecsdk::define_spatial_advanced_filter(m);
  pyorbbecsdk::define_disparity_transform(m);
  pyorbbecsdk::define_HDR_merge_filter(m);
  pyorbbecsdk::define_align_filter(m);
  pyorbbecsdk::define_threshold_filter(m);
  pyorbbecsdk::define_sequence_id_filter(m);
  pyorbbecsdk::define_noise_removal_filter(m);
  pyorbbecsdk::define_decimation_filter(m);

  // frame
  pyorbbecsdk::define_frame(m);
  pyorbbecsdk::define_video_frame(m);
  pyorbbecsdk::define_color_frame(m);
  pyorbbecsdk::define_depth_frame(m);
  pyorbbecsdk::define_ir_frame(m);
  pyorbbecsdk::define_points_frame(m);
  pyorbbecsdk::define_frame_set(m);
  pyorbbecsdk::define_accel_frame(m);
  pyorbbecsdk::define_gyro_frame(m);

  // pipeline
  pyorbbecsdk::define_pipeline(m);
  pyorbbecsdk::define_pipeline_config(m);

  // properties
  pyorbbecsdk::define_properties(m);

  // sensor
  pyorbbecsdk::define_sensor(m);
  pyorbbecsdk::define_sensor_list(m);
  pyorbbecsdk::define_filter_list(m);
  // stream_profile
  pyorbbecsdk::define_stream_profile(m);
  pyorbbecsdk::define_video_stream_profile(m);
  pyorbbecsdk::define_accel_stream_profile(m);
  pyorbbecsdk::define_gyro_stream_profile(m);
  pyorbbecsdk::define_stream_profile_list(m);
  pyorbbecsdk::define_coordinate_transform_helper(m);
  pyorbbecsdk::define_point_cloud_helper(m);
  pyorbbecsdk::define_record(m);
  pyorbbecsdk::define_playback(m);
}

// Bind pyorbbecsdk2 to pyorbbecsdk
PYBIND11_MODULE(pyorbbecsdk2, m) {
  m.doc() = "OrbbecSDK python binding";
  // version
  m.def("get_version", []() {
    auto major = ob::Version::getMajor();
    auto minor = ob::Version::getMinor();
    auto patch = ob::Version::getPatch();
    return std::to_string(major) + "." + std::to_string(minor) + "." +
           std::to_string(patch);
  });
  // test set extensions
  auto extensions_path = get_extensions_path();
  if (!extensions_path.empty()) {
    std::cout << "load extensions from " << extensions_path << std::endl;
    ob::Context::setExtensionsDirectory(extensions_path.c_str());
  }
  // context
  pyorbbecsdk::define_orbbec_types(m);
  pyorbbecsdk::define_context(m);

  // device
  pyorbbecsdk::define_device_info(m);
  pyorbbecsdk::define_device_list(m);
  pyorbbecsdk::define_device_preset_list(m);
  pyorbbecsdk::define_depth_work_mode_list(m);
  pyorbbecsdk::define_device(m);
  pyorbbecsdk::define_camera_list(m);

  // error
  pyorbbecsdk::define_orbbec_error(m);

  // filter
  pyorbbecsdk::define_filter(m);
  pyorbbecsdk::define_point_cloud_filter(m);
  pyorbbecsdk::define_format_covert_filter(m);
  pyorbbecsdk::define_hole_filling_filter(m);
  pyorbbecsdk::define_temporal_filter(m);
  pyorbbecsdk::define_spatial_advanced_filter(m);
  pyorbbecsdk::define_disparity_transform(m);
  pyorbbecsdk::define_HDR_merge_filter(m);
  pyorbbecsdk::define_align_filter(m);
  pyorbbecsdk::define_threshold_filter(m);
  pyorbbecsdk::define_sequence_id_filter(m);
  pyorbbecsdk::define_noise_removal_filter(m);
  pyorbbecsdk::define_decimation_filter(m);

  // frame
  pyorbbecsdk::define_frame(m);
  pyorbbecsdk::define_video_frame(m);
  pyorbbecsdk::define_color_frame(m);
  pyorbbecsdk::define_depth_frame(m);
  pyorbbecsdk::define_ir_frame(m);
  pyorbbecsdk::define_points_frame(m);
  pyorbbecsdk::define_frame_set(m);
  pyorbbecsdk::define_accel_frame(m);
  pyorbbecsdk::define_gyro_frame(m);

  // pipeline
  pyorbbecsdk::define_pipeline(m);
  pyorbbecsdk::define_pipeline_config(m);

  // properties
  pyorbbecsdk::define_properties(m);

  // sensor
  pyorbbecsdk::define_sensor(m);
  pyorbbecsdk::define_sensor_list(m);
  pyorbbecsdk::define_filter_list(m);
  // stream_profile
  pyorbbecsdk::define_stream_profile(m);
  pyorbbecsdk::define_video_stream_profile(m);
  pyorbbecsdk::define_accel_stream_profile(m);
  pyorbbecsdk::define_gyro_stream_profile(m);
  pyorbbecsdk::define_stream_profile_list(m);
  pyorbbecsdk::define_coordinate_transform_helper(m);
  pyorbbecsdk::define_point_cloud_helper(m);
  pyorbbecsdk::define_record(m);
  pyorbbecsdk::define_playback(m);
}
