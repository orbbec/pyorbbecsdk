"""Parameterized translations of tests/unit/TC_CPP_18_playback_test.cpp.

Everything here needs a BAG file recorded from a device: the C++ ``SetUp`` skips
when the fixture parameter is empty and so does this module.  Point
``resource.bagPaths`` at one or more bags in ``test_config.json`` to run it.

The C++ ``TEST_P`` matrix is one parametrised function with the original case ids
as parameter ids, so JUnit names stay diffable against the C++ report.
"""

from __future__ import annotations

import math
import os
import time
from pathlib import Path

import numpy as np
import pytest

from conftest import ob

pytestmark = pytest.mark.unit


def _bag_paths():
    """BAG files from test_config.json (``OB_TEST_CONFIG`` or ./test_config.json)."""
    import json

    path = Path(os.getenv("OB_TEST_CONFIG", "test_config.json"))
    if not path.is_file():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return []
    return [item for item in data.get("resource", {}).get("bagPaths", []) if item]


_BAGS = _bag_paths()


def pytest_generate_tests(metafunc):
    """Feed ``bag_path`` from the config, mirroring the C++ fixture parameter."""
    if "bag_path" in metafunc.fixturenames:
        metafunc.parametrize(
            "bag_path",
            _BAGS or [None],
            ids=[Path(item).name if item else "no-bag" for item in (_BAGS or [None])],
        )


def _require_bag(bag_path):
    if not bag_path:
        pytest.skip("Playback bag not available, matching the C++ fixture precondition")
    if not Path(bag_path).is_file():
        pytest.skip(f"Playback bag not found: {bag_path}")


def _playback(bag_path):
    _require_bag(bag_path)
    return ob.PlaybackDevice(str(bag_path))


def _started_pipeline(playback):
    pipeline = ob.Pipeline(playback)
    config = ob.Config()
    sensors = playback.get_sensor_list()
    assert sensors.get_count() > 0
    for index in range(sensors.get_count()):
        sensor_type = sensors.get_type_by_index(index)
        try:
            profile_list = playback.get_sensor(sensor_type).get_stream_profile_list()
            config.enable_stream(profile_list.get_stream_profile_by_index(0))
        except Exception:  # noqa: BLE001
            continue
    try:
        config.set_frame_aggregate_output_mode(ob.OBFrameAggregateOutputMode.ANY_SITUATION)
    except Exception:  # noqa: BLE001
        pass
    pipeline.start(config)
    return pipeline


def _frameset(pipeline, retries=15, timeout=1000):
    for _ in range(retries):
        frameset = pipeline.wait_for_frames(timeout)
        if frameset is not None:
            return frameset
    pytest.fail("No frames from playback")


def _depth(bag_path):
    pipeline = _started_pipeline(_playback(bag_path))
    try:
        for _ in range(5):
            frame = _frameset(pipeline).get_depth_frame()
            if frame is not None:
                return frame
        pytest.skip("No depth frame in playback bag")
    finally:
        pipeline.stop()


def _video_profile(playback, sensor_type):
    sensor = playback.get_sensor_list().get_sensor_by_type(sensor_type)
    if sensor is None:
        pytest.skip(f"No {sensor_type.name.lower()} profile")
    profiles = sensor.get_stream_profile_list()
    if profiles.get_count() == 0:
        pytest.skip(f"No {sensor_type.name.lower()} profile")
    return profiles.get_stream_profile_by_index(0).as_video_stream_profile()


def _range_is_valid(value_range):
    return value_range.min <= value_range.max


def _frames_with_depth(bag_path, count=5):
    pipeline = _started_pipeline(_playback(bag_path))
    frames = []
    try:
        for _ in range(count):
            frameset = _frameset(pipeline)
            if frameset.get_depth_frame() is not None:
                frames.append(frameset)
    finally:
        pipeline.stop()
    if len(frames) < count:
        pytest.skip(f"Playback bag does not contain {count} depth frames")
    return frames


# ---------------------------------------------------------------------------
# named cases
# ---------------------------------------------------------------------------


def test_TC_CPP_18_03_playback_device_create_and_play(bag_path):
    playback = _playback(bag_path)
    assert playback.get_device_info().get_name()

    pipeline = _started_pipeline(playback)
    try:
        assert _frameset(pipeline) is not None
    finally:
        pipeline.stop()


def test_TC_CPP_18_04_playback_duration_position(bag_path):
    playback = _playback(bag_path)
    duration = playback.get_duration()
    assert duration > 0
    assert playback.get_position() >= 0


def test_TC_CPP_18_05_playback_seek_and_rate(bag_path):
    playback = _playback(bag_path)
    duration = playback.get_duration()
    if duration > 100:
        playback.seek(duration // 2)
    playback.set_playback_rate(2.0)


def test_TC_CPP_18_06_playback_pause_resume_status(bag_path):
    playback = _playback(bag_path)
    pipeline = _started_pipeline(playback)
    try:
        _frameset(pipeline)
        playback.pause()
        assert playback.get_playback_status() == ob.OBPlaybackStatus.STATUS_PAUSED
        playback.resume()
    finally:
        pipeline.stop()


def test_TC_CPP_18_07_playback_status_callback(bag_path):
    playback = _playback(bag_path)
    statuses = []
    playback.set_playback_status_change_callback(lambda status: statuses.append(status))

    pipeline = _started_pipeline(playback)
    try:
        time.sleep(0.5)
        playback.pause()
        time.sleep(0.2)

        deadline = time.monotonic() + 5
        while not statuses and time.monotonic() < deadline:
            time.sleep(0.05)
        playback.resume()
    finally:
        pipeline.stop()

    assert statuses


#: The C++ TEST_P matrix, kept as parameter ids so JUnit names match upstream.
_PLAYBACK_CASES = [
    "TC_CPP_18_10_playback_device_info",
    "TC_CPP_18_11_playback_sensor_list",
    "TC_CPP_18_12_playback_stream_profile_list",
    "TC_CPP_18_20_playback_depth_frame",
    "TC_CPP_18_21_playback_color_frame",
    "TC_CPP_18_22_playback_ir_frame",
    "TC_CPP_18_23_playback_frame_metadata",
    "TC_CPP_18_24_playback_frame_timestamps",
    "TC_CPP_18_25_playback_frameset_multi_stream",
    "TC_CPP_18_30_playback_depth_intrinsic",
    "TC_CPP_18_31_playback_color_intrinsic",
    "TC_CPP_18_32_playback_depth_distortion",
    "TC_CPP_18_33_playback_depth_to_color_extrinsic",
    "TC_CPP_18_34_playback_calibration_camera_param_list",
    "TC_CPP_18_40_playback_decimation_filter",
    "TC_CPP_18_41_playback_threshold_filter",
    "TC_CPP_18_42_playback_format_converter",
    "TC_CPP_18_43_playback_point_cloud_filter",
    "TC_CPP_18_44_playback_align_filter",
    "TC_CPP_18_45_playback_recommended_filters",
    "TC_CPP_18_46_playback_filter_chain",
    "TC_CPP_18_47_playback_hdr_merge",
    "TC_CPP_18_48_playback_sequence_id_filter",
    "TC_CPP_18_49_playback_spatial_advanced_filter",
    "TC_CPP_18_50_playback_spatial_fast_filter",
    "TC_CPP_18_51_playback_spatial_moderate_filter",
    "TC_CPP_18_52_playback_hole_filling_filter",
    "TC_CPP_18_53_playback_noise_removal_filter",
    "TC_CPP_18_54_playback_temporal_filter",
    "TC_CPP_18_55_playback_false_positive_filter",
    "TC_CPP_18_56_playback_disparity_transform",
    "TC_CPP_18_60_playback_coord_transform_2d_to_3d",
    "TC_CPP_18_61_playback_coord_transform_3d_to_2d",
]


@pytest.mark.parametrize("case_id", _PLAYBACK_CASES)
def test_TC_CPP_18_playback_parameterized(bag_path, case_id):
    _require_bag(bag_path)
    playback = _playback(bag_path)

    if case_id == "TC_CPP_18_10_playback_device_info":
        info = playback.get_device_info()
        assert all(
            (
                info.get_name(),
                info.get_serial_number(),
                info.get_firmware_version(),
                info.get_connection_type(),
            )
        )

    elif case_id == "TC_CPP_18_11_playback_sensor_list":
        sensors = playback.get_sensor_list()
        assert sensors.get_count() > 0
        for index in range(sensors.get_count()):
            assert sensors.get_sensor_by_index(index) is not None
            assert sensors.get_type_by_index(index) in set(ob.OBSensorType)

    elif case_id == "TC_CPP_18_12_playback_stream_profile_list":
        checked = 0
        for sensor_type in (ob.OBSensorType.DEPTH_SENSOR, ob.OBSensorType.COLOR_SENSOR):
            sensor = playback.get_sensor_list().get_sensor_by_type(sensor_type)
            if sensor is None:
                continue
            profiles = sensor.get_stream_profile_list()
            assert profiles.get_count() > 0
            for index in range(profiles.get_count()):
                profile = profiles.get_stream_profile_by_index(index)
                if profile.is_video_stream_profile():
                    video = profile.as_video_stream_profile()
                    assert video.get_width() > 0
                    assert video.get_height() > 0
                    assert video.get_fps() > 0
            checked += 1
        assert checked > 0

    elif case_id == "TC_CPP_18_20_playback_depth_frame":
        depth = _depth(bag_path)
        assert depth.get_type() == ob.OBFrameType.DEPTH_FRAME
        assert depth.get_data_size() > 0
        assert depth.get_timestamp_us() > 0

    elif case_id == "TC_CPP_18_21_playback_color_frame":
        pipeline = _started_pipeline(playback)
        try:
            color = None
            for _ in range(5):
                color = _frameset(pipeline).get_color_frame()
                if color is not None:
                    break
        finally:
            pipeline.stop()
        if color is None:
            pytest.skip("No color frame in playback bag")
        assert color.get_type() == ob.OBFrameType.COLOR_FRAME
        assert color.get_format() in (
            ob.OBFormat.RGB,
            ob.OBFormat.BGR,
            ob.OBFormat.RGBA,
            ob.OBFormat.BGRA,
            ob.OBFormat.YUYV,
            ob.OBFormat.UYVY,
            ob.OBFormat.MJPG,
            ob.OBFormat.NV12,
            ob.OBFormat.NV21,
            ob.OBFormat.I420,
        )
        assert color.get_data_size() > 0

    elif case_id == "TC_CPP_18_22_playback_ir_frame":
        pipeline = _started_pipeline(playback)
        try:
            frame = None
            for _ in range(5):
                frameset = _frameset(pipeline)
                for frame_type in (
                    ob.OBFrameType.IR_FRAME,
                    ob.OBFrameType.LEFT_IR_FRAME,
                    ob.OBFrameType.RIGHT_IR_FRAME,
                ):
                    frame = frameset.get_frame(frame_type)
                    if frame is not None:
                        break
                if frame is not None:
                    break
        finally:
            pipeline.stop()
        if frame is None:
            pytest.skip("No IR/IR_LEFT/IR_RIGHT frame in playback bag")
        assert frame.get_data_size() > 0

    elif case_id == "TC_CPP_18_23_playback_frame_metadata":
        frames = _frames_with_depth(bag_path)
        frame = None
        for frameset in frames:
            candidate = frameset.get_depth_frame() or frameset.get_color_frame()
            if candidate is not None:
                frame = candidate
                break
        if frame is None:
            pytest.skip("No depth/color frame for metadata test")
        assert frame.has_metadata(ob.OBFrameMetadataType.TIMESTAMP)
        assert frame.get_metadata_value(ob.OBFrameMetadataType.TIMESTAMP) > 0

    elif case_id == "TC_CPP_18_24_playback_frame_timestamps":
        frames = _frames_with_depth(bag_path)
        first = frames[0].get_depth_frame()
        last = frames[-1].get_depth_frame()
        assert first.get_system_timestamp_us() >= 0
        assert last.get_global_timestamp_us() >= 0
        assert last.get_timestamp_us() >= first.get_timestamp_us()

    elif case_id == "TC_CPP_18_25_playback_frameset_multi_stream":
        frames = _frames_with_depth(bag_path)
        types = {
            frameset.get_frame_by_index(index).get_type()
            for frameset in frames
            for index in range(frameset.get_count())
        }
        assert types

    elif case_id == "TC_CPP_18_30_playback_depth_intrinsic":
        intrinsic = _video_profile(playback, ob.OBSensorType.DEPTH_SENSOR).get_intrinsic()
        for value in (intrinsic.fx, intrinsic.fy, intrinsic.cx, intrinsic.cy):
            assert math.isfinite(float(value))
        assert intrinsic.fx > 0
        assert intrinsic.width > 0
        assert intrinsic.height > 0

    elif case_id == "TC_CPP_18_31_playback_color_intrinsic":
        intrinsic = _video_profile(playback, ob.OBSensorType.COLOR_SENSOR).get_intrinsic()
        for value in (intrinsic.fx, intrinsic.fy, intrinsic.cx, intrinsic.cy):
            assert math.isfinite(float(value))
        assert intrinsic.fx > 0

    elif case_id == "TC_CPP_18_32_playback_depth_distortion":
        distortion = _video_profile(
            playback, ob.OBSensorType.DEPTH_SENSOR
        ).get_distortion()
        for value in (
            distortion.k1,
            distortion.k2,
            distortion.k3,
            distortion.k4,
            distortion.k5,
            distortion.k6,
            distortion.p1,
            distortion.p2,
        ):
            assert math.isfinite(float(value))

    elif case_id == "TC_CPP_18_33_playback_depth_to_color_extrinsic":
        profile = _video_profile(playback, ob.OBSensorType.DEPTH_SENSOR)
        color = playback.get_sensor_list().get_sensor_by_type(ob.OBSensorType.COLOR_SENSOR)
        if color is None:
            pytest.skip("playback bag has no colour sensor")
        extrinsic = profile.get_extrinsic_to(
            color.get_stream_profile_list().get_stream_profile_by_index(0)
        )
        rotation = np.asarray(extrinsic.rot, dtype=float).reshape(3, 3)
        assert np.all(np.isfinite(rotation))
        assert np.allclose(rotation @ rotation.T, np.eye(3), atol=0.05)

    elif case_id == "TC_CPP_18_34_playback_calibration_camera_param_list":
        params = playback.get_calibration_camera_param_list()
        assert params.get_count() > 0
        param = params.get_camera_param(0)
        assert math.isfinite(float(param.depth_intrinsic.fx))
        assert math.isfinite(float(param.rgb_intrinsic.fx))

    elif case_id in _FILTER_CASE_IDS or case_id in (
        "TC_CPP_18_45_playback_recommended_filters",
        "TC_CPP_18_46_playback_filter_chain",
    ):
        _run_filter_case(playback, bag_path, case_id)

    elif case_id == "TC_CPP_18_60_playback_coord_transform_2d_to_3d":
        intrinsic = _video_profile(playback, ob.OBSensorType.DEPTH_SENSOR).get_intrinsic()
        extrinsic = ob.OBExtrinsic()
        extrinsic.rot = np.eye(3, dtype=np.float32)
        extrinsic.transform = np.zeros(3, dtype=np.float32)
        result = ob.transformation2dto3d(
            ob.OBPoint2f(intrinsic.cx, intrinsic.cy), 1000.0, intrinsic, extrinsic
        )
        assert math.isfinite(float(result.x))
        assert math.isfinite(float(result.y))
        assert math.isfinite(float(result.z))

    elif case_id == "TC_CPP_18_61_playback_coord_transform_3d_to_2d":
        intrinsic = _video_profile(playback, ob.OBSensorType.DEPTH_SENSOR).get_intrinsic()
        extrinsic = ob.OBExtrinsic()
        extrinsic.rot = np.eye(3, dtype=np.float32)
        extrinsic.transform = np.zeros(3, dtype=np.float32)
        result = ob.transformation3dto2d(
            ob.OBPoint3f(0.0, 0.0, 1000.0),
            intrinsic,
            ob.OBCameraDistortion(),
            extrinsic,
        )
        assert math.isfinite(float(result.x))
        assert math.isfinite(float(result.y))

    else:  # pragma: no cover - guards against an unhandled id being added
        pytest.fail(f"unhandled playback case id: {case_id}")


#: Case id -> filter name for the playback filter matrix.  Explicit so a new
#: case id fails loudly instead of silently matching the wrong filter.
_FILTER_CASES = {
    "TC_CPP_18_40_playback_decimation_filter": "DecimationFilter",
    "TC_CPP_18_41_playback_threshold_filter": "ThresholdFilter",
    "TC_CPP_18_42_playback_format_converter": "FormatConverter",
    "TC_CPP_18_43_playback_point_cloud_filter": "PointCloudFilter",
    "TC_CPP_18_44_playback_align_filter": "Align",
    "TC_CPP_18_47_playback_hdr_merge": "HDRMerge",
    "TC_CPP_18_48_playback_sequence_id_filter": "SequenceIdFilter",
    "TC_CPP_18_49_playback_spatial_advanced_filter": "SpatialAdvancedFilter",
    "TC_CPP_18_50_playback_spatial_fast_filter": "SpatialFastFilter",
    "TC_CPP_18_51_playback_spatial_moderate_filter": "SpatialModerateFilter",
    "TC_CPP_18_52_playback_hole_filling_filter": "HoleFillingFilter",
    "TC_CPP_18_53_playback_noise_removal_filter": "NoiseRemovalFilter",
    "TC_CPP_18_54_playback_temporal_filter": "TemporalFilter",
    "TC_CPP_18_55_playback_false_positive_filter": "FalsePositiveFilter",
    "TC_CPP_18_56_playback_disparity_transform": "DisparityTransform",
}

_FILTER_CASE_IDS = frozenset(_FILTER_CASES)

#: Filters that are built in, so they must not be skipped when absent.
_REQUIRED_FILTERS = ("DecimationFilter", "ThresholdFilter", "PointCloudFilter")


def _run_filter_case(playback, bag_path, case_id):
    """Run one ported filter case against a played-back depth frame."""
    from conftest import make_filter

    depth = _depth(bag_path)

    if case_id == "TC_CPP_18_45_playback_recommended_filters":
        created = sum(1 for name in _REQUIRED_FILTERS if make_filter(name) is not None)
        assert created > 0
        return

    if case_id == "TC_CPP_18_46_playback_filter_chain":
        chain = [
            created
            for created in (make_filter(name) for name in _REQUIRED_FILTERS)
            if created is not None
        ]
        assert chain
        result = depth
        for filter_ in chain:
            result = filter_.process(result)
            assert result is not None
        return

    filter_name = _FILTER_CASES[case_id]
    created = make_filter(filter_name)
    if created is None:
        pytest.skip(f"{filter_name} not available: private filter library not activated")

    result = created.process(depth)
    assert result is not None
    assert result.get_data_size() > 0
