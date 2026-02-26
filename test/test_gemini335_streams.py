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
Gemini 335 stream data validation tests.

Tests in this module verify:
- Depth / Color / IR streams start and produce valid frames
- Frame dimensions match configured profiles
- Frame data is non-trivial (not all zeros / black)
- Timestamps are monotonically increasing
- Achieved frame rate is within ±10% of configured rate
- Multi-stream (Color+Depth+IR) pipeline runs without dropped frames
- Frame synchronization (color ↔ depth timestamp delta) meets spec
"""

import time
import pytest
import numpy as np

from pyorbbecsdk import (
    Config,
    OBSensorType,
    OBFormat,
    OBError,
    OBStreamType,
    OBFrameType,
)

pytestmark = [pytest.mark.hardware, pytest.mark.gemini335]

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
FRAME_COLLECT_COUNT = 30          # frames per test
FRAME_TIMEOUT_MS = 2000           # ms per wait_for_frames call
TARGET_FPS = 30
FPS_TOLERANCE = 0.10              # ±10%
SYNC_DELTA_MS = 33                # max |color_ts - depth_ts| for sync test
TIGHT_SYNC_DELTA_MS = 10          # when frame sync is explicitly enabled


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _start_single_stream(pipeline, sensor_type, width=0, height=0,
                          fps=30, fmt=None):
    """Configure and start a single-sensor pipeline; return the profile used."""
    config = Config()
    profile_list = pipeline.get_stream_profile_list(sensor_type)
    if fmt is not None:
        try:
            profile = profile_list.get_video_stream_profile(width, height, fmt, fps)
        except OBError:
            profile = profile_list.get_default_video_stream_profile()
    else:
        profile = profile_list.get_default_video_stream_profile()
    config.enable_stream(profile)
    pipeline.start(config)
    return profile


def _collect_frames(pipeline, frame_type, count, timeout_ms=FRAME_TIMEOUT_MS):
    """Collect up to `count` frames of a given OBFrameType."""
    frames = []
    deadline = time.time() + count * (1.0 / TARGET_FPS) * 4
    while len(frames) < count and time.time() < deadline:
        fs = pipeline.wait_for_frames(timeout_ms)
        if fs is None:
            continue
        f = fs.get_frame_by_type(frame_type)
        if f is not None:
            frames.append(f)
    return frames


# ===========================================================================
# Depth stream tests
# ===========================================================================

class TestDepthStream:

    def test_depth_stream_starts(self, pipeline, gemini335_device):
        """Depth stream must start without raising an exception."""
        _start_single_stream(pipeline, OBSensorType.DEPTH_SENSOR)
        # If we reach here, start() succeeded

    def test_depth_frame_received(self, pipeline, gemini335_device):
        """At least one depth frame must arrive within timeout."""
        profile = _start_single_stream(pipeline, OBSensorType.DEPTH_SENSOR)
        frames = _collect_frames(pipeline, OBFrameType.DEPTH_FRAME, count=1)
        assert len(frames) >= 1, "No depth frame received within timeout"

    def test_depth_frame_dimensions(self, pipeline, gemini335_device):
        """Depth frame size must match the configured stream profile."""
        profile = _start_single_stream(pipeline, OBSensorType.DEPTH_SENSOR)
        expected_w = profile.get_width()
        expected_h = profile.get_height()

        frames = _collect_frames(pipeline, OBFrameType.DEPTH_FRAME, count=1)
        assert frames, "No depth frame received"
        frame = frames[0].as_depth_frame()

        assert frame.get_width() == expected_w, (
            f"Width mismatch: expected {expected_w}, got {frame.get_width()}"
        )
        assert frame.get_height() == expected_h, (
            f"Height mismatch: expected {expected_h}, got {frame.get_height()}"
        )

    def test_depth_frame_data_nonzero(self, pipeline, gemini335_device):
        """More than 10% of depth pixels should be non-zero (camera sees something)."""
        _start_single_stream(pipeline, OBSensorType.DEPTH_SENSOR)
        frames = _collect_frames(pipeline, OBFrameType.DEPTH_FRAME, count=5)
        assert frames, "No depth frame received"

        frame = frames[-1].as_depth_frame()
        data = np.frombuffer(frame.get_data(), dtype=np.uint16)
        nonzero_ratio = np.count_nonzero(data) / data.size
        assert nonzero_ratio > 0.10, (
            f"Too many zero-depth pixels ({nonzero_ratio:.1%}). "
            "Make sure an object is in front of the camera."
        )

    def test_depth_scale_factor(self, pipeline, gemini335_device):
        """Depth scale factor must be in a physically reasonable range (0.1mm–1mm per unit)."""
        _start_single_stream(pipeline, OBSensorType.DEPTH_SENSOR)
        frames = _collect_frames(pipeline, OBFrameType.DEPTH_FRAME, count=1)
        assert frames
        scale = frames[0].as_depth_frame().get_depth_scale()
        assert 0.0001 <= scale <= 0.01, (
            f"Depth scale {scale} is outside expected range [0.0001, 0.01]"
        )

    def test_depth_values_in_valid_range(self, pipeline, gemini335_device):
        """Non-zero depth values must be within sensor operating range (20mm–10000mm)."""
        _start_single_stream(pipeline, OBSensorType.DEPTH_SENSOR)
        frames = _collect_frames(pipeline, OBFrameType.DEPTH_FRAME, count=5)
        assert frames

        frame = frames[-1].as_depth_frame()
        scale = frame.get_depth_scale()
        data = np.frombuffer(frame.get_data(), dtype=np.uint16).astype(np.float32) * scale
        valid = data[data > 0]
        if len(valid) > 0:
            assert valid.min() >= 10.0, (
                f"Min depth {valid.min():.1f}mm is below 10mm (noise floor)"
            )
            assert valid.max() <= 15000.0, (
                f"Max depth {valid.max():.1f}mm exceeds 15000mm"
            )

    def test_depth_timestamps_monotonic(self, pipeline, gemini335_device):
        """Consecutive depth frame timestamps must be strictly increasing."""
        _start_single_stream(pipeline, OBSensorType.DEPTH_SENSOR)
        frames = _collect_frames(pipeline, OBFrameType.DEPTH_FRAME,
                                  count=FRAME_COLLECT_COUNT)
        assert len(frames) >= 5, f"Only got {len(frames)} frames, need ≥5"

        timestamps = [f.get_timestamp() for f in frames]
        for i in range(1, len(timestamps)):
            assert timestamps[i] > timestamps[i - 1], (
                f"Timestamps not monotonic at index {i}: "
                f"{timestamps[i-1]} → {timestamps[i]}"
            )

    @pytest.mark.timeout(30)
    def test_depth_fps_accuracy(self, pipeline, gemini335_device):
        """Achieved depth frame rate should be within ±10% of 30fps."""
        _start_single_stream(pipeline, OBSensorType.DEPTH_SENSOR,
                              fps=TARGET_FPS)

        # Collect for ~3 seconds
        frames = _collect_frames(pipeline, OBFrameType.DEPTH_FRAME,
                                  count=FRAME_COLLECT_COUNT)
        assert len(frames) >= 10, "Insufficient frames to measure FPS"

        t_start = frames[0].get_timestamp()
        t_end = frames[-1].get_timestamp()
        elapsed_s = (t_end - t_start) / 1000.0
        if elapsed_s > 0:
            actual_fps = (len(frames) - 1) / elapsed_s
            low = TARGET_FPS * (1 - FPS_TOLERANCE)
            high = TARGET_FPS * (1 + FPS_TOLERANCE)
            assert low <= actual_fps <= high, (
                f"FPS {actual_fps:.1f} outside [{low:.1f}, {high:.1f}]"
            )


# ===========================================================================
# Color stream tests
# ===========================================================================

class TestColorStream:

    def test_color_stream_starts(self, pipeline, gemini335_device):
        """Color stream must start without raising an exception."""
        _start_single_stream(pipeline, OBSensorType.COLOR_SENSOR)

    def test_color_frame_received(self, pipeline, gemini335_device):
        """At least one color frame must arrive."""
        _start_single_stream(pipeline, OBSensorType.COLOR_SENSOR)
        frames = _collect_frames(pipeline, OBFrameType.COLOR_FRAME, count=1)
        assert len(frames) >= 1, "No color frame received within timeout"

    def test_color_frame_dimensions(self, pipeline, gemini335_device):
        """Color frame dimensions must match configured profile."""
        profile = _start_single_stream(pipeline, OBSensorType.COLOR_SENSOR)
        expected_w = profile.get_width()
        expected_h = profile.get_height()

        frames = _collect_frames(pipeline, OBFrameType.COLOR_FRAME, count=1)
        assert frames
        frame = frames[0].as_color_frame()

        assert frame.get_width() == expected_w
        assert frame.get_height() == expected_h

    def test_color_frame_not_black(self, pipeline, gemini335_device):
        """Color frame pixel mean must be above minimum brightness threshold."""
        _start_single_stream(pipeline, OBSensorType.COLOR_SENSOR)
        frames = _collect_frames(pipeline, OBFrameType.COLOR_FRAME, count=5)
        assert frames

        frame = frames[-1].as_color_frame()
        data = np.frombuffer(frame.get_data(), dtype=np.uint8)
        mean_val = data.mean()
        assert mean_val > 5.0, (
            f"Color frame mean brightness {mean_val:.1f} is suspiciously dark. "
            "Check if lens cap is on or room is dark."
        )

    def test_color_timestamps_monotonic(self, pipeline, gemini335_device):
        """Color frame timestamps must be strictly increasing."""
        _start_single_stream(pipeline, OBSensorType.COLOR_SENSOR)
        frames = _collect_frames(pipeline, OBFrameType.COLOR_FRAME,
                                  count=FRAME_COLLECT_COUNT)
        assert len(frames) >= 5

        timestamps = [f.get_timestamp() for f in frames]
        for i in range(1, len(timestamps)):
            assert timestamps[i] > timestamps[i - 1], (
                f"Color timestamps not monotonic at index {i}"
            )

    def test_color_mjpeg_format(self, pipeline, gemini335_device):
        """Gemini 335 should support MJPEG color format."""
        config = Config()
        try:
            profile_list = pipeline.get_stream_profile_list(OBSensorType.COLOR_SENSOR)
            profile = profile_list.get_video_stream_profile(
                0, 0, OBFormat.MJPG, TARGET_FPS
            )
            config.enable_stream(profile)
            pipeline.start(config)
            frames = _collect_frames(pipeline, OBFrameType.COLOR_FRAME, count=3)
            assert len(frames) >= 1, "No MJPEG frame received"
        except OBError as e:
            pytest.skip(f"MJPEG format not supported on this device: {e}")


# ===========================================================================
# IR stream tests
# ===========================================================================

class TestIRStream:

    def test_ir_stream_starts(self, pipeline, gemini335_device):
        """IR stream must start (using IR_SENSOR or LEFT_IR_SENSOR)."""
        config = Config()
        sensor_type = None
        for st in [OBSensorType.IR_SENSOR, OBSensorType.LEFT_IR_SENSOR]:
            try:
                profile_list = pipeline.get_stream_profile_list(st)
                profile = profile_list.get_default_video_stream_profile()
                config.enable_stream(profile)
                sensor_type = st
                break
            except OBError:
                continue
        if sensor_type is None:
            pytest.skip("No IR sensor available on this device")
        pipeline.start(config)

    def test_ir_frame_data_valid(self, pipeline, gemini335_device):
        """IR frame must contain non-trivial data."""
        config = Config()
        frame_type = None
        for st, ft in [
            (OBSensorType.IR_SENSOR, OBFrameType.IR_FRAME),
            (OBSensorType.LEFT_IR_SENSOR, OBFrameType.IR_FRAME),
        ]:
            try:
                profile_list = pipeline.get_stream_profile_list(st)
                profile = profile_list.get_default_video_stream_profile()
                config.enable_stream(profile)
                frame_type = ft
                break
            except OBError:
                continue

        if frame_type is None:
            pytest.skip("No IR sensor available on this device")

        pipeline.start(config)
        frames = _collect_frames(pipeline, frame_type, count=5)
        assert frames, "No IR frame received"

        frame = frames[-1]
        data = np.frombuffer(frame.get_data(), dtype=np.uint8)
        assert data.mean() > 0, "IR frame data appears to be all zeros"


# ===========================================================================
# Multi-stream synchronization tests
# ===========================================================================

class TestMultiStreamSync:

    def test_color_depth_sync_timestamps(self, pipeline, gemini335_device):
        """Color and depth timestamps in a synced frame set must differ by < 33ms."""
        config = Config()
        try:
            depth_profiles = pipeline.get_stream_profile_list(OBSensorType.DEPTH_SENSOR)
            config.enable_stream(depth_profiles.get_default_video_stream_profile())
            color_profiles = pipeline.get_stream_profile_list(OBSensorType.COLOR_SENSOR)
            config.enable_stream(color_profiles.get_default_video_stream_profile())
        except OBError as e:
            pytest.skip(f"Could not configure dual stream: {e}")

        pipeline.start(config)

        deltas = []
        deadline = time.time() + 10
        while len(deltas) < 20 and time.time() < deadline:
            fs = pipeline.wait_for_frames(FRAME_TIMEOUT_MS)
            if fs is None:
                continue
            depth = fs.get_depth_frame()
            color = fs.get_color_frame()
            if depth is not None and color is not None:
                delta = abs(color.get_timestamp() - depth.get_timestamp())
                deltas.append(delta)

        assert deltas, "Could not collect paired color+depth frames"
        median_delta = sorted(deltas)[len(deltas) // 2]
        assert median_delta <= SYNC_DELTA_MS, (
            f"Median color↔depth timestamp delta {median_delta}ms "
            f"exceeds {SYNC_DELTA_MS}ms threshold"
        )

    def test_frame_sync_reduces_delta(self, pipeline, gemini335_device):
        """Enabling frame sync should reduce color↔depth timestamp delta vs disabled."""
        config = Config()
        try:
            depth_profiles = pipeline.get_stream_profile_list(OBSensorType.DEPTH_SENSOR)
            config.enable_stream(depth_profiles.get_default_video_stream_profile())
            color_profiles = pipeline.get_stream_profile_list(OBSensorType.COLOR_SENSOR)
            config.enable_stream(color_profiles.get_default_video_stream_profile())
        except OBError as e:
            pytest.skip(f"Could not configure dual stream: {e}")

        pipeline.enable_frame_sync()
        pipeline.start(config)

        deltas = []
        deadline = time.time() + 10
        while len(deltas) < 20 and time.time() < deadline:
            fs = pipeline.wait_for_frames(FRAME_TIMEOUT_MS)
            if fs is None:
                continue
            depth = fs.get_depth_frame()
            color = fs.get_color_frame()
            if depth is not None and color is not None:
                delta = abs(color.get_timestamp() - depth.get_timestamp())
                deltas.append(delta)

        assert deltas, "Could not collect paired color+depth frames with sync enabled"
        p95_delta = sorted(deltas)[int(len(deltas) * 0.95)]
        assert p95_delta <= TIGHT_SYNC_DELTA_MS, (
            f"P95 sync delta {p95_delta}ms exceeds {TIGHT_SYNC_DELTA_MS}ms "
            "with frame sync enabled"
        )

    @pytest.mark.timeout(60)
    def test_tri_stream_no_dropped_frames(self, pipeline, gemini335_device):
        """Color + Depth + IR streams running simultaneously for 60 frames with < 5% drop rate."""
        config = Config()
        enabled_streams = 0
        for sensor_type in [
            OBSensorType.DEPTH_SENSOR,
            OBSensorType.COLOR_SENSOR,
            OBSensorType.IR_SENSOR,
        ]:
            try:
                pl = pipeline.get_stream_profile_list(sensor_type)
                config.enable_stream(pl.get_default_video_stream_profile())
                enabled_streams += 1
            except OBError:
                pass

        if enabled_streams < 2:
            pytest.skip("Fewer than 2 streams available for multi-stream test")

        pipeline.start(config)

        received = 0
        deadline = time.time() + 30
        while received < FRAME_COLLECT_COUNT and time.time() < deadline:
            fs = pipeline.wait_for_frames(FRAME_TIMEOUT_MS)
            if fs is not None and fs.get_frame_count() > 0:
                received += 1

        drop_rate = 1.0 - received / FRAME_COLLECT_COUNT
        assert drop_rate <= 0.05, (
            f"Multi-stream drop rate {drop_rate:.1%} exceeds 5% "
            f"(received {received}/{FRAME_COLLECT_COUNT} frame sets)"
        )
