"""Offline regression tests for the AF 4.0.2/4.0.3 version boundary."""
import unittest
from mcfr import af_release_version_audit as d


class AFVersionDiffTest(unittest.TestCase):
    def test_github_pin_matches_previous_int3_source_record(self):
        self.assertEqual(d.UPSTREAM, "57eb624cbb7f408d43398c7434b0d38d312cb55d")
        self.assertEqual(d.EXPECTED_SOURCE_BLOB,
                         "37643398d7a49fdcfc6f2308ca04c13fb0b43aed")
        self.assertEqual(len(d.PINNED_PARENT_BLOBS), 2)

    def test_variant_statuses_are_not_guessed_from_blob_sha(self):
        research = {"variants": {"facing=north,tucked=false,variant=1":
                                 {"model": "another_furniture:block/chair/acacia_1"},
                                 "facing=south,tucked=false,variant=1":
                                 {"model": "another_furniture:block/chair/acacia_1", "y": 180},
                                 "facing=east,tucked=false,variant=1":
                                 {"model": "another_furniture:block/chair/acacia_1", "y": 90}}}
        runtime = {"variants": {"facing=north,tucked=false,variant=1":
                                {"model": "another_furniture:block/chair/acacia_1"},
                                "facing=south,tucked=false,variant=1":
                                {"model": "another_furniture:block/chair/acacia_2", "y": 180},
                                "facing=west,tucked=false,variant=1":
                                {"model": "another_furniture:block/chair/acacia_1", "y": 270}}}
        rows = {r["selector"]: r for r in d.compare_variant(research, runtime)}
        self.assertEqual(rows["facing=north,tucked=false,variant=1"]["status"], "SAME")
        self.assertEqual(rows["facing=south,tucked=false,variant=1"]["status"], "CHANGED")
        self.assertEqual(rows["facing=east,tucked=false,variant=1"]["status"], "STUDY_ONLY")
        self.assertEqual(rows["facing=west,tucked=false,variant=1"]["status"], "RUNTIME_ONLY")

    def test_inheritance_geometry_and_uv_are_independent_of_texture_slots(self):
        parent = "models/block/template/chair.json"
        child = "models/block/chair/acacia_1.json"
        base = {"elements": [{"from": [1, 0, 1], "to": [5, 4, 5],
                              "faces": {"north": {"uv": [0, 0, 4, 4], "texture": "#seat"}}}],
                "textures": {"seat": "another_furniture:block/chair/oak"}}
        docs = {parent: base, child: {"parent": "another_furniture:block/template/chair",
                                      "textures": {"seat": "another_furniture:block/chair/acacia"}}}
        result = d.effective(child, docs)
        self.assertEqual(result["element_count"], 1)
        self.assertEqual(result["face_count"], 1)
        self.assertEqual(result["geometry"][0]["from"], [1, 0, 1])
        self.assertEqual(result["uv"][0]["north"]["uv"], [0, 0, 4, 4])
        self.assertEqual(result["face_bindings"][0]["north"]["texture"],
                         "another_furniture:block/chair/acacia")
        modified = {**base, "elements": [{**base["elements"][0],
                      "faces": {"north": {"uv": [1, 0, 4, 4], "texture": "#seat"}}}]}
        newer = d.effective(child, {parent: modified, child: docs[child]})
        self.assertEqual(result["geometry"], newer["geometry"])
        self.assertNotEqual(result["uv"], newer["uv"])
        self.assertEqual(result["face_bindings"], newer["face_bindings"])

    def test_reject_model_path_escape_and_missing_parent(self):
        self.assertIsNone(d.model_path("minecraft:block/block"))
        self.assertEqual(d.model_path("another_furniture:block/chair/acacia_1"),
                         "models/block/chair/acacia_1.json")
        with self.assertRaises(ValueError):
            d.model_path("another_furniture:block/../escape")
        with self.assertRaises(ValueError):
            d.effective("models/block/chair/missing.json", {})


if __name__ == "__main__":
    unittest.main()
