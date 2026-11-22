"""Prevent broadening historic 1-5 comparisons into unsupported AI/runtime claims."""
import importlib.util
from pathlib import Path
import unittest


def entry():
    file=Path(__file__).resolve().parents[2]/"scripts/integration/build_int4_e_research_reconciliation.py"
    s=importlib.util.spec_from_file_location("int4e_evidence",file)
    mod=importlib.util.module_from_spec(s)
    assert s.loader is not None
    s.loader.exec_module(mod)
    return mod


e=entry()


class ResearchScopeTests(unittest.TestCase):
    def test_all_7_counterexamples_remain_scope_limited(self):
        self.assertEqual(e.preserve_classification("UNVERIFIED_OR_COUNTEREXAMPLE","SCOPE_LIMIT_ONLY"),
                         "SCOPE_LIMIT_ONLY_NOT_UNIVERSAL_MODELING_RULE")

    def test_counterexample_cannot_be_turned_into_ai_candidate(self):
        with self.assertRaises(AssertionError):
            e.preserve_classification("UNVERIFIED_OR_COUNTEREXAMPLE","CANDIDATE_REQUIRES_REVIEW")

    def test_fourteen_candidates_are_not_approved(self):
        for kind in ("VANILLA_SHARED","MULTI_MOD_SHARED","MOD_SPECIFIC"):
            self.assertEqual(e.preserve_classification(kind,"CANDIDATE_REQUIRES_REVIEW"),
                             "CONDITIONAL_RESEARCH_CANDIDATE_NOT_AI_APPROVED")

    def test_other_classifications_cannot_be_incorrectly_downgraded(self):
        with self.assertRaises(AssertionError):
            e.preserve_classification("MOD_SPECIFIC","SCOPE_LIMIT_ONLY")

    def test_release_vanilla_not_in_mod_D(self):
        self.assertEqual(e.application_decision("VANILLA","NOT_IN_1158_MOD_BLOCKSTATE_COHORT",0),
                         "VANILLA_1_21_11_ORIGINAL_SOURCE_AUDITED_HISTORICALLY")

    def test_mod_source_join_is_not_render_success(self):
        self.assertEqual(e.application_decision("AF","SOURCE_SELECTED_MODEL_EXACT_MATCH",0),
                         "PINNED_MOD_STATE_MODEL_SOURCE_JOINED_RUNTIME_PENDING")

    def test_unjoined_mod_source_cannot_pass(self):
        self.assertEqual(e.application_decision("HC","UNJOINED_OPTION",0),
                         "HOLD_UNMATCHED_MOD_SOURCE_OPTION")

    def test_pixel_exception_is_conditional_not_screen_fault(self):
        self.assertEqual(e.application_decision("MACAW","SOURCE_SELECTED_MODEL_EXACT_MATCH",9),
                         "CONDITIONAL_MOD_SOURCE_MODEL_WITH_PIXEL_EXCEPTION")

    def test_original_reference_sha_is_pinned(self):
        path="research/furniture_mods/phase_1-5/B/CASES.csv"
        sha=e.FILES[path]
        try:
            e.FILES[path]="0"*40
            with self.assertRaises(AssertionError):
                e.pin(path)
        finally:
            e.FILES[path]=sha

    def test_duplicate_source_keys_blocked(self):
        with self.assertRaises(AssertionError):
            e.keyed([{"case":"V01"},{"case":"V01"}],lambda x:x["case"],"CASES")

    def test_required_classification_totals(self):
        self.assertEqual(sum(e.CLASSES.values()),21)
        self.assertEqual(e.HANDOFF,{"CANDIDATE_REQUIRES_REVIEW":14,"SCOPE_LIMIT_ONLY":7})


if __name__=="__main__":
    unittest.main()
