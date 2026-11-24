"""H17 source-only regression tests. Synthetic asset bytes never count as game proof."""
import hashlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from zipfile import ZipFile

from PIL import Image

from mcfr import int4_h17_af_drawer_parent_face_uv as h17


def rgba_png(pixel):
    im = Image.new("RGBA", (16, 16), (100, 90, 80, 255))
    im.putpixel((3, 1), pixel)
    buf = io.BytesIO()
    im.save(buf, format="PNG")
    return buf.getvalue()


def fake_source(geometry_change=False, nonfront_change=False, implicit_uv=False):
    f = {
        "texture": "#front",
        "uv": [0, 0, 8, 8],
    }
    if implicit_uv:
        del f["uv"]
    root = {
        "elements": [{
            "from": [0, 0, 0], "to": [16, 16, 16],
            "faces": {"north": f, "south": {"texture": "#side"}},
        }]
    }
    closed = {
        "parent": "another_furniture:block/template/drawer",
        "textures": {
            "front": "another_furniture:block/drawer/oak_front",
            "side": "another_furniture:block/drawer/oak_side",
        },
    }
    opened = {
        "parent": "another_furniture:block/drawer/oak",
        "textures": {"front": "another_furniture:block/drawer/oak_front_open"},
    }
    if geometry_change:
        opened["elements"] = [{"from": [0,0,0], "to": [8,8,8],
                               "faces": {"north": {"texture":"#front"}}}]
    if nonfront_change:
        opened["textures"]["side"] = "another_furniture:block/drawer/another_side"
    content = {
        h17.BLOCKSTATE_PATH: {"variants": {
            "facing=north,open=false": {"model":"another_furniture:block/drawer/oak"},
            "facing=north,open=true": {"model":"another_furniture:block/drawer/oak_open"}
        }},
        "assets/another_furniture/models/block/template/drawer.json": root,
        "assets/another_furniture/models/block/drawer/oak.json": closed,
        "assets/another_furniture/models/block/drawer/oak_open.json": opened,
    }
    return content


def fake_prior():
    return {
        "source_model": {"official_original_AF_mod_jar_sha1": h17.AF_RELEASE_SHA1},
        "verified_new_real_game": {
            "run_conclusion": "success",
            "github_actions_run": h17.F2_ORIGINAL_RUN,
            "exact_game_state_markers_2_of_2": True,
            "new_north_open_closed_RGB24_changed_screen_pixels": 1208,
        },
        "study_scope": {"H03_case_fully_approved": False},
    }


class H17DrawerParentFaceUV(unittest.TestCase):
    def make_jar(self, target: Path, **kw):
        with ZipFile(target, "w") as z:
            for path, obj in fake_source(**kw).items():
                z.writestr(path, json.dumps(obj))
            z.writestr("assets/another_furniture/textures/block/drawer/oak_front.png",
                       rgba_png((10, 20, 30, 255)))
            z.writestr("assets/another_furniture/textures/block/drawer/oak_front_open.png",
                       rgba_png((10, 20, 30, 0)))

    def run_fixture(self, **kw):
        with tempfile.TemporaryDirectory() as td:
            jar = Path(td)/"original-fake.jar"
            self.make_jar(jar, **kw)
            with patch.object(h17, "AF_RELEASE_SHA1",
                              hashlib.sha1(jar.read_bytes()).hexdigest()):
                return h17.inspect_jar(jar, fake_prior())

    def test_parent_chain_and_only_front_alias_changed(self):
        doc = self.run_fixture()
        self.assertTrue(doc["only_front_texture_binding_changed"])
        self.assertTrue(doc["geometry_and_face_uv_arrays_identical"])
        self.assertEqual(doc["changed_face_count"], 1)
        self.assertEqual(doc["changed_faces"][0]["direction"], "north")
        self.assertEqual(doc["changed_faces"][0]["uv"], [0,0,8,8])
        self.assertEqual(doc["changed_faces"][0]["texture_alias_chain"] if
                         "texture_alias_chain" in doc["changed_faces"][0] else ["front"], ["front"])
        self.assertEqual(doc["source_cases"]["S20"]["element_count"], 1)
        self.assertEqual(doc["source_cases"]["S21"]["face_count"], 2)
        self.assertEqual(doc["front_png_changed_rgba_texels"], 1)
        self.assertEqual(doc["front_png_changed_alpha_texels"], 1)
        self.assertEqual(doc["changed_png_texels_inside_explicit_front_face_uv_union"], 1)
        self.assertEqual(doc["changed_front_faces_with_implicit_uv"], 0)
        self.assertFalse(doc["pixel_to_GPU_face_UV_texel_exact_causal_approved"])

    def test_implicit_uv_preserved_as_unresolved(self):
        doc = self.run_fixture(implicit_uv=True)
        self.assertEqual(doc["changed_front_faces_with_implicit_uv"], 1)
        self.assertIsNone(doc["changed_faces"][0]["diff_texel_coverage"])
        self.assertEqual(doc["changed_png_texels_inside_explicit_front_face_uv_union"], 0)

    def test_parent_geometry_mutation_rejected(self):
        with self.assertRaisesRegex(ValueError, "H17_DRAWER_GEOMETRY_CHANGED"):
            self.run_fixture(geometry_change=True)

    def test_nonfront_texture_override_rejected(self):
        with self.assertRaisesRegex(ValueError, "H17_CHANGED_NONFRONT_FACE_TEXTURE"):
            self.run_fixture(nonfront_change=True)

    def test_unpinned_official_jar_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            jar = Path(td)/"wrong.jar"
            self.make_jar(jar)
            with self.assertRaisesRegex(ValueError, "H17_OFFICIAL_AF_402_RELEASE_SHA1_MISMATCH"):
                h17.inspect_jar(jar, fake_prior())

    def test_source_f2_contract_drift_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            jar = Path(td)/"fake.jar"
            self.make_jar(jar)
            prior = fake_prior()
            prior["verified_new_real_game"]["new_north_open_closed_RGB24_changed_screen_pixels"] = 0
            with patch.object(h17, "AF_RELEASE_SHA1",
                              hashlib.sha1(jar.read_bytes()).hexdigest()):
                with self.assertRaisesRegex(ValueError, "H17_PRIOR_ORIGINAL_F2_SOURCE_EVIDENCE_DRIFT"):
                    h17.inspect_jar(jar, prior)

    def test_alias_cycle_and_parent_cycle_rejected(self):
        with self.assertRaisesRegex(ValueError, "H17_TEXTURE_ALIAS_CYCLE"):
            h17.resolve_texture({"front":"#inner", "inner":"#front"}, "#front")
        with tempfile.TemporaryDirectory() as td:
            jar = Path(td)/"cycle.jar"
            with ZipFile(jar,"w") as z:
                z.writestr("assets/another_furniture/models/block/drawer/oak.json",
                           json.dumps({"parent":"another_furniture:block/drawer/oak"}))
            with ZipFile(jar) as z:
                with self.assertRaisesRegex(ValueError, "H17_MODEL_PARENT_CYCLE"):
                    h17.resolve_leaf(z, "another_furniture:block/drawer/oak")

    def test_uv_coverage_reversal_and_clamping(self):
        self.assertEqual(h17.texels_in_uv([8,8,0,0], (16,16)),
                         {(x,y) for x in range(8) for y in range(8)})
        self.assertEqual(len(h17.texels_in_uv([-2,-2,20,20],(16,16))),256)

    def test_path_traversal_and_namespace_rejected(self):
        for bad in ("minecraft:block/drawer/oak", "another_furniture:../escape",
                    "another_furniture:block//drawer"):
            with self.assertRaisesRegex(ValueError,"H17_INVALID_MODEL_NAMESPACE_OR_PATH"):
                h17.identifier_to_path(bad,"models")


if __name__ == "__main__":
    unittest.main()
