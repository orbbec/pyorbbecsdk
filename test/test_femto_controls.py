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
Femto Bolt / Femto Mega sensor control (property get/set) tests.

Femto control characteristics:
- Depth controls: exposure, gain, auto-exposure, mirror, flip
- Color controls: exposure, gain, AWB, brightness, contrast, mirror
- IR controls: not all properties apply to ToF IR
- Laser / flood controls: Femto uses a flood LED, not a dot projector
- No LDP (Laser Dot Projector) property on Femto

All properties are checked for support before testing;
unsupported properties are skipped gracefully.
"""

import pytest

from pyorbbecsdk import OBPermissionType, OBPropertyID

pytestmark = [pytest.mark.hardware, pytest.mark.femto, pytest.mark.functional]


def _skip_if_unsupported(device, prop_id, perm=OBPermissionType.PERMISSION_READ_WRITE):
    if not device.is_property_supported(prop_id, perm):
        pytest.skip(f"Property {prop_id} not supported on this Femto device")


def _int_prop_range(device, prop_id):
    try:
        r = device.get_int_property_range(prop_id)
        return r.min, r.max, r.step
    except Exception:
        return None, None, None


def _clamp(val, lo, hi):
    return max(lo, min(hi, val))


class TestFemtoDepthControls:

    def test_depth_exposure_get_set(self, femto_device, disable_depth_auto_exposure):
        prop = OBPropertyID.OB_PROP_DEPTH_EXPOSURE_INT
        _skip_if_unsupported(femto_device, prop)
        current = femto_device.get_int_property(prop)
        lo, hi, step = _int_prop_range(femto_device, prop)
        step = step if step and step > 0 else 1
        new_val = _clamp(current + step, lo or 1, hi or current + step)
        if new_val == current and current > (lo or 0):
            new_val = current - step
        femto_device.set_int_property(prop, new_val)
        assert femto_device.get_int_property(prop) == new_val
        femto_device.set_int_property(prop, current)

    def test_depth_auto_exposure_toggle(self, femto_device):
        prop = OBPropertyID.OB_PROP_DEPTH_AUTO_EXPOSURE_BOOL
        _skip_if_unsupported(femto_device, prop)
        original = femto_device.get_bool_property(prop)
        femto_device.set_bool_property(prop, not original)
        assert femto_device.get_bool_property(prop) == (not original)
        femto_device.set_bool_property(prop, original)

    def test_depth_mirror_toggle(self, femto_device):
        prop = OBPropertyID.OB_PROP_DEPTH_MIRROR_BOOL
        _skip_if_unsupported(femto_device, prop)
        original = femto_device.get_bool_property(prop)
        femto_device.set_bool_property(prop, not original)
        assert femto_device.get_bool_property(prop) == (not original)
        femto_device.set_bool_property(prop, original)

    def test_depth_flip_toggle(self, femto_device):
        prop = OBPropertyID.OB_PROP_DEPTH_FLIP_BOOL
        _skip_if_unsupported(femto_device, prop)
        original = femto_device.get_bool_property(prop)
        femto_device.set_bool_property(prop, not original)
        assert femto_device.get_bool_property(prop) == (not original)
        femto_device.set_bool_property(prop, original)


class TestFemtoColorControls:

    def test_color_exposure_get_set(self, femto_device, disable_color_auto_exposure):
        prop = OBPropertyID.OB_PROP_COLOR_EXPOSURE_INT
        _skip_if_unsupported(femto_device, prop)
        current = femto_device.get_int_property(prop)
        lo, hi, step = _int_prop_range(femto_device, prop)
        step = step if step and step > 0 else 1
        new_val = _clamp(current + step, lo or 1, hi or current + step)
        if new_val == current:
            new_val = _clamp(current - step, lo or 0, hi or current)
        femto_device.set_int_property(prop, new_val)
        assert femto_device.get_int_property(prop) == new_val
        femto_device.set_int_property(prop, current)

    def test_color_gain_get_set(self, femto_device, disable_color_auto_exposure):
        prop = OBPropertyID.OB_PROP_COLOR_GAIN_INT
        _skip_if_unsupported(femto_device, prop)
        current = femto_device.get_int_property(prop)
        lo, hi, step = _int_prop_range(femto_device, prop)
        step = step if step and step > 0 else 1
        new_val = _clamp(current + step, lo or 1, hi or current + step)
        if new_val == current:
            new_val = _clamp(current - step, lo or 0, hi or current)
        femto_device.set_int_property(prop, new_val)
        assert femto_device.get_int_property(prop) == new_val
        femto_device.set_int_property(prop, current)

    def test_color_auto_exposure_toggle(self, femto_device):
        prop = OBPropertyID.OB_PROP_COLOR_AUTO_EXPOSURE_BOOL
        _skip_if_unsupported(femto_device, prop)
        original = femto_device.get_bool_property(prop)
        femto_device.set_bool_property(prop, not original)
        assert femto_device.get_bool_property(prop) == (not original)
        femto_device.set_bool_property(prop, original)

    def test_color_auto_white_balance_toggle(self, femto_device):
        prop = OBPropertyID.OB_PROP_COLOR_AUTO_WHITE_BALANCE_BOOL
        _skip_if_unsupported(femto_device, prop)
        original = femto_device.get_bool_property(prop)
        femto_device.set_bool_property(prop, not original)
        assert femto_device.get_bool_property(prop) == (not original)
        femto_device.set_bool_property(prop, original)

    def test_color_brightness_get_set(self, femto_device):
        prop = OBPropertyID.OB_PROP_COLOR_BRIGHTNESS_INT
        _skip_if_unsupported(femto_device, prop)
        current = femto_device.get_int_property(prop)
        lo, hi, step = _int_prop_range(femto_device, prop)
        step = step if step and step > 0 else 1
        new_val = _clamp(current + step, lo or -64, hi or 64)
        if new_val == current:
            new_val = _clamp(current - step, lo or -64, hi or 64)
        femto_device.set_int_property(prop, new_val)
        assert femto_device.get_int_property(prop) == new_val
        femto_device.set_int_property(prop, current)

    def test_color_contrast_get_set(self, femto_device):
        prop = OBPropertyID.OB_PROP_COLOR_CONTRAST_INT
        _skip_if_unsupported(femto_device, prop)
        current = femto_device.get_int_property(prop)
        lo, hi, step = _int_prop_range(femto_device, prop)
        step = step if step and step > 0 else 1
        new_val = _clamp(current + step, lo or 0, hi or 100)
        if new_val == current:
            new_val = _clamp(current - step, lo or 0, hi or 100)
        femto_device.set_int_property(prop, new_val)
        assert femto_device.get_int_property(prop) == new_val
        femto_device.set_int_property(prop, current)

    def test_color_mirror_toggle(self, femto_device):
        prop = OBPropertyID.OB_PROP_COLOR_MIRROR_BOOL
        _skip_if_unsupported(femto_device, prop)
        original = femto_device.get_bool_property(prop)
        femto_device.set_bool_property(prop, not original)
        assert femto_device.get_bool_property(prop) == (not original)
        femto_device.set_bool_property(prop, original)


class TestFemtoLaserControls:
    """Femto uses a flood LED illuminator; OB_PROP_LASER_BOOL may map to it."""

    def test_laser_enable_toggle(self, femto_device):
        prop = OBPropertyID.OB_PROP_LASER_BOOL
        _skip_if_unsupported(femto_device, prop)
        original = femto_device.get_bool_property(prop)
        femto_device.set_bool_property(prop, not original)
        assert femto_device.get_bool_property(prop) == (not original)
        femto_device.set_bool_property(prop, original)
