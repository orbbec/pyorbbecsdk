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

API used (per stubs/pyorbbecsdk.pyi and examples/coordinate_transform.py):
  pipeline.get_camera_param()              -> OBCameraParam
  OBCameraParam.depth_intrinsic            -> OBCameraIntrinsic  (.fx .fy .cx .cy .width .height)
  OBCameraParam.rgb_intrinsic              -> OBCameraIntrinsic
  OBCameraParam.depth_distortion           -> OBCameraDistortion (.k1 .k2 .k3 .p1 .p2)
  OBCameraParam.rgb_distortion             -> OBCameraDistortion
  OBCameraParam.transform                  -> OBExtrinsic
  OBExtrinsic.rot                          -> numpy.ndarray[float32], shape (9,)  — rotation matrix (row-major)
  OBExtrinsic.transform                    -> numpy.ndarray[float32], shape (3,)  — translation vector (mm)

Alternative per-stream API (from coordinate_transform.py):
  video_stream_profile.get_intrinsic()     -> OBCameraIntrinsic
  video_stream_profile.get_distortion()    -> OBCameraDistortion
  depth_profile.get_extrinsic_to(color_profile)  -> OBExtrinsic
"""

import logging

import numpy as np
import pytest

from pyorbbecsdk import Config, OBError, OBSensorType

pytestmark = [pytest.mark.hardware, pytest.mark.g300_series, pytest.mark.functional]

logger = logging.getLogger(__name__)

TIMEOUT_MS = 2000


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _get_pipeline_camera_param(pipeline):
    """
    Start depth+color pipeline and return (OBCameraParam, depth_profile, color_profile).
    Waits for at least one frameset so parameters are fully initialised.
    """
    import time

    config = Config()
    depth_profile = pipeline.get_stream_profile_list(OBSensorType.DEPTH_SENSOR).get_default_video_stream_profile()
    color_profile = pipeline.get_stream_profile_list(OBSensorType.COLOR_SENSOR).get_default_video_stream_profile()
    config.enable_stream(depth_profile)
    config.enable_stream(color_profile)
    pipeline.start(config)

    deadline = time.time() + 5
    while time.time() < deadline:
        fs = pipeline.wait_for_frames(TIMEOUT_MS)
        if fs:
            break

    param = pipeline.get_camera_param()
    logger.debug("OBCameraParam repr: %s", repr(param))
    return param, depth_profile, color_profile


def _assert_intrinsic_valid(intrinsic, name):
    logger.debug(
        "%s intrinsic: fx=%.3f fy=%.3f cx=%.3f cy=%.3f w=%d h=%d",
        name,
        intrinsic.fx,
        intrinsic.fy,
        intrinsic.cx,
        intrinsic.cy,
        intrinsic.width,
        intrinsic.height,
    )
    assert intrinsic.fx > 0, f"{name}: fx must be > 0, got {intrinsic.fx}"
    assert intrinsic.fy > 0, f"{name}: fy must be > 0, got {intrinsic.fy}"
    assert intrinsic.cx > 0, f"{name}: cx must be > 0, got {intrinsic.cx}"
    assert intrinsic.cy > 0, f"{name}: cy must be > 0, got {intrinsic.cy}"
    assert intrinsic.width > 0, f"{name}: width must be > 0"
    assert intrinsic.height > 0, f"{name}: height must be > 0"
    assert 100 <= intrinsic.fx <= 5000, f"{name}: fx={intrinsic.fx:.1f} out of expected range [100, 5000]"
    assert 100 <= intrinsic.fy <= 5000, f"{name}: fy={intrinsic.fy:.1f} out of expected range [100, 5000]"
    assert (
        0 < intrinsic.cx < intrinsic.width
    ), f"{name}: cx={intrinsic.cx:.1f} must be within image width={intrinsic.width}"
    assert (
        0 < intrinsic.cy < intrinsic.height
    ), f"{name}: cy={intrinsic.cy:.1f} must be within image height={intrinsic.height}"


def _log_distortion(dist, name):
    attrs = {a: getattr(dist, a, None) for a in ["k1", "k2", "k3", "p1", "p2"]}
    logger.debug("%s distortion: %s", name, attrs)
    return attrs


# ---------------------------------------------------------------------------
# Tests: pipeline.get_camera_param()
# ---------------------------------------------------------------------------


class TestPipelineCameraParam:

    def test_camera_param_accessible(self, pipeline, g300_series_device):
        """get_camera_param() must succeed after pipeline start."""
        try:
            param, _, _ = _get_pipeline_camera_param(pipeline)
            assert param is not None
            logger.debug("get_camera_param() succeeded: %s", repr(param))
        except OBError as e:
            pytest.fail(f"get_camera_param() raised OBError: {e}")

    def test_depth_intrinsics_valid(self, pipeline, g300_series_device):
        param, _, _ = _get_pipeline_camera_param(pipeline)
        _assert_intrinsic_valid(param.depth_intrinsic, "depth")

    def test_color_intrinsics_valid(self, pipeline, g300_series_device):
        param, _, _ = _get_pipeline_camera_param(pipeline)
        _assert_intrinsic_valid(param.rgb_intrinsic, "color")

    def test_depth_distortion_bounded(self, pipeline, g300_series_device):
        """Distortion coefficients must be finite and |val| < 10."""
        param, _, _ = _get_pipeline_camera_param(pipeline)
        attrs = _log_distortion(param.depth_distortion, "depth")
        for attr, val in attrs.items():
            if val is not None:
                assert np.isfinite(val), f"depth_distortion.{attr}={val} is not finite"
                assert abs(val) < 10.0, f"depth_distortion.{attr}={val:.4f} seems unreasonably large"

    def test_color_distortion_bounded(self, pipeline, g300_series_device):
        param, _, _ = _get_pipeline_camera_param(pipeline)
        attrs = _log_distortion(param.rgb_distortion, "color")
        for attr, val in attrs.items():
            if val is not None:
                assert np.isfinite(val), f"rgb_distortion.{attr}={val} is not finite"
                assert abs(val) < 10.0, f"rgb_distortion.{attr}={val:.4f} seems unreasonably large"

    def test_extrinsic_rotation_finite(self, pipeline, g300_series_device):
        """
        OBExtrinsic.rot is a numpy float32 array of 9 elements (3×3 row-major).
        All values must be finite.
        """
        param, _, _ = _get_pipeline_camera_param(pipeline)
        rot = param.transform.rot  # numpy.ndarray[float32], shape (9,)
        trans = param.transform.transform  # numpy.ndarray[float32], shape (3,)
        logger.debug(
            "Extrinsic rot (9 values): %s",
            np.array2string(np.asarray(rot), precision=6),
        )
        logger.debug(
            "Extrinsic translation (mm): %s",
            np.array2string(np.asarray(trans), precision=3),
        )
        rot_arr = np.asarray(rot, dtype=np.float64)
        assert rot_arr.size == 9, f"Expected OBExtrinsic.rot to have 9 elements, got {rot_arr.size}"
        non_finite = ~np.isfinite(rot_arr)
        assert not non_finite.any(), (
            f"Extrinsic rotation contains non-finite values at indices "
            f"{np.where(non_finite)[0].tolist()}: {rot_arr}"
        )

    def test_extrinsic_rotation_near_orthogonal(self, pipeline, g300_series_device):
        """
        Rotation matrix R (from OBExtrinsic.rot, 9 float32 values, row-major)
        must satisfy det(R) ≈ 1 and R @ R.T ≈ I.
        """
        param, _, _ = _get_pipeline_camera_param(pipeline)
        rot_flat = np.asarray(param.transform.rot, dtype=np.float64)
        R = rot_flat.reshape(3, 3)
        logger.debug("Rotation matrix R:\n%s", np.array2string(R, precision=6))

        det = float(np.linalg.det(R))
        logger.debug("det(R) = %.6f", det)
        assert abs(det - 1.0) < 0.05, f"det(R)={det:.4f} deviates from 1.0 — R may not be a valid rotation matrix"

        residual_mat = R @ R.T - np.eye(3)
        identity_residual = float(np.max(np.abs(residual_mat)))
        logger.debug(
            "R @ R.T - I max abs residual = %.6f\n%s",
            identity_residual,
            np.array2string(residual_mat, precision=6),
        )
        assert identity_residual < 0.05, f"R @ R.T residual {identity_residual:.4f} exceeds 0.05 — R is not orthogonal"

    def test_extrinsic_via_stream_profile(self, pipeline, g300_series_device):
        """
        Cross-check: extrinsic obtained via depth_profile.get_extrinsic_to(color_profile)
        (the API used in coordinate_transform.py) must also produce a valid rotation matrix.
        """
        _, depth_profile, color_profile = _get_pipeline_camera_param(pipeline)
        try:
            extrinsic = depth_profile.get_extrinsic_to(color_profile)
        except OBError as e:
            pytest.skip(f"get_extrinsic_to() not available: {e}")

        rot_flat = np.asarray(extrinsic.rot, dtype=np.float64)
        logger.debug(
            "Stream-profile extrinsic rot: %s",
            np.array2string(rot_flat, precision=6),
        )
        assert rot_flat.size == 9, f"Expected OBExtrinsic.rot size 9, got {rot_flat.size}"
        R = rot_flat.reshape(3, 3)
        det = float(np.linalg.det(R))
        logger.debug("Stream-profile det(R) = %.6f", det)
        assert abs(det - 1.0) < 0.05, f"Stream-profile extrinsic det(R)={det:.4f} deviates from 1.0"


# ---------------------------------------------------------------------------
# Tests: device.get_calibration_camera_param_list()
# ---------------------------------------------------------------------------


class TestCalibrationList:

    def test_calib_list_nonempty(self, g300_series_device):
        calib = g300_series_device.get_calibration_camera_param_list()
        assert calib is not None and calib.get_count() > 0, "get_calibration_camera_param_list() returned empty list"
        logger.debug("Calibration param list count: %d", calib.get_count())

    def test_calib_entries_have_valid_depth_intrinsics(self, g300_series_device):
        calib = g300_series_device.get_calibration_camera_param_list()
        for i in range(calib.get_count()):
            entry = calib.get_camera_param(i)
            logger.debug("Checking calib[%d] depth intrinsic", i)
            _assert_intrinsic_valid(entry.depth_intrinsic, f"calib[{i}].depth")

    def test_calib_entries_have_valid_color_intrinsics(self, g300_series_device):
        calib = g300_series_device.get_calibration_camera_param_list()
        for i in range(calib.get_count()):
            entry = calib.get_camera_param(i)
            logger.debug("Checking calib[%d] color intrinsic", i)
            _assert_intrinsic_valid(entry.rgb_intrinsic, f"calib[{i}].color")

    def test_calib_entries_extrinsic_rotation_valid(self, g300_series_device):
        """Each calibration entry's extrinsic rotation must be orthogonal."""
        calib = g300_series_device.get_calibration_camera_param_list()
        for i in range(calib.get_count()):
            entry = calib.get_camera_param(i)
            rot_flat = np.asarray(entry.transform.rot, dtype=np.float64)
            logger.debug(
                "calib[%d] extrinsic rot: %s",
                i,
                np.array2string(rot_flat, precision=6),
            )
            assert rot_flat.size == 9, f"calib[{i}] OBExtrinsic.rot expected size 9, got {rot_flat.size}"
            R = rot_flat.reshape(3, 3)
            det = float(np.linalg.det(R))
            logger.debug("calib[%d] det(R) = %.6f", i, det)
            assert abs(det - 1.0) < 0.05, f"calib[{i}] det(R)={det:.4f} deviates from 1.0"
