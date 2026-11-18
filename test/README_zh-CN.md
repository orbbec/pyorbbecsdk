
[English](README.md) | **中文**

<a id="pyorbbecsdk-test-suite"></a>

# pyorbbecsdk 测试套件

此目录包含基于 pytest 的 pyorbbecsdk 测试套件，按设备系列和测试类别组织，覆盖设备发现、传感器控制、数据流验证、后处理滤波、标定及性能基准测试。

---

<a id="prerequisites"></a>

## 前置条件

1. **安装 pyorbbecsdk**（或从源码构建，参阅 [CONTRIBUTING.md](../.github/CONTRIBUTING_zh-CN.md#building-from-source)）。
2. **安装测试依赖：**

   ```bash
   pip install -r test/requirements_test.txt
   ```

3. **一次性系统配置（仅硬件测试需要）：**
   - **Linux**：安装 udev 规则，使 SDK 可以访问 USB 设备。

     ```bash
     cd scripts/env_setup && sudo ./install_udev_rules.sh
     sudo udevadm control --reload && sudo udevadm trigger
     ```

   - **Windows**：注册帧元数据（获取时间戳所必需）。

     ```powershell
     # Run PowerShell as Administrator
     cd scripts\env_setup
     .\obsensor_metadata_win10.ps1 -op install_all
     ```

---

<a id="one-click-test-runner"></a>

## 一键测试运行器

`run_tests.py` 会自动检测已连接的相机，并通过一条命令运行对应测试套件。

```bash
# Auto-detect device and run all its tests
python test/run_tests.py

# Specify device family explicitly
python test/run_tests.py --device g300
python test/run_tests.py --device femto
python test/run_tests.py --device astra_mini
python test/run_tests.py --device astra2

# Filter by test category
python test/run_tests.py --category functional
python test/run_tests.py --category stability
python test/run_tests.py --category performance

# Combine filters — G300 functional tests only
python test/run_tests.py --device g300 --category functional

# Skip long performance benchmarks
python test/run_tests.py --quick

# No camera needed
python test/run_tests.py --no-hardware

# Save report to a custom directory
python test/run_tests.py --output my_reports/
```

**`--device` 支持的值：**

| 别名 | 设备系列 |
|-------|---------------|
| `g300`, `gemini`, `gemini335`, `gemini336`, … | G300 系列 |
| `femto`, `femto_bolt`, `femto_mega` | Femto Bolt / Mega |
| `astra_mini`, `astra_mini_pro` | Astra Mini |
| `astra2`, `astra_2` | Astra 2 |

报告保存到 `reports/`，并额外写入一份 `reports/test_report_latest.html`。

---

<a id="running-tests-manually"></a>

## 手动运行测试

所有命令均在**仓库根目录**执行。

<a id="quick-check--no-camera-needed"></a>

### 快速检查：无需相机

```bash
pytest test/ -m "not hardware" -v
```

<a id="run-all-tests-for-a-specific-device-family"></a>

### 运行特定设备系列的全部测试

```bash
# G300 series (Gemini 330 / 335 / 336 / 305 / 345 and variants)
pytest test/test_g300_series_*.py -v

# Femto Bolt / Femto Mega
pytest test/test_femto_*.py -v

# Astra Mini Pro / S Pro
pytest test/test_astra_mini_*.py -v

# Astra 2
pytest test/test_astra2_*.py -v
```

<a id="run-by-device-marker"></a>

### 按设备标记运行

```bash
pytest test/ -m g300_series -v   # G300 series
pytest test/ -m femto       -v   # Femto Bolt/Mega
pytest test/ -m astra_mini  -v   # Astra Mini
pytest test/ -m astra2      -v   # Astra 2
pytest test/ -m hardware    -v   # All hardware tests
```

<a id="run-by-category"></a>

### 按类别运行

```bash
pytest test/ -m functional   -v   # API correctness only
pytest test/ -m stability    -v   # Reliability/sync only
pytest test/ -m performance  -v   # Benchmarks only
```

<a id="combine-device--category"></a>

### 组合设备与类别

```bash
pytest test/ -m "g300_series and functional"  -v
pytest test/ -m "femto and stability"         -v
pytest test/ -m "not performance"             -v   # skip benchmarks
```

<a id="core-tests-only-2-min-with-camera"></a>

### 仅运行核心测试（连接相机时约 2 分钟）

```bash
pytest test/test_g300_series_device.py \
       test/test_g300_series_controls.py \
       test/test_g300_series_calib.py \
       test/test_context.py \
       test/test_device.py -v
```

<a id="full-test-session"></a>

### 运行完整测试

```bash
pytest test/ -v
```

---

<a id="test-markers"></a>

## 测试标记

<a id="device--scope-markers"></a>

### 设备与范围标记

| 标记 | 含义 | 自动跳过条件 |
|--------|---------|---------------------|
| `hardware` | 需要实体 Orbbec 相机 | 未连接设备 |
| `g300_series` | 任意 Gemini 330/335/336/305/345 型号 | 设备系列不匹配 |
| `femto` | Femto Bolt 或 Femto Mega | 设备系列不匹配 |
| `astra_mini` | Astra Mini Pro / S Pro | 设备系列不匹配 |
| `astra2` | Astra 2 | 设备系列不匹配 |

> **提示：** 如果连接了其他系列的相机，设备专属测试会自动跳过并给出明确提示，不会被判定为失败。

<a id="category-markers"></a>

### 类别标记

| 标记 | 含义 | 典型耗时 |
|--------|---------|-----------------|
| `functional` | API 正确性：设备信息、流启动、传感器控制、标定和滤波器 | 数秒 |
| `stability` | 多帧可靠性：时间戳单调性、同步精度和丢帧率 | 10–30 秒 |
| `performance` | 长时间基准测试：FPS、延迟和吞吐量 | 60 秒以上 |

类别标记可与设备标记自由组合：

```bash
pytest test/ -m "g300_series and stability" -v
pytest test/ -m "not performance"           -v
```

---

<a id="test-file-map"></a>

## 测试文件索引

<a id="category-key-f--functional--s--stability--p--performance"></a>

### 类别缩写：`F` = 功能 · `S` = 稳定性 · `P` = 性能

<a id="basic-tests-no-camera-needed"></a>

### 基础测试（无需相机）

| 文件 | 类别 | 测试内容 |
|------|----------|---------------|
| `test_basic_import.py` | F | 模块基本导入和属性 |
| `test_basic_device.py` | F | Context 创建与设备枚举（无需硬件） |
| `test_basic_capture.py` | F | Pipeline 创建和帧采集基础 |

<a id="generic-tests-any-orbbec-camera"></a>

### 通用测试（任意 Orbbec 相机）

| 文件 | 类别 | 测试内容 |
|------|----------|---------------|
| `test_context.py` | F | Context API：设备枚举、日志和回调 |
| `test_device.py` | F | 通用设备信息、传感器列表、深度工作模式和温度 |
| `test_pipeline.py` | F | Pipeline 相机参数 API |

<a id="g300-series-gemini-330--335--336--305--345-variants"></a>

### G300 系列（Gemini 330 / 335 / 336 / 305 / 345 及其变体）

| 文件 | 类别 | 测试内容 |
|------|----------|---------------|
| `test_g300_series_device.py` | F | 设备标识及 G300 全部传感器要求 |
| `test_g300_series_controls.py` | F | 深度、彩色、IR、激光和 HDR 属性读写 |
| `test_g300_series_filters.py` | F | 完整后处理滤波流程 |
| `test_g300_series_calib.py` | F | 内参、畸变和外参正交性 |
| `test_g300_series_streams.py` | F + S | 流有效性、FPS、多流同步和时间戳单调性 |
| `test_g300_series_performance.py` | P | 启动延迟、60 秒 FPS 稳定性、重启时间和吞吐量 |

<a id="femto-bolt--femto-mega"></a>

### Femto Bolt / Femto Mega

| 文件 | 类别 | 测试内容 |
|------|----------|---------------|
| `test_femto_device.py` | F | 设备标识、ToF 传感器（深度、彩色、左/右 IR、IMU） |
| `test_femto_controls.py` | F | 深度、彩色和激光属性读写 |
| `test_femto_calib.py` | F | 内参、畸变和外参正交性 |
| `test_femto_streams.py` | F + S | 深度（ToF 范围 300–8000 mm）、彩色、IR、IMU 和同步 |

<a id="astra-mini-pro--s-pro"></a>

### Astra Mini Pro / S Pro

| 文件 | 类别 | 测试内容 |
|------|----------|---------------|
| `test_astra_mini_device.py` | F | 设备标识、传感器和标定 |
| `test_astra_mini_streams.py` | F + S | 深度（300–8000 mm）、彩色、IR、控制和时间戳 |

<a id="astra-2"></a>

### Astra 2

| 文件 | 类别 | 测试内容 |
|------|----------|---------------|
| `test_astra2_device.py` | F | 设备标识、传感器和深度工作模式 |
| `test_astra2_streams.py` | F + S | 深度（300–10000 mm）、彩色、IR、同步和控制 |

---

<a id="generating-html-test-reports"></a>

## 生成 HTML 测试报告

```bash
# One-click runner (auto-detects device, saves to reports/)
python test/run_tests.py

# Quick suite via generate_report.py (skips performance benchmarks)
python test/generate_report.py --quick

# Full suite via generate_report.py
python test/generate_report.py
```

报告保存到 `reports/test_report_latest.html`。使用任意浏览器打开 HTML 文件即可查看。

---

<a id="known-teardown-behavior"></a>

## 已知的退出行为

测试会话结束后，Orbbec SDK 可能打印：

```
Fatal Python error: Aborted
```

这是 Python 解释器关闭时发生的**已知 SDK 线程清理问题**，并不表示测试失败；此消息之前记录的全部测试结果仍然有效。

---

<a id="device-depth-range-reference"></a>

## 设备深度范围参考

| 设备系列 | 最小深度 | 最大深度 | 传感器类型 |
|---------------|-----------|-----------|-------------|
| G300 系列（330/335/336） | ~20 mm | ~10 000 mm | 结构光 |
| G300 系列（305/345） | ~20 mm | ~10 000 mm | 结构光 |
| Femto Bolt / Mega | 300 mm | 8 000 mm | 飞行时间（ToF） |
| Astra Mini Pro | 300 mm | 8 000 mm | 结构光 |
| Astra 2 | 300 mm | 10 000 mm | 结构光 |

---

<a id="adding-new-device-tests"></a>

## 添加新设备测试

为新的设备系列添加测试：

1. 在 `conftest.py` 中**注册 fixture**：

   ```python
   @pytest.fixture(scope="session")
   def my_device_fixture(device, device_info):
       name = device_info.get_name() or ""
       if "My Device Name" not in name:
           pytest.skip(f"Not My Device, got '{name}'")
       return device
   ```

2. 在 `conftest.py` 中**注册标记**：

   ```python
   config.addinivalue_line("markers", "my_device: test for My Device")
   ```

3. 按照命名规则**创建测试文件**：

   ```
   test_my_device_device.py    # device discovery + sensors       → functional
   test_my_device_streams.py   # stream validation + timestamps   → functional + stability
   test_my_device_controls.py  # property get/set                 → functional
   ```

4. 使用 `hardware`、设备标记和类别标记**标注测试**：

   ```python
   # device + functional tests
   pytestmark = [pytest.mark.hardware, pytest.mark.my_device, pytest.mark.functional]

   # stream tests (functional correctness + stability)
   pytestmark = [pytest.mark.hardware, pytest.mark.my_device,
                 pytest.mark.functional, pytest.mark.stability]
   ```

5. 在 `run_tests.py` 的 `_DEVICE_ALIASES` 和 `_DEVICE_NAME_PATTERNS` 中**注册设备别名**。
