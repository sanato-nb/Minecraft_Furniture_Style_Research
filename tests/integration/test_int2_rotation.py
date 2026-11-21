"""Independent model element AABB calculator tests."""
import math
from pathlib import Path
import runpy
import unittest

f=runpy.run_path(str(Path(__file__).resolve().parents[2]/"scripts/integration/audit_int2_rotation.py"))
corners=f["corner_bounds"]
analytic=f["center_extents_bounds"]
affine=f["affine"]


class RotationMathTests(unittest.TestCase):
    def assert_box(self, old, new):
        for a,b in zip(old[0]+old[1],new[0]+new[1]):
            self.assertAlmostEqual(a,b,places=9)

    def test_90_degree_y_square_aabb(self):
        # No rescale: a centered cube remains a centered cube for 90°.
        rotate={"origin":[8,8,8],"axis":"y","angle":90,"rescale":False}
        a=corners((0,0,0),(16,16,16),rotate)
        b=analytic((0,0,0),(16,16,16),rotate)
        self.assert_box(a,b)
        for low,high in zip(a[0],a[1]):
            self.assertAlmostEqual(low,0)
            self.assertAlmostEqual(high,16)

    def test_45_degree_and_rescale(self):
        for axis in ("x","y","z"):
            for rescale in (True,False):
                rot={"origin":[8,8,8],"axis":axis,"angle":45,"rescale":rescale}
                a=corners((0,1,4),(16,14,13),rot)
                b=analytic((0,1,4),(16,14,13),rot)
                self.assert_box(a,b)

    def test_zero_thickness_and_inverted_coordinates(self):
        for angle in (-45,-22.5,0,22.5,45):
            r={"origin":[7,10,6],"axis":"x","angle":angle}
            self.assert_box(
                corners((10,8,12),(-2,8,17),r),
                analytic((10,8,12),(-2,8,17),r),
            )

    def test_unrotated_matches_original_coordinates(self):
        self.assertEqual(corners((0,0,0),(16,16,16),None),((0.,0.,0.),(16.,16.,16.)))

    def test_singular_rescale_fails(self):
        with self.assertRaises(ValueError):
            affine({"origin":[8,8,8],"axis":"y","angle":90,"rescale":True})


if __name__=="__main__":
    unittest.main()
