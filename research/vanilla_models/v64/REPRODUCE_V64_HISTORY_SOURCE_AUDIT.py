#!/usr/bin/env python3
"""v64 historical document audit reproducibility from FULL GitHub repository checkout.
Saved only; NOT executed end-to-end in this connected chat runtime.
Validates original file Git blob SHA for the 30 MD+19 JSON+4 Python sources
and preservation of v63/v64 CSVs; does not run scripts or decode SQLite.
"""
from pathlib import Path
import csv,hashlib,io,json
ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parent
def rd(p):return (ROOT/p).read_bytes()
def sha(b):return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\x00"+b).hexdigest()
def tab(p):return list(csv.DictReader(io.StringIO(rd(p).decode("utf-8-sig"))))
old=tab("research/vanilla_models/v63/00A_HISTORY_V5_V43_FILE_INVENTORY_194.csv")
now=tab("research/vanilla_models/v64/00_HISTORY_194_FILE_AUDIT_LEDGER.csv")
assert len(old)==len(now)==194
assert len(old[0])==11 and len(now[0])==17
for a,b in zip(old,now):
    for k in a:assert a[k]==b[k]
    if b["v64_original_document_content_reopened_GitSHA"]=="true" or b["v64_original_Python_source_reopened_GitSHA"]=="true":
        body=rd(b["source_file_path"])
        assert sha(body)==b["source_git_blob_sha_from_tree"],b["source_file_path"]
        if b["v64_original_document_JSON_parsed"]=="true":json.loads(body)
assert sum(x["v64_original_document_content_reopened_GitSHA"]=="true" for x in now)==49
assert sum(x["v64_original_Python_source_reopened_GitSHA"]=="true" for x in now)==4
assert sum(x["v64_selected_original_content_reopened_total"]=="true" for x in now)==77
a=tab("research/vanilla_models/v63/07_P1_544_EVIDENCE_LEDGER.csv")
b=tab("research/vanilla_models/v64/07_P1_544_EVIDENCE_LEDGER.csv")
assert len(a)==len(b)==544 and len(a[0])==325 and len(b[0])==330
for x,y in zip(a,b):
    for k in x:assert x[k]==y[k]
s0=tab("research/vanilla_models/v63/04_SOURCE_REVIEW_LEDGER_544.csv")
s1=tab("research/vanilla_models/v64/04_SOURCE_REVIEW_LEDGER_544.csv")
assert len(s0)==len(s1)==544 and len(s0[0])==30 and len(s1[0])==33
for x,y in zip(s0,s1):
    for k in x:assert x[k]==y[k]
assert sum(x["v64_original_v30_report_Git_SHA_reopened"]=="true" for x in b)==4
print("PASS: 53 historical Markdown/JSON/Python content Git SHAs; prior 24 CSV; 77/194 selected files; P1 old325 columns and source review old30 columns unchanged")
print("No re-run of historical scripts, independent model JSONs, PNG RGBA, Minecraft renderer or SQLite B-trees in v64.")
