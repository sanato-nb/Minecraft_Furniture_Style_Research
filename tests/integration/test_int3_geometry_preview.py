"""Geometry-only diagrams never count as in-game visual or style verification."""
import sys
from pathlib import Path
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/"scripts/integration"))
from render_int3_chair_geometry import camera,cube_points,transform,FACE_CORNERS,ROLE_ORDER

class RawGeometryTests(unittest.TestCase):
    def test_cube_face_vertices(self):
        box={"a":[0,0,0],"b":[16,16,16],"axis":"","angle":0,"pivot":[8,8,8],"rescale":False}
        pts=cube_points(box)
        self.assertEqual(len(pts),8)
        self.assertEqual(pts[0],(0,0,0))
        self.assertEqual(pts[6],(16,16,16))
        self.assertEqual(len(FACE_CORNERS),6)
        self.assertTrue(all(len(v)==4 for v in FACE_CORNERS.values()))

    def test_zero_angle_does_not_displace_model(self):
        box={"axis":"y","angle":0,"pivot":[8,8,8],"rescale":False}
        self.assertEqual(transform((1,2,3),box),(1,2,3))

    def test_y_rotation_90_around_pivot(self):
        box={"axis":"y","angle":90,"pivot":[0,0,0],"rescale":False}
        x,y,z=transform((1,0,0),box)
        self.assertAlmostEqual(x,0,places=7)
        self.assertAlmostEqual(z,-1,places=7)

    def test_both_cameras_have_depth(self):
        a=camera((0,0,0),45)
        b=camera((1,5,3),45)
        self.assertNotEqual(a,b)

    def test_only_original_four_role_types(self):
        self.assertEqual(len(ROLE_ORDER),4)

if __name__=="__main__":unittest.main()
