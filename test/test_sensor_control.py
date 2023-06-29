import unittest
from pyorbbecsdk import *


class SensorControlTest(unittest.TestCase):
    def setUp(self) -> None:
        self.context = Context()
        device_list = self.context.query_devices()
        self.assertIsNotNone(device_list)
        self.assertGreater(device_list.get_count(), 0)
        self.device = device_list.get_device_by_index(0)
        self.assertIsNotNone(self.device)
        self.pipeline = Pipeline(self.device)

    def tearDown(self) -> None:
        self.pipeline = None
        self.device = None
        self.context = None

    def turn_off_depth_auto_exposure(self):
        if not self.device.is_property_supported(OBPropertyID.OB_PROP_DEPTH_AUTO_EXPOSURE_BOOL,
                                                 OBPermissionType.PERMISSION_READ_WRITE):
            print("Current device not support depth auto exposure!")
            return
        self.device.set_bool_property(OBPropertyID.OB_PROP_DEPTH_AUTO_EXPOSURE_BOOL, False)

    def turn_on_depth_auto_exposure(self):
        if not self.device.is_property_supported(OBPropertyID.OB_PROP_DEPTH_AUTO_EXPOSURE_BOOL,
                                                 OBPermissionType.PERMISSION_READ_WRITE):
            print("Current device not support depth auto exposure!")
            return
        self.device.set_bool_property(OBPropertyID.OB_PROP_DEPTH_AUTO_EXPOSURE_BOOL, True)

    def turn_off_ir_auto_exposure(self):
        if not self.device.is_property_supported(OBPropertyID.OB_PROP_IR_AUTO_EXPOSURE_BOOL,
                                                 OBPermissionType.PERMISSION_READ_WRITE):
            print("Current device not support ir auto exposure!")
            return
        self.device.set_bool_property(OBPropertyID.OB_PROP_IR_AUTO_EXPOSURE_BOOL, False)

    def turn_on_ir_auto_exposure(self):
        if not self.device.is_property_supported(OBPropertyID.OB_PROP_IR_AUTO_EXPOSURE_BOOL,
                                                 OBPermissionType.PERMISSION_READ_WRITE):
            print("Current device not support ir auto exposure!")
            return
        self.device.set_bool_property(OBPropertyID.OB_PROP_IR_AUTO_EXPOSURE_BOOL, True)

    def turn_off_color_auto_exposure(self):
        if not self.device.is_property_supported(OBPropertyID.OB_PROP_COLOR_AUTO_EXPOSURE_BOOL,
                                                 OBPermissionType.PERMISSION_READ_WRITE):
            print("Current device not support color auto exposure!")
            return
        self.device.set_bool_property(OBPropertyID.OB_PROP_COLOR_AUTO_EXPOSURE_BOOL, False)

    def turn_on_color_auto_exposure(self):
        if not self.device.is_property_supported(OBPropertyID.OB_PROP_COLOR_AUTO_EXPOSURE_BOOL,
                                                 OBPermissionType.PERMISSION_READ_WRITE):
            print("Current device not support color auto exposure!")
            return
        self.device.set_bool_property(OBPropertyID.OB_PROP_COLOR_AUTO_EXPOSURE_BOOL, True)

    def test_get_and_set_ir_gain(self):
        if not self.device.is_property_supported(OBPropertyID.OB_PROP_IR_GAIN_INT,
                                                 OBPermissionType.PERMISSION_READ_WRITE):
            print("Current device not support ir gain!")
            return
        self.turn_off_ir_auto_exposure()
        curr_ir_gain = self.device.get_int_property(OBPropertyID.OB_PROP_IR_GAIN_INT)
        self.assertIsNotNone(curr_ir_gain)
        print("Current ir gain: ", curr_ir_gain)
        ir_gain = curr_ir_gain + 1
        self.device.set_int_property(OBPropertyID.OB_PROP_IR_GAIN_INT, ir_gain)
        new_ir_gain = self.device.get_int_property(OBPropertyID.OB_PROP_IR_GAIN_INT)
        self.assertIsNotNone(new_ir_gain)
        self.assertEqual(new_ir_gain, ir_gain)
        self.device.set_int_property(OBPropertyID.OB_PROP_IR_GAIN_INT, curr_ir_gain)
        self.turn_on_ir_auto_exposure()

    def test_get_and_set_color_gain(self):
        if not self.device.is_property_supported(OBPropertyID.OB_PROP_COLOR_GAIN_INT,
                                                 OBPermissionType.PERMISSION_READ_WRITE):
            print("Current device not support color gain!")
            return
        self.turn_off_color_auto_exposure()
        curr_color_gain = self.device.get_int_property(OBPropertyID.OB_PROP_COLOR_GAIN_INT)
        self.assertIsNotNone(curr_color_gain)
        print("Current color gain: ", curr_color_gain)
        color_gain = curr_color_gain + 1
        self.device.set_int_property(OBPropertyID.OB_PROP_COLOR_GAIN_INT, color_gain)
        new_color_gain = self.device.get_int_property(OBPropertyID.OB_PROP_COLOR_GAIN_INT)
        self.assertIsNotNone(new_color_gain)
        self.assertEqual(new_color_gain, color_gain)
        self.device.set_int_property(OBPropertyID.OB_PROP_COLOR_GAIN_INT, curr_color_gain)
        self.turn_on_color_auto_exposure()

    def test_get_and_set_depth_gain(self):
        if not self.device.is_property_supported(OBPropertyID.OB_PROP_DEPTH_GAIN_INT,
                                                 OBPermissionType.PERMISSION_READ_WRITE):
            print("Current device not support depth gain!")
            return
        self.turn_off_depth_auto_exposure()
        curr_depth_gain = self.device.get_int_property(OBPropertyID.OB_PROP_DEPTH_GAIN_INT)
        self.assertIsNotNone(curr_depth_gain)
        print("Current depth gain: ", curr_depth_gain)
        depth_gain = curr_depth_gain + 1
        self.device.set_int_property(OBPropertyID.OB_PROP_DEPTH_GAIN_INT, depth_gain)
        new_depth_gain = self.device.get_int_property(OBPropertyID.OB_PROP_DEPTH_GAIN_INT)
        self.assertIsNotNone(new_depth_gain)
        self.assertEqual(new_depth_gain, depth_gain)
        self.device.set_int_property(OBPropertyID.OB_PROP_DEPTH_GAIN_INT, curr_depth_gain)
        self.turn_on_depth_auto_exposure()

    def test_get_and_set_color_exposure(self):
        if not self.device.is_property_supported(OBPropertyID.OB_PROP_COLOR_EXPOSURE_INT,
                                                 OBPermissionType.PERMISSION_READ_WRITE):
            print("Current device not support color exposure!")
            return
        self.turn_off_color_auto_exposure()
        curr_color_exposure = self.device.get_int_property(OBPropertyID.OB_PROP_COLOR_EXPOSURE_INT)
        self.assertIsNotNone(curr_color_exposure)
        print("Current color exposure: ", curr_color_exposure)
        color_exposure = curr_color_exposure + 1
        self.device.set_int_property(OBPropertyID.OB_PROP_COLOR_EXPOSURE_INT, color_exposure)
        new_color_exposure = self.device.get_int_property(OBPropertyID.OB_PROP_COLOR_EXPOSURE_INT)
        self.assertIsNotNone(new_color_exposure)
        self.assertEqual(new_color_exposure, color_exposure)
        self.device.set_int_property(OBPropertyID.OB_PROP_COLOR_EXPOSURE_INT, curr_color_exposure)
        self.turn_on_color_auto_exposure()

    def test_get_and_set_ir_exposure(self):
        if not self.device.is_property_supported(OBPropertyID.OB_PROP_IR_EXPOSURE_INT,
                                                 OBPermissionType.PERMISSION_READ_WRITE):
            print("Current device not support ir exposure!")
            return
        self.turn_off_ir_auto_exposure()
        curr_ir_exposure = self.device.get_int_property(OBPropertyID.OB_PROP_IR_EXPOSURE_INT)
        self.assertIsNotNone(curr_ir_exposure)
        print("Current ir exposure: ", curr_ir_exposure)
        ir_exposure = curr_ir_exposure + 1
        self.device.set_int_property(OBPropertyID.OB_PROP_IR_EXPOSURE_INT, ir_exposure)
        new_ir_exposure = self.device.get_int_property(OBPropertyID.OB_PROP_IR_EXPOSURE_INT)
        self.assertIsNotNone(new_ir_exposure)
        self.assertEqual(new_ir_exposure, ir_exposure)
        self.device.set_int_property(OBPropertyID.OB_PROP_IR_EXPOSURE_INT, curr_ir_exposure)
        self.turn_on_ir_auto_exposure()

    def test_get_and_set_color_auto_white_balance(self):
        if not self.device.is_property_supported(OBPropertyID.OB_PROP_COLOR_AUTO_WHITE_BALANCE_BOOL,
                                                 OBPermissionType.PERMISSION_READ_WRITE):
            print("Current device not support color auto white balance!")
            return
        self.turn_on_color_auto_exposure()
        curr_color_auto_white_balance = self.device.get_bool_property(
            OBPropertyID.OB_PROP_COLOR_AUTO_WHITE_BALANCE_BOOL)
        self.assertIsNotNone(curr_color_auto_white_balance)
        print("Current color auto white balance: ", curr_color_auto_white_balance)
        color_auto_white_balance = not curr_color_auto_white_balance
        self.device.set_bool_property(OBPropertyID.OB_PROP_COLOR_AUTO_WHITE_BALANCE_BOOL,
                                      color_auto_white_balance)
        new_color_auto_white_balance = self.device.get_bool_property(
            OBPropertyID.OB_PROP_COLOR_AUTO_WHITE_BALANCE_BOOL)
        self.assertIsNotNone(new_color_auto_white_balance)
        self.assertEqual(new_color_auto_white_balance, color_auto_white_balance)
        self.device.set_bool_property(OBPropertyID.OB_PROP_COLOR_AUTO_WHITE_BALANCE_BOOL,
                                      curr_color_auto_white_balance)
        self.turn_off_color_auto_exposure()

    def test_get_and_set_ldp(self):
        if not self.device.is_property_supported(OBPropertyID.OB_PROP_LDP_BOOL,
                                                 OBPermissionType.PERMISSION_READ_WRITE):
            print("Current device not support LDP!")
            return
        curr_ldp = self.device.get_bool_property(OBPropertyID.OB_PROP_LDP_BOOL)
        self.assertIsNotNone(curr_ldp)
        print("Current LDP: ", curr_ldp)
        ldp = not curr_ldp
        self.device.set_bool_property(OBPropertyID.OB_PROP_LDP_BOOL, ldp)
        new_ldp = self.device.get_bool_property(OBPropertyID.OB_PROP_LDP_BOOL)
        self.assertIsNotNone(new_ldp)
        self.device.set_bool_property(OBPropertyID.OB_PROP_LDP_BOOL, curr_ldp)

    def test_get_and_set_laser(self):
        if not self.device.is_property_supported(OBPropertyID.OB_PROP_LASER_BOOL,
                                                 OBPermissionType.PERMISSION_READ_WRITE):
            print("Current device not support laser!")
            return
        curr_laser = self.device.get_bool_property(OBPropertyID.OB_PROP_LASER_BOOL)
        self.assertIsNotNone(curr_laser)
        print("Current laser: ", curr_laser)
        laser = not curr_laser
        self.device.set_bool_property(OBPropertyID.OB_PROP_LASER_BOOL, laser)
        new_laser = self.device.get_bool_property(OBPropertyID.OB_PROP_LASER_BOOL)
        self.assertIsNotNone(new_laser)
        self.assertEqual(new_laser, laser)
        self.device.set_bool_property(OBPropertyID.OB_PROP_LASER_BOOL, curr_laser)

    def test_get_and_set_flood(self):
        if not self.device.is_property_supported(OBPropertyID.OB_PROP_FLOOD_BOOL,
                                                 OBPermissionType.PERMISSION_READ_WRITE):
            print("Current device not support flood!")
            return
        curr_flood = self.device.get_bool_property(OBPropertyID.OB_PROP_FLOOD_BOOL)
        self.assertIsNotNone(curr_flood)
        print("Current flood: ", curr_flood)
        flood = not curr_flood
        self.device.set_bool_property(OBPropertyID.OB_PROP_FLOOD_BOOL, flood)
        new_flood = self.device.get_bool_property(OBPropertyID.OB_PROP_FLOOD_BOOL)
        self.assertIsNotNone(new_flood)
        self.assertEqual(new_flood, flood)
        self.device.set_bool_property(OBPropertyID.OB_PROP_FLOOD_BOOL, curr_flood)

    def test_get_and_set_soft_filter(self):
        if not self.device.is_property_supported(OBPropertyID.OB_PROP_DEPTH_SOFT_FILTER_BOOL,
                                                 OBPermissionType.PERMISSION_READ_WRITE):
            print("Current device not support soft filter!")
            return
        curr_soft_filter = self.device.get_bool_property(OBPropertyID.OB_PROP_DEPTH_SOFT_FILTER_BOOL)
        self.assertIsNotNone(curr_soft_filter)
        print("Current soft filter: ", curr_soft_filter)
        soft_filter = not curr_soft_filter
        self.device.set_bool_property(OBPropertyID.OB_PROP_DEPTH_SOFT_FILTER_BOOL, soft_filter)
        new_soft_filter = self.device.get_bool_property(OBPropertyID.OB_PROP_DEPTH_SOFT_FILTER_BOOL)
        self.assertIsNotNone(new_soft_filter)
        self.assertEqual(new_soft_filter, soft_filter)
        self.device.set_bool_property(OBPropertyID.OB_PROP_DEPTH_SOFT_FILTER_BOOL, curr_soft_filter)

    def test_get_and_set_color_mirror(self):
        if not self.device.is_property_supported(OBPropertyID.OB_PROP_COLOR_MIRROR_BOOL,
                                                 OBPermissionType.PERMISSION_READ_WRITE):
            print("Current device not support color mirror!")
            return
        curr_color_mirror = self.device.get_bool_property(OBPropertyID.OB_PROP_COLOR_MIRROR_BOOL)
        self.assertIsNotNone(curr_color_mirror)
        print("Current color mirror: ", curr_color_mirror)
        color_mirror = not curr_color_mirror
        self.device.set_bool_property(OBPropertyID.OB_PROP_COLOR_MIRROR_BOOL, color_mirror)
        new_color_mirror = self.device.get_bool_property(OBPropertyID.OB_PROP_COLOR_MIRROR_BOOL)
        self.assertIsNotNone(new_color_mirror)
        self.assertEqual(new_color_mirror, color_mirror)
        self.device.set_bool_property(OBPropertyID.OB_PROP_COLOR_MIRROR_BOOL, curr_color_mirror)

    def test_get_and_set_depth_mirror(self):
        if not self.device.is_property_supported(OBPropertyID.OB_PROP_DEPTH_MIRROR_BOOL,
                                                 OBPermissionType.PERMISSION_READ_WRITE):
            print("Current device not support depth mirror!")
            return
        curr_depth_mirror = self.device.get_bool_property(OBPropertyID.OB_PROP_DEPTH_MIRROR_BOOL)
        self.assertIsNotNone(curr_depth_mirror)
        print("Current depth mirror: ", curr_depth_mirror)
        depth_mirror = not curr_depth_mirror
        self.device.set_bool_property(OBPropertyID.OB_PROP_DEPTH_MIRROR_BOOL, depth_mirror)
        new_depth_mirror = self.device.get_bool_property(OBPropertyID.OB_PROP_DEPTH_MIRROR_BOOL)
        self.assertIsNotNone(new_depth_mirror)
        self.assertEqual(new_depth_mirror, depth_mirror)
        self.device.set_bool_property(OBPropertyID.OB_PROP_DEPTH_MIRROR_BOOL, curr_depth_mirror)

    def test_get_and_set_ir_mirror(self):
        if not self.device.is_property_supported(OBPropertyID.OB_PROP_IR_MIRROR_BOOL,
                                                 OBPermissionType.PERMISSION_READ_WRITE):
            print("Current device not support ir mirror!")
            return
        curr_ir_mirror = self.device.get_bool_property(OBPropertyID.OB_PROP_IR_MIRROR_BOOL)
        self.assertIsNotNone(curr_ir_mirror)
        print("Current ir mirror: ", curr_ir_mirror)
        ir_mirror = not curr_ir_mirror
        self.device.set_bool_property(OBPropertyID.OB_PROP_IR_MIRROR_BOOL, ir_mirror)
        new_ir_mirror = self.device.get_bool_property(OBPropertyID.OB_PROP_IR_MIRROR_BOOL)
        self.assertIsNotNone(new_ir_mirror)
        self.assertEqual(new_ir_mirror, ir_mirror)
        self.device.set_bool_property(OBPropertyID.OB_PROP_IR_MIRROR_BOOL, curr_ir_mirror)

    def test_get_and_set_color_auto_exposure(self):
        if not self.device.is_property_supported(OBPropertyID.OB_PROP_COLOR_AUTO_EXPOSURE_BOOL,
                                                 OBPermissionType.PERMISSION_READ_WRITE):
            print("Current device not support color auto exposure!")
            return
        curr_color_auto_exposure = self.device.get_bool_property(OBPropertyID.OB_PROP_COLOR_AUTO_EXPOSURE_BOOL)
        self.assertIsNotNone(curr_color_auto_exposure)
        print("Current color auto exposure: ", curr_color_auto_exposure)
        color_auto_exposure = not curr_color_auto_exposure
        self.device.set_bool_property(OBPropertyID.OB_PROP_COLOR_AUTO_EXPOSURE_BOOL, color_auto_exposure)
        new_color_auto_exposure = self.device.get_bool_property(OBPropertyID.OB_PROP_COLOR_AUTO_EXPOSURE_BOOL)
        self.assertIsNotNone(new_color_auto_exposure)
        self.assertEqual(new_color_auto_exposure, color_auto_exposure)
        self.device.set_bool_property(OBPropertyID.OB_PROP_COLOR_AUTO_EXPOSURE_BOOL, curr_color_auto_exposure)

    def test_get_and_set_depth_auto_exposure(self):
        if not self.device.is_property_supported(OBPropertyID.OB_PROP_DEPTH_AUTO_EXPOSURE_BOOL,
                                                 OBPermissionType.PERMISSION_READ_WRITE):
            print("Current device not support depth auto exposure!")
            return
        curr_depth_auto_exposure = self.device.get_bool_property(OBPropertyID.OB_PROP_DEPTH_AUTO_EXPOSURE_BOOL)
        self.assertIsNotNone(curr_depth_auto_exposure)
        print("Current depth auto exposure: ", curr_depth_auto_exposure)
        depth_auto_exposure = not curr_depth_auto_exposure
        self.device.set_bool_property(OBPropertyID.OB_PROP_DEPTH_AUTO_EXPOSURE_BOOL, depth_auto_exposure)
        new_depth_auto_exposure = self.device.get_bool_property(OBPropertyID.OB_PROP_DEPTH_AUTO_EXPOSURE_BOOL)
        self.assertIsNotNone(new_depth_auto_exposure)
        self.assertEqual(new_depth_auto_exposure, depth_auto_exposure)
        self.device.set_bool_property(OBPropertyID.OB_PROP_DEPTH_AUTO_EXPOSURE_BOOL, curr_depth_auto_exposure)

    def test_get_and_set_ir_auto_exposure(self):
        if not self.device.is_property_supported(OBPropertyID.OB_PROP_IR_AUTO_EXPOSURE_BOOL,
                                                 OBPermissionType.PERMISSION_READ_WRITE):
            print("Current device not support ir auto exposure!")
            return
        curr_ir_auto_exposure = self.device.get_bool_property(OBPropertyID.OB_PROP_IR_AUTO_EXPOSURE_BOOL)
        self.assertIsNotNone(curr_ir_auto_exposure)
        print("Current ir auto exposure: ", curr_ir_auto_exposure)
        ir_auto_exposure = not curr_ir_auto_exposure
        self.device.set_bool_property(OBPropertyID.OB_PROP_IR_AUTO_EXPOSURE_BOOL, ir_auto_exposure)
        new_ir_auto_exposure = self.device.get_bool_property(OBPropertyID.OB_PROP_IR_AUTO_EXPOSURE_BOOL)
        self.assertIsNotNone(new_ir_auto_exposure)
        self.assertEqual(new_ir_auto_exposure, ir_auto_exposure)
        self.device.set_bool_property(OBPropertyID.OB_PROP_IR_AUTO_EXPOSURE_BOOL, curr_ir_auto_exposure)

    def test_get_and_set_color_flip(self):
        if not self.device.is_property_supported(OBPropertyID.OB_PROP_COLOR_FLIP_BOOL,
                                                 OBPermissionType.PERMISSION_READ_WRITE):
            print("Current device not support color flip!")
            return
        curr_color_flip = self.device.get_bool_property(OBPropertyID.OB_PROP_COLOR_FLIP_BOOL)
        self.assertIsNotNone(curr_color_flip)
        print("Current color flip: ", curr_color_flip)
        color_flip = not curr_color_flip
        self.device.set_bool_property(OBPropertyID.OB_PROP_COLOR_FLIP_BOOL, color_flip)
        new_color_flip = self.device.get_bool_property(OBPropertyID.OB_PROP_COLOR_FLIP_BOOL)
        self.assertIsNotNone(new_color_flip)
        self.assertEqual(new_color_flip, color_flip)
        self.device.set_bool_property(OBPropertyID.OB_PROP_COLOR_FLIP_BOOL, curr_color_flip)

    def test_get_and_set_depth_flip(self):
        if not self.device.is_property_supported(OBPropertyID.OB_PROP_DEPTH_FLIP_BOOL,
                                                 OBPermissionType.PERMISSION_READ_WRITE):
            print("Current device not support depth flip!")
            return
        curr_depth_flip = self.device.get_bool_property(OBPropertyID.OB_PROP_DEPTH_FLIP_BOOL)
        self.assertIsNotNone(curr_depth_flip)
        print("Current depth flip: ", curr_depth_flip)
        depth_flip = not curr_depth_flip
        self.device.set_bool_property(OBPropertyID.OB_PROP_DEPTH_FLIP_BOOL, depth_flip)
        new_depth_flip = self.device.get_bool_property(OBPropertyID.OB_PROP_DEPTH_FLIP_BOOL)
        self.assertIsNotNone(new_depth_flip)
        self.assertEqual(new_depth_flip, depth_flip)
        self.device.set_bool_property(OBPropertyID.OB_PROP_DEPTH_FLIP_BOOL, curr_depth_flip)

    def test_get_and_set_ir_flip(self):
        if not self.device.is_property_supported(OBPropertyID.OB_PROP_IR_FLIP_BOOL,
                                                 OBPermissionType.PERMISSION_READ_WRITE):
            print("Current device not support ir flip!")
            return
        curr_ir_flip = self.device.get_bool_property(OBPropertyID.OB_PROP_IR_FLIP_BOOL)
        self.assertIsNotNone(curr_ir_flip)
        print("Current ir flip: ", curr_ir_flip)
        ir_flip = not curr_ir_flip
        self.device.set_bool_property(OBPropertyID.OB_PROP_IR_FLIP_BOOL, ir_flip)
        new_ir_flip = self.device.get_bool_property(OBPropertyID.OB_PROP_IR_FLIP_BOOL)
        self.assertIsNotNone(new_ir_flip)
        self.assertEqual(new_ir_flip, ir_flip)
        self.device.set_bool_property(OBPropertyID.OB_PROP_IR_FLIP_BOOL, curr_ir_flip)

    def test_get_and_set_color_sharpness(self):
        if not self.device.is_property_supported(OBPropertyID.OB_PROP_COLOR_SHARPNESS_INT,
                                                 OBPermissionType.PERMISSION_READ_WRITE):
            print("Current device not support color sharpness!")
            return
        self.turn_off_color_auto_exposure()
        curr_color_sharpness = self.device.get_int_property(OBPropertyID.OB_PROP_COLOR_SHARPNESS_INT)
        self.assertIsNotNone(curr_color_sharpness)
        print("Current color sharpness: ", curr_color_sharpness)
        color_sharpness = curr_color_sharpness + 1
        self.device.set_int_property(OBPropertyID.OB_PROP_COLOR_SHARPNESS_INT, color_sharpness)
        new_color_sharpness = self.device.get_int_property(OBPropertyID.OB_PROP_COLOR_SHARPNESS_INT)
        self.assertIsNotNone(new_color_sharpness)
        self.assertEqual(new_color_sharpness, color_sharpness)
        self.device.set_int_property(OBPropertyID.OB_PROP_COLOR_SHARPNESS_INT, curr_color_sharpness)
        self.turn_on_color_auto_exposure()

    def test_get_and_set_color_hue(self):
        if not self.device.is_property_supported(OBPropertyID.OB_PROP_COLOR_HUE_INT,
                                                 OBPermissionType.PERMISSION_READ_WRITE):
            print("Current device not support color hue!")
            return
        self.turn_off_color_auto_exposure()
        curr_color_hue = self.device.get_int_property(OBPropertyID.OB_PROP_COLOR_HUE_INT)
        self.assertIsNotNone(curr_color_hue)
        print("Current color hue: ", curr_color_hue)
        color_hue = curr_color_hue + 1
        self.device.set_int_property(OBPropertyID.OB_PROP_COLOR_HUE_INT, color_hue)
        new_color_hue = self.device.get_int_property(OBPropertyID.OB_PROP_COLOR_HUE_INT)
        self.assertIsNotNone(new_color_hue)
        self.assertEqual(new_color_hue, color_hue)
        self.device.set_int_property(OBPropertyID.OB_PROP_COLOR_HUE_INT, curr_color_hue)
        self.turn_on_color_auto_exposure()

    def test_get_and_set_color_contrast(self):
        if not self.device.is_property_supported(OBPropertyID.OB_PROP_COLOR_CONTRAST_INT,
                                                 OBPermissionType.PERMISSION_READ_WRITE):
            print("Current device not support color contrast!")
            return
        self.turn_off_color_auto_exposure()
        curr_color_contrast = self.device.get_int_property(OBPropertyID.OB_PROP_COLOR_CONTRAST_INT)
        self.assertIsNotNone(curr_color_contrast)
        print("Current color contrast: ", curr_color_contrast)
        color_contrast = curr_color_contrast + 1
        self.device.set_int_property(OBPropertyID.OB_PROP_COLOR_CONTRAST_INT, color_contrast)
        new_color_contrast = self.device.get_int_property(OBPropertyID.OB_PROP_COLOR_CONTRAST_INT)
        self.assertIsNotNone(new_color_contrast)
        self.assertEqual(new_color_contrast, color_contrast)
        self.device.set_int_property(OBPropertyID.OB_PROP_COLOR_CONTRAST_INT, curr_color_contrast)
        self.turn_on_color_auto_exposure()

    def test_get_and_set_color_brightness(self):
        if not self.device.is_property_supported(OBPropertyID.OB_PROP_COLOR_BRIGHTNESS_INT,
                                                 OBPermissionType.PERMISSION_READ_WRITE):
            print("Current device not support color brightness!")
            return
        self.turn_off_color_auto_exposure()
        curr_color_brightness = self.device.get_int_property(OBPropertyID.OB_PROP_COLOR_BRIGHTNESS_INT)
        self.assertIsNotNone(curr_color_brightness)
        print("Current color brightness: ", curr_color_brightness)
        color_brightness = curr_color_brightness + 1
        self.device.set_int_property(OBPropertyID.OB_PROP_COLOR_BRIGHTNESS_INT, color_brightness)
        new_color_brightness = self.device.get_int_property(OBPropertyID.OB_PROP_COLOR_BRIGHTNESS_INT)
        self.assertIsNotNone(new_color_brightness)
        self.assertEqual(new_color_brightness, color_brightness)
        self.device.set_int_property(OBPropertyID.OB_PROP_COLOR_BRIGHTNESS_INT, curr_color_brightness)
        self.turn_on_color_auto_exposure()

    def test_get_and_set_depth_work_mode(self):
        if not self.device.is_property_supported(OBPropertyID.OB_STRUCT_CURRENT_DEPTH_ALG_MODE,
                                                 OBPermissionType.PERMISSION_READ_WRITE):
            print("Current device not support depth work mode!")
            return
        curr_depth_work_mode = self.device.get_depth_work_mode()
        self.assertIsNotNone(curr_depth_work_mode)
        print("Current depth work mode: ", curr_depth_work_mode)
        depth_work_mode_list = self.device.get_depth_work_mode_list()
        self.assertIsNotNone(depth_work_mode_list)
        select_depth_work_mode = None
        for i in range(depth_work_mode_list.get_count()):
            depth_work_mode = depth_work_mode_list.get_depth_work_mode_by_index(i)
            print("depth_work_mode: ", depth_work_mode)
            if depth_work_mode != curr_depth_work_mode:
                select_depth_work_mode = depth_work_mode

        if select_depth_work_mode is None:
            print("Not found depth work mode!")
            return
        self.device.set_depth_work_mode(select_depth_work_mode)
        new_depth_work_mode = self.device.get_depth_work_mode()
        self.assertIsNotNone(new_depth_work_mode)
        self.assertEqual(new_depth_work_mode, select_depth_work_mode)
        self.device.set_depth_work_mode(curr_depth_work_mode)

    def test_get_and_set_fan_work_mode(self):
        if not self.device.is_property_supported(OBPropertyID.OB_PROP_FAN_WORK_MODE_INT,
                                                 OBPermissionType.PERMISSION_READ_WRITE):
            print("Current device not support fan work mode!")
            return
        curr_fan_work_mode = self.device.get_int_property(OBPropertyID.OB_PROP_FAN_WORK_MODE_INT)
        self.assertIsNotNone(curr_fan_work_mode)
        print("Current fan work mode: ", curr_fan_work_mode)
        fan_work_mode = not curr_fan_work_mode
        self.device.set_int_property(OBPropertyID.OB_PROP_FAN_WORK_MODE_INT, fan_work_mode)
        new_fan_work_mode = self.device.get_int_property(OBPropertyID.OB_PROP_FAN_WORK_MODE_INT)
        self.assertIsNotNone(new_fan_work_mode)
        self.assertEqual(new_fan_work_mode, fan_work_mode)
        self.device.set_int_property(OBPropertyID.OB_PROP_FAN_WORK_MODE_INT, curr_fan_work_mode)


if __name__ == '__main__':
    print("Start test SensorControl interface, Please make sure you have connected a device to your computer.")
    unittest.main()
