// Copyright (c) Orbbec Inc. All Rights Reserved.
// Licensed under the MIT License.

#pragma once

#include "Device.hpp"
#include "StreamProfile.hpp"
#include "Error.hpp"
#include "libobsensor/h/Advanced.h"
#include "libobsensor/h/ApplicationConfig.h"

#include <memory>
#include <stdexcept>
#include <vector>

namespace ob {

class ApplicationSensorConfig {
public:
    explicit ApplicationSensorConfig(OBSensorType sensorType) : sensorType_(sensorType) {}

    OBSensorType sensorType() const {
        return sensorType_;
    }

    void enableStream(bool enabled) {
        streamEnabled_ = enabled;
    }

    bool isStreamEnabled() const {
        return streamEnabled_;
    }

    void setStreamProfile(const std::shared_ptr<StreamProfile> &profile) {
        streamProfile_ = profile;
    }

    std::shared_ptr<StreamProfile> streamProfile() const {
        return streamProfile_;
    }

    void enableUndistortion(bool enabled) {
        undistortionEnabled_ = enabled;
    }

    bool isUndistortionEnabled() const {
        return undistortionEnabled_;
    }

private:
    OBSensorType                   sensorType_{ OB_SENSOR_UNKNOWN };
    bool                           streamEnabled_ = { false };
    std::shared_ptr<StreamProfile> streamProfile_;
    bool                           undistortionEnabled_ = { false };
};

class ApplicationPointCloudConfig {
public:
    void enable(bool enabled) {
        enabled_ = enabled;
    }

    bool isEnabled() const {
        return enabled_;
    }

    void setFormat(OBFormat format) {
        format_ = format;
    }

    OBFormat format() const {
        return format_;
    }

    void setDecimationFactor(int32_t factor) {
        decimationFactor_ = factor;
    }

    int32_t decimationFactor() const {
        return decimationFactor_;
    }

    void setAlignMode(OBAlignMode mode) {
        alignMode_ = mode;
    }

    OBAlignMode alignMode() const {
        return alignMode_;
    }

    void enableFrameSync(bool enabled) {
        frameSync_ = enabled;
    }

    bool isFrameSyncEnabled() const {
        return frameSync_;
    }

    void setAllFrameTypeRequired(bool enabled) {
        allFrameTypeRequired_ = enabled;
    }

    bool isAllFrameTypeRequired() const {
        return allFrameTypeRequired_;
    }

    void enableMatchTargetResolution(bool enabled) {
        matchTargetResolution_ = enabled;
    }

    bool isMatchTargetResolutionEnabled() const {
        return matchTargetResolution_;
    }

private:
    bool        enabled_{ false };
    OBFormat    format_{ OB_FORMAT_POINT };
    int32_t     decimationFactor_{ 0 };
    OBAlignMode alignMode_{ ALIGN_DISABLE };
    bool        frameSync_{ false };
    bool        allFrameTypeRequired_{ false };
    bool        matchTargetResolution_{ false };
};

class ApplicationHDRMergeConfig {
public:
    void enable(bool enabled) {
        enabled_ = enabled;
    }

    bool isEnabled() const {
        return enabled_;
    }

    void enableIR(bool enabled) {
        enableIRforHDR_ = enabled;
    }

    bool isIREnabled() const {
        return enableIRforHDR_;
    }

private:
    bool enabled_{ false };
    bool enableIRforHDR_{ true };
};

class ApplicationDevDecimationConfig {
public:
    void enable(bool enabled) {
        enabled_ = enabled;
    }

    bool isEnabled() const {
        return enabled_;
    }

    void setPresetResolutionConfig(const OBPresetResolutionConfig &config) {
        config_ = config;
    }

    const OBPresetResolutionConfig &presetResolutionConfig() const {
        return config_;
    }

private:
    bool                     enabled_{ false };
    OBPresetResolutionConfig config_;
};

class ApplicationConfig {
public:
    static bool isSupported(const std::shared_ptr<Device> &device) {
        ob_error *error = nullptr;
        auto      ret   = ob_device_is_application_config_supported(device->getImpl(), &error);
        Error::handle(&error);
        return ret;
    }

    static std::shared_ptr<ApplicationConfig> get(const std::shared_ptr<Device> &device) {
        ob_error *error  = nullptr;
        auto      handle = ob_device_get_application_config(device->getImpl(), &error);
        Error::handle(&error);
        return std::make_shared<ApplicationConfig>(handle);
    }

    /**
     * @brief Get the application config carried by an externally imported preset, by preset name.
     * @return nullptr for built-in presets or presets that carry no application config.
     */
    static std::shared_ptr<ApplicationConfig> get(const std::shared_ptr<Device> &device, const std::string &presetName) {
        ob_error *error  = nullptr;
        auto      handle = ob_device_get_application_config_by_preset(device->getImpl(), presetName.c_str(), &error);
        Error::handle(&error);
        if(!handle) {
            return nullptr;
        }
        return std::make_shared<ApplicationConfig>(handle);
    }

    explicit ApplicationConfig(ob_application_config *handle) : handle_(handle) {}

    ~ApplicationConfig() noexcept {
        if(handle_) {
            ob_error *error = nullptr;
            ob_delete_application_config(handle_, &error);
            Error::handle(&error, false);
        }
    }

    ob_application_config *handle() const {
        return handle_;
    }

    void reset() {
        ob_error *error = nullptr;
        ob_application_config_reset(handle_, &error);
        Error::handle(&error);
    }

    std::vector<std::shared_ptr<ApplicationSensorConfig>> sensors() const {
        std::vector<std::shared_ptr<ApplicationSensorConfig>> result;
        ob_error                                             *error = nullptr;
        auto                                                  count = ob_application_config_get_count(handle_, OB_APP_CONFIG_SENSORS, &error);
        Error::handle(&error);
        for(uint32_t i = 0; i < count; ++i) {
            auto sensorType = static_cast<OBSensorType>(ob_application_config_get_int(handle_, OB_APP_CONFIG_ARRAY_ITEM(OB_APP_CONFIG_SENSOR_TYPE, i), &error));
            Error::handle(&error);
            auto sensorConfig = std::make_shared<ApplicationSensorConfig>(sensorType);
            // enable
            auto enable = ob_application_config_get_bool(handle_, OB_APP_CONFIG_ARRAY_ITEM(OB_APP_CONFIG_STREAM_ENABLED, i), &error);
            Error::handle(&error);
            sensorConfig->enableStream(enable);
            // profile
            auto profile = ob_application_config_get_profile(handle_, OB_APP_CONFIG_ARRAY_ITEM(OB_APP_CONFIG_STREAM_PROFILE, i), &error);
            Error::handle(&error);
            sensorConfig->setStreamProfile(StreamProfileFactory::create(profile));
            result.emplace_back(sensorConfig);
            // undistortion
            enable = ob_application_config_get_bool(handle_, OB_APP_CONFIG_ARRAY_ITEM(OB_APP_CONFIG_UNDISTORTION_ENABLED, i), &error);
            Error::handle(&error, false);  // optional
            sensorConfig->enableUndistortion(enable);
        }
        return result;
    }

    void setSensors(const std::vector<std::shared_ptr<ApplicationSensorConfig>> &sensors) {
        for(const auto &sensor: sensors) {
            setSensor(sensor);
        }
    }

    void setSensor(const std::shared_ptr<ApplicationSensorConfig> &sensor) {
        if(!sensor) {
            return;
        }
        ob_error *error = nullptr;
        auto      index = sensorIndex(sensor->sensorType());
        // enable
        ob_application_config_set_bool(handle_, OB_APP_CONFIG_ARRAY_ITEM(OB_APP_CONFIG_STREAM_ENABLED, index), sensor->isStreamEnabled(), &error);
        Error::handle(&error);
        // profile
        auto profile = sensor->streamProfile();
        if(!profile) {
            throw std::runtime_error("ApplicationSensorConfig: stream profile must not be null");
        }
        ob_application_config_set_profile(handle_, OB_APP_CONFIG_ARRAY_ITEM(OB_APP_CONFIG_STREAM_PROFILE, index), profile->getImpl(), &error);
        Error::handle(&error);
        // undistortion
        ob_application_config_set_bool(handle_, OB_APP_CONFIG_ARRAY_ITEM(OB_APP_CONFIG_UNDISTORTION_ENABLED, index), sensor->isUndistortionEnabled(), &error);
        Error::handle(&error);
    }

    std::shared_ptr<ApplicationDevDecimationConfig> deviceDecimation() const {
        auto      cfg   = std::make_shared<ApplicationDevDecimationConfig>();
        ob_error *error = nullptr;
        // enable
        auto enable = ob_application_config_get_bool(handle_, OB_APP_CONFIG_ITEM(OB_APP_CONFIG_DEVICE_DECIMATION_ENABLED), &error);
        Error::handle(&error);
        cfg->enable(enable);
        if(enable) {
            // Preset resolution
            OBPresetResolutionConfig config{};
            ob_application_config_get_struct(handle_, OB_APP_CONFIG_ITEM(OB_APP_CONFIG_DEVICE_DECIMATION), &config, sizeof(config), &error);
            Error::handle(&error);
            cfg->setPresetResolutionConfig(config);
        }
        return cfg;
    }

    void setDeviceDecimation(const std::shared_ptr<ApplicationDevDecimationConfig> &config) {
        if(!config) {
            return;
        }
        ob_error *error = nullptr;
        ob_application_config_set_bool(handle_, OB_APP_CONFIG_ITEM(OB_APP_CONFIG_DEVICE_DECIMATION_ENABLED), config->isEnabled(), &error);
        Error::handle(&error);
        auto presetResConfig = config->presetResolutionConfig();
        ob_application_config_set_struct(handle_, OB_APP_CONFIG_ITEM(OB_APP_CONFIG_DEVICE_DECIMATION), &presetResConfig, sizeof(presetResConfig), &error);
        Error::handle(&error);
    }

    std::shared_ptr<ApplicationPointCloudConfig> pointCloud() const {
        auto      cfg   = std::make_shared<ApplicationPointCloudConfig>();
        ob_error *error = nullptr;
        // enable
        auto enable = ob_application_config_get_bool(handle_, OB_APP_CONFIG_ITEM(OB_APP_CONFIG_POINTCLOUD_ENABLED), &error);
        Error::handle(&error);
        cfg->enable(enable);
        // format
        auto value = ob_application_config_get_int(handle_, OB_APP_CONFIG_ITEM(OB_APP_CONFIG_POINTCLOUD_FORMAT), &error);
        Error::handle(&error);
        cfg->setFormat(static_cast<OBFormat>(value));
        // decimation factor
        value = ob_application_config_get_int(handle_, OB_APP_CONFIG_ITEM(OB_APP_CONFIG_POINTCLOUD_DECIMATION_FACTOR), &error);
        Error::handle(&error);
        cfg->setDecimationFactor(value);
        // align mode
        value = ob_application_config_get_int(handle_, OB_APP_CONFIG_ITEM(OB_APP_CONFIG_POINTCLOUD_ALIGN_MODE), &error);
        Error::handle(&error);
        cfg->setAlignMode(static_cast<OBAlignMode>(value));
        // frame sync
        enable = ob_application_config_get_bool(handle_, OB_APP_CONFIG_ITEM(OB_APP_CONFIG_POINTCLOUD_FRAME_SYNC), &error);
        Error::handle(&error);
        cfg->enableFrameSync(enable);
        // frame aggregate mode
        enable = ob_application_config_get_bool(handle_, OB_APP_CONFIG_ITEM(OB_APP_CONFIG_POINTCLOUD_ALL_FRAME_TYPE_REQUIRED), &error);
        Error::handle(&error);
        cfg->setAllFrameTypeRequired(enable);
        // match target resolution
        enable = ob_application_config_get_bool(handle_, OB_APP_CONFIG_ITEM(OB_APP_CONFIG_POINTCLOUD_MATCH_TARGET_RESOLUTION), &error);
        Error::handle(&error);
        cfg->enableMatchTargetResolution(enable);
        return cfg;
    }

    void setPointCloud(const std::shared_ptr<ApplicationPointCloudConfig> &config) {
        if(!config) {
            return;
        }
        ob_error *error = nullptr;
        ob_application_config_set_bool(handle_, OB_APP_CONFIG_ITEM(OB_APP_CONFIG_POINTCLOUD_ENABLED), config->isEnabled(), &error);
        Error::handle(&error);
        ob_application_config_set_int(handle_, OB_APP_CONFIG_ITEM(OB_APP_CONFIG_POINTCLOUD_FORMAT), static_cast<int32_t>(config->format()), &error);
        Error::handle(&error);
        ob_application_config_set_int(handle_, OB_APP_CONFIG_ITEM(OB_APP_CONFIG_POINTCLOUD_DECIMATION_FACTOR), config->decimationFactor(), &error);
        Error::handle(&error);
        ob_application_config_set_int(handle_, OB_APP_CONFIG_ITEM(OB_APP_CONFIG_POINTCLOUD_ALIGN_MODE), static_cast<int32_t>(config->alignMode()), &error);
        Error::handle(&error);
        ob_application_config_set_bool(handle_, OB_APP_CONFIG_ITEM(OB_APP_CONFIG_POINTCLOUD_FRAME_SYNC), config->isFrameSyncEnabled(), &error);
        Error::handle(&error);
        ob_application_config_set_bool(handle_, OB_APP_CONFIG_ITEM(OB_APP_CONFIG_POINTCLOUD_ALL_FRAME_TYPE_REQUIRED), config->isAllFrameTypeRequired(), &error);
        Error::handle(&error);
        ob_application_config_set_bool(handle_, OB_APP_CONFIG_ITEM(OB_APP_CONFIG_POINTCLOUD_MATCH_TARGET_RESOLUTION), config->isMatchTargetResolutionEnabled(),
                                       &error);
        Error::handle(&error);
    }

    std::shared_ptr<ApplicationHDRMergeConfig> hdrMerge() const {
        auto      cfg   = std::make_shared<ApplicationHDRMergeConfig>();
        ob_error *error = nullptr;
        // enable
        auto enable = ob_application_config_get_bool(handle_, OB_APP_CONFIG_ITEM(OB_APP_CONFIG_HDR_MERGE_ENABLED), &error);
        Error::handle(&error);
        cfg->enable(enable);
        // IR enable
        enable = ob_application_config_get_bool(handle_, OB_APP_CONFIG_ITEM(OB_APP_CONFIG_HDR_MERGE_IR_ENABLED), &error);
        Error::handle(&error);
        cfg->enableIR(enable);
        return cfg;
    }

    void setHDRMerge(const std::shared_ptr<ApplicationHDRMergeConfig> &config) {
        if(!config) {
            return;
        }
        ob_error *error = nullptr;
        ob_application_config_set_bool(handle_, OB_APP_CONFIG_ITEM(OB_APP_CONFIG_HDR_MERGE_ENABLED), config->isEnabled(), &error);
        Error::handle(&error);
        ob_application_config_set_bool(handle_, OB_APP_CONFIG_ITEM(OB_APP_CONFIG_HDR_MERGE_IR_ENABLED), config->isIREnabled(), &error);
        Error::handle(&error);
    }

private:
    uint32_t sensorIndex(OBSensorType sensorType) const {
        ob_error *error = nullptr;
        auto      count = ob_application_config_get_count(handle_, OB_APP_CONFIG_SENSORS, &error);
        Error::handle(&error);
        for(uint32_t i = 0; i < count; ++i) {
            auto current = static_cast<OBSensorType>(ob_application_config_get_int(handle_, OB_APP_CONFIG_ARRAY_ITEM(OB_APP_CONFIG_SENSOR_TYPE, i), &error));
            Error::handle(&error);
            if(current == sensorType) {
                return i;
            }
        }
        throw std::runtime_error("Application sensor config not found");
    }

    ob_application_config *handle_ = nullptr;
};

using ApplicationConfigPtr = std::shared_ptr<ApplicationConfig>;

}  // namespace ob
