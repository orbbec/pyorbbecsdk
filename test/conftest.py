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
    pytest test/ -v                          # Run all tests (skip if no device)
    pytest test/ -v -m hardware              # Only hardware tests
    pytest test/ -v -m "not hardware"        # Only non-hardware tests
    pytest test/ -v -m gemini335            # Only Gemini 335 tests
    pytest test/test_gemini335_*.py -v      # All Gemini 335 tests
"""

import time
import pytest

from pyorbbecsdk import (
    Context,
    Pipeline,
    Config,
    OBSensorType,
    OBPropertyID,
    OBPermissionType,
    OBLogLevel,
)


# ---------------------------------------------------------------------------
# Marker registration
# ---------------------------------------------------------------------------

def pytest_configure(config):
    config.addinivalue_line("markers", "hardware: test requires a physical Orbbec camera")
    config.addinivalue_line("markers", "gemini335: test specific to Gemini 335 camera")
    config.addinivalue_line("markers", "performance: long-running performance benchmark")


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


@pytest.fixture(scope="session")
def gemini335_device(device, device_info):
    """
    Return a device only if it is a Gemini 335 (or 335L / 335Le).
    Skip otherwise so Gemini 335-specific tests are not run on other cameras.
    """
    name = device_info.get_name() or ""
    if "Gemini 335" not in name and "Gemini335" not in name:
        pytest.skip(f"Connected device is '{name}', not Gemini 335 — skipping")
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
        frame = frame_set.get_frame_by_type(
            _sensor_to_frame_type(sensor_type)
        )
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
    }
    return mapping.get(sensor_type, OBFrameType.DEPTH_FRAME)
