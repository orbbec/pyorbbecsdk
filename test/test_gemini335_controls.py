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
Gemini 335 sensor control (property get/set) tests.

Each test follows the pattern:
  1. Check property support — skip if unsupported (not fail)
  2. Disable relevant auto mode if needed
  3. Read current value
  4. Write a new value (±1 or toggled)
  5. Read back and assert equality
  6. Restore original value
  7. Re-enable auto mode

All original values are restored regardless of test outcome via fixtures.
"""

import pytest

from pyorbbecsdk import (
    OBPropertyID,
    OBPermissionType,
    OBError,
)

pytestmark = [pytest.mark.hardware, pytest.mark.gemini335]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _skip_if_unsupported(device, prop_id,
                          perm=OBPermissionType.PERMISSION_READ_WRITE):
    if not device.is_property_supported(prop_id, perm):
        pytest.skip(f"Property {prop_id} not supported or accessible on this device")


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

    def test_depth_exposure_get_set(self, gemini335_device,
                                    disable_depth_auto_exposure):
        """Depth exposure can be read and written when auto-exposure is off."""
        prop = OBPropertyID.OB_PROP_DEPTH_EXPOSURE_INT
        _skip_if_unsupported(gemini335_device, prop)

        current = gemini335_device.get_int_property(prop)
        assert current is not None

        lo, hi, step = _int_prop_range(gemini335_device, prop)
        step = step if step and step > 0 else 1
        new_val = _clamp(current + step, lo or 1, hi or current + step)
        if new_val == current and current > (lo or 0):
            new_val = current - step

        gemini335_device.set_int_property(prop, new_val)
        read_back = gemini335_device.get_int_property(prop)
        assert read_back == new_val, (
            f"Depth exposure set to {new_val}, but read back {read_back}"
        )
        gemini335_device.set_int_property(prop, current)

    def test_depth_gain_get_set(self, gemini335_device,
                                 disable_depth_auto_exposure):
        """Depth gain can be read and written."""
        prop = OBPropertyID.OB_PROP_DEPTH_GAIN_INT
        _skip_if_unsupported(gemini335_device, prop)

        current = gemini335_device.get_int_property(prop)
        lo, hi, step = _int_prop_range(gemini335_device, prop)
        step = step if step and step > 0 else 1
        new_val = _clamp(current + step, lo or 1, hi or current + step)
        if new_val == current:
            new_val = _clamp(current - step, lo or 0, hi or current)

        gemini335_device.set_int_property(prop, new_val)
        assert gemini335_device.get_int_property(prop) == new_val
        gemini335_device.set_int_property(prop, current)

    def test_depth_auto_exposure_toggle(self, gemini335_device):
        """Depth auto-exposure bool can be toggled on/off."""
        prop = OBPropertyID.OB_PROP_DEPTH_AUTO_EXPOSURE_BOOL
        _skip_if_unsupported(gemini335_device, prop)

        original = gemini335_device.get_bool_property(prop)
        gemini335_device.set_bool_property(prop, not original)
        assert gemini335_device.get_bool_property(prop) == (not original)
        gemini335_device.set_bool_property(prop, original)

    def test_depth_mirror_toggle(self, gemini335_device):
        """Depth mirror property can be toggled."""
        prop = OBPropertyID.OB_PROP_DEPTH_MIRROR_BOOL
        _skip_if_unsupported(gemini335_device, prop)

        original = gemini335_device.get_bool_property(prop)
        gemini335_device.set_bool_property(prop, not original)
        assert gemini335_device.get_bool_property(prop) == (not original)
        gemini335_device.set_bool_property(prop, original)

    def test_depth_flip_toggle(self, gemini335_device):
        """Depth flip property can be toggled."""
        prop = OBPropertyID.OB_PROP_DEPTH_FLIP_BOOL
        _skip_if_unsupported(gemini335_device, prop)

        original = gemini335_device.get_bool_property(prop)
        gemini335_device.set_bool_property(prop, not original)
        assert gemini335_device.get_bool_property(prop) == (not original)
        gemini335_device.set_bool_property(prop, original)


# ---------------------------------------------------------------------------
# Color controls
# ---------------------------------------------------------------------------

class TestColorControls:

    def test_color_exposure_get_set(self, gemini335_device,
                                    disable_color_auto_exposure):
        """Color exposure can be read and written when auto-exposure is off."""
        prop = OBPropertyID.OB_PROP_COLOR_EXPOSURE_INT
        _skip_if_unsupported(gemini335_device, prop)

        current = gemini335_device.get_int_property(prop)
        lo, hi, step = _int_prop_range(gemini335_device, prop)
        step = step if step and step > 0 else 1
        new_val = _clamp(current + step, lo or 1, hi or current + step)
        if new_val == current:
            new_val = _clamp(current - step, lo or 0, hi or current)

        gemini335_device.set_int_property(prop, new_val)
        assert gemini335_device.get_int_property(prop) == new_val
        gemini335_device.set_int_property(prop, current)

    def test_color_gain_get_set(self, gemini335_device,
                                 disable_color_auto_exposure):
        """Color gain can be read and written."""
        prop = OBPropertyID.OB_PROP_COLOR_GAIN_INT
        _skip_if_unsupported(gemini335_device, prop)

        current = gemini335_device.get_int_property(prop)
        lo, hi, step = _int_prop_range(gemini335_device, prop)
        step = step if step and step > 0 else 1
        new_val = _clamp(current + step, lo or 1, hi or current + step)
        if new_val == current:
            new_val = _clamp(current - step, lo or 0, hi or current)

        gemini335_device.set_int_property(prop, new_val)
        assert gemini335_device.get_int_property(prop) == new_val
        gemini335_device.set_int_property(prop, current)

    def test_color_auto_exposure_toggle(self, gemini335_device):
        """Color auto-exposure bool can be toggled."""
        prop = OBPropertyID.OB_PROP_COLOR_AUTO_EXPOSURE_BOOL
        _skip_if_unsupported(gemini335_device, prop)

        original = gemini335_device.get_bool_property(prop)
        gemini335_device.set_bool_property(prop, not original)
        assert gemini335_device.get_bool_property(prop) == (not original)
        gemini335_device.set_bool_property(prop, original)

    def test_color_auto_white_balance_toggle(self, gemini335_device):
        """Color auto white balance can be toggled."""
        prop = OBPropertyID.OB_PROP_COLOR_AUTO_WHITE_BALANCE_BOOL
        _skip_if_unsupported(gemini335_device, prop)

        original = gemini335_device.get_bool_property(prop)
        gemini335_device.set_bool_property(prop, not original)
        assert gemini335_device.get_bool_property(prop) == (not original)
        gemini335_device.set_bool_property(prop, original)

    def test_color_brightness_get_set(self, gemini335_device):
        """Color brightness can be read and written."""
        prop = OBPropertyID.OB_PROP_COLOR_BRIGHTNESS_INT
        _skip_if_unsupported(gemini335_device, prop)

        current = gemini335_device.get_int_property(prop)
        lo, hi, step = _int_prop_range(gemini335_device, prop)
        step = step if step and step > 0 else 1
        new_val = _clamp(current + step, lo or -64, hi or 64)
        if new_val == current:
            new_val = _clamp(current - step, lo or -64, hi or 64)

        gemini335_device.set_int_property(prop, new_val)
        assert gemini335_device.get_int_property(prop) == new_val
        gemini335_device.set_int_property(prop, current)

    def test_color_contrast_get_set(self, gemini335_device):
        """Color contrast can be read and written."""
        prop = OBPropertyID.OB_PROP_COLOR_CONTRAST_INT
        _skip_if_unsupported(gemini335_device, prop)

        current = gemini335_device.get_int_property(prop)
        lo, hi, step = _int_prop_range(gemini335_device, prop)
        step = step if step and step > 0 else 1
        new_val = _clamp(current + step, lo or 0, hi or 100)
        if new_val == current:
            new_val = _clamp(current - step, lo or 0, hi or 100)

        gemini335_device.set_int_property(prop, new_val)
        assert gemini335_device.get_int_property(prop) == new_val
        gemini335_device.set_int_property(prop, current)

    def test_color_sharpness_get_set(self, gemini335_device):
        """Color sharpness can be read and written."""
        prop = OBPropertyID.OB_PROP_COLOR_SHARPNESS_INT
        _skip_if_unsupported(gemini335_device, prop)

        current = gemini335_device.get_int_property(prop)
        lo, hi, step = _int_prop_range(gemini335_device, prop)
        step = step if step and step > 0 else 1
        new_val = _clamp(current + step, lo or 0, hi or 100)
        if new_val == current:
            new_val = _clamp(current - step, lo or 0, hi or 100)

        gemini335_device.set_int_property(prop, new_val)
        assert gemini335_device.get_int_property(prop) == new_val
        gemini335_device.set_int_property(prop, current)

    def test_color_hue_get_set(self, gemini335_device):
        """Color hue can be read and written."""
        prop = OBPropertyID.OB_PROP_COLOR_HUE_INT
        _skip_if_unsupported(gemini335_device, prop)

        current = gemini335_device.get_int_property(prop)
        lo, hi, step = _int_prop_range(gemini335_device, prop)
        step = step if step and step > 0 else 1
        new_val = _clamp(current + step, lo or -180, hi or 180)
        if new_val == current:
            new_val = _clamp(current - step, lo or -180, hi or 180)

        gemini335_device.set_int_property(prop, new_val)
        assert gemini335_device.get_int_property(prop) == new_val
        gemini335_device.set_int_property(prop, current)

    def test_color_mirror_toggle(self, gemini335_device):
        """Color mirror can be toggled."""
        prop = OBPropertyID.OB_PROP_COLOR_MIRROR_BOOL
        _skip_if_unsupported(gemini335_device, prop)

        original = gemini335_device.get_bool_property(prop)
        gemini335_device.set_bool_property(prop, not original)
        assert gemini335_device.get_bool_property(prop) == (not original)
        gemini335_device.set_bool_property(prop, original)

    def test_color_flip_toggle(self, gemini335_device):
        """Color flip can be toggled."""
        prop = OBPropertyID.OB_PROP_COLOR_FLIP_BOOL
        _skip_if_unsupported(gemini335_device, prop)

        original = gemini335_device.get_bool_property(prop)
        gemini335_device.set_bool_property(prop, not original)
        assert gemini335_device.get_bool_property(prop) == (not original)
        gemini335_device.set_bool_property(prop, original)


# ---------------------------------------------------------------------------
# IR controls
# ---------------------------------------------------------------------------

class TestIRControls:

    def test_ir_exposure_get_set(self, gemini335_device,
                                  disable_ir_auto_exposure):
        """IR exposure can be read and written when auto-exposure is off."""
        prop = OBPropertyID.OB_PROP_IR_EXPOSURE_INT
        _skip_if_unsupported(gemini335_device, prop)

        current = gemini335_device.get_int_property(prop)
        lo, hi, step = _int_prop_range(gemini335_device, prop)
        step = step if step and step > 0 else 1
        new_val = _clamp(current + step, lo or 1, hi or current + step)
        if new_val == current:
            new_val = _clamp(current - step, lo or 0, hi or current)

        gemini335_device.set_int_property(prop, new_val)
        assert gemini335_device.get_int_property(prop) == new_val
        gemini335_device.set_int_property(prop, current)

    def test_ir_gain_get_set(self, gemini335_device,
                              disable_ir_auto_exposure):
        """IR gain can be read and written."""
        prop = OBPropertyID.OB_PROP_IR_GAIN_INT
        _skip_if_unsupported(gemini335_device, prop)

        current = gemini335_device.get_int_property(prop)
        lo, hi, step = _int_prop_range(gemini335_device, prop)
        step = step if step and step > 0 else 1
        new_val = _clamp(current + step, lo or 1, hi or current + step)
        if new_val == current:
            new_val = _clamp(current - step, lo or 0, hi or current)

        gemini335_device.set_int_property(prop, new_val)
        assert gemini335_device.get_int_property(prop) == new_val
        gemini335_device.set_int_property(prop, current)

    def test_ir_auto_exposure_toggle(self, gemini335_device):
        """IR auto-exposure can be toggled."""
        prop = OBPropertyID.OB_PROP_IR_AUTO_EXPOSURE_BOOL
        _skip_if_unsupported(gemini335_device, prop)

        original = gemini335_device.get_bool_property(prop)
        gemini335_device.set_bool_property(prop, not original)
        assert gemini335_device.get_bool_property(prop) == (not original)
        gemini335_device.set_bool_property(prop, original)

    def test_ir_mirror_toggle(self, gemini335_device):
        """IR mirror can be toggled."""
        prop = OBPropertyID.OB_PROP_IR_MIRROR_BOOL
        _skip_if_unsupported(gemini335_device, prop)

        original = gemini335_device.get_bool_property(prop)
        gemini335_device.set_bool_property(prop, not original)
        assert gemini335_device.get_bool_property(prop) == (not original)
        gemini335_device.set_bool_property(prop, original)

    def test_ir_flip_toggle(self, gemini335_device):
        """IR flip can be toggled."""
        prop = OBPropertyID.OB_PROP_IR_FLIP_BOOL
        _skip_if_unsupported(gemini335_device, prop)

        original = gemini335_device.get_bool_property(prop)
        gemini335_device.set_bool_property(prop, not original)
        assert gemini335_device.get_bool_property(prop) == (not original)
        gemini335_device.set_bool_property(prop, original)


# ---------------------------------------------------------------------------
# Laser / illuminator controls
# ---------------------------------------------------------------------------

class TestLaserControls:

    def test_laser_enable_toggle(self, gemini335_device):
        """Laser illuminator can be toggled on/off."""
        prop = OBPropertyID.OB_PROP_LASER_BOOL
        _skip_if_unsupported(gemini335_device, prop)

        original = gemini335_device.get_bool_property(prop)
        gemini335_device.set_bool_property(prop, not original)
        assert gemini335_device.get_bool_property(prop) == (not original)
        # Always restore laser to original state
        gemini335_device.set_bool_property(prop, original)

    def test_ldp_enable_toggle(self, gemini335_device):
        """LDP (Laser Dot Projector) can be toggled."""
        prop = OBPropertyID.OB_PROP_LDP_BOOL
        _skip_if_unsupported(gemini335_device, prop)

        original = gemini335_device.get_bool_property(prop)
        gemini335_device.set_bool_property(prop, not original)
        assert gemini335_device.get_bool_property(prop) == (not original)
        gemini335_device.set_bool_property(prop, original)

    def test_soft_filter_toggle(self, gemini335_device):
        """Software depth filter can be toggled."""
        prop = OBPropertyID.OB_PROP_DEPTH_SOFT_FILTER_BOOL
        _skip_if_unsupported(gemini335_device, prop)

        original = gemini335_device.get_bool_property(prop)
        gemini335_device.set_bool_property(prop, not original)
        assert gemini335_device.get_bool_property(prop) == (not original)
        gemini335_device.set_bool_property(prop, original)
