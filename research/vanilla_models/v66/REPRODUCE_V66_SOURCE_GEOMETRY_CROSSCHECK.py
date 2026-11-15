#!/usr/bin/env python3
"""v66 source/face/ledger audit replay in a FULL local Git repository checkout.
Saved for independent reproducibility; not executed in current connected GitHub mode.
Python standard library only.
"""
from pathlib import Path
import csv, io, hashlib, json

repo=Path(__file__).resolve().parents[3]
d=Path(__file__).resolve().parent
def original(path):
    return (repo/path).read_bytes()
def blobsha(b):
    return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def rows(path):
    return list(csv.DictReader(io.StringIO(original(path).decode("utf-8-sig"))))
def proof(name):
    return json.loads((d/name).read_text(encoding="utf-8"))
def same_old(old_path,new_path):
    before=rows(old_path);after=rows(new_path)
    assert len(before)==len(after)
    for prior,now in zip(before,after):
        for k,v in prior.items():
            assert now[k]==v,(old_path,k,prior.get("source_model"))
    return len(before)*len(before[0])

u=proof("00_V33_12_MODELS_148_IMPLICIT_UV_RECHECK.json")
assert u["rows_checked"]==148 and len(u["face_rows"])==148 and u["errors"]==[]
for m in u["original_source_models"]:
    assert blobsha(original(m["source_path"]))==m["original_model_git_sha"]
assert all(all(k==148 for k in u["checks_passed"].values()) for _ in [0])

s=proof("00_V38_OAK_SHELF_38_FACE_24_STATE_32_COMBINATIONS_RECHECK.json")
assert len(s["original_shelf_face_evidence"])==38
assert s["face_mismatches"]==[] and s["source_blockstate_rule_mismatches"]==[]
assert len(s["all_32_static_state_cases"])==32
assert all(x["rules"]==2 and x["unrotated_face_instances"]==16 for x in s["all_32_static_state_cases"])
for m in s["original_shelf_model_sources"]:
    assert blobsha(original(m["path"]))==m["sha"]
assert blobsha(original(s["original_blockstate"]["path"]))==s["original_blockstate"]["sha"]
assert blobsha(original(s["original_PNG_SHA_IHDR"]["path"]))==s["original_PNG_SHA_IHDR"]["sha"]

sum28=proof("00_DIRECT_SOURCE_PRIOR28_AGGREGATE.json")
assert sum28["new_unique_original_JSON_direct_review_flags"]==28
for source in sum28["source_batches"]:
    b=proof(Path(source["path"]).name)
    for m in b["models"]:
        assert blobsha(original(m["source_path"]))==m["git_blob_sha"]
assert same_old("research/vanilla_models/v65/07_P1_544_EVIDENCE_LEDGER.csv", "research/vanilla_models/v66/07_P1_544_EVIDENCE_LEDGER.csv")==544*337
assert same_old("research/vanilla_models/v65/04_SOURCE_REVIEW_LEDGER_544.csv","research/vanilla_models/v66/04_SOURCE_REVIEW_LEDGER_544.csv")==544*37
p=rows("research/vanilla_models/v66/07_P1_544_EVIDENCE_LEDGER.csv")
assert len(p)==544 and len(p[0])==351
assert sum(x["v66_new_direct_JSON_from_history_only_28"]=="true" for x in p)==28
assert sum(x["v66_cumulative_original_JSON_direct_recheck_flag_v35_v66"]=="true" for x in p)==544
assert len(rows("research/vanilla_models/v66/01_ORIGINAL_SOURCE_FACE_CROSSCHECK_186.csv"))==186
print("PASS: original model JSON SHA, v33 148 implicit face candidates, v38 38 source explicit faces/24 multipart/32 static states, old ledgers preserved.")
print("Not authenticated: official Minecraft renderer implicit UV, UVLOCK, visible world faces, full PNG RGBA this round.")
