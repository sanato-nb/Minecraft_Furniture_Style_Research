"""INT-4-F3: fixed original cases, no source drift or old fixture breakage."""
import unittest
from mcfr import int4_f3_storage_shelf_light_capture as f
from mcfr import int4_nonchair_runtime as base

class SevenModCases(unittest.TestCase):
    def test_ids_exact_nonduplicated(self):
        self.assertEqual(f.CASES,("S20","S21","S26","S27","S44","S45","S46"))

    def test_source_original_case_filenames_sha(self):
        r,h=f.original_7_cases()
        self.assertEqual(set(r),set(f.CASES))
        self.assertEqual(len(h),64)

    def test_original_elements_faces(self):
        self.assertEqual(sum(f.EXPECTED[x][3] for x in f.CASES),30)
        self.assertEqual(sum(f.EXPECTED[x][4] for x in f.CASES),144)

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

    def test_lamp_pair_and_drawer_pair_preserved(self):
        src,_=f.original_7_cases()
        self.assertEqual(src["S20"]["block"],src["S21"]["block"])
        self.assertNotEqual(src["S20"]["state"],src["S21"]["state"])
        self.assertEqual(src["S44"]["block"],src["S45"]["block"])
        self.assertNotEqual(src["S44"]["state"],src["S45"]["state"])

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
