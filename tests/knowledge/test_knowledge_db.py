"""INT-3 provenance/rights, UV default and conservative evidence semantics tests."""
import json
from fractions import Fraction
from pathlib import Path
import sqlite3
import unittest

from mcfr import knowledge_db as k

class KnowledgePureTests(unittest.TestCase):
    def test_uv_default_from_original_source_coordinates(self):
        a=tuple(map(Fraction,[1,2,3]))
        b=tuple(map(Fraction,[7,9,13]))
        want={
            "up":(1,3,7,13),"down":(1,3,7,13),
            "north":(9,7,15,14),"south":(1,7,7,14),
            "west":(3,7,13,14),"east":(3,7,13,14)}
        for name,values in want.items():
            self.assertEqual(k.implicit_uv(a,b,name),tuple(map(Fraction,values)))

    def test_static_animation_and_unbound_status(self):
        uv=tuple(map(Fraction,[0,0,16,16]))
        samples={1:(16,16,1),2:(16,16,4)}
        self.assertEqual(k.status(None,uv,samples),"SLOT_UNBOUND")
        self.assertEqual(k.status(3,uv,samples),"MISSING_PINNED_PNG")
        self.assertEqual(k.status(1,uv,samples),"STATIC_RECT")
        self.assertEqual(k.status(2,uv,samples),"ANIMATED_FRAME_RECTS")
        self.assertEqual(k.status(1,(Fraction(8),Fraction(1),Fraction(8),Fraction(5)),samples),"ZERO_UV_AREA")
        self.assertEqual(k.status(1,(Fraction(-2),Fraction(0),Fraction(4),Fraction(8)),samples),"OUTSIDE_TEXTURE_UV")

    def test_clip_and_no_intersection_are_not_equivalent(self):
        partially=tuple(map(Fraction,[-3,1,4,9]))
        outside=tuple(map(Fraction,[-10,1,-3,9]))
        edge=tuple(map(Fraction,[-5,1,0,9]))
        self.assertEqual(k.pixel_support("OUTSIDE_TEXTURE_UV",partially),"SOURCE_REGION_REMEASURED")
        self.assertEqual(k.pixel_support("OUTSIDE_TEXTURE_UV",edge),"SOURCE_REGION_REMEASURED")
        self.assertEqual(k.pixel_support("OUTSIDE_TEXTURE_UV",outside),"NO_SOURCE_INTERSECTION")

    def test_zero_thickness_density_does_not_divide_by_zero(self):
        uv=tuple(map(Fraction,[0,0,16,16]))
        x,y=k.density(uv,0,"up",(Fraction(0),)*3,(Fraction(16),Fraction(0),Fraction(0)),(16,16,1))
        self.assertEqual((x,y),("1",None))

    def test_fraction_canonical(self):
        self.assertEqual(k.pack(k.coordinates("1.25|2|3/2|4")),"5/4|2|3/2|4")

class SchemaRightsTests(unittest.TestCase):
    def setUp(self):
        self.db=sqlite3.connect(":memory:")
        self.db.execute("PRAGMA foreign_keys=ON")
        self.db.executescript(k.SCHEMA.read_text(encoding="utf-8"))

    def tearDown(self):
        self.db.close()

    def _source(self):
        self.db.execute("""INSERT INTO source_release(
              source_id,version,minecraft_version,origin,pin_kind,pin_digest,asset_hash_kind
            ) VALUES ('AF','4.0.3','1.21.1','upstream','GIT_COMMIT_SHA1','deadbeef','GIT_BLOB_SHA1')""")

    def test_rights_are_not_inferred_from_source_audit(self):
        self._source()
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.execute("UPDATE source_release SET training_approved=1 WHERE source_id='AF'")
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.execute("UPDATE source_release SET redistribution_approved=1 WHERE source_id='AF'")
        self.assertEqual(self.db.execute("SELECT training_approved FROM source_release").fetchone()[0],0)

    def test_counterexample_cannot_be_promoted_to_candidate(self):
        self._source()
        self.db.execute("INSERT INTO evidence_manifest VALUES('COMPARISON','path','sha','PASS','AUDIT','sample')")
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.execute("""INSERT INTO comparison_finding VALUES(
                  'C01','SEATING','UNVERIFIED_OR_COUNTEREXAMPLE','HEIGHT','{}',
                  'obs','limits','CANDIDATE_REQUIRES_REVIEW','review','COMPARISON')""")
        self.db.execute("""INSERT INTO comparison_finding VALUES(
                  'C01','SEATING','UNVERIFIED_OR_COUNTEREXAMPLE','HEIGHT','{}',
                  'obs','limits','SCOPE_LIMIT_ONLY','review','COMPARISON')""")
        self.assertEqual(self.db.execute("SELECT COUNT(*) FROM candidate_finding").fetchone()[0],0)

    def test_application_state_model_provider_source_fk(self):
        self._source()
        self.db.execute("INSERT INTO study_case(case_id,cohort,minecraft_version,block,bbox) VALUES('S01','AF','1.21.1','chair','bbox')")
        self.db.execute("INSERT INTO comparison_asset VALUES(7,'AF','1.21.1','assets/af/models/chair.json','MODEL')")
        self.db.execute("INSERT INTO case_application VALUES('S01',0,0,7,NULL,7,NULL,0,0,0,'UNMATCHED_SCOPE')")
        self.db.execute("INSERT INTO case_application_source VALUES('S01',0,0,'model',7)")
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.execute("INSERT INTO case_application_source VALUES('S01',0,0,'state',999)")
        self.assertEqual(self.db.execute("SELECT COUNT(*) FROM case_application_source").fetchone()[0],1)

    def test_model_not_trainable_by_default(self):
        self._source()
        self.db.execute("INSERT INTO evidence_manifest VALUES('FACES','audit','sha','PASS','AUDIT','sample')")
        self.db.execute("""INSERT INTO model(
              model_key,source_id,resource_id,source_path,source_sha,model_kind,static_grade,
              provider_key,terminal_status,terminal_resource,effective_elements,effective_faces,audit_evidence_id)
              VALUES('M','AF','af:block/chair','assets/af/models/chair.json','sha','MOD','STATIC',
                     NULL,'ROOT','',1,1,'FACES')""")
        self.assertEqual(self.db.execute("SELECT COUNT(*) FROM ai_training_eligible_model").fetchone()[0],0)
        self.db.execute("UPDATE source_release SET license_review='CLEARED',training_approved=1 WHERE source_id='AF'")
        self.assertEqual(self.db.execute("SELECT COUNT(*) FROM ai_training_eligible_model").fetchone()[0],0,
                         "Cannot approve an incomplete model whose source face evidence is missing")

if __name__=="__main__":
    unittest.main()
