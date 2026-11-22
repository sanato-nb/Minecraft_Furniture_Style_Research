import unittest

from mcfr.int4_bed_exterior import projected_tags, tag_matches


class ExteriorBedTests(unittest.TestCase):
    def test_upper_footboard_tags_preserve_camera_quadrants(self):
        points = projected_tags(840)
        self.assertEqual(points["nw_red"], (477, 440))
        self.assertEqual(points["se_yellow"], (547, 452))
        self.assertLess(points["nw_red"][0], points["ne_green"][0])
        self.assertLess(points["nw_red"][1], points["sw_blue"][1])

    def test_uv_classifier_rejects_wood_and_dark_pixels(self):
        self.assertTrue(tag_matches((130, 11, 12), "nw_red"))
        self.assertTrue(tag_matches((130, 125, 12), "se_yellow"))
        self.assertFalse(tag_matches((184, 148, 95), "se_yellow"))
        self.assertFalse(tag_matches((0, 0, 18), "sw_blue"))
