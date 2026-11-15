#!/usr/bin/env python3
"""v69 standalone replay in a FULL checkout of this repository.
Saved for independent verification. Not executed in this connected GitHub-only analysis.
Python stdlib; verifies original Git blobs, exhaustive multipart rules and ledger old columns.
"""
from pathlib import Path
import hashlib, json, csv, io, struct, itertools
root=Path(__file__).resolve().parents[3]
folder=Path(__file__).resolve().parent
def raw(path): return (root/path).read_bytes()
def sha(b): return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def table(path): return list(csv.DictReader(io.StringIO(raw(path).decode("utf-8-sig"))))
source=json.loads((folder/"00_ORIGINAL_BREWING_7_MODELS_1_BLOCKSTATE.json").read_text())
models=source["original_models"]
assert len(models)==7
byname={}
for m in models:
    data=raw(m["path"])
    assert sha(data)==m["git_blob_sha"] and json.loads(data)==m["original_JSON"]
    byname["minecraft:block/"+Path(m["path"]).stem]=m
state=source["original_blockstate"]
data=raw(state["path"])
assert sha(data)==state["git_blob_sha"] and json.loads(data)==state["original_JSON"]
rules=state["original_JSON"]["multipart"]
assert len(rules)==7
seen=set()
for bits in itertools.product((False,True),repeat=3):
    applies=[]
    for obj in rules:
        if "when" not in obj or all(str(bits[int(k[-1])]).lower()==v for k,v in obj["when"].items()):
            applies.append(obj["apply"]["model"])
    assert len(applies)==4 and len(set(applies))==4 and "minecraft:block/brewing_stand" in applies
    assert sum(len(byname[x]["original_JSON"]["elements"]) for x in applies)==7
    assert sum(sum(len(e["faces"]) for e in byname[x]["original_JSON"]["elements"]) for x in applies)==30
    seen.add(bits)
assert len(seen)==8
png=json.loads((folder/"00_BREWING_TWO_PNG_ORIGINAL_SHA_IHDR.json").read_text())
for p in png["source_PNG_files"]:
    b=raw(p["source_path"])
    assert sha(b)==p["git_blob_sha"]
    assert b[:8]==b"\x89PNG\r\n\x1a\n"
    assert struct.unpack(">II",b[16:24])==(16,16) and b[25]==3
p0=table("research/vanilla_models/v68/07_P1_544_EVIDENCE_LEDGER.csv")
p1=table("research/vanilla_models/v69/07_P1_544_EVIDENCE_LEDGER.csv")
r0=table("research/vanilla_models/v68/04_SOURCE_REVIEW_LEDGER_544.csv")
r1=table("research/vanilla_models/v69/04_SOURCE_REVIEW_LEDGER_544.csv")
for before,after,cols0,cols1 in [(p0,p1,379,393),(r0,r1,64,70)]:
    assert len(before)==len(after)==544 and len(before[0])==cols0 and len(after[0])==cols1
    for x,y in zip(before,after):
        for key,val in x.items(): assert y[key]==val,(key,x.get("source_path"))
print("PASS: seven original JSON, multipart 8 states, 36 unique faces, 240 applied face refs, 2 indexed PNG SHA/IHDR and preserved old ledger cells")
print("Note: no Minecraft client runtime/UVLOCK or actual pixel RGBA decoded during original v69 study")
