# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [2.1.3] - 2026-10-30

### What's Changed
- Updated Orbbec SDK to v2.10.6.
- Added Action Command support for GVCP network devices, together with the new `GROUP_ACTIONS` multi-device sync mode.
- Added versioned depth work mode presets, so presets sharing the same name can be told apart by version.
- Added configuration of the firmware heartbeat and firmware-log polling interval.
- Added AWB status/gain properties and the `OBAwbGainParams` struct, plus the Action Signal property set.
- Added Python 3.14 build and packaging support.
- Added a pytest port of the C++ test suite under `auto_tests`.
- Fixed depth flicker in the multi-stream sample.
- Bundled the Orbbec SDK license (`sdk/LICENSE.txt`) and all third-party license files into the wheel.
- Improved documentation and API reference.

## Key New APIs

**Action Command** for GVCP network devices (multi-unit trigger):
  - `Context.send_action_command(device_key, group_key, group_mask, dest_ip="255.255.255.255", scheduled_time=0)`
  - `OBMultiDeviceSyncMode.GROUP_ACTIONS`
  - Action Signal properties: `OB_PROP_ACTION_SIGNAL_COUNT_INT` (296), `OB_PROP_ACTION_DEVICE_KEY_INT` (297),
  `OB_PROP_ACTION_SCHEDULED_COMMAND_QUEUE_SIZE_INT` (298), `OB_PROP_ACTION_SELECTOR_INT` (299),
  `OB_PROP_ACTION_GROUP_KEY_INT` (300), `OB_PROP_ACTION_GROUP_MASK_INT` (301)

  **Versioned depth work mode presets**:
  - `Device.get_current_preset_depth_work_mode_version()`, `DevicePresetList.get_depth_work_mode_version(index)` —
  return the version string (e.g. `"1.2.3"`), or an empty string when the device does not support versioned modes.
  - `Device.load_preset(preset_name, version)` — overload of `load_preset(preset_name)` for loading a specific version.

  **Firmware monitor polling interval**:
  - `Device.set_monitor_poll_interval(interval_ms)`, `Device.get_monitor_poll_interval()` — heartbeat and firmware-log
  polling interval in milliseconds; default 3000 ms, valid range [1000, 10000], out-of-range values are clamped.

  **Color AE / AWB**:
  - `OBAwbGainParams` (`r_gain`, `g_gain`, `b_gain`), `OB_STRUCT_COLOR_AWB_GAIN` (1097)
  - `OB_PROP_COLOR_AE_AWB_STATUS_INT` (287), alias `OB_PROP_COLOR_AE_AWB_STAT_INT`
  - `OB_PROP_COLOR_WB_CTRL_INT` (2053)

  **Python 3.14**:
  - Pre-built wheels for Python 3.8–3.14 on Windows x64, Linux x64/ARM64, and macOS (Apple Silicon).
  - On Python 3.14 the package uses `pygame-ce` and the latest `av` release; `open3d` is installed on Python 3.8–3.11 only.

## [2.1.2] - 2026-08-11

### What's Changed
- Updated Orbbec SDK to v2.9.3.
- Added support for importing/exporting parameters in Record & Playback samples.
- Added ApplicationConfig, new depth filters and extended device/context interfaces.
- Improved samples by making all rendering windows resizable.
- Improved sensor configuration display in Enumeration samples.
- Fixed rendering aspect ratio in samples to prevent image distortion.

## Key New APIs

**Application Config** for Gemini 330 series devices:
  - `ApplicationConfig.is_supported(device)`, `ApplicationConfig.get(device)`, `ApplicationConfig.get_by_preset(device,
  preset_name)`
  - `ApplicationSensorConfig(sensor_type)`, `ApplicationPointCloudConfig()`, `ApplicationHDRMergeConfig()`,
  `ApplicationDevDecimationConfig()`

  **Color Preset**:
  - `Device.is_color_preset_supported()`, `Device.get_current_color_preset_name()`, `Device.switch_color_preset(name)`,
  `Device.get_color_preset_list()`
  - Applications should use these APIs to query and switch Color Presets. Direct access to
  `OB_PROP_COLOR_PRESET_PRIORITY_INT` (ID 255) is not recommended because the property will become internal in a future
  release.

  **Timestamp clock source and hardware PPS time synchronization** for DaBai series devices:
  - `Context.set_timestamp_clock_type(clock_type)`, `Context.sync_device_hardware_pps_time(hardware_pps_time)`,
  `Device.sync_hardware_pps_time(hardware_pps_time)`

  **Network-device CCP state queries** for Gemini 335Le and Gemini 435Le:
  - `DeviceList.query_device_access_state(index)`,
  `DeviceList.query_device_access_state_by_serial_number(serial_number)`

  **Firmware-log state queries**:
  - `Device.is_firmware_log_enabled()`

  **New depth filters**:
  - `UnDistortionFilter(stream_type)` — undistortion filter for video streams
  - `EnhancedDepthFilter(device, model_path)` — depth enhancement filter requiring device activation
  - `SpatialFastFilter(activation_key)`, `SpatialModerateFilter(activation_key)`,
  `FalsePositiveFilter(activation_key)` — advanced noise removal filters
  - `FilterFactory.create_filter(name)`, `FilterFactory.create_private_filter(name, activation_key)` — create filters
  by name at runtime

  **Frame factory** (static methods on `Frame`):
  - `Frame.create_frame(frame_type, format, data_size)`, `Frame.create_video_frame(...)`,
  - `Frame.create_frame_from_other_frame(...)`, `Frame.create_frame_from_stream_profile(profile)`, 
  - `Frame.create_frame_set()`, `Frame.set_frame_device_timestamp_us(frame, timestamp_us)`

## [2.1.1] - 2026-05-22

### What's Changed
- Updated Orbbec SDK to v2.8.6.
- Added support for Gemini 305g.
- Added macOS platform support.
- Added automated UV packaging and build scripts.
- Added GitHub Actions CI/CD workflows.
- Improved project documentation and API reference.  
- Refactored samples and reorganized directory structure.  

## [2.0.18] - 2026-02-13

### What's Changed
- Updated OrbbecSDK to v2.7.6.
- Added support for Gemini 305.
- Added support for Pulsar ME450 and Pulsar SL450 LiDAR devices.
- Added several new samples for device control, recording, playback, confidence, and LiDAR usage.
- Refactored and enhanced several existing samples.

## [2.0.15] - 2025-10-24

### What's Changed
- Updated OrbbecSDK to v2.5.5.
- Added samples for laser_interleave.py and forceip.py.
- Added an API to enable device heartbeat.
- Added an API to configure and query network device IP addresses.
- Added compatibility with numpy>=2.0.0.
- Added support for installing pyorbbecsdk2 via **PyPI**.

## [2.0.13] - 2025-07-11

### What's Changed
- Updated Orbbec SDK to v2.4.8.
- Added support for Gemini 435Le.
- Added object detect sample using YOLOv5.
- Added installation packages for Python 3.8 version to Python 3.13 version.
- Ensured compatibility with all new Orbbec USB products that comply with the UVC standard.

## [2.0.10] - 2025-04-30

### What's Changed
- Bug fixes and improvements.

## [2.0.9] - 2025-02-24

### What's Changed
- Bug fixes and improvements.

## [2.0.7] - 2025-01-24

### What's Changed
- Bug fixes and improvements.

## [2.0.6] - 2024-12-02

### What's Changed
- Bug fixes and improvements.

## [2.0.5] - 2024-11-23

### What's Changed
- Initial releases based on v2-main branch.
- Python wrapper integrated with open-source Orbbec SDK v2.

## [1.3.4] - 2024-11-06

### What's Changed
- Legacy v1.x branch releases.
- Python wrapper for Orbbec SDK v1.

## [1.3.3] - 2024-06-21

### What's Changed
- Legacy v1.x branch releases.
- Python wrapper for Orbbec SDK v1.

---

**Note:** The Python wrapper for the open-source [Orbbec SDK v2](https://github.com/orbbec/OrbbecSDK_v2) is versioned as v2.x.x, while the Python wrapper for the [Orbbec SDK v1](https://github.com/orbbec/OrbbecSDK) is versioned as v1.x.x.
