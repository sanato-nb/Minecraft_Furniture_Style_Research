"""Source geometry renderer must never pretend to approve semantic roles."""
import math
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

from mcfr import semantic_visual_evidence as v

class GeometryRenderUnitTests(unittest.TestCase):
    def test_rotated_point_same_as_original_c_axis_x(self):
        p=v.rotate_point((1,2,3),(0,0,0),"x",90,False)
        for actual,expected in zip(p,(1,-3,2)):
            self.assertAlmostEqual(actual,expected,places=7)

    def test_rotated_point_source_y_axis(self):
        p=v.rotate_point((1,2,3),(0,0,0),"y",90,False)
        self.assertAlmostEqual(p[0],-3)
        self.assertAlmostEqual(p[1],2)
        self.assertAlmostEqual(p[2],1)

    def test_rotated_point_rescale_as_original_c(self):
        p=v.rotate_point((4,4,0),(0,0,0),"z",45,True)
        self.assertAlmostEqual(p[0],0)
        self.assertAlmostEqual(p[1],8)

    def test_source_aabb_matches_axis_aligned_cube(self):
        sample={
            "provider_key":"A","element_index":0,
            "source_from":"1|2|3","source_to":"5|7|9",
            "pivot":"8|8|8","axis":"","angle":0,"rescale":0,
            "rotated_bbox":"1|2|3|5|7|9",
            "part_candidate":"UNDETERMINED","part_evidence":"GEOMETRY_ONLY"}
        result=v.build_element(sample)
        self.assertEqual(result["bounds"],(1,2,3,5,7,9))
        self.assertEqual(len(result["vertices"]),8)

    def test_corrupted_original_rotated_bbox_fails_closed(self):
        sample={
            "provider_key":"A","element_index":0,
            "source_from":"0|0|0","source_to":"3|4|5",
            "pivot":"0|0|0","axis":"y","angle":0,"rescale":0,
            "rotated_bbox":"0|0|0|3|4|6",
            "part_candidate":"SEAT_LAYER","part_evidence":"GEOMETRY_AND_FACE_SLOTS"}
        with self.assertRaises(ValueError):
            v.build_element(sample)

    def test_svg_both_views_parses_and_keeps_review_warning(self):
        example={
            "index":2,"role":"LEG_OR_LOWER_POST",
            "evidence":"GEOMETRY_AND_FACE_SLOTS",
            "vertices":v.corners((0,0,0),(2,8,2))
        }
        p1=v.svg_panel([example],"Original model",43,selected=2)
        p2=v.svg_panel([example],"Original model",223,selected=2)
        combo=v.svg_sheet([p1,p2],"Two projections")
        svg=ET.fromstring(combo)
        self.assertTrue(svg.tag.endswith("svg"))
        self.assertEqual(len(list(svg.iter("{http://www.w3.org/2000/svg}polygon"))),12)
        self.assertIn("HIGHLIGHT e2",combo)
        self.assertIn("Original model",combo)

    def test_never_generate_role_from_undetermined(self):
        example={"index":0,"role":"UNDETERMINED",
                 "evidence":"GEOMETRY_ONLY",
                 "vertices":v.corners((0,0,0),(1,1,1))}
        combined=v.svg_panel([example],"Neutral object",43)
        self.assertNotIn("SEAT_LAYER",combined)
        self.assertIn("textures intentionally omitted",combined)

    def test_template_registry_fixed_to_prior_four_providers(self):
        self.assertEqual(len(v.TEMPLATES),4)
        self.assertEqual(sum(mod=="AF" for mod,_,_ in v.TEMPLATES),2)
        self.assertEqual(sum(mod=="HC" for mod,_,_ in v.TEMPLATES),1)
        self.assertEqual(sum(mod=="MACAW" for mod,_,_ in v.TEMPLATES),1)

if __name__=="__main__":
    unittest.main()
