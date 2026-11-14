#!/usr/bin/env python3
"""v65 source evidence audit reproducibility in a FULL repository checkout.
This script is supplied for independent execution, NOT claimed to have been run here.
Python stdlib only; will perform sqlite3 PRAGMA integrity_check if independently run.
"""
from pathlib import Path
import hashlib, io, csv, sqlite3, json

repo = Path(__file__).resolve().parents[3]
here = Path(__file__).resolve().parent
def raw(p):
    return (repo / p).read_bytes()
def blobsha(b):
    return hashlib.sha1(b"blob " + str(len(b)).encode() + b"\0" + b).hexdigest()
def csvfile(p):
    return list(csv.DictReader(io.StringIO(raw(p).decode("utf-8-sig"))))
def audit_legacy(old,new,col):
    assert len(old)==len(new), (len(old),len(new))
    for a,b in zip(old,new):
        for field in old[0]:
            assert a[field]==b[field], (field,a.get("source_path"))
    assert len(old[0])==col

files=csvfile("research/vanilla_models/v65/00_HISTORY_194_FILE_AUDIT_LEDGER.csv")
assert len(files)==194
counts={}
for r in files:
    path=r["source_file_path"]
    assert blobsha(raw(path))==r["source_git_blob_sha_from_tree"],path
    ext=r["file_extension"]
    counts[ext]=counts.get(ext,0)+1
    assert r["v65_original_source_file_content_reopened_cumulative"]=="true"
assert counts=={"csv":137,"md":30,"json":19,"sqlite":4,"py":4}

# All historical text CSVs can be opened/parsed and have expected column widths
for r in files:
    if r["file_extension"]!="csv":
        continue
    with io.StringIO(raw(r["source_file_path"]).decode("utf-8-sig")) as stream:
        table=list(csv.reader(stream))
    assert all(len(row)==len(table[0]) for row in table[1:]),r["source_file_path"]

# DB file readback; this independent runnable script uses real SQLite SQL engine.
static=json.loads((here/"00_SQLITE_4_ORIGINAL_STATIC_BTREE_AUDIT.json").read_text())
for item in static["db_files"]:
    path=repo / item["path"]
    assert blobsha(path.read_bytes())==item["git_blob_sha"]
    con=sqlite3.connect("file:"+str(path)+"?mode=ro",uri=True)
    assert con.execute("PRAGMA integrity_check").fetchone()[0]=="ok",path
    for t in item["table_contents"]:
        table=t["name"]
        safe=table.replace('"','""')
        n=con.execute('SELECT COUNT(*) FROM "'+safe+'"').fetchone()[0]
        assert n==t["btree"]["rows"],(table,n,t["btree"]["rows"])
    con.close()

old=csvfile("research/vanilla_models/v64/07_P1_544_EVIDENCE_LEDGER.csv")
now=csvfile("research/vanilla_models/v65/07_P1_544_EVIDENCE_LEDGER.csv")
assert len(old)==len(now)==544 and len(old[0])==330 and len(now[0])==337
audit_legacy(old,now,330)
s0=csvfile("research/vanilla_models/v64/04_SOURCE_REVIEW_LEDGER_544.csv")
s1=csvfile("research/vanilla_models/v65/04_SOURCE_REVIEW_LEDGER_544.csv")
assert len(s0)==len(s1)==544 and len(s0[0])==33 and len(s1[0])==37
audit_legacy(s0,s1,33)
h0=csvfile("research/vanilla_models/v64/00_HISTORY_194_FILE_AUDIT_LEDGER.csv")
h1=csvfile("research/vanilla_models/v65/00_HISTORY_194_FILE_AUDIT_LEDGER.csv")
assert len(h0)==len(h1)==194 and len(h0[0])==17 and len(h1[0])==26
audit_legacy(h0,h1,17)

w=csvfile("research/vanilla_models/v65/01_V65_NON_INVENTORY_ORIGINAL_SOURCE_SHA_WITNESSES_230.csv")
assert len(w)==230
assert len({x["full_source_path"] for x in w})==88
src={x["source_path"]:x for x in now}
for x in w:
    assert src[x["full_source_path"]]["source_git_blob_sha"]==x["original_model_git_blob_sha"]
print("PASS original SHA 194 historical sources; 113 new CSV; v65 model witness230 and prior ledgers preserved.")
print("Extra executable sqlite3 integrity_check and SELECT COUNT(*) performed by this independent replay, not by v65 GitHub static parser.")
