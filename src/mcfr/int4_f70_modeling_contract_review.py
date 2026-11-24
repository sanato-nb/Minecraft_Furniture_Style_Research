"""F70 modeling contract v1: independent ledger reconciliation, not original F exit.

Historical model cases and risk questions have separate denominators. Frozen
legacy approvals, raw assets, and original game records are never modified.
A modeling PASS is restricted to the pinned source model, selected state,
source UV measurements and bounded existing visual evidence; no GPU/rights
claim. Missing or different version evidence remains conditional.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import lzma
from collections import Counter, defaultdict
from pathlib import Path
import re
import subprocess
import sys

I="project/integration/"
B="research/furniture_mods/phase_1-5/B/"
PINS={
 I+"INT4_F_RENDER_TARGETS_V1.csv":"bf5d2caa3bfed68cec7cde9f2771e2b6f7944c92",
 I+"INT4_F11F_70_TARGET_EVIDENCE_DISPOSITIONS_V15.csv":"0cfbf3b1b174efc968de35c8466e2af8a9cd41c7",
 I+"INT4_G5_70_REAL_F2_SCOPED_DISPOSITIONS_V1.csv":"36b5ab428ad391f4b98d3191e61a50554b491e01",
 I+"INT4_E_62_CASE_SOURCE_LINKS_V1.csv":"e373dee238876476c96b305e1ec60f66f004c5ea",
 I+"INT4_H6_70_CASE_LOG_STATE_PROVENANCE_V1.csv":"f820efd9e85c4cee8df4673a2db4f4d868b4de31",
 I+"INT4_H03_H05_P0_P1_P2_70_CASE_NEW_ARCHIVE_REAUDIT_V1.csv":"54fbaa1b89c29c46106ade51638f8170306a15b0",
 I+"INT4_H03_H05_P0_P1_P2_70_CASE_SOURCE_RECHECK_V1.json":"c66e927e523d3d1deb4db8bc8d80aaf7ac18c32e",
 I+"INT4_H7_21_RISK_SUBSTAGE_SOURCE_VERIFIED_V1.csv":"5587951d70799c4dd7b7aafa7ef2ffee9a35c2fd",
 I+"INT4_H7_SIX_RISK_SOURCE_STAGE_AUDIT_V1.json":"fc0c28d005b45bf83e800535bfaac8ef1f3a9ea5",
 I+"INT4_H8_R03_ACTUAL_PLAYER_ITEM_SERVER_SHA_RESULT_V1.json":"6475bfe55c5e7b1f9b579c692a5d21144b252ef5",
 I+"INT4_F11F_R08_TWO_FABRIC_ORIGINAL_F2_INDEPENDENT_AUDIT_V1.json":"dbf5118138851f664468e5bcb8ef84e1edde6fd5",
 I+"INT4_F11E_R06_TEMPORAL_ORIGINAL_F2_INDEPENDENT_AUDIT_V1.json":"3ebc913a067e1e9817f7fe930673f9b651fdecc8",
 I+"INT4_F4_DIRECT_VISUAL_PARTIAL_ACCEPTANCE_SUMMARY_V1.json":"37c070d9c1a02fc2c93e264e4daaee72b1a552bf",
 I+"INT4_F7_S22_VANILLA_PARENT_EXTERNAL_EXCEPTION_V1.json":"e6eacf276641e9688c8fc35a7aec4af57d643302",
 I+"INT4_F8_S22_HASH_ALGORITHM_CORRECTION_V1.json":"2fbf9eb646a6720256e232f92fc5c586490b7abf",
 I+"INT4_H10_OCCUPIED_FOOT_REAL_CLIENT_SOURCE_AUDIT_V1.json":"b4e4639259f687c145f1766a2656346705e89027",
 I+"INT4_H10_OCCUPIED_SINGLE_FOOT_FACE_UV_SOURCE_AUDIT_V1.json":"65fbec88fde903d3f6858a1882215cc8ea859c2e",
 I+"INT4_H17_AF_DRAWER_ORIGINAL_PARENT_FACE_UV_TEXEL_RESEARCH_V1.json":"ad8f20b94a4d0cbdf1500db1ace57f3710b8149f",
 I+"INT4_H19_V11_BED_TYPE_RENDERER_REGISTRATION_RESULT_V1.json":"c02eb1cfb26b8e2396fac9ffff39b3f0db91112d",
 B+"APPLICATIONS.csv":"56e6f4c21c50714b97079ec61f7219bea845f179",
 B+"CASES.csv":"aebf449326b1e015c91b40417dde6e3e2dddd4f3",
 B+"ELEMENTS.csv":"d33bae64c9ea3d3e4a491b4e8f531af3a0d037d3",
 B+"FACES.csv.xz":"761d2a62ab5010aa5a4d4311218153b2f80678df",
 B+"ANIMATION_FRAMES.csv.xz":"b76f1fb05096f069562465727dd2b4f5605f5a49",
 B+"INDEPENDENT_AUDIT.json":"3fbc5151f9fb3fdc22100c5d991fb6d5d5f41c93",
 B+"audit_comparison.py":"b095382d9f7e5969da2ae3c000f498232ae9e7cc",
}
LEGACY="INT4_F11F_70_TARGET_EVIDENCE_DISPOSITIONS_V15.csv"
G5="INT4_G5_70_REAL_F2_SCOPED_DISPOSITIONS_V1.csv"
OUTPUT="INT4_F70_MODELING_CONTRACT_CASE_REVIEW_V1.csv"
SUMMARY="INT4_F70_MODELING_CONTRACT_SUMMARY_V1.json"
HIST={f"V{i:02}" for i in range(1,16)}|{f"S{i:02}" for i in range(1,48)}
RISKS={f"R{i:02}" for i in range(1,9)}
OK="PASS_MODELING_SCOPE"
RISK_OK="PASS_RISK_QUESTION_SCOPE"
COND="CONDITIONAL_MODELING"
HOLD="HOLD_MODELING"
RISK_COND="CONDITIONAL_RISK_QUESTION"

def check(condition,msg):
    if not condition:
        raise ValueError(msg)

def blob(data):
    return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()

def rows(p):
    opener=lzma.open if p.suffix==".xz" else open
    with opener(p,"rt",encoding="utf-8-sig",newline="") as f:
        return list(csv.DictReader(f))

def index(rs,k):
    d={r[k]:r for r in rs}
    check(len(d)==len(rs),"duplicate "+k)
    return d

def truth(v):return v is True or v=="true"
def document(root,name):return json.loads((root/I/name).read_text(encoding="utf-8"))
def hashes(s):return {x for x in s.split(";") if x}
def same_set(a,b):return hashes(a)==hashes(b)

def source_geometry(root,case_rows,e_rows,f_rows):
    # Read the complete compressed source geometry/UV population, not only
    # previously summarized totals. Reuse independent audit of exact old keys.
    apps=rows(root/B/"APPLICATIONS.csv")
    elements=rows(root/B/"ELEMENTS.csv")
    faces=rows(root/B/"FACES.csv.xz")
    animation=rows(root/B/"ANIMATION_FRAMES.csv.xz")
    check((len(apps),len(elements),len(faces),len(animation))==(74,390,1844,109),"source population drift")
    appkey=lambda r:(r["case"],r["rule_index"],r["option_index"])
    facekey=lambda r:appkey(r)+(r["element_index"],r["direction"])
    appmap={appkey(r):r for r in apps}
    check(len(appmap)==74 and len({facekey(r) for r in faces})==1844,"duplicate source key")
    check({a["case"] for a in apps}==HIST,"missing historical case")
    facegroups=defaultdict(list)
    elem_counts=Counter(appkey(r) for r in elements)
    face_counts=Counter(appkey(r) for r in faces)
    for a in apps:
        k=appkey(a)
        check(int(a["elements"])==elem_counts[k] and int(a["faces"])==face_counts[k],"geometry count mismatch "+str(k))
        for key in ("state_path","state_sha","model_path","model_sha"):
            check(bool(a[key]),"missing source path/hash "+str(k))
        if int(a["faces"]):
            check(a["provider_path"] and a["provider_sha"],"missing geometry parent "+str(k))
    for r in faces:
        check(appkey(r) in appmap and r["status"] in {"STATIC_RECT","ANIMATED_FRAME_RECTS","ZERO_UV_AREA"},"unclassified UV")
        check(r["uv"] and r["uv_method"] in ("DEFAULT","EXPLICIT") and r["png_sha"],"incomplete UV/texture source")
        check(bool(re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}",r["png_sha"])),"invalid PNG hash")
        facegroups[r["case"]].append(r)
    summary={}
    for id in sorted(HIST):
        c,e,f=case_rows[id],e_rows[id],f_rows[id]
        check(c["cohort"]==e["cohort"]==f["cohort"] and c["minecraft"]==e["minecraft"]==f["minecraft_version"] and c["block"]==e["block"]==f["block"],"case identity mismatch "+id)
        af=[a for a in apps if a["case"]==id]
        count=Counter(r["status"] for r in facegroups[id])
        check(count==json.loads(c["status_counts"]),"face status mismatch "+id)
        check(len(af)==int(c["applications"])==int(e["crosschecked_application_rows"])==int(f["original_source_applications"]),"app count "+id)
        check(sum(int(a["elements"]) for a in af)==int(c["elements"])==int(e["crosschecked_application_elements"]),"element count "+id)
        check(sum(count.values())==int(c["faces"])==int(e["crosschecked_application_faces"])==int(f["original_source_faces"]),"face count "+id)
        check(int(e["int4_c_exception_affected_applications"])==0,"source C exception unclassified "+id)
        check(int(c["faces_measured"])+count["ZERO_UV_AREA"]==int(c["faces"]),"incomplete source pixels "+id)
        summary[id]={"applications":len(af),"elements":int(c["elements"]),"faces":int(c["faces"]),"measured":int(c["faces_measured"]),"zero_uv":count["ZERO_UV_AREA"],"animated":count["ANIMATED_FRAME_RECTS"],"source_keys":af}
    return summary

def choose_historical(id,f,geometry,f4,correct,external,h10,h19,h17):
    tag=f["source_state_and_release_assessment"]
    cohort=f["cohort"]
    if geometry["faces"]==0:
        check(id=="V11" and h19["registration"]["bootstrap_constructor_method_handle_verified"] and not h19["exact_model_geometry_and_per_face_UV_extracted"],"unexpected special geometry state")
        return HOLD,"H19 special BedRenderer registration proven; actual renderer head/foot geometry and UV still missing","H19;F11D","Extract actual BedRenderer model parts and UV; compare native F2."
    if cohort=="AF":
        extra=""
        if id in ("S20","S21"):
            check(h17["differential_source"]["changed_texture_slot"]=="front" and h17["native_F2_reference"]["changed_screen_pixels_rgb24"]==1208,"H17 drift")
            extra=" H17 official 4.0.2 front-face UV and F2 difference proven; entire 4.0.3 study comparison not established."
        return COND,"Research Git 4.0.3 versus release Fabric 4.0.2: do not merge different source model/texture versions."+extra,"F11F;H17" if extra else "F11F","Compare selected release model/parents, texture bindings and source UV against pinned study; or make separate release-specific record."
    if id in ("S33","S47"):
        r=f4["cases"][id]
        check(r["server_exact_requested_state"] and r["source_model_selector_matches_game_JAR"] and all(r["research_release_state_model_parent_byte_equality"].values()) and r["native_png_sha256"] in hashes(f["image_sha256s"]),"F4 exact byte evidence changed")
        return OK,"Source state/model/provider byte match and recorded exact F2; UV rectangles are source-level.","F4;E;B;H97",""
    if id=="S22":
        a=geometry["source_keys"][0]
        check(external["HC_state_and_leaf_match_pinned_study"] and external["real_client_game_state_and_F2_recorded"] and correct["inherited_parent_world_fields_stable"] and correct["recorded_original_parent_SHA"]==a["provider_sha"]==correct["official_1_21_1_parent_file_SHA256"]==correct["official_1_21_11_parent_file_SHA256"],"S22 external parent not corrected")
        return OK,"Original provider hash label corrected to SHA256; world geometry parent bytes match; item display excluded.","F7;F8;E;B;H97",""
    if id=="S37":
        m=h10["source_reproduction"]["models"]["false"]
        a=geometry["source_keys"][0]
        check(m["runtime_leaf_JSON_equal"] and m["runtime_parent_JSON_equal"] and m["model_git_sha1"]==a["model_sha"] and m["parent_git_sha1"]==a["provider_sha"] and (m["elements"],m["faces"])==(geometry["elements"],geometry["faces"]) and h10["screen_ROI_changed_pixels"]["occupied_false_vs_air"]>0,"H10 foot identity drift")
        return OK,"H10 new pinned occupied=false foot F2 with exact original model and parent; original source UV verified; head not covered.","H10;E;B;H97",""
    exact=(
      cohort=="VANILLA" and tag in {
        "OFFICIAL_12111_MODEL_PARENT_BLOCKSTATE_GIT_BLOB_SHA1_MATCH",
        "OFFICIAL_VANILLA_12111_12_MULTIPART_MODEL_LEAF_PROVIDER_SERVER_EXACT",
        "PINNED_MOJANG_12111_SOURCE_BLOCKSTATE_SELECTED_MODEL_GEOMETRY_AND_GAME_F2"
      } or cohort=="HC" and tag in {
        "HC_RESEARCH_AND_FABRIC_RELEASE_SOURCE_SHA_MATCH",
        "HC_4_0_3_SOURCE_STATE_MODEL_PROVIDER_GIT_BYTES_EQUAL_RELEASE",
        "HC_STUDY_SOURCE_4_0_3_RELEASE_BYTE_EQUAL_SERVER_CAUSAL_CONDITION_PASS"
      } or cohort=="MACAW" and tag in {
        "MACAW_3_4_2_RELEASE_JAR_MODEL_PROVIDER_STATE_SHA256_MATCH_ORIGINAL_GAME",
        "MACAW_3_4_2_EXACT_SOURCE_STATE_RELEASE_PARENT_MODEL_SHA256_AND_ORIGINAL_F2_MATCH"
      })
    if exact:
        return OK,"Pinned selected source model/state/provider match and native F2 observation; source UV only (not baked GPU mapping).","F11F;E;B;H97",""
    return COND,"Historical F2 reuse is traceable, but selected source/runtime model/provider identity not independently established for this case.","F11F;H97;E;B","Reconcile the existing game manifest and exact selected runtime model/parent; rerun only if original evidence cannot resolve it."

def risk_decisions(root,stages,reviewed,geometry):
    g=defaultdict(list)
    for r in stages:
        check(truth(r["source_stage_state_verified"]) and not truth(r["full_risk_contract_approved"]) and len(r["source_PNG_sha256"])==64,"risk stage drift")
        g[r["risk_id"]].append(r)
    check({k:len(v) for k,v in g.items()}=={"R01":1,"R02":6,"R03":3,"R04":2,"R05":5,"R07":4},"risk stage population changed")
    r8=document(root,"INT4_F11F_R08_TWO_FABRIC_ORIGINAL_F2_INDEPENDENT_AUDIT_V1.json")
    r6=document(root,"INT4_F11E_R06_TEMPORAL_ORIGINAL_F2_INDEPENDENT_AUDIT_V1.json")
    gui=document(root,"INT4_H8_R03_ACTUAL_PLAYER_ITEM_SERVER_SHA_RESULT_V1.json")
    h10=document(root,"INT4_H10_OCCUPIED_FOOT_REAL_CLIENT_SOURCE_AUDIT_V1.json")
    u10=document(root,"INT4_H10_OCCUPIED_SINGLE_FOOT_FACE_UV_SOURCE_AUDIT_V1.json")
    check(reviewed["S10"]["modeling_status"]==OK,"R01 representative not approved")
    check({r["source_stage"] for r in g["R02"]}=={"AFV3_north","AFV3_east","AFV3_south","AFV3_west","AFV1_north","AFV1_south"},"R02 exact states missing")
    r02={r["source_stage"]:r for r in g["R02"]}
    for r in g["R07"]:
        check(r["source_PNG_sha256"]==r02[r["source_stage"]]["source_PNG_sha256"],"R07 not shared source")
    check("SELECTS_ACACIA_1" in r02["AFV3_south"]["archived_real_server_state_proof"] and all("SELECTS_ACACIA_3" in r02["AFV3_"+d]["archived_real_server_state_proof"] for d in ("north","east","west")),"AF selector asymmetry changed")
    check(gui["scope"]["player_creative_GUI_item_placement_verified"] and gui["neighbor_transition_observation"]["joined_bidirectionally"] and gui["neighbor_transition_observation"]["automatically_disconnected_after_remove"],"R03 transition evidence changed")
    check(geometry["S42"]["faces"]==55 and geometry["S43"]["faces"]==56 and geometry["S43"]["animated"]==1 and len(g["R04"])==2,"R04 state/face evidence changed")
    check(len({r["original_run_id"] for r in g["R05"]})==2 and h10["screen_ROI_changed_pixels"]["occupied_false_vs_true"]==2097 and u10["face_counts"]["changed_face_UV_records"]==24,"R05 model/visual evidence changed")
    check(r6["real_server_state_checks"]==3 and r6["direct_original_F2_pixel_review"]["water_pixel_changed_observed"] and not r6["water_animation_causally_approved"],"R06 temporal boundary changed")
    check(r8["official_4_0_3_NeoForge_not_tested"] and all(x["actual_server_PASS"] for x in r8["versions"].values()) and len({x["native_F2_SHA256"] for x in r8["versions"].values()})==1,"R08 narrow comparison drift")
    return {
       "R01":(RISK_OK,"Representative S10 only: source state and native F2 accepted.","H7;S10",""),
       "R02":(RISK_OK,"Six exact selectors and screenshots; release difference explicitly recorded, not geometry equivalence.","H7;F11F;R07",""),
       "R03":(RISK_OK,"Three-state directional connection/disconnection observed; H8 creative GUI supplement; no model-wide UV approval.","H7;H8",""),
       "R04":(RISK_OK,"Two static water states observed; historical source 55/56 faces distinguished; release linkage of S42/S43 remains separate.","H7;B",""),
       "R05":(RISK_OK,"Selected occupied foot model difference (24 changed face records and 2097 screen pixels); old two-run lifecycle explicitly separate.","H7;H9;H10",""),
       "R06":(RISK_COND,"Three exact sampled frames show 22/9/8 water-region pixel differences; animation origin not established.","F11E;H97","Trace selected water face/animation source; use narrowly controlled timing only if source insufficient."),
       "R07":(RISK_OK,"Four selectors: south variant3 selects acacia_1, others acacia_3; shared R02 F2, no author-intent claim.","H7;R02",""),
       "R08":(RISK_OK,"Only north variant1 Fabric 4.0.2 vs study-built Fabric 4.0.3: same F2, differing source SHA, not whole version equality.","F11F",""),
    }

def audit(root,out):
    root=Path(root).resolve()
    resolved={}
    for p,expected in PINS.items():
        got=blob((root/p).read_bytes())
        check(expected is not None and got==expected,"pinned source drift "+p+" "+got)
        resolved[p]=got
    # The historic auditor checks animation keys and 1,610 mod face records
    # against the previous research archive, as well as each PNG pixel rectangle.
    run=subprocess.run([sys.executable,str(root/B/"audit_comparison.py")],cwd=root,capture_output=True,text=True)
    check(run.returncode==0,"historic independent source audit failed "+run.stderr[-500:])
    old_audit=json.loads(run.stdout)
    check(old_audit["status"]=="PASS" and old_audit["faces"]==1844,"historic source audit unexpected")
    f=index(rows(root/I/LEGACY),"target_id")
    targets=index(rows(root/I/"INT4_F_RENDER_TARGETS_V1.csv"),"target_id")
    g5=index(rows(root/I/G5),"target_id")
    h6=index(rows(root/I/"INT4_H6_70_CASE_LOG_STATE_PROVENANCE_V1.csv"),"target_id")
    h97=index(rows(root/I/"INT4_H03_H05_P0_P1_P2_70_CASE_NEW_ARCHIVE_REAUDIT_V1.csv"),"target_id")
    e=index(rows(root/I/"INT4_E_62_CASE_SOURCE_LINKS_V1.csv"),"case")
    c=index(rows(root/B/"CASES.csv"),"case")
    check(all(set(x)==HIST|RISKS for x in (f,targets,g5,h6,h97)) and set(c)==set(e)==HIST,"denominator drift")
    evidence=document(root,"INT4_H03_H05_P0_P1_P2_70_CASE_SOURCE_RECHECK_V1.json")
    check(evidence["fresh_archive_independent_evidence"]["case_original_file_linkage_verified"]==70 and evidence["fresh_archive_independent_evidence"]["original_F2_PNG_sha_decode_1024x684_checked"]==91,"prior artifact audit incomplete")
    geometry=source_geometry(root,c,e,f)
    f4=document(root,"INT4_F4_DIRECT_VISUAL_PARTIAL_ACCEPTANCE_SUMMARY_V1.json")
    correction=document(root,"INT4_F8_S22_HASH_ALGORITHM_CORRECTION_V1.json")
    external=document(root,"INT4_F7_S22_VANILLA_PARENT_EXTERNAL_EXCEPTION_V1.json")
    h10=document(root,"INT4_H10_OCCUPIED_FOOT_REAL_CLIENT_SOURCE_AUDIT_V1.json")
    h19=document(root,"INT4_H19_V11_BED_TYPE_RENDERER_REGISTRATION_RESULT_V1.json")
    h17=document(root,"INT4_H17_AF_DRAWER_ORIGINAL_PARENT_FACE_UV_TEXEL_RESEARCH_V1.json")
    result={}
    for id in sorted(f):
        a,b,d=f[id],h6[id],h97[id]
        check(a["target_kind"]==targets[id]["target_kind"] and a["original_acceptance_contract"]==targets[id]["acceptance_contract"],"legacy target contract drift "+id)
        check(a["final_disposition"].startswith("CONDITIONAL") and a["runtime_evidence_accepted_as_full_F_PASS"]=="false" and g5[id]["full_F_approved"]=="false" and d["full_F_final_approved"]=="false","legacy F gate must remain unchanged "+id)
        check(a["image_sha256s"] and a["image_run_ids"] and a["image_artifact_ids"] and a["human_observation_text"] and truth(b["ZIP_CRC_and_all_PNG_SHA_verified"]) and truth(b["whole_client_log_sha_matched_capture_report"]) and truth(d["historical_human_visual_qualitative_text_present"]),"source/F2 evidence missing "+id)
        check(all(d[k].startswith("PASS_FRESH_RUN_") for k in ("original_zip20_crc_sha_new_audit","actual_original_f2_91_png_sha_new_audit","actual_client_log21_sha_new_audit")),"prior fresh review missing "+id)
        geom=geometry.get(id)
        if geom:
            check(a["source_E_case_match"]=="PASS" and truth(d["source_case_manifest_exact_meta"]),"no precise source or state capture record "+id)
            status,reason,source,next_task=choose_historical(id,a,geom,f4,correction,external,h10,h19,h17)
        else:status,reason,source,next_task="PENDING_RISK","","",""
        result[id]=dict(target_id=id,unit_kind=a["target_kind"],cohort=a["cohort"],minecraft_version=a["minecraft_version"],block=a["block"],
          source_applications=geom["applications"] if geom else "",source_elements=geom["elements"] if geom else "",source_faces=geom["faces"] if geom else "",
          source_uv_measured_faces=geom["measured"] if geom else "",documented_zero_uv_faces=geom["zero_uv"] if geom else "",animated_source_faces=geom["animated"] if geom else "",
          modeling_status=status,reason=reason,evidence_refs=source,next_required=next_task,
          original_f2_run_ids=a["image_run_ids"],original_f2_sha256s=a["image_sha256s"],legacy_disposition=a["final_disposition"],legacy_unconditional_F="false",
          runtime_GPU_per_face_approved="false",INT5_meaning_approved="false",INT6_rights_approved="false",new_game_or_F2="false")
    for id,(status,reason,source,next_task) in risk_decisions(root,rows(root/I/"INT4_H7_21_RISK_SUBSTAGE_SOURCE_VERIFIED_V1.csv"),result,geometry).items():
        result[id].update(modeling_status=status,reason=reason,evidence_refs=source,next_required=next_task)
    model_counts=Counter(result[id]["modeling_status"] for id in HIST)
    risk_counts=Counter(result[id]["modeling_status"] for id in RISKS)
    check(sum(model_counts.values())==62 and sum(risk_counts.values())==8,"new denominator changed")
    out=Path(out)
    out.mkdir(parents=True,exist_ok=True)
    rr=list(result.values())
    with (out/OUTPUT).open("w",encoding="utf-8",newline="") as w:
        writer=csv.DictWriter(w,fieldnames=list(rr[0]),lineterminator="\n")
        writer.writeheader()
        writer.writerows(rr)
    summary={
      "schema":"MCFR_INT4_F70_SEPARATE_MODELING_CONTRACT_V1",
      "source_parent":"60837ead604fb605d7cba32968b77de10249acd7",
      "legacy_F70":{"conditional":70,"unconditional":0,"H03":"HOLD","H05":"CONDITIONAL","INT5":0,"INT6":0},
      "historical_modeling":{"denominator":62,"counts":dict(model_counts),"pass_ids":sorted(id for id in HIST if result[id]["modeling_status"]==OK),"remaining_ids":sorted(id for id in HIST if result[id]["modeling_status"]!=OK)},
      "risk_question_scope":{"denominator":8,"counts":dict(risk_counts),"pass_ids":sorted(id for id in RISKS if result[id]["modeling_status"]==RISK_OK),"remaining_ids":sorted(id for id in RISKS if result[id]["modeling_status"]!=RISK_OK)},
      "combined_review_scope_only":{"denominator":70,"closed_units":model_counts[OK]+risk_counts[RISK_OK],"note":"Historical model evidence and narrow risk questions are heterogeneous; not legacy F PASS and not a uniform model count."},
      "reconciled_source":{"cases":62,"applications":74,"elements":390,"faces":1844,"animation_frame_rows":109,"prior_original_F2_records":91,"prior_original_zip_records":20,"prior_original_client_logs":21,"new_game_runs":0,"new_F2":0,"new_original_JAR_or_PNG_reads":0},
      "approval_scope":"Existing pinned source geometry/UV and native F2 observation, not fresh visual inspection, GPU baking, release texture byte equality, semantic or rights acceptance.",
      "frozen_source_git_blobs":resolved,
      "output_csv_sha256":hashlib.sha256((out/OUTPUT).read_bytes()).hexdigest()
    }
    (out/SUMMARY).write_text(json.dumps(summary,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({k:summary[k] for k in ("legacy_F70","historical_modeling","risk_question_scope","combined_review_scope_only","reconciled_source")},ensure_ascii=False,sort_keys=True))
    return summary

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--root",default=".")
    p.add_argument("--out",required=True)
    args=p.parse_args()
    audit(args.root,args.out)
