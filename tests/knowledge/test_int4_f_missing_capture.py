"""INT-4-F2 missing original cases: do not claim screenshot=semantic model approval."""
import unittest
from mcfr import int4_f_missing_capture as q
from mcfr import int4_nonchair_runtime as nc

class FourMissingHistoricalCaseTests(unittest.TestCase):
    def test_case_ids(self):
        self.assertEqual(q.CASES,("S05","S06","S07","S10"))

    def test_original_four_records_and_hash(self):
        rows,sha=q.original_4_cases()
        self.assertEqual(set(rows),set(q.CASES))
        self.assertEqual(len(sha),64)

    def test_category_case_counts(self):
        self.assertEqual(sum(q.EXPECTED[x][3] for x in q.CASES),42)
        self.assertEqual(sum(q.EXPECTED[x][4] for x in q.CASES),248)

    def test_selected_one_to_one_application(self):
        rows,sha=nc.applications(case_ids=q.CASES)
        self.assertEqual(set(rows),set(q.CASES))
        self.assertTrue(all(len(x)==1 for x in rows.values()))

    def test_source_only_stages_have_exact_four(self):
        cases=nc.stages("1.21.1",case_ids=q.CASES,source_only=True)
        self.assertEqual(set(cases),set(q.CASES))
        self.assertTrue(all("subject" in checks for _,checks in cases.values()))

    def test_source_only_cannot_use_unsupported_interaction(self):
        with self.assertRaises(ValueError):
            nc.stages("1.21.1",case_ids=q.CASES,source_only=True,interaction=True)

    def test_duplicate_case_selector_rejected(self):
        with self.assertRaises(ValueError):
            nc.applications(case_ids=["S05","S05"])

    def test_unlisted_case_rejected(self):
        with self.assertRaises(ValueError):
            nc.applications(case_ids=["R01"])

    def test_old_source_cases_unchanged(self):
        rows,_=nc.applications()
        self.assertEqual(set(rows),set(nc.REMAINING))
        self.assertEqual(set(nc.REMAINING),{"S14","S15","S16","S17","S39","S40"})

    def test_old_scoped_stages_still_include_bed(self):
        stages=nc.stages("1.21.1",{"facing":["north"]})
        self.assertIn("bed_empty",stages)
        self.assertIn("S14",stages)

    def test_case_selected_state_serialization(self):
        rows,_=q.original_4_cases()
        self.assertEqual(nc.state(rows["S10"]["block"],rows["S10"]["state"]),
            "handcrafted:oak_side_table[color=none,facing=north,waterlogged=false]")

if __name__=="__main__":
    unittest.main()
