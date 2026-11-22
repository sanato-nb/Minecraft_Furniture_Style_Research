import unittest

from mcfr.int4_bed_exterior import OVERHEAD
from mcfr.int4_bed_uv_faces import FACES, project, texels


class BedUVFacesTests(unittest.TestCase):
    def test_view_projection_keeps_uv_quadrants_in_screen_order(self):
        bounds = {
            "footboard_south": [[0, 7, 13], [16, 9, 16]],
            "headboard_up": [[0, 14, -16], [16, 16, -13]],
            "sheet_east": [[1, 8, -3], [15, 11, 13]],
        }
        expected = {
            "footboard_south": [(474, 338), (558, 338), (474, 346), (558, 346)],
            "headboard_up": [(479, 262), (551, 262), (479, 275), (551, 275)],
            "sheet_east": [(467, 333), (494, 333), (467, 351), (494, 351)],
        }
        for key, (_, normal, view, uv, rotation, _) in FACES.items():
            with self.subTest(face=key):
                face = {"normal": normal, "view": view, "uv": uv,
                        "rotation": rotation, "bounds": bounds[key]}
                self.assertEqual([project(face, xy, 430.08, OVERHEAD)
                                  for xy in texels(key).values()], expected[key])
