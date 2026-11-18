
[English](obsensor_metadata_win10.md) | **中文**

<a id="obsensor_metadata_win10"></a>

# obsensor_metadata_win10

本文介绍如何在 Windows 系统中通过 UVC 协议获取相机元数据。以下流程已在 Windows 10 和 Windows 11 上验证。

<a id="registering-metadata-using-a-script"></a>

## 使用脚本注册元数据

由于 Windows 系统的默认限制，通过 UVC 协议获取设备元数据前，需要修改注册表并完成注册。

1. 连接设备并确认设备在线。
2. 以管理员身份打开 PowerShell，然后使用 `cd` 命令进入脚本所在目录。
3. 执行 `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`，按提示输入 `Y` 确认。
   - 如果该命令在某些情况下执行失败，可尝试 `Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope CurrentUser`。
4. 执行 `.\obsensor_metadata_win10.ps1 -op install_all` 完成注册。

**注意：** 每次连接新设备时，都需要运行此脚本。这一步容易遗漏，可能导致无法获取设备元数据。
