"""H7 six historic-risk cases: stage alias resolution and guardrail tests."""
import importlib.util,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
p=ROOT/"scripts/integration/build_int4_h7_six_risk_source_stage_audit.py"
sp=importlib.util.spec_from_file_location("mcfr_int4_h7",p)
h7=importlib.util.module_from_spec(sp);sp.loader.exec_module(h7)

class RiskSixOriginalStages(unittest.TestCase):
    def test_all_six_fixed_missing_original_H6_case_ids(self):
        self.assertEqual(h7.RISK,("R01","R02","R03","R04","R05","R07"))
        self.assertEqual({k:len(v) for k,v in h7.STAGES.items()},
                         {"R01":1,"R02":6,"R03":3,"R04":2,"R05":5,"R07":4})
    def test_six_distinct_actions_archives_and_21_case_occurrences(self):
        self.assertEqual(sum(map(len,h7.STAGES.values())),21)
        self.assertEqual(len({a for xs in h7.ART.values() for a in xs}),6)
        self.assertEqual(h7.ART["R02"],h7.ART["R07"])
        self.assertEqual(len(h7.ART["R05"]),2)
    def test_original_H6_and_F70_git_blobs_are_frozen(self):
        self.assertEqual(len(h7.PIN),6)
        for name,pin in h7.PIN.items():
            self.assertEqual(h7.blob(h7.fixed(name)),pin)
    def test_original_F70_all_still_conditional(self):
        r=h7.rows(h7.fixed("INT4_F11F_70_TARGET_EVIDENCE_DISPOSITIONS_V15.csv"))
        self.assertEqual(len(r),70)
        self.assertTrue(all(x["final_disposition"].startswith("CONDITIONAL") for x in r))
        self.assertTrue(all(x["runtime_evidence_accepted_as_full_F_PASS"]=="false" for x in r))
    def test_r01_reuses_real_S10_source_not_faked_R01_world_state(self):
        d={"server_states":{"S10":{"subject":{"exact":True}}}}
        self.assertEqual(h7.prove("R01","S10",d,False),"S10_SUBJECT_EXACT_TRUE")
        with self.assertRaises((KeyError,AssertionError)):
            h7.prove("R01","S10",{"server_states":{"R01":{"subject":{"exact":True}}}},False)
    def test_af_south_variant3_source_discontinuity_not_hidden(self):
        d={"states":[{"case_id":"AFV3_south","original_state":
          "another_furniture:acacia_chair[facing=south,tucked=false,variant=3]",
          "server_blockstate_verified":True,
          "original_model_target":"another_furniture:block/chair/acacia_1",
          "source_version_equivalence":"RELEASE_SOURCE_DIFF_MUST_VALIDATE_EACH_SELECTED_STATE"}]}
        self.assertIn("ACACIA_1",h7.prove("R07","AFV3_south",d,False))
        d["states"][0]["original_model_target"]="another_furniture:block/chair/acacia_3"
        with self.assertRaises(AssertionError):h7.prove("R07","AFV3_south",d,False)
    def test_r03_join_and_remove_requires_actual_neighbor_state(self):
        d={"observed_server_states":{
          "join":{"centre":{"block":"table","east":True},
                  "east":{"block":"table","west":True}},
          "remove":{"centre":{"block":"table","east":False},
                    "east":{"block":"air"}}},
          "transitions":{"joined_bidirectionally":True,
                         "automatically_disconnected_after_remove":True,
                         "player_item_placement_tested":False}}
        self.assertIn("JOIN",h7.prove("R03","join",d,False))
        self.assertIn("REMOVE",h7.prove("R03","remove",d,False))
        d["transitions"]["player_item_placement_tested"]=True
        with self.assertRaises(AssertionError):h7.prove("R03","join",d,False)
    def test_r04_water_state_must_be_explicit(self):
        d={"states":[{"case_id":"S43","server_blockstate_verified":True,
                       "block_id":"mcwfurnitures:oak_kitchen_sink",
                       "original_state":"mcwfurnitures:oak_kitchen_sink[facing=north,water=true]"}]}
        self.assertIn("S43",h7.prove("R04","S43",d,False))
        d["states"][0]["original_state"]="mcwfurnitures:oak_kitchen_sink[facing=north,water=false]"
        with self.assertRaises(AssertionError):h7.prove("R04","S43",d,False)
    def test_r05_two_separate_runs_and_bed_sleep_occupied(self):
        pos=lambda occupied:{"block":"present","facing":"north","occupied":occupied}
        d={"server_states":{"bed_sleeping":{
          "foot_position":pos("true"),"head_position":pos("true")}},
          "interaction":True,
          "sleep_timers":{"check_bed_sleeping":"positive","check_bed_awake":"zero"}}
        self.assertIn("BED_SLEEPING",h7.prove("R05","bed_sleeping",d,False))
        d["server_states"]["bed_sleeping"]["foot_position"]["occupied"]="false"
        with self.assertRaises(AssertionError):h7.prove("R05","bed_sleeping",d,False)
    def test_r05_destroy_requires_both_parts_air(self):
        d={"server_states":{"bed_foot_broken":{
          "foot_position":{"block":"air"},"head_position":{"block":"air"}}}}
        self.assertIn("BED_FOOT_BROKEN",h7.prove("R05","bed_foot_broken",d,True))
        d["server_states"]["bed_foot_broken"]["head_position"]["block"]="present"
        with self.assertRaises(AssertionError):h7.prove("R05","bed_foot_broken",d,True)
    def test_unknown_risk_alias_fails_closed(self):
        with self.assertRaises(AssertionError):h7.prove("R09","Z99",{},False)
    def test_H03_and_H05_current_gates_still_not_final(self):
        gates=h7.rows(h7.fixed("INT4_H6_H03_H05_SCOPE_REASSESSMENT_V1.csv"))
        lookup={x["gate_id"]:x for x in gates}
        self.assertEqual(lookup["H03"]["review_status"],"HOLD_FULL_F_EXIT")
        self.assertTrue(lookup["H05"]["review_status"].startswith("CONDITIONAL"))
        self.assertTrue(all(x["full_unconditional_exit_satisfied"]=="false" for x in gates))
if __name__=="__main__":unittest.main()
