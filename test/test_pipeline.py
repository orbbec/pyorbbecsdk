import pytest

from pyorbbecsdk import Pipeline, Config, OBSensorType

pytestmark = pytest.mark.hardware


class TestPipelineCameraParam:

    def test_camera_param_accessible(self, pipeline, device):
        """get_camera_param() must not raise; returned object must be non-None."""
        config = Config()
        for sensor in [OBSensorType.DEPTH_SENSOR, OBSensorType.COLOR_SENSOR]:
            try:
                pl = pipeline.get_stream_profile_list(sensor)
                config.enable_stream(pl.get_default_video_stream_profile())
            except Exception:
                pass
        pipeline.start(config)
        param = pipeline.get_camera_param()
        assert param is not None

    def test_depth_intrinsic_not_none(self, pipeline, device):
        config = Config()
        try:
            pl = pipeline.get_stream_profile_list(OBSensorType.DEPTH_SENSOR)
            config.enable_stream(pl.get_default_video_stream_profile())
        except Exception:
            pytest.skip("Could not enable depth stream")
        pipeline.start(config)
        param = pipeline.get_camera_param()
        assert param.depth_intrinsic is not None

    def test_rgb_intrinsic_not_none(self, pipeline, device):
        config = Config()
        for sensor in [OBSensorType.DEPTH_SENSOR, OBSensorType.COLOR_SENSOR]:
            try:
                pl = pipeline.get_stream_profile_list(sensor)
                config.enable_stream(pl.get_default_video_stream_profile())
            except Exception:
                pass
        pipeline.start(config)
        param = pipeline.get_camera_param()
        assert param.rgb_intrinsic is not None

    def test_transform_not_none(self, pipeline, device):
        config = Config()
        for sensor in [OBSensorType.DEPTH_SENSOR, OBSensorType.COLOR_SENSOR]:
            try:
                pl = pipeline.get_stream_profile_list(sensor)
                config.enable_stream(pl.get_default_video_stream_profile())
            except Exception:
                pass
        pipeline.start(config)
        param = pipeline.get_camera_param()
        assert param.transform is not None
