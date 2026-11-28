#!/usr/bin/env python3
"""RQ001 F: independently reconcile historical ledger and pinned source bytes."""
import argparse
from collections import Counter
from contextlib import closing, contextmanager
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import urllib.request
from zipfile import ZipFile, BadZipFile

from rq001_d import load_scope, pack, atomic, sha, blob
from mcfr import research_db as catalog, legacy_catalog as legacy, research_engine as engine


def git(root,*args):
    return subprocess.check_output(["git","-C",str(root),*args],stderr=subprocess.PIPE,timeout=240)


def tree(root,pin):
    result={}
    for record in git(root,"ls-tree","-rlz",pin).split(b"\0"):
        if not record:
            continue
        meta,path=record.split(b"\t",1)
        mode,kind,digest,size=meta.split()
        if kind==b"blob":
            result[path.decode("utf-8")]=(digest.decode(),int(size),mode.decode())
    return result


def direct_ledger(repo,scope,inventory):
    # Independent mapping from raw historical rows; no legacy importer for expected keys.
    expected={}
    sources=Counter()
    def add(code,path,kind,resource,alg,digest,size,evidence):
        k=(code,path)
        if k in expected:
            raise ValueError("duplicate raw ledger key: "+repr(k))
        catalog.relative_path(path)
        if alg not in ("GIT_BLOB_SHA1","SHA256") or len(digest)!=(40 if alg=="GIT_BLOB_SHA1" else 64) or any(c not in "0123456789abcdef" for c in digest):
            raise ValueError("invalid digest: "+repr(k))
        if evidence not in inventory:
            raise ValueError("unlocked evidence: "+evidence)
        expected[k]={"source_path":path,"kind":kind,"resource_id":resource,"hash_algorithm":alg,"digest":digest,"byte_count":size,"evidence_path":evidence}
        sources[evidence]+=1
    root="research/vanilla_models/phase_1-2-G/final/"
    p=root+"G_FINAL_SOURCE_SHA_4669.csv"
    for row in legacy.read_rows(repo,Path(p)):
        assert row["source_sha_match"]=="True"
        path=row["path"]
        kind={"BLOCK_MODEL_JSON":"model","BLOCKSTATE_JSON":"blockstate","BLOCK_TEXTURE_PNG":"texture"}[row["type"]]
        resource="minecraft:"+path.split("/assets/minecraft/",1)[1].split("/",1)[1].rsplit(".",1)[0]
        add("vanilla",path,kind,resource,"GIT_BLOB_SHA1",row["sha"],int(row["bytes"]),p)
    p=root+"G_FINAL_MCMETA_99.csv"
    for row in legacy.read_rows(repo,Path(p)):
        path=row["mcmeta_path"]
        resource="minecraft:"+path.split("/assets/minecraft/",1)[1].split("/",1)[1].removesuffix(".mcmeta").rsplit(".",1)[0]
        add("vanilla",path,"texture_sidecar",resource,"GIT_BLOB_SHA1",row["git_sha"],int(row["bytes"]),p)
    root="research/furniture_mods/phase_1-3/"
    for code in ("AF","HC","MACAW"):
        p=root+"B/source_verification/B_"+code+"_SOURCE_BODIES.csv.gz"
        alg="SHA256" if code=="MACAW" else "GIT_BLOB_SHA1"
        for row in legacy.read_rows(repo,Path(p)):
            assert row["mod_id"]==code
            add(code,row["path"],{"models":"model","blockstates":"blockstate","items":"item_definition"}[row["family"]],row["asset_id"],alg,row["sha"],int(row["bytes"]),p)
    p=root+"F/1-3_TEXTURE_UV_HANDOFF.csv"
    for row in legacy.read_rows(repo,Path(p)):
        if row["texture_status"]=="PINNED_MOD_PNG":
            add(row["source_id"],row["path"],"texture",row["resource_id"],row["source_hash_kind"],row["source_sha"],None,p)
    for p in sources:
        assert blob((repo/p).read_bytes())==inventory[p]["git_blob_sha1"],p
    assert len(expected)==25387
    assert Counter(k[0] for k in expected)=={r["code"]:r["expected_count"] for r in scope["releases"]}
    return expected,dict(sources)


def rebuild(repo,scope,rows,scratch):
    registry=json.loads((repo/"registry/legacy-releases.json").read_bytes())
    locked={r["code"]:{k:v for k,v in r.items() if k not in ("code","expected_count")} for r in scope["releases"]}
    assert registry==locked
    inventory={r["path"]:r for r in rows}
    expected,sources=direct_ledger(repo,scope,inventory)
    path=scratch/"catalog.sqlite"
    catalog.initialize(path)
    with closing(catalog.open_db(path,"rw")) as db:
        with catalog.write_transaction(db):
            first=legacy.import_catalog(db,repo,catalog.register_release)
        with catalog.write_transaction(db):
            second=legacy.import_catalog(db,repo,catalog.register_release)
        assert first["assets_added"]==25387 and second["assets_added"]==0
        assert db.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
        assert not db.execute("PRAGMA foreign_key_check").fetchall()
        code_by_key={r["release_key"]:r["code"] for r in scope["releases"]}
        actual={}
        for row in db.execute("SELECT * FROM asset ORDER BY release_key,source_path"):
            row=dict(row)
            key=(code_by_key[row.pop("release_key")],row["source_path"])
            assert key not in actual
            actual[key]=row
        assert actual==expected,"catalog differs from direct historical rows"
        release_rows={code_by_key[r["release_key"]]:dict(r) for r in db.execute("SELECT * FROM release")}
        assert release_rows==locked
        return actual,{"status":"PASS","schema":catalog.db_identity(db)[1],"first":first,"second":second,"direct_ledger_rows":len(expected),"duplicate_keys":0,"evidence_rows":sources,"releases":catalog.summary(db)["releases"],"catalog_vs_direct_ledger":"exact match"}


@contextmanager
def source_reader(repo,scratch,release,scope):
    code=release["code"]
    pin=release["pin_digest"]
    if code=="vanilla":
        # Historical tree and current main tree must agree; current checkout read separately.
        git(repo,"cat-file","-e",pin+"^{commit}")
        historical=tree(repo,pin)
        current=tree(repo,scope["main_pin"])
        def read(path):
            if path not in historical or path not in current:
                raise ValueError("missing path in historical or current pinned tree")
            if historical[path]!=current[path]:
                raise ValueError("historical vs main Git tree mismatch")
            p=repo/path
            if p.is_symlink() or not p.resolve().is_relative_to(repo) or historical[path][2] not in ("100644","100755"):
                raise ValueError("nonregular source path")
            body=p.read_bytes()
            if (blob(body),len(body))!=historical[path][:2]:
                raise ValueError("actual bytes differ from pinned tree")
            return body
        yield read,"historical_and_main_git_tree_and_body"
    elif code in ("AF","HC"):
        dest=scratch/code
        dest.mkdir()
        git(dest,"init","-q")
        git(dest,"-c","protocol.file.allow=never","fetch","--depth=1","--no-tags",release["source"],pin)
        git(dest,"checkout","--detach","FETCH_HEAD")
        if git(dest,"rev-parse","HEAD").decode().strip()!=pin:
            raise ValueError("fetched commit mismatch")
        t=tree(dest,pin)
        def read(path):
            p=dest/path
            if path not in t or t[path][2] not in ("100644","100755") or p.is_symlink() or not p.resolve().is_relative_to(dest):
                raise ValueError("missing or nonregular pinned Git member")
            body=p.read_bytes()
            if (blob(body),len(body))!=t[path][:2]:
                raise ValueError("Git tree/body mismatch")
            return body
        yield read,"pinned_git_commit_and_body"
    else:
        request=urllib.request.Request("https://api.modrinth.com/v2/version/xhmciaUD",headers={"User-Agent":"MCFR-RQ001 source-integrity audit"})
        with urllib.request.urlopen(request,timeout=60) as response:
            meta=json.load(response)
        if meta.get("id")!="xhmciaUD":
            raise ValueError("Modrinth version ID differs")
        # Modrinth often provides SHA512 and SHA1, not SHA256. Select exact filename
        # candidates for the fixed version, then verify the entire archive against lock.
        candidates=[f for f in meta.get("files",[]) if f.get("filename","").lower().endswith(".jar")]
        candidates=[f for f in candidates if f.get("hashes",{}).get("sha256",pin)==pin]
        candidates.sort(key=lambda f:not f.get("primary",False))
        if not candidates:
            raise FileNotFoundError("no matching pinned JAR candidate")
        path=scratch/"macaw.jar"
        matched=False
        for f in candidates:
            url=f["url"]
            if not url.startswith("https://"):
                raise ValueError("non-HTTPS JAR URL")
            total=0
            h=hashlib.sha256()
            req=urllib.request.Request(url,headers={"User-Agent":"MCFR-RQ001 source-integrity audit"})
            with urllib.request.urlopen(req,timeout=60) as stream,path.open("wb") as out:
                while chunk:=stream.read(1024*1024):
                    total+=len(chunk)
                    if total>512*1024*1024:
                        raise ValueError("JAR exceeds bounded size")
                    h.update(chunk)
                    out.write(chunk)
            if h.hexdigest()==pin:
                matched=True
                break
        if not matched:
            raise ValueError("no version file matches locked whole-JAR SHA256")
        with ZipFile(path) as z:
            names=z.namelist()
            if len(names)!=len(set(names)):
                raise ValueError("duplicate ZIP member path")
            yield z.read,"pinned_whole_jar_sha256_and_member"


def verify_one(row,read):
    record=dict(row)
    try:
        body=read(row["source_path"])
        record["actual_bytes"]=len(body)
        record["actual_digest"]=engine.asset_digest(body,row["hash_algorithm"])
        record["actual_sha256"]=sha(body)
        if record["actual_digest"]!=row["digest"] or (row["byte_count"] is not None and row["byte_count"]!=len(body)):
            raise ValueError("source digest or byte count mismatch")
        record["hash_status"]="PASS"
        # Existing verifier records independent basic format observations,
        # while the source identity result stays distinct.
        v=engine.verify_entry({**row,"reason":"RQ001 fixed historical source"},lambda _:body)
        record["basic_format_status"]=v["status"]
        if v["status"]=="PASS":
            record["observations"]=v["observations"]
            record["status"]="PASS"
        else:
            record.update(status="FAIL",reason=v.get("error","basic format failure"))
    except (ValueError,KeyError,FileNotFoundError,BadZipFile) as e:
        record.update(status="FAIL",hash_status=record.get("hash_status","FAIL"),reason=str(e))
    except OSError as e:
        record.update(status="HOLD",hash_status="HOLD",reason=str(e))
    return record


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo",type=Path,required=True)
    ap.add_argument("--out",type=Path,required=True)
    a=ap.parse_args()
    repo=a.repo.resolve()
    out=a.out.resolve()
    assert not out.is_relative_to(repo)
    out.mkdir(parents=True,exist_ok=True)
    scope,rows,scope_sha=load_scope(repo)
    assert json.loads((repo/"project/audits/research_quality/RQ001/E_FINAL_EVIDENCE.json").read_bytes())["summary"]["status"]=="PASS"
    with tempfile.TemporaryDirectory(dir=out) as tmp:
        scratch=Path(tmp)
        actual,cat=rebuild(repo,scope,rows,scratch)
        atomic(out/"F_catalog.json",pack(cat))
        print("RQ001_F_CATALOG "+json.dumps({k:v for k,v in cat.items() if k!="releases"},ensure_ascii=False),flush=True)
        allrows=[]
        results=[]
        for rel in scope["releases"]:
            code=rel["code"]
            entries=[row for (c,p),row in sorted(actual.items()) if c==code]
            assert len(entries)==rel["expected_count"]
            try:
                with source_reader(repo,scratch,rel,scope) as (read,pin_check):
                    records=[verify_one(row,read) for row in entries]
            except (subprocess.SubprocessError,OSError,ValueError,BadZipFile,KeyError) as e:
                # Missing access is HOLD. A confirmed mismatch to a fixed pin
                # or duplicate archive paths is FAIL, never silently substitute.
                status="FAIL" if isinstance(e,(ValueError,BadZipFile)) else "HOLD"
                pin_check=status
                records=[{**row,"status":status,"hash_status":"HOLD","reason":str(e)[:500]} for row in entries]
            for rec in records:
                rec["release_code"]=code
                rec["release_key"]=rel["release_key"]
                rec["pin_digest"]=rel["pin_digest"]
                rec["pin_check"]=pin_check
            data=b"".join(pack(x) for x in records)
            atomic(out/(code+"_assets.jsonl"),data)
            counts=dict(Counter(x["status"] for x in records))
            hcounts=dict(Counter(x["hash_status"] for x in records))
            summary={"code":code,"expected":len(entries),"rows":len(records),"attempted":sum("actual_digest" in x for x in records),
                     "counts":counts,"hash_counts":hcounts,"pin_check":pin_check,"ledger_sha256":sha(data),
                     "examples":[{"path":x["source_path"],"reason":x.get("reason")} for x in records if x["status"]!="PASS"][:8]}
            print("RQ001_F_RELEASE "+json.dumps(summary,ensure_ascii=False),flush=True)
            results.append(summary)
            allrows.extend(records)
        assert len(allrows)==25387 and len({(x["release_code"],x["source_path"]) for x in allrows})==25387
        data=b"".join(pack(x) for x in allrows)
        atomic(out/"F_assets.jsonl",data)
        counts=dict(Counter(x["status"] for x in allrows))
        hcounts=dict(Counter(x["hash_status"] for x in allrows))
        summary={"gate":"6-F","status":"FAIL" if counts.get("FAIL") else "HOLD" if counts.get("HOLD") else "PASS",
                 "expected":25387,"recorded":len(allrows),"body_attempted":sum("actual_digest" in x for x in allrows),
                 "catalog_status":cat["status"],"counts":counts,"hash_counts":hcounts,"releases":results,
                 "scope_sha256":scope_sha,"code_sha256":sha(Path(__file__).read_bytes()),"ledger_sha256":sha(data),
                 "limits":"Fixed registered source identities and basic format only; no full release coverage or semantic model analysis."}
        atomic(out/"F_summary.json",pack(summary))
        print("RQ001_F_SUMMARY "+json.dumps(summary,ensure_ascii=False),flush=True)


if __name__=="__main__":
    main()
