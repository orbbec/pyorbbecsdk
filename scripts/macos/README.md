# macOS USB 设备访问使用指南

## 问题说明

在 macOS 上使用 pyorbbecsdk 访问 Orbbec 相机时，会出现以下错误：

```
Error: uvc_open failed: [Path: x-x.x-x.x, Return Code: -3]
```

这是因为 macOS 的安全机制要求访问 USB 设备需要 root 权限。

---

## 重要提示：sudo 与虚拟环境

⚠️ **直接使用 `sudo python` 会导致使用系统 Python，而不是虚拟环境的 Python！**

```bash
# ❌ 错误做法
source venv-py310/bin/activate
sudo python examples/multi_streams.py  # 这会使用 /usr/bin/python，不是虚拟环境！

# ✅ 正确做法
source venv-py310/bin/activate
sudo -E python examples/multi_streams.py  # -E 保留环境变量

# ✅ 或者使用绝对路径
sudo /path/to/venv/bin/python examples/multi_streams.py
```

---

## 解决方案

### 方式一：使用 run_sudo.sh 脚本（推荐）

脚本会自动处理环境变量和 Python 路径：

```bash
# 使用默认 Python（自动检测虚拟环境）
./scripts/macos/run_sudo.sh examples/multi_streams.py

# 指定 Python 版本
./scripts/macos/run_sudo.sh --python 3.11 examples/multi_streams.py
./scripts/macos/run_sudo.sh -p 3.10 examples/multi_streams.py

# 使用绝对路径
./scripts/macos/run_sudo.sh -p /opt/homebrew/bin/python3.11 examples/multi_streams.py
```

### 方式二：正确使用 sudo + 虚拟环境

```bash
# 激活虚拟环境
source venv-py310/bin/activate

# 方法 A：使用 -E 保留环境变量（推荐）
sudo -E python examples/multi_streams.py

# 方法 B：使用虚拟环境 Python 的绝对路径
sudo $(which python) examples/multi_streams.py

# 方法 C：直接指定路径
sudo ./venv-py310/bin/python examples/multi_streams.py
```

### 方式三：指定 Python 版本运行

```bash
# 使用 Python 3.10
./scripts/macos/run_sudo.sh --python 3.10 examples/multi_streams.py

# 使用 Python 3.11
./scripts/macos/run_sudo.sh --python 3.11 examples/multi_streams.py

# 使用系统 Python
./scripts/macos/run_sudo.sh --python system examples/multi_streams.py
```

---

## 命令参数详解

```bash
./scripts/macos/run_sudo.sh [选项] <脚本路径> [脚本参数...]
```

| 选项 | 说明 | 示例 |
|------|------|------|
| `-p, --python <版本>` | 指定 Python 版本 | `--python 3.11` |
| `-h, --help` | 显示帮助信息 | `--help` |
| `--list` | 列出可用的 Python 版本 | `--list` |

### Python 版本指定方式

| 指定方式 | 说明 |
|----------|------|
| `3.10` | 使用 `python3.10`（从 PATH 查找） |
| `3.11` | 使用 `python3.11`（从 PATH 查找） |
| `system` | 使用系统自带 Python |
| `/完整/路径/python3.x` | 使用指定路径的 Python |

---

## 查看可用的 Python 版本

```bash
./scripts/macos/run_sudo.sh --list
```

输出示例：
```
可用的 Python 版本:
  * python3.10 -> /opt/homebrew/bin/python3.10
  * python3.11 -> /opt/homebrew/bin/python3.11
  - system -> /usr/bin/python3
```

---

## 完整示例

### 示例 1：使用 Python 3.11 运行

```bash
cd /Users/gongye/gongye/pythonWrapper/python-github/pyorbbecsdk

# 查看可用版本
./scripts/macos/run_sudo.sh --list

# 使用 Python 3.11 运行
./scripts/macos/run_sudo.sh --python 3.11 examples/multi_streams.py
```

### 示例 2：使用虚拟环境 + sudo

```bash
# 激活虚拟环境
source venv-py310/bin/activate

# 验证 Python 路径
which python
# 输出: /Users/.../venv-py310/bin/python

# 使用 -E 保留环境变量
sudo -E python examples/multi_streams.py
```

### 示例 3：传递参数给脚本

```bash
./scripts/macos/run_sudo.sh --python 3.10 examples/depth_viewer.py --resolution 640x480
```

---

## sudo 环境变量说明

| 方式 | PATH 变量 | 虚拟环境 | 推荐度 |
|------|-----------|----------|--------|
| `sudo python` | 系统默认 | ❌ 不生效 | ❌ |
| `sudo -E python` | 保留用户环境 | ✅ 生效 | ✅ |
| `sudo $(which python)` | 使用绝对路径 | ✅ 生效 | ✅ |
| `./run_sudo.sh` | 脚本自动处理 | ✅ 生效 | ✅✅ |

---

## 常见问题

### Q: 为什么 `sudo python` 找不到 pyorbbecsdk？

因为 sudo 重置了 PATH，使用了系统 Python，没有安装 pyorbbecsdk。

**解决方法**：
```bash
sudo -E python your_script.py
```

### Q: 提示 "Python not found"

1. 检查 Python 是否已安装：`which python3.10`
2. 使用 `--list` 查看可用版本
3. 使用绝对路径指定 Python

### Q: 每次都要输入密码？

是的，macOS 访问 USB 设备需要 root 权限。

### Q: 如何在 IDE 中使用？

**VSCode launch.json:**
```json
{
    "name": "Python: Current File (sudo)",
    "type": "python",
    "request": "launch",
    "program": "${file}",
    "console": "integratedTerminal",
    "sudo": true
}
```

---

## 快速参考

```bash
# 查看帮助
./scripts/macos/run_sudo.sh --help

# 查看可用 Python
./scripts/macos/run_sudo.sh --list

# 使用 Python 3.10
./scripts/macos/run_sudo.sh -p 3.10 examples/multi_streams.py

# 使用虚拟环境（正确方式）
source venv-py310/bin/activate
sudo -E python examples/multi_streams.py
```