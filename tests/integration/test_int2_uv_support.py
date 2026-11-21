"""C-followup independent UV support math regression tests."""
import runpy
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/"scripts/integration"))
from fractions import Fraction
from PIL import Image
import unittest

fn=runpy.run_path(str(Path(__file__).resolve().parents[2]/"scripts/integration/audit_int2_uv_support.py"))
axis=fn["axis_uv"]
pixels=fn["region_metrics"]


class SupplementalUVTests(unittest.TestCase):
    def test_clipped_fraction_inside_frame(self):
        a=axis(Fraction(-8),Fraction(8),16)
        self.assertEqual(a,(0,8,Fraction(1,2),"SPAN"))

    def test_line_on_texel_boundary(self):
        a=axis(Fraction(8),Fraction(8),16)
        self.assertEqual(a,(7,9,Fraction(1),"TEXEL_EDGE"))

    def test_touching_sprite_edge(self):
        a=axis(Fraction(-4),Fraction(0),16)
        self.assertEqual(a,(0,1,Fraction(0),"EDGE_CONTACT"))

    def test_uv_outside_source_sprite(self):
        self.assertIsNone(axis(Fraction(-9),Fraction(-1),16))
        self.assertIsNone(axis(Fraction(17),Fraction(21),16))

    def test_rgba_region_histogram(self):
        im=Image.new("RGBA",(2,2))
        im.putdata([(0,0,0,0),(1,2,3,255),(1,2,3,255),(9,9,9,200)])
        result=pixels(im)
        self.assertEqual([result[x] for x in ("transparent","partial_alpha","opaque")],[1,1,2])
        self.assertEqual(result["visible_rgb"],2)
        self.assertTrue(result["dominant_rgba"].startswith("010203ff:2"))


if __name__=="__main__":
    unittest.main()
