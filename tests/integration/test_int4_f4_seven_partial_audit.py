"""INT-4-F4 full 70-target evidence guard; no fabricated 7/7 success."""
import csv
import importlib.util
import io
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[2]
path=ROOT/"scripts/integration/build_int4_f4_seven_original_f2_partial_audit.py"
spec=importlib.util.spec_from_file_location("f4",path)
f=importlib.util.module_from_spec(spec)
spec.loader.exec_module(f)

def rows(data):
    return list(csv.DictReader(io.StringIO(data.decode("utf-8"))))

class ExactStateAudit(unittest.TestCase):
    def test_explicit_failed_property_cases(self):
        self.assertEqual(f.EXACT,{"S01","S31","S32","S33","S47"})
        self.assertEqual(f.NOT_EXACT,{"S02","S34"})
        self.assertEqual(set(f.CASES),f.EXACT|f.NOT_EXACT)

    def test_original_70_unmodified_history_source(self):
        a=f.read_csv(f.pinned(f.BASE))
        self.assertEqual(len(a),70)
        self.assertEqual(sum(r["final_disposition"].startswith("CONDITIONAL") for r in a),32)
        self.assertEqual(sum(r["final_disposition"].startswith("HOLD") for r in a),38)

    def test_source_research_sha_and_versions(self):
        self.assertEqual(len(f.pinned(f.APPLICATIONS))>10000,True)
        self.assertEqual(f.RELEASE["AF"],{"state":False,"model":False,"provider":False})
        self.assertEqual(f.RELEASE["HC"],{"state":True,"model":True,"provider":True})

    def test_original_F2_zip_hash_is_locked(self):
        self.assertEqual(len(f.ZIP_SHA256),64)
        self.assertEqual(f.ARTIFACT,14755665621)

    def test_seven_filenames_have_distinct_case_coverage(self):
        self.assertEqual(len(f.CASES),7)
        self.assertEqual(len(set(f.CASES)),7)
        self.assertEqual(set(f.OBS),set(f.CASES))

    def test_never_reclassify_wrong_game_state_as_exact(self):
        self.assertNotIn("S02",f.EXACT)
        self.assertNotIn("S34",f.EXACT)
        self.assertIn("S02",f.NOT_EXACT)
        self.assertIn("S34",f.NOT_EXACT)

    def test_lock_drift_fails_closed(self):
        saved=f.PIN[str(f.BASE)]
        try:
            f.PIN[str(f.BASE)]="0"*40
            with self.assertRaises(AssertionError):
                f.pinned(f.BASE)
        finally:
            f.PIN[str(f.BASE)]=saved

if __name__=="__main__":unittest.main()
