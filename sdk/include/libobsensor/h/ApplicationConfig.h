// Copyright (c) Orbbec Inc. All Rights Reserved.
// Licensed under the MIT License.

#pragma once

#include "ObTypes.h"

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @brief Application configuration key.
 *        Each key has a fixed value type and item usage.
 *        Keys must stay within the low 32 bits because @ref OBAppConfigItem stores the key in bits 0-31.
 */
typedef enum {
    OB_APP_CONFIG_SENSORS              = 0, /**< array, sensor list. Use @ref ob_application_config_get_count to get sensor count. */
    OB_APP_CONFIG_SENSOR_TYPE          = 1, /**< int32_t, sensor item: OBSensorType. */
    OB_APP_CONFIG_STREAM_ENABLED       = 2, /**< bool, sensor item: whether the sensor stream should be started. */
    OB_APP_CONFIG_STREAM_PROFILE       = 3, /**< ob_stream_profile, sensor item: stream profile. */
    OB_APP_CONFIG_UNDISTORTION_ENABLED = 4, /**< bool, sensor item: whether undistortion should be enabled. */

    OB_APP_CONFIG_DEVICE_DECIMATION_ENABLED = 5, /**< bool, global item: whether device-level decimation should be applied. */
    OB_APP_CONFIG_DEVICE_DECIMATION         = 6, /**< OBPresetResolutionConfig, global item: device-level decimation configuration. */
                                                 /**< Currently applied only by Gemini 435Le. */
    // Point cloud
    OB_APP_CONFIG_POINTCLOUD_ENABLED                 = 100, /**< bool, global item: whether point cloud output should be enabled. */
    OB_APP_CONFIG_POINTCLOUD_FORMAT                  = 101, /**< int32_t, global item: OBFormat, point cloud output format. */
    OB_APP_CONFIG_POINTCLOUD_DECIMATION_FACTOR       = 102, /**< int32_t, global item: point cloud decimation factor. */
    OB_APP_CONFIG_POINTCLOUD_ALIGN_MODE              = 103, /**< int32_t, global item: OBAlignMode. */
    OB_APP_CONFIG_POINTCLOUD_FRAME_SYNC              = 104, /**< bool, global item: whether frame sync should be enabled. */
    OB_APP_CONFIG_POINTCLOUD_ALL_FRAME_TYPE_REQUIRED = 105, /**< bool, global item: false: output on any situation, true: require all frame types. */
    OB_APP_CONFIG_POINTCLOUD_MATCH_TARGET_RESOLUTION = 106, /**< bool, global item: whether to match target resolution. */
    // HDR Merge
    OB_APP_CONFIG_HDR_MERGE_ENABLED    = 200, /**< bool, global item: whether HDR merge should be enabled. */
    OB_APP_CONFIG_HDR_MERGE_IR_ENABLED = 201, /**< bool, global item: whether IR frame should be enabled for HDR merge. */
} OBAppConfigKey,
    ob_app_config_key;

/**
 * @brief Application configuration item.
 *        An item combines a configuration key and an optional array index.
 *        Non-array keys use @ref OB_APP_CONFIG_ITEM.
 *        Array keys use @ref OB_APP_CONFIG_ARRAY_ITEM.
 *        The key is stored in bits 0-31 and the index is stored in bits 32-63.
 */
typedef uint64_t OBAppConfigItem, ob_app_config_item;

#define OB_APP_CONFIG_INDEX_NONE (0u)
#define OB_APP_CONFIG_ITEM(key) ((OBAppConfigItem)(uint32_t)(key))
#define OB_APP_CONFIG_ARRAY_ITEM(key, index) ((((OBAppConfigItem)(uint32_t)(index)) << 32) | (OBAppConfigItem)(uint32_t)(key))
#define OB_APP_CONFIG_ITEM_KEY(item) ((OBAppConfigKey)((uint32_t)((item) & 0xFFFFFFFFu)))
#define OB_APP_CONFIG_ITEM_INDEX(item) ((uint32_t)(((item) >> 32) & 0xFFFFFFFFu))

/**
 * @brief Application configuration value type.
 */
typedef enum {
    OB_APP_CONFIG_VALUE_BOOL,   /**< Boolean value. */
    OB_APP_CONFIG_VALUE_INT,    /**< int32_t value. */
    OB_APP_CONFIG_VALUE_FLOAT,  /**< float value. */
    OB_APP_CONFIG_VALUE_STRING, /**< String value. The returned pointer is owned by the config object. */
    OB_APP_CONFIG_VALUE_STRUCT, /**< Fixed-size SDK structure value. */
} OBAppConfigValueType,
    ob_app_config_value_type;

/**
 * @brief Get the application runtime configuration cache for the device.
 *
 * @param[in] device The device object.
 * @param[out] error Pointer to an error object that will be set if an error occurs.
 *
 * @return ob_application_config* The application configuration object cached by the device.
 * @attention If the device has no application configuration cache, the SDK creates one with default values.
 * @attention Changes made through the returned config update the device cache directly.
 * @attention The returned config should be released by calling @ref ob_delete_application_config.
 */
OB_EXPORT ob_application_config *ob_device_get_application_config(ob_device *device, ob_error **error);

/**
 * @brief Get the application configuration carried by an externally imported preset, by preset name.
 *
 * @param[in] device The device object.
 * @param[in] preset_name The preset name to query.
 * @param[out] error Pointer to an error object that will be set if an error occurs.
 *
 * @return ob_application_config* The application configuration imported with the given preset, or NULL for
 * built-in presets or presets that carry no application configuration.
 * @attention The returned config is owned by the device; it should still be released by calling
 * @ref ob_delete_application_config (releasing the handle does not destroy the cached object).
 */
OB_EXPORT ob_application_config *ob_device_get_application_config_by_preset(ob_device *device, const char *preset_name, ob_error **error);

/**
 * @brief Delete an application configuration object.
 *
 * @param[in] config The application configuration object to be deleted.
 * @param[out] error Pointer to an error object that will be set if an error occurs.
 */
OB_EXPORT void ob_delete_application_config(ob_application_config *config, ob_error **error);

/**
 * @brief Check whether the current device supports application runtime configuration import/export.
 *
 * @param[in] device The device object.
 * @param[out] error Pointer to an error object that will be set if an error occurs.
 *
 * @return bool Return true if application configuration import/export is supported, false otherwise.
 */
OB_EXPORT bool ob_device_is_application_config_supported(ob_device *device, ob_error **error);

/**
 * @brief Reset an application configuration object to default values.
 *
 * @param[in] config The application configuration object.
 * @param[out] error Pointer to an error object that will be set if an error occurs.
 */
OB_EXPORT void ob_application_config_reset(ob_application_config *config, ob_error **error);

/**
 * @brief Set a bool value.
 *
 * @param[in] config The application configuration object.
 * @param[in] item The configuration item to update. Use @ref OB_APP_CONFIG_ITEM or @ref OB_APP_CONFIG_ARRAY_ITEM to build it.
 * @param[in] value The bool value to be set.
 * @param[out] error Pointer to an error object that will be set if an error occurs.
 */
OB_EXPORT void ob_application_config_set_bool(ob_application_config *config, OBAppConfigItem item, bool value, ob_error **error);

/**
 * @brief Get a bool value.
 *
 * @param[in] config The application configuration object.
 * @param[in] item The configuration item to read. Use @ref OB_APP_CONFIG_ITEM or @ref OB_APP_CONFIG_ARRAY_ITEM to build it.
 * @param[out] error Pointer to an error object that will be set if an error occurs.
 *
 * @return bool The bool value.
 */
OB_EXPORT bool ob_application_config_get_bool(const ob_application_config *config, OBAppConfigItem item, ob_error **error);

/**
 * @brief Set an int32_t value.
 *
 * @param[in] config The application configuration object.
 * @param[in] item The configuration item to update. Use @ref OB_APP_CONFIG_ITEM or @ref OB_APP_CONFIG_ARRAY_ITEM to build it.
 * @param[in] value The int32_t value to be set.
 * @param[out] error Pointer to an error object that will be set if an error occurs.
 */
OB_EXPORT void ob_application_config_set_int(ob_application_config *config, OBAppConfigItem item, int32_t value, ob_error **error);

/**
 * @brief Get an int32_t value.
 *
 * @param[in] config The application configuration object.
 * @param[in] item The configuration item to read. Use @ref OB_APP_CONFIG_ITEM or @ref OB_APP_CONFIG_ARRAY_ITEM to build it.
 * @param[out] error Pointer to an error object that will be set if an error occurs.
 *
 * @return int32_t The int32_t value.
 */
OB_EXPORT int32_t ob_application_config_get_int(const ob_application_config *config, OBAppConfigItem item, ob_error **error);

/**
 * @brief Set a float value.
 *
 * @param[in] config The application configuration object.
 * @param[in] item The configuration item to update. Use @ref OB_APP_CONFIG_ITEM or @ref OB_APP_CONFIG_ARRAY_ITEM to build it.
 * @param[in] value The float value to be set.
 * @param[out] error Pointer to an error object that will be set if an error occurs.
 */
OB_EXPORT void ob_application_config_set_float(ob_application_config *config, OBAppConfigItem item, float value, ob_error **error);

/**
 * @brief Get a float value.
 *
 * @param[in] config The application configuration object.
 * @param[in] item The configuration item to read. Use @ref OB_APP_CONFIG_ITEM or @ref OB_APP_CONFIG_ARRAY_ITEM to build it.
 * @param[out] error Pointer to an error object that will be set if an error occurs.
 *
 * @return float The float value.
 */
OB_EXPORT float ob_application_config_get_float(const ob_application_config *config, OBAppConfigItem item, ob_error **error);

/**
 * @brief Set a string value.
 *
 * @param[in] config The application configuration object.
 * @param[in] item The configuration item to update. Use @ref OB_APP_CONFIG_ITEM or @ref OB_APP_CONFIG_ARRAY_ITEM to build it.
 * @param[in] value The string value to be set.
 * @param[out] error Pointer to an error object that will be set if an error occurs.
 */
OB_EXPORT void ob_application_config_set_string(ob_application_config *config, OBAppConfigItem item, const char *value, ob_error **error);

/**
 * @brief Get a string value.
 *
 * @param[in] config The application configuration object.
 * @param[in] item The configuration item to read. Use @ref OB_APP_CONFIG_ITEM or @ref OB_APP_CONFIG_ARRAY_ITEM to build it.
 * @param[out] error Pointer to an error object that will be set if an error occurs.
 *
 * @return const char* The string value.
 * @attention The returned pointer is owned by the config object and becomes invalid after the config is modified or deleted.
 */
OB_EXPORT const char *ob_application_config_get_string(const ob_application_config *config, OBAppConfigItem item, ob_error **error);

/**
 * @brief Set a fixed-size SDK structure value.
 *
 * @param[in] config The application configuration object.
 * @param[in] item The configuration item to update. Use @ref OB_APP_CONFIG_ITEM or @ref OB_APP_CONFIG_ARRAY_ITEM to build it.
 * @param[in] value Pointer to the structure value to be copied.
 * @param[in] valueSize Size of the structure value in bytes.
 * @param[out] error Pointer to an error object that will be set if an error occurs.
 */
OB_EXPORT void ob_application_config_set_struct(ob_application_config *config, OBAppConfigItem item, const void *value, uint32_t valueSize, ob_error **error);

/**
 * @brief Get a fixed-size SDK structure value.
 *
 * @param[in] config The application configuration object.
 * @param[in] item The configuration item to read. Use @ref OB_APP_CONFIG_ITEM or @ref OB_APP_CONFIG_ARRAY_ITEM to build it.
 * @param[out] value Pointer to the buffer that receives the structure value.
 * @param[in] valueSize Size of the output buffer in bytes.
 * @param[out] error Pointer to an error object that will be set if an error occurs.
 */
OB_EXPORT void ob_application_config_get_struct(const ob_application_config *config, OBAppConfigItem item, void *value, uint32_t valueSize, ob_error **error);

/**
 * @brief Set the stream profile for a sensor item.
 *
 * @param[in] config The application configuration object.
 * @param[in] item The sensor stream profile item to update. Use @ref OB_APP_CONFIG_ARRAY_ITEM with @ref OB_APP_CONFIG_STREAM_PROFILE.
 * @param[in] profile The stream profile to be copied into the config object.
 * @param[out] error Pointer to an error object that will be set if an error occurs.
 *
 * @attention The config object clones the profile. The caller still owns and should release the input profile.
 */
OB_EXPORT void ob_application_config_set_profile(ob_application_config *config, OBAppConfigItem item, const ob_stream_profile *profile, ob_error **error);

/**
 * @brief Get the stream profile from a sensor item.
 *
 * @param[in] config The application configuration object.
 * @param[in] item The sensor stream profile item to read. Use @ref OB_APP_CONFIG_ARRAY_ITEM with @ref OB_APP_CONFIG_STREAM_PROFILE.
 * @param[out] error Pointer to an error object that will be set if an error occurs.
 *
 * @return ob_stream_profile* The stream profile stored in the sensor item.
 * @attention The returned profile should be released by calling @ref ob_delete_stream_profile.
 */
OB_EXPORT ob_stream_profile *ob_application_config_get_profile(const ob_application_config *config, OBAppConfigItem item, ob_error **error);

/**
 * @brief Get the number of items in an array key.
 *
 * Currently only @ref OB_APP_CONFIG_SENSORS is supported.
 *
 * @param[in] config The application configuration object.
 * @param[in] key The array key to count. Refer to @ref OBAppConfigKey for available keys.
 * @param[out] error Pointer to an error object that will be set if an error occurs.
 *
 * @return uint32_t The number of items in the array key.
 */
OB_EXPORT uint32_t ob_application_config_get_count(const ob_application_config *config, OBAppConfigKey key, ob_error **error);

#ifdef __cplusplus
}
#endif
