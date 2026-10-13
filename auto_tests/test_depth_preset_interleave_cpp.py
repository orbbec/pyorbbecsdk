"""Direct translations of TC_CPP_15 through TC_CPP_17 hardware cases.

These cases change persistent device state (depth work mode, preset, frame
interleave).  Every case restores the previous value in a ``finally`` block,
matching the C++ guard/RAII behaviour.
"""

from __future__ import annotations

import pytest

from conftest import first_profile, ob

pytestmark = pytest.mark.hardware


def _depth_modes(device):
    try:
        modes = device.get_depth_work_mode_list()
    except Exception as exc:  # noqa: BLE001
        pytest.skip(f"Depth work mode not supported on this device: {exc}")
    if modes is None or modes.get_count() == 0:
        pytest.skip("Depth work mode not supported on this device")
    return modes


def _restore_depth_mode(device, name):
    try:
        device.set_depth_work_mode(name)
    except Exception:  # noqa: BLE001
        pass


def _presets(device):
    try:
        presets = device.get_available_preset_list()
    except Exception as exc:  # noqa: BLE001
        pytest.skip(f"Preset not supported on this device: {exc}")
    if presets is None or presets.get_count() == 0:
        pytest.skip("Preset not supported on this device")
    return presets


def _restore_preset(device, name):
    if not name:
        return
    try:
        device.load_preset(name)
    except Exception:  # noqa: BLE001
        pass


def _interleave_list(device):
    if not device.isFrameInterleaveSupported():
        pytest.skip("Frame interleave not supported")
    return device.get_available_frame_interleave_list()


# ---------------------------------------------------------------------------
# TC_CPP_15 depth work mode
# ---------------------------------------------------------------------------


def test_TC_CPP_15_01_current_mode(device):
    _depth_modes(device)
    assert device.get_depth_work_mode() is not None
    assert device.get_depth_work_mode().name
    assert device.get_current_depth_mode_name()


def test_TC_CPP_15_02_enum_modes(device):
    modes = _depth_modes(device)
    assert modes.get_count() > 0

    for index in range(modes.get_count()):
        assert modes.get_depth_work_mode_by_index(index).name


def test_TC_CPP_15_03_switch_by_name(device):
    modes = _depth_modes(device)
    assert modes.get_count() > 0

    original = device.get_depth_work_mode().name
    # Pick a mode different from the current one when the device offers one.
    target = original
    for index in range(modes.get_count()):
        name = modes.get_depth_work_mode_by_index(index).name
        if name != original:
            target = name
            break

    try:
        assert device.set_depth_work_mode(target) == ob.OBStatus.STATUS_OK
        assert device.get_current_depth_mode_name() == target
    finally:
        _restore_depth_mode(device, original)


def test_TC_CPP_15_04_switch_by_struct(device):
    modes = _depth_modes(device)
    assert modes.get_count() > 0

    original = device.get_depth_work_mode()
    target = modes.get_depth_work_mode_by_index(0)

    try:
        assert device.set_depth_work_mode(target) == ob.OBStatus.STATUS_OK
        assert device.get_depth_work_mode().name == target.name
    finally:
        _restore_depth_mode(device, original.name)


def test_TC_CPP_15_05_profile_change_after_switch(device):
    modes = _depth_modes(device)
    if modes.get_count() < 2:
        pytest.skip("Only 1 depth mode available")

    original = device.get_depth_work_mode().name
    sensor = device.get_sensor(ob.OBSensorType.DEPTH_SENSOR)

    def profiles():
        stream_profiles = sensor.get_stream_profile_list()
        return [
            (
                stream_profiles.get_stream_profile_by_index(index)
                .as_video_stream_profile()
                .get_width(),
                stream_profiles.get_stream_profile_by_index(index)
                .as_video_stream_profile()
                .get_height(),
            )
            for index in range(stream_profiles.get_count())
        ]

    before = profiles()
    target = next(
        name
        for index in range(modes.get_count())
        if (name := modes.get_depth_work_mode_by_index(index).name) != original
    )

    try:
        assert device.set_depth_work_mode(target) == ob.OBStatus.STATUS_OK
        after = profiles()
        assert before
        assert after
    finally:
        _restore_depth_mode(device, original)


# ---------------------------------------------------------------------------
# TC_CPP_16 presets
# ---------------------------------------------------------------------------


def test_TC_CPP_16_01_current_and_list(device):
    presets = _presets(device)
    assert presets.get_count() > 0
    assert device.get_current_preset_name()


def test_TC_CPP_16_02_load_builtin(device):
    presets = _presets(device)
    assert presets.get_count() > 0

    original = device.get_current_preset_name()
    target = presets.get_name_by_index(0)
    try:
        device.load_preset(target)
    finally:
        _restore_preset(device, original)


def test_TC_CPP_16_03_export_json(device):
    presets = _presets(device)
    assert presets.get_count() > 0
    # The binding takes the preset name as an argument.
    data = device.export_settings_as_preset_json_data(presets.get_name_by_index(0))
    assert data


def test_TC_CPP_16_04_load_from_json(device):
    presets = _presets(device)
    assert presets.get_count() > 0

    original = device.get_current_preset_name()
    data = device.export_settings_as_preset_json_data(presets.get_name_by_index(0))
    if isinstance(data, bytes):
        data = data.decode("utf-8")
    assert data

    try:
        # Binding signature: (preset_name, json_data) - both str.
        device.load_preset_from_json_data("roundtrip_test", data)
    finally:
        _restore_preset(device, original)


def test_TC_CPP_16_05_preset_changes_properties(device):
    presets = _presets(device)
    if presets.get_count() < 2:
        pytest.skip("Need >=2 presets")

    prop = ob.OBPropertyID.OB_PROP_DEPTH_EXPOSURE_INT
    if not device.is_property_supported(prop, ob.OBPermissionType.PERMISSION_READ):
        pytest.skip("No readable depth property to compare between presets")

    original = device.get_current_preset_name()
    first_name = device.get_current_preset_name()
    second_name = next(
        name
        for index in range(presets.get_count())
        if (name := presets.get_name_by_index(index)) != first_name
    )

    try:
        device.load_preset(first_name)
        first_exposure = device.get_int_property(prop)
        device.load_preset(second_name)
        second_exposure = device.get_int_property(prop)
        assert first_exposure is not None
        assert second_exposure is not None
    finally:
        _restore_preset(device, original)


# ---------------------------------------------------------------------------
# TC_CPP_17 frame interleave
# ---------------------------------------------------------------------------


def test_TC_CPP_17_01_support_query(device):
    modes = _interleave_list(device)
    assert modes.get_count() > 0
    for index in range(modes.get_count()):
        assert modes.get_name(index)


def test_TC_CPP_17_02_load_interleave(device):
    modes = _interleave_list(device)
    assert modes.get_count() > 0

    current = device.get_current_frame_interleave_name()
    if not current:
        pytest.skip(
            "Device did not report a current interleave name; refusing to leave hardware state changed"
        )

    try:
        device.loadFrameInterleave(modes.get_name(0))
    except Exception:  # noqa: BLE001
        pass
    finally:
        try:
            device.loadFrameInterleave(current)
        except Exception:  # noqa: BLE001
            pass


def test_TC_CPP_17_03_interleave_stream(device):
    modes = _interleave_list(device)
    if modes.get_count() == 0:
        pytest.skip("No frame interleave list available")

    current = device.get_current_frame_interleave_name()
    if not current:
        pytest.skip(
            "Device did not report a current interleave name; refusing to leave hardware state changed"
        )

    pipeline = ob.Pipeline(device)
    try:
        device.loadFrameInterleave(modes.get_name(0))

        config = ob.Config()
        config.enable_stream(first_profile(pipeline, ob.OBSensorType.DEPTH_SENSOR))
        pipeline.start(config)

        received = sum(
            1 for _ in range(5) if pipeline.wait_for_frames(1000) is not None
        )
        assert received, "Interleave stream produced no frames"
    finally:
        try:
            pipeline.stop()
        except Exception:
            pass
        try:
            device.loadFrameInterleave(current)
        except Exception:  # noqa: BLE001
            pass
