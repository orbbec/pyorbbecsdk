# Python Bindings for Orbbec SDK

the v2-main branch provides Python bindings for the [Orbbec SDK v2.x](https://github.com/orbbec/OrbbecSDK_v2),  enabling developers to interface with Orbbec devices using Python. The Orbbec SDK v.2.x is an open-source cross-platform SDK library based on Orbbec RGB-D cameras. The differences between Orbbec SDK v2.x and [Orbbec SDK v1.x](https://github.com/orbbec/OrbbecSDK) can be found in the [README](https://github.com/orbbec/OrbbecSDK_v2).

If you are a user in China, it is recommended to use [gitee Repo](https://gitee.com/orbbecdeveloper/pyorbbecsdk).
> [!IMPORTANT]
>
> Welcome to the python wrapper . Before you begin using this version of python wrapper , it's crucial to check the following device support list to verify the compatibility.

Here is the device support list of main branch (v1.x) and v2-main branch (v2.x):

<table border="1" style="border-collapse: collapse; text-align: left; width: 100%;">
  <thead>
    <tr style="background-color: #1f4e78; color: white; text-align: center;">
      <th>Product Series</th>
      <th>Product</th>
      <th><a href="https://github.com/orbbec/pyorbbecsdk/tree/main" style="color: black; text-decoration: none;">Branch main</a></th>
      <th><a href="https://github.com/orbbec/pyorbbecsdk/tree/v2-main" style="color: black; text-decoration: none;">Branch v2-main</a></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td rowspan="8" style="text-align: center; font-weight: bold;">Gemini 330</td>
      <td>Gemini 335Le</td>
      <td>not supported</td>
      <td>recommended for new designs</td>
    </tr>
    <tr>
      <td>Gemini 335</td>
      <td>full maintenance</td>
      <td>recommended for new designs</td>
    </tr>
    <tr>
      <td>Gemini 336</td>
      <td>full maintenance</td>
      <td>recommended for new designs</td>
    </tr>
    <tr>
      <td>Gemini 330</td>
      <td>full maintenance</td>
      <td>recommended for new designs</td>
    </tr>
    <tr>
      <td>Gemini 335L</td>
      <td>full maintenance</td>
      <td>recommended for new designs</td>
    </tr>
    <tr>
      <td>Gemini 336L</td>
      <td>full maintenance</td>
      <td>recommended for new designs</td>
    </tr>
    <tr>
      <td>Gemini 330L</td>
      <td>full maintenance</td>
      <td>recommended for new designs</td>
    </tr>
    <tr>
      <td>Gemini 335Lg</td>
      <td>not supported</td>
      <td>recommended for new designs</td>
    </tr>
    <tr>
      <td rowspan="5" style="text-align: center; font-weight: bold;">Gemini 2</td>
      <td>Gemini 2</td>
      <td>full maintenance</td>
      <td>recommended for new designs</td>
    </tr>
    <tr>
      <td>Gemini 2 L</td>
      <td>full maintenance</td>
      <td>recommended for new designs</td>
    </tr>
    <tr>
      <td>Gemini 2 XL</td>
      <td>recommended for new designs</td>
      <td>to be supported</td>
    </tr>
    <tr>
      <td>Gemini 215</td>
      <td>not supported</td>
      <td>recommended for new designs</td>
    </tr>
    <tr>
      <td>Gemini 210</td>
      <td>not supported</td>
      <td>recommended for new designs</td>
    </tr>
    <tr>
      <td rowspan="3" style="text-align: center; font-weight: bold;">Femto</td>
      <td>Femto Bolt</td>
      <td>full maintenance</td>
      <td>recommended for new designs</td>
    </tr>
    <tr>
      <td>Femto Mega</td>
      <td>full maintenance</td>
      <td>recommended for new designs</td>
    </tr>
    <tr>
      <td>Femto Mega I</td>
      <td>full maintenance</td>
      <td>recommended for new designs</td>
    </tr>
    <tr>
      <td rowspan="3" style="text-align: center; font-weight: bold;">Astra</td>
      <td>Astra 2</td>
      <td>full maintenance</td>
      <td>recommended for new designs</td>
    </tr>
    <tr>
      <td>Astra+</td>
      <td>limited maintenance</td>
      <td>not supported</td>
    </tr>
    <tr>
      <td>Astra Pro Plus</td>
      <td>limited maintenance</td>
      <td>not supported</td>
    </tr>
    <tr>
      <td style="text-align: center; font-weight: bold;">Astra Mini</td>
      <td>Astra Mini Pro</td>
      <td>full maintenance</td>
      <td>not supported</td>
    </tr>
  </tbody>
</table>

**Note**: If you do not find your device, please contact our FAE or sales representative for help.

**Definition**:

1. recommended for new designs: we will provide full supports with new features,  bug fix and performance optimization;
2. full maintenance: we will provide bug fix support;
3. limited maintenance: we will provide critical bug fix support;
4. not supported: we will not support specific device in this version;
5. to be supported: we will add support in the near future.


## Hardware Products Supported by Python SDK

| **Products List** | **Minimal Firmware Version** |
|-------------------|------------------------------|
| Gemini 335Le        | 1.5.31                       |
| Gemini 330        | 1.2.20                       |
| Gemini 330L       | 1.2.20                       |
| Gemini 335        | 1.2.20                       |
| Gemini 335L       | 1.2.20                       |
| Gemini 336        | 1.2.20                       |
| Gemini 336L       | 1.2.20                       |
| Gemini 335Lg      | 1.3.46                       |
| Femto Bolt        | 1.1.2                  |
| Femto Mega        | 1.3.0                  |
| Femto Mega I        | 2.0.4                  |
| Astra 2           | 2.8.20                       |
| Gemini 2 L        | 1.4.53                       |
| Gemini 2          | 1.4.92               |
| Gemini 215        | 1.0.9                        |
| Gemini 210        | 1.0.9                        |


## Supported Platforms

- Windows: Windows 10 (x64)
- Linux: 18.04/20.04/22.04 (x64)
- Arm64: Ubuntu18.04/20.04/22.04
- Linux ARM32: coming soon



## Documentation

Refer to [UserGuide](https://orbbec.github.io/pyorbbecsdk/index.html) for detailed documentation.

## License
This project is licensed under the Apache License 2.0.

