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
Astra 2 stream data validation tests.

Astra 2 depth characteristics:
- Structured light sensor, wider range than Astra Mini
- Valid depth range: 300 mm – 10 000 mm
- Typical resolution: 640 × 480 @ 30fps
- Has Color and IR sensors

Tests verify stream data validity, FPS, timestamp monotonicity,
and color↔depth synchronization.
"""

import time

import numpy as np
import pytest

from pyorbbecsdk import Config, OBError, OBFrameType, OBSensorType

pytestmark = [
    pytest.mark.hardware,
    pytest.mark.astra2,
    pytest.mark.functional,
    pytest.mark.stability,
]

FRAME_COLLECT_COUNT = 30
FRAME_TIMEOUT_MS = 2000
TARGET_FPS = 30
FPS_TOLERANCE = 0.15
SYNC_DELTA_MS = 50

ASTRA2_DEPTH_MIN_MM = 200.0
ASTRA2_DEPTH_MAX_MM = 10500.0


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


class TestAstra2DepthStream:

    def test_depth_stream_starts(self, pipeline, astra2_device):
        _start_single_stream(pipeline, OBSensorType.DEPTH_SENSOR)

    def test_depth_frame_received(self, pipeline, astra2_device):
        _start_single_stream(pipeline, OBSensorType.DEPTH_SENSOR)
        frames = _collect_frames(pipeline, OBFrameType.DEPTH_FRAME, count=1)
        assert len(frames) >= 1

    def test_depth_frame_dimensions_match_profile(self, pipeline, astra2_device):
        config = Config()
        pl = pipeline.get_stream_profile_list(OBSensorType.DEPTH_SENSOR)
        profile = pl.get_default_video_stream_profile()
        config.enable_stream(profile)
        pipeline.start(config)
        frames = _collect_frames(pipeline, OBFrameType.DEPTH_FRAME, count=1)
        assert frames
        frame = frames[0].as_depth_frame()
        assert frame.get_width() == profile.get_width()
        assert frame.get_height() == profile.get_height()

    def test_depth_frame_data_nonzero(self, pipeline, astra2_device):
        _start_single_stream(pipeline, OBSensorType.DEPTH_SENSOR)
        frames = _collect_frames(pipeline, OBFrameType.DEPTH_FRAME, count=5)
        assert frames
        data = np.frombuffer(frames[-1].as_depth_frame().get_data(), dtype=np.uint16)
        assert np.count_nonzero(data) / data.size > 0.10

    def test_depth_values_within_astra2_range(self, pipeline, astra2_device):
        """Astra 2 depth range is wider than Astra Mini: up to 10 m."""
        _start_single_stream(pipeline, OBSensorType.DEPTH_SENSOR)
        frames = _collect_frames(pipeline, OBFrameType.DEPTH_FRAME, count=5)
        assert frames
        frame = frames[-1].as_depth_frame()
        scale = frame.get_depth_scale()
        data = np.frombuffer(frame.get_data(), dtype=np.uint16).astype(np.float32) * scale
        valid = data[data > 0]
        if len(valid) > 0:
            assert valid.min() >= ASTRA2_DEPTH_MIN_MM
            assert valid.max() <= ASTRA2_DEPTH_MAX_MM

    def test_depth_timestamps_monotonic(self, pipeline, astra2_device):
        _start_single_stream(pipeline, OBSensorType.DEPTH_SENSOR)
        frames = _collect_frames(pipeline, OBFrameType.DEPTH_FRAME, count=FRAME_COLLECT_COUNT)
        assert len(frames) >= 5
        ts = [f.get_timestamp() for f in frames]
        for i in range(1, len(ts)):
            assert ts[i] > ts[i - 1]

    @pytest.mark.timeout(30)
    def test_depth_fps_accuracy(self, pipeline, astra2_device):
        _start_single_stream(pipeline, OBSensorType.DEPTH_SENSOR)
        frames = _collect_frames(pipeline, OBFrameType.DEPTH_FRAME, count=FRAME_COLLECT_COUNT)
        assert len(frames) >= 10
        elapsed = (frames[-1].get_timestamp() - frames[0].get_timestamp()) / 1000.0
        if elapsed > 0:
            actual_fps = (len(frames) - 1) / elapsed
            assert TARGET_FPS * (1 - FPS_TOLERANCE) <= actual_fps <= TARGET_FPS * (1 + FPS_TOLERANCE)


class TestAstra2ColorStream:

    def test_color_stream_starts(self, pipeline, astra2_device):
        _start_single_stream(pipeline, OBSensorType.COLOR_SENSOR)

    def test_color_frame_received(self, pipeline, astra2_device):
        _start_single_stream(pipeline, OBSensorType.COLOR_SENSOR)
        frames = _collect_frames(pipeline, OBFrameType.COLOR_FRAME, count=1)
        assert len(frames) >= 1

    def test_color_frame_not_black(self, pipeline, astra2_device):
        _start_single_stream(pipeline, OBSensorType.COLOR_SENSOR)
        frames = _collect_frames(pipeline, OBFrameType.COLOR_FRAME, count=5)
        assert frames
        data = np.frombuffer(frames[-1].as_color_frame().get_data(), dtype=np.uint8)
        assert data.mean() > 5.0

    def test_color_timestamps_monotonic(self, pipeline, astra2_device):
        _start_single_stream(pipeline, OBSensorType.COLOR_SENSOR)
        frames = _collect_frames(pipeline, OBFrameType.COLOR_FRAME, count=FRAME_COLLECT_COUNT)
        assert len(frames) >= 5
        ts = [f.get_timestamp() for f in frames]
        for i in range(1, len(ts)):
            assert ts[i] > ts[i - 1]


class TestAstra2IRStream:

    def test_ir_stream_starts(self, pipeline, astra2_device):
        config = Config()
        for st in [OBSensorType.IR_SENSOR, OBSensorType.LEFT_IR_SENSOR]:
            try:
                config.enable_stream(pipeline.get_stream_profile_list(st).get_default_video_stream_profile())
                pipeline.start(config)
                return
            except OBError:
                continue
        pytest.skip("No IR sensor available")

    def test_ir_frame_data_valid(self, pipeline, astra2_device):
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
        if not frame_type:
            pytest.skip("No IR sensor available")
        pipeline.start(config)
        frames = _collect_frames(pipeline, frame_type, count=5)
        assert frames
        assert np.frombuffer(frames[-1].get_data(), dtype=np.uint8).mean() > 0


class TestAstra2MultiStreamSync:

    def test_color_depth_sync_timestamps(self, pipeline, astra2_device):
        config = Config()
        try:
            config.enable_stream(
                pipeline.get_stream_profile_list(OBSensorType.DEPTH_SENSOR).get_default_video_stream_profile()
            )
            config.enable_stream(
                pipeline.get_stream_profile_list(OBSensorType.COLOR_SENSOR).get_default_video_stream_profile()
            )
        except OBError as e:
            pytest.skip(f"Dual stream not available: {e}")
        pipeline.start(config)

        deltas, deadline = [], time.time() + 15
        while len(deltas) < 20 and time.time() < deadline:
            fs = pipeline.wait_for_frames(FRAME_TIMEOUT_MS)
            if fs:
                d, c = fs.get_depth_frame(), fs.get_color_frame()
                if d and c:
                    deltas.append(abs(c.get_timestamp() - d.get_timestamp()))
        assert deltas
        median = sorted(deltas)[len(deltas) // 2]
        assert median <= SYNC_DELTA_MS, f"Median sync delta {median}ms exceeds {SYNC_DELTA_MS}ms"


class TestAstra2Controls:
    """Basic sensor controls for Astra 2."""

    def test_depth_mirror_toggle(self, astra2_device):
        from pyorbbecsdk import OBPermissionType, OBPropertyID

        prop = OBPropertyID.OB_PROP_DEPTH_MIRROR_BOOL
        if not astra2_device.is_property_supported(prop, OBPermissionType.PERMISSION_READ_WRITE):
            pytest.skip("Mirror property not supported")
        original = astra2_device.get_bool_property(prop)
        astra2_device.set_bool_property(prop, not original)
        assert astra2_device.get_bool_property(prop) == (not original)
        astra2_device.set_bool_property(prop, original)

    def test_color_auto_exposure_toggle(self, astra2_device):
        from pyorbbecsdk import OBPermissionType, OBPropertyID

        prop = OBPropertyID.OB_PROP_COLOR_AUTO_EXPOSURE_BOOL
        if not astra2_device.is_property_supported(prop, OBPermissionType.PERMISSION_READ_WRITE):
            pytest.skip("Color auto-exposure not supported")
        original = astra2_device.get_bool_property(prop)
        astra2_device.set_bool_property(prop, not original)
        assert astra2_device.get_bool_property(prop) == (not original)
        astra2_device.set_bool_property(prop, original)

    def test_laser_toggle(self, astra2_device):
        from pyorbbecsdk import OBPermissionType, OBPropertyID

        prop = OBPropertyID.OB_PROP_LASER_BOOL
        if not astra2_device.is_property_supported(prop, OBPermissionType.PERMISSION_READ_WRITE):
            pytest.skip("Laser property not supported")
        original = astra2_device.get_bool_property(prop)
        astra2_device.set_bool_property(prop, not original)
        assert astra2_device.get_bool_property(prop) == (not original)
        astra2_device.set_bool_property(prop, original)
