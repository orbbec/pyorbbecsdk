// Copyright (c) Orbbec Inc. All Rights Reserved.
// Licensed under the MIT License.

#pragma once

#ifdef __cplusplus
extern "C" {
#endif

#include "ObTypes.h"

/**
 * @brief Convert OBFormat to " char* " type and then return.
 *
 * @param[in] type OBFormat type.
 *
 * @return OBFormat of "char*" type.
 */
OB_EXPORT const char* ob_format_type_to_string(OBFormat type);

/**
 * @brief Convert OBFrameType to " char* " type and then return.
 *
 * @param[in] type OBFrameType type.
 *
 * @return OBFrameType of "char*" type.
 */
OB_EXPORT const char* ob_frame_type_to_string(OBFrameType type);

/**
 * @brief Convert OBStreamType to " char* " type and then return.
 *
 * @param[in] type OBStreamType type.
 *
 * @return OBStreamType of "char*" type.
 */
OB_EXPORT const char* ob_stream_type_to_string(OBStreamType type);

/**
 * @brief Convert OBSensorType to " char* " type and then return.
 *
 * @param[in] type OBSensorType type.
 *
 * @return OBSensorType of "char*" type.
 */
OB_EXPORT const char* ob_sensor_type_to_string(OBSensorType type);

/**
 * @brief Convert OBIMUSampleRate to " char* " type and then return.
 *
 * @param[in] type OBIMUSampleRate type.
 *
 * @return OBIMUSampleRate of "char*" type.
 */
OB_EXPORT const char* ob_imu_rate_type_to_string(OBIMUSampleRate type);

/**
 * @brief Convert OBIMUSampleRate to its numeric frequency value in Hz.
 *
 * @param[in] type OBIMUSampleRate type.
 *
 * @return IMU sample rate value in Hz. Returns 0 for unknown values.
 */
OB_EXPORT float ob_imu_rate_type_to_value(OBIMUSampleRate type);

/**
 * @brief Convert a numeric IMU sample rate value in Hz to OBIMUSampleRate.
 *
 * @param[in] value IMU sample rate value in Hz.
 *
 * @return Matching OBIMUSampleRate. Returns OB_SAMPLE_RATE_UNKNOWN when no exact SDK rate matches.
 */
OB_EXPORT OBIMUSampleRate ob_imu_rate_value_to_type(float value);

/**
 * @brief Convert OBGyroFullScaleRange to " char* " type and then return.
 *
 * @param[in] type OBGyroFullScaleRange type.
 *
 * @return OBGyroFullScaleRange of "char*" type.
 */
OB_EXPORT const char* ob_gyro_range_type_to_string(OBGyroFullScaleRange type);

/**
 * @brief Convert OBAccelFullScaleRange to " char* " type and then return.
 *
 * @param[in] type OBAccelFullScaleRange type.
 *
 * @return OBAccelFullScaleRange of "char*" type.
 */
OB_EXPORT const char* ob_accel_range_type_to_string(OBAccelFullScaleRange type);

/**
 * @brief Convert OBLiDARScanRate to " char* " type and then return.
 *
 * @param[in] type OBLiDARScanRate type.
 * @return OBLiDARScanRate of "char*" type.
 */
OB_EXPORT const char *ob_lidar_scan_rate_type_to_string(OBLiDARScanRate type);

/**
 * @brief Convert OBFrameMetadataType to " char* " type and then return.
 *
 * @param[in] type OBFrameMetadataType type.
 *
 * @return OBFrameMetadataType of "char*" type.
 */
OB_EXPORT const char* ob_meta_data_type_to_string(OBFrameMetadataType type);

/**
 * @brief Convert OBSensorType to OBStreamType.
 *
 * @param[in] type The sensor type to convert.
 *
 * @return The corresponding stream type.
 */
OB_EXPORT OBStreamType ob_sensor_type_to_stream_type(OBSensorType type);

/**
 * @brief Convert OBStreamType to OBSensorType.
 *
 * @param[in] type The stream type to convert.
 *
 * @return The corresponding sensor type.
 */
OB_EXPORT OBSensorType ob_stream_type_to_sensor_type(OBStreamType type);

/**
 * @brief Convert OBStreamType to OBFrameType.
 *
 * @param[in] type The stream type to convert.
 *
 * @return The corresponding frame type.
 */
OB_EXPORT OBFrameType ob_stream_type_to_frame_type(OBStreamType type);

/**
 * @brief Convert OBFrameType to OBStreamType.
 *
 * @param[in] type The frame type to convert.
 *
 * @return The corresponding stream type.
 */
OBStreamType ob_frame_type_to_stream_type(OBFrameType type);

/**
 * @brief Convert OBFrameType to OBSensorType.
 *
 * @param[in] type The frame type to convert.
 *
 * @return The corresponding sensor type.
 */
OB_EXPORT OBSensorType ob_frame_type_to_sensor_type(OBFrameType type);

/**
 * @brief Convert OBFormat to " char* " type and then return.
 *
 * @param[in] format The OBFormat to convert.
 *
 * @return The string.
 */
OB_EXPORT const char *ob_format_to_string(OBFormat format);
#ifdef __cplusplus
}
#endif
