"""INT-4 H27 source provenance and negative controls for actual Mojang vertices."""
import copy
import json
import unittest
from collections import Counter

from mcfr import int4_h27_adorn_mojang_rotation_vertices as h
from mcfr import int4_h25_adorn_release_source as h25


class H27OfficialAdornMojangRotation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.h26result, cls.h25result = h.load_parent()
        grouped = {}
        for f in cls.h26result["five_model_unique_source_faces"]:
            key = f["model"]
            elements = grouped.setdefault(key, {})
            element = {
                "element_index": f["element"],
                "from": f["from"], "to": f["to"],
                "original_element_rotation": f["element_rotation_declaration"],
            }
            old = elements.get(f["element"])
            if old is not None:
                assert old == element
            elements[f["element"]] = element
        cls.elements = {m: [v[k] for k in sorted(v)] for m, v in grouped.items()}

    def test_parent_H26_sources_are_exactly_pinned(self):
        self.assertEqual(len(self.h26result["five_model_unique_source_faces"]), 139)
        self.assertEqual(self.h26result["counts"]["state_weighted_original_mojang_default_uv"], 400)
        self.assertEqual(self.h26result["counts"]["state_weighted_source_faces"], 656)
        self.assertEqual(self.h26result["preserved_approvals"]["strict_F70_unconditional"], 0)

    def test_adorn_five_original_models_have_29_distinct_elements(self):
        self.assertEqual([len(self.elements[m]) for m in h25.MODELS], [12, 3, 3, 3, 8])
        self.assertEqual(sum(map(len, self.elements.values())), 29)
        shelf = self.elements["adorn:block/iron_shelf"]
        self.assertIsNone(shelf[0]["original_element_rotation"])
        self.assertEqual([x["original_element_rotation"]["axis"] for x in shelf[1:]], ["z", "z"])
        self.assertEqual([x["original_element_rotation"]["angle"] for x in shelf[1:]], [-45, -45])

    def test_exact_21_state_and_136_element_instances(self):
        cases, rows = h.build_selected_elements(self.h25result, self.elements)
        self.assertEqual(len(cases), 21)
        self.assertEqual(len(rows), 136)
        self.assertEqual(sum(x["model_applications"] for x in cases), 29)
        self.assertEqual(sum(x["source_faces"] for x in cases), 656)
        self.assertEqual(sum(r["element_rotation_axis"] != "none" for r in rows), 8)
        self.assertEqual(len({x["id"] for x in rows}), 136)

    def test_iron_shelf_four_directions_not_no_rotation(self):
        cases, rows = h.build_selected_elements(self.h25result, self.elements)
        shelves = [c for c in cases if c["block"] == "adorn:iron_shelf"]
        self.assertEqual(len(shelves), 4)
        self.assertEqual([c["state"]["facing"] for c in shelves],
                         ["north", "east", "south", "west"])
        self.assertEqual([c["source_y_rotations"] for c in shelves],
                         [[270], [0], [90], [180]])

    def test_brewer_state_y_and_optional_mug_provenance(self):
        cases, rows = h.build_selected_elements(self.h25result, self.elements)
        brewer = [c for c in cases if c["block"] == "adorn:brewer"]
        self.assertEqual(len(brewer), 16)
        self.assertEqual(Counter(c["source_elements"] for c in brewer), {3: 8, 11: 8})
        self.assertEqual(sum(c["source_faces"] for c in brewer), 8*16 + 8*51)
        self.assertEqual({tuple(c["source_y_rotations"]) for c in brewer},
                         {(0,), (90,), (180,), (270,),
                          (0, 0), (90, 90), (180, 180), (270, 270)})

    def test_bogus_original_state_orientation_fail_closed(self):
        corrupted = copy.deepcopy(self.h25result)
        corrupted["selected_state_cases"][1]["selected"][0]["y"] = 45
        with self.assertRaisesRegex(ValueError, "selected model/state rotation"):
            h.build_selected_elements(corrupted, self.elements)

    def test_bogus_uv_lock_fail_closed(self):
        corrupted = copy.deepcopy(self.h25result)
        corrupted["selected_state_cases"][1]["selected"][0]["uvlock"] = True
        with self.assertRaisesRegex(ValueError, "UV-lock"):
            h.build_selected_elements(corrupted, self.elements)

    def test_original_shelf_element_angle_drift_fail_closed(self):
        broken = copy.deepcopy(self.elements)
        broken["adorn:block/iron_shelf"][1]["original_element_rotation"]["angle"] = -30
        with self.assertRaisesRegex(ValueError, "element rotations drift"):
            h.build_selected_elements(self.h25result, broken)

    def test_original_mojang_class_mapping_must_be_pinned(self):
        with self.assertRaisesRegex(ValueError, "mapped original class"):
            h.official_mapping("arbitrary class content")
        self.assertEqual(h.ORIGINAL_CLASSES["bakery"],
                         "net.minecraft.client.renderer.block.model.FaceBakery")
        self.assertTrue(h.PROBE.is_file())
        java = h.PROBE.read_text(encoding="utf-8")
        self.assertIn("rotate.invoke(null, vertex, blockCenter, originalStateMatrix)", java)
        self.assertIn("elementTransform.invoke(originalElement)", java)
        self.assertNotIn("bakeQuad(", java)

    def test_original_approvals_and_no_game_calls(self):
        approved = self.h26result["preserved_approvals"]
        self.assertEqual(approved["H03"], "HOLD")
        self.assertEqual(approved["H05"], "CONDITIONAL")
        self.assertEqual(approved["INT5"], 0)
        self.assertEqual(approved["INT6"], 0)
        self.assertFalse(approved["GPU_per_face_approved"])


if __name__ == "__main__":
    unittest.main()
