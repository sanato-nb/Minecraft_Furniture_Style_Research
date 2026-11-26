"""Strict B24 all-45 source role hypotheses never become final semantics."""
import csv
import shutil
import tempfile
import unittest
from pathlib import Path

from mcfr import int5_b24_role_evidence_batch as b24

ROOT=Path(__file__).resolve().parents[2]

class Full45RoleSemanticBatchTest(unittest.TestCase):
    def test_original_45_229_source_and_state_cross_audit(self):
        rows,doc=b24.build(ROOT)
        self.assertEqual(len(rows),45)
        self.assertEqual(len({(r["model"],r["provider"],r["source_element_index"])
                             for r in rows}),45)
        self.assertEqual(sum(int(r["face_count"]) for r in rows),229)
        self.assertEqual(doc["original_single_element_bounded_visible_response"],43)
        self.assertEqual(doc["original_single_element_no_visible_response"],2)
        self.assertEqual(doc["source_named_or_distinct_texture_cues_not_role_approvals"],10)
        self.assertEqual(doc["weak_shared_texture_role_cue_count"],35)

    def test_exact_two_B21_B22_target_original_element5_rows_are_preserved(self):
        rows,doc=b24.build(ROOT)
        targets=[r for r in rows if
                 r["B19_original_removal_pixel_response_observed"]=="false"]
        self.assertEqual({(r["model"],r["provider"],r["source_element_index"])
                          for r in targets},
                          {("AF121","AF1393","5"),("AF123","AF1394","5")})
        self.assertTrue(all(
            r["B21_real_isolation_experiment"]==
             "VISIBLE_ORIGINAL_SOURCE5_ONLY_NOT_VISIBLE_IN_FULL_MODEL"
            and r["B22_original_pair_real_experiment"]==
             "PASS_PAIR5_6_HAS_ADDITIONAL_RENDER_PIXELS_OVER_ORIGINAL6_ONLY"
            for r in targets))
        self.assertTrue(doc["B23_real_multi_context_results_not_prejudged"])

    def test_none_of_45_roles_material_rights_or_pixels_are_semantic_approved(self):
        rows,doc=b24.build(ROOT)
        for row in rows:
            for k in ("original_element_to_F2_unique_face_pixel_attributed",
                      "role_function_semantics_approved","material_or_style_approved",
                      "third_party_training_or_redistribution_rights_approved"):
                self.assertEqual(row[k],"false")
        for k in ("individual_original_face_UV_GPU_pixel_ownership_approved",
                  "individual_original_physical_function_role_approved",
                  "individual_original_material_style_approved",
                  "third_party_AI_training_and_redistribution_rights_approved",
                  "F70_unconditional_approved"):
            self.assertEqual(doc[k],0)
        self.assertEqual(doc["H03"],"HOLD")
        self.assertEqual(doc["H05"],"CONDITIONAL")

    def test_original_four_model_source_role_catalog_preserved(self):
        rows,doc=b24.build(ROOT)
        self.assertEqual(doc["source_element_count_by_original_model"],
            {"AF121":10,"AF123":10,"HC11210":13,"MACAW67":12})
        self.assertEqual(set(doc["role_hypotheses_not_final_approvals"]),
                         b24.SUPPORTED_ROLES)
        self.assertEqual(set(doc["texture_source_cues_not_semantic_proof"]),
                         b24.SUPPORTED_CUES)
        self.assertEqual(sum(doc["role_hypotheses_not_final_approvals"].values()),45)

    def test_duplicate_source_element_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            for original in (b24.SOURCE_B3,b24.SOURCE_B22):
                dest=root/original
                dest.parent.mkdir(parents=True,exist_ok=True)
                shutil.copyfile(ROOT/original,dest)
            source=root/b24.SOURCE_B3
            raw=source.read_text()
            lines=raw.splitlines()
            lines[2]=lines[1]
            source.write_text("\n".join(lines)+"\n")
            with self.assertRaisesRegex(ValueError,"duplicated|identities"):
                b24.build(root)

    def test_unauthorized_semantic_approval_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            for original in (b24.SOURCE_B3,b24.SOURCE_B22):
                dest=root/original
                dest.parent.mkdir(parents=True,exist_ok=True)
                shutil.copyfile(ROOT/original,dest)
            p=root/b24.SOURCE_B3
            with p.open(encoding="utf-8",newline="") as f:
                rows=list(csv.DictReader(f))
            rows[0]["part_function_verified"]="true"
            with p.open("w",encoding="utf-8",newline="") as f:
                w=csv.DictWriter(f,fieldnames=rows[0].keys())
                w.writeheader();w.writerows(rows)
            with self.assertRaisesRegex(ValueError,"unsupported semantic"):
                b24.build(root)

if __name__=="__main__":
    unittest.main()
