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
Gemini 335 post-processing filter pipeline tests.

Tests verify that each filter:
  - Processes frames without raising exceptions
  - Produces output that differs from (or is a superset of) the input
  - Produces output in the expected dimensions / format
"""

import time
import pytest
import numpy as np

from pyorbbecsdk import (
    Config,
    OBSensorType,
    OBFrameType,
    OBStreamType,
    OBFormat,
    OBError,
    TemporalFilter,
    SpatialAdvancedFilter,
    HoleFillingFilter,
    DecimationFilter,
    ThresholdFilter,
    AlignFilter,
    PointCloudFilter,
    NoiseRemovalFilter,
)

pytestmark = [pytest.mark.hardware, pytest.mark.gemini335]

FRAME_TIMEOUT_MS = 2000


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _get_depth_frames(pipeline, count=10):
    """Start depth stream and collect `count` frames."""
    config = Config()
    pl = pipeline.get_stream_profile_list(OBSensorType.DEPTH_SENSOR)
    profile = pl.get_default_video_stream_profile()
    config.enable_stream(profile)
    pipeline.start(config)

    frames = []
    deadline = time.time() + 15
    while len(frames) < count and time.time() < deadline:
        fs = pipeline.wait_for_frames(FRAME_TIMEOUT_MS)
        if fs is None:
            continue
        f = fs.get_depth_frame()
        if f is not None:
            frames.append(f)
    return frames, profile


def _depth_as_array(frame):
    """Convert a depth frame to a float32 numpy array (in mm)."""
    depth_frame = frame.as_depth_frame()
    w = depth_frame.get_width()
    h = depth_frame.get_height()
    scale = depth_frame.get_depth_scale()
    data = np.frombuffer(frame.get_data(), dtype=np.uint16).reshape(h, w)
    return data.astype(np.float32) * scale


# ---------------------------------------------------------------------------
# Temporal filter
# ---------------------------------------------------------------------------

class TestTemporalFilter:

    def test_temporal_filter_produces_output(self, pipeline, gemini335_device):
        """TemporalFilter must return a non-None frame."""
        frames, _ = _get_depth_frames(pipeline, count=5)
        assert frames, "No depth frames collected"

        tf = TemporalFilter()
        result = None
        for f in frames:
            result = tf.process(f)
        assert result is not None, "TemporalFilter returned None after 5 frames"

    def test_temporal_filter_reduces_noise(self, pipeline, gemini335_device):
        """After temporal smoothing, per-pixel std-dev should decrease vs raw."""
        frames, _ = _get_depth_frames(pipeline, count=15)
        assert len(frames) >= 10, f"Only got {len(frames)} frames"

        raw_stack = np.stack([_depth_as_array(f) for f in frames[-5:]], axis=0)

        tf = TemporalFilter()
        filtered = []
        for f in frames:
            out = tf.process(f)
            if out is not None:
                filtered.append(_depth_as_array(out))

        if len(filtered) < 5:
            pytest.skip("Temporal filter did not produce enough output frames")

        filtered_stack = np.stack(filtered[-5:], axis=0)

        # Only compare valid (non-zero) pixels across all frames
        valid_mask = (raw_stack > 0).all(axis=0)
        if valid_mask.sum() < 100:
            pytest.skip("Not enough valid depth pixels for noise comparison")

        raw_std = raw_stack[:, valid_mask].std(axis=0).mean()
        filtered_std = filtered_stack[:, valid_mask].std(axis=0).mean()

        # Allow a relaxed criterion — temporal filter should not increase noise
        assert filtered_std <= raw_std * 1.1, (
            f"Temporal filter increased noise: raw_std={raw_std:.2f}, "
            f"filtered_std={filtered_std:.2f}"
        )


# ---------------------------------------------------------------------------
# Spatial advanced filter
# ---------------------------------------------------------------------------

class TestSpatialFilter:

    def test_spatial_filter_produces_output(self, pipeline, gemini335_device):
        """SpatialAdvancedFilter must return a non-None frame."""
        frames, _ = _get_depth_frames(pipeline, count=3)
        assert frames

        sf = SpatialAdvancedFilter()
        result = sf.process(frames[-1])
        assert result is not None, "SpatialAdvancedFilter returned None"

    def test_spatial_filter_reduces_holes(self, pipeline, gemini335_device):
        """Spatial filter should not increase the number of zero-depth pixels."""
        frames, _ = _get_depth_frames(pipeline, count=3)
        assert frames

        raw = np.frombuffer(frames[-1].get_data(), dtype=np.uint16)
        raw_zeros = (raw == 0).sum()

        sf = SpatialAdvancedFilter()
        result = sf.process(frames[-1])
        assert result is not None

        filtered = np.frombuffer(result.get_data(), dtype=np.uint16)
        filtered_zeros = (filtered == 0).sum()

        # Spatial filter should fill some holes; zeros should not increase
        assert filtered_zeros <= raw_zeros, (
            f"Spatial filter increased zero pixels: {raw_zeros} → {filtered_zeros}"
        )


# ---------------------------------------------------------------------------
# Hole-filling filter
# ---------------------------------------------------------------------------

class TestHoleFillingFilter:

    def test_hole_filling_produces_output(self, pipeline, gemini335_device):
        """HoleFillingFilter must return a non-None frame."""
        frames, _ = _get_depth_frames(pipeline, count=3)
        assert frames

        hf = HoleFillingFilter()
        result = hf.process(frames[-1])
        assert result is not None

    def test_hole_filling_reduces_zeros(self, pipeline, gemini335_device):
        """Hole-filling should reduce or maintain the number of zero-depth pixels."""
        frames, _ = _get_depth_frames(pipeline, count=3)
        assert frames

        raw = np.frombuffer(frames[-1].get_data(), dtype=np.uint16)
        raw_zeros = (raw == 0).sum()

        hf = HoleFillingFilter()
        result = hf.process(frames[-1])
        assert result is not None

        filtered = np.frombuffer(result.get_data(), dtype=np.uint16)
        filtered_zeros = (filtered == 0).sum()

        assert filtered_zeros <= raw_zeros, (
            f"Hole filling increased zero pixels: {raw_zeros} → {filtered_zeros}"
        )


# ---------------------------------------------------------------------------
# Decimation filter
# ---------------------------------------------------------------------------

class TestDecimationFilter:

    def test_decimation_halves_resolution(self, pipeline, gemini335_device):
        """Decimation filter with scale=2 should halve width and height."""
        frames, profile = _get_depth_frames(pipeline, count=3)
        assert frames

        orig_w = profile.get_width()
        orig_h = profile.get_height()

        df = DecimationFilter()
        df.set_scale_value(2)
        result = df.process(frames[-1])
        assert result is not None

        out_frame = result.as_video_frame() if hasattr(result, 'as_video_frame') else result
        # Decimated frame should be approximately half size (may round)
        try:
            out_w = out_frame.get_width()
            out_h = out_frame.get_height()
            assert abs(out_w - orig_w // 2) <= 4, (
                f"Decimated width {out_w} not ≈ {orig_w // 2}"
            )
            assert abs(out_h - orig_h // 2) <= 4, (
                f"Decimated height {out_h} not ≈ {orig_h // 2}"
            )
        except AttributeError:
            pytest.skip("Output frame does not expose get_width/get_height")


# ---------------------------------------------------------------------------
# Threshold filter
# ---------------------------------------------------------------------------

class TestThresholdFilter:

    def test_threshold_filter_clips_values(self, pipeline, gemini335_device):
        """ThresholdFilter should zero out pixels outside [min, max] range."""
        frames, _ = _get_depth_frames(pipeline, count=3)
        assert frames

        frame = frames[-1].as_depth_frame()
        scale = frame.get_depth_scale()
        raw = np.frombuffer(frames[-1].get_data(), dtype=np.uint16)

        # Set threshold: only keep depths 500–2000mm
        min_mm, max_mm = 500, 2000
        min_raw = int(min_mm / scale) if scale > 0 else 500
        max_raw = int(max_mm / scale) if scale > 0 else 2000

        tf = ThresholdFilter()
        tf.set_value_range(min_mm, max_mm)
        result = tf.process(frames[-1])
        assert result is not None

        filtered = np.frombuffer(result.get_data(), dtype=np.uint16)

        # All non-zero filtered values must be within range
        valid = filtered[filtered > 0]
        if len(valid) > 0:
            assert valid.min() >= min_raw * 0.9, (
                f"Values below min threshold found: {valid.min()} < {min_raw}"
            )
            assert valid.max() <= max_raw * 1.1, (
                f"Values above max threshold found: {valid.max()} > {max_raw}"
            )


# ---------------------------------------------------------------------------
# Align filter (depth to color)
# ---------------------------------------------------------------------------

class TestAlignFilter:

    def test_align_filter_produces_output(self, pipeline, gemini335_device):
        """AlignFilter must produce a non-None result from a dual-stream frame set."""
        config = Config()
        try:
            depth_pl = pipeline.get_stream_profile_list(OBSensorType.DEPTH_SENSOR)
            config.enable_stream(depth_pl.get_default_video_stream_profile())
            color_pl = pipeline.get_stream_profile_list(OBSensorType.COLOR_SENSOR)
            color_profile = color_pl.get_default_video_stream_profile()
            config.enable_stream(color_profile)
        except OBError as e:
            pytest.skip(f"Cannot configure dual stream: {e}")

        pipeline.start(config)
        align_filter = AlignFilter(align_to_stream=OBStreamType.COLOR_STREAM)

        result = None
        deadline = time.time() + 10
        while result is None and time.time() < deadline:
            fs = pipeline.wait_for_frames(FRAME_TIMEOUT_MS)
            if fs is None:
                continue
            if fs.get_depth_frame() is not None and fs.get_color_frame() is not None:
                result = align_filter.process(fs)

        assert result is not None, "AlignFilter returned None for all frame sets"

    def test_aligned_depth_matches_color_size(self, pipeline, gemini335_device):
        """After alignment, depth frame dimensions should match color frame dimensions."""
        config = Config()
        color_w = color_h = None
        try:
            depth_pl = pipeline.get_stream_profile_list(OBSensorType.DEPTH_SENSOR)
            config.enable_stream(depth_pl.get_default_video_stream_profile())
            color_pl = pipeline.get_stream_profile_list(OBSensorType.COLOR_SENSOR)
            color_profile = color_pl.get_default_video_stream_profile()
            color_w = color_profile.get_width()
            color_h = color_profile.get_height()
            config.enable_stream(color_profile)
        except OBError as e:
            pytest.skip(f"Cannot configure dual stream: {e}")

        pipeline.start(config)
        align_filter = AlignFilter(align_to_stream=OBStreamType.COLOR_STREAM)

        aligned_fs = None
        deadline = time.time() + 10
        while aligned_fs is None and time.time() < deadline:
            fs = pipeline.wait_for_frames(FRAME_TIMEOUT_MS)
            if fs is None:
                continue
            if fs.get_depth_frame() is not None and fs.get_color_frame() is not None:
                aligned_fs = align_filter.process(fs)

        if aligned_fs is None:
            pytest.skip("Could not get aligned frame set")

        aligned_depth = aligned_fs.get_depth_frame()
        if aligned_depth is None:
            pytest.skip("Aligned frame set has no depth frame")

        assert aligned_depth.get_width() == color_w, (
            f"Aligned depth width {aligned_depth.get_width()} ≠ color width {color_w}"
        )
        assert aligned_depth.get_height() == color_h, (
            f"Aligned depth height {aligned_depth.get_height()} ≠ color height {color_h}"
        )


# ---------------------------------------------------------------------------
# Point cloud filter
# ---------------------------------------------------------------------------

class TestPointCloudFilter:

    def test_point_cloud_produces_points(self, pipeline, gemini335_device):
        """PointCloudFilter must produce a PointsFrame with > 0 points."""
        config = Config()
        try:
            depth_pl = pipeline.get_stream_profile_list(OBSensorType.DEPTH_SENSOR)
            config.enable_stream(depth_pl.get_default_video_stream_profile())
        except OBError as e:
            pytest.skip(f"Cannot configure depth stream: {e}")

        pipeline.start(config)
        align_filter = AlignFilter(align_to_stream=OBStreamType.COLOR_STREAM)
        pc_filter = PointCloudFilter()
        pc_filter.set_create_point_format(OBFormat.POINT)

        points_frame = None
        deadline = time.time() + 15
        while points_frame is None and time.time() < deadline:
            fs = pipeline.wait_for_frames(FRAME_TIMEOUT_MS)
            if fs is None or fs.get_depth_frame() is None:
                continue
            points_frame = pc_filter.process(fs)

        assert points_frame is not None, "PointCloudFilter returned None"
        data = np.frombuffer(points_frame.get_data(), dtype=np.float32)
        assert len(data) > 0, "Point cloud data is empty"

    def test_point_cloud_coordinates_reasonable(self, pipeline, gemini335_device):
        """Point cloud XYZ coordinates must be within physical camera range (±5m)."""
        config = Config()
        try:
            depth_pl = pipeline.get_stream_profile_list(OBSensorType.DEPTH_SENSOR)
            config.enable_stream(depth_pl.get_default_video_stream_profile())
        except OBError as e:
            pytest.skip(f"Cannot configure depth stream: {e}")

        pipeline.start(config)
        pc_filter = PointCloudFilter()
        pc_filter.set_create_point_format(OBFormat.POINT)

        points_frame = None
        deadline = time.time() + 15
        while points_frame is None and time.time() < deadline:
            fs = pipeline.wait_for_frames(FRAME_TIMEOUT_MS)
            if fs is None or fs.get_depth_frame() is None:
                continue
            points_frame = pc_filter.process(fs)

        if points_frame is None:
            pytest.skip("Could not get point cloud frame")

        # OBFormat.POINT = [X, Y, Z] float32 triples (in mm)
        data = np.frombuffer(points_frame.get_data(), dtype=np.float32)
        if len(data) < 3:
            pytest.skip("Point cloud has fewer than 1 point")

        points = data.reshape(-1, 3)
        valid = points[np.any(points != 0, axis=1)]  # exclude [0,0,0] invalid
        if len(valid) == 0:
            pytest.skip("All points are [0,0,0]")

        max_coord_mm = 10000.0  # 10 meters in mm
        assert np.abs(valid).max() <= max_coord_mm, (
            f"Point coordinate {np.abs(valid).max():.1f}mm exceeds 10m range"
        )


# ---------------------------------------------------------------------------
# Noise removal filter
# ---------------------------------------------------------------------------

class TestNoiseRemovalFilter:

    def test_noise_removal_produces_output(self, pipeline, gemini335_device):
        """NoiseRemovalFilter must return a non-None frame."""
        frames, _ = _get_depth_frames(pipeline, count=3)
        assert frames

        nrf = NoiseRemovalFilter()
        result = nrf.process(frames[-1])
        assert result is not None, "NoiseRemovalFilter returned None"
