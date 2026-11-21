"""PR33 F2 chair screenshots must isolate stage floors from model semantics."""
import unittest
from PIL import Image, ImageDraw
from mcfr import chair_runtime_fixture as f
from mcfr import chair_capture_isolation_audit as isolation

class ChairIsolationTests(unittest.TestCase):
    def test_source_study_all_16_state_ids_and_four_cardinals_unchanged(self):
        self.assertEqual(len(f.cases("1.21.1")),12)
        self.assertEqual(len(f.cases("1.21.11")),4)
        self.assertEqual({i.facing for i in f.cases("1.21.1")},set(f.DIRS))
        self.assertEqual({i.case_id for i in f.cases("1.21.1")}, {
          f"{m}_{direction}" for m in ("AF121","AF123","HC11210") for direction in f.DIRS
        })
        self.assertEqual({i.z for i in f.cases("1.21.1")},{40})
        self.assertEqual({i.z for i in f.cases("1.21.11")},{40})

    def test_foreign_floor_never_intersects_conservative_90_degree_view(self):
        # Fixed F2 camera is 5.5 blocks south of chair, facing north.
        # Every 7x7 stage ends within +/-3 on each axis.
        # Even at the furthest visible stage depth (5.5+3), other floors
        # must be laterally outside a generous 90-degree horizontal cone.
        for version in f.CHAIRS:
            cases=f.cases(version)
            for chair in cases:
                cx=chair.x+0.5
                camera_z=chair.z+5.5
                for other in cases:
                    if other.case_id==chair.case_id:continue
                    dx=max(0,abs(other.x-cx)-3)
                    farthest=max(0,camera_z-(other.z-3))
                    self.assertGreater(dx,farthest,
                        f"{chair.case_id} sees platform under {other.case_id}")
            if version=="1.21.1":
                self.assertEqual(
                    sorted(set(i.x for i in cases)),
                    [-88,-72,-56,-40,-24,-8,8,24,40,56,72,88])

    def test_dynamic_force_load_is_exactly_within_original_study_floor_range(self):
        for version in f.CHAIRS:
            cases=f.cases(version)
            place,check=f.pack_lines(version)
            expect=f"forceload add {min(i.x for i in cases)-4} {min(i.z for i in cases)-4} {max(i.x for i in cases)+4} {max(i.z for i in cases)+4}"
            self.assertIn(expect,place)
            self.assertEqual(sum("minecraft:oak_slab[type=top]" in x for x in place),
                             4 if version=="1.21.1" else 0)
            self.assertEqual(sum(x.startswith("execute if block") for x in check),len(cases))

    def test_stone_proxy_on_synthetic_stone_is_not_model_semantics(self):
        plain=Image.new("RGB",(1024,684),(173,200,247))
        self.assertEqual(isolation.stone_pixels(plain),0)
        draw=ImageDraw.Draw(plain)
        draw.rectangle((210,160,290,210),fill=(140,142,146))
        self.assertGreater(isolation.stone_pixels(plain),3000)

    def test_color_gate_separates_synthetic_seat_from_gray_stone(self):
        scene=Image.new("RGB",(1024,684),(180,180,180))
        self.assertEqual(isolation.specimen_color_pixels(scene),0)
        draw=ImageDraw.Draw(scene)
        draw.rectangle((480,420,514,468),fill=(180,90,40))
        self.assertGreater(isolation.specimen_color_pixels(scene),300)

if __name__=="__main__":
    unittest.main()
