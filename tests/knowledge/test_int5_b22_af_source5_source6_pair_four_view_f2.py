"""B22 exact two original AF model elements: real Minecraft source pair controls."""
import copy
import json
import tempfile
import unittest
from pathlib import Path

from PIL import Image,ImageDraw

from mcfr import int5_b19_four_unresolved_four_view_f2 as b19
from mcfr import int5_b20_af_reversed_x_three_session_f2 as b20
from mcfr import int5_b21_af_source5_isolation_four_view_f2 as b21
from mcfr import int5_b22_af_source5_source6_pair_four_view_f2 as b22
from test_int5_b21_af_source5_isolation_four_view_f2 import fixture

def frame(target,mode,control=False,plus=False):
    b22.set_target(target)
    im=Image.new("RGB",(1024,684),(198,201,204))
    if not control:
        d=ImageDraw.Draw(im)
        if mode=="original_5":
            d.rectangle((470,381,495,406),fill=(160,90,35))
        elif mode in ("positive_6","pair_5_6"):
            d.rectangle((470,381,496,407),fill=(110,80,45))
            if mode=="pair_5_6" and plus:
                d.rectangle((490,392,512,419),fill=(160,90,35))
    return im

def scenes(target,add_pair_pixels=False,negative_drift=False,
           temporal_drift=False,positive_missing=False):
    b22.set_target(target)
    before,control,after,empty=b19.stages()
    scenes={}
    for mode in b22.MODES:
        scenes[mode]={}
        for view in b19.VIEWS:
            f=frame(target,mode,control=positive_missing and mode=="positive_6",
                    plus=add_pair_pixels)
            last=frame(target,mode,control=positive_missing and mode=="positive_6",
                       plus=add_pair_pixels)
            if temporal_drift and mode=="pair_5_6":
                d=ImageDraw.Draw(last)
                d.rectangle((490,385,530,430),fill=(150,23,90))
            ctrl=frame(target,mode,control=not (
                negative_drift and mode=="pair_5_6"))
            empty_frame=frame(target,mode,control=True)
            scenes[mode][view]={before:f,control:ctrl,after:last,empty:empty_frame}
    return scenes

class B22OriginalPairTests(unittest.TestCase):
    def tearDown(self):
        b22.set_target("AF121_5")

    def test_targets_and_three_separate_game_sessions_are_fixed(self):
        self.assertEqual(b22.TARGETS,("AF121_5","AF123_5"))
        self.assertEqual(b22.MODES,("original_5","positive_6","pair_5_6"))
        for target in b22.TARGETS:
            s=b22.source_identity(target)
            self.assertEqual(s["source_element_index"],5)
            self.assertEqual(s["source_faces"],4)

    def test_pair_is_exactly_two_original_parent_elements_and_original_child_metadata(self):
        for target in b22.TARGETS:
            child,parent,parsed,child_model=fixture(target)
            raw,meta=b22.pair_child(child,parent,target)
            new=json.loads(raw)
            self.assertEqual(new["elements"],[parsed["elements"][5],
                                               parsed["elements"][6]])
            self.assertEqual({k:v for k,v in new.items() if k!="elements"},
                             child_model)
            self.assertEqual(meta["selected_original_source_elements"],[5,6])
            self.assertEqual(meta["result_element_count"],2)
            self.assertEqual(meta["result_face_count"],8)
            self.assertTrue(meta["all_faces_textures_UV_copied_verbatim"])

    def test_bad_original_reverse_x_parent_or_faces_fail_closed(self):
        child,parent,parsed,_=fixture("AF121_5")
        for mutate in [
            lambda p:p["elements"][5]["from"].__setitem__(0,12),
            lambda p:p["elements"][5]["faces"].pop("north"),
            lambda p:p["elements"][6]["faces"].pop("north"),
            lambda p:p["elements"].pop(4),
            lambda p:p["elements"][6]["to"].__setitem__(0,0),
        ]:
            altered=copy.deepcopy(parsed)
            mutate(altered)
            with self.assertRaisesRegex(ValueError,"original|parent"):
                b22.pair_child(child,json.dumps(altered).encode(),"AF121_5")

    def test_non_af_or_other_target_rejected(self):
        child,parent,*_=fixture("AF121_5")
        with self.assertRaisesRegex(ValueError,"only two"):
            b22.pair_child(child,parent,"HC11210_3")

    def test_pair_matching_positive6_is_scoped_four_view_result(self):
        for target in b22.TARGETS:
            m=b22.compare_three(scenes(target))
            self.assertEqual(b22.decision(m),
                "PASS_PAIR5_6_MATCHES_ORIGINAL6_ONLY_AT_FOUR_CARDINAL_VIEWS")
            self.assertTrue(all(row["pair5_6_vs_original6_before_pixels"]==0
                                for row in m.values()))
            self.assertTrue(any(row["original5_vs_original6_before_pixels"]>0
                                for row in m.values()))

    def test_pair_adds_visible_pixels_in_valid_control(self):
        for target in b22.TARGETS:
            m=b22.compare_three(scenes(target,add_pair_pixels=True))
            self.assertEqual(b22.decision(m),
                "PASS_PAIR5_6_HAS_ADDITIONAL_RENDER_PIXELS_OVER_ORIGINAL6_ONLY")
            self.assertTrue(any(row["pair5_6_vs_original6_before_pixels"]>0
                                for row in m.values()))

    def test_negative_other_variant_drift_invalidates_claim(self):
        m=b22.compare_three(scenes("AF121_5",negative_drift=True))
        self.assertEqual(b22.decision(m),
                         "CONDITIONAL_B22_NEGATIVE_OR_TEMPORAL_CONTROLS_UNSTABLE")

    def test_temporal_original_restore_drift_invalidates_claim(self):
        m=b22.compare_three(scenes("AF121_5",temporal_drift=True))
        self.assertEqual(b22.decision(m),
                         "CONDITIONAL_B22_NEGATIVE_OR_TEMPORAL_CONTROLS_UNSTABLE")

    def test_no_positive_source6_cannot_prove_pair_suppression(self):
        m=b22.compare_three(scenes("AF121_5",positive_missing=True))
        self.assertEqual(b22.decision(m),
             "CONDITIONAL_B22_ORIGINAL5_OR_POSITIVE6_SINGLE_CONTROL_INVALID")

    def test_negative_control_server_is_pin_exact_and_top_slab_is_legal(self):
        for target in b22.TARGETS:
            b22.set_target(target)
            self.assertEqual(b19.VERSION,b22.VERSION)
            self.assertEqual(set(b19.cameras()),set(b19.VIEWS))
            self.assertEqual(len(b19.stages()),4)
            if target=="AF123_5":
                self.assertEqual(b19.support(b19.stages()[0]),
                                 "minecraft:oak_slab[type=top]")
                self.assertEqual(b19.support(b19.stages()[1]),
                                 "minecraft:oak_slab[type=top]")

    def test_cannot_audit_without_real_original_F2_or_game_logs(self):
        with tempfile.TemporaryDirectory() as tmp:
            for t in b22.TARGETS:
                with self.assertRaises(FileNotFoundError):
                    b22.audit(tmp,t)

    def test_does_not_promote_original_rights_or_b19_full_chair_source5(self):
        s=Path(b22.__file__).read_text(encoding="utf-8")
        for expected in (
            '"H03":"HOLD"','"H05":"CONDITIONAL"',
            '"F70_unconditional_approved":0',
            '"original_element5_exclusive_occlusion_or_root_cause_proven":False',
            '"individual_original_face_UV_exclusive_GPU_pixel_ownership_proven":False',
            '"third_party_training_redistribution_rights_approved":False',
            '"B19_cumulative_bounded_render_source_removals_43_of_45_kept":True',
        ):
            self.assertIn(expected,s)

if __name__=="__main__":
    unittest.main()
