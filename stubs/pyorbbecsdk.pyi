"""
OrbbecSDK python binding
"""
from __future__ import annotations
import numpy
import typing
__all__ = ['AccelFrame', 'AccelStreamProfile', 'AlignFilter', 'CameraParamList', 'ColorFrame', 'Config', 'Context', 'DecimationFilter', 'DepthFrame', 'Device', 'DeviceInfo', 'DeviceList', 'DevicePresetList', 'DisparityTransform', 'EdgeNoiseRemovalFilter', 'Filter', 'FormatConvertFilter', 'Frame', 'FrameSet', 'GyroFrame', 'GyroStreamProfile', 'HDRMergeFilter', 'HoleFillingFilter', 'IRFrame', 'NoiseRemovalFilter', 'OBAccelFullScaleRange', 'OBAccelIntrinsic', 'OBAccelValue', 'OBAlignMode', 'OBBaselineCalibrationParam', 'OBCalibrationParam', 'OBCameraAlignIntrinsic', 'OBCameraDistortion', 'OBCameraDistortionModel', 'OBCameraIntrinsic', 'OBCameraParam', 'OBCmdVersion', 'OBColorPoint', 'OBCommunicationType', 'OBCompressionMode', 'OBCompressionParams', 'OBConvertFormat', 'OBCoordinateSystemType', 'OBD2CTransform', 'OBDCPowerState', 'OBDDONoiseRemovalType', 'OBDataBundle', 'OBDataTranState', 'OBDepthCroppingMode', 'OBDepthPrecisionLevel', 'OBDepthWorkMode', 'OBDepthWorkModeList', 'OBDeviceDevelopmentMode', 'OBDeviceIpAddrConfig', 'OBDeviceSyncConfig', 'OBDeviceTemperature', 'OBDeviceTimestampResetConfig', 'OBDeviceType', 'OBEdgeNoiseRemovalFilterParams', 'OBEdgeNoiseRemovalType', 'OBError', 'OBException', 'OBFileTranState', 'OBFilterList', 'OBFloatPropertyRange', 'OBFormat', 'OBFrameAggregateOutputMode', 'OBFrameMetadataType', 'OBFrameType', 'OBGyroIntrinsic', 'OBGyroSampleRate', 'OBHdrConfig', 'OBHoleFillingMode', 'OBIntPropertyRange', 'OBLogLevel', 'OBMediaState', 'OBMediaType', 'OBMultiDeviceSyncConfig', 'OBMultiDeviceSyncMode', 'OBNoiseRemovalFilterParams', 'OBPermissionType', 'OBPoint', 'OBPoint2f', 'OBPowerLineFreqMode', 'OBPropertyID', 'OBPropertyItem', 'OBPropertyType', 'OBProtocolVersion', 'OBRect', 'OBRegionOfInterest', 'OBRotateDegreeType', 'OBSensorType', 'OBSequenceIdItem', 'OBSpatialAdvancedFilterParams', 'OBStatus', 'OBStreamType', 'OBSyncMode', 'OBTofExposureThresholdControl', 'OBTofFilterRange', 'OBUSBPowerState', 'OBUint16PropertyRange', 'OBUint8PropertyRange', 'OBUpgradeState', 'Pipeline', 'Playback', 'PointCloudFilter', 'PointsFrame', 'Recorder', 'Sensor', 'SensorList', 'SequenceIdFilter', 'SpatialAdvancedFilter', 'StreamProfile', 'StreamProfileList', 'TemporalFilter', 'ThresholdFilter', 'VideoFrame', 'VideoStreamProfile', 'calibration_2d_to_3d', 'calibration_2d_to_3d_undistortion', 'calibration_3d_to_2d', 'calibration_3d_to_3d', 'get_version']
class AccelFrame(Frame):
    def __init__(self, arg0: Frame) -> None:
        ...
    def __repr__(self) -> None:
        ...
    def get_temperature(self) -> float:
        ...
    def get_value(self) -> OBAccelValue:
        ...
    def get_x(self) -> float:
        ...
    def get_y(self) -> float:
        ...
    def get_z(self) -> float:
        ...
class AccelStreamProfile(StreamProfile):
    def __init__(self, arg0: StreamProfile) -> None:
        ...
    def __repr__(self) -> str:
        ...
    def get_full_scale_range(self) -> OBAccelFullScaleRange:
        ...
    def get_intrinsic(self) -> OBAccelIntrinsic:
        ...
    def get_sample_rate(self) -> OBGyroSampleRate:
        ...
class AlignFilter(Filter):
    def __init__(self, align_to_stream: OBStreamType) -> None:
        ...
    def get_align_to_stream_type(self) -> OBStreamType:
        ...
class CameraParamList:
    def __len__(self) -> int:
        ...
    def get_camera_param(self, arg0: int) -> OBCameraParam:
        """
        Get the camera parameters for the specified index
        """
    def get_count(self) -> int:
        """
        Get the number of devices in the list
        """
class ColorFrame(VideoFrame):
    def __init__(self, arg0: Frame) -> None:
        ...
class Config:
    def __init__(self) -> None:
        ...
    def disable_all_stream(self) -> None:
        ...
    def disable_stream(self, arg0: OBStreamType) -> None:
        ...
    def enable_all_stream(self) -> None:
        ...
    def enable_stream(self, arg0: ...) -> None:
        ...
    def set_align_mode(self, arg0: OBAlignMode) -> None:
        ...
    def set_d2c_target_resolution(self, arg0: int, arg1: int) -> None:
        ...
    def set_depth_scale_require(self, arg0: bool) -> None:
        ...
class Context:
    @staticmethod
    def set_logger_level(arg0: OBLogLevel) -> None:
        ...
    @staticmethod
    def set_logger_to_console(arg0: OBLogLevel) -> None:
        """
        Set logger to console
        """
    @staticmethod
    def set_logger_to_file(arg0: OBLogLevel, arg1: str) -> None:
        """
        Set logger to file
        """
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: str) -> None:
        ...
    def create_net_device(self, arg0: str, arg1: int) -> ...:
        """
        Create net device
        """
    def enable_multi_device_sync(self, arg0: int) -> None:
        """
        Activates the multi-device synchronization function to synchronize the clock of the created device (the device needs to support this function).repeat_interval: The synchronization time interval (unit: ms; if repeatInterval=0, it means that it will only be synchronized once and will not be executed regularly).
        """
    def query_devices(self) -> ...:
        """
        Query devices
        """
    def set_device_changed_callback(self, arg0: typing.Callable) -> None:
        """
        Set device changed callback, callback will be called when device changed
        """
class DecimationFilter(Filter):
    def __init__(self) -> None:
        ...
    def get_scale_range(self) -> OBUint8PropertyRange:
        ...
    def get_scale_value(self) -> int:
        ...
    def set_scale_value(self, arg0: int) -> None:
        ...
class DepthFrame(VideoFrame):
    def __init__(self, arg0: Frame) -> None:
        ...
    def get_depth_scale(self) -> float:
        ...
class Device:
    __hash__: typing.ClassVar[None] = None
    def __eq__(self, arg0: Device) -> bool:
        ...
    def active_authorization(self, arg0: str) -> bool:
        ...
    def export_settings_as_preset_json_file(self, arg0: str) -> None:
        ...
    def get_available_preset_list(self) -> DevicePresetList:
        ...
    def get_baseline(self) -> OBBaselineCalibrationParam:
        ...
    def get_bool_property(self, arg0: OBPropertyID) -> bool:
        ...
    def get_bool_property_range(self, arg0: OBPropertyID) -> OBBoolPropertyRange:
        ...
    def get_calibration_camera_param_list(self) -> ...:
        ...
    def get_current_preset_name(self) -> str:
        ...
    def get_depth_precision_support_list(self) -> list:
        ...
    def get_depth_work_mode(self) -> OBDepthWorkMode:
        ...
    def get_depth_work_mode_list(self) -> OBDepthWorkModeList:
        ...
    def get_device_info(self) -> DeviceInfo:
        ...
    def get_device_state(self) -> int:
        ...
    def get_float_property(self, arg0: OBPropertyID) -> float:
        ...
    def get_float_property_range(self, arg0: OBPropertyID) -> OBFloatPropertyRange:
        ...
    def get_int_property(self, arg0: OBPropertyID) -> int:
        ...
    def get_int_property_range(self, arg0: OBPropertyID) -> OBIntPropertyRange:
        ...
    def get_multi_device_sync_config(self) -> OBMultiDeviceSyncConfig:
        ...
    def get_sensor(self, arg0: OBSensorType) -> ...:
        ...
    def get_sensor_list(self) -> ...:
        ...
    def get_support_property_count(self) -> int:
        ...
    def get_supported_property(self, arg0: int) -> OBPropertyItem:
        ...
    def get_temperature(self) -> OBDeviceTemperature:
        ...
    def get_timestamp_reset_config(self) -> OBDeviceTimestampResetConfig:
        ...
    def is_property_supported(self, arg0: OBPropertyID, arg1: OBPermissionType) -> bool:
        ...
    def load_depth_filter_config(self, arg0: str) -> None:
        ...
    def load_preset(self, arg0: str) -> None:
        ...
    def load_preset_from_json_data(self, arg0: str, arg1: str) -> None:
        ...
    def load_preset_from_json_file(self, arg0: str) -> None:
        ...
    def reboot(self) -> None:
        ...
    def reset_default_depth_filter_config(self) -> None:
        ...
    def set_bool_property(self, arg0: OBPropertyID, arg1: bool) -> None:
        ...
    def set_depth_work_mode(self, arg0: OBDepthWorkMode) -> OBStatus:
        ...
    def set_device_state_changed_callback(self, arg0: typing.Callable) -> None:
        ...
    def set_float_property(self, arg0: OBPropertyID, arg1: float) -> None:
        ...
    def set_hdr_config(self, arg0: OBHdrConfig) -> None:
        ...
    def set_int_property(self, arg0: OBPropertyID, arg1: int) -> None:
        ...
    def set_multi_device_sync_config(self, arg0: OBMultiDeviceSyncConfig) -> None:
        ...
    def set_timestamp_reset_config(self, arg0: OBDeviceTimestampResetConfig) -> None:
        ...
    def timer_sync_with_host(self) -> None:
        ...
    def timestamp_reset(self) -> None:
        ...
    def trigger_capture(self) -> None:
        ...
class DeviceInfo:
    def __repr__(self) -> str:
        ...
    def get_connection_type(self) -> str:
        """
        Get the connection type of the device
        """
    def get_device_type(self) -> OBDeviceType:
        """
        Get the device type
        """
    def get_firmware_version(self) -> str:
        """
        Get the version number of the firmware
        """
    def get_hardware_version(self) -> str:
        """
        Get the version number of the hardware
        """
    def get_name(self) -> str:
        """
        Get device name
        """
    def get_pid(self) -> int:
        """
        Get device pid
        """
    def get_serial_number(self) -> str:
        """
        Get the serial number of the device
        """
    def get_supported_min_sdk_version(self) -> str:
        """
        Get the minimum version number of the SDK supported by the device
        """
    def get_uid(self) -> str:
        """
        Get system assigned uid for distinguishing between different devices
        """
    def get_vid(self) -> int:
        """
        Get device vid
        """
class DeviceList:
    def __len__(self) -> int:
        ...
    def get_count(self) -> int:
        ...
    def get_device_by_index(self, arg0: int) -> ...:
        ...
    def get_device_by_serial_number(self, arg0: str) -> ...:
        ...
    def get_device_by_uid(self, arg0: str) -> ...:
        ...
    def get_device_pid_by_index(self, arg0: int) -> int:
        ...
    def get_device_serial_number_by_index(self, arg0: int) -> str:
        ...
    def get_device_uid_by_index(self, arg0: int) -> str:
        ...
    def get_device_vid_by_index(self, arg0: int) -> int:
        ...
class DevicePresetList:
    def get_count(self) -> int:
        ...
    def get_name_by_index(self, arg0: int) -> str:
        ...
    def has_preset(self, arg0: str) -> bool:
        ...
class DisparityTransform(Filter):
    def __init__(self, depth_to_disparity: bool = False) -> None:
        ...
class EdgeNoiseRemovalFilter(Filter):
    def __init__(self) -> None:
        ...
    def get_filter_params(self) -> OBEdgeNoiseRemovalFilterParams:
        ...
    def get_margin_bottom_th_range(self) -> OBUint16PropertyRange:
        ...
    def get_margin_left_th_range(self) -> OBUint16PropertyRange:
        ...
    def get_margin_right_th_range(self) -> OBUint16PropertyRange:
        ...
    def get_margin_top_th_range(self) -> OBUint16PropertyRange:
        ...
    def set_filter_params(self, arg0: OBEdgeNoiseRemovalFilterParams) -> None:
        ...
class Filter:
    def __init__(self) -> None:
        ...
    def enable(self, arg0: bool) -> None:
        ...
    def get_name(self) -> str:
        ...
    def is_align_filter(self) -> bool:
        ...
    def is_compression_filter(self) -> bool:
        ...
    def is_decimation_filter(self) -> bool:
        ...
    def is_decompression_filter(self) -> bool:
        ...
    def is_disparity_transform_filter(self) -> bool:
        ...
    def is_edge_noise_removal_filter(self) -> bool:
        ...
    def is_enabled(self) -> bool:
        ...
    def is_format_converter(self) -> bool:
        ...
    def is_hdr_merge_filter(self) -> bool:
        ...
    def is_hole_filling_filter(self) -> bool:
        ...
    def is_noise_removal_filter(self) -> bool:
        ...
    def is_point_cloud_filter(self) -> bool:
        ...
    def is_sequence_id_filter(self) -> bool:
        ...
    def is_spatial_advanced_filter(self) -> bool:
        ...
    def is_temporal_filter(self) -> bool:
        ...
    def is_threshold_filter(self) -> bool:
        ...
    def process(self, arg0: ...) -> ...:
        ...
    def push_frame(self, arg0: ...) -> None:
        ...
    def reset(self) -> None:
        ...
    def set_callback(self, arg0: typing.Callable) -> None:
        ...
class FormatConvertFilter(Filter):
    def __init__(self) -> None:
        ...
    def set_format_convert_format(self, arg0: OBConvertFormat) -> None:
        """
        Set the format to convert to
        """
class Frame:
    def __repr__(self) -> None:
        ...
    def as_accel_frame(self) -> ...:
        ...
    def as_color_frame(self) -> ...:
        ...
    def as_depth_frame(self) -> ...:
        ...
    def as_frame_set(self) -> ...:
        ...
    def as_gyro_frame(self) -> ...:
        ...
    def as_ir_frame(self) -> ...:
        ...
    def as_points_frame(self) -> ...:
        ...
    def as_video_frame(self) -> ...:
        ...
    def get_data(self) -> numpy.ndarray[numpy.uint8]:
        ...
    def get_data_pointer(self) -> capsule:
        ...
    def get_data_size(self) -> int:
        ...
    def get_format(self) -> OBFormat:
        ...
    def get_global_timestamp_us(self) -> int:
        ...
    def get_index(self) -> int:
        ...
    def get_metadata_value(self, arg0: OBFrameMetadataType) -> int:
        ...
    def get_system_timestamp(self) -> int:
        ...
    def get_system_timestamp_us(self) -> int:
        ...
    def get_timestamp(self) -> int:
        """
        Get the hardware timestamp of the frame in milliseconds
        """
    def get_timestamp_us(self) -> int:
        ...
    def get_type(self) -> OBFrameType:
        ...
    def has_metadata(self, arg0: OBFrameMetadataType) -> bool:
        ...
class FrameSet(Frame):
    def __repr__(self) -> None:
        ...
    def convert_to_color_points(self, arg0: OBCameraParam) -> list:
        ...
    def convert_to_points(self, arg0: OBCameraParam) -> list:
        ...
    def get_color_frame(self) -> ColorFrame:
        ...
    def get_color_point_cloud(self, arg0: OBCameraParam) -> numpy.ndarray[numpy.float32]:
        ...
    def get_depth_frame(self) -> DepthFrame:
        ...
    def get_frame(self, arg0: OBFrameType) -> Frame:
        ...
    def get_frame_by_index(self, arg0: int) -> Frame:
        ...
    def get_frame_by_type(self, arg0: OBFrameType) -> Frame:
        ...
    def get_frame_count(self) -> int:
        ...
    def get_ir_frame(self) -> IRFrame:
        ...
    def get_point_cloud(self, arg0: OBCameraParam) -> numpy.ndarray[numpy.float32]:
        ...
    def get_points_frame(self) -> PointsFrame:
        ...
class GyroFrame(Frame):
    def __init__(self, arg0: Frame) -> None:
        ...
    def __repr__(self) -> None:
        ...
    def get_temperature(self) -> float:
        ...
    def get_value(self) -> OBAccelValue:
        ...
    def get_x(self) -> float:
        ...
    def get_y(self) -> float:
        ...
    def get_z(self) -> float:
        ...
class GyroStreamProfile(StreamProfile):
    def __init__(self, arg0: StreamProfile) -> None:
        ...
    def __repr__(self) -> str:
        ...
    def get_full_scale_range(self) -> OBGyroFullScaleRange:
        ...
    def get_intrinsic(self) -> OBGyroIntrinsic:
        ...
    def get_sample_rate(self) -> OBGyroSampleRate:
        ...
class HDRMergeFilter(Filter):
    def __init__(self) -> None:
        ...
class HoleFillingFilter(Filter):
    def __init__(self) -> None:
        ...
    def get_filling_mode(self) -> OBHoleFillingMode:
        ...
    def set_filling_mode(self, arg0: OBHoleFillingMode) -> None:
        """
        Set the filling mode
        """
class IRFrame(VideoFrame):
    def __init__(self, arg0: Frame) -> None:
        ...
    def get_data_source(self) -> OBSensorType:
        ...
class NoiseRemovalFilter(Filter):
    def __init__(self) -> None:
        ...
    def get_disp_diff_range(self) -> OBUint16PropertyRange:
        ...
    def get_filter_params(self) -> OBNoiseRemovalFilterParams:
        ...
    def get_max_size_range(self) -> OBUint16PropertyRange:
        ...
    def set_filter_params(self, arg0: OBNoiseRemovalFilterParams) -> None:
        ...
class OBAccelFullScaleRange:
    """
    Members:
    
      ACCEL_FS_2g
    
      ACCEL_FS_4g
    
      ACCEL_FS_8g
    
      ACCEL_FS_16g
    """
    ACCEL_FS_16g: typing.ClassVar[OBAccelFullScaleRange]  # value = <OBAccelFullScaleRange.ACCEL_FS_16g: 4>
    ACCEL_FS_2g: typing.ClassVar[OBAccelFullScaleRange]  # value = <OBAccelFullScaleRange.ACCEL_FS_2g: 1>
    ACCEL_FS_4g: typing.ClassVar[OBAccelFullScaleRange]  # value = <OBAccelFullScaleRange.ACCEL_FS_4g: 2>
    ACCEL_FS_8g: typing.ClassVar[OBAccelFullScaleRange]  # value = <OBAccelFullScaleRange.ACCEL_FS_8g: 3>
    __members__: typing.ClassVar[dict[str, OBAccelFullScaleRange]]  # value = {'ACCEL_FS_2g': <OBAccelFullScaleRange.ACCEL_FS_2g: 1>, 'ACCEL_FS_4g': <OBAccelFullScaleRange.ACCEL_FS_4g: 2>, 'ACCEL_FS_8g': <OBAccelFullScaleRange.ACCEL_FS_8g: 3>, 'ACCEL_FS_16g': <OBAccelFullScaleRange.ACCEL_FS_16g: 4>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class OBAccelIntrinsic:
    bias: numpy.ndarray[numpy.float64]
    gravity: numpy.ndarray[numpy.float64]
    noise_density: float
    random_walk: float
    reference_temp: float
    scale_misalignment: numpy.ndarray[numpy.float64]
    temp_slope: numpy.ndarray[numpy.float64]
    def __init__(self) -> None:
        ...
class OBAccelValue:
    x: float
    y: float
    z: float
    def __init__(self) -> None:
        ...
    def __repr__(self) -> str:
        ...
class OBAlignMode:
    """
    Members:
    
      DISABLE
    
      HW_MODE
    
      SW_MODE
    """
    DISABLE: typing.ClassVar[OBAlignMode]  # value = <OBAlignMode.DISABLE: 0>
    HW_MODE: typing.ClassVar[OBAlignMode]  # value = <OBAlignMode.HW_MODE: 1>
    SW_MODE: typing.ClassVar[OBAlignMode]  # value = <OBAlignMode.SW_MODE: 2>
    __members__: typing.ClassVar[dict[str, OBAlignMode]]  # value = {'DISABLE': <OBAlignMode.DISABLE: 0>, 'HW_MODE': <OBAlignMode.HW_MODE: 1>, 'SW_MODE': <OBAlignMode.SW_MODE: 2>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class OBBaselineCalibrationParam:
    baseline: float
    zpd: float
    def __init__(self) -> None:
        ...
class OBCalibrationParam:
    def __init__(self) -> None:
        ...
    def get_distortion(self, arg0: int) -> OBCameraDistortion:
        ...
    def get_extrinsic(self, arg0: int, arg1: int) -> OBD2CTransform:
        ...
    def get_intrinsic(self, arg0: int) -> OBCameraIntrinsic:
        ...
    def set_distortion(self, arg0: int, arg1: OBCameraDistortion) -> None:
        ...
    def set_extrinsic(self, arg0: int, arg1: int, arg2: OBD2CTransform) -> None:
        ...
    def set_intrinsic(self, arg0: int, arg1: OBCameraIntrinsic) -> None:
        ...
class OBCameraAlignIntrinsic:
    coeffs: numpy.ndarray[numpy.float32]
    fx: float
    fy: float
    height: int
    model: OBCameraDistortionModel
    ppx: float
    ppy: float
    width: int
    def __init__(self) -> None:
        ...
class OBCameraDistortion:
    k1: float
    k2: float
    k3: float
    k4: float
    k5: float
    k6: float
    p1: float
    p2: float
    def __init__(self) -> None:
        ...
    def __repr__(self) -> str:
        ...
class OBCameraDistortionModel:
    """
    Members:
    
      NONE
    
      MODIFIED_BROWN_CONRADY
    
      INVERSE_BROWN_CONRADY
    
      BROWN_CONRADY
    """
    BROWN_CONRADY: typing.ClassVar[OBCameraDistortionModel]  # value = <OBCameraDistortionModel.BROWN_CONRADY: 3>
    INVERSE_BROWN_CONRADY: typing.ClassVar[OBCameraDistortionModel]  # value = <OBCameraDistortionModel.INVERSE_BROWN_CONRADY: 2>
    MODIFIED_BROWN_CONRADY: typing.ClassVar[OBCameraDistortionModel]  # value = <OBCameraDistortionModel.MODIFIED_BROWN_CONRADY: 1>
    NONE: typing.ClassVar[OBCameraDistortionModel]  # value = <OBCameraDistortionModel.NONE: 0>
    __members__: typing.ClassVar[dict[str, OBCameraDistortionModel]]  # value = {'NONE': <OBCameraDistortionModel.NONE: 0>, 'MODIFIED_BROWN_CONRADY': <OBCameraDistortionModel.MODIFIED_BROWN_CONRADY: 1>, 'INVERSE_BROWN_CONRADY': <OBCameraDistortionModel.INVERSE_BROWN_CONRADY: 2>, 'BROWN_CONRADY': <OBCameraDistortionModel.BROWN_CONRADY: 3>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class OBCameraIntrinsic:
    cx: float
    cy: float
    fx: float
    fy: float
    height: int
    width: int
    def __init__(self) -> None:
        ...
    def __repr__(self) -> str:
        ...
class OBCameraParam:
    depth_distortion: OBCameraDistortion
    depth_intrinsic: OBCameraIntrinsic
    rgb_distortion: OBCameraDistortion
    rgb_intrinsic: OBCameraIntrinsic
    transform: OBD2CTransform
    def __init__(self) -> None:
        ...
    def __repr__(self) -> str:
        ...
class OBCmdVersion:
    """
    Members:
    
      V0
    
      V1
    
      V2
    
      V3
    
      NONE
    
      INVALID
    """
    INVALID: typing.ClassVar[OBCmdVersion]  # value = <OBCmdVersion.INVALID: 65535>
    NONE: typing.ClassVar[OBCmdVersion]  # value = <OBCmdVersion.NONE: 65534>
    V0: typing.ClassVar[OBCmdVersion]  # value = <OBCmdVersion.V0: 0>
    V1: typing.ClassVar[OBCmdVersion]  # value = <OBCmdVersion.V1: 1>
    V2: typing.ClassVar[OBCmdVersion]  # value = <OBCmdVersion.V2: 2>
    V3: typing.ClassVar[OBCmdVersion]  # value = <OBCmdVersion.V3: 3>
    __members__: typing.ClassVar[dict[str, OBCmdVersion]]  # value = {'V0': <OBCmdVersion.V0: 0>, 'V1': <OBCmdVersion.V1: 1>, 'V2': <OBCmdVersion.V2: 2>, 'V3': <OBCmdVersion.V3: 3>, 'NONE': <OBCmdVersion.NONE: 65534>, 'INVALID': <OBCmdVersion.INVALID: 65535>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class OBColorPoint:
    b: int
    g: int
    r: int
    x: float
    y: float
    z: float
    @staticmethod
    def get_sizeof() -> int:
        ...
    def __init__(self) -> None:
        ...
    def __repr__(self) -> str:
        ...
class OBCommunicationType:
    """
    Members:
    
      USB
    
      ETHERNET
    """
    ETHERNET: typing.ClassVar[OBCommunicationType]  # value = <OBCommunicationType.ETHERNET: 1>
    USB: typing.ClassVar[OBCommunicationType]  # value = <OBCommunicationType.USB: 0>
    __members__: typing.ClassVar[dict[str, OBCommunicationType]]  # value = {'USB': <OBCommunicationType.USB: 0>, 'ETHERNET': <OBCommunicationType.ETHERNET: 1>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class OBCompressionMode:
    """
    Members:
    
      LOSSLESS
    
      LOSSY
    """
    LOSSLESS: typing.ClassVar[OBCompressionMode]  # value = <OBCompressionMode.LOSSLESS: 0>
    LOSSY: typing.ClassVar[OBCompressionMode]  # value = <OBCompressionMode.LOSSY: 1>
    __members__: typing.ClassVar[dict[str, OBCompressionMode]]  # value = {'LOSSLESS': <OBCompressionMode.LOSSLESS: 0>, 'LOSSY': <OBCompressionMode.LOSSY: 1>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class OBCompressionParams:
    threshold: int
    def __init__(self) -> None:
        ...
class OBConvertFormat:
    """
    Members:
    
      YUYV_TO_RGB888
    
      I420_TO_RGB888
    
      NV21_TO_RGB888
    
      NV12_TO_RGB888
    
      MJPG_TO_I420
    
      RGB888_TO_BGR
    
      MJPG_TO_NV21
    
      MJPG_TO_RGB888
    
      MJPG_TO_BGR888
    
      MJPG_TO_BGRA
    
      UYVY_TO_RGB888
    
      BGR_TO_RGB
    """
    BGR_TO_RGB: typing.ClassVar[OBConvertFormat]  # value = <OBConvertFormat.BGR_TO_RGB: 11>
    I420_TO_RGB888: typing.ClassVar[OBConvertFormat]  # value = <OBConvertFormat.I420_TO_RGB888: 1>
    MJPG_TO_BGR888: typing.ClassVar[OBConvertFormat]  # value = <OBConvertFormat.MJPG_TO_BGR888: 8>
    MJPG_TO_BGRA: typing.ClassVar[OBConvertFormat]  # value = <OBConvertFormat.MJPG_TO_BGRA: 9>
    MJPG_TO_I420: typing.ClassVar[OBConvertFormat]  # value = <OBConvertFormat.MJPG_TO_I420: 4>
    MJPG_TO_NV21: typing.ClassVar[OBConvertFormat]  # value = <OBConvertFormat.MJPG_TO_NV21: 6>
    MJPG_TO_RGB888: typing.ClassVar[OBConvertFormat]  # value = <OBConvertFormat.MJPG_TO_RGB888: 7>
    NV12_TO_RGB888: typing.ClassVar[OBConvertFormat]  # value = <OBConvertFormat.NV12_TO_RGB888: 3>
    NV21_TO_RGB888: typing.ClassVar[OBConvertFormat]  # value = <OBConvertFormat.NV21_TO_RGB888: 2>
    RGB888_TO_BGR: typing.ClassVar[OBConvertFormat]  # value = <OBConvertFormat.RGB888_TO_BGR: 5>
    UYVY_TO_RGB888: typing.ClassVar[OBConvertFormat]  # value = <OBConvertFormat.UYVY_TO_RGB888: 10>
    YUYV_TO_RGB888: typing.ClassVar[OBConvertFormat]  # value = <OBConvertFormat.YUYV_TO_RGB888: 0>
    __members__: typing.ClassVar[dict[str, OBConvertFormat]]  # value = {'YUYV_TO_RGB888': <OBConvertFormat.YUYV_TO_RGB888: 0>, 'I420_TO_RGB888': <OBConvertFormat.I420_TO_RGB888: 1>, 'NV21_TO_RGB888': <OBConvertFormat.NV21_TO_RGB888: 2>, 'NV12_TO_RGB888': <OBConvertFormat.NV12_TO_RGB888: 3>, 'MJPG_TO_I420': <OBConvertFormat.MJPG_TO_I420: 4>, 'RGB888_TO_BGR': <OBConvertFormat.RGB888_TO_BGR: 5>, 'MJPG_TO_NV21': <OBConvertFormat.MJPG_TO_NV21: 6>, 'MJPG_TO_RGB888': <OBConvertFormat.MJPG_TO_RGB888: 7>, 'MJPG_TO_BGR888': <OBConvertFormat.MJPG_TO_BGR888: 8>, 'MJPG_TO_BGRA': <OBConvertFormat.MJPG_TO_BGRA: 9>, 'UYVY_TO_RGB888': <OBConvertFormat.UYVY_TO_RGB888: 10>, 'BGR_TO_RGB': <OBConvertFormat.BGR_TO_RGB: 11>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class OBCoordinateSystemType:
    """
    Members:
    
      LEFT_HAND
    
      RIGHT_HAND
    """
    LEFT_HAND: typing.ClassVar[OBCoordinateSystemType]  # value = <OBCoordinateSystemType.LEFT_HAND: 0>
    RIGHT_HAND: typing.ClassVar[OBCoordinateSystemType]  # value = <OBCoordinateSystemType.RIGHT_HAND: 1>
    __members__: typing.ClassVar[dict[str, OBCoordinateSystemType]]  # value = {'LEFT_HAND': <OBCoordinateSystemType.LEFT_HAND: 0>, 'RIGHT_HAND': <OBCoordinateSystemType.RIGHT_HAND: 1>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class OBD2CTransform:
    rot: numpy.ndarray[numpy.float32]
    transform: numpy.ndarray[numpy.float32]
    def __init__(self) -> None:
        ...
    def __repr__(self) -> str:
        ...
class OBDCPowerState:
    """
    Members:
    
      OFF
    
      ON
    """
    OFF: typing.ClassVar[OBDCPowerState]  # value = <OBDCPowerState.OFF: 0>
    ON: typing.ClassVar[OBDCPowerState]  # value = <OBDCPowerState.ON: 1>
    __members__: typing.ClassVar[dict[str, OBDCPowerState]]  # value = {'OFF': <OBDCPowerState.OFF: 0>, 'ON': <OBDCPowerState.ON: 1>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class OBDDONoiseRemovalType:
    """
    Members:
    
      LUT
    
      OVERALL
    """
    LUT: typing.ClassVar[OBDDONoiseRemovalType]  # value = <OBDDONoiseRemovalType.LUT: 0>
    OVERALL: typing.ClassVar[OBDDONoiseRemovalType]  # value = <OBDDONoiseRemovalType.OVERALL: 1>
    __members__: typing.ClassVar[dict[str, OBDDONoiseRemovalType]]  # value = {'LUT': <OBDDONoiseRemovalType.LUT: 0>, 'OVERALL': <OBDDONoiseRemovalType.OVERALL: 1>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class OBDataBundle:
    cmd_version: OBCmdVersion
    data_size: int
    item_count: int
    item_type_size: int
    def __init__(self) -> None:
        ...
    def get_data(self) -> numpy.ndarray:
        ...
    def set_data(self, data: numpy.ndarray[numpy.uint8]) -> None:
        ...
class OBDataTranState:
    """
    Members:
    
      STOPPED
    
      DONE
    
      VERIFYING
    
      TRANSFERRING
    
      BUSY
    
      UNSUPPORTED_ERROR
    
      TRANSFER_FAILED
    
      VERIFY_FAILED
    
      OTHER_ERROR
    """
    BUSY: typing.ClassVar[OBDataTranState]  # value = <OBDataTranState.BUSY: -1>
    DONE: typing.ClassVar[OBDataTranState]  # value = <OBDataTranState.DONE: 2>
    OTHER_ERROR: typing.ClassVar[OBDataTranState]  # value = <OBDataTranState.OTHER_ERROR: -5>
    STOPPED: typing.ClassVar[OBDataTranState]  # value = <OBDataTranState.STOPPED: 3>
    TRANSFERRING: typing.ClassVar[OBDataTranState]  # value = <OBDataTranState.TRANSFERRING: 0>
    TRANSFER_FAILED: typing.ClassVar[OBDataTranState]  # value = <OBDataTranState.TRANSFER_FAILED: -3>
    UNSUPPORTED_ERROR: typing.ClassVar[OBDataTranState]  # value = <OBDataTranState.UNSUPPORTED_ERROR: -2>
    VERIFYING: typing.ClassVar[OBDataTranState]  # value = <OBDataTranState.VERIFYING: 1>
    VERIFY_FAILED: typing.ClassVar[OBDataTranState]  # value = <OBDataTranState.VERIFY_FAILED: -4>
    __members__: typing.ClassVar[dict[str, OBDataTranState]]  # value = {'STOPPED': <OBDataTranState.STOPPED: 3>, 'DONE': <OBDataTranState.DONE: 2>, 'VERIFYING': <OBDataTranState.VERIFYING: 1>, 'TRANSFERRING': <OBDataTranState.TRANSFERRING: 0>, 'BUSY': <OBDataTranState.BUSY: -1>, 'UNSUPPORTED_ERROR': <OBDataTranState.UNSUPPORTED_ERROR: -2>, 'TRANSFER_FAILED': <OBDataTranState.TRANSFER_FAILED: -3>, 'VERIFY_FAILED': <OBDataTranState.VERIFY_FAILED: -4>, 'OTHER_ERROR': <OBDataTranState.OTHER_ERROR: -5>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class OBDepthCroppingMode:
    """
    Members:
    
      AUTO
    
      CLOSE
    
      OPEN
    """
    AUTO: typing.ClassVar[OBDepthCroppingMode]  # value = <OBDepthCroppingMode.AUTO: 0>
    CLOSE: typing.ClassVar[OBDepthCroppingMode]  # value = <OBDepthCroppingMode.CLOSE: 1>
    OPEN: typing.ClassVar[OBDepthCroppingMode]  # value = <OBDepthCroppingMode.OPEN: 2>
    __members__: typing.ClassVar[dict[str, OBDepthCroppingMode]]  # value = {'AUTO': <OBDepthCroppingMode.AUTO: 0>, 'CLOSE': <OBDepthCroppingMode.CLOSE: 1>, 'OPEN': <OBDepthCroppingMode.OPEN: 2>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class OBDepthPrecisionLevel:
    """
    Members:
    
      ONE_MM
    
      ZERO_POINT_EIGHT_MM
    
      ZERO_POINT_FOUR_MM
    
      ZERO_POINT_TWO_MM
    
      ZERO_POINT_ONE_MM
    """
    ONE_MM: typing.ClassVar[OBDepthPrecisionLevel]  # value = <OBDepthPrecisionLevel.ONE_MM: 0>
    ZERO_POINT_EIGHT_MM: typing.ClassVar[OBDepthPrecisionLevel]  # value = <OBDepthPrecisionLevel.ZERO_POINT_EIGHT_MM: 1>
    ZERO_POINT_FOUR_MM: typing.ClassVar[OBDepthPrecisionLevel]  # value = <OBDepthPrecisionLevel.ZERO_POINT_FOUR_MM: 2>
    ZERO_POINT_ONE_MM: typing.ClassVar[OBDepthPrecisionLevel]  # value = <OBDepthPrecisionLevel.ZERO_POINT_ONE_MM: 3>
    ZERO_POINT_TWO_MM: typing.ClassVar[OBDepthPrecisionLevel]  # value = <OBDepthPrecisionLevel.ZERO_POINT_TWO_MM: 4>
    __members__: typing.ClassVar[dict[str, OBDepthPrecisionLevel]]  # value = {'ONE_MM': <OBDepthPrecisionLevel.ONE_MM: 0>, 'ZERO_POINT_EIGHT_MM': <OBDepthPrecisionLevel.ZERO_POINT_EIGHT_MM: 1>, 'ZERO_POINT_FOUR_MM': <OBDepthPrecisionLevel.ZERO_POINT_FOUR_MM: 2>, 'ZERO_POINT_TWO_MM': <OBDepthPrecisionLevel.ZERO_POINT_TWO_MM: 4>, 'ZERO_POINT_ONE_MM': <OBDepthPrecisionLevel.ZERO_POINT_ONE_MM: 3>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class OBDepthWorkMode:
    __hash__: typing.ClassVar[None] = None
    checksum: numpy.ndarray[numpy.uint8]
    name: str
    def __eq__(self, arg0: OBDepthWorkMode) -> bool:
        ...
    def __init__(self) -> None:
        ...
    def __repr__(self) -> str:
        ...
class OBDepthWorkModeList:
    def __len__(self) -> int:
        ...
    def get_count(self) -> int:
        """
        Get the number of OBDepthWorkMode objects in the list
        """
    def get_depth_work_mode_by_index(self, arg0: int) -> OBDepthWorkMode:
        """
        Get the OBDepthWorkMode object at the specified index
        """
    def get_name_by_index(self, arg0: int) -> str:
        """
        Get the name of the depth work mode at the specified index
        """
class OBDeviceDevelopmentMode:
    """
    Members:
    
      NORMAL
    
      DEVELOPMENT
    """
    DEVELOPMENT: typing.ClassVar[OBDeviceDevelopmentMode]  # value = <OBDeviceDevelopmentMode.DEVELOPMENT: 1>
    NORMAL: typing.ClassVar[OBDeviceDevelopmentMode]  # value = <OBDeviceDevelopmentMode.NORMAL: 0>
    __members__: typing.ClassVar[dict[str, OBDeviceDevelopmentMode]]  # value = {'NORMAL': <OBDeviceDevelopmentMode.NORMAL: 0>, 'DEVELOPMENT': <OBDeviceDevelopmentMode.DEVELOPMENT: 1>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class OBDeviceIpAddrConfig:
    address: str
    dhcp: int
    gateway: str
    netmask: str
    def __init__(self) -> None:
        ...
class OBDeviceSyncConfig:
    device_index: int
    device_trigger_signal_out_delay: int
    device_trigger_signal_out_polarity: int
    ir_trigger_signal_delay: int
    mcu_trigger_frequency: int
    mode: OBSyncMode
    rgb_trigger_signal_delay: int
    def __init__(self) -> None:
        ...
class OBDeviceTemperature:
    chip_bottom_temperature: float
    chip_top_temperature: float
    cpu_temperature: float
    imu_temperature: float
    ir_left_temperature: float
    ir_right_temperature: float
    ir_temperature: float
    laser_temperature: float
    main_board_temperature: float
    rgb_temperature: float
    tec_temperature: float
    def __init__(self) -> None:
        ...
    def __repr__(self) -> str:
        ...
class OBDeviceTimestampResetConfig:
    enable: bool
    timestamp_reset_delay_us: int
    def __init__(self) -> None:
        ...
class OBDeviceType:
    """
    Members:
    
      LIGHT_MONOCULAR
    
      LIGHT_BINOCULAR
    
      TIME_OF_FLIGHT
    """
    LIGHT_BINOCULAR: typing.ClassVar[OBDeviceType]  # value = <OBDeviceType.LIGHT_BINOCULAR: 1>
    LIGHT_MONOCULAR: typing.ClassVar[OBDeviceType]  # value = <OBDeviceType.LIGHT_MONOCULAR: 0>
    TIME_OF_FLIGHT: typing.ClassVar[OBDeviceType]  # value = <OBDeviceType.TIME_OF_FLIGHT: 2>
    __members__: typing.ClassVar[dict[str, OBDeviceType]]  # value = {'LIGHT_MONOCULAR': <OBDeviceType.LIGHT_MONOCULAR: 0>, 'LIGHT_BINOCULAR': <OBDeviceType.LIGHT_BINOCULAR: 1>, 'TIME_OF_FLIGHT': <OBDeviceType.TIME_OF_FLIGHT: 2>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class OBEdgeNoiseRemovalFilterParams:
    margin_bottom_th: int
    margin_left_th: int
    margin_right_th: int
    margin_top_th: int
    type: OBEdgeNoiseRemovalType
    def __init__(self) -> None:
        ...
class OBEdgeNoiseRemovalType:
    """
    Members:
    
      MG_FILTER
    
      MGH_FILTER
    
      MGA_FILTER
    
      MGC_FILTER
    """
    MGA_FILTER: typing.ClassVar[OBEdgeNoiseRemovalType]  # value = <OBEdgeNoiseRemovalType.MGA_FILTER: 2>
    MGC_FILTER: typing.ClassVar[OBEdgeNoiseRemovalType]  # value = <OBEdgeNoiseRemovalType.MGC_FILTER: 3>
    MGH_FILTER: typing.ClassVar[OBEdgeNoiseRemovalType]  # value = <OBEdgeNoiseRemovalType.MGH_FILTER: 1>
    MG_FILTER: typing.ClassVar[OBEdgeNoiseRemovalType]  # value = <OBEdgeNoiseRemovalType.MG_FILTER: 0>
    __members__: typing.ClassVar[dict[str, OBEdgeNoiseRemovalType]]  # value = {'MG_FILTER': <OBEdgeNoiseRemovalType.MG_FILTER: 0>, 'MGH_FILTER': <OBEdgeNoiseRemovalType.MGH_FILTER: 1>, 'MGA_FILTER': <OBEdgeNoiseRemovalType.MGA_FILTER: 2>, 'MGC_FILTER': <OBEdgeNoiseRemovalType.MGC_FILTER: 3>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class OBError(Exception):
    pass
class OBException:
    """
    Members:
    
      UNKNOWN
    
      CAMERA_DISCONNECTED
    
      PLATFORM
    
      INVALID_VALUE
    
      WRONG_API_CALL_SEQUENCE
    
      NOT_IMPLEMENTED
    
      IO_ERROR
    """
    CAMERA_DISCONNECTED: typing.ClassVar[OBException]  # value = <OBException.CAMERA_DISCONNECTED: 1>
    INVALID_VALUE: typing.ClassVar[OBException]  # value = <OBException.INVALID_VALUE: 3>
    IO_ERROR: typing.ClassVar[OBException]  # value = <OBException.IO_ERROR: 6>
    NOT_IMPLEMENTED: typing.ClassVar[OBException]  # value = <OBException.NOT_IMPLEMENTED: 5>
    PLATFORM: typing.ClassVar[OBException]  # value = <OBException.PLATFORM: 2>
    UNKNOWN: typing.ClassVar[OBException]  # value = <OBException.UNKNOWN: 0>
    WRONG_API_CALL_SEQUENCE: typing.ClassVar[OBException]  # value = <OBException.WRONG_API_CALL_SEQUENCE: 4>
    __members__: typing.ClassVar[dict[str, OBException]]  # value = {'UNKNOWN': <OBException.UNKNOWN: 0>, 'CAMERA_DISCONNECTED': <OBException.CAMERA_DISCONNECTED: 1>, 'PLATFORM': <OBException.PLATFORM: 2>, 'INVALID_VALUE': <OBException.INVALID_VALUE: 3>, 'WRONG_API_CALL_SEQUENCE': <OBException.WRONG_API_CALL_SEQUENCE: 4>, 'NOT_IMPLEMENTED': <OBException.NOT_IMPLEMENTED: 5>, 'IO_ERROR': <OBException.IO_ERROR: 6>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class OBFileTranState:
    """
    Members:
    
      TRANSFER
    
      DONE
    
      PREPARING
    
      DDR_ERROR
    
      NOT_ENOUGH_SPACE_ERROR
    
      PATH_NOT_WRITABLE_ERROR
    
      MD5_ERROR
    
      WRITE_FLASH_ERROR
    
      TIMEOUT_ERROR
    """
    DDR_ERROR: typing.ClassVar[OBFileTranState]  # value = <OBFileTranState.DDR_ERROR: -1>
    DONE: typing.ClassVar[OBFileTranState]  # value = <OBFileTranState.DONE: 1>
    MD5_ERROR: typing.ClassVar[OBFileTranState]  # value = <OBFileTranState.MD5_ERROR: -4>
    NOT_ENOUGH_SPACE_ERROR: typing.ClassVar[OBFileTranState]  # value = <OBFileTranState.NOT_ENOUGH_SPACE_ERROR: -2>
    PATH_NOT_WRITABLE_ERROR: typing.ClassVar[OBFileTranState]  # value = <OBFileTranState.PATH_NOT_WRITABLE_ERROR: -3>
    PREPARING: typing.ClassVar[OBFileTranState]  # value = <OBFileTranState.PREPARING: 0>
    TIMEOUT_ERROR: typing.ClassVar[OBFileTranState]  # value = <OBFileTranState.TIMEOUT_ERROR: -6>
    TRANSFER: typing.ClassVar[OBFileTranState]  # value = <OBFileTranState.TRANSFER: 2>
    WRITE_FLASH_ERROR: typing.ClassVar[OBFileTranState]  # value = <OBFileTranState.WRITE_FLASH_ERROR: -5>
    __members__: typing.ClassVar[dict[str, OBFileTranState]]  # value = {'TRANSFER': <OBFileTranState.TRANSFER: 2>, 'DONE': <OBFileTranState.DONE: 1>, 'PREPARING': <OBFileTranState.PREPARING: 0>, 'DDR_ERROR': <OBFileTranState.DDR_ERROR: -1>, 'NOT_ENOUGH_SPACE_ERROR': <OBFileTranState.NOT_ENOUGH_SPACE_ERROR: -2>, 'PATH_NOT_WRITABLE_ERROR': <OBFileTranState.PATH_NOT_WRITABLE_ERROR: -3>, 'MD5_ERROR': <OBFileTranState.MD5_ERROR: -4>, 'WRITE_FLASH_ERROR': <OBFileTranState.WRITE_FLASH_ERROR: -5>, 'TIMEOUT_ERROR': <OBFileTranState.TIMEOUT_ERROR: -6>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class OBFilterList:
    def __len__(self) -> int:
        ...
    def get_count(self) -> int:
        ...
    def get_filter(self, arg0: int) -> Filter:
        ...
class OBFloatPropertyRange:
    current: float
    default_value: float
    max: float
    min: float
    step: float
    def __init__(self) -> None:
        ...
class OBFormat:
    """
    Members:
    
      UNKNOWN_FORMAT
    
      YUYV
    
      YUY2
    
      UYVY
    
      NV12
    
      NV21
    
      MJPG
    
      H264
    
      H265
    
      Y16
    
      Y8
    
      Y10
    
      Y11
    
      Y12
    
      GRAY
    
      HEVC
    
      I420
    
      ACCEL
    
      GYRO
    
      POINT
    
      RGB_POINT
    
      RLE
    
      RGB
    
      BGR
    
      Y14
    
      BGRA
    
      COMPRESSED
    
      RVL
    """
    ACCEL: typing.ClassVar[OBFormat]  # value = <OBFormat.ACCEL: 16>
    BGR: typing.ClassVar[OBFormat]  # value = <OBFormat.BGR: 23>
    BGRA: typing.ClassVar[OBFormat]  # value = <OBFormat.BGRA: 25>
    COMPRESSED: typing.ClassVar[OBFormat]  # value = <OBFormat.COMPRESSED: 26>
    GRAY: typing.ClassVar[OBFormat]  # value = <OBFormat.GRAY: 13>
    GYRO: typing.ClassVar[OBFormat]  # value = <OBFormat.GYRO: 17>
    H264: typing.ClassVar[OBFormat]  # value = <OBFormat.H264: 6>
    H265: typing.ClassVar[OBFormat]  # value = <OBFormat.H265: 7>
    HEVC: typing.ClassVar[OBFormat]  # value = <OBFormat.HEVC: 14>
    I420: typing.ClassVar[OBFormat]  # value = <OBFormat.I420: 15>
    MJPG: typing.ClassVar[OBFormat]  # value = <OBFormat.MJPG: 5>
    NV12: typing.ClassVar[OBFormat]  # value = <OBFormat.NV12: 3>
    NV21: typing.ClassVar[OBFormat]  # value = <OBFormat.NV21: 4>
    POINT: typing.ClassVar[OBFormat]  # value = <OBFormat.POINT: 19>
    RGB: typing.ClassVar[OBFormat]  # value = <OBFormat.RGB: 22>
    RGB_POINT: typing.ClassVar[OBFormat]  # value = <OBFormat.RGB_POINT: 20>
    RLE: typing.ClassVar[OBFormat]  # value = <OBFormat.RLE: 21>
    RVL: typing.ClassVar[OBFormat]  # value = <OBFormat.RVL: 27>
    UNKNOWN_FORMAT: typing.ClassVar[OBFormat]  # value = <OBFormat.UNKNOWN_FORMAT: 255>
    UYVY: typing.ClassVar[OBFormat]  # value = <OBFormat.UYVY: 2>
    Y10: typing.ClassVar[OBFormat]  # value = <OBFormat.Y10: 10>
    Y11: typing.ClassVar[OBFormat]  # value = <OBFormat.Y11: 11>
    Y12: typing.ClassVar[OBFormat]  # value = <OBFormat.Y12: 12>
    Y14: typing.ClassVar[OBFormat]  # value = <OBFormat.Y14: 24>
    Y16: typing.ClassVar[OBFormat]  # value = <OBFormat.Y16: 8>
    Y8: typing.ClassVar[OBFormat]  # value = <OBFormat.Y8: 9>
    YUY2: typing.ClassVar[OBFormat]  # value = <OBFormat.YUY2: 1>
    YUYV: typing.ClassVar[OBFormat]  # value = <OBFormat.YUYV: 0>
    __members__: typing.ClassVar[dict[str, OBFormat]]  # value = {'UNKNOWN_FORMAT': <OBFormat.UNKNOWN_FORMAT: 255>, 'YUYV': <OBFormat.YUYV: 0>, 'YUY2': <OBFormat.YUY2: 1>, 'UYVY': <OBFormat.UYVY: 2>, 'NV12': <OBFormat.NV12: 3>, 'NV21': <OBFormat.NV21: 4>, 'MJPG': <OBFormat.MJPG: 5>, 'H264': <OBFormat.H264: 6>, 'H265': <OBFormat.H265: 7>, 'Y16': <OBFormat.Y16: 8>, 'Y8': <OBFormat.Y8: 9>, 'Y10': <OBFormat.Y10: 10>, 'Y11': <OBFormat.Y11: 11>, 'Y12': <OBFormat.Y12: 12>, 'GRAY': <OBFormat.GRAY: 13>, 'HEVC': <OBFormat.HEVC: 14>, 'I420': <OBFormat.I420: 15>, 'ACCEL': <OBFormat.ACCEL: 16>, 'GYRO': <OBFormat.GYRO: 17>, 'POINT': <OBFormat.POINT: 19>, 'RGB_POINT': <OBFormat.RGB_POINT: 20>, 'RLE': <OBFormat.RLE: 21>, 'RGB': <OBFormat.RGB: 22>, 'BGR': <OBFormat.BGR: 23>, 'Y14': <OBFormat.Y14: 24>, 'BGRA': <OBFormat.BGRA: 25>, 'COMPRESSED': <OBFormat.COMPRESSED: 26>, 'RVL': <OBFormat.RVL: 27>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class OBFrameAggregateOutputMode:
    """
    Members:
    
      FULL_FRAME_REQUIRE
    
      COLOR_FRAME_REQUIRE
    
      ANY_SITUATION
    """
    ANY_SITUATION: typing.ClassVar[OBFrameAggregateOutputMode]  # value = <OBFrameAggregateOutputMode.ANY_SITUATION: 2>
    COLOR_FRAME_REQUIRE: typing.ClassVar[OBFrameAggregateOutputMode]  # value = <OBFrameAggregateOutputMode.COLOR_FRAME_REQUIRE: 1>
    FULL_FRAME_REQUIRE: typing.ClassVar[OBFrameAggregateOutputMode]  # value = <OBFrameAggregateOutputMode.FULL_FRAME_REQUIRE: 0>
    __members__: typing.ClassVar[dict[str, OBFrameAggregateOutputMode]]  # value = {'FULL_FRAME_REQUIRE': <OBFrameAggregateOutputMode.FULL_FRAME_REQUIRE: 0>, 'COLOR_FRAME_REQUIRE': <OBFrameAggregateOutputMode.COLOR_FRAME_REQUIRE: 1>, 'ANY_SITUATION': <OBFrameAggregateOutputMode.ANY_SITUATION: 2>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class OBFrameMetadataType:
    """
    Members:
    
      TIMESTAMP
    
      SENSOR_TIMESTAMP
    
      FRAME_NUMBER
    
      AUTO_EXPOSURE
    
      EXPOSURE
    
      GAIN
    
      AUTO_WHITE_BALANCE
    
      WHITE_BALANCE
    
      BRIGHTNESS
    
      CONTRAST
    
      SATURATION
    
      SHARPNESS
    
      BACKLIGHT_COMPENSATION
    
      HUE
    
      GAMMA
    
      POWER_LINE_FREQUENCY
    
      LOW_LIGHT_COMPENSATION
    
      MANUAL_WHITE_BALANCE
    
      ACTUAL_FRAME_RATE
    
      FRAME_RATE
    
      AE_ROI_LEFT
    
      AE_ROI_TOP
    
      AE_ROI_RIGHT
    
      AE_ROI_BOTTOM
    
      EXPOSURE_PRIORITY
    
      HDR_SEQUENCE_NAME
    
      HDR_SEQUENCE_SIZE
    
      HDR_SEQUENCE_INDEX
    
      LASER_POWER
    
      LASER_POWER_LEVEL
    
      LASER_STATUS
    
      GPIO_INPUT_DATA
    
      COUNT
    """
    ACTUAL_FRAME_RATE: typing.ClassVar[OBFrameMetadataType]  # value = <OBFrameMetadataType.ACTUAL_FRAME_RATE: 18>
    AE_ROI_BOTTOM: typing.ClassVar[OBFrameMetadataType]  # value = <OBFrameMetadataType.AE_ROI_BOTTOM: 23>
    AE_ROI_LEFT: typing.ClassVar[OBFrameMetadataType]  # value = <OBFrameMetadataType.AE_ROI_LEFT: 20>
    AE_ROI_RIGHT: typing.ClassVar[OBFrameMetadataType]  # value = <OBFrameMetadataType.AE_ROI_RIGHT: 22>
    AE_ROI_TOP: typing.ClassVar[OBFrameMetadataType]  # value = <OBFrameMetadataType.AE_ROI_TOP: 21>
    AUTO_EXPOSURE: typing.ClassVar[OBFrameMetadataType]  # value = <OBFrameMetadataType.AUTO_EXPOSURE: 3>
    AUTO_WHITE_BALANCE: typing.ClassVar[OBFrameMetadataType]  # value = <OBFrameMetadataType.AUTO_WHITE_BALANCE: 6>
    BACKLIGHT_COMPENSATION: typing.ClassVar[OBFrameMetadataType]  # value = <OBFrameMetadataType.BACKLIGHT_COMPENSATION: 12>
    BRIGHTNESS: typing.ClassVar[OBFrameMetadataType]  # value = <OBFrameMetadataType.BRIGHTNESS: 8>
    CONTRAST: typing.ClassVar[OBFrameMetadataType]  # value = <OBFrameMetadataType.CONTRAST: 9>
    COUNT: typing.ClassVar[OBFrameMetadataType]  # value = <OBFrameMetadataType.COUNT: 32>
    EXPOSURE: typing.ClassVar[OBFrameMetadataType]  # value = <OBFrameMetadataType.EXPOSURE: 4>
    EXPOSURE_PRIORITY: typing.ClassVar[OBFrameMetadataType]  # value = <OBFrameMetadataType.EXPOSURE_PRIORITY: 24>
    FRAME_NUMBER: typing.ClassVar[OBFrameMetadataType]  # value = <OBFrameMetadataType.FRAME_NUMBER: 2>
    FRAME_RATE: typing.ClassVar[OBFrameMetadataType]  # value = <OBFrameMetadataType.FRAME_RATE: 19>
    GAIN: typing.ClassVar[OBFrameMetadataType]  # value = <OBFrameMetadataType.GAIN: 5>
    GAMMA: typing.ClassVar[OBFrameMetadataType]  # value = <OBFrameMetadataType.GAMMA: 14>
    GPIO_INPUT_DATA: typing.ClassVar[OBFrameMetadataType]  # value = <OBFrameMetadataType.GPIO_INPUT_DATA: 31>
    HDR_SEQUENCE_INDEX: typing.ClassVar[OBFrameMetadataType]  # value = <OBFrameMetadataType.HDR_SEQUENCE_INDEX: 27>
    HDR_SEQUENCE_NAME: typing.ClassVar[OBFrameMetadataType]  # value = <OBFrameMetadataType.HDR_SEQUENCE_NAME: 25>
    HDR_SEQUENCE_SIZE: typing.ClassVar[OBFrameMetadataType]  # value = <OBFrameMetadataType.HDR_SEQUENCE_SIZE: 26>
    HUE: typing.ClassVar[OBFrameMetadataType]  # value = <OBFrameMetadataType.HUE: 13>
    LASER_POWER: typing.ClassVar[OBFrameMetadataType]  # value = <OBFrameMetadataType.LASER_POWER: 28>
    LASER_POWER_LEVEL: typing.ClassVar[OBFrameMetadataType]  # value = <OBFrameMetadataType.LASER_POWER_LEVEL: 29>
    LASER_STATUS: typing.ClassVar[OBFrameMetadataType]  # value = <OBFrameMetadataType.LASER_STATUS: 30>
    LOW_LIGHT_COMPENSATION: typing.ClassVar[OBFrameMetadataType]  # value = <OBFrameMetadataType.LOW_LIGHT_COMPENSATION: 16>
    MANUAL_WHITE_BALANCE: typing.ClassVar[OBFrameMetadataType]  # value = <OBFrameMetadataType.MANUAL_WHITE_BALANCE: 17>
    POWER_LINE_FREQUENCY: typing.ClassVar[OBFrameMetadataType]  # value = <OBFrameMetadataType.POWER_LINE_FREQUENCY: 15>
    SATURATION: typing.ClassVar[OBFrameMetadataType]  # value = <OBFrameMetadataType.SATURATION: 10>
    SENSOR_TIMESTAMP: typing.ClassVar[OBFrameMetadataType]  # value = <OBFrameMetadataType.SENSOR_TIMESTAMP: 1>
    SHARPNESS: typing.ClassVar[OBFrameMetadataType]  # value = <OBFrameMetadataType.SHARPNESS: 11>
    TIMESTAMP: typing.ClassVar[OBFrameMetadataType]  # value = <OBFrameMetadataType.TIMESTAMP: 0>
    WHITE_BALANCE: typing.ClassVar[OBFrameMetadataType]  # value = <OBFrameMetadataType.WHITE_BALANCE: 7>
    __members__: typing.ClassVar[dict[str, OBFrameMetadataType]]  # value = {'TIMESTAMP': <OBFrameMetadataType.TIMESTAMP: 0>, 'SENSOR_TIMESTAMP': <OBFrameMetadataType.SENSOR_TIMESTAMP: 1>, 'FRAME_NUMBER': <OBFrameMetadataType.FRAME_NUMBER: 2>, 'AUTO_EXPOSURE': <OBFrameMetadataType.AUTO_EXPOSURE: 3>, 'EXPOSURE': <OBFrameMetadataType.EXPOSURE: 4>, 'GAIN': <OBFrameMetadataType.GAIN: 5>, 'AUTO_WHITE_BALANCE': <OBFrameMetadataType.AUTO_WHITE_BALANCE: 6>, 'WHITE_BALANCE': <OBFrameMetadataType.WHITE_BALANCE: 7>, 'BRIGHTNESS': <OBFrameMetadataType.BRIGHTNESS: 8>, 'CONTRAST': <OBFrameMetadataType.CONTRAST: 9>, 'SATURATION': <OBFrameMetadataType.SATURATION: 10>, 'SHARPNESS': <OBFrameMetadataType.SHARPNESS: 11>, 'BACKLIGHT_COMPENSATION': <OBFrameMetadataType.BACKLIGHT_COMPENSATION: 12>, 'HUE': <OBFrameMetadataType.HUE: 13>, 'GAMMA': <OBFrameMetadataType.GAMMA: 14>, 'POWER_LINE_FREQUENCY': <OBFrameMetadataType.POWER_LINE_FREQUENCY: 15>, 'LOW_LIGHT_COMPENSATION': <OBFrameMetadataType.LOW_LIGHT_COMPENSATION: 16>, 'MANUAL_WHITE_BALANCE': <OBFrameMetadataType.MANUAL_WHITE_BALANCE: 17>, 'ACTUAL_FRAME_RATE': <OBFrameMetadataType.ACTUAL_FRAME_RATE: 18>, 'FRAME_RATE': <OBFrameMetadataType.FRAME_RATE: 19>, 'AE_ROI_LEFT': <OBFrameMetadataType.AE_ROI_LEFT: 20>, 'AE_ROI_TOP': <OBFrameMetadataType.AE_ROI_TOP: 21>, 'AE_ROI_RIGHT': <OBFrameMetadataType.AE_ROI_RIGHT: 22>, 'AE_ROI_BOTTOM': <OBFrameMetadataType.AE_ROI_BOTTOM: 23>, 'EXPOSURE_PRIORITY': <OBFrameMetadataType.EXPOSURE_PRIORITY: 24>, 'HDR_SEQUENCE_NAME': <OBFrameMetadataType.HDR_SEQUENCE_NAME: 25>, 'HDR_SEQUENCE_SIZE': <OBFrameMetadataType.HDR_SEQUENCE_SIZE: 26>, 'HDR_SEQUENCE_INDEX': <OBFrameMetadataType.HDR_SEQUENCE_INDEX: 27>, 'LASER_POWER': <OBFrameMetadataType.LASER_POWER: 28>, 'LASER_POWER_LEVEL': <OBFrameMetadataType.LASER_POWER_LEVEL: 29>, 'LASER_STATUS': <OBFrameMetadataType.LASER_STATUS: 30>, 'GPIO_INPUT_DATA': <OBFrameMetadataType.GPIO_INPUT_DATA: 31>, 'COUNT': <OBFrameMetadataType.COUNT: 32>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class OBFrameType:
    """
    Members:
    
      UNKNOWN_FRAME
    
      VIDEO_FRAME
    
      IR_FRAME
    
      COLOR_FRAME
    
      DEPTH_FRAME
    
      ACCEL_FRAME
    
      GYRO_FRAME
    
      LEFT_IR_FRAME
    
      RIGHT_IR_FRAME
    
      FRAME_SET
    """
    ACCEL_FRAME: typing.ClassVar[OBFrameType]  # value = <OBFrameType.ACCEL_FRAME: 4>
    COLOR_FRAME: typing.ClassVar[OBFrameType]  # value = <OBFrameType.COLOR_FRAME: 2>
    DEPTH_FRAME: typing.ClassVar[OBFrameType]  # value = <OBFrameType.DEPTH_FRAME: 3>
    FRAME_SET: typing.ClassVar[OBFrameType]  # value = <OBFrameType.FRAME_SET: 5>
    GYRO_FRAME: typing.ClassVar[OBFrameType]  # value = <OBFrameType.GYRO_FRAME: 7>
    IR_FRAME: typing.ClassVar[OBFrameType]  # value = <OBFrameType.IR_FRAME: 1>
    LEFT_IR_FRAME: typing.ClassVar[OBFrameType]  # value = <OBFrameType.LEFT_IR_FRAME: 8>
    RIGHT_IR_FRAME: typing.ClassVar[OBFrameType]  # value = <OBFrameType.RIGHT_IR_FRAME: 9>
    UNKNOWN_FRAME: typing.ClassVar[OBFrameType]  # value = <OBFrameType.UNKNOWN_FRAME: -1>
    VIDEO_FRAME: typing.ClassVar[OBFrameType]  # value = <OBFrameType.VIDEO_FRAME: 0>
    __members__: typing.ClassVar[dict[str, OBFrameType]]  # value = {'UNKNOWN_FRAME': <OBFrameType.UNKNOWN_FRAME: -1>, 'VIDEO_FRAME': <OBFrameType.VIDEO_FRAME: 0>, 'IR_FRAME': <OBFrameType.IR_FRAME: 1>, 'COLOR_FRAME': <OBFrameType.COLOR_FRAME: 2>, 'DEPTH_FRAME': <OBFrameType.DEPTH_FRAME: 3>, 'ACCEL_FRAME': <OBFrameType.ACCEL_FRAME: 4>, 'GYRO_FRAME': <OBFrameType.GYRO_FRAME: 7>, 'LEFT_IR_FRAME': <OBFrameType.LEFT_IR_FRAME: 8>, 'RIGHT_IR_FRAME': <OBFrameType.RIGHT_IR_FRAME: 9>, 'FRAME_SET': <OBFrameType.FRAME_SET: 5>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class OBGyroIntrinsic:
    bias: numpy.ndarray[numpy.float64]
    noise_density: float
    random_walk: float
    reference_temp: float
    scale_misalignment: numpy.ndarray[numpy.float64]
    temp_slope: numpy.ndarray[numpy.float64]
    def __init__(self) -> None:
        ...
class OBGyroSampleRate:
    """
    Members:
    
      SAMPLE_RATE_1_5625_HZ
    
      SAMPLE_RATE_3_125_HZ
    
      SAMPLE_RATE_6_25_HZ
    
      SAMPLE_RATE_12_5_HZ
    
      SAMPLE_RATE_25_HZ
    
      SAMPLE_RATE_50_HZ
    
      SAMPLE_RATE_100_HZ
    
      SAMPLE_RATE_200_HZ
    
      SAMPLE_RATE_500_HZ
    
      SAMPLE_RATE_1_KHZ
    
      SAMPLE_RATE_2_KHZ
    
      SAMPLE_RATE_4_KHZ
    
      SAMPLE_RATE_8_KHZ
    
      SAMPLE_RATE_16_KHZ
    
      SAMPLE_RATE_32_KHZ
    """
    SAMPLE_RATE_100_HZ: typing.ClassVar[OBGyroSampleRate]  # value = <OBGyroSampleRate.SAMPLE_RATE_100_HZ: 7>
    SAMPLE_RATE_12_5_HZ: typing.ClassVar[OBGyroSampleRate]  # value = <OBGyroSampleRate.SAMPLE_RATE_12_5_HZ: 4>
    SAMPLE_RATE_16_KHZ: typing.ClassVar[OBGyroSampleRate]  # value = <OBGyroSampleRate.SAMPLE_RATE_16_KHZ: 14>
    SAMPLE_RATE_1_5625_HZ: typing.ClassVar[OBGyroSampleRate]  # value = <OBGyroSampleRate.SAMPLE_RATE_1_5625_HZ: 1>
    SAMPLE_RATE_1_KHZ: typing.ClassVar[OBGyroSampleRate]  # value = <OBGyroSampleRate.SAMPLE_RATE_1_KHZ: 10>
    SAMPLE_RATE_200_HZ: typing.ClassVar[OBGyroSampleRate]  # value = <OBGyroSampleRate.SAMPLE_RATE_200_HZ: 8>
    SAMPLE_RATE_25_HZ: typing.ClassVar[OBGyroSampleRate]  # value = <OBGyroSampleRate.SAMPLE_RATE_25_HZ: 5>
    SAMPLE_RATE_2_KHZ: typing.ClassVar[OBGyroSampleRate]  # value = <OBGyroSampleRate.SAMPLE_RATE_2_KHZ: 11>
    SAMPLE_RATE_32_KHZ: typing.ClassVar[OBGyroSampleRate]  # value = <OBGyroSampleRate.SAMPLE_RATE_32_KHZ: 15>
    SAMPLE_RATE_3_125_HZ: typing.ClassVar[OBGyroSampleRate]  # value = <OBGyroSampleRate.SAMPLE_RATE_3_125_HZ: 2>
    SAMPLE_RATE_4_KHZ: typing.ClassVar[OBGyroSampleRate]  # value = <OBGyroSampleRate.SAMPLE_RATE_4_KHZ: 12>
    SAMPLE_RATE_500_HZ: typing.ClassVar[OBGyroSampleRate]  # value = <OBGyroSampleRate.SAMPLE_RATE_500_HZ: 9>
    SAMPLE_RATE_50_HZ: typing.ClassVar[OBGyroSampleRate]  # value = <OBGyroSampleRate.SAMPLE_RATE_50_HZ: 6>
    SAMPLE_RATE_6_25_HZ: typing.ClassVar[OBGyroSampleRate]  # value = <OBGyroSampleRate.SAMPLE_RATE_6_25_HZ: 3>
    SAMPLE_RATE_8_KHZ: typing.ClassVar[OBGyroSampleRate]  # value = <OBGyroSampleRate.SAMPLE_RATE_8_KHZ: 13>
    __members__: typing.ClassVar[dict[str, OBGyroSampleRate]]  # value = {'SAMPLE_RATE_1_5625_HZ': <OBGyroSampleRate.SAMPLE_RATE_1_5625_HZ: 1>, 'SAMPLE_RATE_3_125_HZ': <OBGyroSampleRate.SAMPLE_RATE_3_125_HZ: 2>, 'SAMPLE_RATE_6_25_HZ': <OBGyroSampleRate.SAMPLE_RATE_6_25_HZ: 3>, 'SAMPLE_RATE_12_5_HZ': <OBGyroSampleRate.SAMPLE_RATE_12_5_HZ: 4>, 'SAMPLE_RATE_25_HZ': <OBGyroSampleRate.SAMPLE_RATE_25_HZ: 5>, 'SAMPLE_RATE_50_HZ': <OBGyroSampleRate.SAMPLE_RATE_50_HZ: 6>, 'SAMPLE_RATE_100_HZ': <OBGyroSampleRate.SAMPLE_RATE_100_HZ: 7>, 'SAMPLE_RATE_200_HZ': <OBGyroSampleRate.SAMPLE_RATE_200_HZ: 8>, 'SAMPLE_RATE_500_HZ': <OBGyroSampleRate.SAMPLE_RATE_500_HZ: 9>, 'SAMPLE_RATE_1_KHZ': <OBGyroSampleRate.SAMPLE_RATE_1_KHZ: 10>, 'SAMPLE_RATE_2_KHZ': <OBGyroSampleRate.SAMPLE_RATE_2_KHZ: 11>, 'SAMPLE_RATE_4_KHZ': <OBGyroSampleRate.SAMPLE_RATE_4_KHZ: 12>, 'SAMPLE_RATE_8_KHZ': <OBGyroSampleRate.SAMPLE_RATE_8_KHZ: 13>, 'SAMPLE_RATE_16_KHZ': <OBGyroSampleRate.SAMPLE_RATE_16_KHZ: 14>, 'SAMPLE_RATE_32_KHZ': <OBGyroSampleRate.SAMPLE_RATE_32_KHZ: 15>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class OBHdrConfig:
    enable: int
    exposure_1: int
    exposure_2: int
    gain_1: int
    gain_2: int
    sequence_name: int
    def __init__(self) -> None:
        ...
class OBHoleFillingMode:
    """
    Members:
    
      TOP
    
      NEAREST
    
      FURTHEST
    """
    FURTHEST: typing.ClassVar[OBHoleFillingMode]  # value = <OBHoleFillingMode.FURTHEST: 2>
    NEAREST: typing.ClassVar[OBHoleFillingMode]  # value = <OBHoleFillingMode.NEAREST: 1>
    TOP: typing.ClassVar[OBHoleFillingMode]  # value = <OBHoleFillingMode.TOP: 0>
    __members__: typing.ClassVar[dict[str, OBHoleFillingMode]]  # value = {'TOP': <OBHoleFillingMode.TOP: 0>, 'NEAREST': <OBHoleFillingMode.NEAREST: 1>, 'FURTHEST': <OBHoleFillingMode.FURTHEST: 2>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class OBIntPropertyRange:
    current: int
    default_value: int
    max: int
    min: int
    step: int
    def __init__(self) -> None:
        ...
class OBLogLevel:
    """
    Members:
    
      DEBUG
    
      INFO
    
      WARNING
    
      ERROR
    
      FATAL
    
      NONE
    """
    DEBUG: typing.ClassVar[OBLogLevel]  # value = <OBLogLevel.DEBUG: 0>
    ERROR: typing.ClassVar[OBLogLevel]  # value = <OBLogLevel.ERROR: 3>
    FATAL: typing.ClassVar[OBLogLevel]  # value = <OBLogLevel.FATAL: 4>
    INFO: typing.ClassVar[OBLogLevel]  # value = <OBLogLevel.INFO: 1>
    NONE: typing.ClassVar[OBLogLevel]  # value = <OBLogLevel.NONE: 5>
    WARNING: typing.ClassVar[OBLogLevel]  # value = <OBLogLevel.WARNING: 2>
    __members__: typing.ClassVar[dict[str, OBLogLevel]]  # value = {'DEBUG': <OBLogLevel.DEBUG: 0>, 'INFO': <OBLogLevel.INFO: 1>, 'WARNING': <OBLogLevel.WARNING: 2>, 'ERROR': <OBLogLevel.ERROR: 3>, 'FATAL': <OBLogLevel.FATAL: 4>, 'NONE': <OBLogLevel.NONE: 5>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class OBMediaState:
    """
    Members:
    
      OB_MEDIA_BEGIN
    
      OB_MEDIA_PAUSE
    
      OB_MEDIA_RESUME
    
      OB_MEDIA_END
    """
    OB_MEDIA_BEGIN: typing.ClassVar[OBMediaState]  # value = <OBMediaState.OB_MEDIA_BEGIN: 0>
    OB_MEDIA_END: typing.ClassVar[OBMediaState]  # value = <OBMediaState.OB_MEDIA_END: 3>
    OB_MEDIA_PAUSE: typing.ClassVar[OBMediaState]  # value = <OBMediaState.OB_MEDIA_PAUSE: 1>
    OB_MEDIA_RESUME: typing.ClassVar[OBMediaState]  # value = <OBMediaState.OB_MEDIA_PAUSE: 1>
    __members__: typing.ClassVar[dict[str, OBMediaState]]  # value = {'OB_MEDIA_BEGIN': <OBMediaState.OB_MEDIA_BEGIN: 0>, 'OB_MEDIA_PAUSE': <OBMediaState.OB_MEDIA_PAUSE: 1>, 'OB_MEDIA_RESUME': <OBMediaState.OB_MEDIA_PAUSE: 1>, 'OB_MEDIA_END': <OBMediaState.OB_MEDIA_END: 3>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class OBMediaType:
    """
    Members:
    
      DEPTH
    
      COLOR
    
      IR
    
      GYRO
    
      ACCEL
    
      CAMERA_PARAM
    
      DEVICE_INFO
    
      STREAM_INFO
    
      LEFT_IR
    
      RIGHT_IR
    """
    ACCEL: typing.ClassVar[OBMediaType]  # value = <OBMediaType.ACCEL: 16>
    CAMERA_PARAM: typing.ClassVar[OBMediaType]  # value = <OBMediaType.CAMERA_PARAM: 32>
    COLOR: typing.ClassVar[OBMediaType]  # value = <OBMediaType.COLOR: 1>
    DEPTH: typing.ClassVar[OBMediaType]  # value = <OBMediaType.DEPTH: 2>
    DEVICE_INFO: typing.ClassVar[OBMediaType]  # value = <OBMediaType.DEVICE_INFO: 64>
    GYRO: typing.ClassVar[OBMediaType]  # value = <OBMediaType.GYRO: 8>
    IR: typing.ClassVar[OBMediaType]  # value = <OBMediaType.IR: 4>
    LEFT_IR: typing.ClassVar[OBMediaType]  # value = <OBMediaType.LEFT_IR: 256>
    RIGHT_IR: typing.ClassVar[OBMediaType]  # value = <OBMediaType.RIGHT_IR: 512>
    STREAM_INFO: typing.ClassVar[OBMediaType]  # value = <OBMediaType.STREAM_INFO: 128>
    __members__: typing.ClassVar[dict[str, OBMediaType]]  # value = {'DEPTH': <OBMediaType.DEPTH: 2>, 'COLOR': <OBMediaType.COLOR: 1>, 'IR': <OBMediaType.IR: 4>, 'GYRO': <OBMediaType.GYRO: 8>, 'ACCEL': <OBMediaType.ACCEL: 16>, 'CAMERA_PARAM': <OBMediaType.CAMERA_PARAM: 32>, 'DEVICE_INFO': <OBMediaType.DEVICE_INFO: 64>, 'STREAM_INFO': <OBMediaType.STREAM_INFO: 128>, 'LEFT_IR': <OBMediaType.LEFT_IR: 256>, 'RIGHT_IR': <OBMediaType.RIGHT_IR: 512>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class OBMultiDeviceSyncConfig:
    color_delay_us: int
    depth_delay_us: int
    frames_per_trigger: int
    mode: OBMultiDeviceSyncMode
    trigger_out_delay_us: int
    trigger_out_enable: bool
    trigger_to_image_delay_us: int
    def __init__(self) -> None:
        ...
class OBMultiDeviceSyncMode:
    """
    Members:
    
      FREE_RUN
    
      STANDALONE
    
      PRIMARY
    
      SECONDARY
    
      SECONDARY_SYNCED
    
      SOFTWARE_TRIGGERING
    
      HARDWARE_TRIGGERING
    """
    FREE_RUN: typing.ClassVar[OBMultiDeviceSyncMode]  # value = <OBMultiDeviceSyncMode.FREE_RUN: 1>
    HARDWARE_TRIGGERING: typing.ClassVar[OBMultiDeviceSyncMode]  # value = <OBMultiDeviceSyncMode.HARDWARE_TRIGGERING: 64>
    PRIMARY: typing.ClassVar[OBMultiDeviceSyncMode]  # value = <OBMultiDeviceSyncMode.PRIMARY: 4>
    SECONDARY: typing.ClassVar[OBMultiDeviceSyncMode]  # value = <OBMultiDeviceSyncMode.SECONDARY: 8>
    SECONDARY_SYNCED: typing.ClassVar[OBMultiDeviceSyncMode]  # value = <OBMultiDeviceSyncMode.SECONDARY_SYNCED: 16>
    SOFTWARE_TRIGGERING: typing.ClassVar[OBMultiDeviceSyncMode]  # value = <OBMultiDeviceSyncMode.SOFTWARE_TRIGGERING: 32>
    STANDALONE: typing.ClassVar[OBMultiDeviceSyncMode]  # value = <OBMultiDeviceSyncMode.STANDALONE: 2>
    __members__: typing.ClassVar[dict[str, OBMultiDeviceSyncMode]]  # value = {'FREE_RUN': <OBMultiDeviceSyncMode.FREE_RUN: 1>, 'STANDALONE': <OBMultiDeviceSyncMode.STANDALONE: 2>, 'PRIMARY': <OBMultiDeviceSyncMode.PRIMARY: 4>, 'SECONDARY': <OBMultiDeviceSyncMode.SECONDARY: 8>, 'SECONDARY_SYNCED': <OBMultiDeviceSyncMode.SECONDARY_SYNCED: 16>, 'SOFTWARE_TRIGGERING': <OBMultiDeviceSyncMode.SOFTWARE_TRIGGERING: 32>, 'HARDWARE_TRIGGERING': <OBMultiDeviceSyncMode.HARDWARE_TRIGGERING: 64>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class OBNoiseRemovalFilterParams:
    disp_diff: int
    max_size: int
    type: OBDDONoiseRemovalType
    def __init__(self) -> None:
        ...
class OBPermissionType:
    """
    Members:
    
      PERMISSION_DENY
    
      PERMISSION_READ
    
      PERMISSION_WRITE
    
      PERMISSION_READ_WRITE
    """
    PERMISSION_DENY: typing.ClassVar[OBPermissionType]  # value = <OBPermissionType.PERMISSION_DENY: 0>
    PERMISSION_READ: typing.ClassVar[OBPermissionType]  # value = <OBPermissionType.PERMISSION_READ: 1>
    PERMISSION_READ_WRITE: typing.ClassVar[OBPermissionType]  # value = <OBPermissionType.PERMISSION_READ_WRITE: 3>
    PERMISSION_WRITE: typing.ClassVar[OBPermissionType]  # value = <OBPermissionType.PERMISSION_WRITE: 2>
    __members__: typing.ClassVar[dict[str, OBPermissionType]]  # value = {'PERMISSION_DENY': <OBPermissionType.PERMISSION_DENY: 0>, 'PERMISSION_READ': <OBPermissionType.PERMISSION_READ: 1>, 'PERMISSION_WRITE': <OBPermissionType.PERMISSION_WRITE: 2>, 'PERMISSION_READ_WRITE': <OBPermissionType.PERMISSION_READ_WRITE: 3>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class OBPoint:
    x: float
    y: float
    z: float
    @staticmethod
    def get_sizeof() -> int:
        ...
    def __init__(self) -> None:
        ...
    def __repr__(self) -> str:
        ...
class OBPoint2f:
    x: float
    y: float
    def __init__(self) -> None:
        ...
    def __repr__(self) -> str:
        ...
class OBPowerLineFreqMode:
    """
    Members:
    
      FREQUENCY_50HZ
    
      FREQUENCY_60HZ
    
      FREQUENCY_CLOSE
    """
    FREQUENCY_50HZ: typing.ClassVar[OBPowerLineFreqMode]  # value = <OBPowerLineFreqMode.FREQUENCY_50HZ: 1>
    FREQUENCY_60HZ: typing.ClassVar[OBPowerLineFreqMode]  # value = <OBPowerLineFreqMode.FREQUENCY_60HZ: 2>
    FREQUENCY_CLOSE: typing.ClassVar[OBPowerLineFreqMode]  # value = <OBPowerLineFreqMode.FREQUENCY_CLOSE: 0>
    __members__: typing.ClassVar[dict[str, OBPowerLineFreqMode]]  # value = {'FREQUENCY_50HZ': <OBPowerLineFreqMode.FREQUENCY_50HZ: 1>, 'FREQUENCY_60HZ': <OBPowerLineFreqMode.FREQUENCY_60HZ: 2>, 'FREQUENCY_CLOSE': <OBPowerLineFreqMode.FREQUENCY_CLOSE: 0>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class OBPropertyID:
    """
    Members:
    
      OB_PROP_LDP_BOOL : LDP switch
    
      OB_PROP_LASER_BOOL : Laser switch
    
      OB_PROP_LASER_PULSE_WIDTH_INT : laser pulse width
    
      OB_PROP_LASER_CURRENT_FLOAT : Laser current (uint: mA)
    
      OB_PROP_FLOOD_BOOL : IR flood switch
    
      OB_PROP_FLOOD_LEVEL_INT : IR flood level
    
      OB_PROP_DEPTH_MIRROR_BOOL : Depth mirror
    
      OB_PROP_DEPTH_FLIP_BOOL : Depth flip
    
      OB_PROP_DEPTH_POSTFILTER_BOOL : Depth Post filter
    
      OB_PROP_DEPTH_HOLEFILTER_BOOL : Depth Hole filter
    
      OB_PROP_IR_MIRROR_BOOL : IR mirror
    
      OB_PROP_IR_FLIP_BOOL : IR flip
    
      OB_PROP_MIN_DEPTH_INT : Minimum depth threshold
    
      OB_PROP_MAX_DEPTH_INT : Maximum depth threshold
    
      OB_PROP_DEPTH_SOFT_FILTER_BOOL : Software filter switch
    
      OB_PROP_LDP_STATUS_BOOL : LDP status
    
      OB_PROP_DEPTH_MAX_DIFF_INT : soft filter max diff param
    
      OB_PROP_DEPTH_MAX_SPECKLE_SIZE_INT : soft filter maxSpeckleSize
    
      OB_PROP_DEPTH_ALIGN_HARDWARE_BOOL : Hardware d2c is on
    
      OB_PROP_TIMESTAMP_OFFSET_INT : Timestamp adjustment
    
      OB_PROP_HARDWARE_DISTORTION_SWITCH_BOOL :  Hardware distortion switch Rectify
    
      OB_PROP_FAN_WORK_MODE_INT : Fan mode switch
    
      OB_PROP_DEPTH_ALIGN_HARDWARE_MODE_INT : Multi-resolution D2C mode
    
      OB_PROP_ANTI_COLLUSION_ACTIVATION_STATUS_BOOL : Anti_collusion activation status
    
      OB_PROP_DEPTH_PRECISION_LEVEL_INT : he depth precision level, which may change the depth frame data unit, needs to be confirmed through the ValueScale interface of DepthFrame
    
      OB_PROP_TOF_FILTER_RANGE_INT : tof filter range configuration
    
      OB_PROP_LASER_MODE_INT : laser mode, the firmware terminal currently only return 1: IR Drive, 2: Torch
    
      OB_PROP_RECTIFY2_BOOL : brt2r-rectify function switch (brt2r is a special module on mx6600), 0: Disable, 1: Rectify Enable
    
      OB_PROP_COLOR_MIRROR_BOOL : Color mirror
    
      OB_PROP_COLOR_FLIP_BOOL : Color flip
    
      OB_PROP_INDICATOR_LIGHT_BOOL : Indicator switch, 0: Disable, 1: Enable
    
      OB_PROP_DISPARITY_TO_DEPTH_BOOL : Disparity to depth switch, 0: off, the depth stream outputs the disparity map; 1. On, the depth stream outputs the depth map.
    
      OB_PROP_BRT_BOOL : BRT function switch (anti-background interference), 0: Disable, 1: Enable
    
      OB_PROP_WATCHDOG_BOOL : Watchdog function switch, 0: Disable, 1: Enable
    
      OB_PROP_EXTERNAL_SIGNAL_RESET_BOOL : External signal reset function switch, 0: Disable, 1: Enable
    
      OB_PROP_HEARTBEAT_BOOL : Heartbeat monitoring function switch, 0: Disable, 1: Enable
    
      OB_PROP_DEPTH_CROPPING_MODE_INT : Depth cropping mode device: OB_DEPTH_CROPPING_MODE
    
      OB_PROP_D2C_PREPROCESS_BOOL : D2C preprocessing switch (such as RGB cropping), 0: off, 1: on
    
      OB_PROP_RGB_CUSTOM_CROP_BOOL : Custom RGB cropping switch, 0 is off, 1 is on custom cropping, and the ROI cropping area is issued
    
      OB_PROP_DEVICE_WORK_MODE_INT : Device operating mode (power consumption)
    
      OB_PROP_DEVICE_COMMUNICATION_TYPE_INT : Device communication type, 0: USB; 1: Ethernet(RTSP)
    
      OB_PROP_SWITCH_IR_MODE_INT : Switch infrared imaging mode, 0: active IR mode, 1: passive IR mode
    
      OB_PROP_LASER_POWER_LEVEL_CONTROL_INT : Laser power level
    
      OB_PROP_LASER_ENERGY_LEVEL_INT : Laser energy level
    
      OB_PROP_LDP_MEASURE_DISTANCE_INT : LDP's measure distance, unit: mm
    
      OB_PROP_TIMER_RESET_SIGNAL_BOOL : Reset device time to zero
    
      OB_PROP_TIMER_RESET_TRIGGER_OUT_ENABLE_BOOL : Enable send reset device time signal to other device. true: enable, false: disable
    
      OB_PROP_TIMER_RESET_DELAY_US_INT : Delay to reset device time, unit: us
    
      OB_PROP_CAPTURE_IMAGE_SIGNAL_BOOL
    
      OB_PROP_IR_RIGHT_MIRROR_BOOL : Signal to capture image
    
      OB_PROP_CAPTURE_IMAGE_FRAME_NUMBER_INT : Number frame to capture once a OB_PROP_CAPTURE_IMAGE_SIGNAL_BOOL' effect. range: [1, 255]
    
      OB_PROP_IR_RIGHT_FLIP_BOOL : Right IR sensor flip state. true: flip image, false: origin, default: false
    
      OB_PROP_COLOR_ROTATE_INT : Color sensor rotation, angle{0, 90, 180, 270}
    
      OB_PROP_IR_ROTATE_INT : IR/Left-IR sensor rotation, angle{0, 90, 180, 270}
    
      OB_PROP_IR_RIGHT_ROTATE_INT : Right IR sensor rotation, angle{0, 90, 180, 270}
    
      OB_PROP_DEPTH_ROTATE_INT : Depth sensor rotation, angle{0, 90, 180, 270}
    
      OB_PROP_LASER_HW_ENERGY_LEVEL_INT : Get hardware laser energy level which real state of laser element. OB_PROP_LASER_ENERGY_LEVEL_INT(99)will effect this command which it setting and changed the hardware laser energy level.
    
      OB_PROP_USB_POWER_STATE_INT : USB's power state
    
      OB_PROP_DC_POWER_STATE_INT : DC's power state
    
      OB_PROP_DEVICE_DEVELOPMENT_MODE_INT
    
      OB_PROP_SYNC_SIGNAL_TRIGGER_OUT_BOOL
    
      OB_PROP_RESTORE_FACTORY_SETTINGS_BOOL
    
      OB_PROP_BOOT_INTO_RECOVERY_MODE_BOOL
    
      OB_PROP_DEVICE_IN_RECOVERY_MODE_BOOL
    
      OB_PROP_CAPTURE_INTERVAL_MODE_INT
    
      OB_PROP_CAPTURE_IMAGE_TIME_INTERVAL_INT
    
      OB_PROP_CAPTURE_IMAGE_NUMBER_INTERVAL_INT
    
      OB_PROP_TIMER_RESET_ENABLE_BOOL
    
      OB_PROP_DEVICE_USB3_REPEAT_IDENTIFY_BOOL
    
      OB_PROP_DEVICE_REBOOT_DELAY_INT
    
      OB_PROP_LASER_OVERCURRENT_PROTECTION_STATUS_BOOL
    
      OB_PROP_LASER_PULSE_WIDTH_PROTECTION_STATUS_BOOL
    
      OB_PROP_LASER_ALWAYS_ON_BOOL
    
      OB_PROP_LASER_ON_OFF_PATTERN_INT
    
      OB_PROP_DEPTH_UNIT_FLEXIBLE_ADJUSTMENT_FLOAT
    
      OB_PROP_LASER_CONTROL_INT
    
      OB_PROP_IR_BRIGHTNESS_INT
    
      OB_STRUCT_BASELINE_CALIBRATION_PARAM
    
      OB_STRUCT_DEVICE_TEMPERATURE
    
      OB_STRUCT_TOF_EXPOSURE_THRESHOLD_CONTROL
    
      OB_STRUCT_DEVICE_SERIAL_NUMBER
    
      OB_STRUCT_DEVICE_TIME
    
      OB_STRUCT_MULTI_DEVICE_SYNC_CONFIG
    
      OB_STRUCT_RGB_CROP_ROI
    
      OB_STRUCT_DEVICE_IP_ADDR_CONFIG
    
      OB_STRUCT_CURRENT_DEPTH_ALG_MODE
    
      OB_STRUCT_DEPTH_PRECISION_SUPPORT_LIST
    
      OB_STRUCT_DEVICE_STATIC_IP_CONFIG_RECORD
    
      OB_STRUCT_DEPTH_HDR_CONFIG
    
      OB_STRUCT_COLOR_AE_ROI
    
      OB_STRUCT_DEPTH_AE_ROI
    
      OB_STRUCT_ASIC_SERIAL_NUMBER
    
      OB_PROP_COLOR_AUTO_EXPOSURE_BOOL
    
      OB_PROP_COLOR_EXPOSURE_INT
    
      OB_PROP_COLOR_GAIN_INT
    
      OB_PROP_COLOR_AUTO_WHITE_BALANCE_BOOL
    
      OB_PROP_COLOR_WHITE_BALANCE_INT
    
      OB_PROP_COLOR_BRIGHTNESS_INT
    
      OB_PROP_COLOR_SHARPNESS_INT
    
      OB_PROP_COLOR_SHUTTER_INT
    
      OB_PROP_COLOR_SATURATION_INT
    
      OB_PROP_COLOR_CONTRAST_INT
    
      OB_PROP_COLOR_GAMMA_INT
    
      OB_PROP_COLOR_ROLL_INT
    
      OB_PROP_COLOR_AUTO_EXPOSURE_PRIORITY_INT
    
      OB_PROP_COLOR_BACKLIGHT_COMPENSATION_INT
    
      OB_PROP_COLOR_HUE_INT
    
      OB_PROP_COLOR_POWER_LINE_FREQUENCY_INT
    
      OB_PROP_DEPTH_AUTO_EXPOSURE_BOOL
    
      OB_PROP_DEPTH_EXPOSURE_INT
    
      OB_PROP_DEPTH_GAIN_INT
    
      OB_PROP_IR_AUTO_EXPOSURE_BOOL
    
      OB_PROP_IR_EXPOSURE_INT
    
      OB_PROP_IR_GAIN_INT
    
      OB_PROP_IR_CHANNEL_DATA_SOURCE_INT
    
      OB_PROP_DEPTH_RM_FILTER_BOOL
    
      OB_PROP_COLOR_MAXIMAL_GAIN_INT
    
      OB_PROP_COLOR_MAXIMAL_SHUTTER_INT
    
      OB_PROP_IR_SHORT_EXPOSURE_BOOL
    
      OB_PROP_COLOR_HDR_BOOL
    
      OB_PROP_IR_LONG_EXPOSURE_BOOL
    
      OB_PROP_SKIP_FRAME_BOOL
    
      OB_PROP_HDR_MERGE_BOOL
    
      OB_PROP_COLOR_FOCUS_INT
    
      OB_PROP_SDK_DISPARITY_TO_DEPTH_BOOL
    
      OB_PROP_SDK_DEPTH_FRAME_UNPACK_BOOL
    
      OB_PROP_SDK_IR_FRAME_UNPACK_BOOL
    
      OB_PROP_SDK_ACCEL_FRAME_TRANSFORMED_BOOL
    
      OB_PROP_SDK_GYRO_FRAME_TRANSFORMED_BOOL
    
      OB_PROP_SDK_IR_LEFT_FRAME_UNPACK_BOOL
    
      OB_PROP_SDK_IR_RIGHT_FRAME_UNPACK_BOOL
    
      OB_RAW_DATA_CAMERA_CALIB_JSON_FILE : Calibration JSON file read from device (Femto Mega, read only)
    """
    OB_PROP_ANTI_COLLUSION_ACTIVATION_STATUS_BOOL: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_ANTI_COLLUSION_ACTIVATION_STATUS_BOOL: 64>
    OB_PROP_BOOT_INTO_RECOVERY_MODE_BOOL: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_BOOT_INTO_RECOVERY_MODE_BOOL: 132>
    OB_PROP_BRT_BOOL: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_BRT_BOOL: 86>
    OB_PROP_CAPTURE_IMAGE_FRAME_NUMBER_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_CAPTURE_IMAGE_FRAME_NUMBER_INT: 113>
    OB_PROP_CAPTURE_IMAGE_NUMBER_INTERVAL_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_CAPTURE_IMAGE_NUMBER_INTERVAL_INT: 136>
    OB_PROP_CAPTURE_IMAGE_SIGNAL_BOOL: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_CAPTURE_IMAGE_SIGNAL_BOOL: 107>
    OB_PROP_CAPTURE_IMAGE_TIME_INTERVAL_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_CAPTURE_IMAGE_TIME_INTERVAL_INT: 135>
    OB_PROP_CAPTURE_INTERVAL_MODE_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_CAPTURE_INTERVAL_MODE_INT: 134>
    OB_PROP_COLOR_AUTO_EXPOSURE_BOOL: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_COLOR_AUTO_EXPOSURE_BOOL: 2000>
    OB_PROP_COLOR_AUTO_EXPOSURE_PRIORITY_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_COLOR_AUTO_EXPOSURE_PRIORITY_INT: 2012>
    OB_PROP_COLOR_AUTO_WHITE_BALANCE_BOOL: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_COLOR_AUTO_WHITE_BALANCE_BOOL: 2003>
    OB_PROP_COLOR_BACKLIGHT_COMPENSATION_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_COLOR_BACKLIGHT_COMPENSATION_INT: 2013>
    OB_PROP_COLOR_BRIGHTNESS_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_COLOR_BRIGHTNESS_INT: 2005>
    OB_PROP_COLOR_CONTRAST_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_COLOR_CONTRAST_INT: 2009>
    OB_PROP_COLOR_EXPOSURE_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_COLOR_EXPOSURE_INT: 2001>
    OB_PROP_COLOR_FLIP_BOOL: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_COLOR_FLIP_BOOL: 82>
    OB_PROP_COLOR_FOCUS_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_COLOR_FOCUS_INT: 2038>
    OB_PROP_COLOR_GAIN_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_COLOR_GAIN_INT: 2002>
    OB_PROP_COLOR_GAMMA_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_COLOR_GAMMA_INT: 2010>
    OB_PROP_COLOR_HDR_BOOL: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_COLOR_HDR_BOOL: 2034>
    OB_PROP_COLOR_HUE_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_COLOR_HUE_INT: 2014>
    OB_PROP_COLOR_MAXIMAL_GAIN_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_COLOR_MAXIMAL_GAIN_INT: 2030>
    OB_PROP_COLOR_MAXIMAL_SHUTTER_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_COLOR_MAXIMAL_SHUTTER_INT: 2031>
    OB_PROP_COLOR_MIRROR_BOOL: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_COLOR_MIRROR_BOOL: 81>
    OB_PROP_COLOR_POWER_LINE_FREQUENCY_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_COLOR_POWER_LINE_FREQUENCY_INT: 2015>
    OB_PROP_COLOR_ROLL_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_COLOR_ROLL_INT: 2011>
    OB_PROP_COLOR_ROTATE_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_COLOR_ROTATE_INT: 115>
    OB_PROP_COLOR_SATURATION_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_COLOR_SATURATION_INT: 2008>
    OB_PROP_COLOR_SHARPNESS_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_COLOR_SHARPNESS_INT: 2006>
    OB_PROP_COLOR_SHUTTER_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_COLOR_SHUTTER_INT: 2007>
    OB_PROP_COLOR_WHITE_BALANCE_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_COLOR_WHITE_BALANCE_INT: 2004>
    OB_PROP_D2C_PREPROCESS_BOOL: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_D2C_PREPROCESS_BOOL: 91>
    OB_PROP_DC_POWER_STATE_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_DC_POWER_STATE_INT: 122>
    OB_PROP_DEPTH_ALIGN_HARDWARE_BOOL: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_DEPTH_ALIGN_HARDWARE_BOOL: 42>
    OB_PROP_DEPTH_ALIGN_HARDWARE_MODE_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_DEPTH_ALIGN_HARDWARE_MODE_INT: 63>
    OB_PROP_DEPTH_AUTO_EXPOSURE_BOOL: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_DEPTH_AUTO_EXPOSURE_BOOL: 2016>
    OB_PROP_DEPTH_CROPPING_MODE_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_DEPTH_CROPPING_MODE_INT: 90>
    OB_PROP_DEPTH_EXPOSURE_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_DEPTH_EXPOSURE_INT: 2017>
    OB_PROP_DEPTH_FLIP_BOOL: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_DEPTH_FLIP_BOOL: 15>
    OB_PROP_DEPTH_GAIN_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_DEPTH_GAIN_INT: 2018>
    OB_PROP_DEPTH_HOLEFILTER_BOOL: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_DEPTH_HOLEFILTER_BOOL: 17>
    OB_PROP_DEPTH_MAX_DIFF_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_DEPTH_MAX_DIFF_INT: 40>
    OB_PROP_DEPTH_MAX_SPECKLE_SIZE_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_DEPTH_MAX_SPECKLE_SIZE_INT: 41>
    OB_PROP_DEPTH_MIRROR_BOOL: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_DEPTH_MIRROR_BOOL: 14>
    OB_PROP_DEPTH_POSTFILTER_BOOL: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_DEPTH_POSTFILTER_BOOL: 16>
    OB_PROP_DEPTH_PRECISION_LEVEL_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_DEPTH_PRECISION_LEVEL_INT: 75>
    OB_PROP_DEPTH_RM_FILTER_BOOL: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_DEPTH_RM_FILTER_BOOL: 2029>
    OB_PROP_DEPTH_ROTATE_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_DEPTH_ROTATE_INT: 118>
    OB_PROP_DEPTH_SOFT_FILTER_BOOL: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_DEPTH_SOFT_FILTER_BOOL: 24>
    OB_PROP_DEPTH_UNIT_FLEXIBLE_ADJUSTMENT_FLOAT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_DEPTH_UNIT_FLEXIBLE_ADJUSTMENT_FLOAT: 176>
    OB_PROP_DEVICE_COMMUNICATION_TYPE_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_DEVICE_COMMUNICATION_TYPE_INT: 97>
    OB_PROP_DEVICE_DEVELOPMENT_MODE_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_DEVICE_DEVELOPMENT_MODE_INT: 129>
    OB_PROP_DEVICE_IN_RECOVERY_MODE_BOOL: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_DEVICE_IN_RECOVERY_MODE_BOOL: 133>
    OB_PROP_DEVICE_REBOOT_DELAY_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_DEVICE_REBOOT_DELAY_INT: 142>
    OB_PROP_DEVICE_USB3_REPEAT_IDENTIFY_BOOL: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_DEVICE_USB3_REPEAT_IDENTIFY_BOOL: 141>
    OB_PROP_DEVICE_WORK_MODE_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_DEVICE_WORK_MODE_INT: 95>
    OB_PROP_DISPARITY_TO_DEPTH_BOOL: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_DISPARITY_TO_DEPTH_BOOL: 85>
    OB_PROP_EXTERNAL_SIGNAL_RESET_BOOL: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_EXTERNAL_SIGNAL_RESET_BOOL: 88>
    OB_PROP_FAN_WORK_MODE_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_FAN_WORK_MODE_INT: 62>
    OB_PROP_FLOOD_BOOL: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_FLOOD_BOOL: 6>
    OB_PROP_FLOOD_LEVEL_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_FLOOD_LEVEL_INT: 7>
    OB_PROP_HARDWARE_DISTORTION_SWITCH_BOOL: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_HARDWARE_DISTORTION_SWITCH_BOOL: 61>
    OB_PROP_HDR_MERGE_BOOL: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_HDR_MERGE_BOOL: 2037>
    OB_PROP_HEARTBEAT_BOOL: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_HEARTBEAT_BOOL: 89>
    OB_PROP_INDICATOR_LIGHT_BOOL: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_INDICATOR_LIGHT_BOOL: 83>
    OB_PROP_IR_AUTO_EXPOSURE_BOOL: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_IR_AUTO_EXPOSURE_BOOL: 2025>
    OB_PROP_IR_BRIGHTNESS_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_IR_BRIGHTNESS_INT: 184>
    OB_PROP_IR_CHANNEL_DATA_SOURCE_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_IR_CHANNEL_DATA_SOURCE_INT: 2028>
    OB_PROP_IR_EXPOSURE_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_IR_EXPOSURE_INT: 2026>
    OB_PROP_IR_FLIP_BOOL: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_IR_FLIP_BOOL: 19>
    OB_PROP_IR_GAIN_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_IR_GAIN_INT: 2027>
    OB_PROP_IR_LONG_EXPOSURE_BOOL: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_IR_LONG_EXPOSURE_BOOL: 2035>
    OB_PROP_IR_MIRROR_BOOL: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_IR_MIRROR_BOOL: 18>
    OB_PROP_IR_RIGHT_FLIP_BOOL: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_IR_RIGHT_FLIP_BOOL: 114>
    OB_PROP_IR_RIGHT_MIRROR_BOOL: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_IR_RIGHT_MIRROR_BOOL: 112>
    OB_PROP_IR_RIGHT_ROTATE_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_IR_RIGHT_ROTATE_INT: 117>
    OB_PROP_IR_ROTATE_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_IR_ROTATE_INT: 116>
    OB_PROP_IR_SHORT_EXPOSURE_BOOL: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_IR_SHORT_EXPOSURE_BOOL: 2032>
    OB_PROP_LASER_ALWAYS_ON_BOOL: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_LASER_ALWAYS_ON_BOOL: 174>
    OB_PROP_LASER_BOOL: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_LASER_BOOL: 3>
    OB_PROP_LASER_CONTROL_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_LASER_CONTROL_INT: 182>
    OB_PROP_LASER_CURRENT_FLOAT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_LASER_CURRENT_FLOAT: 5>
    OB_PROP_LASER_ENERGY_LEVEL_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_LASER_POWER_LEVEL_CONTROL_INT: 99>
    OB_PROP_LASER_HW_ENERGY_LEVEL_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_LASER_HW_ENERGY_LEVEL_INT: 119>
    OB_PROP_LASER_MODE_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_LASER_MODE_INT: 79>
    OB_PROP_LASER_ON_OFF_PATTERN_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_LASER_ON_OFF_PATTERN_INT: 175>
    OB_PROP_LASER_OVERCURRENT_PROTECTION_STATUS_BOOL: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_LASER_OVERCURRENT_PROTECTION_STATUS_BOOL: 148>
    OB_PROP_LASER_POWER_LEVEL_CONTROL_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_LASER_POWER_LEVEL_CONTROL_INT: 99>
    OB_PROP_LASER_PULSE_WIDTH_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_LASER_PULSE_WIDTH_INT: 4>
    OB_PROP_LASER_PULSE_WIDTH_PROTECTION_STATUS_BOOL: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_LASER_PULSE_WIDTH_PROTECTION_STATUS_BOOL: 149>
    OB_PROP_LDP_BOOL: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_LDP_BOOL: 2>
    OB_PROP_LDP_MEASURE_DISTANCE_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_LDP_MEASURE_DISTANCE_INT: 100>
    OB_PROP_LDP_STATUS_BOOL: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_LDP_STATUS_BOOL: 32>
    OB_PROP_MAX_DEPTH_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_MAX_DEPTH_INT: 23>
    OB_PROP_MIN_DEPTH_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_MIN_DEPTH_INT: 22>
    OB_PROP_RECTIFY2_BOOL: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_RECTIFY2_BOOL: 80>
    OB_PROP_RESTORE_FACTORY_SETTINGS_BOOL: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_RESTORE_FACTORY_SETTINGS_BOOL: 131>
    OB_PROP_RGB_CUSTOM_CROP_BOOL: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_RGB_CUSTOM_CROP_BOOL: 94>
    OB_PROP_SDK_ACCEL_FRAME_TRANSFORMED_BOOL: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_SDK_ACCEL_FRAME_TRANSFORMED_BOOL: 3009>
    OB_PROP_SDK_DEPTH_FRAME_UNPACK_BOOL: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_SDK_DEPTH_FRAME_UNPACK_BOOL: 3007>
    OB_PROP_SDK_DISPARITY_TO_DEPTH_BOOL: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_SDK_DISPARITY_TO_DEPTH_BOOL: 3004>
    OB_PROP_SDK_GYRO_FRAME_TRANSFORMED_BOOL: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_SDK_GYRO_FRAME_TRANSFORMED_BOOL: 3010>
    OB_PROP_SDK_IR_FRAME_UNPACK_BOOL: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_SDK_IR_FRAME_UNPACK_BOOL: 3008>
    OB_PROP_SDK_IR_LEFT_FRAME_UNPACK_BOOL: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_SDK_IR_LEFT_FRAME_UNPACK_BOOL: 3011>
    OB_PROP_SDK_IR_RIGHT_FRAME_UNPACK_BOOL: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_SDK_IR_RIGHT_FRAME_UNPACK_BOOL: 3012>
    OB_PROP_SKIP_FRAME_BOOL: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_SKIP_FRAME_BOOL: 2036>
    OB_PROP_SWITCH_IR_MODE_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_SWITCH_IR_MODE_INT: 98>
    OB_PROP_SYNC_SIGNAL_TRIGGER_OUT_BOOL: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_SYNC_SIGNAL_TRIGGER_OUT_BOOL: 130>
    OB_PROP_TIMER_RESET_DELAY_US_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_TIMER_RESET_DELAY_US_INT: 106>
    OB_PROP_TIMER_RESET_ENABLE_BOOL: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_TIMER_RESET_ENABLE_BOOL: 140>
    OB_PROP_TIMER_RESET_SIGNAL_BOOL: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_TIMER_RESET_SIGNAL_BOOL: 104>
    OB_PROP_TIMER_RESET_TRIGGER_OUT_ENABLE_BOOL: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_TIMER_RESET_TRIGGER_OUT_ENABLE_BOOL: 105>
    OB_PROP_TIMESTAMP_OFFSET_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_TIMESTAMP_OFFSET_INT: 43>
    OB_PROP_TOF_FILTER_RANGE_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_TOF_FILTER_RANGE_INT: 76>
    OB_PROP_USB_POWER_STATE_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_USB_POWER_STATE_INT: 121>
    OB_PROP_WATCHDOG_BOOL: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_WATCHDOG_BOOL: 87>
    OB_RAW_DATA_CAMERA_CALIB_JSON_FILE: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_RAW_DATA_CAMERA_CALIB_JSON_FILE: 4029>
    OB_STRUCT_ASIC_SERIAL_NUMBER: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_STRUCT_ASIC_SERIAL_NUMBER: 1063>
    OB_STRUCT_BASELINE_CALIBRATION_PARAM: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_STRUCT_BASELINE_CALIBRATION_PARAM: 1002>
    OB_STRUCT_COLOR_AE_ROI: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_STRUCT_COLOR_AE_ROI: 1060>
    OB_STRUCT_CURRENT_DEPTH_ALG_MODE: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_STRUCT_CURRENT_DEPTH_ALG_MODE: 1043>
    OB_STRUCT_DEPTH_AE_ROI: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_STRUCT_DEPTH_AE_ROI: 1061>
    OB_STRUCT_DEPTH_HDR_CONFIG: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_STRUCT_DEPTH_HDR_CONFIG: 1059>
    OB_STRUCT_DEPTH_PRECISION_SUPPORT_LIST: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_STRUCT_DEPTH_PRECISION_SUPPORT_LIST: 1045>
    OB_STRUCT_DEVICE_IP_ADDR_CONFIG: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_STRUCT_DEVICE_IP_ADDR_CONFIG: 1041>
    OB_STRUCT_DEVICE_SERIAL_NUMBER: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_STRUCT_DEVICE_SERIAL_NUMBER: 1035>
    OB_STRUCT_DEVICE_STATIC_IP_CONFIG_RECORD: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_STRUCT_DEVICE_STATIC_IP_CONFIG_RECORD: 1053>
    OB_STRUCT_DEVICE_TEMPERATURE: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_STRUCT_DEVICE_TEMPERATURE: 1003>
    OB_STRUCT_DEVICE_TIME: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_STRUCT_DEVICE_TIME: 1037>
    OB_STRUCT_MULTI_DEVICE_SYNC_CONFIG: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_STRUCT_MULTI_DEVICE_SYNC_CONFIG: 1038>
    OB_STRUCT_RGB_CROP_ROI: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_STRUCT_RGB_CROP_ROI: 1040>
    OB_STRUCT_TOF_EXPOSURE_THRESHOLD_CONTROL: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_STRUCT_TOF_EXPOSURE_THRESHOLD_CONTROL: 1024>
    __members__: typing.ClassVar[dict[str, OBPropertyID]]  # value = {'OB_PROP_LDP_BOOL': <OBPropertyID.OB_PROP_LDP_BOOL: 2>, 'OB_PROP_LASER_BOOL': <OBPropertyID.OB_PROP_LASER_BOOL: 3>, 'OB_PROP_LASER_PULSE_WIDTH_INT': <OBPropertyID.OB_PROP_LASER_PULSE_WIDTH_INT: 4>, 'OB_PROP_LASER_CURRENT_FLOAT': <OBPropertyID.OB_PROP_LASER_CURRENT_FLOAT: 5>, 'OB_PROP_FLOOD_BOOL': <OBPropertyID.OB_PROP_FLOOD_BOOL: 6>, 'OB_PROP_FLOOD_LEVEL_INT': <OBPropertyID.OB_PROP_FLOOD_LEVEL_INT: 7>, 'OB_PROP_DEPTH_MIRROR_BOOL': <OBPropertyID.OB_PROP_DEPTH_MIRROR_BOOL: 14>, 'OB_PROP_DEPTH_FLIP_BOOL': <OBPropertyID.OB_PROP_DEPTH_FLIP_BOOL: 15>, 'OB_PROP_DEPTH_POSTFILTER_BOOL': <OBPropertyID.OB_PROP_DEPTH_POSTFILTER_BOOL: 16>, 'OB_PROP_DEPTH_HOLEFILTER_BOOL': <OBPropertyID.OB_PROP_DEPTH_HOLEFILTER_BOOL: 17>, 'OB_PROP_IR_MIRROR_BOOL': <OBPropertyID.OB_PROP_IR_MIRROR_BOOL: 18>, 'OB_PROP_IR_FLIP_BOOL': <OBPropertyID.OB_PROP_IR_FLIP_BOOL: 19>, 'OB_PROP_MIN_DEPTH_INT': <OBPropertyID.OB_PROP_MIN_DEPTH_INT: 22>, 'OB_PROP_MAX_DEPTH_INT': <OBPropertyID.OB_PROP_MAX_DEPTH_INT: 23>, 'OB_PROP_DEPTH_SOFT_FILTER_BOOL': <OBPropertyID.OB_PROP_DEPTH_SOFT_FILTER_BOOL: 24>, 'OB_PROP_LDP_STATUS_BOOL': <OBPropertyID.OB_PROP_LDP_STATUS_BOOL: 32>, 'OB_PROP_DEPTH_MAX_DIFF_INT': <OBPropertyID.OB_PROP_DEPTH_MAX_DIFF_INT: 40>, 'OB_PROP_DEPTH_MAX_SPECKLE_SIZE_INT': <OBPropertyID.OB_PROP_DEPTH_MAX_SPECKLE_SIZE_INT: 41>, 'OB_PROP_DEPTH_ALIGN_HARDWARE_BOOL': <OBPropertyID.OB_PROP_DEPTH_ALIGN_HARDWARE_BOOL: 42>, 'OB_PROP_TIMESTAMP_OFFSET_INT': <OBPropertyID.OB_PROP_TIMESTAMP_OFFSET_INT: 43>, 'OB_PROP_HARDWARE_DISTORTION_SWITCH_BOOL': <OBPropertyID.OB_PROP_HARDWARE_DISTORTION_SWITCH_BOOL: 61>, 'OB_PROP_FAN_WORK_MODE_INT': <OBPropertyID.OB_PROP_FAN_WORK_MODE_INT: 62>, 'OB_PROP_DEPTH_ALIGN_HARDWARE_MODE_INT': <OBPropertyID.OB_PROP_DEPTH_ALIGN_HARDWARE_MODE_INT: 63>, 'OB_PROP_ANTI_COLLUSION_ACTIVATION_STATUS_BOOL': <OBPropertyID.OB_PROP_ANTI_COLLUSION_ACTIVATION_STATUS_BOOL: 64>, 'OB_PROP_DEPTH_PRECISION_LEVEL_INT': <OBPropertyID.OB_PROP_DEPTH_PRECISION_LEVEL_INT: 75>, 'OB_PROP_TOF_FILTER_RANGE_INT': <OBPropertyID.OB_PROP_TOF_FILTER_RANGE_INT: 76>, 'OB_PROP_LASER_MODE_INT': <OBPropertyID.OB_PROP_LASER_MODE_INT: 79>, 'OB_PROP_RECTIFY2_BOOL': <OBPropertyID.OB_PROP_RECTIFY2_BOOL: 80>, 'OB_PROP_COLOR_MIRROR_BOOL': <OBPropertyID.OB_PROP_COLOR_MIRROR_BOOL: 81>, 'OB_PROP_COLOR_FLIP_BOOL': <OBPropertyID.OB_PROP_COLOR_FLIP_BOOL: 82>, 'OB_PROP_INDICATOR_LIGHT_BOOL': <OBPropertyID.OB_PROP_INDICATOR_LIGHT_BOOL: 83>, 'OB_PROP_DISPARITY_TO_DEPTH_BOOL': <OBPropertyID.OB_PROP_DISPARITY_TO_DEPTH_BOOL: 85>, 'OB_PROP_BRT_BOOL': <OBPropertyID.OB_PROP_BRT_BOOL: 86>, 'OB_PROP_WATCHDOG_BOOL': <OBPropertyID.OB_PROP_WATCHDOG_BOOL: 87>, 'OB_PROP_EXTERNAL_SIGNAL_RESET_BOOL': <OBPropertyID.OB_PROP_EXTERNAL_SIGNAL_RESET_BOOL: 88>, 'OB_PROP_HEARTBEAT_BOOL': <OBPropertyID.OB_PROP_HEARTBEAT_BOOL: 89>, 'OB_PROP_DEPTH_CROPPING_MODE_INT': <OBPropertyID.OB_PROP_DEPTH_CROPPING_MODE_INT: 90>, 'OB_PROP_D2C_PREPROCESS_BOOL': <OBPropertyID.OB_PROP_D2C_PREPROCESS_BOOL: 91>, 'OB_PROP_RGB_CUSTOM_CROP_BOOL': <OBPropertyID.OB_PROP_RGB_CUSTOM_CROP_BOOL: 94>, 'OB_PROP_DEVICE_WORK_MODE_INT': <OBPropertyID.OB_PROP_DEVICE_WORK_MODE_INT: 95>, 'OB_PROP_DEVICE_COMMUNICATION_TYPE_INT': <OBPropertyID.OB_PROP_DEVICE_COMMUNICATION_TYPE_INT: 97>, 'OB_PROP_SWITCH_IR_MODE_INT': <OBPropertyID.OB_PROP_SWITCH_IR_MODE_INT: 98>, 'OB_PROP_LASER_POWER_LEVEL_CONTROL_INT': <OBPropertyID.OB_PROP_LASER_POWER_LEVEL_CONTROL_INT: 99>, 'OB_PROP_LASER_ENERGY_LEVEL_INT': <OBPropertyID.OB_PROP_LASER_POWER_LEVEL_CONTROL_INT: 99>, 'OB_PROP_LDP_MEASURE_DISTANCE_INT': <OBPropertyID.OB_PROP_LDP_MEASURE_DISTANCE_INT: 100>, 'OB_PROP_TIMER_RESET_SIGNAL_BOOL': <OBPropertyID.OB_PROP_TIMER_RESET_SIGNAL_BOOL: 104>, 'OB_PROP_TIMER_RESET_TRIGGER_OUT_ENABLE_BOOL': <OBPropertyID.OB_PROP_TIMER_RESET_TRIGGER_OUT_ENABLE_BOOL: 105>, 'OB_PROP_TIMER_RESET_DELAY_US_INT': <OBPropertyID.OB_PROP_TIMER_RESET_DELAY_US_INT: 106>, 'OB_PROP_CAPTURE_IMAGE_SIGNAL_BOOL': <OBPropertyID.OB_PROP_CAPTURE_IMAGE_SIGNAL_BOOL: 107>, 'OB_PROP_IR_RIGHT_MIRROR_BOOL': <OBPropertyID.OB_PROP_IR_RIGHT_MIRROR_BOOL: 112>, 'OB_PROP_CAPTURE_IMAGE_FRAME_NUMBER_INT': <OBPropertyID.OB_PROP_CAPTURE_IMAGE_FRAME_NUMBER_INT: 113>, 'OB_PROP_IR_RIGHT_FLIP_BOOL': <OBPropertyID.OB_PROP_IR_RIGHT_FLIP_BOOL: 114>, 'OB_PROP_COLOR_ROTATE_INT': <OBPropertyID.OB_PROP_COLOR_ROTATE_INT: 115>, 'OB_PROP_IR_ROTATE_INT': <OBPropertyID.OB_PROP_IR_ROTATE_INT: 116>, 'OB_PROP_IR_RIGHT_ROTATE_INT': <OBPropertyID.OB_PROP_IR_RIGHT_ROTATE_INT: 117>, 'OB_PROP_DEPTH_ROTATE_INT': <OBPropertyID.OB_PROP_DEPTH_ROTATE_INT: 118>, 'OB_PROP_LASER_HW_ENERGY_LEVEL_INT': <OBPropertyID.OB_PROP_LASER_HW_ENERGY_LEVEL_INT: 119>, 'OB_PROP_USB_POWER_STATE_INT': <OBPropertyID.OB_PROP_USB_POWER_STATE_INT: 121>, 'OB_PROP_DC_POWER_STATE_INT': <OBPropertyID.OB_PROP_DC_POWER_STATE_INT: 122>, 'OB_PROP_DEVICE_DEVELOPMENT_MODE_INT': <OBPropertyID.OB_PROP_DEVICE_DEVELOPMENT_MODE_INT: 129>, 'OB_PROP_SYNC_SIGNAL_TRIGGER_OUT_BOOL': <OBPropertyID.OB_PROP_SYNC_SIGNAL_TRIGGER_OUT_BOOL: 130>, 'OB_PROP_RESTORE_FACTORY_SETTINGS_BOOL': <OBPropertyID.OB_PROP_RESTORE_FACTORY_SETTINGS_BOOL: 131>, 'OB_PROP_BOOT_INTO_RECOVERY_MODE_BOOL': <OBPropertyID.OB_PROP_BOOT_INTO_RECOVERY_MODE_BOOL: 132>, 'OB_PROP_DEVICE_IN_RECOVERY_MODE_BOOL': <OBPropertyID.OB_PROP_DEVICE_IN_RECOVERY_MODE_BOOL: 133>, 'OB_PROP_CAPTURE_INTERVAL_MODE_INT': <OBPropertyID.OB_PROP_CAPTURE_INTERVAL_MODE_INT: 134>, 'OB_PROP_CAPTURE_IMAGE_TIME_INTERVAL_INT': <OBPropertyID.OB_PROP_CAPTURE_IMAGE_TIME_INTERVAL_INT: 135>, 'OB_PROP_CAPTURE_IMAGE_NUMBER_INTERVAL_INT': <OBPropertyID.OB_PROP_CAPTURE_IMAGE_NUMBER_INTERVAL_INT: 136>, 'OB_PROP_TIMER_RESET_ENABLE_BOOL': <OBPropertyID.OB_PROP_TIMER_RESET_ENABLE_BOOL: 140>, 'OB_PROP_DEVICE_USB3_REPEAT_IDENTIFY_BOOL': <OBPropertyID.OB_PROP_DEVICE_USB3_REPEAT_IDENTIFY_BOOL: 141>, 'OB_PROP_DEVICE_REBOOT_DELAY_INT': <OBPropertyID.OB_PROP_DEVICE_REBOOT_DELAY_INT: 142>, 'OB_PROP_LASER_OVERCURRENT_PROTECTION_STATUS_BOOL': <OBPropertyID.OB_PROP_LASER_OVERCURRENT_PROTECTION_STATUS_BOOL: 148>, 'OB_PROP_LASER_PULSE_WIDTH_PROTECTION_STATUS_BOOL': <OBPropertyID.OB_PROP_LASER_PULSE_WIDTH_PROTECTION_STATUS_BOOL: 149>, 'OB_PROP_LASER_ALWAYS_ON_BOOL': <OBPropertyID.OB_PROP_LASER_ALWAYS_ON_BOOL: 174>, 'OB_PROP_LASER_ON_OFF_PATTERN_INT': <OBPropertyID.OB_PROP_LASER_ON_OFF_PATTERN_INT: 175>, 'OB_PROP_DEPTH_UNIT_FLEXIBLE_ADJUSTMENT_FLOAT': <OBPropertyID.OB_PROP_DEPTH_UNIT_FLEXIBLE_ADJUSTMENT_FLOAT: 176>, 'OB_PROP_LASER_CONTROL_INT': <OBPropertyID.OB_PROP_LASER_CONTROL_INT: 182>, 'OB_PROP_IR_BRIGHTNESS_INT': <OBPropertyID.OB_PROP_IR_BRIGHTNESS_INT: 184>, 'OB_STRUCT_BASELINE_CALIBRATION_PARAM': <OBPropertyID.OB_STRUCT_BASELINE_CALIBRATION_PARAM: 1002>, 'OB_STRUCT_DEVICE_TEMPERATURE': <OBPropertyID.OB_STRUCT_DEVICE_TEMPERATURE: 1003>, 'OB_STRUCT_TOF_EXPOSURE_THRESHOLD_CONTROL': <OBPropertyID.OB_STRUCT_TOF_EXPOSURE_THRESHOLD_CONTROL: 1024>, 'OB_STRUCT_DEVICE_SERIAL_NUMBER': <OBPropertyID.OB_STRUCT_DEVICE_SERIAL_NUMBER: 1035>, 'OB_STRUCT_DEVICE_TIME': <OBPropertyID.OB_STRUCT_DEVICE_TIME: 1037>, 'OB_STRUCT_MULTI_DEVICE_SYNC_CONFIG': <OBPropertyID.OB_STRUCT_MULTI_DEVICE_SYNC_CONFIG: 1038>, 'OB_STRUCT_RGB_CROP_ROI': <OBPropertyID.OB_STRUCT_RGB_CROP_ROI: 1040>, 'OB_STRUCT_DEVICE_IP_ADDR_CONFIG': <OBPropertyID.OB_STRUCT_DEVICE_IP_ADDR_CONFIG: 1041>, 'OB_STRUCT_CURRENT_DEPTH_ALG_MODE': <OBPropertyID.OB_STRUCT_CURRENT_DEPTH_ALG_MODE: 1043>, 'OB_STRUCT_DEPTH_PRECISION_SUPPORT_LIST': <OBPropertyID.OB_STRUCT_DEPTH_PRECISION_SUPPORT_LIST: 1045>, 'OB_STRUCT_DEVICE_STATIC_IP_CONFIG_RECORD': <OBPropertyID.OB_STRUCT_DEVICE_STATIC_IP_CONFIG_RECORD: 1053>, 'OB_STRUCT_DEPTH_HDR_CONFIG': <OBPropertyID.OB_STRUCT_DEPTH_HDR_CONFIG: 1059>, 'OB_STRUCT_COLOR_AE_ROI': <OBPropertyID.OB_STRUCT_COLOR_AE_ROI: 1060>, 'OB_STRUCT_DEPTH_AE_ROI': <OBPropertyID.OB_STRUCT_DEPTH_AE_ROI: 1061>, 'OB_STRUCT_ASIC_SERIAL_NUMBER': <OBPropertyID.OB_STRUCT_ASIC_SERIAL_NUMBER: 1063>, 'OB_PROP_COLOR_AUTO_EXPOSURE_BOOL': <OBPropertyID.OB_PROP_COLOR_AUTO_EXPOSURE_BOOL: 2000>, 'OB_PROP_COLOR_EXPOSURE_INT': <OBPropertyID.OB_PROP_COLOR_EXPOSURE_INT: 2001>, 'OB_PROP_COLOR_GAIN_INT': <OBPropertyID.OB_PROP_COLOR_GAIN_INT: 2002>, 'OB_PROP_COLOR_AUTO_WHITE_BALANCE_BOOL': <OBPropertyID.OB_PROP_COLOR_AUTO_WHITE_BALANCE_BOOL: 2003>, 'OB_PROP_COLOR_WHITE_BALANCE_INT': <OBPropertyID.OB_PROP_COLOR_WHITE_BALANCE_INT: 2004>, 'OB_PROP_COLOR_BRIGHTNESS_INT': <OBPropertyID.OB_PROP_COLOR_BRIGHTNESS_INT: 2005>, 'OB_PROP_COLOR_SHARPNESS_INT': <OBPropertyID.OB_PROP_COLOR_SHARPNESS_INT: 2006>, 'OB_PROP_COLOR_SHUTTER_INT': <OBPropertyID.OB_PROP_COLOR_SHUTTER_INT: 2007>, 'OB_PROP_COLOR_SATURATION_INT': <OBPropertyID.OB_PROP_COLOR_SATURATION_INT: 2008>, 'OB_PROP_COLOR_CONTRAST_INT': <OBPropertyID.OB_PROP_COLOR_CONTRAST_INT: 2009>, 'OB_PROP_COLOR_GAMMA_INT': <OBPropertyID.OB_PROP_COLOR_GAMMA_INT: 2010>, 'OB_PROP_COLOR_ROLL_INT': <OBPropertyID.OB_PROP_COLOR_ROLL_INT: 2011>, 'OB_PROP_COLOR_AUTO_EXPOSURE_PRIORITY_INT': <OBPropertyID.OB_PROP_COLOR_AUTO_EXPOSURE_PRIORITY_INT: 2012>, 'OB_PROP_COLOR_BACKLIGHT_COMPENSATION_INT': <OBPropertyID.OB_PROP_COLOR_BACKLIGHT_COMPENSATION_INT: 2013>, 'OB_PROP_COLOR_HUE_INT': <OBPropertyID.OB_PROP_COLOR_HUE_INT: 2014>, 'OB_PROP_COLOR_POWER_LINE_FREQUENCY_INT': <OBPropertyID.OB_PROP_COLOR_POWER_LINE_FREQUENCY_INT: 2015>, 'OB_PROP_DEPTH_AUTO_EXPOSURE_BOOL': <OBPropertyID.OB_PROP_DEPTH_AUTO_EXPOSURE_BOOL: 2016>, 'OB_PROP_DEPTH_EXPOSURE_INT': <OBPropertyID.OB_PROP_DEPTH_EXPOSURE_INT: 2017>, 'OB_PROP_DEPTH_GAIN_INT': <OBPropertyID.OB_PROP_DEPTH_GAIN_INT: 2018>, 'OB_PROP_IR_AUTO_EXPOSURE_BOOL': <OBPropertyID.OB_PROP_IR_AUTO_EXPOSURE_BOOL: 2025>, 'OB_PROP_IR_EXPOSURE_INT': <OBPropertyID.OB_PROP_IR_EXPOSURE_INT: 2026>, 'OB_PROP_IR_GAIN_INT': <OBPropertyID.OB_PROP_IR_GAIN_INT: 2027>, 'OB_PROP_IR_CHANNEL_DATA_SOURCE_INT': <OBPropertyID.OB_PROP_IR_CHANNEL_DATA_SOURCE_INT: 2028>, 'OB_PROP_DEPTH_RM_FILTER_BOOL': <OBPropertyID.OB_PROP_DEPTH_RM_FILTER_BOOL: 2029>, 'OB_PROP_COLOR_MAXIMAL_GAIN_INT': <OBPropertyID.OB_PROP_COLOR_MAXIMAL_GAIN_INT: 2030>, 'OB_PROP_COLOR_MAXIMAL_SHUTTER_INT': <OBPropertyID.OB_PROP_COLOR_MAXIMAL_SHUTTER_INT: 2031>, 'OB_PROP_IR_SHORT_EXPOSURE_BOOL': <OBPropertyID.OB_PROP_IR_SHORT_EXPOSURE_BOOL: 2032>, 'OB_PROP_COLOR_HDR_BOOL': <OBPropertyID.OB_PROP_COLOR_HDR_BOOL: 2034>, 'OB_PROP_IR_LONG_EXPOSURE_BOOL': <OBPropertyID.OB_PROP_IR_LONG_EXPOSURE_BOOL: 2035>, 'OB_PROP_SKIP_FRAME_BOOL': <OBPropertyID.OB_PROP_SKIP_FRAME_BOOL: 2036>, 'OB_PROP_HDR_MERGE_BOOL': <OBPropertyID.OB_PROP_HDR_MERGE_BOOL: 2037>, 'OB_PROP_COLOR_FOCUS_INT': <OBPropertyID.OB_PROP_COLOR_FOCUS_INT: 2038>, 'OB_PROP_SDK_DISPARITY_TO_DEPTH_BOOL': <OBPropertyID.OB_PROP_SDK_DISPARITY_TO_DEPTH_BOOL: 3004>, 'OB_PROP_SDK_DEPTH_FRAME_UNPACK_BOOL': <OBPropertyID.OB_PROP_SDK_DEPTH_FRAME_UNPACK_BOOL: 3007>, 'OB_PROP_SDK_IR_FRAME_UNPACK_BOOL': <OBPropertyID.OB_PROP_SDK_IR_FRAME_UNPACK_BOOL: 3008>, 'OB_PROP_SDK_ACCEL_FRAME_TRANSFORMED_BOOL': <OBPropertyID.OB_PROP_SDK_ACCEL_FRAME_TRANSFORMED_BOOL: 3009>, 'OB_PROP_SDK_GYRO_FRAME_TRANSFORMED_BOOL': <OBPropertyID.OB_PROP_SDK_GYRO_FRAME_TRANSFORMED_BOOL: 3010>, 'OB_PROP_SDK_IR_LEFT_FRAME_UNPACK_BOOL': <OBPropertyID.OB_PROP_SDK_IR_LEFT_FRAME_UNPACK_BOOL: 3011>, 'OB_PROP_SDK_IR_RIGHT_FRAME_UNPACK_BOOL': <OBPropertyID.OB_PROP_SDK_IR_RIGHT_FRAME_UNPACK_BOOL: 3012>, 'OB_RAW_DATA_CAMERA_CALIB_JSON_FILE': <OBPropertyID.OB_RAW_DATA_CAMERA_CALIB_JSON_FILE: 4029>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class OBPropertyItem:
    def __init__(self) -> None:
        ...
    @property
    def id(self) -> OBPropertyID:
        """
        Property ID 
        """
    @id.setter
    def id(self, arg0: OBPropertyID) -> None:
        ...
    @property
    def name(self) -> str:
        """
        Property name
        """
    @name.setter
    def name(self, arg0: str) -> None:
        ...
    @property
    def permission(self) -> OBPermissionType:
        """
        Property permission
        """
    @permission.setter
    def permission(self, arg0: OBPermissionType) -> None:
        ...
    @property
    def type(self) -> OBPropertyType:
        """
        Property type
        """
    @type.setter
    def type(self, arg0: OBPropertyType) -> None:
        ...
class OBPropertyType:
    """
    Members:
    
      OB_BOOL_PROPERTY : Boolean property
    
      OB_INT_PROPERTY : Integer property
    
      OB_FLOAT_PROPERTY : Float property
    
      OB_STRUCT_PROPERTY : Struct property
    """
    OB_BOOL_PROPERTY: typing.ClassVar[OBPropertyType]  # value = <OBPropertyType.OB_BOOL_PROPERTY: 0>
    OB_FLOAT_PROPERTY: typing.ClassVar[OBPropertyType]  # value = <OBPropertyType.OB_FLOAT_PROPERTY: 2>
    OB_INT_PROPERTY: typing.ClassVar[OBPropertyType]  # value = <OBPropertyType.OB_INT_PROPERTY: 1>
    OB_STRUCT_PROPERTY: typing.ClassVar[OBPropertyType]  # value = <OBPropertyType.OB_STRUCT_PROPERTY: 3>
    __members__: typing.ClassVar[dict[str, OBPropertyType]]  # value = {'OB_BOOL_PROPERTY': <OBPropertyType.OB_BOOL_PROPERTY: 0>, 'OB_INT_PROPERTY': <OBPropertyType.OB_INT_PROPERTY: 1>, 'OB_FLOAT_PROPERTY': <OBPropertyType.OB_FLOAT_PROPERTY: 2>, 'OB_STRUCT_PROPERTY': <OBPropertyType.OB_STRUCT_PROPERTY: 3>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class OBProtocolVersion:
    major: int
    minor: int
    patch: int
    def __init__(self) -> None:
        ...
class OBRect:
    height: int
    width: int
    x: int
    y: int
    def __init__(self) -> None:
        ...
class OBRegionOfInterest:
    x0_left: int
    x1_right: int
    y0_top: int
    y1_bottom: int
    def __init__(self) -> None:
        ...
class OBRotateDegreeType:
    """
    Members:
    
      ROTATE_0
    
      ROTATE_90
    
      ROTATE_180
    
      ROTATE_270
    """
    ROTATE_0: typing.ClassVar[OBRotateDegreeType]  # value = <OBRotateDegreeType.ROTATE_0: 0>
    ROTATE_180: typing.ClassVar[OBRotateDegreeType]  # value = <OBRotateDegreeType.ROTATE_180: 180>
    ROTATE_270: typing.ClassVar[OBRotateDegreeType]  # value = <OBRotateDegreeType.ROTATE_270: 270>
    ROTATE_90: typing.ClassVar[OBRotateDegreeType]  # value = <OBRotateDegreeType.ROTATE_90: 90>
    __members__: typing.ClassVar[dict[str, OBRotateDegreeType]]  # value = {'ROTATE_0': <OBRotateDegreeType.ROTATE_0: 0>, 'ROTATE_90': <OBRotateDegreeType.ROTATE_90: 90>, 'ROTATE_180': <OBRotateDegreeType.ROTATE_180: 180>, 'ROTATE_270': <OBRotateDegreeType.ROTATE_270: 270>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class OBSensorType:
    """
    Members:
    
      UNKNOWN_SENSOR
    
      IR_SENSOR
    
      COLOR_SENSOR
    
      DEPTH_SENSOR
    
      ACCEL_SENSOR
    
      GYRO_SENSOR
    
      LEFT_IR_SENSOR
    
      RIGHT_IR_SENSOR
    """
    ACCEL_SENSOR: typing.ClassVar[OBSensorType]  # value = <OBSensorType.ACCEL_SENSOR: 4>
    COLOR_SENSOR: typing.ClassVar[OBSensorType]  # value = <OBSensorType.COLOR_SENSOR: 2>
    DEPTH_SENSOR: typing.ClassVar[OBSensorType]  # value = <OBSensorType.DEPTH_SENSOR: 3>
    GYRO_SENSOR: typing.ClassVar[OBSensorType]  # value = <OBSensorType.GYRO_SENSOR: 5>
    IR_SENSOR: typing.ClassVar[OBSensorType]  # value = <OBSensorType.IR_SENSOR: 1>
    LEFT_IR_SENSOR: typing.ClassVar[OBSensorType]  # value = <OBSensorType.LEFT_IR_SENSOR: 6>
    RIGHT_IR_SENSOR: typing.ClassVar[OBSensorType]  # value = <OBSensorType.RIGHT_IR_SENSOR: 7>
    UNKNOWN_SENSOR: typing.ClassVar[OBSensorType]  # value = <OBSensorType.UNKNOWN_SENSOR: 0>
    __members__: typing.ClassVar[dict[str, OBSensorType]]  # value = {'UNKNOWN_SENSOR': <OBSensorType.UNKNOWN_SENSOR: 0>, 'IR_SENSOR': <OBSensorType.IR_SENSOR: 1>, 'COLOR_SENSOR': <OBSensorType.COLOR_SENSOR: 2>, 'DEPTH_SENSOR': <OBSensorType.DEPTH_SENSOR: 3>, 'ACCEL_SENSOR': <OBSensorType.ACCEL_SENSOR: 4>, 'GYRO_SENSOR': <OBSensorType.GYRO_SENSOR: 5>, 'LEFT_IR_SENSOR': <OBSensorType.LEFT_IR_SENSOR: 6>, 'RIGHT_IR_SENSOR': <OBSensorType.RIGHT_IR_SENSOR: 7>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class OBSequenceIdItem:
    name: str
    sequence_select_id: int
    def __init__(self) -> None:
        ...
class OBSpatialAdvancedFilterParams:
    alpha: float
    disp_diff: int
    magnitude: int
    radius: int
    def __init__(self) -> None:
        ...
    def __repr__(self) -> str:
        ...
class OBStatus:
    """
    Members:
    
      STATUS_OK
    
      STATUS_ERROR
    """
    STATUS_ERROR: typing.ClassVar[OBStatus]  # value = <OBStatus.STATUS_ERROR: 1>
    STATUS_OK: typing.ClassVar[OBStatus]  # value = <OBStatus.STATUS_OK: 0>
    __members__: typing.ClassVar[dict[str, OBStatus]]  # value = {'STATUS_OK': <OBStatus.STATUS_OK: 0>, 'STATUS_ERROR': <OBStatus.STATUS_ERROR: 1>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class OBStreamType:
    """
    Members:
    
      UNKNOWN_STREAM
    
      VIDEO_STREAM
    
      IR_STREAM
    
      COLOR_STREAM
    
      DEPTH_STREAM
    
      ACCEL_STREAM
    
      GYRO_STREAM
    
      LEFT_IR_STREAM
    
      RIGHT_IR_STREAM
    """
    ACCEL_STREAM: typing.ClassVar[OBStreamType]  # value = <OBStreamType.ACCEL_STREAM: 4>
    COLOR_STREAM: typing.ClassVar[OBStreamType]  # value = <OBStreamType.COLOR_STREAM: 2>
    DEPTH_STREAM: typing.ClassVar[OBStreamType]  # value = <OBStreamType.DEPTH_STREAM: 3>
    GYRO_STREAM: typing.ClassVar[OBStreamType]  # value = <OBStreamType.GYRO_STREAM: 5>
    IR_STREAM: typing.ClassVar[OBStreamType]  # value = <OBStreamType.IR_STREAM: 1>
    LEFT_IR_STREAM: typing.ClassVar[OBStreamType]  # value = <OBStreamType.LEFT_IR_STREAM: 6>
    RIGHT_IR_STREAM: typing.ClassVar[OBStreamType]  # value = <OBStreamType.RIGHT_IR_STREAM: 7>
    UNKNOWN_STREAM: typing.ClassVar[OBStreamType]  # value = <OBStreamType.UNKNOWN_STREAM: -1>
    VIDEO_STREAM: typing.ClassVar[OBStreamType]  # value = <OBStreamType.VIDEO_STREAM: 0>
    __members__: typing.ClassVar[dict[str, OBStreamType]]  # value = {'UNKNOWN_STREAM': <OBStreamType.UNKNOWN_STREAM: -1>, 'VIDEO_STREAM': <OBStreamType.VIDEO_STREAM: 0>, 'IR_STREAM': <OBStreamType.IR_STREAM: 1>, 'COLOR_STREAM': <OBStreamType.COLOR_STREAM: 2>, 'DEPTH_STREAM': <OBStreamType.DEPTH_STREAM: 3>, 'ACCEL_STREAM': <OBStreamType.ACCEL_STREAM: 4>, 'GYRO_STREAM': <OBStreamType.GYRO_STREAM: 5>, 'LEFT_IR_STREAM': <OBStreamType.LEFT_IR_STREAM: 6>, 'RIGHT_IR_STREAM': <OBStreamType.RIGHT_IR_STREAM: 7>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class OBSyncMode:
    """
    Members:
    
      CLOSE
    
      STANDALONE
    
      PRIMARY
    
      SECONDARY
    
      PRIMARY_MCU_TRIGGER
    
      PRIMARY_IR_TRIGGER
    
      PRIMARY_SOFT_TRIGGER
    
      SECONDARY_SOFT_TRIGGER
    
      UNKNOWN
    """
    CLOSE: typing.ClassVar[OBSyncMode]  # value = <OBSyncMode.CLOSE: 0>
    PRIMARY: typing.ClassVar[OBSyncMode]  # value = <OBSyncMode.PRIMARY: 2>
    PRIMARY_IR_TRIGGER: typing.ClassVar[OBSyncMode]  # value = <OBSyncMode.PRIMARY_IR_TRIGGER: 5>
    PRIMARY_MCU_TRIGGER: typing.ClassVar[OBSyncMode]  # value = <OBSyncMode.PRIMARY_MCU_TRIGGER: 4>
    PRIMARY_SOFT_TRIGGER: typing.ClassVar[OBSyncMode]  # value = <OBSyncMode.PRIMARY_SOFT_TRIGGER: 6>
    SECONDARY: typing.ClassVar[OBSyncMode]  # value = <OBSyncMode.SECONDARY: 3>
    SECONDARY_SOFT_TRIGGER: typing.ClassVar[OBSyncMode]  # value = <OBSyncMode.SECONDARY_SOFT_TRIGGER: 7>
    STANDALONE: typing.ClassVar[OBSyncMode]  # value = <OBSyncMode.STANDALONE: 1>
    UNKNOWN: typing.ClassVar[OBSyncMode]  # value = <OBSyncMode.UNKNOWN: 255>
    __members__: typing.ClassVar[dict[str, OBSyncMode]]  # value = {'CLOSE': <OBSyncMode.CLOSE: 0>, 'STANDALONE': <OBSyncMode.STANDALONE: 1>, 'PRIMARY': <OBSyncMode.PRIMARY: 2>, 'SECONDARY': <OBSyncMode.SECONDARY: 3>, 'PRIMARY_MCU_TRIGGER': <OBSyncMode.PRIMARY_MCU_TRIGGER: 4>, 'PRIMARY_IR_TRIGGER': <OBSyncMode.PRIMARY_IR_TRIGGER: 5>, 'PRIMARY_SOFT_TRIGGER': <OBSyncMode.PRIMARY_SOFT_TRIGGER: 6>, 'SECONDARY_SOFT_TRIGGER': <OBSyncMode.SECONDARY_SOFT_TRIGGER: 7>, 'UNKNOWN': <OBSyncMode.UNKNOWN: 255>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class OBTofExposureThresholdControl:
    lower: int
    upper: int
    def __init__(self) -> None:
        ...
class OBTofFilterRange:
    """
    Members:
    
      CLOSE
    
      MIDDLE
    
      FAR
    
      DEBUG
    """
    CLOSE: typing.ClassVar[OBTofFilterRange]  # value = <OBTofFilterRange.CLOSE: 0>
    DEBUG: typing.ClassVar[OBTofFilterRange]  # value = <OBTofFilterRange.DEBUG: 100>
    FAR: typing.ClassVar[OBTofFilterRange]  # value = <OBTofFilterRange.FAR: 2>
    MIDDLE: typing.ClassVar[OBTofFilterRange]  # value = <OBTofFilterRange.MIDDLE: 1>
    __members__: typing.ClassVar[dict[str, OBTofFilterRange]]  # value = {'CLOSE': <OBTofFilterRange.CLOSE: 0>, 'MIDDLE': <OBTofFilterRange.MIDDLE: 1>, 'FAR': <OBTofFilterRange.FAR: 2>, 'DEBUG': <OBTofFilterRange.DEBUG: 100>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class OBUSBPowerState:
    """
    Members:
    
      OFF
    
      POWER_5V_0A9
    
      POWER_5V_1A5
    
      POWER_5V_3A0
    """
    OFF: typing.ClassVar[OBUSBPowerState]  # value = <OBUSBPowerState.OFF: 0>
    POWER_5V_0A9: typing.ClassVar[OBUSBPowerState]  # value = <OBUSBPowerState.POWER_5V_0A9: 1>
    POWER_5V_1A5: typing.ClassVar[OBUSBPowerState]  # value = <OBUSBPowerState.POWER_5V_1A5: 2>
    POWER_5V_3A0: typing.ClassVar[OBUSBPowerState]  # value = <OBUSBPowerState.POWER_5V_3A0: 3>
    __members__: typing.ClassVar[dict[str, OBUSBPowerState]]  # value = {'OFF': <OBUSBPowerState.OFF: 0>, 'POWER_5V_0A9': <OBUSBPowerState.POWER_5V_0A9: 1>, 'POWER_5V_1A5': <OBUSBPowerState.POWER_5V_1A5: 2>, 'POWER_5V_3A0': <OBUSBPowerState.POWER_5V_3A0: 3>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class OBUint16PropertyRange:
    current: int
    default_value: int
    max: int
    min: int
    step: int
    def __init__(self) -> None:
        ...
class OBUint8PropertyRange:
    current: int
    default_value: int
    max: int
    min: int
    step: int
    def __init__(self) -> None:
        ...
class OBUpgradeState:
    """
    Members:
    
      FILE_TRANSFER
    
      DONE
    
      IN_PROGRESS
    
      START
    
      VERIFY_IMAGE
    
      VERIFY_ERROR
    
      PROGRAM_ERROR
    
      ERASE_ERROR
    
      FLASH_TYPE_ERROR
    
      IMAGE_SIZE_ERROR
    
      OTHER_ERROR
    
      DDR_ERROR
    
      TIMEOUT_ERROR
    """
    DDR_ERROR: typing.ClassVar[OBUpgradeState]  # value = <OBUpgradeState.DDR_ERROR: -7>
    DONE: typing.ClassVar[OBUpgradeState]  # value = <OBUpgradeState.DONE: 3>
    ERASE_ERROR: typing.ClassVar[OBUpgradeState]  # value = <OBUpgradeState.ERASE_ERROR: -3>
    FILE_TRANSFER: typing.ClassVar[OBUpgradeState]  # value = <OBUpgradeState.FILE_TRANSFER: 4>
    FLASH_TYPE_ERROR: typing.ClassVar[OBUpgradeState]  # value = <OBUpgradeState.FLASH_TYPE_ERROR: -4>
    IMAGE_SIZE_ERROR: typing.ClassVar[OBUpgradeState]  # value = <OBUpgradeState.IMAGE_SIZE_ERROR: -5>
    IN_PROGRESS: typing.ClassVar[OBUpgradeState]  # value = <OBUpgradeState.IN_PROGRESS: 2>
    OTHER_ERROR: typing.ClassVar[OBUpgradeState]  # value = <OBUpgradeState.OTHER_ERROR: -6>
    PROGRAM_ERROR: typing.ClassVar[OBUpgradeState]  # value = <OBUpgradeState.PROGRAM_ERROR: -2>
    START: typing.ClassVar[OBUpgradeState]  # value = <OBUpgradeState.START: 1>
    TIMEOUT_ERROR: typing.ClassVar[OBUpgradeState]  # value = <OBUpgradeState.TIMEOUT_ERROR: -8>
    VERIFY_ERROR: typing.ClassVar[OBUpgradeState]  # value = <OBUpgradeState.VERIFY_ERROR: -1>
    VERIFY_IMAGE: typing.ClassVar[OBUpgradeState]  # value = <OBUpgradeState.VERIFY_IMAGE: 0>
    __members__: typing.ClassVar[dict[str, OBUpgradeState]]  # value = {'FILE_TRANSFER': <OBUpgradeState.FILE_TRANSFER: 4>, 'DONE': <OBUpgradeState.DONE: 3>, 'IN_PROGRESS': <OBUpgradeState.IN_PROGRESS: 2>, 'START': <OBUpgradeState.START: 1>, 'VERIFY_IMAGE': <OBUpgradeState.VERIFY_IMAGE: 0>, 'VERIFY_ERROR': <OBUpgradeState.VERIFY_ERROR: -1>, 'PROGRAM_ERROR': <OBUpgradeState.PROGRAM_ERROR: -2>, 'ERASE_ERROR': <OBUpgradeState.ERASE_ERROR: -3>, 'FLASH_TYPE_ERROR': <OBUpgradeState.FLASH_TYPE_ERROR: -4>, 'IMAGE_SIZE_ERROR': <OBUpgradeState.IMAGE_SIZE_ERROR: -5>, 'OTHER_ERROR': <OBUpgradeState.OTHER_ERROR: -6>, 'DDR_ERROR': <OBUpgradeState.DDR_ERROR: -7>, 'TIMEOUT_ERROR': <OBUpgradeState.TIMEOUT_ERROR: -8>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class Pipeline:
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: Device) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: str) -> None:
        ...
    def disable_frame_sync(self) -> None:
        ...
    def enable_frame_sync(self) -> None:
        ...
    def get_camera_param(self) -> OBCameraParam:
        ...
    def get_config(self) -> ...:
        ...
    def get_d2c_valid_area(self, arg0: int, arg1: int) -> OBRect:
        ...
    def get_device(self) -> Device:
        ...
    def get_playback(self) -> ...:
        ...
    def get_stream_profile_list(self, arg0: OBSensorType) -> ...:
        ...
    @typing.overload
    def start(self, arg0: ...) -> None:
        ...
    @typing.overload
    def start(self, arg0: ..., arg1: typing.Callable) -> None:
        ...
    @typing.overload
    def start(self) -> None:
        ...
    def start_recording(self, arg0: str) -> None:
        ...
    def stop(self) -> None:
        ...
    def stop_recording(self) -> None:
        ...
    def switch_config(self, arg0: ...) -> None:
        ...
    def wait_for_frames(self, arg0: int) -> FrameSet:
        ...
class Playback:
    def get_camera_param(self) -> OBCameraParam:
        ...
    def get_device_info(self) -> DeviceInfo:
        ...
    def set_playback_state_callback(self, arg0: typing.Callable) -> None:
        ...
    def start(self, callback: typing.Callable, media_type: OBMediaType = ...) -> None:
        ...
    def stop(self) -> None:
        ...
class PointCloudFilter(Filter):
    def __init__(self) -> None:
        ...
    def calculate(self, arg0: ...) -> numpy.ndarray[numpy.float32]:
        ...
    def set_camera_param(self, arg0: OBCameraParam) -> None:
        ...
    def set_color_data_normalization(self, arg0: bool) -> None:
        ...
    def set_create_point_format(self, arg0: OBFormat) -> None:
        ...
    def set_frame_align_state(self, arg0: bool) -> None:
        ...
    def set_position_data_scaled(self, arg0: float) -> None:
        ...
class PointsFrame(Frame):
    def get_position_value_scale(self) -> float:
        ...
class Recorder:
    def start(self, arg0: str) -> None:
        ...
    def stop(self) -> None:
        ...
    def write(self, arg0: Frame) -> None:
        ...
class Sensor:
    def __repr__(self) -> str:
        ...
    def get_recommended_filters(self) -> ...:
        ...
    def get_stream_profile_list(self) -> ...:
        ...
    def get_type(self) -> OBSensorType:
        ...
    def start(self, arg0: ..., arg1: typing.Callable) -> None:
        ...
    def stop(self) -> None:
        ...
    def switch_profile(self, arg0: ...) -> None:
        ...
class SensorList:
    def __len__(self) -> int:
        ...
    def get_count(self) -> int:
        ...
    def get_sensor_by_index(self, arg0: int) -> Sensor:
        ...
    def get_sensor_by_type(self, arg0: OBSensorType) -> Sensor:
        ...
    def get_type_by_index(self, arg0: int) -> OBSensorType:
        ...
class SequenceIdFilter(Filter):
    def __init__(self) -> None:
        ...
    def get_select_sequence_id(self) -> int:
        ...
    def get_sequence_id_list(self) -> list:
        ...
    def get_sequence_id_list_size(self) -> int:
        ...
    def select_sequence_id(self, arg0: int) -> None:
        ...
class SpatialAdvancedFilter(Filter):
    def __init__(self) -> None:
        ...
    def get_alpha_range(self) -> OBFloatPropertyRange:
        """
        get alpha range
        """
    def get_disp_diff_range(self) -> OBUint16PropertyRange:
        ...
    def get_filter_params(self) -> OBSpatialAdvancedFilterParams:
        ...
    def get_magnitude_range(self) -> OBIntPropertyRange:
        ...
    def get_radius_range(self) -> OBUint16PropertyRange:
        ...
    def set_filter_params(self, arg0: OBSpatialAdvancedFilterParams) -> None:
        ...
class StreamProfile:
    def as_accel_stream_profile(self) -> ...:
        ...
    def as_gyro_stream_profile(self) -> ...:
        ...
    def as_video_stream_profile(self) -> ...:
        ...
    def get_format(self) -> OBFormat:
        ...
    def get_type(self) -> OBStreamType:
        ...
    def is_accel_stream_profile(self) -> bool:
        ...
    def is_gyro_stream_profile(self) -> bool:
        ...
    def is_video_stream_profile(self) -> bool:
        ...
class StreamProfileList:
    def __len__(self) -> int:
        ...
    def get_count(self) -> int:
        ...
    def get_default_video_stream_profile(self) -> VideoStreamProfile:
        ...
    def get_stream_profile_by_index(self, arg0: int) -> StreamProfile:
        ...
    def get_video_stream_profile(self, arg0: int, arg1: int, arg2: OBFormat, arg3: int) -> VideoStreamProfile:
        ...
class TemporalFilter(Filter):
    def __init__(self) -> None:
        ...
    def get_diff_scale_range(self) -> OBFloatPropertyRange:
        """
        get diff scale range
        """
    def get_weight_range(self) -> OBFloatPropertyRange:
        """
        get weight range
        """
    def set_diff_scale(self, arg0: float) -> None:
        """
        set diff scale
        """
    def set_weight(self, arg0: float) -> None:
        ...
class ThresholdFilter(Filter):
    def __init__(self) -> None:
        ...
    def get_max_range(self) -> OBIntPropertyRange:
        ...
    def get_min_range(self) -> OBIntPropertyRange:
        ...
    def set_value_range(self, arg0: int, arg1: int) -> bool:
        ...
class VideoFrame(Frame):
    def __init__(self, arg0: Frame) -> None:
        ...
    def __repr__(self) -> None:
        ...
    def as_color_frame(self) -> ...:
        ...
    def as_depth_frame(self) -> ...:
        ...
    def as_ir_frame(self) -> ...:
        ...
    def as_points_frame(self) -> ...:
        ...
    def get_height(self) -> int:
        ...
    def get_metadata(self) -> numpy.ndarray[numpy.uint8]:
        ...
    def get_metadata_size(self) -> int:
        ...
    def get_pixel_available_bit_size(self) -> int:
        ...
    def get_width(self) -> int:
        ...
class VideoStreamProfile(StreamProfile):
    def __init__(self, arg0: StreamProfile) -> None:
        ...
    def __repr__(self) -> str:
        ...
    def get_distortion(self) -> OBCameraDistortion:
        ...
    def get_fps(self) -> int:
        ...
    def get_height(self) -> int:
        ...
    def get_intrinsic(self) -> OBCameraIntrinsic:
        ...
    def get_width(self) -> int:
        ...
def calibration_2d_to_3d(arg0: OBCalibrationParam, arg1: OBPoint2f, arg2: float, arg3: OBSensorType, arg4: OBSensorType) -> OBPoint:
    ...
def calibration_2d_to_3d_undistortion(arg0: OBCalibrationParam, arg1: OBPoint2f, arg2: float, arg3: OBSensorType, arg4: OBSensorType) -> OBPoint:
    ...
@typing.overload
def calibration_3d_to_2d(arg0: OBCalibrationParam, arg1: OBPoint, arg2: OBSensorType, arg3: OBSensorType) -> OBPoint2f:
    ...
@typing.overload
def calibration_3d_to_2d(arg0: OBCalibrationParam, arg1: OBPoint, arg2: OBSensorType, arg3: OBSensorType) -> OBPoint2f:
    ...
def calibration_3d_to_3d(arg0: OBCalibrationParam, arg1: OBPoint, arg2: OBSensorType, arg3: OBSensorType) -> OBPoint:
    ...
def get_version() -> str:
    ...
