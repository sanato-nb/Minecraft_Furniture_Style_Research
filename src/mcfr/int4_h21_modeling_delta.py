"""Validate the H21 single-cohort V2 -> V3 modeling ledger transition."""
import csv
import json
from pathlib import Path
from collections import Counter
from .int4_h21_af16_release_comparison import IDS,blob,req

I=Path("project/integration")
def load(name):return json.loads((I/name).read_text(encoding="utf-8"))
def rows(name):
    with (I/name).open(encoding="utf-8",newline="") as f:return list(csv.DictReader(f))
def main():
    s=load("INT4_F70_MODELING_CONTRACT_SUMMARY_V3.json")
    d=load("INT4_H21_AF16_RELEASE_SOURCE_UV_RESULT_V1.json")
    a=rows("INT4_F70_MODELING_CONTRACT_CASE_REVIEW_V2.csv")
    b=rows("INT4_F70_MODELING_CONTRACT_CASE_REVIEW_V3.csv")
    for k,n in {"parent_modeling_summary_git_blob":"INT4_F70_MODELING_CONTRACT_SUMMARY_V2.json","parent_modeling_csv_git_blob":"INT4_F70_MODELING_CONTRACT_CASE_REVIEW_V2.csv","af16_original_comparison_git_blob":"INT4_H21_AF16_RELEASE_SOURCE_UV_RESULT_V1.json"}.items():
        req(s[k]==blob((I/n).read_bytes()),"delta source hash "+n)
    req(len(a)==len(b)==len({r["target_id"] for r in b})==70,"denominator")
    req([r["target_id"] for r in a]==[r["target_id"] for r in b],"case order")
    changes=[(x,y) for x,y in zip(a,b) if x!=y]
    req(len(changes)==16 and {x["target_id"] for x,y in changes}==IDS==set(s["changed_targets"])==set(d["cases"]),"delta ID scope")
    for x,y in changes:
        id=x["target_id"];c=d["cases"][id]
        req(x["cohort"]==y["cohort"]=="AF" and x["modeling_status"]=="CONDITIONAL_MODELING" and y["modeling_status"]=="PASS_MODELING_SCOPE","AF transition")
        req({k for k in x if x[k]!=y[k]}=={"modeling_status","reason","evidence_refs","next_required"},"nonmodeling row changed "+id)
        req(c["modeling_status"]=="PASS_MODELING_SCOPE" and not c["issues"] and c["selected_options_equal"] and c["entire_blockstate_JSON_equal"] and c["existing_visual_evidence"]["existing_exact_capture_evidence"],"case evidence")
        req(c["existing_visual_evidence"]["existing_F2_sha256"]==x["original_f2_sha256s"] and c["existing_visual_evidence"]["existing_run"]==x["original_f2_run_ids"],"prior F2 identity")
        req(sum(z["historical_face_png_hash_and_uv_rows_verified"] for z in c["applications"])==int(x["source_faces"]),"face count")
        req(all(z["chain_json_equal"] and z["elements_equal"] and z["face_uv_bindings_equal"] for z in c["applications"]),"app structure")
    assets=list(d["asset_comparisons"].values())
    req(len(assets)==80 and all(z["equivalent"] for z in assets) and sum(z["raw_equal"] for z in assets)==40,"asset totals")
    req(sum(z["kind"]=="json" for z in assets)==41 and sum(z["kind"]=="png" and z["raw_equal"] for z in assets)==39,"JSON/PNG count")
    req((d["case_count"],d["application_count"],d["face_count"])==(16,21,535),"original evidence totals")
    req(Counter(y["modeling_status"] for y in b)=={"PASS_MODELING_SCOPE":50,"CONDITIONAL_MODELING":12,"PASS_RISK_QUESTION_SCOPE":7,"CONDITIONAL_RISK_QUESTION":1},"derived scope counts")
    req(s["historical_modeling"]=={"denominator":62,"pass":50,"conditional":12,"hold":0} and s["risk_questions"]=={"denominator":8,"pass":7,"conditional":1,"hold":0} and s["combined_review_scope_only"]=={"denominator":70,"closed_units":57,"conditional":13,"hold":0},"summary counts")
    req(all(y["legacy_unconditional_F"]==y["runtime_GPU_per_face_approved"]==y["INT5_meaning_approved"]==y["INT6_rights_approved"]=="false" for y in b),"legacy row changed")
    req(s["legacy_F70"]=={"conditional":70,"unconditional":0,"H03":"HOLD","H05":"CONDITIONAL","INT5":0,"INT6":0},"legacy gate")
    req(s["new_game_runs"]==s["new_F2"]==d["new_game_runs"]==d["new_F2"]==0,"new execution claim")
    print("H21_F70_V3_DELTA_VERIFIED_57_OF_70_ONLY_AF16_PROMOTED")
if __name__=="__main__":main()
