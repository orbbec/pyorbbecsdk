# pyorbbecsdk Test Suite

This directory contains the pytest-based test suite for pyorbbecsdk.
Tests cover device discovery, sensor controls, stream validation, post-processing filters, calibration, and performance benchmarks — organized by device family and test category.

---

## Prerequisites

1. **Install pyorbbecsdk** (or build from source — see [CONTRIBUTING.md](../.github/CONTRIBUTING.md#building-from-source))
2. **Install test dependencies:**
   ```bash
   pip install -r test/requirements_test.txt
   ```
3. **One-time OS setup (hardware tests only):**
   - **Linux:** install udev rules so the SDK can open USB devices
     ```bash
     cd scripts/env_setup && sudo ./install_udev_rules.sh
     sudo udevadm control --reload && sudo udevadm trigger
     ```
   - **Windows:** register frame metadata (required for timestamps)
     ```powershell
     # Run PowerShell as Administrator
     cd scripts\env_setup
     .\obsensor_metadata_win10.ps1 -op install_all
     ```

---

## One-Click Test Runner

`run_tests.py` auto-detects the connected camera and runs the matching test suite with a single command.

```bash
# Auto-detect device and run all its tests
python test/run_tests.py

# Specify device family explicitly
python test/run_tests.py --device g300
python test/run_tests.py --device femto
python test/run_tests.py --device astra_mini
python test/run_tests.py --device astra2

# Filter by test category
python test/run_tests.py --category functional
python test/run_tests.py --category stability
python test/run_tests.py --category performance

# Combine filters — G300 functional tests only
python test/run_tests.py --device g300 --category functional

# Skip long performance benchmarks
python test/run_tests.py --quick

# No camera needed
python test/run_tests.py --no-hardware

# Save report to a custom directory
python test/run_tests.py --output my_reports/
```

**`--device` accepted values:**

| Alias | Device family |
|-------|---------------|
| `g300`, `gemini`, `gemini335`, `gemini336`, … | G300 Series |
| `femto`, `femto_bolt`, `femto_mega` | Femto Bolt / Mega |
| `astra_mini`, `astra_mini_pro` | Astra Mini |
| `astra2`, `astra_2` | Astra 2 |

Reports are saved to `reports/` and a copy is written to `reports/test_report_latest.html`.

---

## Running Tests Manually

All commands are run from the **repository root**.

### Quick check — no camera needed

```bash
pytest test/ -m "not hardware" -v
```

### Run all tests for a specific device family

```bash
# G300 series (Gemini 330 / 335 / 336 / 305 / 345 and variants)
pytest test/test_g300_series_*.py -v

# Femto Bolt / Femto Mega
pytest test/test_femto_*.py -v

# Astra Mini Pro / S Pro
pytest test/test_astra_mini_*.py -v

# Astra 2
pytest test/test_astra2_*.py -v
```

### Run by device marker

```bash
pytest test/ -m g300_series -v   # G300 series
pytest test/ -m femto       -v   # Femto Bolt/Mega
pytest test/ -m astra_mini  -v   # Astra Mini
pytest test/ -m astra2      -v   # Astra 2
pytest test/ -m hardware    -v   # All hardware tests
```

### Run by category

```bash
pytest test/ -m functional   -v   # API correctness only
pytest test/ -m stability    -v   # Reliability/sync only
pytest test/ -m performance  -v   # Benchmarks only
```

### Combine device + category

```bash
pytest test/ -m "g300_series and functional"  -v
pytest test/ -m "femto and stability"         -v
pytest test/ -m "not performance"             -v   # skip benchmarks
```

### Core tests only (~2 min with camera)

```bash
pytest test/test_g300_series_device.py \
       test/test_g300_series_controls.py \
       test/test_g300_series_calib.py \
       test/test_context.py \
       test/test_device.py -v
```

### Full test session

```bash
pytest test/ -v
```

---

## Test Markers

### Device / scope markers

| Marker | Meaning | Auto-skip condition |
|--------|---------|---------------------|
| `hardware` | Requires a physical Orbbec camera | No device connected |
| `g300_series` | Any Gemini 330/335/336/305/345 variant | Wrong device family |
| `femto` | Femto Bolt or Femto Mega | Wrong device family |
| `astra_mini` | Astra Mini Pro / S Pro | Wrong device family |
| `astra2` | Astra 2 | Wrong device family |

> **Tip:** If the wrong camera is connected, device-specific tests skip automatically with a clear message — they do **not** fail.

### Category markers

| Marker | Meaning | Typical duration |
|--------|---------|-----------------|
| `functional` | API correctness — device info, stream start, sensor controls, calibration, filters | seconds |
| `stability` | Multi-frame reliability — timestamp monotonicity, sync accuracy, drop rate | 10–30 s |
| `performance` | Long-running benchmarks — FPS, latency, throughput | 60+ s |

Category markers compose freely with device markers:

```bash
pytest test/ -m "g300_series and stability" -v
pytest test/ -m "not performance"           -v
```

---

## Test File Map

### Category key: `F` = functional · `S` = stability · `P` = performance

### Basic tests (no camera needed)

| File | Category | What it tests |
|------|----------|---------------|
| `test_basic_import.py` | F | Basic module import and attributes |
| `test_basic_device.py` | F | Context creation and device enumeration (without hardware) |
| `test_basic_capture.py` | F | Pipeline creation and frame capture basics |

### Generic tests (any Orbbec camera)

| File | Category | What it tests |
|------|----------|---------------|
| `test_context.py` | F | Context API: device enumeration, logging, callbacks |
| `test_device.py` | F | Generic device info, sensor list, depth work mode, temperature |
| `test_pipeline.py` | F | Pipeline camera parameter API |

### G300 Series (Gemini 330 / 335 / 336 / 305 / 345 variants)

| File | Category | What it tests |
|------|----------|---------------|
| `test_g300_series_device.py` | F | Device identity, all G300 sensor requirements |
| `test_g300_series_controls.py` | F | Depth/Color/IR/Laser/HDR property read-write |
| `test_g300_series_filters.py` | F | Full post-processing filter pipeline |
| `test_g300_series_calib.py` | F | Intrinsics, distortion, extrinsic orthogonality |
| `test_g300_series_streams.py` | F + S | Stream validity, FPS, multi-stream sync, timestamp monotonicity |
| `test_g300_series_performance.py` | P | Startup latency, 60 s FPS stability, restart time, throughput |

### Femto Bolt / Femto Mega

| File | Category | What it tests |
|------|----------|---------------|
| `test_femto_device.py` | F | Identity, ToF sensors (Depth, Color, Left/Right IR, IMU) |
| `test_femto_controls.py` | F | Depth/Color/Laser property read-write |
| `test_femto_calib.py` | F | Intrinsics, distortion, extrinsic orthogonality |
| `test_femto_streams.py` | F + S | Depth (ToF range 300–8000 mm), Color, IR, IMU, sync |

### Astra Mini Pro / S Pro

| File | Category | What it tests |
|------|----------|---------------|
| `test_astra_mini_device.py` | F | Device identity, sensors, calibration |
| `test_astra_mini_streams.py` | F + S | Depth (300–8000 mm), Color, IR, controls, timestamps |

### Astra 2

| File | Category | What it tests |
|------|----------|---------------|
| `test_astra2_device.py` | F | Device identity, sensors, depth work mode |
| `test_astra2_streams.py` | F + S | Depth (300–10000 mm), Color, IR, sync, controls |

---

## Generating HTML Test Reports

```bash
# One-click runner (auto-detects device, saves to reports/)
python test/run_tests.py

# Quick suite via generate_report.py (skips performance benchmarks)
python test/generate_report.py --quick

# Full suite via generate_report.py
python test/generate_report.py
```

Reports are saved to `reports/test_report_latest.html`.

To view: open the HTML file in any browser.

---

## Known Teardown Behavior

After the test session completes, the Orbbec SDK may print:

```
Fatal Python error: Aborted
```

This is a **known SDK threading cleanup issue** that occurs during Python interpreter shutdown. It does **not** indicate test failures — all test results logged before this message are valid.

---

## Device Depth Range Reference

| Device Family | Min Depth | Max Depth | Sensor Type |
|---------------|-----------|-----------|-------------|
| G300 series (330/335/336) | ~20 mm | ~10 000 mm | Structured light |
| G300 series (305/345) | ~20 mm | ~10 000 mm | Structured light |
| Femto Bolt / Mega | 300 mm | 8 000 mm | Time-of-Flight (ToF) |
| Astra Mini Pro | 300 mm | 8 000 mm | Structured light |
| Astra 2 | 300 mm | 10 000 mm | Structured light |

---

## Adding New Device Tests

To add tests for a new device family:

1. **Register the fixture** in `conftest.py`:
   ```python
   @pytest.fixture(scope="session")
   def my_device_fixture(device, device_info):
       name = device_info.get_name() or ""
       if "My Device Name" not in name:
           pytest.skip(f"Not My Device, got '{name}'")
       return device
   ```

2. **Register the marker** in `conftest.py`:
   ```python
   config.addinivalue_line("markers", "my_device: test for My Device")
   ```

3. **Create test files** following the naming pattern:
   ```
   test_my_device_device.py    # device discovery + sensors       → functional
   test_my_device_streams.py   # stream validation + timestamps   → functional + stability
   test_my_device_controls.py  # property get/set                 → functional
   ```

4. **Mark tests** with `hardware`, device marker, and category markers:
   ```python
   # device + functional tests
   pytestmark = [pytest.mark.hardware, pytest.mark.my_device, pytest.mark.functional]

   # stream tests (functional correctness + stability)
   pytestmark = [pytest.mark.hardware, pytest.mark.my_device,
                 pytest.mark.functional, pytest.mark.stability]
   ```

5. **Register the device alias** in `run_tests.py` under `_DEVICE_ALIASES` and `_DEVICE_NAME_PATTERNS`.
