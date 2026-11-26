"""Five-context original-source5 suppression experiment. Never substitutes fake F2 for CI."""
import copy
import json
import tempfile
import unittest

from PIL import Image,ImageDraw
from mcfr import int5_b19_four_unresolved_four_view_f2 as b19
from mcfr import int5_b23_multigroup_source5_context_f2 as b23
from test_int5_b21_af_source5_isolation_four_view_f2 import fixture

def imgs(target,mode,extra=True,bad_control=False,bad_time=False):
    b23.set_target(target)
    before,control,after,air=b19.stages()
    def pic(extra_part=False):
        frame=Image.new("RGB",(1024,684),(192,198,200))
        pen=ImageDraw.Draw(frame)
        pen.rectangle((480,385,506,420),fill=(110,65,35))
        if extra_part:
            pen.rectangle((502,399,515,425),fill=(151,82,36))
        return frame
    def blank():
        return Image.new("RGB",(1024,684),(192,198,200))
    output={}
    for view in b19.VIEWS:
        a=pic(extra and mode=="with_5")
        b=pic(extra and mode=="with_5")
        if bad_time and mode=="with_5":
            ImageDraw.Draw(b).rectangle((490,380,520,395),fill=(220,20,50))
        neg=blank()
        if bad_control and mode=="with_5":
            ImageDraw.Draw(neg).rectangle((480,385,510,411),fill=(130,20,100))
        output[view]={before:a,control:neg,after:b,air:blank()}
    return output

def scene(target,extra=True,bad_control=False,bad_time=False):
    return {
      mode:imgs(target,mode,extra,bad_control,bad_time)
      for mode in b23.MODES
    }

class ContextSource5OriginalBatchTest(unittest.TestCase):
    def tearDown(self):
        b23.set_target("AF121_5")

    def test_five_contexts_partition_eight_original_other_elements(self):
        self.assertEqual(len(b23.CONTEXTS),5)
        self.assertEqual(set(b23.CONTEXTS["legs_0_3"]+
                             b23.CONTEXTS["seat_4"]+
                             b23.CONTEXTS["back_7_9"]),
                         set(range(10))-{5,6})
        self.assertEqual(b23.CONTEXTS["all_others"],(0,1,2,3,4,7,8,9))
        self.assertEqual(b23.MODES,("without_5","with_5"))

    def test_each_context_has_only_index5_addition_and_exact_sorted_original_order(self):
        for context in b23.CONTEXTS:
            without=b23.choose(context,"without_5")
            with5=b23.choose(context,"with_5")
            self.assertEqual(with5,tuple(sorted(without+(5,))))
            self.assertNotIn(5,without)
            self.assertIn(6,without)
            self.assertEqual(set(with5)-set(without),{5})
            self.assertEqual(len(with5)-len(without),1)

    def test_all_5_contexts_both_AF_model_geometry_UV_and_original_child_properties(self):
        for target in b23.TARGETS:
            child,parent,original_parent,original_child=fixture(target)
            for context in b23.CONTEXTS:
                for mode in b23.MODES:
                    raw,proof=b23.child_for_context(child,parent,target,context,mode)
                    result=json.loads(raw)
                    self.assertEqual(result["elements"],
                        [original_parent["elements"][i]
                         for i in b23.choose(context,mode)])
                    self.assertEqual({k:v for k,v in result.items()
                                      if k!="elements"},original_child)
                    self.assertTrue(proof["faces_uv_textures_coordinates_identical_to_original_parent"])
                    self.assertEqual(proof["selected_original_element_indices"],
                                     list(b23.choose(context,mode)))
                    self.assertFalse(proof["third_party_training_or_redistribution_approved"])

    def test_source5_reverse_x_and_source6_positive_face_guards(self):
        child,parent,original_parent,_=fixture("AF121_5")
        for corrupt in (
            lambda p:p["elements"][5]["from"].__setitem__(0,7),
            lambda p:p["elements"][5]["faces"].pop("north"),
            lambda p:p["elements"][6]["faces"].pop("north"),
            lambda p:p["elements"].pop(2),
            lambda p:p["elements"][9]["faces"].pop("north"),
        ):
            bad=copy.deepcopy(original_parent)
            corrupt(bad)
            with self.assertRaises(ValueError):
                b23.child_for_context(child,json.dumps(bad).encode(),"AF121_5",
                                      "all_others","with_5")

    def test_reject_out_of_scope_context_and_model(self):
        child,parent,*_=fixture("AF121_5")
        for target,context,mode in (
            ("HC11210_3","seat_4","with_5"),
            ("AF121_5","bad_context","with_5"),
            ("AF121_5","seat_4","bad_mode")):
            with self.assertRaises(ValueError):
                b23.child_for_context(child,parent,target,context,mode)

    def test_two_original_scenes_stable_visible_addition_is_positive(self):
        for target in b23.TARGETS:
            metrics=b23.compare_frames(scene(target))
            self.assertEqual(b23.decide(metrics),
                             "PASS_SOURCE5_ADDS_PIXELS_IN_ORIGINAL_CONTEXT")
            self.assertTrue(all(r["five_addition_before_pixels"]>0
                                for r in metrics.values()))

    def test_two_original_scenes_no_additional_source5_is_bounded_negative(self):
        for target in b23.TARGETS:
            metrics=b23.compare_frames(scene(target,extra=False))
            self.assertEqual(b23.decide(metrics),
                             "PASS_SOURCE5_NO_ADDITIONAL_PIXELS_IN_ORIGINAL_CONTEXT")

    def test_negative_control_difference_invalidates_claim(self):
        m=b23.compare_frames(scene("AF121_5",bad_control=True))
        self.assertEqual(b23.decide(m),
                         "CONDITIONAL_B23_TEMPORAL_NEGATIVE_OR_BACKGROUND_DRIFT")

    def test_temporal_difference_invalidates_claim(self):
        m=b23.compare_frames(scene("AF121_5",bad_time=True))
        self.assertEqual(b23.decide(m),
                         "CONDITIONAL_B23_TEMPORAL_NEGATIVE_OR_BACKGROUND_DRIFT")

    def test_missing_real_f2_and_clients_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            for target in b23.TARGETS:
                with self.assertRaises(FileNotFoundError):
                    b23.audit(tmp,target,"all_others")

    def test_no_rights_or_semantic_automatic_approval(self):
        from pathlib import Path
        source=Path(b23.__file__).read_text(encoding="utf-8")
        for piece in ('"role_function_material_style_approved_45":0',
                      '"original_face_UV_exclusive_GPU_pixel_owner_approved":0',
                      '"third_party_training_or_redistribution_rights_approved":0',
                      '"H03":"HOLD"','"H05":"CONDITIONAL"',
                      '"F70_unconditional_approved":0'):
            self.assertIn(piece,source)

if __name__=="__main__":
    unittest.main()
