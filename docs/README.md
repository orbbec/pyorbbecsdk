**English** | [中文](README_zh-CN.md)

# Documentation Index

See the [project README](../README.md) for an overview, installation, and supported platforms. This index lists the English and Chinese documentation maintained in this repository.

## Online User Guide

- [English](https://orbbec.github.io/pyorbbecsdk/en/index.html)
- [中文](https://orbbec.github.io/pyorbbecsdk/zh_CN/index.html)

## Repository Guides

Use the English / 中文 links at the top of each document to switch languages.

| Document | English | 中文 |
|---|---|---|
| Code of conduct | [English](../.github/CODE_OF_CONDUCT.md) | [中文](../.github/CODE_OF_CONDUCT_zh-CN.md) |
| Contributing | [English](../.github/CONTRIBUTING.md) | [中文](../.github/CONTRIBUTING_zh-CN.md) |
| Bug report template | [English](../.github/ISSUE_TEMPLATE/bug_report.md) | [中文](../.github/ISSUE_TEMPLATE/bug_report_zh-CN.md) |
| Feature request template | [English](../.github/ISSUE_TEMPLATE/feature_request.md) | [中文](../.github/ISSUE_TEMPLATE/feature_request_zh-CN.md) |
| Pull request template | [English](../.github/PULL_REQUEST_TEMPLATE.md) | [中文](../.github/PULL_REQUEST_TEMPLATE/zh-CN.md) |
| SDK configuration | [English](../config/OrbbecSDKConfig.md) | [中文](../config/OrbbecSDKConfig_zh-CN.md) |
| Changelog | [English](CHANGELOG.md) | [中文](CHANGELOG_zh-CN.md) |
| V2 features | [English](guide/V2_FEATURES.md) | [中文](guide/V2_FEATURES_zh-CN.md) |
| Device binary data interfaces | [English](guide/binary_device_data.md) | [中文](guide/binary_device_data_zh-CN.md) |
| Playback preset investigation | [English](playback_preset_analysis_en.md) | [中文](playback_preset_analysis.md) |
| Example catalog and learning path | [English](../examples/README.md) | [中文](../examples/README_zh-CN.md) |
| YOLO object detection | [English](../examples/applications/object_detection/README.md) | [中文](../examples/applications/object_detection/README_zh-CN.md) |
| YOLO model setup | [English](../examples/applications/object_detection/models/readme.md) | [中文](../examples/applications/object_detection/models/readme_zh-CN.md) |
| Logging configuration | [English](../examples/beginner/LOG_CONFIGURATION.md) | [中文](../examples/beginner/LOG_CONFIGURATION_zh-CN.md) |
| Windows UVC metadata registration | [English](../scripts/env_setup/obsensor_metadata_win10.md) | [中文](../scripts/env_setup/obsensor_metadata_win10_zh-CN.md) |
| SDK configuration: arm64 | [English](../sdk/lib/arm64/OrbbecSDKConfig.md) | [中文](../sdk/lib/arm64/OrbbecSDKConfig_zh-CN.md) |
| SDK configuration: linux_x64 | [English](../sdk/lib/linux_x64/OrbbecSDKConfig.md) | [中文](../sdk/lib/linux_x64/OrbbecSDKConfig_zh-CN.md) |
| SDK configuration: macOS | [English](../sdk/lib/macOS/OrbbecSDKConfig.md) | [中文](../sdk/lib/macOS/OrbbecSDKConfig_zh-CN.md) |
| SDK configuration: win_x64 | [English](../sdk/lib/win_x64/OrbbecSDKConfig.md) | [中文](../sdk/lib/win_x64/OrbbecSDKConfig_zh-CN.md) |
| Third-party dependency inventory | [English](../sdk/licenses/THIRD_PARTY_LICENSES.md) | [中文](../sdk/licenses/THIRD_PARTY_LICENSES_zh-CN.md) |
| Type stubs and IDE configuration | [English](../stubs/README.md) | [中文](../stubs/README_zh-CN.md) |
| Test markers | [English](../test/MARKERS.md) | [中文](../test/MARKERS_zh-CN.md) |
| Test suite | [English](../test/README.md) | [中文](../test/README_zh-CN.md) |

## Maintenance

- Keep the original English filename and add `_zh-CN.md` for Chinese. The existing Chinese investigation keeps its filename and has an `_en.md` English counterpart.
- Update both languages together and verify section anchors and relative links. Chinese guides link to Chinese counterparts where available.
- Preserve API names, commands, arguments, enums, configuration keys, paths, and code examples. Comments and diagnostic output inside code blocks also remain unchanged for comparison with source.
- HTML pages, search indexes, and `_sources` under `en/` and `zh_CN/` are generated website content; update them through the documentation build workflow.
- License texts, including libjpeg `LICENSE.md`, retain their upstream wording. `sdk/lib/README.md` is currently a Git LFS pointer; fetch its actual content before translating it. Downloaded third-party SDK trees, build outputs, and local scratch reports are outside this index.
- On GitHub, select the Chinese PR template by adding `template=zh-CN.md` to the new pull request URL. The existing default PR template remains available.
