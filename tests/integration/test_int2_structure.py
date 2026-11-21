"""INT-2 independent geometry and source-option regression tests."""
from pathlib import Path
import runpy
import unittest

AUDIT = runpy.run_path(str(Path(__file__).resolve().parents[2] / "scripts/integration/audit_int2_structure.py"))
ancestry = AUDIT["ancestry"]
source_faces = AUDIT["source_faces"]
state_model_options = AUDIT["state_model_options"]
block_model_path = AUDIT["block_model_path"]
compare_model = AUDIT["compare_model"]


class IndependentGeometryChecks(unittest.TestCase):
    def test_inherited_geometry_and_uv_slot_binding(self):
        base = "1.21.11/assets/minecraft/models/block/base.json"
        leaf = "1.21.11/assets/minecraft/models/block/leaf.json"
        models = {
            base: {
                "textures": {"top": "block/stone"},
                "elements": [
                    {"from": [0, 0, 0], "to": [16, 16, 16],
                     "faces": {"up": {"texture": "#top", "uv": [0, 0, 16, 16]},
                               "down": {"texture": "#later"}}},
                ],
            },
            leaf: {"parent": "minecraft:block/base", "textures": {"later": "minecraft:block/dirt"}},
        }
        pngs = {"1.21.11/assets/minecraft/textures/block/stone.png",
                "1.21.11/assets/minecraft/textures/block/dirt.png"}
        result = source_faces(leaf, models, pngs)
        self.assertEqual(result["parent_depth"], 1)
        self.assertEqual(result["elements"], 1)
        self.assertEqual(result["applied_faces"], 2)
        self.assertEqual(result["explicit_uv_faces"], 1)
        self.assertEqual(result["implicit_uv_faces"], 1)
        self.assertEqual(result["bound_png_faces"], 2)
        self.assertEqual(result["slot_count"], 2)
        self.assertEqual(result["unbound_template_faces"], 0)

    def test_missing_slot_is_not_promoted_to_png(self):
        path = "1.21.11/assets/minecraft/models/block/template.json"
        models = {path: {"elements": [{"faces": {"up": {"texture": "#missing"}}}]}}
        result = source_faces(path, models, set())
        self.assertEqual(result["unbound_template_faces"], 1)
        self.assertEqual(result["bound_png_faces"], 0)

    def test_cycle_is_error(self):
        a = "1.21.11/assets/minecraft/models/block/a.json"
        b = "1.21.11/assets/minecraft/models/block/b.json"
        models = {a: {"parent": "block/b"}, b: {"parent": "block/a"}}
        with self.assertRaisesRegex(ValueError, "cycle"):
            ancestry(a, models)

    def test_blockstate_alternatives_and_multipart(self):
        variants = {"variants": {
            "facing=north": [{"model": "minecraft:block/a", "weight": 2},
                             {"model": "minecraft:block/b"}],
            "facing=east": {"model": "minecraft:block/c"}}}
        multipart = {"multipart": [{"when": {"north": "true"}, "apply": {"model": "block/a"}},
                                    {"apply": [{"model": "block/b"}, {"model": "block/c"}]}]}
        self.assertEqual(len(state_model_options(variants)), 3)
        self.assertEqual(len(state_model_options(multipart)), 3)
        self.assertEqual(block_model_path("block/a"),
                         "1.21.11/assets/minecraft/models/block/a.json")
        with self.assertRaises(ValueError):
            state_model_options({"variants": {}, "multipart": []})

    def test_c_ledger_disagreement_is_reported(self):
        old = {
            "C_applied_faces": "2", "C_explicit_uv_faces": "1",
            "C_implicit_uv_key_absent_faces": "1",
            "C_bound_png_face_refs": "2", "C_template_unbound_face_refs": "0",
            "C_binding_rows": "1",
        }
        actual = {
            "applied_faces": 2, "explicit_uv_faces": 1,
            "implicit_uv_faces": 1, "bound_png_faces": 2,
            "unbound_template_faces": 0, "slot_count": 2,
        }
        self.assertEqual(len(compare_model(old, actual)), 1)


if __name__ == "__main__":
    unittest.main()
