
[English](binary_device_data.md) | **中文**

<a id="device-binary-data-interfaces"></a>

# 设备二进制数据接口

这些绑定直接暴露 SDK 操作。二进制输入必须是 `bytes`（可通过 `bytes(buffer)` 将 `bytearray` 或 `memoryview` 转换）。嵌入的零字节会保留；输入长度自动推断，读取结果返回拥有独立内存的 Python `bytes`。设备和固件的支持限制以及 SDK 错误仍然适用。

<a id="protocol-request--response"></a>

## 协议请求与响应

```python
# device is an existing Device; command is a valid SDK/device protocol packet.
response = device.send_and_receive_data(command, receive_capacity=4096)
```

应根据实际命令的最大响应长度选择容量；4096 仅为示例。容量必须为正数，且不能超过 `uint32_t` 的范围。结果包含实际返回的字节（SDK 返回零字节时也可能为空）。绑定不负责构造命令、重试或解析协议。

<a id="customer-data"></a>

## 客户数据

```python
original = device.read_customer_data()
# Explicit write: changes the device's customer data.
device.write_customer_data(b"customer\x00data")
readback = device.read_customer_data()
# Restore only when appropriate for your device/application:
device.write_customer_data(original)
```

SDK 文档规定最大长度为 65532 字节。读取长度参数仅用于输出，因此绑定会分配最大容量，而不会先通过空缓冲区查询大小。此 API 访问设备客户存储空间，并非通用文件 API；它可能与设备的扩展 User ID 共用存储。如果必须保留设备现有客户数据，请先评估该用途，再运行此写入示例。

<a id="firmware-bytes"></a>

## 固件字节数据

```python
from pathlib import Path

def on_progress(state, message, percent):
    print(state, message, percent)

# Only use firmware intended for this device. This performs a real upgrade.
firmware = Path("firmware.bin").read_bytes()
device.update_firmware_from_data(firmware, on_progress, async_update=False)
```

`async_update=False` 会等待 SDK 操作返回。默认值为 `True`，与 C++ 一致；异步操作完成前必须保持 `Device` 存活。应根据 SDK 的完成或错误状态判断结果，而不是 Python 方法的返回值。不要在同一设备上启动相互重叠的固件操作。

绑定会在 SDK 回调对象中保留固件字节数据和回调，直到该对象被替换或设备被销毁；调用 Python 时会获取 GIL。回调异常通过 `sys.unraisablehook` 报告，不会沿 SDK 工作线程展开。回调应只报告进度；设备释放或后续升级操作应在回调之外执行。

<a id="verification-after-rebuilding"></a>

## 重新构建后的验证

接口存在性测试不包含任何设备写入或固件升级操作：

```powershell
python -B -m pytest test/test_all_interfaces.py -k 'test_binary_data_methods or test_update_firmware_from_data' -v -p no:cacheprovider
```

此测试仅检查重新构建或安装的扩展是否暴露全部四个方法，不能证明特定设备支持这些方法。硬件验证应使用有效协议数据、适当设备及获准使用的固件。
