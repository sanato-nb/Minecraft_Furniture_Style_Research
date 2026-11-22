"""INT-4 real Macaw neighbor state survey: never assume a connection exists."""
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from mcfr import int4_macaw_neighbor_capture as n

class MacawTableNeighborTests(unittest.TestCase):
    def test_pack_stages_are_sequential_and_do_not_force_connection_flags(self):
        lines=n.pack_lines()
        self.assertEqual(set(lines),{
            "reset","join","remove","verify_reset","verify_join","verify_remove"})
        self.assertIn("setblock 0 120 40 mcwfurnitures:oak_table",lines["reset"])
        self.assertIn("setblock 1 120 40 mcwfurnitures:oak_table",lines["join"])
        self.assertIn("setblock 1 120 40 minecraft:air",lines["remove"])
        for part in ("reset","join","remove"):
            script="\n".join(lines[part])
            self.assertNotIn("[east=",script)
            self.assertNotIn("[west=",script)
            self.assertTrue(any("mcfr" not in x for x in lines[part]))
            self.assertEqual(sum("say MCFR_NEIGHBOR_" in x for x in lines[part]),1)
            self.assertGreaterEqual(len(lines["verify_"+part]),18)

    def test_new_world_pack_is_version_pinned_and_never_overwrites(self):
        with TemporaryDirectory() as td:
            dest=Path(td)/"neighbor"
            r=n.make_pack(n.VERSION,dest)
            self.assertEqual(r["stages"],list(n.STAGES))
            self.assertFalse(r["player_item_placement_tested"])
            self.assertTrue((dest/"data/mcfr_neighbor/function/verify_join.mcfunction").exists())
            self.assertEqual(len(r["files_sha256"]),7)
            with self.assertRaises(ValueError):n.make_pack(n.VERSION,dest)
            with self.assertRaises(ValueError):n.make_pack("1.21.1",Path(td)/"bad")

    @staticmethod
    def server_log(stage,centre_east=False,east_present=False,
                   east_west=False,duplicated=False):
        def say(tag):
            return "[12:00:00] [Server thread/INFO]: [RenderAudit] MCFR_NEIGHBOR_"+stage+"_"+tag
        lines=[say("CENTRE_TABLE_PRESENT")]
        for prop in ("EAST","WEST","NORTH","SOUTH"):
            lines.append(say("CENTRE_"+prop+"_"+("TRUE" if prop=="EAST" and centre_east else "FALSE")))
        lines.append(say("EAST_TABLE_PRESENT" if east_present else "EAST_AIR_PRESENT"))
        if east_present:
            for prop in ("EAST","WEST","NORTH","SOUTH"):
                lines.append(say("EAST_"+prop+"_"+("TRUE" if prop=="WEST" and east_west else "FALSE")))
        if duplicated:lines.append(say("CENTRE_EAST_FALSE"))
        lines.append(say("OBSERVED"))
        return "\n".join(lines)

    def test_real_server_state_parser_counts_all_properties_without_guessing(self):
        reset=n.extract(self.server_log("reset"),"reset")
        joined=n.extract(self.server_log("join",True,True,True),"join")
        removed=n.extract(self.server_log("remove"),"remove")
        proof=n.summarize({"reset":reset,"join":joined,"remove":removed})
        self.assertTrue(proof["joined_bidirectionally"])
        self.assertTrue(proof["automatically_disconnected_after_remove"])
        self.assertTrue(proof["state_changed_after_adjacent_setblock"])
        self.assertFalse(proof["player_item_placement_tested"])

    def test_nonconnecting_behavior_is_valid_observation_not_fabricated_pass(self):
        observed={
            "reset":n.extract(self.server_log("reset"),"reset"),
            "join":n.extract(self.server_log("join",False,True,False),"join"),
            "remove":n.extract(self.server_log("remove"),"remove")}
        proof=n.summarize(observed)
        self.assertFalse(proof["joined_bidirectionally"])
        self.assertFalse(proof["state_changed_after_adjacent_setblock"])
        with self.assertRaisesRegex(ValueError,"missing/ambiguous"):
            n.extract(self.server_log("reset",duplicated=True),"reset")
        # We cannot assume initial EAST=false without measuring the game.
        # Even a surprising default state is a legitimate observation.
        strange=n.summarize({**observed,"reset":n.extract(self.server_log("reset",True),"reset")})
        self.assertTrue(strange["centre_east_baseline"])
        self.assertTrue(strange["state_changed_after_adjacent_setblock"])

if __name__=="__main__":
    unittest.main()
