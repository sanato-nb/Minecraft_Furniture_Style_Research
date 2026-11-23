"""F11C original Minecraft vanilla V12-V15 static-source and distinct renderer safeguards."""
import unittest
from mcfr import int4_f11c_vanilla_kitchen_decor_four_capture as f11c
from mcfr import int4_f11b_vanilla_multipart_five_capture as f11b
from mcfr.chair_runtime_fixture import pack_lines

class F11COriginalFour(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source,cls.digest=f11c.source_rows()

    def test_original_locked_study_bytes(self):
        self.assertEqual(self.digest,f11c.PIN_LEDGER_SHA256)
        self.assertEqual(set(self.source),{"V12","V13","V14","V15"})

    def test_exact_historical_original_models_geometry(self):
        self.assertEqual({key:(int(v["elements"]),int(v["faces"]))
                          for key,v in self.source.items()},
                          {"V12":(13,58),"V13":(14,59),"V14":(4,15),"V15":(5,22)})
        self.assertEqual(sum(int(r["elements"]) for r in self.source.values()),36)
        self.assertEqual(sum(int(r["faces"]) for r in self.source.values()),154)

    def test_no_v11_bed_ordinary_model_approvals(self):
        self.assertNotIn("V11",f11c.ORDER)
        self.assertTrue(set(f11c.ORDER).isdisjoint(set(f11b.ORDER)))
        self.assertEqual(len(f11c.ORDER),4)

    def test_exact_original_server_states(self):
        self.assertEqual({case.case_id:case.state() for case in f11c.capture_cases()},
                         {"V12":"minecraft:cauldron",
                          "V13":"minecraft:water_cauldron[level=3]",
                          "V14":"minecraft:lantern[hanging=false]",
                          "V15":"minecraft:flower_pot"})

    def test_four_source_models_with_hash_kind(self):
        for row in self.source.values():
            self.assertEqual(row["cohort"],"VANILLA")
            self.assertEqual(row["minecraft"],"1.21.11")
            self.assertEqual(row["model_hash_kind"],"GIT_BLOB_SHA1")
            self.assertEqual(row["geometry_status"],"STATIC_SOURCE")
            for field in ("state_sha","model_sha","provider_sha"):
                self.assertEqual(len(row[field]),40)

    def test_model_provider_source_hierarchy_not_guessed(self):
        self.assertEqual(self.source["V12"]["model_path"],self.source["V12"]["provider_path"])
        self.assertEqual(self.source["V15"]["model_path"],self.source["V15"]["provider_path"])
        self.assertEqual(self.source["V13"]["provider_path"],
                         "assets/minecraft/models/block/template_cauldron_full.json")
        self.assertEqual(self.source["V14"]["provider_path"],
                         "assets/minecraft/models/block/template_lantern.json")

    def test_world_datapack_states_and_locations(self):
        cases=f11c.capture_cases()
        place,verify=pack_lines(f11c.VERSION,cases)
        for case in cases:
            self.assertIn("setblock "+str(case.x)+" "+str(case.y)+" "+str(case.z)+" "+case.state(),place)
            self.assertTrue(any("MCFR_CHAIR_STATE_"+case.case_id+"=PASS" in line for line in verify))
        self.assertEqual(len([line for line in place if line.startswith("setblock ")]),4)
        self.assertEqual({c.x for c in cases},{-30,-10,10,30})

    def test_official_mojang_runtime_sha_pinned(self):
        self.assertEqual(f11c.MOJANG_CLIENT_SHA1,"ba2df812c2d12e0219c489c4cd9a5e1f0760f5bd")
        self.assertEqual(f11c.MOJANG_CLIENT_SHA256,
                         "1473c9489ac50fda3c435049a76a70d61a10b8610db27f5ba9d8756b686cd3bd")

    def test_fail_closed_on_wrong_game_version(self):
        with self.assertRaises(ValueError):
            f11c.capture_cases("1.21.1")

    def test_distinguish_static_original_F2_from_animation_and_rights(self):
        self.assertEqual(f11c.EXPECTED["V13"][0],"water_cauldron")
        self.assertEqual(f11c.EXPECTED["V14"][0],"lantern")
        self.assertNotIn("R06",f11c.ORDER)
        self.assertNotIn("R08",f11c.ORDER)

if __name__=="__main__":
    unittest.main()
