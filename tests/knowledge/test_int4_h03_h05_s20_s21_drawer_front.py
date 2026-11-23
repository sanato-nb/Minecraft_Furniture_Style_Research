"""P0 drawer original source/camera negative controls; no mock-game F2 approvals."""
import hashlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from zipfile import ZipFile

from PIL import Image

from mcfr import int4_h03_h05_s20_s21_drawer_front as drawer
from mcfr import int4_nonchair_runtime as original


class P0FrontCamera(unittest.TestCase):
    def test_old_and_new_observer_faces_are_opposite(self):
        self.assertEqual(drawer.CAMERA_OLD,"3.4 123.6 45.7 151 28")
        self.assertEqual(drawer.CAMERA_FRONT,"0.5 122.3 35.5 0 20")
        self.assertEqual(drawer.BLOCK,(0,120,40))
        self.assertEqual(drawer.CASES,("S20","S21"))
        self.assertEqual(drawer.VERSION,"1.21.1")

    def test_original_old_camera_images_same_bytes(self):
        self.assertEqual(drawer.OLD_S20_S21_NATIVE_SHA256,
                         "02ee02a4b05d0d9877fc12debd214a96823cea734e56e7f60972bb72ff29f566")

    def test_wrong_mod_jar_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            jar=Path(td)/"mods"/"another_furniture-fabric-4.0.2.jar"
            jar.parent.mkdir()
            jar.write_bytes(b"fake")
            with patch.object(drawer.f3,"original_7_cases",return_value=({
                "S20":{"state":"facing=north;open=false"},
                "S21":{"state":"facing=north;open=true"}},"pin")):
                with self.assertRaisesRegex(ValueError,"OFFICIAL_AF_SHA1_NOT_PINNED"):
                    drawer.source_preflight(td)

    def test_two_states_selected_as_two_distinct_leaves_with_only_front_slot(self):
        with tempfile.TemporaryDirectory() as td:
            jar=Path(td)/"mods"/"another_furniture-fabric-4.0.2.jar"
            jar.parent.mkdir()
            paths={
                "assets/another_furniture/blockstates/oak_drawer.json":{
                    "variants":{
                     "facing=north,open=false":{"model":"another_furniture:block/drawer/oak"},
                     "facing=north,open=true":{"model":"another_furniture:block/drawer/oak_open"}}},
                "assets/another_furniture/models/block/drawer/oak.json":{
                    "parent":"another_furniture:block/template/drawer",
                    "textures":{"front":"another_furniture:block/drawer/oak_front",
                                "side":"another_furniture:block/drawer/oak_side",
                                "top":"another_furniture:block/drawer/oak_top"}},
                "assets/another_furniture/models/block/drawer/oak_open.json":{
                    "parent":"another_furniture:block/drawer/oak",
                    "textures":{"front":"another_furniture:block/drawer/oak_front_open"}}
            }
            with ZipFile(jar,"w") as z:
                for p,v in paths.items():z.writestr(p,json.dumps(v).encode())
                z.writestr("assets/another_furniture/textures/block/drawer/oak_front.png",b"a")
                z.writestr("assets/another_furniture/textures/block/drawer/oak_front_open.png",b"b")
            sha=hashlib.sha1(jar.read_bytes()).hexdigest()
            with patch.object(drawer.f3,"original_7_cases",return_value=({
                "S20":{"state":"facing=north;open=false"},
                "S21":{"state":"facing=north;open=true"}},"pin")), \
                 patch.object(drawer,"OFFICIAL_AF_SHA1",sha):
                d=drawer.source_preflight(td)
                self.assertEqual(d["model_differing_texture_slot"],"front")
                self.assertEqual(d["modeled_front_face_direction_for_north_facing_block"],"north")

    def test_roi_change_detection_is_source_independent_and_repeatable(self):
        a=Image.new("RGB",(1024,684),(100,110,120))
        b=a.copy()
        for x in range(492,507):
            for y in range(423,437):
                b.putpixel((x,y),(255,0,255))
        diffs=drawer.changed_pixels(a,b)
        self.assertEqual(len(diffs),210)
        self.assertEqual(drawer.changed_pixels(a,a),[])
        self.assertEqual(len([p for p in diffs if 450<=p[0]<=570 and 345<=p[1]<=555]),210)

    def test_result_file_not_created_by_fake_game(self):
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(FileNotFoundError):
                drawer.audit(td)

if __name__=="__main__":
    unittest.main()
