"""INT-4-A 112예외 분류의 경계·부정 시험. 원본 모델 수정 없음."""
import importlib.util
from pathlib import Path
import unittest


def load_audit():
    root = Path(__file__).resolve().parents[2]
    path = root / "scripts/integration/adjudicate_int4_a_exceptions.py"
    spec = importlib.util.spec_from_file_location("adjudicate_int4_a_exceptions", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


audit = load_audit()


def model(mod, resource, geometry, term, own, effective, pm, ns, missing=""):
    return {
        "mod":mod,"model_id":resource,"geometry_status":geometry,
        "terminal_status":term,"own_elements":str(own),"effective_elements":str(effective),
        "parent_missing":str(int(pm)),"no_static":str(int(ns)),"terminal_ref":missing,
    }


def evidence(resource, pm, ns):
    return {
        "resource_id":resource,
        "historical_parent_missing":str(int(pm)),
        "historical_no_static":str(int(ns)),
        "static_selection_reachability": (
            "NOT_REACHED_IN_PINNED_STATIC_BLOCKSTATE_OR_ITEM_CHAIN"
            if pm else "NOT_CHECKED_BY_PARENT48_AUDIT"
        ),
    }


class DispositionTests(unittest.TestCase):
    def test_normal_static(self):
        row=model("HC","handcrafted:block/bookcase","LOCAL","ROOT",3,3,False,False)
        result=audit.classify(row,None)
        self.assertEqual(result["exception_class"],"STATIC_REUSED")
        self.assertNotEqual(result["int4_a_review_result"],"NOT_APPLICABLE_TO_JSON_CUBOID_GEOMETRY")

    def test_af_missing_parent_has_geometry_and_static_reachability_boundary(self):
        res="another_furniture:block/lantern_post_base"
        row=model("AF",res,"PARTIAL_OWN_OR_LOCAL_GEOMETRY","PARENT_MISSING",
                  2,2,True,False,"minecraft:lantern")
        result=audit.classify(row,evidence(res,True,False))
        self.assertEqual(result["exception_class"],"PARENT_MISSING_PARTIAL_STATIC_UNREACHABLE")
        self.assertIn("DYNAMIC",result["required_followup_stage"])
        self.assertIn("UNREACHABLE",result["static_blockstate_item_reachability"])

    def test_macaw_missing_parent_desk(self):
        res="mcwfurnitures:block/desk/oak_desk"
        row=model("MACAW",res,"UNRESOLVED_PARENT","PARENT_MISSING",
                  0,0,True,True,"mcwfurnitures:block/parent/desk")
        self.assertEqual(audit.classify(row,evidence(res,True,True))["exception_class"],
                         "PARENT_MISSING_NO_ELEMENTS_STATIC_UNREACHABLE")

    def test_macaw_missing_parent_drawer(self):
        res="mcwfurnitures:block/drawer/oak_drawer_base"
        row=model("MACAW",res,"UNRESOLVED_PARENT","PARENT_MISSING",
                  0,0,True,True,"mcwfurnitures:block/parent/drawer_base")
        self.assertEqual(audit.classify(row,evidence(res,True,True))["exception_class"],
                         "PARENT_MISSING_NO_ELEMENTS_STATIC_UNREACHABLE")

    def test_hc_base_is_hold_not_render_failure(self):
        res="handcrafted:block/base/bed_block"
        row=model("HC",res,"NONE","ROOT",0,0,False,True)
        result=audit.classify(row,evidence(res,False,True))
        self.assertEqual(result["exception_class"],"BASE_MODEL_NO_EXPLICIT_ELEMENTS")
        self.assertEqual(result["int4_a_review_result"],"HOLD_MODEL_USAGE_AND_RENDER_PATH")

    def test_generated_item_is_static_cuboid_na(self):
        cases=[
            ("AF","another_furniture:item/furniture_hammer"),
            ("HC","handcrafted:item/hammer"),
            ("MACAW","mcwfurnitures:item/cabinet_door"),
        ]
        for mod,res in cases:
            with self.subTest(mod=mod):
                row=model(mod,res,"GENERATED_ITEM_RUNTIME","BUILTIN",0,0,False,True)
                result=audit.classify(row,evidence(res,False,True))
                self.assertEqual(result["int4_a_review_result"],
                                 "NOT_APPLICABLE_TO_JSON_CUBOID_GEOMETRY")
                self.assertNotIn("VERIFIED",result["int4_a_review_result"])

    def test_wrong_reachability_must_be_rejected(self):
        res="mcwfurnitures:block/desk/oak_desk"
        row=model("MACAW",res,"UNRESOLVED_PARENT","PARENT_MISSING",
                  0,0,True,True,"mcwfurnitures:block/parent/desk")
        inp=evidence(res,True,True)
        inp["static_selection_reachability"]="UNVERIFIED"
        with self.assertRaises(AssertionError):
            audit.classify(row,inp)

    def test_parent_missing_is_not_automatically_repaired(self):
        res="another_furniture:block/lantern_post_base"
        row=model("AF",res,"PARTIAL_OWN_OR_LOCAL_GEOMETRY","ROOT",2,2,True,False,"")
        with self.assertRaises(AssertionError):
            audit.classify(row,evidence(res,True,False))

    def test_hc_base_does_not_inherit_48_reachability(self):
        res="handcrafted:block/base/bed_block"
        row=model("HC",res,"NONE","ROOT",0,0,False,True)
        inp=evidence(res,False,True)
        inp["static_selection_reachability"]="NOT_REACHED_IN_PINNED_STATIC_BLOCKSTATE_OR_ITEM_CHAIN"
        with self.assertRaises(AssertionError):
            audit.classify(row,inp)

    def test_source_drift_is_rejected(self):
        bad="project/integration/INT4_A_MODEL_PARENT_AUDIT_V1.json"
        old=audit.FILES[bad]
        try:
            audit.FILES[bad]="0"*40
            with self.assertRaises(AssertionError):
                audit.locked_bytes(bad)
        finally:
            audit.FILES[bad]=old


if __name__=="__main__":
    unittest.main()
