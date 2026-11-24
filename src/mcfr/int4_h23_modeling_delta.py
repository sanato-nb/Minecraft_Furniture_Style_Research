"""Promote R06 in the separate modeling contract only from a successful H23 control.

Historical F evidence, original F2 identities, and all prior approvals stay intact.
This script cannot produce V5 on an inconclusive experiment.
"""
import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path
from . import int4_h23_r06_animation_control as h
I=Path("project/integration")
V4CSV=I/"INT4_F70_MODELING_CONTRACT_CASE_REVIEW_V4.csv"
V4JSON=I/"INT4_F70_MODELING_CONTRACT_SUMMARY_V4.json"
REOPEN=I/"INT4_H23_R06_HISTORICAL_ORIGINAL_F2_REOPEN_V1.json"
def blob(p):
    b=p.read_bytes()
    return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def require(v,why):
    if not v: raise ValueError("H23 V5 "+why)
def load(p):return json.loads(p.read_text(encoding="utf-8"))
def main(source,out):
    d=load(source);old=load(V4JSON);prior=load(REOPEN)
    require(blob(V4CSV)=="1643a35581b7f62a41d2e9866bf2c99dbc2129a6" and blob(V4JSON)=="362ddca4c5b4207665e46ea173d1f6bdf117cfa9","prior V4 pin")
    require(d["schema"]=="MCFR_INT4_H23_R06_CONTROLLED_ANIMATION_METADATA_V1" and d["status"]=="PASS_R06_CONTROLLED_ANIMATION_SCOPE" and d["R06_animation_source_causal_scope"] is True,"inconclusive result cannot promote")
    require(d["source_H22_git_blob"]==prior["source_uv_and_animation"]["H22_original_source_git_blob"],"H22 evidence drift")
    require(d["new_game_runs"]==2 and d["new_F2"]==6 and d["legacy_F70_unconditional"]==d["INT5"]==d["INT6"]==0,"experiment and approvals")
    require(not d["old_F2_exact_frame_index_proven"] and not d["exact_GPU_texel_causality"],"overclaim")
    require(d["cross_session_stone_changed"]==d["cross_session_sink_nonwater_changed"]==0,"cross-session control drift")
    for mode in ("original","frozen"):
        q=d["sessions"][mode];p=q["intervention"];c=q["capture"]
        require(p["mode"]==mode and p["official_original_jar_sha256"]==h.k.MACAW_SHA256 and p["changed_members"]==([h.META] if mode=="frozen" else []),"intervention")
        require((p["runtime_jar_sha256"]!=h.k.MACAW_SHA256)==(mode=="frozen"),"runtime jar pin")
        require(p["source_frames"]==32 and p["distinct_source_uv_crops"]>1 and p["original_texture_sha256"]==h.PNG_SHA and p["original_mcmeta_sha256"]==h.META_SHA and p["selected_frame_indices"]==([0] if mode=="frozen" else list(range(32))),"source metadata")
        require(c["real_exact_server_state_checks"]==c["original_native_F2_count"]==3 and len(c["native_F2_sha256"])==3 and min(c["time_intervals_seconds"])>=8,"capture")
        diffs=list(q["pair_diffs"].values())
        require(len(diffs)==3 and all(x["water_changed"]==x["water_both_blue"] and x["sink_nonwater_changed"]==x["stone_changed"]==0 for x in diffs),"localized changes")
        require((sum(x["water_changed"]>0 for x in diffs)>=2) if mode=="original" else all(x["water_changed"]==0 for x in diffs),"animation control difference")
    with V4CSV.open(encoding="utf-8",newline="") as f:
        reader=csv.DictReader(f); fields=reader.fieldnames;rows=list(reader)
    require(len(rows)==len({r["target_id"] for r in rows})==70,"70 case denominator")
    require(Counter(r["modeling_status"] for r in rows)=={"PASS_MODELING_SCOPE":62,"PASS_RISK_QUESTION_SCOPE":7,"CONDITIONAL_RISK_QUESTION":1},"prior totals")
    for r in rows:
        require(all(r[k]=="false" for k in ("legacy_unconditional_F","runtime_GPU_per_face_approved","INT5_meaning_approved","INT6_rights_approved")),"legacy row approvals")
        if r["target_id"]=="R06":
            require(r["modeling_status"]=="CONDITIONAL_RISK_QUESTION" and r["original_f2_run_ids"]==str(prior["historical_run"]),"R06 prior")
            require(r["original_f2_sha256s"].split(";")==list(prior["actual_png_sha256"].values()),"old original F2 pins")
            r.update(modeling_status="PASS_RISK_QUESTION_SCOPE",reason="H23 original animated water vs frozen frame-zero controlled native F2 change; original metadata and selected UV verified; exact old frame index not claimed",evidence_refs="F11E;H22;H23",next_required="",new_game_or_F2="true")
    require(Counter(r["modeling_status"] for r in rows)=={"PASS_MODELING_SCOPE":62,"PASS_RISK_QUESTION_SCOPE":8},"V5 totals")
    out.mkdir(parents=True,exist_ok=True)
    with (out/"INT4_F70_MODELING_CONTRACT_CASE_REVIEW_V5.csv").open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields,lineterminator="\n");w.writeheader();w.writerows(rows)
    summary={"schema":"MCFR_INT4_F70_MODELING_CONTRACT_H23_DELTA_V5","parent_modeling_summary_git_blob":blob(V4JSON),"parent_modeling_csv_git_blob":blob(V4CSV),"h23_control_result_git_blob":blob(source),"changed_targets":["R06"],"historical_modeling":{"denominator":62,"pass":62,"conditional":0,"hold":0},"risk_questions":{"denominator":8,"pass":8,"conditional":0,"hold":0},"combined_review_scope_only":{"denominator":70,"closed_units":70,"conditional":0,"hold":0},"legacy_F70":old["legacy_F70"],"new_game_runs":2,"new_F2":6,"remaining_work":{"AF_release_comparison":0,"historical_runtime_source_identity":0,"R06_temporal_source":0},"scope":"Separate model and risk question research scope only. H23 intervention supports selected water animation origin; exact old frame, GPU, legacy F, INT5 and INT6 not approved."}
    require(summary["legacy_F70"]=={"conditional":70,"unconditional":0,"H03":"HOLD","H05":"CONDITIONAL","INT5":0,"INT6":0},"legacy gate")
    (out/"INT4_F70_MODELING_CONTRACT_SUMMARY_V5.json").write_text(json.dumps(summary,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print("H23_V5_R06_ONLY_70_OF_70_MODELING_SCOPE_NOT_LEGACY_F")
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--source",type=Path,required=True);p.add_argument("--output",type=Path,required=True)
    a=p.parse_args();main(a.source,a.output)
