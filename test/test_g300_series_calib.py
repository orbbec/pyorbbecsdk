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
G300 series camera calibration parameter tests.

Covers: Gemini 330 / 335 / 335L / 335Le / 335Lg / 336 / 336L / 330L / 305 / 345

Tests verify:
- Intrinsic parameters (focal length, principal point, image size) are physically valid
- Distortion coefficients are finite and bounded
- Extrinsic rotation matrix is orthogonal (det ≈ 1, R @ R.T ≈ I)
- Calibration list from device contains valid entries
"""

import pytest
import numpy as np

from pyorbbecsdk import Config, OBSensorType, OBError

pytestmark = [pytest.mark.hardware, pytest.mark.g300_series, pytest.mark.functional]

TIMEOUT_MS = 2000


def _get_pipeline_camera_param(pipeline):
    """Start depth+color pipeline and extract camera parameters."""
    config = Config()
    config.enable_stream(
        pipeline.get_stream_profile_list(OBSensorType.DEPTH_SENSOR)
                .get_default_video_stream_profile()
    )
    config.enable_stream(
        pipeline.get_stream_profile_list(OBSensorType.COLOR_SENSOR)
                .get_default_video_stream_profile()
    )
    pipeline.start(config)
    # Wait for at least one frame set so parameters are fully initialized
    import time
    deadline = time.time() + 5
    while time.time() < deadline:
        fs = pipeline.wait_for_frames(TIMEOUT_MS)
        if fs:
            break
    return pipeline.get_camera_param()


def _assert_intrinsic_valid(intrinsic, name):
    assert intrinsic.fx > 0,  f"{name}: fx must be > 0"
    assert intrinsic.fy > 0,  f"{name}: fy must be > 0"
    assert intrinsic.cx > 0,  f"{name}: cx must be > 0"
    assert intrinsic.cy > 0,  f"{name}: cy must be > 0"
    assert intrinsic.width  > 0
    assert intrinsic.height > 0
    assert 100 <= intrinsic.fx <= 5000, f"{name}: fx={intrinsic.fx} out of range"
    assert 100 <= intrinsic.fy <= 5000, f"{name}: fy={intrinsic.fy} out of range"
    assert 0 < intrinsic.cx < intrinsic.width,  f"{name}: cx={intrinsic.cx} out of range"
    assert 0 < intrinsic.cy < intrinsic.height, f"{name}: cy={intrinsic.cy} out of range"


class TestPipelineCameraParam:

    def test_camera_param_accessible(self, pipeline, g300_series_device):
        """get_camera_param() must succeed after pipeline start."""
        try:
            param = _get_pipeline_camera_param(pipeline)
            assert param is not None
        except OBError as e:
            pytest.fail(f"get_camera_param() raised OBError: {e}")

    def test_depth_intrinsics_valid(self, pipeline, g300_series_device):
        param = _get_pipeline_camera_param(pipeline)
        _assert_intrinsic_valid(param.depth_intrinsic, "depth")

    def test_color_intrinsics_valid(self, pipeline, g300_series_device):
        param = _get_pipeline_camera_param(pipeline)
        _assert_intrinsic_valid(param.rgb_intrinsic, "color")

    def test_depth_distortion_bounded(self, pipeline, g300_series_device):
        """Distortion coefficients must be finite and |val| < 10."""
        param = _get_pipeline_camera_param(pipeline)
        dist = param.depth_distortion
        for attr in ["k1", "k2", "k3", "p1", "p2"]:
            val = getattr(dist, attr, None)
            if val is not None:
                assert np.isfinite(val), f"depth_distortion.{attr} is not finite"
                assert abs(val) < 10.0, f"depth_distortion.{attr}={val} seems large"

    def test_color_distortion_bounded(self, pipeline, g300_series_device):
        param = _get_pipeline_camera_param(pipeline)
        dist = param.rgb_distortion
        for attr in ["k1", "k2", "k3", "p1", "p2"]:
            val = getattr(dist, attr, None)
            if val is not None:
                assert np.isfinite(val), f"rgb_distortion.{attr} is not finite"
                assert abs(val) < 10.0, f"rgb_distortion.{attr}={val} seems large"

    def test_extrinsic_rotation_finite(self, pipeline, g300_series_device):
        param = _get_pipeline_camera_param(pipeline)
        rot = param.transform.rot
        for val in rot:
            assert np.isfinite(val), f"Extrinsic rotation contains non-finite value: {val}"

    def test_extrinsic_rotation_near_orthogonal(self, pipeline, g300_series_device):
        """Rotation matrix R must satisfy det(R) ≈ 1 and R @ R.T ≈ I."""
        param = _get_pipeline_camera_param(pipeline)
        R = np.array(param.transform.rot, dtype=np.float64).reshape(3, 3)
        det = float(np.linalg.det(R))
        assert abs(det - 1.0) < 0.05, f"det(R)={det:.4f} deviates from 1.0"
        identity_residual = np.max(np.abs(R @ R.T - np.eye(3)))
        assert identity_residual < 0.05, (
            f"R @ R.T residual {identity_residual:.4f} — R is not orthogonal"
        )


class TestCalibrationList:

    def test_calib_list_nonempty(self, g300_series_device):
        calib = g300_series_device.get_calibration_camera_param_list()
        assert calib is not None and calib.get_count() > 0

    def test_calib_entries_have_valid_depth_intrinsics(self, g300_series_device):
        calib = g300_series_device.get_calibration_camera_param_list()
        for i in range(calib.get_count()):
            _assert_intrinsic_valid(calib.get_camera_param(i).depth_intrinsic,
                                    f"calib[{i}].depth")

    def test_calib_entries_have_valid_color_intrinsics(self, g300_series_device):
        calib = g300_series_device.get_calibration_camera_param_list()
        for i in range(calib.get_count()):
            _assert_intrinsic_valid(calib.get_camera_param(i).rgb_intrinsic,
                                    f"calib[{i}].color")
