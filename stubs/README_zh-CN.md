
[English](README.md) | **中文**

<a id="type-stubs-for-pyorbbecsdk"></a>

# pyorbbecsdk 类型存根

此目录包含 pyorbbecsdk 软件包的 Python 类型存根文件（`.pyi`）。

<a id="what-are-pyi-files"></a>

## 什么是 .pyi 文件？

`.pyi` 类型存根文件为 Python 软件包提供类型信息，可用于：

- **IDE 自动补全**：支持 VS Code、PyCharm 等编辑器的智能代码补全。
- **类型检查**：通过 mypy、pyright 等工具执行静态类型分析。
- **文档提示**：为类和函数提供内联文档。

<a id="usage"></a>

## 使用方法

> 💡 **推荐使用虚拟环境**
>
> 本文假定你已使用 Python 虚拟环境。如果尚未配置，请先阅读[虚拟环境指南](https://orbbec.github.io/pyorbbecsdk/zh_CN/source/2_installation/virtual_environment_guide.html)。

<a id="scenario-1-pip-install-recommended"></a>

### 场景一：通过 pip 安装（推荐）

从 PyPI 安装时会自动包含存根：

```bash
pip install --upgrade pyorbbecsdk2
```

**验证：** 安装后，检查存根是否存在：

```bash
# Linux/macOS
python -c "import pyorbbecsdk; import os; print(os.path.dirname(pyorbbecsdk.__file__))"
# Expected output example: /home/user/.local/lib/python3.x/site-packages/pyorbbecsdk

# Windows PowerShell
python -c "import pyorbbecsdk; import os; print(os.path.dirname(pyorbbecsdk.__file__))"
# Expected output example: C:\Users\User\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.x\LocalCache\local-packages\Python3x\site-packages\pyorbbecsdk
```

如果目录中包含 `.pyi` 文件，说明存根已可用，可直接跳到 [IDE 配置](#ide-configuration)。

<a id="scenario-2-source-build"></a>

### 场景二：从源码构建

从源码构建时，需要手动将存根复制到软件包目录。

<a id="step-1-find-your-package-installation-path"></a>

#### 第一步：查找软件包安装路径

运行以下命令，查找 pyorbbecsdk 的安装位置：

**Linux/macOS：**

```bash
python -c "import pyorbbecsdk; import os; print(os.path.dirname(pyorbbecsdk.__file__))"
```

**Windows PowerShell：**

```powershell
python -c "import pyorbbecsdk; import os; print(os.path.dirname(pyorbbecsdk.__file__))"
```

**Windows CMD：**

```cmd
python -c "import pyorbbecsdk; import os; print(os.path.dirname(pyorbbecsdk.__file__))"
```

**输出示例：**

```
/home/user/pyorbbecsdk/build/lib/pyorbbecsdk
```

**注意：** 保存此路径，供下一步使用。

<a id="step-2-copy-stubs-to-the-package-directory"></a>

#### 第二步：将存根复制到软件包目录

进入 pyorbbecsdk 源码目录（本 README 所在仓库），然后运行：

**Linux/macOS：**

```bash
# Replace with your actual path from Step 1
PACKAGE_PATH="/home/user/pyorbbecsdk/build/lib/pyorbbecsdk"
cp stubs/*.pyi "$PACKAGE_PATH/"
```

**Windows PowerShell：**

```powershell
# Replace with your actual path from Step 1
$PackagePath = "C:\Users\User\pyorbbecsdk\build\lib\pyorbbecsdk"
Copy-Item "stubs\*.pyi" "$PackagePath\"
```

**Windows CMD：**

```cmd
:: Replace with your actual path from Step 1
set PACKAGE_PATH=C:\Users\User\pyorbbecsdk\build\lib\pyorbbecsdk
copy stubs\*.pyi "%PACKAGE_PATH%\"
```

<a id="step-3-verify-the-stubs-are-copied"></a>

#### 第三步：确认存根已复制

检查软件包目录中是否已有 `.pyi` 文件：

**Linux/macOS：**

```bash
ls -la "$PACKAGE_PATH/*.pyi"
```

**Windows PowerShell：**

```powershell
Get-ChildItem "$PackagePath\*.pyi"
```

**Windows CMD：**

```cmd
dir "%PACKAGE_PATH%\*.pyi"
```

应能看到 `__init__.pyi` 和 `pyorbbecsdk.pyi`。

<a id="ide-configuration"></a>

## IDE 配置

<a id="vs-code-with-pylance"></a>

### VS Code（使用 Pylance）

如果存根已位于软件包目录，无需额外配置，Pylance 会自动检测。

验证存根是否生效：

```python
from pyorbbecsdk import Context, Pipeline, Config

pipeline = Pipeline()
pipeline.start()  # Try typing: you should see autocomplete suggestions
```

如果自动补全未生效，可尝试重新加载 VS Code：

1. 按 `Ctrl+Shift+P`（macOS 上按 `Cmd+Shift+P`）。
2. 输入 “Developer: Reload Window”。
3. 按回车。

<a id="pycharm"></a>

### PyCharm

PyCharm 应自动检测软件包目录中的存根。

如果未检测到，可将存根目录添加到外部文档路径：

1. 打开 `File` → `Settings`（macOS 上为 `PyCharm` → `Preferences`）。
2. 进入 `Project` → `Python Interpreter`。
3. 点击齿轮图标 → `Show All`。
4. 选择解释器，点击文件夹图标（`Interpreter Paths`）。
5. 添加存根目录路径。

<a id="faq"></a>

## 常见问题

<a id="q-i-copied-the-stubs-but-still-dont-get-code-completion"></a>

### 问：已经复制存根，为何仍没有代码补全？

**答：** 请尝试：

1. **重启 IDE**：多数 IDE 会缓存类型信息，需要重启。
2. **检查存根位置**：确保 `.pyi` 文件与 `__init__.py` 位于同一目录：

   ```bash
   python -c "import pyorbbecsdk; import os; print(os.listdir(os.path.dirname(pyorbbecsdk.__file__)))"
   ```

   输出中应包含 `__init__.py`、`__init__.pyi` 和 `pyorbbecsdk.pyi`。

3. **检查 IDE 设置**：确保启用 Python 语言服务（VS Code 的 Pylance，或 PyCharm 的 Python 插件）。

<a id="q-how-do-i-confirm-the-stubs-path-is-correct"></a>

### 问：如何确认存根路径正确？

**答：** 运行以下 Python 脚本：

```python
import pyorbbecsdk
import os

package_dir = os.path.dirname(pyorbbecsdk.__file__)
print(f"Package directory: {package_dir}")

files = os.listdir(package_dir)
stubs = [f for f in files if f.endswith('.pyi')]
print(f"Stubs found: {stubs}")

if stubs:
    print("✓ Stubs are correctly installed!")
else:
    print("✗ No stubs found. Please copy .pyi files to the directory above.")
```

<a id="q-do-i-need-to-reinstall-stubs-after-rebuilding-the-package"></a>

### 问：重新构建软件包后需要重新安装存根吗？

**答：** 需要。从源码重新构建软件包（如再次运行 `pip install .`）可能改变或清理安装目录，因此应按照[场景二](#scenario-2-source-build)重新复制存根。

<a id="q-are-these-stubs-required-to-run-the-code"></a>

### 问：运行代码必须有这些存根吗？

**答：** 不需要。存根仅用于辅助开发（自动补全和类型检查），没有存根也可以正常运行代码。

<a id="generating-stubs"></a>

## 生成存根

在仓库根目录激活包含新构建模块的环境。存根生成工具会检查已安装的模块，因此 C++ 绑定发生变化后，应先重新构建并安装。

```bash
# Install pybind11-stubgen
pip install pybind11-stubgen

# Generate both package and extension stubs into a separate directory
python -m pybind11_stubgen pyorbbecsdk -o generated_stubs

# Always repair the generated annotations before copying them into the package
python scripts/fix_pyi.py generated_stubs/pyorbbecsdk/pyorbbecsdk.pyi stubs/pyorbbecsdk.pyi
python scripts/fix_pyi.py generated_stubs/pyorbbecsdk/__init__.pyi stubs/__init__.pyi
```

修复脚本支持 Python 3.8+，仅使用标准库，并可重复运行。它会修复 NumPy 数组类型和可写数组属性、数值输入协议、可空返回值、固件回调、序列参数、枚举默认值及绑定特有返回类型。如果已安装 Black 和 isort，脚本会使用它们格式化；修复本身不依赖这两个工具。

运行无需硬件的回归测试：

```bash
python -m unittest discover -s scripts/tests -v
```

<a id="files"></a>

## 文件

- `__init__.pyi`：模块导出和类型定义。
- `pyorbbecsdk.pyi`：全部类和函数的主要类型定义。
