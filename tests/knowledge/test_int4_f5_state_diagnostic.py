"""Opt-in F5 server-property diagnosis: preserve 7 F4 histories and native data."""
import unittest
from mcfr import int4_nonchair_runtime as runner
from mcfr import int4_f5_state_diagnostic as f5
from mcfr import int4_f4_chair_bench_couch_capture as f4

FAKE={
    "S02":{"facing":["east","north","south","west"],"tucked":["false","true"],"variant":["1","2","3"]},
    "S34":{"color":["none","white"],"facing":["east","north","south","west"],
           "shape":["single","inner_left","inner_right","outer_left","outer_right"],
           "waterlogged":["false","true"]},
    "_table_present":True,
}

class PropertyMode(unittest.TestCase):
    def test_pinned_original_source_unchanged(self):
        r,digest=f5.original_source()
        self.assertEqual(set(r),{"S02","S34"})
        self.assertEqual(len(digest),64)
        self.assertEqual(r["S02"]["state"],"facing=north;tucked=true;variant=1")
        self.assertEqual(r["S34"]["state"],"color=white;facing=north;shape=inner_left;waterlogged=false")

    def test_release_variants_are_enumerated_without_guessed_value(self):
        v=f5._values({"variants":{
            "facing=north,tucked=true,variant=1":{"model":"model"},
            "facing=south,tucked=false,variant=3":{"model":"model2"}}})
        self.assertEqual(v["facing"],["north","south"])
        self.assertEqual(v["tucked"],["false","true"])
        self.assertEqual(v["variant"],["1","3"])

    def test_12_stages_when_actual_table_present(self):
        stages=f5.stages(FAKE)
        self.assertEqual(len(stages),12)
        self.assertEqual(set(stages),set(f5.CHALLENGE_STAGES))
        self.assertIn("S02_ISOLATED",stages)
        self.assertIn("S34_L_EAST_SOUTH",stages)

    def test_10_stages_no_table_when_mod_asset_missing(self):
        v={**FAKE,"_table_present":False}
        stages=f5.stages(v)
        self.assertEqual(len(stages),10)
        self.assertFalse(any("TABLE" in k for k in stages))

    def test_server_properties_explicitly_probed_not_just_exact_boolean(self):
        for name,(commands,checks) in f5.stages(FAKE).items():
            self.assertIn("actual",checks)
            self.assertIn("subject",checks)
            props=checks["actual"]
            self.assertIn("present",props)
            self.assertIn("air",props)
            case="S02" if name.startswith("S02") else "S34"
            for k,values in FAKE[case].items():
                for value in values:
                    self.assertIn(f"{k}={value}",props)
            self.assertTrue(checks["subject"]["exact"].endswith(
                f5.S02_STATE if case=="S02" else f5.S34_STATE))

    def test_each_trial_clears_previous_neighborhood(self):
        for name,(commands,checks) in f5.stages(FAKE).items():
            self.assertTrue(commands[0].startswith("fill "))
            self.assertTrue(commands[-1].startswith("setblock 0 120 40 "))
            self.assertEqual(checks["subject"]["block"].split()[0:3],["0","120","40"])

    def test_non_diagnostic_stages_remain_original(self):
        self.assertEqual(runner.REMAINING,("S14","S15","S16","S17","S39","S40"))
        cases,source=runner.applications(("S02","S34"))
        self.assertEqual(set(cases),{"S02","S34"})
        self.assertEqual(len(source),64)
        self.assertEqual(set(runner.stages("1.21.1",case_ids=("S02","S34"),
                                         source_only=True)),{"S02","S34"})

    def test_opt_in_from_main_runner_has_identical_diagnostic_stage_set(self):
        diagnostic=runner.stages("1.21.1",FAKE,case_ids=("S02","S34"),
                                  source_only=True,diagnostic_mode=True)
        self.assertEqual(diagnostic,f5.stages(FAKE))

    def test_reject_wrong_version_or_mode_or_case_list(self):
        for bad in (
            {"version":"1.21.11","case_ids":("S02","S34"),"source_only":True},
            {"version":"1.21.1","case_ids":("S34",),"source_only":True},
            {"version":"1.21.1","case_ids":("S02","S34"),"source_only":False},
            {"version":"1.21.1","case_ids":("S02","S34"),"source_only":True,"interaction":True},
        ):
            version=bad.pop("version")
            with self.assertRaises((ValueError,AssertionError)):
                runner.stages(version,FAKE,diagnostic_mode=True,**bad)

    def test_f4_original_seven_unchanged(self):
        self.assertEqual(f4.CASES,("S01","S02","S31","S32","S33","S34","S47"))
        self.assertEqual(sum(f4.EXPECTED[c][3] for c in f4.CASES),60)
        self.assertEqual(sum(f4.EXPECTED[c][4] for c in f4.CASES),293)
        self.assertEqual(runner.state("handcrafted:white_glazed_medium_pot",""),
                         "handcrafted:white_glazed_medium_pot")

    def test_no_early_acceptance_assertion_in_stage_logic(self):
        stages=f5.stages(FAKE)
        self.assertIn("tucked=true",stages["S02_ISOLATED"][1]["subject"]["exact"])
        self.assertIn("shape=inner_left",stages["S34_ISOLATED"][1]["subject"]["exact"])

if __name__=="__main__":unittest.main()
