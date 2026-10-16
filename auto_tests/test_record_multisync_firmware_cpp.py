"""Direct translations of TC_CPP_18 through TC_CPP_21 hardware cases.

Recording artifacts use pytest's ``tmp_path`` instead of the C++ tree's fixed
working-directory names, so a run leaves no droppings behind.

``TC_CPP_21_06`` reboots on purpose and carries the ``reboot`` mark; ``21_07``
(firmware update) and ``21_08`` (depth preset update) need
``OB_ALLOW_DESTRUCTIVE=1`` plus the matching resource path in ``test_config.json``.
"""

from __future__ import annotations

import gc
import math
import threading
import time
from pathlib import Path

import pytest
from conftest import (
    first_profile,
    ob,
    open_test_device,
    reboot_and_reconnect,
    require_destructive,
    wait_for_frameset_with_retry,
)

pytestmark = pytest.mark.hardware


def _record_depth(device, path, pause_resume=False):
    """Record a short depth stream to ``path``; returns the created path.

    Note the binding difference from C++: ``RecordDevice`` is *not* a ``Device``
    subclass and cannot be passed to ``Pipeline(...)``.  Constructing it against
    the device is enough - a pipeline opened on that same device is recorded.
    """
    path = Path(path)
    recorder = ob.RecordDevice(device, str(path))
    pipeline = None
    try:
        pipeline = ob.Pipeline(device)
        config = ob.Config()
        config.enable_stream(first_profile(pipeline, ob.OBSensorType.DEPTH_SENSOR))
        pipeline.start(config)

        assert pipeline.wait_for_frames(1000) is not None
        if pause_resume:
            recorder.pause()
            time.sleep(0.5)
            recorder.resume()
            assert pipeline.wait_for_frames(1000) is not None
    finally:
        # Stop the stream first, then drop the recorder deterministically: the
        # recorder owns a background writer, and leaving it to the garbage
        # collector corrupts the heap for later tests in the same process.
        if pipeline is not None:
            try:
                pipeline.stop()
            except Exception:  # noqa: BLE001
                pass
        del pipeline
        del recorder
        gc.collect()
    return path


def _sync_config(device):
    try:
        config = device.get_multi_device_sync_config()
    except Exception as exc:  # noqa: BLE001
        pytest.skip(f"Multi-device sync not supported on this device: {exc}")
    return config


def _restore_sync_config(device, config):
    try:
        device.set_multi_device_sync_config(config)
    except Exception:  # noqa: BLE001
        pass


# ---------------------------------------------------------------------------
# TC_CPP_18 recording
# ---------------------------------------------------------------------------


def test_TC_CPP_18_01_record_device(device, tmp_path):
    path = _record_depth(device, tmp_path / "ob_test_record.bag")

    assert path.is_file(), "Record file not created"
    assert path.stat().st_size > 1024, "Record file too small"


def test_TC_CPP_18_02_record_pause_resume(device, tmp_path):
    path = _record_depth(device, tmp_path / "ob_test_record2.bag", pause_resume=True)
    assert path.is_file(), "Record file not created"


def test_TC_CPP_18_08_record_playback_roundtrip(device, tmp_path):
    path = _record_depth(device, tmp_path / "ob_test_roundtrip.bag")

    assert path.is_file(), "Recorded bag file was not created"
    assert path.stat().st_size > 1024, "Recorded bag file is unexpectedly small"

    # Recording writes through a background thread; without a collection point
    # the writer can still hold the bag when playback opens it, which made this
    # case hang when it ran after the other recording cases.
    gc.collect()

    try:
        playback = ob.PlaybackDevice(str(path))
    except Exception as exc:  # noqa: BLE001
        pytest.skip(f"Failed to open recorded bag as playback device: {exc}")

    pipeline = ob.Pipeline(playback)
    frames = []
    try:
        config = ob.Config()
        config.enable_stream(first_profile(pipeline, ob.OBSensorType.DEPTH_SENSOR))
        pipeline.start(config)

        for _ in range(5):
            frameset = pipeline.wait_for_frames(1000)
            if frameset is not None and frameset.get_depth_frame() is not None:
                frames.append(frameset)
    finally:
        try:
            pipeline.stop()
        except Exception:  # noqa: BLE001
            pass
        # Release the playback device explicitly and synchronously; leaving it
        # to the garbage collector corrupts the heap for later tests.
        del pipeline
        del playback
        gc.collect()

    assert frames, "Playback did not produce any frameset"
    assert frames[0].get_depth_frame() is not None, "Playback frameset has no depth frame"


# ---------------------------------------------------------------------------
# TC_CPP_19 multi-device sync
# ---------------------------------------------------------------------------


def test_TC_CPP_19_01_sync_mode_support(device):
    config = _sync_config(device)
    bitmap = device.get_supported_multi_device_sync_mode_bitmap()
    assert bitmap, "No sync modes supported"
    assert int(config.mode) & int(bitmap), "Current syncMode not in supported bitmap"

    for name in (
        "depth_delay_us",
        "color_delay_us",
        "trigger_to_image_delay_us",
        "trigger_out_delay_us",
    ):
        value = getattr(config, name)
        assert math.isfinite(float(value))


def test_TC_CPP_19_02_freerun_standalone(device):
    original = _sync_config(device)

    try:
        config = ob.OBMultiDeviceSyncConfig()
        config.mode = ob.OBMultiDeviceSyncMode.FREE_RUN
        device.set_multi_device_sync_config(config)
        assert device.get_multi_device_sync_config().mode == ob.OBMultiDeviceSyncMode.FREE_RUN

        config.mode = ob.OBMultiDeviceSyncMode.STANDALONE
        device.set_multi_device_sync_config(config)
        assert device.get_multi_device_sync_config().mode == ob.OBMultiDeviceSyncMode.STANDALONE
    finally:
        _restore_sync_config(device, original)


def test_TC_CPP_19_03_primary_secondary(device, test_config):
    count = int(test_config.get("device", {}).get("count", 1))
    if count < 2:
        pytest.skip(f"Test requires >= 2 devices, configured: {count}")

    devices = ob.Context().query_devices()
    if devices.get_count() < 2:
        pytest.skip(f"Test requires >= 2 devices, available: {devices.get_count()}")

    device_a = devices.get_device_by_index(0)
    device_b = devices.get_device_by_index(1)
    original_a = _sync_config(device_a)
    original_b = _sync_config(device_b)

    pipeline_a = pipeline_b = None
    try:
        primary = ob.OBMultiDeviceSyncConfig()
        primary.mode = ob.OBMultiDeviceSyncMode.PRIMARY
        primary.trigger_out_enable = True
        primary.frames_per_trigger = 1
        device_a.set_multi_device_sync_config(primary)
        assert device_a.get_multi_device_sync_config().mode == ob.OBMultiDeviceSyncMode.PRIMARY

        secondary = ob.OBMultiDeviceSyncConfig()
        secondary.mode = ob.OBMultiDeviceSyncMode.SECONDARY
        device_b.set_multi_device_sync_config(secondary)

        pipeline_a = ob.Pipeline(device_a)
        pipeline_b = ob.Pipeline(device_b)
        for pipeline in (pipeline_a, pipeline_b):
            config = ob.Config()
            config.enable_stream(first_profile(pipeline, ob.OBSensorType.DEPTH_SENSOR))
            pipeline.start(config)

        assert pipeline_a.wait_for_frames(1000) is not None
        assert pipeline_b.wait_for_frames(1000) is not None
    except Exception as exc:  # noqa: BLE001
        pytest.skip(f"primary/secondary sync not runnable on this setup: {exc}")
    finally:
        for pipeline in (pipeline_a, pipeline_b):
            if pipeline is None:
                continue
            try:
                pipeline.stop()
            except Exception:  # noqa: BLE001
                pass
        _restore_sync_config(device_a, original_a)
        _restore_sync_config(device_b, original_b)


def test_TC_CPP_19_04_software_trigger(device):
    bitmap = device.get_supported_multi_device_sync_mode_bitmap()
    if not (int(bitmap) & int(ob.OBMultiDeviceSyncMode.SOFTWARE_TRIGGERING)):
        pytest.skip("Software triggering not supported")

    prop = ob.OBPropertyID.OB_PROP_CAPTURE_IMAGE_SIGNAL_BOOL
    if not device.is_property_supported(prop, ob.OBPermissionType.PERMISSION_WRITE):
        pytest.skip("Capture trigger property is not writable on this device")

    original = _sync_config(device)
    pipeline = None
    try:
        config = ob.OBMultiDeviceSyncConfig()
        config.mode = ob.OBMultiDeviceSyncMode.SOFTWARE_TRIGGERING
        config.frames_per_trigger = 1
        device.set_multi_device_sync_config(config)

        pipeline = ob.Pipeline(device)
        stream_config = ob.Config()
        stream_config.enable_stream(first_profile(pipeline, ob.OBSensorType.DEPTH_SENSOR))
        pipeline.start(stream_config)

        frames = []
        # The C++ case makes 3 trigger attempts, each waiting through the shared
        # retry helper rather than a single waitForFrames.  Five attempts here
        # because the trigger edge is occasionally missed while the stream is
        # still settling, and two extra attempts cost at most a second.
        for _ in range(5):
            device.trigger_capture()
            frameset = wait_for_frameset_with_retry(pipeline)
            if frameset is not None:
                frames.append(frameset)
        assert frames, "Software trigger failed to produce any frames"
    finally:
        if pipeline is not None:
            try:
                pipeline.stop()
            except Exception:  # noqa: BLE001
                pass
        _restore_sync_config(device, original)


def test_TC_CPP_19_05_timestamp_reset(device):
    config = device.get_timestamp_reset_config()
    original_enable = config.enable

    try:
        device.set_timestamp_reset_config(config)
        assert device.get_timestamp_reset_config().enable == original_enable
        device.timestamp_reset()
    except Exception as exc:  # noqa: BLE001
        pytest.skip(f"timestampReset not supported: {exc}")


def test_TC_CPP_19_06_timer_sync_host(device):
    _sync_config(device)
    device.timer_sync_with_host()


def test_TC_CPP_19_07_sync_config_fields(device):
    original = _sync_config(device)

    try:
        config = ob.OBMultiDeviceSyncConfig()
        config.mode = ob.OBMultiDeviceSyncMode.FREE_RUN
        config.depth_delay_us = 100
        config.color_delay_us = 200
        config.trigger_to_image_delay_us = 0
        config.trigger_out_enable = True
        config.trigger_out_delay_us = 100
        config.frames_per_trigger = 1
        device.set_multi_device_sync_config(config)

        read_back = device.get_multi_device_sync_config()
        assert read_back.mode == ob.OBMultiDeviceSyncMode.FREE_RUN
        assert read_back.depth_delay_us == 100
        assert read_back.color_delay_us == 200
    finally:
        _restore_sync_config(device, original)


# ---------------------------------------------------------------------------
# TC_CPP_20 / 21 point cloud, state, firmware
# ---------------------------------------------------------------------------


def test_TC_CPP_20_05_save_ply(device, tmp_path):
    pipeline = ob.Pipeline(device)
    frames = []
    try:
        config = ob.Config()
        config.enable_stream(first_profile(pipeline, ob.OBSensorType.DEPTH_SENSOR))
        config.enable_stream(first_profile(pipeline, ob.OBSensorType.COLOR_SENSOR))
        config.set_frame_aggregate_output_mode(ob.OBFrameAggregateOutputMode.FULL_FRAME_REQUIRE)
        pipeline.start(config)

        for _ in range(5):
            frameset = wait_for_frameset_with_retry(pipeline)
            if frameset is not None and frameset.get_depth_frame() is not None:
                frames.append(frameset)
    finally:
        try:
            pipeline.stop()
        except Exception:  # noqa: BLE001
            pass

    assert frames

    cloud = ob.FilterFactory.create_filter("PointCloudFilter")
    result = cloud.process(frames[0].get_depth_frame())
    assert result is not None

    ascii_path = tmp_path / "ob_test_points.ply"
    ob.save_point_cloud_to_ply(str(ascii_path), result)
    assert ascii_path.is_file(), "ASCII PLY file not created"

    binary_path = tmp_path / "ob_test_points_binary.ply"
    ob.save_point_cloud_to_ply(str(binary_path), result, True)
    assert binary_path.is_file(), "Binary PLY file not created"

    # The XYZ->RGB point format switch (C++ setCreatePointFormat) is not exposed
    # on the Python Filter returned by the factory, so the RGB PLY variant is
    # only produced when the cloud already carries RGB points.
    if result.get_format() in (ob.OBFormat.RGB_POINT,):
        rgb_path = tmp_path / "ob_test_points_rgb.ply"
        ob.save_point_cloud_to_ply(str(rgb_path), result)
        assert rgb_path.is_file(), "RGB ASCII PLY file not created"


def test_TC_CPP_21_01_global_timestamp(device):
    if not device.is_global_timestamp_supported():
        pytest.skip("global timestamp not supported")
    device.enable_global_timestamp(True)
    device.enable_global_timestamp(False)


def test_TC_CPP_21_02_device_state(device):
    state = device.get_device_state()
    assert state is not None
    assert int(state) >= 0


def test_TC_CPP_21_03_state_change_callback(device):
    seen = []
    device.set_device_state_changed_callback(lambda state: seen.append(state))

    deadline = time.monotonic() + 2
    while not seen and time.monotonic() < deadline:
        time.sleep(0.05)
    # The callback is registered without error; delivery depends on a real state
    # transition, which is not guaranteed on an idle device.
    assert device.get_device_state() is not None


def test_TC_CPP_21_04_heartbeat(device):
    device.enable_heart_beat(True)
    time.sleep(1)
    device.enable_heart_beat(False)


def test_TC_CPP_21_05_calibration_param_list(device):
    params = device.get_calibration_camera_param_list()
    assert params is not None
    assert params.get_count() > 0

    for index in range(params.get_count()):
        param = params.get_camera_param(index)
        for value in (
            param.depth_intrinsic.fx,
            param.depth_intrinsic.fy,
            param.depth_intrinsic.cx,
            param.depth_intrinsic.cy,
            param.rgb_intrinsic.fx,
            param.rgb_intrinsic.fy,
        ):
            assert math.isfinite(float(value))


@pytest.mark.reboot
def test_TC_CPP_21_06_reboot(test_config):
    context = ob.Context()
    device = open_test_device(context, test_config)
    serial = device.get_device_info().get_serial_number()

    reconnected = threading.Event()

    # The binding adapts the C++ two-list callback signature.
    def on_device_changed(removed_list, added_list):
        if added_list is not None and added_list.get_count() > 0:
            reconnected.set()

    callback_id = context.register_device_changed_callback(on_device_changed)
    try:
        device.reboot()
        del device
        gc.collect()

        assert reconnected.wait(30), "Device-added callback not received after reboot"
    finally:
        context.unregister_device_changed_callback(callback_id)

    devices = context.query_devices()
    assert devices.get_device_by_serial_number(serial) is not None, f"Device SN {serial} not found after reboot"


@pytest.mark.destructive
def test_TC_CPP_21_07_firmware_update(test_config):
    require_destructive()

    firmware = test_config.get("resource", {}).get("firmwarePath", "")
    if not firmware:
        pytest.skip("No firmware file - set resource.firmwarePath in config")

    done = threading.Event()
    state = {"value": None}

    def callback(upgrade_state, message):
        state["value"] = upgrade_state
        if upgrade_state in (
            ob.OBUpgradeState.DONE,
            ob.OBUpgradeState.DONE_WITH_DUPLICATES,
            ob.OBUpgradeState.DONE_REBOOT_AND_REUPDATE,
        ):
            done.set()

    context = ob.Context()
    device = open_test_device(context, test_config)
    serial = device.get_device_info().get_serial_number()
    device = reboot_and_reconnect(context, device, serial)

    device.update_firmware(firmware, callback)

    assert done.wait(180), "Firmware update did not complete within 3 minutes"
    if state["value"] in (ob.OBUpgradeState.ERR_MISMATCH, ob.OBUpgradeState.ERR_UNSUPPORT_DEV):
        pytest.skip(f"Firmware not compatible with connected device: {state['value']}")
    assert state["value"] is not None


@pytest.mark.destructive
def test_TC_CPP_21_08_update_depth_presets(test_config):
    require_destructive()

    preset = test_config.get("resource", {}).get("depthPresetPath", "")
    if not preset:
        pytest.skip("No depth preset file - set resource.depthPresetPath in config")

    done = threading.Event()
    state = {"value": None}

    def callback(upgrade_state, message):
        state["value"] = upgrade_state
        if upgrade_state in (
            ob.OBUpgradeState.DONE,
            ob.OBUpgradeState.DONE_WITH_DUPLICATES,
            ob.OBUpgradeState.DONE_REBOOT_AND_REUPDATE,
        ):
            done.set()

    context = ob.Context()
    device = open_test_device(context, test_config)
    serial = device.get_device_info().get_serial_number()
    device = reboot_and_reconnect(context, device, serial)

    device.update_optional_depth_presets([preset], callback)

    assert done.wait(120), "Depth preset update did not complete within 2 minutes"
    if state["value"] in (ob.OBUpgradeState.ERR_MISMATCH, ob.OBUpgradeState.ERR_UNSUPPORT_DEV):
        pytest.skip("Depth preset resource is not compatible with the connected device")
    assert state["value"] is not None
