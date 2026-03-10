#!/bin/bash
#
# macOS USB Device Access Runner
# 以管理员权限运行 Python 脚本，解决 macOS USB 设备访问权限问题
#
# 用法:
#   ./run_sudo.sh [选项] <脚本路径> [脚本参数...]
#
# 选项:
#   -p, --python <版本>    指定 Python 版本 (如: 3.10, 3.11, system, 或绝对路径)
#   -h, --help            显示帮助信息
#   --list                列出可用的 Python 版本
#
# 示例:
#   ./run_sudo.sh examples/multi_streams.py
#   ./run_sudo.sh --python 3.11 examples/multi_streams.py
#   ./run_sudo.sh -p /opt/homebrew/bin/python3.10 examples/depth.py
#

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"

# 默认 Python 版本
PYTHON_VERSION=""

# 显示帮助信息
show_help() {
    cat << EOF
macOS USB Device Access Runner
以管理员权限运行 Python 脚本

用法:
    $0 [选项] <脚本路径> [脚本参数...]

选项:
    -p, --python <版本>    指定 Python 版本
                          - 版本号: 3.10, 3.11 等
                          - "system": 使用系统 Python
                          - 绝对路径: /path/to/python
    -h, --help            显示此帮助信息
    --list                列出可用的 Python 版本

示例:
    $0 examples/multi_streams.py
    $0 --python 3.11 examples/multi_streams.py
    $0 -p /opt/homebrew/bin/python3.10 examples/depth.py
    $0 --list

注意:
    运行时会要求输入管理员密码 (sudo)
EOF
}

# 列出可用的 Python 版本
list_pythons() {
    echo "可用的 Python 版本:"
    echo ""

    # 检查常见的 Python 版本
    for ver in 3.8 3.9 3.10 3.11 3.12 3.13; do
        python_path=$(which "python${ver}" 2>/dev/null || true)
        if [ -n "$python_path" ]; then
            echo "  * python${ver} -> ${python_path}"
        fi
    done

    # 检查默认 python3
    python3_path=$(which python3 2>/dev/null || true)
    if [ -n "$python3_path" ]; then
        echo "  * python3 -> ${python3_path}"
    fi

    # 系统自带的 Python
    if [ -x "/usr/bin/python3" ]; then
        echo "  - system -> /usr/bin/python3"
    fi

    echo ""
    echo "提示: 使用 -p 或 --python 指定版本"
}

# 查找 Python 解释器
find_python() {
    local version="$1"

    if [ -z "$version" ]; then
        # 未指定版本，检查虚拟环境或使用默认
        if [ -n "$VIRTUAL_ENV" ] && [ -x "$VIRTUAL_ENV/bin/python" ]; then
            echo "$VIRTUAL_ENV/bin/python"
            return 0
        fi

        # 检查项目目录中的虚拟环境
        for venv_name in venv venv-py310 venv-py311 venv-py39; do
            venv_python="${PROJECT_DIR}/${venv_name}/bin/python"
            if [ -x "$venv_python" ]; then
                echo "$venv_python"
                return 0
            fi
        done

        # 使用系统默认
        echo "python3"
        return 0
    fi

    # 指定了版本
    case "$version" in
        system)
            echo "/usr/bin/python3"
            ;;
        /*)
            # 绝对路径
            if [ -x "$version" ]; then
                echo "$version"
            else
                echo "错误: Python 不存在于 $version" >&2
                return 1
            fi
            ;;
        3.*)
            # 版本号
            python_path=$(which "python${version}" 2>/dev/null || true)
            if [ -n "$python_path" ]; then
                echo "$python_path"
            else
                echo "错误: 未找到 python${version}" >&2
                return 1
            fi
            ;;
        *)
            # 尝试作为命令查找
            python_path=$(which "$version" 2>/dev/null || true)
            if [ -n "$python_path" ]; then
                echo "$python_path"
            else
                echo "错误: 未找到 $version" >&2
                return 1
            fi
            ;;
    esac
}

# 解析参数
PYTHON_PATH=""
SCRIPT_ARGS=()
SCRIPT_FILE=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        -h|--help)
            show_help
            exit 0
            ;;
        --list)
            list_pythons
            exit 0
            ;;
        -p|--python)
            if [ -z "$2" ]; then
                echo "错误: --python 需要指定版本" >&2
                exit 1
            fi
            PYTHON_VERSION="$2"
            shift 2
            ;;
        -*)
            echo "错误: 未知选项 $1" >&2
            echo "运行 '$0 --help' 查看帮助" >&2
            exit 1
            ;;
        *)
            # 第一个非选项参数是脚本文件
            if [ -z "$SCRIPT_FILE" ]; then
                SCRIPT_FILE="$1"
            fi
            SCRIPT_ARGS+=("$1")
            shift
            ;;
    esac
done

# 检查是否指定了脚本
if [ -z "$SCRIPT_FILE" ]; then
    echo "错误: 未指定要运行的 Python 脚本" >&2
    echo "" >&2
    echo "用法: $0 [选项] <脚本路径> [参数...]" >&2
    echo "运行 '$0 --help' 查看帮助" >&2
    exit 1
fi

# 检查脚本文件是否存在
if [ ! -f "$SCRIPT_FILE" ]; then
    echo "错误: 脚本文件不存在: $SCRIPT_FILE" >&2
    exit 1
fi

# 查找 Python
PYTHON_PATH=$(find_python "$PYTHON_VERSION")
if [ $? -ne 0 ]; then
    exit 1
fi

# 显示信息
echo "=========================================="
echo "macOS USB Device Access Runner"
echo "=========================================="
echo "Python:    $PYTHON_PATH"
echo "脚本:      $SCRIPT_FILE"
if [ ${#SCRIPT_ARGS[@]} -gt 1 ]; then
    echo "参数:      ${SCRIPT_ARGS[@]:1}"
fi
echo "=========================================="
echo ""

# 运行脚本
exec sudo -E env \
    PATH="$PATH" \
    VIRTUAL_ENV="$VIRTUAL_ENV" \
    PYTHONPATH="${PROJECT_DIR}/src:${PYTHONPATH:-}" \
    "$PYTHON_PATH" "${SCRIPT_ARGS[@]}"