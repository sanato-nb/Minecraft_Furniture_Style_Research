"""F9 original Macaw five source cases and runtime pack exact regressions."""
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile
from mcfr import int4_f9_macaw_five_capture as f9
from mcfr.chair_runtime_fixture import make_pack,cases

class FiveOriginalCases(unittest.TestCase):
    def test_pinned_source_rows_and_exact_selector_values(self):
        rows,ledger_sha,checkpoint=f9.source_rows()
        self.assertEqual(tuple(rows),f9.ORDER)
        self.assertEqual(len(ledger_sha),64)
        self.assertEqual(f9.ORDER,("S08","S09","S11","S12","S23"))
        self.assertEqual([x.state() for x in f9.capture_cases()],[
            "mcwfurnitures:oak_chair[facing=north]",
            "mcwfurnitures:oak_stool_chair",
            "mcwfurnitures:oak_end_table[east=false,north=false,south=false,west=false]",
            "mcwfurnitures:oak_coffee_table[connection=with_leg]",
            "mcwfurnitures:oak_drawer[connection=single,facing=north]"])
        self.assertEqual([int(rows[k]["elements"]) for k in f9.ORDER],[12,6,14,2,5])
        self.assertEqual([int(rows[k]["faces"]) for k in f9.ORDER],[59,31,52,11,26])
        self.assertEqual([int(rows[k]["y"]) for k in f9.ORDER],[90,0,0,0,180])
        self.assertEqual(sum(int(rows[k]["faces"]) for k in f9.ORDER),179)
        self.assertEqual(sum(int(rows[k]["elements"]) for k in f9.ORDER),39)

    def test_wrong_version_fails_closed(self):
        with self.assertRaises(ValueError):
            f9.capture_cases("1.21.1")

    def test_real_world_fixture_generates_five_unique_source_positions(self):
        c=f9.capture_cases()
        self.assertEqual(len({x.x for x in c}),5)
        self.assertTrue(all(abs(x.x-y.x)>=16
                            for i,x in enumerate(c) for y in c[i+1:]))
        with TemporaryDirectory() as folder:
            p=Path(folder)/"pack"
            result=make_pack("1.21.11",p,c)
            self.assertEqual(result["test_cases"],5)
            placed=(p/"data/mcfr_chair/function/place.mcfunction").read_text()
            verify=(p/"data/mcfr_chair/function/verify.mcfunction").read_text()
            self.assertEqual(placed.count("setblock "),5)
            self.assertEqual(verify.count("=PASS"),5)
            self.assertEqual(verify.count("=FAIL"),5)
            self.assertIn("setblock -20 120 40 mcwfurnitures:oak_stool_chair",placed)

    def test_pinned_mod_jar_identity_refuses_missing_or_fake_jar(self):
        with TemporaryDirectory() as directory:
            p=Path(directory)
            with self.assertRaises(ValueError):
                f9.verify_running_source(p)
            with ZipFile(p/"fake.jar","w") as archive:
                archive.writestr("assets/mcwfurnitures/blockstates/oak_bookshelf.json","{}")
            with self.assertRaisesRegex(ValueError,"SHA256"):
                f9.verify_running_source(p)

    def test_prior_chair_and_table_regressions_unmodified(self):
        self.assertEqual(len(cases("1.21.1")),12)
        self.assertEqual(len(cases("1.21.11")),4)
        self.assertEqual(f9.MACAW_SHA256,
                         "e55d7a78b878043af82875cb8738941b0bba1a3c77652dea3d75a434dbba1a0e")

    def test_source_metadata_never_claims_natural_neighbor_transition(self):
        self.assertEqual(len(f9.ORDER),5)
        self.assertEqual(f9.MANIFEST,"INT4_F9_MACAW_FIVE_REAL_F2_CAPTURE.json")
        self.assertEqual(sum(row[2] for row in f9.EXPECTED.values()),39)
        self.assertEqual(sum(row[3] for row in f9.EXPECTED.values()),179)

if __name__=="__main__":
    unittest.main()
