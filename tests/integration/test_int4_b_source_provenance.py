"""INT-4-B 행 생성·증거 경계·원본 SHA 변경 주입 회귀검증."""
import csv
import gzip
import importlib.util
import io
from pathlib import Path
import unittest


def loaded():
    script=Path(__file__).resolve().parents[2]/"scripts/integration/build_int4_b_source_provenance.py"
    spec=importlib.util.spec_from_file_location("int4_b_provenance",script)
    mod=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


audit=loaded()


class ProvenanceTests(unittest.TestCase):
    def test_uv_declaration_classification(self):
        for v in ("1","True","true"):
            self.assertTrue(audit.uv_is_explicit(v))
        for v in ("0","False","false"):
            self.assertFalse(audit.uv_is_explicit(v))
        with self.assertRaises(AssertionError):
            audit.uv_is_explicit("UNKNOWN")

    def test_unique_index_detects_duplicate_model(self):
        with self.assertRaises(AssertionError):
            audit.index_unique([{"key":"A"},{"key":"A"}],"key","sample")

    def test_gzip_csv_is_deterministic(self):
        def produce():
            w=audit.GzipCSV(["id","scope"])
            w.write({"id":"A","scope":"UV_DECLARED"})
            w.write({"id":"B","scope":"STATIC_ONLY"})
            return w.close()
        p=produce()
        self.assertEqual(p,produce())
        table=list(csv.DictReader(io.StringIO(gzip.decompress(p).decode("utf-8"))))
        self.assertEqual(len(table),2)
        self.assertEqual(table[0]["scope"],"UV_DECLARED")

    def test_source_blob_pin_fails_when_injected(self):
        key="research/furniture_mods/phase_1-3/C/C_GEOMETRY_REUSE.csv"
        old=audit.SOURCES[key]
        try:
            audit.SOURCES[key]="0"*40
            with self.assertRaises(AssertionError):
                audit.src(key)
        finally:
            audit.SOURCES[key]=old


if __name__=="__main__":
    unittest.main()
