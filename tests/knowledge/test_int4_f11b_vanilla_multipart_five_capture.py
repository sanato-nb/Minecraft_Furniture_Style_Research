"""F11B original vanilla 5 cases, 12 simultaneous model selectors, 13 elements, 45 faces."""
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from mcfr import int4_f11b_vanilla_multipart_five_capture as f11b
from mcfr import int4_f11_vanilla_five_capture as f11a
from mcfr.chair_runtime_fixture import pack_lines,make_pack

class F11BOriginalVanillaSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.selected,cls.sha=f11b.source_rows()

    def test_five_original_source_cases_and_sha(self):
        self.assertEqual(f11b.ORDER,("V03","V04","V06","V08","V09"))
        self.assertEqual(self.sha,f11b.PIN_LEDGER_SHA256)
        self.assertEqual(len(self.selected),5)

    def test_twelve_selected_models_in_five_cases(self):
        self.assertEqual({k:len(v) for k,v in self.selected.items()},
                         {"V03":2,"V04":1,"V06":1,"V08":7,"V09":1})
        self.assertEqual(sum(len(v) for v in self.selected.values()),12)

    def test_original_model_13_elements_45_faces(self):
        self.assertEqual(sum(sum(int(r["elements"]) for r in group)
                             for group in self.selected.values()),13)
        self.assertEqual(sum(sum(int(r["faces"]) for r in group)
                             for group in self.selected.values()),45)
        self.assertEqual({k:sum(int(r["faces"]) for r in group)
                          for k,group in self.selected.items()},
                          {"V03":16,"V04":6,"V06":6,"V08":11,"V09":6})

    def test_original_v03_two_multipart_selections(self):
        rows=self.selected["V03"]
        self.assertEqual({int(r["rule_index"]) for r in rows},{0,1})
        self.assertEqual({int(r["uvlock"]) for r in rows},{0,1})
        self.assertEqual({r["model_path"].rsplit("/",1)[-1] for r in rows},
                         {"oak_fence_post.json","oak_fence_side.json"})

    def test_original_v08_seven_multipart_selections(self):
        rows=self.selected["V08"]
        self.assertEqual({int(r["rule_index"]) for r in rows},{0,1,4,6,8,10,12})
        self.assertEqual({int(r["faces"]) for r in rows},{1,5})
        self.assertEqual({int(r["elements"]) for r in rows},{1})
        state=f11b.EXPECTED["V08"][1]
        self.assertEqual(state["slot_0_occupied"],"true")
        self.assertEqual(sum(v=="true" for k,v in state.items() if k.endswith("_occupied")),1)

    def test_condition_tree_true_and_false_rules(self):
        props={"north":"true","south":"false","slot_0_occupied":"true"}
        self.assertTrue(f11b.matches_when(None,props))
        self.assertTrue(f11b.matches_when({"north":"true"},props))
        self.assertFalse(f11b.matches_when({"north":"false"},props))
        self.assertTrue(f11b.matches_when({"OR":[{"west":"true"},{"north":"true"}]},props))
        self.assertTrue(f11b.matches_when({"AND":[{"north":"true"},{"south":"false"}]},props))
        self.assertFalse(f11b.matches_when({"slot_0_occupied":"false"},props))

    def test_actual_fence_neighbor_is_disposable_world_source_not_guessed_state(self):
        cases=f11b.capture_cases()
        self.assertEqual({c.case_id for c in cases},set(f11b.ORDER))
        with TemporaryDirectory() as folder:
            pack=Path(folder)/"pack"
            make_pack(f11b.VERSION,pack,selected_cases=cases)
            rule=f11b.prepare_fence_neighbor_datapack(pack)
            data=(pack/"data/mcfr_chair/function/place.mcfunction").read_text()
            self.assertIn(rule,data)
            self.assertEqual(data.count(rule),1)
            fence=next(x for x in cases if x.case_id=="V03")
            self.assertIn(f"setblock {fence.x} {fence.y} {fence.z-1} minecraft:oak_fence",rule)
            self.assertTrue(any("MCFR_CHAIR_STATE_V03=PASS" in x for x in
                                (pack/"data/mcfr_chair/function/verify.mcfunction").read_text().splitlines()))

    def test_original_source_hash_kind_is_40_character_git_blob_sha1(self):
        for group in self.selected.values():
            for row in group:
                self.assertEqual(row["model_hash_kind"],"GIT_BLOB_SHA1")
                for what in ("state","model","provider"):
                    self.assertEqual(len(row[what+"_sha"]),40)

    def test_f11a_old_batch_unchanged(self):
        self.assertEqual(f11a.ORDER,("V01","V02","V05","V07","V10"))
        self.assertTrue(set(f11b.ORDER).isdisjoint(f11a.ORDER))

    def test_reject_wrong_minecraft_version(self):
        with self.assertRaises(ValueError):f11b.capture_cases("1.21.1")

if __name__=="__main__":
    unittest.main()
