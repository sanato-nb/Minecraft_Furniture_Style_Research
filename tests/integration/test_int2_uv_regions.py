"""Independent ordinary 1-4 UV rectangle crop math."""
import runpy
import sys
from pathlib import Path
from fractions import Fraction
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[2]/"scripts/integration"))
obj=runpy.run_path(str(Path(__file__).resolve().parents[2]/"scripts/integration/audit_int2_uv_regions.py"))
box=obj["pixel_box"]


class OrdinaryUVPixelBoxTests(unittest.TestCase):
    def test_forward_rect(self):
        self.assertEqual(box(tuple(map(Fraction,[0,0,16,16])),16,16),(0,0,16,16))

    def test_reversed_rect(self):
        self.assertEqual(box(tuple(map(Fraction,[16,16,8,8])),32,32),(16,16,32,32))

    def test_fractional_crop_rounds_outward(self):
        uv=(Fraction(1,4),Fraction(1,4),Fraction(9,4),Fraction(9,4))
        self.assertEqual(box(uv,16,16),(0,0,3,3))

    def test_zero_area_uv_is_not_bogus_pixel_sample(self):
        with self.assertRaises(ValueError):
            box(tuple(map(Fraction,[8,1,8,16])),16,16)

    def test_outside_uv_cannot_enter_regular_region(self):
        with self.assertRaises(ValueError):
            box(tuple(map(Fraction,[-1,0,3,6])),16,16)


if __name__=="__main__":
    unittest.main()
