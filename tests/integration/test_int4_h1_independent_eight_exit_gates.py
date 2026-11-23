"""Independent H1 source, status, and 8-exit non-approval regression gates."""
from pathlib import Path
import importlib.util,unittest

ROOT=Path(__file__).resolve().parents[2]
FILE=ROOT/"scripts/integration/build_int4_h1_independent_eight_exit_gates.py"
s=importlib.util.spec_from_file_location("h1exit",FILE)
h=importlib.util.module_from_spec(s);s.loader.exec_module(h)

class H1ExitAssessment(unittest.TestCase):
    def test_baseline_main_sha_and_all_8_prior_actions_pinned(self):
        self.assertEqual(h.MAIN_SHA,"176f7f34de2336eb7984c4734e97b6eb156c19f4")
        self.assertEqual(len(h.ACTIONS),8)
        self.assertEqual(h.ACTIONS["G4_first_failed_parent_chain_assumption"][1],"failure")
        self.assertEqual(h.ACTIONS["G4_corrected_parent_chain"][1],"success")
    def test_five_population_rows_are_not_one_combined_denominator(self):
        self.assertEqual(sorted(h.ROWS.values()),[21,70,1158,16572,592312])
    def test_prior_audit_git_shas_still_match(self):
        for name in h.AUDITS:
            self.assertIsInstance(h.raw_audit(name),dict)
    def test_g5_ledger_sha_verified(self):
        d=h.raw_audit("INT4_G5_FOUR_DENOMINATORS_SCOPED_DECISIONS_V1.json")
        self.assertEqual(d["status"],"PASS_G5_PER_POPULATION_SCOPED_DISPOSITIONS_NOT_FINAL_G_OR_H_EXIT")
        for name,count in h.ROWS.items():
            self.assertEqual(len(h.rows(name,d["derived_output_SHA256"][name]["sha256"],count)),count)
    def test_g5_full_exit_AND_INT5_INT6_remaining_zero(self):
        d=h.raw_audit("INT4_G5_FOUR_DENOMINATORS_SCOPED_DECISIONS_V1.json")
        self.assertEqual(d["G_unconditional_exit_approved"],0)
        self.assertEqual(d["H_independent_exit_approved"],0)
        self.assertEqual(d["INT5_semantic_approved"],0)
        self.assertEqual(d["INT6_training_and_redistribution_rights_approved"],0)
    def test_source_sha_tamper_fails_closed(self):
        k="INT4_G5_FOUR_DENOMINATORS_SCOPED_DECISIONS_V1.json"
        original=h.AUDITS[k]
        try:
            h.AUDITS[k]="0"*40
            with self.assertRaises(AssertionError):h.raw_audit(k)
        finally:h.AUDITS[k]=original
    def test_eight_gates_cover_all_and_do_not_blindly_pass(self):
        d=h.raw_audit("INT4_G5_FOUR_DENOMINATORS_SCOPED_DECISIONS_V1.json")
        self.assertEqual(len(d["H_eight_gate_preflight_only"]),8)
        self.assertTrue(any(x["status"]=="BLOCKED" for x in d["H_eight_gate_preflight_only"]))
    def test_source_f70_eight_risks_remain_conditional(self):
        d=h.raw_audit("INT4_F11F_R08_TWO_FABRIC_ORIGINAL_F2_INDEPENDENT_AUDIT_V1.json")
        self.assertEqual(d["counts"]["F_targets"],70)
        self.assertEqual(d["counts"]["F_conditional_after"],70)
        self.assertEqual(d["counts"]["F_unconditional_final_approvals"],0)

if __name__=="__main__":unittest.main()
