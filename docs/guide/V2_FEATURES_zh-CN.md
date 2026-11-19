
[English](V2_FEATURES.md) | **中文**

<a id="v2-new-features"></a>

# V2 新功能

本文介绍 **v2-main** 分支（SDK v2.x 系列）引入的新功能、能力和架构演进。

---

<a id="overview"></a>

## 概览

v2-main 分支面向 **Orbbec SDK v2.7.6+** 全面重写 Python 绑定。该 SDK 相较 v1.x 也进行了重大架构演进：主要区别是 SDK v2.x 对较新设备使用 UVC 协议，而 v1.x 使用专有的 OpenNI 协议。

> v1.x 更新日志请参阅 [main 分支](https://github.com/orbbec/pyorbbecsdk/tree/main)。

<a id="dependencies"></a>

### 依赖

- 需要 **Orbbec SDK v2.7.6** 或更高版本（预编译库位于 `sdk/lib/`）。
- pybind11 2.12.0（在 `pyproject.toml` 中固定版本，以兼容 NumPy 2.x）。

<a id="added"></a>

### 新增功能

<a id="core-api-classes"></a>

#### 核心 API 类

- `Context` — SDK 入口；设备枚举和生命周期管理。
- `Pipeline` / `Config` — 流配置和帧采集循环。
- `Device` / `DeviceList` / `DeviceInfo` — 设备标识、固件信息和属性访问。
- `Sensor` / `SensorList` — 传感器枚举（深度、彩色、IR、IMU 等）。
- `StreamProfile` / `VideoStreamProfile` / `AccelStreamProfile` / `GyroStreamProfile` — 流分辨率、FPS 和格式配置。

<a id="frame-types"></a>

#### 帧类型

- `Frame`, `VideoFrame` — 帧基类，提供时间戳、元数据和数据缓冲区访问。
- `DepthFrame` — 带比例系数的深度数据（将原始 `uint16` 转换为毫米）。
- `ColorFrame` — RGB / MJPEG / Y8 彩色帧。
- `IRFrame` — 红外帧（双目相机支持左、右 IR）。
- `PointsFrame` — 3D 点云数据。
- `AccelFrame` / `GyroFrame` — IMU 加速度计和陀螺仪帧。
- `FrameSet` — 由 `Pipeline.wait_for_frames()` 返回的多流帧容器。

<a id="post-processing-filters"></a>

#### 后处理滤波器

- `AlignFilter` — 软件深度到彩色或彩色到深度对齐。
- `TemporalFilter` — 通过连续帧平均减少深度噪声。
- `SpatialAdvancedFilter` — 保留边缘的空间平滑。
- `HoleFillingFilter` — 使用邻域插值填充无效深度像素。
- `ThresholdFilter` — 将深度值裁剪到指定最小值和最大值之间。
- `DecimationFilter` — 在保留深度有效性的同时降低分辨率。
- `FormatConvertFilter` — 转换帧格式。
- `NoiseRemovalFilter` — 移除孤立的深度噪声像素。
- `PointCloudFilter` — 根据深度和彩色帧生成彩色 3D 点云。
- `HDRMergeFilter` — 合并交替曝光帧，扩展动态范围。
- `SequenceIdFilter` — 选择指定序列的帧（例如 HDR）。

<a id="calibration-and-geometry"></a>

#### 标定与几何

- `OBCameraIntrinsic` — 焦距、主点和图像尺寸。
- `OBCameraDistortion` — 径向和切向畸变系数。
- `OBExtrinsic` — 传感器坐标系之间的旋转矩阵和平移向量。
- `OBCalibrationParam` — 全部传感器的完整标定参数集。
- `CoordinateTransformHelper` — 2D ↔ 3D ↔ 深度 ↔ 彩色坐标变换工具。

<a id="device-features"></a>

#### 设备功能

- IMU 数据流 — 通过 `OBSensorType.ACCEL` / `GYRO` 获取加速度计和陀螺仪数据。
- 多设备支持 — 同时打开多台相机并获取数据流。
- 热插拔检测 — 注册设备连接与断开事件回调。
- 网络相机支持 — 通过以太网连接 Femto Mega 和 Gemini 2 XL。
- HDR 合并 — 高动态范围深度（Gemini 330 系列）。
- 硬件 D2C 对齐 — 在设备端完成深度到彩色对齐。
- 深度工作模式切换 — High Accuracy、High Density 等（部分设备）。
- 设备预设管理 — 加载、保存命名深度预设（Gemini 330 系列）。
- 设备固件升级 — 通过 `device_firmware_update.py` 执行 OTA 固件升级。
- 录制与回放 — 将流录制为 bag 文件，并离线回放。

<a id="developer-experience"></a>

#### 开发体验

- 完整类型存根（`stubs/pyorbbecsdk.pyi`，3600 行以上），支持完整 IDE 自动补全。
- 面向 Windows x64、Linux x64/ARM64 和 macOS 的预编译 wheel 包（Python 3.8–3.14）。
- 基础示例系列（`examples/beginner/`）：
  - `01_hello_camera.py` — 设备发现和信息显示。
  - `02_depth_visualization.py` — 使用 OpenCV 色图显示深度流。
  - `03_color_and_depth_aligned.py` — 使用 AlignFilter 的多流示例。
- 进阶示例系列（`examples/advanced/`）：
  - `high_performance_pipeline.py` — 异步回调、有界帧队列和 FPS 计数器。
  - `custom_filter_chain.py` — 支持键盘实时调节的滤波器链。
- 25 个以上独立示例，覆盖 SDK 各项主要功能。
- pytest 测试套件：
  - 设备、控制、数据流、滤波器、标定和性能测试模块。
  - `conftest.py` 提供会话级 fixture 和自动硬件跳过机制。
  - 通过 `test/generate_report.py` 生成 HTML 报告。

<a id="supported-platforms"></a>

### 支持的平台

| 平台 | 架构 | 操作系统 |
|----------|--------------|----|
| Windows | x64 | Windows 10+ |
| Linux | x64 | Ubuntu 18.04, 20.04, 22.04 |
| Linux | ARM64 | Ubuntu 18.04, 20.04, 22.04 |
| macOS | ARM64（Apple Silicon） | 构建部署目标：macOS 11.0；已在 M2、macOS 13.2 上测试 |

<a id="supported-python-versions"></a>

### 支持的 Python 版本

Python 3.8, 3.9, 3.10, 3.11, 3.12, 3.13, 3.14

<a id="supported-devices"></a>

### 支持的设备

请参阅 README.md 中的[设备支持说明](../../README_zh-CN.md#支持的设备)。

v2-main 支持的主要设备系列：

- **Gemini 435Le**
- **Gemini 330 系列**（335、335L、335Le、335Lg、336、336L、330、330L）
- **Gemini 2 系列**（Gemini 2、2L、215、210）
- **Femto 系列**（Femto Bolt、Femto Mega、Femto Mega I）
- **Astra 2**、**Astra Mini Pro/S Pro**
- **Gemini 305**、**Gemini 345**、**Gemini 345Lg**
- **Pulsar SL450**、**Pulsar ME450**
