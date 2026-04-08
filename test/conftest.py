# ******************************************************************************
#  Copyright (c) 2024 Orbbec 3D Technology, Inc
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
# ******************************************************************************
"""
pytest configuration and shared fixtures for pyorbbecsdk test suite.

Usage:
    pytest test/ -v                              # Run all tests (skip if no device)
    pytest test/ -v -m hardware                  # Only hardware tests
    pytest test/ -v -m "not hardware"            # Only non-hardware tests
    pytest test/ -v -m g300_series               # All G300 series tests
    pytest test/ -v -m femto                     # All Femto Bolt/Mega tests
    pytest test/ -v -m astra_mini                # All Astra Mini tests
    pytest test/ -v -m astra2                    # All Astra 2 tests
    pytest test/test_g300_series_*.py -v         # All G300 series test files
    pytest test/test_femto_*.py -v               # All Femto test files
    pytest test/ -m "not performance" -v         # Skip long benchmarks
"""

import time

import pytest

from pyorbbecsdk import (
    Config,
    Context,
    OBLogLevel,
    OBPermissionType,
    OBPropertyID,
    OBSensorType,
    Pipeline,
)

# ---------------------------------------------------------------------------
# Device name sets used for fixture matching
# ---------------------------------------------------------------------------

# Gemini 330 series: 330, 335, 335L, 335Le, 335Lg, 336, 336L, 330L, 335Le
_G300_NAME_PREFIXES = [
    "Gemini 330",
    "Gemini 335",
    "Gemini 336",
    "Gemini 305",
    "Gemini 345",
    "Gemini345",
    "Gemini305",
]

# Femto Bolt and Femto Mega family
_FEMTO_NAME_PREFIXES = ["Femto Bolt", "Femto Mega", "FemtoBolt", "FemtoMega"]

# Astra Mini Pro / S Pro
_ASTRA_MINI_NAME_PREFIXES = ["Astra Mini", "Astra mini"]

# Astra 2
_ASTRA2_NAME_PREFIXES = ["Astra 2", "Astra2"]


def _device_matches(name: str, prefixes: list) -> bool:
    name = name or ""
    return any(p in name for p in prefixes)


# ---------------------------------------------------------------------------
# Marker registration
# ---------------------------------------------------------------------------


def pytest_configure(config):
    config.addinivalue_line("markers", "hardware: test requires a physical Orbbec camera")
    config.addinivalue_line(
        "markers",
        "g300_series: test for G300 series cameras (Gemini 330/335/336/305/345)",
    )
    config.addinivalue_line("markers", "femto: test for Femto Bolt / Femto Mega cameras")
    config.addinivalue_line("markers", "astra_mini: test for Astra Mini Pro / S Pro cameras")
    config.addinivalue_line("markers", "astra2: test for Astra 2 cameras")
    config.addinivalue_line(
        "markers",
        "functional: API correctness — device info, stream start, sensor controls, calibration, filters",
    )
    config.addinivalue_line(
        "markers",
        "stability: multi-frame reliability — timestamp monotonicity, sync accuracy, drop rate",
    )
    config.addinivalue_line(
        "markers",
        "performance: long-running benchmark — FPS, latency, throughput (60+ seconds)",
    )


# ---------------------------------------------------------------------------
# Session-scoped device fixture (shared across all tests in one run)
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def context():
    """Create a shared SDK Context for the entire test session."""
    ctx = Context()
    ctx.set_logger_level(OBLogLevel.WARNING)
    yield ctx


@pytest.fixture(scope="session")
def device(context):
    """
    Return the first connected Orbbec device.
    Skip (not fail) when no device is connected.
    """
    device_list = context.query_devices()
    if device_list.get_count() == 0:
        pytest.skip("No Orbbec device connected — skipping hardware test")
    dev = device_list.get_device_by_index(0)
    yield dev


@pytest.fixture(scope="session")
def device_info(device):
    """Return device info object for the connected device."""
    return device.get_device_info()


# ---------------------------------------------------------------------------
# Device-specific fixtures — each skips if wrong model is connected
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def g300_series_device(device, device_info):
    """
    Return device for any G300 series camera:
    Gemini 330, 335, 335L, 335Le, 335Lg, 336, 336L, 330L, 305, 345.
    Skip if a different device family is connected.
    """
    name = device_info.get_name() or ""
    if not _device_matches(name, _G300_NAME_PREFIXES):
        pytest.skip(
            f"Connected device is '{name}', not a G300 series camera — skipping. "
            f"G300 series includes: Gemini 330/335/336/305/345 and their variants."
        )
    return device


@pytest.fixture(scope="session")
def femto_device(device, device_info):
    """
    Return device for Femto Bolt or Femto Mega cameras.
    Skip if a non-Femto device is connected.
    """
    name = device_info.get_name() or ""
    if not _device_matches(name, _FEMTO_NAME_PREFIXES):
        pytest.skip(
            f"Connected device is '{name}', not a Femto Bolt/Mega — skipping. "
            f"Femto series includes: Femto Bolt, Femto Mega, Femto Mega I."
        )
    return device


@pytest.fixture(scope="session")
def astra_mini_device(device, device_info):
    """
    Return device for Astra Mini Pro or Astra Mini S Pro cameras.
    Skip if a different device is connected.
    """
    name = device_info.get_name() or ""
    if not _device_matches(name, _ASTRA_MINI_NAME_PREFIXES):
        pytest.skip(
            f"Connected device is '{name}', not an Astra Mini — skipping. "
            f"Astra Mini series includes: Astra Mini Pro, Astra Mini S Pro."
        )
    return device


@pytest.fixture(scope="session")
def astra2_device(device, device_info):
    """
    Return device for Astra 2 cameras.
    Skip if a different device is connected.
    """
    name = device_info.get_name() or ""
    if not _device_matches(name, _ASTRA2_NAME_PREFIXES):
        pytest.skip(f"Connected device is '{name}', not an Astra 2 — skipping.")
    return device


# ---------------------------------------------------------------------------
# Function-scoped pipeline fixture (fresh pipeline per test)
# ---------------------------------------------------------------------------


@pytest.fixture
def pipeline(device):
    """Create a fresh Pipeline per test, guaranteed to be stopped after."""
    pipe = Pipeline(device)
    yield pipe
    try:
        pipe.stop()
    except Exception:
        pass


# ---------------------------------------------------------------------------
# Helper fixtures for sensor control tests
# ---------------------------------------------------------------------------


@pytest.fixture
def disable_depth_auto_exposure(device):
    """
    Context manager fixture: disables depth auto-exposure before the test,
    restores it afterwards.
    """
    prop = OBPropertyID.OB_PROP_DEPTH_AUTO_EXPOSURE_BOOL
    perm = OBPermissionType.PERMISSION_READ_WRITE
    supported = device.is_property_supported(prop, perm)
    if supported:
        original = device.get_bool_property(prop)
        device.set_bool_property(prop, False)
    yield
    if supported:
        device.set_bool_property(prop, original)


@pytest.fixture
def disable_color_auto_exposure(device):
    prop = OBPropertyID.OB_PROP_COLOR_AUTO_EXPOSURE_BOOL
    perm = OBPermissionType.PERMISSION_READ_WRITE
    supported = device.is_property_supported(prop, perm)
    if supported:
        original = device.get_bool_property(prop)
        device.set_bool_property(prop, False)
    yield
    if supported:
        device.set_bool_property(prop, original)


@pytest.fixture
def disable_ir_auto_exposure(device):
    prop = OBPropertyID.OB_PROP_IR_AUTO_EXPOSURE_BOOL
    perm = OBPermissionType.PERMISSION_READ_WRITE
    supported = device.is_property_supported(prop, perm)
    if supported:
        original = device.get_bool_property(prop)
        device.set_bool_property(prop, False)
    yield
    if supported:
        device.set_bool_property(prop, original)


# ---------------------------------------------------------------------------
# Utility helpers (not fixtures)
# ---------------------------------------------------------------------------


def collect_frames(pipeline, sensor_type, count=30, timeout_ms=2000):
    """
    Start pipeline with the default profile for `sensor_type`,
    collect `count` frames, then stop. Returns list of frames.
    """
    config = Config()
    profile_list = pipeline.get_stream_profile_list(sensor_type)
    profile = profile_list.get_default_video_stream_profile()
    config.enable_stream(profile)
    pipeline.start(config)

    frames = []
    deadline = time.time() + (count * (1.0 / 30) * 3)  # generous timeout
    while len(frames) < count and time.time() < deadline:
        frame_set = pipeline.wait_for_frames(timeout_ms)
        if frame_set is None:
            continue
        frame = frame_set.get_frame_by_type(_sensor_to_frame_type(sensor_type))
        if frame is not None:
            frames.append(frame)

    pipeline.stop()
    return frames


def _sensor_to_frame_type(sensor_type):
    from pyorbbecsdk import OBFrameType

    mapping = {
        OBSensorType.DEPTH_SENSOR: OBFrameType.DEPTH_FRAME,
        OBSensorType.COLOR_SENSOR: OBFrameType.COLOR_FRAME,
        OBSensorType.IR_SENSOR: OBFrameType.IR_FRAME,
        OBSensorType.LEFT_IR_SENSOR: OBFrameType.IR_FRAME,
        OBSensorType.RIGHT_IR_SENSOR: OBFrameType.IR_FRAME,
        OBSensorType.ACCEL_SENSOR: OBFrameType.ACCEL_FRAME,
        OBSensorType.GYRO_SENSOR: OBFrameType.GYRO_FRAME,
    }
    return mapping.get(sensor_type, OBFrameType.DEPTH_FRAME)
