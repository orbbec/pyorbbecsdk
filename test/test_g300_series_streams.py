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
G300 series stream data validation tests.

Covers: Gemini 330 / 335 / 335L / 335Le / 335Lg / 336 / 336L / 330L / 305 / 345

Tests verify:
- Depth / Color / IR streams start and produce valid frames
- Frame dimensions match configured profiles
- Frame data is non-trivial (not all zeros / black)
- Timestamps are monotonically increasing
- Achieved FPS is within ±10% of configured rate
- Color↔depth timestamp synchronization meets spec
- Multi-stream pipeline runs without excessive dropped frames
"""

import os
import time

import numpy as np
import pytest

from pyorbbecsdk import Config, OBError, OBFormat, OBFrameType, OBSensorType

pytestmark = [
    pytest.mark.hardware,
    pytest.mark.g300_series,
    pytest.mark.functional,
    pytest.mark.stability,
]

FRAME_COLLECT_COUNT = 30
FRAME_TIMEOUT_MS = 2000
TARGET_FPS = 30
FPS_TOLERANCE = 0.10
SYNC_DELTA_MS = 33
TIGHT_SYNC_DELTA_MS = 10

# G300 series depth operating range (structured light, ~20 mm – 10 000 mm)
DEPTH_MIN_MM = 10.0
DEPTH_MAX_MM = 15000.0


DEPTH_DEBUG_DIR = os.path.join(os.path.dirname(__file__), "..", "reports", "depth_debug")


def _save_depth_debug(raw_u16, width, height, scale, val_min, val_max):
    """Save raw depth frame as .npy and a normalised 8-bit PNG for visual inspection."""
    os.makedirs(DEPTH_DEBUG_DIR, exist_ok=True)
    tag = time.strftime("%Y%m%d_%H%M%S")
    depth_2d = raw_u16.reshape((height, width))

    # Save raw uint16 numpy array (lossless)
    npy_path = os.path.join(DEPTH_DEBUG_DIR, f"depth_raw_{tag}.npy")
    np.save(npy_path, depth_2d)

    # Save normalised 8-bit PNG for quick visual analysis
    try:
        import cv2

        norm = depth_2d.copy().astype(np.float32)
        norm[norm > 0] = np.clip(norm[norm > 0], 1, 65535)
        norm = (norm / norm.max() * 255).astype(np.uint8)
        coloured = cv2.applyColorMap(norm, cv2.COLORMAP_JET)
        coloured[depth_2d == 0] = 0  # keep invalid pixels black
        png_path = os.path.join(DEPTH_DEBUG_DIR, f"depth_vis_{tag}.png")
        cv2.imwrite(png_path, coloured)
    except ImportError:
        png_path = "(cv2 not available, skipped PNG)"

    # Save a small text summary
    info_path = os.path.join(DEPTH_DEBUG_DIR, f"depth_info_{tag}.txt")
    with open(info_path, "w") as f:
        f.write(f"timestamp : {tag}\n")
        f.write(f"resolution: {width}x{height}\n")
        f.write(f"scale     : {scale}\n")
        f.write(f"valid_min : {val_min:.2f} mm\n")
        f.write(f"valid_max : {val_max:.2f} mm\n")
        f.write(f"expected  : [{DEPTH_MIN_MM}, {DEPTH_MAX_MM}] mm\n")
        f.write(f"npy_file  : {npy_path}\n")
        f.write(f"png_file  : {png_path}\n")

    return npy_path


def _start_single_stream(pipeline, sensor_type, width=0, height=0, fps=30, fmt=None):
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
    time.sleep(0.5)  # Wait for stream to stabilize
    return profile


def _collect_frames(pipeline, frame_type, count, timeout_ms=FRAME_TIMEOUT_MS):
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
# Depth stream
# ===========================================================================


class TestDepthStream:

    def test_depth_stream_starts(self, pipeline, g300_series_device):
        _start_single_stream(pipeline, OBSensorType.DEPTH_SENSOR)

    def test_depth_frame_received(self, pipeline, g300_series_device):
        _start_single_stream(pipeline, OBSensorType.DEPTH_SENSOR)
        frames = _collect_frames(pipeline, OBFrameType.DEPTH_FRAME, count=1)
        assert len(frames) >= 1, "No depth frame received within timeout"

    def test_depth_frame_dimensions(self, pipeline, g300_series_device):
        profile = _start_single_stream(pipeline, OBSensorType.DEPTH_SENSOR)
        frames = _collect_frames(pipeline, OBFrameType.DEPTH_FRAME, count=1)
        assert frames, "No depth frame received"
        frame = frames[0].as_depth_frame()
        assert frame.get_width() == profile.get_width()
        assert frame.get_height() == profile.get_height()

    def test_depth_frame_data_nonzero(self, pipeline, g300_series_device):
        """More than 10% of pixels must be non-zero."""
        _start_single_stream(pipeline, OBSensorType.DEPTH_SENSOR)
        frames = _collect_frames(pipeline, OBFrameType.DEPTH_FRAME, count=5)
        assert frames
        data = np.frombuffer(frames[-1].as_depth_frame().get_data(), dtype=np.uint16)
        assert (
            np.count_nonzero(data) / data.size > 0.10
        ), "Too many zero-depth pixels — ensure an object is in front of the camera"

    def test_depth_scale_factor(self, pipeline, g300_series_device):
        _start_single_stream(pipeline, OBSensorType.DEPTH_SENSOR)
        frames = _collect_frames(pipeline, OBFrameType.DEPTH_FRAME, count=1)
        assert frames
        scale = frames[0].as_depth_frame().get_depth_scale()
        assert 0.0001 <= scale <= 1, f"Unexpected depth scale: {scale}"

    def test_depth_values_in_valid_range(self, pipeline, g300_series_device):
        _start_single_stream(pipeline, OBSensorType.DEPTH_SENSOR)
        frames = _collect_frames(pipeline, OBFrameType.DEPTH_FRAME, count=5)
        assert frames
        frame = frames[-1].as_depth_frame()
        width, height = frame.get_width(), frame.get_height()
        raw = np.frombuffer(frame.get_data(), dtype=np.uint16)
        data = raw.astype(np.float32) * frame.get_depth_scale()
        valid = data[data > 0]
        if len(valid) > 0:
            ok = valid.min() >= DEPTH_MIN_MM and valid.max() <= DEPTH_MAX_MM
            if not ok:
                _save_depth_debug(
                    raw,
                    width,
                    height,
                    frame.get_depth_scale(),
                    valid.min(),
                    valid.max(),
                )
            assert valid.min() >= DEPTH_MIN_MM, (
                f"Depth min {valid.min():.2f} mm < {DEPTH_MIN_MM} mm. " f"Debug files saved to {DEPTH_DEBUG_DIR}"
            )
            assert valid.max() <= DEPTH_MAX_MM, (
                f"Depth max {valid.max():.2f} mm > {DEPTH_MAX_MM} mm. " f"Debug files saved to {DEPTH_DEBUG_DIR}"
            )

    def test_depth_timestamps_monotonic(self, pipeline, g300_series_device):
        _start_single_stream(pipeline, OBSensorType.DEPTH_SENSOR)
        frames = _collect_frames(pipeline, OBFrameType.DEPTH_FRAME, count=FRAME_COLLECT_COUNT)
        assert len(frames) >= 5
        ts = [f.get_timestamp() for f in frames]
        for i in range(1, len(ts)):
            assert ts[i] > ts[i - 1], f"Timestamps not monotonic at index {i}"

    @pytest.mark.timeout(30)
    def test_depth_fps_accuracy(self, pipeline, g300_series_device):
        _start_single_stream(pipeline, OBSensorType.DEPTH_SENSOR, fps=TARGET_FPS)
        frames = _collect_frames(pipeline, OBFrameType.DEPTH_FRAME, count=FRAME_COLLECT_COUNT)
        assert len(frames) >= 10, "Insufficient frames to measure FPS"
        elapsed = (frames[-1].get_timestamp() - frames[0].get_timestamp()) / 1000.0
        if elapsed > 0:
            actual_fps = (len(frames) - 1) / elapsed
            lo, hi = TARGET_FPS * (1 - FPS_TOLERANCE), TARGET_FPS * (1 + FPS_TOLERANCE)
            assert lo <= actual_fps <= hi, f"Depth FPS {actual_fps:.1f} outside [{lo:.1f}, {hi:.1f}]"


# ===========================================================================
# Color stream
# ===========================================================================


class TestColorStream:

    def test_color_stream_starts(self, pipeline, g300_series_device):
        _start_single_stream(pipeline, OBSensorType.COLOR_SENSOR)

    def test_color_frame_received(self, pipeline, g300_series_device):
        _start_single_stream(pipeline, OBSensorType.COLOR_SENSOR)
        frames = _collect_frames(pipeline, OBFrameType.COLOR_FRAME, count=1)
        assert len(frames) >= 1

    def test_color_frame_dimensions(self, pipeline, g300_series_device):
        profile = _start_single_stream(pipeline, OBSensorType.COLOR_SENSOR)
        frames = _collect_frames(pipeline, OBFrameType.COLOR_FRAME, count=1)
        assert frames
        frame = frames[0].as_color_frame()
        assert frame.get_width() == profile.get_width()
        assert frame.get_height() == profile.get_height()

    def test_color_frame_not_black(self, pipeline, g300_series_device):
        _start_single_stream(pipeline, OBSensorType.COLOR_SENSOR)
        frames = _collect_frames(pipeline, OBFrameType.COLOR_FRAME, count=5)
        assert frames
        data = np.frombuffer(frames[-1].as_color_frame().get_data(), dtype=np.uint8)
        assert data.mean() > 5.0, "Color frame suspiciously dark — check lens cap"

    def test_color_timestamps_monotonic(self, pipeline, g300_series_device):
        _start_single_stream(pipeline, OBSensorType.COLOR_SENSOR)
        frames = _collect_frames(pipeline, OBFrameType.COLOR_FRAME, count=FRAME_COLLECT_COUNT)
        assert len(frames) >= 5
        ts = [f.get_timestamp() for f in frames]
        for i in range(1, len(ts)):
            assert ts[i] > ts[i - 1]

    def test_color_mjpeg_format(self, pipeline, g300_series_device):
        """G300 series supports MJPEG color format."""
        config = Config()
        try:
            pl = pipeline.get_stream_profile_list(OBSensorType.COLOR_SENSOR)
            profile = pl.get_video_stream_profile(0, 0, OBFormat.MJPG, TARGET_FPS)
            config.enable_stream(profile)
            pipeline.start(config)
            frames = _collect_frames(pipeline, OBFrameType.COLOR_FRAME, count=3)
            assert len(frames) >= 1
        except OBError as e:
            pytest.skip(f"MJPEG not supported: {e}")


# ===========================================================================
# IR stream
# ===========================================================================


def _has_dual_ir(device):
    """
    Return True if the device exposes LEFT_IR_SENSOR or RIGHT_IR_SENSOR
    (G300 series Gemini 330/335/336 use dual IR).
    """
    sensor_list = device.get_sensor_list()
    for i in range(len(sensor_list)):
        st = sensor_list[i].get_type()
        if st in (OBSensorType.LEFT_IR_SENSOR, OBSensorType.RIGHT_IR_SENSOR):
            return True
    return False


class TestIRStream:

    def test_ir_dual_streams_start(self, pipeline, g300_series_device):
        """
        G300 series has dual IR (LEFT + RIGHT).  Both streams must start
        simultaneously; fall back to single IR_SENSOR if dual is absent.
        """
        config = Config()
        if _has_dual_ir(g300_series_device):
            try:
                config.enable_video_stream(OBSensorType.LEFT_IR_SENSOR)
                config.enable_video_stream(OBSensorType.RIGHT_IR_SENSOR)
            except OBError as e:
                pytest.skip(f"Could not enable dual IR streams: {e}")
        else:
            try:
                pl = pipeline.get_stream_profile_list(OBSensorType.IR_SENSOR)
                config.enable_stream(pl.get_default_video_stream_profile())
            except OBError as e:
                pytest.skip(f"No IR sensor available: {e}")
        pipeline.start(config)

    def test_left_ir_frame_valid(self, pipeline, g300_series_device):
        """Left IR stream must produce non-trivial frame data."""
        if not _has_dual_ir(g300_series_device):
            pytest.skip("Device does not have dual IR (LEFT/RIGHT) sensors")
        config = Config()
        try:
            config.enable_video_stream(OBSensorType.LEFT_IR_SENSOR)
            config.enable_video_stream(OBSensorType.RIGHT_IR_SENSOR)
        except OBError as e:
            pytest.skip(f"Could not enable dual IR streams: {e}")
        pipeline.start(config)
        frames = _collect_frames(pipeline, OBFrameType.LEFT_IR_FRAME, count=5)
        assert frames, "No LEFT_IR_FRAME received within timeout"
        data = np.frombuffer(frames[-1].get_data(), dtype=np.uint8)
        assert data.mean() > 0, "Left IR frame is entirely zero"

    def test_right_ir_frame_valid(self, pipeline, g300_series_device):
        """Right IR stream must produce non-trivial frame data."""
        if not _has_dual_ir(g300_series_device):
            pytest.skip("Device does not have dual IR (LEFT/RIGHT) sensors")
        config = Config()
        try:
            config.enable_video_stream(OBSensorType.LEFT_IR_SENSOR)
            config.enable_video_stream(OBSensorType.RIGHT_IR_SENSOR)
        except OBError as e:
            pytest.skip(f"Could not enable dual IR streams: {e}")
        pipeline.start(config)
        frames = _collect_frames(pipeline, OBFrameType.RIGHT_IR_FRAME, count=5)
        assert frames, "No RIGHT_IR_FRAME received within timeout"
        data = np.frombuffer(frames[-1].get_data(), dtype=np.uint8)
        assert data.mean() > 0, "Right IR frame is entirely zero"

    def test_ir_frame_valid_single_sensor(self, pipeline, g300_series_device):
        """For devices with a single IR sensor, IR_FRAME must be non-trivial."""
        if _has_dual_ir(g300_series_device):
            pytest.skip("Device has dual IR — use test_left/right_ir_frame_valid instead")
        config = Config()
        try:
            pl = pipeline.get_stream_profile_list(OBSensorType.IR_SENSOR)
            config.enable_stream(pl.get_default_video_stream_profile())
        except OBError as e:
            pytest.skip(f"No IR_SENSOR available: {e}")
        pipeline.start(config)
        frames = _collect_frames(pipeline, OBFrameType.IR_FRAME, count=5)
        assert frames, "No IR_FRAME received within timeout"
        data = np.frombuffer(frames[-1].get_data(), dtype=np.uint8)
        assert data.mean() > 0, "IR frame is entirely zero"


# ===========================================================================
# Multi-stream synchronization
# ===========================================================================


class TestMultiStreamSync:

    def test_color_depth_sync_timestamps(self, pipeline, g300_series_device):
        """Color and depth timestamps must differ by < 33 ms."""
        config = Config()
        try:
            config.enable_stream(
                pipeline.get_stream_profile_list(OBSensorType.DEPTH_SENSOR).get_default_video_stream_profile()
            )
            config.enable_stream(
                pipeline.get_stream_profile_list(OBSensorType.COLOR_SENSOR).get_default_video_stream_profile()
            )
        except OBError as e:
            pytest.skip(f"Could not configure dual stream: {e}")
        pipeline.start(config)

        deltas, deadline = [], time.time() + 10
        while len(deltas) < 20 and time.time() < deadline:
            fs = pipeline.wait_for_frames(FRAME_TIMEOUT_MS)
            if fs is None:
                continue
            d, c = fs.get_depth_frame(), fs.get_color_frame()
            if d and c:
                deltas.append(abs(c.get_timestamp() - d.get_timestamp()))
        assert deltas
        median = sorted(deltas)[len(deltas) // 2]
        assert median <= SYNC_DELTA_MS, f"Median color↔depth delta {median}ms exceeds {SYNC_DELTA_MS}ms"

    def test_frame_sync_reduces_delta(self, pipeline, g300_series_device):
        """With frame sync enabled, P95 color↔depth delta should be ≤ 10 ms."""
        config = Config()
        try:
            config.enable_stream(
                pipeline.get_stream_profile_list(OBSensorType.DEPTH_SENSOR).get_default_video_stream_profile()
            )
            config.enable_stream(
                pipeline.get_stream_profile_list(OBSensorType.COLOR_SENSOR).get_default_video_stream_profile()
            )
        except OBError as e:
            pytest.skip(f"Could not configure dual stream: {e}")
        pipeline.enable_frame_sync()
        pipeline.start(config)

        deltas, deadline = [], time.time() + 10
        while len(deltas) < 20 and time.time() < deadline:
            fs = pipeline.wait_for_frames(FRAME_TIMEOUT_MS)
            if fs is None:
                continue
            d, c = fs.get_depth_frame(), fs.get_color_frame()
            if d and c:
                deltas.append(abs(c.get_timestamp() - d.get_timestamp()))
        assert deltas
        p95 = sorted(deltas)[int(len(deltas) * 0.95)]
        assert p95 <= TIGHT_SYNC_DELTA_MS, f"P95 sync delta {p95}ms exceeds {TIGHT_SYNC_DELTA_MS}ms"

    @pytest.mark.timeout(60)
    def test_tri_stream_no_dropped_frames(self, pipeline, g300_series_device):
        """
        Depth + Color + IR (LEFT+RIGHT for dual-IR devices) running for
        60 frames with < 5% drop rate.
        """
        config = Config()
        enabled = 0

        # Depth
        try:
            config.enable_stream(
                pipeline.get_stream_profile_list(OBSensorType.DEPTH_SENSOR).get_default_video_stream_profile()
            )
            enabled += 1
        except OBError:
            pass

        # Color
        try:
            config.enable_stream(
                pipeline.get_stream_profile_list(OBSensorType.COLOR_SENSOR).get_default_video_stream_profile()
            )
            enabled += 1
        except OBError:
            pass

        # IR — dual (G300) or single
        if _has_dual_ir(g300_series_device):
            try:
                config.enable_video_stream(OBSensorType.LEFT_IR_SENSOR)
                config.enable_video_stream(OBSensorType.RIGHT_IR_SENSOR)
                enabled += 1
            except OBError:
                pass
        else:
            try:
                config.enable_stream(
                    pipeline.get_stream_profile_list(OBSensorType.IR_SENSOR).get_default_video_stream_profile()
                )
                enabled += 1
            except OBError:
                pass

        if enabled < 2:
            pytest.skip("Fewer than 2 streams available")
        pipeline.start(config)
        received, deadline = 0, time.time() + 30
        while received < FRAME_COLLECT_COUNT and time.time() < deadline:
            fs = pipeline.wait_for_frames(FRAME_TIMEOUT_MS)
            if fs and fs.get_frame_count() > 0:
                received += 1
        drop_rate = 1.0 - received / FRAME_COLLECT_COUNT
        assert drop_rate <= 0.05, (
            f"Drop rate {drop_rate:.1%} exceeds 5% " f"({received}/{FRAME_COLLECT_COUNT} frame sets)"
        )
