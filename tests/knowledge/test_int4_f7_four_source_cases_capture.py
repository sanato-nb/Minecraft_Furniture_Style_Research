"""Source-locked F7 four-case test: AF variant3, two-model bench, vanilla parent."""
import unittest
from mcfr import int4_nonchair_runtime as rt
from mcfr import int4_f7_four_source_cases_capture as f7
from mcfr import int4_f4_chair_bench_couch_capture as f4

class F7ExactOriginalEvidence(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases,cls.hash=f7.original_cases()

    def test_original_4_study_case_count(self):
        self.assertEqual(tuple(self.cases),f7.CASES)
        self.assertEqual(len(self.cases),4)
        self.assertEqual(len(self.hash),64)

    def test_original_5_model_applications_but_only_4_case_ids(self):
        self.assertEqual(sum(len(x) for x in self.cases.values()),5)
        self.assertEqual(len(self.cases["S30"]),2)

    def test_original_31_elements_and_144_faces(self):
        self.assertEqual(sum(sum(int(y["elements"]) for y in x) for x in self.cases.values()),31)
        self.assertEqual(sum(sum(int(y["faces"]) for y in x) for x in self.cases.values()),144)

    def test_bench_two_models_selected_simultaneously_not_as_two_cases(self):
        rows=self.cases["S30"]
        self.assertEqual({int(r["faces"]) for r in rows},{34,12})
        self.assertEqual(len({r["model_path"] for r in rows}),2)
        self.assertEqual({r["rule_index"] for r in rows},{"0","16"})
        self.assertEqual({r["provider_sha"] for r in rows},
                         {"7109ebf4fd72259a08c14dc220b52c71dbdb8988",
                          "a7c52985fe9ef80eb1262f100c8368347895f7c0"})

    def test_s03_s04_variant3_original_leaf_is_named_1(self):
        for case,wood in (("S03","birch"),("S04","spruce")):
            r=self.cases[case][0]
            self.assertIn("variant=3",r["state"])
            self.assertTrue(r["model_path"].endswith("/chair/"+wood+"_1.json"))
            self.assertEqual(r["y"],"180")

    def test_s22_vanilla_parent_is_explicit_external_to_hc_mod(self):
        row=self.cases["S22"][0]
        self.assertEqual(row["provider_path"],f7.EXTERNAL_VANILLA_PARENT)
        self.assertEqual(row["provider_sha"],f7.EXTERNAL_VANILLA_GIT_SHA)
        self.assertEqual(row["model_path"].split("/")[-1],"oak_drawer_single_1.json")

    def test_original_git_ledger_hash_sha256_unchanged(self):
        self.assertEqual(self.hash,f7.SOURCE_SHA)

    def test_live_capture_plan_routes_through_actual_original_state_selector(self):
        from_runner,h=rt.applications(f7.CASES)
        self.assertEqual(set(from_runner),set(self.cases))
        self.assertEqual(h,self.hash)
        source_only=rt.stages(f7.VERSION,case_ids=f7.CASES,source_only=True)
        self.assertEqual(set(source_only),set(f7.CASES))
        for case in f7.CASES:
            commands,check=source_only[case]
            original=self.cases[case][0]
            expected=rt.state(original["block"],original["state"])
            self.assertTrue(commands[-1].endswith(expected))
            self.assertTrue(check["subject"]["exact"].endswith(expected))

    def test_existing_f4_f5_f6_source_case_invariants_unchanged(self):
        self.assertEqual(f4.CASES,("S01","S02","S31","S32","S33","S34","S47"))
        self.assertEqual(rt.REMAINING,("S14","S15","S16","S17","S39","S40"))

    def test_invalid_case_ids_or_changed_geometry_are_rejected(self):
        with self.assertRaisesRegex(ValueError,"Inconsistent original case"):
            rt.applications(("S70",))
        with self.assertRaises((ValueError,AssertionError)):
            rt.applications(("S30","S30"))

    def test_no_external_parent_blind_approval(self):
        self.assertEqual(f7.EXTERNAL_VANILLA_PARENT,"assets/minecraft/models/block/cube.json")
        self.assertEqual(f7.EXPECTED["S22"][4:6],(1,6))

if __name__=="__main__":
    unittest.main()
