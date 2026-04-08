# ******************************************************************************
#  Copyright (c) 2024 Orbbec 3D Technology, Inc
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
# ******************************************************************************
"""
Astra Mini Pro / Astra Mini S Pro stream data validation tests.

Astra Mini depth characteristics:
- Structured light sensor
- Valid depth range: 300 mm – 8000 mm
- Typical resolution: 640 × 480 @ 30fps
- Has IR sensor for structured light pattern
"""

import time

import numpy as np
import pytest

from pyorbbecsdk import Config, OBError, OBFrameType, OBSensorType

pytestmark = [
    pytest.mark.hardware,
    pytest.mark.astra_mini,
    pytest.mark.functional,
    pytest.mark.stability,
]

FRAME_COLLECT_COUNT = 30
FRAME_TIMEOUT_MS = 2000
TARGET_FPS = 30
FPS_TOLERANCE = 0.15  # slightly relaxed for compact camera
SYNC_DELTA_MS = 50  # relaxed for USB 2.0 devices

ASTRA_MINI_DEPTH_MIN_MM = 200.0
ASTRA_MINI_DEPTH_MAX_MM = 8500.0


def _start_single_stream(pipeline, sensor_type):
    config = Config()
    pl = pipeline.get_stream_profile_list(sensor_type)
    config.enable_stream(pl.get_default_video_stream_profile())
    pipeline.start(config)


def _collect_frames(pipeline, frame_type, count, timeout_ms=FRAME_TIMEOUT_MS):
    frames, deadline = [], time.time() + count * (1.0 / TARGET_FPS) * 5
    while len(frames) < count and time.time() < deadline:
        fs = pipeline.wait_for_frames(timeout_ms)
        if fs:
            f = fs.get_frame_by_type(frame_type)
            if f:
                frames.append(f)
    return frames


class TestAstraMiniDepthStream:

    def test_depth_stream_starts(self, pipeline, astra_mini_device):
        _start_single_stream(pipeline, OBSensorType.DEPTH_SENSOR)

    def test_depth_frame_received(self, pipeline, astra_mini_device):
        _start_single_stream(pipeline, OBSensorType.DEPTH_SENSOR)
        frames = _collect_frames(pipeline, OBFrameType.DEPTH_FRAME, count=1)
        assert len(frames) >= 1, "No depth frame received"

    def test_depth_frame_data_nonzero(self, pipeline, astra_mini_device):
        _start_single_stream(pipeline, OBSensorType.DEPTH_SENSOR)
        frames = _collect_frames(pipeline, OBFrameType.DEPTH_FRAME, count=5)
        assert frames
        data = np.frombuffer(frames[-1].as_depth_frame().get_data(), dtype=np.uint16)
        assert np.count_nonzero(data) / data.size > 0.10, "Too many zero-depth pixels"

    def test_depth_values_within_range(self, pipeline, astra_mini_device):
        _start_single_stream(pipeline, OBSensorType.DEPTH_SENSOR)
        frames = _collect_frames(pipeline, OBFrameType.DEPTH_FRAME, count=5)
        assert frames
        frame = frames[-1].as_depth_frame()
        scale = frame.get_depth_scale()
        data = np.frombuffer(frame.get_data(), dtype=np.uint16).astype(np.float32) * scale
        valid = data[data > 0]
        if len(valid) > 0:
            assert valid.min() >= ASTRA_MINI_DEPTH_MIN_MM
            assert valid.max() <= ASTRA_MINI_DEPTH_MAX_MM

    def test_depth_timestamps_monotonic(self, pipeline, astra_mini_device):
        _start_single_stream(pipeline, OBSensorType.DEPTH_SENSOR)
        frames = _collect_frames(pipeline, OBFrameType.DEPTH_FRAME, count=FRAME_COLLECT_COUNT)
        assert len(frames) >= 5
        ts = [f.get_timestamp() for f in frames]
        for i in range(1, len(ts)):
            assert ts[i] > ts[i - 1]

    @pytest.mark.timeout(30)
    def test_depth_fps_accuracy(self, pipeline, astra_mini_device):
        _start_single_stream(pipeline, OBSensorType.DEPTH_SENSOR)
        frames = _collect_frames(pipeline, OBFrameType.DEPTH_FRAME, count=FRAME_COLLECT_COUNT)
        assert len(frames) >= 10
        elapsed = (frames[-1].get_timestamp() - frames[0].get_timestamp()) / 1000.0
        if elapsed > 0:
            actual_fps = (len(frames) - 1) / elapsed
            lo = TARGET_FPS * (1 - FPS_TOLERANCE)
            hi = TARGET_FPS * (1 + FPS_TOLERANCE)
            assert lo <= actual_fps <= hi, f"Depth FPS {actual_fps:.1f} outside [{lo:.1f}, {hi:.1f}]"


class TestAstraMiniColorStream:

    def test_color_stream_starts(self, pipeline, astra_mini_device):
        try:
            _start_single_stream(pipeline, OBSensorType.COLOR_SENSOR)
        except OBError as e:
            pytest.skip(f"Color sensor not available on this Astra Mini variant: {e}")

    def test_color_frame_received(self, pipeline, astra_mini_device):
        try:
            _start_single_stream(pipeline, OBSensorType.COLOR_SENSOR)
        except OBError as e:
            pytest.skip(f"Color sensor not available: {e}")
        frames = _collect_frames(pipeline, OBFrameType.COLOR_FRAME, count=1)
        assert len(frames) >= 1

    def test_color_frame_not_black(self, pipeline, astra_mini_device):
        try:
            _start_single_stream(pipeline, OBSensorType.COLOR_SENSOR)
        except OBError as e:
            pytest.skip(f"Color sensor not available: {e}")
        frames = _collect_frames(pipeline, OBFrameType.COLOR_FRAME, count=5)
        assert frames
        data = np.frombuffer(frames[-1].as_color_frame().get_data(), dtype=np.uint8)
        assert data.mean() > 5.0, "Color frame suspiciously dark"


class TestAstraMiniIRStream:

    def test_ir_stream_starts(self, pipeline, astra_mini_device):
        config = Config()
        for st in [OBSensorType.IR_SENSOR, OBSensorType.LEFT_IR_SENSOR]:
            try:
                pl = pipeline.get_stream_profile_list(st)
                config.enable_stream(pl.get_default_video_stream_profile())
                pipeline.start(config)
                return
            except OBError:
                continue
        pytest.skip("No IR sensor available on this device")

    def test_ir_frame_data_valid(self, pipeline, astra_mini_device):
        config = Config()
        frame_type = None
        for st, ft in [
            (OBSensorType.IR_SENSOR, OBFrameType.IR_FRAME),
            (OBSensorType.LEFT_IR_SENSOR, OBFrameType.IR_FRAME),
        ]:
            try:
                config.enable_stream(pipeline.get_stream_profile_list(st).get_default_video_stream_profile())
                frame_type = ft
                break
            except OBError:
                continue
        if frame_type is None:
            pytest.skip("No IR sensor available")
        pipeline.start(config)
        frames = _collect_frames(pipeline, frame_type, count=5)
        assert frames
        assert np.frombuffer(frames[-1].get_data(), dtype=np.uint8).mean() > 0


class TestAstraMiniControls:
    """Basic sensor controls applicable to Astra Mini."""

    def test_depth_mirror_toggle(self, astra_mini_device):
        from pyorbbecsdk import OBPermissionType, OBPropertyID

        prop = OBPropertyID.OB_PROP_DEPTH_MIRROR_BOOL
        if not astra_mini_device.is_property_supported(prop, OBPermissionType.PERMISSION_READ_WRITE):
            pytest.skip("Mirror property not supported")
        original = astra_mini_device.get_bool_property(prop)
        astra_mini_device.set_bool_property(prop, not original)
        assert astra_mini_device.get_bool_property(prop) == (not original)
        astra_mini_device.set_bool_property(prop, original)

    def test_color_auto_exposure_toggle(self, astra_mini_device):
        from pyorbbecsdk import OBPermissionType, OBPropertyID

        prop = OBPropertyID.OB_PROP_COLOR_AUTO_EXPOSURE_BOOL
        if not astra_mini_device.is_property_supported(prop, OBPermissionType.PERMISSION_READ_WRITE):
            pytest.skip("Color auto-exposure not supported")
        original = astra_mini_device.get_bool_property(prop)
        astra_mini_device.set_bool_property(prop, not original)
        assert astra_mini_device.get_bool_property(prop) == (not original)
        astra_mini_device.set_bool_property(prop, original)
