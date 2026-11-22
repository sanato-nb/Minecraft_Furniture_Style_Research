"""INT-4-F10 Macaw historical source state and real-capture fail-closed tests."""
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile
from mcfr import int4_f10_macaw_connected_five_capture as f10
from mcfr.chair_runtime_fixture import make_pack, cases

class FiveConnectedMacawOriginal(unittest.TestCase):
    def test_five_historical_exact_source_and_SHA(self):
        rows,sha,prior=f10.source_rows()
        self.assertEqual(tuple(rows),f10.ORDER)
        self.assertEqual(len(sha),64)
        self.assertEqual(f10.ORDER,("S13","S24","S25","S35","S36"))
        self.assertEqual([x.state() for x in f10.capture_cases()],[
            "mcwfurnitures:oak_coffee_table[connection=center]",
            "mcwfurnitures:oak_drawer[connection=middle,facing=north]",
            "mcwfurnitures:oak_wardrobe[connection=base,facing=north,hinge=left]",
            "mcwfurnitures:white_couch[facing=north,shape=single]",
            "mcwfurnitures:white_couch[facing=north,shape=left_corner]",
        ])
        self.assertEqual([int(rows[k]["elements"]) for k in f10.ORDER],[1,6,5,11,7])
        self.assertEqual([int(rows[k]["faces"]) for k in f10.ORDER],[6,31,26,66,42])
        self.assertEqual([int(rows[k]["y"]) for k in f10.ORDER],[0,180,180,90,90])
        self.assertEqual(sum(int(rows[k]["faces"]) for k in f10.ORDER),171)
        self.assertEqual(sum(int(rows[k]["elements"]) for k in f10.ORDER),30)

    def test_wrong_mc_version_refused(self):
        with self.assertRaises(ValueError):
            f10.capture_cases("1.21.1")

    def test_five_states_real_datapack_placed_and_checked(self):
        c=f10.capture_cases()
        self.assertEqual(len({x.x for x in c}),5)
        self.assertTrue(all(abs(x.x-y.x)>=16 for i,x in enumerate(c) for y in c[i+1:]))
        with TemporaryDirectory() as tmp:
            path=Path(tmp)/"pack"
            result=make_pack("1.21.11",path,c)
            self.assertEqual(result["test_cases"],5)
            place=(path/"data/mcfr_chair/function/place.mcfunction").read_text()
            verify=(path/"data/mcfr_chair/function/verify.mcfunction").read_text()
            self.assertEqual(place.count("setblock "),5)
            self.assertEqual(verify.count("=PASS"),5)
            self.assertEqual(verify.count("=FAIL"),5)
            self.assertIn("oak_coffee_table[connection=center]",place)
            self.assertIn("white_couch[facing=north,shape=left_corner]",place)

    def test_missing_or_fake_pinned_macaw_mod_rejected(self):
        with TemporaryDirectory() as d:
            path=Path(d)
            with self.assertRaisesRegex(ValueError,"Exactly one pinned Macaw"):
                f10.verify_running_source(path)
            with ZipFile(path/"fake.jar","w") as z:
                z.writestr("assets/mcwfurnitures/blockstates/oak_bookshelf.json","{}")
            with self.assertRaisesRegex(ValueError,"SHA256"):
                f10.verify_running_source(path)

    def test_original_16_chair_cases_and_release_pinned(self):
        self.assertEqual(len(cases("1.21.1")),12)
        self.assertEqual(len(cases("1.21.11")),4)
        self.assertEqual(f10.MACAW_SHA256,
                         "e55d7a78b878043af82875cb8738941b0bba1a3c77652dea3d75a434dbba1a0e")

    def test_study_geometry_limits_do_not_claim_automatic_connections(self):
        self.assertEqual(sum(row[2] for row in f10.EXPECTED.values()),30)
        self.assertEqual(sum(row[3] for row in f10.EXPECTED.values()),171)
        self.assertEqual(f10.MANIFEST,"INT4_F10_MACAW_FIVE_REAL_F2_CAPTURE.json")

if __name__=="__main__":
    unittest.main()
