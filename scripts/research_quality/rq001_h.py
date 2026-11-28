#!/usr/bin/env python3
"""RQ001 H: conservative per-path classification, not a semantic certification."""
import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import re
from rq001_d import load_scope, pack, atomic, sha, blob

DIR="project/audits/research_quality/RQ001"

def historical_path(path):
    parts=path.split("/")
    if len(parts)<4 or parts[0]!="research":
        return False
    if parts[1] in ("vanilla_models","furniture_mods"):
        version=parts[2]
    elif parts[1]=="vanilla_textures" and "_" in parts[2]:
        version=parts[2].split("_",1)[0]
    else:
        return False
    return version.startswith("v") and version[1:].isascii() and version[1:].isdigit()

def main():
    ap=argparse.ArgumentParser()
    for name in ("repo","inputs","out"):
        ap.add_argument("--"+name,type=Path,required=True)
    a=ap.parse_args()
    repo,inputs,out=a.repo.resolve(),a.inputs.resolve(),a.out.resolve()
    assert not out.is_relative_to(repo)
    scope,rows,scope_sha=load_scope(repo)
    def permanent(name):
        return json.loads((repo/DIR/name).read_bytes())
    def artifact(gate,name):
        return (inputs/gate/name).read_bytes()
    d,e,f,g=[permanent(n) for n in ("D_FINAL_EVIDENCE.json","E_FINAL_EVIDENCE.json","F_FINAL_EVIDENCE.json","G_areas.json")]
    d_raw=artifact("D","D_files.jsonl")
    e_raw=artifact("E","E_databases.json")
    f_raw=artifact("F","F_assets.jsonl")
    assert sha(d_raw)==d["summaries"][-1]["ledger_sha256"]
    assert sha(e_raw)==e["summary"]["results_sha256"]
    assert sha(f_raw)==f["summary"]["ledger_sha256"]
    dr={x["path"]:x for x in map(json.loads,d_raw.splitlines())}
    er={x["path"]:x for x in json.loads(e_raw)}
    fr=defaultdict(list)
    for x in map(json.loads,f_raw.splitlines()):
        fr[x["evidence_path"]].append(x)
    assert len(dr)==len(rows)==3167 and len(er)==9 and sum(map(len,fr.values()))==25387
    # Independently re-read all explicitly mapped G evidence, including current
    # TV001/RQ001 evidence outside the original historical population.
    gmap=defaultdict(list)
    checked={}
    for area in g["areas"]:
        for ev in area["evidence"]:
            p=ev["path"]
            raw=(repo/p).read_bytes()
            assert blob(raw)==ev["git_blob"],p
            body=raw.decode("utf-8-sig")
            missing=[x for x in ev["fields"] if x not in body]
            assert not missing,(p,missing)
            checked[p]=ev["git_blob"]
            gmap[p].append({"area":area["id"],"type":ev["type"],"fields":ev["fields"],"boundary":ev["boundary"]})
    dup=defaultdict(list)
    for x in rows:
        dup[x["git_blob_sha1"]].append(x["path"])
    actual={k:sorted(v) for k,v in dup.items() if len(v)>1}
    declared={x["sha"]:sorted(x["paths"]) for x in permanent("duplicate_blob_candidates.json")["groups"]}
    assert actual==declared and len(actual)==7
    roles={
      "data/MC_Furniture_Style_Stage1_Research_v8.sqlite":"registered catalog legacy DB location",
      "research/vanilla_models/v8/MC_Furniture_Style_Stage1_Research_v8.sqlite":"historical v8 research location",
      "research/furniture_mods/phase_1-3/D/D_EXCEPTIONS.csv":"D-stage original exception ledger",
      "research/furniture_mods/phase_1-3/followup/D_EXCEPTION_RECHECK.csv":"follow-up exception recheck location",
      "research/vanilla_models/phase_1-2-A_completion/round2/A_CHECKPOINT_26_EVIDENCE_CROSSWALK.csv":"A-round2 crosswalk location",
      "research/vanilla_models/phase_1-2-A_completion/round2/A_CHECKPOINT_26_EVIDENCE_INDEX.csv":"A-round2 index location",
      "research/vanilla_models/phase_1-2-A_completion/round2/A_TO_BCDEFG_HANDOFF_QUEUE_2390.csv":"count-labelled handoff queue location",
      "research/vanilla_models/phase_1-2-A_completion/round2/A_TO_BCDEFG_HANDOFF_QUEUE.csv":"generic handoff queue location",
      "research/vanilla_models/v5/05_v4계승_150종_픽셀측정.csv":"v5 inherited measurement location",
      "research/vanilla_textures/v4_150/01_누적150종_픽셀측정.csv":"v4 texture measurement location",
      "research/vanilla_textures/by_stage/1-1-05/TEX05-R002/EDGE_RGBA_AUDIT.csv":"R002 edge audit location",
      "research/vanilla_textures/by_stage/1-1-05/TEX05-R002/SOURCE_LEDGER.csv":"R002 source ledger location",
      "research/vanilla_textures/v3_100/analyze_vanilla_100.py":"v3 analyzer location",
      "research/vanilla_textures/v4_150/analyze_vanilla_100.py":"v4 inherited analyzer location"}
    assert set(roles)=={p for v in actual.values() for p in v}
    mapped_paths=frozenset(gmap)
    records=[]
    for x in rows:
        p=x["path"]
        z=dr[p]
        assert z["actual_git_blob"]==x["git_blob_sha1"] and z["hash_status"]=="PASS"
        assert sha((repo/p).read_bytes())==z["actual_sha256"]
        rec={"path":p,"git_blob":x["git_blob_sha1"],"sha256":z["actual_sha256"],"format":x["format"],
             "group":x["group"],"file_status":z["status"],"format_status":z["format_status"],
             "semantic_status":"NOT_REVALIDATED","evidence_areas":gmap.get(p, []),
             "duplicate_candidate":p in roles,"preserve_original":True}
        # Verified source ledgers can be reused ONLY for source identity.
        if z["status"]!="PASS":
            c,reason="REVALIDATE",z.get("reason","file audit did not pass")
        elif p in roles:
            c,reason="DUPLICATE_CANDIDATE","identical pinned bytes; location role preserved, no deletion approval"
        elif p in fr:
            assert all(y["status"]=="PASS" for y in fr[p])
            c,reason="REUSABLE_LIMITED","F exact catalog/source identity evidence only"
            rec["source_assets_verified"]=len(fr[p])
        elif p in er:
            assert er[p]["status"]=="PASS"
            if re.search(r"/v[567]/",p) or "/entry04/" in p:
                c,reason="HISTORICAL","earlier historical DB snapshot; physical integrity only"
            else:
                c,reason="REUSABLE_LIMITED","E physical integrity and declared schema only; content not certified"
            rec["db_tables"]=er[p]["table_count"]
        elif p=="src/mcfr/research_schema.sql" or p=="registry/legacy-releases.json":
            c,reason="REUSABLE_LIMITED","F reproduced catalog v4 and exact release/source records; no schema redesign"
        elif p in mapped_paths:
            c,reason="REVALIDATE","G field/statement evidence mapped; semantic accuracy not revalidated"
        elif historical_path(p):
            c,reason="HISTORICAL","versioned historical snapshot candidate; preserve as prior evidence, not current truth"
        else:
            c,reason="REVALIDATE","file identity/format only; no sufficient specific reuse evidence"
        rec.update(classification=c,reason=reason)
        if p in roles:
            rec.update(duplicate_role=roles[p],duplicate_peers=[q for q in actual[x["git_blob_sha1"]] if q!=p])
        records.append(rec)
    assert frozenset(gmap)==mapped_paths, "evidence lookup must not mutate membership"
    expected_counts={"REVALIDATE":2268,"REUSABLE_LIMITED":11,"DUPLICATE_CANDIDATE":14,"HISTORICAL":874}
    actual_counts=dict(Counter(x["classification"] for x in records))
    assert actual_counts==expected_counts, (actual_counts,expected_counts)
    print("RQ001_H_POLICY_REGRESSION PASS",actual_counts,flush=True)
    raw=b"".join(pack(x) for x in records)
    atomic(out/"H_classification.jsonl",raw)
    summary={"gate":"6-H","status":"COMPLETE","expected":3167,"classified":len(records),
             "counts":dict(Counter(x["classification"] for x in records)),
             "duplicate_groups":len(actual),"duplicate_paths":len(roles),"verified_g_paths":len(checked),
             "verified_g_evidence":sum(len(x["evidence"]) for x in g["areas"]),
             "g_source_blobs":checked,"scope_sha256":scope_sha,"ledger_sha256":sha(raw),
             "code_sha256":sha(Path(__file__).read_bytes()),"limits":"Conservative path-level disposition, not per-row semantic certification. All original files preserved."}
    atomic(out/"H_summary.json",pack(summary))
    print("RQ001_H_SUMMARY "+json.dumps(summary,ensure_ascii=False),flush=True)

if __name__=="__main__":
    main()
