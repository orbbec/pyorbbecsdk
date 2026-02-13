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
      <td style="text-align: center; font-weight: bold;">Gemini 435Le</td>
      <td>Gemini 435Le</td>
      <td>not supported</td>
      <td>recommended for new designs</td>
    </tr>
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
      <td>Astra Mini (S) Pro</td>
      <td>full maintenance</td>
      <td>recommended for new designs</td>
    </tr>
  </tbody>
</table>

**Note**:
- If you do not find your device, please contact our FAE or sales representative for help.
- Starting from October 2025 (Orbbec SDK v2.5.5), we will begin upgrading devices that use the OpenNI protocol to the UVC protocol, Already upgraded devices and future upgrade schedule and how to upgrade from openni protocol to uvc protocol,please refer to [the document](https://github.com/orbbec/OrbbecSDK_v2?tab=readme-ov-file#12-upgrading-from-openni-protocol-to-uvc-protocol).


**Definition**:

1. recommended for new designs: we will provide full supports with new features,  bug fix and performance optimization;
2. full maintenance: we will provide bug fix support;
3. limited maintenance: we will provide critical bug fix support;
4. not supported: we will not support specific device in this version;
5. to be supported: we will add support in the near future.


## Hardware Products Supported by Python SDK

| **Products List** | **Minimal Firmware Version** | **Recommended Firmware Version**    |
|-------------------|------------------------------|-------------------------------|
| Gemini 305        | 1.0.30                       |        1.0.30                       |
| Gemini 345        | 1.7.04                       |        1.9.03                       |
| Gemini 345Lg        | 1.7.04                     |        1.9.03                   |
| Gemini 435Le        | 1.2.4                     |        1.3.6                   |
| Gemini 335Le        | 1.5.31                     |        1.6.00                     |
| Gemini 330        | 1.2.20                       |        1.6.00                       |
| Gemini 330L       | 1.2.20                       |       1.6.00                      |
| Gemini 335        | 1.2.20                       |       1.6.00                        |
| Gemini 335L       | 1.2.20                       |        1.6.00                       |
| Gemini 336        | 1.2.20                       |       1.6.00                        |
| Gemini 336L       | 1.2.20                       |        1.6.00                       |
| Gemini 335Lg      | 1.3.46                       |        1.6.00                       |
| Femto Bolt        | 1.1.2                  |              1.1.3                       |
| Femto Mega        | 1.3.0                  |              1.3.1                       |
| Femto Mega I        | 2.0.4                  |            2.0.4                     |
| Astra 2           | 2.8.20                       |         2.8.20                      |
| Gemini 2 L        | 1.4.53                       |        1.5.2                       |
| Gemini 2          | 1.4.92               |                1.4.98                       |
| Gemini 215        | 1.0.9                        |        1.0.9                      |
| Gemini 210        | 1.0.9                        |        1.0.9                      |
| Astra mini Pro        | 2.0.03                        |        2.0.03                        |
| Astra mini S Pro        | 2.0.03                        |        2.0.03                        |
| Pulsar SL450        | 2.2.4.5                        |        2.2.4.5                        |
| Pulsar ME450        | 1.0.0.6                        |        1.0.0.6                        |

## Supported Platforms

- Windows: Windows 10 (x64)
- Linux: 18.04/20.04/22.04 (x64)
- Arm64: Ubuntu18.04/20.04/22.04

## Supported Python Versions

python 3.8 to python 3.13

## Environment Setup

### Windows

For windows, you need to register the metadata associated with frames (this includes things like timestamps and other information about the video frame).

- Connect the device and confirm that the device is online;
- Open PowerShell with administrator privileges, then use the `cd` command to enter the directory where the `obsensor_metadata_win10.ps1` script is located;
- Execute the `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` command, and enter `Y` as prompted to confirm;

  Try to execute the `Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope CurrentUser` command if the previous command fails in some cases;
- Execute `.\obsensor_metadata_win10.ps1 -op install_all` to complete the registration.


*Notes: If the metadata is not registered, the device timestamp will be abnormal, thereby affecting the SDK's internal frame synchronization functionality.*


### Linux

For Linux, we have provided a script to help you set up the environment. You can run the script as follows:

```bash
  cd pyorbbecsdk/scripts/env_setup
  sudo chmod +x ./install_udev_rules.sh
  sudo ./install_udev_rules.sh
  sudo udevadm control --reload && sudo udevadm trigger
```

*Notes: If this script is not executed, open the device will fail due to permission issues.*

## How to Use install package
To make Python more user-friendly, We provide two installation methods: online installation and offline installation.


### Windows

We provide both online and offline installation packages for Python versions **3.8** to **3.13**.

Follow the [windows install documentation](
https://orbbec.github.io/pyorbbecsdk/source/2_installation/install_the_package.html#windows) to install the SDK online or offline. Then verify the package and run the sample.


### Linux

We provide online installation packages for Python versions **3.9** to **3.13** and provide offline installation packages for Python versions **3.8** to **3.13**.

Follow the [linux install documentation](
https://orbbec.github.io/pyorbbecsdk/source/2_installation/install_the_package.html#linux) to install the SDK online or offline. Then verify the package and run the sample.

## Documentation

[Orbbec SDK V2 Python Wrapper User Guide](https://orbbec.github.io/pyorbbecsdk/index.html) provides an overview of the concepts and architecture of Orbbec SDK v2, details on the Python Wrapper installation packages and source compilation, an introduction to commonly used Python Wrapper interfaces, and a FAQ section. Please read it carefully.


## License
This project is licensed under the Apache License 2.0.

