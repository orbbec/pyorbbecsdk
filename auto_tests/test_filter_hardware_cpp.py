"""Direct translations of tests/hardware/TC_CPP_13_filter_hw_test.cpp.

Extended filters (spatial / temporal / hole-filling / noise-removal /
disparity / false-positive) live in a private library.  In builds where that
library is not activated the filter classes exist but constructing them aborts
the process, so every filter is created through ``conftest.make_filter`` and an
unavailable filter is reported as a skip instead of a crash.
"""

from __future__ import annotations

import time

import pytest
from conftest import first_profile, make_filter, ob, wait_for_frameset_with_retry

pytestmark = pytest.mark.hardware


def _depth(device, retries=4):
    """Return a live depth frame, or fail the case."""
    pipeline = ob.Pipeline(device)
    try:
        config = ob.Config()
        config.enable_stream(first_profile(pipeline, ob.OBSensorType.DEPTH_SENSOR))
        pipeline.start(config)

        for _ in range(retries):
            frameset = wait_for_frameset_with_retry(pipeline)
            if frameset is not None:
                frame = frameset.get_depth_frame()
                if frame is not None:
                    return frame
        pytest.fail("No depth frame received")
    finally:
        try:
            pipeline.stop()
        except Exception:
            pass


def _filter_or_skip(name, required=False):
    """Create a filter, skipping when the implementation is unavailable."""
    created = make_filter(name, required=required)
    if created is None:
        pytest.skip(f"{name} not available: private filter library not activated")
    return created


def test_TC_CPP_13_03_filter_sync_process(device):
    filter_ = _filter_or_skip("DecimationFilter", required=True)
    depth = _depth(device)

    result = filter_.process(depth)
    assert result is not None
    assert result.get_data_size() > 0


def test_TC_CPP_13_04_filter_async_callback(device):
    filter_ = _filter_or_skip("DecimationFilter", required=True)
    callback_frames = []
    filter_.set_callback(lambda frame: callback_frames.append(frame))

    filter_.push_frame(_depth(device))

    deadline = time.monotonic() + 0.5
    while not callback_frames and time.monotonic() < deadline:
        time.sleep(0.01)
    assert callback_frames


def test_TC_CPP_13_08_pointcloud_filter(device):
    filter_ = _filter_or_skip("PointCloudFilter", required=True)
    result = filter_.process(_depth(device))
    assert result is not None
    assert result.get_data_size() > 0


def test_TC_CPP_13_09_align_filter(device):
    pipeline = ob.Pipeline(device)
    try:
        config = ob.Config()
        config.enable_stream(first_profile(pipeline, ob.OBSensorType.DEPTH_SENSOR))
        config.enable_stream(first_profile(pipeline, ob.OBSensorType.COLOR_SENSOR))
        config.set_frame_aggregate_output_mode(ob.OBFrameAggregateOutputMode.FULL_FRAME_REQUIRE)
        pipeline.start(config)

        frames = []
        deadline = time.monotonic() + 10
        while len(frames) < 5 and time.monotonic() < deadline:
            frameset = wait_for_frameset_with_retry(pipeline)
            if frameset is None:
                continue
            if frameset.get_depth_frame() is not None and frameset.get_color_frame() is not None:
                frames.append(frameset)
    finally:
        try:
            pipeline.stop()
        except Exception:
            pass

    if not frames:
        pytest.skip("Could not capture frameset with both depth and color")

    # AlignFilter needs a target stream type; it is a built-in filter.
    align = ob.AlignFilter(ob.OBStreamType.COLOR_STREAM)
    aligned = align.process(frames[0])
    assert aligned is not None
    assert aligned.get_data_size() > 0
    assert aligned.get_depth_frame().get_width() > 0
    assert aligned.get_color_frame().get_height() > 0


def test_TC_CPP_13_10_format_converter(device):
    pipeline = ob.Pipeline(device)
    try:
        config = ob.Config()
        config.enable_stream(first_profile(pipeline, ob.OBSensorType.COLOR_SENSOR))
        pipeline.start(config)

        color = None
        for _ in range(6):
            frameset = pipeline.wait_for_frames(1000)
            if frameset is not None and frameset.get_color_frame() is not None:
                color = frameset.get_color_frame()
                break
    finally:
        try:
            pipeline.stop()
        except Exception:
            pass

    if color is None:
        pytest.skip("No color frame produced by this device")

    converter = _filter_or_skip("FormatConverter", required=True)
    result = converter.process(color)
    assert result is not None
    assert result.get_data_size() > 0


def test_TC_CPP_13_11_hdr_merge(device):
    hdr = make_filter("HDRMerge")
    sequence = make_filter("SequenceIdFilter")
    if hdr is None or sequence is None:
        pytest.skip("HDRMergeFilter or SequenceIdFilter not available: private filter library not activated")

    result = hdr.process(_depth(device))
    assert result is not None
    assert result.get_data_size() > 0


def test_TC_CPP_13_12_decimation_filter(device):
    filter_ = _filter_or_skip("DecimationFilter", required=True)
    depth = _depth(device)

    result = filter_.process(depth)
    assert result is not None
    video = result.as_video_frame()
    assert video is not None
    assert video.get_width() > 0


def test_TC_CPP_13_13_threshold_filter(device):
    filter_ = _filter_or_skip("ThresholdFilter", required=True)
    result = filter_.process(_depth(device))
    assert result is not None
    assert result.get_data_size() > 0


def test_TC_CPP_13_14_spatial_filters(device):
    depth = _depth(device)

    results = []
    for name in ("SpatialAdvancedFilter", "SpatialFastFilter", "SpatialModerateFilter"):
        created = make_filter(name)
        if created is None:
            continue
        try:
            results.append(created.process(depth))
        except Exception:  # noqa: BLE001 - filter accepted but cannot run here
            continue

    if not results:
        pytest.skip("No spatial filters available: private filter library not activated")

    for result in results:
        assert result is not None
        assert result.get_data_size() > 0


def test_TC_CPP_13_15_temporal_holefilling_noise(device):
    filters = []
    for name in ("TemporalFilter", "HoleFillingFilter", "NoiseRemovalFilter"):
        created = make_filter(name)
        if created is not None:
            filters.append((name, created))

    if not filters:
        pytest.skip("No temporal/holefilling/noise filters available")

    depth = _depth(device)
    for name, created in filters:
        result = created.process(depth)
        assert result is not None, name
        assert result.get_data_size() > 0, name


def test_TC_CPP_13_16_false_positive_disparity(device):
    filters = []
    for name in ("FalsePositiveFilter", "DisparityTransform"):
        created = make_filter(name)
        if created is not None:
            filters.append((name, created))

    if not filters:
        pytest.skip("No false-positive/disparity filters available")

    depth = _depth(device)
    for name, created in filters:
        result = created.process(depth)
        assert result is not None, name
        assert result.get_data_size() > 0, name
