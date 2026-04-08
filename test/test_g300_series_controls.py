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
G300 series sensor control (property get/set) tests.

Covers: Gemini 330 / 335 / 335L / 335Le / 335Lg / 336 / 336L / 330L / 305 / 345

Each test:
  1. Checks property support — skips gracefully if not supported
  2. Disables relevant auto mode if needed (via fixture)
  3. Reads current value
  4. Writes a new value
  5. Reads back and asserts equality
  6. Restores original value

All G300 models share the same control API; per-model differences are
handled by is_property_supported() skipping unsupported properties.
"""

import pytest

from pyorbbecsdk import OBPermissionType, OBPropertyID

pytestmark = [pytest.mark.hardware, pytest.mark.g300_series, pytest.mark.functional]


def _skip_if_unsupported(device, prop_id, perm=OBPermissionType.PERMISSION_READ_WRITE):
    if not device.is_property_supported(prop_id, perm):
        pytest.skip(f"Property {prop_id} not supported on this device")


def _int_prop_range(device, prop_id):
    try:
        r = device.get_int_property_range(prop_id)
        return r.min, r.max, r.step
    except Exception:
        return None, None, None


def _clamp(val, lo, hi):
    return max(lo, min(hi, val))


# ---------------------------------------------------------------------------
# Depth controls
# ---------------------------------------------------------------------------


class TestDepthControls:

    def test_depth_exposure_get_set(self, g300_series_device, disable_depth_auto_exposure):
        prop = OBPropertyID.OB_PROP_DEPTH_EXPOSURE_INT
        _skip_if_unsupported(g300_series_device, prop)
        current = g300_series_device.get_int_property(prop)
        lo, hi, step = _int_prop_range(g300_series_device, prop)
        step = step if step and step > 0 else 1
        new_val = _clamp(current + step, lo or 1, hi or current + step)
        if new_val == current and current > (lo or 0):
            new_val = current - step
        g300_series_device.set_int_property(prop, new_val)
        assert g300_series_device.get_int_property(prop) == new_val
        g300_series_device.set_int_property(prop, current)

    def test_depth_gain_get_set(self, g300_series_device, disable_depth_auto_exposure):
        prop = OBPropertyID.OB_PROP_DEPTH_GAIN_INT
        _skip_if_unsupported(g300_series_device, prop)
        current = g300_series_device.get_int_property(prop)
        lo, hi, step = _int_prop_range(g300_series_device, prop)
        step = step if step and step > 0 else 1
        new_val = _clamp(current + step, lo or 1, hi or current + step)
        if new_val == current:
            new_val = _clamp(current - step, lo or 0, hi or current)
        g300_series_device.set_int_property(prop, new_val)
        assert g300_series_device.get_int_property(prop) == new_val
        g300_series_device.set_int_property(prop, current)

    def test_depth_auto_exposure_toggle(self, g300_series_device):
        prop = OBPropertyID.OB_PROP_DEPTH_AUTO_EXPOSURE_BOOL
        _skip_if_unsupported(g300_series_device, prop)
        original = g300_series_device.get_bool_property(prop)
        g300_series_device.set_bool_property(prop, not original)
        assert g300_series_device.get_bool_property(prop) == (not original)
        g300_series_device.set_bool_property(prop, original)

    def test_depth_mirror_toggle(self, g300_series_device):
        prop = OBPropertyID.OB_PROP_DEPTH_MIRROR_BOOL
        _skip_if_unsupported(g300_series_device, prop)
        original = g300_series_device.get_bool_property(prop)
        g300_series_device.set_bool_property(prop, not original)
        assert g300_series_device.get_bool_property(prop) == (not original)
        g300_series_device.set_bool_property(prop, original)

    def test_depth_flip_toggle(self, g300_series_device):
        prop = OBPropertyID.OB_PROP_DEPTH_FLIP_BOOL
        _skip_if_unsupported(g300_series_device, prop)
        original = g300_series_device.get_bool_property(prop)
        g300_series_device.set_bool_property(prop, not original)
        assert g300_series_device.get_bool_property(prop) == (not original)
        g300_series_device.set_bool_property(prop, original)

    def test_depth_soft_filter_toggle(self, g300_series_device):
        """Software depth filter (noise reduction) toggle."""
        prop = OBPropertyID.OB_PROP_DEPTH_SOFT_FILTER_BOOL
        _skip_if_unsupported(g300_series_device, prop)
        original = g300_series_device.get_bool_property(prop)
        g300_series_device.set_bool_property(prop, not original)
        assert g300_series_device.get_bool_property(prop) == (not original)
        g300_series_device.set_bool_property(prop, original)


# ---------------------------------------------------------------------------
# Color controls
# ---------------------------------------------------------------------------


class TestColorControls:

    def test_color_exposure_get_set(self, g300_series_device, disable_color_auto_exposure):
        prop = OBPropertyID.OB_PROP_COLOR_EXPOSURE_INT
        _skip_if_unsupported(g300_series_device, prop)
        current = g300_series_device.get_int_property(prop)
        lo, hi, step = _int_prop_range(g300_series_device, prop)
        step = step if step and step > 0 else 1
        new_val = _clamp(current + step, lo or 1, hi or current + step)
        if new_val == current:
            new_val = _clamp(current - step, lo or 0, hi or current)
        g300_series_device.set_int_property(prop, new_val)
        assert g300_series_device.get_int_property(prop) == new_val
        g300_series_device.set_int_property(prop, current)

    def test_color_gain_get_set(self, g300_series_device, disable_color_auto_exposure):
        prop = OBPropertyID.OB_PROP_COLOR_GAIN_INT
        _skip_if_unsupported(g300_series_device, prop)
        current = g300_series_device.get_int_property(prop)
        lo, hi, step = _int_prop_range(g300_series_device, prop)
        step = step if step and step > 0 else 1
        new_val = _clamp(current + step, lo or 1, hi or current + step)
        if new_val == current:
            new_val = _clamp(current - step, lo or 0, hi or current)
        g300_series_device.set_int_property(prop, new_val)
        assert g300_series_device.get_int_property(prop) == new_val
        g300_series_device.set_int_property(prop, current)

    def test_color_auto_exposure_toggle(self, g300_series_device):
        prop = OBPropertyID.OB_PROP_COLOR_AUTO_EXPOSURE_BOOL
        _skip_if_unsupported(g300_series_device, prop)
        original = g300_series_device.get_bool_property(prop)
        g300_series_device.set_bool_property(prop, not original)
        assert g300_series_device.get_bool_property(prop) == (not original)
        g300_series_device.set_bool_property(prop, original)

    def test_color_auto_white_balance_toggle(self, g300_series_device):
        prop = OBPropertyID.OB_PROP_COLOR_AUTO_WHITE_BALANCE_BOOL
        _skip_if_unsupported(g300_series_device, prop)
        original = g300_series_device.get_bool_property(prop)
        g300_series_device.set_bool_property(prop, not original)
        assert g300_series_device.get_bool_property(prop) == (not original)
        g300_series_device.set_bool_property(prop, original)

    def test_color_brightness_get_set(self, g300_series_device):
        prop = OBPropertyID.OB_PROP_COLOR_BRIGHTNESS_INT
        _skip_if_unsupported(g300_series_device, prop)
        current = g300_series_device.get_int_property(prop)
        lo, hi, step = _int_prop_range(g300_series_device, prop)
        step = step if step and step > 0 else 1
        new_val = _clamp(current + step, lo or -64, hi or 64)
        if new_val == current:
            new_val = _clamp(current - step, lo or -64, hi or 64)
        g300_series_device.set_int_property(prop, new_val)
        assert g300_series_device.get_int_property(prop) == new_val
        g300_series_device.set_int_property(prop, current)

    def test_color_contrast_get_set(self, g300_series_device):
        prop = OBPropertyID.OB_PROP_COLOR_CONTRAST_INT
        _skip_if_unsupported(g300_series_device, prop)
        current = g300_series_device.get_int_property(prop)
        lo, hi, step = _int_prop_range(g300_series_device, prop)
        step = step if step and step > 0 else 1
        new_val = _clamp(current + step, lo or 0, hi or 100)
        if new_val == current:
            new_val = _clamp(current - step, lo or 0, hi or 100)
        g300_series_device.set_int_property(prop, new_val)
        assert g300_series_device.get_int_property(prop) == new_val
        g300_series_device.set_int_property(prop, current)

    def test_color_sharpness_get_set(self, g300_series_device):
        prop = OBPropertyID.OB_PROP_COLOR_SHARPNESS_INT
        _skip_if_unsupported(g300_series_device, prop)
        current = g300_series_device.get_int_property(prop)
        lo, hi, step = _int_prop_range(g300_series_device, prop)
        step = step if step and step > 0 else 1
        new_val = _clamp(current + step, lo or 0, hi or 100)
        if new_val == current:
            new_val = _clamp(current - step, lo or 0, hi or 100)
        g300_series_device.set_int_property(prop, new_val)
        assert g300_series_device.get_int_property(prop) == new_val
        g300_series_device.set_int_property(prop, current)

    def test_color_hue_get_set(self, g300_series_device):
        prop = OBPropertyID.OB_PROP_COLOR_HUE_INT
        _skip_if_unsupported(g300_series_device, prop)
        current = g300_series_device.get_int_property(prop)
        lo, hi, step = _int_prop_range(g300_series_device, prop)
        step = step if step and step > 0 else 1
        new_val = _clamp(current + step, lo or -180, hi or 180)
        if new_val == current:
            new_val = _clamp(current - step, lo or -180, hi or 180)
        g300_series_device.set_int_property(prop, new_val)
        assert g300_series_device.get_int_property(prop) == new_val
        g300_series_device.set_int_property(prop, current)

    def test_color_mirror_toggle(self, g300_series_device):
        prop = OBPropertyID.OB_PROP_COLOR_MIRROR_BOOL
        _skip_if_unsupported(g300_series_device, prop)
        original = g300_series_device.get_bool_property(prop)
        g300_series_device.set_bool_property(prop, not original)
        assert g300_series_device.get_bool_property(prop) == (not original)
        g300_series_device.set_bool_property(prop, original)

    def test_color_flip_toggle(self, g300_series_device):
        prop = OBPropertyID.OB_PROP_COLOR_FLIP_BOOL
        _skip_if_unsupported(g300_series_device, prop)
        original = g300_series_device.get_bool_property(prop)
        g300_series_device.set_bool_property(prop, not original)
        assert g300_series_device.get_bool_property(prop) == (not original)
        g300_series_device.set_bool_property(prop, original)


# ---------------------------------------------------------------------------
# IR controls
# ---------------------------------------------------------------------------


class TestIRControls:

    def test_ir_exposure_get_set(self, g300_series_device, disable_ir_auto_exposure):
        prop = OBPropertyID.OB_PROP_IR_EXPOSURE_INT
        _skip_if_unsupported(g300_series_device, prop)
        current = g300_series_device.get_int_property(prop)
        lo, hi, step = _int_prop_range(g300_series_device, prop)
        step = step if step and step > 0 else 1
        new_val = _clamp(current + step, lo or 1, hi or current + step)
        if new_val == current:
            new_val = _clamp(current - step, lo or 0, hi or current)
        g300_series_device.set_int_property(prop, new_val)
        assert g300_series_device.get_int_property(prop) == new_val
        g300_series_device.set_int_property(prop, current)

    def test_ir_gain_get_set(self, g300_series_device, disable_ir_auto_exposure):
        prop = OBPropertyID.OB_PROP_IR_GAIN_INT
        _skip_if_unsupported(g300_series_device, prop)
        current = g300_series_device.get_int_property(prop)
        lo, hi, step = _int_prop_range(g300_series_device, prop)
        step = step if step and step > 0 else 1
        new_val = _clamp(current + step, lo or 1, hi or current + step)
        if new_val == current:
            new_val = _clamp(current - step, lo or 0, hi or current)
        g300_series_device.set_int_property(prop, new_val)
        assert g300_series_device.get_int_property(prop) == new_val
        g300_series_device.set_int_property(prop, current)

    def test_ir_auto_exposure_toggle(self, g300_series_device):
        prop = OBPropertyID.OB_PROP_IR_AUTO_EXPOSURE_BOOL
        _skip_if_unsupported(g300_series_device, prop)
        original = g300_series_device.get_bool_property(prop)
        g300_series_device.set_bool_property(prop, not original)
        assert g300_series_device.get_bool_property(prop) == (not original)
        g300_series_device.set_bool_property(prop, original)

    def test_ir_mirror_toggle(self, g300_series_device):
        prop = OBPropertyID.OB_PROP_IR_MIRROR_BOOL
        _skip_if_unsupported(g300_series_device, prop)
        original = g300_series_device.get_bool_property(prop)
        g300_series_device.set_bool_property(prop, not original)
        assert g300_series_device.get_bool_property(prop) == (not original)
        g300_series_device.set_bool_property(prop, original)

    def test_ir_flip_toggle(self, g300_series_device):
        prop = OBPropertyID.OB_PROP_IR_FLIP_BOOL
        _skip_if_unsupported(g300_series_device, prop)
        original = g300_series_device.get_bool_property(prop)
        g300_series_device.set_bool_property(prop, not original)
        assert g300_series_device.get_bool_property(prop) == (not original)
        g300_series_device.set_bool_property(prop, original)


# ---------------------------------------------------------------------------
# Laser / illuminator controls
# ---------------------------------------------------------------------------


class TestLaserControls:

    def test_laser_enable_toggle(self, g300_series_device):
        """Structured-light projector can be toggled."""
        prop = OBPropertyID.OB_PROP_LASER_BOOL
        _skip_if_unsupported(g300_series_device, prop)
        original = g300_series_device.get_bool_property(prop)
        g300_series_device.set_bool_property(prop, not original)
        assert g300_series_device.get_bool_property(prop) == (not original)
        g300_series_device.set_bool_property(prop, original)

    def test_ldp_enable_toggle(self, g300_series_device):
        """Laser Dot Projector (safety sensor) toggle."""
        prop = OBPropertyID.OB_PROP_LDP_BOOL
        _skip_if_unsupported(g300_series_device, prop)
        original = g300_series_device.get_bool_property(prop)
        g300_series_device.set_bool_property(prop, not original)
        assert g300_series_device.get_bool_property(prop) == (not original)
        g300_series_device.set_bool_property(prop, original)


# ---------------------------------------------------------------------------
# G300-series-specific: HDR controls (Gemini 330 / 335 / 336)
# ---------------------------------------------------------------------------


class TestHDRControls:

    def test_hdr_mode_toggle(self, g300_series_device):
        """HDR merge mode toggle — skipped on models that do not support it."""
        prop = OBPropertyID.OB_PROP_FRAME_INTERLEAVE_ENABLE_BOOL
        _skip_if_unsupported(g300_series_device, prop)
        original = g300_series_device.get_bool_property(prop)
        g300_series_device.set_bool_property(prop, not original)
        assert g300_series_device.get_bool_property(prop) == (not original)
        g300_series_device.set_bool_property(prop, original)
