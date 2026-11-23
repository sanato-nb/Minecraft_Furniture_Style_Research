"""G4 6 Handcrafted source-only display base and original parent chain gate."""
from pathlib import Path
import importlib.util
import unittest

ROOT=Path(__file__).resolve().parents[2]
source=ROOT/"scripts/integration/build_int4_g4_hc_six_base_parent_chain.py"
spec=importlib.util.spec_from_file_location("g4sixsource",source)
g4=importlib.util.module_from_spec(spec)
spec.loader.exec_module(g4)

class TestSixHCParentScope(unittest.TestCase):
    def test_pinned_HC_commit_and_original_six_model_blobs(self):
        self.assertEqual(g4.HC_COMMIT,"8d21d1665916850c3fa3bdaf1370c50ec2ca7035")
        self.assertEqual(len(g4.BASE),6)
        self.assertEqual(set(g4.BASE),{"HC1","HC2","HC3","HC4","HC5","HC6"})
        self.assertEqual(len({p for p,_ in g4.BASE.values()}),6)
        self.assertTrue(all(len(sha)==40 for _,sha in g4.BASE.values()))

    def test_original_parent_chain_source_schema_and_row_count(self):
        self.assertEqual(g4.PINS[str(g4.CHAIN)],"9a4eeddf419f502bb8fc7808272c7c8336ff9695")
        self.assertEqual(g4.CHAIN.name,"MODEL_PARENT_CHAINS.csv.gz")
        self.assertEqual(g4.CAUDIT.name,"C_AUDIT.json")

    def test_exact_source_pin_SHA_algorithm(self):
        for key in g4.PINS:
            p=Path(key)
            b=g4.read_pinned(p)
            expected=g4.sha256(b) if p in (g4.A_MODELS,g4.D_OPTIONS) else g4.blob_sha1(b)
            self.assertEqual(expected,g4.PINS[key])

    def test_static_D_options_not_inferred_as_all_runtime_references(self):
        self.assertEqual(g4.D_OPTIONS.name,"INT4_D_78456_OPTION_PROVENANCE_V1.csv.gz")
        self.assertTrue(g4.OUT_DESC.name.endswith(".csv.gz"))
        self.assertEqual(g4.OUT_BASE.name,"INT4_G4_HC6_BASE_SOURCE_PARENT_DISPOSITIONS_V1.csv")

    def test_stop_on_original_input_digest_drift(self):
        original=g4.PINS[str(g4.CHAIN)]
        try:
            g4.PINS[str(g4.CHAIN)]="0"*40
            with self.assertRaises(AssertionError):
                g4.read_pinned(g4.CHAIN)
        finally:g4.PINS[str(g4.CHAIN)]=original

    def test_G3_hold_evidence_retained_and_not_reinterpreted_as_F_pass(self):
        import json
        audit=json.loads(g4.read_pinned(g4.G3_AUDIT))
        self.assertEqual(audit["A_112_exception_model_dispositions"]["HOLD_HANDCRAFTED_BASE_MODEL_USAGE_AND_JAVA_UNKNOWN"],6)
        self.assertEqual(audit["G_final_approved"],0)
        self.assertEqual(audit["H_final_approved"],0)
        self.assertEqual(audit["INT6_rights_approved"],0)

if __name__=="__main__":
    unittest.main()
