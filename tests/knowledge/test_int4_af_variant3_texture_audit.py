"""Offline fail-closed regressions for AF variant=3 original-source exception."""
import copy
import unittest
from pathlib import Path

from mcfr import int4_af_variant3_texture_audit as a


class Variant3SourceAuditTest(unittest.TestCase):
    @staticmethod
    def example_states():
        variants = {a.selector(d): {
            "model": a.expected_model(d),
            **({"y": i * 90} if i else {})
        } for i, d in enumerate(a.DIRECTIONS)}
        variants.update({f"synthetic={i}": {"model": "another_furniture:block/chair/acacia_1"}
                         for i in range(84)})
        return {"variants": variants}

    @staticmethod
    def original_like_models():
        faces = ("north", "east", "south", "west", "up")
        elements = []
        for i in range(10):
            names = faces if i < 6 else faces[:4]
            slot = "#back" if i in (7, 8, 9) else "#bottom"
            elements.append({
                "from": [i, 0, 1], "to": [i + 1, 4, 2],
                "faces": {face: {"texture": slot, "uv": [0, 0, 4, 4]} for face in names},
            })
        return {
            a.PARENT: {"elements": elements},
            a.CHILDREN[0]: {"parent": "another_furniture:block/template/chair",
                            "textures": {"back": a.BACK_SOURCE[
                                "another_furniture:block/chair/acacia_1"],
                                "bottom": "another_furniture:block/chair/bottom/acacia"}},
            a.CHILDREN[1]: {"parent": "another_furniture:block/template/chair",
                            "textures": {"back": a.BACK_SOURCE[
                                "another_furniture:block/chair/acacia_3"],
                                "bottom": "another_furniture:block/chair/bottom/acacia"}},
        }

    def test_selectors_exact_three_three_one_model_counts(self):
        states = self.example_states()
        rows = a.state_rows(states, copy.deepcopy(states))
        self.assertEqual(len(rows), 4)
        self.assertEqual([r["model"] for r in rows], [
            "another_furniture:block/chair/acacia_3",
            "another_furniture:block/chair/acacia_3",
            "another_furniture:block/chair/acacia_1",
            "another_furniture:block/chair/acacia_3"
        ])
        self.assertEqual([r["y"] for r in rows], [0, 90, 180, 270])
        self.assertEqual(sum(r["different_model_from_variant3_majority"] for r in rows), 1)
        self.assertFalse(any(r["game_client_visual_verified"] for r in rows))

    def test_runtime_release_selector_mismatch_blocks_evidence(self):
        a1 = self.example_states()
        a2 = copy.deepcopy(a1)
        a2["variants"][a.selector("south")]["model"] = "another_furniture:block/chair/acacia_3"
        with self.assertRaisesRegex(a.EvidenceError, "selector semantic difference"):
            a.state_rows(a1, a2)

    def test_different_rotation_blocks_evidence(self):
        a1 = self.example_states()
        a1["variants"][a.selector("west")]["y"] = 0
        with self.assertRaisesRegex(a.EvidenceError, "direction rotation"):
            a.state_rows(a1, copy.deepcopy(a1))

    def test_same_geometry_uv_different_back_face_bindings(self):
        faces, summary = a.compare_inherited_models(self.original_like_models())
        self.assertEqual(summary["element_count_each"], 10)
        self.assertEqual(summary["face_count_each"], 46)
        self.assertEqual(summary["changed_texture_binding_faces"], 12)
        self.assertEqual(summary["unchanged_texture_binding_faces"], 34)
        self.assertEqual(summary["changed_element_indices"], [7, 8, 9])
        self.assertTrue(all(r["same_face_uv"] for r in faces))

    def test_changed_geometry_rejected_as_texture_only(self):
        d = self.original_like_models()
        d[a.CHILDREN[1]]["elements"] = copy.deepcopy(d[a.PARENT]["elements"])
        d[a.CHILDREN[1]]["elements"][0]["to"] = [8, 4, 2]
        with self.assertRaisesRegex(a.EvidenceError, "geometry or per-face UV mismatch"):
            a.compare_inherited_models(d)

    def test_non_back_texture_binding_change_rejected(self):
        d = self.original_like_models()
        d[a.CHILDREN[1]]["textures"]["bottom"] = "another_furniture:block/chair/bottom/other"
        with self.assertRaisesRegex(a.EvidenceError, "Different texture slot beyond"):
            a.compare_inherited_models(d)

    def test_original_int3_study_scope_still_pinned(self):
        hashes = a.verify_historical(Path(__file__).resolve().parents[2])
        self.assertEqual(len(hashes), 2)
        self.assertTrue(all(len(s) == 64 for s in hashes.values()))

    def test_composited_pixel_transparent_matter_is_separate(self):
        self.assertEqual(a.composite((100, 20, 10, 0), 0), (0, 0, 0))
        self.assertEqual(a.composite((100, 20, 10, 0), 255), (255, 255, 255))
        self.assertEqual(a.composite((20, 30, 40, 255), 0), (20, 30, 40))


if __name__ == "__main__":
    unittest.main()
