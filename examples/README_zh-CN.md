
[English](README.md) | **中文**

<a id="pyorbbecsdk-examples"></a>

# pyorbbecsdk 示例

按难度组织的示例集合，涵盖从连接第一台相机到构建完整深度感知应用的全过程。

> **重要安装变更：** 示例依赖现已改为可选安装。
> `pip install "pyorbbecsdk2"` 仅安装核心 SDK 和 NumPy。
> 运行这些示例前，请执行 `pip install --upgrade "pyorbbecsdk2[examples]"` 安装或更新，即使已经安装 SDK 也需要执行。
> **请用双引号括住整个软件包或 wheel 参数**（包括 `[examples]`），避免 zsh 报出 `no matches found`，并保留路径中的空格。

---

<a id="quick-start-"></a>

## 快速入门

安装示例依赖并连接相机，然后在仓库根目录运行：

```bash
pip install --upgrade "pyorbbecsdk2[examples]"
python examples/quick_start.py
```

程序会立即打开彩色与深度并排显示的查看器，无需额外配置。确认运行成功后，可按照下方**学习路径**继续。

---

<a id="prerequisites"></a>

## 前置条件

1. 安装 pyorbbecsdk：

   ```bash
   pip install "pyorbbecsdk2[examples]"
   ```

   该命令安装 NumPy 和示例使用的可选依赖，并保留此前默认安装使用的依赖版本约束。

2. **一次性系统配置：**

   - **Linux**：通过 udev 规则授予 USB 访问权限：

     ```bash
     cd scripts/env_setup
     sudo chmod +x install_udev_rules.sh && sudo ./install_udev_rules.sh
     sudo udevadm control --reload && sudo udevadm trigger
     ```

   - **Windows**：注册帧元数据（以管理员身份运行 PowerShell）：

     ```powershell
     cd scripts\env_setup
     Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
     .\obsensor_metadata_win10.ps1 -op install_all
     ```

---

<a id="level-1--beginner-"></a>

## 第一级：基础示例 ⭐

九个编号教程，建议**按 01 → 02 → … → 09 的顺序运行**。每个脚本均有详细注释，讲解一个概念，并在前一个教程基础上逐步展开。

| # | 脚本 | 学习内容 | 依赖 |
|---|--------|---------------|--------------|
| 01 | `beginner/01_hello_camera.py` | SDK 日志配置；发现设备；打印名称、固件和序列号；枚举默认流配置；读取深度预设 | 无 |
| 02 | `beginner/02_depth_visualization.py` | 深度流；uint16 转换为 mm；伽马校正；Scharr 梯度 3D 光照；按 **C** 循环切换 8 种色图 | numpy, opencv |
| 03 | `beginner/03_color_and_depth_aligned.py` | 彩色与深度流；软件 `AlignFilter`（默认）或硬件 D2C（`--hw`）；混合叠加；切换方向与透明度 | numpy, opencv |
| 04 | `beginner/04_camera_calibration.py` | 读取 `OBCameraParam`：内参（fx、fy、cx、cy）、畸变系数、深度到彩色外参（R\|t）；构建 OpenCV K 矩阵 | numpy |
| 05 | `beginner/05_point_cloud.py` | 使用 `PointCloudFilter` 和 `AlignFilter` 生成彩色 3D 点云；保存为 `.ply`，供 Open3D / MeshLab 使用 | numpy |
| 06 | `beginner/06_multi_streams.py` | 通过异步回调同时获取彩色、深度、IR、IMU 数据流；动态网格显示 | numpy, opencv |
| 07 | `beginner/07_imu.py` | 启用 ACCEL 和 GYRO；实时读取时间戳、温度与三轴数值 | 无 |
| 08 | `beginner/08_net_device.py` | 连接网络相机；使用 PyAV 解码 H.264 / MJPG；通过 pygame 显示 | av, pygame |
| 09 | `beginner/09_device_firmware_update.py` | 从 `.bin` 文件进行 OTA 固件升级；进度回调；安全升级实践 | 无 |

```bash
# Run any beginner example from the repo root:
python examples/beginner/01_hello_camera.py
python examples/beginner/03_color_and_depth_aligned.py        # software align
python examples/beginner/03_color_and_depth_aligned.py --hw   # hardware D2C
```

---

<a id="level-2--advanced-"></a>

## 第二级：进阶示例 ⭐⭐

每个脚本围绕 SDK 的一项功能进行深入介绍。

<a id="recording--playback"></a>

### 录制与回放

| 脚本 | 说明 | 适用设备 |
|--------|-------------|-------|
| `advanced/01_recorder.py` | 将所有流录制为 `.bag`；默认使用 GUI 预览，也可通过 `--no-gui` 无界面运行；支持暂停与继续 | 全部 |
| `advanced/02_playback.py` | 回放 `.bag` 文件；自动循环；动态多流网格 | 全部 |
| `advanced/03_save_image_to_disk.py` | 采集固定数量的帧并保存为 PNG / 16 位 PNG | 全部 |

<a id="device--system"></a>

### 设备与系统

| 脚本 | 说明 | 适用设备 |
|--------|-------------|-------|
| `advanced/04_enumerate.py` | 交互式列出所有设备、传感器及支持的流配置 | 全部 |
| `advanced/05_hot_plug.py` | 注册回调，检测相机连接与断开事件 | 全部 |
| `advanced/06_control.py` | 枚举所有设备属性（bool/int/float），检查权限并读写属性值 | 全部 |
| `advanced/07_metadata.py` | 读取逐帧元数据：曝光时间、增益、时间戳和传感器温度 | 全部 |

<a id="depth-processing--alignment"></a>

### 深度处理与对齐

| 脚本 | 说明 | 适用设备 |
|--------|-------------|-------|
| `advanced/08_custom_filter_chain.py` | 串联 Temporal、Spatial、HoleFilling、Threshold 滤波器；通过键盘实时调节 | 全部 |
| `advanced/09_post_processing.py` | 完整后处理流程；并排对比原始和滤波结果 | Gemini 330 |
| `advanced/10_hdr.py` | HDR 合并：通过 `HdrMergeFilter` 合并交替曝光帧 | Gemini 330 |
| `advanced/11_preset.py` | 加载命名深度预设（`Default`、`Hand`、`High Accuracy`）；运行时切换 | Gemini 330 |
| `advanced/12_depth_work_mode.py` | 运行时切换深度工作模式（High Accuracy、High Density 等） | Gemini 2 系列 |
| `advanced/13_confidence.py` | 获取深度置信度图；可视化并按像素置信度进行阈值处理 | 部分设备 |

<a id="multi-device--network"></a>

### 多设备与网络

| 脚本 | 说明 | 适用设备 |
|--------|-------------|-------|
| `advanced/14_two_devices_sync.py` | 同时使用两台相机；通过 JSON 配置硬件帧同步 | 全部 |
| `advanced/15_high_performance_pipeline.py` | 异步回调流水线；有界帧队列；测量 FPS 和延迟 | 全部 |
| `advanced/16_coordinate_transform.py` | 使用标定 API 实现 2D↔2D、2D↔3D、3D↔3D、3D↔2D 变换；按 1–4 切换 | 全部 |
| `advanced/17_laser_interleave.py` | 激光交错模式，减少多相机红外干扰 | 部分设备 |
| `advanced/18_forceip.py` | 为网络相机分配静态 IP | Femto Mega, Gemini 2 XL |
| `advanced/19_device_optional_depth_presets_update.py` | 将可选深度预设配置写入设备 | Gemini 330 |

```bash
python examples/advanced/01_recorder.py              # with live preview
python examples/advanced/01_recorder.py --no-gui     # headless, prints FPS
python examples/advanced/08_custom_filter_chain.py
```

---

<a id="level-3--applications-"></a>

## 第三级：应用示例 ⭐⭐⭐

结合多项 SDK 功能的完整应用。

| 脚本 | 说明 | 依赖 |
|--------|-------------|--------------|
| `applications/object_detection.py` | 在对齐后的彩色流上实时执行 YOLO 目标检测；为每个目标叠加深度信息 | onnxruntime, opencv |
| `applications/ruler.py` | **交互式深度测距工具**：在彩色图像上拖动绘制线段，通过反投影计算真实 3D 欧氏距离（mm）；按 **C** 清除 | numpy, opencv |

```bash
python examples/applications/ruler.py
python examples/applications/object_detection.py
```

> **测距原理：** 对于每个端点 (u, v)，应用读取对齐深度值 Z，然后计算 `X = (u−cx)·Z/fx`、`Y = (v−cy)·Z/fy`。距离 = ‖P2 − P1‖₂，单位为 mm。

---

<a id="specialized--lidar-"></a>

## 专项示例：LiDAR ⭐⭐⭐

面向 Orbbec LiDAR 设备，位于 `examples/lidar_examples/`。

| 脚本 | 说明 |
|--------|-------------|
| `lidar_quick_start.py` | 最简 LiDAR 数据流示例，推荐 LiDAR 用户首先运行 |
| `lidar_stream.py` | 持续显示 LiDAR 点云及实时统计信息 |
| `lidar_device_control.py` | 读写 LiDAR 专用属性；启用扫描和 IMU |
| `lidar_record.py` | 将 LiDAR 数据录制为 `.bag` 文件 |
| `lidar_playback.py` | 回放已录制的 LiDAR 数据 |

---

<a id="utilities"></a>

## 工具

| 文件 | 用途 |
|------|---------|
| `utils.py` | 公共辅助工具：`frame_to_bgr_image()`、格式转换和设备类型检查 |
| `requirements.txt` | 示例集合的全部 Python 依赖 |

---

<a id="learning-path"></a>

## 学习路径

```
首次使用？           →  quick_start.py（30 秒获取第一帧）
                       然后依次运行 beginner/01 → 02 → 03 → 04 → 05

了解特定 SDK 功能？  →  按类别选择第二级中的相应脚本

构建应用？           →  applications/ruler.py
                       applications/object_detection.py

多设备 / 同步？      →  advanced/14_two_devices_sync.py
追求高性能？         →  advanced/15_high_performance_pipeline.py

使用 LiDAR？         →  lidar_examples/lidar_quick_start.py
```
