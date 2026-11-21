"""INT-4 independent non-chair state+source regression tests; no images fabricated."""
import json
from pathlib import Path
import unittest

from scripts.integration import audit_int4_nonchair_source as a

ROOT=Path(__file__).resolve().parents[2]

class NonChairSourceTest(unittest.TestCase):
    def test_fixed_15_cases_furniture_categories_four(self):
        self.assertEqual(len(a.CASE_IDS),15)
        self.assertEqual(set(a.CATEGORY.values()),{"LARGE_TABLE","SHELVING","BED","KITCHEN"})
        self.assertEqual(sum(v[0] for v in a.EXPECTED.values()),19)
        self.assertEqual(len(a.CLAIM_CASES),6)

    def test_original_model_row_count_and_history_cases(self):
        cases,_=a.read_rows(ROOT/a.CASES)
        apps,_=a.read_rows(ROOT/a.APPS)
        self.assertEqual(len(cases),62)
        self.assertEqual(len(apps),74)
        self.assertEqual(len([x for x in apps if x["case"] in a.CASE_IDS]),19)
        self.assertEqual({x["cohort"] for x in apps if x["case"] in a.CASE_IDS},
                         {"AF","HC","MACAW"})

    def test_multipart_and_variants_source_rules(self):
        state=a.state_map("facing=north;leg_1=true")
        table={"multipart":[
           {"apply":{"model":"another_furniture:block/table/oak_top"}},
           {"when":{"leg_1":"true|false"},"apply":[
              {"model":"another_furniture:block/table/oak_leg","y":90},
              {"model":"another_furniture:block/table/oak_leg","y":270}]},
           {"when":{"OR":[{"facing":"south"},{"facing":"west"}]},"apply":{"model":"x:y"}}
        ]}
        rows=a.match_state(table,state)
        self.assertEqual([(n,i) for n,i,_ in rows],[(0,0),(1,0),(1,1)])
        self.assertEqual(len(a.match_state({"variants":{
            "facing=north,leg_1=true":{"model":"a:b"},
            "facing=south,leg_1=true":{"model":"a:c"}}},state)),1)

    def test_comparison_pairs_preserve_actual_historical_faces(self):
        values={}
        case_records={}
        for case,(apps,elements,faces) in a.EXPECTED.items():
            per_e,extra_e=divmod(elements,apps)
            per_f,extra_f=divmod(faces,apps)
            values[case]=[
               {"model_source_sha":case+str(i),
                "element_count":per_e+(i<extra_e),
                "face_count":per_f+(i<extra_f)} for i in range(apps)]
            case_records[case]={"elements":str(elements),"faces":str(faces)}
        pairs=a.check_pairs(values,case_records)
        self.assertEqual(len(pairs),6)
        self.assertEqual(pairs[-1]["left_face_count"],55)
        self.assertEqual(pairs[-1]["right_face_count"],56)
        self.assertFalse(any(x["client_visual_equivalence_approved"] for x in pairs))

    def test_mutated_face_count_rejected(self):
        values={}
        case_records={}
        for case,(apps,elements,faces) in a.EXPECTED.items():
            values[case]=[{"model_source_sha":str(i),"element_count":elements if i==0 else 0,
                            "face_count":faces if i==0 else 0} for i in range(apps)]
            case_records[case]={"elements":str(elements),"faces":str(faces)}
        values["S42"][0]["face_count"]=56
        with self.assertRaisesRegex(a.EvidenceError,"geometry count mismatch"):
            a.check_pairs(values,case_records)

    def test_texture_slot_resolution_bound_missing_and_cycles(self):
        faces=[
           ({"texture":"#front"},{"front":"#base","base":"mcwfurnitures:block/counter/oak"}, "TEXTURE_RESOURCE_RESOLVED"),
           ({"texture":"#wrong"},{"front":"x:y"},"SLOT_UNBOUND"),
           ({"texture":"#loop"},{"loop":"#other","other":"#loop"},"CYCLIC_TEXTURE_SLOT"),
           ({},{},"FACE_TEXTURE_UNDECLARED"),
        ]
        for face,slots,status in faces:
            with self.subTest(status=status):
                self.assertEqual(a.resolve_face_texture(face,slots)[0],status)

    def test_invalid_selector_duplicates_and_wrong_multipart_are_rejected(self):
        for content in ["x=y;x=z","facing","=north"]:
            with self.assertRaises(a.EvidenceError):
                a.state_map(content)
        with self.assertRaises(a.EvidenceError):
            a.match_state({"multipart":[{"when":{},"x":1}]},{"facing":"north"})
        with self.assertRaises(a.EvidenceError):
            a.obj(b'{"parent":"a","parent":"b"}',"bad")

    def test_original_comparison_claims_remain_historic_only(self):
        claims,_=a.read_rows(ROOT/a.CLAIMS)
        dictionary={x["finding_id"]:x for x in claims}
        for key,required in a.CLAIM_CASES.items():
            self.assertEqual(dictionary[key]["runtime_evidence_status"],
                             "HISTORIC_ONLY_NOT_REEXECUTED")
            self.assertTrue(set(required).issubset(set(dictionary[key]["cases"].split("|"))))

    def test_parent_48_are_out_of_the_int4_nonchair_reachability_scope(self):
        data=json.loads((ROOT/a.REACHABILITY).read_text(encoding="utf-8"))
        self.assertEqual(data["observed"]["summary"]["in_static_blockstate_source_selection_or_parent_chain"],0)
        self.assertEqual(data["observed"]["summary"]["historical_missing_parent_model_paths"],48)
        self.assertFalse(data["boundaries"]["game_client_visual_fault_not_proven"] is False)

if __name__=="__main__":
    unittest.main()
