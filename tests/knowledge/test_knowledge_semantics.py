"""Evidence-conservative semantic annotation unit tests."""
from fractions import Fraction
import sqlite3
import unittest

from mcfr import knowledge_db
from mcfr import knowledge_semantics as semantic

class ShapeFactsTests(unittest.TestCase):
    def test_zero_thickness_is_geometry_not_function(self):
        self.assertEqual(semantic.shape_axes(
            (Fraction(0),Fraction(2),Fraction(3)),
            (Fraction(16),Fraction(2),Fraction(12))),
            ("y","","0"))

    def test_reversed_coordinate_retained_without_role_guess(self):
        self.assertEqual(semantic.shape_axes(
            (Fraction(16),Fraction(8),Fraction(3)),
            (Fraction(0),Fraction(3),Fraction(13))),
            ("","xy","800"))

    def test_known_candidate_names_are_only_historical_chair_roles(self):
        self.assertEqual(semantic.ROLE_SET,
          frozenset(["LEG_OR_LOWER_POST","SEAT_LAYER","BACKREST_ASSEMBLY","LOWER_FRAME"]))

class SemanticEvidenceConstraints(unittest.TestCase):
    def setUp(self):
        self.db=sqlite3.connect(":memory:")
        self.db.execute("PRAGMA foreign_keys=ON")
        self.db.executescript(knowledge_db.SCHEMA.read_text(encoding="utf-8"))
        self.db.executescript(semantic.SCHEMA.read_text(encoding="utf-8"))
        self.db.execute("""INSERT INTO source_release(
          source_id,version,minecraft_version,origin,pin_kind,pin_digest,asset_hash_kind)
          VALUES('AF','4.0.3','1.21.1','upstream','GIT_COMMIT_SHA1','pin','GIT_BLOB_SHA1')""")
        self.db.execute("INSERT INTO evidence_manifest VALUES('FACES','audit','sha','PASS','AUDIT','sample')")
        self.db.execute("""INSERT INTO model(
          model_key,source_id,resource_id,source_path,source_sha,model_kind,static_grade,
          provider_key,terminal_status,terminal_resource,effective_elements,effective_faces,audit_evidence_id)
          VALUES('KEY','AF','af:block/chair','models/chair.json','sha','MOD','STATIC',
                 NULL,'ROOT','',1,0,'FACES')""")
        self.db.execute("""INSERT INTO geometry_element VALUES(
          'KEY',0,'0|0|0','1|1|1','0|0|0|1|1|1',0,'','LEG_OR_LOWER_POST','GEOMETRY_AND_FACE_SLOTS')""")
        self.db.execute("""INSERT INTO semantic_geometry(
          provider_key,element_index,source_geometry_type,source_size,source_center,
          source_texture_slots,primitive_zero_axes,primitive_reversed_axes,
          local_volume_model_units3,original_role_candidate,original_role_evidence,evidence_grade)
          VALUES('KEY',0,'BAR','1|1|1','1/2|1/2|1/2','#leg','','','1',
                 'LEG_OR_LOWER_POST','GEOMETRY_AND_FACE_SLOTS','ROLE_CANDIDATE_GEOMETRY_AND_SLOTS')""")
    def tearDown(self):
        self.db.close()

    def test_role_is_not_inferred_by_being_present(self):
        self.db.execute("""INSERT INTO part_role_candidate(
           provider_key,element_index,role_label,role_basis,source_model_key,source_model_sha)
           VALUES('KEY',0,'LEG_OR_LOWER_POST','GEOMETRY_AND_FACE_SLOTS','KEY','sha')""")
        self.assertEqual(self.db.execute("SELECT count(*) FROM ai_approved_semantic_part").fetchone()[0],0)

    def test_review_requires_an_actual_element(self):
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.execute("""INSERT INTO semantic_review_queue(
              queue_id,review_kind,provider_key,element_index,request,evidence_source)
              VALUES('ROLE:MISSING:4','ELEMENT_ROLE_VISUAL','MISSING',4,'check','C')""")

    def test_candidate_requires_matching_model_identity(self):
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.execute("""INSERT INTO part_role_candidate(
              provider_key,element_index,role_label,role_basis,source_model_key,source_model_sha)
              VALUES('KEY',0,'LEG_OR_LOWER_POST','GEOMETRY_AND_FACE_SLOTS','MISSING','sha')""")

    def test_material_style_not_created_automatically(self):
        self.assertEqual(self.db.execute("SELECT count(*) FROM verified_material_style").fetchone()[0],0)
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.execute("""INSERT INTO verified_material_style VALUES(
                '1','TEXTURE','1','MATERIAL','oak','VISUAL_VERIFIED','','','')""")

if __name__=="__main__":
    unittest.main()
