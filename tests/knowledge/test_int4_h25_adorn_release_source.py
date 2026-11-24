"""Unit checks for exact-source Adorn 7.6.1 selection and evidence limits."""
import copy
import json
import unittest
from pathlib import Path

from mcfr import int4_h25_adorn_release_source as m


class H25AdornReleaseSource(unittest.TestCase):
    def test_release_and_upstream_sha_frozen(self):
        self.assertEqual(len(m.SOURCE_BLOBS), 9)
        self.assertEqual(m.UPSTREAM_COMMIT, "6bfee0ee1ec2c259a577c5cde0b038641874fb2c")
        self.assertEqual(len(m.RELEASE_SHA256), 64)
        self.assertEqual(m.RELEASE_FILE, "Adorn-7.6.1+1.21.11-fabric.jar")

    def test_model_path_and_external_vanilla_boundary(self):
        self.assertEqual(m.model_member("adorn:block/templates/shelf"),
                         "assets/adorn/models/block/templates/shelf.json")
        self.assertIsNone(m.model_member("minecraft:block/block"))
        self.assertIsNone(m.model_member("block/block"))
        with self.assertRaisesRegex(ValueError, "unverified external"):
            m.model_member("minecraft:block/cube_all")
        with self.assertRaisesRegex(ValueError, "unrecognized"):
            m.model_member("adorn:block/../bad")

    def test_parent_geometry_and_child_texture_override(self):
        files = {
            "assets/adorn/models/block/example.json": {
                "parent": "adorn:block/templates/example",
                "textures": {"a": "minecraft:block/stone"},
            },
            "assets/adorn/models/block/templates/example.json": {
                "parent": "minecraft:block/block",
                "textures": {"a": "minecraft:block/oak_planks", "b": "#a"},
                "elements": [{
                    "from": [0, 0, 0], "to": [16, 16, 16],
                    "faces": {
                        "north": {"texture": "#b", "uv": [0, 0, 16, 16]},
                        "up": {"texture": "#a"},
                        "south": {"texture": "#a", "uv": [1, 1, 1, 4]},
                    },
                }],
            },
        }
        p = m.model_profile("adorn:block/example", files)
        self.assertEqual(p["source_elements"], 1)
        self.assertEqual(p["source_faces"], 3)
        self.assertEqual(p["explicit_uv_faces"], 2)
        self.assertEqual(p["implicit_uv_faces_require_bake"], 1)
        self.assertEqual(p["documented_zero_area_explicit_uv_faces"], 1)
        self.assertEqual(p["resolved_face_textures"], {"minecraft:block/stone": 3})

    def test_circular_texture_and_parent_rejected(self):
        with self.assertRaisesRegex(ValueError, "circular"):
            m.resolve_texture("#a", {"a": "#b", "b": "#a"})
        files = {"assets/adorn/models/block/cycle.json":
                 {"parent": "adorn:block/cycle", "elements": [
                     {"from": [0, 0, 0], "to": [1, 1, 1],
                      "faces": {"north": {"texture": "minecraft:block/stone"}}}]}}
        with self.assertRaisesRegex(ValueError, "cyclic"):
            m.model_profile("adorn:block/cycle", files)

    def test_facing_variants_and_unknown_state_rejected(self):
        d = {"variants": {
            "facing=east": {"model": "adorn:block/iron_shelf"},
            "facing=west": {"model": "adorn:block/iron_shelf", "y": 180},
        }}
        self.assertEqual(m.selected_parts(d, {"facing": "west"})[0]["y"], 180)
        with self.assertRaisesRegex(ValueError, "missing exact"):
            m.selected_parts(d, {"facing": "south"})

    def test_variant_order_independent(self):
        d = {"variants": {
            "facing=north,waterlogged=false": {"model": "adorn:block/iron_shelf"}
        }}
        self.assertEqual(len(m.selected_parts(d, {"waterlogged": False, "facing": "north"})), 1)

    def test_multipart_bool_and_string_cases(self):
        d = {"multipart": [
            {"when": {"facing": "north", "active": False},
             "apply": {"model": "adorn:block/brewer"}},
            {"when": {"facing": "north", "active": True},
             "apply": {"model": "adorn:block/brewer_active"}},
            {"when": {"facing": "north", "has_mug": "true"},
             "apply": {"model": "adorn:block/brewer_mug"}},
        ]}
        s = {"facing": "north", "active": True, "has_mug": True}
        self.assertEqual([x["model"] for x in m.selected_parts(d, s)],
                         ["adorn:block/brewer_active", "adorn:block/brewer_mug"])
        s["has_mug"] = False
        self.assertEqual(len(m.selected_parts(d, s)), 1)
        s["active"] = False
        self.assertEqual(m.selected_parts(d, s)[0]["model"], "adorn:block/brewer")

    def test_reject_unsupported_multipart_state(self):
        d = {"multipart": [{"when": {"OR": [{"north": True}, {"south": True}]},
                            "apply": {"model": "adorn:block/brewer"}}]}
        with self.assertRaisesRegex(ValueError, "unsupported"):
            m.selected_parts(d, {"facing": "north"})

    def test_existing_legacy_gates_still_unapproved(self):
        i = m.ROOT / "project/integration"
        v5 = json.loads((i / "INT4_F70_MODELING_CONTRACT_SUMMARY_V5.json").read_text())
        h24 = json.loads((i / "INT4_H24_CROSSMOD_OAK_TABLE_RESULT_V1.json").read_text())
        self.assertEqual(v5["combined_review_scope_only"]["closed_units"], 70)
        self.assertEqual(v5["legacy_F70"]["unconditional"], 0)
        self.assertEqual(h24["strict_legacy_F70"]["H03"], "HOLD")
        self.assertEqual(h24["strict_legacy_F70"]["H05"], "CONDITIONAL")
        self.assertEqual(h24["strict_legacy_F70"]["INT5"], 0)
        self.assertEqual(h24["strict_legacy_F70"]["INT6"], 0)


if __name__ == "__main__":
    unittest.main()
