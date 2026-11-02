# Device binary data interfaces

These bindings expose the SDK operations directly. Binary input must be `bytes`
(use `bytes(buffer)` to convert a `bytearray` or `memoryview`). Embedded zero bytes
are preserved; input lengths are inferred, and reads return owned Python `bytes`.
Device/firmware support and SDK errors still apply.

## Protocol request / response

```python
# device is an existing Device; command is a valid SDK/device protocol packet.
response = device.send_and_receive_data(command, receive_capacity=4096)
```

Choose the capacity from the actual command's maximum response size; 4096 is
only an example. Capacity must be positive and fit `uint32_t`. The result contains
the actual returned bytes (which may be empty if the SDK returns zero bytes).
The binding does not build commands, retry, or interpret the protocol.

## Customer data

```python
original = device.read_customer_data()
# Explicit write: changes the device's customer data.
device.write_customer_data(b"customer\x00data")
readback = device.read_customer_data()
# Restore only when appropriate for your device/application:
device.write_customer_data(original)
```

The SDK documents a maximum of 65532 bytes. Its read length is OUT-only;
the binding allocates that maximum, rather than issuing a null-buffer size query.
This API is device customer storage, not a general file API; it may share the
device's extended User ID storage. Do not run this write example on a device
whose existing customer data must be preserved without first reviewing that use.

## Firmware bytes

```python
from pathlib import Path

def on_progress(state, message, percent):
    print(state, message, percent)

# Only use firmware intended for this device. This performs a real upgrade.
firmware = Path("firmware.bin").read_bytes()
device.update_firmware_from_data(firmware, on_progress, async_update=False)
```

`async_update=False` waits for the SDK operation to return. The default is `True`,
matching C++; keep the `Device` alive until the asynchronous operation completes.
The SDK's completion/error states determine the result, not the Python method's
return value. Do not start overlapping firmware operations on the same device.

The binding retains the firmware bytes and callback in the SDK callback object
until it is replaced or the device is destroyed, and acquires the GIL when
calling Python. Callback exceptions are reported through `sys.unraisablehook`
without unwinding through SDK worker threads. Callbacks should only report
progress; perform device disposal or further upgrade operations outside them.

## Verification after rebuilding

No device writes or firmware upgrades are part of the interface-presence test:

```powershell
python -B -m pytest test/test_all_interfaces.py -k 'test_binary_data_methods or test_update_firmware_from_data' -v -p no:cacheprovider
```

This checks the rebuilt/installed extension exposes all four methods; it does
not establish that a particular device supports them. Use valid protocol data,
an appropriate device and approved firmware for hardware validation.
