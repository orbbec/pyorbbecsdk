---
name: Pull Request
about: 向 pyorbbecsdk 提交修改
title: '[PR] '
---

[English](https://github.com/orbbec/pyorbbecsdk/blob/v2-main/.github/PULL_REQUEST_TEMPLATE.md) | **中文**

<a id="description"></a>

## 说明

<!-- 请清晰、简洁地描述修改 -->

**此 PR 实现了什么？**

<!-- 描述 PR 的目的和解决的问题 -->

**动机与背景**

<!-- 为什么需要此修改？它解决了什么问题？ -->
<!-- 如修复已有 issue，请在此关联：Fixes #NNN -->

<a id="type-of-change"></a>

## 修改类型

<!-- 在相应选项中填写 [x] -->

- [ ] 缺陷修复（修复问题且不破坏兼容性）
- [ ] 新功能（新增能力且不破坏兼容性）
- [ ] 破坏性修改（导致现有功能行为发生不兼容变化的修复或功能）
- [ ] 文档更新
- [ ] 性能改进
- [ ] 代码重构（不改变功能）
- [ ] 构建或 CI 改进
- [ ] 其他（请说明）：

<a id="changes-made"></a>

## 修改内容

<!-- 列出此 PR 的主要修改 -->

1.
2.
3.

<a id="testing"></a>

## 测试

<!-- 描述执行过的测试及复现方式 -->

**测试环境：**

- 操作系统：<!-- 如 Ubuntu 22.04、Windows 11、macOS 14 -->
- Python 版本：<!-- 如 3.10、3.12 -->
- 设备：<!-- 如 Gemini 335、Femto Mega -->

**已执行测试：**

- [ ] 单元测试通过（`pytest test/ -m "not hardware" -v`）
- [ ] 硬件测试通过（如适用，需连接相机）
- [ ] 已完成手动测试
- [ ] 示例运行无错误

**测试命令：**

<!-- 提供测试此次修改时使用的命令 -->

```bash
# Example test commands
```

<a id="checklist"></a>

## 检查清单

<!-- 在已完成项中填写 [x] -->

- [ ] 已阅读 [CONTRIBUTING.md](../CONTRIBUTING_zh-CN.md)
- [ ] 代码符合项目风格（C++：clang-format；Python：PEP 8）
- [ ] 已更新文档（如适用）
  - [ ] 已更新 README.md
  - [ ] 已更新 API 文档
  - [ ] 已更新类型存根（`stubs/pyorbbecsdk.pyi`）
- [ ] 已添加或更新测试（如适用）
- [ ] 全部测试在本地通过
- [ ] 修改未产生新的警告
- [ ] 已检查公共 API 是否存在破坏性修改
- [ ] 提交信息清晰，符合 conventional commits 格式

<a id="related-issues"></a>

## 关联问题

<!-- 关联相关 issue -->

Fixes #（issue 编号）
Related to #（issue 编号）

<a id="screenshots-if-applicable"></a>

## 截图（如适用）

<!-- 添加有助于说明修改的截图 -->

<a id="additional-notes"></a>

## 补充说明

<!-- 审阅者需要了解的其他信息 -->

<a id="reviewer-notes"></a>

## 审阅提示

<!-- 希望审阅者重点关注的部分 -->
