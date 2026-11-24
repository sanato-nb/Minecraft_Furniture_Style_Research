"""Reconcile H20's single V11 promotion without changing the legacy F ledger."""
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

from .int4_h18_v11_bed_renderer_bytecode import git_blob

I=Path("project/integration")
def require(ok,msg):
    if not ok: raise ValueError("H20_DELTA "+msg)

def load(name):return json.loads((I/name).read_text(encoding="utf-8"))
def rows(name):
    with (I/name).open(encoding="utf-8",newline="") as f:return list(csv.DictReader(f))

def main():
    s=load("INT4_F70_MODELING_CONTRACT_SUMMARY_V2.json")
    m=load("INT4_H20_V11_BED_MESH_UV_RESULT_V1.json")
    p=load("INT4_H20_V11_BED_POSE_MATERIAL_RESULT_V1.json")
    prior=rows("INT4_F70_MODELING_CONTRACT_CASE_REVIEW_V1.csv")
    new=rows("INT4_F70_MODELING_CONTRACT_CASE_REVIEW_V2.csv")
    for field,path in {
        "parent_modeling_summary_git_blob":"INT4_F70_MODELING_CONTRACT_SUMMARY_V1.json",
        "parent_modeling_csv_git_blob":"INT4_F70_MODELING_CONTRACT_CASE_REVIEW_V1.csv",
        "mesh_git_blob":"INT4_H20_V11_BED_MESH_UV_RESULT_V1.json",
        "pose_material_git_blob":"INT4_H20_V11_BED_POSE_MATERIAL_RESULT_V1.json",
    }.items():
        require(git_blob((I/path).read_bytes())==s[field],"source hash "+path)
    require(len(prior)==len(new)==len({r["target_id"] for r in new})==70,"case denominator")
    require([r["target_id"] for r in prior]==[r["target_id"] for r in new],"case order")
    changed=[(a,b) for a,b in zip(prior,new) if a!=b]
    require(len(changed)==1,"only V11 may change")
    a,b=changed[0]
    require(a["target_id"]==b["target_id"]=="V11" and a["modeling_status"]=="HOLD_MODELING" and b["modeling_status"]=="PASS_MODELING_SCOPE","V11 transition")
    require({k for k in a if a[k]!=b[k]}=={"modeling_status","reason","evidence_refs","next_required"},"legacy/ordinary field changed")
    require(b["source_faces"]=="0" and b["source_uv_measured_faces"]=="0","ordinary JSON counts preserved")
    require(m["counts"]=={"root_parts":2,"child_parts":6,"cubes":6,"polygons":36,"vertices":144} and m["isolated_original_JVM_model_bake"],"actual mesh evidence")
    require(p["source_mesh_git_blob"]==s["mesh_git_blob"] and m["source_pins"]==p["source_pins"] and p["modeling_V11_scope_evidence_complete"],"pose material evidence")
    require(p["material"]["resolved_png"]==m["texture"]["candidate_official_white_png_path"] and p["white_png_sha256"]==m["texture"]["sha256"],"white texture evidence")
    require(p["world_vertex_count"]==576 and p["north_foot_origin_head_z_minus_1"]==[0,0,-1,1,0.5625,1],"north bounds")
    require(all(r["legacy_unconditional_F"]==r["runtime_GPU_per_face_approved"]==r["INT5_meaning_approved"]==r["INT6_rights_approved"]=="false" for r in new),"old approvals changed")
    c=Counter(r["modeling_status"] for r in new)
    require(c=={"PASS_MODELING_SCOPE":34,"CONDITIONAL_MODELING":28,"PASS_RISK_QUESTION_SCOPE":7,"CONDITIONAL_RISK_QUESTION":1},"scope counts")
    require(s["historical_modeling"]=={"denominator":62,"pass":34,"conditional":28,"hold":0} and s["risk_questions"]=={"denominator":8,"pass":7,"conditional":1,"hold":0} and s["combined_review_scope_only"]=={"denominator":70,"closed_units":41,"conditional":29,"hold":0},"summary mismatch")
    require(s["legacy_F70"]=={"conditional":70,"unconditional":0,"H03":"HOLD","H05":"CONDITIONAL","INT5":0,"INT6":0},"legacy gate")
    require(p["new_game_runs"]==p["new_F2"]==s["new_game_runs"]==s["new_F2"]==0 and not p["live_renderer_call_during_old_F2_verified"] and not p["exact_GPU_pixel_causality"],"dynamic claims")
    print("H20_F70_V2_DELTA_VERIFIED_41_OF_70_ONLY_V11_PROMOTED")
if __name__=="__main__":main()
