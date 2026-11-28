#!/usr/bin/env python3
"""RQ001 E: read-only deep inspection of nine pinned historical database paths."""
import argparse
import collections
import hashlib
import json
import lzma
from pathlib import Path
import sqlite3
import tempfile
from contextlib import closing

from rq001_d import atomic, blob, pack, sha, load_scope, LIMIT, Unjudgeable


def quote(name):
    return '"' + name.replace('"','""') + '"'


def hash_file(path):
    with path.open("rb") as f:
        return hashlib.file_digest(f,"sha256").hexdigest()


def unpack(source,dest):
    size=0
    with lzma.open(source,"rb") as inp,dest.open("wb") as out:
        while chunk:=inp.read(1024*1024):
            size+=len(chunk)
            if size>LIMIT:
                raise Unjudgeable("SQLite decompressed size exceeds 512 MiB")
            out.write(chunk)
    return size


def inspect_sqlite(path):
    uri=path.resolve().as_uri()+"?mode=ro&immutable=1"
    with closing(sqlite3.connect(uri,uri=True)) as db:
        db.row_factory=sqlite3.Row
        db.execute("PRAGMA query_only=ON")
        db.execute("PRAGMA trusted_schema=OFF")
        db.execute("PRAGMA foreign_keys=ON")
        integrity=[r[0] for r in db.execute("PRAGMA integrity_check")]
        fk_violations=[list(r) for r in db.execute("PRAGMA foreign_key_check")]
        schema=[dict(r) for r in db.execute("SELECT type,name,tbl_name,sql FROM sqlite_schema ORDER BY type,name")]
        tables=[]
        for s in schema:
            if s["type"]!="table" or s["name"].startswith("sqlite_"):
                continue
            name=s["name"]
            q=quote(name)
            columns=[dict(r) for r in db.execute("PRAGMA table_xinfo("+q+")")]
            fks=[dict(r) for r in db.execute("PRAGMA foreign_key_list("+q+")")]
            indexes=[]
            for r in db.execute("PRAGMA index_list("+q+")"):
                ix=dict(r)
                ix["columns"]=[dict(c) for c in db.execute("PRAGMA index_xinfo("+quote(ix["name"])+")")]
                indexes.append(ix)
            count=db.execute("SELECT count(*) FROM "+q).fetchone()[0]
            tables.append({"name":name,"row_count":count,"columns":columns,"foreign_keys":fks,"indexes":indexes,
                           "primary_key":[c["name"] for c in sorted(columns,key=lambda c:c["pk"]) if c["pk"]]})
        fk_count=sum(len(t["foreign_keys"]) for t in tables)
        return {"integrity_check":integrity,"foreign_key_check":fk_violations,
                "fk_declared_rows":fk_count,"fk_status":"FAIL" if fk_violations else "PASS" if fk_count else "NOT_APPLICABLE",
                "application_id":db.execute("PRAGMA application_id").fetchone()[0],
                "user_version":db.execute("PRAGMA user_version").fetchone()[0],
                "schema":schema,"tables":tables,"table_count":len(tables),
                "row_count_sum_nonunique":sum(t["row_count"] for t in tables)}


def inspect_path(repo, item, scratch):
    path=repo/item["path"]
    result={"path":item["path"],"expected_git_blob":item["sha"],"expected_bytes":item["bytes"],"status":"HOLD"}
    before=None
    try:
        if path.is_symlink() or not path.is_file() or not path.resolve().is_relative_to(repo):
            raise Unjudgeable("missing/nonregular/outside input")
        if path.stat().st_size!=item["bytes"]:
            result.update(status="FAIL",reason="source size mismatch")
            return result
        raw=path.read_bytes()
        before=sha(raw)
        result.update(original_sha256_before=before,actual_git_blob=blob(raw),actual_bytes=len(raw))
        if result["actual_git_blob"]!=item["sha"]:
            result.update(status="FAIL",reason="source Git blob mismatch")
            return result
        with tempfile.TemporaryDirectory(dir=scratch) as d:
            actual=Path(d)/"database.sqlite"
            if path.suffix==".xz":
                result["sqlite_bytes"]=unpack(path,actual)
            else:
                actual.write_bytes(raw)
                result["sqlite_bytes"]=len(raw)
            result["decoded_sha256"]=hash_file(actual)
            if actual.open("rb").read(16)!=b"SQLite format 3\0":
                raise ValueError("SQLite header invalid")
            result.update(inspect_sqlite(actual))
            result["status"]="PASS" if result["integrity_check"]==["ok"] and not result["foreign_key_check"] else "FAIL"
    except Unjudgeable as e:
        result["reason"]=str(e)
    except (sqlite3.DatabaseError,ValueError,lzma.LZMAError,EOFError) as e:
        result.update(status="FAIL",reason=f"{type(e).__name__}: {e}")
    except (OSError,MemoryError) as e:
        result["reason"]=f"{type(e).__name__}: {e}"
    finally:
        if before is not None:
            try:
                result["original_sha256_after"]=hash_file(path)
                result["original_unchanged"]=result["original_sha256_after"]==before
                if not result["original_unchanged"]:
                    result.update(status="FAIL",reason="source changed during inspection")
            except OSError as e:
                result.update(status="HOLD",reason="post-check source unavailable: "+str(e))
    return result


def selftest():
    with tempfile.TemporaryDirectory() as d:
        p=Path(d)/"sample.sqlite"
        with closing(sqlite3.connect(p)) as db:
            db.executescript("CREATE TABLE parent(id INTEGER PRIMARY KEY);CREATE TABLE child(id INTEGER PRIMARY KEY,pid INTEGER REFERENCES parent(id));INSERT INTO parent VALUES(1);INSERT INTO child VALUES(1,1);")
            db.commit()
        r=inspect_sqlite(p)
        assert r["integrity_check"]==["ok"] and r["fk_status"]=="PASS" and r["table_count"]==2
        assert r["row_count_sum_nonunique"]==2
        with closing(sqlite3.connect(p)) as db:
            db.execute("INSERT INTO child VALUES(2,99)")
            db.commit()
        assert inspect_sqlite(p)["fk_status"]=="FAIL"
        q=Path(d)/"no_fk.sqlite"
        with closing(sqlite3.connect(q)) as db:
            db.execute("CREATE TABLE t(x)")
            db.commit()
        assert inspect_sqlite(q)["fk_status"]=="NOT_APPLICABLE"
        compressed=Path(d)/"sample.sqlite.xz"
        compressed.write_bytes(lzma.compress(p.read_bytes()))
        target=Path(d)/"out.sqlite"
        assert unpack(compressed,target)==p.stat().st_size and hash_file(target)==hash_file(p)
    print("RQ001_E_SELFTEST PASS 4",flush=True)


def main():
    a=argparse.ArgumentParser()
    a.add_argument("--repo",type=Path,required=True)
    a.add_argument("--out",type=Path,required=True)
    opt=a.parse_args()
    repo=opt.repo.resolve()
    out=opt.out.resolve()
    assert not out.is_relative_to(repo)
    out.mkdir(parents=True,exist_ok=True)
    selftest()
    scope,rows,scope_sha=load_scope(repo)
    d=json.loads((repo/"project/audits/research_quality/RQ001/D_FINAL_EVIDENCE.json").read_bytes())
    assert d["execution_complete"] and d["summaries"][-1]["scope_sha256"]==scope_sha
    items=scope["sqlite"]
    assert len(items)==9 and len({i["sha"] for i in items})==8
    by_path={x["path"]:x for x in rows}
    assert all(by_path[i["path"]]["git_blob_sha1"]==i["sha"] and int(by_path[i["path"]]["bytes"])==i["bytes"] for i in items)
    results=[]
    for item in items:
        result=inspect_path(repo,item,out)
        results.append(result)
        print("RQ001_E_DATABASE "+json.dumps({k:v for k,v in result.items() if k not in ("schema","tables","foreign_key_check")},ensure_ascii=False),flush=True)
        print("RQ001_E_TABLES "+json.dumps({"path":result["path"],"tables":[{"name":t["name"],"rows":t["row_count"],"columns":len(t["columns"]),"pk":t["primary_key"],"fk":len(t["foreign_keys"])} for t in result.get("tables",[])]},ensure_ascii=False),flush=True)
    counts=dict(collections.Counter(x["status"] for x in results))
    data=pack(results)
    atomic(out/"E_databases.json",data)
    summary={"gate":"6-E","status":"FAIL" if counts.get("FAIL") else "HOLD" if counts.get("HOLD") else "PASS",
             "attempted":len(results),"expected":9,"unique_expected_blobs":8,"counts":counts,
             "scope_sha256":scope_sha,"code_sha256":sha(Path(__file__).read_bytes()),"results_sha256":sha(data),
             "unchanged":sum(x.get("original_unchanged") is True for x in results),
             "foreign_key_status":dict(collections.Counter(x.get("fk_status","UNKNOWN") for x in results)),
             "limits":"Physical SQLite integrity and declared FK only; no semantic row correctness or data migration."}
    atomic(out/"E_summary.json",pack(summary))
    print("RQ001_E_SUMMARY "+json.dumps(summary,ensure_ascii=False),flush=True)


if __name__=="__main__":
    main()
