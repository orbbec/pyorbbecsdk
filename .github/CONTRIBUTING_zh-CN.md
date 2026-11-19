
[English](CONTRIBUTING.md) | **中文**

<a id="contributing-to-pyorbbecsdk"></a>

# 参与 pyorbbecsdk 贡献

感谢关注并参与贡献！欢迎修复缺陷、添加功能、改进文档或报告问题。

提交修改前请阅读本指南，并遵守[行为准则](CODE_OF_CONDUCT_zh-CN.md)。

---

<a id="table-of-contents"></a>

## 目录

- [开发前置条件](#development-prerequisites)
- [获取源码](#getting-the-source-code)
- [从源码构建](#building-from-source)
- [环境配置](#environment-setup)
- [运行测试套件](#running-the-test-suite)
- [代码风格](#code-style)
- [提交修改](#submitting-changes)
- [报告问题](#reporting-issues)

---

<a id="development-prerequisites"></a>

## 开发前置条件

<a id="required-tools"></a>

### 必需工具

| 工具 | 最低版本 | 说明 |
|------|----------------|-------|
| CMake | 3.15 | |
| Python | 3.8+ | 运行完整测试套件推荐使用 3.10 |
| pybind11 | 2.12.0 | 兼容 numpy 2.x 所必需。通过 pip 安装：`pip install pybind11==2.12.0 pybind11-global==2.12.0` |
| C++ 编译器 | 支持 C++14 | 参阅下方编译器要求 |
| Git | 近期版本 | |

<a id="compiler-requirements"></a>

### 编译器要求

- **Windows：** Visual Studio 2019 或更新版本（MSVC 14.x+）。
- **Linux / macOS：** GCC 7+ 或 Clang 6+。

<a id="runtime-dependencies"></a>

### 运行依赖

基础 SDK：

```bash
python -m pip install --upgrade pyorbbecsdk2
```

运行示例时安装可选示例依赖：

```bash
python -m pip install --upgrade "pyorbbecsdk2[examples]"
```

运行目标检测示例还需要：

```bash
pip install onnxruntime
```

> **NumPy 兼容性说明：**
>
> 基础包仅声明 `numpy`，没有指定版本范围。可选的 `[examples]` 依赖根据 Python 版本设置以下 NumPy 约束，以兼容 Open3D 等示例依赖：
> - **Python 3.8-3.11**：使用 `numpy<2.0.0`。
> - **Python 3.12+**：使用 `numpy>=2.1.0`。
>
> 这些版本范围仅在安装 `[examples]` 时生效；使用 Python 3.12+ 本身并不意味着基础 SDK 必须使用 NumPy 2.x。Open3D 仅在 Python 3.8–3.11 上安装，可选依赖组选用 `open3d==0.18.0`。
>
> 构建兼容 NumPy 2.x 的绑定需要 pybind11>=2.12.0；本项目的构建配置固定使用 pybind11 2.12.0。

---

<a id="getting-the-source-code"></a>

## 获取源码

1. 在 GitHub 上 **Fork** 仓库。
2. **克隆**你的 fork：

   ```bash
   git clone https://github.com/<your-username>/pyorbbecsdk.git
   cd pyorbbecsdk
   ```

3. **添加上游远程仓库：**

   ```bash
   git remote add upstream https://github.com/orbbec/pyorbbecsdk.git
   ```

> **分支说明：** 开发在 `v2-main`（SDK v2.x）上进行。`main` 是旧版 v1.x 分支。请始终基于 `v2-main` 开发。

---

<a id="building-from-source"></a>

## 从源码构建

提供两种构建方式：

1. **UV 构建（推荐）**：快速、可复现，并自动管理 Python 版本。
2. **传统 CMake 构建**：手动配置 pip 和虚拟环境。

<a id="option-1-uv-build-recommended"></a>

### 方式一：UV 构建（推荐）

UV 是快速的 Python 包管理器，依赖解析速度可达 pip 的 10–100 倍，支持自动管理 Python 版本，并提供跨平台统一构建脚本。

<a id="prerequisites-for-uv-build"></a>

#### UV 构建前置条件

- **uv**：参阅[官方安装指南](https://docs.astral.sh/uv/getting-started/installation/)。

  ```bash
  # Linux/macOS
  curl -LsSf https://astral.sh/uv/install.sh | sh

  # Windows PowerShell
  powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```

- **CMake** 3.15+ 和平台编译器（与传统构建相同）。

<a id="quick-uv-build"></a>

#### 快速 UV 构建

```bash
# Linux
chmod +x scripts/build_whl/build-whl-uv.sh
./scripts/build_whl/build-whl-uv.sh  # Build for Python 3.10 (default)
./scripts/build_whl/build-whl-uv.sh 3.11  # Build for Python 3.11
./scripts/build_whl/build-whl-uv.sh all   # Build all supported versions (3.8-3.14)

# macOS
chmod +x scripts/build_whl/build-whl-uv-macos.sh
./scripts/build_whl/build-whl-uv-macos.sh

# Windows PowerShell
.\scripts\build_whl\build-whl-uv.ps1
```

wheel 包输出到 `wheel/` 目录。

> 离线构建、脚本选项和故障排查等详细说明，请参阅[使用 UV 构建](https://orbbec.github.io/pyorbbecsdk/zh_CN/source/4_Package/build_with_uv.html)。

---

<a id="option-2-traditional-cmake-build"></a>

### 方式二：传统 CMake 构建

构建分为两个阶段：先通过 CMake 编译 C++ pybind11 绑定，再通过 Python 将结果打包为 wheel。

<a id="stage-1-cmake-build"></a>

#### 第一阶段：CMake 构建

```bash
cmake -S . -B build -DPYBIND11_PYTHON_VERSION=3.12
cmake --build build --config Release
cmake --install build
```

安装后，编译得到的 `.pyd` / `.so` 文件和 Orbbec SDK 原生库位于 `install/lib/`。

<a id="stage-2-python-wheel"></a>

#### 第二阶段：Python wheel 打包

```bash
python setup.py bdist_wheel
```

输出 wheel：`dist/pyorbbecsdk2-2.1.0-*.whl`。

<a id="setting-pythonpath-required-to-run-examples-after-source-build"></a>

#### 设置 PYTHONPATH（源码构建后运行示例所必需）

```bash
# Linux / macOS
source env.sh

# Windows (PowerShell)
$env:PYTHONPATH = "$PWD\install\lib;$env:PYTHONPATH"

# Windows (cmd)
set PYTHONPATH=%CD%\install\lib;%PYTHONPATH%
```

---

<a id="environment-setup"></a>

## 环境配置

打开相机前，Orbbec SDK 需要进行一次系统级配置。连接设备，然后运行：

```bash
# Windows (PowerShell — will auto-request Administrator)
python scripts/env_setup/setup_env.py

# Linux (will auto-request sudo)
python3 scripts/env_setup/setup_env.py
```

脚本会自动检测操作系统并应用对应配置：

- **Windows**：在注册表中注册 UVC 元数据（正确获取时间戳和帧同步所必需）。
- **Linux**：安装 udev 规则以访问 USB 设备。

通过 `--check` 检查配置，或通过 `--uninstall` 移除配置：

```bash
python scripts/env_setup/setup_env.py --check      # verify status
python scripts/env_setup/setup_env.py --uninstall   # remove configuration
```

> **Linux 提示：** 还需将当前用户加入 `plugdev` 组，随后注销并重新登录：
>
> ```bash
> sudo usermod -aG plugdev $USER
> ```

<details>
<summary><strong>手动配置（不使用脚本时）</strong></summary>

**Windows**：注册帧元数据（以管理员身份运行 PowerShell）：

```powershell
cd scripts\env_setup
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\obsensor_metadata_win10.ps1 -op install_all
```

**Linux**：安装 udev 规则：

```bash
cd scripts/env_setup
sudo chmod +x ./install_udev_rules.sh
sudo ./install_udev_rules.sh
sudo udevadm control --reload && sudo udevadm trigger
```

</details>

---

<a id="running-the-test-suite"></a>

## 运行测试套件

<a id="test-markers"></a>

### 测试标记

| 标记 | 含义 |
|--------|---------|
| `hardware` | 需要实体 Orbbec 相机；未连接时自动跳过 |
| `gemini335` | 需要 Gemini 335 |
| `performance` | 长时间基准测试，每项 60 秒以上 |

<a id="common-test-commands"></a>

### 常用测试命令

```bash
# No camera needed (CI-safe)
python -m pytest test/ -m "not hardware" -v

# Core tests (device, controls, calibration) — ~2 min with camera
python -m pytest \
  test/test_gemini335_device.py \
  test/test_gemini335_controls.py \
  test/test_gemini335_calib.py \
  test/test_context.py \
  test/test_device.py -v

# Full Gemini 335 test suite (camera must be connected)
python -m pytest test/test_gemini335_*.py -v

# Skip long performance benchmarks
python -m pytest test/ -m "not performance" -v
```

<a id="generating-html-reports"></a>

### 生成 HTML 报告

```bash
python test/generate_report.py --quick   # quick suite
python test/generate_report.py          # full suite (saved to reports/)
```

> **已知退出行为：** 测试会话结束后，Orbbec SDK 可能打印 `Fatal Python error: Aborted`。这是已知的 SDK 线程清理问题，不表示测试失败；该消息前记录的全部测试结果有效。

---

<a id="code-style"></a>

## 代码风格

<a id="c-code"></a>

### C++ 代码

C++ 代码使用 **clang-format** 的 Google 风格（由 `.clang-format` 配置）。

提交前执行格式化：

```bash
clang-format -i src/pyorbbecsdk/*.cpp src/pyorbbecsdk/*.hpp
```

<a id="python-code"></a>

### Python 代码

Python 代码遵循 **PEP 8**。

修改公共 API（新增或修改 C++ 绑定签名）时，请更新 `stubs/pyorbbecsdk.pyi`，确保 IDE 自动补全准确。

---

<a id="submitting-changes"></a>

## 提交修改

1. 创建分支前先**同步上游**：

   ```bash
   git fetch upstream
   git checkout -b my-feature upstream/v2-main
   ```

2. 按照上述代码风格指南**进行修改**。
3. 新增功能时，在 `test/` 中**添加或更新测试**。
4. **运行测试套件**，至少运行无需硬件的测试：

   ```bash
   python -m pytest test/ -m "not hardware" -v
   ```

5. 向 `orbbec/pyorbbecsdk` 的 `v2-main` 分支**提交 Pull Request**：
   - 完整填写 [PR 模板](PULL_REQUEST_TEMPLATE/zh-CN.md)。
   - 使用 `Fixes #NNN` 或 `Related to #NNN` 关联 issue。
   - 如果修改公共 API，确认已更新 `stubs/pyorbbecsdk.pyi`。

---

<a id="reporting-issues"></a>

## 报告问题

提交 issue 前，请检查：

- [现有 issue 列表](https://github.com/orbbec/pyorbbecsdk/issues)中是否已有相同问题。
- 文档中的 [FAQ / 故障排查](https://orbbec.github.io/pyorbbecsdk/zh_CN/source/7_FAQ/FAQ.html)。
- 设备固件是否满足 [README.md：自动固件升级](../README_zh-CN.md#自动固件升级)要求的最低版本。
- Linux 上是否已安装 udev 规则。
- Windows 上是否已完成元数据注册。

提交新 issue 时，请使用[缺陷报告模板](ISSUE_TEMPLATE/bug_report_zh-CN.md)。
