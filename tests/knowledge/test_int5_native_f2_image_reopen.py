"""INT-5-B2 actual GitHub PNG byte reopening: fail-closed research checks."""
from collections import Counter
import io
import json
import os
from pathlib import Path
import unittest
import zipfile

from mcfr import int5_native_f2_image_reopen as a


class INT5OriginalImageReview(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        d=os.environ.get("INT5_B2_ARTIFACT_DIR")
        if not d:
            raise unittest.SkipTest("Real original F2 archive test requires INT5_B2_ARTIFACT_DIR; dedicated INT5-B2 workflow provides it")
        cls.raw=a.read_pinned()
        cls.archives=a.download_archives(Path(d))
        cls.parts,cls.images,cls.summary=a.calculate(cls.raw,cls.archives)

    def test_all_native_images_and_client_logs_actually_reopened(self):
        self.assertEqual(self.summary["counts"]["native_screenshot_PNG_opened_SHA_decoded"],16)
        self.assertEqual(self.summary["counts"]["original_client_logs_SHA_verified"],2)
        self.assertEqual(self.summary["counts"]["original_archives_downloaded"],3)
        self.assertEqual(len(self.images),16)
        self.assertTrue(all(r["actual_original_F2_bytes_reopened"]=="true" for r in self.images))

    def test_original_source_face_229_across_each_of_45_roles(self):
        self.assertEqual(len(self.parts),45)
        self.assertEqual(sum(int(r["source_element_face_count"]) for r in self.parts),229)
        self.assertEqual(set(r["child_model_key"] for r in self.parts),
                         {"AF121","AF123","HC11210","MACAW67"})
        self.assertTrue(all(r["source_element_png_paths"] and
                            r["exact_source_uv_face_keys"] for r in self.parts))

    def test_twelve_visible_and_four_occluded_group_scope(self):
        self.assertEqual(Counter(r["whole_object_appearance_grade"] for r in self.images),
                         {"WHOLE_CHAIR_SEAT_BACK_SUPPORT_SHAPES_VISIBLE":12,
                          "CHAIR_PARTLY_OCCLUDED_BY_ADJACENT_LIGHT_TABLE":4})
        self.assertTrue(all(r["human_reviewed_original_scene_in_this_turn"]=="true"
                            for r in self.images))
        self.assertEqual(self.summary["counts"]["source_part_individual_F2_pixel_mapping_approved"],0)

    def test_no_automatic_semantic_training_or_material_permission(self):
        self.assertEqual(self.summary["counts"]["part_function_approved"],0)
        self.assertEqual(self.summary["counts"]["style_or_material_approved"],0)
        self.assertEqual(self.summary["counts"]["INT6_training_redistribution_rights_approved"],0)
        self.assertTrue(all(r["function_role_approved"]=="false" for r in self.parts))
        self.assertTrue(all(r["semantic_part_function_approved"]=="false" for r in self.images))

    @staticmethod
    def replace_member(archive,filename,update):
        original=io.BytesIO(archive)
        new=io.BytesIO()
        with zipfile.ZipFile(original) as src,zipfile.ZipFile(new,"w",
                compression=zipfile.ZIP_DEFLATED) as dst:
            for item in src.namelist():
                data=src.read(item)
                if item==filename: data=update(data)
                dst.writestr(item,data)
        return new.getvalue()

    def test_one_corrupted_screenshot_png_causes_source_rejection(self):
        mutated=dict(self.archives)
        mutated["native_1_21_1"]=self.replace_member(
            self.archives["native_1_21_1"],"AF121_north.png",
            lambda x:x[:-12]+b"bad from fake capture")
        with self.assertRaises(Exception):
            a.calculate(self.raw,mutated)

    def test_corrupted_source_face_csv_fails_closed(self):
        changed=dict(self.archives)
        changed["textured_face_uv"]=self.replace_member(
            self.archives["textured_face_uv"],
            "INT3_229_ORIGINAL_FACE_UV_TEXTURE_EVIDENCE.csv",
            lambda data:data.replace(b"AF121,",b"FAKE1,",1))
        with self.assertRaisesRegex(ValueError,"original face CSV SHA mismatch"):
            a.calculate(self.raw,changed)

    def test_false_png_sha_metadata_cannot_be_accepted(self):
        changed=dict(self.raw)
        k="INT3_CLIENT_RUNTIME_16_F2_EVIDENCE.json"
        j=json.loads(changed[k])
        j["collected"]["per_image"][0]["sha256"]="a"*64
        changed[k]=json.dumps(j).encode("utf-8")
        with self.assertRaisesRegex(ValueError,"PNG/model/blockstate mismatch"):
            a.calculate(changed,self.archives)

    def test_pinned_git_blobs_all_match(self):
        for filename,data in self.raw.items():
            self.assertEqual(a.gitblob(data),a.PINS[filename])

    def test_committed_output_matches_actual_three_archive_replay(self):
        files=a.output_files(self.raw,self.archives)
        existing=[p for p in files if (a.ROOT/p).exists()]
        if existing:
            self.assertEqual(len(existing),3,"partially committed INT5-B2 results")
        for p in existing:
            self.assertEqual((a.ROOT/p).read_text(encoding="utf-8"),files[p])

    def test_original_image_sources_are_only_temporary_evidence(self):
        self.assertEqual(self.summary["counts"]["new_Minecraft_game_runs"],0)
        self.assertEqual(self.summary["counts"]["new_game_F2_captures"],0)
        self.assertEqual(self.summary["counts"]["original_source_texture_uv_contact_sheet_opened"],1)
        self.assertTrue(all("source" not in x["decision"].lower() or
                            x["decision"].endswith("_PENDING") for x in self.parts))


if __name__=="__main__":
    unittest.main()
