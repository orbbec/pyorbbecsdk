
[English](MARKERS.md) | **中文**

<a id="test-markers"></a>

# 测试标记

<a id="usage"></a>

## 使用方法

```bash
# Run all tests
pytest test/ -v

# Skip hardware tests (CI without device)
pytest test/ -v -m "not hardware"

# Run only hardware tests
pytest test/ -v -m "hardware"

# Run specific device family tests
pytest test/ -v -m "g300_series"
pytest test/ -v -m "femto"
pytest test/ -v -m "astra2"

# Skip long-running performance tests
pytest test/ -v -m "not performance"

# Run P0 release gate tests
pytest test/ -v -m "p0"
```

<a id="marker-definitions"></a>

## 标记定义

| 标记 | 说明 |
|--------|-------------|
| `hardware` | 需要实体 Orbbec 相机 |
| `g300_series` | Gemini 330/335/336/305/345 系列 |
| `femto` | Femto Bolt / Femto Mega |
| `astra_mini` | Astra Mini Pro / S Pro |
| `astra2` | Astra 2 |
| `functional` | API 正确性测试 |
| `stability` | 多帧可靠性测试 |
| `performance` | 长时间运行的基准测试 |
| `slow` | 耗时较长的测试 |
| `p0` | P0 发布门禁测试 |
