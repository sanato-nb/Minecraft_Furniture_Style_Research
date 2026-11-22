"""Original F6 70-target audit fixtures and non-upcasting guards."""
import unittest
import importlib.util
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[2]
script=ROOT/"scripts/integration/build_int4_f6_source_recovery_70.py"
sp=importlib.util.spec_from_file_location("f6_cross_audit",script)
f=importlib.util.module_from_spec(sp)
sp.loader.exec_module(f)

class RealF6SourceEvidence(unittest.TestCase):
    def test_70_prior_case_source_sha_pinned(self):
        for p in (f.BASE,f.PRIOR,f.QUEUE):
            self.assertEqual(f.blob(f.pinned(p)),f.PINS[str(p)])

    def test_old_f5_conditional_37_hold_33(self):
        report=json.loads(f.pinned(f.PRIOR))
        self.assertEqual(report["counts"]["F70_conditional_current"],37)
        self.assertEqual(report["counts"]["F70_hold_current"],33)
        self.assertEqual(report["counts"]["historic_exact_F2_linked"],31)

    def test_only_two_original_cases_allowed_to_change(self):
        self.assertEqual(f.STUDY,{
            "S02":"S02_NORTH_TABLE_TUCK","S34":"S34_NORTH_WEST_INNER_LEFT"})
        original=f.rows(f.pinned(f.BASE))
        holds={r["target_id"] for r in original if r["final_disposition"].startswith("HOLD")}
        self.assertTrue(set(f.STUDY)<=holds)

    def test_original_artifact_sha_is_exactly_pinned(self):
        self.assertEqual(len(f.ZIP_SHA),64)
        self.assertEqual(f.ARTIFACT,14756442623)
        self.assertEqual(f.RUN,45028305708)

    def test_origin_all_other_68_cases_locked(self):
        rows=f.rows(f.pinned(f.BASE))
        self.assertEqual(len(rows),70)
        self.assertEqual(len({x["target_id"] for x in rows}),70)
        self.assertEqual(len([x for x in rows if x["target_id"] not in f.STUDY]),68)

    def test_no_source_approval_upcast_in_initial_history(self):
        rows=f.rows(f.pinned(f.BASE))
        self.assertTrue(all(r["runtime_evidence_accepted_as_full_F_PASS"]=="false" for r in rows))

    def test_mutated_source_sha_fails_closed(self):
        old=f.PINS[str(f.BASE)]
        try:
            f.PINS[str(f.BASE)]="0"*40
            with self.assertRaises(AssertionError):
                f.pinned(f.BASE)
        finally:
            f.PINS[str(f.BASE)]=old

if __name__=="__main__":
    unittest.main()
