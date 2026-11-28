#!/usr/bin/env python3
"""Independent RQ001 I reconciliation against original artifact bytes and pinned tree."""
import argparse
from collections import Counter, defaultdict
import csv
import hashlib
import io
import json
from pathlib import Path
import subprocess

DIR="project/audits/research_quality/RQ001"
def sha(b): return hashlib.sha256(b).hexdigest()
def gitblob(b): return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def read(p): return json.loads(p.read_bytes())
def jsonl(b): return [json.loads(x) for x in b.splitlines()]
def counts(rows,key): return dict(Counter(r[key] for r in rows))
def main():
    ap=argparse.ArgumentParser()
    for n in ("repo","inputs","out"): ap.add_argument("--"+n,type=Path,required=True)
    a=ap.parse_args()
    repo,inputs,out=a.repo.resolve(),a.inputs.resolve(),a.out.resolve()
    folder=repo/DIR
    lock=read(folder/"scope_lock.json")
    scope_sha=sha((folder/"scope_lock.json").read_bytes())
    expected={}
    for inv in lock["inventory"]:
        raw=(repo/inv["path"]).read_bytes()
        assert gitblob(raw)==inv["git_blob"]
        rows=list(csv.DictReader(io.StringIO(raw.decode()),delimiter="\t"))
        assert len(rows)==inv["count"]
        for r in rows:
            assert r["path"] not in expected
            expected[r["path"]]=(r["git_blob_sha1"],int(r["bytes"]))
    assert len(expected)==3167
    tree=subprocess.check_output(["git","-C",str(repo),"ls-tree","-rlz",lock["main_pin"]])
    tree_index={}
    for line in tree.split(b"\0"):
        if line:
            meta,path=line.split(b"\t",1)
            mode,kind,digest,size=meta.split()
            path=path.decode()
            if kind==b"blob" and not path.startswith("1.21.11/"):
                tree_index[path]=(digest.decode(),int(size))
    assert expected==tree_index
    # Protect every historical path, including 28,163 source paths.
    diff=subprocess.check_output(["git","-C",str(repo),"diff","--name-status",lock["main_pin"],"HEAD"]).decode().splitlines()
    assert all(x.startswith("A\t") for x in diff),diff[:10]
    assert not subprocess.check_output(["git","-C",str(repo),"status","--porcelain","--untracked-files=no"])
    d=read(folder/"D_FINAL_EVIDENCE.json")
    e=read(folder/"E_FINAL_EVIDENCE.json")
    f=read(folder/"F_FINAL_EVIDENCE.json")
    g=read(folder/"G_areas.json")
    hs=read(out/"H_summary.json")
    ds=read(inputs/"D/D_summary.json")
    es=read(inputs/"E/E_summary.json")
    fs=read(inputs/"F/F_summary.json")
    assert all(x["scope_sha256"]==scope_sha for x in (ds,es,fs,hs))
    assert ds=={**d["summaries"][-1],"batches":ds["batches"]}
    assert es==e["summary"] and fs==f["summary"]
    for summary,name in ((ds,"rq001_d.py"),(es,"rq001_e.py"),(fs,"rq001_f.py"),(hs,"rq001_h.py")):
        assert sha((repo/"scripts/research_quality"/name).read_bytes())==summary["code_sha256"]
    dr=(inputs/"D/D_files.jsonl").read_bytes()
    er=(inputs/"E/E_databases.json").read_bytes()
    fr=(inputs/"F/F_assets.jsonl").read_bytes()
    hr=(out/"H_classification.jsonl").read_bytes()
    assert sha(dr)==ds["ledger_sha256"] and sha(er)==es["results_sha256"] and sha(fr)==fs["ledger_sha256"] and sha(hr)==hs["ledger_sha256"]
    dl,el,fl,hl=jsonl(dr),json.loads(er),jsonl(fr),jsonl(hr)
    assert len(dl)==len(hl)==3167 and len(el)==9 and len(fl)==25387
    assert len({x["path"] for x in dl})==len({x["path"] for x in hl})==3167
    assert {x["path"] for x in dl}=={x["path"] for x in hl}==set(expected)
    assert counts(dl,"status")==ds["counts"]=={"PASS":3165,"FAIL":2}
    assert counts(dl,"hash_status")=={"PASS":3167}
    batches=[]
    for n in range(1,17):
        p=inputs/"D/batches"/f"{n:02d}.jsonl"
        raw=p.read_bytes()
        cp=read(p.with_suffix(".checkpoint.json"))
        assert sha(raw)==cp["result_sha256"]==ds["batches"][n-1]["result_sha256"]
        assert cp["scope_sha256"]==scope_sha and cp["code_sha256"]==ds["code_sha256"]
        assert len(jsonl(raw))==cp["count"]==ds["batches"][n-1]["count"]==(167 if n==16 else 200)
        batches.append(raw)
    assert b"".join(batches)==dr
    failed={x["path"] for x in dl if x["status"]=="FAIL"}
    assert failed=={x["path"] for x in d["findings"]}
    edict={x["path"]:x for x in el}
    assert set(edict)=={x["path"] for x in lock["sqlite"]} and len({x["actual_git_blob"] for x in el})==8
    assert all(x["status"]=="PASS" and x["integrity_check"]==["ok"] and not x["foreign_key_check"] and x["original_unchanged"] for x in el)
    for item in lock["sqlite"]:
        x=edict[item["path"]]
        assert x["actual_git_blob"]==item["sha"] and x["actual_bytes"]==item["bytes"]
    assert len({(x["release_code"],x["source_path"]) for x in fl})==25387
    assert counts(fl,"release_code")=={x["code"]:x["expected_count"] for x in lock["releases"]}
    assert all(x["status"]==x["hash_status"]=="PASS" and x["actual_digest"]==x["digest"] and (x["byte_count"] is None or x["actual_bytes"]==x["byte_count"]) for x in fl)
    for item in lock["releases"]:
        code=item["code"]
        raw=(inputs/"F"/(code+"_assets.jsonl")).read_bytes()
        rs=next(x for x in fs["releases"] if x["code"]==code)
        assert sha(raw)==rs["ledger_sha256"]
        assert all(x["pin_digest"]==item["pin_digest"] for x in jsonl(raw))
        assert jsonl(raw)==[x for x in fl if x["release_code"]==code]
    cat=read(inputs/"F/F_catalog.json")
    assert cat["first"]["assets_added"]==25387 and cat["second"]["assets_added"]==0 and cat["duplicate_keys"]==0
    assert {k:v for k,v in cat.items() if k!="releases"}==f["catalog"]
    assert [x["id"] for x in g["areas"]]==list(range(1,15))
    assert counts(g["areas"],"coverage")==g["coverage_counts"]
    evidence={}
    for area in g["areas"]:
        for ev in area["evidence"]:
            raw=(repo/ev["path"]).read_bytes()
            assert gitblob(raw)==ev["git_blob"] and all(k in raw.decode("utf-8-sig") for k in ev["fields"])
            evidence[ev["path"]]=ev["git_blob"]
    assert evidence==hs["g_source_blobs"]
    duplicated=defaultdict(list)
    for p,(b,n) in expected.items(): duplicated[b].append(p)
    duplicate_paths={p for paths in duplicated.values() if len(paths)>1 for p in paths}
    assert len(duplicate_paths)==14 and sum(len(x)>1 for x in duplicated.values())==7
    assert {x["path"] for x in hl if x["duplicate_candidate"]}==duplicate_paths
    by_d={x["path"]:x for x in dl}
    for x in hl:
        p=x["path"]
        raw=(repo/p).read_bytes()
        assert (gitblob(raw),len(raw))==expected[p] and sha(raw)==x["sha256"]==by_d[p]["actual_sha256"]
        assert x["preserve_original"] and x["semantic_status"]=="NOT_REVALIDATED"
        assert x["file_status"]==by_d[p]["status"]
        if p in failed: assert x["classification"]=="REVALIDATE"
        if x["classification"]=="REUSABLE_LIMITED":
            assert p in edict or p in {q["evidence_path"] for q in fl} or p in ("src/mcfr/research_schema.sql","registry/legacy-releases.json")
    assert counts(hl,"classification")==hs["counts"]
    summary={"gate":"6-I","audit_execution":"PASS","quality_status":"FAIL","bounded_closure":"CLOSED_WITH_FINDINGS",
             "historical_files_preserved":True,"historical_paths_checked":3167,"original_tree_protected_by_git_diff":True,
             "batches":16,"db_paths":9,"registered_sources":25387,"areas":14,"g_sources_rechecked":len(evidence),
             "duplicate_groups":7,"duplicate_paths":14,"classified_paths":3167,"classification_counts":hs["counts"],
             "mandatory_failure":"6-D: 2 historical CSV format defects; do not promote to PASS",
             "scope_sha256":scope_sha,"D_ledger_sha256":sha(dr),"E_results_sha256":sha(er),"F_ledger_sha256":sha(fr),
             "H_ledger_sha256":sha(hr),"code_sha256":sha(Path(__file__).read_bytes()),
             "limits":"Reconciliation of actual prior artifacts, not rerun of all external source acquisition; no semantic accuracy certification."}
    (out/"I_summary.json").write_text(json.dumps(summary,ensure_ascii=False,sort_keys=True)+"\n")
    print("RQ001_I_SUMMARY "+json.dumps(summary,ensure_ascii=False),flush=True)
if __name__=="__main__": main()
