"""
OrbbecSDK python binding
"""

from __future__ import annotations

import collections.abc
import typing

import numpy
import numpy.typing
import typing_extensions

__all__: list[str] = [
    "AccelFrame",
    "AccelStreamProfile",
    "AlignFilter",
    "COUNT",
    "CameraParamList",
    "ColorFrame",
    "ConfidenceFrame",
    "Config",
    "Context",
    "DecimationFilter",
    "DepthFrame",
    "Device",
    "DeviceInfo",
    "DeviceList",
    "DevicePresetList",
    "DisparityTransform",
    "EdgeNoiseRemovalFilter",
    "Filter",
    "FormatConvertFilter",
    "Frame",
    "FrameSet",
    "GyroFrame",
    "GyroStreamProfile",
    "HDRMergeFilter",
    "HoleFillingFilter",
    "IRFrame",
    "LiDARPointsFrame",
    "LiDARStreamProfile",
    "LutNoiseRemovalFilter",
    "MgcNoiseRemovalFilter",
    "NoiseRemovalFilter",
    "OBAccelFullScaleRange",
    "OBAccelIntrinsic",
    "OBAccelSampleRate",
    "OBAccelValue",
    "OBAlignMode",
    "OBBaselineCalibrationParam",
    "OBBoolPropertyRange",
    "OBCalibrationParam",
    "OBCameraDistortion",
    "OBCameraDistortionModel",
    "OBCameraIntrinsic",
    "OBCameraParam",
    "OBCmdVersion",
    "OBColorPoint",
    "OBCommunicationType",
    "OBCompressionMode",
    "OBCompressionParams",
    "OBConvertFormat",
    "OBCoordinateSystemType",
    "OBDCPowerState",
    "OBDDONoiseRemovalType",
    "OBDataTranState",
    "OBDepthCroppingMode",
    "OBDepthPrecisionLevel",
    "OBDepthWorkMode",
    "OBDepthWorkModeList",
    "OBDepthWorkModeTag",
    "OBDeviceAccessMode",
    "OBDeviceDevelopmentMode",
    "OBDeviceIpAddrConfig",
    "OBDeviceSyncConfig",
    "OBDeviceTemperature",
    "OBDeviceTimestampResetConfig",
    "OBDeviceType",
    "OBEdgeNoiseRemovalFilterParams",
    "OBEdgeNoiseRemovalType",
    "OBError",
    "OBErrorDetails",
    "OBException",
    "OBExtrinsic",
    "OBFileTranState",
    "OBFilterConfigSchemaItem",
    "OBFilterConfigValueType",
    "OBFilterList",
    "OBFloat3D",
    "OBFloatPropertyRange",
    "OBFormat",
    "OBFrameAggregateOutputMode",
    "OBFrameMetadataType",
    "OBFrameType",
    "OBGvcpPortScheme",
    "OBGyroFullScaleRange",
    "OBGyroIntrinsic",
    "OBGyroSampleRate",
    "OBGyroValue",
    "OBHardwareDecimationConfig",
    "OBHdrConfig",
    "OBHoleFillingMode",
    "OBIntPropertyRange",
    "OBIpSourceType",
    "OBLiDARPoint",
    "OBLiDARScanPoint",
    "OBLiDARScanRate",
    "OBLiDARSpherePoint",
    "OBLogLevel",
    "OBLutNoiseRemovalFilterParams",
    "OBMediaState",
    "OBMediaType",
    "OBMgcNoiseRemovalFilterParams",
    "OBMultiDeviceSyncConfig",
    "OBMultiDeviceSyncMode",
    "OBNetIpConfigV2",
    "OBNoiseRemovalFilterParams",
    "OBPermissionType",
    "OBPipelineIssue",
    "OBPipelineStatus",
    "OBPixelType",
    "OBPlaybackStatus",
    "OBPoint2f",
    "OBPoint3f",
    "OBPowerLineFreqMode",
    "OBPresetResolutionConfig",
    "OBPropertyID",
    "OBPropertyItem",
    "OBPropertyType",
    "OBProtocolVersion",
    "OBRect",
    "OBRegionOfInterest",
    "OBRotateDegreeType",
    "OBSensorType",
    "OBSequenceIdItem",
    "OBSpatialAdvancedFilterParams",
    "OBStatus",
    "OBStreamType",
    "OBSyncMode",
    "OBTofExposureThresholdControl",
    "OBTofFilterRange",
    "OBUSBPowerState",
    "OBUint16PropertyRange",
    "OBUint8PropertyRange",
    "OBUpgradeState",
    "PAUSED",
    "PLAYING",
    "Pipeline",
    "PlaybackDevice",
    "PointCloudFilter",
    "PointsFrame",
    "PresetResolutionConfigList",
    "RecordDevice",
    "SAMPLE_RATE_100_HZ",
    "SAMPLE_RATE_12_5_HZ",
    "SAMPLE_RATE_16_KHZ",
    "SAMPLE_RATE_1_5625_HZ",
    "SAMPLE_RATE_1_KHZ",
    "SAMPLE_RATE_200_HZ",
    "SAMPLE_RATE_25_HZ",
    "SAMPLE_RATE_2_KHZ",
    "SAMPLE_RATE_32_KHZ",
    "SAMPLE_RATE_3_125_HZ",
    "SAMPLE_RATE_400_HZ",
    "SAMPLE_RATE_4_KHZ",
    "SAMPLE_RATE_500_HZ",
    "SAMPLE_RATE_50_HZ",
    "SAMPLE_RATE_6_25_HZ",
    "SAMPLE_RATE_800_HZ",
    "SAMPLE_RATE_8_KHZ",
    "SAMPLE_RATE_UNKNOWN",
    "STOPPED",
    "Sensor",
    "SensorList",
    "SequenceIdFilter",
    "SpatialAdvancedFilter",
    "StreamProfile",
    "StreamProfileList",
    "TemporalFilter",
    "ThresholdFilter",
    "UNKNOWN",
    "VideoFrame",
    "VideoStreamProfile",
    "get_version",
    "save_lidar_point_cloud_to_ply",
    "save_point_cloud_to_ply",
    "transformation2dto2d",
    "transformation2dto3d",
    "transformation3dto2d",
    "transformation3dto3d",
]

class AccelFrame(Frame):
    def __repr__(self) -> str: ...
    def get_temperature(self) -> float: ...
    def get_value(self) -> OBAccelValue: ...
    def get_x(self) -> float: ...
    def get_y(self) -> float: ...
    def get_z(self) -> float: ...

class AccelStreamProfile(StreamProfile):
    def __repr__(self) -> str: ...
    def get_full_scale_range(self) -> OBAccelFullScaleRange: ...
    def get_intrinsic(self) -> OBAccelIntrinsic: ...
    def get_sample_rate(self) -> OBGyroSampleRate: ...

class AlignFilter(Filter):
    def __init__(self, align_to_stream: OBStreamType) -> None: ...
    def get_align_to_stream_type(self) -> OBStreamType: ...

class CameraParamList:
    def __getitem__(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> OBCameraParam: ...
    def __len__(self) -> int: ...
    def get_camera_param(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> OBCameraParam:
        """
        Get the camera parameters for the specified index
        """

    def get_count(self) -> int:
        """
        Get the number of devices in the list
        """

class ColorFrame(VideoFrame):
    pass

class ConfidenceFrame(VideoFrame):
    pass

class Config:
    def __init__(self) -> None: ...
    def disable_all_stream(self) -> None: ...
    @typing.overload
    def disable_stream(self, arg0: OBStreamType) -> None: ...
    @typing.overload
    def disable_stream(self, arg0: OBSensorType) -> None: ...
    def enable_accel_stream(
        self,
        full_scale_range: OBAccelFullScaleRange = OBAccelFullScaleRange.ACCEL_FS_UNKNOWN,
        sample_rate: OBGyroSampleRate = OBGyroSampleRate.SAMPLE_RATE_UNKNOWN,
    ) -> None: ...
    def enable_all_stream(self) -> None: ...
    def enable_gyro_stream(
        self,
        full_scale_range: OBGyroFullScaleRange = OBGyroFullScaleRange.FS_UNKNOWN,
        sample_rate: OBGyroSampleRate = OBGyroSampleRate.SAMPLE_RATE_UNKNOWN,
    ) -> None: ...
    def enable_lidar_stream(
        self,
        scan_rate: OBLiDARScanRate = OBLiDARScanRate.LIDAR_SCAN_UNKNOWN,
        format: OBFormat = OBFormat.UNKNOWN_FORMAT,
    ) -> None: ...
    @typing.overload
    def enable_stream(self, arg0: StreamProfile) -> None: ...
    @typing.overload
    def enable_stream(self, arg0: OBStreamType) -> None: ...
    @typing.overload
    def enable_stream(self, arg0: OBSensorType) -> None: ...
    @typing.overload
    def enable_video_stream(
        self,
        stream_type: OBStreamType,
        width: typing.SupportsInt | typing.SupportsIndex = 0,
        height: typing.SupportsInt | typing.SupportsIndex = 0,
        fps: typing.SupportsInt | typing.SupportsIndex = 0,
        format: OBFormat = OBFormat.UNKNOWN_FORMAT,
    ) -> None: ...
    @typing.overload
    def enable_video_stream(
        self,
        sensor_type: OBSensorType,
        width: typing.SupportsInt | typing.SupportsIndex = 0,
        height: typing.SupportsInt | typing.SupportsIndex = 0,
        fps: typing.SupportsInt | typing.SupportsIndex = 0,
        format: OBFormat = OBFormat.UNKNOWN_FORMAT,
    ) -> None: ...
    @typing.overload
    def enable_video_stream(
        self,
        sensor_type: OBSensorType,
        decimation_config: OBHardwareDecimationConfig,
        fps: typing.SupportsInt | typing.SupportsIndex = 0,
        format: OBFormat = OBFormat.UNKNOWN_FORMAT,
    ) -> None: ...
    def get_enabled_stream_profile_list(self) -> StreamProfileList: ...
    def set_align_mode(self, arg0: OBAlignMode) -> None: ...
    def set_depth_scale_require(self, arg0: bool) -> None: ...
    def set_frame_aggregate_output_mode(self, arg0: OBFrameAggregateOutputMode) -> None: ...

class Context:
    @staticmethod
    def log_external_message(
        arg0: OBLogLevel, arg1: str, arg2: str, arg3: str, arg4: str, arg5: typing.SupportsInt | typing.SupportsIndex
    ) -> None: ...
    @staticmethod
    def set_logger_file_name(arg0: str) -> None:
        """
        Set logger file name
        """

    @staticmethod
    def set_logger_level(arg0: OBLogLevel) -> None: ...
    @staticmethod
    def set_logger_to_callback(arg0: OBLogLevel, arg1: collections.abc.Callable) -> None:
        """
        Set logger to callback
        """

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
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, arg0: str) -> None: ...
    def create_net_device(
        self,
        address: str,
        port: typing.SupportsInt | typing.SupportsIndex,
        access_mode: OBDeviceAccessMode = OBDeviceAccessMode.OB_DEVICE_DEFAULT_ACCESS,
    ) -> Device:
        """
        Create net device
        """

    def enable_multi_device_sync(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None:
        """
        Activates the multi-device synchronization function to synchronize the clock of the created device (the device needs to support this function).repeat_interval: The synchronization time interval (unit: ms; if repeatInterval=0, it means that it will only be synchronized once and will not be executed regularly).
        """

    def enable_net_device_enumeration(self, arg0: bool) -> None: ...
    def get_gvcp_port_scheme(self) -> OBGvcpPortScheme:
        """
        Get the current GVCP port scheme
        """

    def ob_force_ip_config(self, arg0: str, arg1: OBDeviceIpAddrConfig) -> bool:
        """
        Change the IP configuration
        """

    def query_devices(self) -> DeviceList:
        """
        Query devices
        """

    def register_device_changed_callback(self, arg0: collections.abc.Callable) -> int: ...
    def set_device_changed_callback(self, arg0: collections.abc.Callable) -> None:
        """
        Set device changed callback, callback will be called when device changed
        """

    def set_gvcp_port_scheme(self, arg0: OBGvcpPortScheme) -> None:
        """
        Set the GVCP port scheme used for network device discovery and control
        """

    def unregister_device_changed_callback(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...

class DecimationFilter(Filter):
    def __init__(self) -> None: ...
    def get_scale_range(self) -> OBUint8PropertyRange: ...
    def get_scale_value(self) -> int: ...
    def set_scale_value(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...

class DepthFrame(VideoFrame):
    def get_depth_scale(self) -> float: ...
    def set_value_scale(self, arg0: typing.SupportsFloat | typing.SupportsIndex) -> None: ...

class Device:
    __hash__: typing.ClassVar[None] = None
    def __eq__(self, arg0: Device) -> bool: ...
    def enable_firmware_log(self, arg0: bool) -> None:
        """
        Enable or disable the device firmware log
        """

    def enable_heart_beat(self, arg0: bool) -> None: ...
    def export_settings_as_preset_json_file(self, arg0: str) -> None: ...
    def get_available_preset_list(self) -> DevicePresetList: ...
    def get_available_preset_resolution_config_list(self) -> PresetResolutionConfigList: ...
    def get_baseline(self) -> OBBaselineCalibrationParam: ...
    def get_bool_property(self, arg0: OBPropertyID) -> bool: ...
    def get_bool_property_range(self, arg0: OBPropertyID) -> OBBoolPropertyRange: ...
    def get_calibration_camera_param_list(self) -> CameraParamList: ...
    def get_current_preset_name(self) -> str: ...
    def get_depth_work_mode(self) -> OBDepthWorkMode: ...
    def get_depth_work_mode_list(self) -> OBDepthWorkModeList: ...
    def get_device_info(self) -> DeviceInfo: ...
    def get_device_state(self) -> int: ...
    def get_float_property(self, arg0: OBPropertyID) -> float: ...
    def get_float_property_range(self, arg0: OBPropertyID) -> OBFloatPropertyRange: ...
    def get_int_property(self, arg0: OBPropertyID) -> int: ...
    def get_int_property_range(self, arg0: OBPropertyID) -> OBIntPropertyRange: ...
    def get_multi_device_sync_config(self) -> OBMultiDeviceSyncConfig: ...
    def get_sensor(self, arg0: OBSensorType) -> Sensor: ...
    def get_sensor_list(self) -> SensorList: ...
    def get_support_property_count(self) -> int: ...
    def get_supported_property(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> OBPropertyItem: ...
    def get_temperature(self) -> OBDeviceTemperature: ...
    def get_timestamp_reset_config(self) -> OBDeviceTimestampResetConfig: ...
    def isFrameInterleaveSupported(self) -> bool: ...
    def is_property_supported(self, arg0: OBPropertyID, arg1: OBPermissionType) -> bool: ...
    def loadFrameInterleave(self, arg0: str) -> None: ...
    def load_depth_filter_config(self, arg0: str) -> None: ...
    def load_preset(self, arg0: str) -> None: ...
    def load_preset_from_json_data(self, arg0: str, arg1: str) -> None: ...
    def load_preset_from_json_file(self, arg0: str) -> None: ...
    def reboot(self) -> None: ...
    def set_bool_property(self, arg0: OBPropertyID, arg1: bool) -> None: ...
    @typing.overload
    def set_depth_work_mode(self, arg0: OBDepthWorkMode) -> OBStatus: ...
    @typing.overload
    def set_depth_work_mode(self, arg0: str) -> OBStatus: ...
    def set_device_state_changed_callback(self, arg0: collections.abc.Callable) -> None: ...
    def set_float_property(self, arg0: OBPropertyID, arg1: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    def set_hdr_config(self, arg0: OBHdrConfig) -> None: ...
    def set_int_property(self, arg0: OBPropertyID, arg1: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @typing.overload
    def set_ip_config(self, arg0: OBNetIpConfigV2) -> None: ...
    @typing.overload
    def set_ip_config(self, arg0: OBDeviceIpAddrConfig) -> None: ...
    def set_multi_device_sync_config(self, arg0: OBMultiDeviceSyncConfig) -> None: ...
    def set_preset_resolution_config(self, arg0: OBPresetResolutionConfig) -> None: ...
    def set_timestamp_reset_config(self, arg0: OBDeviceTimestampResetConfig) -> None: ...
    def timer_reset(self) -> None: ...
    def timer_sync_with_host(self) -> None: ...
    def timestamp_reset(self) -> None: ...
    def trigger_capture(self) -> None: ...
    def update_firmware(
        self, file_path: str, callback: collections.abc.Callable, async_update: bool = True
    ) -> None: ...
    def update_optional_depth_presets(self, file_path_list: list, callback: collections.abc.Callable) -> None: ...

class DeviceInfo:
    def __repr__(self) -> str: ...
    def get_connection_type(self) -> str:
        """
        Get the connection type of the device
        """

    def get_device_gateway(self) -> str:
        """
        Get device gateway
        """

    def get_device_ip_address(self) -> str:
        """
        Get device ip address
        """

    def get_device_subnet_mask(self) -> str:
        """
        Get device subnet mask
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
    def __getitem__(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> Device: ...
    def __len__(self) -> int: ...
    def get_count(self) -> int: ...
    def get_device_by_index(
        self,
        index: typing.SupportsInt | typing.SupportsIndex,
        access_mode: OBDeviceAccessMode = OBDeviceAccessMode.OB_DEVICE_DEFAULT_ACCESS,
    ) -> Device: ...
    def get_device_by_serial_number(
        self, serial_number: str, access_mode: OBDeviceAccessMode = OBDeviceAccessMode.OB_DEVICE_DEFAULT_ACCESS
    ) -> Device: ...
    def get_device_by_uid(
        self, uid: str, access_mode: OBDeviceAccessMode = OBDeviceAccessMode.OB_DEVICE_DEFAULT_ACCESS
    ) -> Device: ...
    def get_device_connection_type_by_index(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> str: ...
    def get_device_gateway_by_index(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> str: ...
    def get_device_ip_address_by_index(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> str: ...
    def get_device_name_by_index(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> str: ...
    def get_device_pid_by_index(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> int: ...
    def get_device_serial_number_by_index(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> str: ...
    def get_device_subnet_mask_by_index(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> str: ...
    def get_device_uid_by_index(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> str: ...
    def get_device_user_name_by_index(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> str:
        """
        Get the user-defined name of the device at the specified index
        """

    def get_device_vid_by_index(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> int: ...
    def get_ip_source_type(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> OBIpSourceType:
        """
        Get the current GVCP IP configuration status of the device
        """

    def get_local_gateway(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> str:
        """
        Get the host gateway for the specified device
        """

    def get_local_ip(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> str:
        """
        Get the host Ip address for the specified device
        """

    def get_local_mac_address(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> str:
        """
        Get the host Mac address for the specified device
        """

    def get_local_net_interface_name(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> str:
        """
        Get the name of the host network interface corresponding to the device
        """

    def get_local_subnet_length(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> int:
        """
        Get the host subnet length for the specified device
        """

class DevicePresetList:
    def __contains__(self, arg0: str) -> bool: ...
    def __getitem__(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> str: ...
    def __len__(self) -> int: ...
    def get_count(self) -> int: ...
    def get_name_by_index(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> str: ...
    def has_preset(self, arg0: str) -> bool: ...

class DisparityTransform(Filter):
    def __init__(self, activationKey: str = "") -> None: ...

class EdgeNoiseRemovalFilter(Filter):
    def __init__(self, activation_key: str = "") -> None: ...
    def get_height_range(self) -> OBUint16PropertyRange: ...
    def get_limit_x_th_range(self) -> OBUint16PropertyRange: ...
    def get_limit_y_th_range(self) -> OBUint16PropertyRange: ...
    def get_margin_x_th_range(self) -> OBUint16PropertyRange: ...
    def get_margin_y_th_range(self) -> OBUint16PropertyRange: ...
    def get_vertical_direction_enable_range(self) -> OBUint16PropertyRange: ...
    def get_width_range(self) -> OBUint16PropertyRange: ...
    def set_filter_params(self, arg0: OBEdgeNoiseRemovalFilterParams) -> None: ...

class Filter:
    def enable(self, arg0: bool) -> None: ...
    def get_config_schema_vec(self) -> list[OBFilterConfigSchemaItem]: ...
    def get_config_value(self, arg0: str) -> float: ...
    def get_name(self) -> str: ...
    def is_align_filter(self) -> bool: ...
    def is_decimation_filter(self) -> bool: ...
    def is_disparity_transform_filter(self) -> bool: ...
    def is_edge_noise_removal_filter(self) -> bool: ...
    def is_enabled(self) -> bool: ...
    def is_format_converter(self) -> bool: ...
    def is_hdr_merge_filter(self) -> bool: ...
    def is_hole_filling_filter(self) -> bool: ...
    def is_noise_removal_filter(self) -> bool: ...
    def is_point_cloud_filter(self) -> bool: ...
    def is_sequence_id_filter(self) -> bool: ...
    def is_spatial_advanced_filter(self) -> bool: ...
    def is_temporal_filter(self) -> bool: ...
    def is_threshold_filter(self) -> bool: ...
    def process(self, arg0: Frame) -> typing.Any: ...
    def push_frame(self, arg0: Frame) -> None: ...
    def reset(self) -> None: ...
    def set_callback(self, arg0: collections.abc.Callable) -> None: ...
    def set_config_value(self, arg0: str, arg1: typing.SupportsFloat | typing.SupportsIndex) -> None: ...

class FormatConvertFilter(Filter):
    def __init__(self) -> None: ...
    def set_format_convert_format(self, arg0: OBConvertFormat) -> None:
        """
        Set the format to convert to
        """

class Frame:
    def __repr__(self) -> str: ...
    def as_accel_frame(self) -> AccelFrame: ...
    def as_color_frame(self) -> ColorFrame: ...
    def as_confidence_frame(self) -> ConfidenceFrame: ...
    def as_depth_frame(self) -> DepthFrame: ...
    def as_frame_set(self) -> FrameSet: ...
    def as_gyro_frame(self) -> GyroFrame: ...
    def as_ir_frame(self) -> IRFrame: ...
    def as_lidar_points_frame(self) -> LiDARPointsFrame: ...
    def as_points_frame(self) -> PointsFrame: ...
    def as_video_frame(self) -> VideoFrame:
        """
        DISCOURAGED: This method is rarely needed in normal usage.
        """

    def copy_frame_info(self, arg0: Frame) -> None: ...
    def get_data(self) -> numpy.typing.NDArray[numpy.uint8]: ...
    def get_data_pointer(self) -> typing.Any: ...
    def get_data_size(self) -> int: ...
    def get_device(self) -> Device: ...
    def get_format(self) -> OBFormat: ...
    def get_global_timestamp_us(self) -> int: ...
    def get_index(self) -> int: ...
    def get_metadata_value(self, arg0: OBFrameMetadataType) -> int: ...
    def get_sensor(self) -> Sensor: ...
    def get_stream_profile(self) -> StreamProfile: ...
    def get_system_timestamp(self) -> int: ...
    def get_system_timestamp_us(self) -> int: ...
    def get_timestamp(self) -> int:
        """
        Get the hardware timestamp of the frame in milliseconds
        """

    def get_timestamp_us(self) -> int: ...
    def get_type(self) -> OBFrameType: ...
    def has_metadata(self, arg0: OBFrameMetadataType) -> bool: ...
    def set_stream_profile(self, arg0: StreamProfile) -> None: ...
    def set_system_timestamp_us(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def update_data(self, arg0: typing_extensions.Buffer) -> None: ...
    def update_metadata(self, arg0: typing_extensions.Buffer) -> None: ...

class FrameSet(Frame):
    def __getitem__(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> Frame: ...
    def __len__(self) -> int: ...
    def __repr__(self) -> str: ...
    def get_accel_frame(self) -> AccelFrame: ...
    def get_color_frame(self) -> ColorFrame: ...
    def get_confidence_frame(self) -> ConfidenceFrame: ...
    def get_count(self) -> int: ...
    def get_depth_frame(self) -> DepthFrame: ...
    def get_frame(self, arg0: OBFrameType) -> Frame: ...
    def get_frame_by_index(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> Frame: ...
    def get_frame_by_type(self, arg0: OBFrameType) -> Frame: ...
    def get_frame_count(self) -> int: ...
    def get_gyro_frame(self) -> GyroFrame: ...
    def get_ir_frame(self) -> IRFrame: ...
    def get_left_color_frame(self) -> ColorFrame: ...
    def get_left_ir_frame(self) -> IRFrame: ...
    def get_lidar_points_frame(self) -> LiDARPointsFrame: ...
    def get_points_frame(self) -> PointsFrame: ...
    def get_right_color_frame(self) -> ColorFrame: ...
    def get_right_ir_frame(self) -> IRFrame: ...
    def push_frame(self, arg0: Frame) -> None: ...

class GyroFrame(Frame):
    def __repr__(self) -> str: ...
    def get_temperature(self) -> float: ...
    def get_value(self) -> OBAccelValue: ...
    def get_x(self) -> float: ...
    def get_y(self) -> float: ...
    def get_z(self) -> float: ...

class GyroStreamProfile(StreamProfile):
    def __repr__(self) -> str: ...
    def get_full_scale_range(self) -> OBGyroFullScaleRange: ...
    def get_intrinsic(self) -> OBGyroIntrinsic: ...
    def get_sample_rate(self) -> OBGyroSampleRate: ...

class HDRMergeFilter(Filter):
    def __init__(self) -> None: ...

class HoleFillingFilter(Filter):
    def __init__(self) -> None: ...
    def get_filling_mode(self) -> OBHoleFillingMode: ...
    def set_filling_mode(self, arg0: OBHoleFillingMode) -> None:
        """
        Set the filling mode
        """

class IRFrame(VideoFrame):
    pass

class LiDARPointsFrame(Frame):
    pass

class LiDARStreamProfile(StreamProfile):
    def get_scan_rate(self) -> OBLiDARScanRate: ...

class LutNoiseRemovalFilter(Filter):
    def __init__(self, activation_key: str = "") -> None: ...
    def get_filter_params(self) -> OBLutNoiseRemovalFilterParams: ...
    def get_height_range(self) -> OBUint16PropertyRange: ...
    def get_max_lut_range(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> OBUint16PropertyRange: ...
    def get_min_diff_range(self) -> OBUint16PropertyRange: ...
    def get_width_range(self) -> OBUint16PropertyRange: ...
    def set_filter_params(self, arg0: OBLutNoiseRemovalFilterParams) -> None: ...

class MgcNoiseRemovalFilter(Filter):
    def __init__(self, activation_key: str = "") -> None: ...
    def get_filter_params(self) -> OBMgcNoiseRemovalFilterParams: ...
    def get_height_range(self) -> OBUint16PropertyRange: ...
    def get_limit_x_th_range(self) -> OBUint16PropertyRange: ...
    def get_limit_y_th_range(self) -> OBUint16PropertyRange: ...
    def get_margin_x_th_range(self) -> OBUint16PropertyRange: ...
    def get_margin_y_th_range(self) -> OBUint16PropertyRange: ...
    def get_max_radius_range(self) -> OBUint16PropertyRange: ...
    def get_max_width_left_range(self) -> OBUint16PropertyRange: ...
    def get_max_width_right_range(self) -> OBUint16PropertyRange: ...
    def get_width_range(self) -> OBUint16PropertyRange: ...
    def set_filter_params(self, arg0: OBMgcNoiseRemovalFilterParams) -> None: ...

class NoiseRemovalFilter(Filter):
    def __init__(self) -> None: ...
    def get_disp_diff_range(self) -> OBUint16PropertyRange: ...
    def get_filter_params(self) -> OBNoiseRemovalFilterParams: ...
    def get_max_size_range(self) -> OBUint16PropertyRange: ...
    def set_filter_params(self, arg0: OBNoiseRemovalFilterParams) -> None: ...

class OBAccelFullScaleRange:
    """
    Members:

      ACCEL_FS_UNKNOWN

      ACCEL_FS_2g

      ACCEL_FS_4g

      ACCEL_FS_8g

      ACCEL_FS_16g

      ACCEL_FS_3g

      ACCEL_FS_6g

      ACCEL_FS_12g

      ACCEL_FS_24g
    """

    ACCEL_FS_12g: typing.ClassVar[OBAccelFullScaleRange]  # value = <OBAccelFullScaleRange.ACCEL_FS_12g: 7>
    ACCEL_FS_16g: typing.ClassVar[OBAccelFullScaleRange]  # value = <OBAccelFullScaleRange.ACCEL_FS_16g: 4>
    ACCEL_FS_24g: typing.ClassVar[OBAccelFullScaleRange]  # value = <OBAccelFullScaleRange.ACCEL_FS_24g: 8>
    ACCEL_FS_2g: typing.ClassVar[OBAccelFullScaleRange]  # value = <OBAccelFullScaleRange.ACCEL_FS_2g: 1>
    ACCEL_FS_3g: typing.ClassVar[OBAccelFullScaleRange]  # value = <OBAccelFullScaleRange.ACCEL_FS_3g: 5>
    ACCEL_FS_4g: typing.ClassVar[OBAccelFullScaleRange]  # value = <OBAccelFullScaleRange.ACCEL_FS_4g: 2>
    ACCEL_FS_6g: typing.ClassVar[OBAccelFullScaleRange]  # value = <OBAccelFullScaleRange.ACCEL_FS_6g: 6>
    ACCEL_FS_8g: typing.ClassVar[OBAccelFullScaleRange]  # value = <OBAccelFullScaleRange.ACCEL_FS_8g: 3>
    ACCEL_FS_UNKNOWN: typing.ClassVar[OBAccelFullScaleRange]  # value = <OBAccelFullScaleRange.ACCEL_FS_UNKNOWN: -1>
    __members__: typing.ClassVar[
        dict[str, OBAccelFullScaleRange]
    ]  # value = {'ACCEL_FS_UNKNOWN': <OBAccelFullScaleRange.ACCEL_FS_UNKNOWN: -1>, 'ACCEL_FS_2g': <OBAccelFullScaleRange.ACCEL_FS_2g: 1>, 'ACCEL_FS_4g': <OBAccelFullScaleRange.ACCEL_FS_4g: 2>, 'ACCEL_FS_8g': <OBAccelFullScaleRange.ACCEL_FS_8g: 3>, 'ACCEL_FS_16g': <OBAccelFullScaleRange.ACCEL_FS_16g: 4>, 'ACCEL_FS_3g': <OBAccelFullScaleRange.ACCEL_FS_3g: 5>, 'ACCEL_FS_6g': <OBAccelFullScaleRange.ACCEL_FS_6g: 6>, 'ACCEL_FS_12g': <OBAccelFullScaleRange.ACCEL_FS_12g: 7>, 'ACCEL_FS_24g': <OBAccelFullScaleRange.ACCEL_FS_24g: 8>}
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class OBAccelIntrinsic:
    def __init__(self) -> None: ...
    @property
    def bias(self) -> numpy.typing.NDArray[numpy.float64]: ...
    @bias.setter
    def bias(self, arg1: typing.Annotated[numpy.typing.ArrayLike, numpy.float64]) -> None: ...
    @property
    def gravity(self) -> numpy.typing.NDArray[numpy.float64]: ...
    @gravity.setter
    def gravity(self, arg1: typing.Annotated[numpy.typing.ArrayLike, numpy.float64]) -> None: ...
    @property
    def noise_density(self) -> float: ...
    @noise_density.setter
    def noise_density(self, arg0: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def random_walk(self) -> float: ...
    @random_walk.setter
    def random_walk(self, arg0: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def reference_temp(self) -> float: ...
    @reference_temp.setter
    def reference_temp(self, arg0: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def scale_misalignment(self) -> numpy.typing.NDArray[numpy.float64]: ...
    @scale_misalignment.setter
    def scale_misalignment(self, arg1: typing.Annotated[numpy.typing.ArrayLike, numpy.float64]) -> None: ...
    @property
    def temp_slope(self) -> numpy.typing.NDArray[numpy.float64]: ...
    @temp_slope.setter
    def temp_slope(self, arg1: typing.Annotated[numpy.typing.ArrayLike, numpy.float64]) -> None: ...

class OBAccelValue:
    def __init__(self) -> None: ...
    def __repr__(self) -> str: ...
    @property
    def x(self) -> float: ...
    @x.setter
    def x(self, arg0: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def y(self) -> float: ...
    @y.setter
    def y(self, arg0: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def z(self) -> float: ...
    @z.setter
    def z(self, arg0: typing.SupportsFloat | typing.SupportsIndex) -> None: ...

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
    __members__: typing.ClassVar[
        dict[str, OBAlignMode]
    ]  # value = {'DISABLE': <OBAlignMode.DISABLE: 0>, 'HW_MODE': <OBAlignMode.HW_MODE: 1>, 'SW_MODE': <OBAlignMode.SW_MODE: 2>}
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class OBBaselineCalibrationParam:
    def __init__(self) -> None: ...
    @property
    def baseline(self) -> float: ...
    @baseline.setter
    def baseline(self, arg0: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def zpd(self) -> float: ...
    @zpd.setter
    def zpd(self, arg0: typing.SupportsFloat | typing.SupportsIndex) -> None: ...

class OBBoolPropertyRange:
    cur: bool
    default_value: bool
    max: bool
    min: bool
    step: bool
    def __init__(self) -> None: ...

class OBCalibrationParam:
    def __init__(self) -> None: ...
    def get_distortion(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> OBCameraDistortion: ...
    def get_extrinsic(
        self, arg0: typing.SupportsInt | typing.SupportsIndex, arg1: typing.SupportsInt | typing.SupportsIndex
    ) -> OBExtrinsic: ...
    def get_intrinsic(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> OBCameraIntrinsic: ...
    def set_distortion(self, arg0: typing.SupportsInt | typing.SupportsIndex, arg1: OBCameraDistortion) -> None: ...
    def set_extrinsic(
        self,
        arg0: typing.SupportsInt | typing.SupportsIndex,
        arg1: typing.SupportsInt | typing.SupportsIndex,
        arg2: OBExtrinsic,
    ) -> None: ...
    def set_intrinsic(self, arg0: typing.SupportsInt | typing.SupportsIndex, arg1: OBCameraIntrinsic) -> None: ...

class OBCameraDistortion:
    def __init__(self) -> None: ...
    def __repr__(self) -> str: ...
    @property
    def k1(self) -> float: ...
    @k1.setter
    def k1(self, arg0: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def k2(self) -> float: ...
    @k2.setter
    def k2(self, arg0: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def k3(self) -> float: ...
    @k3.setter
    def k3(self, arg0: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def k4(self) -> float: ...
    @k4.setter
    def k4(self, arg0: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def k5(self) -> float: ...
    @k5.setter
    def k5(self, arg0: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def k6(self) -> float: ...
    @k6.setter
    def k6(self, arg0: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def p1(self) -> float: ...
    @p1.setter
    def p1(self, arg0: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def p2(self) -> float: ...
    @p2.setter
    def p2(self, arg0: typing.SupportsFloat | typing.SupportsIndex) -> None: ...

class OBCameraDistortionModel:
    """
    Members:

      NONE

      MODIFIED_BROWN_CONRADY

      INVERSE_BROWN_CONRADY

      BROWN_CONRADY
    """

    BROWN_CONRADY: typing.ClassVar[OBCameraDistortionModel]  # value = <OBCameraDistortionModel.BROWN_CONRADY: 3>
    INVERSE_BROWN_CONRADY: typing.ClassVar[
        OBCameraDistortionModel
    ]  # value = <OBCameraDistortionModel.INVERSE_BROWN_CONRADY: 2>
    MODIFIED_BROWN_CONRADY: typing.ClassVar[
        OBCameraDistortionModel
    ]  # value = <OBCameraDistortionModel.MODIFIED_BROWN_CONRADY: 1>
    NONE: typing.ClassVar[OBCameraDistortionModel]  # value = <OBCameraDistortionModel.NONE: 0>
    __members__: typing.ClassVar[
        dict[str, OBCameraDistortionModel]
    ]  # value = {'NONE': <OBCameraDistortionModel.NONE: 0>, 'MODIFIED_BROWN_CONRADY': <OBCameraDistortionModel.MODIFIED_BROWN_CONRADY: 1>, 'INVERSE_BROWN_CONRADY': <OBCameraDistortionModel.INVERSE_BROWN_CONRADY: 2>, 'BROWN_CONRADY': <OBCameraDistortionModel.BROWN_CONRADY: 3>}
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class OBCameraIntrinsic:
    def __init__(self) -> None: ...
    def __repr__(self) -> str: ...
    @property
    def cx(self) -> float: ...
    @cx.setter
    def cx(self, arg0: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def cy(self) -> float: ...
    @cy.setter
    def cy(self, arg0: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def fx(self) -> float: ...
    @fx.setter
    def fx(self, arg0: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def fy(self) -> float: ...
    @fy.setter
    def fy(self, arg0: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def height(self) -> int: ...
    @height.setter
    def height(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def width(self) -> int: ...
    @width.setter
    def width(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...

class OBCameraParam:
    depth_distortion: OBCameraDistortion
    depth_intrinsic: OBCameraIntrinsic
    rgb_distortion: OBCameraDistortion
    rgb_intrinsic: OBCameraIntrinsic
    transform: OBExtrinsic
    def __init__(self) -> None: ...
    def __repr__(self) -> str: ...

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
    __members__: typing.ClassVar[
        dict[str, OBCmdVersion]
    ]  # value = {'V0': <OBCmdVersion.V0: 0>, 'V1': <OBCmdVersion.V1: 1>, 'V2': <OBCmdVersion.V2: 2>, 'V3': <OBCmdVersion.V3: 3>, 'NONE': <OBCmdVersion.NONE: 65534>, 'INVALID': <OBCmdVersion.INVALID: 65535>}
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class OBColorPoint:
    @staticmethod
    def get_sizeof() -> int: ...
    def __init__(self) -> None: ...
    def __repr__(self) -> str: ...
    @property
    def b(self) -> int: ...
    @b.setter
    def b(self, arg1: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def g(self) -> int: ...
    @g.setter
    def g(self, arg1: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def r(self) -> int: ...
    @r.setter
    def r(self, arg1: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def x(self) -> float: ...
    @x.setter
    def x(self, arg0: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def y(self) -> float: ...
    @y.setter
    def y(self, arg0: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def z(self) -> float: ...
    @z.setter
    def z(self, arg0: typing.SupportsFloat | typing.SupportsIndex) -> None: ...

class OBCommunicationType:
    """
    Members:

      USB

      ETHERNET
    """

    ETHERNET: typing.ClassVar[OBCommunicationType]  # value = <OBCommunicationType.ETHERNET: 1>
    USB: typing.ClassVar[OBCommunicationType]  # value = <OBCommunicationType.USB: 0>
    __members__: typing.ClassVar[
        dict[str, OBCommunicationType]
    ]  # value = {'USB': <OBCommunicationType.USB: 0>, 'ETHERNET': <OBCommunicationType.ETHERNET: 1>}
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class OBCompressionMode:
    """
    Members:

      LOSSLESS

      LOSSY
    """

    LOSSLESS: typing.ClassVar[OBCompressionMode]  # value = <OBCompressionMode.LOSSLESS: 0>
    LOSSY: typing.ClassVar[OBCompressionMode]  # value = <OBCompressionMode.LOSSY: 1>
    __members__: typing.ClassVar[
        dict[str, OBCompressionMode]
    ]  # value = {'LOSSLESS': <OBCompressionMode.LOSSLESS: 0>, 'LOSSY': <OBCompressionMode.LOSSY: 1>}
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class OBCompressionParams:
    def __init__(self) -> None: ...
    @property
    def threshold(self) -> int: ...
    @threshold.setter
    def threshold(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...

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
    __members__: typing.ClassVar[
        dict[str, OBConvertFormat]
    ]  # value = {'YUYV_TO_RGB888': <OBConvertFormat.YUYV_TO_RGB888: 0>, 'I420_TO_RGB888': <OBConvertFormat.I420_TO_RGB888: 1>, 'NV21_TO_RGB888': <OBConvertFormat.NV21_TO_RGB888: 2>, 'NV12_TO_RGB888': <OBConvertFormat.NV12_TO_RGB888: 3>, 'MJPG_TO_I420': <OBConvertFormat.MJPG_TO_I420: 4>, 'RGB888_TO_BGR': <OBConvertFormat.RGB888_TO_BGR: 5>, 'MJPG_TO_NV21': <OBConvertFormat.MJPG_TO_NV21: 6>, 'MJPG_TO_RGB888': <OBConvertFormat.MJPG_TO_RGB888: 7>, 'MJPG_TO_BGR888': <OBConvertFormat.MJPG_TO_BGR888: 8>, 'MJPG_TO_BGRA': <OBConvertFormat.MJPG_TO_BGRA: 9>, 'UYVY_TO_RGB888': <OBConvertFormat.UYVY_TO_RGB888: 10>, 'BGR_TO_RGB': <OBConvertFormat.BGR_TO_RGB: 11>}
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class OBCoordinateSystemType:
    """
    Members:

      LEFT_HAND

      RIGHT_HAND
    """

    LEFT_HAND: typing.ClassVar[OBCoordinateSystemType]  # value = <OBCoordinateSystemType.LEFT_HAND: 0>
    RIGHT_HAND: typing.ClassVar[OBCoordinateSystemType]  # value = <OBCoordinateSystemType.RIGHT_HAND: 1>
    __members__: typing.ClassVar[
        dict[str, OBCoordinateSystemType]
    ]  # value = {'LEFT_HAND': <OBCoordinateSystemType.LEFT_HAND: 0>, 'RIGHT_HAND': <OBCoordinateSystemType.RIGHT_HAND: 1>}
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class OBDCPowerState:
    """
    Members:

      OFF

      ON
    """

    OFF: typing.ClassVar[OBDCPowerState]  # value = <OBDCPowerState.OFF: 0>
    ON: typing.ClassVar[OBDCPowerState]  # value = <OBDCPowerState.ON: 1>
    __members__: typing.ClassVar[
        dict[str, OBDCPowerState]
    ]  # value = {'OFF': <OBDCPowerState.OFF: 0>, 'ON': <OBDCPowerState.ON: 1>}
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class OBDDONoiseRemovalType:
    """
    Members:

      LUT

      OVERALL
    """

    LUT: typing.ClassVar[OBDDONoiseRemovalType]  # value = <OBDDONoiseRemovalType.LUT: 0>
    OVERALL: typing.ClassVar[OBDDONoiseRemovalType]  # value = <OBDDONoiseRemovalType.OVERALL: 1>
    __members__: typing.ClassVar[
        dict[str, OBDDONoiseRemovalType]
    ]  # value = {'LUT': <OBDDONoiseRemovalType.LUT: 0>, 'OVERALL': <OBDDONoiseRemovalType.OVERALL: 1>}
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class OBDataTranState:
    """
    Members:

      STOPPED

      DONE

      VERIFYING

      TRANSFERRING

      ERR_BUSY

      ERR_UNSUPPORTED

      ERR_TRAN_FAILED

      ERR_VERIFY_FAILED

      ERR_OTHER
    """

    DONE: typing.ClassVar[OBDataTranState]  # value = <OBDataTranState.DONE: 2>
    ERR_BUSY: typing.ClassVar[OBDataTranState]  # value = <OBDataTranState.ERR_BUSY: -1>
    ERR_OTHER: typing.ClassVar[OBDataTranState]  # value = <OBDataTranState.ERR_OTHER: -5>
    ERR_TRAN_FAILED: typing.ClassVar[OBDataTranState]  # value = <OBDataTranState.ERR_TRAN_FAILED: -3>
    ERR_UNSUPPORTED: typing.ClassVar[OBDataTranState]  # value = <OBDataTranState.ERR_UNSUPPORTED: -2>
    ERR_VERIFY_FAILED: typing.ClassVar[OBDataTranState]  # value = <OBDataTranState.ERR_VERIFY_FAILED: -4>
    STOPPED: typing.ClassVar[OBDataTranState]  # value = <OBDataTranState.STOPPED: 3>
    TRANSFERRING: typing.ClassVar[OBDataTranState]  # value = <OBDataTranState.TRANSFERRING: 0>
    VERIFYING: typing.ClassVar[OBDataTranState]  # value = <OBDataTranState.VERIFYING: 1>
    __members__: typing.ClassVar[
        dict[str, OBDataTranState]
    ]  # value = {'STOPPED': <OBDataTranState.STOPPED: 3>, 'DONE': <OBDataTranState.DONE: 2>, 'VERIFYING': <OBDataTranState.VERIFYING: 1>, 'TRANSFERRING': <OBDataTranState.TRANSFERRING: 0>, 'ERR_BUSY': <OBDataTranState.ERR_BUSY: -1>, 'ERR_UNSUPPORTED': <OBDataTranState.ERR_UNSUPPORTED: -2>, 'ERR_TRAN_FAILED': <OBDataTranState.ERR_TRAN_FAILED: -3>, 'ERR_VERIFY_FAILED': <OBDataTranState.ERR_VERIFY_FAILED: -4>, 'ERR_OTHER': <OBDataTranState.ERR_OTHER: -5>}
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

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
    __members__: typing.ClassVar[
        dict[str, OBDepthCroppingMode]
    ]  # value = {'AUTO': <OBDepthCroppingMode.AUTO: 0>, 'CLOSE': <OBDepthCroppingMode.CLOSE: 1>, 'OPEN': <OBDepthCroppingMode.OPEN: 2>}
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

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
    ZERO_POINT_EIGHT_MM: typing.ClassVar[
        OBDepthPrecisionLevel
    ]  # value = <OBDepthPrecisionLevel.ZERO_POINT_EIGHT_MM: 1>
    ZERO_POINT_FOUR_MM: typing.ClassVar[OBDepthPrecisionLevel]  # value = <OBDepthPrecisionLevel.ZERO_POINT_FOUR_MM: 2>
    ZERO_POINT_ONE_MM: typing.ClassVar[OBDepthPrecisionLevel]  # value = <OBDepthPrecisionLevel.ZERO_POINT_ONE_MM: 3>
    ZERO_POINT_TWO_MM: typing.ClassVar[OBDepthPrecisionLevel]  # value = <OBDepthPrecisionLevel.ZERO_POINT_TWO_MM: 4>
    __members__: typing.ClassVar[
        dict[str, OBDepthPrecisionLevel]
    ]  # value = {'ONE_MM': <OBDepthPrecisionLevel.ONE_MM: 0>, 'ZERO_POINT_EIGHT_MM': <OBDepthPrecisionLevel.ZERO_POINT_EIGHT_MM: 1>, 'ZERO_POINT_FOUR_MM': <OBDepthPrecisionLevel.ZERO_POINT_FOUR_MM: 2>, 'ZERO_POINT_TWO_MM': <OBDepthPrecisionLevel.ZERO_POINT_TWO_MM: 4>, 'ZERO_POINT_ONE_MM': <OBDepthPrecisionLevel.ZERO_POINT_ONE_MM: 3>}
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class OBDepthWorkMode:
    __hash__: typing.ClassVar[None] = None
    name: str
    tag: OBDepthWorkModeTag
    def __eq__(self, arg0: OBDepthWorkMode) -> bool: ...
    def __init__(self) -> None: ...
    def __repr__(self) -> str: ...
    @property
    def checksum(self) -> numpy.typing.NDArray[numpy.uint8]: ...
    @checksum.setter
    def checksum(self, arg1: typing.Annotated[numpy.typing.ArrayLike, numpy.uint8]) -> None: ...

class OBDepthWorkModeList:
    def __getitem__(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> OBDepthWorkMode: ...
    def __len__(self) -> int: ...
    def get_count(self) -> int:
        """
        Get the number of OBDepthWorkMode objects in the list
        """

    def get_depth_work_mode_by_index(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> OBDepthWorkMode:
        """
        Get the OBDepthWorkMode object at the specified index
        """

class OBDepthWorkModeTag:
    """
    Members:

      OB_DEVICE_DEPTH_WORK_MODE

      OB_CUSTOM_DEPTH_WORK_MODE
    """

    OB_CUSTOM_DEPTH_WORK_MODE: typing.ClassVar[
        OBDepthWorkModeTag
    ]  # value = <OBDepthWorkModeTag.OB_CUSTOM_DEPTH_WORK_MODE: 1>
    OB_DEVICE_DEPTH_WORK_MODE: typing.ClassVar[
        OBDepthWorkModeTag
    ]  # value = <OBDepthWorkModeTag.OB_DEVICE_DEPTH_WORK_MODE: 0>
    __members__: typing.ClassVar[
        dict[str, OBDepthWorkModeTag]
    ]  # value = {'OB_DEVICE_DEPTH_WORK_MODE': <OBDepthWorkModeTag.OB_DEVICE_DEPTH_WORK_MODE: 0>, 'OB_CUSTOM_DEPTH_WORK_MODE': <OBDepthWorkModeTag.OB_CUSTOM_DEPTH_WORK_MODE: 1>}
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class OBDeviceAccessMode:
    """
    Members:

      OB_DEVICE_ACCESS_DENIED

      OB_DEVICE_EXCLUSIVE_ACCESS

      OB_DEVICE_CONTROL_ACCESS

      OB_DEVICE_MONITOR_ACCESS

      OB_DEVICE_DEFAULT_ACCESS
    """

    OB_DEVICE_ACCESS_DENIED: typing.ClassVar[
        OBDeviceAccessMode
    ]  # value = <OBDeviceAccessMode.OB_DEVICE_ACCESS_DENIED: 0>
    OB_DEVICE_CONTROL_ACCESS: typing.ClassVar[
        OBDeviceAccessMode
    ]  # value = <OBDeviceAccessMode.OB_DEVICE_CONTROL_ACCESS: 2>
    OB_DEVICE_DEFAULT_ACCESS: typing.ClassVar[
        OBDeviceAccessMode
    ]  # value = <OBDeviceAccessMode.OB_DEVICE_DEFAULT_ACCESS: 4>
    OB_DEVICE_EXCLUSIVE_ACCESS: typing.ClassVar[
        OBDeviceAccessMode
    ]  # value = <OBDeviceAccessMode.OB_DEVICE_EXCLUSIVE_ACCESS: 1>
    OB_DEVICE_MONITOR_ACCESS: typing.ClassVar[
        OBDeviceAccessMode
    ]  # value = <OBDeviceAccessMode.OB_DEVICE_MONITOR_ACCESS: 3>
    __members__: typing.ClassVar[
        dict[str, OBDeviceAccessMode]
    ]  # value = {'OB_DEVICE_ACCESS_DENIED': <OBDeviceAccessMode.OB_DEVICE_ACCESS_DENIED: 0>, 'OB_DEVICE_EXCLUSIVE_ACCESS': <OBDeviceAccessMode.OB_DEVICE_EXCLUSIVE_ACCESS: 1>, 'OB_DEVICE_CONTROL_ACCESS': <OBDeviceAccessMode.OB_DEVICE_CONTROL_ACCESS: 2>, 'OB_DEVICE_MONITOR_ACCESS': <OBDeviceAccessMode.OB_DEVICE_MONITOR_ACCESS: 3>, 'OB_DEVICE_DEFAULT_ACCESS': <OBDeviceAccessMode.OB_DEVICE_DEFAULT_ACCESS: 4>}
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class OBDeviceDevelopmentMode:
    """
    Members:

      NORMAL

      DEVELOPMENT
    """

    DEVELOPMENT: typing.ClassVar[OBDeviceDevelopmentMode]  # value = <OBDeviceDevelopmentMode.DEVELOPMENT: 1>
    NORMAL: typing.ClassVar[OBDeviceDevelopmentMode]  # value = <OBDeviceDevelopmentMode.NORMAL: 0>
    __members__: typing.ClassVar[
        dict[str, OBDeviceDevelopmentMode]
    ]  # value = {'NORMAL': <OBDeviceDevelopmentMode.NORMAL: 0>, 'DEVELOPMENT': <OBDeviceDevelopmentMode.DEVELOPMENT: 1>}
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class OBDeviceIpAddrConfig:
    address: str
    gateway: str
    netmask: str
    def __init__(self) -> None: ...
    @property
    def dhcp(self) -> int: ...
    @dhcp.setter
    def dhcp(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...

class OBDeviceSyncConfig:
    mode: OBSyncMode
    def __init__(self) -> None: ...
    @property
    def device_index(self) -> int: ...
    @device_index.setter
    def device_index(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def device_trigger_signal_out_delay(self) -> int: ...
    @device_trigger_signal_out_delay.setter
    def device_trigger_signal_out_delay(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def device_trigger_signal_out_polarity(self) -> int: ...
    @device_trigger_signal_out_polarity.setter
    def device_trigger_signal_out_polarity(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def ir_trigger_signal_delay(self) -> int: ...
    @ir_trigger_signal_delay.setter
    def ir_trigger_signal_delay(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def mcu_trigger_frequency(self) -> int: ...
    @mcu_trigger_frequency.setter
    def mcu_trigger_frequency(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def rgb_trigger_signal_delay(self) -> int: ...
    @rgb_trigger_signal_delay.setter
    def rgb_trigger_signal_delay(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...

class OBDeviceTemperature:
    def __init__(self) -> None: ...
    def __repr__(self) -> str: ...
    @property
    def chip_bottom_temperature(self) -> float: ...
    @chip_bottom_temperature.setter
    def chip_bottom_temperature(self, arg0: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def chip_top_temperature(self) -> float: ...
    @chip_top_temperature.setter
    def chip_top_temperature(self, arg0: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def cpu_temperature(self) -> float: ...
    @cpu_temperature.setter
    def cpu_temperature(self, arg0: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def imu_temperature(self) -> float: ...
    @imu_temperature.setter
    def imu_temperature(self, arg0: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def ir_left_temperature(self) -> float: ...
    @ir_left_temperature.setter
    def ir_left_temperature(self, arg0: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def ir_right_temperature(self) -> float: ...
    @ir_right_temperature.setter
    def ir_right_temperature(self, arg0: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def ir_temperature(self) -> float: ...
    @ir_temperature.setter
    def ir_temperature(self, arg0: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def laser_temperature(self) -> float: ...
    @laser_temperature.setter
    def laser_temperature(self, arg0: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def main_board_temperature(self) -> float: ...
    @main_board_temperature.setter
    def main_board_temperature(self, arg0: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def rgb_temperature(self) -> float: ...
    @rgb_temperature.setter
    def rgb_temperature(self, arg0: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def tec_temperature(self) -> float: ...
    @tec_temperature.setter
    def tec_temperature(self, arg0: typing.SupportsFloat | typing.SupportsIndex) -> None: ...

class OBDeviceTimestampResetConfig:
    enable: bool
    def __init__(self) -> None: ...
    @property
    def timestamp_reset_delay_us(self) -> int: ...
    @timestamp_reset_delay_us.setter
    def timestamp_reset_delay_us(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...

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
    __members__: typing.ClassVar[
        dict[str, OBDeviceType]
    ]  # value = {'LIGHT_MONOCULAR': <OBDeviceType.LIGHT_MONOCULAR: 0>, 'LIGHT_BINOCULAR': <OBDeviceType.LIGHT_BINOCULAR: 1>, 'TIME_OF_FLIGHT': <OBDeviceType.TIME_OF_FLIGHT: 2>}
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class OBEdgeNoiseRemovalFilterParams:
    enable_direction: bool
    def __init__(self) -> None: ...
    def __repr__(self) -> str: ...
    @property
    def height(self) -> int: ...
    @height.setter
    def height(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def limit_x_th(self) -> int: ...
    @limit_x_th.setter
    def limit_x_th(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def limit_y_th(self) -> int: ...
    @limit_y_th.setter
    def limit_y_th(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def margin_x_th(self) -> int: ...
    @margin_x_th.setter
    def margin_x_th(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def margin_y_th(self) -> int: ...
    @margin_y_th.setter
    def margin_y_th(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def width(self) -> int: ...
    @width.setter
    def width(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...

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
    __members__: typing.ClassVar[
        dict[str, OBEdgeNoiseRemovalType]
    ]  # value = {'MG_FILTER': <OBEdgeNoiseRemovalType.MG_FILTER: 0>, 'MGH_FILTER': <OBEdgeNoiseRemovalType.MGH_FILTER: 1>, 'MGA_FILTER': <OBEdgeNoiseRemovalType.MGA_FILTER: 2>, 'MGC_FILTER': <OBEdgeNoiseRemovalType.MGC_FILTER: 3>}
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class OBError(Exception):
    pass

class OBErrorDetails:
    def get_name(self) -> str: ...
    def get_status(self) -> OBStatus: ...
    def get_type(self) -> OBException: ...
    def what(self) -> str: ...

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

      UNSUPPORTED_OPERATION

      ACCESS_DENIED

      DEVICE_UNAVAILABLE

      INVALID_DATA

      NOT_FOUND

      RESOURCE_BUSY
    """

    ACCESS_DENIED: typing.ClassVar[OBException]  # value = <OBException.ACCESS_DENIED: 10>
    CAMERA_DISCONNECTED: typing.ClassVar[OBException]  # value = <OBException.CAMERA_DISCONNECTED: 2>
    DEVICE_UNAVAILABLE: typing.ClassVar[OBException]  # value = <OBException.DEVICE_UNAVAILABLE: 11>
    INVALID_DATA: typing.ClassVar[OBException]  # value = <OBException.INVALID_DATA: 12>
    INVALID_VALUE: typing.ClassVar[OBException]  # value = <OBException.INVALID_VALUE: 4>
    IO_ERROR: typing.ClassVar[OBException]  # value = <OBException.IO_ERROR: 7>
    NOT_FOUND: typing.ClassVar[OBException]  # value = <OBException.NOT_FOUND: 13>
    NOT_IMPLEMENTED: typing.ClassVar[OBException]  # value = <OBException.NOT_IMPLEMENTED: 6>
    PLATFORM: typing.ClassVar[OBException]  # value = <OBException.PLATFORM: 3>
    RESOURCE_BUSY: typing.ClassVar[OBException]  # value = <OBException.RESOURCE_BUSY: 14>
    UNKNOWN: typing.ClassVar[OBException]  # value = <OBException.UNKNOWN: 0>
    UNSUPPORTED_OPERATION: typing.ClassVar[OBException]  # value = <OBException.UNSUPPORTED_OPERATION: 9>
    WRONG_API_CALL_SEQUENCE: typing.ClassVar[OBException]  # value = <OBException.WRONG_API_CALL_SEQUENCE: 5>
    __members__: typing.ClassVar[
        dict[str, OBException]
    ]  # value = {'UNKNOWN': <OBException.UNKNOWN: 0>, 'CAMERA_DISCONNECTED': <OBException.CAMERA_DISCONNECTED: 2>, 'PLATFORM': <OBException.PLATFORM: 3>, 'INVALID_VALUE': <OBException.INVALID_VALUE: 4>, 'WRONG_API_CALL_SEQUENCE': <OBException.WRONG_API_CALL_SEQUENCE: 5>, 'NOT_IMPLEMENTED': <OBException.NOT_IMPLEMENTED: 6>, 'IO_ERROR': <OBException.IO_ERROR: 7>, 'UNSUPPORTED_OPERATION': <OBException.UNSUPPORTED_OPERATION: 9>, 'ACCESS_DENIED': <OBException.ACCESS_DENIED: 10>, 'DEVICE_UNAVAILABLE': <OBException.DEVICE_UNAVAILABLE: 11>, 'INVALID_DATA': <OBException.INVALID_DATA: 12>, 'NOT_FOUND': <OBException.NOT_FOUND: 13>, 'RESOURCE_BUSY': <OBException.RESOURCE_BUSY: 14>}
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class OBExtrinsic:
    def __init__(self) -> None: ...
    def __repr__(self) -> str: ...
    @property
    def rot(self) -> numpy.typing.NDArray[numpy.float32]: ...
    @rot.setter
    def rot(self, arg1: typing.Annotated[numpy.typing.ArrayLike, numpy.float32]) -> None: ...
    @property
    def transform(self) -> numpy.typing.NDArray[numpy.float32]: ...
    @transform.setter
    def transform(self, arg1: typing.Annotated[numpy.typing.ArrayLike, numpy.float32]) -> None: ...

class OBFileTranState:
    """
    Members:

      TRANSFER

      DONE

      PREPARING

      ERR_DDR

      ERR_NOT_ENOUGH_SPACE

      ERR_PATH_NOT_WRITABLE

      ERR_MD5_ERROR

      ERR_WRITE_FLASH_ERROR

      ERR_TIMEOUT
    """

    DONE: typing.ClassVar[OBFileTranState]  # value = <OBFileTranState.DONE: 1>
    ERR_DDR: typing.ClassVar[OBFileTranState]  # value = <OBFileTranState.ERR_DDR: -1>
    ERR_MD5_ERROR: typing.ClassVar[OBFileTranState]  # value = <OBFileTranState.ERR_MD5_ERROR: -4>
    ERR_NOT_ENOUGH_SPACE: typing.ClassVar[OBFileTranState]  # value = <OBFileTranState.ERR_NOT_ENOUGH_SPACE: -2>
    ERR_PATH_NOT_WRITABLE: typing.ClassVar[OBFileTranState]  # value = <OBFileTranState.ERR_PATH_NOT_WRITABLE: -3>
    ERR_TIMEOUT: typing.ClassVar[OBFileTranState]  # value = <OBFileTranState.ERR_TIMEOUT: -6>
    ERR_WRITE_FLASH_ERROR: typing.ClassVar[OBFileTranState]  # value = <OBFileTranState.ERR_WRITE_FLASH_ERROR: -5>
    PREPARING: typing.ClassVar[OBFileTranState]  # value = <OBFileTranState.PREPARING: 0>
    TRANSFER: typing.ClassVar[OBFileTranState]  # value = <OBFileTranState.TRANSFER: 2>
    __members__: typing.ClassVar[
        dict[str, OBFileTranState]
    ]  # value = {'TRANSFER': <OBFileTranState.TRANSFER: 2>, 'DONE': <OBFileTranState.DONE: 1>, 'PREPARING': <OBFileTranState.PREPARING: 0>, 'ERR_DDR': <OBFileTranState.ERR_DDR: -1>, 'ERR_NOT_ENOUGH_SPACE': <OBFileTranState.ERR_NOT_ENOUGH_SPACE: -2>, 'ERR_PATH_NOT_WRITABLE': <OBFileTranState.ERR_PATH_NOT_WRITABLE: -3>, 'ERR_MD5_ERROR': <OBFileTranState.ERR_MD5_ERROR: -4>, 'ERR_WRITE_FLASH_ERROR': <OBFileTranState.ERR_WRITE_FLASH_ERROR: -5>, 'ERR_TIMEOUT': <OBFileTranState.ERR_TIMEOUT: -6>}
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class OBFilterConfigSchemaItem:
    type: OBFilterConfigValueType
    def __init__(self) -> None: ...
    @property
    def default(self) -> float: ...
    @default.setter
    def default(self, arg0: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def desc(self) -> str: ...
    @property
    def max(self) -> float: ...
    @max.setter
    def max(self, arg0: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def min(self) -> float: ...
    @min.setter
    def min(self, arg0: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def name(self) -> str: ...
    @property
    def step(self) -> float: ...
    @step.setter
    def step(self, arg0: typing.SupportsFloat | typing.SupportsIndex) -> None: ...

class OBFilterConfigValueType:
    """
    Members:

      INVALID

      INT

      FLOAT

      BOOLEAN
    """

    BOOLEAN: typing.ClassVar[OBFilterConfigValueType]  # value = <OBFilterConfigValueType.BOOLEAN: 2>
    FLOAT: typing.ClassVar[OBFilterConfigValueType]  # value = <OBFilterConfigValueType.FLOAT: 1>
    INT: typing.ClassVar[OBFilterConfigValueType]  # value = <OBFilterConfigValueType.INT: 0>
    INVALID: typing.ClassVar[OBFilterConfigValueType]  # value = <OBFilterConfigValueType.INVALID: -1>
    __members__: typing.ClassVar[
        dict[str, OBFilterConfigValueType]
    ]  # value = {'INVALID': <OBFilterConfigValueType.INVALID: -1>, 'INT': <OBFilterConfigValueType.INT: 0>, 'FLOAT': <OBFilterConfigValueType.FLOAT: 1>, 'BOOLEAN': <OBFilterConfigValueType.BOOLEAN: 2>}
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class OBFilterList:
    def __getitem__(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> Filter: ...
    def __len__(self) -> int: ...
    def get_count(self) -> int: ...
    def get_filter(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> Filter: ...

class OBFloatPropertyRange:
    def __init__(self) -> None: ...
    @property
    def current(self) -> float: ...
    @current.setter
    def current(self, arg0: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def default_value(self) -> float: ...
    @default_value.setter
    def default_value(self, arg0: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def max(self) -> float: ...
    @max.setter
    def max(self, arg0: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def min(self) -> float: ...
    @min.setter
    def min(self, arg0: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def step(self) -> float: ...
    @step.setter
    def step(self, arg0: typing.SupportsFloat | typing.SupportsIndex) -> None: ...

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

      Z16

      YV12

      BA81

      RGBA

      BYR2

      RW16

      Y12C4

      LIDAR_POINT

      LIDAR_SPHERE_POINT

      LIDAR_SCAN

      LIDAR_CALIBRATION
    """

    ACCEL: typing.ClassVar[OBFormat]  # value = <OBFormat.ACCEL: 16>
    BA81: typing.ClassVar[OBFormat]  # value = <OBFormat.BA81: 30>
    BGR: typing.ClassVar[OBFormat]  # value = <OBFormat.BGR: 23>
    BGRA: typing.ClassVar[OBFormat]  # value = <OBFormat.BGRA: 25>
    BYR2: typing.ClassVar[OBFormat]  # value = <OBFormat.BYR2: 32>
    COMPRESSED: typing.ClassVar[OBFormat]  # value = <OBFormat.COMPRESSED: 26>
    GRAY: typing.ClassVar[OBFormat]  # value = <OBFormat.GRAY: 13>
    GYRO: typing.ClassVar[OBFormat]  # value = <OBFormat.GYRO: 17>
    H264: typing.ClassVar[OBFormat]  # value = <OBFormat.H264: 6>
    H265: typing.ClassVar[OBFormat]  # value = <OBFormat.H265: 7>
    HEVC: typing.ClassVar[OBFormat]  # value = <OBFormat.HEVC: 14>
    I420: typing.ClassVar[OBFormat]  # value = <OBFormat.I420: 15>
    LIDAR_CALIBRATION: typing.ClassVar[OBFormat]  # value = <OBFormat.LIDAR_CALIBRATION: 38>
    LIDAR_POINT: typing.ClassVar[OBFormat]  # value = <OBFormat.LIDAR_POINT: 35>
    LIDAR_SCAN: typing.ClassVar[OBFormat]  # value = <OBFormat.LIDAR_SCAN: 37>
    LIDAR_SPHERE_POINT: typing.ClassVar[OBFormat]  # value = <OBFormat.LIDAR_SPHERE_POINT: 36>
    MJPG: typing.ClassVar[OBFormat]  # value = <OBFormat.MJPG: 5>
    NV12: typing.ClassVar[OBFormat]  # value = <OBFormat.NV12: 3>
    NV21: typing.ClassVar[OBFormat]  # value = <OBFormat.NV21: 4>
    POINT: typing.ClassVar[OBFormat]  # value = <OBFormat.POINT: 19>
    RGB: typing.ClassVar[OBFormat]  # value = <OBFormat.RGB: 22>
    RGBA: typing.ClassVar[OBFormat]  # value = <OBFormat.RGBA: 31>
    RGB_POINT: typing.ClassVar[OBFormat]  # value = <OBFormat.RGB_POINT: 20>
    RLE: typing.ClassVar[OBFormat]  # value = <OBFormat.RLE: 21>
    RVL: typing.ClassVar[OBFormat]  # value = <OBFormat.RVL: 27>
    RW16: typing.ClassVar[OBFormat]  # value = <OBFormat.RW16: 33>
    UNKNOWN_FORMAT: typing.ClassVar[OBFormat]  # value = <OBFormat.UNKNOWN_FORMAT: -1>
    UYVY: typing.ClassVar[OBFormat]  # value = <OBFormat.UYVY: 2>
    Y10: typing.ClassVar[OBFormat]  # value = <OBFormat.Y10: 10>
    Y11: typing.ClassVar[OBFormat]  # value = <OBFormat.Y11: 11>
    Y12: typing.ClassVar[OBFormat]  # value = <OBFormat.Y12: 12>
    Y12C4: typing.ClassVar[OBFormat]  # value = <OBFormat.Y12C4: 34>
    Y14: typing.ClassVar[OBFormat]  # value = <OBFormat.Y14: 24>
    Y16: typing.ClassVar[OBFormat]  # value = <OBFormat.Y16: 8>
    Y8: typing.ClassVar[OBFormat]  # value = <OBFormat.Y8: 9>
    YUY2: typing.ClassVar[OBFormat]  # value = <OBFormat.YUY2: 1>
    YUYV: typing.ClassVar[OBFormat]  # value = <OBFormat.YUYV: 0>
    YV12: typing.ClassVar[OBFormat]  # value = <OBFormat.YV12: 29>
    Z16: typing.ClassVar[OBFormat]  # value = <OBFormat.Z16: 28>
    __members__: typing.ClassVar[
        dict[str, OBFormat]
    ]  # value = {'UNKNOWN_FORMAT': <OBFormat.UNKNOWN_FORMAT: -1>, 'YUYV': <OBFormat.YUYV: 0>, 'YUY2': <OBFormat.YUY2: 1>, 'UYVY': <OBFormat.UYVY: 2>, 'NV12': <OBFormat.NV12: 3>, 'NV21': <OBFormat.NV21: 4>, 'MJPG': <OBFormat.MJPG: 5>, 'H264': <OBFormat.H264: 6>, 'H265': <OBFormat.H265: 7>, 'Y16': <OBFormat.Y16: 8>, 'Y8': <OBFormat.Y8: 9>, 'Y10': <OBFormat.Y10: 10>, 'Y11': <OBFormat.Y11: 11>, 'Y12': <OBFormat.Y12: 12>, 'GRAY': <OBFormat.GRAY: 13>, 'HEVC': <OBFormat.HEVC: 14>, 'I420': <OBFormat.I420: 15>, 'ACCEL': <OBFormat.ACCEL: 16>, 'GYRO': <OBFormat.GYRO: 17>, 'POINT': <OBFormat.POINT: 19>, 'RGB_POINT': <OBFormat.RGB_POINT: 20>, 'RLE': <OBFormat.RLE: 21>, 'RGB': <OBFormat.RGB: 22>, 'BGR': <OBFormat.BGR: 23>, 'Y14': <OBFormat.Y14: 24>, 'BGRA': <OBFormat.BGRA: 25>, 'COMPRESSED': <OBFormat.COMPRESSED: 26>, 'RVL': <OBFormat.RVL: 27>, 'Z16': <OBFormat.Z16: 28>, 'YV12': <OBFormat.YV12: 29>, 'BA81': <OBFormat.BA81: 30>, 'RGBA': <OBFormat.RGBA: 31>, 'BYR2': <OBFormat.BYR2: 32>, 'RW16': <OBFormat.RW16: 33>, 'Y12C4': <OBFormat.Y12C4: 34>, 'LIDAR_POINT': <OBFormat.LIDAR_POINT: 35>, 'LIDAR_SPHERE_POINT': <OBFormat.LIDAR_SPHERE_POINT: 36>, 'LIDAR_SCAN': <OBFormat.LIDAR_SCAN: 37>, 'LIDAR_CALIBRATION': <OBFormat.LIDAR_CALIBRATION: 38>}
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class OBFrameAggregateOutputMode:
    """
    Members:

      FULL_FRAME_REQUIRE

      COLOR_FRAME_REQUIRE

      ANY_SITUATION

      DISABLE
    """

    ANY_SITUATION: typing.ClassVar[OBFrameAggregateOutputMode]  # value = <OBFrameAggregateOutputMode.ANY_SITUATION: 2>
    COLOR_FRAME_REQUIRE: typing.ClassVar[
        OBFrameAggregateOutputMode
    ]  # value = <OBFrameAggregateOutputMode.COLOR_FRAME_REQUIRE: 1>
    DISABLE: typing.ClassVar[OBFrameAggregateOutputMode]  # value = <OBFrameAggregateOutputMode.DISABLE: 3>
    FULL_FRAME_REQUIRE: typing.ClassVar[
        OBFrameAggregateOutputMode
    ]  # value = <OBFrameAggregateOutputMode.FULL_FRAME_REQUIRE: 0>
    __members__: typing.ClassVar[
        dict[str, OBFrameAggregateOutputMode]
    ]  # value = {'FULL_FRAME_REQUIRE': <OBFrameAggregateOutputMode.FULL_FRAME_REQUIRE: 0>, 'COLOR_FRAME_REQUIRE': <OBFrameAggregateOutputMode.COLOR_FRAME_REQUIRE: 1>, 'ANY_SITUATION': <OBFrameAggregateOutputMode.ANY_SITUATION: 2>, 'DISABLE': <OBFrameAggregateOutputMode.DISABLE: 3>}
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

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

      DISPARITY_SEARCH_OFFSET

      DISPARITY_SEARCH_RANGE

      COUNT
    """

    ACTUAL_FRAME_RATE: typing.ClassVar[OBFrameMetadataType]  # value = <OBFrameMetadataType.ACTUAL_FRAME_RATE: 18>
    AE_ROI_BOTTOM: typing.ClassVar[OBFrameMetadataType]  # value = <OBFrameMetadataType.AE_ROI_BOTTOM: 23>
    AE_ROI_LEFT: typing.ClassVar[OBFrameMetadataType]  # value = <OBFrameMetadataType.AE_ROI_LEFT: 20>
    AE_ROI_RIGHT: typing.ClassVar[OBFrameMetadataType]  # value = <OBFrameMetadataType.AE_ROI_RIGHT: 22>
    AE_ROI_TOP: typing.ClassVar[OBFrameMetadataType]  # value = <OBFrameMetadataType.AE_ROI_TOP: 21>
    AUTO_EXPOSURE: typing.ClassVar[OBFrameMetadataType]  # value = <OBFrameMetadataType.AUTO_EXPOSURE: 3>
    AUTO_WHITE_BALANCE: typing.ClassVar[OBFrameMetadataType]  # value = <OBFrameMetadataType.AUTO_WHITE_BALANCE: 6>
    BACKLIGHT_COMPENSATION: typing.ClassVar[
        OBFrameMetadataType
    ]  # value = <OBFrameMetadataType.BACKLIGHT_COMPENSATION: 12>
    BRIGHTNESS: typing.ClassVar[OBFrameMetadataType]  # value = <OBFrameMetadataType.BRIGHTNESS: 8>
    CONTRAST: typing.ClassVar[OBFrameMetadataType]  # value = <OBFrameMetadataType.CONTRAST: 9>
    COUNT: typing.ClassVar[OBFrameMetadataType]  # value = <OBFrameMetadataType.COUNT: 34>
    DISPARITY_SEARCH_OFFSET: typing.ClassVar[
        OBFrameMetadataType
    ]  # value = <OBFrameMetadataType.DISPARITY_SEARCH_OFFSET: 32>
    DISPARITY_SEARCH_RANGE: typing.ClassVar[
        OBFrameMetadataType
    ]  # value = <OBFrameMetadataType.DISPARITY_SEARCH_RANGE: 33>
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
    LOW_LIGHT_COMPENSATION: typing.ClassVar[
        OBFrameMetadataType
    ]  # value = <OBFrameMetadataType.LOW_LIGHT_COMPENSATION: 16>
    MANUAL_WHITE_BALANCE: typing.ClassVar[OBFrameMetadataType]  # value = <OBFrameMetadataType.MANUAL_WHITE_BALANCE: 17>
    POWER_LINE_FREQUENCY: typing.ClassVar[OBFrameMetadataType]  # value = <OBFrameMetadataType.POWER_LINE_FREQUENCY: 15>
    SATURATION: typing.ClassVar[OBFrameMetadataType]  # value = <OBFrameMetadataType.SATURATION: 10>
    SENSOR_TIMESTAMP: typing.ClassVar[OBFrameMetadataType]  # value = <OBFrameMetadataType.SENSOR_TIMESTAMP: 1>
    SHARPNESS: typing.ClassVar[OBFrameMetadataType]  # value = <OBFrameMetadataType.SHARPNESS: 11>
    TIMESTAMP: typing.ClassVar[OBFrameMetadataType]  # value = <OBFrameMetadataType.TIMESTAMP: 0>
    WHITE_BALANCE: typing.ClassVar[OBFrameMetadataType]  # value = <OBFrameMetadataType.WHITE_BALANCE: 7>
    __members__: typing.ClassVar[
        dict[str, OBFrameMetadataType]
    ]  # value = {'TIMESTAMP': <OBFrameMetadataType.TIMESTAMP: 0>, 'SENSOR_TIMESTAMP': <OBFrameMetadataType.SENSOR_TIMESTAMP: 1>, 'FRAME_NUMBER': <OBFrameMetadataType.FRAME_NUMBER: 2>, 'AUTO_EXPOSURE': <OBFrameMetadataType.AUTO_EXPOSURE: 3>, 'EXPOSURE': <OBFrameMetadataType.EXPOSURE: 4>, 'GAIN': <OBFrameMetadataType.GAIN: 5>, 'AUTO_WHITE_BALANCE': <OBFrameMetadataType.AUTO_WHITE_BALANCE: 6>, 'WHITE_BALANCE': <OBFrameMetadataType.WHITE_BALANCE: 7>, 'BRIGHTNESS': <OBFrameMetadataType.BRIGHTNESS: 8>, 'CONTRAST': <OBFrameMetadataType.CONTRAST: 9>, 'SATURATION': <OBFrameMetadataType.SATURATION: 10>, 'SHARPNESS': <OBFrameMetadataType.SHARPNESS: 11>, 'BACKLIGHT_COMPENSATION': <OBFrameMetadataType.BACKLIGHT_COMPENSATION: 12>, 'HUE': <OBFrameMetadataType.HUE: 13>, 'GAMMA': <OBFrameMetadataType.GAMMA: 14>, 'POWER_LINE_FREQUENCY': <OBFrameMetadataType.POWER_LINE_FREQUENCY: 15>, 'LOW_LIGHT_COMPENSATION': <OBFrameMetadataType.LOW_LIGHT_COMPENSATION: 16>, 'MANUAL_WHITE_BALANCE': <OBFrameMetadataType.MANUAL_WHITE_BALANCE: 17>, 'ACTUAL_FRAME_RATE': <OBFrameMetadataType.ACTUAL_FRAME_RATE: 18>, 'FRAME_RATE': <OBFrameMetadataType.FRAME_RATE: 19>, 'AE_ROI_LEFT': <OBFrameMetadataType.AE_ROI_LEFT: 20>, 'AE_ROI_TOP': <OBFrameMetadataType.AE_ROI_TOP: 21>, 'AE_ROI_RIGHT': <OBFrameMetadataType.AE_ROI_RIGHT: 22>, 'AE_ROI_BOTTOM': <OBFrameMetadataType.AE_ROI_BOTTOM: 23>, 'EXPOSURE_PRIORITY': <OBFrameMetadataType.EXPOSURE_PRIORITY: 24>, 'HDR_SEQUENCE_NAME': <OBFrameMetadataType.HDR_SEQUENCE_NAME: 25>, 'HDR_SEQUENCE_SIZE': <OBFrameMetadataType.HDR_SEQUENCE_SIZE: 26>, 'HDR_SEQUENCE_INDEX': <OBFrameMetadataType.HDR_SEQUENCE_INDEX: 27>, 'LASER_POWER': <OBFrameMetadataType.LASER_POWER: 28>, 'LASER_POWER_LEVEL': <OBFrameMetadataType.LASER_POWER_LEVEL: 29>, 'LASER_STATUS': <OBFrameMetadataType.LASER_STATUS: 30>, 'GPIO_INPUT_DATA': <OBFrameMetadataType.GPIO_INPUT_DATA: 31>, 'DISPARITY_SEARCH_OFFSET': <OBFrameMetadataType.DISPARITY_SEARCH_OFFSET: 32>, 'DISPARITY_SEARCH_RANGE': <OBFrameMetadataType.DISPARITY_SEARCH_RANGE: 33>, 'COUNT': <OBFrameMetadataType.COUNT: 34>}
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

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

      RAW_PHASE_FRAME

      CONFIDENCE_FRAME

      LIDAR_POINTS_FRAME

      LEFT_COLOR_FRAME

      RIGHT_COLOR_FRAME

      TYPE_COUNT_FRAME
    """

    ACCEL_FRAME: typing.ClassVar[OBFrameType]  # value = <OBFrameType.ACCEL_FRAME: 4>
    COLOR_FRAME: typing.ClassVar[OBFrameType]  # value = <OBFrameType.COLOR_FRAME: 2>
    CONFIDENCE_FRAME: typing.ClassVar[OBFrameType]  # value = <OBFrameType.CONFIDENCE_FRAME: 11>
    DEPTH_FRAME: typing.ClassVar[OBFrameType]  # value = <OBFrameType.DEPTH_FRAME: 3>
    FRAME_SET: typing.ClassVar[OBFrameType]  # value = <OBFrameType.FRAME_SET: 5>
    GYRO_FRAME: typing.ClassVar[OBFrameType]  # value = <OBFrameType.GYRO_FRAME: 7>
    IR_FRAME: typing.ClassVar[OBFrameType]  # value = <OBFrameType.IR_FRAME: 1>
    LEFT_COLOR_FRAME: typing.ClassVar[OBFrameType]  # value = <OBFrameType.LEFT_COLOR_FRAME: 13>
    LEFT_IR_FRAME: typing.ClassVar[OBFrameType]  # value = <OBFrameType.LEFT_IR_FRAME: 8>
    LIDAR_POINTS_FRAME: typing.ClassVar[OBFrameType]  # value = <OBFrameType.LIDAR_POINTS_FRAME: 12>
    RAW_PHASE_FRAME: typing.ClassVar[OBFrameType]  # value = <OBFrameType.RAW_PHASE_FRAME: 10>
    RIGHT_COLOR_FRAME: typing.ClassVar[OBFrameType]  # value = <OBFrameType.RIGHT_COLOR_FRAME: 14>
    RIGHT_IR_FRAME: typing.ClassVar[OBFrameType]  # value = <OBFrameType.RIGHT_IR_FRAME: 9>
    TYPE_COUNT_FRAME: typing.ClassVar[OBFrameType]  # value = <OBFrameType.TYPE_COUNT_FRAME: 15>
    UNKNOWN_FRAME: typing.ClassVar[OBFrameType]  # value = <OBFrameType.UNKNOWN_FRAME: -1>
    VIDEO_FRAME: typing.ClassVar[OBFrameType]  # value = <OBFrameType.VIDEO_FRAME: 0>
    __members__: typing.ClassVar[
        dict[str, OBFrameType]
    ]  # value = {'UNKNOWN_FRAME': <OBFrameType.UNKNOWN_FRAME: -1>, 'VIDEO_FRAME': <OBFrameType.VIDEO_FRAME: 0>, 'IR_FRAME': <OBFrameType.IR_FRAME: 1>, 'COLOR_FRAME': <OBFrameType.COLOR_FRAME: 2>, 'DEPTH_FRAME': <OBFrameType.DEPTH_FRAME: 3>, 'ACCEL_FRAME': <OBFrameType.ACCEL_FRAME: 4>, 'GYRO_FRAME': <OBFrameType.GYRO_FRAME: 7>, 'LEFT_IR_FRAME': <OBFrameType.LEFT_IR_FRAME: 8>, 'RIGHT_IR_FRAME': <OBFrameType.RIGHT_IR_FRAME: 9>, 'FRAME_SET': <OBFrameType.FRAME_SET: 5>, 'RAW_PHASE_FRAME': <OBFrameType.RAW_PHASE_FRAME: 10>, 'CONFIDENCE_FRAME': <OBFrameType.CONFIDENCE_FRAME: 11>, 'LIDAR_POINTS_FRAME': <OBFrameType.LIDAR_POINTS_FRAME: 12>, 'LEFT_COLOR_FRAME': <OBFrameType.LEFT_COLOR_FRAME: 13>, 'RIGHT_COLOR_FRAME': <OBFrameType.RIGHT_COLOR_FRAME: 14>, 'TYPE_COUNT_FRAME': <OBFrameType.TYPE_COUNT_FRAME: 15>}
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class OBGvcpPortScheme:
    """
    Members:

      STANDARD

      B
    """

    B: typing.ClassVar[OBGvcpPortScheme]  # value = <OBGvcpPortScheme.B: 1>
    STANDARD: typing.ClassVar[OBGvcpPortScheme]  # value = <OBGvcpPortScheme.STANDARD: 0>
    __members__: typing.ClassVar[
        dict[str, OBGvcpPortScheme]
    ]  # value = {'STANDARD': <OBGvcpPortScheme.STANDARD: 0>, 'B': <OBGvcpPortScheme.B: 1>}
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class OBGyroFullScaleRange:
    """
    Members:

      FS_UNKNOWN

      FS_16dps

      FS_31dps

      FS_62dps

      FS_125dps

      FS_250dps

      FS_500dps

      FS_1000dps

      FS_2000dps

      FS_400dps

      FS_800dps
    """

    FS_1000dps: typing.ClassVar[OBGyroFullScaleRange]  # value = <OBGyroFullScaleRange.FS_1000dps: 7>
    FS_125dps: typing.ClassVar[OBGyroFullScaleRange]  # value = <OBGyroFullScaleRange.FS_125dps: 4>
    FS_16dps: typing.ClassVar[OBGyroFullScaleRange]  # value = <OBGyroFullScaleRange.FS_16dps: 1>
    FS_2000dps: typing.ClassVar[OBGyroFullScaleRange]  # value = <OBGyroFullScaleRange.FS_2000dps: 8>
    FS_250dps: typing.ClassVar[OBGyroFullScaleRange]  # value = <OBGyroFullScaleRange.FS_250dps: 5>
    FS_31dps: typing.ClassVar[OBGyroFullScaleRange]  # value = <OBGyroFullScaleRange.FS_31dps: 2>
    FS_400dps: typing.ClassVar[OBGyroFullScaleRange]  # value = <OBGyroFullScaleRange.FS_400dps: 9>
    FS_500dps: typing.ClassVar[OBGyroFullScaleRange]  # value = <OBGyroFullScaleRange.FS_500dps: 6>
    FS_62dps: typing.ClassVar[OBGyroFullScaleRange]  # value = <OBGyroFullScaleRange.FS_62dps: 3>
    FS_800dps: typing.ClassVar[OBGyroFullScaleRange]  # value = <OBGyroFullScaleRange.FS_800dps: 10>
    FS_UNKNOWN: typing.ClassVar[OBGyroFullScaleRange]  # value = <OBGyroFullScaleRange.FS_UNKNOWN: -1>
    __members__: typing.ClassVar[
        dict[str, OBGyroFullScaleRange]
    ]  # value = {'FS_UNKNOWN': <OBGyroFullScaleRange.FS_UNKNOWN: -1>, 'FS_16dps': <OBGyroFullScaleRange.FS_16dps: 1>, 'FS_31dps': <OBGyroFullScaleRange.FS_31dps: 2>, 'FS_62dps': <OBGyroFullScaleRange.FS_62dps: 3>, 'FS_125dps': <OBGyroFullScaleRange.FS_125dps: 4>, 'FS_250dps': <OBGyroFullScaleRange.FS_250dps: 5>, 'FS_500dps': <OBGyroFullScaleRange.FS_500dps: 6>, 'FS_1000dps': <OBGyroFullScaleRange.FS_1000dps: 7>, 'FS_2000dps': <OBGyroFullScaleRange.FS_2000dps: 8>, 'FS_400dps': <OBGyroFullScaleRange.FS_400dps: 9>, 'FS_800dps': <OBGyroFullScaleRange.FS_800dps: 10>}
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class OBGyroIntrinsic:
    def __init__(self) -> None: ...
    @property
    def bias(self) -> numpy.typing.NDArray[numpy.float64]: ...
    @bias.setter
    def bias(self, arg1: typing.Annotated[numpy.typing.ArrayLike, numpy.float64]) -> None: ...
    @property
    def noise_density(self) -> float: ...
    @noise_density.setter
    def noise_density(self, arg0: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def random_walk(self) -> float: ...
    @random_walk.setter
    def random_walk(self, arg0: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def reference_temp(self) -> float: ...
    @reference_temp.setter
    def reference_temp(self, arg0: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def scale_misalignment(self) -> numpy.typing.NDArray[numpy.float64]: ...
    @scale_misalignment.setter
    def scale_misalignment(self, arg1: typing.Annotated[numpy.typing.ArrayLike, numpy.float64]) -> None: ...
    @property
    def temp_slope(self) -> numpy.typing.NDArray[numpy.float64]: ...
    @temp_slope.setter
    def temp_slope(self, arg1: typing.Annotated[numpy.typing.ArrayLike, numpy.float64]) -> None: ...

class OBGyroSampleRate:
    """
    Members:

      SAMPLE_RATE_UNKNOWN

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

      SAMPLE_RATE_400_HZ

      SAMPLE_RATE_800_HZ
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
    SAMPLE_RATE_400_HZ: typing.ClassVar[OBGyroSampleRate]  # value = <OBGyroSampleRate.SAMPLE_RATE_400_HZ: 16>
    SAMPLE_RATE_4_KHZ: typing.ClassVar[OBGyroSampleRate]  # value = <OBGyroSampleRate.SAMPLE_RATE_4_KHZ: 12>
    SAMPLE_RATE_500_HZ: typing.ClassVar[OBGyroSampleRate]  # value = <OBGyroSampleRate.SAMPLE_RATE_500_HZ: 9>
    SAMPLE_RATE_50_HZ: typing.ClassVar[OBGyroSampleRate]  # value = <OBGyroSampleRate.SAMPLE_RATE_50_HZ: 6>
    SAMPLE_RATE_6_25_HZ: typing.ClassVar[OBGyroSampleRate]  # value = <OBGyroSampleRate.SAMPLE_RATE_6_25_HZ: 3>
    SAMPLE_RATE_800_HZ: typing.ClassVar[OBGyroSampleRate]  # value = <OBGyroSampleRate.SAMPLE_RATE_800_HZ: 17>
    SAMPLE_RATE_8_KHZ: typing.ClassVar[OBGyroSampleRate]  # value = <OBGyroSampleRate.SAMPLE_RATE_8_KHZ: 13>
    SAMPLE_RATE_UNKNOWN: typing.ClassVar[OBGyroSampleRate]  # value = <OBGyroSampleRate.SAMPLE_RATE_UNKNOWN: 0>
    __members__: typing.ClassVar[
        dict[str, OBGyroSampleRate]
    ]  # value = {'SAMPLE_RATE_UNKNOWN': <OBGyroSampleRate.SAMPLE_RATE_UNKNOWN: 0>, 'SAMPLE_RATE_1_5625_HZ': <OBGyroSampleRate.SAMPLE_RATE_1_5625_HZ: 1>, 'SAMPLE_RATE_3_125_HZ': <OBGyroSampleRate.SAMPLE_RATE_3_125_HZ: 2>, 'SAMPLE_RATE_6_25_HZ': <OBGyroSampleRate.SAMPLE_RATE_6_25_HZ: 3>, 'SAMPLE_RATE_12_5_HZ': <OBGyroSampleRate.SAMPLE_RATE_12_5_HZ: 4>, 'SAMPLE_RATE_25_HZ': <OBGyroSampleRate.SAMPLE_RATE_25_HZ: 5>, 'SAMPLE_RATE_50_HZ': <OBGyroSampleRate.SAMPLE_RATE_50_HZ: 6>, 'SAMPLE_RATE_100_HZ': <OBGyroSampleRate.SAMPLE_RATE_100_HZ: 7>, 'SAMPLE_RATE_200_HZ': <OBGyroSampleRate.SAMPLE_RATE_200_HZ: 8>, 'SAMPLE_RATE_500_HZ': <OBGyroSampleRate.SAMPLE_RATE_500_HZ: 9>, 'SAMPLE_RATE_1_KHZ': <OBGyroSampleRate.SAMPLE_RATE_1_KHZ: 10>, 'SAMPLE_RATE_2_KHZ': <OBGyroSampleRate.SAMPLE_RATE_2_KHZ: 11>, 'SAMPLE_RATE_4_KHZ': <OBGyroSampleRate.SAMPLE_RATE_4_KHZ: 12>, 'SAMPLE_RATE_8_KHZ': <OBGyroSampleRate.SAMPLE_RATE_8_KHZ: 13>, 'SAMPLE_RATE_16_KHZ': <OBGyroSampleRate.SAMPLE_RATE_16_KHZ: 14>, 'SAMPLE_RATE_32_KHZ': <OBGyroSampleRate.SAMPLE_RATE_32_KHZ: 15>, 'SAMPLE_RATE_400_HZ': <OBGyroSampleRate.SAMPLE_RATE_400_HZ: 16>, 'SAMPLE_RATE_800_HZ': <OBGyroSampleRate.SAMPLE_RATE_800_HZ: 17>}
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class OBHardwareDecimationConfig:
    def __init__(self) -> None: ...
    @property
    def factor(self) -> int: ...
    @factor.setter
    def factor(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def origin_height(self) -> int: ...
    @origin_height.setter
    def origin_height(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def origin_width(self) -> int: ...
    @origin_width.setter
    def origin_width(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...

class OBHdrConfig:
    def __init__(self) -> None: ...
    @property
    def enable(self) -> int: ...
    @enable.setter
    def enable(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def exposure_1(self) -> int: ...
    @exposure_1.setter
    def exposure_1(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def exposure_2(self) -> int: ...
    @exposure_2.setter
    def exposure_2(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def gain_1(self) -> int: ...
    @gain_1.setter
    def gain_1(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def gain_2(self) -> int: ...
    @gain_2.setter
    def gain_2(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def sequence_name(self) -> int: ...
    @sequence_name.setter
    def sequence_name(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...

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
    __members__: typing.ClassVar[
        dict[str, OBHoleFillingMode]
    ]  # value = {'TOP': <OBHoleFillingMode.TOP: 0>, 'NEAREST': <OBHoleFillingMode.NEAREST: 1>, 'FURTHEST': <OBHoleFillingMode.FURTHEST: 2>}
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class OBIntPropertyRange:
    def __init__(self) -> None: ...
    @property
    def current(self) -> int: ...
    @current.setter
    def current(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def default_value(self) -> int: ...
    @default_value.setter
    def default_value(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def max(self) -> int: ...
    @max.setter
    def max(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def min(self) -> int: ...
    @min.setter
    def min(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def step(self) -> int: ...
    @step.setter
    def step(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...

class OBIpSourceType:
    """
    Members:

      NONE

      LLA

      DHCP

      PERSISTENT
    """

    DHCP: typing.ClassVar[OBIpSourceType]  # value = <OBIpSourceType.DHCP: 2>
    LLA: typing.ClassVar[OBIpSourceType]  # value = <OBIpSourceType.LLA: 1>
    NONE: typing.ClassVar[OBIpSourceType]  # value = <OBIpSourceType.NONE: 0>
    PERSISTENT: typing.ClassVar[OBIpSourceType]  # value = <OBIpSourceType.PERSISTENT: 3>
    __members__: typing.ClassVar[
        dict[str, OBIpSourceType]
    ]  # value = {'NONE': <OBIpSourceType.NONE: 0>, 'LLA': <OBIpSourceType.LLA: 1>, 'DHCP': <OBIpSourceType.DHCP: 2>, 'PERSISTENT': <OBIpSourceType.PERSISTENT: 3>}
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class OBLiDARPoint:
    def __init__(self) -> None: ...
    @property
    def reflectivity(self) -> int: ...
    @reflectivity.setter
    def reflectivity(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def tag(self) -> int: ...
    @tag.setter
    def tag(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def x(self) -> float: ...
    @x.setter
    def x(self, arg0: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def y(self) -> float: ...
    @y.setter
    def y(self, arg0: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def z(self) -> float: ...
    @z.setter
    def z(self, arg0: typing.SupportsFloat | typing.SupportsIndex) -> None: ...

class OBLiDARScanPoint:
    def __init__(self) -> None: ...
    @property
    def angle(self) -> float: ...
    @angle.setter
    def angle(self, arg0: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def distance(self) -> float: ...
    @distance.setter
    def distance(self, arg0: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def intensity(self) -> int: ...
    @intensity.setter
    def intensity(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...

class OBLiDARScanRate:
    """
    Members:

      LIDAR_SCAN_UNKNOWN

      LIDAR_SCAN_5HZ

      LIDAR_SCAN_10HZ

      LIDAR_SCAN_15HZ

      LIDAR_SCAN_20HZ

      LIDAR_SCAN_25HZ

      LIDAR_SCAN_30HZ

      LIDAR_SCAN_40HZ
    """

    LIDAR_SCAN_10HZ: typing.ClassVar[OBLiDARScanRate]  # value = <OBLiDARScanRate.LIDAR_SCAN_10HZ: 2>
    LIDAR_SCAN_15HZ: typing.ClassVar[OBLiDARScanRate]  # value = <OBLiDARScanRate.LIDAR_SCAN_15HZ: 3>
    LIDAR_SCAN_20HZ: typing.ClassVar[OBLiDARScanRate]  # value = <OBLiDARScanRate.LIDAR_SCAN_20HZ: 4>
    LIDAR_SCAN_25HZ: typing.ClassVar[OBLiDARScanRate]  # value = <OBLiDARScanRate.LIDAR_SCAN_25HZ: 5>
    LIDAR_SCAN_30HZ: typing.ClassVar[OBLiDARScanRate]  # value = <OBLiDARScanRate.LIDAR_SCAN_30HZ: 6>
    LIDAR_SCAN_40HZ: typing.ClassVar[OBLiDARScanRate]  # value = <OBLiDARScanRate.LIDAR_SCAN_40HZ: 7>
    LIDAR_SCAN_5HZ: typing.ClassVar[OBLiDARScanRate]  # value = <OBLiDARScanRate.LIDAR_SCAN_5HZ: 1>
    LIDAR_SCAN_UNKNOWN: typing.ClassVar[OBLiDARScanRate]  # value = <OBLiDARScanRate.LIDAR_SCAN_UNKNOWN: 0>
    __members__: typing.ClassVar[
        dict[str, OBLiDARScanRate]
    ]  # value = {'LIDAR_SCAN_UNKNOWN': <OBLiDARScanRate.LIDAR_SCAN_UNKNOWN: 0>, 'LIDAR_SCAN_5HZ': <OBLiDARScanRate.LIDAR_SCAN_5HZ: 1>, 'LIDAR_SCAN_10HZ': <OBLiDARScanRate.LIDAR_SCAN_10HZ: 2>, 'LIDAR_SCAN_15HZ': <OBLiDARScanRate.LIDAR_SCAN_15HZ: 3>, 'LIDAR_SCAN_20HZ': <OBLiDARScanRate.LIDAR_SCAN_20HZ: 4>, 'LIDAR_SCAN_25HZ': <OBLiDARScanRate.LIDAR_SCAN_25HZ: 5>, 'LIDAR_SCAN_30HZ': <OBLiDARScanRate.LIDAR_SCAN_30HZ: 6>, 'LIDAR_SCAN_40HZ': <OBLiDARScanRate.LIDAR_SCAN_40HZ: 7>}
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class OBLiDARSpherePoint:
    def __init__(self) -> None: ...
    @property
    def distance(self) -> float: ...
    @distance.setter
    def distance(self, arg0: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def phi(self) -> float: ...
    @phi.setter
    def phi(self, arg0: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def reflectivity(self) -> int: ...
    @reflectivity.setter
    def reflectivity(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def tag(self) -> int: ...
    @tag.setter
    def tag(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def theta(self) -> float: ...
    @theta.setter
    def theta(self, arg0: typing.SupportsFloat | typing.SupportsIndex) -> None: ...

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
    __members__: typing.ClassVar[
        dict[str, OBLogLevel]
    ]  # value = {'DEBUG': <OBLogLevel.DEBUG: 0>, 'INFO': <OBLogLevel.INFO: 1>, 'WARNING': <OBLogLevel.WARNING: 2>, 'ERROR': <OBLogLevel.ERROR: 3>, 'FATAL': <OBLogLevel.FATAL: 4>, 'NONE': <OBLogLevel.NONE: 5>}
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class OBLutNoiseRemovalFilterParams:
    def __init__(self) -> None: ...
    def __repr__(self) -> str: ...
    @property
    def height(self) -> int: ...
    @height.setter
    def height(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def max_lut(self) -> numpy.typing.NDArray[numpy.uint16]: ...
    @max_lut.setter
    def max_lut(self, arg1: typing.Annotated[numpy.typing.ArrayLike, numpy.uint16]) -> None: ...
    @property
    def min_diff(self) -> int: ...
    @min_diff.setter
    def min_diff(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def width(self) -> int: ...
    @width.setter
    def width(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...

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
    OB_MEDIA_RESUME: typing.ClassVar[OBMediaState]  # value = <OBMediaState.OB_MEDIA_RESUME: 2>
    __members__: typing.ClassVar[
        dict[str, OBMediaState]
    ]  # value = {'OB_MEDIA_BEGIN': <OBMediaState.OB_MEDIA_BEGIN: 0>, 'OB_MEDIA_PAUSE': <OBMediaState.OB_MEDIA_PAUSE: 1>, 'OB_MEDIA_RESUME': <OBMediaState.OB_MEDIA_RESUME: 2>, 'OB_MEDIA_END': <OBMediaState.OB_MEDIA_END: 3>}
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

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
    __members__: typing.ClassVar[
        dict[str, OBMediaType]
    ]  # value = {'DEPTH': <OBMediaType.DEPTH: 2>, 'COLOR': <OBMediaType.COLOR: 1>, 'IR': <OBMediaType.IR: 4>, 'GYRO': <OBMediaType.GYRO: 8>, 'ACCEL': <OBMediaType.ACCEL: 16>, 'CAMERA_PARAM': <OBMediaType.CAMERA_PARAM: 32>, 'DEVICE_INFO': <OBMediaType.DEVICE_INFO: 64>, 'STREAM_INFO': <OBMediaType.STREAM_INFO: 128>, 'LEFT_IR': <OBMediaType.LEFT_IR: 256>, 'RIGHT_IR': <OBMediaType.RIGHT_IR: 512>}
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class OBMgcNoiseRemovalFilterParams:
    def __init__(self) -> None: ...
    def __repr__(self) -> str: ...
    @property
    def height(self) -> int: ...
    @height.setter
    def height(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def limit_x_th(self) -> int: ...
    @limit_x_th.setter
    def limit_x_th(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def limit_y_th(self) -> int: ...
    @limit_y_th.setter
    def limit_y_th(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def margin_x_th(self) -> int: ...
    @margin_x_th.setter
    def margin_x_th(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def margin_y_th(self) -> int: ...
    @margin_y_th.setter
    def margin_y_th(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def max_radius(self) -> int: ...
    @max_radius.setter
    def max_radius(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def max_width_left(self) -> int: ...
    @max_width_left.setter
    def max_width_left(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def max_width_right(self) -> int: ...
    @max_width_right.setter
    def max_width_right(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def width(self) -> int: ...
    @width.setter
    def width(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...

class OBMultiDeviceSyncConfig:
    mode: OBMultiDeviceSyncMode
    trigger_out_enable: bool
    def __init__(self) -> None: ...
    @property
    def color_delay_us(self) -> int: ...
    @color_delay_us.setter
    def color_delay_us(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def depth_delay_us(self) -> int: ...
    @depth_delay_us.setter
    def depth_delay_us(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def frames_per_trigger(self) -> int: ...
    @frames_per_trigger.setter
    def frames_per_trigger(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def trigger_out_delay_us(self) -> int: ...
    @trigger_out_delay_us.setter
    def trigger_out_delay_us(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def trigger_to_image_delay_us(self) -> int: ...
    @trigger_to_image_delay_us.setter
    def trigger_to_image_delay_us(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...

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

      IR_IMU_SYNC

      SOFTWARE_SYNCED
    """

    FREE_RUN: typing.ClassVar[OBMultiDeviceSyncMode]  # value = <OBMultiDeviceSyncMode.FREE_RUN: 1>
    HARDWARE_TRIGGERING: typing.ClassVar[
        OBMultiDeviceSyncMode
    ]  # value = <OBMultiDeviceSyncMode.HARDWARE_TRIGGERING: 64>
    IR_IMU_SYNC: typing.ClassVar[OBMultiDeviceSyncMode]  # value = <OBMultiDeviceSyncMode.IR_IMU_SYNC: 128>
    PRIMARY: typing.ClassVar[OBMultiDeviceSyncMode]  # value = <OBMultiDeviceSyncMode.PRIMARY: 4>
    SECONDARY: typing.ClassVar[OBMultiDeviceSyncMode]  # value = <OBMultiDeviceSyncMode.SECONDARY: 8>
    SECONDARY_SYNCED: typing.ClassVar[OBMultiDeviceSyncMode]  # value = <OBMultiDeviceSyncMode.SECONDARY_SYNCED: 16>
    SOFTWARE_SYNCED: typing.ClassVar[OBMultiDeviceSyncMode]  # value = <OBMultiDeviceSyncMode.SOFTWARE_SYNCED: 256>
    SOFTWARE_TRIGGERING: typing.ClassVar[
        OBMultiDeviceSyncMode
    ]  # value = <OBMultiDeviceSyncMode.SOFTWARE_TRIGGERING: 32>
    STANDALONE: typing.ClassVar[OBMultiDeviceSyncMode]  # value = <OBMultiDeviceSyncMode.STANDALONE: 2>
    __members__: typing.ClassVar[
        dict[str, OBMultiDeviceSyncMode]
    ]  # value = {'FREE_RUN': <OBMultiDeviceSyncMode.FREE_RUN: 1>, 'STANDALONE': <OBMultiDeviceSyncMode.STANDALONE: 2>, 'PRIMARY': <OBMultiDeviceSyncMode.PRIMARY: 4>, 'SECONDARY': <OBMultiDeviceSyncMode.SECONDARY: 8>, 'SECONDARY_SYNCED': <OBMultiDeviceSyncMode.SECONDARY_SYNCED: 16>, 'SOFTWARE_TRIGGERING': <OBMultiDeviceSyncMode.SOFTWARE_TRIGGERING: 32>, 'HARDWARE_TRIGGERING': <OBMultiDeviceSyncMode.HARDWARE_TRIGGERING: 64>, 'IR_IMU_SYNC': <OBMultiDeviceSyncMode.IR_IMU_SYNC: 128>, 'SOFTWARE_SYNCED': <OBMultiDeviceSyncMode.SOFTWARE_SYNCED: 256>}
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class OBNetIpConfigV2:
    address: str
    gateway: str
    netmask: str
    def __init__(self) -> None: ...
    def __repr__(self) -> str: ...
    @property
    def flags(self) -> int: ...
    @flags.setter
    def flags(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...

class OBNoiseRemovalFilterParams:
    type: OBDDONoiseRemovalType
    def __init__(self) -> None: ...
    @property
    def disp_diff(self) -> int: ...
    @disp_diff.setter
    def disp_diff(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def max_size(self) -> int: ...
    @max_size.setter
    def max_size(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...

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
    __members__: typing.ClassVar[
        dict[str, OBPermissionType]
    ]  # value = {'PERMISSION_DENY': <OBPermissionType.PERMISSION_DENY: 0>, 'PERMISSION_READ': <OBPermissionType.PERMISSION_READ: 1>, 'PERMISSION_WRITE': <OBPermissionType.PERMISSION_WRITE: 2>, 'PERMISSION_READ_WRITE': <OBPermissionType.PERMISSION_READ_WRITE: 3>}
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class OBPipelineIssue:
    """
    Members:

      NONE

      SDK

      DRIVER

      FW

      HW
    """

    DRIVER: typing.ClassVar[OBPipelineIssue]  # value = <OBPipelineIssue.DRIVER: 2>
    FW: typing.ClassVar[OBPipelineIssue]  # value = <OBPipelineIssue.FW: 4>
    HW: typing.ClassVar[OBPipelineIssue]  # value = <OBPipelineIssue.HW: 8>
    NONE: typing.ClassVar[OBPipelineIssue]  # value = <OBPipelineIssue.NONE: 0>
    SDK: typing.ClassVar[OBPipelineIssue]  # value = <OBPipelineIssue.SDK: 1>
    __members__: typing.ClassVar[
        dict[str, OBPipelineIssue]
    ]  # value = {'NONE': <OBPipelineIssue.NONE: 0>, 'SDK': <OBPipelineIssue.SDK: 1>, 'DRIVER': <OBPipelineIssue.DRIVER: 2>, 'FW': <OBPipelineIssue.FW: 4>, 'HW': <OBPipelineIssue.HW: 8>}
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class OBPipelineStatus:
    issue: OBPipelineIssue
    def __init__(self) -> None: ...
    def __repr__(self) -> str: ...
    @property
    def dev_status(self) -> int: ...
    @dev_status.setter
    def dev_status(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def drv_status(self) -> int: ...
    @drv_status.setter
    def drv_status(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def sdk_status(self) -> int: ...
    @sdk_status.setter
    def sdk_status(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...

class OBPixelType:
    """
    Members:

      OB_PIXEL_UNKNOWN

      OB_PIXEL_DEPTH

      OB_PIXEL_DISPARITY

      OB_PIXEL_RAW_PHASE

      OB_PIXEL_TOF_DEPTH
    """

    OB_PIXEL_DEPTH: typing.ClassVar[OBPixelType]  # value = <OBPixelType.OB_PIXEL_DEPTH: 0>
    OB_PIXEL_DISPARITY: typing.ClassVar[OBPixelType]  # value = <OBPixelType.OB_PIXEL_DISPARITY: 2>
    OB_PIXEL_RAW_PHASE: typing.ClassVar[OBPixelType]  # value = <OBPixelType.OB_PIXEL_RAW_PHASE: 3>
    OB_PIXEL_TOF_DEPTH: typing.ClassVar[OBPixelType]  # value = <OBPixelType.OB_PIXEL_TOF_DEPTH: 4>
    OB_PIXEL_UNKNOWN: typing.ClassVar[OBPixelType]  # value = <OBPixelType.OB_PIXEL_UNKNOWN: -1>
    __members__: typing.ClassVar[
        dict[str, OBPixelType]
    ]  # value = {'OB_PIXEL_UNKNOWN': <OBPixelType.OB_PIXEL_UNKNOWN: -1>, 'OB_PIXEL_DEPTH': <OBPixelType.OB_PIXEL_DEPTH: 0>, 'OB_PIXEL_DISPARITY': <OBPixelType.OB_PIXEL_DISPARITY: 2>, 'OB_PIXEL_RAW_PHASE': <OBPixelType.OB_PIXEL_RAW_PHASE: 3>, 'OB_PIXEL_TOF_DEPTH': <OBPixelType.OB_PIXEL_TOF_DEPTH: 4>}
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class OBPlaybackStatus:
    """
    Members:

      UNKNOWN

      PLAYING

      PAUSED

      STOPPED

      COUNT
    """

    COUNT: typing.ClassVar[OBPlaybackStatus]  # value = <OBPlaybackStatus.COUNT: 4>
    PAUSED: typing.ClassVar[OBPlaybackStatus]  # value = <OBPlaybackStatus.PAUSED: 2>
    PLAYING: typing.ClassVar[OBPlaybackStatus]  # value = <OBPlaybackStatus.PLAYING: 1>
    STOPPED: typing.ClassVar[OBPlaybackStatus]  # value = <OBPlaybackStatus.STOPPED: 3>
    UNKNOWN: typing.ClassVar[OBPlaybackStatus]  # value = <OBPlaybackStatus.UNKNOWN: 0>
    __members__: typing.ClassVar[
        dict[str, OBPlaybackStatus]
    ]  # value = {'UNKNOWN': <OBPlaybackStatus.UNKNOWN: 0>, 'PLAYING': <OBPlaybackStatus.PLAYING: 1>, 'PAUSED': <OBPlaybackStatus.PAUSED: 2>, 'STOPPED': <OBPlaybackStatus.STOPPED: 3>, 'COUNT': <OBPlaybackStatus.COUNT: 4>}
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class OBPoint2f:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(
        self, arg0: typing.SupportsFloat | typing.SupportsIndex, arg1: typing.SupportsFloat | typing.SupportsIndex
    ) -> None: ...
    def __repr__(self) -> str: ...
    @property
    def x(self) -> float: ...
    @x.setter
    def x(self, arg0: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def y(self) -> float: ...
    @y.setter
    def y(self, arg0: typing.SupportsFloat | typing.SupportsIndex) -> None: ...

class OBPoint3f:
    @staticmethod
    def get_sizeof() -> int: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(
        self,
        arg0: typing.SupportsFloat | typing.SupportsIndex,
        arg1: typing.SupportsFloat | typing.SupportsIndex,
        arg2: typing.SupportsFloat | typing.SupportsIndex,
    ) -> None: ...
    def __repr__(self) -> str: ...
    @property
    def x(self) -> float: ...
    @x.setter
    def x(self, arg0: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def y(self) -> float: ...
    @y.setter
    def y(self, arg0: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def z(self) -> float: ...
    @z.setter
    def z(self, arg0: typing.SupportsFloat | typing.SupportsIndex) -> None: ...

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
    __members__: typing.ClassVar[
        dict[str, OBPowerLineFreqMode]
    ]  # value = {'FREQUENCY_50HZ': <OBPowerLineFreqMode.FREQUENCY_50HZ: 1>, 'FREQUENCY_60HZ': <OBPowerLineFreqMode.FREQUENCY_60HZ: 2>, 'FREQUENCY_CLOSE': <OBPowerLineFreqMode.FREQUENCY_CLOSE: 0>}
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class OBPresetResolutionConfig:
    def __init__(self) -> None: ...
    @property
    def depth_decimation_factor(self) -> int: ...
    @depth_decimation_factor.setter
    def depth_decimation_factor(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def height(self) -> int: ...
    @height.setter
    def height(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def ir_decimation_factor(self) -> int: ...
    @ir_decimation_factor.setter
    def ir_decimation_factor(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def width(self) -> int: ...
    @width.setter
    def width(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...

class OBPropertyID:
    """
    Members:

      OB_PROP_LDP_BOOL : LDP switch

      OB_PROP_LASER_BOOL : Laser switch

      OB_PROP_LASER_PULSE_WIDTH_INT : laser pulse width

      OB_PROP_LASER_CURRENT_FLOAT : Laser current (uint: mA)

      OB_PROP_FLOOD_BOOL : IR flood switch

      OB_PROP_FLOOD_LEVEL_INT : IR flood level

      OB_PROP_TEMPERATURE_COMPENSATION_BOOL : Enable/disable temperature compensation

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

      OB_PROP_DEPTH_NOISE_REMOVAL_FILTER_MAX_DIFF_INT : depth noise removal filter max diff param

      OB_PROP_DEPTH_NOISE_REMOVAL_FILTER_MAX_SPECKLE_SIZE_INT : depth noise removal filter maxSpeckleSize

      OB_PROP_DEPTH_ALIGN_HARDWARE_BOOL : Hardware d2c is on

      OB_PROP_TIMESTAMP_OFFSET_INT : Timestamp adjustment

      OB_PROP_HARDWARE_DISTORTION_SWITCH_BOOL :  Hardware distortion switch Rectify

      OB_PROP_FAN_WORK_MODE_INT : Fan mode switch

      OB_PROP_DEPTH_ALIGN_HARDWARE_MODE_INT : Multi-resolution D2C mode

      OB_PROP_ANTI_COLLUSION_ACTIVATION_STATUS_BOOL : Anti_collusion activation status

      OB_PROP_DEVICE_AE_REFERENCE_INT : Device AE reference source. 0: Depth based, 1: Color based

      OB_PROP_DEVICE_AE_STRATEGY_INT : Device AE strategy. 0: Default, 1: Motion

      OB_PROP_COLOR_ROI_BRIGHTNESS_INT : Color camera ROI brightness adjustment

      OB_PROP_COLOR_PRESET_PRIORITY_INT : Color camera preset priority

      OB_PROP_COLOR_ANTI_FLICKER_BOOL : Color anti-flicker switch

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

      OB_PROP_GPM_BOOL : Enable/disable GPM function

      OB_PROP_RGB_CUSTOM_CROP_BOOL : Custom RGB cropping switch, 0 is off, 1 is on custom cropping, and the ROI cropping area is issued

      OB_PROP_DEVICE_WORK_MODE_INT : Device operating mode (power consumption)

      OB_PROP_DEVICE_COMMUNICATION_TYPE_INT : Device communication type, 0: USB; 1: Ethernet(RTSP)

      OB_PROP_SWITCH_IR_MODE_INT : Switch infrared imaging mode, 0: active IR mode, 1: passive IR mode

      OB_PROP_LASER_POWER_LEVEL_CONTROL_INT : Laser power level

      OB_PROP_LASER_ENERGY_LEVEL_INT : Laser energy level

      OB_PROP_LASER_POWER_ACTUAL_LEVEL_INT : Get hardware laser power actual level which real state of laser element. OB_PROP_LASER_ENERGY_LEVEL_INT will effect this command which it setting and changed the hardware laser energy level.

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

      OB_PROP_COLOR_RIGHT_ROTATE_INT : Right Color sensor rotation, angle{0, 90, 180, 270}

      OB_PROP_COLOR_RIGHT_MIRROR_BOOL : Right Color mirror

      OB_PROP_COLOR_RIGHT_FLIP_BOOL : Right Color flip

      OB_PROP_COLOR_LEFT_ROTATE_INT : Left Color sensor rotation, angle{0, 90, 180, 270}

      OB_PROP_COLOR_LEFT_MIRROR_BOOL : Left Color mirror

      OB_PROP_COLOR_LEFT_FLIP_BOOL : Left Color flip

      OB_PROP_LASER_HW_ENERGY_LEVEL_INT : Get hardware laser energy level which real state of laser element. OB_PROP_LASER_ENERGY_LEVEL_INT(99)will effect this command which it setting and changed the hardware laser energy level.

      OB_PROP_USB_POWER_STATE_INT : USB's power state

      OB_PROP_DC_POWER_STATE_INT : DC's power state

      OB_PROP_DEVICE_DEVELOPMENT_MODE_INT : Device development mode switch

      OB_PROP_SYNC_SIGNAL_TRIGGER_OUT_BOOL :  Multi-DeviceSync synchronized signal trigger out is enable state

      OB_PROP_DEPTH_WITH_CONFIDENCE_STREAM_ENABLE_BOOL : Depth with confidence stream enable

      OB_PROP_CONFIDENCE_STREAM_FILTER_BOOL : Enable or disable confidence stream filter

      OB_PROP_CONFIDENCE_STREAM_FILTER_THRESHOLD_INT : Confidence stream filter threshold, range [0, 255]

      OB_PROP_CONFIDENCE_MIRROR_BOOL : Confidence stream mirror enable

      OB_PROP_CONFIDENCE_FLIP_BOOL : Confidence stream flip enable

      OB_PROP_CONFIDENCE_ROTATE_INT : Confidence stream rotate angle{0, 90, 180, 270}

      OB_PROP_INTRA_CAMERA_SYNC_REFERENCE_INT : Intra-camera Sync Reference based on the exposure start time, the exposure middle time, or the exposure end time.

      OB_PROP_RESTORE_FACTORY_SETTINGS_BOOL : Restore factory settings and factory parameters

      OB_PROP_BOOT_INTO_RECOVERY_MODE_BOOL : Enter recovery mode (flashing mode) when boot the device

      OB_PROP_DEVICE_IN_RECOVERY_MODE_BOOL : Query whether the current device is running in recovery mode(read-only)

      OB_PROP_CAPTURE_INTERVAL_MODE_INT : Capture interval mode, 0:time interval, 1:number interval

      OB_PROP_CAPTURE_IMAGE_TIME_INTERVAL_INT : Capture time interval

      OB_PROP_CAPTURE_IMAGE_NUMBER_INTERVAL_INT : Capture number interval

      OB_PROP_TIMER_RESET_ENABLE_BOOL : OB_PROP_TIMER_RESET_ENABLE_BOOL

      OB_PROP_DEVICE_USB3_REPEAT_IDENTIFY_BOOL : Enable or disable the device to retry USB2.0 re-identification when the device is connected to a USB2.0 port.

      OB_PROP_DEVICE_REBOOT_DELAY_INT : Reboot device delay mode. Delay time unit: ms, range: [0, 8000).

      OB_PROP_DHCP_ASSIGN_IP_TIMEOUT_INT : DHCP assign IP timeout, unit: second

      OB_PROP_LASER_OVERCURRENT_PROTECTION_STATUS_BOOL : Query the status of laser overcurrent protection (read-only)

      OB_PROP_LASER_PULSE_WIDTH_PROTECTION_STATUS_BOOL : Query the status of laser pulse width protection (read-only)

      OB_PROP_LASER_ALWAYS_ON_BOOL :  Laser always on, true: always on, false: off, laser will be turned off when out of exposure time

      OB_PROP_LASER_ON_OFF_PATTERN_INT : Laser on/off alternate mode, 0: off, 1: on-off alternate, 2: off-on alternate

      OB_PROP_DEPTH_UNIT_FLEXIBLE_ADJUSTMENT_FLOAT : Depth unit flexible adjustment,This property allows continuous adjustment of the depth unit

      OB_PROP_LASER_CONTROL_INT : Laser control, 0: off, 1: on, 2: auto

      OB_PROP_IR_BRIGHTNESS_INT : IR brightness

      OB_PROP_SLAVE_DEVICE_SYNC_STATUS_BOOL

      OB_PROP_COLOR_AE_MAX_EXPOSURE_INT : Color AE max exposure

      OB_PROP_IR_AE_MAX_EXPOSURE_INT : Max exposure time of IR auto exposure

      OB_PROP_DISP_SEARCH_RANGE_MODE_INT : Disparity search range mode, 1: 128, 2: 256

      OB_PROP_LASER_HIGH_TEMPERATURE_PROTECT_BOOL : Laser high temperature protection

      OB_PROP_LOW_EXPOSURE_LASER_CONTROL_BOOL : low exposure laser control

      OB_PROP_CHECK_PPS_SYNC_IN_SIGNAL_BOOL : check pps sync in signal

      OB_PROP_DISP_SEARCH_OFFSET_INT : Disparity search range offset, range: [0, 127]

      OB_PROP_CPU_TEMPERATURE_CALIBRATION_BOOL : cpu temperature calibration . true: calibrate temperature

      OB_PROP_DEVICE_REPOWER_BOOL : Repower device (cut off power and power on again)

      OB_PROP_FRAME_INTERLEAVE_CONFIG_INDEX_INT : frame interleave config index

      OB_PROP_FRAME_INTERLEAVE_ENABLE_BOOL : frame interleave enable (true:enable,false:disable)

      OB_PROP_FRAME_INTERLEAVE_LASER_PATTERN_SYNC_DELAY_INT : laser pattern sync with delay(us)

      OB_PROP_ON_CHIP_CALIBRATION_HEALTH_CHECK_FLOAT : Get the health check result from device,range is [0.0f,1.5f]

      OB_PROP_ON_CHIP_CALIBRATION_ENABLE_BOOL : Enable or disable on-chip calibration

      OB_PROP_HW_NOISE_REMOVE_FILTER_ENABLE_BOOL : hardware noise remove filter switch

      OB_PROP_HW_NOISE_REMOVE_FILTER_THRESHOLD_FLOAT : hardware noise remove filter threshold ,range [0.0 - 1.0]

      OB_STRUCT_BASELINE_CALIBRATION_PARAM : Baseline calibration parameters

      OB_STRUCT_DEVICE_TEMPERATURE : Device temperature information

      OB_STRUCT_TOF_EXPOSURE_THRESHOLD_CONTROL : TOF exposure threshold range

      OB_STRUCT_DEVICE_SERIAL_NUMBER

      OB_STRUCT_DEVICE_TIME

      OB_STRUCT_MULTI_DEVICE_SYNC_CONFIG

      OB_STRUCT_RGB_CROP_ROI

      OB_STRUCT_DEVICE_IP_ADDR_CONFIG

      OB_STRUCT_DEVICE_IP_ADDR_CONFIG_V2 : Device IP address configuration v2

      OB_STRUCT_CURRENT_DEPTH_ALG_MODE

      OB_STRUCT_DEPTH_PRECISION_SUPPORT_LIST

      OB_STRUCT_DEVICE_STATIC_IP_CONFIG_RECORD

      OB_STRUCT_DEPTH_HDR_CONFIG

      OB_STRUCT_COLOR_AE_ROI

      OB_STRUCT_DEPTH_AE_ROI

      OB_STRUCT_ASIC_SERIAL_NUMBER

      OB_STRUCT_DISP_OFFSET_CONFIG : Disparity offset interleaving

      OB_STRUCT_PRESET_RESOLUTION_CONFIG : Preset resolution ratio configuration

      OB_STRUCT_COLOR_SYNCED_EXPOSURE_PARAM : Color sensor synchronized exposure parameter structure

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

      OB_PROP_COLOR_DENOISING_LEVEL_INT : Color camera CCI denoising level. 0: Auto; 1-8: higher values indicate stronger denoising.

      OB_PROP_DEVICE_OFFLINE_AFTER_IP_CONFIG_APPLY : Indicates whether the device will go offline after applying IP configuration. This property is a capability flag only.

      OB_PROP_DEPTH_AUTO_EXPOSURE_PRIORITY_INT : Depth camera priority

      OB_PROP_DEPTH_AUTO_EXPOSURE_BOOL

      OB_PROP_DEPTH_EXPOSURE_INT

      OB_PROP_DEPTH_GAIN_INT

      OB_PROP_IR_AUTO_EXPOSURE_BOOL

      OB_PROP_IR_EXPOSURE_INT

      OB_PROP_IR_GAIN_INT

      OB_PROP_IR_CHANNEL_DATA_SOURCE_INT

      OB_PROP_DEPTH_RM_FILTER_BOOL

      OB_PROP_COLOR_AE_MAX_GAIN_INT

      OB_PROP_COLOR_MAXIMAL_SHUTTER_INT

      OB_PROP_IR_SHORT_EXPOSURE_BOOL

      OB_PROP_COLOR_HDR_BOOL

      OB_PROP_IR_LONG_EXPOSURE_BOOL

      OB_PROP_SKIP_FRAME_BOOL

      OB_PROP_HDR_MERGE_BOOL

      OB_PROP_COLOR_FOCUS_INT

      OB_PROP_IR_RECTIFY_BOOL

      OB_PROP_SDK_DISPARITY_TO_DEPTH_BOOL

      OB_PROP_SDK_DEPTH_FRAME_UNPACK_BOOL

      OB_PROP_SDK_IR_FRAME_UNPACK_BOOL

      OB_PROP_SDK_ACCEL_FRAME_TRANSFORMED_BOOL : Accel data conversion function switch (on by default)

      OB_PROP_SDK_GYRO_FRAME_TRANSFORMED_BOOL : Gyro data conversion function switch (on by default)

      OB_PROP_SDK_IR_LEFT_FRAME_UNPACK_BOOL : Left IR frame data unpacking function switch (each current will be turned on by default, support RLE/Y10/Y11/Y12/Y14 format)

      OB_PROP_SDK_IR_RIGHT_FRAME_UNPACK_BOOL : Right IR frame data unpacking function switch (each current will be turned on by default, support RLE/Y10/Y11/Y12/Y14 format)

      OB_PROP_DEPTH_INDUSTRY_MODE_INT : Depth Stream Industry Working Mode Settings

      OB_PROP_NETWORK_BANDWIDTH_TYPE_INT : Read the current network bandwidth type of the network device

      OB_PROP_DEVICE_PERFORMANCE_MODE_INT : Switch device performance mode

      OB_RAW_DATA_CAMERA_CALIB_JSON_FILE : Calibration JSON file read from device (Femto Mega, read only)

      OB_PROP_LIDAR_TAIL_FILTER_LEVEL_INT : LiDAR: set/get tail filter level

      OB_RAW_DATA_LIDAR_IP_ADDRESS : LiDAR: set/get IP address

      OB_PROP_LIDAR_PORT_INT : LiDAR: set/get port

      OB_RAW_DATA_LIDAR_MAC_ADDRESS : LiDAR: set/get MAC address

      OB_RAW_DATA_LIDAR_SUBNET_MASK : LiDAR: set/get subnet mask

      OB_PROP_LIDAR_WORK_MODE_INT : LiDAR: set/get work mode

      OB_PROP_LIDAR_APPLY_CONFIGS_INT : LiDAR: apply configs

      OB_PROP_LIDAR_MEMS_FOV_SIZE_FLOAT : LiDAR: set/get mems fov size

      OB_PROP_LIDAR_MEMS_FRENQUENCY_FLOAT : LiDAR: set/get mems frequency

      OB_RAW_DATA_LIDAR_PRODUCT_MODEL : LiDAR: get product model

      OB_RAW_DATA_LIDAR_FIRMWARE_VERSION : LiDAR: get firmware version

      OB_RAW_DATA_LIDAR_FPGA_VERSION : LiDAR: get fpga version

      OB_PROP_LIDAR_WARNING_INFO_INT : LiDAR: get warning info

      OB_PROP_LIDAR_MOTOR_SPIN_SPEED_INT : LiDAR: get realtime motor spin speed, unit:0.01rpm

      OB_PROP_LIDAR_MCU_TEMPERATURE_INT : LiDAR: get mcu temperature, uint: 0.01degrees delsius

      OB_PROP_LIDAR_APD_TEMPERATURE_INT : LiDAR: get apd temperature, uint: 0.01degrees delsius

      OB_PROP_LIDAR_SPECIFIC_MODE_INT : LiDAR: get/set specific mode

      OB_PROP_LIDAR_REPETITIVE_SCAN_MODE_INT : LiDAR: get/set repetitive scan mode

      OB_PROP_DEPTH_NOISE_REMOVAL_FILTER_BOOL : depth noise removal filter

      OB_DEVICE_AUTO_CAPTURE_ENABLE_BOOL : soft trigger auto capture enable, use in OB_MULTI_DEVICE_SYNC_MODE_SOFTWARE_TRIGGERING mode

      OB_DEVICE_AUTO_CAPTURE_INTERVAL_TIME_INT : soft trigger auto capture interval time, use in OB_MULTI_DEVICE_SYNC_MODE_SOFTWARE_TRIGGERING mode

      OB_DEVICE_PTP_CLOCK_SYNC_ENABLE_BOOL : PTP time synchronization enable

      OB_PROP_DEBUG_ESGM_CONFIDENCE_FLOAT : Confidence degree
    """

    OB_DEVICE_AUTO_CAPTURE_ENABLE_BOOL: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_DEVICE_AUTO_CAPTURE_ENABLE_BOOL: 216>
    OB_DEVICE_AUTO_CAPTURE_INTERVAL_TIME_INT: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_DEVICE_AUTO_CAPTURE_INTERVAL_TIME_INT: 217>
    OB_DEVICE_PTP_CLOCK_SYNC_ENABLE_BOOL: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_DEVICE_PTP_CLOCK_SYNC_ENABLE_BOOL: 223>
    OB_PROP_ANTI_COLLUSION_ACTIVATION_STATUS_BOOL: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_ANTI_COLLUSION_ACTIVATION_STATUS_BOOL: 64>
    OB_PROP_BOOT_INTO_RECOVERY_MODE_BOOL: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_BOOT_INTO_RECOVERY_MODE_BOOL: 132>
    OB_PROP_BRT_BOOL: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_BRT_BOOL: 86>
    OB_PROP_CAPTURE_IMAGE_FRAME_NUMBER_INT: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_CAPTURE_IMAGE_FRAME_NUMBER_INT: 113>
    OB_PROP_CAPTURE_IMAGE_NUMBER_INTERVAL_INT: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_CAPTURE_IMAGE_NUMBER_INTERVAL_INT: 136>
    OB_PROP_CAPTURE_IMAGE_SIGNAL_BOOL: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_CAPTURE_IMAGE_SIGNAL_BOOL: 107>
    OB_PROP_CAPTURE_IMAGE_TIME_INTERVAL_INT: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_CAPTURE_IMAGE_TIME_INTERVAL_INT: 135>
    OB_PROP_CAPTURE_INTERVAL_MODE_INT: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_CAPTURE_INTERVAL_MODE_INT: 134>
    OB_PROP_CHECK_PPS_SYNC_IN_SIGNAL_BOOL: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_CHECK_PPS_SYNC_IN_SIGNAL_BOOL: 195>
    OB_PROP_COLOR_AE_MAX_EXPOSURE_INT: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_COLOR_AE_MAX_EXPOSURE_INT: 189>
    OB_PROP_COLOR_AE_MAX_GAIN_INT: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_COLOR_AE_MAX_GAIN_INT: 2030>
    OB_PROP_COLOR_ANTI_FLICKER_BOOL: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_COLOR_ANTI_FLICKER_BOOL: 259>
    OB_PROP_COLOR_AUTO_EXPOSURE_BOOL: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_COLOR_AUTO_EXPOSURE_BOOL: 2000>
    OB_PROP_COLOR_AUTO_EXPOSURE_PRIORITY_INT: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_COLOR_AUTO_EXPOSURE_PRIORITY_INT: 2012>
    OB_PROP_COLOR_AUTO_WHITE_BALANCE_BOOL: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_COLOR_AUTO_WHITE_BALANCE_BOOL: 2003>
    OB_PROP_COLOR_BACKLIGHT_COMPENSATION_INT: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_COLOR_BACKLIGHT_COMPENSATION_INT: 2013>
    OB_PROP_COLOR_BRIGHTNESS_INT: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_COLOR_BRIGHTNESS_INT: 2005>
    OB_PROP_COLOR_CONTRAST_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_COLOR_CONTRAST_INT: 2009>
    OB_PROP_COLOR_DENOISING_LEVEL_INT: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_COLOR_DENOISING_LEVEL_INT: 5525>
    OB_PROP_COLOR_EXPOSURE_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_COLOR_EXPOSURE_INT: 2001>
    OB_PROP_COLOR_FLIP_BOOL: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_COLOR_FLIP_BOOL: 82>
    OB_PROP_COLOR_FOCUS_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_COLOR_FOCUS_INT: 2038>
    OB_PROP_COLOR_GAIN_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_COLOR_GAIN_INT: 2002>
    OB_PROP_COLOR_GAMMA_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_COLOR_GAMMA_INT: 2010>
    OB_PROP_COLOR_HDR_BOOL: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_COLOR_HDR_BOOL: 2034>
    OB_PROP_COLOR_HUE_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_COLOR_HUE_INT: 2014>
    OB_PROP_COLOR_LEFT_FLIP_BOOL: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_COLOR_LEFT_FLIP_BOOL: 253>
    OB_PROP_COLOR_LEFT_MIRROR_BOOL: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_COLOR_LEFT_MIRROR_BOOL: 252>
    OB_PROP_COLOR_LEFT_ROTATE_INT: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_COLOR_LEFT_ROTATE_INT: 251>
    OB_PROP_COLOR_MAXIMAL_SHUTTER_INT: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_COLOR_MAXIMAL_SHUTTER_INT: 2031>
    OB_PROP_COLOR_MIRROR_BOOL: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_COLOR_MIRROR_BOOL: 81>
    OB_PROP_COLOR_POWER_LINE_FREQUENCY_INT: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_COLOR_POWER_LINE_FREQUENCY_INT: 2015>
    OB_PROP_COLOR_PRESET_PRIORITY_INT: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_COLOR_PRESET_PRIORITY_INT: 255>
    OB_PROP_COLOR_RIGHT_FLIP_BOOL: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_COLOR_RIGHT_FLIP_BOOL: 244>
    OB_PROP_COLOR_RIGHT_MIRROR_BOOL: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_COLOR_RIGHT_MIRROR_BOOL: 243>
    OB_PROP_COLOR_RIGHT_ROTATE_INT: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_COLOR_RIGHT_ROTATE_INT: 242>
    OB_PROP_COLOR_ROI_BRIGHTNESS_INT: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_COLOR_ROI_BRIGHTNESS_INT: 249>
    OB_PROP_COLOR_ROLL_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_COLOR_ROLL_INT: 2011>
    OB_PROP_COLOR_ROTATE_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_COLOR_ROTATE_INT: 115>
    OB_PROP_COLOR_SATURATION_INT: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_COLOR_SATURATION_INT: 2008>
    OB_PROP_COLOR_SHARPNESS_INT: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_COLOR_SHARPNESS_INT: 2006>
    OB_PROP_COLOR_SHUTTER_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_COLOR_SHUTTER_INT: 2007>
    OB_PROP_COLOR_WHITE_BALANCE_INT: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_COLOR_WHITE_BALANCE_INT: 2004>
    OB_PROP_CONFIDENCE_FLIP_BOOL: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_CONFIDENCE_FLIP_BOOL: 230>
    OB_PROP_CONFIDENCE_MIRROR_BOOL: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_CONFIDENCE_MIRROR_BOOL: 229>
    OB_PROP_CONFIDENCE_ROTATE_INT: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_CONFIDENCE_ROTATE_INT: 231>
    OB_PROP_CONFIDENCE_STREAM_FILTER_BOOL: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_CONFIDENCE_STREAM_FILTER_BOOL: 226>
    OB_PROP_CONFIDENCE_STREAM_FILTER_THRESHOLD_INT: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_CONFIDENCE_STREAM_FILTER_THRESHOLD_INT: 227>
    OB_PROP_CPU_TEMPERATURE_CALIBRATION_BOOL: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_CPU_TEMPERATURE_CALIBRATION_BOOL: 199>
    OB_PROP_D2C_PREPROCESS_BOOL: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_D2C_PREPROCESS_BOOL: 91>
    OB_PROP_DC_POWER_STATE_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_DC_POWER_STATE_INT: 122>
    OB_PROP_DEBUG_ESGM_CONFIDENCE_FLOAT: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_DEBUG_ESGM_CONFIDENCE_FLOAT: 5013>
    OB_PROP_DEPTH_ALIGN_HARDWARE_BOOL: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_DEPTH_ALIGN_HARDWARE_BOOL: 42>
    OB_PROP_DEPTH_ALIGN_HARDWARE_MODE_INT: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_DEPTH_ALIGN_HARDWARE_MODE_INT: 63>
    OB_PROP_DEPTH_AUTO_EXPOSURE_BOOL: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_DEPTH_AUTO_EXPOSURE_BOOL: 2016>
    OB_PROP_DEPTH_AUTO_EXPOSURE_PRIORITY_INT: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_DEPTH_AUTO_EXPOSURE_PRIORITY_INT: 2052>
    OB_PROP_DEPTH_CROPPING_MODE_INT: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_DEPTH_CROPPING_MODE_INT: 90>
    OB_PROP_DEPTH_EXPOSURE_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_DEPTH_EXPOSURE_INT: 2017>
    OB_PROP_DEPTH_FLIP_BOOL: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_DEPTH_FLIP_BOOL: 15>
    OB_PROP_DEPTH_GAIN_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_DEPTH_GAIN_INT: 2018>
    OB_PROP_DEPTH_HOLEFILTER_BOOL: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_DEPTH_HOLEFILTER_BOOL: 17>
    OB_PROP_DEPTH_INDUSTRY_MODE_INT: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_DEPTH_INDUSTRY_MODE_INT: 3024>
    OB_PROP_DEPTH_MAX_DIFF_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_DEPTH_MAX_DIFF_INT: 40>
    OB_PROP_DEPTH_MAX_SPECKLE_SIZE_INT: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_DEPTH_MAX_SPECKLE_SIZE_INT: 41>
    OB_PROP_DEPTH_MIRROR_BOOL: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_DEPTH_MIRROR_BOOL: 14>
    OB_PROP_DEPTH_NOISE_REMOVAL_FILTER_BOOL: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_DEPTH_SOFT_FILTER_BOOL: 24>
    OB_PROP_DEPTH_NOISE_REMOVAL_FILTER_MAX_DIFF_INT: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_DEPTH_MAX_DIFF_INT: 40>
    OB_PROP_DEPTH_NOISE_REMOVAL_FILTER_MAX_SPECKLE_SIZE_INT: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_DEPTH_MAX_SPECKLE_SIZE_INT: 41>
    OB_PROP_DEPTH_POSTFILTER_BOOL: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_DEPTH_POSTFILTER_BOOL: 16>
    OB_PROP_DEPTH_PRECISION_LEVEL_INT: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_DEPTH_PRECISION_LEVEL_INT: 75>
    OB_PROP_DEPTH_RM_FILTER_BOOL: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_DEPTH_RM_FILTER_BOOL: 2029>
    OB_PROP_DEPTH_ROTATE_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_DEPTH_ROTATE_INT: 118>
    OB_PROP_DEPTH_SOFT_FILTER_BOOL: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_DEPTH_SOFT_FILTER_BOOL: 24>
    OB_PROP_DEPTH_UNIT_FLEXIBLE_ADJUSTMENT_FLOAT: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_DEPTH_UNIT_FLEXIBLE_ADJUSTMENT_FLOAT: 176>
    OB_PROP_DEPTH_WITH_CONFIDENCE_STREAM_ENABLE_BOOL: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_DEPTH_WITH_CONFIDENCE_STREAM_ENABLE_BOOL: 224>
    OB_PROP_DEVICE_AE_REFERENCE_INT: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_DEVICE_AE_REFERENCE_INT: 247>
    OB_PROP_DEVICE_AE_STRATEGY_INT: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_DEVICE_AE_STRATEGY_INT: 248>
    OB_PROP_DEVICE_COMMUNICATION_TYPE_INT: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_DEVICE_COMMUNICATION_TYPE_INT: 97>
    OB_PROP_DEVICE_DEVELOPMENT_MODE_INT: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_DEVICE_DEVELOPMENT_MODE_INT: 129>
    OB_PROP_DEVICE_IN_RECOVERY_MODE_BOOL: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_DEVICE_IN_RECOVERY_MODE_BOOL: 133>
    OB_PROP_DEVICE_OFFLINE_AFTER_IP_CONFIG_APPLY: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_DEVICE_OFFLINE_AFTER_IP_CONFIG_APPLY: 5555>
    OB_PROP_DEVICE_PERFORMANCE_MODE_INT: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_DEVICE_PERFORMANCE_MODE_INT: 3028>
    OB_PROP_DEVICE_REBOOT_DELAY_INT: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_DEVICE_REBOOT_DELAY_INT: 142>
    OB_PROP_DEVICE_REPOWER_BOOL: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_DEVICE_REPOWER_BOOL: 202>
    OB_PROP_DEVICE_USB3_REPEAT_IDENTIFY_BOOL: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_DEVICE_USB3_REPEAT_IDENTIFY_BOOL: 141>
    OB_PROP_DEVICE_WORK_MODE_INT: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_DEVICE_WORK_MODE_INT: 95>
    OB_PROP_DHCP_ASSIGN_IP_TIMEOUT_INT: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_DHCP_ASSIGN_IP_TIMEOUT_INT: 261>
    OB_PROP_DISPARITY_TO_DEPTH_BOOL: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_DISPARITY_TO_DEPTH_BOOL: 85>
    OB_PROP_DISP_SEARCH_OFFSET_INT: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_DISP_SEARCH_OFFSET_INT: 196>
    OB_PROP_DISP_SEARCH_RANGE_MODE_INT: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_DISP_SEARCH_RANGE_MODE_INT: 191>
    OB_PROP_EXTERNAL_SIGNAL_RESET_BOOL: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_EXTERNAL_SIGNAL_RESET_BOOL: 88>
    OB_PROP_FAN_WORK_MODE_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_FAN_WORK_MODE_INT: 62>
    OB_PROP_FLOOD_BOOL: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_FLOOD_BOOL: 6>
    OB_PROP_FLOOD_LEVEL_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_FLOOD_LEVEL_INT: 7>
    OB_PROP_FRAME_INTERLEAVE_CONFIG_INDEX_INT: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_FRAME_INTERLEAVE_CONFIG_INDEX_INT: 204>
    OB_PROP_FRAME_INTERLEAVE_ENABLE_BOOL: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_FRAME_INTERLEAVE_ENABLE_BOOL: 205>
    OB_PROP_FRAME_INTERLEAVE_LASER_PATTERN_SYNC_DELAY_INT: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_FRAME_INTERLEAVE_LASER_PATTERN_SYNC_DELAY_INT: 206>
    OB_PROP_GPM_BOOL: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_GPM_BOOL: 93>
    OB_PROP_HARDWARE_DISTORTION_SWITCH_BOOL: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_HARDWARE_DISTORTION_SWITCH_BOOL: 61>
    OB_PROP_HDR_MERGE_BOOL: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_HDR_MERGE_BOOL: 2037>
    OB_PROP_HEARTBEAT_BOOL: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_HEARTBEAT_BOOL: 89>
    OB_PROP_HW_NOISE_REMOVE_FILTER_ENABLE_BOOL: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_HW_NOISE_REMOVE_FILTER_ENABLE_BOOL: 211>
    OB_PROP_HW_NOISE_REMOVE_FILTER_THRESHOLD_FLOAT: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_HW_NOISE_REMOVE_FILTER_THRESHOLD_FLOAT: 212>
    OB_PROP_INDICATOR_LIGHT_BOOL: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_INDICATOR_LIGHT_BOOL: 83>
    OB_PROP_INTRA_CAMERA_SYNC_REFERENCE_INT: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_INTRA_CAMERA_SYNC_REFERENCE_INT: 236>
    OB_PROP_IR_AE_MAX_EXPOSURE_INT: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_IR_AE_MAX_EXPOSURE_INT: 190>
    OB_PROP_IR_AUTO_EXPOSURE_BOOL: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_IR_AUTO_EXPOSURE_BOOL: 2025>
    OB_PROP_IR_BRIGHTNESS_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_IR_BRIGHTNESS_INT: 184>
    OB_PROP_IR_CHANNEL_DATA_SOURCE_INT: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_IR_CHANNEL_DATA_SOURCE_INT: 2028>
    OB_PROP_IR_EXPOSURE_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_IR_EXPOSURE_INT: 2026>
    OB_PROP_IR_FLIP_BOOL: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_IR_FLIP_BOOL: 19>
    OB_PROP_IR_GAIN_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_IR_GAIN_INT: 2027>
    OB_PROP_IR_LONG_EXPOSURE_BOOL: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_IR_LONG_EXPOSURE_BOOL: 2035>
    OB_PROP_IR_MIRROR_BOOL: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_IR_MIRROR_BOOL: 18>
    OB_PROP_IR_RECTIFY_BOOL: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_IR_RECTIFY_BOOL: 2040>
    OB_PROP_IR_RIGHT_FLIP_BOOL: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_IR_RIGHT_FLIP_BOOL: 114>
    OB_PROP_IR_RIGHT_MIRROR_BOOL: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_IR_RIGHT_MIRROR_BOOL: 112>
    OB_PROP_IR_RIGHT_ROTATE_INT: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_IR_RIGHT_ROTATE_INT: 117>
    OB_PROP_IR_ROTATE_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_IR_ROTATE_INT: 116>
    OB_PROP_IR_SHORT_EXPOSURE_BOOL: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_IR_SHORT_EXPOSURE_BOOL: 2032>
    OB_PROP_LASER_ALWAYS_ON_BOOL: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_LASER_ALWAYS_ON_BOOL: 174>
    OB_PROP_LASER_BOOL: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_LASER_BOOL: 3>
    OB_PROP_LASER_CONTROL_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_LASER_CONTROL_INT: 182>
    OB_PROP_LASER_CURRENT_FLOAT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_LASER_CURRENT_FLOAT: 5>
    OB_PROP_LASER_ENERGY_LEVEL_INT: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_LASER_POWER_LEVEL_CONTROL_INT: 99>
    OB_PROP_LASER_HIGH_TEMPERATURE_PROTECT_BOOL: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_LASER_HIGH_TEMPERATURE_PROTECT_BOOL: 193>
    OB_PROP_LASER_HW_ENERGY_LEVEL_INT: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_LASER_POWER_ACTUAL_LEVEL_INT: 119>
    OB_PROP_LASER_MODE_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_LASER_MODE_INT: 79>
    OB_PROP_LASER_ON_OFF_PATTERN_INT: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_LASER_ON_OFF_PATTERN_INT: 175>
    OB_PROP_LASER_OVERCURRENT_PROTECTION_STATUS_BOOL: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_LASER_OVERCURRENT_PROTECTION_STATUS_BOOL: 148>
    OB_PROP_LASER_POWER_ACTUAL_LEVEL_INT: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_LASER_POWER_ACTUAL_LEVEL_INT: 119>
    OB_PROP_LASER_POWER_LEVEL_CONTROL_INT: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_LASER_POWER_LEVEL_CONTROL_INT: 99>
    OB_PROP_LASER_PULSE_WIDTH_INT: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_LASER_PULSE_WIDTH_INT: 4>
    OB_PROP_LASER_PULSE_WIDTH_PROTECTION_STATUS_BOOL: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_LASER_PULSE_WIDTH_PROTECTION_STATUS_BOOL: 149>
    OB_PROP_LDP_BOOL: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_LDP_BOOL: 2>
    OB_PROP_LDP_MEASURE_DISTANCE_INT: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_LDP_MEASURE_DISTANCE_INT: 100>
    OB_PROP_LDP_STATUS_BOOL: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_LDP_STATUS_BOOL: 32>
    OB_PROP_LIDAR_APD_TEMPERATURE_INT: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_LIDAR_APD_TEMPERATURE_INT: 8015>
    OB_PROP_LIDAR_APPLY_CONFIGS_INT: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_LIDAR_APPLY_CONFIGS_INT: 8005>
    OB_PROP_LIDAR_MCU_TEMPERATURE_INT: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_LIDAR_MCU_TEMPERATURE_INT: 8014>
    OB_PROP_LIDAR_MEMS_FOV_SIZE_FLOAT: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_LIDAR_MEMS_FOV_SIZE_FLOAT: 8007>
    OB_PROP_LIDAR_MEMS_FRENQUENCY_FLOAT: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_LIDAR_MEMS_FRENQUENCY_FLOAT: 8008>
    OB_PROP_LIDAR_MOTOR_SPIN_SPEED_INT: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_LIDAR_MOTOR_SPIN_SPEED_INT: 8013>
    OB_PROP_LIDAR_PORT_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_LIDAR_PORT_INT: 8001>
    OB_PROP_LIDAR_REPETITIVE_SCAN_MODE_INT: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_LIDAR_REPETITIVE_SCAN_MODE_INT: 8017>
    OB_PROP_LIDAR_SPECIFIC_MODE_INT: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_LIDAR_SPECIFIC_MODE_INT: 8016>
    OB_PROP_LIDAR_TAIL_FILTER_LEVEL_INT: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_LIDAR_TAIL_FILTER_LEVEL_INT: 8006>
    OB_PROP_LIDAR_WARNING_INFO_INT: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_LIDAR_WARNING_INFO_INT: 8012>
    OB_PROP_LIDAR_WORK_MODE_INT: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_LIDAR_WORK_MODE_INT: 8004>
    OB_PROP_LOW_EXPOSURE_LASER_CONTROL_BOOL: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_LOW_EXPOSURE_LASER_CONTROL_BOOL: 194>
    OB_PROP_MAX_DEPTH_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_MAX_DEPTH_INT: 23>
    OB_PROP_MIN_DEPTH_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_MIN_DEPTH_INT: 22>
    OB_PROP_NETWORK_BANDWIDTH_TYPE_INT: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_NETWORK_BANDWIDTH_TYPE_INT: 3027>
    OB_PROP_ON_CHIP_CALIBRATION_ENABLE_BOOL: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_ON_CHIP_CALIBRATION_ENABLE_BOOL: 210>
    OB_PROP_ON_CHIP_CALIBRATION_HEALTH_CHECK_FLOAT: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_ON_CHIP_CALIBRATION_HEALTH_CHECK_FLOAT: 209>
    OB_PROP_RECTIFY2_BOOL: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_RECTIFY2_BOOL: 80>
    OB_PROP_RESTORE_FACTORY_SETTINGS_BOOL: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_RESTORE_FACTORY_SETTINGS_BOOL: 131>
    OB_PROP_RGB_CUSTOM_CROP_BOOL: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_RGB_CUSTOM_CROP_BOOL: 94>
    OB_PROP_SDK_ACCEL_FRAME_TRANSFORMED_BOOL: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_SDK_ACCEL_FRAME_TRANSFORMED_BOOL: 3009>
    OB_PROP_SDK_DEPTH_FRAME_UNPACK_BOOL: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_SDK_DEPTH_FRAME_UNPACK_BOOL: 3007>
    OB_PROP_SDK_DISPARITY_TO_DEPTH_BOOL: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_SDK_DISPARITY_TO_DEPTH_BOOL: 3004>
    OB_PROP_SDK_GYRO_FRAME_TRANSFORMED_BOOL: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_SDK_GYRO_FRAME_TRANSFORMED_BOOL: 3010>
    OB_PROP_SDK_IR_FRAME_UNPACK_BOOL: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_SDK_IR_FRAME_UNPACK_BOOL: 3008>
    OB_PROP_SDK_IR_LEFT_FRAME_UNPACK_BOOL: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_SDK_IR_LEFT_FRAME_UNPACK_BOOL: 3011>
    OB_PROP_SDK_IR_RIGHT_FRAME_UNPACK_BOOL: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_SDK_IR_RIGHT_FRAME_UNPACK_BOOL: 3012>
    OB_PROP_SKIP_FRAME_BOOL: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_SKIP_FRAME_BOOL: 2036>
    OB_PROP_SLAVE_DEVICE_SYNC_STATUS_BOOL: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_SLAVE_DEVICE_SYNC_STATUS_BOOL: 188>
    OB_PROP_SWITCH_IR_MODE_INT: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_SWITCH_IR_MODE_INT: 98>
    OB_PROP_SYNC_SIGNAL_TRIGGER_OUT_BOOL: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_SYNC_SIGNAL_TRIGGER_OUT_BOOL: 130>
    OB_PROP_TEMPERATURE_COMPENSATION_BOOL: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_TEMPERATURE_COMPENSATION_BOOL: 8>
    OB_PROP_TIMER_RESET_DELAY_US_INT: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_TIMER_RESET_DELAY_US_INT: 106>
    OB_PROP_TIMER_RESET_ENABLE_BOOL: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_TIMER_RESET_ENABLE_BOOL: 140>
    OB_PROP_TIMER_RESET_SIGNAL_BOOL: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_TIMER_RESET_SIGNAL_BOOL: 104>
    OB_PROP_TIMER_RESET_TRIGGER_OUT_ENABLE_BOOL: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_TIMER_RESET_TRIGGER_OUT_ENABLE_BOOL: 105>
    OB_PROP_TIMESTAMP_OFFSET_INT: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_TIMESTAMP_OFFSET_INT: 43>
    OB_PROP_TOF_FILTER_RANGE_INT: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_TOF_FILTER_RANGE_INT: 76>
    OB_PROP_USB_POWER_STATE_INT: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_PROP_USB_POWER_STATE_INT: 121>
    OB_PROP_WATCHDOG_BOOL: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_PROP_WATCHDOG_BOOL: 87>
    OB_RAW_DATA_CAMERA_CALIB_JSON_FILE: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_RAW_DATA_CAMERA_CALIB_JSON_FILE: 4029>
    OB_RAW_DATA_LIDAR_FIRMWARE_VERSION: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_RAW_DATA_LIDAR_FIRMWARE_VERSION: 8010>
    OB_RAW_DATA_LIDAR_FPGA_VERSION: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_RAW_DATA_LIDAR_FPGA_VERSION: 8011>
    OB_RAW_DATA_LIDAR_IP_ADDRESS: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_RAW_DATA_LIDAR_IP_ADDRESS: 8000>
    OB_RAW_DATA_LIDAR_MAC_ADDRESS: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_RAW_DATA_LIDAR_MAC_ADDRESS: 8002>
    OB_RAW_DATA_LIDAR_PRODUCT_MODEL: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_RAW_DATA_LIDAR_PRODUCT_MODEL: 8009>
    OB_RAW_DATA_LIDAR_SUBNET_MASK: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_RAW_DATA_LIDAR_SUBNET_MASK: 8003>
    OB_STRUCT_ASIC_SERIAL_NUMBER: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_STRUCT_ASIC_SERIAL_NUMBER: 1063>
    OB_STRUCT_BASELINE_CALIBRATION_PARAM: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_STRUCT_BASELINE_CALIBRATION_PARAM: 1002>
    OB_STRUCT_COLOR_AE_ROI: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_STRUCT_COLOR_AE_ROI: 1060>
    OB_STRUCT_COLOR_SYNCED_EXPOSURE_PARAM: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_STRUCT_COLOR_SYNCED_EXPOSURE_PARAM: 1077>
    OB_STRUCT_CURRENT_DEPTH_ALG_MODE: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_STRUCT_CURRENT_DEPTH_ALG_MODE: 1043>
    OB_STRUCT_DEPTH_AE_ROI: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_STRUCT_DEPTH_AE_ROI: 1061>
    OB_STRUCT_DEPTH_HDR_CONFIG: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_STRUCT_DEPTH_HDR_CONFIG: 1059>
    OB_STRUCT_DEPTH_PRECISION_SUPPORT_LIST: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_STRUCT_DEPTH_PRECISION_SUPPORT_LIST: 1045>
    OB_STRUCT_DEVICE_IP_ADDR_CONFIG: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_STRUCT_DEVICE_IP_ADDR_CONFIG: 1041>
    OB_STRUCT_DEVICE_IP_ADDR_CONFIG_V2: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_STRUCT_DEVICE_IP_ADDR_CONFIG_V2: 1088>
    OB_STRUCT_DEVICE_SERIAL_NUMBER: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_STRUCT_DEVICE_SERIAL_NUMBER: 1035>
    OB_STRUCT_DEVICE_STATIC_IP_CONFIG_RECORD: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_STRUCT_DEVICE_STATIC_IP_CONFIG_RECORD: 1053>
    OB_STRUCT_DEVICE_TEMPERATURE: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_STRUCT_DEVICE_TEMPERATURE: 1003>
    OB_STRUCT_DEVICE_TIME: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_STRUCT_DEVICE_TIME: 1037>
    OB_STRUCT_DISP_OFFSET_CONFIG: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_STRUCT_DISP_OFFSET_CONFIG: 1064>
    OB_STRUCT_MULTI_DEVICE_SYNC_CONFIG: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_STRUCT_MULTI_DEVICE_SYNC_CONFIG: 1038>
    OB_STRUCT_PRESET_RESOLUTION_CONFIG: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_STRUCT_PRESET_RESOLUTION_CONFIG: 1069>
    OB_STRUCT_RGB_CROP_ROI: typing.ClassVar[OBPropertyID]  # value = <OBPropertyID.OB_STRUCT_RGB_CROP_ROI: 1040>
    OB_STRUCT_TOF_EXPOSURE_THRESHOLD_CONTROL: typing.ClassVar[
        OBPropertyID
    ]  # value = <OBPropertyID.OB_STRUCT_TOF_EXPOSURE_THRESHOLD_CONTROL: 1024>
    __members__: typing.ClassVar[
        dict[str, OBPropertyID]
    ]  # value = {'OB_PROP_LDP_BOOL': <OBPropertyID.OB_PROP_LDP_BOOL: 2>, 'OB_PROP_LASER_BOOL': <OBPropertyID.OB_PROP_LASER_BOOL: 3>, 'OB_PROP_LASER_PULSE_WIDTH_INT': <OBPropertyID.OB_PROP_LASER_PULSE_WIDTH_INT: 4>, 'OB_PROP_LASER_CURRENT_FLOAT': <OBPropertyID.OB_PROP_LASER_CURRENT_FLOAT: 5>, 'OB_PROP_FLOOD_BOOL': <OBPropertyID.OB_PROP_FLOOD_BOOL: 6>, 'OB_PROP_FLOOD_LEVEL_INT': <OBPropertyID.OB_PROP_FLOOD_LEVEL_INT: 7>, 'OB_PROP_TEMPERATURE_COMPENSATION_BOOL': <OBPropertyID.OB_PROP_TEMPERATURE_COMPENSATION_BOOL: 8>, 'OB_PROP_DEPTH_MIRROR_BOOL': <OBPropertyID.OB_PROP_DEPTH_MIRROR_BOOL: 14>, 'OB_PROP_DEPTH_FLIP_BOOL': <OBPropertyID.OB_PROP_DEPTH_FLIP_BOOL: 15>, 'OB_PROP_DEPTH_POSTFILTER_BOOL': <OBPropertyID.OB_PROP_DEPTH_POSTFILTER_BOOL: 16>, 'OB_PROP_DEPTH_HOLEFILTER_BOOL': <OBPropertyID.OB_PROP_DEPTH_HOLEFILTER_BOOL: 17>, 'OB_PROP_IR_MIRROR_BOOL': <OBPropertyID.OB_PROP_IR_MIRROR_BOOL: 18>, 'OB_PROP_IR_FLIP_BOOL': <OBPropertyID.OB_PROP_IR_FLIP_BOOL: 19>, 'OB_PROP_MIN_DEPTH_INT': <OBPropertyID.OB_PROP_MIN_DEPTH_INT: 22>, 'OB_PROP_MAX_DEPTH_INT': <OBPropertyID.OB_PROP_MAX_DEPTH_INT: 23>, 'OB_PROP_DEPTH_SOFT_FILTER_BOOL': <OBPropertyID.OB_PROP_DEPTH_SOFT_FILTER_BOOL: 24>, 'OB_PROP_LDP_STATUS_BOOL': <OBPropertyID.OB_PROP_LDP_STATUS_BOOL: 32>, 'OB_PROP_DEPTH_MAX_DIFF_INT': <OBPropertyID.OB_PROP_DEPTH_MAX_DIFF_INT: 40>, 'OB_PROP_DEPTH_MAX_SPECKLE_SIZE_INT': <OBPropertyID.OB_PROP_DEPTH_MAX_SPECKLE_SIZE_INT: 41>, 'OB_PROP_DEPTH_NOISE_REMOVAL_FILTER_MAX_DIFF_INT': <OBPropertyID.OB_PROP_DEPTH_MAX_DIFF_INT: 40>, 'OB_PROP_DEPTH_NOISE_REMOVAL_FILTER_MAX_SPECKLE_SIZE_INT': <OBPropertyID.OB_PROP_DEPTH_MAX_SPECKLE_SIZE_INT: 41>, 'OB_PROP_DEPTH_ALIGN_HARDWARE_BOOL': <OBPropertyID.OB_PROP_DEPTH_ALIGN_HARDWARE_BOOL: 42>, 'OB_PROP_TIMESTAMP_OFFSET_INT': <OBPropertyID.OB_PROP_TIMESTAMP_OFFSET_INT: 43>, 'OB_PROP_HARDWARE_DISTORTION_SWITCH_BOOL': <OBPropertyID.OB_PROP_HARDWARE_DISTORTION_SWITCH_BOOL: 61>, 'OB_PROP_FAN_WORK_MODE_INT': <OBPropertyID.OB_PROP_FAN_WORK_MODE_INT: 62>, 'OB_PROP_DEPTH_ALIGN_HARDWARE_MODE_INT': <OBPropertyID.OB_PROP_DEPTH_ALIGN_HARDWARE_MODE_INT: 63>, 'OB_PROP_ANTI_COLLUSION_ACTIVATION_STATUS_BOOL': <OBPropertyID.OB_PROP_ANTI_COLLUSION_ACTIVATION_STATUS_BOOL: 64>, 'OB_PROP_DEVICE_AE_REFERENCE_INT': <OBPropertyID.OB_PROP_DEVICE_AE_REFERENCE_INT: 247>, 'OB_PROP_DEVICE_AE_STRATEGY_INT': <OBPropertyID.OB_PROP_DEVICE_AE_STRATEGY_INT: 248>, 'OB_PROP_COLOR_ROI_BRIGHTNESS_INT': <OBPropertyID.OB_PROP_COLOR_ROI_BRIGHTNESS_INT: 249>, 'OB_PROP_COLOR_PRESET_PRIORITY_INT': <OBPropertyID.OB_PROP_COLOR_PRESET_PRIORITY_INT: 255>, 'OB_PROP_COLOR_ANTI_FLICKER_BOOL': <OBPropertyID.OB_PROP_COLOR_ANTI_FLICKER_BOOL: 259>, 'OB_PROP_DEPTH_PRECISION_LEVEL_INT': <OBPropertyID.OB_PROP_DEPTH_PRECISION_LEVEL_INT: 75>, 'OB_PROP_TOF_FILTER_RANGE_INT': <OBPropertyID.OB_PROP_TOF_FILTER_RANGE_INT: 76>, 'OB_PROP_LASER_MODE_INT': <OBPropertyID.OB_PROP_LASER_MODE_INT: 79>, 'OB_PROP_RECTIFY2_BOOL': <OBPropertyID.OB_PROP_RECTIFY2_BOOL: 80>, 'OB_PROP_COLOR_MIRROR_BOOL': <OBPropertyID.OB_PROP_COLOR_MIRROR_BOOL: 81>, 'OB_PROP_COLOR_FLIP_BOOL': <OBPropertyID.OB_PROP_COLOR_FLIP_BOOL: 82>, 'OB_PROP_INDICATOR_LIGHT_BOOL': <OBPropertyID.OB_PROP_INDICATOR_LIGHT_BOOL: 83>, 'OB_PROP_DISPARITY_TO_DEPTH_BOOL': <OBPropertyID.OB_PROP_DISPARITY_TO_DEPTH_BOOL: 85>, 'OB_PROP_BRT_BOOL': <OBPropertyID.OB_PROP_BRT_BOOL: 86>, 'OB_PROP_WATCHDOG_BOOL': <OBPropertyID.OB_PROP_WATCHDOG_BOOL: 87>, 'OB_PROP_EXTERNAL_SIGNAL_RESET_BOOL': <OBPropertyID.OB_PROP_EXTERNAL_SIGNAL_RESET_BOOL: 88>, 'OB_PROP_HEARTBEAT_BOOL': <OBPropertyID.OB_PROP_HEARTBEAT_BOOL: 89>, 'OB_PROP_DEPTH_CROPPING_MODE_INT': <OBPropertyID.OB_PROP_DEPTH_CROPPING_MODE_INT: 90>, 'OB_PROP_D2C_PREPROCESS_BOOL': <OBPropertyID.OB_PROP_D2C_PREPROCESS_BOOL: 91>, 'OB_PROP_GPM_BOOL': <OBPropertyID.OB_PROP_GPM_BOOL: 93>, 'OB_PROP_RGB_CUSTOM_CROP_BOOL': <OBPropertyID.OB_PROP_RGB_CUSTOM_CROP_BOOL: 94>, 'OB_PROP_DEVICE_WORK_MODE_INT': <OBPropertyID.OB_PROP_DEVICE_WORK_MODE_INT: 95>, 'OB_PROP_DEVICE_COMMUNICATION_TYPE_INT': <OBPropertyID.OB_PROP_DEVICE_COMMUNICATION_TYPE_INT: 97>, 'OB_PROP_SWITCH_IR_MODE_INT': <OBPropertyID.OB_PROP_SWITCH_IR_MODE_INT: 98>, 'OB_PROP_LASER_POWER_LEVEL_CONTROL_INT': <OBPropertyID.OB_PROP_LASER_POWER_LEVEL_CONTROL_INT: 99>, 'OB_PROP_LASER_ENERGY_LEVEL_INT': <OBPropertyID.OB_PROP_LASER_POWER_LEVEL_CONTROL_INT: 99>, 'OB_PROP_LASER_POWER_ACTUAL_LEVEL_INT': <OBPropertyID.OB_PROP_LASER_POWER_ACTUAL_LEVEL_INT: 119>, 'OB_PROP_LDP_MEASURE_DISTANCE_INT': <OBPropertyID.OB_PROP_LDP_MEASURE_DISTANCE_INT: 100>, 'OB_PROP_TIMER_RESET_SIGNAL_BOOL': <OBPropertyID.OB_PROP_TIMER_RESET_SIGNAL_BOOL: 104>, 'OB_PROP_TIMER_RESET_TRIGGER_OUT_ENABLE_BOOL': <OBPropertyID.OB_PROP_TIMER_RESET_TRIGGER_OUT_ENABLE_BOOL: 105>, 'OB_PROP_TIMER_RESET_DELAY_US_INT': <OBPropertyID.OB_PROP_TIMER_RESET_DELAY_US_INT: 106>, 'OB_PROP_CAPTURE_IMAGE_SIGNAL_BOOL': <OBPropertyID.OB_PROP_CAPTURE_IMAGE_SIGNAL_BOOL: 107>, 'OB_PROP_IR_RIGHT_MIRROR_BOOL': <OBPropertyID.OB_PROP_IR_RIGHT_MIRROR_BOOL: 112>, 'OB_PROP_CAPTURE_IMAGE_FRAME_NUMBER_INT': <OBPropertyID.OB_PROP_CAPTURE_IMAGE_FRAME_NUMBER_INT: 113>, 'OB_PROP_IR_RIGHT_FLIP_BOOL': <OBPropertyID.OB_PROP_IR_RIGHT_FLIP_BOOL: 114>, 'OB_PROP_COLOR_ROTATE_INT': <OBPropertyID.OB_PROP_COLOR_ROTATE_INT: 115>, 'OB_PROP_IR_ROTATE_INT': <OBPropertyID.OB_PROP_IR_ROTATE_INT: 116>, 'OB_PROP_IR_RIGHT_ROTATE_INT': <OBPropertyID.OB_PROP_IR_RIGHT_ROTATE_INT: 117>, 'OB_PROP_DEPTH_ROTATE_INT': <OBPropertyID.OB_PROP_DEPTH_ROTATE_INT: 118>, 'OB_PROP_COLOR_RIGHT_ROTATE_INT': <OBPropertyID.OB_PROP_COLOR_RIGHT_ROTATE_INT: 242>, 'OB_PROP_COLOR_RIGHT_MIRROR_BOOL': <OBPropertyID.OB_PROP_COLOR_RIGHT_MIRROR_BOOL: 243>, 'OB_PROP_COLOR_RIGHT_FLIP_BOOL': <OBPropertyID.OB_PROP_COLOR_RIGHT_FLIP_BOOL: 244>, 'OB_PROP_COLOR_LEFT_ROTATE_INT': <OBPropertyID.OB_PROP_COLOR_LEFT_ROTATE_INT: 251>, 'OB_PROP_COLOR_LEFT_MIRROR_BOOL': <OBPropertyID.OB_PROP_COLOR_LEFT_MIRROR_BOOL: 252>, 'OB_PROP_COLOR_LEFT_FLIP_BOOL': <OBPropertyID.OB_PROP_COLOR_LEFT_FLIP_BOOL: 253>, 'OB_PROP_LASER_HW_ENERGY_LEVEL_INT': <OBPropertyID.OB_PROP_LASER_POWER_ACTUAL_LEVEL_INT: 119>, 'OB_PROP_USB_POWER_STATE_INT': <OBPropertyID.OB_PROP_USB_POWER_STATE_INT: 121>, 'OB_PROP_DC_POWER_STATE_INT': <OBPropertyID.OB_PROP_DC_POWER_STATE_INT: 122>, 'OB_PROP_DEVICE_DEVELOPMENT_MODE_INT': <OBPropertyID.OB_PROP_DEVICE_DEVELOPMENT_MODE_INT: 129>, 'OB_PROP_SYNC_SIGNAL_TRIGGER_OUT_BOOL': <OBPropertyID.OB_PROP_SYNC_SIGNAL_TRIGGER_OUT_BOOL: 130>, 'OB_PROP_DEPTH_WITH_CONFIDENCE_STREAM_ENABLE_BOOL': <OBPropertyID.OB_PROP_DEPTH_WITH_CONFIDENCE_STREAM_ENABLE_BOOL: 224>, 'OB_PROP_CONFIDENCE_STREAM_FILTER_BOOL': <OBPropertyID.OB_PROP_CONFIDENCE_STREAM_FILTER_BOOL: 226>, 'OB_PROP_CONFIDENCE_STREAM_FILTER_THRESHOLD_INT': <OBPropertyID.OB_PROP_CONFIDENCE_STREAM_FILTER_THRESHOLD_INT: 227>, 'OB_PROP_CONFIDENCE_MIRROR_BOOL': <OBPropertyID.OB_PROP_CONFIDENCE_MIRROR_BOOL: 229>, 'OB_PROP_CONFIDENCE_FLIP_BOOL': <OBPropertyID.OB_PROP_CONFIDENCE_FLIP_BOOL: 230>, 'OB_PROP_CONFIDENCE_ROTATE_INT': <OBPropertyID.OB_PROP_CONFIDENCE_ROTATE_INT: 231>, 'OB_PROP_INTRA_CAMERA_SYNC_REFERENCE_INT': <OBPropertyID.OB_PROP_INTRA_CAMERA_SYNC_REFERENCE_INT: 236>, 'OB_PROP_RESTORE_FACTORY_SETTINGS_BOOL': <OBPropertyID.OB_PROP_RESTORE_FACTORY_SETTINGS_BOOL: 131>, 'OB_PROP_BOOT_INTO_RECOVERY_MODE_BOOL': <OBPropertyID.OB_PROP_BOOT_INTO_RECOVERY_MODE_BOOL: 132>, 'OB_PROP_DEVICE_IN_RECOVERY_MODE_BOOL': <OBPropertyID.OB_PROP_DEVICE_IN_RECOVERY_MODE_BOOL: 133>, 'OB_PROP_CAPTURE_INTERVAL_MODE_INT': <OBPropertyID.OB_PROP_CAPTURE_INTERVAL_MODE_INT: 134>, 'OB_PROP_CAPTURE_IMAGE_TIME_INTERVAL_INT': <OBPropertyID.OB_PROP_CAPTURE_IMAGE_TIME_INTERVAL_INT: 135>, 'OB_PROP_CAPTURE_IMAGE_NUMBER_INTERVAL_INT': <OBPropertyID.OB_PROP_CAPTURE_IMAGE_NUMBER_INTERVAL_INT: 136>, 'OB_PROP_TIMER_RESET_ENABLE_BOOL': <OBPropertyID.OB_PROP_TIMER_RESET_ENABLE_BOOL: 140>, 'OB_PROP_DEVICE_USB3_REPEAT_IDENTIFY_BOOL': <OBPropertyID.OB_PROP_DEVICE_USB3_REPEAT_IDENTIFY_BOOL: 141>, 'OB_PROP_DEVICE_REBOOT_DELAY_INT': <OBPropertyID.OB_PROP_DEVICE_REBOOT_DELAY_INT: 142>, 'OB_PROP_DHCP_ASSIGN_IP_TIMEOUT_INT': <OBPropertyID.OB_PROP_DHCP_ASSIGN_IP_TIMEOUT_INT: 261>, 'OB_PROP_LASER_OVERCURRENT_PROTECTION_STATUS_BOOL': <OBPropertyID.OB_PROP_LASER_OVERCURRENT_PROTECTION_STATUS_BOOL: 148>, 'OB_PROP_LASER_PULSE_WIDTH_PROTECTION_STATUS_BOOL': <OBPropertyID.OB_PROP_LASER_PULSE_WIDTH_PROTECTION_STATUS_BOOL: 149>, 'OB_PROP_LASER_ALWAYS_ON_BOOL': <OBPropertyID.OB_PROP_LASER_ALWAYS_ON_BOOL: 174>, 'OB_PROP_LASER_ON_OFF_PATTERN_INT': <OBPropertyID.OB_PROP_LASER_ON_OFF_PATTERN_INT: 175>, 'OB_PROP_DEPTH_UNIT_FLEXIBLE_ADJUSTMENT_FLOAT': <OBPropertyID.OB_PROP_DEPTH_UNIT_FLEXIBLE_ADJUSTMENT_FLOAT: 176>, 'OB_PROP_LASER_CONTROL_INT': <OBPropertyID.OB_PROP_LASER_CONTROL_INT: 182>, 'OB_PROP_IR_BRIGHTNESS_INT': <OBPropertyID.OB_PROP_IR_BRIGHTNESS_INT: 184>, 'OB_PROP_SLAVE_DEVICE_SYNC_STATUS_BOOL': <OBPropertyID.OB_PROP_SLAVE_DEVICE_SYNC_STATUS_BOOL: 188>, 'OB_PROP_COLOR_AE_MAX_EXPOSURE_INT': <OBPropertyID.OB_PROP_COLOR_AE_MAX_EXPOSURE_INT: 189>, 'OB_PROP_IR_AE_MAX_EXPOSURE_INT': <OBPropertyID.OB_PROP_IR_AE_MAX_EXPOSURE_INT: 190>, 'OB_PROP_DISP_SEARCH_RANGE_MODE_INT': <OBPropertyID.OB_PROP_DISP_SEARCH_RANGE_MODE_INT: 191>, 'OB_PROP_LASER_HIGH_TEMPERATURE_PROTECT_BOOL': <OBPropertyID.OB_PROP_LASER_HIGH_TEMPERATURE_PROTECT_BOOL: 193>, 'OB_PROP_LOW_EXPOSURE_LASER_CONTROL_BOOL': <OBPropertyID.OB_PROP_LOW_EXPOSURE_LASER_CONTROL_BOOL: 194>, 'OB_PROP_CHECK_PPS_SYNC_IN_SIGNAL_BOOL': <OBPropertyID.OB_PROP_CHECK_PPS_SYNC_IN_SIGNAL_BOOL: 195>, 'OB_PROP_DISP_SEARCH_OFFSET_INT': <OBPropertyID.OB_PROP_DISP_SEARCH_OFFSET_INT: 196>, 'OB_PROP_CPU_TEMPERATURE_CALIBRATION_BOOL': <OBPropertyID.OB_PROP_CPU_TEMPERATURE_CALIBRATION_BOOL: 199>, 'OB_PROP_DEVICE_REPOWER_BOOL': <OBPropertyID.OB_PROP_DEVICE_REPOWER_BOOL: 202>, 'OB_PROP_FRAME_INTERLEAVE_CONFIG_INDEX_INT': <OBPropertyID.OB_PROP_FRAME_INTERLEAVE_CONFIG_INDEX_INT: 204>, 'OB_PROP_FRAME_INTERLEAVE_ENABLE_BOOL': <OBPropertyID.OB_PROP_FRAME_INTERLEAVE_ENABLE_BOOL: 205>, 'OB_PROP_FRAME_INTERLEAVE_LASER_PATTERN_SYNC_DELAY_INT': <OBPropertyID.OB_PROP_FRAME_INTERLEAVE_LASER_PATTERN_SYNC_DELAY_INT: 206>, 'OB_PROP_ON_CHIP_CALIBRATION_HEALTH_CHECK_FLOAT': <OBPropertyID.OB_PROP_ON_CHIP_CALIBRATION_HEALTH_CHECK_FLOAT: 209>, 'OB_PROP_ON_CHIP_CALIBRATION_ENABLE_BOOL': <OBPropertyID.OB_PROP_ON_CHIP_CALIBRATION_ENABLE_BOOL: 210>, 'OB_PROP_HW_NOISE_REMOVE_FILTER_ENABLE_BOOL': <OBPropertyID.OB_PROP_HW_NOISE_REMOVE_FILTER_ENABLE_BOOL: 211>, 'OB_PROP_HW_NOISE_REMOVE_FILTER_THRESHOLD_FLOAT': <OBPropertyID.OB_PROP_HW_NOISE_REMOVE_FILTER_THRESHOLD_FLOAT: 212>, 'OB_STRUCT_BASELINE_CALIBRATION_PARAM': <OBPropertyID.OB_STRUCT_BASELINE_CALIBRATION_PARAM: 1002>, 'OB_STRUCT_DEVICE_TEMPERATURE': <OBPropertyID.OB_STRUCT_DEVICE_TEMPERATURE: 1003>, 'OB_STRUCT_TOF_EXPOSURE_THRESHOLD_CONTROL': <OBPropertyID.OB_STRUCT_TOF_EXPOSURE_THRESHOLD_CONTROL: 1024>, 'OB_STRUCT_DEVICE_SERIAL_NUMBER': <OBPropertyID.OB_STRUCT_DEVICE_SERIAL_NUMBER: 1035>, 'OB_STRUCT_DEVICE_TIME': <OBPropertyID.OB_STRUCT_DEVICE_TIME: 1037>, 'OB_STRUCT_MULTI_DEVICE_SYNC_CONFIG': <OBPropertyID.OB_STRUCT_MULTI_DEVICE_SYNC_CONFIG: 1038>, 'OB_STRUCT_RGB_CROP_ROI': <OBPropertyID.OB_STRUCT_RGB_CROP_ROI: 1040>, 'OB_STRUCT_DEVICE_IP_ADDR_CONFIG': <OBPropertyID.OB_STRUCT_DEVICE_IP_ADDR_CONFIG: 1041>, 'OB_STRUCT_DEVICE_IP_ADDR_CONFIG_V2': <OBPropertyID.OB_STRUCT_DEVICE_IP_ADDR_CONFIG_V2: 1088>, 'OB_STRUCT_CURRENT_DEPTH_ALG_MODE': <OBPropertyID.OB_STRUCT_CURRENT_DEPTH_ALG_MODE: 1043>, 'OB_STRUCT_DEPTH_PRECISION_SUPPORT_LIST': <OBPropertyID.OB_STRUCT_DEPTH_PRECISION_SUPPORT_LIST: 1045>, 'OB_STRUCT_DEVICE_STATIC_IP_CONFIG_RECORD': <OBPropertyID.OB_STRUCT_DEVICE_STATIC_IP_CONFIG_RECORD: 1053>, 'OB_STRUCT_DEPTH_HDR_CONFIG': <OBPropertyID.OB_STRUCT_DEPTH_HDR_CONFIG: 1059>, 'OB_STRUCT_COLOR_AE_ROI': <OBPropertyID.OB_STRUCT_COLOR_AE_ROI: 1060>, 'OB_STRUCT_DEPTH_AE_ROI': <OBPropertyID.OB_STRUCT_DEPTH_AE_ROI: 1061>, 'OB_STRUCT_ASIC_SERIAL_NUMBER': <OBPropertyID.OB_STRUCT_ASIC_SERIAL_NUMBER: 1063>, 'OB_STRUCT_DISP_OFFSET_CONFIG': <OBPropertyID.OB_STRUCT_DISP_OFFSET_CONFIG: 1064>, 'OB_STRUCT_PRESET_RESOLUTION_CONFIG': <OBPropertyID.OB_STRUCT_PRESET_RESOLUTION_CONFIG: 1069>, 'OB_STRUCT_COLOR_SYNCED_EXPOSURE_PARAM': <OBPropertyID.OB_STRUCT_COLOR_SYNCED_EXPOSURE_PARAM: 1077>, 'OB_PROP_COLOR_AUTO_EXPOSURE_BOOL': <OBPropertyID.OB_PROP_COLOR_AUTO_EXPOSURE_BOOL: 2000>, 'OB_PROP_COLOR_EXPOSURE_INT': <OBPropertyID.OB_PROP_COLOR_EXPOSURE_INT: 2001>, 'OB_PROP_COLOR_GAIN_INT': <OBPropertyID.OB_PROP_COLOR_GAIN_INT: 2002>, 'OB_PROP_COLOR_AUTO_WHITE_BALANCE_BOOL': <OBPropertyID.OB_PROP_COLOR_AUTO_WHITE_BALANCE_BOOL: 2003>, 'OB_PROP_COLOR_WHITE_BALANCE_INT': <OBPropertyID.OB_PROP_COLOR_WHITE_BALANCE_INT: 2004>, 'OB_PROP_COLOR_BRIGHTNESS_INT': <OBPropertyID.OB_PROP_COLOR_BRIGHTNESS_INT: 2005>, 'OB_PROP_COLOR_SHARPNESS_INT': <OBPropertyID.OB_PROP_COLOR_SHARPNESS_INT: 2006>, 'OB_PROP_COLOR_SHUTTER_INT': <OBPropertyID.OB_PROP_COLOR_SHUTTER_INT: 2007>, 'OB_PROP_COLOR_SATURATION_INT': <OBPropertyID.OB_PROP_COLOR_SATURATION_INT: 2008>, 'OB_PROP_COLOR_CONTRAST_INT': <OBPropertyID.OB_PROP_COLOR_CONTRAST_INT: 2009>, 'OB_PROP_COLOR_GAMMA_INT': <OBPropertyID.OB_PROP_COLOR_GAMMA_INT: 2010>, 'OB_PROP_COLOR_ROLL_INT': <OBPropertyID.OB_PROP_COLOR_ROLL_INT: 2011>, 'OB_PROP_COLOR_AUTO_EXPOSURE_PRIORITY_INT': <OBPropertyID.OB_PROP_COLOR_AUTO_EXPOSURE_PRIORITY_INT: 2012>, 'OB_PROP_COLOR_BACKLIGHT_COMPENSATION_INT': <OBPropertyID.OB_PROP_COLOR_BACKLIGHT_COMPENSATION_INT: 2013>, 'OB_PROP_COLOR_HUE_INT': <OBPropertyID.OB_PROP_COLOR_HUE_INT: 2014>, 'OB_PROP_COLOR_POWER_LINE_FREQUENCY_INT': <OBPropertyID.OB_PROP_COLOR_POWER_LINE_FREQUENCY_INT: 2015>, 'OB_PROP_COLOR_DENOISING_LEVEL_INT': <OBPropertyID.OB_PROP_COLOR_DENOISING_LEVEL_INT: 5525>, 'OB_PROP_DEVICE_OFFLINE_AFTER_IP_CONFIG_APPLY': <OBPropertyID.OB_PROP_DEVICE_OFFLINE_AFTER_IP_CONFIG_APPLY: 5555>, 'OB_PROP_DEPTH_AUTO_EXPOSURE_PRIORITY_INT': <OBPropertyID.OB_PROP_DEPTH_AUTO_EXPOSURE_PRIORITY_INT: 2052>, 'OB_PROP_DEPTH_AUTO_EXPOSURE_BOOL': <OBPropertyID.OB_PROP_DEPTH_AUTO_EXPOSURE_BOOL: 2016>, 'OB_PROP_DEPTH_EXPOSURE_INT': <OBPropertyID.OB_PROP_DEPTH_EXPOSURE_INT: 2017>, 'OB_PROP_DEPTH_GAIN_INT': <OBPropertyID.OB_PROP_DEPTH_GAIN_INT: 2018>, 'OB_PROP_IR_AUTO_EXPOSURE_BOOL': <OBPropertyID.OB_PROP_IR_AUTO_EXPOSURE_BOOL: 2025>, 'OB_PROP_IR_EXPOSURE_INT': <OBPropertyID.OB_PROP_IR_EXPOSURE_INT: 2026>, 'OB_PROP_IR_GAIN_INT': <OBPropertyID.OB_PROP_IR_GAIN_INT: 2027>, 'OB_PROP_IR_CHANNEL_DATA_SOURCE_INT': <OBPropertyID.OB_PROP_IR_CHANNEL_DATA_SOURCE_INT: 2028>, 'OB_PROP_DEPTH_RM_FILTER_BOOL': <OBPropertyID.OB_PROP_DEPTH_RM_FILTER_BOOL: 2029>, 'OB_PROP_COLOR_AE_MAX_GAIN_INT': <OBPropertyID.OB_PROP_COLOR_AE_MAX_GAIN_INT: 2030>, 'OB_PROP_COLOR_MAXIMAL_SHUTTER_INT': <OBPropertyID.OB_PROP_COLOR_MAXIMAL_SHUTTER_INT: 2031>, 'OB_PROP_IR_SHORT_EXPOSURE_BOOL': <OBPropertyID.OB_PROP_IR_SHORT_EXPOSURE_BOOL: 2032>, 'OB_PROP_COLOR_HDR_BOOL': <OBPropertyID.OB_PROP_COLOR_HDR_BOOL: 2034>, 'OB_PROP_IR_LONG_EXPOSURE_BOOL': <OBPropertyID.OB_PROP_IR_LONG_EXPOSURE_BOOL: 2035>, 'OB_PROP_SKIP_FRAME_BOOL': <OBPropertyID.OB_PROP_SKIP_FRAME_BOOL: 2036>, 'OB_PROP_HDR_MERGE_BOOL': <OBPropertyID.OB_PROP_HDR_MERGE_BOOL: 2037>, 'OB_PROP_COLOR_FOCUS_INT': <OBPropertyID.OB_PROP_COLOR_FOCUS_INT: 2038>, 'OB_PROP_IR_RECTIFY_BOOL': <OBPropertyID.OB_PROP_IR_RECTIFY_BOOL: 2040>, 'OB_PROP_SDK_DISPARITY_TO_DEPTH_BOOL': <OBPropertyID.OB_PROP_SDK_DISPARITY_TO_DEPTH_BOOL: 3004>, 'OB_PROP_SDK_DEPTH_FRAME_UNPACK_BOOL': <OBPropertyID.OB_PROP_SDK_DEPTH_FRAME_UNPACK_BOOL: 3007>, 'OB_PROP_SDK_IR_FRAME_UNPACK_BOOL': <OBPropertyID.OB_PROP_SDK_IR_FRAME_UNPACK_BOOL: 3008>, 'OB_PROP_SDK_ACCEL_FRAME_TRANSFORMED_BOOL': <OBPropertyID.OB_PROP_SDK_ACCEL_FRAME_TRANSFORMED_BOOL: 3009>, 'OB_PROP_SDK_GYRO_FRAME_TRANSFORMED_BOOL': <OBPropertyID.OB_PROP_SDK_GYRO_FRAME_TRANSFORMED_BOOL: 3010>, 'OB_PROP_SDK_IR_LEFT_FRAME_UNPACK_BOOL': <OBPropertyID.OB_PROP_SDK_IR_LEFT_FRAME_UNPACK_BOOL: 3011>, 'OB_PROP_SDK_IR_RIGHT_FRAME_UNPACK_BOOL': <OBPropertyID.OB_PROP_SDK_IR_RIGHT_FRAME_UNPACK_BOOL: 3012>, 'OB_PROP_DEPTH_INDUSTRY_MODE_INT': <OBPropertyID.OB_PROP_DEPTH_INDUSTRY_MODE_INT: 3024>, 'OB_PROP_NETWORK_BANDWIDTH_TYPE_INT': <OBPropertyID.OB_PROP_NETWORK_BANDWIDTH_TYPE_INT: 3027>, 'OB_PROP_DEVICE_PERFORMANCE_MODE_INT': <OBPropertyID.OB_PROP_DEVICE_PERFORMANCE_MODE_INT: 3028>, 'OB_RAW_DATA_CAMERA_CALIB_JSON_FILE': <OBPropertyID.OB_RAW_DATA_CAMERA_CALIB_JSON_FILE: 4029>, 'OB_PROP_LIDAR_TAIL_FILTER_LEVEL_INT': <OBPropertyID.OB_PROP_LIDAR_TAIL_FILTER_LEVEL_INT: 8006>, 'OB_RAW_DATA_LIDAR_IP_ADDRESS': <OBPropertyID.OB_RAW_DATA_LIDAR_IP_ADDRESS: 8000>, 'OB_PROP_LIDAR_PORT_INT': <OBPropertyID.OB_PROP_LIDAR_PORT_INT: 8001>, 'OB_RAW_DATA_LIDAR_MAC_ADDRESS': <OBPropertyID.OB_RAW_DATA_LIDAR_MAC_ADDRESS: 8002>, 'OB_RAW_DATA_LIDAR_SUBNET_MASK': <OBPropertyID.OB_RAW_DATA_LIDAR_SUBNET_MASK: 8003>, 'OB_PROP_LIDAR_WORK_MODE_INT': <OBPropertyID.OB_PROP_LIDAR_WORK_MODE_INT: 8004>, 'OB_PROP_LIDAR_APPLY_CONFIGS_INT': <OBPropertyID.OB_PROP_LIDAR_APPLY_CONFIGS_INT: 8005>, 'OB_PROP_LIDAR_MEMS_FOV_SIZE_FLOAT': <OBPropertyID.OB_PROP_LIDAR_MEMS_FOV_SIZE_FLOAT: 8007>, 'OB_PROP_LIDAR_MEMS_FRENQUENCY_FLOAT': <OBPropertyID.OB_PROP_LIDAR_MEMS_FRENQUENCY_FLOAT: 8008>, 'OB_RAW_DATA_LIDAR_PRODUCT_MODEL': <OBPropertyID.OB_RAW_DATA_LIDAR_PRODUCT_MODEL: 8009>, 'OB_RAW_DATA_LIDAR_FIRMWARE_VERSION': <OBPropertyID.OB_RAW_DATA_LIDAR_FIRMWARE_VERSION: 8010>, 'OB_RAW_DATA_LIDAR_FPGA_VERSION': <OBPropertyID.OB_RAW_DATA_LIDAR_FPGA_VERSION: 8011>, 'OB_PROP_LIDAR_WARNING_INFO_INT': <OBPropertyID.OB_PROP_LIDAR_WARNING_INFO_INT: 8012>, 'OB_PROP_LIDAR_MOTOR_SPIN_SPEED_INT': <OBPropertyID.OB_PROP_LIDAR_MOTOR_SPIN_SPEED_INT: 8013>, 'OB_PROP_LIDAR_MCU_TEMPERATURE_INT': <OBPropertyID.OB_PROP_LIDAR_MCU_TEMPERATURE_INT: 8014>, 'OB_PROP_LIDAR_APD_TEMPERATURE_INT': <OBPropertyID.OB_PROP_LIDAR_APD_TEMPERATURE_INT: 8015>, 'OB_PROP_LIDAR_SPECIFIC_MODE_INT': <OBPropertyID.OB_PROP_LIDAR_SPECIFIC_MODE_INT: 8016>, 'OB_PROP_LIDAR_REPETITIVE_SCAN_MODE_INT': <OBPropertyID.OB_PROP_LIDAR_REPETITIVE_SCAN_MODE_INT: 8017>, 'OB_PROP_DEPTH_NOISE_REMOVAL_FILTER_BOOL': <OBPropertyID.OB_PROP_DEPTH_SOFT_FILTER_BOOL: 24>, 'OB_DEVICE_AUTO_CAPTURE_ENABLE_BOOL': <OBPropertyID.OB_DEVICE_AUTO_CAPTURE_ENABLE_BOOL: 216>, 'OB_DEVICE_AUTO_CAPTURE_INTERVAL_TIME_INT': <OBPropertyID.OB_DEVICE_AUTO_CAPTURE_INTERVAL_TIME_INT: 217>, 'OB_DEVICE_PTP_CLOCK_SYNC_ENABLE_BOOL': <OBPropertyID.OB_DEVICE_PTP_CLOCK_SYNC_ENABLE_BOOL: 223>, 'OB_PROP_DEBUG_ESGM_CONFIDENCE_FLOAT': <OBPropertyID.OB_PROP_DEBUG_ESGM_CONFIDENCE_FLOAT: 5013>}
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class OBPropertyItem:
    def __init__(self) -> None: ...
    @property
    def id(self) -> OBPropertyID:
        """
        Property ID
        """

    @id.setter
    def id(self, arg0: OBPropertyID) -> None: ...
    @property
    def name(self) -> str:
        """
        Property name
        """

    @name.setter
    def name(self, arg0: str) -> None: ...
    @property
    def permission(self) -> OBPermissionType:
        """
        Property permission
        """

    @permission.setter
    def permission(self, arg0: OBPermissionType) -> None: ...
    @property
    def type(self) -> OBPropertyType:
        """
        Property type
        """

    @type.setter
    def type(self, arg0: OBPropertyType) -> None: ...

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
    __members__: typing.ClassVar[
        dict[str, OBPropertyType]
    ]  # value = {'OB_BOOL_PROPERTY': <OBPropertyType.OB_BOOL_PROPERTY: 0>, 'OB_INT_PROPERTY': <OBPropertyType.OB_INT_PROPERTY: 1>, 'OB_FLOAT_PROPERTY': <OBPropertyType.OB_FLOAT_PROPERTY: 2>, 'OB_STRUCT_PROPERTY': <OBPropertyType.OB_STRUCT_PROPERTY: 3>}
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class OBProtocolVersion:
    def __init__(self) -> None: ...
    @property
    def major(self) -> int: ...
    @major.setter
    def major(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def minor(self) -> int: ...
    @minor.setter
    def minor(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def patch(self) -> int: ...
    @patch.setter
    def patch(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...

class OBRect:
    def __init__(self) -> None: ...
    @property
    def height(self) -> int: ...
    @height.setter
    def height(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def width(self) -> int: ...
    @width.setter
    def width(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def x(self) -> int: ...
    @x.setter
    def x(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def y(self) -> int: ...
    @y.setter
    def y(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...

class OBRegionOfInterest:
    def __init__(self) -> None: ...
    @property
    def x0_left(self) -> int: ...
    @x0_left.setter
    def x0_left(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def x1_right(self) -> int: ...
    @x1_right.setter
    def x1_right(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def y0_top(self) -> int: ...
    @y0_top.setter
    def y0_top(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def y1_bottom(self) -> int: ...
    @y1_bottom.setter
    def y1_bottom(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...

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
    __members__: typing.ClassVar[
        dict[str, OBRotateDegreeType]
    ]  # value = {'ROTATE_0': <OBRotateDegreeType.ROTATE_0: 0>, 'ROTATE_90': <OBRotateDegreeType.ROTATE_90: 90>, 'ROTATE_180': <OBRotateDegreeType.ROTATE_180: 180>, 'ROTATE_270': <OBRotateDegreeType.ROTATE_270: 270>}
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

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

      RAW_PHASE_SENSOR

      CONFIDENCE_SENSOR

      LIDAR_SENSOR

      LEFT_COLOR_SENSOR

      RIGHT_COLOR_SENSOR

      TYPE_COUNT_SENSOR
    """

    ACCEL_SENSOR: typing.ClassVar[OBSensorType]  # value = <OBSensorType.ACCEL_SENSOR: 4>
    COLOR_SENSOR: typing.ClassVar[OBSensorType]  # value = <OBSensorType.COLOR_SENSOR: 2>
    CONFIDENCE_SENSOR: typing.ClassVar[OBSensorType]  # value = <OBSensorType.CONFIDENCE_SENSOR: 9>
    DEPTH_SENSOR: typing.ClassVar[OBSensorType]  # value = <OBSensorType.DEPTH_SENSOR: 3>
    GYRO_SENSOR: typing.ClassVar[OBSensorType]  # value = <OBSensorType.GYRO_SENSOR: 5>
    IR_SENSOR: typing.ClassVar[OBSensorType]  # value = <OBSensorType.IR_SENSOR: 1>
    LEFT_COLOR_SENSOR: typing.ClassVar[OBSensorType]  # value = <OBSensorType.LEFT_COLOR_SENSOR: 11>
    LEFT_IR_SENSOR: typing.ClassVar[OBSensorType]  # value = <OBSensorType.LEFT_IR_SENSOR: 6>
    LIDAR_SENSOR: typing.ClassVar[OBSensorType]  # value = <OBSensorType.LIDAR_SENSOR: 10>
    RAW_PHASE_SENSOR: typing.ClassVar[OBSensorType]  # value = <OBSensorType.RAW_PHASE_SENSOR: 8>
    RIGHT_COLOR_SENSOR: typing.ClassVar[OBSensorType]  # value = <OBSensorType.RIGHT_COLOR_SENSOR: 12>
    RIGHT_IR_SENSOR: typing.ClassVar[OBSensorType]  # value = <OBSensorType.RIGHT_IR_SENSOR: 7>
    TYPE_COUNT_SENSOR: typing.ClassVar[OBSensorType]  # value = <OBSensorType.TYPE_COUNT_SENSOR: 13>
    UNKNOWN_SENSOR: typing.ClassVar[OBSensorType]  # value = <OBSensorType.UNKNOWN_SENSOR: 0>
    __members__: typing.ClassVar[
        dict[str, OBSensorType]
    ]  # value = {'UNKNOWN_SENSOR': <OBSensorType.UNKNOWN_SENSOR: 0>, 'IR_SENSOR': <OBSensorType.IR_SENSOR: 1>, 'COLOR_SENSOR': <OBSensorType.COLOR_SENSOR: 2>, 'DEPTH_SENSOR': <OBSensorType.DEPTH_SENSOR: 3>, 'ACCEL_SENSOR': <OBSensorType.ACCEL_SENSOR: 4>, 'GYRO_SENSOR': <OBSensorType.GYRO_SENSOR: 5>, 'LEFT_IR_SENSOR': <OBSensorType.LEFT_IR_SENSOR: 6>, 'RIGHT_IR_SENSOR': <OBSensorType.RIGHT_IR_SENSOR: 7>, 'RAW_PHASE_SENSOR': <OBSensorType.RAW_PHASE_SENSOR: 8>, 'CONFIDENCE_SENSOR': <OBSensorType.CONFIDENCE_SENSOR: 9>, 'LIDAR_SENSOR': <OBSensorType.LIDAR_SENSOR: 10>, 'LEFT_COLOR_SENSOR': <OBSensorType.LEFT_COLOR_SENSOR: 11>, 'RIGHT_COLOR_SENSOR': <OBSensorType.RIGHT_COLOR_SENSOR: 12>, 'TYPE_COUNT_SENSOR': <OBSensorType.TYPE_COUNT_SENSOR: 13>}
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class OBSequenceIdItem:
    name: str
    def __init__(self) -> None: ...
    @property
    def sequence_select_id(self) -> int: ...
    @sequence_select_id.setter
    def sequence_select_id(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...

class OBSpatialAdvancedFilterParams:
    def __init__(self) -> None: ...
    def __repr__(self) -> str: ...
    @property
    def alpha(self) -> float: ...
    @alpha.setter
    def alpha(self, arg0: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def disp_diff(self) -> int: ...
    @disp_diff.setter
    def disp_diff(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def magnitude(self) -> int: ...
    @magnitude.setter
    def magnitude(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def radius(self) -> int: ...
    @radius.setter
    def radius(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...

class OBStatus:
    """
    Members:

      STATUS_OK

      STATUS_ERROR

      ERROR_UNKNOWN

      ERROR_INVALID_PARAMETER

      ERROR_INVALID_DATA

      ERROR_INVALID_DATA_LEN

      ERROR_BUFFER_TOO_SMALL

      ERROR_MEMORY

      ERROR_WAIT_TIMEOUT

      ERROR_NOT_IMPLEMENTED

      ERROR_UNSUPPORTED_OPERATION

      ERROR_WRONG_API_CALL_SEQUENCE

      ERROR_NO_DEVICE

      ERROR_DEVICE_CONNECT_FAILED

      ERROR_DEVICE_ACCESS_DENIED

      ERROR_DEVICE_DISCONNECTED

      ERROR_DEVICE_UNAVAILABLE

      ERROR_ITEM_NOT_FOUND

      ERROR_IO_FAILURE

      ERROR_RESOURCE_BUSY

      ERROR_FRAME_QUEUE_OVERFLOW

      ERROR_FRAME_DATA

      ERROR_FRAME_DATA_LEN

      ERROR_DEVICE_UNKNOWN

      ERROR_DEVICE_RESPONSE_BAD_MAGIC

      ERROR_DEVICE_RESPONSE_WRONG_ID

      ERROR_DEVICE_RESPONSE_WRONG_OPCODE

      ERROR_DEVICE_RESPONSE_WRONG_DATA_SIZE

      ERROR_DEVICE_RESPONSE_ERROR

      ERROR_DEVICE_RESPONSE_WARNING

      ERROR_DEVICE_RESPONSE_CHANNEL_FAILURE
    """

    ERROR_BUFFER_TOO_SMALL: typing.ClassVar[OBStatus]  # value = <OBStatus.ERROR_BUFFER_TOO_SMALL: 103>
    ERROR_DEVICE_ACCESS_DENIED: typing.ClassVar[OBStatus]  # value = <OBStatus.ERROR_DEVICE_ACCESS_DENIED: 111>
    ERROR_DEVICE_CONNECT_FAILED: typing.ClassVar[OBStatus]  # value = <OBStatus.ERROR_DEVICE_CONNECT_FAILED: 110>
    ERROR_DEVICE_DISCONNECTED: typing.ClassVar[OBStatus]  # value = <OBStatus.ERROR_DEVICE_DISCONNECTED: 112>
    ERROR_DEVICE_RESPONSE_BAD_MAGIC: typing.ClassVar[
        OBStatus
    ]  # value = <OBStatus.ERROR_DEVICE_RESPONSE_BAD_MAGIC: 1001>
    ERROR_DEVICE_RESPONSE_CHANNEL_FAILURE: typing.ClassVar[
        OBStatus
    ]  # value = <OBStatus.ERROR_DEVICE_RESPONSE_CHANNEL_FAILURE: 1007>
    ERROR_DEVICE_RESPONSE_ERROR: typing.ClassVar[OBStatus]  # value = <OBStatus.ERROR_DEVICE_RESPONSE_ERROR: 1005>
    ERROR_DEVICE_RESPONSE_WARNING: typing.ClassVar[OBStatus]  # value = <OBStatus.ERROR_DEVICE_RESPONSE_WARNING: 1006>
    ERROR_DEVICE_RESPONSE_WRONG_DATA_SIZE: typing.ClassVar[
        OBStatus
    ]  # value = <OBStatus.ERROR_DEVICE_RESPONSE_WRONG_DATA_SIZE: 1004>
    ERROR_DEVICE_RESPONSE_WRONG_ID: typing.ClassVar[OBStatus]  # value = <OBStatus.ERROR_DEVICE_RESPONSE_WRONG_ID: 1002>
    ERROR_DEVICE_RESPONSE_WRONG_OPCODE: typing.ClassVar[
        OBStatus
    ]  # value = <OBStatus.ERROR_DEVICE_RESPONSE_WRONG_OPCODE: 1003>
    ERROR_DEVICE_UNAVAILABLE: typing.ClassVar[OBStatus]  # value = <OBStatus.ERROR_DEVICE_UNAVAILABLE: 113>
    ERROR_DEVICE_UNKNOWN: typing.ClassVar[OBStatus]  # value = <OBStatus.ERROR_DEVICE_UNKNOWN: 1000>
    ERROR_FRAME_DATA: typing.ClassVar[OBStatus]  # value = <OBStatus.ERROR_FRAME_DATA: 201>
    ERROR_FRAME_DATA_LEN: typing.ClassVar[OBStatus]  # value = <OBStatus.ERROR_FRAME_DATA_LEN: 202>
    ERROR_FRAME_QUEUE_OVERFLOW: typing.ClassVar[OBStatus]  # value = <OBStatus.ERROR_FRAME_QUEUE_OVERFLOW: 200>
    ERROR_INVALID_DATA: typing.ClassVar[OBStatus]  # value = <OBStatus.ERROR_INVALID_DATA: 101>
    ERROR_INVALID_DATA_LEN: typing.ClassVar[OBStatus]  # value = <OBStatus.ERROR_INVALID_DATA_LEN: 102>
    ERROR_INVALID_PARAMETER: typing.ClassVar[OBStatus]  # value = <OBStatus.ERROR_INVALID_PARAMETER: 100>
    ERROR_IO_FAILURE: typing.ClassVar[OBStatus]  # value = <OBStatus.ERROR_IO_FAILURE: 115>
    ERROR_ITEM_NOT_FOUND: typing.ClassVar[OBStatus]  # value = <OBStatus.ERROR_ITEM_NOT_FOUND: 114>
    ERROR_MEMORY: typing.ClassVar[OBStatus]  # value = <OBStatus.ERROR_MEMORY: 104>
    ERROR_NOT_IMPLEMENTED: typing.ClassVar[OBStatus]  # value = <OBStatus.ERROR_NOT_IMPLEMENTED: 106>
    ERROR_NO_DEVICE: typing.ClassVar[OBStatus]  # value = <OBStatus.ERROR_NO_DEVICE: 109>
    ERROR_RESOURCE_BUSY: typing.ClassVar[OBStatus]  # value = <OBStatus.ERROR_RESOURCE_BUSY: 116>
    ERROR_UNKNOWN: typing.ClassVar[OBStatus]  # value = <OBStatus.STATUS_ERROR: 1>
    ERROR_UNSUPPORTED_OPERATION: typing.ClassVar[OBStatus]  # value = <OBStatus.ERROR_UNSUPPORTED_OPERATION: 107>
    ERROR_WAIT_TIMEOUT: typing.ClassVar[OBStatus]  # value = <OBStatus.ERROR_WAIT_TIMEOUT: 105>
    ERROR_WRONG_API_CALL_SEQUENCE: typing.ClassVar[OBStatus]  # value = <OBStatus.ERROR_WRONG_API_CALL_SEQUENCE: 108>
    STATUS_ERROR: typing.ClassVar[OBStatus]  # value = <OBStatus.STATUS_ERROR: 1>
    STATUS_OK: typing.ClassVar[OBStatus]  # value = <OBStatus.STATUS_OK: 0>
    __members__: typing.ClassVar[
        dict[str, OBStatus]
    ]  # value = {'STATUS_OK': <OBStatus.STATUS_OK: 0>, 'STATUS_ERROR': <OBStatus.STATUS_ERROR: 1>, 'ERROR_UNKNOWN': <OBStatus.STATUS_ERROR: 1>, 'ERROR_INVALID_PARAMETER': <OBStatus.ERROR_INVALID_PARAMETER: 100>, 'ERROR_INVALID_DATA': <OBStatus.ERROR_INVALID_DATA: 101>, 'ERROR_INVALID_DATA_LEN': <OBStatus.ERROR_INVALID_DATA_LEN: 102>, 'ERROR_BUFFER_TOO_SMALL': <OBStatus.ERROR_BUFFER_TOO_SMALL: 103>, 'ERROR_MEMORY': <OBStatus.ERROR_MEMORY: 104>, 'ERROR_WAIT_TIMEOUT': <OBStatus.ERROR_WAIT_TIMEOUT: 105>, 'ERROR_NOT_IMPLEMENTED': <OBStatus.ERROR_NOT_IMPLEMENTED: 106>, 'ERROR_UNSUPPORTED_OPERATION': <OBStatus.ERROR_UNSUPPORTED_OPERATION: 107>, 'ERROR_WRONG_API_CALL_SEQUENCE': <OBStatus.ERROR_WRONG_API_CALL_SEQUENCE: 108>, 'ERROR_NO_DEVICE': <OBStatus.ERROR_NO_DEVICE: 109>, 'ERROR_DEVICE_CONNECT_FAILED': <OBStatus.ERROR_DEVICE_CONNECT_FAILED: 110>, 'ERROR_DEVICE_ACCESS_DENIED': <OBStatus.ERROR_DEVICE_ACCESS_DENIED: 111>, 'ERROR_DEVICE_DISCONNECTED': <OBStatus.ERROR_DEVICE_DISCONNECTED: 112>, 'ERROR_DEVICE_UNAVAILABLE': <OBStatus.ERROR_DEVICE_UNAVAILABLE: 113>, 'ERROR_ITEM_NOT_FOUND': <OBStatus.ERROR_ITEM_NOT_FOUND: 114>, 'ERROR_IO_FAILURE': <OBStatus.ERROR_IO_FAILURE: 115>, 'ERROR_RESOURCE_BUSY': <OBStatus.ERROR_RESOURCE_BUSY: 116>, 'ERROR_FRAME_QUEUE_OVERFLOW': <OBStatus.ERROR_FRAME_QUEUE_OVERFLOW: 200>, 'ERROR_FRAME_DATA': <OBStatus.ERROR_FRAME_DATA: 201>, 'ERROR_FRAME_DATA_LEN': <OBStatus.ERROR_FRAME_DATA_LEN: 202>, 'ERROR_DEVICE_UNKNOWN': <OBStatus.ERROR_DEVICE_UNKNOWN: 1000>, 'ERROR_DEVICE_RESPONSE_BAD_MAGIC': <OBStatus.ERROR_DEVICE_RESPONSE_BAD_MAGIC: 1001>, 'ERROR_DEVICE_RESPONSE_WRONG_ID': <OBStatus.ERROR_DEVICE_RESPONSE_WRONG_ID: 1002>, 'ERROR_DEVICE_RESPONSE_WRONG_OPCODE': <OBStatus.ERROR_DEVICE_RESPONSE_WRONG_OPCODE: 1003>, 'ERROR_DEVICE_RESPONSE_WRONG_DATA_SIZE': <OBStatus.ERROR_DEVICE_RESPONSE_WRONG_DATA_SIZE: 1004>, 'ERROR_DEVICE_RESPONSE_ERROR': <OBStatus.ERROR_DEVICE_RESPONSE_ERROR: 1005>, 'ERROR_DEVICE_RESPONSE_WARNING': <OBStatus.ERROR_DEVICE_RESPONSE_WARNING: 1006>, 'ERROR_DEVICE_RESPONSE_CHANNEL_FAILURE': <OBStatus.ERROR_DEVICE_RESPONSE_CHANNEL_FAILURE: 1007>}
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

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

      RAW_PHASE_STREAM

      CONFIDENCE_STREAM

      LIDAR_STREAM

      LEFT_COLOR_STREAM

      RIGHT_COLOR_STREAM

      TYPE_COUNT_STREAM
    """

    ACCEL_STREAM: typing.ClassVar[OBStreamType]  # value = <OBStreamType.ACCEL_STREAM: 4>
    COLOR_STREAM: typing.ClassVar[OBStreamType]  # value = <OBStreamType.COLOR_STREAM: 2>
    CONFIDENCE_STREAM: typing.ClassVar[OBStreamType]  # value = <OBStreamType.CONFIDENCE_STREAM: 9>
    DEPTH_STREAM: typing.ClassVar[OBStreamType]  # value = <OBStreamType.DEPTH_STREAM: 3>
    GYRO_STREAM: typing.ClassVar[OBStreamType]  # value = <OBStreamType.GYRO_STREAM: 5>
    IR_STREAM: typing.ClassVar[OBStreamType]  # value = <OBStreamType.IR_STREAM: 1>
    LEFT_COLOR_STREAM: typing.ClassVar[OBStreamType]  # value = <OBStreamType.LEFT_COLOR_STREAM: 11>
    LEFT_IR_STREAM: typing.ClassVar[OBStreamType]  # value = <OBStreamType.LEFT_IR_STREAM: 6>
    LIDAR_STREAM: typing.ClassVar[OBStreamType]  # value = <OBStreamType.LIDAR_STREAM: 10>
    RAW_PHASE_STREAM: typing.ClassVar[OBStreamType]  # value = <OBStreamType.RAW_PHASE_STREAM: 8>
    RIGHT_COLOR_STREAM: typing.ClassVar[OBStreamType]  # value = <OBStreamType.RIGHT_COLOR_STREAM: 12>
    RIGHT_IR_STREAM: typing.ClassVar[OBStreamType]  # value = <OBStreamType.RIGHT_IR_STREAM: 7>
    TYPE_COUNT_STREAM: typing.ClassVar[OBStreamType]  # value = <OBStreamType.TYPE_COUNT_STREAM: 13>
    UNKNOWN_STREAM: typing.ClassVar[OBStreamType]  # value = <OBStreamType.UNKNOWN_STREAM: -1>
    VIDEO_STREAM: typing.ClassVar[OBStreamType]  # value = <OBStreamType.VIDEO_STREAM: 0>
    __members__: typing.ClassVar[
        dict[str, OBStreamType]
    ]  # value = {'UNKNOWN_STREAM': <OBStreamType.UNKNOWN_STREAM: -1>, 'VIDEO_STREAM': <OBStreamType.VIDEO_STREAM: 0>, 'IR_STREAM': <OBStreamType.IR_STREAM: 1>, 'COLOR_STREAM': <OBStreamType.COLOR_STREAM: 2>, 'DEPTH_STREAM': <OBStreamType.DEPTH_STREAM: 3>, 'ACCEL_STREAM': <OBStreamType.ACCEL_STREAM: 4>, 'GYRO_STREAM': <OBStreamType.GYRO_STREAM: 5>, 'LEFT_IR_STREAM': <OBStreamType.LEFT_IR_STREAM: 6>, 'RIGHT_IR_STREAM': <OBStreamType.RIGHT_IR_STREAM: 7>, 'RAW_PHASE_STREAM': <OBStreamType.RAW_PHASE_STREAM: 8>, 'CONFIDENCE_STREAM': <OBStreamType.CONFIDENCE_STREAM: 9>, 'LIDAR_STREAM': <OBStreamType.LIDAR_STREAM: 10>, 'LEFT_COLOR_STREAM': <OBStreamType.LEFT_COLOR_STREAM: 11>, 'RIGHT_COLOR_STREAM': <OBStreamType.RIGHT_COLOR_STREAM: 12>, 'TYPE_COUNT_STREAM': <OBStreamType.TYPE_COUNT_STREAM: 13>}
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

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

      IR_IMU_SYNC

      UNKNOWN
    """

    CLOSE: typing.ClassVar[OBSyncMode]  # value = <OBSyncMode.CLOSE: 0>
    IR_IMU_SYNC: typing.ClassVar[OBSyncMode]  # value = <OBSyncMode.IR_IMU_SYNC: 8>
    PRIMARY: typing.ClassVar[OBSyncMode]  # value = <OBSyncMode.PRIMARY: 2>
    PRIMARY_IR_TRIGGER: typing.ClassVar[OBSyncMode]  # value = <OBSyncMode.PRIMARY_IR_TRIGGER: 5>
    PRIMARY_MCU_TRIGGER: typing.ClassVar[OBSyncMode]  # value = <OBSyncMode.PRIMARY_MCU_TRIGGER: 4>
    PRIMARY_SOFT_TRIGGER: typing.ClassVar[OBSyncMode]  # value = <OBSyncMode.PRIMARY_SOFT_TRIGGER: 6>
    SECONDARY: typing.ClassVar[OBSyncMode]  # value = <OBSyncMode.SECONDARY: 3>
    SECONDARY_SOFT_TRIGGER: typing.ClassVar[OBSyncMode]  # value = <OBSyncMode.SECONDARY_SOFT_TRIGGER: 7>
    STANDALONE: typing.ClassVar[OBSyncMode]  # value = <OBSyncMode.STANDALONE: 1>
    UNKNOWN: typing.ClassVar[OBSyncMode]  # value = <OBSyncMode.UNKNOWN: 255>
    __members__: typing.ClassVar[
        dict[str, OBSyncMode]
    ]  # value = {'CLOSE': <OBSyncMode.CLOSE: 0>, 'STANDALONE': <OBSyncMode.STANDALONE: 1>, 'PRIMARY': <OBSyncMode.PRIMARY: 2>, 'SECONDARY': <OBSyncMode.SECONDARY: 3>, 'PRIMARY_MCU_TRIGGER': <OBSyncMode.PRIMARY_MCU_TRIGGER: 4>, 'PRIMARY_IR_TRIGGER': <OBSyncMode.PRIMARY_IR_TRIGGER: 5>, 'PRIMARY_SOFT_TRIGGER': <OBSyncMode.PRIMARY_SOFT_TRIGGER: 6>, 'SECONDARY_SOFT_TRIGGER': <OBSyncMode.SECONDARY_SOFT_TRIGGER: 7>, 'IR_IMU_SYNC': <OBSyncMode.IR_IMU_SYNC: 8>, 'UNKNOWN': <OBSyncMode.UNKNOWN: 255>}
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class OBTofExposureThresholdControl:
    def __init__(self) -> None: ...
    @property
    def lower(self) -> int: ...
    @lower.setter
    def lower(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def upper(self) -> int: ...
    @upper.setter
    def upper(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...

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
    __members__: typing.ClassVar[
        dict[str, OBTofFilterRange]
    ]  # value = {'CLOSE': <OBTofFilterRange.CLOSE: 0>, 'MIDDLE': <OBTofFilterRange.MIDDLE: 1>, 'FAR': <OBTofFilterRange.FAR: 2>, 'DEBUG': <OBTofFilterRange.DEBUG: 100>}
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

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
    __members__: typing.ClassVar[
        dict[str, OBUSBPowerState]
    ]  # value = {'OFF': <OBUSBPowerState.OFF: 0>, 'POWER_5V_0A9': <OBUSBPowerState.POWER_5V_0A9: 1>, 'POWER_5V_1A5': <OBUSBPowerState.POWER_5V_1A5: 2>, 'POWER_5V_3A0': <OBUSBPowerState.POWER_5V_3A0: 3>}
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class OBUint16PropertyRange:
    def __init__(self) -> None: ...
    @property
    def current(self) -> int: ...
    @current.setter
    def current(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def default_value(self) -> int: ...
    @default_value.setter
    def default_value(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def max(self) -> int: ...
    @max.setter
    def max(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def min(self) -> int: ...
    @min.setter
    def min(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def step(self) -> int: ...
    @step.setter
    def step(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...

class OBUint8PropertyRange:
    def __init__(self) -> None: ...
    @property
    def current(self) -> int: ...
    @current.setter
    def current(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def default_value(self) -> int: ...
    @default_value.setter
    def default_value(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def max(self) -> int: ...
    @max.setter
    def max(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def min(self) -> int: ...
    @min.setter
    def min(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def step(self) -> int: ...
    @step.setter
    def step(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...

class OBUpgradeState:
    """
    Members:

      DONE_REBOOT_AND_REUPDATE

      DONE_WITH_DUPLICATES

      VERIFY_SUCCESS

      FILE_TRANSFER

      DONE

      IN_PROGRESS

      START

      VERIFY_IMAGE

      ERR_VERIFY

      ERR_PROGRAM

      ERR_ERASE

      ERR_FLASH_TYPE

      ERR_IMAGE_SIZE

      ERR_OTHER

      ERR_DDR

      ERR_TIMEOUT

      ERR_MISMATCH

      ERR_UNSUPPORT_DEV

      ERR_INVALID_COUNT

      ERR_FILE_READ

      ERR_TRANSFER
    """

    DONE: typing.ClassVar[OBUpgradeState]  # value = <OBUpgradeState.DONE: 3>
    DONE_REBOOT_AND_REUPDATE: typing.ClassVar[OBUpgradeState]  # value = <OBUpgradeState.DONE_REBOOT_AND_REUPDATE: 7>
    DONE_WITH_DUPLICATES: typing.ClassVar[OBUpgradeState]  # value = <OBUpgradeState.DONE_WITH_DUPLICATES: 6>
    ERR_DDR: typing.ClassVar[OBUpgradeState]  # value = <OBUpgradeState.ERR_DDR: -7>
    ERR_ERASE: typing.ClassVar[OBUpgradeState]  # value = <OBUpgradeState.ERR_ERASE: -3>
    ERR_FILE_READ: typing.ClassVar[OBUpgradeState]  # value = <OBUpgradeState.ERR_FILE_READ: -12>
    ERR_FLASH_TYPE: typing.ClassVar[OBUpgradeState]  # value = <OBUpgradeState.ERR_FLASH_TYPE: -4>
    ERR_IMAGE_SIZE: typing.ClassVar[OBUpgradeState]  # value = <OBUpgradeState.ERR_IMAGE_SIZE: -5>
    ERR_INVALID_COUNT: typing.ClassVar[OBUpgradeState]  # value = <OBUpgradeState.ERR_INVALID_COUNT: -11>
    ERR_MISMATCH: typing.ClassVar[OBUpgradeState]  # value = <OBUpgradeState.ERR_MISMATCH: -9>
    ERR_OTHER: typing.ClassVar[OBUpgradeState]  # value = <OBUpgradeState.ERR_OTHER: -6>
    ERR_PROGRAM: typing.ClassVar[OBUpgradeState]  # value = <OBUpgradeState.ERR_PROGRAM: -2>
    ERR_TIMEOUT: typing.ClassVar[OBUpgradeState]  # value = <OBUpgradeState.ERR_TIMEOUT: -8>
    ERR_TRANSFER: typing.ClassVar[OBUpgradeState]  # value = <OBUpgradeState.ERR_TRANSFER: -13>
    ERR_UNSUPPORT_DEV: typing.ClassVar[OBUpgradeState]  # value = <OBUpgradeState.ERR_UNSUPPORT_DEV: -10>
    ERR_VERIFY: typing.ClassVar[OBUpgradeState]  # value = <OBUpgradeState.ERR_VERIFY: -1>
    FILE_TRANSFER: typing.ClassVar[OBUpgradeState]  # value = <OBUpgradeState.FILE_TRANSFER: 4>
    IN_PROGRESS: typing.ClassVar[OBUpgradeState]  # value = <OBUpgradeState.IN_PROGRESS: 2>
    START: typing.ClassVar[OBUpgradeState]  # value = <OBUpgradeState.START: 1>
    VERIFY_IMAGE: typing.ClassVar[OBUpgradeState]  # value = <OBUpgradeState.VERIFY_IMAGE: 0>
    VERIFY_SUCCESS: typing.ClassVar[OBUpgradeState]  # value = <OBUpgradeState.VERIFY_SUCCESS: 5>
    __members__: typing.ClassVar[
        dict[str, OBUpgradeState]
    ]  # value = {'DONE_REBOOT_AND_REUPDATE': <OBUpgradeState.DONE_REBOOT_AND_REUPDATE: 7>, 'DONE_WITH_DUPLICATES': <OBUpgradeState.DONE_WITH_DUPLICATES: 6>, 'VERIFY_SUCCESS': <OBUpgradeState.VERIFY_SUCCESS: 5>, 'FILE_TRANSFER': <OBUpgradeState.FILE_TRANSFER: 4>, 'DONE': <OBUpgradeState.DONE: 3>, 'IN_PROGRESS': <OBUpgradeState.IN_PROGRESS: 2>, 'START': <OBUpgradeState.START: 1>, 'VERIFY_IMAGE': <OBUpgradeState.VERIFY_IMAGE: 0>, 'ERR_VERIFY': <OBUpgradeState.ERR_VERIFY: -1>, 'ERR_PROGRAM': <OBUpgradeState.ERR_PROGRAM: -2>, 'ERR_ERASE': <OBUpgradeState.ERR_ERASE: -3>, 'ERR_FLASH_TYPE': <OBUpgradeState.ERR_FLASH_TYPE: -4>, 'ERR_IMAGE_SIZE': <OBUpgradeState.ERR_IMAGE_SIZE: -5>, 'ERR_OTHER': <OBUpgradeState.ERR_OTHER: -6>, 'ERR_DDR': <OBUpgradeState.ERR_DDR: -7>, 'ERR_TIMEOUT': <OBUpgradeState.ERR_TIMEOUT: -8>, 'ERR_MISMATCH': <OBUpgradeState.ERR_MISMATCH: -9>, 'ERR_UNSUPPORT_DEV': <OBUpgradeState.ERR_UNSUPPORT_DEV: -10>, 'ERR_INVALID_COUNT': <OBUpgradeState.ERR_INVALID_COUNT: -11>, 'ERR_FILE_READ': <OBUpgradeState.ERR_FILE_READ: -12>, 'ERR_TRANSFER': <OBUpgradeState.ERR_TRANSFER: -13>}
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class Pipeline:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, arg0: Device) -> None: ...
    def disable_frame_sync(self) -> None: ...
    def disable_health_monitor(self) -> None:
        """
        Disable pipeline health monitor
        """

    def enable_frame_sync(self) -> None: ...
    def enable_health_monitor(
        self, callback: collections.abc.Callable, interval_ms: typing.SupportsInt | typing.SupportsIndex = 3000
    ) -> None:
        """
        Enable pipeline health monitor with periodic status polling
        """

    def get_camera_param(self) -> OBCameraParam: ...
    def get_config(self) -> Config: ...
    def get_d2c_depth_profile_list(self, arg0: StreamProfile, arg1: OBAlignMode) -> StreamProfileList: ...
    def get_device(self) -> Device: ...
    def get_status(self) -> OBPipelineStatus:
        """
        Get the current pipeline status observed during streaming
        """

    def get_stream_profile_list(self, arg0: OBSensorType) -> StreamProfileList: ...
    @typing.overload
    def start(self, arg0: Config) -> None: ...
    @typing.overload
    def start(self, arg0: Config, arg1: collections.abc.Callable) -> None: ...
    @typing.overload
    def start(self) -> None: ...
    def stop(self) -> None: ...
    def wait_for_frames(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> FrameSet: ...

class PlaybackDevice(Device):
    def __init__(self, file: str) -> None: ...
    def get_duration(self) -> int: ...
    def get_playback_status(self) -> OBPlaybackStatus: ...
    def get_position(self) -> int: ...
    def pause(self) -> None: ...
    def resume(self) -> None: ...
    def seek(self, timestamp: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def set_playback_rate(self, rate: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    def set_playback_status_change_callback(self, arg0: collections.abc.Callable) -> None: ...

class PointCloudFilter(Filter):
    def __init__(self) -> None: ...
    def calculate(self, arg0: Frame) -> numpy.typing.NDArray[numpy.float32]: ...
    def get_decimation_factor_range(self) -> OBIntPropertyRange: ...
    def set_camera_param(self, arg0: OBCameraParam) -> None: ...
    def set_color_data_normalization(self, arg0: bool) -> None: ...
    def set_create_point_format(self, arg0: OBFormat) -> None: ...
    def set_decimation_factor(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def set_frame_align_state(self, arg0: bool) -> None: ...
    def set_position_data_scaled(self, arg0: typing.SupportsFloat | typing.SupportsIndex) -> None: ...

class PointsFrame(Frame):
    def get_height(self) -> int: ...
    def get_position_value_scale(self) -> float: ...
    def get_width(self) -> int: ...

class PresetResolutionConfigList:
    def get_count(self) -> int:
        """
        Get the number of device preset resolution ratio in the list
        """

    def get_preset_resolution_ratio_config(
        self, arg0: typing.SupportsInt | typing.SupportsIndex
    ) -> OBPresetResolutionConfig:
        """
        Get the device preset resolution ratio at the specified index
        """

class RecordDevice:
    def __init__(self, device: Device, file: str, compression: bool = True) -> None: ...
    def pause(self) -> None: ...
    def resume(self) -> None: ...

class Sensor:
    def __repr__(self) -> str: ...
    def get_recommended_filters(self) -> list[Filter]: ...
    def get_stream_profile_list(self) -> StreamProfileList: ...
    def get_type(self) -> OBSensorType: ...
    def start(self, arg0: StreamProfile, arg1: collections.abc.Callable) -> None: ...
    def stop(self) -> None: ...
    def switch_profile(self, arg0: StreamProfile) -> None: ...

class SensorList:
    def __getitem__(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> Sensor: ...
    def __len__(self) -> int: ...
    def get_count(self) -> int: ...
    def get_sensor_by_index(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> Sensor: ...
    def get_sensor_by_type(self, arg0: OBSensorType) -> Sensor: ...
    def get_type_by_index(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> OBSensorType: ...

class SequenceIdFilter(Filter):
    def __init__(self) -> None: ...
    def get_select_sequence_id(self) -> int: ...
    def get_sequence_id_list(self) -> list: ...
    def get_sequence_id_list_size(self) -> int: ...
    def select_sequence_id(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...

class SpatialAdvancedFilter(Filter):
    def __init__(self) -> None: ...
    def get_alpha_range(self) -> OBFloatPropertyRange:
        """
        get alpha range
        """

    def get_disp_diff_range(self) -> OBUint16PropertyRange: ...
    def get_filter_params(self) -> OBSpatialAdvancedFilterParams: ...
    def get_magnitude_range(self) -> OBIntPropertyRange: ...
    def get_radius_range(self) -> OBUint16PropertyRange: ...
    def set_filter_params(self, arg0: OBSpatialAdvancedFilterParams) -> None: ...

class StreamProfile:
    def as_accel_stream_profile(self) -> AccelStreamProfile: ...
    def as_gyro_stream_profile(self) -> GyroStreamProfile: ...
    def as_lidar_stream_profile(self) -> LiDARStreamProfile: ...
    def as_video_stream_profile(self) -> VideoStreamProfile: ...
    @typing.overload
    def bind_extrinsic_to(self, arg0: StreamProfile, arg1: OBExtrinsic) -> None: ...
    @typing.overload
    def bind_extrinsic_to(self, arg0: OBStreamType, arg1: OBExtrinsic) -> None: ...
    def get_extrinsic_to(self, arg0: StreamProfile) -> OBExtrinsic: ...
    def get_format(self) -> OBFormat: ...
    def get_type(self) -> OBStreamType: ...
    def is_accel_stream_profile(self) -> bool: ...
    def is_gyro_stream_profile(self) -> bool: ...
    def is_video_stream_profile(self) -> bool: ...

class StreamProfileList:
    def __getitem__(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> StreamProfile: ...
    def __len__(self) -> int: ...
    def get_accel_stream_profile(self, arg0: OBAccelFullScaleRange, arg1: OBGyroSampleRate) -> AccelStreamProfile: ...
    def get_count(self) -> int: ...
    def get_default_video_stream_profile(self) -> VideoStreamProfile: ...
    def get_gyro_stream_profile(self, arg0: OBGyroFullScaleRange, arg1: OBGyroSampleRate) -> GyroStreamProfile: ...
    def get_lidar_stream_profile(self, arg0: OBLiDARScanRate, arg1: OBFormat) -> LiDARStreamProfile: ...
    def get_stream_profile_by_index(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> StreamProfile: ...
    @typing.overload
    def get_video_stream_profile(
        self,
        width: typing.SupportsInt | typing.SupportsIndex = 0,
        height: typing.SupportsInt | typing.SupportsIndex = 0,
        format: OBFormat = OBFormat.UNKNOWN_FORMAT,
        fps: typing.SupportsInt | typing.SupportsIndex = 0,
    ) -> VideoStreamProfile: ...
    @typing.overload
    def get_video_stream_profile(
        self,
        decimation_config: OBHardwareDecimationConfig,
        format: OBFormat = OBFormat.UNKNOWN_FORMAT,
        fps: typing.SupportsInt | typing.SupportsIndex = 0,
    ) -> VideoStreamProfile: ...

class TemporalFilter(Filter):
    def __init__(self) -> None: ...
    def get_diff_scale_range(self) -> OBFloatPropertyRange:
        """
        get diff scale range
        """

    def get_weight_range(self) -> OBFloatPropertyRange:
        """
        get weight range
        """

    def set_diff_scale(self, arg0: typing.SupportsFloat | typing.SupportsIndex) -> None:
        """
        set diff scale
        """

    def set_weight(self, arg0: typing.SupportsFloat | typing.SupportsIndex) -> None: ...

class ThresholdFilter(Filter):
    def __init__(self) -> None: ...
    def get_max_range(self) -> OBIntPropertyRange: ...
    def get_min_range(self) -> OBIntPropertyRange: ...
    def set_value_range(
        self, arg0: typing.SupportsInt | typing.SupportsIndex, arg1: typing.SupportsInt | typing.SupportsIndex
    ) -> bool: ...

class VideoFrame(Frame):
    def __repr__(self) -> str: ...
    def as_color_frame(self) -> ColorFrame: ...
    def as_confidence_frame(self) -> ConfidenceFrame: ...
    def as_depth_frame(self) -> DepthFrame: ...
    def as_ir_frame(self) -> IRFrame: ...
    def as_points_frame(self) -> PointsFrame: ...
    def get_height(self) -> int: ...
    def get_metadata(self) -> numpy.typing.NDArray[numpy.uint8]: ...
    def get_metadata_size(self) -> int: ...
    def get_pixel_available_bit_size(self) -> int: ...
    def get_pixel_type(self) -> OBPixelType: ...
    def get_width(self) -> int: ...
    def set_pixel_available_bit_size(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def set_pixel_type(self, arg0: OBPixelType) -> None: ...

class VideoStreamProfile(StreamProfile):
    def __repr__(self) -> str: ...
    def get_decimation_config(self) -> OBHardwareDecimationConfig: ...
    def get_distortion(self) -> OBCameraDistortion: ...
    def get_fps(self) -> int: ...
    def get_height(self) -> int: ...
    def get_intrinsic(self) -> OBCameraIntrinsic: ...
    def get_width(self) -> int: ...

def get_version() -> str: ...
def save_lidar_point_cloud_to_ply(arg0: str, arg1: LiDARPointsFrame, arg2: bool) -> None: ...
def save_point_cloud_to_ply(
    file_name: str,
    frame: Frame,
    save_binary: bool = False,
    use_mesh: bool = False,
    mesh_threshold: typing.SupportsFloat | typing.SupportsIndex = 50.0,
) -> None: ...
def transformation2dto2d(
    arg0: OBPoint2f,
    arg1: typing.SupportsFloat | typing.SupportsIndex,
    arg2: OBCameraIntrinsic,
    arg3: OBCameraDistortion,
    arg4: OBCameraIntrinsic,
    arg5: OBCameraDistortion,
    arg6: OBExtrinsic,
) -> OBPoint2f: ...
def transformation2dto3d(
    arg0: OBPoint2f, arg1: typing.SupportsFloat | typing.SupportsIndex, arg2: OBCameraIntrinsic, arg3: OBExtrinsic
) -> OBPoint3f: ...
def transformation3dto2d(
    arg0: OBPoint3f, arg1: OBCameraIntrinsic, arg2: OBCameraDistortion, arg3: OBExtrinsic
) -> OBPoint2f: ...
def transformation3dto3d(arg0: OBPoint3f, arg1: OBExtrinsic) -> OBPoint3f: ...

COUNT: OBPlaybackStatus  # value = <OBPlaybackStatus.COUNT: 4>
PAUSED: OBPlaybackStatus  # value = <OBPlaybackStatus.PAUSED: 2>
PLAYING: OBPlaybackStatus  # value = <OBPlaybackStatus.PLAYING: 1>
SAMPLE_RATE_100_HZ: OBGyroSampleRate  # value = <OBGyroSampleRate.SAMPLE_RATE_100_HZ: 7>
SAMPLE_RATE_12_5_HZ: OBGyroSampleRate  # value = <OBGyroSampleRate.SAMPLE_RATE_12_5_HZ: 4>
SAMPLE_RATE_16_KHZ: OBGyroSampleRate  # value = <OBGyroSampleRate.SAMPLE_RATE_16_KHZ: 14>
SAMPLE_RATE_1_5625_HZ: OBGyroSampleRate  # value = <OBGyroSampleRate.SAMPLE_RATE_1_5625_HZ: 1>
SAMPLE_RATE_1_KHZ: OBGyroSampleRate  # value = <OBGyroSampleRate.SAMPLE_RATE_1_KHZ: 10>
SAMPLE_RATE_200_HZ: OBGyroSampleRate  # value = <OBGyroSampleRate.SAMPLE_RATE_200_HZ: 8>
SAMPLE_RATE_25_HZ: OBGyroSampleRate  # value = <OBGyroSampleRate.SAMPLE_RATE_25_HZ: 5>
SAMPLE_RATE_2_KHZ: OBGyroSampleRate  # value = <OBGyroSampleRate.SAMPLE_RATE_2_KHZ: 11>
SAMPLE_RATE_32_KHZ: OBGyroSampleRate  # value = <OBGyroSampleRate.SAMPLE_RATE_32_KHZ: 15>
SAMPLE_RATE_3_125_HZ: OBGyroSampleRate  # value = <OBGyroSampleRate.SAMPLE_RATE_3_125_HZ: 2>
SAMPLE_RATE_400_HZ: OBGyroSampleRate  # value = <OBGyroSampleRate.SAMPLE_RATE_400_HZ: 16>
SAMPLE_RATE_4_KHZ: OBGyroSampleRate  # value = <OBGyroSampleRate.SAMPLE_RATE_4_KHZ: 12>
SAMPLE_RATE_500_HZ: OBGyroSampleRate  # value = <OBGyroSampleRate.SAMPLE_RATE_500_HZ: 9>
SAMPLE_RATE_50_HZ: OBGyroSampleRate  # value = <OBGyroSampleRate.SAMPLE_RATE_50_HZ: 6>
SAMPLE_RATE_6_25_HZ: OBGyroSampleRate  # value = <OBGyroSampleRate.SAMPLE_RATE_6_25_HZ: 3>
SAMPLE_RATE_800_HZ: OBGyroSampleRate  # value = <OBGyroSampleRate.SAMPLE_RATE_800_HZ: 17>
SAMPLE_RATE_8_KHZ: OBGyroSampleRate  # value = <OBGyroSampleRate.SAMPLE_RATE_8_KHZ: 13>
SAMPLE_RATE_UNKNOWN: OBGyroSampleRate  # value = <OBGyroSampleRate.SAMPLE_RATE_UNKNOWN: 0>
STOPPED: OBPlaybackStatus  # value = <OBPlaybackStatus.STOPPED: 3>
UNKNOWN: OBPlaybackStatus  # value = <OBPlaybackStatus.UNKNOWN: 0>
OBAccelSampleRate = OBGyroSampleRate
OBFloat3D = OBAccelValue
OBGyroValue = OBAccelValue
