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
G300 series post-processing filter tests.

Covers: Gemini 330 / 335 / 335L / 335Le / 335Lg / 336 / 336L / 330L / 305 / 345

All G300 models support the same post-processing filter API.
Tests verify:
- Each filter produces non-None output
- Temporal filter reduces per-pixel noise
- Spatial filter does not increase hole count
- Decimation filter reduces spatial resolution
- Threshold filter clips out-of-range values
- Align filter produces depth frame sized to match color frame
- PointCloud filter generates points with sane coordinates
"""

import numpy as np
import pytest

from pyorbbecsdk import (
    AlignFilter,
    Config,
    DecimationFilter,
    HoleFillingFilter,
    NoiseRemovalFilter,
    OBError,
    OBFrameType,
    OBSensorType,
    OBStreamType,
    PointCloudFilter,
    SpatialAdvancedFilter,
    TemporalFilter,
    ThresholdFilter,
)

pytestmark = [pytest.mark.hardware, pytest.mark.g300_series, pytest.mark.functional]

COLLECT_COUNT = 10
TIMEOUT_MS = 2000


def _get_depth_frames(pipeline, count=COLLECT_COUNT):
    """Start depth stream and return `count` raw DepthFrame objects."""
    import time

    config = Config()
    pl = pipeline.get_stream_profile_list(OBSensorType.DEPTH_SENSOR)
    config.enable_stream(pl.get_default_video_stream_profile())
    pipeline.start(config)
    frames, deadline = [], time.time() + count * 3
    while len(frames) < count and time.time() < deadline:
        fs = pipeline.wait_for_frames(TIMEOUT_MS)
        if fs:
            f = fs.get_depth_frame()
            if f:
                frames.append(f)
    return frames


def _depth_as_array(frame):
    scale = frame.get_depth_scale()
    data = np.frombuffer(frame.get_data(), dtype=np.uint16).astype(np.float32)
    return data * scale  # values in mm


class TestTemporalFilter:

    def test_temporal_filter_produces_output(self, pipeline, g300_series_device):
        frames = _get_depth_frames(pipeline, count=5)
        assert frames
        filt = TemporalFilter()
        result = None
        for f in frames:
            result = filt.process(f)
        assert result is not None, "TemporalFilter returned None"

    def test_temporal_filter_reduces_noise(self, pipeline, g300_series_device):
        """Filtered std-dev should not be worse than raw std-dev × 1.1."""
        frames = _get_depth_frames(pipeline)
        assert len(frames) >= 5
        filt = TemporalFilter()
        for f in frames:
            filtered = filt.process(f)
        raw_std = float(np.std(_depth_as_array(frames[-1])))
        filt_std = float(np.std(_depth_as_array(filtered.as_depth_frame())))
        assert filt_std <= raw_std * 1.1, f"TemporalFilter increased std-dev: {raw_std:.2f} → {filt_std:.2f}"


class TestSpatialFilter:

    def test_spatial_filter_produces_output(self, pipeline, g300_series_device):
        frames = _get_depth_frames(pipeline, count=3)
        assert frames
        result = SpatialAdvancedFilter().process(frames[-1])
        assert result is not None

    def test_spatial_filter_does_not_increase_holes(self, pipeline, g300_series_device):
        frames = _get_depth_frames(pipeline, count=3)
        assert frames
        raw_zeros = int(np.count_nonzero(np.frombuffer(frames[-1].get_data(), dtype=np.uint16) == 0))
        result = SpatialAdvancedFilter().process(frames[-1])
        filt_zeros = int(np.count_nonzero(np.frombuffer(result.as_depth_frame().get_data(), dtype=np.uint16) == 0))
        assert filt_zeros <= raw_zeros, f"SpatialFilter introduced new holes: {raw_zeros} → {filt_zeros} zeros"


class TestHoleFillingFilter:

    def test_hole_filling_produces_output(self, pipeline, g300_series_device):
        frames = _get_depth_frames(pipeline, count=3)
        assert frames
        result = HoleFillingFilter().process(frames[-1])
        assert result is not None

    def test_hole_filling_reduces_zeros(self, pipeline, g300_series_device):
        frames = _get_depth_frames(pipeline, count=3)
        assert frames
        raw = np.frombuffer(frames[-1].get_data(), dtype=np.uint16)
        raw_zeros = int(np.count_nonzero(raw == 0))
        result = HoleFillingFilter().process(frames[-1])
        filt = np.frombuffer(result.as_depth_frame().get_data(), dtype=np.uint16)
        filt_zeros = int(np.count_nonzero(filt == 0))
        assert filt_zeros <= raw_zeros, f"HoleFillingFilter did not reduce zeros: {raw_zeros} → {filt_zeros}"


class TestDecimationFilter:

    def test_decimation_halves_resolution(self, pipeline, g300_series_device):
        """With scale=2 the output should be approximately half width/height."""
        frames = _get_depth_frames(pipeline, count=3)
        assert frames
        original = frames[-1]
        orig_w = original.get_width()
        orig_h = original.get_height()

        filt = DecimationFilter()
        filt.set_config_value("decimate", 2)
        result = filt.process(original)
        assert result is not None
        out = result.as_depth_frame()
        assert abs(out.get_width() - orig_w // 2) <= 4
        assert abs(out.get_height() - orig_h // 2) <= 4


class TestThresholdFilter:

    def test_threshold_filter_clips_values(self, pipeline, g300_series_device):
        """Non-zero values must be within the configured min/max range (±10% tolerance)."""
        frames = _get_depth_frames(pipeline, count=3)
        assert frames
        filt = ThresholdFilter()
        min_mm, max_mm = 300, 3000
        filt.set_config_value("min", min_mm)
        filt.set_config_value("max", max_mm)
        result = filt.process(frames[-1])
        assert result is not None
        data = _depth_as_array(result.as_depth_frame())
        valid = data[data > 0]
        if len(valid) > 0:
            assert valid.min() >= min_mm * 0.9
            assert valid.max() <= max_mm * 1.1


class TestAlignFilter:

    def test_align_filter_produces_output(self, pipeline, g300_series_device):
        """AlignFilter should return a non-None depth frame aligned to color."""
        import time

        config = Config()
        try:
            config.enable_stream(
                pipeline.get_stream_profile_list(OBSensorType.DEPTH_SENSOR).get_default_video_stream_profile()
            )
            config.enable_stream(
                pipeline.get_stream_profile_list(OBSensorType.COLOR_SENSOR).get_default_video_stream_profile()
            )
        except OBError as e:
            pytest.skip(f"Cannot configure dual stream: {e}")

        pipeline.start(config)
        filt = AlignFilter(align_to_stream=OBStreamType.COLOR_STREAM)
        result = None
        deadline = time.time() + 10
        while result is None and time.time() < deadline:
            fs = pipeline.wait_for_frames(TIMEOUT_MS)
            if fs:
                result = filt.process(fs)
        assert result is not None, "AlignFilter returned None"

    def test_aligned_depth_matches_color_size(self, pipeline, g300_series_device):
        """Aligned depth frame must have same dimensions as color frame."""
        import time

        config = Config()
        try:
            dp = pipeline.get_stream_profile_list(OBSensorType.DEPTH_SENSOR).get_default_video_stream_profile()
            cp = pipeline.get_stream_profile_list(OBSensorType.COLOR_SENSOR).get_default_video_stream_profile()
            config.enable_stream(dp)
            config.enable_stream(cp)
        except OBError as e:
            pytest.skip(f"Cannot configure dual stream: {e}")

        pipeline.start(config)
        filt = AlignFilter(align_to_stream=OBStreamType.COLOR_STREAM)
        fs_result = None
        deadline = time.time() + 10
        while fs_result is None and time.time() < deadline:
            fs = pipeline.wait_for_frames(TIMEOUT_MS)
            if fs:
                fs_result = filt.process(fs)
        assert fs_result is not None

        depth_aligned = fs_result.get_depth_frame()
        color = fs_result.get_color_frame()
        assert depth_aligned and color
        assert depth_aligned.get_width() == color.get_width()
        assert depth_aligned.get_height() == color.get_height()


class TestPointCloudFilter:

    def test_point_cloud_produces_points(self, pipeline, g300_series_device):
        """PointCloudFilter must return a PointsFrame with at least one point."""
        import time

        config = Config()
        try:
            config.enable_stream(
                pipeline.get_stream_profile_list(OBSensorType.DEPTH_SENSOR).get_default_video_stream_profile()
            )
        except OBError as e:
            pytest.skip(f"Cannot start depth stream: {e}")
        pipeline.start(config)
        filt = PointCloudFilter()
        result = None
        deadline = time.time() + 10
        while result is None and time.time() < deadline:
            fs = pipeline.wait_for_frames(TIMEOUT_MS)
            if fs:
                result = filt.process(fs)
        assert result is not None
        pts = result.as_points_frame()
        assert pts.get_data_size() > 0

    def test_point_cloud_coordinates_reasonable(self, pipeline, g300_series_device):
        """All XYZ coordinates must be within ±10 000 mm (±10 m)."""
        import time

        config = Config()
        try:
            config.enable_stream(
                pipeline.get_stream_profile_list(OBSensorType.DEPTH_SENSOR).get_default_video_stream_profile()
            )
        except OBError as e:
            pytest.skip(f"Cannot start depth stream: {e}")
        pipeline.start(config)
        filt = PointCloudFilter()
        result = None
        deadline = time.time() + 10
        while result is None and time.time() < deadline:
            fs = pipeline.wait_for_frames(TIMEOUT_MS)
            if fs:
                result = filt.process(fs)
        assert result is not None
        pts = result.as_points_frame()
        data = np.frombuffer(pts.get_data(), dtype=np.float32)
        if len(data) >= 3:
            assert np.all(np.abs(data) <= 10000.0), "Point cloud contains coordinates beyond ±10 000 mm"


class TestNoiseRemovalFilter:

    def test_noise_removal_produces_output(self, pipeline, g300_series_device):
        frames = _get_depth_frames(pipeline, count=3)
        assert frames
        result = NoiseRemovalFilter().process(frames[-1])
        assert result is not None
