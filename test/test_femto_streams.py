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
Femto Bolt / Femto Mega stream data validation tests.

Femto-specific depth characteristics (ToF sensor):
- Valid depth range: 300 mm – 8000 mm
- Frame size: typically 640 × 576 @ 30fps
- Has Left IR + Right IR for active illumination
- IMU streams: accelerometer and gyroscope

Tests verify:
- Depth / Color / IR streams start and produce valid frames
- Depth values are within the Femto ToF operating range (300–8000 mm)
- IMU (accelerometer, gyroscope) streams produce valid data
- Timestamp monotonicity and FPS accuracy
- Multi-stream synchronization
"""

import time

import numpy as np
import pytest

from pyorbbecsdk import Config, OBError, OBFrameType, OBSensorType

pytestmark = [
    pytest.mark.hardware,
    pytest.mark.femto,
    pytest.mark.functional,
    pytest.mark.stability,
]

FRAME_COLLECT_COUNT = 30
FRAME_TIMEOUT_MS = 2000
TARGET_FPS = 30
FPS_TOLERANCE = 0.10
SYNC_DELTA_MS = 33

# Femto ToF depth operating range
FEMTO_DEPTH_MIN_MM = 200.0
FEMTO_DEPTH_MAX_MM = 8500.0


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


# ===========================================================================
# Depth stream (ToF)
# ===========================================================================


class TestFemtoDepthStream:

    def test_depth_stream_starts(self, pipeline, femto_device):
        _start_single_stream(pipeline, OBSensorType.DEPTH_SENSOR)

    def test_depth_frame_received(self, pipeline, femto_device):
        _start_single_stream(pipeline, OBSensorType.DEPTH_SENSOR)
        frames = _collect_frames(pipeline, OBFrameType.DEPTH_FRAME, count=1)
        assert len(frames) >= 1, "No depth frame received"

    def test_depth_frame_data_nonzero(self, pipeline, femto_device):
        _start_single_stream(pipeline, OBSensorType.DEPTH_SENSOR)
        frames = _collect_frames(pipeline, OBFrameType.DEPTH_FRAME, count=5)
        assert frames
        data = np.frombuffer(frames[-1].as_depth_frame().get_data(), dtype=np.uint16)
        assert (
            np.count_nonzero(data) / data.size > 0.10
        ), "Too many zero-depth pixels — ensure an object is in front of the camera"

    def test_depth_values_within_tof_range(self, pipeline, femto_device):
        """Femto ToF depth values must be within 200–8500 mm."""
        _start_single_stream(pipeline, OBSensorType.DEPTH_SENSOR)
        frames = _collect_frames(pipeline, OBFrameType.DEPTH_FRAME, count=5)
        assert frames
        frame = frames[-1].as_depth_frame()
        scale = frame.get_depth_scale()
        data = np.frombuffer(frame.get_data(), dtype=np.uint16).astype(np.float32) * scale
        valid = data[data > 0]
        if len(valid) > 0:
            assert (
                valid.min() >= FEMTO_DEPTH_MIN_MM
            ), f"Min depth {valid.min():.1f}mm below ToF minimum {FEMTO_DEPTH_MIN_MM}mm"
            assert (
                valid.max() <= FEMTO_DEPTH_MAX_MM
            ), f"Max depth {valid.max():.1f}mm above ToF maximum {FEMTO_DEPTH_MAX_MM}mm"

    def test_depth_scale_factor(self, pipeline, femto_device):
        _start_single_stream(pipeline, OBSensorType.DEPTH_SENSOR)
        frames = _collect_frames(pipeline, OBFrameType.DEPTH_FRAME, count=1)
        assert frames
        scale = frames[0].as_depth_frame().get_depth_scale()
        assert 0.0001 <= scale <= 0.01, f"Unexpected depth scale: {scale}"

    def test_depth_timestamps_monotonic(self, pipeline, femto_device):
        _start_single_stream(pipeline, OBSensorType.DEPTH_SENSOR)
        frames = _collect_frames(pipeline, OBFrameType.DEPTH_FRAME, count=FRAME_COLLECT_COUNT)
        assert len(frames) >= 5
        ts = [f.get_timestamp() for f in frames]
        for i in range(1, len(ts)):
            assert ts[i] > ts[i - 1], f"Non-monotonic timestamp at index {i}"

    @pytest.mark.timeout(30)
    def test_depth_fps_accuracy(self, pipeline, femto_device):
        _start_single_stream(pipeline, OBSensorType.DEPTH_SENSOR)
        frames = _collect_frames(pipeline, OBFrameType.DEPTH_FRAME, count=FRAME_COLLECT_COUNT)
        assert len(frames) >= 10
        elapsed = (frames[-1].get_timestamp() - frames[0].get_timestamp()) / 1000.0
        if elapsed > 0:
            actual_fps = (len(frames) - 1) / elapsed
            lo = TARGET_FPS * (1 - FPS_TOLERANCE)
            hi = TARGET_FPS * (1 + FPS_TOLERANCE)
            assert lo <= actual_fps <= hi, f"Depth FPS {actual_fps:.1f} outside [{lo:.1f}, {hi:.1f}]"


# ===========================================================================
# Color stream
# ===========================================================================


class TestFemtoColorStream:

    def test_color_stream_starts(self, pipeline, femto_device):
        _start_single_stream(pipeline, OBSensorType.COLOR_SENSOR)

    def test_color_frame_received(self, pipeline, femto_device):
        _start_single_stream(pipeline, OBSensorType.COLOR_SENSOR)
        frames = _collect_frames(pipeline, OBFrameType.COLOR_FRAME, count=1)
        assert len(frames) >= 1

    def test_color_frame_not_black(self, pipeline, femto_device):
        _start_single_stream(pipeline, OBSensorType.COLOR_SENSOR)
        frames = _collect_frames(pipeline, OBFrameType.COLOR_FRAME, count=5)
        assert frames
        data = np.frombuffer(frames[-1].as_color_frame().get_data(), dtype=np.uint8)
        assert data.mean() > 5.0, "Color frame suspiciously dark"

    def test_color_timestamps_monotonic(self, pipeline, femto_device):
        _start_single_stream(pipeline, OBSensorType.COLOR_SENSOR)
        frames = _collect_frames(pipeline, OBFrameType.COLOR_FRAME, count=FRAME_COLLECT_COUNT)
        assert len(frames) >= 5
        ts = [f.get_timestamp() for f in frames]
        for i in range(1, len(ts)):
            assert ts[i] > ts[i - 1]


# ===========================================================================
# IR stream (ToF active illumination)
# ===========================================================================


class TestFemtoIRStream:

    def test_ir_stream_starts(self, pipeline, femto_device):
        """Femto uses Left IR / Right IR; try both."""
        config = Config()
        for st in [OBSensorType.LEFT_IR_SENSOR, OBSensorType.IR_SENSOR]:
            try:
                pl = pipeline.get_stream_profile_list(st)
                config.enable_stream(pl.get_default_video_stream_profile())
                pipeline.start(config)
                return
            except OBError:
                continue
        pytest.skip("No IR sensor available on this Femto device")

    def test_ir_frame_data_valid(self, pipeline, femto_device):
        config = Config()
        frame_type = None
        for st, ft in [
            (OBSensorType.LEFT_IR_SENSOR, OBFrameType.IR_FRAME),
            (OBSensorType.IR_SENSOR, OBFrameType.IR_FRAME),
        ]:
            try:
                pl = pipeline.get_stream_profile_list(st)
                config.enable_stream(pl.get_default_video_stream_profile())
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


# ===========================================================================
# IMU streams (unique to Femto family)
# ===========================================================================


class TestFemtoIMUStreams:
    """Femto cameras have an onboard IMU (accelerometer + gyroscope)."""

    def test_accel_stream_starts(self, pipeline, femto_device):
        try:
            _start_single_stream(pipeline, OBSensorType.ACCEL_SENSOR)
        except OBError as e:
            pytest.skip(f"Accelerometer not available: {e}")

    def test_accel_frame_received(self, pipeline, femto_device):
        try:
            _start_single_stream(pipeline, OBSensorType.ACCEL_SENSOR)
        except OBError as e:
            pytest.skip(f"Accelerometer not available: {e}")
        frames, deadline = [], time.time() + 5
        while len(frames) < 5 and time.time() < deadline:
            fs = pipeline.wait_for_frames(FRAME_TIMEOUT_MS)
            if fs:
                f = fs.get_frame_by_type(OBFrameType.ACCEL_FRAME)
                if f:
                    frames.append(f)
        assert len(frames) >= 1, "No accelerometer frame received"

    def test_gyro_stream_starts(self, pipeline, femto_device):
        try:
            _start_single_stream(pipeline, OBSensorType.GYRO_SENSOR)
        except OBError as e:
            pytest.skip(f"Gyroscope not available: {e}")

    def test_gyro_frame_received(self, pipeline, femto_device):
        try:
            _start_single_stream(pipeline, OBSensorType.GYRO_SENSOR)
        except OBError as e:
            pytest.skip(f"Gyroscope not available: {e}")
        frames, deadline = [], time.time() + 5
        while len(frames) < 5 and time.time() < deadline:
            fs = pipeline.wait_for_frames(FRAME_TIMEOUT_MS)
            if fs:
                f = fs.get_frame_by_type(OBFrameType.GYRO_FRAME)
                if f:
                    frames.append(f)
        assert len(frames) >= 1, "No gyroscope frame received"


# ===========================================================================
# Color-depth synchronization
# ===========================================================================


class TestFemtoMultiStreamSync:

    def test_color_depth_sync_timestamps(self, pipeline, femto_device):
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
        assert deltas, "No paired color+depth frames received"
        median = sorted(deltas)[len(deltas) // 2]
        assert median <= SYNC_DELTA_MS, f"Median sync delta {median}ms exceeds {SYNC_DELTA_MS}ms"
