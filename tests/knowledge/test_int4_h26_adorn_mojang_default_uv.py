"""H26 isolated Mojang FaceBakery.defaultFaceUV provenance and evidence guards."""
from collections import Counter
import copy
import json
from pathlib import Path
import unittest

from mcfr import int4_h26_adorn_mojang_default_uv as h
from mcfr import int4_h21_af16_release_comparison as h21


def original_mapping_fixture():
    head = (
        "net.minecraft.client.renderer.block.model.FaceBakery -> hqi:\n"
        "    28:34:net.minecraft.client.renderer.block.model.BlockElementFace$UVs "
        "defaultFaceUV(org.joml.Vector3fc,org.joml.Vector3fc,net.minecraft.core.Direction) -> a\n"
        "net.minecraft.core.Direction -> iz:\n"
    )
    for i, label in enumerate(("DOWN", "UP", "NORTH", "SOUTH", "WEST", "EAST")):
        head += "    static final net.minecraft.core.Direction " + label + " -> " + "abcdef"[i] + "\n"
    head += "net.minecraft.client.renderer.block.model.BlockElementFace$UVs -> hqc$b:\n"
    for f, m in zip(("minU", "minV", "maxU", "maxV"), "abcd"):
        head += "    float " + f + "() -> " + m + "\n"
    return head


class H26OriginalMojangUV(unittest.TestCase):
    def test_parent_H25_exact_source_pins_and_gate(self):
        source = h.load_h25()
        self.assertEqual(source["scope"]["verified_exact_selected_states"], 21)
        self.assertEqual(source["legacy_gates_unchanged"]["strict_F70_unconditional"], 0)
        self.assertEqual(source["legacy_gates_unchanged"]["H03"], "HOLD")
        self.assertEqual(source["legacy_gates_unchanged"]["H05"], "CONDITIONAL")
        self.assertEqual(source["legacy_gates_unchanged"]["INT5"], 0)
        self.assertEqual(source["legacy_gates_unchanged"]["INT6"], 0)

    def test_exact_mojang_pins(self):
        self.assertEqual(len(h.VANILLA_PNGS), 5)
        self.assertTrue(all(len(x) == 64 for x in h.VANILLA_PNGS.values()))
        self.assertEqual(h.MOJANG_MANIFEST_SHA1,
                         "a969d96978af7b52dba8df44e177f48ec4ebe0d8")
        self.assertEqual(h.MOJANG_CLIENT_SHA1,
                         "ba2df812c2d12e0219c489c4cd9a5e1f0760f5bd")
        self.assertTrue(h.PROBE.is_file())

    def test_original_exact_class_mapping_can_be_parsed(self):
        got = h.original_uv_mapping(original_mapping_fixture())
        self.assertEqual(got["face_bakery_class"], "hqi")
        self.assertEqual(got["direction_class"], "iz")
        self.assertEqual(got["uv_record_class"], "hqc$b")
        self.assertEqual(got["default_uv_method"], "a")
        self.assertEqual(got["direction_enum_names"],
                         {"down": "a", "up": "b", "north": "c",
                          "south": "d", "west": "e", "east": "f"})

    def test_wrong_original_mojang_method_rejected(self):
        changed = original_mapping_fixture().replace("defaultFaceUV(", "calculateFaceUV(")
        with self.assertRaisesRegex(ValueError, "defaultFaceUV signature"):
            h.original_uv_mapping(changed)

    def test_missing_enum_direction_rejected(self):
        changed = original_mapping_fixture().replace(
            "Direction NORTH -> c", "Direction SOMETHING -> c")
        with self.assertRaisesRegex(ValueError, "NORTH"):
            h.original_uv_mapping(changed)

    def test_wrong_original_uv_record_accessors_rejected(self):
        changed = original_mapping_fixture().replace("float maxV() -> d", "float maxV() -> x")
        with self.assertRaisesRegex(ValueError, "accessor mappings"):
            h.original_uv_mapping(changed)

    def test_mojang_default_formula_reference_six_directions(self):
        element = {"from": [2, 3, 4], "to": [9, 10, 11]}
        cases = {
            "down": [2, 5, 9, 12],
            "up": [2, 4, 9, 11],
            "north": [7, 6, 14, 13],
            "south": [2, 6, 9, 13],
            "west": [4, 6, 11, 13],
            "east": [5, 6, 12, 13],
        }
        for side, expected in cases.items():
            got, status = h21.uv_values(element, side, {"texture": "#test"})
            self.assertEqual(status, "DEFAULT")
            self.assertEqual(list(map(float, got)), expected)

    def test_explicit_uv_not_promoted_to_default(self):
        element = {"from": [2, 3, 4], "to": [9, 10, 11]}
        face = {"texture": "#test", "uv": [3.5, 1, 9.5, 9]}
        got, status = h21.uv_values(element, "north", face)
        self.assertEqual(status, "EXPLICIT")
        self.assertEqual(list(map(float, got)), face["uv"])

    def test_mojang_method_proof_is_separate_from_full_bake_and_F2(self):
        source = h.PROBE.read_text(encoding="utf-8")
        self.assertIn("FaceBakery.defaultFaceUV", source)
        self.assertIn("uv.invoke(null, from, to, enumerations.get(face))", source)
        self.assertNotIn("bakeQuad", source)
        self.assertNotIn("renderMinecraftClientFrame", source)

    def test_original_asset_library_not_redistributed(self):
        self.assertFalse(any(x.endswith(".png") for x in h.VANILLA_PNGS))
        self.assertEqual(h.H25_JSON_BLOB,
                         "5aefb171ab57d48aebba213ccedc8dbad268fbba")
        self.assertEqual(h.H25_CSV_BLOB,
                         "762c6f0b6b650b9ac4e137486f886e037149124a")


if __name__ == "__main__":
    unittest.main()
