"""G5 source-scoped decisions: strict source SHA and no outcome laundering."""
import importlib.util,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
f=ROOT/"scripts/integration/build_int4_g5_scoped_final_dispositions.py"
spec=importlib.util.spec_from_file_location("g5scoped",f)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class G5DispositionsSourceGates(unittest.TestCase):
    def test_source_hashes_all_pinned(self):
        for name in m.PIN:
            self.assertEqual(m.sha(m.source(name)),m.PIN[name],name)
    def test_prior_A_to_F_audit_git_blob_identity(self):
        for name in m.GIT:
            obj=m.prior(name)
            self.assertIsInstance(obj,dict)
    def test_exact_five_separate_population_denominators(self):
        self.assertEqual(m.O_MODEL.name,"INT4_G5_16572_MODEL_SCOPED_DISPOSITIONS_V1.csv.gz")
        self.assertEqual(m.O_FACE.name,"INT4_G5_592312_FACE_SCOPED_DISPOSITIONS_V1.csv.gz")
        self.assertEqual(m.O_STATE.name,"INT4_G5_1158_STATE_SCOPED_DISPOSITIONS_V1.csv")
        self.assertEqual(m.O_FINDING.name,"INT4_G5_21_FINDING_SCOPED_DISPOSITIONS_V1.csv")
        self.assertEqual(m.O_F.name,"INT4_G5_70_REAL_F2_SCOPED_DISPOSITIONS_V1.csv")
    def test_original_HC_six_not_automatically_painted_game_pass(self):
        g4=m.prior("INT4_G4_HC6_PARENT_CHAIN_AND_ORIGINAL_GIT_AUDIT_V1.json")
        self.assertEqual(len(g4["bases"]),6)
        self.assertEqual(g4["G4_game_runtime_or_baked_UV_approved"],False)
        self.assertEqual(g4["G_final_approved"],0)
        self.assertEqual(g4["H_final_approved"],0)
    def test_real_F70_not_fully_approved(self):
        f11=m.prior("INT4_F11F_R08_TWO_FABRIC_ORIGINAL_F2_INDEPENDENT_AUDIT_V1.json")
        self.assertEqual(f11["counts"]["F_conditional_after"],70)
        self.assertEqual(f11["counts"]["F_unconditional_final_approvals"],0)
    def test_face_key_exact_uv_and_slot(self):
        a={"model_key":"A","element_index":"0","face_direction":"west",
           "texture_slot":"#wood","source_uv":"0|0|1|1"}
        b={"model_key":"A","element_index":"0","face_direction":"west",
           "source_slot":"#wood","uv":"0|0|1|1"}
        self.assertEqual(m.Bkey(a),m.Ckey(b))
        b["uv"]="0|0|2|2"
        self.assertNotEqual(m.Bkey(a),m.Ckey(b))
    def test_source_sha_tamper_fails_closed(self):
        key="INT4_G2_1158_STATE_RUNTIME_SOURCE_GATES_V1.csv"
        orig=m.PIN[key]
        try:
            m.PIN[key]="0"*64
            with self.assertRaises(AssertionError):m.source(key)
        finally:m.PIN[key]=orig
    def test_prior_HC_G4_must_preserve_old_A_HOLD(self):
        b=m.csvparse(m.source("INT4_G4_HC6_BASE_SOURCE_PARENT_DISPOSITIONS_V1.csv"))
        self.assertEqual(len(b),6)
        self.assertTrue(all(x["full_in_game_runtime_render_approved"]=="false" for x in b))

if __name__=="__main__":unittest.main()
