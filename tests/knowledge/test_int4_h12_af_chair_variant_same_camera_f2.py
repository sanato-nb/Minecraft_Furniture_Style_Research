"""INT-4-H12 only source-pinned AF same-camera, repeated-control F2 contract.

Synthetic image tests cannot be counted as actual game F2.
"""
from pathlib import Path
import unittest
from tempfile import TemporaryDirectory
from PIL import Image,ImageDraw

from mcfr import int4_h12_af_chair_variant_same_camera_f2 as h
from mcfr.chair_runtime_fixture import make_pack,pack_lines

class H12AFSameCamera(unittest.TestCase):
    def test_model_and_runtime_original_pins(self):
        self.assertEqual(h.VERSION,"1.21.1")
        self.assertEqual(h.RELEASE_SHA1,"c2f992081bdc4795ed6d87771a3b5f7c71103785")
        self.assertEqual(h.SOURCE_GIT,"57eb624cbb7f408d43398c7434b0d38d312cb55d")
        self.assertEqual(h.H11_GIT_SHA1,"1869ee05afce779bd37233ba1cc74850d736160f")

    def test_original_fixed_north_variant1_case(self):
        v=h.original_case()
        self.assertEqual(len(v),1)
        self.assertEqual(v[0].state(),h.state("v1"))
        self.assertEqual((v[0].x,v[0].y,v[0].z),(0,120,40))
        self.assertEqual(v[0].camera(),h.POSE)

    def test_state_change_only_variant(self):
        self.assertEqual(h.state("v1"),"another_furniture:acacia_chair[facing=north,tucked=false,variant=1]")
        self.assertEqual(h.state("v3"),"another_furniture:acacia_chair[facing=north,tucked=false,variant=3]")
        with self.assertRaises(ValueError):h.state("sleep")

    def test_original_pack_does_not_stage_multiple_positions(self):
        placed,verified=pack_lines(h.VERSION,h.original_case())
        chair=[x for x in placed if x.startswith("setblock") and "acacia_chair" in x]
        self.assertEqual(len(chair),1)
        self.assertIn("variant=1",chair[0])
        self.assertEqual(sum("=PASS" in x for x in verified),1)

    def test_create_isolated_world_pack(self):
        with TemporaryDirectory() as d:
            p=Path(d)/"pack"
            info=make_pack(h.VERSION,p,selected_cases=h.original_case())
            self.assertEqual(info["test_cases"],1)
            self.assertIn("variant=1",(p/"data/mcfr_chair/function/place.mcfunction").read_text())
            self.assertNotIn("variant=3",(p/"data/mcfr_chair/function/place.mcfunction").read_text())

    def test_actual_four_game_F2_contract(self):
        self.assertEqual(h.FRAMES,("v1","v3","v1_repeat","air"))
        s=Path(h.__file__).read_text(encoding="utf-8")
        for line in ('verify("v1",state("v1"))','verify("v3",state("v3"))',
                     'verify("v1_repeat",state("v1"))','verify("air","minecraft:air")',
                     'snap("v1")','snap("v3")','snap("v1_repeat")','snap("air")'):
            self.assertIn(line,s)

    def test_different_image_and_repeat_baseline_pixel_math(self):
        with TemporaryDirectory() as temp:
            folder=Path(temp)
            a=Image.new("RGB",(1024,684),(210,214,225))
            b=a.copy()
            ImageDraw.Draw(a).rectangle((470,350,510,410),fill=(30,35,42))
            ImageDraw.Draw(b).rectangle((470,350,510,410),fill=(30,35,42))
            ImageDraw.Draw(b).rectangle((480,370,500,390),fill=(244,35,42))
            for key,im in [("v1",a),("v3",b),("v1_repeat",a),("air",Image.new("RGB",(1024,684),(210,214,225)))]:
                im.save(folder/(key+".png"))
            c=h.compare_frames(folder)
            self.assertGreaterEqual(c["variant1_vs_variant3_full_frame_pixels"],400)
            self.assertEqual(c["variant1_vs_variant1_repeat_pixels"],0)
            self.assertTrue(c["conservative_visible_model_difference"])
            self.assertFalse(c["actual_face_to_exact_GPU_texel_match_approved"])

    def test_no_visual_difference_must_be_conditional(self):
        with TemporaryDirectory() as temp:
            folder=Path(temp)
            a=Image.new("RGB",(1024,684),(30,45,66))
            for key in ("v1","v3","v1_repeat"):a.save(folder/(key+".png"))
            Image.new("RGB",(1024,684),(215,225,230)).save(folder/"air.png")
            self.assertFalse(h.compare_frames(folder)["conservative_visible_model_difference"])

    def test_H_F_and_asset_rights_approval_boundaries(self):
        text=Path(h.__file__).read_text()
        self.assertIn('"F70_full_approval":0',text)
        self.assertIn('"H03_H05_full_exit":False',text)
        self.assertIn('"face_by_face_GPU_UV_causality_approved":False',text)
        self.assertIn('"INT5_semantic_approval":0',text)
        self.assertIn('"INT6_AI_training_redistribution_approval":0',text)
        self.assertNotIn('"/function mcfr_chair:sleep"',text)

if __name__=="__main__":unittest.main()
