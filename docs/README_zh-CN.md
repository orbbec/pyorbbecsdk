[English](README.md) | **中文**

# 文档索引

项目说明、安装方法和支持的平台请参阅[项目 README](../README_zh-CN.md)。本索引汇总仓库维护的中英文文档。

## 在线用户指南

- [English](https://orbbec.github.io/pyorbbecsdk/en/index.html)
- [中文](https://orbbec.github.io/pyorbbecsdk/zh_CN/index.html)

## 仓库文档

每份文档顶部均可切换 English / 中文。

| 文档 | English | 中文 |
|---|---|---|
| 行为准则 | [English](../.github/CODE_OF_CONDUCT.md) | [中文](../.github/CODE_OF_CONDUCT_zh-CN.md) |
| 贡献指南 | [English](../.github/CONTRIBUTING.md) | [中文](../.github/CONTRIBUTING_zh-CN.md) |
| 缺陷报告模板 | [English](../.github/ISSUE_TEMPLATE/bug_report.md) | [中文](../.github/ISSUE_TEMPLATE/bug_report_zh-CN.md) |
| 功能建议模板 | [English](../.github/ISSUE_TEMPLATE/feature_request.md) | [中文](../.github/ISSUE_TEMPLATE/feature_request_zh-CN.md) |
| PR 模板 | [English](../.github/PULL_REQUEST_TEMPLATE.md) | [中文](../.github/PULL_REQUEST_TEMPLATE/zh-CN.md) |
| SDK 配置说明 | [English](../config/OrbbecSDKConfig.md) | [中文](../config/OrbbecSDKConfig_zh-CN.md) |
| 更新日志 | [English](CHANGELOG.md) | [中文](CHANGELOG_zh-CN.md) |
| V2 功能介绍 | [English](guide/V2_FEATURES.md) | [中文](guide/V2_FEATURES_zh-CN.md) |
| 设备二进制数据接口 | [English](guide/binary_device_data.md) | [中文](guide/binary_device_data_zh-CN.md) |
| 回放预设问题分析 | [English](playback_preset_analysis_en.md) | [中文](playback_preset_analysis.md) |
| 示例索引与学习路径 | [English](../examples/README.md) | [中文](../examples/README_zh-CN.md) |
| YOLO 目标检测 | [English](../examples/applications/object_detection/README.md) | [中文](../examples/applications/object_detection/README_zh-CN.md) |
| YOLO 模型配置 | [English](../examples/applications/object_detection/models/readme.md) | [中文](../examples/applications/object_detection/models/readme_zh-CN.md) |
| 日志配置 | [English](../examples/beginner/LOG_CONFIGURATION.md) | [中文](../examples/beginner/LOG_CONFIGURATION_zh-CN.md) |
| Windows UVC 元数据注册 | [English](../scripts/env_setup/obsensor_metadata_win10.md) | [中文](../scripts/env_setup/obsensor_metadata_win10_zh-CN.md) |
| 类型存根与 IDE 配置 | [English](../stubs/README.md) | [中文](../stubs/README_zh-CN.md) |
| 测试标记 | [English](../test/MARKERS.md) | [中文](../test/MARKERS_zh-CN.md) |
| 测试套件 | [English](../test/README.md) | [中文](../test/README_zh-CN.md) |

## 维护约定

- 默认保留原英文文件名，中文版使用 `_zh-CN.md`。原为中文的分析报告保留文件名，并提供 `_en.md` 英文版。
- 更新说明时同步维护两种语言，并检查章节锚点和相对链接。中文文档优先链接到中文版。
- API 名称、命令、参数、枚举、配置键、文件路径和代码示例保留原样。代码块中的注释及诊断输出也保留，便于与源码对照。
- `en/` 和 `zh_CN/` 下的 HTML、搜索索引及 `_sources` 是生成的网站内容，应通过文档构建流程更新。
- 许可证正文（包括 libjpeg 的 `LICENSE.md`）保留上游原文。`sdk/lib/README.md` 当前为 Git LFS 指针，需先获取实际内容，不能将指针当作说明文档翻译。下载的第三方 SDK、构建产物和本地临时报告不包含在本索引中。
- 在 GitHub 新建 PR 时，可通过 URL 参数 `template=zh-CN.md` 选择中文模板；原默认 PR 模板仍可使用。
