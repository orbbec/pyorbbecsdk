# 回放预设未生效问题分析报告

> **场景**：pyorbbecsdk 录制/回放 sample 引入侧车 JSON 预设机制后，回放时预设未实际生效。
> **设备**：Orbbec Gemini 336L
> **SDK 版本**：OrbbecSDK v2.9.0
> **参考实现**：OpenOrbbecViewer v2.9.0（`FrameFilterManager` / `MainPage`）

---

## 一、问题现象

录制 sample 在停止录制后，导出与 `.bag` 同名的 `.json` 侧车预设文件；回放 sample 检测并加载该 JSON。运行回放时控制台提示：

```
[Sidecar] Loaded preset JSON: Orbbec Gemini 336L_..._20260618101957.json
```

但**实际预设未生效**——例如录制时开启的深度填洞滤波（HoleFillingFilter），回放画面中看不到任何效果。

---

## 二、排查过程

排查分四个阶段层层递进，每一阶段都通过诊断代码证伪或证实一个假设。

### 阶段一：怀疑加载时机错乱

**假设**：`load_preset_from_json_file` 调用晚于 `Pipeline()` 创建，导致 Property 没传递到内部 filter-chain。

**验证**：在 `PlaybackDevice` 创建后、`Pipeline()` 创建前加载 JSON，并打印加载前后的设备属性。

**诊断输出**：
```
OB_PROP_DEPTH_HOLEFILTER_BOOL: supported=False value=None   (加载前)
OB_PROP_DEPTH_HOLEFILTER_BOOL: supported=False value=None   (加载后)
```

**结论**：时机不是根因。`OB_PROP_DEPTH_HOLEFILTER_BOOL` 这个设备属性在 Gemini 336L 上**根本不被支持**（`supported=False`），填洞滤波不是走设备属性通道的。

### 阶段二：检查 JSON 内容

**假设**：可能导出端没有把填洞滤波写进 JSON。

**验证**：读取 JSON 并定位 `post_processing_filter` 段。

**诊断输出**：
```json
"post_processing_filter": [
  { "filter_name": "SpatialAdvancedFilter", "enable": true, ... },
  { "filter_name": "TemporalFilter",        "enable": true, ... },
  { "filter_name": "HoleFillingFilter",     "enable": true, "hole_filling_mode": 0 },
  { "filter_name": "DisparityTransform",    "enable": true, ... }
]
```

**结论**：JSON 里填洞滤波确实存在且 `enable: true`，导出端没问题。这些是 **SDK 软件 filter**，存在 JSON 的 `post_processing_filter` 数组里，与设备硬件属性无关。

### 阶段三：检查 recommended filters 状态

**假设**：`load_preset_from_json_file` 没有正确恢复 filter 的启用状态。

**验证**：读取每个 sensor 的 `get_recommended_filters()` 并打印 `is_enabled()`。

**诊断输出（加载前）**：
```
sensor=DEPTH_SENSOR filter=HoleFillingFilter     enabled=False
sensor=DEPTH_SENSOR filter=SpatialAdvancedFilter enabled=False
sensor=DEPTH_SENSOR filter=TemporalFilter        enabled=False
```

**诊断输出（加载后）**：
```
sensor=DEPTH_SENSOR filter=HoleFillingFilter     enabled=True   ✅
sensor=DEPTH_SENSOR filter=SpatialAdvancedFilter enabled=True   ✅
sensor=DEPTH_SENSOR filter=TemporalFilter        enabled=True   ✅
sensor=DEPTH_SENSOR filter=DisparityTransform    enabled=True   ✅
```

**结论**：`load_preset_from_json_file` **确实正确配置**了 recommended filters 的启用状态。状态是对的，但画面没效果——说明问题不在"加载"，而在"应用"。

### 阶段四：对照 OpenOrbbecViewer 源码

查阅 `OpenOrbbecViewer/server/core/FrameFilterManager.cpp` 与 `app/OrbbecViewer/view/MainPage/MainPage.cpp`：

- OpenOrbbecViewer **没有**依赖 Pipeline 自动应用 filter
- 它用自建的 `FrameFilterManager`，在 `OBSensorExt` 的帧回调里**手动**把 recommended filters 串起来调用 `filter.process(frame)`
- `loadPresetFromJsonFile` 只负责配置 filter 的 `enable` 状态和参数，**不负责把 filter 接入数据通路**

**根因确认**：Python 的 `Pipeline(config, callback)` 回调模式下，SDK **不会自动**把启用的 recommended filters 应用到帧上。filter 的 `enabled=True` 只是一个状态标记，需要使用者自己在帧通路上执行 `process()`。

---

## 三、根因总结

| 层次 | 结论 |
|------|------|
| JSON 导出 | ✅ 正确，`post_processing_filter` 含 `HoleFillingFilter enable:true` |
| JSON 加载 | ✅ 正确，`load_preset_from_json_file` 后 recommended filters 的 `is_enabled()` 变为 `True` |
| 设备属性 | ❌ 无关，`OB_PROP_DEPTH_HOLEFILTER_BOOL` 在该设备不支持，填洞是软件 filter |
| Filter 应用 | ❌ **根因所在**：Pipeline 回调模式不自动应用 recommended filters，需要手动 `process()` |

简言之：**"配置对了，但没人执行"**。SDK 把 filter 状态恢复成"已启用"，但帧数据通路里没有人调用这些 filter，所以画面看不到效果。

---

## 四、数据通路对比

### 错误通路（原 sample）

```
Pipeline.start(config, callback)
        │
        ▼
  帧到达 callback（原始帧，未经 filter 处理）
        │
        ▼
  直接可视化  ←  填洞/spatial/temporal 全部未执行
```

`load_preset_from_json_file` 配置了 filter 的 `enable=True`，但这条通路里没有任何节点调用 `filter.process()`，filter 处于"已启用但闲置"状态。

### 正确通路（修复后）

```
Pipeline.start(config, callback)
        │
        ▼
  帧到达 callback
        │
        ▼
  _apply_filter_chain(frame, enabled_filters)   ← 手动执行 recommended filters
        │   ├─ SpatialAdvancedFilter.process()
        │   ├─ TemporalFilter.process()
        │   ├─ HoleFillingFilter.process()
        │   └─ DisparityTransform.process()
        ▼
  可视化  ←  与录制时一致
```

### OpenOrbbecViewer 的等价做法

OpenOrbbecViewer 的 `FrameFilterManager` 在 `OBSensorExt` 帧回调里维护一个 filter 链，对每一帧依次执行 enabled filter 的 `process()`。Python 侧的 `_apply_filter_chain` 即是对这一机制的精简复刻。

---

## 五、修复方案

参考 OpenOrbbecViewer 的 `FrameFilterManager` 思路，在 Python 侧手动应用 recommended filters：

### 1. 收集启用的 filter

```python
def _collect_enabled_filters(device):
    """加载预设后，遍历每个 sensor 的 recommended filters，收集 enabled 的。"""
    enabled = {}
    sensor_list = device.get_sensor_list()
    for i in range(len(sensor_list)):
        sensor = sensor_list[i]
        stype = sensor.get_type()
        filters = sensor.get_recommended_filters()
        chain = [f for f in filters if _safe_is_enabled(f)]
        if chain:
            enabled[stype] = chain
    return enabled
```

### 2. 通用 filter 链执行器

```python
def _apply_filter_chain(frame, filters):
    """依次执行 filter.process()，单个 filter 失败则跳过而非丢帧。"""
    out = frame
    for f in filters:
        try:
            processed = f.process(out)
            if processed is not None:
                out = processed
        except Exception:
            continue
    return out
```

### 3. 帧回调中应用

```python
def video_frame_callback(frames):
    if frames is None:
        return
    with state.frame_mutex:
        depth_frame = frames.get_depth_frame()
        if depth_frame:
            depth_filters = state.enabled_filters.get(OBSensorType.DEPTH_SENSOR)
            if depth_filters:
                depth_frame = _apply_filter_chain(depth_frame, depth_filters)
            state.cached_frames["depth"] = process_depth(depth_frame)
        # ... 其余流处理
```

### 4. 加载预设后收集 filter

```python
preset_loaded = _load_sidecar_json(playback, file_path)
if preset_loaded:
    state.enabled_filters = _collect_enabled_filters(playback)
    for stype, flist in state.enabled_filters.items():
        names = [f.get_name() for f in flist]
        print(f"[Filters] {stype}: applying {names}")
```

启动时会打印实际应用的 filter 链，便于确认：

```
[Filters] OBSensorType.DEPTH_SENSOR: applying ['SpatialAdvancedFilter', 'TemporalFilter', 'HoleFillingFilter', 'DisparityTransform']
```

---

## 六、关键经验

### 1. "设备属性"与"软件 filter"要区分

`OB_PROP_DEPTH_HOLEFILTER_BOOL` 是设备属性通道，很多设备不支持；实际生效的填洞滤波是 SDK 的 `HoleFillingFilter`，存在 JSON 的 `post_processing_filter` 里。排查时若只盯设备属性，会误判为"设备不支持"而放弃。

### 2. `loadPresetFromJsonFile` 只"配置"不"执行"

它恢复 filter 的 `enable` 状态和参数，但**不会**把 filter 自动接入帧通路。自动应用是 OpenOrbbecViewer 这类上层应用自己实现的逻辑。这一隐含约定 SDK 文档未显式说明。

### 3. 诊断要先证伪再定位

本次排查顺序：

| 阶段 | 假设 | 验证手段 | 结果 |
|------|------|---------|------|
| 一 | 加载时机错乱 | 打印设备属性 supported/value | 证伪（属性 supported=False） |
| 二 | JSON 没导出 | 读取 JSON post_processing_filter | 证伪（JSON 含 enable:true） |
| 三 | 加载没生效 | 打印 recommended filters is_enabled | 证伪（加载后 enabled=True） |
| 四 | 没人执行 filter | 对照 OpenOrbbecViewer 源码 | **确认根因** |

三个诊断阶段层层递进，每步都排除了一个错误方向，避免了在错误假设上反复猜测调用顺序。

### 4. Pipeline 回调模式的隐含约定

`Pipeline(config, callback)` 给的是"原始帧"，recommended filters 需自行处理。这一点需从官方 Viewer 实现中反推，是本次最容易踩的坑。

---

## 七、涉及文件

| 文件 | 角色 |
|------|------|
| `examples/advanced/01_recorder.py` | 录制端：停止后导出侧车 JSON |
| `examples/advanced/02_playback.py` | 回放端：加载 JSON + 手动应用 recommended filters |
| `sdk/include/libobsensor/hpp/Filter.hpp` | `HoleFillingFilter` 等 filter 定义 |
| `sdk/include/libobsensor/hpp/Device.hpp` | `loadPresetFromJsonFile` / `exportSettingsAsPresetJsonFile` |
| OpenOrbbecViewer `server/core/FrameFilterManager.cpp` | 官方 filter 链应用参考实现 |
| OpenOrbbecViewer `app/OrbbecViewer/view/MainPage/MainPage.cpp` | 官方回放预设加载流程参考 |
