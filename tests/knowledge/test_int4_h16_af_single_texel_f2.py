"""H16 single source texel intervention tests; no fake-game success statements."""
from __future__ import annotations

import hashlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from zipfile import ZipFile

from PIL import Image,ImageDraw

from mcfr import int4_h16_af_single_texel_f2 as h16
from mcfr import int4_h15_af_opposing_f2_capture as h15
from mcfr import int4_h12_af_chair_samepose_f2_capture as h12


def source_png():
    img=Image.new("RGBA",(16,16),(30,40,50,255))
    img.putpixel(h16.TARGET,h16.SOURCE_RGBA)
    out=io.BytesIO()
    img.save(out,"PNG")
    return out.getvalue()


def stub_game(root,raw):
    game=Path(root)
    jar=game/"mods"/"another_furniture-fabric-4.0.2.jar"
    jar.parent.mkdir(exist_ok=True)
    with ZipFile(jar,"w") as z:
        z.writestr(h16.TEX_REL,raw)
    (game/"options.txt").write_text(
        "renderDistance:4\nsimulationDistance:5\nmaxFps:30\nguiScale:2\n",
        encoding="utf-8")
    return jar


class H16SourceOneTexel(unittest.TestCase):
    def test_pinned_version_and_target_are_opaque(self):
        self.assertEqual(h16.VERSION,"1.21.1")
        self.assertEqual(h16.PACK_FORMAT,34)
        self.assertEqual(h16.TARGET,(3,1))
        self.assertEqual(h16.SOURCE_RGBA,(173,93,50,255))
        self.assertEqual(h16.PROBE_RGBA,(255,0,255,255))
        self.assertEqual(h16.CAMERAS,h15.EXPECTED_CAMERAS)
        self.assertEqual(len(h16.VIEWS)*len(h16.STAGES),6)

    def test_writes_one_temp_pixel_only_original_mod_unchanged(self):
        raw=source_png()
        with tempfile.TemporaryDirectory() as td:
            jar=stub_game(td,raw)
            original_jar_sha=hashlib.sha1(jar.read_bytes()).hexdigest()
            with patch.object(h12,"static_preflight",return_value={"h11_git_blob_sha1":"original-h11"}), \
                 patch.object(h12,"JAR_SHA1",original_jar_sha), \
                 patch.object(h16,"TEX_BLOB_PIN",h16.blob(raw)):
                doc=h16.prepare_one_texel_probe(Path(td))
            self.assertEqual(doc["RGBA_texels_modified"],1)
            self.assertTrue(doc["original_jar_remains_byte_identical"])
            self.assertEqual(doc["original_texel_xy"],[3,1])
            self.assertEqual(doc["new_texel_rgba"],[255,0,255,255])
            self.assertEqual(hashlib.sha1(jar.read_bytes()).hexdigest(),original_jar_sha)
            opt=(Path(td)/"options.txt").read_text()
            self.assertIn("file/"+h16.PACK_NAME,opt)
            pack=Path(td)/"resourcepacks"/h16.PACK_NAME
            self.assertEqual(json.loads((pack/"pack.mcmeta").read_text())["pack"]["pack_format"],34)
            with Image.open(pack/h16.TEX_REL) as new:
                new=new.convert("RGBA")
                with Image.open(io.BytesIO(raw)) as old:
                    old=old.convert("RGBA")
                    diffs=sum(new.getpixel((x,y))!=old.getpixel((x,y))
                              for x in range(16) for y in range(16))
            self.assertEqual(diffs,1)
            self.assertEqual(new.getpixel(h16.TARGET),h16.PROBE_RGBA)

    def test_fails_closed_on_unpinned_original_texture_texel(self):
        raw=source_png()
        with tempfile.TemporaryDirectory() as td:
            stub_game(td,raw)
            with patch.object(h12,"static_preflight",return_value={"h11_git_blob_sha1":"old"}), \
                 patch.object(h12,"JAR_SHA1","bogus"):
                with self.assertRaisesRegex(ValueError,"JAR_SHA_MISMATCH"):
                    h16.prepare_one_texel_probe(Path(td))

    def test_no_faked_pack_activation_from_options_alone(self):
        with self.assertRaisesRegex(ValueError,"NOT_LOADED"):
            h16.assert_resource_pack_loaded(
                "options resourcePacks selected file/"+h16.PACK_NAME)
        valid="[Render thread/INFO]: Reloading ResourceManager: vanilla, fabric, file/"+h16.PACK_NAME
        self.assertEqual(len(h16.assert_resource_pack_loaded(valid)),64)

    def test_original_6_cases_same_facing_and_no_extra_mutation(self):
        self.assertEqual(h16.STAGES,("model1_before","model3","model1_after"))
        self.assertEqual(h16.model_state("model1_before"),h12.state("model1"))
        self.assertEqual(h16.model_state("model3"),h12.state("model3"))
        self.assertEqual(h16.model_state("model1_after"),h12.state("model1"))
        self.assertEqual(h16.BLOCK,(-88,120,40))
        with self.assertRaisesRegex(ValueError,"BAD_MODEL"):
            h16.model_state("air")

    def test_screen_roi_single_changed_texel_geometry_controls(self):
        one=Image.new("RGB",(1024,684),(190,190,190))
        patch_img=one.copy()
        ImageDraw.Draw(patch_img).rectangle((499,419,501,421),fill=(240,0,240))
        changed=h15.pixel_changes(one,patch_img)
        self.assertEqual(len(changed),9)
        self.assertTrue(all(499<=x<=501 and 419<=y<=421 for x,y in changed))
        self.assertFalse(h15.pixel_changes(one,one))

    def test_original_game_audit_missing_manifest_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(FileNotFoundError):
                h16.audit(Path(td),Path(td)/"not-h15.zip")

    def test_negative_control_and_approval_limits_present(self):
        code=Path(h16.__file__).read_text(encoding="utf-8")
        self.assertIn('negative_pixels=h15.pixel_changes(imgs["model3"],base_images["model3"])',code)
        self.assertIn('repeat_pixels=h15.pixel_changes(imgs["model1_before"],imgs["model1_after"])',code)
        self.assertIn('"specific_GPU_face_to_UV_texel_pixel_attribution_approved":False',code)
        self.assertIn('"F70_unconditional_approvals":0',code)
        self.assertIn('"INT6_training_or_redistribution_rights_approved":0',code)
        self.assertNotIn("player_sleep_wake_destroy",code)


if __name__=="__main__":
    unittest.main()
