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
Femto Bolt / Femto Mega camera calibration parameter tests.

Femto ToF calibration notes:
- Depth resolution is typically 640 × 576 (different from G300 structured light)
- Focal lengths tend to be shorter (wider FoV ToF sensor)
- Extrinsic rotation between depth and color cameras must be orthogonal

Tests verify the same calibration validity criteria as G300 series,
adapted for Femto's different sensor geometry.
"""

import time

import numpy as np
import pytest

from pyorbbecsdk import Config, OBError, OBSensorType

pytestmark = [pytest.mark.hardware, pytest.mark.femto, pytest.mark.functional]

TIMEOUT_MS = 2000


def _get_pipeline_camera_param(pipeline):
    config = Config()
    config.enable_stream(pipeline.get_stream_profile_list(OBSensorType.DEPTH_SENSOR).get_default_video_stream_profile())
    config.enable_stream(pipeline.get_stream_profile_list(OBSensorType.COLOR_SENSOR).get_default_video_stream_profile())
    pipeline.start(config)
    deadline = time.time() + 5
    while time.time() < deadline:
        if pipeline.wait_for_frames(TIMEOUT_MS):
            break
    return pipeline.get_camera_param()


def _assert_intrinsic_valid(intrinsic, name):
    assert intrinsic.fx > 0
    assert intrinsic.fy > 0
    assert intrinsic.cx > 0
    assert intrinsic.cy > 0
    assert intrinsic.width > 0
    assert intrinsic.height > 0
    assert 50 <= intrinsic.fx <= 5000, f"{name}: fx={intrinsic.fx} out of range"
    assert 50 <= intrinsic.fy <= 5000, f"{name}: fy={intrinsic.fy} out of range"
    assert 0 < intrinsic.cx < intrinsic.width
    assert 0 < intrinsic.cy < intrinsic.height


class TestFemtoPipelineCameraParam:

    def test_camera_param_accessible(self, pipeline, femto_device):
        try:
            param = _get_pipeline_camera_param(pipeline)
            assert param is not None
        except OBError as e:
            pytest.fail(f"get_camera_param() raised: {e}")

    def test_depth_intrinsics_valid(self, pipeline, femto_device):
        param = _get_pipeline_camera_param(pipeline)
        _assert_intrinsic_valid(param.depth_intrinsic, "femto_depth")

    def test_color_intrinsics_valid(self, pipeline, femto_device):
        param = _get_pipeline_camera_param(pipeline)
        _assert_intrinsic_valid(param.rgb_intrinsic, "femto_color")

    def test_depth_distortion_bounded(self, pipeline, femto_device):
        param = _get_pipeline_camera_param(pipeline)
        for attr in ["k1", "k2", "k3", "p1", "p2"]:
            val = getattr(param.depth_distortion, attr, None)
            if val is not None:
                assert np.isfinite(val)
                assert abs(val) < 10.0

    def test_extrinsic_rotation_near_orthogonal(self, pipeline, femto_device):
        param = _get_pipeline_camera_param(pipeline)
        R = np.array(param.transform.rot, dtype=np.float64).reshape(3, 3)
        assert abs(float(np.linalg.det(R)) - 1.0) < 0.05
        assert np.max(np.abs(R @ R.T - np.eye(3))) < 0.05


class TestFemtoCalibrationList:

    def test_calib_list_nonempty(self, femto_device):
        calib = femto_device.get_calibration_camera_param_list()
        assert calib and calib.get_count() > 0

    def test_calib_entries_valid(self, femto_device):
        calib = femto_device.get_calibration_camera_param_list()
        for i in range(calib.get_count()):
            _assert_intrinsic_valid(calib.get_camera_param(i).depth_intrinsic, f"femto_calib[{i}].depth")
