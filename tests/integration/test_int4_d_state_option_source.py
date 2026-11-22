"""INT-4-D static-state: original selection exceptions and transformation boundaries."""
from pathlib import Path
import importlib.util
import unittest


def load():
    script=Path(__file__).resolve().parents[2]/"scripts/integration/build_int4_d_state_option_source.py"
    spec=importlib.util.spec_from_file_location("int4d_state_option",script)
    module=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


a=load()


class SourceStateTests(unittest.TestCase):
    def test_local_target_is_not_runtime(self):
        self.assertEqual(a.classify_option("LOCAL"),"STATIC_LOCAL_MODEL_TARGET")

    def test_vanilla_ref_is_separate_release(self):
        self.assertEqual(a.classify_option("VANILLA_JAR"),"VANILLA_1_21_1_SOURCE_MODEL_REFERENCE")

    def test_unresolved_must_be_hold(self):
        self.assertEqual(a.classify_option("UNRESOLVED_MODEL_REF"),"HOLD_ORIGINAL_SOURCE_TARGET_MISSING")
        with self.assertRaises(AssertionError):
            a.classify_option("APPROVED_MODEL")

    def test_source_exception_priority(self):
        self.assertEqual(a.classify_state(1,0,0,0,""),
                         "CONDITIONAL_SOURCE_HAS_UNRESOLVED_MODEL_TARGET")
        self.assertEqual(a.classify_state(0,1,0,0,""),
                         "HOLD_SELECTED_MODEL_PARENT_MISSING")
        self.assertEqual(a.classify_state(0,0,1,0,""),
                         "CONDITIONAL_SELECTED_MODEL_NO_STATIC_ELEMENTS")
        self.assertEqual(a.classify_state(0,0,0,1,""),
                         "CONDITIONAL_ORIGINAL_SELECTOR_ANOMALY")
        self.assertEqual(a.classify_state(0,0,0,0,""),
                         "REUSED_STATIC_BLOCKSTATE_SOURCE_VERIFIED_ONLY")

    def test_pixel_context_does_not_imply_game_defect(self):
        self.assertEqual(a.followup_status("LOCAL",3),
                         "INT4_C_PIXEL_EXCEPTION_AND_D_REACHABILITY_F_CASE")
        self.assertEqual(a.followup_status("UNRESOLVED_MODEL_REF",0),
                         "INT4_D_CODE_STATE_REGISTRATION_AND_F_RENDER_WHEN_TARGET_EXISTS")

    def test_git_blob_pin_rejects_source_drift(self):
        path="research/furniture_mods/phase_1-3/D/D_AUDIT.json"
        original=a.FILES[path]
        try:
            a.FILES[path]="0"*40
            with self.assertRaises(AssertionError):
                a.lock(path)
        finally:
            a.FILES[path]=original

    def test_source_unique_does_not_silently_merge(self):
        with self.assertRaises(AssertionError):
            a.unique([{"k":"b"},{"k":"b"}],lambda r:r["k"],"test")

    def test_known_fixed_denominators(self):
        self.assertEqual(sum(a.COUNTS[k][0] for k in a.COUNTS),1158)
        self.assertEqual(sum(a.COUNTS[k][1] for k in a.COUNTS),78456)


if __name__=="__main__":
    unittest.main()
