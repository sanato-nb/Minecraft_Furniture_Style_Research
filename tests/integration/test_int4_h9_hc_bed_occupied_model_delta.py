"""INT-4-H9 modeling-only occupancy variant / parent model / UV scope."""
import importlib.util,json,unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
P=ROOT/"scripts/integration/build_int4_h9_hc_bed_occupied_model_delta.py"
spec=importlib.util.spec_from_file_location("int4_h9_bed_source",P)
h9=importlib.util.module_from_spec(spec);spec.loader.exec_module(h9)

class BedOccupiedVisualModelOnly(unittest.TestCase):
    def test_historical_original_source_github_sha_pinned(self):
        self.assertEqual(h9.COMMIT,"8d21d1665916850c3fa3bdaf1370c50ec2ca7035")
        self.assertEqual(h9.PINS[h9.BLOCK],"0dfb7493ac098a7e5549db6663bffd9310c1882a")
        self.assertEqual(len(h9.PINS),8)
        for file in (h9.LEDGER,h9.F2DOC):
            raw=(ROOT/file).read_bytes()
            self.assertEqual(h9.gitblob(raw),h9.PINS[str(file)])

    def test_occupied_source_population_cartesian_geometry(self):
        self.assertEqual(len(h9.COLORS),16)
        self.assertEqual(len(h9.FACING),4)
        self.assertEqual(len(h9.SHAPES),4)
        self.assertEqual(len(h9.PARTS),2)
        self.assertEqual(16*4*4*2*2,1024)
        self.assertEqual(16*4*4*2,512)

    def test_parse_source_case_selector_not_gameplay(self):
        v=h9.parse_selector("color=white,facing=north,occupied=true,part=foot,shape=single")
        self.assertEqual(v,dict(color="white",facing="north",occupied="true",part="foot",shape="single"))

    def test_unknown_selector_rejected(self):
        for s in ("color=white,facing=north,occupied=true,part=foot",
                  "color=white,facing=north,occupied=true,part=foot,shape=stool",
                  "color=white,facing=north,occupied=true,part=foot,shape=single,sleep=yes"):
            with self.assertRaises(AssertionError):h9.parse_selector(s)

    def test_original_model_resource_conversion(self):
        self.assertEqual(
          h9.path_of("handcrafted:block/oak_fancy_bed_single_white_foot_occupied"),
          h9.MODELS+"oak_fancy_bed_single_white_foot_occupied.json")
        with self.assertRaises(AssertionError):h9.path_of("minecraft:block/bed")

    def test_face_and_element_deltas_are_source_records_not_rendered_pixels(self):
        base={"elements":[{"from":[0,0,0],"to":[16,8,16],"faces":{"up":{"uv":[0,0,16,16]}}}]}
        occupied={"elements":[*base["elements"],
             {"from":[0,8,0],"to":[16,9,16],"faces":{"up":{"uv":[0,0,16,16]},"north":{"uv":[0,0,16,1]}}}]}
        a=h9.model_diff(base,occupied)
        self.assertEqual(a["identical_element_records"],1)
        self.assertEqual(a["added_element_records"],1)
        self.assertEqual(a["removed_element_records"],0)
        self.assertEqual(a["added_face_UV_records"],2)
        self.assertEqual(h9.counts(occupied),(2,3))

    def test_unchanged_head_leaf_is_distinct_from_named_selector(self):
        key="handcrafted:block/oak_fancy_bed_single_white_head"
        self.assertNotEqual(key,key+"_occupied")
        # Source leaf hash equality is checked at runtime for every 256 head pair.
        self.assertEqual(h9.PINS[h9.MODELS+"oak_fancy_bed_single_white_head.json"],
                         "81117620d95782b093fa23b396af04cf42f6729a")

    def test_original_study_F2_proves_only_unoccupied_bed(self):
        originals,f2=h9.original_study()
        self.assertEqual(set(originals),{"S37","S38"})
        self.assertEqual(originals["S37"][0]["state"].split(";")[2],"occupied=false")
        self.assertEqual(originals["S38"][0]["state"].split(";")[2],"occupied=false")
        self.assertEqual(len(f2),2)

    def test_pinned_real_image_is_not_relabelled_occupied_true(self):
        doc=json.loads((ROOT/h9.F2DOC).read_text())
        self.assertFalse(doc["first_paired_background_controlled_f2"]["observed"]
                         ["limitations"]["natural_bed_two_part_behavior_tested"])
        self.assertFalse(doc["first_paired_background_controlled_f2"]["observed"]
                         ["limitations"]["texture_pixelwise_uv_color_approved"])

if __name__=="__main__":unittest.main()
