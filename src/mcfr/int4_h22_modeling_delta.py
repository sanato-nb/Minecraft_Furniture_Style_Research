"""Independently reconcile H22 V4 against the unchanged V3 and original audit."""
from collections import Counter
from .int4_h22_hc_macaw12_original_source import IDS,HC,I,load,idx,req,h
def main():
    s=load("INT4_F70_MODELING_CONTRACT_SUMMARY_V4.json")
    d=load("INT4_H22_HC_MACAW12_SOURCE_RESULT_V1.json")
    old=idx(I/"INT4_F70_MODELING_CONTRACT_CASE_REVIEW_V3.csv","target_id")
    new=idx(I/"INT4_F70_MODELING_CONTRACT_CASE_REVIEW_V4.csv","target_id")
    for k,n in {"parent_modeling_summary_git_blob":"INT4_F70_MODELING_CONTRACT_SUMMARY_V3.json","parent_modeling_csv_git_blob":"INT4_F70_MODELING_CONTRACT_CASE_REVIEW_V3.csv","h22_source_result_git_blob":"INT4_H22_HC_MACAW12_SOURCE_RESULT_V1.json"}.items():
        req(s[k]==h.blob((I/n).read_bytes()),"delta source hash "+n)
    req(len(old)==len(new)==70 and list(old)==list(new),"unchanged scope and case order")
    req({k for k in old if old[k]!=new[k]}==IDS==set(s["changed_targets"])==set(d["cases"]),"delta exactly 12 historical cases")
    for k in IDS:
        a,b,c=old[k],new[k],d["cases"][k]
        req(a["modeling_status"]=="CONDITIONAL_MODELING" and b["modeling_status"]==c["modeling_status"]=="PASS_MODELING_SCOPE","scope promotion "+k)
        req({f for f in a if a[f]!=b[f]}=={"modeling_status","reason","evidence_refs","next_required"},"unrelated change "+k)
        req(c["cohort"]==a["cohort"] and c["all_selected_JSON_bytes_equal"] and c["all_selected_texture_bytes_equal"] and c["historical_uv_and_png_hash_faces_verified"]==int(a["source_faces"]),"source match "+k)
        req(c["existing_capture"]["F2_sha256"]==a["original_f2_sha256s"] and str(c["existing_capture"]["run"])==a["original_f2_run_ids"],"F2 provenance "+k)
    req((d["case_count"],d["applications"],d["elements"],d["faces"])==(12,12,77,311),"source census")
    req(d["face_status_counts"]=={"STATIC_RECT":286,"ZERO_UV_AREA":24,"ANIMATED_FRAME_RECTS":1},"face categories")
    req(all(a["raw_equal"] and a["equivalent"] for v in d["asset_comparisons"].values() for a in v.values()),"original asset comparison")
    req(Counter(r["modeling_status"] for r in new.values())=={"PASS_MODELING_SCOPE":62,"PASS_RISK_QUESTION_SCOPE":7,"CONDITIONAL_RISK_QUESTION":1},"V4 totals")
    req(new["R06"]==old["R06"] and not d["R06_temporal_causality_approved"],"R06 must remain conditional")
    req(s["historical_modeling"]=={"denominator":62,"pass":62,"conditional":0,"hold":0} and s["combined_review_scope_only"]=={"denominator":70,"closed_units":69,"conditional":1,"hold":0} and s["risk_questions"]=={"denominator":8,"pass":7,"conditional":1,"hold":0},"summary counts")
    req(s["legacy_F70"]=={"conditional":70,"unconditional":0,"H03":"HOLD","H05":"CONDITIONAL","INT5":0,"INT6":0},"legacy gate")
    req(all(r["legacy_unconditional_F"]==r["runtime_GPU_per_face_approved"]==r["INT5_meaning_approved"]==r["INT6_rights_approved"]=="false" for r in new.values()),"legacy row approvals")
    req(d["new_game_runs"]==d["new_F2"]==s["new_game_runs"]==s["new_F2"]==0,"new execution count")
    print("H22_V4_VERIFIED_62_OF_62_HISTORICAL_69_OF_70_SCOPED_R06_ONLY_REMAINS")
if __name__=="__main__":main()
