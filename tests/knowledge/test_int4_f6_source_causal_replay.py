"""INT-4-F6 original coded chair tuck + HC inner/outer corner source tests."""
import unittest
from mcfr import int4_f6_source_causal_replay as f6
from mcfr import int4_nonchair_runtime as runner
from mcfr import int4_f5_state_diagnostic as f5
from mcfr import int4_f4_chair_bench_couch_capture as f4

FAKE={
    "S02":{
        "facing":["east","north","south","west"],
        "tucked":["false","true"],
        "variant":[str(i) for i in range(1,12)]
    },
    "S34":{
        "color":["none","white"],"facing":["east","north","south","west"],
        "shape":["single","left","middle","right","inner_left","inner_right",
                 "outer_left","outer_right"],
        "waterlogged":["false","true"],
    },
    "_table_present":True,
}

class F6OriginalSourceCausalReplay(unittest.TestCase):
    def test_f5_historical_original_model_sha_still_locked(self):
        originals,digest=f6.original_source()
        self.assertEqual(set(originals),{"S02","S34"})
        self.assertEqual(len(digest),64)
        self.assertEqual(f6.CHAIR_TARGET,
                         "another_furniture:oak_chair[facing=north,tucked=true,variant=1]")
        self.assertEqual(f6.COUCH_TARGET,
                         "handcrafted:oak_couch[color=white,facing=north,shape=inner_left,waterlogged=false]")

    def test_ten_fixed_source_condition_stage_names(self):
        plans=f6.stages(FAKE)
        self.assertEqual(tuple(plans),f6.TRIALS)
        self.assertEqual(len(plans),10)

    def test_chair_table_is_in_front_not_east_or_south(self):
        plans=f6.stages(FAKE)
        stage=plans["S02_NORTH_TABLE_TUCK"][0]
        self.assertIn("setblock 0 120 39 another_furniture:oak_table",stage)
        self.assertTrue(stage[-1].endswith(f6.CHAIR_TARGET))
        self.assertNotIn("setblock 1 120 40 another_furniture:oak_table",stage)

    def test_slab_north_top_is_source_approved_chair_tuck_support(self):
        commands=f6.stages(FAKE)["S02_NORTH_TOP_SLAB_TUCK"][0]
        self.assertIn("setblock 0 120 39 minecraft:oak_slab[type=top,waterlogged=false]",commands)

    def test_remove_slab_after_tucked_chair_requires_new_server_state(self):
        a=f6.stages(FAKE)["S02_NORTH_SLAB_REMOVED"][0]
        self.assertTrue(a[-1].endswith("minecraft:air"))
        self.assertTrue(a[-2].endswith(f6.CHAIR_TARGET))

    def test_hc_north_neighbor_west_facing_is_inner_left(self):
        cmds,checks=f6.stages(FAKE)["S34_NORTH_WEST_INNER_LEFT"]
        self.assertIn(
            "setblock 0 120 39 handcrafted:oak_couch[color=white,facing=west,shape=single,waterlogged=false]",
            cmds)
        self.assertIn("shape=inner_left",checks["subject"]["exact"])
        self.assertEqual(f6.EXPECTED_SHAPES["S34_NORTH_WEST_INNER_LEFT"],"inner_left")

    def test_hc_north_neighbor_east_is_inner_right(self):
        commands,_=f6.stages(FAKE)["S34_NORTH_EAST_INNER_RIGHT"]
        self.assertTrue(any("0 120 39 " in c and "facing=east" in c for c in commands))
        self.assertEqual(f6.EXPECTED_SHAPES["S34_NORTH_EAST_INNER_RIGHT"],"inner_right")

    def test_hc_south_neighbor_orientation_selects_outer_corner(self):
        cases=f6.stages(FAKE)
        for direction,expected in (("WEST","outer_left"),("EAST","outer_right")):
            stage="S34_SOUTH_"+direction+"_"+expected.upper()
            commands,_=cases[stage]
            self.assertTrue(any("0 120 41 " in c for c in commands))
            self.assertEqual(f6.EXPECTED_SHAPES[stage],expected)

    def test_east_neighbor_blocks_inner_left_selection_even_with_north_west(self):
        commands,_=f6.stages(FAKE)["S34_NORTH_WEST_EAST_OCCUPIED"]
        self.assertEqual(len(commands),4)
        self.assertTrue(any("setblock 1 120 40 " in c for c in commands))
        self.assertEqual(f6.EXPECTED_SHAPES["S34_NORTH_WEST_EAST_OCCUPIED"],"right")

    def test_every_f6_case_has_actual_server_property_probe(self):
        for k,(commands,predicates) in f6.stages(FAKE).items():
            self.assertEqual(set(predicates),{"subject","actual"})
            self.assertIn("present",predicates["actual"])
            self.assertIn("exact",predicates["subject"])
            self.assertTrue(commands[0].startswith("fill "))
            self.assertEqual(commands[0],f6.stages(FAKE)[k][0][0])

    def test_runner_opt_in_f6_not_f5_and_original_f4_untouched(self):
        actual=runner.stages("1.21.1",FAKE,source_only=True,
                              case_ids=("S02","S34"),diagnostic_mode="f6")
        self.assertEqual(actual,f6.stages(FAKE))
        legacy=runner.stages("1.21.1",FAKE,source_only=True,
                              case_ids=("S02","S34"),diagnostic_mode=True)
        self.assertEqual(len(legacy),12)
        self.assertEqual(f4.CASES,("S01","S02","S31","S32","S33","S34","S47"))

    def test_release_git_sha_pins_are_explicit_not_current_moving_branch(self):
        self.assertEqual(len(f6.SOURCE_PINS),5)
        self.assertEqual(f6.SOURCE_PINS["af_git_commit"],
                         "57eb624cbb7f408d43398c7434b0d38d312cb55d")
        self.assertEqual(f6.SOURCE_PINS["hc_git_commit"],
                         "8d21d1665916850c3fa3bdaf1370c50ec2ca7035")

    def test_original_mode_wrong_version_and_case_selection_fails(self):
        for version,ids in (
            ("1.21.11",("S02","S34")),
            ("1.21.1",("S02",)),
            ("1.21.1",("S02","S02")),
        ):
            with self.assertRaises((ValueError,AssertionError)):
                runner.stages(version,FAKE,source_only=True,
                              case_ids=ids,diagnostic_mode="f6")

    def test_no_uv_rights_or_final_f_approval_in_study(self):
        self.assertEqual(f6.MODE,"f6")
        self.assertEqual(f6.HISTORY_EXPECTED_EXACT,
                         {"S02_NORTH_TABLE_TUCK","S02_NORTH_TOP_SLAB_TUCK",
                          "S34_NORTH_WEST_INNER_LEFT"})

if __name__=="__main__":
    unittest.main()
