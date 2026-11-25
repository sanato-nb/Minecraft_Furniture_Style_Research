"""INT-5-B6: independently join 45 B3 source parts and 15 role groups to B5 F2.

Strictly distinguish (a) source geometry/UV/texture role hypotheses, (b) one
verified *removal* -> rendered screen response, and (c) NEVER approved original
element-owned pixels, real-world physical function, material, style or rights.
This step does not execute Minecraft or extract/commit third-party assets.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import csv
import hashlib
import io
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
D = Path("project/integration")
SOURCES = {
    "INT5_B3_45_PART_ROLE_TEXTURE_CUE_DECISIONS_V1.csv":
        "d314941b950b70fa637536f86182eb4866b7aed1",
    "INT5_B3_15_ROLE_GROUP_SCREEN_EVIDENCE_V1.csv":
        "5b329287591d413cf47b23762e0c5b2755f6a210",
    "INT5_B3_45_ROLE_TEXTURE_SOURCE_SCOPE_RESULT_V1.json":
        "3af3bf3db640439a88d8a9fc2d8c1d92fbd677e6",
    "INT5_B4_AF_TUCKED_SLAB_REAL_F2_AUDIT_V1.json":
        "aa7afebac071a21e497d396a9b77840f2f4047cd",
    "INT5_B5_AF123_ELEMENT4_NATIVE_F2_CAUSAL_AUDIT_V1.json":
        "a1943b38c12025d41e6948670a67694ff9a39456",
}
OUT = {
    "parts": D / "INT5_B6_45_ELEMENT_CAUSAL_EVIDENCE_LEDGER_V1.csv",
    "groups": D / "INT5_B6_15_ROLE_GROUP_CAUSAL_COVERAGE_V1.csv",
    "queue": D / "INT5_B6_NEXT_SOURCE_ELEMENT_EXPERIMENT_QUEUE_V1.csv",
    "summary": D / "INT5_B6_45_PART_CAUSAL_SCOPE_RESULT_V1.json",
}
MODELS = {"AF121": (10,46), "AF123": (10,46),
          "HC11210": (13,78), "MACAW67": (12,59)}
ROLES = {"LEG_OR_LOWER_POST":16, "BACKREST_ASSEMBLY":16,
         "LOWER_FRAME":7, "SEAT_LAYER":6}
PROVIDERS = {"AF121":"AF1393", "AF123":"AF1394",
             "HC11210":"HC13","MACAW67":"MACAW1424"}
CUE_NAMED = {
    "ROLE_NAMED_ORIGINAL_SEAT_PNG",
    "ROLE_NAMED_ORIGINAL_BACK_PNG",
    "ROLE_NAMED_ORIGINAL_CUSHION_PNG",
}
CONTRAST = "UNIQUE_SOURCE_TEXTURE_CONTRAST_NO_ROLE_NAME"
GENERIC = "GENERIC_OR_SHARED_TEXTURE_NOT_ROLE_PROOF"
TESTED_KEY = ("AF123", "AF1394", 4)
QUEUE_KEYS = [("AF121",4),("HC11210",12),
              ("AF121",7),("AF121",8),("AF121",9),
              ("AF123",7),("AF123",8),("AF123",9),("MACAW67",0)]
PART_COLUMNS = (
    "child_model_key","provider_key","original_source_element_index",
    "original_role_hypothesis","source_element_original_face_count",
    "source_texture_role_cue","original_source_f2_cases",
    "original_game_scene_observation","research_to_runtime_caveat",
    "causal_screen_response_status","causal_tested_game_case",
    "source_element_removed_from_disposable_release_model",
    "native_f2_pair_count_original_plus_modified",
    "south_source_intervention_changed_pixels",
    "north_source_intervention_changed_pixels",
    "south_unchanged_slab_and_air_negative_control_pixels",
    "north_unchanged_slab_and_air_negative_control_pixels",
    "original_element_unique_pixel_ownership_approved",
    "part_function_verified","material_or_style_verified",
    "training_or_redistribution_rights_approved",
    "evidence_source","next_experiment_priority_only"
)
GROUP_COLUMNS = (
    "child_model_key","original_role_group_hypothesis",
    "original_source_group_element_count","source_group_element_indices",
    "original_group_source_faces","tested_element_count",
    "tested_element_indices","render_response_confirmed_element_count",
    "south_positive_screen_response_count",
    "north_zero_screen_response_count",
    "untested_element_count","source_group_role_hypothesis_only",
    "group_function_or_material_approved","evidence"
)
QUEUE_COLUMNS = (
    "priority","child_model_key","provider_key","original_source_element_index",
    "original_role_hypothesis","original_source_role_texture_cue",
    "original_F2_scene_context","proposed_bounded_next_test",
    "candidate_only_not_a_completed_experiment"
)

def need(ok, why):
    if not ok:
        raise ValueError("INT5-B6 independent source/causality rejected: " + why)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def git_blob(data):
    return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()

def rows(data):
    result=list(csv.DictReader(io.StringIO(data.decode("utf-8-sig"))))
    need(bool(result) and all(None not in r for r in result),
         "missing CSV cells or invalid CSV header")
    return result

def original_sources(root=ROOT):
    root=Path(root)
    blobs={}
    for name, expected in SOURCES.items():
        data=(root/D/name).read_bytes()
        need(git_blob(data)==expected, "pinned upstream Git blob changed: "+name)
        blobs[name]=data
    return blobs

def index_source(parts):
    need(len(parts)==45, "B3 exact 45 elements missing")
    matched={}
    models=Counter()
    faces=Counter()
    roles=Counter()
    cues=Counter()
    for r in parts:
        k=r["child_model_key"]
        need(k in MODELS and r["provider_key"]==PROVIDERS[k],
             "unknown child/provider exact source identity")
        i=int(r["original_source_element_index"])
        idx=(k,r["provider_key"],i)
        need(idx not in matched and 0<=i<MODELS[k][0],
             "duplicate/out-of-range element")
        n=int(r["source_element_original_face_count"])
        need(0<n<=6 and r["original_role_hypothesis"] in ROLES,
             "invalid source face/role")
        need(all(r[c]=="false" for c in (
            "individual_element_to_original_F2_pixels_approved",
            "part_function_verified","material_or_style_verified",
            "training_or_redistribution_rights_approved")),
            "a historical B3 element was falsely promoted")
        need(len(r["source_related_real_F2_cases"].split("|"))==4,
             "original four states absent")
        cue=r["role_discriminating_texture_cue"]
        need(cue in CUE_NAMED|{CONTRAST,GENERIC},"unknown original cue")
        models[k]+=1
        faces[k]+=n
        roles[r["original_role_hypothesis"]]+=1
        cues[cue]+=1
        matched[idx]=r
    need({k:(models[k],faces[k]) for k in MODELS}==MODELS,
         "original 45 element / 229 faces provider distribution changed")
    need(dict(roles)==ROLES,"original 45 part-role partition drift")
    need(sum(cues[x] for x in CUE_NAMED)==9 and
         cues[CONTRAST]==1 and cues[GENERIC]==35,
         "B3 exact role cues 9 + 1 + 35 drift")
    return matched, models, faces, cues

def validate_groups(groups, indexed):
    need(len(groups)==15,"B3 exact 15 role groups missing")
    grouped={}
    used=set()
    for r in groups:
        model=r["child_model_key"]
        role=r["original_role_group_hypothesis"]
        need(model in MODELS and role in ROLES,
             "unknown original group/role")
        label=(model,role)
        need(label not in grouped,"duplicate B3 role group")
        indices=[int(i) for i in r["element_indices"].split("|")]
        need(indices and len(indices)==len(set(indices)) and
             int(r["source_element_count"])==len(indices),
             "duplicate/empty group indices")
        subset=[indexed[(model,PROVIDERS[model],i)] for i in indices]
        need(all(x["original_role_hypothesis"]==role for x in subset),
             "role group does not match exact individual source element roles")
        need(sum(int(x["source_element_original_face_count"]) for x in subset)==
             int(r["total_source_faces_in_group"]),
             "group original UV face sum not proved")
        need(r["actual_element_function_verified"]=="false" and
             r["unique_element_screen_pixels_approved"]=="false",
             "B3 group unsupported meaning/pixel approval")
        need(r["source_group_render_appearance_scope_only"]=="true",
             "B3 original group render-scope flag drift")
        for i in indices:
            key=(model,PROVIDERS[model],i)
            need(key not in used, "source element appears in two groups")
            used.add(key)
        grouped[label]=(r,indices)
    need(used==set(indexed),"15 groups do not partition all 45 exact parts")
    need(sum(int(r["total_source_faces_in_group"]) for r in groups)==229,
         "groups do not partition 229 UV faces")
    return grouped

def validate_audit(b3,b4,b5,indexed):
    need(b3["decision"]==
         "PASS_INDEPENDENT_SOURCE_UV_ROLE_CUE_AND_WHOLE_GROUP_VISUAL_TRIAGE_ONLY",
         "B3 source/visual limited decision changed")
    c=b3["counts"]
    need(all(c[key]==n for key,n in {
        "source_elements_reopened":45,"original_source_faces_reopened":229,
        "native_F2_screenshots_reopened":16,"role_groups_context_checked":15,
        "named_source_texture_role_cue_elements":9,
        "role_cue_and_visible_group_appearance_consistent":8,
        "AF_tucked_seat_cue_obscured":1,
        "distinct_texture_without_role_name":1,
        "generic_texture_only_role_hypotheses":35,
        "element_function_semantics_final_approvals":0,
        "new_exact_element_to_screen_pixel_identifications":0,
        "INT6_training_or_redistribution_approvals":0}.items()),
         "B3 historical evidence or approvals drift")
    b3files=b3["output_sha256"]
    need(sha(original_sources()[SOURCES_NAMES[0]])==b3files[str(D/SOURCES_NAMES[0])] and
         sha(original_sources()[SOURCES_NAMES[1]])==b3files[str(D/SOURCES_NAMES[1])],
         "B3 source row CSV is not the independently verified original")
    need(b4["decision"]==
         "PASS_REAL_FABRIC_BOTH_VIEW_SUPPORTED_TUCKED_CHAIR_VS_SLAB_CONTROLS" and
         b4["original_native_F2_verified"]==8 and
         b4["exact_server_chair_state_and_slab_pair_checks"]==16 and
         b4["source_case"]=="AF123_north" and
         b4["tucked_true_without_support_was_tested"] is False and
         b4["new_element_function_approvals"]==0,
         "B4 original legal support-slab controls missing")
    need(b5["decision"]=="PASS_BOUNDED_AF123_ELEMENT4_REMOVAL_RENDER_RESPONSE" and
         b5["original_baseline_F2_sha256"]==b4["native_F2_sha256"] and
         b5["original_client_log_sha256"]==b4["original_client_log_sha256"] and
         b5["baseline_F2_verified"]==b4["original_native_F2_verified"]==8 and
         b5["disposable_model_F2_verified"]==8 and
         b5["two_separate_real_game_sessions"]==2 and
         b5["modified_session_server_chair_slab_state_checks"]==16,
         "B5 baseline/native-F2/state SHA provenance not anchored to B4")
    p=b5["provenance"]
    need(p["original_element_index"]==4 and
         p["selected_original_blockstate"]==
         "another_furniture:acacia_chair[facing=north,tucked=true,variant=10]" and
         p["selected_original_model"]==
         "another_furniture:block/chair/acacia_10_tucked" and
         p["provider_member"]==
         "assets/another_furniture/models/block/template/chair_tucked.json" and
         p["original_released_provider_element_count"]==10 and
         p["disposable_provider_element_count"]==9 and
         p["original_released_face_count"]==46 and
         p["disposable_provider_face_count"]==40 and
         len(p["original_element_faces"])==6 and
         p["modified_uncompressed_jar_member_count"]==1 and
         p["modified_member_is_only_provider_json"] is True and
         p["modified_jar_and_source_model_never_archived"] is True and
         p["source_4_0_3_vs_release_4_0_2_not_assumed_equivalent"] is True,
         "B5 ephemeral original JAR/element index not independently validated")
    need(b5["source_role_hypothesis_not_function"]==
         indexed[TESTED_KEY]["original_role_hypothesis"]=="SEAT_LAYER",
         "B3 source element not the same B5 tested element")
    metrics=b5["per_view_effects"]
    need(set(metrics)=={"south","north"} and
         metrics["south"]["element4_removal_source_intervention_delta_pixels"]==751 and
         metrics["north"]["element4_removal_source_intervention_delta_pixels"]==0 and
         all(v["element4_removal_source_intervention_delta_pixels"]==
             v["element4_removal_repeated_delta_pixels"] for v in metrics.values()) and
         all(v["unchanged_slab_only_negative_control_pixels"]==0 and
             v["unchanged_air_negative_control_pixels"]==0 and
             v["modified_session_temporal_delta_pixels"]==0 and
             v["intervention_pixels_outside_original_visible_chair_foreground"]==0
             for v in metrics.values()) and
         b5["unmodified_controls_equal"] is True and
         b5["visible_screen_effect_detected"] is True and
         b5["no_change_outside_original_chair_foreground"] is True and
         b5["individual_original_element_pixel_ownership_approved"] is False and
         b5["physical_seating_or_material_approved"] is False and
         b5["final_INT5_part_meaning_approvals"]==0 and
         b5["INT6_AI_training_or_redistribution_approvals"]==0,
         "original B5 signed per-camera 751/0 causality or negative control drift")
    return metrics

SOURCES_NAMES = (
    "INT5_B3_45_PART_ROLE_TEXTURE_CUE_DECISIONS_V1.csv",
    "INT5_B3_15_ROLE_GROUP_SCREEN_EVIDENCE_V1.csv",
    "INT5_B3_45_ROLE_TEXTURE_SOURCE_SCOPE_RESULT_V1.json",
    "INT5_B4_AF_TUCKED_SLAB_REAL_F2_AUDIT_V1.json",
    "INT5_B5_AF123_ELEMENT4_NATIVE_F2_CAUSAL_AUDIT_V1.json",
)

def calculate(root=ROOT):
    blobs=original_sources(root)
    inputs={name:blobs[name] for name in SOURCES_NAMES}
    source_parts=rows(inputs[SOURCES_NAMES[0]])
    source_groups=rows(inputs[SOURCES_NAMES[1]])
    b3,b4,b5=(json.loads(inputs[name]) for name in SOURCES_NAMES[2:])
    indexed,models,faces,cues=index_source(source_parts)
    groups=validate_groups(source_groups,indexed)
    evidence=validate_audit(b3,b4,b5,indexed)
    part_rows=[]
    for idx,r in sorted(indexed.items()):
        tested=idx==TESTED_KEY
        role_cue=r["role_discriminating_texture_cue"]
        status=("PASS_SOURCE_ELEMENT_REMOVAL_CAUSES_REAL_SOUTH_F2_CHANGE"
                if tested else "NOT_INDIVIDUALLY_CAUSAL_TESTED")
        follow=("NEXT_A_F_121_ELEMENT4_EXPOSED_SEAT_CONTROL" if
                (idx[0],idx[2])==("AF121",4) else
                "ROLE_NAMED_SOURCE_CUE_NEXT_CANDIDATE" if role_cue in CUE_NAMED and not tested
                else "DISTINCT_TEXTURE_NO_ROLE_NAME_NEXT_CANDIDATE" if role_cue==CONTRAST
                else "NOT_PRIORITY_BASED_ON_FILENAME")
        part_rows.append(dict(zip(PART_COLUMNS, (
            idx[0],idx[1],str(idx[2]),r["original_role_hypothesis"],
            r["source_element_original_face_count"],role_cue,
            r["source_related_real_F2_cases"],r["original_game_scene_observation"],
            r["research_and_runtime_source_caveat"],
            status,"AF123_north" if tested else "",
            "true" if tested else "false","8+8" if tested else "",
            str(evidence["south"]["element4_removal_source_intervention_delta_pixels"]) if tested else "",
            str(evidence["north"]["element4_removal_source_intervention_delta_pixels"]) if tested else "",
            "0" if tested else "","0" if tested else "",
            "false","false","false","false",
            "INT5_B5_AF123_ELEMENT4_NATIVE_F2_CAUSAL_AUDIT_V1.json" if tested else
            "INT5_B3_45_PART_ROLE_TEXTURE_CUE_DECISIONS_V1.csv",follow
        ))))
    group_rows=[]
    for (model,role),(source,indices) in sorted(groups.items()):
        tested=[i for i in indices if (model,PROVIDERS[model],i)==TESTED_KEY]
        group_rows.append(dict(zip(GROUP_COLUMNS,(
            model,role,str(len(indices)),"|".join(map(str,indices)),
            source["total_source_faces_in_group"],str(len(tested)),
            "|".join(map(str,tested)),str(len(tested)),str(len(tested)),
            "0",str(len(indices)-len(tested)),"true","false",
            "B3_ROLE_GROUP+LIMITED_B5_CAUSAL_RESPONSE_ONLY" if tested else
            "B3_ROLE_GROUP_SOURCE_ONLY"
        ))))
    need(len(part_rows)==45 and len(group_rows)==15 and
         sum(r["causal_screen_response_status"].startswith("PASS_") for r in part_rows)==1 and
         sum(int(r["tested_element_count"]) for r in group_rows)==1 and
         sum(int(r["untested_element_count"]) for r in group_rows)==44,
         "one tested vs 44 untouched partition not preserved")
    lookup={(r["child_model_key"],int(r["original_source_element_index"])):r
            for r in part_rows}
    need(len(QUEUE_KEYS)==len(set(QUEUE_KEYS))==9,
         "source experiment proposal queue missing a unique candidate")
    queue=[]
    for rank,k in enumerate(QUEUE_KEYS,1):
        r=lookup[k]
        need(r["causal_screen_response_status"]=="NOT_INDIVIDUALLY_CAUSAL_TESTED",
             "prioritize only untested exact source elements")
        need(r["source_texture_role_cue"] in CUE_NAMED|{CONTRAST},
             "do not present generic texture as a role-specific priority")
        kind=("SAME_FABRIC_1_21_1_EXPOSED_SEAT_SINGLE_ELEMENT_REMOVAL_TWO_VIEW_F2"
              if k==("AF121",4) else
              "SEPARATE_PINNED_RELEASE_ORIGINAL_ELEMENT_F2_CAUSAL_TRIAL_NOT_YET_RUN")
        queue.append(dict(zip(QUEUE_COLUMNS,(
            str(rank),r["child_model_key"],r["provider_key"],
            r["original_source_element_index"],r["original_role_hypothesis"],
            r["source_texture_role_cue"],r["original_game_scene_observation"],
            kind,"true"
        ))))
    summary={
        "schema":"MCFR_INT5_B6_45_ORIGINAL_ELEMENT_CAUSAL_PROVENANCE_LEDGER/v1",
        "decision":"PASS_PINNED_B3_B4_B5_META_EVIDENCE_RECONCILIATION_ONLY",
        "counts":{
            "original_source_elements":45,"original_source_faces":229,
            "role_groups":15,"original_native_F2_B3":16,
            "historical_b4_native_F2_used":8,"b5_disposable_new_native_F2":8,
            "b5_actual_game_sessions_total_in_comparison":2,
            "b5_server_chair_slab_pair_checks":16,
            "tested_element_render_response":1,
            "untested_elements":44,"source_role_named_cues_all":9,
            "source_role_named_cues_still_untested":8,
            "distinct_texture_no_role_name_untested":1,
            "generic_source_texture_untested":35,
            "proposed_priority_queue_not_executed":9,
            "original_pixel_ownership_confirmations":0,
            "part_function_final_approvals":0,
            "material_or_style_final_approvals":0,
            "INT6_AI_training_or_redistribution_approvals":0,
            "new_native_F2_captured_in_B6":0,
            "new_game_sessions_in_B6":0,
        },
        "tested_exact_part":{
            "child_model_key":"AF123","provider_key":"AF1394",
            "source_element_index":4,"source_role_hypothesis_not_function":"SEAT_LAYER",
            "actual_running_fabric_release":"4.0.2",
            "tested_source_blockstate":b5["provenance"]["selected_original_blockstate"],
            "tested_original_F2_state":"AF123_north",
            "original_release_provider":b5["provenance"]["provider_member"],
            "source_provider_git_blob_sha1":b5["provenance"]["original_provider_git_blob_sha1"],
            "actual_game_south_intervention_delta_pixels":751,
            "actual_game_north_intervention_delta_pixels":0,
            "negative_controls_per_view_all_zero":True,
            "no_pixel_change_outside_original_chair_foreground":True,
            "source_element_removal_vs_exclusive_original_pixels":
                "REMOVAL_RENDER_RESPONSE_ONLY_NOT_UNIQUE_ORIGINAL_ELEMENT_OWNERSHIP",
        },
        "next_high_priority_explicit_candidate":{
            "model_key":"AF121","source_element_index":4,
            "why":"B3 seat-specific texture and four whole-chair F2 views; no tucked=true support slab; B5 response is not transferred to AF121.",
            "test_status":"NOT_RUN",
        },
        "pinned_git_blob_sha1":dict(sorted(SOURCES.items())),
        "pinned_B3_output_sha256":b3["output_sha256"],
        "pinned_B4_native_F2_sha256":b4["native_F2_sha256"],
        "pinned_B5_disposable_native_F2_sha256":b5["modified_runtime_F2_sha256"],
        "limits":[
            "All 45 B3 source elements and 15 role groups remain intact; only AF123 element4 has tested removal-induced screen response.",
            "Original B3 source is Git 4.0.3, while the tested AF123 runtime model is official Fabric 4.0.2. No cross-version byte equivalence inferred.",
            "AF123 element4 is only proven to change 751 pixels south and 0 north under the pinned B4 supported tucked state and ROI, not to exclusively own those pixels.",
            "No evidence is transferred from the tested north-facing AF123 to the untested three facings, AF121, HC, Macaw, or the other 44 elements.",
            "Texture role names, screen shape, geometric positioning, and pixel response do not prove seating, structural function, material, style, AI training or redistribution rights.",
            "Priority order is a research hypothesis, not a completion percentage or certification.",
            "Old strict INT4 H03 HOLD, H05 CONDITIONAL and F70 0 unconditional approvals remain unchanged.",
        ],
    }
    return part_rows,group_rows,queue,summary

def csv_bytes(dataset, columns):
    b=io.StringIO(newline="")
    writer=csv.DictWriter(b,fieldnames=columns,lineterminator="\n")
    writer.writeheader()
    writer.writerows(dataset)
    return b.getvalue().encode("utf-8")

def products(root=ROOT):
    parts,groups,queue,summary=calculate(root)
    output={
        OUT["parts"]:csv_bytes(parts,PART_COLUMNS),
        OUT["groups"]:csv_bytes(groups,GROUP_COLUMNS),
        OUT["queue"]:csv_bytes(queue,QUEUE_COLUMNS),
    }
    summary["output_sha256"]={str(k):sha(v) for k,v in sorted(
        output.items(),key=lambda x:str(x[0]))}
    output[OUT["summary"]]=(
        json.dumps(summary,ensure_ascii=False,sort_keys=True,indent=2)+"\n"
    ).encode("utf-8")
    return output

def run(root=ROOT,out=ROOT,verify=False):
    calculated=products(root)
    dest=Path(out)
    for relative,raw in calculated.items():
        path=dest/relative
        if verify:
            need(path.is_file() and path.read_bytes()==raw,
                 "committed output not an exact original-input regeneration: "+str(relative))
        else:
            path.parent.mkdir(parents=True,exist_ok=True)
            path.write_bytes(raw)
    return json.loads(calculated[OUT["summary"]])

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--root",type=Path,default=ROOT)
    p.add_argument("--out",type=Path,default=ROOT)
    p.add_argument("--verify",action="store_true")
    args=p.parse_args()
    print(json.dumps(run(args.root,args.out,args.verify),
                     ensure_ascii=False,sort_keys=True))

if __name__=="__main__":
    main()
