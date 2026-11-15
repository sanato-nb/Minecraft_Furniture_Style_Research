#!/usr/bin/env python3
"""Reproduce v67 source asset parent, face and blockstate checks in a complete Git checkout.
Python stdlib only. Saved as a reproducibility aid. NOT executed in the current GitHub connector round.
It does not execute or certify Minecraft client runtime renderers or full PNG RGBA decoding.
"""
from pathlib import Path
import csv,hashlib,io,json,struct

root=Path(__file__).resolve().parents[3]
folder=Path(__file__).resolve().parent
def data(p): return (root/p).read_bytes()
def gitsha(x): return hashlib.sha1(b"blob "+str(len(x)).encode()+b"\0"+x).hexdigest()
def readcsv(p): return list(csv.DictReader(io.StringIO(data(p).decode("utf-8-sig"))))
def js(p): return json.loads((folder/p).read_text(encoding="utf-8"))
def compare(old,new):
    assert len(old)==len(new)
    for a,b in zip(old,new):
        for c in old[0]:
            assert a[c]==b[c],(c,a.get("source_path"))

leaves=js("00_ORIGINAL_SOURCE_13_ZERO_OWN_LEAVES.json")["files"]
others=js("00_ORIGINAL_SOURCE_8_PARENTS_9_BLOCKSTATES.json")["files"]
inherit=js("00_INHERITANCE_AND_SOURCE_FACE_13.json")
pngs=js("00_PNG_9_ORIGINAL_SOURCE_SHA_IHDR.json")
assert len(leaves)==13 and len(others)==17
for item in leaves+others:
    body=data(item["full_source_path"])
    assert gitsha(body)==item["git_blob_sha"]
    assert json.loads(body)==item["original_JSON"]
assert len(inherit["source_faces"])==134
assert len(inherit["original_blockstate_target_variant_refs"])==23
assert len(inherit["models"])==13
assert sum(x["effective_source_face_reference_count"] for x in inherit["models"])==134
assert sum(x["source_implicitUV_face_count"] for x in inherit["models"])==6
assert sum(x["source_explicitUV_face_count"] for x in inherit["models"])==128
assert sum(x["geometry_source_path"] is None for x in inherit["models"])==5
for item in pngs["original_PNGs"]:
    body=data(item["full_source_path"])
    assert gitsha(body)==item["git_blob_sha"]
    assert body[:8]==b"\x89PNG\r\n\x1a\n"
    assert struct.unpack(">II",body[16:24])==(16,16)

old=readcsv("research/vanilla_models/v66/07_P1_544_EVIDENCE_LEDGER.csv")
new=readcsv("research/vanilla_models/v67/07_P1_544_EVIDENCE_LEDGER.csv")
assert len(old)==len(new)==544 and len(old[0])==351 and len(new[0])==365
compare(old,new)
s0=readcsv("research/vanilla_models/v66/04_SOURCE_REVIEW_LEDGER_544.csv")
s1=readcsv("research/vanilla_models/v67/04_SOURCE_REVIEW_LEDGER_544.csv")
assert len(s0)==len(s1)==544 and len(s0[0])==48 and len(s1[0])==56
compare(s0,s1)
print("v67 PASS: 13 original leaf JSON, 8 parents, 9 blockstates, 9 PNG SHA/IHDR, 134 face refs, 23 blockstate refs, 544x365 & review544x56 old cells preserved")
print("Not claimed: engine UV behavior, visual renderer geometry, full PNG RGBA, all P1 544 deep completion.")
