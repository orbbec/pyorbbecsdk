# Log Configuration Guide

This guide explains how to configure or disable SDK logging in pyorbbecsdk.

## Table of Contents

- [Log Levels](#log-levels)
- [Configuration via Code](#configuration-via-code)
- [Configuration via XML File](#configuration-via-xml-file)
- [Examples](#examples)

## Log Levels

| Value | Level | Description |
|:---|:---|:---|
| 0 | DEBUG | Detailed debug information |
| 1 | INFO | General information (default) |
| 2 | WARN | Warning messages |
| 3 | ERROR | Error messages |
| 4 | FATAL | Fatal errors only |
| 5 | NONE | Disables logging |

## Configuration via Code

Use the `Context` class to configure logging programmatically:

```python
from pyorbbecsdk import Context, OBLogLevel

# Set console logger level
Context.set_logger_to_console(OBLogLevel.INFO)

# Set file logger with custom path
Context.set_logger_to_file(OBLogLevel.DEBUG, "/path/to/logs")

# Disable console logging
Context.set_logger_to_console(OBLogLevel.NONE)
```

## Configuration via XML File

You can also configure logging by editing the `OrbbecSDKConfig.xml` file:

### Step 1: Locate the Configuration File

For pip-installed packages:

```bash
pip show pyorbbecsdk2
# Output: Location: /path/to/site-packages
# Full path: /path/to/site-packages/OrbbecSDKConfig.xml
```

### Step 2: Modify Log Levels

Open the XML file and find the `<Log>` section:

```xml
<Log>
    <FileLogLevel>5</FileLogLevel>      <!-- Change to 5 to disable file logging -->
    <ConsoleLogLevel>3</ConsoleLogLevel>  <!-- 0=DEBUG, 1=INFO, 2=WARN, 3=ERROR, 4=FATAL, 5=NONE -->
</Log>
```

### Example: Disable All Logging

```xml
<Log>
    <FileLogLevel>5</FileLogLevel>      <!-- 5 = NONE, disables file logging -->
    <ConsoleLogLevel>5</ConsoleLogLevel>  <!-- 5 = NONE, disables console logging -->
</Log>
```

## Examples

See [10_logger.py](./10_logger.py) for a complete working example.

## Troubleshooting

**Log files not being created?**
- Ensure the log directory exists and has write permissions
- Check that `FileLogLevel` is not set to 5 (NONE)

**Too much log output?**
- Increase the log level (e.g., from DEBUG to INFO or WARN)
- Set console logging to NONE if you only need file logs
