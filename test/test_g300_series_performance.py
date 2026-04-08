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
G300 series performance benchmark tests.

Covers all G300 series cameras: Gemini 330, 335, 335L, 335Le, 335Lg,
336, 336L, 330L, 305, 345 and their variants.

These tests measure:
  - Time-to-first-frame (stream startup latency)
  - Sustained frame rate stability over 60 seconds
  - Frame processing throughput (numpy operations vs 30fps budget)
  - Pipeline restart time (stop → start)
  - Dual-stream synchronization latency distribution (P50 / P95)

All tests have generous timeouts to accommodate USB enumeration variance.
"""

import statistics
import time

import numpy as np
import pytest

from pyorbbecsdk import Config, OBError, OBSensorType

pytestmark = [pytest.mark.hardware, pytest.mark.g300_series, pytest.mark.performance]

FRAME_TIMEOUT_MS = 2000
TARGET_FPS = 30
FRAME_BUDGET_MS = 1000.0 / TARGET_FPS  # 33.3ms


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _depth_config(pipeline):
    config = Config()
    pl = pipeline.get_stream_profile_list(OBSensorType.DEPTH_SENSOR)
    config.enable_stream(pl.get_default_video_stream_profile())
    return config


# ---------------------------------------------------------------------------
# Startup latency
# ---------------------------------------------------------------------------


class TestStartupLatency:

    @pytest.mark.timeout(15)
    def test_time_to_first_depth_frame(self, pipeline, g300_series_device):
        """First depth frame must arrive within 5 seconds of pipeline.start()."""
        config = _depth_config(pipeline)
        t0 = time.perf_counter()
        pipeline.start(config)

        first_frame = None
        deadline = time.perf_counter() + 5.0
        while first_frame is None and time.perf_counter() < deadline:
            fs = pipeline.wait_for_frames(FRAME_TIMEOUT_MS)
            if fs is not None:
                first_frame = fs.get_depth_frame()

        elapsed = time.perf_counter() - t0
        assert first_frame is not None, f"No depth frame within 5s of pipeline start"
        assert elapsed <= 5.0, f"Time-to-first-frame {elapsed:.2f}s exceeds 5s threshold"
        print(f"\n  Time-to-first-depth-frame: {elapsed*1000:.0f}ms")

    @pytest.mark.timeout(15)
    def test_time_to_first_color_frame(self, pipeline, g300_series_device):
        """First color frame must arrive within 5 seconds of pipeline.start()."""
        config = Config()
        try:
            pl = pipeline.get_stream_profile_list(OBSensorType.COLOR_SENSOR)
            config.enable_stream(pl.get_default_video_stream_profile())
        except OBError as e:
            pytest.skip(f"Color sensor not available: {e}")

        t0 = time.perf_counter()
        pipeline.start(config)

        first_frame = None
        deadline = time.perf_counter() + 5.0
        while first_frame is None and time.perf_counter() < deadline:
            fs = pipeline.wait_for_frames(FRAME_TIMEOUT_MS)
            if fs is not None:
                first_frame = fs.get_color_frame()

        elapsed = time.perf_counter() - t0
        assert first_frame is not None, "No color frame within 5s of pipeline start"
        assert elapsed <= 5.0, f"Time-to-first-color-frame {elapsed:.2f}s exceeds 5s threshold"
        print(f"\n  Time-to-first-color-frame: {elapsed*1000:.0f}ms")


# ---------------------------------------------------------------------------
# Frame rate stability
# ---------------------------------------------------------------------------


class TestFrameRateStability:

    @pytest.mark.timeout(75)
    def test_depth_fps_over_60_seconds(self, pipeline, g300_series_device):
        """
        Collect depth frames for 60 seconds; measure per-second frame counts.
        Mean FPS must be ≥27, std-dev ≤ 3.
        """
        config = _depth_config(pipeline)
        pipeline.start(config)

        per_second_counts = []
        bucket_start = time.perf_counter()
        bucket_count = 0
        total_deadline = time.perf_counter() + 62  # ~60s + warm-up

        # Skip first 2 seconds (warm-up)
        warmup_end = time.perf_counter() + 2
        while time.perf_counter() < warmup_end:
            pipeline.wait_for_frames(FRAME_TIMEOUT_MS)

        bucket_start = time.perf_counter()
        while time.perf_counter() < total_deadline:
            fs = pipeline.wait_for_frames(FRAME_TIMEOUT_MS)
            if fs is not None and fs.get_depth_frame() is not None:
                bucket_count += 1

            elapsed = time.perf_counter() - bucket_start
            if elapsed >= 1.0:
                per_second_counts.append(bucket_count)
                bucket_count = 0
                bucket_start = time.perf_counter()

        assert len(per_second_counts) >= 10, f"Only collected {len(per_second_counts)} per-second samples"

        mean_fps = statistics.mean(per_second_counts)
        std_fps = statistics.stdev(per_second_counts) if len(per_second_counts) > 1 else 0

        print(
            f"\n  Depth FPS: mean={mean_fps:.1f}, std={std_fps:.2f}, "
            f"min={min(per_second_counts)}, max={max(per_second_counts)}"
        )

        assert mean_fps >= 27, f"Mean depth FPS {mean_fps:.1f} below 27fps threshold"
        assert std_fps <= 3.0, f"Depth FPS std-dev {std_fps:.2f} exceeds 3.0 (unstable stream)"


# ---------------------------------------------------------------------------
# Pipeline restart time
# ---------------------------------------------------------------------------


class TestPipelineRestart:

    @pytest.mark.timeout(30)
    def test_restart_time(self, pipeline, g300_series_device):
        """
        stop() → start() round-trip must complete and produce a frame within 3s.
        Tested 3 times to check consistency.
        """
        config = _depth_config(pipeline)
        pipeline.start(config)

        # Get initial frame to confirm running
        fs = pipeline.wait_for_frames(FRAME_TIMEOUT_MS)
        assert fs is not None, "Pipeline did not start initially"

        restart_times = []
        for i in range(3):
            pipeline.stop()
            t0 = time.perf_counter()
            pipeline.start(config)

            first_frame = None
            deadline = time.perf_counter() + 5.0
            while first_frame is None and time.perf_counter() < deadline:
                fs = pipeline.wait_for_frames(FRAME_TIMEOUT_MS)
                if fs is not None:
                    first_frame = fs.get_depth_frame()

            elapsed = time.perf_counter() - t0
            restart_times.append(elapsed)
            assert first_frame is not None, f"Restart {i+1}: No frame within 5s after restart"

        mean_restart = statistics.mean(restart_times)
        print(f"\n  Restart times: {[f'{t*1000:.0f}ms' for t in restart_times]}, " f"mean={mean_restart*1000:.0f}ms")

        assert mean_restart <= 3.0, f"Mean restart time {mean_restart:.2f}s exceeds 3s threshold"


# ---------------------------------------------------------------------------
# Frame processing throughput
# ---------------------------------------------------------------------------


class TestFrameProcessingThroughput:

    @pytest.mark.timeout(30)
    def test_numpy_processing_under_frame_budget(self, pipeline, g300_series_device):
        """
        Common depth post-processing (uint16→float32 reshape, normalize, colormap)
        must complete within 33ms per frame (30fps budget) on this machine.
        Measures average over 30 frames.
        """
        config = _depth_config(pipeline)
        pipeline.start(config)

        # Warm up
        for _ in range(5):
            pipeline.wait_for_frames(FRAME_TIMEOUT_MS)

        processing_times = []
        collected = 0
        deadline = time.perf_counter() + 20
        while collected < 30 and time.perf_counter() < deadline:
            fs = pipeline.wait_for_frames(FRAME_TIMEOUT_MS)
            if fs is None:
                continue
            depth_frame = fs.get_depth_frame()
            if depth_frame is None:
                continue

            w = depth_frame.get_width()
            h = depth_frame.get_height()
            scale = depth_frame.get_depth_scale()

            t0 = time.perf_counter()

            # Typical processing pipeline
            raw = np.frombuffer(depth_frame.get_data(), dtype=np.uint16)
            depth = raw.reshape(h, w).astype(np.float32) * scale
            depth = np.where((depth > 20) & (depth < 10000), depth, 0)
            normalized = _cv2_normalize_equiv(depth)

            elapsed_ms = (time.perf_counter() - t0) * 1000
            processing_times.append(elapsed_ms)
            collected += 1

        assert processing_times, "No frames processed"
        mean_ms = statistics.mean(processing_times)
        p95_ms = sorted(processing_times)[int(len(processing_times) * 0.95)]

        print(f"\n  Depth processing: mean={mean_ms:.1f}ms, P95={p95_ms:.1f}ms " f"(budget={FRAME_BUDGET_MS:.1f}ms)")

        assert (
            mean_ms <= FRAME_BUDGET_MS
        ), f"Mean processing time {mean_ms:.1f}ms exceeds {FRAME_BUDGET_MS:.1f}ms frame budget"


def _cv2_normalize_equiv(arr: np.ndarray) -> np.ndarray:
    """Equivalent to cv2.normalize(arr, None, 0, 255, NORM_MINMAX) without cv2 dep."""
    valid = arr[arr > 0]
    if len(valid) == 0:
        return np.zeros_like(arr, dtype=np.uint8)
    lo, hi = valid.min(), valid.max()
    if hi == lo:
        return np.zeros_like(arr, dtype=np.uint8)
    normalized = np.clip((arr - lo) / (hi - lo) * 255, 0, 255)
    return normalized.astype(np.uint8)


# ---------------------------------------------------------------------------
# Dual-stream sync latency distribution
# ---------------------------------------------------------------------------


class TestDualStreamSyncLatency:

    @pytest.mark.timeout(30)
    def test_color_depth_sync_latency_distribution(self, pipeline, g300_series_device):
        """
        Collect 50 paired (color, depth) frame sets and measure timestamp deltas.
        P50 ≤ 20ms and P95 ≤ 33ms (one frame duration at 30fps).
        """
        config = Config()
        try:
            depth_pl = pipeline.get_stream_profile_list(OBSensorType.DEPTH_SENSOR)
            config.enable_stream(depth_pl.get_default_video_stream_profile())
            color_pl = pipeline.get_stream_profile_list(OBSensorType.COLOR_SENSOR)
            config.enable_stream(color_pl.get_default_video_stream_profile())
        except OBError as e:
            pytest.skip(f"Cannot configure dual stream: {e}")

        pipeline.enable_frame_sync()
        pipeline.start(config)

        deltas = []
        deadline = time.perf_counter() + 25
        while len(deltas) < 50 and time.perf_counter() < deadline:
            fs = pipeline.wait_for_frames(FRAME_TIMEOUT_MS)
            if fs is None:
                continue
            depth = fs.get_depth_frame()
            color = fs.get_color_frame()
            if depth is not None and color is not None:
                delta = abs(int(color.get_timestamp()) - int(depth.get_timestamp()))
                deltas.append(delta)

        if len(deltas) < 10:
            pytest.skip(f"Insufficient paired frames: {len(deltas)}")

        p50 = sorted(deltas)[len(deltas) // 2]
        p95 = sorted(deltas)[int(len(deltas) * 0.95)]

        print(f"\n  Color↔Depth sync: P50={p50}ms, P95={p95}ms " f"(n={len(deltas)})")

        assert p50 <= 20, f"P50 sync delta {p50}ms exceeds 20ms"
        assert p95 <= 33, f"P95 sync delta {p95}ms exceeds 33ms (1 frame)"
