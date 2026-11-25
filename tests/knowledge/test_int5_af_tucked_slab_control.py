"""INT-5 B4 source-state controls, mock frames NOT presented as real F2."""
from pathlib import Path
from tempfile import TemporaryDirectory
import io
import json
import unittest

from PIL import Image,ImageDraw

from mcfr import int5_af_tucked_slab_control as b4
from mcfr import chair_runtime_fixture as fixture


class TuckedSlabIndependentControls(unittest.TestCase):
    def test_pinned_north_tucked_source_without_illegal_slab_removal(self):
        c=b4.target_case()
        self.assertEqual(c.case_id,"AF123_north")
        self.assertEqual(c.state(),
          "another_furniture:acacia_chair[facing=north,tucked=true,variant=10]")
        self.assertEqual(b4.MODEL,"another_furniture:block/chair/acacia_10_tucked")
        self.assertEqual(b4.slab_xyz(),(c.x,c.y,c.z-1))
        self.assertEqual(b4.stage_slab_state("chair_plus_slab_before"),
                         "minecraft:oak_slab[type=top]")
        self.assertEqual(b4.stage_slab_state("chair_plus_slab_after"),
                         "minecraft:oak_slab[type=top]")
        self.assertEqual(b4.stage_slab_state("slab_only"),
                         "minecraft:oak_slab[type=top]")
        self.assertEqual(b4.stage_slab_state("empty"),"minecraft:air")
        self.assertEqual(b4.stage_chair_state("slab_only"),"minecraft:air")

    def test_source_fixture_places_slab_before_actual_tucked_chair(self):
        c=b4.target_case()
        cmds,verify=fixture.pack_lines("1.21.1",(c,))
        slab=f"setblock {c.x} {c.y} {c.z-1} minecraft:oak_slab[type=top]"
        chair=f"setblock {c.x} {c.y} {c.z} {c.state()}"
        self.assertIn(slab,cmds)
        self.assertIn(chair,cmds)
        self.assertLess(cmds.index(slab),cmds.index(chair))
        self.assertIn(c.state(),verify[0])

    def test_two_cameras_reference_same_world_block(self):
        cam=b4.cameras()
        self.assertEqual(set(cam),{"south","north"})
        self.assertEqual(cam["south"],b4.target_case().camera())
        self.assertTrue(cam["south"].endswith("180 20"))
        self.assertTrue(cam["north"].endswith("0 20"))
        self.assertEqual(cam["south"].split()[:2],cam["north"].split()[:2])

    def test_a_b_a_air_chair_only_and_slab_only_mask(self):
        def solid():
            return Image.new("RGB",(1024,684),(200,200,200))
        A,B,A2,air=solid(),solid(),solid(),solid()
        for im in (A,B,A2):
            ImageDraw.Draw(im).rectangle((480,400,540,445),fill=(150,110,75))
        for im in (A,A2):
            ImageDraw.Draw(im).rectangle((480,446,535,505),fill=(100,65,40))
        m=b4.measure(dict(chair_plus_slab_before=A,slab_only=B,
                          chair_plus_slab_after=A2,empty=air))
        self.assertGreater(m["chair_pixel_delta_with_slab_fixed"],50)
        self.assertGreater(m["slab_pixel_delta_with_chair_absent"],50)
        self.assertEqual(m["same_chair_state_temporal_delta"],0)
        self.assertGreater(m["chair_delta_minus_temporal"],50)

    def test_state_stage_and_geometry_fail_closed(self):
        with self.assertRaisesRegex(ValueError,"unknown real"):
            b4.stage_slab_state("chair_without_slab")
        with self.assertRaisesRegex(ValueError,"unknown real"):
            b4.label("top","chair_plus_slab_before")
        with self.assertRaisesRegex(ValueError,"dimensions mismatch"):
            b4.pixel_delta(Image.new("RGB",(10,10)),
                           Image.new("RGB",(10,10)))

    def test_no_unapproved_function_rights_or_hidden_chair_claim(self):
        src=Path(b4.__file__).read_text(encoding="utf-8")
        self.assertIn('"tucked_true_without_support_was_tested":False',src)
        self.assertIn('"new_individual_element_F2_pixel_identifications":0',src)
        self.assertIn('"new_element_function_approvals":0',src)
        self.assertIn('"INT6_training_redistribution_approvals":0',src)
        self.assertIn('"real client',src)

    def test_reject_bogus_original_game_manifest(self):
        with TemporaryDirectory() as d:
            (Path(d)/b4.ORIGINAL).write_text(
                json.dumps({"schema":"not true"}),encoding="utf-8")
            with self.assertRaisesRegex(ValueError,"invalid actual source manifest"):
                b4.audit(d)


if __name__=="__main__":
    unittest.main()
