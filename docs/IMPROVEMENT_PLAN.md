# pyorbbecsdk 仓库优化改进计划

> 基于 README、Examples 及 GitHub 标准的分析报告，生成于 2026-03-04

---

## 一、改进任务清单

### 优先级 P0 - 必须完成

| # | 任务 | 状态 | 说明 |
|---|------|------|------|
| 1 | 创建 `.github/ISSUE_TEMPLATE/bug_report.md` | ⬜ 待完成 | Bug 报告模板，规范用户提交问题 |
| 2 | 创建 `.github/ISSUE_TEMPLATE/feature_request.md` | ⬜ 待完成 | 功能请求模板 |
| 3 | 创建 `.github/PULL_REQUEST_TEMPLATE.md` | ⬜ 待完成 | PR 提交模板，规范贡献流程 |
| 4 | 创建 `CODE_OF_CONDUCT.md` | ⬜ 待完成 | CONTRIBUTING.md 已引用但文件不存在 |

### 优先级 P1 - 应该完成

| # | 任务 | 状态 | 说明 |
|---|------|------|------|
| 5 | 修复 `examples/utils.py:25` 重复 pid 检查 | ⬜ 待完成 | 代码错误：`pid == 0x069d` 重复出现 |
| 6 | 更新 `CONTRIBUTING.md` numpy 版本说明 | ⬜ 待完成 | 仓库已支持 numpy>=2.0，需更新文档 |
| 7 | 统一 `examples/requirements.txt` 依赖版本说明 | ⬜ 待完成 | 添加版本兼容性注释 |

### 优先级 P2 - 可选改进

| # | 任务 | 状态 | 说明 |
|---|------|------|------|
| 8 | README 添加 GIF/视频演示 | ⬜ 可选 | 增强项目展示效果 |
| 9 | 拆分设备支持表到独立文档 | ⬜ 可选 | README 篇幅较长，可拆分到 `docs/DEVICES.md` |
| 10 | 添加 `SECURITY.md` | ⬜ 可选 | 安全政策文件 |
| 11 | 添加 `CODEOWNERS` | ⬜ 可选 | 定义代码负责人 |

---

## 二、详细任务说明

### 任务 1-3: GitHub 模板文件

#### 1.1 Bug 报告模板 (`.github/ISSUE_TEMPLATE/bug_report.md`)

```markdown
---
name: Bug report
about: Report a bug to help us improve
title: '[BUG] '
labels: bug
assignees: ''
---

## Bug Description
A clear and concise description of what the bug is.

## Steps to Reproduce
1.
2.
3.

## Expected Behavior
A clear and concise description of what you expected to happen.

## Actual Behavior
A clear and concise description of what actually happened.

## Environment
- **OS**: [e.g. Windows 10, Ubuntu 22.04]
- **Python version**: [e.g. 3.10.12]
- **pyorbbecsdk version**: [e.g. 2.0.18]
- **Device model**: [e.g. Gemini 335, Femto Bolt]
- **Firmware version**: [e.g. 1.2.20]

## Log Output
```
Paste any relevant log output here
```

## Screenshots
If applicable, add screenshots to help explain your problem.

## Additional Context
Add any other context about the problem here.
```

#### 1.2 功能请求模板 (`.github/ISSUE_TEMPLATE/feature_request.md`)

```markdown
---
name: Feature request
about: Suggest an idea for this project
title: '[FEATURE] '
labels: enhancement
assignees: ''
---

## Is your feature request related to a problem?
A clear and concise description of what the problem is.

## Describe the solution you'd like
A clear and concise description of what you want to happen.

## Describe alternatives you've considered
A clear and concise description of any alternative solutions.

## Additional Context
Add any other context or screenshots about the feature request here.

## Would you be willing to submit a PR?
- [ ] Yes, I would like to submit a PR to implement this feature.
```

#### 1.3 PR 模板 (`.github/PULL_REQUEST_TEMPLATE.md`)

```markdown
## Description
<!-- Provide a brief description of the changes in this PR -->

## Related Issue
Fixes #

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update
- [ ] Code refactoring

## How Has This Been Tested?
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing with device

**Test Environment:**
- OS:
- Python version:
- Device model:

## Checklist
- [ ] My code follows the style guidelines
- [ ] I have performed a self-review
- [ ] I have commented my code
- [ ] I have updated documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests
- [ ] I have updated type stubs if public API changed
```

---

### 任务 4: CODE_OF_CONDUCT.md

使用 Contributor Covenant 2.0 标准模板，主要内容包括：
- 行为准则承诺
- 可接受/不可接受行为标准
- 执行责任
- 适用范围
- 执行方式
- 联系方式：support@orbbec.com

---

### 任务 5: 修复 utils.py 代码错误

**文件**: `examples/utils.py`

**问题**: 第 25 行 `is_astra_mini_device` 函数中有重复的 pid 检查

**当前代码**:
```python
def is_astra_mini_device(vid: int, pid: int) -> bool:
    if (vid == 0x2bc5) and (pid == 0x069d or pid == 0x069d or pid ==0x065b or pid == 0x065e):
        return True
    return False
```

**修复后代码**:
```python
def is_astra_mini_device(vid: int, pid: int) -> bool:
    if (vid == 0x2bc5) and (pid == 0x069d or pid == 0x065b or pid == 0x065e):
        return True
    return False
```

**问题列表**:
1. `pid == 0x069d` 重复出现
2. `pid ==0x065b` 缺少空格（格式问题）

---

### 任务 6: 更新 CONTRIBUTING.md numpy 版本说明

**文件**: `CONTRIBUTING.md`

**当前内容** (第 45-46 行):
```markdown
Key dependency note: use `numpy<2.0` — numpy 2.x introduced breaking C API changes.
See [issue #47](https://github.com/orbbec/pyorbbecsdk/issues/47) for details.
```

**更新为**:
```markdown
Key dependency note: the SDK supports numpy 2.x.
```

---

### 任务 7: 更新 requirements.txt 说明

**文件**: `examples/requirements.txt`

**当前内容**:
```txt
pybind11==2.11.0
pybind11-global==2.11.0
opencv-python
wheel
numpy
open3d
av
pygame
pynput
onnxruntime
```

**建议添加注释说明**:
```txt
# Build dependencies
pybind11==2.11.0
pybind11-global==2.11.0
wheel

# Runtime dependencies (versions not pinned for compatibility)
opencv-python
numpy           # Supports numpy 1.x and 2.x
open3d          # For point cloud visualization
av              # For H.264 decoding (network camera examples)
pygame          # For visualization
pynput          # For keyboard input
onnxruntime     # For object detection example
```

---

## 三、执行命令参考

### 创建目录结构
```bash
mkdir -p .github/ISSUE_TEMPLATE
```

### Git 操作
```bash
# 添加所有新文件
git add .github/ISSUE_TEMPLATE/
git add .github/PULL_REQUEST_TEMPLATE.md
git add CODE_OF_CONDUCT.md

# 添加修改的文件
git add examples/utils.py
git add CONTRIBUTING.md

# 提交更改
git commit -m "chore: add GitHub templates and fix code issues

- Add bug_report.md and feature_request.md issue templates
- Add PULL_REQUEST_TEMPLATE.md
- Add CODE_OF_CONDUCT.md (referenced by CONTRIBUTING.md)
- Fix duplicate pid check in examples/utils.py
- Update numpy version note in CONTRIBUTING.md (now supports numpy 2.x)"
```

---

## 四、验证清单

完成所有任务后，验证以下内容：

- [ ] `.github/ISSUE_TEMPLATE/bug_report.md` 存在且格式正确
- [ ] `.github/ISSUE_TEMPLATE/feature_request.md` 存在且格式正确
- [ ] `.github/PULL_REQUEST_TEMPLATE.md` 存在且格式正确
- [ ] `CODE_OF_CONDUCT.md` 存在
- [ ] `examples/utils.py` 中 `is_astra_mini_device` 函数无重复 pid 检查
- [ ] `CONTRIBUTING.md` 中 numpy 版本说明已更新
- [ ] 所有更改已提交到 git

---

## 五、评分对比

| 维度 | 优化前 | 优化后 |
|------|--------|--------|
| README 质量 | ⭐⭐⭐⭐ (4/5) | ⭐⭐⭐⭐ (4/5) |
| Examples 质量 | ⭐⭐⭐⭐⭐ (5/5) | ⭐⭐⭐⭐⭐ (5/5) |
| GitHub 标准符合 | ⭐⭐⭐ (3/5) | ⭐⭐⭐⭐⭐ (5/5) |
| 用户体验 | ⭐⭐⭐⭐ (4/5) | ⭐⭐⭐⭐ (4/5) |
| **总体评分** | **⭐⭐⭐⭐ (4/5)** | **⭐⭐⭐⭐⭐ (5/5)** |

---

## 六、参考资源

- [GitHub Issue Templates 文档](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/configuring-issue-templates-for-your-repository)
- [GitHub PR Templates 文档](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/creating-a-pull-request-template-for-your-repository)
- [Contributor Covenant](https://www.contributor-covenant.org/)
- [Open Source Guides](https://opensource.guide/)