"""F11A five fixed vanilla original source cases and official client SHA gates."""
import unittest
from pathlib import Path
from mcfr import int4_f11_vanilla_five_capture as f11
from mcfr import int4_f10_macaw_connected_five_capture as f10
from mcfr import chair_runtime_fixture as fixture

class F11VanillaOriginalSourceAudit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows,cls.ledger=f11.source_rows()

    def test_fixed_five_and_1_5_ledger(self):
        self.assertEqual(f11.ORDER,("V01","V02","V05","V07","V10"))
        self.assertEqual(self.ledger,f11.PIN_LEDGER_SHA256)
        self.assertEqual(len(self.rows),5)

    def test_source_genuine_github_git_blob_sha1(self):
        self.assertEqual({r["model_hash_kind"] for r in self.rows.values()},{"GIT_BLOB_SHA1"})
        self.assertTrue(all(len(r["model_sha"])==40 and len(r["provider_sha"])==40
                            and len(r["state_sha"])==40 for r in self.rows.values()))

    def test_exact_original_case_model_denominators(self):
        self.assertEqual({k:(int(v["elements"]),int(v["faces"])) for k,v in self.rows.items()},
                         {"V01":(2,11),"V02":(1,6),"V05":(1,6),
                          "V07":(1,6),"V10":(1,6)})
        self.assertEqual(sum(int(r["faces"]) for r in self.rows.values()),35)

    def test_real_game_state_strings_are_exact_1_5(self):
        cases=f11.capture_cases()
        wanted={"V01":"minecraft:oak_stairs[facing=north,half=bottom,shape=straight]",
                "V02":"minecraft:oak_slab[type=bottom]",
                "V05":"minecraft:barrel[facing=north,open=false]",
                "V07":"minecraft:bookshelf",
                "V10":"minecraft:oak_planks"}
        self.assertEqual({c.case_id:c.state() for c in cases},wanted)

    def test_staged_world_datapack_is_original_source_exact(self):
        cases=f11.capture_cases()
        place,checks=fixture.pack_lines(f11.VERSION,cases)
        self.assertEqual(len([x for x in place if x.startswith("setblock ")]),5)
        for c in cases:
            self.assertIn("setblock "+str(c.x)+" "+str(c.y)+" "+str(c.z)+" "+c.state(),place)
            self.assertTrue(any("MCFR_CHAIR_STATE_"+c.case_id+"=PASS" in x for x in checks))

    def test_separate_coordinates_avoid_contact_artifacts(self):
        cases=f11.capture_cases()
        self.assertEqual({x.x for x in cases},{-40,-20,0,20,40})
        self.assertEqual({x.z for x in cases},{40})

    def test_official_mojang_client_12111_is_pinned(self):
        self.assertEqual(f11.MOJANG_CLIENT_SHA1,"ba2df812c2d12e0219c489c4cd9a5e1f0760f5bd")
        self.assertEqual(f11.MOJANG_CLIENT_SHA256,
                         "1473c9489ac50fda3c435049a76a70d61a10b8610db27f5ba9d8756b686cd3bd")
        self.assertEqual(len(f11.MOJANG_CLIENT_SHA256),64)

    def test_parent_and_option_sha_from_vanilla_source(self):
        self.assertEqual(self.rows["V01"]["provider_path"],
                         "assets/minecraft/models/block/stairs.json")
        self.assertEqual(self.rows["V02"]["provider_path"],
                         "assets/minecraft/models/block/slab.json")
        for case in ("V05","V07","V10"):
            self.assertEqual(self.rows[case]["provider_path"],
                             "assets/minecraft/models/block/cube.json")

    def test_earlier_f10_macaw_scope_unchanged(self):
        self.assertEqual(f10.ORDER,("S13","S24","S25","S35","S36"))

    def test_bad_version_fails_closed(self):
        with self.assertRaises(ValueError):
            f11.capture_cases("1.21.1")

    def test_not_claiming_full_F_or_special_states(self):
        self.assertTrue(set(f11.ORDER).isdisjoint({"V03","V04","V06","V08","V11","R06","R08"}))
        self.assertEqual((sum(x[2] for x in f11.EXPECTED.values()),
                          sum(x[3] for x in f11.EXPECTED.values())),(6,35))

if __name__=="__main__":
    unittest.main()
