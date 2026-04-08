# Test Markers

## Usage

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

## Marker Definitions

| Marker | Description |
|--------|-------------|
| `hardware` | Requires physical Orbbec camera |
| `g300_series` | Gemini 330/335/336/305/345 series |
| `femto` | Femto Bolt / Femto Mega |
| `astra_mini` | Astra Mini Pro / S Pro |
| `astra2` | Astra 2 |
| `functional` | API correctness tests |
| `stability` | Multi-frame reliability tests |
| `performance` | Long-running benchmark tests |
| `slow` | Extended duration tests |
| `p0` | P0 release gate |
