"""H10 model-only actual same-camera 1.21.1 Handcrafted bed occupancy controls.

These are synthetic regressions; only Github Actions real native F2 + server
log counts as actual game evidence.
"""
from __future__ import annotations
import hashlib,json,unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from mcfr import int4_h10_hc_bed_occupied_f2_capture as h10
from mcfr.chair_runtime_fixture import pack_lines,make_pack

class H10BedModelOccupied(unittest.TestCase):
    def test_version_source_release_pinned(self):
        self.assertEqual(h10.VERSION,"1.21.1")
        self.assertEqual(h10.SOURCE_GIT_COMMIT,"8d21d1665916850c3fa3bdaf1370c50ec2ca7035")
        self.assertEqual(h10.RELEASE_SHA1,"a9579fecd7ed429c282be21d5c921d220197acc6")
    def test_only_one_original_S37_foot_fixture(self):
        case=h10.capture_case()
        self.assertEqual(len(case),1)
        self.assertEqual(case[0].case_id,"S37")
        self.assertEqual(case[0].state(),h10.command_state("false"))
        self.assertEqual(h10.XYZ,(-16,120,40))
    def test_state_pairs_do_not_invent_unrelated_properties(self):
        self.assertIn("occupied=false",h10.command_state("false"))
        self.assertIn("occupied=true",h10.command_state("true"))
        self.assertIn("part=foot",h10.command_state("true"))
        for invalid in ("foo","occupied", "sleep"):
            with self.assertRaises(ValueError):h10.command_state(invalid)
    def test_data_pack_original_source_case_no_gameplay(self):
        placed,verified=pack_lines(h10.VERSION,h10.capture_case())
        self.assertEqual(sum(x.startswith("setblock") for x in placed),1)
        self.assertIn("occupied=false", "\n".join(placed))
        self.assertNotIn("occupied=true","\n".join(placed))
        self.assertIn("S37=PASS","\n".join(verified))
    def test_pack_created_from_single_original_study_case(self):
        with TemporaryDirectory() as temp:
            dest=Path(temp)/"pack"
            m=make_pack(h10.VERSION,dest,selected_cases=h10.capture_case())
            self.assertEqual(m["test_cases"],1)
            self.assertEqual((dest/"data/mcfr_chair/function/verify.mcfunction").read_text().count("=PASS"),1)
    def test_same_camera_three_F2_and_no_sleep_gameplay(self):
        s=Path(h10.__file__).read_text(encoding="utf-8")
        self.assertIn('check_server("false")',s)
        self.assertIn('check_server("true")',s)
        self.assertIn('capture_frame("air")',s)
        self.assertEqual(h10.CASES,("false","true","air"))
        self.assertNotIn('cmd("/time add',s)
        self.assertNotIn('"/function mcfr_chair:sleep',s)
        self.assertNotIn('"/gamemode survival"',s)
    def test_source_scope_F70_H_approval_remain_zero(self):
        s=Path(h10.__file__).read_text(encoding="utf-8")
        self.assertIn('"full_F70_unconditional_approvals":0',s)
        self.assertIn('"H03_H05_full_exit_approved":False',s)
        self.assertIn('"face_by_face_texture_UV_pixel_causality_approved":False',s)
        self.assertIn('"INT5_semantic_approved":0',s)
        self.assertIn('"INT6_AI_training_redistribution_approved":0',s)
    def test_synthetic_image_roi_difference_not_source_proof(self):
        from PIL import Image,ImageDraw
        a=Image.new("RGB",(1024,684),(180,201,226))
        b=a.copy()
        ImageDraw.Draw(b).rectangle((420,345,500,445),fill=(80,35,25))
        self.assertGreaterEqual(h10.image_delta(a,b),100)
        self.assertEqual(h10.image_delta(a,a),0)
    def test_original_h9_occupied_pair_not_faked_F2(self):
        p=h10.hc.ROOT/h10.H9_REPORT
        d=json.loads(p.read_text(encoding="utf-8"))
        self.assertEqual(d["counts"]["new_occupied_true_native_F2"],0)
        self.assertEqual(d["counts"]["foot_parent_geometry_changed_pairs"],256)

if __name__=="__main__":unittest.main()
