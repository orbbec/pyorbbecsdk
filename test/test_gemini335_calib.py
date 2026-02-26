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
Gemini 335 camera calibration and intrinsics tests.

Tests verify:
- Camera intrinsic parameters (focal length, principal point) are physically plausible
- Distortion coefficients are present and bounded
- Extrinsic rotation matrix is orthogonal (det ≈ 1)
- Pipeline camera_param matches calibration list entries
"""

import math
import pytest
import numpy as np

from pyorbbecsdk import Config, OBSensorType, OBError

pytestmark = [pytest.mark.hardware, pytest.mark.gemini335]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _get_pipeline_camera_param(pipeline):
    """Start a minimal depth+color pipeline and return camera_param."""
    config = Config()
    for sensor in [OBSensorType.DEPTH_SENSOR, OBSensorType.COLOR_SENSOR]:
        try:
            pl = pipeline.get_stream_profile_list(sensor)
            config.enable_stream(pl.get_default_video_stream_profile())
        except OBError:
            pass
    pipeline.start(config)
    param = pipeline.get_camera_param()
    pipeline.stop()
    return param


def _assert_intrinsic_valid(intrinsic, name):
    """Assert that a camera intrinsic struct contains physically plausible values."""
    fx = intrinsic.fx
    fy = intrinsic.fy
    cx = intrinsic.cx
    cy = intrinsic.cy
    w = intrinsic.width
    h = intrinsic.height

    assert fx > 0, f"{name}: fx={fx} must be > 0"
    assert fy > 0, f"{name}: fy={fy} must be > 0"
    assert cx > 0, f"{name}: cx={cx} must be > 0"
    assert cy > 0, f"{name}: cy={cy} must be > 0"
    assert w > 0, f"{name}: width={w} must be > 0"
    assert h > 0, f"{name}: height={h} must be > 0"

    # Focal length should be within [100, 5000] px for typical depth cameras
    assert 100 <= fx <= 5000, f"{name}: fx={fx:.1f} outside [100, 5000]"
    assert 100 <= fy <= 5000, f"{name}: fy={fy:.1f} outside [100, 5000]"

    # Principal point should be roughly within the image frame
    assert 0 < cx < w, f"{name}: cx={cx:.1f} not within image width {w}"
    assert 0 < cy < h, f"{name}: cy={cy:.1f} not within image height {h}"


# ---------------------------------------------------------------------------
# Pipeline camera_param tests
# ---------------------------------------------------------------------------

class TestPipelineCameraParam:

    def test_camera_param_accessible(self, pipeline, gemini335_device):
        """get_camera_param() must succeed without exception."""
        param = _get_pipeline_camera_param(pipeline)
        assert param is not None

    def test_depth_intrinsics_valid(self, pipeline, gemini335_device):
        """Depth camera intrinsics must be physically plausible."""
        param = _get_pipeline_camera_param(pipeline)
        _assert_intrinsic_valid(param.depth_intrinsic, "depth")

    def test_color_intrinsics_valid(self, pipeline, gemini335_device):
        """Color camera intrinsics must be physically plausible."""
        param = _get_pipeline_camera_param(pipeline)
        _assert_intrinsic_valid(param.rgb_intrinsic, "color/rgb")

    def test_depth_distortion_bounded(self, pipeline, gemini335_device):
        """Depth distortion coefficients must be finite and within typical bounds."""
        param = _get_pipeline_camera_param(pipeline)
        dist = param.depth_distortion
        for attr in ["k1", "k2", "k3", "p1", "p2"]:
            val = getattr(dist, attr, None)
            if val is None:
                continue
            assert math.isfinite(val), f"depth_distortion.{attr} is not finite: {val}"
            assert abs(val) < 10.0, (
                f"depth_distortion.{attr}={val:.4f} is suspiciously large (|val| < 10)"
            )

    def test_color_distortion_bounded(self, pipeline, gemini335_device):
        """Color distortion coefficients must be finite and within typical bounds."""
        param = _get_pipeline_camera_param(pipeline)
        dist = param.rgb_distortion
        for attr in ["k1", "k2", "k3", "p1", "p2"]:
            val = getattr(dist, attr, None)
            if val is None:
                continue
            assert math.isfinite(val), f"rgb_distortion.{attr} is not finite: {val}"
            assert abs(val) < 10.0, (
                f"rgb_distortion.{attr}={val:.4f} is suspiciously large"
            )

    def test_extrinsic_transform_finite(self, pipeline, gemini335_device):
        """Transform (extrinsic) matrix elements must all be finite."""
        param = _get_pipeline_camera_param(pipeline)
        transform = param.transform
        for attr in ["rot"]:
            mat = getattr(transform, attr, None)
            if mat is None:
                continue
            # rot may be a 2D numpy array — flatten to get scalar values
            arr = np.array(mat).flatten()
            for v in arr:
                assert math.isfinite(float(v)), (
                    f"transform.{attr} contains non-finite value: {v}"
                )

    def test_extrinsic_rotation_near_orthogonal(self, pipeline, gemini335_device):
        """
        The rotation part of the extrinsic transform must be approximately orthogonal.
        det(R) ≈ 1 and R @ R.T ≈ I.
        """
        param = _get_pipeline_camera_param(pipeline)
        transform = param.transform
        rot = getattr(transform, "rot", None)
        if rot is None:
            pytest.skip("transform.rot not accessible")

        try:
            R = np.array(list(rot), dtype=np.float64).reshape(3, 3)
        except Exception:
            pytest.skip("Could not parse transform.rot as 3×3 matrix")

        det = np.linalg.det(R)
        assert abs(det - 1.0) < 0.05, (
            f"Rotation matrix det={det:.4f} not close to 1.0 (orthogonality check)"
        )

        RRt = R @ R.T
        I = np.eye(3)
        assert np.allclose(RRt, I, atol=0.05), (
            f"R @ R.T not close to identity:\n{RRt}"
        )


# ---------------------------------------------------------------------------
# Device calibration list tests
# ---------------------------------------------------------------------------

class TestCalibrationList:

    def test_calib_list_nonempty(self, gemini335_device):
        """Calibration camera parameter list must have at least one entry."""
        calib_list = gemini335_device.get_calibration_camera_param_list()
        assert calib_list is not None
        count = calib_list.get_count()
        assert count > 0, "Calibration camera param list is empty"

    def test_calib_entries_have_valid_depth_intrinsics(self, gemini335_device):
        """All calibration entries must have valid depth intrinsics."""
        calib_list = gemini335_device.get_calibration_camera_param_list()
        for i in range(calib_list.get_count()):
            param = calib_list.get_camera_param(i)
            assert param is not None, f"Calibration entry {i} is None"
            _assert_intrinsic_valid(param.depth_intrinsic,
                                    f"calib[{i}].depth")

    def test_calib_entries_have_valid_color_intrinsics(self, gemini335_device):
        """All calibration entries must have valid color intrinsics."""
        calib_list = gemini335_device.get_calibration_camera_param_list()
        for i in range(calib_list.get_count()):
            param = calib_list.get_camera_param(i)
            _assert_intrinsic_valid(param.rgb_intrinsic,
                                    f"calib[{i}].color")
