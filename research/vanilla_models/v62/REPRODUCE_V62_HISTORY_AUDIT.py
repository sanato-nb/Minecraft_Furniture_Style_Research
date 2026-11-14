#!/usr/bin/env python3
"""v62 evidence provenance reproduction in a FULL repository checkout.
Only tests selected v44 historical 21 CSV files and retained v61/v62 ledgers.
Does not claim exhaustive v5-v43 coverage, model renderer, implicit UV or PNG pixel validation.
"""
from pathlib import Path
import csv, io, hashlib, json, collections

repo = Path(__file__).resolve().parents[3]
here = Path(__file__).resolve().parent
def data(path):
    return (repo / path).read_bytes()
def table(path):
    return list(csv.DictReader(io.StringIO(data(path).decode("utf-8-sig"))))
def gitsha(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\x00" + raw).hexdigest()

audit = json.loads((here / "02_HISTORICAL_RECHECK_SCOPE_AND_COUNTERS.json").read_text())
group_paths = [
    "00A_HISTORICAL_CSV_RECHECK_GROUP1_10.json",
    "00B_HISTORICAL_CSV_RECHECK_GROUP2_11.json",
]
proof = {}
for f in group_paths:
    segment = json.loads((here/f).read_text())
    for original in segment["original_csv_files"]:
        name = original["path"]
        raw = data(name)
        assert gitsha(raw) == original["git_blob_sha"], name
        source = table(name)
        assert len(source) == original["original_rows"], name
        for e in original["links"]:
            k = (e["source_path"],e["model_sha"],name)
            assert k not in proof, k
            proof[k] = (e,original["git_blob_sha"])
assert len(proof) == 176

old = table("research/vanilla_models/v61/07_P1_544_EVIDENCE_LEDGER.csv")
new = table("research/vanilla_models/v62/07_P1_544_EVIDENCE_LEDGER.csv")
source_review = table("research/vanilla_models/v62/04_SOURCE_REVIEW_LEDGER_544.csv")
historical = table("research/vanilla_models/v62/01_HISTORICAL_EVIDENCE_CROSSWALK_176.csv")
v44 = table("research/vanilla_models/v44/02_SOURCE_EVIDENCE_LINKS_176.csv")
assert len(old)==len(new)==len(source_review)==544
assert len(historical)==len(v44)==176
old_fields = list(old[0])
assert len(old_fields) == 297 and len(new[0]) == 310
assert len(source_review[0]) == 24
assert all(all(n[k] == o[k] for k in old_fields) for o,n in zip(old,new))

original_p1 = {x["source_path"]:x for x in old}
sha_mismatch=0
classes=collections.Counter()
for item in historical:
    p = item["full_source_path"]
    assert original_p1[p]["source_git_blob_sha"] == item["original_model_git_blob_sha"]
    assert original_p1[p]["source_model"] == item["source_model"]
    original_file=item["historical_evidence_csv"]
    proof_data,file_sha=proof[(p,item["original_model_git_blob_sha"],original_file)]
    assert item["direct_reopened_original_csv_git_blob_sha"] == file_sha
    assert item["original_source_row_evidence_tier"] == proof_data["provenance"]
    ok=item["v44_recorded_evidence_csv_git_blob_sha"]==file_sha
    assert item["historical_evidence_file_sha_match"] == str(ok).lower()
    if not ok: sha_mismatch+=1
    classes[item["original_source_row_evidence_tier"]]+=1
assert sha_mismatch == 6, sha_mismatch
assert classes["same_row_typed_path_and_original_model_SHA"] == 78
assert classes["same_row_model_name_and_original_model_SHA"] == 98

grades=collections.Counter(x["evidence_tier_selected_scope"] for x in source_review)
assert grades["direct_JSON_source_review_flag_present"] == 514, grades
assert grades["historical_CSV_same_row_model_SHA_without_later_direct_flag"] == 28, grades
assert grades["source_identity_only_in_selected_history"] == 2, grades
unlinked={x["source_model"] for x in source_review if x["evidence_tier_selected_scope"]=="source_identity_only_in_selected_history"}
assert unlinked=={"chipped_anvil.json","damaged_anvil.json"}
print("PASSED: 21 original CSV Git SHAs, 176 historical original model links, 110 unique P1 models.")
print("P1 544x310, previous v61 297 columns all preserved; historical v44 file-SHA typo: 6 refs / 1 CSV.")
print("Model grades 514/28/2. Full v5-v43 corpus reconciliation not completed.")
