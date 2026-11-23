"""H4 CI exact PR73 source fix tests without weakening full game F exit."""
import importlib.util,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
p=ROOT/"scripts/integration/build_int4_h4_h06_ci_integrated_source_audit.py"
spec=importlib.util.spec_from_file_location("h4cigates",p)
h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)

class H4CIIntegration(unittest.TestCase):
    def test_five_independent_original_PR73_sources(self):
        self.assertEqual(len(h.PINS),5)
        for path,sha in h.PINS.items():
            self.assertEqual(h.blobsha((ROOT/path).read_bytes()),sha,path)
    def test_exact_four_integration_and_one_knowledge_tests(self):
        self.assertEqual(sum("int2-" in p for p in h.PINS),4)
        self.assertEqual(sum("int3-knowledge" in p for p in h.PINS),1)
    def test_original_H3_all_91_png_reopened(self):
        doc=h.load_json(h.H3,h.H3_SHA)
        self.assertEqual(doc["fixed_case_count"],70)
        self.assertEqual(doc["original_distinct_actions_archive_downloaded"],20)
        self.assertEqual(doc["recorded_original_PNG_occurrences"],91)
        self.assertTrue(doc["all_91_native_F2_PNG_sha256_verified"])
        self.assertFalse(doc["every_original_case_server_state_log_reopened_and_reapproved"])
    def test_original_H1_all_eight_gates_not_fully_pass(self):
        doc=h.load_json(h.H1,h.H1_SHA)
        self.assertEqual(doc["H_eight_gates_reviewed"],8)
        self.assertEqual(doc["H_gate_hold"],2)
        self.assertEqual(doc["H_gate_conditional"],1)
        self.assertEqual(doc["H_full_exit_approved"],0)
    def test_H1_Git_blob_tamper_protection(self):
        original=h.H1_SHA
        try:
            h.H1_SHA="0"*40
            with self.assertRaises(AssertionError):h.load_json(h.H1,h.H1_SHA)
        finally:h.H1_SHA=original

if __name__=="__main__":unittest.main()
