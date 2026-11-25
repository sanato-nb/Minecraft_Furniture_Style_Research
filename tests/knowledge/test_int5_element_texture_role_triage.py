"""INT-5 B3: original textured-chair role-cue scope with fail-closed tests."""
from collections import Counter
import csv
import io
import json
import os
from pathlib import Path
import unittest

from mcfr import int5_element_texture_role_triage as stage
from mcfr import int5_native_f2_image_reopen as original


class INT5B3SourceRoleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        folder=os.environ.get("INT5_B3_ARTIFACT_DIR")
        if not folder:
            raise unittest.SkipTest(
                "Actual original three image archives required; dedicated INT5-B3 Actions provides INT5_B3_ARTIFACT_DIR")
        cls.raw=stage.read_pinned()
        cls.b2=original.read_pinned()
        cls.archives=original.download_archives(Path(folder))
        cls.parts,cls.groups,cls.report=stage.adjudicate(
            cls.raw,cls.archives,cls.b2)

    def test_exact_45_element_229_face_16_scene_reinspection(self):
        self.assertEqual(len(self.parts),45)
        self.assertEqual(sum(int(r["source_element_original_face_count"]) for r in self.parts),229)
        self.assertEqual(self.report["counts"]["native_F2_screenshots_reopened"],16)
        self.assertEqual(self.report["counts"]["role_groups_context_checked"],15)

    def test_only_9_original_role_named_source_texture_elements(self):
        self.assertEqual(Counter(r["role_discriminating_texture_cue"]
                                 for r in self.parts),{
            "ROLE_NAMED_ORIGINAL_SEAT_PNG":2,
            "ROLE_NAMED_ORIGINAL_BACK_PNG":6,
            "ROLE_NAMED_ORIGINAL_CUSHION_PNG":1,
            "UNIQUE_SOURCE_TEXTURE_CONTRAST_NO_ROLE_NAME":1,
            "GENERIC_OR_SHARED_TEXTURE_NOT_ROLE_PROOF":35,
        })
        self.assertEqual(self.report["counts"]["named_source_texture_role_cue_elements"],9)

    def test_screen_context_supports_only_8_cues_and_1_occluded(self):
        self.assertEqual(Counter(r["decision"] for r in self.parts),{
            "SOURCE_TEXTURE_ROLE_CUE_AND_WHOLE_GROUP_APPEARANCE_CORROBORATED":8,
            "ORIGINAL_TEXTURE_ROLE_CUE_SEAT_OCCLUDED":1,
            "UNIQUE_SOURCE_TEXTURE_CONTRAST_ONLY_NO_FUNCTION":1,
            "GEOMETRY_AND_SOURCE_UV_ONLY_ROLE_HYPOTHESIS":35,
        })
        obscured=[x for x in self.parts if
                   x["decision"]=="ORIGINAL_TEXTURE_ROLE_CUE_SEAT_OCCLUDED"]
        self.assertEqual([(x["child_model_key"],x["original_source_element_index"])
                          for x in obscured],[("AF123","4")])

    def test_15_original_role_group_boundaries_preserved(self):
        self.assertEqual(len(self.groups),15)
        self.assertEqual(sum(int(x["source_element_count"]) for x in self.groups),45)
        self.assertEqual(sum(int(x["total_source_faces_in_group"]) for x in self.groups),229)
        self.assertEqual(sum(x["child_model_key"]=="AF123" for x in self.groups),4)

    def test_no_unproven_element_pixel_function_or_rights(self):
        self.assertTrue(all(x["individual_element_to_original_F2_pixels_approved"]=="false"
                            and x["part_function_verified"]=="false"
                            and x["training_or_redistribution_rights_approved"]=="false"
                            for x in self.parts))
        self.assertEqual(self.report["counts"]["new_exact_element_to_screen_pixel_identifications"],0)
        self.assertEqual(self.report["counts"]["element_function_semantics_final_approvals"],0)
        self.assertEqual(self.report["counts"]["INT6_training_or_redistribution_approvals"],0)

    def test_git_source_byte_pins_are_exact(self):
        for name,data in self.raw.items():
            self.assertEqual(original.gitblob(data),stage.PINNED[name])
        for name,data in self.b2.items():
            self.assertEqual(original.gitblob(data),original.PINS[name])

    def test_fabric_research_release_difference_unaltered(self):
        self.assertTrue(self.report["source_versus_runtime_AF_drift_preserved"])
        self.assertEqual(sum("AF_SOURCE_4_0_3_RELEASE_4_0_2" in x["research_and_runtime_source_caveat"]
                             for x in self.parts),20)

    def test_one_fabricated_role_in_original_b2_source_is_rejected(self):
        tampered=dict(self.raw)
        key="INT5_B2_45_ELEMENT_SOURCE_TEXTURE_FACE_REVIEW_V1.csv"
        records=list(csv.DictReader(io.StringIO(tampered[key].decode("utf-8"))))
        records[0]["original_role_hypothesis"]="BOGUS"
        buf=io.StringIO()
        w=csv.DictWriter(buf,fieldnames=list(records[0]))
        w.writeheader();w.writerows(records)
        tampered[key]=buf.getvalue().encode("utf-8")
        with self.assertRaisesRegex(ValueError,"B2 pinned part row"):
            stage.adjudicate(tampered,self.archives,self.b2)

    def test_wrong_assumed_af_seat_from_generic_leg_texture_is_not_named(self):
        source,_,_,_=original.source_data(self.b2)
        f,by,_,_=original.read_artifacts(self.archives,source,
            json.loads(self.b2["INT3_CLIENT_RUNTIME_16_F2_EVIDENCE.json"]),
            json.loads(self.b2["INT3_TEXTURED_CHAIRS_SOURCE_SUMMARY.json"]))
        leg_faces=by[("AF1393","0")]
        self.assertEqual(stage.cue_for("AF121","SEAT_LAYER",leg_faces),
                         "GENERIC_OR_SHARED_TEXTURE_NOT_ROLE_PROOF")
        seat_faces=by[("AF1393","4")]
        self.assertEqual(stage.cue_for("AF121","SEAT_LAYER",seat_faces),
                         "ROLE_NAMED_ORIGINAL_SEAT_PNG")

    def test_exact_derived_files_stay_replayable(self):
        outputs=stage.output_files(self.raw,self.archives,self.b2)
        existing=[p for p in outputs if (stage.ROOT/p).exists()]
        if existing:
            self.assertEqual(len(existing),len(outputs),"partial INT5-B3 research files")
        for path in existing:
            self.assertEqual((stage.ROOT/path).read_text(encoding="utf-8"),outputs[path])


if __name__=="__main__":
    unittest.main()
