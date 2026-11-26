"""INT-5-B24 independent 45-element/229-face texture and role-evidence coverage audit.

Read the original B3 source/UV semantic-proposal ledger and the B22 45-element
native-F2 provenance ledger; do not infer physical meaning from a texture name.
Only provenance and bounded render response are already supported, while
function, material, style, face-pixel ownership and rights remain unapproved.
This script never reads/shares original third-party image or mod JAR bytes.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

SOURCE_B3="project/integration/INT5_B3_45_PART_ROLE_TEXTURE_CUE_DECISIONS_V1.csv"
SOURCE_B22="project/integration/INT5_B22_FOUR_MODEL_45_ELEMENT_STATUS_V1.csv"
CSV_COLUMNS=(
    "model","provider","source_element_index","face_count",
    "source_role_hypothesis_not_approved",
    "source_texture_cue","original_texture_source_hashes",
    "source_runtime_version_caveat","B19_original_removal_status",
    "B19_original_removal_pixel_response_observed",
    "B21_real_isolation_experiment","B22_original_pair_real_experiment",
    "original_element_to_F2_unique_face_pixel_attributed",
    "role_function_semantics_approved","material_or_style_approved",
    "third_party_training_or_redistribution_rights_approved",
    "next_evidence_needed","strict_decision"
)
SUPPORTED_ROLES={
    "LEG_OR_LOWER_POST","SEAT_LAYER","LOWER_FRAME","BACKREST_ASSEMBLY"
}
SUPPORTED_CUES={
    "GENERIC_OR_SHARED_TEXTURE_NOT_ROLE_PROOF",
    "ROLE_NAMED_ORIGINAL_SEAT_PNG",
    "ROLE_NAMED_ORIGINAL_BACK_PNG",
    "ROLE_NAMED_ORIGINAL_CUSHION_PNG",
    "UNIQUE_SOURCE_TEXTURE_CONTRAST_NO_ROLE_NAME"
}
NO_RESPONSE="B19_FOUR_VIEW_NO_VISIBLE_RESPONSE"
TARGETS={"AF121/AF1393/5","AF123/AF1394/5"}

def need(condition,reason):
    if not condition:
        raise ValueError("INT5-B24: "+reason)

def read_csv(root,rel):
    file=root/rel
    data=file.read_bytes()
    with file.open(encoding="utf-8-sig",newline="") as stream:
        rows=list(csv.DictReader(stream))
    need(rows and all(None not in r and all(v is not None for v in r.values())
                      for r in rows),"original CSV empty or malformed: "+rel)
    return rows,hashlib.sha256(data).hexdigest()

def build(root):
    root=Path(root)
    b3,b3hash=read_csv(root,SOURCE_B3)
    b22,b22hash=read_csv(root,SOURCE_B22)
    need(len(b3)==len(b22)==45,"exact original 45 source elements required")
    source={}
    legacy={}
    for row in b3:
        key=(row["child_model_key"],row["provider_key"],
             row["original_source_element_index"])
        need(key not in source,"B3 duplicated original element")
        need(row["original_role_hypothesis"] in SUPPORTED_ROLES and
             row["role_discriminating_texture_cue"] in SUPPORTED_CUES and
             row["individual_element_to_original_F2_pixels_approved"]=="false" and
             row["part_function_verified"]=="false" and
             row["material_or_style_verified"]=="false" and
             row["training_or_redistribution_rights_approved"]=="false",
             "B3 contains unsupported semantic or rights approvals")
        source[key]=row
    for row in b22:
        key=(row["model"],row["provider"],row["index"])
        need(key not in legacy,"B22 duplicated original element")
        need(row["state"].endswith("CAUSAL_PASS") or
             row["state"]==NO_RESPONSE,
             "B22 source removal status is not the validated original observation")
        need(row["B19_original_B18_status"] in (
             "", "B16_NO_VISIBLE_RESPONSE", "B15_NO_VISIBLE_RESPONSE",
             "B17_NO_VISIBLE_RESPONSE", "B19_FOUR_VIEW_NO_VISIBLE_RESPONSE"),
             "B22 previous original source status unexpected")
        legacy[key]=row
    need(set(source)==set(legacy),"45 source identities across B3/B22 do not match")
    result=[]
    for key in sorted(source):
        b,old=source[key],legacy[key]
        idx=int(key[2])
        face_count=int(b["source_element_original_face_count"])
        need(face_count>0 and face_count==int(old["faces"]),
             "original source face count differs in two independent evidence ledgers")
        need(int(old["index"])==idx and
             0<=idx<({"AF121":10,"AF123":10,"HC11210":13,
                       "MACAW67":12}[key[0]]),"original source range invalid")
        joined="/".join(key)
        is_unresolved=old["state"]==NO_RESPONSE
        expected_target=joined in TARGETS
        need(is_unresolved==expected_target,
             "original 2 B19 visible-response gaps must remain exact two AF source5")
        cue=b["role_discriminating_texture_cue"]
        texture_hashes=b["original_texture_source_hashes"]
        need(texture_hashes and b["original_textures_used"] and
             len(texture_hashes.split("|"))==len(b["original_textures_used"].split("|")),
             "each original texture evidence path needs matching source hash count")
        next_actions=[
            "ACTUAL_IMAGE_TO_INDIVIDUAL_ORIGINAL_ELEMENT_FACE_UV_PIXEL_ATTRIBUTION",
            "DIRECT_INDEPENDENT_VISUAL_ROLE_FUNCTION_PROOF",
            "MATERIAL_STYLE_REAL_TEXTURE_AND_RUNTIME_SOURCE_VERSION_CONFIRMATION",
            "THIRD_PARTY_RIGHTS_SEPARATE_AUTHORIZATION",
        ]
        if is_unresolved:
            next_actions.insert(0,"B23_ORIGINAL_CONTEXT_GROUP_INTERVENTION_AUDIT")
        if cue=="GENERIC_OR_SHARED_TEXTURE_NOT_ROLE_PROOF":
            next_actions.insert(0,"DISTINCTIVE_ROLE_TEXTURE_EVIDENCE_ABSENT")
        if key[0].startswith("AF"):
            next_actions.insert(0,"AF_SOURCE_4_0_3_RUNTIME_4_0_2_BYTE_EQUIVALENCE_NOT_ESTABLISHED")
        result.append({
            "model":key[0],"provider":key[1],
            "source_element_index":str(idx),"face_count":str(face_count),
            "source_role_hypothesis_not_approved":b["original_role_hypothesis"],
            "source_texture_cue":cue,
            "original_texture_source_hashes":texture_hashes,
            "source_runtime_version_caveat":b["research_and_runtime_source_caveat"],
            "B19_original_removal_status":old["state"],
            "B19_original_removal_pixel_response_observed":str(not is_unresolved).lower(),
            "B21_real_isolation_experiment":
                old["B21_result"] if expected_target else "NOT_REQUIRED_FOR_THIS_ELEMENT",
            "B22_original_pair_real_experiment":
                old["B22_pair_decision"] if expected_target else "NOT_REQUIRED_FOR_THIS_ELEMENT",
            "original_element_to_F2_unique_face_pixel_attributed":"false",
            "role_function_semantics_approved":"false",
            "material_or_style_approved":"false",
            "third_party_training_or_redistribution_rights_approved":"false",
            "next_evidence_needed":"|".join(next_actions),
            "strict_decision":"RENDER_RESPONSE_UNRESOLVED_SEMANTIC_NOT_APPROVED"
                if is_unresolved else
                "BOUNDED_RENDER_RESPONSE_SEMANTIC_NOT_APPROVED",
        })
    counts=Counter(r["model"] for r in result)
    roles=Counter(r["source_role_hypothesis_not_approved"] for r in result)
    cues=Counter(r["source_texture_cue"] for r in result)
    needs=Counter("B19_VISIBLE_RESPONSE" if r["B19_original_removal_pixel_response_observed"]=="true"
                  else "B19_NO_RESPONSE" for r in result)
    need(dict(counts)=={"AF121":10,"AF123":10,"HC11210":13,"MACAW67":12}
         and sum(int(r["face_count"]) for r in result)==229
         and needs["B19_VISIBLE_RESPONSE"]==43
         and needs["B19_NO_RESPONSE"]==2
         and sum(v for k,v in cues.items() if k!="GENERIC_OR_SHARED_TEXTURE_NOT_ROLE_PROOF")==10,
         "45-element 229-face original evidence coverage invariant changed")
    return result,{
        "schema":"MCFR_INT5_B24_EXHAUSTIVE_45_SOURCE_ELEMENT_ROLE_EVIDENCE_COVERAGE/v1",
        "source_csv_sha256":{"B3":b3hash,"B22":b22hash},
        "original_source_elements":45,"original_source_faces":229,
        "source_element_count_by_original_model":dict(sorted(counts.items())),
        "role_hypotheses_not_final_approvals":dict(sorted(roles.items())),
        "texture_source_cues_not_semantic_proof":dict(sorted(cues.items())),
        "original_single_element_bounded_visible_response":43,
        "original_single_element_no_visible_response":2,
        "B21_B22_isolated_two_AF_cases_measured_but_original_full_model_unchanged":2,
        "source_named_or_distinct_texture_cues_not_role_approvals":10,
        "weak_shared_texture_role_cue_count":35,
        "individual_original_face_UV_GPU_pixel_ownership_approved":0,
        "individual_original_physical_function_role_approved":0,
        "individual_original_material_style_approved":0,
        "third_party_AI_training_and_redistribution_rights_approved":0,
        "H03":"HOLD","H05":"CONDITIONAL","F70_unconditional_approved":0,
        "B23_real_multi_context_results_not_prejudged":True,
        "original_assets_or_patched_mod_JAR_included":False,
        "note":"Original role text remains a hypothesis, not a proven identity. Texture path names and source face counts are not direct semantic labels. AF source 4.0.3 and pinned runtime 4.0.2 cannot be equated without direct byte evidence.",
    }

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root",type=Path,default=Path(__file__).resolve().parents[2])
    p.add_argument("--csv-out",type=Path,required=True)
    p.add_argument("--json-out",type=Path,required=True)
    args=p.parse_args()
    rows,doc=build(args.root)
    for file in (args.csv_out,args.json_out):
        file.parent.mkdir(parents=True,exist_ok=True)
        if file.resolve() in (args.root/SOURCE_B3,args.root/SOURCE_B22):
            raise ValueError("Original source ledgers must never be overwritten")
    with args.csv_out.open("w",encoding="utf-8",newline="") as stream:
        writer=csv.DictWriter(stream,fieldnames=CSV_COLUMNS)
        writer.writeheader();writer.writerows(rows)
    args.json_out.write_text(
        json.dumps(doc,ensure_ascii=False,indent=2,sort_keys=True)+"\n",
        encoding="utf-8")
    print(json.dumps(doc,ensure_ascii=False,sort_keys=True))

if __name__=="__main__":
    main()
