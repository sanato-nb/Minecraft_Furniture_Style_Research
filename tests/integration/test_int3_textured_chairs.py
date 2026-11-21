"""Synthetic UV and original-source trace tests; no mod assets in fixtures."""
from pathlib import Path
import sys
import unittest
from PIL import Image

sys.path.insert(0,str(Path(__file__).resolve().parents[2]/"scripts/integration"))
import render_int3_textured_chairs as textured

class TextureQuadMapping(unittest.TestCase):
    def test_uv_rotation_produces_four_corner_permutation(self):
        u=(1,3,9,13)
        self.assertEqual(textured.uvs(u,0),[(1,3),(9,3),(9,13),(1,13)])
        self.assertEqual(textured.uvs(u,90),[(9,3),(9,13),(1,13),(1,3)])
        self.assertEqual(textured.uvs(u,180),[(9,13),(1,13),(1,3),(9,3)])
        self.assertEqual(textured.uvs(u,270),[(1,13),(1,3),(9,3),(9,13)])
        with self.assertRaises(ValueError):
            textured.uvs(u,45)

    def test_all_four_fixed_study_children_and_source_faces(self):
        self.assertEqual(textured.MODEL_KEYS,{
            "AF1393":"AF121","AF1394":"AF123",
            "HC13":"HC11210","MACAW1424":"MACAW67"
        })
        self.assertEqual(textured.EXPECTED_FACES,229)
        self.assertEqual(sum(textured.FACE_TOTALS.values()),229)

    def test_affine_source_pixel_quad_is_not_uniform_face_color(self):
        original=Image.new("RGBA",(16,16),(0,0,0,255))
        for x in range(16):
            for y in range(16):
                original.putpixel((x,y),(int(x*15),int(y*15),80,255))
        canvas=Image.new("RGBA",(128,128),(255,255,255,255))
        points=[(12,12),(112,12),(112,112),(12,112)]
        done=textured.polygon_texture(canvas,original,points,textured.uvs((0,0,16,16),0))
        self.assertEqual(done,1)
        self.assertLess(canvas.getpixel((20,20))[0],canvas.getpixel((100,20))[0])
        self.assertLess(canvas.getpixel((20,20))[1],canvas.getpixel((20,100))[1])

    def test_uv_reverse_preserves_original_axis_orientation(self):
        original=Image.new("RGBA",(16,16),(0,0,0,255))
        for x in range(16):
            for y in range(16):
                original.putpixel((x,y),(x*16,y*16,7,255))
        canvas=Image.new("RGBA",(128,128),(0,0,0,255))
        coords=[(0,0),(120,0),(120,120),(0,120)]
        textured.polygon_texture(canvas,original,coords,textured.uvs((16,0,0,16),0))
        self.assertGreater(canvas.getpixel((15,20))[0],canvas.getpixel((105,20))[0])

    def test_zero_area_uv_does_not_claim_valid_raster_geometry(self):
        canvas=Image.new("RGBA",(64,64),(255,255,255,255))
        src=Image.new("RGBA",(16,16),(0,0,0,255))
        self.assertEqual(textured.polygon_texture(canvas,src,[(0,0),(10,0),(20,0),(10,0)],
                         textured.uvs((0,0,16,16),0)),0)

    def test_camera_face_direction_not_fabricated_material(self):
        box={"angle":0,"axis":"","rescale":False,"pivot":(8,8,8)}
        self.assertTrue(textured.visible((0,0,1),box,0))
        self.assertFalse(textured.visible((0,0,-1),box,0))
        self.assertEqual(textured.YAW,(45,-135))

if __name__=="__main__":
    unittest.main()
