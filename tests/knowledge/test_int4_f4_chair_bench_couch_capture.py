"""INT-4-F4: pinned chair/bench/sofa/pot original cases, no source drift or old fixture breakage."""
import unittest
from mcfr import int4_f4_chair_bench_couch_capture as f
from mcfr import int4_nonchair_runtime as base

class SevenModCases(unittest.TestCase):
    def test_ids_exact_nonduplicated(self):
        self.assertEqual(f.CASES,("S01","S02","S31","S32","S33","S34","S47"))

    def test_source_original_case_filenames_sha(self):
        r,h=f.original_7_cases()
        self.assertEqual(set(r),set(f.CASES))
        self.assertEqual(len(h),64)

    def test_original_elements_faces(self):
        self.assertEqual(sum(f.EXPECTED[x][3] for x in f.CASES),60)
        self.assertEqual(sum(f.EXPECTED[x][4] for x in f.CASES),293)

    def test_historical_applications_exact_seven(self):
        records,ledger=base.applications(f.CASES)
        self.assertEqual(set(records),set(f.CASES))
        self.assertTrue(all(len(a)==1 for a in records.values()))
        self.assertEqual(len(ledger),64)

    def test_each_stage_exact_block_id(self):
        stage=base.stages("1.21.1",case_ids=f.CASES,source_only=True)
        self.assertEqual(set(stage),set(f.CASES))
        for cid in f.CASES:
            actions,checks=stage[cid]
            self.assertTrue(any(cmd.startswith("setblock ") for cmd in actions))
            self.assertIn(f.EXPECTED[cid][1],checks["subject"]["exact"])
            self.assertIn(f.EXPECTED[cid][2].replace(";",","),checks["subject"]["exact"])

    def test_chair_tucked_pair_and_couch_corner_pair_preserved(self):
        src,_=f.original_7_cases()
        self.assertEqual(src["S01"]["block"],src["S02"]["block"])
        self.assertNotEqual(src["S01"]["state"],src["S02"]["state"])
        self.assertEqual(src["S33"]["block"],src["S34"]["block"])
        self.assertNotEqual(src["S33"]["state"],src["S34"]["state"])

    def test_no_property_pot_selects_bare_block_id_without_invalid_empty_brackets(self):
        rows,_=f.original_7_cases()
        self.assertEqual(rows["S47"]["state"],"")
        actual=base.state(rows["S47"]["block"],rows["S47"]["state"])
        self.assertEqual(actual,"handcrafted:white_glazed_medium_pot")
        commands,checks=base.stages("1.21.1",case_ids=("S47",),source_only=True)["S47"]
        self.assertTrue(any(c.endswith(" handcrafted:white_glazed_medium_pot") for c in commands))
        self.assertEqual(checks["subject"]["exact"],"0 120 40 handcrafted:white_glazed_medium_pot")

    def test_does_not_force_player_interaction_as_automatic(self):
        with self.assertRaises(ValueError):
            base.stages("1.21.1",case_ids=f.CASES,source_only=True,interaction=True)

    def test_old_historic_6_unmodified(self):
        self.assertEqual(base.REMAINING,("S14","S15","S16","S17","S39","S40"))
        original,_=base.applications()
        self.assertEqual(set(original),set(base.REMAINING))

    def test_old_4_and_new_7_disjoint(self):
        from mcfr import int4_f_missing_capture as old
        self.assertEqual(set(f.CASES)&set(old.CASES),set())

    def test_unknown_historical_case_fails(self):
        with self.assertRaises(ValueError):
            base.applications(["R01"])

if __name__=="__main__":
    unittest.main()
