#!/usr/bin/env python3
"""v68 source evidence full-clone replay. Saved for independent execution; not executed in the current GitHub connector-only research session."""
from pathlib import Path
import csv, hashlib, io, json, struct
ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parent
def raw(path): return (ROOT / path).read_bytes()
def git_sha(b): return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def sheet(path): return list(csv.DictReader(io.StringIO(raw(path).decode("utf-8-sig"))))
s=json.loads((HERE/"00_CANDLE_4_LIT_LEAF_4_TEMPLATE_1_BLOCKSTATE_SOURCE.json").read_text())
for f in s["files"]:
    b=raw(f["source_path"])
    assert git_sha(b)==f["git_blob_sha"],f["source_path"]
    assert json.loads(b)==f["original_JSON"]
p=json.loads((HERE/"00_CANDLE_LIT_4_PARENT_100_FACE_AND_8_STATE_PROOF.json").read_text())
assert len(p["leaf_model_geometry"])==4
assert len(p["lit_applied_parent_face_instances"])==100
assert len(p["original_candle_blockstate_variants_all_eight"])==8
assert all(x["original_face_explicit_UV"] is not None for x in p["lit_applied_parent_face_instances"])
png=json.loads((HERE/"03_ORIGINAL_CANDLE_PNG_TWO_SHA_IHDR.json").read_text())
for f in png["original_PNGs"]:
    data=raw(f["path"]);assert git_sha(data)==f["sha"]
    assert data[:8]==b"\x89PNG\r\n\x1a\n"
    assert struct.unpack(">II",data[16:24])==(16,16)
old=sheet("research/vanilla_models/v67/07_P1_544_EVIDENCE_LEDGER.csv")
new=sheet("research/vanilla_models/v68/07_P1_544_EVIDENCE_LEDGER.csv")
rv0=sheet("research/vanilla_models/v67/04_SOURCE_REVIEW_LEDGER_544.csv")
rv1=sheet("research/vanilla_models/v68/04_SOURCE_REVIEW_LEDGER_544.csv")
for a,b,ocol,ncol in ((old,new,365,379),(rv0,rv1,56,64)):
    assert len(a)==len(b)==544 and len(a[0])==ocol and len(b[0])==ncol
    for x,y in zip(a,b):
        for k in a[0]:assert x[k]==y[k],k
print("PASS v68 original lit4 parent state8 source faces100, PNG SHA/IHDR2, preserved v67 old ledger cells")
print("Unverified: official client.jar runtime renderer; source third-party Java 2nd-party static references only")
