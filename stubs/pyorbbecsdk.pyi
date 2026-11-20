"""
OrbbecSDK python binding
"""

from __future__ import annotations

import typing

import numpy
import numpy.typing
import typing_extensions

__all__: list[str] = [
    "AccelFrame",
    "AccelStreamProfile",
    "AlignFilter",
    "ApplicationConfig",
    "ApplicationDevDecimationConfig",
    "ApplicationHDRMergeConfig",
    "ApplicationPointCloudConfig",
    "ApplicationSensorConfig",
    "COUNT",
    "CameraParamList",
    "ColorFrame",
    "ColorPresetList",
    "ConfidenceFrame",
    "Config",
    "Context",
    "DecimationFilter",
    "DepthFrame",
    "Device",
    "DeviceFrameInterleaveList",
    "DeviceInfo",
    "DeviceList",
    "DevicePresetList",
    "DisparityTransform",
    "EdgeNoiseRemovalFilter",
    "EnhancedDepthFilter",
    "FalsePositiveFilter",
    "Filter",
    "FilterFactory",
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
    "OBAwbGainParams",
    "OBBaselineCalibrationParam",
    "OBBoolPropertyRange",
    "OBCalibrationParam",
    "OBCameraDistortion",
    "OBCameraDistortionModel",
    "OBCameraIntrinsic",
    "OBCameraParam",
    "OBCameraPerformanceMode",
    "OBClockType",
    "OBCmdVersion",
    "OBColorPoint",
    "OBColorPreset",
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
    "OBDepthWorkModeInternal",
    "OBDepthWorkModeList",
    "OBDepthWorkModeTag",
    "OBDepthWorkMode_Internal",
    "OBDeviceAccessMode",
    "OBDeviceAccessState",
    "OBDeviceDevelopmentMode",
    "OBDeviceErrorCode",
    "OBDeviceErrorState",
    "OBDeviceIpAddrConfig",
    "OBDeviceSerialNumber",
    "OBDeviceSyncConfig",
    "OBDeviceTemperature",
    "OBDeviceTime",
    "OBDeviceTimestampResetConfig",
    "OBDeviceType",
    "OBDispOffsetConfig",
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
    "OBImuPresetList",
    "OBIntPropertyRange",
    "OBIntraCameraSyncReference",
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
    "OBNetIpConfig",
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
    "OBSerialNumber",
    "OBSpatialAdvancedFilterParams",
    "OBSpatialFastFilterParams",
    "OBSpatialModerateFilterParams",
    "OBStatus",
    "OBStreamType",
    "OBSyncMode",
    "OBTofExposureThresholdControl",
    "OBTofFilterRange",
    "OBUSBPowerState",
    "OBUint16PropertyRange",
    "OBUint8PropertyRange",
    "OBUpgradeState",
    "OBUvcBackendType",
    "OBVersionInfo",
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
    "SpatialFastFilter",
    "SpatialModerateFilter",
    "StreamProfile",
    "StreamProfileList",
    "TemporalFilter",
    "ThresholdFilter",
    "UNKNOWN",
    "UnDistortionFilter",
    "VideoFrame",
    "VideoStreamProfile",
    "convert_accel_full_scale_range_to_string",
    "convert_format_to_string",
    "convert_frame_metadata_type_to_string",
    "convert_frame_type_to_sensor_type",
    "convert_frame_type_to_stream_type",
    "convert_frame_type_to_string",
    "convert_gyro_full_scale_range_to_string",
    "convert_imu_sample_rate_to_string",
    "convert_imu_sample_rate_to_value",
    "convert_imu_sample_rate_value_to_type",
    "convert_lidar_scan_rate_to_string",
    "convert_sensor_type_to_stream_type",
    "convert_sensor_type_to_string",
    "convert_stream_type_to_frame_type",
    "convert_stream_type_to_sensor_type",
    "convert_stream_type_to_string",
    "get_version",
    "get_version_major",
    "get_version_minor",
    "get_version_patch",
    "get_version_stage",
    "is_video_sensor_type",
    "is_video_stream_type",
    "save_lidar_point_cloud_to_ply",
    "save_point_cloud_to_ply",
    "transformation2dto2d",
    "transformation2dto3d",
    "transformation3dto2d",
    "transformation3dto3d",
]

class OBDeviceErrorCode:
    """
    Members:

      DEVICE_ERROR_RGB_SENSOR

      DEVICE_ERROR_IRL_SENSOR

      DEVICE_ERROR_IRR_SENSOR

      DEVICE_ERROR_IMU_SENSOR

      DEVICE_ERROR_LASER_MODULE

      DEVICE_ERROR_FLOOD_MODULE

      DEVICE_ERROR_LDP_SENSOR

      DEVICE_ERROR_M_ADC_CHIP

      DEVICE_ERROR_S_ADC_CHIP

      DEVICE_ERROR_EEPROM_SENSOR

      DEVICE_ERROR_CFG_PARAM

      DEVICE_ERROR_CALIB_PARAM

      DEVICE_ERROR_TEC_FUN

      DEVICE_ERROR_MCU_FUN

      DEVICE_ERROR_DSP_MODULE

      DEVICE_ERROR_OVER_LOAD

      DEVICE_ERROR_ISP_MODULE

      DEVICE_ERROR_TRB_EXHAUSTION

      DEVICE_ERROR_OVF_MODULE

      DEVICE_ERROR_RGB_STREAM

      DEVICE_ERROR_IRL_STREAM

      DEVICE_ERROR_IRR_STREAM

      DEVICE_ERROR_DEP_STREAM

      DEVICE_ERROR_IRL_SNS_STREAM

      DEVICE_ERROR_IRR_SNS_STREAM

      DEVICE_WARNING_PERMISSION

      DEVICE_WARNING_IR_TEMPERATURE

      DEVICE_WARNING_RGB_TEMPERATURE

      DEVICE_WARNING_LASER_TEMPERATURE

      DEVICE_WARNING_CPU_TEMPERATURE

      DEVICE_WARNING_RES_MISMATCH

      DEVICE_WARNING_FPS_MISMATCH

      DEVICE_WARNING_D2C_UNSPPOURT

      DEVICE_WARNING_USB_LOG

      DEVICE_WARNING_LOG_OVERFLOW
    """

    DEVICE_ERROR_CALIB_PARAM: typing.ClassVar[OBDeviceErrorCode]
    DEVICE_ERROR_CFG_PARAM: typing.ClassVar[OBDeviceErrorCode]
    DEVICE_ERROR_DEP_STREAM: typing.ClassVar[OBDeviceErrorCode]
    DEVICE_ERROR_DSP_MODULE: typing.ClassVar[OBDeviceErrorCode]
    DEVICE_ERROR_EEPROM_SENSOR: typing.ClassVar[OBDeviceErrorCode]
    DEVICE_ERROR_FLOOD_MODULE: typing.ClassVar[OBDeviceErrorCode]
    DEVICE_ERROR_IMU_SENSOR: typing.ClassVar[OBDeviceErrorCode]
    DEVICE_ERROR_IRL_SENSOR: typing.ClassVar[OBDeviceErrorCode]
    DEVICE_ERROR_IRL_SNS_STREAM: typing.ClassVar[OBDeviceErrorCode]
    DEVICE_ERROR_IRL_STREAM: typing.ClassVar[OBDeviceErrorCode]
    DEVICE_ERROR_IRR_SENSOR: typing.ClassVar[OBDeviceErrorCode]
    DEVICE_ERROR_IRR_SNS_STREAM: typing.ClassVar[OBDeviceErrorCode]
    DEVICE_ERROR_IRR_STREAM: typing.ClassVar[OBDeviceErrorCode]
    DEVICE_ERROR_ISP_MODULE: typing.ClassVar[OBDeviceErrorCode]
    DEVICE_ERROR_LASER_MODULE: typing.ClassVar[OBDeviceErrorCode]
    DEVICE_ERROR_LDP_SENSOR: typing.ClassVar[OBDeviceErrorCode]
    DEVICE_ERROR_MCU_FUN: typing.ClassVar[OBDeviceErrorCode]
    DEVICE_ERROR_M_ADC_CHIP: typing.ClassVar[OBDeviceErrorCode]
    DEVICE_ERROR_OVER_LOAD: typing.ClassVar[OBDeviceErrorCode]
    DEVICE_ERROR_OVF_MODULE: typing.ClassVar[OBDeviceErrorCode]
    DEVICE_ERROR_RGB_SENSOR: typing.ClassVar[OBDeviceErrorCode]
    DEVICE_ERROR_RGB_STREAM: typing.ClassVar[OBDeviceErrorCode]
    DEVICE_ERROR_S_ADC_CHIP: typing.ClassVar[OBDeviceErrorCode]
    DEVICE_ERROR_TEC_FUN: typing.ClassVar[OBDeviceErrorCode]
    DEVICE_ERROR_TRB_EXHAUSTION: typing.ClassVar[OBDeviceErrorCode]
    DEVICE_WARNING_CPU_TEMPERATURE: typing.ClassVar[OBDeviceErrorCode]
    DEVICE_WARNING_D2C_UNSPPOURT: typing.ClassVar[OBDeviceErrorCode]
    DEVICE_WARNING_FPS_MISMATCH: typing.ClassVar[OBDeviceErrorCode]
    DEVICE_WARNING_IR_TEMPERATURE: typing.ClassVar[OBDeviceErrorCode]
    DEVICE_WARNING_LASER_TEMPERATURE: typing.ClassVar[OBDeviceErrorCode]
    DEVICE_WARNING_LOG_OVERFLOW: typing.ClassVar[OBDeviceErrorCode]
    DEVICE_WARNING_PERMISSION: typing.ClassVar[OBDeviceErrorCode]
    DEVICE_WARNING_RES_MISMATCH: typing.ClassVar[OBDeviceErrorCode]
    DEVICE_WARNING_RGB_TEMPERATURE: typing.ClassVar[OBDeviceErrorCode]
    DEVICE_WARNING_USB_LOG: typing.ClassVar[OBDeviceErrorCode]
    __members__: typing.ClassVar[dict[str, OBDeviceErrorCode]]
    def __and__(self, other: typing.Any) -> typing.Any: ...
    def __eq__(self, other: typing.Any) -> bool: ...
    def __ge__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __gt__(self, other: typing.Any) -> bool: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __invert__(self) -> typing.Any: ...
    def __le__(self, other: typing.Any) -> bool: ...
    def __lt__(self, other: typing.Any) -> bool: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __or__(self, other: typing.Any) -> typing.Any: ...
    def __rand__(self, other: typing.Any) -> typing.Any: ...
    def __repr__(self) -> str: ...
    def __ror__(self, other: typing.Any) -> typing.Any: ...
    def __rxor__(self, other: typing.Any) -> typing.Any: ...
    def __setstate__(self, state: int) -> None: ...
    def __str__(self) -> str: ...
    def __xor__(self, other: typing.Any) -> typing.Any: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class OBDeviceTime:
    @property
    def rtt(self) -> int: ...
    @rtt.setter
    def rtt(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def time(self) -> int: ...
    @time.setter
    def time(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @staticmethod
    def from_bytes(data: bytes) -> OBDeviceTime:
        """
        Decode an exact-size native packed SDK payload.
        """

    def __init__(self) -> None: ...
    def to_bytes(self) -> bytes:
        """
        Copy the native packed SDK layout.
        """

class OBDeviceErrorState:
    @property
    def error_code(self) -> int: ...
    @error_code.setter
    def error_code(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @staticmethod
    def from_bytes(data: bytes) -> OBDeviceErrorState:
        """
        Decode an exact-size native packed SDK payload.
        """

    def __init__(self) -> None: ...
    def to_bytes(self) -> bytes:
        """
        Copy the native packed SDK layout.
        """

class OBVersionInfo:
    depth_chip: str
    device_name: str
    @property
    def device_type(self) -> int: ...
    @device_type.setter
    def device_type(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    firmware_version: str
    hardware_version: str
    reserved: bytes
    sdk_version: str
    serial_number: str
    sub_system_version: str
    system_chip: str
    @staticmethod
    def from_bytes(data: bytes) -> OBVersionInfo:
        """
        Decode an exact-size native packed SDK payload.
        """

    def __init__(self) -> None: ...
    def to_bytes(self) -> bytes:
        """
        Copy the native packed SDK layout.
        """

class OBDepthWorkModeInternal:
    checksum: bytes
    name: str
    @property
    def option_code(self) -> int: ...
    @option_code.setter
    def option_code(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @staticmethod
    def from_bytes(data: bytes) -> OBDepthWorkModeInternal:
        """
        Decode an exact-size native packed SDK payload.
        """

    def __init__(self) -> None: ...
    def to_bytes(self) -> bytes:
        """
        Copy the native packed SDK layout.
        """

class OBImuPresetList:
    @staticmethod
    def from_bytes(data: bytes) -> OBImuPresetList:
        """
        Decode an exact-size native packed SDK payload.
        """

    def __init__(self) -> None: ...
    def to_bytes(self) -> bytes:
        """
        Copy the native packed SDK layout.
        """

    @property
    def count(self) -> int: ...
    @property
    def values(self) -> list[int]: ...
    @values.setter
    def values(self, arg1: typing.Sequence[int]) -> None: ...

class OBPermissionType:
    """
    Members:

      PERMISSION_DENY

      PERMISSION_READ

      PERMISSION_WRITE

      PERMISSION_READ_WRITE

      PERMISSION_ANY
    """

    PERMISSION_ANY: typing.ClassVar[OBPermissionType]
    PERMISSION_DENY: typing.ClassVar[OBPermissionType]
    PERMISSION_READ: typing.ClassVar[OBPermissionType]
    PERMISSION_READ_WRITE: typing.ClassVar[OBPermissionType]
    PERMISSION_WRITE: typing.ClassVar[OBPermissionType]
    __members__: typing.ClassVar[dict[str, OBPermissionType]]
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

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

    ERROR_BUFFER_TOO_SMALL: typing.ClassVar[OBStatus]
    ERROR_DEVICE_ACCESS_DENIED: typing.ClassVar[OBStatus]
    ERROR_DEVICE_CONNECT_FAILED: typing.ClassVar[OBStatus]
    ERROR_DEVICE_DISCONNECTED: typing.ClassVar[OBStatus]
    ERROR_DEVICE_RESPONSE_BAD_MAGIC: typing.ClassVar[OBStatus]
    ERROR_DEVICE_RESPONSE_CHANNEL_FAILURE: typing.ClassVar[OBStatus]
    ERROR_DEVICE_RESPONSE_ERROR: typing.ClassVar[OBStatus]
    ERROR_DEVICE_RESPONSE_WARNING: typing.ClassVar[OBStatus]
    ERROR_DEVICE_RESPONSE_WRONG_DATA_SIZE: typing.ClassVar[OBStatus]
    ERROR_DEVICE_RESPONSE_WRONG_ID: typing.ClassVar[OBStatus]
    ERROR_DEVICE_RESPONSE_WRONG_OPCODE: typing.ClassVar[OBStatus]
    ERROR_DEVICE_UNAVAILABLE: typing.ClassVar[OBStatus]
    ERROR_DEVICE_UNKNOWN: typing.ClassVar[OBStatus]
    ERROR_FRAME_DATA: typing.ClassVar[OBStatus]
    ERROR_FRAME_DATA_LEN: typing.ClassVar[OBStatus]
    ERROR_FRAME_QUEUE_OVERFLOW: typing.ClassVar[OBStatus]
    ERROR_INVALID_DATA: typing.ClassVar[OBStatus]
    ERROR_INVALID_DATA_LEN: typing.ClassVar[OBStatus]
    ERROR_INVALID_PARAMETER: typing.ClassVar[OBStatus]
    ERROR_IO_FAILURE: typing.ClassVar[OBStatus]
    ERROR_ITEM_NOT_FOUND: typing.ClassVar[OBStatus]
    ERROR_MEMORY: typing.ClassVar[OBStatus]
    ERROR_NOT_IMPLEMENTED: typing.ClassVar[OBStatus]
    ERROR_NO_DEVICE: typing.ClassVar[OBStatus]
    ERROR_RESOURCE_BUSY: typing.ClassVar[OBStatus]
    ERROR_UNKNOWN: typing.ClassVar[OBStatus]
    ERROR_UNSUPPORTED_OPERATION: typing.ClassVar[OBStatus]
    ERROR_WAIT_TIMEOUT: typing.ClassVar[OBStatus]
    ERROR_WRONG_API_CALL_SEQUENCE: typing.ClassVar[OBStatus]
    STATUS_ERROR: typing.ClassVar[OBStatus]
    STATUS_OK: typing.ClassVar[OBStatus]
    __members__: typing.ClassVar[dict[str, OBStatus]]
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

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

    DEBUG: typing.ClassVar[OBLogLevel]
    ERROR: typing.ClassVar[OBLogLevel]
    FATAL: typing.ClassVar[OBLogLevel]
    INFO: typing.ClassVar[OBLogLevel]
    NONE: typing.ClassVar[OBLogLevel]
    WARNING: typing.ClassVar[OBLogLevel]
    __members__: typing.ClassVar[dict[str, OBLogLevel]]
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

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

      LICENSE_VERIFY_FAILED : License verification failed, the device/feature license is missing, invalid or expired

      STD_EXCEPTION

      TYPE_MEMORY
    """

    ACCESS_DENIED: typing.ClassVar[OBException]
    CAMERA_DISCONNECTED: typing.ClassVar[OBException]
    DEVICE_UNAVAILABLE: typing.ClassVar[OBException]
    INVALID_DATA: typing.ClassVar[OBException]
    INVALID_VALUE: typing.ClassVar[OBException]
    IO_ERROR: typing.ClassVar[OBException]
    LICENSE_VERIFY_FAILED: typing.ClassVar[OBException]
    NOT_FOUND: typing.ClassVar[OBException]
    NOT_IMPLEMENTED: typing.ClassVar[OBException]
    PLATFORM: typing.ClassVar[OBException]
    RESOURCE_BUSY: typing.ClassVar[OBException]
    STD_EXCEPTION: typing.ClassVar[OBException]
    TYPE_MEMORY: typing.ClassVar[OBException]
    UNKNOWN: typing.ClassVar[OBException]
    UNSUPPORTED_OPERATION: typing.ClassVar[OBException]
    WRONG_API_CALL_SEQUENCE: typing.ClassVar[OBException]
    __members__: typing.ClassVar[dict[str, OBException]]
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
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

    ACCEL_SENSOR: typing.ClassVar[OBSensorType]
    COLOR_SENSOR: typing.ClassVar[OBSensorType]
    CONFIDENCE_SENSOR: typing.ClassVar[OBSensorType]
    DEPTH_SENSOR: typing.ClassVar[OBSensorType]
    GYRO_SENSOR: typing.ClassVar[OBSensorType]
    IR_SENSOR: typing.ClassVar[OBSensorType]
    LEFT_COLOR_SENSOR: typing.ClassVar[OBSensorType]
    LEFT_IR_SENSOR: typing.ClassVar[OBSensorType]
    LIDAR_SENSOR: typing.ClassVar[OBSensorType]
    RAW_PHASE_SENSOR: typing.ClassVar[OBSensorType]
    RIGHT_COLOR_SENSOR: typing.ClassVar[OBSensorType]
    RIGHT_IR_SENSOR: typing.ClassVar[OBSensorType]
    TYPE_COUNT_SENSOR: typing.ClassVar[OBSensorType]
    UNKNOWN_SENSOR: typing.ClassVar[OBSensorType]
    __members__: typing.ClassVar[dict[str, OBSensorType]]
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
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

    ACCEL_STREAM: typing.ClassVar[OBStreamType]
    COLOR_STREAM: typing.ClassVar[OBStreamType]
    CONFIDENCE_STREAM: typing.ClassVar[OBStreamType]
    DEPTH_STREAM: typing.ClassVar[OBStreamType]
    GYRO_STREAM: typing.ClassVar[OBStreamType]
    IR_STREAM: typing.ClassVar[OBStreamType]
    LEFT_COLOR_STREAM: typing.ClassVar[OBStreamType]
    LEFT_IR_STREAM: typing.ClassVar[OBStreamType]
    LIDAR_STREAM: typing.ClassVar[OBStreamType]
    RAW_PHASE_STREAM: typing.ClassVar[OBStreamType]
    RIGHT_COLOR_STREAM: typing.ClassVar[OBStreamType]
    RIGHT_IR_STREAM: typing.ClassVar[OBStreamType]
    TYPE_COUNT_STREAM: typing.ClassVar[OBStreamType]
    UNKNOWN_STREAM: typing.ClassVar[OBStreamType]
    VIDEO_STREAM: typing.ClassVar[OBStreamType]
    __members__: typing.ClassVar[dict[str, OBStreamType]]
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
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

    ACCEL_FRAME: typing.ClassVar[OBFrameType]
    COLOR_FRAME: typing.ClassVar[OBFrameType]
    CONFIDENCE_FRAME: typing.ClassVar[OBFrameType]
    DEPTH_FRAME: typing.ClassVar[OBFrameType]
    FRAME_SET: typing.ClassVar[OBFrameType]
    GYRO_FRAME: typing.ClassVar[OBFrameType]
    IR_FRAME: typing.ClassVar[OBFrameType]
    LEFT_COLOR_FRAME: typing.ClassVar[OBFrameType]
    LEFT_IR_FRAME: typing.ClassVar[OBFrameType]
    LIDAR_POINTS_FRAME: typing.ClassVar[OBFrameType]
    RAW_PHASE_FRAME: typing.ClassVar[OBFrameType]
    RIGHT_COLOR_FRAME: typing.ClassVar[OBFrameType]
    RIGHT_IR_FRAME: typing.ClassVar[OBFrameType]
    TYPE_COUNT_FRAME: typing.ClassVar[OBFrameType]
    UNKNOWN_FRAME: typing.ClassVar[OBFrameType]
    VIDEO_FRAME: typing.ClassVar[OBFrameType]
    __members__: typing.ClassVar[dict[str, OBFrameType]]
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class OBPixelType:
    """
    Members:

      OB_PIXEL_UNKNOWN

      OB_PIXEL_DEPTH

      OB_PIXEL_DISPARITY

      OB_PIXEL_RAW_PHASE

      OB_PIXEL_TOF_DEPTH
    """

    OB_PIXEL_DEPTH: typing.ClassVar[OBPixelType]
    OB_PIXEL_DISPARITY: typing.ClassVar[OBPixelType]
    OB_PIXEL_RAW_PHASE: typing.ClassVar[OBPixelType]
    OB_PIXEL_TOF_DEPTH: typing.ClassVar[OBPixelType]
    OB_PIXEL_UNKNOWN: typing.ClassVar[OBPixelType]
    __members__: typing.ClassVar[dict[str, OBPixelType]]
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

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

    ACCEL: typing.ClassVar[OBFormat]
    BA81: typing.ClassVar[OBFormat]
    BGR: typing.ClassVar[OBFormat]
    BGRA: typing.ClassVar[OBFormat]
    BYR2: typing.ClassVar[OBFormat]
    COMPRESSED: typing.ClassVar[OBFormat]
    GRAY: typing.ClassVar[OBFormat]
    GYRO: typing.ClassVar[OBFormat]
    H264: typing.ClassVar[OBFormat]
    H265: typing.ClassVar[OBFormat]
    HEVC: typing.ClassVar[OBFormat]
    I420: typing.ClassVar[OBFormat]
    LIDAR_CALIBRATION: typing.ClassVar[OBFormat]
    LIDAR_POINT: typing.ClassVar[OBFormat]
    LIDAR_SCAN: typing.ClassVar[OBFormat]
    LIDAR_SPHERE_POINT: typing.ClassVar[OBFormat]
    MJPG: typing.ClassVar[OBFormat]
    NV12: typing.ClassVar[OBFormat]
    NV21: typing.ClassVar[OBFormat]
    POINT: typing.ClassVar[OBFormat]
    RGB: typing.ClassVar[OBFormat]
    RGBA: typing.ClassVar[OBFormat]
    RGB_POINT: typing.ClassVar[OBFormat]
    RLE: typing.ClassVar[OBFormat]
    RVL: typing.ClassVar[OBFormat]
    RW16: typing.ClassVar[OBFormat]
    UNKNOWN_FORMAT: typing.ClassVar[OBFormat]
    UYVY: typing.ClassVar[OBFormat]
    Y10: typing.ClassVar[OBFormat]
    Y11: typing.ClassVar[OBFormat]
    Y12: typing.ClassVar[OBFormat]
    Y12C4: typing.ClassVar[OBFormat]
    Y14: typing.ClassVar[OBFormat]
    Y16: typing.ClassVar[OBFormat]
    Y8: typing.ClassVar[OBFormat]
    YUY2: typing.ClassVar[OBFormat]
    YUYV: typing.ClassVar[OBFormat]
    YV12: typing.ClassVar[OBFormat]
    Z16: typing.ClassVar[OBFormat]
    __members__: typing.ClassVar[dict[str, OBFormat]]
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

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

    DONE: typing.ClassVar[OBUpgradeState]
    DONE_REBOOT_AND_REUPDATE: typing.ClassVar[OBUpgradeState]
    DONE_WITH_DUPLICATES: typing.ClassVar[OBUpgradeState]
    ERR_DDR: typing.ClassVar[OBUpgradeState]
    ERR_ERASE: typing.ClassVar[OBUpgradeState]
    ERR_FILE_READ: typing.ClassVar[OBUpgradeState]
    ERR_FLASH_TYPE: typing.ClassVar[OBUpgradeState]
    ERR_IMAGE_SIZE: typing.ClassVar[OBUpgradeState]
    ERR_INVALID_COUNT: typing.ClassVar[OBUpgradeState]
    ERR_MISMATCH: typing.ClassVar[OBUpgradeState]
    ERR_OTHER: typing.ClassVar[OBUpgradeState]
    ERR_PROGRAM: typing.ClassVar[OBUpgradeState]
    ERR_TIMEOUT: typing.ClassVar[OBUpgradeState]
    ERR_TRANSFER: typing.ClassVar[OBUpgradeState]
    ERR_UNSUPPORT_DEV: typing.ClassVar[OBUpgradeState]
    ERR_VERIFY: typing.ClassVar[OBUpgradeState]
    FILE_TRANSFER: typing.ClassVar[OBUpgradeState]
    IN_PROGRESS: typing.ClassVar[OBUpgradeState]
    START: typing.ClassVar[OBUpgradeState]
    VERIFY_IMAGE: typing.ClassVar[OBUpgradeState]
    VERIFY_SUCCESS: typing.ClassVar[OBUpgradeState]
    __members__: typing.ClassVar[dict[str, OBUpgradeState]]
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

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

    DONE: typing.ClassVar[OBFileTranState]
    ERR_DDR: typing.ClassVar[OBFileTranState]
    ERR_MD5_ERROR: typing.ClassVar[OBFileTranState]
    ERR_NOT_ENOUGH_SPACE: typing.ClassVar[OBFileTranState]
    ERR_PATH_NOT_WRITABLE: typing.ClassVar[OBFileTranState]
    ERR_TIMEOUT: typing.ClassVar[OBFileTranState]
    ERR_WRITE_FLASH_ERROR: typing.ClassVar[OBFileTranState]
    PREPARING: typing.ClassVar[OBFileTranState]
    TRANSFER: typing.ClassVar[OBFileTranState]
    __members__: typing.ClassVar[dict[str, OBFileTranState]]
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
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

    DONE: typing.ClassVar[OBDataTranState]
    ERR_BUSY: typing.ClassVar[OBDataTranState]
    ERR_OTHER: typing.ClassVar[OBDataTranState]
    ERR_TRAN_FAILED: typing.ClassVar[OBDataTranState]
    ERR_UNSUPPORTED: typing.ClassVar[OBDataTranState]
    ERR_VERIFY_FAILED: typing.ClassVar[OBDataTranState]
    STOPPED: typing.ClassVar[OBDataTranState]
    TRANSFERRING: typing.ClassVar[OBDataTranState]
    VERIFYING: typing.ClassVar[OBDataTranState]
    __members__: typing.ClassVar[dict[str, OBDataTranState]]
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class OBIntPropertyRange:
    @property
    def current(self) -> int: ...
    @current.setter
    def current(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def default_value(self) -> int: ...
    @default_value.setter
    def default_value(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def max(self) -> int: ...
    @max.setter
    def max(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def min(self) -> int: ...
    @min.setter
    def min(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def step(self) -> int: ...
    @step.setter
    def step(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __init__(self) -> None: ...

class OBFloatPropertyRange:
    @property
    def current(self) -> float: ...
    @current.setter
    def current(self, value: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def default_value(self) -> float: ...
    @default_value.setter
    def default_value(self, value: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def max(self) -> float: ...
    @max.setter
    def max(self, value: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def min(self) -> float: ...
    @min.setter
    def min(self, value: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def step(self) -> float: ...
    @step.setter
    def step(self, value: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    def __init__(self) -> None: ...

class OBUint16PropertyRange:
    @property
    def current(self) -> int: ...
    @current.setter
    def current(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def default_value(self) -> int: ...
    @default_value.setter
    def default_value(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def max(self) -> int: ...
    @max.setter
    def max(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def min(self) -> int: ...
    @min.setter
    def min(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def step(self) -> int: ...
    @step.setter
    def step(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __init__(self) -> None: ...

class OBUint8PropertyRange:
    @property
    def current(self) -> int: ...
    @current.setter
    def current(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def default_value(self) -> int: ...
    @default_value.setter
    def default_value(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def max(self) -> int: ...
    @max.setter
    def max(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def min(self) -> int: ...
    @min.setter
    def min(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def step(self) -> int: ...
    @step.setter
    def step(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __init__(self) -> None: ...

class OBBoolPropertyRange:
    cur: bool
    default_value: bool
    max: bool
    min: bool
    step: bool
    def __init__(self) -> None: ...

class OBCameraIntrinsic:
    @property
    def cx(self) -> float: ...
    @cx.setter
    def cx(self, value: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def cy(self) -> float: ...
    @cy.setter
    def cy(self, value: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def fx(self) -> float: ...
    @fx.setter
    def fx(self, value: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def fy(self) -> float: ...
    @fy.setter
    def fy(self, value: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def height(self) -> int: ...
    @height.setter
    def height(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def width(self) -> int: ...
    @width.setter
    def width(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __init__(self) -> None: ...
    def __repr__(self) -> str: ...

class OBAccelIntrinsic:
    @property
    def bias(self) -> numpy.typing.NDArray[numpy.float64]: ...
    @bias.setter
    def bias(self, value: typing_extensions.Annotated[numpy.typing.ArrayLike, numpy.float64]) -> None: ...
    @property
    def gravity(self) -> numpy.typing.NDArray[numpy.float64]: ...
    @gravity.setter
    def gravity(self, value: typing_extensions.Annotated[numpy.typing.ArrayLike, numpy.float64]) -> None: ...
    @property
    def noise_density(self) -> float: ...
    @noise_density.setter
    def noise_density(self, value: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def random_walk(self) -> float: ...
    @random_walk.setter
    def random_walk(self, value: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def reference_temp(self) -> float: ...
    @reference_temp.setter
    def reference_temp(self, value: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def scale_misalignment(self) -> numpy.typing.NDArray[numpy.float64]: ...
    @scale_misalignment.setter
    def scale_misalignment(self, value: typing_extensions.Annotated[numpy.typing.ArrayLike, numpy.float64]) -> None: ...
    @property
    def temp_slope(self) -> numpy.typing.NDArray[numpy.float64]: ...
    @temp_slope.setter
    def temp_slope(self, value: typing_extensions.Annotated[numpy.typing.ArrayLike, numpy.float64]) -> None: ...
    def __init__(self) -> None: ...

class OBGyroIntrinsic:
    @property
    def bias(self) -> numpy.typing.NDArray[numpy.float64]: ...
    @bias.setter
    def bias(self, value: typing_extensions.Annotated[numpy.typing.ArrayLike, numpy.float64]) -> None: ...
    @property
    def noise_density(self) -> float: ...
    @noise_density.setter
    def noise_density(self, value: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def random_walk(self) -> float: ...
    @random_walk.setter
    def random_walk(self, value: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def reference_temp(self) -> float: ...
    @reference_temp.setter
    def reference_temp(self, value: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def scale_misalignment(self) -> numpy.typing.NDArray[numpy.float64]: ...
    @scale_misalignment.setter
    def scale_misalignment(self, value: typing_extensions.Annotated[numpy.typing.ArrayLike, numpy.float64]) -> None: ...
    @property
    def temp_slope(self) -> numpy.typing.NDArray[numpy.float64]: ...
    @temp_slope.setter
    def temp_slope(self, value: typing_extensions.Annotated[numpy.typing.ArrayLike, numpy.float64]) -> None: ...
    def __init__(self) -> None: ...

class OBCameraDistortion:
    @property
    def k1(self) -> float: ...
    @k1.setter
    def k1(self, value: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def k2(self) -> float: ...
    @k2.setter
    def k2(self, value: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def k3(self) -> float: ...
    @k3.setter
    def k3(self, value: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def k4(self) -> float: ...
    @k4.setter
    def k4(self, value: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def k5(self) -> float: ...
    @k5.setter
    def k5(self, value: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def k6(self) -> float: ...
    @k6.setter
    def k6(self, value: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    model: OBCameraDistortionModel
    @property
    def p1(self) -> float: ...
    @p1.setter
    def p1(self, value: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def p2(self) -> float: ...
    @p2.setter
    def p2(self, value: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    def __init__(self) -> None: ...
    def __repr__(self) -> str: ...

class OBCameraDistortionModel:
    """
    Members:

      NONE

      MODIFIED_BROWN_CONRADY

      INVERSE_BROWN_CONRADY

      BROWN_CONRADY

      BROWN_CONRADY_K6

      KANNALA_BRANDT4
    """

    BROWN_CONRADY: typing.ClassVar[OBCameraDistortionModel]
    BROWN_CONRADY_K6: typing.ClassVar[OBCameraDistortionModel]
    INVERSE_BROWN_CONRADY: typing.ClassVar[OBCameraDistortionModel]
    KANNALA_BRANDT4: typing.ClassVar[OBCameraDistortionModel]
    MODIFIED_BROWN_CONRADY: typing.ClassVar[OBCameraDistortionModel]
    NONE: typing.ClassVar[OBCameraDistortionModel]
    __members__: typing.ClassVar[dict[str, OBCameraDistortionModel]]
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class OBExtrinsic:
    @property
    def rot(self) -> numpy.typing.NDArray[numpy.float32]: ...
    @rot.setter
    def rot(self, value: typing_extensions.Annotated[numpy.typing.ArrayLike, numpy.float32]) -> None: ...
    @property
    def transform(self) -> numpy.typing.NDArray[numpy.float32]: ...
    @transform.setter
    def transform(self, value: typing_extensions.Annotated[numpy.typing.ArrayLike, numpy.float32]) -> None: ...
    def __init__(self) -> None: ...
    def __repr__(self) -> str: ...

class OBCameraParam:
    depth_distortion: OBCameraDistortion
    depth_intrinsic: OBCameraIntrinsic
    is_mirrored: bool
    rgb_distortion: OBCameraDistortion
    rgb_intrinsic: OBCameraIntrinsic
    transform: OBExtrinsic
    def __init__(self) -> None: ...
    def __repr__(self) -> str: ...

class OBPresetResolutionConfig:
    @property
    def depth_decimation_factor(self) -> int: ...
    @depth_decimation_factor.setter
    def depth_decimation_factor(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def height(self) -> int: ...
    @height.setter
    def height(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def ir_decimation_factor(self) -> int: ...
    @ir_decimation_factor.setter
    def ir_decimation_factor(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def width(self) -> int: ...
    @width.setter
    def width(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @staticmethod
    def from_bytes(data: bytes) -> OBPresetResolutionConfig:
        """
        Decode an exact-size native packed SDK payload.
        """

    def __init__(self) -> None: ...
    def to_bytes(self) -> bytes:
        """
        Copy the native packed SDK layout.
        """

class OBAlignMode:
    """
    Members:

      DISABLE

      HW_MODE

      SW_MODE

      C2D_SW_MODE
    """

    C2D_SW_MODE: typing.ClassVar[OBAlignMode]
    DISABLE: typing.ClassVar[OBAlignMode]
    HW_MODE: typing.ClassVar[OBAlignMode]
    SW_MODE: typing.ClassVar[OBAlignMode]
    __members__: typing.ClassVar[dict[str, OBAlignMode]]
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class OBRect:
    @property
    def height(self) -> int: ...
    @height.setter
    def height(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def width(self) -> int: ...
    @width.setter
    def width(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def x(self) -> int: ...
    @x.setter
    def x(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def y(self) -> int: ...
    @y.setter
    def y(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @staticmethod
    def from_bytes(data: bytes) -> OBRect:
        """
        Decode an exact-size native packed SDK payload.
        """

    def __init__(self) -> None: ...
    def to_bytes(self) -> bytes:
        """
        Copy the native packed SDK layout.
        """

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

      MJPG_TO_NV12

      YUYV_TO_BGR

      YUYV_TO_RGBA

      YUYV_TO_BGRA

      YUYV_TO_Y16

      YUYV_TO_Y8

      RGBA_TO_RGB

      BGRA_TO_BGR

      Y16_TO_RGB

      Y8_TO_RGB
    """

    BGRA_TO_BGR: typing.ClassVar[OBConvertFormat]
    BGR_TO_RGB: typing.ClassVar[OBConvertFormat]
    I420_TO_RGB888: typing.ClassVar[OBConvertFormat]
    MJPG_TO_BGR888: typing.ClassVar[OBConvertFormat]
    MJPG_TO_BGRA: typing.ClassVar[OBConvertFormat]
    MJPG_TO_I420: typing.ClassVar[OBConvertFormat]
    MJPG_TO_NV12: typing.ClassVar[OBConvertFormat]
    MJPG_TO_NV21: typing.ClassVar[OBConvertFormat]
    MJPG_TO_RGB888: typing.ClassVar[OBConvertFormat]
    NV12_TO_RGB888: typing.ClassVar[OBConvertFormat]
    NV21_TO_RGB888: typing.ClassVar[OBConvertFormat]
    RGB888_TO_BGR: typing.ClassVar[OBConvertFormat]
    RGBA_TO_RGB: typing.ClassVar[OBConvertFormat]
    UYVY_TO_RGB888: typing.ClassVar[OBConvertFormat]
    Y16_TO_RGB: typing.ClassVar[OBConvertFormat]
    Y8_TO_RGB: typing.ClassVar[OBConvertFormat]
    YUYV_TO_BGR: typing.ClassVar[OBConvertFormat]
    YUYV_TO_BGRA: typing.ClassVar[OBConvertFormat]
    YUYV_TO_RGB888: typing.ClassVar[OBConvertFormat]
    YUYV_TO_RGBA: typing.ClassVar[OBConvertFormat]
    YUYV_TO_Y16: typing.ClassVar[OBConvertFormat]
    YUYV_TO_Y8: typing.ClassVar[OBConvertFormat]
    __members__: typing.ClassVar[dict[str, OBConvertFormat]]
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

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

    SAMPLE_RATE_100_HZ: typing.ClassVar[OBGyroSampleRate]
    SAMPLE_RATE_12_5_HZ: typing.ClassVar[OBGyroSampleRate]
    SAMPLE_RATE_16_KHZ: typing.ClassVar[OBGyroSampleRate]
    SAMPLE_RATE_1_5625_HZ: typing.ClassVar[OBGyroSampleRate]
    SAMPLE_RATE_1_KHZ: typing.ClassVar[OBGyroSampleRate]
    SAMPLE_RATE_200_HZ: typing.ClassVar[OBGyroSampleRate]
    SAMPLE_RATE_25_HZ: typing.ClassVar[OBGyroSampleRate]
    SAMPLE_RATE_2_KHZ: typing.ClassVar[OBGyroSampleRate]
    SAMPLE_RATE_32_KHZ: typing.ClassVar[OBGyroSampleRate]
    SAMPLE_RATE_3_125_HZ: typing.ClassVar[OBGyroSampleRate]
    SAMPLE_RATE_400_HZ: typing.ClassVar[OBGyroSampleRate]
    SAMPLE_RATE_4_KHZ: typing.ClassVar[OBGyroSampleRate]
    SAMPLE_RATE_500_HZ: typing.ClassVar[OBGyroSampleRate]
    SAMPLE_RATE_50_HZ: typing.ClassVar[OBGyroSampleRate]
    SAMPLE_RATE_6_25_HZ: typing.ClassVar[OBGyroSampleRate]
    SAMPLE_RATE_800_HZ: typing.ClassVar[OBGyroSampleRate]
    SAMPLE_RATE_8_KHZ: typing.ClassVar[OBGyroSampleRate]
    SAMPLE_RATE_UNKNOWN: typing.ClassVar[OBGyroSampleRate]
    __members__: typing.ClassVar[dict[str, OBGyroSampleRate]]
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
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

    FS_1000dps: typing.ClassVar[OBGyroFullScaleRange]
    FS_125dps: typing.ClassVar[OBGyroFullScaleRange]
    FS_16dps: typing.ClassVar[OBGyroFullScaleRange]
    FS_2000dps: typing.ClassVar[OBGyroFullScaleRange]
    FS_250dps: typing.ClassVar[OBGyroFullScaleRange]
    FS_31dps: typing.ClassVar[OBGyroFullScaleRange]
    FS_400dps: typing.ClassVar[OBGyroFullScaleRange]
    FS_500dps: typing.ClassVar[OBGyroFullScaleRange]
    FS_62dps: typing.ClassVar[OBGyroFullScaleRange]
    FS_800dps: typing.ClassVar[OBGyroFullScaleRange]
    FS_UNKNOWN: typing.ClassVar[OBGyroFullScaleRange]
    __members__: typing.ClassVar[dict[str, OBGyroFullScaleRange]]
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

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

    ACCEL_FS_12g: typing.ClassVar[OBAccelFullScaleRange]
    ACCEL_FS_16g: typing.ClassVar[OBAccelFullScaleRange]
    ACCEL_FS_24g: typing.ClassVar[OBAccelFullScaleRange]
    ACCEL_FS_2g: typing.ClassVar[OBAccelFullScaleRange]
    ACCEL_FS_3g: typing.ClassVar[OBAccelFullScaleRange]
    ACCEL_FS_4g: typing.ClassVar[OBAccelFullScaleRange]
    ACCEL_FS_6g: typing.ClassVar[OBAccelFullScaleRange]
    ACCEL_FS_8g: typing.ClassVar[OBAccelFullScaleRange]
    ACCEL_FS_UNKNOWN: typing.ClassVar[OBAccelFullScaleRange]
    __members__: typing.ClassVar[dict[str, OBAccelFullScaleRange]]
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class OBAccelValue:
    @property
    def x(self) -> float: ...
    @x.setter
    def x(self, value: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def y(self) -> float: ...
    @y.setter
    def y(self, value: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def z(self) -> float: ...
    @z.setter
    def z(self, value: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    def __init__(self) -> None: ...
    def __repr__(self) -> str: ...

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

    LIDAR_SCAN_10HZ: typing.ClassVar[OBLiDARScanRate]
    LIDAR_SCAN_15HZ: typing.ClassVar[OBLiDARScanRate]
    LIDAR_SCAN_20HZ: typing.ClassVar[OBLiDARScanRate]
    LIDAR_SCAN_25HZ: typing.ClassVar[OBLiDARScanRate]
    LIDAR_SCAN_30HZ: typing.ClassVar[OBLiDARScanRate]
    LIDAR_SCAN_40HZ: typing.ClassVar[OBLiDARScanRate]
    LIDAR_SCAN_5HZ: typing.ClassVar[OBLiDARScanRate]
    LIDAR_SCAN_UNKNOWN: typing.ClassVar[OBLiDARScanRate]
    __members__: typing.ClassVar[dict[str, OBLiDARScanRate]]
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class OBDeviceTemperature:
    @property
    def chip_bottom_temperature(self) -> float: ...
    @chip_bottom_temperature.setter
    def chip_bottom_temperature(self, value: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def chip_top_temperature(self) -> float: ...
    @chip_top_temperature.setter
    def chip_top_temperature(self, value: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def cpu_temperature(self) -> float: ...
    @cpu_temperature.setter
    def cpu_temperature(self, value: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def imu_temperature(self) -> float: ...
    @imu_temperature.setter
    def imu_temperature(self, value: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def ir_left_temperature(self) -> float: ...
    @ir_left_temperature.setter
    def ir_left_temperature(self, value: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def ir_right_temperature(self) -> float: ...
    @ir_right_temperature.setter
    def ir_right_temperature(self, value: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def ir_temperature(self) -> float: ...
    @ir_temperature.setter
    def ir_temperature(self, value: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def laser_temperature(self) -> float: ...
    @laser_temperature.setter
    def laser_temperature(self, value: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def main_board_temperature(self) -> float: ...
    @main_board_temperature.setter
    def main_board_temperature(self, value: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def rgb_temperature(self) -> float: ...
    @rgb_temperature.setter
    def rgb_temperature(self, value: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def tec_temperature(self) -> float: ...
    @tec_temperature.setter
    def tec_temperature(self, value: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @staticmethod
    def from_bytes(data: bytes) -> OBDeviceTemperature:
        """
        Decode an exact-size native packed SDK payload.
        """

    def __init__(self) -> None: ...
    def __repr__(self) -> str: ...
    def to_bytes(self) -> bytes:
        """
        Copy the native packed SDK layout.
        """

class OBDepthCroppingMode:
    """
    Members:

      AUTO

      CLOSE

      OPEN
    """

    AUTO: typing.ClassVar[OBDepthCroppingMode]
    CLOSE: typing.ClassVar[OBDepthCroppingMode]
    OPEN: typing.ClassVar[OBDepthCroppingMode]
    __members__: typing.ClassVar[dict[str, OBDepthCroppingMode]]
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class OBDeviceType:
    """
    Members:

      UNKNOWN

      LIGHT_MONOCULAR

      LIGHT_BINOCULAR

      TIME_OF_FLIGHT
    """

    LIGHT_BINOCULAR: typing.ClassVar[OBDeviceType]
    LIGHT_MONOCULAR: typing.ClassVar[OBDeviceType]
    TIME_OF_FLIGHT: typing.ClassVar[OBDeviceType]
    UNKNOWN: typing.ClassVar[OBDeviceType]
    __members__: typing.ClassVar[dict[str, OBDeviceType]]
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
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

      ALL
    """

    ACCEL: typing.ClassVar[OBMediaType]
    ALL: typing.ClassVar[OBMediaType]
    CAMERA_PARAM: typing.ClassVar[OBMediaType]
    COLOR: typing.ClassVar[OBMediaType]
    DEPTH: typing.ClassVar[OBMediaType]
    DEVICE_INFO: typing.ClassVar[OBMediaType]
    GYRO: typing.ClassVar[OBMediaType]
    IR: typing.ClassVar[OBMediaType]
    LEFT_IR: typing.ClassVar[OBMediaType]
    RIGHT_IR: typing.ClassVar[OBMediaType]
    STREAM_INFO: typing.ClassVar[OBMediaType]
    __members__: typing.ClassVar[dict[str, OBMediaType]]
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class OBMediaState:
    """
    Members:

      OB_MEDIA_BEGIN

      OB_MEDIA_PAUSE

      OB_MEDIA_RESUME

      OB_MEDIA_END
    """

    OB_MEDIA_BEGIN: typing.ClassVar[OBMediaState]
    OB_MEDIA_END: typing.ClassVar[OBMediaState]
    OB_MEDIA_PAUSE: typing.ClassVar[OBMediaState]
    OB_MEDIA_RESUME: typing.ClassVar[OBMediaState]
    __members__: typing.ClassVar[dict[str, OBMediaState]]
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
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

      ZERO_POINT_FIVE_MM

      ZERO_POINT_ZERO_FIVE_MM

      UNKNOWN
    """

    ONE_MM: typing.ClassVar[OBDepthPrecisionLevel]
    UNKNOWN: typing.ClassVar[OBDepthPrecisionLevel]
    ZERO_POINT_EIGHT_MM: typing.ClassVar[OBDepthPrecisionLevel]
    ZERO_POINT_FIVE_MM: typing.ClassVar[OBDepthPrecisionLevel]
    ZERO_POINT_FOUR_MM: typing.ClassVar[OBDepthPrecisionLevel]
    ZERO_POINT_ONE_MM: typing.ClassVar[OBDepthPrecisionLevel]
    ZERO_POINT_TWO_MM: typing.ClassVar[OBDepthPrecisionLevel]
    ZERO_POINT_ZERO_FIVE_MM: typing.ClassVar[OBDepthPrecisionLevel]
    __members__: typing.ClassVar[dict[str, OBDepthPrecisionLevel]]
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class OBTofFilterRange:
    """
    Members:

      CLOSE

      MIDDLE

      FAR

      DEBUG
    """

    CLOSE: typing.ClassVar[OBTofFilterRange]
    DEBUG: typing.ClassVar[OBTofFilterRange]
    FAR: typing.ClassVar[OBTofFilterRange]
    MIDDLE: typing.ClassVar[OBTofFilterRange]
    __members__: typing.ClassVar[dict[str, OBTofFilterRange]]
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class OBPoint3f:
    @property
    def x(self) -> float: ...
    @x.setter
    def x(self, value: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def y(self) -> float: ...
    @y.setter
    def y(self, value: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def z(self) -> float: ...
    @z.setter
    def z(self, value: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
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

class OBColorPoint:
    @property
    def b(self) -> int: ...
    @b.setter
    def b(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def g(self) -> int: ...
    @g.setter
    def g(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def r(self) -> int: ...
    @r.setter
    def r(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def x(self) -> float: ...
    @x.setter
    def x(self, value: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def y(self) -> float: ...
    @y.setter
    def y(self, value: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def z(self) -> float: ...
    @z.setter
    def z(self, value: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @staticmethod
    def get_sizeof() -> int: ...
    def __init__(self) -> None: ...
    def __repr__(self) -> str: ...

class OBLiDARScanPoint:
    @property
    def angle(self) -> float: ...
    @angle.setter
    def angle(self, value: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def distance(self) -> float: ...
    @distance.setter
    def distance(self, value: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def intensity(self) -> int: ...
    @intensity.setter
    def intensity(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __init__(self) -> None: ...

class OBLiDARPoint:
    @property
    def reflectivity(self) -> int: ...
    @reflectivity.setter
    def reflectivity(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def tag(self) -> int: ...
    @tag.setter
    def tag(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def x(self) -> float: ...
    @x.setter
    def x(self, value: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def y(self) -> float: ...
    @y.setter
    def y(self, value: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def z(self) -> float: ...
    @z.setter
    def z(self, value: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    def __init__(self) -> None: ...

class OBLiDARSpherePoint:
    @property
    def distance(self) -> float: ...
    @distance.setter
    def distance(self, value: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def phi(self) -> float: ...
    @phi.setter
    def phi(self, value: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def reflectivity(self) -> int: ...
    @reflectivity.setter
    def reflectivity(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def tag(self) -> int: ...
    @tag.setter
    def tag(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def theta(self) -> float: ...
    @theta.setter
    def theta(self, value: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    def __init__(self) -> None: ...

class OBCompressionMode:
    """
    Members:

      LOSSLESS

      LOSSY
    """

    LOSSLESS: typing.ClassVar[OBCompressionMode]
    LOSSY: typing.ClassVar[OBCompressionMode]
    __members__: typing.ClassVar[dict[str, OBCompressionMode]]
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class OBCompressionParams:
    @property
    def threshold(self) -> int: ...
    @threshold.setter
    def threshold(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __init__(self) -> None: ...

class OBTofExposureThresholdControl:
    @property
    def lower(self) -> int: ...
    @lower.setter
    def lower(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def upper(self) -> int: ...
    @upper.setter
    def upper(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @staticmethod
    def from_bytes(data: bytes) -> OBTofExposureThresholdControl:
        """
        Decode an exact-size native packed SDK payload.
        """

    def __init__(self) -> None: ...
    def to_bytes(self) -> bytes:
        """
        Copy the native packed SDK layout.
        """

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

    CLOSE: typing.ClassVar[OBSyncMode]
    IR_IMU_SYNC: typing.ClassVar[OBSyncMode]
    PRIMARY: typing.ClassVar[OBSyncMode]
    PRIMARY_IR_TRIGGER: typing.ClassVar[OBSyncMode]
    PRIMARY_MCU_TRIGGER: typing.ClassVar[OBSyncMode]
    PRIMARY_SOFT_TRIGGER: typing.ClassVar[OBSyncMode]
    SECONDARY: typing.ClassVar[OBSyncMode]
    SECONDARY_SOFT_TRIGGER: typing.ClassVar[OBSyncMode]
    STANDALONE: typing.ClassVar[OBSyncMode]
    UNKNOWN: typing.ClassVar[OBSyncMode]
    __members__: typing.ClassVar[dict[str, OBSyncMode]]
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class OBPowerLineFreqMode:
    """
    Members:

      FREQUENCY_50HZ

      FREQUENCY_60HZ

      FREQUENCY_CLOSE
    """

    FREQUENCY_50HZ: typing.ClassVar[OBPowerLineFreqMode]
    FREQUENCY_60HZ: typing.ClassVar[OBPowerLineFreqMode]
    FREQUENCY_CLOSE: typing.ClassVar[OBPowerLineFreqMode]
    __members__: typing.ClassVar[dict[str, OBPowerLineFreqMode]]
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class OBDeviceSyncConfig:
    @property
    def device_index(self) -> int: ...
    @device_index.setter
    def device_index(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def device_trigger_signal_out_delay(self) -> int: ...
    @device_trigger_signal_out_delay.setter
    def device_trigger_signal_out_delay(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def device_trigger_signal_out_polarity(self) -> int: ...
    @device_trigger_signal_out_polarity.setter
    def device_trigger_signal_out_polarity(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def ir_trigger_signal_delay(self) -> int: ...
    @ir_trigger_signal_delay.setter
    def ir_trigger_signal_delay(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def mcu_trigger_frequency(self) -> int: ...
    @mcu_trigger_frequency.setter
    def mcu_trigger_frequency(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    mode: OBSyncMode
    @property
    def rgb_trigger_signal_delay(self) -> int: ...
    @rgb_trigger_signal_delay.setter
    def rgb_trigger_signal_delay(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @staticmethod
    def from_bytes(data: bytes) -> OBDeviceSyncConfig:
        """
        Decode an exact-size native packed SDK payload.
        """

    def __init__(self) -> None: ...
    def to_bytes(self) -> bytes:
        """
        Copy the native packed SDK layout.
        """

class OBDepthWorkModeTag:
    """
    Members:

      OB_DEVICE_DEPTH_WORK_MODE

      OB_CUSTOM_DEPTH_WORK_MODE
    """

    OB_CUSTOM_DEPTH_WORK_MODE: typing.ClassVar[OBDepthWorkModeTag]
    OB_DEVICE_DEPTH_WORK_MODE: typing.ClassVar[OBDepthWorkModeTag]
    __members__: typing.ClassVar[dict[str, OBDepthWorkModeTag]]
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class OBDepthWorkMode:
    __hash__: typing.ClassVar[None] = None  # type: ignore[assignment]
    @property
    def checksum(self) -> numpy.typing.NDArray[numpy.uint8]: ...
    @checksum.setter
    def checksum(self, value: typing_extensions.Annotated[numpy.typing.ArrayLike, numpy.uint8]) -> None: ...
    name: str
    tag: OBDepthWorkModeTag
    @staticmethod
    def from_bytes(data: bytes) -> OBDepthWorkMode:
        """
        Decode an exact-size native packed SDK payload.
        """

    def __eq__(self, arg0: object) -> bool: ...
    def __init__(self) -> None: ...
    def __repr__(self) -> str: ...
    def to_bytes(self) -> bytes:
        """
        Copy the native packed SDK layout.
        """

class OBSequenceIdItem:
    name: str
    @property
    def sequence_select_id(self) -> int: ...
    @sequence_select_id.setter
    def sequence_select_id(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __init__(self) -> None: ...

class OBHoleFillingMode:
    """
    Members:

      TOP

      NEAREST

      FURTHEST
    """

    FURTHEST: typing.ClassVar[OBHoleFillingMode]
    NEAREST: typing.ClassVar[OBHoleFillingMode]
    TOP: typing.ClassVar[OBHoleFillingMode]
    __members__: typing.ClassVar[dict[str, OBHoleFillingMode]]
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class OBSpatialAdvancedFilterParams:
    @property
    def alpha(self) -> float: ...
    @alpha.setter
    def alpha(self, value: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def disp_diff(self) -> int: ...
    @disp_diff.setter
    def disp_diff(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def magnitude(self) -> int: ...
    @magnitude.setter
    def magnitude(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def radius(self) -> int: ...
    @radius.setter
    def radius(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __init__(self) -> None: ...
    def __repr__(self) -> str: ...

class OBSpatialFastFilterParams:
    @property
    def radius(self) -> int: ...
    @radius.setter
    def radius(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __init__(self) -> None: ...
    def __repr__(self) -> str: ...

class OBSpatialModerateFilterParams:
    @property
    def disp_diff(self) -> int: ...
    @disp_diff.setter
    def disp_diff(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def magnitude(self) -> int: ...
    @magnitude.setter
    def magnitude(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def radius(self) -> int: ...
    @radius.setter
    def radius(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __init__(self) -> None: ...
    def __repr__(self) -> str: ...

class OBEdgeNoiseRemovalType:
    """
    Members:

      MG_FILTER

      MGH_FILTER

      MGA_FILTER

      MGC_FILTER
    """

    MGA_FILTER: typing.ClassVar[OBEdgeNoiseRemovalType]
    MGC_FILTER: typing.ClassVar[OBEdgeNoiseRemovalType]
    MGH_FILTER: typing.ClassVar[OBEdgeNoiseRemovalType]
    MG_FILTER: typing.ClassVar[OBEdgeNoiseRemovalType]
    __members__: typing.ClassVar[dict[str, OBEdgeNoiseRemovalType]]
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class OBEdgeNoiseRemovalFilterParams:
    enable_direction: bool
    @property
    def height(self) -> int: ...
    @height.setter
    def height(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def limit_x_th(self) -> int: ...
    @limit_x_th.setter
    def limit_x_th(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def limit_y_th(self) -> int: ...
    @limit_y_th.setter
    def limit_y_th(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def margin_x_th(self) -> int: ...
    @margin_x_th.setter
    def margin_x_th(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def margin_y_th(self) -> int: ...
    @margin_y_th.setter
    def margin_y_th(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def width(self) -> int: ...
    @width.setter
    def width(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __init__(self) -> None: ...
    def __repr__(self) -> str: ...

class OBMgcNoiseRemovalFilterParams:
    @property
    def height(self) -> int: ...
    @height.setter
    def height(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def limit_x_th(self) -> int: ...
    @limit_x_th.setter
    def limit_x_th(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def limit_y_th(self) -> int: ...
    @limit_y_th.setter
    def limit_y_th(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def margin_x_th(self) -> int: ...
    @margin_x_th.setter
    def margin_x_th(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def margin_y_th(self) -> int: ...
    @margin_y_th.setter
    def margin_y_th(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def max_radius(self) -> int: ...
    @max_radius.setter
    def max_radius(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def max_width_left(self) -> int: ...
    @max_width_left.setter
    def max_width_left(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def max_width_right(self) -> int: ...
    @max_width_right.setter
    def max_width_right(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def width(self) -> int: ...
    @width.setter
    def width(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __init__(self) -> None: ...
    def __repr__(self) -> str: ...

class OBLutNoiseRemovalFilterParams:
    @property
    def height(self) -> int: ...
    @height.setter
    def height(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def max_lut(self) -> numpy.typing.NDArray[numpy.uint16]: ...
    @max_lut.setter
    def max_lut(self, value: typing_extensions.Annotated[numpy.typing.ArrayLike, numpy.uint16]) -> None: ...
    @property
    def min_diff(self) -> int: ...
    @min_diff.setter
    def min_diff(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def width(self) -> int: ...
    @width.setter
    def width(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __init__(self) -> None: ...
    def __repr__(self) -> str: ...

class OBDDONoiseRemovalType:
    """
    Members:

      LUT

      OVERALL
    """

    LUT: typing.ClassVar[OBDDONoiseRemovalType]
    OVERALL: typing.ClassVar[OBDDONoiseRemovalType]
    __members__: typing.ClassVar[dict[str, OBDDONoiseRemovalType]]
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class OBNoiseRemovalFilterParams:
    @property
    def disp_diff(self) -> int: ...
    @disp_diff.setter
    def disp_diff(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def max_size(self) -> int: ...
    @max_size.setter
    def max_size(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    type: OBDDONoiseRemovalType
    def __init__(self) -> None: ...

class OBDeviceIpAddrConfig:
    address: str
    @property
    def dhcp(self) -> int: ...
    @dhcp.setter
    def dhcp(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    gateway: str
    netmask: str
    @staticmethod
    def from_bytes(data: bytes) -> OBDeviceIpAddrConfig:
        """
        Decode an exact-size native packed SDK payload.
        """

    def __init__(self) -> None: ...
    def to_bytes(self) -> bytes:
        """
        Copy the native packed SDK layout.
        """

class OBNetIpConfigV2:
    address: str
    @property
    def flags(self) -> int: ...
    @flags.setter
    def flags(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    gateway: str
    netmask: str
    @staticmethod
    def from_bytes(data: bytes) -> OBNetIpConfigV2:
        """
        Decode an exact-size native packed SDK payload.
        """

    def __init__(self) -> None: ...
    def __repr__(self) -> str: ...
    def to_bytes(self) -> bytes:
        """
        Copy the native packed SDK layout.
        """

class OBCommunicationType:
    """
    Members:

      USB

      ETHERNET
    """

    ETHERNET: typing.ClassVar[OBCommunicationType]
    USB: typing.ClassVar[OBCommunicationType]
    __members__: typing.ClassVar[dict[str, OBCommunicationType]]
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
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

    OFF: typing.ClassVar[OBUSBPowerState]
    POWER_5V_0A9: typing.ClassVar[OBUSBPowerState]
    POWER_5V_1A5: typing.ClassVar[OBUSBPowerState]
    POWER_5V_3A0: typing.ClassVar[OBUSBPowerState]
    __members__: typing.ClassVar[dict[str, OBUSBPowerState]]
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
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

    OFF: typing.ClassVar[OBDCPowerState]
    ON: typing.ClassVar[OBDCPowerState]
    __members__: typing.ClassVar[dict[str, OBDCPowerState]]
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class OBRotateDegreeType:
    """
    Members:

      ROTATE_0

      ROTATE_90

      ROTATE_180

      ROTATE_270
    """

    ROTATE_0: typing.ClassVar[OBRotateDegreeType]
    ROTATE_180: typing.ClassVar[OBRotateDegreeType]
    ROTATE_270: typing.ClassVar[OBRotateDegreeType]
    ROTATE_90: typing.ClassVar[OBRotateDegreeType]
    __members__: typing.ClassVar[dict[str, OBRotateDegreeType]]
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class OBProtocolVersion:
    @property
    def major(self) -> int: ...
    @major.setter
    def major(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def minor(self) -> int: ...
    @minor.setter
    def minor(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def patch(self) -> int: ...
    @patch.setter
    def patch(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __init__(self) -> None: ...

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

    INVALID: typing.ClassVar[OBCmdVersion]
    NONE: typing.ClassVar[OBCmdVersion]
    V0: typing.ClassVar[OBCmdVersion]
    V1: typing.ClassVar[OBCmdVersion]
    V2: typing.ClassVar[OBCmdVersion]
    V3: typing.ClassVar[OBCmdVersion]
    __members__: typing.ClassVar[dict[str, OBCmdVersion]]
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
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

    ANY_SITUATION: typing.ClassVar[OBFrameAggregateOutputMode]
    COLOR_FRAME_REQUIRE: typing.ClassVar[OBFrameAggregateOutputMode]
    DISABLE: typing.ClassVar[OBFrameAggregateOutputMode]
    FULL_FRAME_REQUIRE: typing.ClassVar[OBFrameAggregateOutputMode]
    __members__: typing.ClassVar[dict[str, OBFrameAggregateOutputMode]]
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
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

    LEFT_HAND: typing.ClassVar[OBCoordinateSystemType]
    RIGHT_HAND: typing.ClassVar[OBCoordinateSystemType]
    __members__: typing.ClassVar[dict[str, OBCoordinateSystemType]]
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
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

    DEVELOPMENT: typing.ClassVar[OBDeviceDevelopmentMode]
    NORMAL: typing.ClassVar[OBDeviceDevelopmentMode]
    __members__: typing.ClassVar[dict[str, OBDeviceDevelopmentMode]]
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

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

      GROUP_ACTIONS
    """

    FREE_RUN: typing.ClassVar[OBMultiDeviceSyncMode]
    GROUP_ACTIONS: typing.ClassVar[OBMultiDeviceSyncMode]
    HARDWARE_TRIGGERING: typing.ClassVar[OBMultiDeviceSyncMode]
    IR_IMU_SYNC: typing.ClassVar[OBMultiDeviceSyncMode]
    PRIMARY: typing.ClassVar[OBMultiDeviceSyncMode]
    SECONDARY: typing.ClassVar[OBMultiDeviceSyncMode]
    SECONDARY_SYNCED: typing.ClassVar[OBMultiDeviceSyncMode]
    SOFTWARE_SYNCED: typing.ClassVar[OBMultiDeviceSyncMode]
    SOFTWARE_TRIGGERING: typing.ClassVar[OBMultiDeviceSyncMode]
    STANDALONE: typing.ClassVar[OBMultiDeviceSyncMode]
    __members__: typing.ClassVar[dict[str, OBMultiDeviceSyncMode]]
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class OBMultiDeviceSyncConfig:
    @property
    def color_delay_us(self) -> int: ...
    @color_delay_us.setter
    def color_delay_us(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def depth_delay_us(self) -> int: ...
    @depth_delay_us.setter
    def depth_delay_us(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def frames_per_trigger(self) -> int: ...
    @frames_per_trigger.setter
    def frames_per_trigger(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    mode: OBMultiDeviceSyncMode
    @property
    def trigger_out_delay_us(self) -> int: ...
    @trigger_out_delay_us.setter
    def trigger_out_delay_us(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    trigger_out_enable: bool
    @property
    def trigger_to_image_delay_us(self) -> int: ...
    @trigger_to_image_delay_us.setter
    def trigger_to_image_delay_us(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @staticmethod
    def from_bytes(data: bytes) -> OBMultiDeviceSyncConfig:
        """
        Decode an exact-size native packed SDK payload.
        """

    def __init__(self) -> None: ...
    def to_bytes(self) -> bytes:
        """
        Copy the native packed SDK layout.
        """

class OBDeviceTimestampResetConfig:
    enable: bool
    @property
    def timestamp_reset_delay_us(self) -> int: ...
    @timestamp_reset_delay_us.setter
    def timestamp_reset_delay_us(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    timestamp_reset_signal_output_enable: bool
    def __init__(self) -> None: ...

class OBBaselineCalibrationParam:
    @property
    def baseline(self) -> float: ...
    @baseline.setter
    def baseline(self, value: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def zpd(self) -> float: ...
    @zpd.setter
    def zpd(self, value: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @staticmethod
    def from_bytes(data: bytes) -> OBBaselineCalibrationParam:
        """
        Decode an exact-size native packed SDK payload.
        """

    def __init__(self) -> None: ...
    def to_bytes(self) -> bytes:
        """
        Copy the native packed SDK layout.
        """

class OBDeviceSerialNumber:
    @staticmethod
    def from_bytes(data: bytes) -> OBDeviceSerialNumber:
        """
        Decode an exact-size native packed SDK payload.
        """

    def __init__(self) -> None: ...
    def to_bytes(self) -> bytes:
        """
        Copy the native packed SDK layout.
        """

    @property
    def number_str(self) -> str:
        """
        SDK numberStr field; at most 16 UTF-8 bytes, without embedded NUL.
        """

    @number_str.setter
    def number_str(self, arg1: str) -> None: ...

class OBDispOffsetConfig:
    @property
    def enable(self) -> int: ...
    @enable.setter
    def enable(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def offset0(self) -> int: ...
    @offset0.setter
    def offset0(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def offset1(self) -> int: ...
    @offset1.setter
    def offset1(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def reserved(self) -> int: ...
    @reserved.setter
    def reserved(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @staticmethod
    def from_bytes(data: bytes) -> OBDispOffsetConfig:
        """
        Decode an exact-size native packed SDK payload.
        """

    def __init__(self) -> None: ...
    def to_bytes(self) -> bytes:
        """
        Copy the native packed SDK layout.
        """

class OBAwbGainParams:
    @property
    def b_gain(self) -> int: ...
    @b_gain.setter
    def b_gain(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def g_gain(self) -> int: ...
    @g_gain.setter
    def g_gain(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def r_gain(self) -> int: ...
    @r_gain.setter
    def r_gain(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @staticmethod
    def from_bytes(data: bytes) -> OBAwbGainParams:
        """
        Decode an exact-size native packed SDK payload.
        """

    def __init__(self) -> None: ...
    def to_bytes(self) -> bytes:
        """
        Copy the native packed SDK layout.
        """

class OBHdrConfig:
    @property
    def enable(self) -> int: ...
    @enable.setter
    def enable(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def exposure_1(self) -> int: ...
    @exposure_1.setter
    def exposure_1(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def exposure_2(self) -> int: ...
    @exposure_2.setter
    def exposure_2(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def gain_1(self) -> int: ...
    @gain_1.setter
    def gain_1(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def gain_2(self) -> int: ...
    @gain_2.setter
    def gain_2(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def sequence_name(self) -> int: ...
    @sequence_name.setter
    def sequence_name(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @staticmethod
    def from_bytes(data: bytes) -> OBHdrConfig:
        """
        Decode an exact-size native packed SDK payload.
        """

    def __init__(self) -> None: ...
    def to_bytes(self) -> bytes:
        """
        Copy the native packed SDK layout.
        """

class OBRegionOfInterest:
    @property
    def x0_left(self) -> int: ...
    @x0_left.setter
    def x0_left(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def x1_right(self) -> int: ...
    @x1_right.setter
    def x1_right(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def y0_top(self) -> int: ...
    @y0_top.setter
    def y0_top(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def y1_bottom(self) -> int: ...
    @y1_bottom.setter
    def y1_bottom(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @staticmethod
    def from_bytes(data: bytes) -> OBRegionOfInterest:
        """
        Decode an exact-size native packed SDK payload.
        """

    def __init__(self) -> None: ...
    def to_bytes(self) -> bytes:
        """
        Copy the native packed SDK layout.
        """

class OBFilterConfigValueType:
    """
    Members:

      INVALID

      INT

      FLOAT

      BOOLEAN
    """

    BOOLEAN: typing.ClassVar[OBFilterConfigValueType]
    FLOAT: typing.ClassVar[OBFilterConfigValueType]
    INT: typing.ClassVar[OBFilterConfigValueType]
    INVALID: typing.ClassVar[OBFilterConfigValueType]
    __members__: typing.ClassVar[dict[str, OBFilterConfigValueType]]
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class OBFilterConfigSchemaItem:
    @property
    def default(self) -> float: ...
    @default.setter
    def default(self, value: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def max(self) -> float: ...
    @max.setter
    def max(self, value: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def min(self) -> float: ...
    @min.setter
    def min(self, value: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def step(self) -> float: ...
    @step.setter
    def step(self, value: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    type: OBFilterConfigValueType
    def __init__(self) -> None: ...
    @property
    def desc(self) -> str: ...
    @property
    def name(self) -> str: ...

class OBHardwareDecimationConfig:
    @property
    def factor(self) -> int: ...
    @factor.setter
    def factor(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def origin_height(self) -> int: ...
    @origin_height.setter
    def origin_height(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def origin_width(self) -> int: ...
    @origin_width.setter
    def origin_width(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __init__(self) -> None: ...

class OBPlaybackStatus:
    """
    Members:

      UNKNOWN

      PLAYING

      PAUSED

      STOPPED

      COUNT
    """

    COUNT: typing.ClassVar[OBPlaybackStatus]
    PAUSED: typing.ClassVar[OBPlaybackStatus]
    PLAYING: typing.ClassVar[OBPlaybackStatus]
    STOPPED: typing.ClassVar[OBPlaybackStatus]
    UNKNOWN: typing.ClassVar[OBPlaybackStatus]
    __members__: typing.ClassVar[dict[str, OBPlaybackStatus]]
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
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

    ACTUAL_FRAME_RATE: typing.ClassVar[OBFrameMetadataType]
    AE_ROI_BOTTOM: typing.ClassVar[OBFrameMetadataType]
    AE_ROI_LEFT: typing.ClassVar[OBFrameMetadataType]
    AE_ROI_RIGHT: typing.ClassVar[OBFrameMetadataType]
    AE_ROI_TOP: typing.ClassVar[OBFrameMetadataType]
    AUTO_EXPOSURE: typing.ClassVar[OBFrameMetadataType]
    AUTO_WHITE_BALANCE: typing.ClassVar[OBFrameMetadataType]
    BACKLIGHT_COMPENSATION: typing.ClassVar[OBFrameMetadataType]
    BRIGHTNESS: typing.ClassVar[OBFrameMetadataType]
    CONTRAST: typing.ClassVar[OBFrameMetadataType]
    COUNT: typing.ClassVar[OBFrameMetadataType]
    DISPARITY_SEARCH_OFFSET: typing.ClassVar[OBFrameMetadataType]
    DISPARITY_SEARCH_RANGE: typing.ClassVar[OBFrameMetadataType]
    EXPOSURE: typing.ClassVar[OBFrameMetadataType]
    EXPOSURE_PRIORITY: typing.ClassVar[OBFrameMetadataType]
    FRAME_NUMBER: typing.ClassVar[OBFrameMetadataType]
    FRAME_RATE: typing.ClassVar[OBFrameMetadataType]
    GAIN: typing.ClassVar[OBFrameMetadataType]
    GAMMA: typing.ClassVar[OBFrameMetadataType]
    GPIO_INPUT_DATA: typing.ClassVar[OBFrameMetadataType]
    HDR_SEQUENCE_INDEX: typing.ClassVar[OBFrameMetadataType]
    HDR_SEQUENCE_NAME: typing.ClassVar[OBFrameMetadataType]
    HDR_SEQUENCE_SIZE: typing.ClassVar[OBFrameMetadataType]
    HUE: typing.ClassVar[OBFrameMetadataType]
    LASER_POWER: typing.ClassVar[OBFrameMetadataType]
    LASER_POWER_LEVEL: typing.ClassVar[OBFrameMetadataType]
    LASER_STATUS: typing.ClassVar[OBFrameMetadataType]
    LOW_LIGHT_COMPENSATION: typing.ClassVar[OBFrameMetadataType]
    MANUAL_WHITE_BALANCE: typing.ClassVar[OBFrameMetadataType]
    POWER_LINE_FREQUENCY: typing.ClassVar[OBFrameMetadataType]
    SATURATION: typing.ClassVar[OBFrameMetadataType]
    SENSOR_TIMESTAMP: typing.ClassVar[OBFrameMetadataType]
    SHARPNESS: typing.ClassVar[OBFrameMetadataType]
    TIMESTAMP: typing.ClassVar[OBFrameMetadataType]
    WHITE_BALANCE: typing.ClassVar[OBFrameMetadataType]
    __members__: typing.ClassVar[dict[str, OBFrameMetadataType]]
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class OBPoint2f:
    @property
    def x(self) -> float: ...
    @x.setter
    def x(self, value: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @property
    def y(self) -> float: ...
    @y.setter
    def y(self, value: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(
        self, arg0: typing.SupportsFloat | typing.SupportsIndex, arg1: typing.SupportsFloat | typing.SupportsIndex
    ) -> None: ...
    def __repr__(self) -> str: ...

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

class OBDeviceAccessMode:
    """
    Members:

      OB_DEVICE_ACCESS_DENIED

      OB_DEVICE_EXCLUSIVE_ACCESS

      OB_DEVICE_CONTROL_ACCESS

      OB_DEVICE_MONITOR_ACCESS

      OB_DEVICE_DEFAULT_ACCESS
    """

    OB_DEVICE_ACCESS_DENIED: typing.ClassVar[OBDeviceAccessMode]
    OB_DEVICE_CONTROL_ACCESS: typing.ClassVar[OBDeviceAccessMode]
    OB_DEVICE_DEFAULT_ACCESS: typing.ClassVar[OBDeviceAccessMode]
    OB_DEVICE_EXCLUSIVE_ACCESS: typing.ClassVar[OBDeviceAccessMode]
    OB_DEVICE_MONITOR_ACCESS: typing.ClassVar[OBDeviceAccessMode]
    __members__: typing.ClassVar[dict[str, OBDeviceAccessMode]]
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class OBDeviceAccessState:
    """
    Members:

      OB_DEVICE_ACCESS_STATE_UNKNOWN : The access state cannot be determined

      OB_DEVICE_ACCESS_STATE_UNSUPPORTED : The device or current build does not support access-state query

      OB_DEVICE_ACCESS_STATE_AVAILABLE : The device is available for control access

      OB_DEVICE_ACCESS_STATE_CONTROLLED : The device has a controller; monitor access may still be available

      OB_DEVICE_ACCESS_STATE_EXCLUSIVE : The device is held exclusively and cannot be accessed

      OB_DEVICE_ACCESS_STATE_UNREACHABLE : The device did not respond or the network path is unreachable

      OB_DEVICE_ACCESS_STATE_FW_NOT_SUPPORTED : The device supports CCP, but the firmware version is too old
    """

    OB_DEVICE_ACCESS_STATE_AVAILABLE: typing.ClassVar[OBDeviceAccessState]
    OB_DEVICE_ACCESS_STATE_CONTROLLED: typing.ClassVar[OBDeviceAccessState]
    OB_DEVICE_ACCESS_STATE_EXCLUSIVE: typing.ClassVar[OBDeviceAccessState]
    OB_DEVICE_ACCESS_STATE_FW_NOT_SUPPORTED: typing.ClassVar[OBDeviceAccessState]
    OB_DEVICE_ACCESS_STATE_UNKNOWN: typing.ClassVar[OBDeviceAccessState]
    OB_DEVICE_ACCESS_STATE_UNREACHABLE: typing.ClassVar[OBDeviceAccessState]
    OB_DEVICE_ACCESS_STATE_UNSUPPORTED: typing.ClassVar[OBDeviceAccessState]
    __members__: typing.ClassVar[dict[str, OBDeviceAccessState]]
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class OBIpSourceType:
    """
    Members:

      NONE

      LLA

      DHCP

      PERSISTENT
    """

    DHCP: typing.ClassVar[OBIpSourceType]
    LLA: typing.ClassVar[OBIpSourceType]
    NONE: typing.ClassVar[OBIpSourceType]
    PERSISTENT: typing.ClassVar[OBIpSourceType]
    __members__: typing.ClassVar[dict[str, OBIpSourceType]]
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class OBClockType:
    """
    Members:

      REALTIME

      MONOTONIC
    """

    MONOTONIC: typing.ClassVar[OBClockType]
    REALTIME: typing.ClassVar[OBClockType]
    __members__: typing.ClassVar[dict[str, OBClockType]]
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
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

    B: typing.ClassVar[OBGvcpPortScheme]
    STANDARD: typing.ClassVar[OBGvcpPortScheme]
    __members__: typing.ClassVar[dict[str, OBGvcpPortScheme]]
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
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

    DRIVER: typing.ClassVar[OBPipelineIssue]
    FW: typing.ClassVar[OBPipelineIssue]
    HW: typing.ClassVar[OBPipelineIssue]
    NONE: typing.ClassVar[OBPipelineIssue]
    SDK: typing.ClassVar[OBPipelineIssue]
    __members__: typing.ClassVar[dict[str, OBPipelineIssue]]
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class OBPipelineStatus:
    @property
    def dev_status(self) -> int: ...
    @dev_status.setter
    def dev_status(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @property
    def drv_status(self) -> int: ...
    @drv_status.setter
    def drv_status(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    issue: OBPipelineIssue
    @property
    def sdk_status(self) -> int: ...
    @sdk_status.setter
    def sdk_status(self, value: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def __init__(self) -> None: ...
    def __repr__(self) -> str: ...

class OBCameraPerformanceMode:
    """
    Members:

      ADAPTIVE

      HIGH
    """

    ADAPTIVE: typing.ClassVar[OBCameraPerformanceMode]
    HIGH: typing.ClassVar[OBCameraPerformanceMode]
    __members__: typing.ClassVar[dict[str, OBCameraPerformanceMode]]
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class OBColorPreset:
    """
    Members:

      DEFAULT

      WARM_BIASED_AWB
    """

    DEFAULT: typing.ClassVar[OBColorPreset]
    WARM_BIASED_AWB: typing.ClassVar[OBColorPreset]
    __members__: typing.ClassVar[dict[str, OBColorPreset]]
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class OBUvcBackendType:
    """
    Members:

      AUTO

      LIBUVC

      V4L2

      MSMF
    """

    AUTO: typing.ClassVar[OBUvcBackendType]
    LIBUVC: typing.ClassVar[OBUvcBackendType]
    MSMF: typing.ClassVar[OBUvcBackendType]
    V4L2: typing.ClassVar[OBUvcBackendType]
    __members__: typing.ClassVar[dict[str, OBUvcBackendType]]
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class OBIntraCameraSyncReference:
    """
    Members:

      START_OF_EXPOSURE

      MIDDLE_OF_EXPOSURE

      END_OF_EXPOSURE
    """

    END_OF_EXPOSURE: typing.ClassVar[OBIntraCameraSyncReference]
    MIDDLE_OF_EXPOSURE: typing.ClassVar[OBIntraCameraSyncReference]
    START_OF_EXPOSURE: typing.ClassVar[OBIntraCameraSyncReference]
    __members__: typing.ClassVar[dict[str, OBIntraCameraSyncReference]]
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

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
    def is_lidar_stream_profile(self) -> bool: ...
    def is_video_stream_profile(self) -> bool: ...

class VideoStreamProfile(StreamProfile):
    def __repr__(self) -> str: ...
    def get_decimation_config(self) -> OBHardwareDecimationConfig: ...
    def get_distortion(self) -> OBCameraDistortion: ...
    def get_fps(self) -> int: ...
    def get_height(self) -> int: ...
    def get_intrinsic(self) -> OBCameraIntrinsic: ...
    def get_width(self) -> int: ...
    def set_distortion(self, arg0: OBCameraDistortion) -> None: ...
    def set_intrinsic(self, arg0: OBCameraIntrinsic) -> None: ...

class AccelStreamProfile(StreamProfile):
    def __repr__(self) -> str: ...
    def get_full_scale_range(self) -> OBAccelFullScaleRange: ...
    def get_intrinsic(self) -> OBAccelIntrinsic: ...
    def get_sample_rate(self) -> OBGyroSampleRate: ...

class GyroStreamProfile(StreamProfile):
    def __repr__(self) -> str: ...
    def get_full_scale_range(self) -> OBGyroFullScaleRange: ...
    def get_intrinsic(self) -> OBGyroIntrinsic: ...
    def get_sample_rate(self) -> OBGyroSampleRate: ...

class LiDARStreamProfile(StreamProfile):
    def get_scan_rate(self) -> OBLiDARScanRate: ...

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

class Sensor:
    def __repr__(self) -> str: ...
    def get_recommended_filters(self) -> list[Filter]: ...
    def get_stream_profile_list(self) -> StreamProfileList: ...
    def get_type(self) -> OBSensorType: ...
    def start(self, arg0: StreamProfile, arg1: typing.Callable) -> None: ...
    def stop(self) -> None: ...
    def switch_profile(self, arg0: StreamProfile) -> None: ...

class SensorList:
    def __getitem__(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> Sensor: ...
    def __len__(self) -> int: ...
    def get_count(self) -> int: ...
    def get_sensor_by_index(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> Sensor: ...
    def get_sensor_by_type(self, arg0: OBSensorType) -> Sensor: ...
    def get_type_by_index(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> OBSensorType: ...

class DeviceInfo:
    def __repr__(self) -> str: ...
    def get_asic_name(self) -> str:
        """
        Get the ASIC name of the device
        """

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

class DevicePresetList:
    def __contains__(self, arg0: str) -> bool: ...
    def __getitem__(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> str: ...
    def __len__(self) -> int: ...
    def get_count(self) -> int: ...
    def get_depth_work_mode_version(self, index: typing.SupportsInt | typing.SupportsIndex) -> str:
        """
        Get the depth work mode version of the preset at the specified index, e.g. "1.2.3". Empty string when the device does not support versioned modes
        """

    def get_name_by_index(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> str: ...
    def has_preset(self, arg0: str) -> bool: ...

class ColorPresetList:
    def __getitem__(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> str: ...
    def __len__(self) -> int: ...
    def get_count(self) -> int: ...
    def get_name_by_index(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> str: ...

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

class Device:
    __hash__: typing.ClassVar[None] = None  # type: ignore[assignment]
    def __eq__(self, arg0: object) -> bool: ...
    def clear_license_info(self) -> None:
        """
        Clear license information stored on the device
        """

    def enable_firmware_log(self, arg0: bool) -> None:
        """
        Enable or disable the device firmware log
        """

    def enable_global_timestamp(self, enable: bool) -> None:
        """
        Enable or disable global timestamp
        """

    def enable_heart_beat(self, arg0: bool) -> None: ...
    def export_settings_as_preset_json_data(self, preset_name: str) -> bytes:
        """
        Export current device settings as a preset JSON data blob
        """

    def export_settings_as_preset_json_file(self, arg0: str) -> None: ...
    def get_available_frame_interleave_list(self) -> DeviceFrameInterleaveList:
        """
        Get the list of available frame interleave modes
        """

    def get_available_preset_list(self) -> DevicePresetList: ...
    def get_available_preset_resolution_config_list(self) -> PresetResolutionConfigList: ...
    def get_baseline(self) -> OBBaselineCalibrationParam: ...
    def get_bool_property(self, arg0: OBPropertyID) -> bool: ...
    def get_bool_property_range(self, arg0: OBPropertyID) -> OBBoolPropertyRange: ...
    def get_calibration_camera_param_list(self) -> CameraParamList: ...
    def get_color_preset_list(self) -> ColorPresetList: ...
    def get_current_color_preset_name(self) -> str: ...
    def get_current_depth_mode_name(self) -> str:
        """
        Get the current depth work mode name
        """

    def get_current_frame_interleave_name(self) -> str:
        """
        Get current frame interleave name
        """

    def get_current_preset_depth_work_mode_version(self) -> str:
        """
        Get the version of the current depth work mode, e.g. "1.2.3". Empty string when the device does not support versioned modes
        """

    def get_current_preset_name(self) -> str: ...
    def get_depth_work_mode(self) -> OBDepthWorkMode: ...
    def get_depth_work_mode_list(self) -> OBDepthWorkModeList: ...
    def get_device_info(self) -> DeviceInfo: ...
    def get_device_state(self) -> int: ...
    def get_extension_info(self, info_key: str) -> str:
        """
        Get extension info by key
        """

    def get_float_property(self, arg0: OBPropertyID) -> float: ...
    def get_float_property_range(self, arg0: OBPropertyID) -> OBFloatPropertyRange: ...
    def get_hdr_config(self) -> OBHdrConfig:
        """
        Read the fixed-size HDR configuration as OBHdrConfig.
        """

    def get_int_property(self, arg0: OBPropertyID) -> int: ...
    def get_int_property_range(self, arg0: OBPropertyID) -> OBIntPropertyRange: ...
    def get_monitor_poll_interval(self) -> int:
        """
        Get the device monitor polling interval in milliseconds
        """

    def get_multi_device_sync_config(self) -> OBMultiDeviceSyncConfig: ...
    def get_sensor(self, arg0: OBSensorType) -> Sensor: ...
    def get_sensor_list(self) -> SensorList: ...
    def get_structured_data(self, property_id: OBPropertyID) -> bytes:
        """
        Read bytes for a property with a known SDK layout. Sync config and depth work mode use public SDK structs via dedicated SDK methods. Unknown or variable-size layouts raise ValueError before SDK access; unsupported/unreadable device properties raise OBError.
        """

    def get_support_property_count(self) -> int: ...
    def get_supported_multi_device_sync_mode_bitmap(self) -> int:
        """
        Get the supported multi-device sync mode bitmap
        """

    def get_supported_property(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> OBPropertyItem: ...
    def get_temperature(self) -> OBDeviceTemperature: ...
    def get_timestamp_reset_config(self) -> OBDeviceTimestampResetConfig: ...
    def isFrameInterleaveSupported(self) -> bool: ...
    def is_color_preset_supported(self) -> bool: ...
    def is_extension_info_exist(self, info_key: str) -> bool:
        """
        Check if extension info exists
        """

    def is_firmware_log_enabled(self) -> bool:
        """
        Check whether the device firmware log is enabled
        """

    def is_global_timestamp_supported(self) -> bool:
        """
        Check if global timestamp is supported
        """

    def is_license_authorization_supported(self) -> bool:
        """
        Check whether the device supports license authorization
        """

    def is_property_supported(self, arg0: OBPropertyID, arg1: OBPermissionType) -> bool: ...
    def loadFrameInterleave(self, arg0: str) -> None: ...
    def load_depth_filter_config(self, arg0: str) -> None: ...
    @typing.overload
    def load_preset(self, preset_name: str) -> None: ...
    @typing.overload
    def load_preset(self, preset_name: str, version: str) -> None:
        """
        Load the preset by preset name and the target depth work mode version, e.g. "1.2.3"
        """

    def load_preset_from_json_data(self, arg0: str, arg1: str) -> None: ...
    def load_preset_from_json_file(self, arg0: str) -> None: ...
    def read_customer_data(self) -> bytes: ...
    def read_license_info(self) -> str:
        """
        Read signed device license information as SDK license_info JSON string
        """

    @typing.overload
    def reboot(self) -> None: ...
    @typing.overload
    def reboot(self, delay_ms: typing.SupportsInt | typing.SupportsIndex = 0) -> None:
        """
        Reboot the device with optional delay
        """

    def send_and_receive_data(self, data: bytes, receive_capacity: typing.SupportsInt | typing.SupportsIndex) -> bytes:
        """
        Send SDK protocol bytes and return the actual response bytes.
        """

    def set_bool_property(self, arg0: OBPropertyID, arg1: bool) -> None: ...
    @typing.overload
    def set_depth_work_mode(self, arg0: OBDepthWorkMode) -> OBStatus: ...
    @typing.overload
    def set_depth_work_mode(self, arg0: str) -> OBStatus: ...
    def set_device_state_changed_callback(self, arg0: typing.Callable) -> None: ...
    def set_float_property(self, arg0: OBPropertyID, arg1: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    def set_hdr_config(self, arg0: OBHdrConfig) -> None: ...
    def set_int_property(self, arg0: OBPropertyID, arg1: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    @typing.overload
    def set_ip_config(self, arg0: OBNetIpConfigV2) -> None: ...
    @typing.overload
    def set_ip_config(self, arg0: OBDeviceIpAddrConfig) -> None: ...
    def set_monitor_poll_interval(self, interval_ms: typing.SupportsInt | typing.SupportsIndex) -> None:
        """
        Set the device monitor polling interval for heartbeat and firmware log retrieval, in milliseconds (valid range [1000, 10000], values outside are clamped)
        """

    def set_multi_device_sync_config(self, arg0: OBMultiDeviceSyncConfig) -> None: ...
    def set_preset_resolution_config(self, arg0: OBPresetResolutionConfig) -> None: ...
    def set_structured_data(self, property_id: OBPropertyID, data: bytes) -> None:
        """
        Set a structured property from non-empty bytes in the SDK's native struct layout. The byte length is inferred; property/type matching and serialization are the caller's responsibility.
        """

    def set_timestamp_reset_config(self, arg0: OBDeviceTimestampResetConfig) -> None: ...
    def switch_color_preset(self, arg0: str) -> None: ...
    def sync_hardware_pps_time(self, hardware_pps_time: typing.SupportsInt | typing.SupportsIndex) -> bool:
        """
        Synchronize the device time (synchronize hardwarePPS time to device)
        """

    def timer_reset(self) -> None: ...
    def timer_sync_with_host(self) -> None: ...
    def timestamp_reset(self) -> None: ...
    def trigger_capture(self) -> None: ...
    def update_firmware(self, file_path: str, callback: typing.Callable, async_update: bool = True) -> None: ...
    def update_firmware_from_data(
        self, data: bytes, callback: typing.Callable[[OBUpgradeState, str, int], None], async_update: bool = True
    ) -> None:
        """
        Update from firmware bytes. Keep Device alive until completion. Callback exceptions are reported via sys.unraisablehook.
        """

    def update_optional_depth_presets(self, file_path_list: list, callback: typing.Callable) -> None: ...
    def update_optional_depth_presets_from_data(self, data_list: list, callback: typing.Callable) -> None:
        """
        Update the device optional depth presets from preset data blocks loaded in memory (a list of bytes objects)
        """

    def write_customer_data(self, data: bytes) -> None: ...
    def write_license_info(self, license_info: str) -> None:
        """
        Write signed device license information (SDK license_info JSON string)
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

    def query_device_access_state(self, index: typing.SupportsInt | typing.SupportsIndex) -> OBDeviceAccessState:
        """
        Query the current device access state (GVCP CCP) without opening the device. Blocks on the network; prefer calling off the UI thread
        """

    def query_device_access_state_by_serial_number(self, serial_number: str) -> OBDeviceAccessState:
        """
        Query the current device access state (GVCP CCP) by serial number without opening the device. Blocks on the network; prefer calling off the UI thread
        """

class DeviceFrameInterleaveList:
    def __getitem__(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> str: ...
    def __len__(self) -> int: ...
    def get_count(self) -> int: ...
    def get_name(self, index: typing.SupportsInt | typing.SupportsIndex) -> str: ...
    def has_frame_interleave(self, name: str) -> bool: ...

class ApplicationSensorConfig:
    def __init__(self, sensor_type: OBSensorType) -> None: ...
    def enable_stream(self, enabled: bool) -> None:
        """
        Enable or disable the stream
        """

    def enable_undistortion(self, enabled: bool) -> None:
        """
        Enable or disable undistortion
        """

    def is_stream_enabled(self) -> bool:
        """
        Check if the stream is enabled
        """

    def is_undistortion_enabled(self) -> bool:
        """
        Check if undistortion is enabled
        """

    def sensor_type(self) -> OBSensorType:
        """
        Get the sensor type
        """

    def set_stream_profile(self, profile: StreamProfile) -> None:
        """
        Set the stream profile
        """

    def stream_profile(self) -> typing.Optional[StreamProfile]:
        """
        Get the stream profile
        """

class ApplicationPointCloudConfig:
    def __init__(self) -> None: ...
    def align_mode(self) -> OBAlignMode:
        """
        Get the align mode
        """

    def decimation_factor(self) -> int:
        """
        Get the point cloud decimation factor
        """

    def enable(self, enabled: bool) -> None:
        """
        Enable or disable point cloud output
        """

    def enable_frame_sync(self, enabled: bool) -> None:
        """
        Enable or disable frame sync
        """

    def enable_match_target_resolution(self, enabled: bool) -> None:
        """
        Enable or disable match target resolution
        """

    def format(self) -> OBFormat:
        """
        Get the point cloud output format
        """

    def is_all_frame_type_required(self) -> bool:
        """
        Check if all frame types are required
        """

    def is_enabled(self) -> bool:
        """
        Check if point cloud is enabled
        """

    def is_frame_sync_enabled(self) -> bool:
        """
        Check if frame sync is enabled
        """

    def is_match_target_resolution_enabled(self) -> bool:
        """
        Check if match target resolution is enabled
        """

    def set_align_mode(self, mode: OBAlignMode) -> None:
        """
        Set the align mode
        """

    def set_all_frame_type_required(self, enabled: bool) -> None:
        """
        Set whether all frame types are required
        """

    def set_decimation_factor(self, factor: typing.SupportsInt | typing.SupportsIndex) -> None:
        """
        Set the point cloud decimation factor
        """

    def set_format(self, format: OBFormat) -> None:
        """
        Set the point cloud output format
        """

class ApplicationHDRMergeConfig:
    def __init__(self) -> None: ...
    def enable(self, enabled: bool) -> None:
        """
        Enable or disable HDR merge
        """

    def enable_ir(self, enabled: bool) -> None:
        """
        Enable or disable IR for HDR merge
        """

    def is_enabled(self) -> bool:
        """
        Check if HDR merge is enabled
        """

    def is_ir_enabled(self) -> bool:
        """
        Check if IR is enabled for HDR merge
        """

class ApplicationDevDecimationConfig:
    def __init__(self) -> None: ...
    def enable(self, enabled: bool) -> None:
        """
        Enable or disable device-level decimation
        """

    def is_enabled(self) -> bool:
        """
        Check if device-level decimation is enabled
        """

    def preset_resolution_config(self) -> OBPresetResolutionConfig:
        """
        Get the preset resolution configuration
        """

    def set_preset_resolution_config(self, config: OBPresetResolutionConfig) -> None:
        """
        Set the preset resolution configuration
        """

class ApplicationConfig:
    @staticmethod
    def get(device: Device) -> ApplicationConfig:
        """
        Get the application runtime configuration cache for the device
        """

    @staticmethod
    def get_by_preset(device: Device, preset_name: str) -> typing.Optional[ApplicationConfig]:
        """
        Get the application config carried by an externally imported preset, by preset name. Returns None for built-in presets or presets that carry no application config
        """

    @staticmethod
    def is_supported(device: Device) -> bool:
        """
        Check whether the device supports application runtime configuration import/export
        """

    def device_decimation(self) -> ApplicationDevDecimationConfig:
        """
        Get the device decimation configuration
        """

    def hdr_merge(self) -> ApplicationHDRMergeConfig:
        """
        Get the HDR merge configuration
        """

    def point_cloud(self) -> ApplicationPointCloudConfig:
        """
        Get the point cloud configuration
        """

    def reset(self) -> None:
        """
        Reset the application configuration to default values
        """

    def sensors(self) -> list[ApplicationSensorConfig]:
        """
        Get the list of sensor configurations
        """

    def set_device_decimation(self, config: ApplicationDevDecimationConfig) -> None:
        """
        Set the device decimation configuration
        """

    def set_hdr_merge(self, config: ApplicationHDRMergeConfig) -> None:
        """
        Set the HDR merge configuration
        """

    def set_point_cloud(self, config: ApplicationPointCloudConfig) -> None:
        """
        Set the point cloud configuration
        """

    def set_sensor(self, sensor: ApplicationSensorConfig) -> None:
        """
        Set a single sensor configuration
        """

    def set_sensors(self, sensors: typing.Sequence[ApplicationSensorConfig]) -> None:
        """
        Set the list of sensor configurations
        """

class Frame:
    @staticmethod
    def create_frame(
        frame_type: OBFrameType, format: OBFormat, data_size: typing.SupportsInt | typing.SupportsIndex
    ) -> Frame:
        """
        Create a Frame object of a specific type with a given format and data size
        """

    @staticmethod
    def create_frame_from_other_frame(other_frame: Frame, should_copy_data: bool = True) -> Frame:
        """
        Clone a frame object from another frame, with optional data copy
        """

    @staticmethod
    def create_frame_from_stream_profile(profile: StreamProfile) -> Frame:
        """
        Create a frame from a stream profile
        """

    @staticmethod
    def create_frame_set() -> FrameSet:
        """
        Create a new empty FrameSet object
        """

    @staticmethod
    def create_video_frame(
        frame_type: OBFrameType,
        format: OBFormat,
        width: typing.SupportsInt | typing.SupportsIndex,
        height: typing.SupportsInt | typing.SupportsIndex,
        stride: typing.SupportsInt | typing.SupportsIndex = 0,
    ) -> VideoFrame:
        """
        Create a VideoFrame with a given format, width, height, and stride
        """

    @staticmethod
    def set_frame_device_timestamp_us(
        frame: Frame, device_timestamp_us: typing.SupportsInt | typing.SupportsIndex
    ) -> None:
        """
        Set the device timestamp of the frame in microseconds
        """

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
    def get_token(self) -> int:
        """
        Get the auth token carried by the frame
        """

    def get_type(self) -> OBFrameType: ...
    def has_metadata(self, arg0: OBFrameMetadataType) -> bool: ...
    def set_stream_profile(self, arg0: StreamProfile) -> None: ...
    def set_system_timestamp_us(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def set_token(self, token: typing.SupportsInt | typing.SupportsIndex) -> None:
        """
        Set the auth token carried by the frame
        """

    def update_data(self, arg0: typing_extensions.Buffer) -> None: ...
    def update_metadata(self, arg0: typing_extensions.Buffer) -> None: ...

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

class ColorFrame(VideoFrame):
    pass

class DepthFrame(VideoFrame):
    def get_depth_scale(self) -> float: ...
    def set_value_scale(self, arg0: typing.SupportsFloat | typing.SupportsIndex) -> None: ...

class IRFrame(VideoFrame):
    pass

class ConfidenceFrame(VideoFrame):
    pass

class PointsFrame(Frame):
    def get_height(self) -> int: ...
    def get_position_value_scale(self) -> float: ...
    def get_width(self) -> int: ...

class AccelFrame(Frame):
    def __repr__(self) -> str: ...
    def get_temperature(self) -> float: ...
    def get_value(self) -> OBAccelValue: ...
    def get_x(self) -> float: ...
    def get_y(self) -> float: ...
    def get_z(self) -> float: ...

class GyroFrame(Frame):
    def __repr__(self) -> str: ...
    def get_temperature(self) -> float: ...
    def get_value(self) -> OBAccelValue: ...
    def get_x(self) -> float: ...
    def get_y(self) -> float: ...
    def get_z(self) -> float: ...

class LiDARPointsFrame(Frame):
    pass

class FrameSet(Frame):
    def __getitem__(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> typing.Optional[Frame]: ...
    def __len__(self) -> int: ...
    def __repr__(self) -> str: ...
    def get_accel_frame(self) -> typing.Optional[AccelFrame]: ...
    def get_color_frame(self) -> typing.Optional[ColorFrame]: ...
    def get_confidence_frame(self) -> typing.Optional[ConfidenceFrame]: ...
    def get_count(self) -> int: ...
    def get_depth_frame(self) -> typing.Optional[DepthFrame]: ...
    def get_frame(self, arg0: OBFrameType) -> typing.Optional[Frame]: ...
    def get_frame_by_index(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> typing.Optional[Frame]: ...
    def get_frame_by_type(self, arg0: OBFrameType) -> typing.Optional[Frame]: ...
    def get_frame_count(self) -> int: ...
    def get_gyro_frame(self) -> typing.Optional[GyroFrame]: ...
    def get_ir_frame(self) -> typing.Optional[IRFrame]: ...
    def get_left_color_frame(self) -> typing.Optional[ColorFrame]: ...
    def get_left_ir_frame(self) -> typing.Optional[IRFrame]: ...
    def get_lidar_points_frame(self) -> typing.Optional[LiDARPointsFrame]: ...
    def get_points_frame(self) -> typing.Optional[PointsFrame]: ...
    def get_right_color_frame(self) -> typing.Optional[ColorFrame]: ...
    def get_right_ir_frame(self) -> typing.Optional[IRFrame]: ...
    def push_frame(self, arg0: Frame) -> None: ...

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
    def is_enhanced_depth_filter(self) -> bool: ...
    def is_false_positive_filter(self) -> bool: ...
    def is_format_converter(self) -> bool: ...
    def is_hdr_merge_filter(self) -> bool: ...
    def is_hole_filling_filter(self) -> bool: ...
    def is_lut_noise_removal_filter(self) -> bool: ...
    def is_mgc_noise_removal_filter(self) -> bool: ...
    def is_noise_removal_filter(self) -> bool: ...
    def is_point_cloud_filter(self) -> bool: ...
    def is_sequence_id_filter(self) -> bool: ...
    def is_spatial_advanced_filter(self) -> bool: ...
    def is_spatial_fast_filter(self) -> bool: ...
    def is_spatial_moderate_filter(self) -> bool: ...
    def is_temporal_filter(self) -> bool: ...
    def is_threshold_filter(self) -> bool: ...
    def is_undistortion_filter(self) -> bool: ...
    def process(self, arg0: Frame) -> typing.Optional[Frame]: ...
    def push_frame(self, arg0: Frame) -> None: ...
    def reset(self) -> None: ...
    def set_callback(self, arg0: typing.Callable) -> None: ...
    def set_config_value(self, arg0: str, arg1: typing.SupportsFloat | typing.SupportsIndex) -> None: ...

class PointCloudFilter(Filter):
    def __init__(self) -> None: ...
    def calculate(self, arg0: Frame) -> numpy.typing.NDArray[numpy.float32]: ...
    def get_decimation_factor_range(self) -> OBIntPropertyRange: ...
    def set_camera_param(self, arg0: OBCameraParam) -> None: ...
    def set_color_data_normalization(self, arg0: bool) -> None: ...
    def set_coordinate_data_scaled(self, arg0: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    def set_coordinate_system(self, arg0: OBCoordinateSystemType) -> None: ...
    def set_create_point_format(self, arg0: OBFormat) -> None: ...
    def set_decimation_factor(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def set_frame_align_state(self, arg0: bool) -> None: ...
    def set_position_data_scaled(self, arg0: typing.SupportsFloat | typing.SupportsIndex) -> None: ...

class FormatConvertFilter(Filter):
    def __init__(self) -> None: ...
    def set_format_convert_format(self, arg0: OBConvertFormat) -> None:
        """
        Set the format to convert to
        """

class HoleFillingFilter(Filter):
    def __init__(self) -> None: ...
    def get_filling_mode(self) -> OBHoleFillingMode: ...
    def set_filling_mode(self, arg0: OBHoleFillingMode) -> None:
        """
        Set the filling mode
        """

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

class DisparityTransform(Filter):
    def __init__(self, activationKey: str = "") -> None: ...

class HDRMergeFilter(Filter):
    def __init__(self) -> None: ...

class AlignFilter(Filter):
    def __init__(self, align_to_stream: OBStreamType) -> None: ...
    def get_align_to_stream_type(self) -> OBStreamType: ...
    def set_align_to_stream_profile(self, arg0: StreamProfile) -> None: ...
    def set_match_target_resolution(self, arg0: bool) -> None: ...

class ThresholdFilter(Filter):
    def __init__(self) -> None: ...
    def get_max_range(self) -> OBIntPropertyRange: ...
    def get_min_range(self) -> OBIntPropertyRange: ...
    def set_value_range(
        self, arg0: typing.SupportsInt | typing.SupportsIndex, arg1: typing.SupportsInt | typing.SupportsIndex
    ) -> bool: ...

class SequenceIdFilter(Filter):
    def __init__(self) -> None: ...
    def get_select_sequence_id(self) -> int: ...
    def get_sequence_id_list(self) -> list: ...
    def get_sequence_id_list_size(self) -> int: ...
    def select_sequence_id(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...

class NoiseRemovalFilter(Filter):
    def __init__(self) -> None: ...
    def get_disp_diff_range(self) -> OBUint16PropertyRange: ...
    def get_filter_params(self) -> OBNoiseRemovalFilterParams: ...
    def get_max_size_range(self) -> OBUint16PropertyRange: ...
    def set_filter_params(self, arg0: OBNoiseRemovalFilterParams) -> None: ...

class DecimationFilter(Filter):
    def __init__(self) -> None: ...
    def get_scale_range(self) -> OBUint8PropertyRange: ...
    def get_scale_value(self) -> int: ...
    def set_scale_value(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...

class EdgeNoiseRemovalFilter(Filter):
    def __init__(self, activation_key: str = "") -> None: ...
    def get_filter_params(self) -> OBEdgeNoiseRemovalFilterParams: ...
    def get_height_range(self) -> OBUint16PropertyRange: ...
    def get_limit_x_th_range(self) -> OBUint16PropertyRange: ...
    def get_limit_y_th_range(self) -> OBUint16PropertyRange: ...
    def get_margin_x_th_range(self) -> OBUint16PropertyRange: ...
    def get_margin_y_th_range(self) -> OBUint16PropertyRange: ...
    def get_vertical_direction_enable_range(self) -> OBUint16PropertyRange: ...
    def get_width_range(self) -> OBUint16PropertyRange: ...
    def set_filter_params(self, arg0: OBEdgeNoiseRemovalFilterParams) -> None: ...

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

class LutNoiseRemovalFilter(Filter):
    def __init__(self, activation_key: str = "") -> None: ...
    def get_filter_params(self) -> OBLutNoiseRemovalFilterParams: ...
    def get_height_range(self) -> OBUint16PropertyRange: ...
    def get_max_lut_range(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> OBUint16PropertyRange: ...
    def get_min_diff_range(self) -> OBUint16PropertyRange: ...
    def get_width_range(self) -> OBUint16PropertyRange: ...
    def set_filter_params(self, arg0: OBLutNoiseRemovalFilterParams) -> None: ...

class UnDistortionFilter(Filter):
    def __init__(self, stream_type: OBStreamType = OBStreamType.COLOR_STREAM) -> None: ...
    def clear_new_camera_matrix(self) -> None: ...
    def get_stream_type(self) -> OBStreamType: ...
    def set_new_camera_matrix(self, arg0: OBCameraIntrinsic) -> None: ...
    def set_stream_type(self, arg0: OBStreamType) -> None: ...

class EnhancedDepthFilter(Filter):
    @staticmethod
    def get_supported_formats(stream_type: OBStreamType) -> list:
        """
        Get the list of supported frame formats for the given stream type (color: RGB; depth: Y10/Y11/Y12/Y14/Y16/Z16). Empty for unsupported stream types
        """

    @staticmethod
    def get_supported_resolutions() -> list:
        """
        Get the list of supported {width, height} pairs for the constrained (aligned-to) stream
        """

    @staticmethod
    def is_supported_format(stream_type: OBStreamType, format: OBFormat) -> bool:
        """
        Check whether a frame format is supported for the given stream type
        """

    @staticmethod
    def is_supported_resolution(
        source_stream_type: OBStreamType,
        align_to_stream_type: OBStreamType,
        width: typing.SupportsInt | typing.SupportsIndex,
        height: typing.SupportsInt | typing.SupportsIndex,
    ) -> bool:
        """
        Check whether a resolution is supported for the given stream alignment pair
        """

    def __init__(self, device: Device, model_path: str = "") -> None: ...
    def get_confidence_threshold_range(self) -> OBIntPropertyRange:
        """
        Get the property range of the confidence threshold
        """

    def get_current_height(self) -> int:
        """
        Get the current configured frame height
        """

    def get_current_width(self) -> int:
        """
        Get the current configured frame width
        """

    def set_confidence_threshold(self, value: typing.SupportsInt | typing.SupportsIndex) -> None:
        """
        Set the confidence threshold for depth values
        """

    def set_resolution(
        self, width: typing.SupportsInt | typing.SupportsIndex, height: typing.SupportsInt | typing.SupportsIndex
    ) -> None:
        """
        Set the working resolution of the enhanced depth filter
        """

class OBFilterList:
    def __getitem__(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> Filter: ...
    def __len__(self) -> int: ...
    def get_count(self) -> int: ...
    def get_filter(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> Filter: ...

class FilterFactory:
    @staticmethod
    def create_filter(name: str) -> Filter:
        """
        Create a filter by name
        """

    @staticmethod
    def create_private_filter(name: str, activation_key: str = "") -> Filter:
        """
        Create a private filter by name and activation key
        """

    @staticmethod
    def get_filter_vendor_specific_code(name: str) -> str:
        """
        Get the vendor specific code of a filter by name
        """

class SpatialFastFilter(Filter):
    def __init__(self, activation_key: str = "") -> None: ...
    def get_filter_params(self) -> OBSpatialFastFilterParams: ...
    def get_radius_range(self) -> OBIntPropertyRange: ...
    def set_filter_params(self, arg0: OBSpatialFastFilterParams) -> None: ...

class SpatialModerateFilter(Filter):
    def __init__(self, activation_key: str = "") -> None: ...
    def get_disp_diff_range(self) -> OBIntPropertyRange: ...
    def get_filter_params(self) -> OBSpatialModerateFilterParams: ...
    def get_magnitude_range(self) -> OBIntPropertyRange: ...
    def get_radius_range(self) -> OBIntPropertyRange: ...
    def set_filter_params(self, arg0: OBSpatialModerateFilterParams) -> None: ...

class FalsePositiveFilter(Filter):
    def __init__(self, activation_key: str = "") -> None: ...
    def get_fp_edge_bleed_filter_enable_range(self) -> OBUint8PropertyRange: ...
    def get_fp_pattern_ambiguity_filter_enable_range(self) -> OBUint8PropertyRange: ...
    def get_fp_texture_sparsity_filter_enable_range(self) -> OBUint8PropertyRange: ...
    def get_fpebf_min_bleed_length_range(self) -> OBUint16PropertyRange: ...
    def get_fpebf_roi_max_x_ratio_range(self) -> OBFloatPropertyRange: ...
    def get_fpebf_roi_max_y_ratio_range(self) -> OBFloatPropertyRange: ...
    def get_fpebf_roi_min_x_ratio_range(self) -> OBFloatPropertyRange: ...
    def get_fpebf_roi_min_y_ratio_range(self) -> OBFloatPropertyRange: ...
    def get_fppaf_max_height_ratio_range(self) -> OBFloatPropertyRange: ...
    def get_fppaf_max_noise_level_range(self) -> OBUint16PropertyRange: ...
    def get_fppaf_max_speckle_size_range(self) -> OBUint16PropertyRange: ...
    def get_fppaf_max_width_ratio_range(self) -> OBFloatPropertyRange: ...
    def get_fppaf_roi_max_x_ratio_range(self) -> OBFloatPropertyRange: ...
    def get_fppaf_roi_max_y_ratio_range(self) -> OBFloatPropertyRange: ...
    def get_fppaf_roi_min_x_ratio_range(self) -> OBFloatPropertyRange: ...
    def get_fppaf_roi_min_y_ratio_range(self) -> OBFloatPropertyRange: ...
    def get_fppaf_score_range(self) -> OBUint16PropertyRange: ...
    def get_fppaf_tolerance_range(self) -> OBFloatPropertyRange: ...
    def get_fptsf_max_noise_level_range(self) -> OBUint16PropertyRange: ...
    def get_fptsf_max_speckle_size_range(self) -> OBUint16PropertyRange: ...
    def get_fptsf_roi_max_x_ratio_range(self) -> OBFloatPropertyRange: ...
    def get_fptsf_roi_max_y_ratio_range(self) -> OBFloatPropertyRange: ...
    def get_fptsf_roi_min_x_ratio_range(self) -> OBFloatPropertyRange: ...
    def get_fptsf_roi_min_y_ratio_range(self) -> OBFloatPropertyRange: ...

class Context:
    @staticmethod
    def log_external_message(
        arg0: OBLogLevel, arg1: str, arg2: str, arg3: str, arg4: str, arg5: typing.SupportsInt | typing.SupportsIndex
    ) -> None: ...
    @staticmethod
    def set_extensions_directory(path: str) -> None:
        """
        Set the extensions directory for loading extension modules
        """

    @staticmethod
    def set_logger_file_name(arg0: str) -> None:
        """
        Set logger file name
        """

    @staticmethod
    def set_logger_level(arg0: OBLogLevel) -> None: ...
    @staticmethod
    def set_logger_to_callback(arg0: OBLogLevel, arg1: typing.Callable) -> None:
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
    def free_idle_memory(self) -> None:
        """
        Free idle memory from the internal frame memory pool
        """

    def get_gvcp_port_scheme(self) -> OBGvcpPortScheme:
        """
        Get the current GVCP port scheme
        """

    def get_timestamp_clock_type(self) -> OBClockType:
        """
        Get the current host-side timestamp clock type for the context
        """

    def ob_force_ip_config(self, arg0: str, arg1: OBDeviceIpAddrConfig) -> bool:
        """
        Change the IP configuration
        """

    def query_devices(self) -> DeviceList:
        """
        Query devices
        """

    def register_device_changed_callback(self, arg0: typing.Callable) -> int: ...
    def send_action_command(
        self,
        device_key: typing.SupportsInt | typing.SupportsIndex,
        group_key: typing.SupportsInt | typing.SupportsIndex,
        group_mask: typing.SupportsInt | typing.SupportsIndex,
        dest_ip: str = "255.255.255.255",
        scheduled_time: typing.SupportsInt | typing.SupportsIndex = 0,
    ) -> bool:
        """
        Send an Action Command to GVCP devices
        """

    def set_device_changed_callback(self, arg0: typing.Callable) -> None:
        """
        Set device changed callback, callback will be called when device changed
        """

    def set_gvcp_port_scheme(self, arg0: OBGvcpPortScheme) -> None:
        """
        Set the GVCP port scheme used for network device discovery and control
        """

    def set_timestamp_clock_type(self, clock_type: OBClockType) -> None:
        """
        Set the host-side timestamp clock type for the current context
        """

    def set_uvc_backend_type(self, type: OBUvcBackendType) -> None:
        """
        Set the UVC backend type (Linux only: LIBUVC or V4L2)
        """

    def sync_device_hardware_pps_time(self, hardware_pps_time: typing.SupportsInt | typing.SupportsIndex) -> None:
        """
        Synchronize the device time (synchronize hardwarePPS time to all created devices)
        """

    def unregister_device_changed_callback(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None: ...

class OBError(Exception):
    pass

class OBErrorDetails:
    def get_args(self) -> str: ...
    def get_name(self) -> str: ...
    def get_status(self) -> OBStatus: ...
    def get_type(self) -> OBException: ...
    def what(self) -> str: ...

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
        self, callback: typing.Callable, interval_ms: typing.SupportsInt | typing.SupportsIndex = 3000
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
    def start(self, arg0: Config, arg1: typing.Callable) -> None: ...
    @typing.overload
    def start(self) -> None: ...
    def stop(self) -> None: ...
    def wait_for_frames(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> typing.Optional[FrameSet]: ...

class OBPropertyID:
    """
    Members:

      OB_STRUCT_VERSION

      OB_STRUCT_GET_GYRO_PRESETS_ODR_LIST

      OB_STRUCT_GET_ACCEL_PRESETS_ODR_LIST

      OB_STRUCT_GET_GYRO_PRESETS_FULL_SCALE_LIST

      OB_STRUCT_GET_ACCEL_PRESETS_FULL_SCALE_LIST

      OB_STRUCT_DEVICE_ERROR_STATE

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

      OB_PROP_DEVICE_IP_MODE_INT : Device IP mode configuration (AMR/Industrial)

      OB_PROP_DHCP_ASSIGN_IP_TIMEOUT_INT : DHCP assign IP timeout, unit: second

      OB_PROP_USB_SYNC_VOLTAGE_LEVEL_INT : USB sync I/O voltage level

      OB_PROP_CURRENT_DISP_SEARCH_RANGE_MODE_INT : Get the current disparity search range mode value (read only)

      OB_PROP_CURRENT_DISP_SEARCH_OFFSET_INT : Get the current disparity search offset value (read only)

      OB_PROP_FPS_BOOST_BOOL : Enable FPS boost in trigger mode

      OB_PROP_MJPEG_QUALITY_INT : MJPEG encoding quality factor

      OB_PROP_COLOR_AE_AWB_STATUS_INT : Color AE/AWB status, 0: converging, 1: dual convergence

      OB_PROP_COLOR_AE_AWB_STAT_INT : Alias of OB_PROP_COLOR_AE_AWB_STATUS_INT

      OB_PROP_ACTION_SIGNAL_COUNT_INT : Number of Action Signal blocks supported by the device

      OB_PROP_ACTION_DEVICE_KEY_INT : Action Device Key, shared across all Action Commands

      OB_PROP_ACTION_SCHEDULED_COMMAND_QUEUE_SIZE_INT : Maximum number of scheduled Action Commands that can be queued by the device

      OB_PROP_ACTION_SELECTOR_INT : Action Signal selector, 0..N-1; subsequent selector-scoped reads/writes target the selected block

      OB_PROP_ACTION_GROUP_KEY_INT : Action Group Key for the currently selected block

      OB_PROP_ACTION_GROUP_MASK_INT : Action Group Mask for the currently selected block

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

      OB_STRUCT_COLOR_AWB_GAIN : Color AWB gain parameters

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

      OB_PROP_COLOR_WB_CTRL_INT : Color camera WB control

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

      OB_PROP_DEPTH_OUTLIERS_FILTER_BOOL : depth outliers filter switch

      OB_PROP_DEPTH_OUTLIERS_FILTER_SEARCH_MODE_INT : depth outliers filter search range mode

      OB_DEVICE_AUTO_CAPTURE_ENABLE_BOOL : soft trigger auto capture enable, use in OB_MULTI_DEVICE_SYNC_MODE_SOFTWARE_TRIGGERING mode

      OB_DEVICE_AUTO_CAPTURE_INTERVAL_TIME_INT : soft trigger auto capture interval time, use in OB_MULTI_DEVICE_SYNC_MODE_SOFTWARE_TRIGGERING mode

      OB_DEVICE_PTP_CLOCK_SYNC_ENABLE_BOOL : PTP time synchronization enable

      OB_PROP_DEBUG_ESGM_CONFIDENCE_FLOAT : Confidence degree
    """

    OB_DEVICE_AUTO_CAPTURE_ENABLE_BOOL: typing.ClassVar[OBPropertyID]
    OB_DEVICE_AUTO_CAPTURE_INTERVAL_TIME_INT: typing.ClassVar[OBPropertyID]
    OB_DEVICE_PTP_CLOCK_SYNC_ENABLE_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_ACTION_DEVICE_KEY_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_ACTION_GROUP_KEY_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_ACTION_GROUP_MASK_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_ACTION_SCHEDULED_COMMAND_QUEUE_SIZE_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_ACTION_SELECTOR_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_ACTION_SIGNAL_COUNT_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_ANTI_COLLUSION_ACTIVATION_STATUS_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_BOOT_INTO_RECOVERY_MODE_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_BRT_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_CAPTURE_IMAGE_FRAME_NUMBER_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_CAPTURE_IMAGE_NUMBER_INTERVAL_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_CAPTURE_IMAGE_SIGNAL_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_CAPTURE_IMAGE_TIME_INTERVAL_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_CAPTURE_INTERVAL_MODE_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_CHECK_PPS_SYNC_IN_SIGNAL_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_COLOR_AE_AWB_STATUS_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_COLOR_AE_AWB_STAT_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_COLOR_AE_MAX_EXPOSURE_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_COLOR_AE_MAX_GAIN_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_COLOR_ANTI_FLICKER_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_COLOR_AUTO_EXPOSURE_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_COLOR_AUTO_EXPOSURE_PRIORITY_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_COLOR_AUTO_WHITE_BALANCE_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_COLOR_BACKLIGHT_COMPENSATION_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_COLOR_BRIGHTNESS_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_COLOR_CONTRAST_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_COLOR_DENOISING_LEVEL_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_COLOR_EXPOSURE_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_COLOR_FLIP_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_COLOR_FOCUS_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_COLOR_GAIN_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_COLOR_GAMMA_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_COLOR_HDR_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_COLOR_HUE_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_COLOR_LEFT_FLIP_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_COLOR_LEFT_MIRROR_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_COLOR_LEFT_ROTATE_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_COLOR_MAXIMAL_SHUTTER_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_COLOR_MIRROR_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_COLOR_POWER_LINE_FREQUENCY_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_COLOR_PRESET_PRIORITY_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_COLOR_RIGHT_FLIP_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_COLOR_RIGHT_MIRROR_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_COLOR_RIGHT_ROTATE_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_COLOR_ROI_BRIGHTNESS_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_COLOR_ROLL_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_COLOR_ROTATE_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_COLOR_SATURATION_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_COLOR_SHARPNESS_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_COLOR_SHUTTER_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_COLOR_WB_CTRL_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_COLOR_WHITE_BALANCE_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_CONFIDENCE_FLIP_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_CONFIDENCE_MIRROR_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_CONFIDENCE_ROTATE_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_CONFIDENCE_STREAM_FILTER_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_CONFIDENCE_STREAM_FILTER_THRESHOLD_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_CPU_TEMPERATURE_CALIBRATION_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_CURRENT_DISP_SEARCH_OFFSET_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_CURRENT_DISP_SEARCH_RANGE_MODE_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_D2C_PREPROCESS_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_DC_POWER_STATE_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_DEBUG_ESGM_CONFIDENCE_FLOAT: typing.ClassVar[OBPropertyID]
    OB_PROP_DEPTH_ALIGN_HARDWARE_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_DEPTH_ALIGN_HARDWARE_MODE_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_DEPTH_AUTO_EXPOSURE_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_DEPTH_AUTO_EXPOSURE_PRIORITY_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_DEPTH_CROPPING_MODE_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_DEPTH_EXPOSURE_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_DEPTH_FLIP_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_DEPTH_GAIN_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_DEPTH_HOLEFILTER_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_DEPTH_INDUSTRY_MODE_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_DEPTH_MAX_DIFF_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_DEPTH_MAX_SPECKLE_SIZE_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_DEPTH_MIRROR_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_DEPTH_NOISE_REMOVAL_FILTER_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_DEPTH_NOISE_REMOVAL_FILTER_MAX_DIFF_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_DEPTH_NOISE_REMOVAL_FILTER_MAX_SPECKLE_SIZE_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_DEPTH_OUTLIERS_FILTER_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_DEPTH_OUTLIERS_FILTER_SEARCH_MODE_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_DEPTH_POSTFILTER_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_DEPTH_PRECISION_LEVEL_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_DEPTH_RM_FILTER_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_DEPTH_ROTATE_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_DEPTH_SOFT_FILTER_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_DEPTH_UNIT_FLEXIBLE_ADJUSTMENT_FLOAT: typing.ClassVar[OBPropertyID]
    OB_PROP_DEPTH_WITH_CONFIDENCE_STREAM_ENABLE_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_DEVICE_AE_REFERENCE_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_DEVICE_AE_STRATEGY_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_DEVICE_COMMUNICATION_TYPE_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_DEVICE_DEVELOPMENT_MODE_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_DEVICE_IN_RECOVERY_MODE_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_DEVICE_IP_MODE_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_DEVICE_OFFLINE_AFTER_IP_CONFIG_APPLY: typing.ClassVar[OBPropertyID]
    OB_PROP_DEVICE_PERFORMANCE_MODE_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_DEVICE_REBOOT_DELAY_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_DEVICE_REPOWER_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_DEVICE_USB3_REPEAT_IDENTIFY_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_DEVICE_WORK_MODE_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_DHCP_ASSIGN_IP_TIMEOUT_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_DISPARITY_TO_DEPTH_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_DISP_SEARCH_OFFSET_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_DISP_SEARCH_RANGE_MODE_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_EXTERNAL_SIGNAL_RESET_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_FAN_WORK_MODE_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_FLOOD_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_FLOOD_LEVEL_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_FPS_BOOST_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_FRAME_INTERLEAVE_CONFIG_INDEX_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_FRAME_INTERLEAVE_ENABLE_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_FRAME_INTERLEAVE_LASER_PATTERN_SYNC_DELAY_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_GPM_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_HARDWARE_DISTORTION_SWITCH_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_HDR_MERGE_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_HEARTBEAT_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_HW_NOISE_REMOVE_FILTER_ENABLE_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_HW_NOISE_REMOVE_FILTER_THRESHOLD_FLOAT: typing.ClassVar[OBPropertyID]
    OB_PROP_INDICATOR_LIGHT_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_INTRA_CAMERA_SYNC_REFERENCE_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_IR_AE_MAX_EXPOSURE_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_IR_AUTO_EXPOSURE_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_IR_BRIGHTNESS_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_IR_CHANNEL_DATA_SOURCE_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_IR_EXPOSURE_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_IR_FLIP_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_IR_GAIN_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_IR_LONG_EXPOSURE_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_IR_MIRROR_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_IR_RECTIFY_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_IR_RIGHT_FLIP_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_IR_RIGHT_MIRROR_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_IR_RIGHT_ROTATE_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_IR_ROTATE_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_IR_SHORT_EXPOSURE_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_LASER_ALWAYS_ON_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_LASER_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_LASER_CONTROL_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_LASER_CURRENT_FLOAT: typing.ClassVar[OBPropertyID]
    OB_PROP_LASER_ENERGY_LEVEL_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_LASER_HIGH_TEMPERATURE_PROTECT_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_LASER_HW_ENERGY_LEVEL_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_LASER_MODE_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_LASER_ON_OFF_PATTERN_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_LASER_OVERCURRENT_PROTECTION_STATUS_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_LASER_POWER_ACTUAL_LEVEL_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_LASER_POWER_LEVEL_CONTROL_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_LASER_PULSE_WIDTH_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_LASER_PULSE_WIDTH_PROTECTION_STATUS_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_LDP_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_LDP_MEASURE_DISTANCE_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_LDP_STATUS_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_LIDAR_APD_TEMPERATURE_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_LIDAR_APPLY_CONFIGS_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_LIDAR_MCU_TEMPERATURE_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_LIDAR_MEMS_FOV_SIZE_FLOAT: typing.ClassVar[OBPropertyID]
    OB_PROP_LIDAR_MEMS_FRENQUENCY_FLOAT: typing.ClassVar[OBPropertyID]
    OB_PROP_LIDAR_MOTOR_SPIN_SPEED_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_LIDAR_PORT_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_LIDAR_REPETITIVE_SCAN_MODE_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_LIDAR_SPECIFIC_MODE_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_LIDAR_TAIL_FILTER_LEVEL_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_LIDAR_WARNING_INFO_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_LIDAR_WORK_MODE_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_LOW_EXPOSURE_LASER_CONTROL_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_MAX_DEPTH_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_MIN_DEPTH_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_MJPEG_QUALITY_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_NETWORK_BANDWIDTH_TYPE_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_ON_CHIP_CALIBRATION_ENABLE_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_ON_CHIP_CALIBRATION_HEALTH_CHECK_FLOAT: typing.ClassVar[OBPropertyID]
    OB_PROP_RECTIFY2_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_RESTORE_FACTORY_SETTINGS_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_RGB_CUSTOM_CROP_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_SDK_ACCEL_FRAME_TRANSFORMED_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_SDK_DEPTH_FRAME_UNPACK_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_SDK_DISPARITY_TO_DEPTH_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_SDK_GYRO_FRAME_TRANSFORMED_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_SDK_IR_FRAME_UNPACK_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_SDK_IR_LEFT_FRAME_UNPACK_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_SDK_IR_RIGHT_FRAME_UNPACK_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_SKIP_FRAME_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_SLAVE_DEVICE_SYNC_STATUS_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_SWITCH_IR_MODE_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_SYNC_SIGNAL_TRIGGER_OUT_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_TEMPERATURE_COMPENSATION_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_TIMER_RESET_DELAY_US_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_TIMER_RESET_ENABLE_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_TIMER_RESET_SIGNAL_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_TIMER_RESET_TRIGGER_OUT_ENABLE_BOOL: typing.ClassVar[OBPropertyID]
    OB_PROP_TIMESTAMP_OFFSET_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_TOF_FILTER_RANGE_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_USB_POWER_STATE_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_USB_SYNC_VOLTAGE_LEVEL_INT: typing.ClassVar[OBPropertyID]
    OB_PROP_WATCHDOG_BOOL: typing.ClassVar[OBPropertyID]
    OB_RAW_DATA_CAMERA_CALIB_JSON_FILE: typing.ClassVar[OBPropertyID]
    OB_RAW_DATA_LIDAR_FIRMWARE_VERSION: typing.ClassVar[OBPropertyID]
    OB_RAW_DATA_LIDAR_FPGA_VERSION: typing.ClassVar[OBPropertyID]
    OB_RAW_DATA_LIDAR_IP_ADDRESS: typing.ClassVar[OBPropertyID]
    OB_RAW_DATA_LIDAR_MAC_ADDRESS: typing.ClassVar[OBPropertyID]
    OB_RAW_DATA_LIDAR_PRODUCT_MODEL: typing.ClassVar[OBPropertyID]
    OB_RAW_DATA_LIDAR_SUBNET_MASK: typing.ClassVar[OBPropertyID]
    OB_STRUCT_ASIC_SERIAL_NUMBER: typing.ClassVar[OBPropertyID]
    OB_STRUCT_BASELINE_CALIBRATION_PARAM: typing.ClassVar[OBPropertyID]
    OB_STRUCT_COLOR_AE_ROI: typing.ClassVar[OBPropertyID]
    OB_STRUCT_COLOR_AWB_GAIN: typing.ClassVar[OBPropertyID]
    OB_STRUCT_COLOR_SYNCED_EXPOSURE_PARAM: typing.ClassVar[OBPropertyID]
    OB_STRUCT_CURRENT_DEPTH_ALG_MODE: typing.ClassVar[OBPropertyID]
    OB_STRUCT_DEPTH_AE_ROI: typing.ClassVar[OBPropertyID]
    OB_STRUCT_DEPTH_HDR_CONFIG: typing.ClassVar[OBPropertyID]
    OB_STRUCT_DEPTH_PRECISION_SUPPORT_LIST: typing.ClassVar[OBPropertyID]
    OB_STRUCT_DEVICE_ERROR_STATE: typing.ClassVar[OBPropertyID]
    OB_STRUCT_DEVICE_IP_ADDR_CONFIG: typing.ClassVar[OBPropertyID]
    OB_STRUCT_DEVICE_IP_ADDR_CONFIG_V2: typing.ClassVar[OBPropertyID]
    OB_STRUCT_DEVICE_SERIAL_NUMBER: typing.ClassVar[OBPropertyID]
    OB_STRUCT_DEVICE_STATIC_IP_CONFIG_RECORD: typing.ClassVar[OBPropertyID]
    OB_STRUCT_DEVICE_TEMPERATURE: typing.ClassVar[OBPropertyID]
    OB_STRUCT_DEVICE_TIME: typing.ClassVar[OBPropertyID]
    OB_STRUCT_DISP_OFFSET_CONFIG: typing.ClassVar[OBPropertyID]
    OB_STRUCT_GET_ACCEL_PRESETS_FULL_SCALE_LIST: typing.ClassVar[OBPropertyID]
    OB_STRUCT_GET_ACCEL_PRESETS_ODR_LIST: typing.ClassVar[OBPropertyID]
    OB_STRUCT_GET_GYRO_PRESETS_FULL_SCALE_LIST: typing.ClassVar[OBPropertyID]
    OB_STRUCT_GET_GYRO_PRESETS_ODR_LIST: typing.ClassVar[OBPropertyID]
    OB_STRUCT_MULTI_DEVICE_SYNC_CONFIG: typing.ClassVar[OBPropertyID]
    OB_STRUCT_PRESET_RESOLUTION_CONFIG: typing.ClassVar[OBPropertyID]
    OB_STRUCT_RGB_CROP_ROI: typing.ClassVar[OBPropertyID]
    OB_STRUCT_TOF_EXPOSURE_THRESHOLD_CONTROL: typing.ClassVar[OBPropertyID]
    OB_STRUCT_VERSION: typing.ClassVar[OBPropertyID]
    __members__: typing.ClassVar[dict[str, OBPropertyID]]
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class OBPropertyType:
    """
    Members:

      OB_BOOL_PROPERTY : Boolean property

      OB_INT_PROPERTY : Integer property

      OB_FLOAT_PROPERTY : Float property

      OB_STRUCT_PROPERTY : Struct property
    """

    OB_BOOL_PROPERTY: typing.ClassVar[OBPropertyType]
    OB_FLOAT_PROPERTY: typing.ClassVar[OBPropertyType]
    OB_INT_PROPERTY: typing.ClassVar[OBPropertyType]
    OB_STRUCT_PROPERTY: typing.ClassVar[OBPropertyType]
    __members__: typing.ClassVar[dict[str, OBPropertyType]]
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
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

class RecordDevice:
    def __init__(self, device: Device, file: str, compression: bool = True) -> None: ...
    def pause(self) -> None: ...
    def resume(self) -> None: ...

class PlaybackDevice(Device):
    def __init__(self, file: str, preset_path: str = "") -> None: ...
    def get_duration(self) -> int: ...
    def get_playback_status(self) -> OBPlaybackStatus: ...
    def get_position(self) -> int: ...
    def pause(self) -> None: ...
    def resume(self) -> None: ...
    def seek(self, timestamp: typing.SupportsInt | typing.SupportsIndex) -> None: ...
    def set_playback_rate(self, rate: typing.SupportsFloat | typing.SupportsIndex) -> None: ...
    def set_playback_status_change_callback(self, arg0: typing.Callable) -> None: ...

def convert_accel_full_scale_range_to_string(arg0: OBAccelFullScaleRange) -> str: ...
def convert_format_to_string(arg0: OBFormat) -> str: ...
def convert_frame_metadata_type_to_string(arg0: OBFrameMetadataType) -> str: ...
def convert_frame_type_to_sensor_type(arg0: OBFrameType) -> OBSensorType: ...
def convert_frame_type_to_stream_type(arg0: OBFrameType) -> OBStreamType: ...
def convert_frame_type_to_string(arg0: OBFrameType) -> str: ...
def convert_gyro_full_scale_range_to_string(arg0: OBGyroFullScaleRange) -> str: ...
def convert_imu_sample_rate_to_string(arg0: OBGyroSampleRate) -> str: ...
def convert_imu_sample_rate_to_value(arg0: OBGyroSampleRate) -> float: ...
def convert_imu_sample_rate_value_to_type(arg0: typing.SupportsFloat | typing.SupportsIndex) -> OBGyroSampleRate: ...
def convert_lidar_scan_rate_to_string(arg0: OBLiDARScanRate) -> str: ...
def convert_sensor_type_to_stream_type(arg0: OBSensorType) -> OBStreamType: ...
def convert_sensor_type_to_string(arg0: OBSensorType) -> str: ...
def convert_stream_type_to_frame_type(arg0: OBStreamType) -> OBFrameType: ...
def convert_stream_type_to_sensor_type(arg0: OBStreamType) -> OBSensorType: ...
def convert_stream_type_to_string(arg0: OBStreamType) -> str: ...
def get_version() -> str: ...
def get_version_major() -> int: ...
def get_version_minor() -> int: ...
def get_version_patch() -> int: ...
def get_version_stage() -> str: ...
def is_video_sensor_type(arg0: OBSensorType) -> bool: ...
def is_video_stream_type(arg0: OBStreamType) -> bool: ...
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

COUNT: OBPlaybackStatus
PAUSED: OBPlaybackStatus
PLAYING: OBPlaybackStatus
SAMPLE_RATE_100_HZ: OBGyroSampleRate
SAMPLE_RATE_12_5_HZ: OBGyroSampleRate
SAMPLE_RATE_16_KHZ: OBGyroSampleRate
SAMPLE_RATE_1_5625_HZ: OBGyroSampleRate
SAMPLE_RATE_1_KHZ: OBGyroSampleRate
SAMPLE_RATE_200_HZ: OBGyroSampleRate
SAMPLE_RATE_25_HZ: OBGyroSampleRate
SAMPLE_RATE_2_KHZ: OBGyroSampleRate
SAMPLE_RATE_32_KHZ: OBGyroSampleRate
SAMPLE_RATE_3_125_HZ: OBGyroSampleRate
SAMPLE_RATE_400_HZ: OBGyroSampleRate
SAMPLE_RATE_4_KHZ: OBGyroSampleRate
SAMPLE_RATE_500_HZ: OBGyroSampleRate
SAMPLE_RATE_50_HZ: OBGyroSampleRate
SAMPLE_RATE_6_25_HZ: OBGyroSampleRate
SAMPLE_RATE_800_HZ: OBGyroSampleRate
SAMPLE_RATE_8_KHZ: OBGyroSampleRate
SAMPLE_RATE_UNKNOWN: OBGyroSampleRate
STOPPED: OBPlaybackStatus
UNKNOWN: OBPlaybackStatus
OBAccelSampleRate = OBGyroSampleRate
OBGyroValue = OBAccelValue
OBFloat3D = OBAccelValue
OBSerialNumber = OBDeviceSerialNumber
OBNetIpConfig = OBDeviceIpAddrConfig
OBDepthWorkMode_Internal = OBDepthWorkModeInternal
