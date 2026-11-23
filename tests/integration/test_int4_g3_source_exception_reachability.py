"""INT-4-G3 original AF 4.0.3 registry scope and source static selection gates."""
import importlib.util
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[2]
path=ROOT/"scripts/integration/build_int4_g3_source_exception_reachability.py"
spec=importlib.util.spec_from_file_location("g3scope",path)
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
class G3OriginalSourceGate(unittest.TestCase):
    def test_study_source_commit_and_original_paths(self):
        self.assertEqual(g.GIT,"57eb624cbb7f408d43398c7434b0d38d312cb55d")
        self.assertEqual(g.UPSTREAM[g.UNUSED],"f1330a172a20d47a24d40288317293bc47c59511")
        self.assertTrue(g.JAVA.endswith("/AFBlocks.java"))
    def test_all_original_sha_pins(self):
        for p in g.PINS:
            self.assertEqual(g.blobhash(g.pinned(p)),g.PINS[p])
    def test_112_6343_and_78456_population_pins(self):
        self.assertEqual([v[1] for v in g.COMP.values()],[16572,6343,78456])
    def test_research_E_universal_rights_not_approved(self):
        e=g.csvrows(g.pinned("INT4_E_21_FINDING_DISPOSITIONS_V1.csv"))
        self.assertEqual(len(e),21)
        self.assertTrue(all(x["int6_rights_approved"]=="false" for x in e))
    def test_F70_no_runtime_full_exit(self):
        f=g.csvrows(g.pinned("INT4_F11F_70_TARGET_EVIDENCE_DISPOSITIONS_V15.csv"))
        self.assertEqual(len(f),70)
        self.assertTrue(all(x["runtime_evidence_accepted_as_full_F_PASS"]=="false" for x in f))
    def test_D_six_source_anomalies_not_game_bugs(self):
        d=g.csvrows(g.pinned("INT4_D_6_SOURCE_OPTION_EXCEPTIONS_V1.csv"))
        self.assertEqual(len(d),6)
        self.assertTrue(all(x["runtime_defect_proven"]=="false" for x in d))
        self.assertEqual(sum(x["exception_type"]=="UNRESOLVED_MODEL_REF" for x in d),4)
        self.assertEqual(sum(x["exception_type"]=="PRIOR_CHAIR_VARIANT_3_POINTS_TO_1" for x in d),2)
    def test_hash_tamper_fails_closed(self):
        key="INT4_G2_SOURCE_CROSSJOIN_AUDIT_V1.json"
        a=g.PINS[key]
        try:
            g.PINS[key]="0"*40
            with self.assertRaises(AssertionError):g.pinned(key)
        finally:g.PINS[key]=a
if __name__=="__main__":unittest.main()
