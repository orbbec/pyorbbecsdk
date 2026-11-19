
[English](LOG_CONFIGURATION.md) | **中文**

<a id="log-configuration-guide"></a>

# 日志配置指南

本指南介绍如何配置或禁用 pyorbbecsdk 的 SDK 日志。

<a id="table-of-contents"></a>

## 目录

- [日志级别](#log-levels)
- [通过代码配置](#configuration-via-code)
- [通过 XML 文件配置](#configuration-via-xml-file)
- [示例](#examples)

<a id="log-levels"></a>

## 日志级别

| 值 | 级别 | 说明 |
|:---|:---|:---|
| 0 | DEBUG | 详细调试信息 |
| 1 | INFO | 常规信息（默认） |
| 2 | WARN | 警告信息 |
| 3 | ERROR | 错误信息 |
| 4 | FATAL | 仅记录致命错误 |
| 5 | NONE | 禁用日志 |

<a id="configuration-via-code"></a>

## 通过代码配置

使用 `Context` 类以编程方式配置日志：

```python
from pyorbbecsdk import Context, OBLogLevel

# Set console logger level
Context.set_logger_to_console(OBLogLevel.INFO)

# Set file logger with custom path
Context.set_logger_to_file(OBLogLevel.DEBUG, "/path/to/logs")

# Disable console logging
Context.set_logger_to_console(OBLogLevel.NONE)
```

<a id="configuration-via-xml-file"></a>

## 通过 XML 文件配置

也可以编辑 `OrbbecSDKConfig.xml` 文件来配置日志。

<a id="step-1-locate-the-configuration-file"></a>

### 第一步：定位配置文件

对于通过 pip 安装的软件包：

```bash
pip show pyorbbecsdk2
# Output: Location: /path/to/site-packages
# Full path: /path/to/site-packages/OrbbecSDKConfig.xml
```

<a id="step-2-modify-log-levels"></a>

### 第二步：修改日志级别

打开 XML 文件并找到 `<Log>` 部分：

```xml
<Log>
    <FileLogLevel>5</FileLogLevel>      <!-- Change to 5 to disable file logging -->
    <ConsoleLogLevel>3</ConsoleLogLevel>  <!-- 0=DEBUG, 1=INFO, 2=WARN, 3=ERROR, 4=FATAL, 5=NONE -->
</Log>
```

<a id="example-disable-all-logging"></a>

### 示例：禁用所有日志

```xml
<Log>
    <FileLogLevel>5</FileLogLevel>      <!-- 5 = NONE, disables file logging -->
    <ConsoleLogLevel>5</ConsoleLogLevel>  <!-- 5 = NONE, disables console logging -->
</Log>
```

<a id="examples"></a>

## 示例

完整示例请参阅 [10_logger.py](./10_logger.py)。

<a id="troubleshooting"></a>

## 故障排查

**没有生成日志文件？**

- 确认日志目录存在且具有写入权限。
- 检查 `FileLogLevel` 是否被设为 5（NONE）。

**日志输出过多？**

- 提高日志级别，例如从 DEBUG 调整为 INFO 或 WARN。
- 如果只需要文件日志，将控制台日志设为 NONE。
