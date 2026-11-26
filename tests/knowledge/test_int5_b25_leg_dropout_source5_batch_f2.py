"""B25 eight source5 on/off original leg dropout contexts, no semantic promotion."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
from mcfr import int5_b23_multigroup_source5_context_f2 as b23
from mcfr import int5_b25_leg_dropout_source5_batch_f2 as b25
from test_int5_b21_af_source5_isolation_four_view_f2 import fixture

class OriginalLegDropoutB25Tests(unittest.TestCase):
    def test_exact_four_unique_leg_dropout_masks(self):
        self.assertEqual(len(b25.OMIT_LEG_CONTEXTS),4)
        keys={"without_leg0","without_leg1","without_leg2","without_leg3"}
        self.assertEqual(set(b25.OMIT_LEG_CONTEXTS),keys)
        for ctx,indices in b25.OMIT_LEG_CONTEXTS.items():
            dropped=int(ctx[-1])
            self.assertEqual(set(indices),{0,1,2,3,4}-{dropped})
            self.assertIn(4,indices)
            self.assertNotIn(5,indices)
            self.assertNotIn(6,indices)

    def test_each_original_source5_intervention_differs_only_by_index5(self):
        for ctx in b25.OMIT_LEG_CONTEXTS:
            missing=int(ctx[-1])
            off=b25.evidence_selected(ctx,"without_5")
            on=b25.evidence_selected(ctx,"with_5")
            self.assertEqual(set(on)-set(off),{5})
            self.assertEqual(set(off),{0,1,2,3,4,6}-{missing})
            self.assertEqual(on,tuple(sorted(on)))
            self.assertIn(6,on)

    def test_both_original_model_types_preserve_exact_elements_and_uv(self):
        for target in b25.TARGETS:
            child,parent,original_parent,original_child=fixture(target)
            for ctx in b25.OMIT_LEG_CONTEXTS:
                b25.setup(ctx)
                for mode in b23.MODES:
                    raw,scope=b23.child_for_context(child,parent,target,ctx,mode)
                    self.assertEqual(json.loads(raw)["elements"],
                        [original_parent["elements"][i] for i in b25.evidence_selected(ctx,mode)])
                    self.assertEqual({k:v for k,v in json.loads(raw).items()
                                      if k!="elements"},original_child)
                    self.assertTrue(scope["faces_uv_textures_coordinates_identical_to_original_parent"])
                    self.assertFalse(scope["original_or_patched_JAR_distributed"])

    def test_source5_from_to_face_and_parent_pins_fail_closed(self):
        child,parent,original_parent,_=fixture("AF121_5")
        for mutation in (
            lambda p:p["elements"][5]["from"].__setitem__(0,12),
            lambda p:p["elements"][5]["faces"].pop("north"),
            lambda p:p["elements"][6]["faces"].pop("north"),
            lambda p:p["elements"].pop(0)
        ):
            mutated=copy.deepcopy(original_parent)
            mutation(mutated)
            with self.assertRaises(ValueError):
                b23.child_for_context(child,json.dumps(mutated).encode("utf-8"),
                                      "AF121_5","without_leg1","with_5")

    def test_reject_undefined_target_or_mask(self):
        for target,ctx in (("HC11210_3","without_leg0"),
                           ("AF121_5","without_leg5"),
                           ("AF121_5","front_0_4")):
            with self.assertRaises(ValueError):
                b25.capture([],{},None,None,"1.21.1",target,ctx)

    def test_all_four_contexts_require_original_real_F2_for_audit(self):
        with tempfile.TemporaryDirectory() as temp:
            for ctx in b25.OMIT_LEG_CONTEXTS:
                with self.assertRaises(FileNotFoundError):
                    b25.audit(temp,"AF121_5",ctx)

    def test_strict_approval_gates_remain_false(self):
        code=Path(b25.__file__).read_text(encoding="utf-8")
        for required in (
            '"exclusive_single_original_leg_occlusion_cause_proven":False',
            '"physical_leg_or_seat_role_proven":False',
            '"original_face_UV_GPU_pixel_owner_verified":False',
            '"material_style_verified":False',
            '"third_party_training_or_redistribution_rights_approved":False',
            '"F70_unconditional_approved":0',
            '"H03":"HOLD"','"H05":"CONDITIONAL"',
        ):
            self.assertIn(required,code)

if __name__=="__main__":
    unittest.main()
