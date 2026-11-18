
**English** | [中文](playback_preset_analysis.md)

<a id="回放预设未生效问题分析报告"></a>

# Analysis: Playback Presets Not Taking Effect

> **Scenario:** After sidecar JSON presets were introduced into the pyorbbecsdk recording/playback samples, presets did not take effect during playback.
> **Device:** Orbbec Gemini 336L
> **SDK version:** OrbbecSDK v2.9.0
> **Reference implementation:** OpenOrbbecViewer v2.9.0 (`FrameFilterManager` / `MainPage`)

---

<a id="一问题现象"></a>

## 1. Symptoms

After recording stops, the recording sample exports a `.json` sidecar preset with the same name as the `.bag` file. The playback sample detects and loads this JSON. Playback prints:

```
[Sidecar] Loaded preset JSON: Orbbec Gemini 336L_..._20260618101957.json
```

However, **the preset has no visible effect**. For example, hole filling (HoleFillingFilter) enabled during recording produces no visible effect during playback.

---

<a id="二排查过程"></a>

## 2. Investigation

The investigation proceeded through four stages, each using diagnostic code to confirm or reject a hypothesis.

<a id="阶段一怀疑加载时机错乱"></a>

### Stage 1: Suspected Loading Order

**Hypothesis:** Calling `load_preset_from_json_file` after creating `Pipeline()` prevents properties from reaching the internal filter chain.

**Verification:** Load JSON after creating `PlaybackDevice` but before creating `Pipeline()`, and print device properties before and after loading.

**Diagnostic output:**

```
OB_PROP_DEPTH_HOLEFILTER_BOOL: supported=False value=None   (加载前)
OB_PROP_DEPTH_HOLEFILTER_BOOL: supported=False value=None   (加载后)
```

**Conclusion:** Timing is not the root cause. The device property `OB_PROP_DEPTH_HOLEFILTER_BOOL` is **not supported** on Gemini 336L (`supported=False`). Hole filling is not controlled through this device property.

<a id="阶段二检查-json-内容"></a>

### Stage 2: Check JSON Content

**Hypothesis:** The export code may have omitted the hole-filling filter from JSON.

**Verification:** Read JSON and locate `post_processing_filter`.

**Diagnostic output:**

```json
"post_processing_filter": [
  { "filter_name": "SpatialAdvancedFilter", "enable": true, ... },
  { "filter_name": "TemporalFilter",        "enable": true, ... },
  { "filter_name": "HoleFillingFilter",     "enable": true, "hole_filling_mode": 0 },
  { "filter_name": "DisparityTransform",    "enable": true, ... }
]
```

**Conclusion:** The JSON contains the hole-filling filter with `enable: true`; export is correct. These are **SDK software filters** stored in the JSON `post_processing_filter` array, independent of device hardware properties.

<a id="阶段三检查-recommended-filters-状态"></a>

### Stage 3: Check Recommended Filter State

**Hypothesis:** `load_preset_from_json_file` does not restore filter enable states correctly.

**Verification:** Read `get_recommended_filters()` for each sensor and print `is_enabled()`.

**Diagnostic output before loading:**

```
sensor=DEPTH_SENSOR filter=HoleFillingFilter     enabled=False
sensor=DEPTH_SENSOR filter=SpatialAdvancedFilter enabled=False
sensor=DEPTH_SENSOR filter=TemporalFilter        enabled=False
```

**Diagnostic output after loading:**

```
sensor=DEPTH_SENSOR filter=HoleFillingFilter     enabled=True   ✅
sensor=DEPTH_SENSOR filter=SpatialAdvancedFilter enabled=True   ✅
sensor=DEPTH_SENSOR filter=TemporalFilter        enabled=True   ✅
sensor=DEPTH_SENSOR filter=DisparityTransform    enabled=True   ✅
```

**Conclusion:** `load_preset_from_json_file` **does configure** the recommended filter enable states correctly. The correct state without any visible effect points to filter application rather than loading.

<a id="阶段四对照-openorbbecviewer-源码"></a>

### Stage 4: Compare OpenOrbbecViewer Source

Inspect `OpenOrbbecViewer/server/core/FrameFilterManager.cpp` and `app/OrbbecViewer/view/MainPage/MainPage.cpp`:

- OpenOrbbecViewer does not rely on Pipeline to apply filters automatically.
- Its `FrameFilterManager` manually chains recommended filters using `filter.process(frame)` in the `OBSensorExt` frame callback.
- `loadPresetFromJsonFile` configures filter `enable` states and parameters; it does not connect filters to the data path.

**Confirmed root cause:** In Python's `Pipeline(config, callback)` callback mode, the SDK does not automatically apply enabled recommended filters to frames. `enabled=True` is a state flag; the application must execute `process()` in the frame path.

---

<a id="三根因总结"></a>

## 3. Root Cause Summary

| Layer | Finding |
|------|------|
| JSON export | ✅ Correct: `post_processing_filter` contains `HoleFillingFilter enable:true` |
| JSON loading | ✅ Correct: after `load_preset_from_json_file`, recommended filters report `is_enabled()` as `True` |
| Device property | ❌ Unrelated: `OB_PROP_DEPTH_HOLEFILTER_BOOL` is unsupported on this device; hole filling is a software filter |
| Filter application | ❌ **Root cause:** Pipeline callback mode does not automatically apply recommended filters; call `process()` manually |

The SDK restores the enabled filter states, but no component in the frame data path calls those filters, so the displayed image remains unaffected.

---

<a id="四数据通路对比"></a>

## 4. Data Path Comparison

<a id="错误通路原-sample"></a>

### Incorrect Path: Original Sample

```
Pipeline.start(config, callback)
        │
        ▼
  帧到达 callback（原始帧，未经 filter 处理）
        │
        ▼
  直接可视化  ←  填洞/spatial/temporal 全部未执行
```

`load_preset_from_json_file` sets `enable=True`, but no node calls `filter.process()`. Filters remain enabled but idle.

<a id="正确通路修复后"></a>

### Correct Path: After the Fix

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

<a id="openorbbecviewer-的等价做法"></a>

### Equivalent OpenOrbbecViewer Behavior

OpenOrbbecViewer's `FrameFilterManager` maintains a filter chain in the `OBSensorExt` frame callback and calls `process()` on each enabled filter for every frame. Python's `_apply_filter_chain` is a simplified implementation of the same mechanism.

---

<a id="五修复方案"></a>

## 5. Fix

Following OpenOrbbecViewer's `FrameFilterManager`, apply recommended filters manually in Python.

<a id="1-收集启用的-filter"></a>

### 1. Collect Enabled Filters

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

<a id="2-通用-filter-链执行器"></a>

### 2. Generic Filter Chain Executor

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

<a id="3-帧回调中应用"></a>

### 3. Apply Filters in the Frame Callback

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

<a id="4-加载预设后收集-filter"></a>

### 4. Collect Filters After Loading a Preset

```python
preset_loaded = _load_sidecar_json(playback, file_path)
if preset_loaded:
    state.enabled_filters = _collect_enabled_filters(playback)
    for stype, flist in state.enabled_filters.items():
        names = [f.get_name() for f in flist]
        print(f"[Filters] {stype}: applying {names}")
```

Startup prints the filter chain being applied for confirmation:

```
[Filters] OBSensorType.DEPTH_SENSOR: applying ['SpatialAdvancedFilter', 'TemporalFilter', 'HoleFillingFilter', 'DisparityTransform']
```

---

<a id="六关键经验"></a>

## 6. Lessons

<a id="1-设备属性与软件-filter要区分"></a>

### 1. Distinguish Device Properties from Software Filters

`OB_PROP_DEPTH_HOLEFILTER_BOOL` is a device property unsupported by many devices. The effective hole-filling operation uses the SDK's `HoleFillingFilter`, stored in JSON under `post_processing_filter`. Checking only device properties can incorrectly suggest that the device does not support the feature.

<a id="2-loadpresetfromjsonfile-只配置不执行"></a>

### 2. `loadPresetFromJsonFile` Configures but Does Not Execute

It restores filter `enable` states and parameters, but does not automatically connect filters to the frame path. Automatic application is implemented by applications such as OpenOrbbecViewer. This implicit convention was not explicitly documented in the SDK documentation.

<a id="3-诊断要先证伪再定位"></a>

### 3. Test Hypotheses Before Narrowing the Cause

Investigation sequence:

| Stage | Hypothesis | Verification | Result |
|------|------|---------|------|
| 1 | Incorrect loading order | Print device property supported/value | Rejected: property supported=False |
| 2 | Missing JSON export | Read JSON post_processing_filter | Rejected: JSON contains enable:true |
| 3 | Loading did not take effect | Print recommended filter is_enabled | Rejected: enabled=True after loading |
| 4 | No filter execution | Compare OpenOrbbecViewer source | **Root cause confirmed** |

Each of the first three diagnostic stages eliminated an incorrect direction, avoiding repeated guesses about call order based on a false assumption.

<a id="4-pipeline-回调模式的隐含约定"></a>

### 4. Implicit Pipeline Callback Contract

`Pipeline(config, callback)` provides raw frames; applications must process recommended filters themselves. This behavior had to be inferred from the official Viewer implementation and was the main pitfall in this investigation.

---

<a id="七涉及文件"></a>

## 7. Relevant Files

| File | Role |
|------|------|
| `examples/advanced/01_recorder.py` | Recording: exports sidecar JSON after stopping |
| `examples/advanced/02_playback.py` | Playback: loads JSON and manually applies recommended filters |
| `sdk/include/libobsensor/hpp/Filter.hpp` | Definitions of `HoleFillingFilter` and other filters |
| `sdk/include/libobsensor/hpp/Device.hpp` | `loadPresetFromJsonFile` / `exportSettingsAsPresetJsonFile` |
| OpenOrbbecViewer `server/core/FrameFilterManager.cpp` | Official reference for applying filter chains |
| OpenOrbbecViewer `app/OrbbecViewer/view/MainPage/MainPage.cpp` | Official reference for loading playback presets |
