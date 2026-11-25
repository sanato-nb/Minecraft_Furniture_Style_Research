"""INT-5-B6: independent source/causality agreement and fail-closed tests."""
from __future__ import annotations
from copy import deepcopy
import csv
import io
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from mcfr import int5_b6_element_causal_evidence_ledger as b6


def loaded():
    raw=b6.original_sources()
    return (b6.rows(raw[b6.SOURCES_NAMES[0]]),
            b6.rows(raw[b6.SOURCES_NAMES[1]]),
            *[json.loads(raw[n]) for n in b6.SOURCES_NAMES[2:]])


class ElementCausalLedgerTests(unittest.TestCase):

    def test_exact_five_original_git_blobs_and_source_sha256(self):
        blobs=b6.original_sources()
        self.assertEqual(len(blobs),5)
        for name, pinned in b6.SOURCES.items():
            self.assertEqual(b6.git_blob(blobs[name]),pinned)
        p,g,b3,b4,b5=loaded()
        self.assertEqual(b6.sha(blobs[b6.SOURCES_NAMES[0]]),
                         b3["output_sha256"][str(b6.D/b6.SOURCES_NAMES[0])])
        self.assertEqual(b6.sha(blobs[b6.SOURCES_NAMES[1]]),
                         b3["output_sha256"][str(b6.D/b6.SOURCES_NAMES[1])])

    def test_exact_45_parts_229_faces_15_groups_source_partition(self):
        p,g,b3,b4,b5=loaded()
        idx,m,f,cues=b6.index_source(p)
        self.assertEqual(len(idx),45)
        self.assertEqual(sum(f.values()),229)
        self.assertEqual(len(b6.validate_groups(g,idx)),15)
        self.assertEqual(sum(cues[x] for x in b6.CUE_NAMED),9)
        self.assertEqual(cues[b6.CONTRAST],1)
        self.assertEqual(cues[b6.GENERIC],35)

    def test_b5_exact_source_and_real_f2_751_south_zero_north(self):
        p,g,b3,b4,b5=loaded()
        idx,*_=b6.index_source(p)
        views=b6.validate_audit(b3,b4,b5,idx)
        self.assertEqual(views["south"]["element4_removal_source_intervention_delta_pixels"],751)
        self.assertEqual(views["north"]["element4_removal_source_intervention_delta_pixels"],0)
        self.assertEqual(b5["original_baseline_F2_sha256"],b4["native_F2_sha256"])
        self.assertEqual(b5["original_client_log_sha256"],b4["original_client_log_sha256"])

    def test_single_tested_causal_response_all_others_unexamined(self):
        parts,groups,queue,summary=b6.calculate()
        tested=[x for x in parts if x["causal_screen_response_status"].startswith("PASS_")]
        self.assertEqual(len(tested),1)
        self.assertEqual((tested[0]["child_model_key"],tested[0]["provider_key"],
                          tested[0]["original_source_element_index"]),
                         ("AF123","AF1394","4"))
        self.assertEqual(tested[0]["south_source_intervention_changed_pixels"],"751")
        self.assertEqual(tested[0]["north_source_intervention_changed_pixels"],"0")
        self.assertEqual(sum(x["causal_screen_response_status"]=="NOT_INDIVIDUALLY_CAUSAL_TESTED"
                             for x in parts),44)
        self.assertEqual(summary["counts"]["tested_element_render_response"],1)

    def test_15_group_single_tested_seat_and_44_untested(self):
        parts,groups,queue,summary=b6.calculate()
        tested=[x for x in groups if x["tested_element_count"]=="1"]
        self.assertEqual(len(tested),1)
        self.assertEqual((tested[0]["child_model_key"],
                          tested[0]["original_role_group_hypothesis"],
                          tested[0]["tested_element_indices"]),
                         ("AF123","SEAT_LAYER","4"))
        self.assertEqual(sum(int(x["untested_element_count"]) for x in groups),44)
        self.assertTrue(all(x["group_function_or_material_approved"]=="false"
                            for x in groups))

    def test_proposals_not_claimed_as_actual_tests(self):
        parts,groups,queue,summary=b6.calculate()
        self.assertEqual(len(queue),9)
        self.assertEqual((queue[0]["priority"],queue[0]["child_model_key"],
                          queue[0]["original_source_element_index"]),("1","AF121","4"))
        self.assertTrue(all(x["candidate_only_not_a_completed_experiment"]=="true"
                            for x in queue))
        self.assertEqual(summary["next_high_priority_explicit_candidate"]["test_status"],
                         "NOT_RUN")
        self.assertEqual(summary["counts"]["new_game_sessions_in_B6"],0)

    def test_no_false_material_style_function_ownership_or_training_rights(self):
        parts,groups,queue,summary=b6.calculate()
        self.assertTrue(all(
            r["original_element_unique_pixel_ownership_approved"]=="false" and
            r["part_function_verified"]=="false" and
            r["material_or_style_verified"]=="false" and
            r["training_or_redistribution_rights_approved"]=="false" for r in parts))
        c=summary["counts"]
        for key in ("original_pixel_ownership_confirmations",
                    "part_function_final_approvals","material_or_style_final_approvals",
                    "INT6_AI_training_or_redistribution_approvals",
                    "new_native_F2_captured_in_B6"):
            self.assertEqual(c[key],0)

    def test_b5_south_pixels_or_b4_original_sha_mutation_rejected(self):
        p,g,b3,b4,b5=loaded()
        idx,*_=b6.index_source(p)
        bad=deepcopy(b5)
        bad["per_view_effects"]["south"]["element4_removal_source_intervention_delta_pixels"]=752
        with self.assertRaisesRegex(ValueError,"original B5 signed"):
            b6.validate_audit(b3,b4,bad,idx)
        bad=deepcopy(b5)
        bad["original_baseline_F2_sha256"]["north_slab_only"]="0"*64
        with self.assertRaisesRegex(ValueError,"baseline/native-F2"):
            b6.validate_audit(b3,b4,bad,idx)

    def test_source_missing_element_or_group_membership_rejected(self):
        p,g,b3,b4,b5=loaded()
        with self.assertRaisesRegex(ValueError,"exact 45"):
            b6.index_source(p[:-1])
        idx,*_=b6.index_source(p)
        corrupt=deepcopy(g)
        corrupt[0]["element_indices"]="7|8|8"
        with self.assertRaisesRegex(ValueError,"duplicate/empty group"):
            b6.validate_groups(corrupt,idx)

    def test_sha_drift_rejected_and_original_files_unmodified(self):
        original=b6.original_sources()
        with TemporaryDirectory() as folder:
            root=Path(folder)
            (root/b6.D).mkdir(parents=True)
            for name,raw in original.items():
                (root/b6.D/name).write_bytes(raw)
            name=b6.SOURCES_NAMES[0]
            (root/b6.D/name).write_bytes(original[name]+b"mutated")
            with self.assertRaisesRegex(ValueError,"Git blob changed"):
                b6.original_sources(root)
        self.assertEqual(b6.original_sources(),original)

    def test_outputs_rebuild_deterministically_and_verify_drift(self):
        data=b6.products()
        self.assertEqual(len(data),4)
        with TemporaryDirectory() as d:
            root=Path(d)
            for path,blob in data.items():
                p=root/path
                p.parent.mkdir(parents=True,exist_ok=True)
                p.write_bytes(blob)
            self.assertEqual(b6.run(out=root,verify=True)["counts"]["untested_elements"],44)
            p=root/b6.OUT["parts"]
            p.write_bytes(p.read_bytes()+b"\n")
            with self.assertRaisesRegex(ValueError,"not an exact original-input"):
                b6.run(out=root,verify=True)

if __name__=="__main__":
    unittest.main()
