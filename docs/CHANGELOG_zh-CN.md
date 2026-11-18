
[English](CHANGELOG.md) | **中文**

<a id="changelog"></a>

# 更新日志

本文件记录本项目的所有重要变更。

格式参考 [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)。

<a id="213---2026-10-30"></a>

## [2.1.3] - 2026-10-30

<a id="whats-changed"></a>

### 变更内容
- 将 Orbbec SDK 更新至 v2.10.6.
- 新增 GVCP 网络设备 Action Command 支持，以及 `GROUP_ACTIONS` 多设备同步模式。
- 新增带版本的深度工作模式预设，可通过版本区分同名预设。
- 新增固件心跳和固件日志轮询间隔配置。
- 新增 AWB 状态及增益属性、`OBAwbGainParams` 结构体和 Action Signal 属性集。
- 新增 Python 3.14 构建与打包支持。
- 在 `auto_tests` 下新增 C++ 测试套件的 pytest 移植版本。
- 修复多流示例中的深度闪烁。
- 将 Orbbec SDK 许可证（`sdk/LICENSE.txt`）和全部第三方许可证文件包含到 wheel 包中。
- 改进文档和 API 参考。

<a id="key-new-apis"></a>

## 主要新增 API

面向 GVCP 网络设备的 **Action Command**（多机触发）：
  - `Context.send_action_command(device_key, group_key, group_mask, dest_ip="255.255.255.255", scheduled_time=0)`
  - `OBMultiDeviceSyncMode.GROUP_ACTIONS`
  - Action Signal 属性： `OB_PROP_ACTION_SIGNAL_COUNT_INT` (296), `OB_PROP_ACTION_DEVICE_KEY_INT` (297),
  `OB_PROP_ACTION_SCHEDULED_COMMAND_QUEUE_SIZE_INT` (298), `OB_PROP_ACTION_SELECTOR_INT` (299),
  `OB_PROP_ACTION_GROUP_KEY_INT` (300), `OB_PROP_ACTION_GROUP_MASK_INT` (301)

  **带版本的深度工作模式预设**：
  - `Device.get_current_preset_depth_work_mode_version()`, `DevicePresetList.get_depth_work_mode_version(index)` —
  返回版本字符串（如 `"1.2.3"`）；设备不支持带版本模式时返回空字符串。
  - `Device.load_preset(preset_name, version)` — `load_preset(preset_name)` 的重载，用于加载指定版本。

  **固件监控轮询间隔**：
  - `Device.set_monitor_poll_interval(interval_ms)`, `Device.get_monitor_poll_interval()` — 心跳和固件日志轮询间隔，单位为毫秒；默认 3000 ms，有效范围为 [1000, 10000]，超出范围的值会被限制到边界。

  **彩色 AE / AWB**：
  - `OBAwbGainParams` (`r_gain`, `g_gain`, `b_gain`), `OB_STRUCT_COLOR_AWB_GAIN` (1097)
  - `OB_PROP_COLOR_AE_AWB_STATUS_INT` (287)，别名为 `OB_PROP_COLOR_AE_AWB_STAT_INT`
  - `OB_PROP_COLOR_WB_CTRL_INT` (2053)

  **Python 3.14**:
  - 为 Windows x64、Linux x64/ARM64 和 macOS（Apple Silicon）上的 Python 3.8–3.14 提供预编译 wheel 包。
  - Python 3.14 使用 `pygame-ce` 和最新版 `av`；`open3d` 仅在 Python 3.8–3.11 上安装。

<a id="212---2026-08-11"></a>

## [2.1.2] - 2026-08-11

<a id="whats-changed-1"></a>

### 变更内容
- 将 Orbbec SDK 更新至 v2.10.6.
- 新增 GVCP 网络设备 Action Command 支持，以及 `GROUP_ACTIONS` 多设备同步模式。
- 新增带版本的深度工作模式预设，可通过版本区分同名预设。
- 新增固件心跳和固件日志轮询间隔配置。
- 新增 AWB 状态及增益属性、`OBAwbGainParams` 结构体和 Action Signal 属性集。
- 新增 Python 3.14 构建与打包支持。
- 在 `auto_tests` 下新增 C++ 测试套件的 pytest 移植版本。
- 修复多流示例中的深度闪烁。
- 将 Orbbec SDK 许可证（`sdk/LICENSE.txt`）和全部第三方许可证文件包含到 wheel 包中。
- 改进文档和 API 参考。

<a id="key-new-apis-1"></a>

## 主要新增 API

面向 GVCP 网络设备的 **Action Command**（多机触发）：
  - `Context.send_action_command(device_key, group_key, group_mask, dest_ip="255.255.255.255", scheduled_time=0)`
  - `OBMultiDeviceSyncMode.GROUP_ACTIONS`
  - Action Signal 属性： `OB_PROP_ACTION_SIGNAL_COUNT_INT` (296), `OB_PROP_ACTION_DEVICE_KEY_INT` (297),
  `OB_PROP_ACTION_SCHEDULED_COMMAND_QUEUE_SIZE_INT` (298), `OB_PROP_ACTION_SELECTOR_INT` (299),
  `OB_PROP_ACTION_GROUP_KEY_INT` (300), `OB_PROP_ACTION_GROUP_MASK_INT` (301)

  **带版本的深度工作模式预设**：
  - `Device.get_current_preset_depth_work_mode_version()`, `DevicePresetList.get_depth_work_mode_version(index)` —
  返回版本字符串（如 `"1.2.3"`）；设备不支持带版本模式时返回空字符串。
  - `Device.load_preset(preset_name, version)` — `load_preset(preset_name)` 的重载，用于加载指定版本。

  **固件监控轮询间隔**：
  - `Device.set_monitor_poll_interval(interval_ms)`, `Device.get_monitor_poll_interval()` — 心跳和固件日志轮询间隔，单位为毫秒；默认 3000 ms，有效范围为 [1000, 10000]，超出范围的值会被限制到边界。

  **彩色 AE / AWB**：
  - `OBAwbGainParams` (`r_gain`, `g_gain`, `b_gain`), `OB_STRUCT_COLOR_AWB_GAIN` (1097)
  - `OB_PROP_COLOR_AE_AWB_STATUS_INT` (287)，别名为 `OB_PROP_COLOR_AE_AWB_STAT_INT`
  - `OB_PROP_COLOR_WB_CTRL_INT` (2053)

  **Python 3.14**:
  - 为 Windows x64、Linux x64/ARM64 和 macOS（Apple Silicon）上的 Python 3.8–3.14 提供预编译 wheel 包。
  - Python 3.14 使用 `pygame-ce` 和最新版 `av`；`open3d` 仅在 Python 3.8–3.11 上安装。

<a id="212---2026-08-11-1"></a>

## [2.1.2] - 2026-08-11

<a id="whats-changed-2"></a>

### 变更内容
- 将 Orbbec SDK 更新至 v2.9.3.
- 录制与回放示例新增参数导入、导出支持。
- 新增 ApplicationConfig、新的深度滤波器和扩展设备及上下文接口。
- 改进示例，所有渲染窗口均支持调整大小。
- 改进枚举示例中的传感器配置显示。
- 修复示例渲染宽高比，避免图像变形。

<a id="key-new-apis-2"></a>

## 主要新增 API

面向 Gemini 330 系列设备的 **Application Config**：
  - `ApplicationConfig.is_supported(device)`, `ApplicationConfig.get(device)`, `ApplicationConfig.get_by_preset(device,
  preset_name)`
  - `ApplicationSensorConfig(sensor_type)`, `ApplicationPointCloudConfig()`, `ApplicationHDRMergeConfig()`,
  `ApplicationDevDecimationConfig()`

  **彩色预设**：
  - `Device.is_color_preset_supported()`, `Device.get_current_color_preset_name()`, `Device.switch_color_preset(name)`,
  `Device.get_color_preset_list()`
  - 应用应通过这些 API 查询和切换彩色预设。不建议直接访问 `OB_PROP_COLOR_PRESET_PRIORITY_INT`（ID 255），因为该属性将在未来版本中改为内部属性。

  面向 DaBai 系列设备的**时间戳时钟源和硬件 PPS 时间同步**：
  - `Context.set_timestamp_clock_type(clock_type)`, `Context.sync_device_hardware_pps_time(hardware_pps_time)`,
  `Device.sync_hardware_pps_time(hardware_pps_time)`

  面向 Gemini 335Le 和 Gemini 435Le 的**网络设备 CCP 状态查询**：
  - `DeviceList.query_device_access_state(index)`,
  `DeviceList.query_device_access_state_by_serial_number(serial_number)`

  **固件日志状态查询**：
  - `Device.is_firmware_log_enabled()`

  **新增深度滤波器**：
  - `UnDistortionFilter(stream_type)` — 视频流去畸变滤波器
  - `EnhancedDepthFilter(device, model_path)` — 需要设备激活的深度增强滤波器
  - `SpatialFastFilter(activation_key)`, `SpatialModerateFilter(activation_key)`,
  `FalsePositiveFilter(activation_key)` — 高级降噪滤波器
  - `FilterFactory.create_filter(name)`, `FilterFactory.create_private_filter(name, activation_key)` — 在运行时按名称创建滤波器

  **帧工厂**（`Frame` 的静态方法）：
  - `Frame.create_frame(frame_type, format, data_size)`, `Frame.create_video_frame(...)`,
  - `Frame.create_frame_from_other_frame(...)`, `Frame.create_frame_from_stream_profile(profile)`,
  - `Frame.create_frame_set()`, `Frame.set_frame_device_timestamp_us(frame, timestamp_us)`

<a id="211---2026-05-22"></a>

## [2.1.1] - 2026-05-22

<a id="whats-changed-3"></a>

### 变更内容
- 将 Orbbec SDK 更新至 v2.8.6.
- 新增 Gemini 305g 支持。
- 新增 macOS 平台支持。
- 新增自动化 UV 打包和构建脚本。
- 新增 GitHub Actions CI/CD 工作流。
- 改进项目文档和 API 参考。
- 重构示例并重新组织目录结构。

<a id="2018---2026-02-13"></a>

## [2.0.18] - 2026-02-13

<a id="whats-changed-4"></a>

### 变更内容
- 将 OrbbecSDK 更新至 v2.7.6.
- 新增 Gemini 305 支持。
- 新增 Pulsar ME450 和 Pulsar SL450 LiDAR 设备支持。
- 新增设备控制、录制、回放、置信度和 LiDAR 使用示例。
- 重构并增强多个现有示例。

<a id="2015---2025-10-24"></a>

## [2.0.15] - 2025-10-24

<a id="whats-changed-5"></a>

### 变更内容
- 将 OrbbecSDK 更新至 v2.5.5.
- 新增 laser_interleave.py 和 forceip.py 示例。
- 新增启用设备心跳的 API。
- 新增配置和查询网络设备 IP 地址的 API。
- 新增 numpy>=2.0.0 兼容支持。
- 新增通过 **PyPI** 安装 pyorbbecsdk2 的支持。

<a id="2013---2025-07-11"></a>

## [2.0.13] - 2025-07-11

<a id="whats-changed-6"></a>

### 变更内容
- 将 Orbbec SDK 更新至 v2.4.8.
- 新增 Gemini 435Le 支持。
- 新增使用 YOLOv5 的目标检测示例。
- 新增 Python 3.8 至 Python 3.13 的安装包。
- 确保兼容所有符合 UVC 标准的新款 Orbbec USB 产品。

<a id="2010---2025-04-30"></a>

## [2.0.10] - 2025-04-30

<a id="whats-changed-7"></a>

### 变更内容
- 修复缺陷并进行改进。

<a id="209---2025-02-24"></a>

## [2.0.9] - 2025-02-24

<a id="whats-changed-8"></a>

### 变更内容
- 修复缺陷并进行改进。

<a id="207---2025-01-24"></a>

## [2.0.7] - 2025-01-24

<a id="whats-changed-9"></a>

### 变更内容
- 修复缺陷并进行改进。

<a id="206---2024-12-02"></a>

## [2.0.6] - 2024-12-02

<a id="whats-changed-10"></a>

### 变更内容
- 修复缺陷并进行改进。

<a id="205---2024-11-23"></a>

## [2.0.5] - 2024-11-23

<a id="whats-changed-11"></a>

### 变更内容
- 基于 v2-main 分支的首次发布。
- Python 封装集成开源 Orbbec SDK v2。

<a id="134---2024-11-06"></a>

## [1.3.4] - 2024-11-06

<a id="whats-changed-12"></a>

### 变更内容
- 旧版 v1.x 分支发布。
- Orbbec SDK v1 的 Python 封装。

<a id="133---2024-06-21"></a>

## [1.3.3] - 2024-06-21

<a id="whats-changed-13"></a>

### 变更内容
- 旧版 v1.x 分支发布。
- Orbbec SDK v1 的 Python 封装。

---

**说明：** 开源 [Orbbec SDK v2](https://github.com/orbbec/OrbbecSDK_v2) 的 Python 封装版本号为 v2.x.x，[Orbbec SDK v1](https://github.com/orbbec/OrbbecSDK) 的 Python 封装版本号为 v1.x.x。
