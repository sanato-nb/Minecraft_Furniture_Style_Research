#!/usr/bin/env python3
"""RQ-001 D: fixed-path byte and format audit; never modify research inputs."""
import argparse
import ast
import collections
import csv
import gzip
import hashlib
import io
import json
import lzma
import os
from pathlib import Path, PurePosixPath
import subprocess
import tempfile
import xml.etree.ElementTree as ET

from PIL import Image
import yaml

TEXT = {"md", "sql", "txt", "java", "sh", "js", "mcfunction", "gitignore", "log"}
LIMIT = 536870912
SCOPE = "project/audits/research_quality/RQ001/scope_lock.json"


class Unjudgeable(Exception):
    pass


def sha(b):
    return hashlib.sha256(b).hexdigest()


def blob(b):
    return hashlib.sha1(b"blob " + str(len(b)).encode() + b"\0" + b).hexdigest()


def pack(obj):
    return (json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()


def atomic(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as f:
        f.write(data)
        tmp = Path(f.name)
    os.replace(tmp, path)


def pairs(items):
    out = {}
    for k, v in items:
        if k in out:
            raise ValueError("duplicate JSON key: " + k)
        out[k] = v
    return out


def bad_const(s):
    raise ValueError("nonfinite JSON constant: " + s)


def json_check(s):
    return json.loads(s, object_pairs_hook=pairs, parse_constant=bad_const)


def decomp(data, kind):
    source = io.BytesIO(data)
    opener = gzip.GzipFile(fileobj=source, mode="rb") if kind == "gz" else lzma.LZMAFile(source, "rb")
    with opener as stream:
        out = bytearray()
        while chunk := stream.read(1024 * 1024):
            if len(out) + len(chunk) > LIMIT:
                raise Unjudgeable("decompressed size exceeds 512 MiB")
            out.extend(chunk)
    return out


def format_check(raw, kind):
    info = {"format": kind}
    if kind.endswith((".gz", ".xz")):
        kind, compression = kind.rsplit(".", 1)
        raw = decomp(raw, compression)
        info["decompressed_bytes"] = len(raw)
    if kind == "sqlite":
        if not raw.startswith(b"SQLite format 3\0") or len(raw) < 100:
            raise ValueError("invalid SQLite header")
        info["check"] = "header_only_deep_check_E"
    elif kind in ("png", "jpg"):
        expected = "PNG" if kind == "png" else "JPEG"
        with Image.open(io.BytesIO(raw)) as image:
            if image.format != expected:
                raise ValueError("image format mismatch")
            image.verify()
        with Image.open(io.BytesIO(raw)) as image:
            image.load()
            info.update(width=image.width, height=image.height, frames=getattr(image,"n_frames",1))
            for i in range(1, info["frames"]):
                image.seek(i)
                image.load()
        info["check"] = "Pillow_verify_and_decode"
    elif kind in {"json", "jsonl", "csv", "tsv", "svg", "yml", "py"} | TEXT:
        s = raw.decode("utf-8-sig", errors="strict")
        if "\0" in s:
            raise ValueError("NUL in text")
        if kind == "json":
            json_check(s)
            info["check"] = "strict_JSON"
        elif kind == "jsonl":
            n = 0
            for line_no, line in enumerate(s.splitlines(), 1):
                if line.strip():
                    try:
                        json_check(line)
                    except ValueError as e:
                        raise ValueError(f"JSONL line {line_no}: {e}") from e
                    n += 1
            info.update(check="strict_JSONL", records=n)
        elif kind in ("csv", "tsv"):
            csv.field_size_limit(32 * 1024 * 1024)
            reader = csv.reader(io.StringIO(s, newline=""), delimiter="," if kind == "csv" else "\t", strict=True)
            width = None
            n = 0
            anomalies = []
            for row in reader:
                if not row:
                    continue
                if width is None:
                    width = len(row)
                elif len(row) != width:
                    if len(anomalies) < 10:
                        anomalies.append([reader.line_num, len(row)])
                n += 1
            info.update(check="strict_delimited_parse_and_width", records=n, columns=width, width_anomalies=anomalies)
            if anomalies:
                raise ValueError(f"record width differs from first record {width}: {anomalies}")
            # Header meaning is not assumed. Empty tables are format-readable only.
        elif kind == "svg":
            root = ET.fromstring(raw)
            if root.tag.rsplit("}",1)[-1] != "svg":
                raise ValueError("SVG root mismatch")
            info["check"] = "XML_parse"
        elif kind == "yml":
            list(yaml.safe_load_all(s))
            info["check"] = "YAML_parse"
        elif kind == "py":
            ast.parse(s)
            info["check"] = "Python_AST_only"
        else:
            info["check"] = "UTF8_only"
    else:
        raise Unjudgeable("unsupported format: " + kind)
    return info


def selftest():
    tests = [
        (b'{"a":1}', "json", "PASS"),
        (b'{"a":1,"a":2}', "json", "FAIL"),
        (b'{"a":NaN}', "json", "FAIL"),
        (b'{"a":1}\ninvalid', "jsonl", "FAIL"),
        (b'a,b\n1,2\n', "csv", "PASS"),
        (b'a,b\n1\n', "csv", "FAIL"),
        (gzip.compress(b'a,b\n1,2\n'), "csv.gz", "PASS"),
        (lzma.compress(b'a\tb\n1\t2\n'), "tsv.xz", "PASS"),
        (b'not gzip', "csv.gz", "FAIL"),
        (b'\xff', "md", "FAIL"),
        (b'def invalid(', "py", "FAIL"),
        (b'abc', "unknown", "HOLD"),
    ]
    for raw, kind, expected in tests:
        try:
            format_check(raw,kind)
            result="PASS"
        except Unjudgeable:
            result="HOLD"
        except Exception:
            result="FAIL"
        assert result == expected, (kind, result, expected)
    print("RQ001_D_SELFTEST PASS",len(tests),flush=True)


def load_scope(repo):
    raw = (repo/SCOPE).read_bytes()
    scope = json.loads(raw)
    assert scope["state"] == "LOCKED_BEFORE_EXECUTION"
    assert scope["batch"]["size"] == 200 and scope["batch"]["count"] == 16
    rows = []
    for item in scope["inventory"]:
        data = (repo/item["path"]).read_bytes()
        assert blob(data) == item["git_blob"], item["path"]
        part = list(csv.DictReader(io.StringIO(data.decode()),delimiter="\t"))
        assert len(part) == item["count"]
        rows.extend(part)
    index = {}
    for row in rows:
        p = PurePosixPath(row["path"])
        assert not p.is_absolute() and ".." not in p.parts and str(p)==row["path"]
        assert row["path"] not in index and not row["path"].startswith("1.21.11/")
        index[row["path"]] = (row["git_blob_sha1"], int(row["bytes"]))
    assert len(index)==3167
    raw_tree=subprocess.check_output(["git","-C",str(repo),"ls-tree","-rlz",scope["main_pin"]])
    expected={}
    for entry in raw_tree.split(b"\0"):
        if not entry:
            continue
        meta, path=entry.split(b"\t",1)
        mode, kind, digest, size=meta.split()
        path=path.decode("utf-8")
        if kind==b"blob" and not path.startswith("1.21.11/"):
            expected[path]=(digest.decode(), int(size))
    assert index==expected, "locked inventory differs from pinned Git tree"
    return scope, sorted(rows,key=lambda x:x["path"].encode("utf-8")), sha(raw)


def audit_row(repo,row):
    result=dict(row)
    result["expected_bytes"]=int(row["bytes"])
    result["hash_status"]="HOLD"
    result["format_status"]="HOLD"
    result["status"]="HOLD"
    p=repo/row["path"]
    try:
        if p.is_symlink() or not p.is_file():
            if not p.exists() and not p.is_symlink():
                result.update(hash_status="FAIL",status="FAIL",reason="missing file")
                return result
            raise Unjudgeable("nonregular or symlink input")
        if not p.resolve().is_relative_to(repo):
            raise Unjudgeable("path escape")
        raw=p.read_bytes()
        result.update(actual_bytes=len(raw),actual_git_blob=blob(raw),actual_sha256=sha(raw))
        if (len(raw),result["actual_git_blob"]) != (int(row["bytes"]),row["git_blob_sha1"]):
            result.update(hash_status="FAIL",status="FAIL",reason="byte size or Git blob mismatch")
            return result
        result["hash_status"]="PASS"
        try:
            result["format_details"]=format_check(raw,row["format"])
            result["format_status"]="PASS"
            result["status"]="PASS"
        except Unjudgeable as e:
            result["reason"]=str(e)
        except (MemoryError, OSError) as e:
            # OSError from compressed or image readers indicates invalid input,
            # except unavailable filesystem resources (raw input already read).
            if isinstance(e, MemoryError):
                result["reason"]="MemoryError during format inspection"
            else:
                result.update(format_status="FAIL",status="FAIL",reason=str(e))
        except Exception as e:
            result.update(format_status="FAIL",status="FAIL",reason=f"{type(e).__name__}: {e}")
    except (OSError,Unjudgeable) as e:
        result["reason"]=str(e)
    return result


def current_matches(repo,records):
    for rec in records:
        p=repo/rec["path"]
        if rec["hash_status"]!="PASS" or p.is_symlink() or not p.is_file():
            return False
        try:
            if sha(p.read_bytes())!=rec["actual_sha256"]:
                return False
        except OSError:
            return False
    return True


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo",type=Path,required=True)
    ap.add_argument("--out",type=Path,required=True)
    ap.add_argument("--limit-batches",type=int,default=16)
    a=ap.parse_args()
    repo=a.repo.resolve()
    out=a.out.resolve()
    if out.is_relative_to(repo):
        raise ValueError("output must be outside research checkout")
    if not 1<=a.limit_batches<=16:
        raise ValueError("invalid batch limit")
    selftest()
    scope, rows, scope_sha=load_scope(repo)
    code_sha=sha(Path(__file__).read_bytes())
    all_records=[]
    batch_index=[]
    new=0
    reused=0
    for n,start in enumerate(range(0,len(rows),200),1):
        part=rows[start:start+200]
        input_sha=sha(pack(part))
        ident={"scope_sha256":scope_sha,"code_sha256":code_sha,"input_sha256":input_sha,"count":len(part)}
        ledger=out/"batches"/f"{n:02d}.jsonl"
        marker=out/"batches"/f"{n:02d}.checkpoint.json"
        records=None
        if ledger.exists() and marker.exists():
            try:
                m=json.loads(marker.read_bytes())
                data=ledger.read_bytes()
                candidate=[json.loads(l) for l in data.splitlines()]
                if (all(m.get(k)==v for k,v in ident.items()) and m.get("result_sha256")==sha(data)
                    and [x["path"] for x in candidate]==[x["path"] for x in part]
                    and current_matches(repo,candidate)):
                    records=candidate
                    reused+=1
            except (ValueError,KeyError,OSError):
                pass
        if records is None:
            if new>=a.limit_batches:
                break
            records=[audit_row(repo,row) for row in part]
            data=b"".join(pack(x) for x in records)
            atomic(ledger,data)
            atomic(marker,pack({**ident,"result_sha256":sha(data)}))
            new+=1
        all_records.extend(records)
        batch_index.append({"batch":n,"count":len(records),"result_sha256":sha(data)})
        print("RQ001_D_BATCH",n,len(records),dict(collections.Counter(x["status"] for x in records)),flush=True)
    data=b"".join(pack(x) for x in all_records)
    atomic(out/"D_files.jsonl",data)
    totals=dict(collections.Counter(x["status"] for x in all_records))
    hashes=dict(collections.Counter(x["hash_status"] for x in all_records))
    formats=dict(collections.Counter(x["format_status"] for x in all_records))
    complete=len(all_records)==3167 and len(batch_index)==16
    status="FAIL" if totals.get("FAIL") else "HOLD" if totals.get("HOLD") else "PASS" if complete else "PARTIAL"
    summary={"gate":"6-D","status":status,"scope_complete":complete,"expected":3167,"attempted":len(all_records),
             "counts":totals,"hash_counts":hashes,"format_counts":formats,"new_batches":new,
             "reused_batches":reused,"batches":batch_index,"scope_sha256":scope_sha,"code_sha256":code_sha,
             "ledger_sha256":sha(data),"source_pin":scope["main_pin"],"limits":"File identity and format only, not semantic accuracy."}
    atomic(out/"D_summary.json",pack(summary))
    print("RQ001_D_SUMMARY "+json.dumps({k:v for k,v in summary.items() if k!="batches"},ensure_ascii=False),flush=True)


if __name__=="__main__":
    main()
