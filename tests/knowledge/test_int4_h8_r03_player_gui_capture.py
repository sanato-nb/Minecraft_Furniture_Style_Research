"""INT-4-H8 R03 real player GUI input must not call source setblock neighbor join."""
import unittest
from pathlib import Path
from mcfr import int4_h8_r03_player_gui_capture as h8
from mcfr import int4_macaw_neighbor_capture as old
class H8ActualPlayerItem(unittest.TestCase):
    def test_fixed_original_mod_release_and_world_version(self):
        self.assertEqual(h8.VERSION,"1.21.11")
        self.assertEqual(h8.MACAW_SHA256,old.MACAW_SHA256)
        self.assertEqual(h8.TABLE,"mcwfurnitures:oak_table")
    def test_original_data_pack_server_stage_probes_preserved(self):
        self.assertEqual(h8.pack_lines(),old.pack_lines())
        self.assertEqual(h8.STAGES,("reset","join","remove"))
    def test_new_game_client_only_mouse_places_and_breaks_east(self):
        content=Path(h8.__file__).read_text(encoding="utf-8")
        self.assertIn('xdo("click","3")',content)
        self.assertIn('xdo("click","1")',content)
        self.assertNotIn('cmd("/function mcfr_neighbor:"+stage',content)
        self.assertIn('cmd("/function mcfr_neighbor:reset"',content)
        self.assertIn('cmd("/function mcfr_neighbor:verify_"+stage',content)
        self.assertIn('"/item replace entity @s weapon.mainhand with "+TABLE+" 1"',content)
    def test_real_GUI_click_failure_closed_on_wrong_east_server_state(self):
        content=Path(h8.__file__).read_text(encoding="utf-8")
        self.assertIn('GUI right click did not place and connect',content)
        self.assertIn('GUI left click did not break east table',content)
        self.assertIn('SIGNAL+"join_STAGE_DONE" not in logs',content)
    def test_physical_mouse_pose_in_reach_and_target_bounds(self):
        self.assertEqual(h8.EAST,(1,120,40))
        content=Path(h8.__file__).read_text(encoding="utf-8")
        self.assertIn('1.5 120 43.5 180 28',content)
        self.assertIn('1.5 120 43.5 180 16',content)
    def test_no_f_H_final_rights_or_uv_claims(self):
        content=Path(h8.__file__).read_text(encoding="utf-8")
        self.assertIn('"full_F_unconditional_pass":False',content)
        self.assertIn('"UV_pixel_to_face_causal_proof":False',content)
        self.assertIn('"int5_semantic_approvals":0',content)
        self.assertIn('"int6_rights_approvals":0',content)
    def test_original_baseline_reset_does_not_double_place_neighbor(self):
        commands=old.pack_lines()
        self.assertIn("setblock 0 120 40 mcwfurnitures:oak_table",commands["reset"])
        self.assertNotIn("setblock 1 120 40 mcwfurnitures:oak_table",commands["reset"])
        self.assertIn("setblock 1 120 40 mcwfurnitures:oak_table",commands["join"])
        self.assertNotIn("setblock 1 120 40 mcwfurnitures:oak_table",commands["verify_join"])
if __name__=="__main__":unittest.main()
