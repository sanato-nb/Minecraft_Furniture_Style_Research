"""H24 selected oak_table source/UV independence and approval guards."""
import copy
import unittest

from mcfr import int4_h24_crossmod_oak_table as m


class H24CrossModOakTable(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sources = m.load_sources()
        cls.result = m.reconcile(*cls.sources)

    def test_all_six_pinned_original_cases(self):
        cases = self.result["cases"]
        self.assertEqual([x["target_id"] for x in cases],
                         ["S14", "S15", "S16", "S17", "S18", "S19"])
        self.assertEqual([x["source_elements"] for x in cases], [13, 1, 10, 2, 6, 1])
        self.assertEqual([x["source_faces"] for x in cases], [42, 6, 60, 12, 31, 6])
        self.assertEqual([x["source_uv_measured_faces"] for x in cases],
                         [42, 6, 40, 8, 31, 6])
        self.assertEqual([x["documented_zero_uv_faces"] for x in cases],
                         [0, 0, 20, 4, 0, 0])
        self.assertEqual(len({x["original_f2_sha256s"] for x in cases}), 6)

    def test_different_state_mechanics_not_cross_mod_equivalence(self):
        pairs = self.result["within_mod_comparisons"]
        self.assertEqual([p["changed_state_keys"] for p in pairs], [
            ["leg_1", "leg_2", "leg_3", "leg_4"],
            ["shape"],
            ["east", "north", "south", "west"],
        ])
        self.assertEqual([p["selected_model_delta"]["source_faces"] for p in pairs],
                         [36, 48, 25])
        self.assertTrue(self.result["research_scope"]["not_claimed_as_equivalent_state"])

    def test_release_versions_and_model_applications(self):
        cases = self.result["cases"]
        self.assertEqual([x["minecraft_version"] for x in cases],
                         ["1.21.1"] * 4 + ["1.21.11"] * 2)
        self.assertEqual([x["source_applications"] for x in cases],
                         [5, 1, 1, 1, 1, 1])
        self.assertEqual([x["cohort"] for x in cases], ["AF", "AF", "HC", "HC", "MACAW", "MACAW"])
        self.assertEqual(len(cases[0]["selected_model_paths"]), 2)

    def test_original_F2_hash_corruption_rejected(self):
        h21, h22, ledger, summary = copy.deepcopy(self.sources)
        next(x for x in ledger if x["target_id"] == "S18")["original_f2_sha256s"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "native F2 identity"):
            m.reconcile(h21, h22, ledger, summary)

    def test_wrong_original_face_rejected(self):
        h21, h22, ledger, summary = copy.deepcopy(self.sources)
        h21["cases"]["S14"]["applications"][1]["faces"] += 1
        with self.assertRaisesRegex(ValueError, "original UV proof|original selected-model geometry"):
            m.reconcile(h21, h22, ledger, summary)

    def test_zero_uv_reclassification_rejected(self):
        h21, h22, ledger, summary = copy.deepcopy(self.sources)
        next(x for x in ledger if x["target_id"] == "S16")["documented_zero_uv_faces"] = "0"
        with self.assertRaisesRegex(ValueError, "UV face accounting"):
            m.reconcile(h21, h22, ledger, summary)

    def test_legacy_approvals_cannot_be_promoted(self):
        h21, h22, ledger, summary = copy.deepcopy(self.sources)
        summary["legacy_F70"]["H03"] = "PASS"
        with self.assertRaisesRegex(ValueError, "original approvals"):
            m.reconcile(h21, h22, ledger, summary)
        h21, h22, ledger, summary = copy.deepcopy(self.sources)
        next(x for x in ledger if x["target_id"] == "S14")["INT6_rights_approved"] = "true"
        with self.assertRaisesRegex(ValueError, "approval boundary"):
            m.reconcile(h21, h22, ledger, summary)

    def test_duplicate_state_property_rejected(self):
        with self.assertRaisesRegex(ValueError, "duplicate"):
            m.parse_state("east=false;east=true")
        with self.assertRaisesRegex(ValueError, "invalid"):
            m.parse_state("east=false;north")

    def test_input_pins_and_persisted_results(self):
        self.assertEqual(len(m.PINS), 4)
        m.verify_saved(self.result)
        self.assertEqual(self.result["research_scope"]["new_game_runs"], 0)
        self.assertEqual(self.result["research_scope"]["new_F2"], 0)
        self.assertEqual(self.result["strict_legacy_F70"]["unconditional"], 0)
        self.assertEqual(self.result["strict_legacy_F70"]["INT5"], 0)
        self.assertEqual(self.result["strict_legacy_F70"]["INT6"], 0)


if __name__ == "__main__":
    unittest.main()
