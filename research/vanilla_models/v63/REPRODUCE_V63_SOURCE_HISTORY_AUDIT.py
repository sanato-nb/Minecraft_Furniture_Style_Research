#!/usr/bin/env python3
"""Re-run v63 source/history checks inside a FULL repository checkout.
Requires only Python stdlib. Does NOT decode full RGBA or authenticate Minecraft renderer.
This saved script has not been run end-to-end in the current connected GitHub session.
"""
from pathlib import Path
import hashlib, csv, io, json, collections, struct
repo=Path(__file__).resolve().parents[3]
d=Path(__file__).resolve().parent
def raw(path):
    return (repo/path).read_bytes()
def sha(b):
    return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def load(path):
    return list(csv.DictReader(io.StringIO(raw(path).decode("utf-8-sig"))))
def jsonfile(name):
    return json.loads((d/name).read_text(encoding="utf-8"))

m=jsonfile("00A_HISTORY_V5_V43_FILE_INVENTORY_SUMMARY.json")
manifest=load("research/vanilla_models/v63/00A_HISTORY_V5_V43_FILE_INVENTORY_194.csv")
assert len(manifest)==194 and m["original_subtree_git_blob_files"]==194
for item in manifest:
    assert sha(raw(item["source_file_path"]))==item["source_git_blob_sha_from_tree"], item["source_file_path"]
assert sum(x["v63_source_content_reopened_any"]=="true" for x in manifest)==24

a=jsonfile("00B_ORIGINAL_ANVIL_4_MODELS_3_BLOCKSTATES.json")
for item in a["models"]:
    b=raw(item["path"])
    assert sha(b)==item["sha"]
    assert json.loads(b)==item["original"]
for item in a["blockstates"]:
    b=raw(item["path"])
    assert sha(b)==item["sha"]
    assert json.loads(b)==item["original"]
parent=a["common_block_parent"]
b=raw(parent["path"])
assert sha(b)==parent["sha"] and json.loads(b)==parent["original"]

png=jsonfile("00C_ORIGINAL_ANVIL_PNG_4_IHDR_SHA.json")
for item in png["original_PNGs"]:
    b=raw(item["path"])
    assert sha(b)==item["sha"]
    assert b[:8]==b"\x89PNG\r\n\x1a\n"
    assert list(struct.unpack(">II",b[16:24]))==[16,16]

v30=jsonfile("00D_HISTORICAL_V30_SELECTED_CSV_4_ORIGINAL.json")
for item in v30["v30_historical_files"]:
    assert sha(raw(item["path"]))==item["git_sha"]
    assert raw(item["path"]).decode("utf-8")==item["original_text"]
old=load("research/vanilla_models/v62/07_P1_544_EVIDENCE_LEDGER.csv")
new=load("research/vanilla_models/v63/07_P1_544_EVIDENCE_LEDGER.csv")
assert len(old)==len(new)==544
assert len(old[0])==310 and len(new[0])==325
for x,y in zip(old,new):
    for k in old[0]:
        assert x[k]==y[k]
s0=load("research/vanilla_models/v62/04_SOURCE_REVIEW_LEDGER_544.csv")
s1=load("research/vanilla_models/v63/04_SOURCE_REVIEW_LEDGER_544.csv")
assert len(s0)==len(s1)==544 and len(s0[0])==24 and len(s1[0])==30
for x,y in zip(s0,s1):
    for k in s0[0]: assert x[k]==y[k]
h0=load("research/vanilla_models/v62/01_HISTORICAL_EVIDENCE_CROSSWALK_176.csv")
h1=load("research/vanilla_models/v63/01_HISTORICAL_EVIDENCE_CROSSWALK_179.csv")
assert len(h0)==176 and len(h1)==179
assert h1[:176]==h0
assert len({x["full_source_path"] for x in h1})==112
grade=collections.Counter(x["v63_updated_selected_proof_tier"] for x in s1)
assert grade["direct_JSON_source_review_flag_present_v35_v63"]==516,grade
assert grade["historical_CSV_same_row_model_SHA_without_direct_review_flag"]==28,grade
assert sum(x["v63_original_anvil_model_JSON_rechecked"]=="true" for x in s1)==4
assert sum(x["v63_new_v30_08_historical_model_source_SHA_row"]=="true" for x in s1)==3
print("PASS v63: 194 source tree sha; four model JSON; three blockstates; four PNG binary/IHDR; historical 179; P1 544x325, review 544x30; grades 516+28.")
print("NOT VERIFIED: Minecraft client engine render/UVLOCK, full PNG RGBA pixels, entire historical research semantic content.")
