"""B31/B32/B33 no-gameplay source evidence invariants and fail-closed mutations."""
import csv
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from mcfr.int5_b31_remaining21_real_archive_audit import original_cases, audit_one
from mcfr.int5_b32_b33_texture_context_source_audit import (
    B23, B24, B28, RECORD_PATH, audit_texture, audit_context,
)

ROOT = Path(__file__).resolve().parents[2] / "project" / "integration"


class OriginalSourceResearchBatch(unittest.TestCase):
    def test_B31_expected_21_unverified_archive_cases_are_exact(self):
        cases = original_cases(ROOT)
        self.assertEqual(len(cases), 21)
        self.assertEqual(sum(int(x["per_case_native_F2_SHA256_verified"]) for x in cases), 176)
        self.assertEqual(sum(int(x["per_case_real_client_logs_SHA256_verified"]) for x in cases), 22)
        self.assertEqual(sorted((x["model"],int(x["source_element_index"])) for x in cases),
                         sorted([("AF121",i) for i in range(10)] +
                                [("AF123",i) for i in range(10)] + [("HC11210",12)]))

    def test_B31_missing_real_ZIP_refuses_approval(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError,"Missing unmodified GitHub ZIP"):
                audit_one(original_cases(ROOT)[0], Path(tmp))

    def test_B32_texture_provenance_8_groups_9_hashes(self):
        out=audit_texture(ROOT)
        self.assertEqual(out["texture_hash_group_count"],8)
        self.assertEqual(out["atomic_sha1_sha256_checksum_count"],8)
        self.assertEqual(len(out["named_or_contrast_texture_evidence_not_semantic_approval"]),10)
        self.assertEqual(out["physical_role_material_style_approved"],0)

    def test_B32_AF_runtime_version_caveat_not_resolved(self):
        out=audit_texture(ROOT)
        self.assertEqual(out["source_runtime_version_caveats"]["AF_SOURCE_4_0_3_RELEASE_4_0_2_NOT_BYTE_IDENTICAL"],20)
        self.assertEqual(out["source_runtime_version_caveats"]["BLOCKSTATE_SHA_EQUAL_PARENT_JSON_RUNTIME_NOT_FULLY_PROVEN"],25)

    def test_B33_all_8_conditional_micro_contexts(self):
        out=audit_context(ROOT)
        self.assertEqual(out["B28_positive_intervention_cases"],7)
        self.assertEqual(out["B28_nonzero_camera_comparisons"],8)
        self.assertEqual(out["B28_total_micro_changed_screen_pixels"],10)
        self.assertEqual(len(out["source5_unchanged_in_B27_full_model"]),2)

    def _mutation(self, file, edit, csv_file=False):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            for path in (B23,B24,B28,RECORD_PATH):
                shutil.copyfile(ROOT/path, root/path)
            p=root/file
            if csv_file:
                with p.open(encoding="utf8",newline="") as stream:
                    reader=csv.DictReader(stream)
                    header=reader.fieldnames
                    rows=list(reader)
                edit(rows)
                with p.open("w",encoding="utf8",newline="") as stream:
                    writer=csv.DictWriter(stream,header)
                    writer.writeheader()
                    writer.writerows(rows)
            else:
                obj=json.loads(p.read_text(encoding="utf8"))
                edit(obj)
                p.write_text(json.dumps(obj),encoding="utf8")
            with self.assertRaisesRegex(ValueError,"INT5_B32_B33_EVIDENCE_REJECT"):
                (audit_texture if file==B24 else audit_context)(root)

    def test_B32_fake_material_approval_is_rejected(self):
        self._mutation(B24,lambda r:r[0].__setitem__("material_or_style_approved","true"),True)

    def test_B32_fake_original_texture_hash_rejected(self):
        self._mutation(B24,lambda r:r[0].__setitem__("original_texture_source_hashes","NOT-SHA"),True)

    def test_B33_false_positive_when_full_original_is_zero_rejected(self):
        self._mutation(B23,lambda j:j["results"][0].__setitem__(
            "original_source_element5_added_vs_absent_pixels_south_north_east_west",[1,0,0,0]))

    def test_B33_micro_coordinates_cannot_exceed_count(self):
        self._mutation(B28,lambda j:j["records"][1].__setitem__("changed_pixel_positions_xy",{}))


if __name__=="__main__":
    unittest.main()
