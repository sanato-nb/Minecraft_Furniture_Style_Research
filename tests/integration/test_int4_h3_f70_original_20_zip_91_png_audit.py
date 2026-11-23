"""H3 F70 archived 20 zip and 91 screenshot exact-source parsing regression."""
import importlib.util,io,json,unittest
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED

ROOT=Path(__file__).resolve().parents[2]
path=ROOT/"scripts/integration/build_int4_h3_f70_original_20_zip_91_png_audit.py"
spec=importlib.util.spec_from_file_location("h3original",path)
h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)

class TestH3OriginalArchives(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        b=(ROOT/h.LEDGER).read_bytes()
        assert h.gitblob(b)==h.LEDGER_BLOB
        cls.records=h.rows(b)
        cls.byid={r["target_id"]:r for r in cls.records}
    def test_original_F70_SHA_and_population(self):
        self.assertEqual(len(self.records),70)
        self.assertEqual(len(self.byid),70)
        self.assertEqual(sum(r["target_kind"]=="HISTORICAL_1_5_CASE" for r in self.records),62)
        self.assertEqual(sum(r["target_kind"]=="RISK_SCENARIO" for r in self.records),8)
    def test_20_actual_archives_and_91_picture_occurrences(self):
        ex=[x for r in self.records for x in h.expand(r)]
        self.assertEqual(len(ex),91)
        self.assertEqual(len({x["artifact_id"] for x in ex}),20)
        self.assertEqual(len({x["run_id"] for x in ex}),19)
        self.assertTrue(all(len(x["expected_zip_sha256"])==64 for x in ex))
    def test_r06_inherited_archive_prefix_for_semicolon_images(self):
        ex=h.expand(self.byid["R06"])
        self.assertEqual(len(ex),3)
        self.assertEqual([x["declared_native_png_member"] for x in ex],
            ["R06_T0.png","R06_T1.png","R06_T2.png"])
        self.assertEqual(len({x["artifact_id"] for x in ex}),1)
    def test_r08_two_nested_game_images_same_SHA(self):
        ex=h.expand(self.byid["R08"])
        self.assertEqual(len(ex),2)
        self.assertEqual(len({x["artifact_id"] for x in ex}),1)
        self.assertEqual(len({x["expected_png_sha256"] for x in ex}),1)
        self.assertTrue(all("native-F2/" in x["declared_native_png_member"] for x in ex))
    def test_r05_two_different_artifacts_for_sleep_and_destroy(self):
        ex=h.expand(self.byid["R05"])
        self.assertEqual(len(ex),5)
        self.assertEqual(len({x["artifact_id"] for x in ex}),2)
        self.assertEqual(len({x["run_id"] for x in ex}),2)
    def test_r02_and_r07_share_original_zip_with_distinct_cases(self):
        a=h.expand(self.byid["R02"]);b=h.expand(self.byid["R07"])
        self.assertEqual((len(a),len(b)),(6,4))
        self.assertEqual({x["artifact_id"] for x in a},{x["artifact_id"] for x in b})
    def test_original_zip_member_lookup_fail_closed(self):
        buf=io.BytesIO()
        with ZipFile(buf,"w",ZIP_DEFLATED) as z:z.writestr("folder/a.png",b"png")
        with ZipFile(io.BytesIO(buf.getvalue())) as z:
            self.assertEqual(h.find_member(z,"a.png"),"folder/a.png")
            with self.assertRaises(AssertionError):
                h.find_member(z,"absent.png")
    def test_modified_ledger_hash_would_fail(self):
        b=(ROOT/h.LEDGER).read_bytes()
        self.assertNotEqual(h.gitblob(b+b"invalid"),h.LEDGER_BLOB)
    def test_original_F70_is_conditional_not_full_approved(self):
        self.assertTrue(all(r["final_disposition"].startswith("CONDITIONAL") for r in self.records))
        self.assertTrue(all(r["runtime_evidence_accepted_as_full_F_PASS"]=="false" for r in self.records))

if __name__=="__main__":unittest.main()
