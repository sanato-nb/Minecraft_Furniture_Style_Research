#!/usr/bin/env python3
"""Compare a local Minecraft Java 1.21.11 client.jar against stored hashes.

Usage:
  python scripts/verify_official_jar.py --jar /path/to/1.21.11.jar --db data/MC_Furniture_Style_Stage1_Research_v8.sqlite --out comparison.json

Requires only the Python standard library. No copyrighted Minecraft files
are downloaded or redistributed.
"""
import argparse
import hashlib
import json
import pathlib
import sqlite3
import sys
import zipfile
from collections import Counter

def git_blob_sha1(data):
    return hashlib.sha1(f"blob {len(data)}".encode("ascii")+bytes([0])+data).hexdigest()

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--jar",required=True,type=pathlib.Path)
    ap.add_argument("--db",required=True,type=pathlib.Path)
    ap.add_argument("--out",default="client_jar_comparison.json",type=pathlib.Path)
    ap.add_argument("--strict",action="store_true")
    args=ap.parse_args()
    if not args.jar.is_file() or not args.db.is_file():
        ap.error("Both --jar and --db must point to existing files.")
    c=sqlite3.connect(args.db)
    try:
        textures=c.execute("SELECT texture_id,sha256 FROM texture_stats_v4").fetchall()
        sources=c.execute("SELECT path,github_blob_sha1 FROM sources WHERE github_blob_sha1 IS NOT NULL AND github_blob_sha1!=''").fetchall()
    finally:
        c.close()
    targets=[]
    for name,sha in textures:
        targets.append({"category":"texture_png","path":f"assets/minecraft/textures/block/{name}.png","expected":sha,"hash":"sha256"})
    for name,sha in sources:
        targets.append({"category":"model_state_source","path":name,"expected":sha,"hash":"git_blob_sha1"})
    observations=[]
    with zipfile.ZipFile(args.jar) as archive:
        members=set(archive.namelist())
        for t in targets:
            o=dict(t)
            if t["path"] not in members:
                o.update(status="missing",observed=None)
            else:
                data=archive.read(t["path"])
                digest=hashlib.sha256(data).hexdigest() if t["hash"]=="sha256" else git_blob_sha1(data)
                o.update(status="match" if digest.lower()==t["expected"].lower() else "mismatch",observed=digest)
            observations.append(o)
    counts=Counter(o["status"] for o in observations)
    result={
        "reference_minecraft_version":"1.21.11",
        "jar_path":str(args.jar),
        "jar_sha256":hashlib.sha256(args.jar.read_bytes()).hexdigest(),
        "db_path":str(args.db),
        "db_sha256":hashlib.sha256(args.db.read_bytes()).hexdigest(),
        "status":"PASS" if not counts["mismatch"] and not counts["missing"] else "INCOMPLETE_OR_MISMATCH",
        "counts":dict(counts),
        "observations":observations,
        "limits":[
            "This compares byte hashes only; in-game tint, UV, animation and rendering are not verified.",
            "Verify the provided JAR really is the official Java 1.21.11 client yourself.",
            "Formatting differences can cause model JSON Git blob mismatches even if their meanings are equivalent.",
            "Extracted entity models/animations are not expected to appear as these static asset paths."
        ]
    }
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("records=",len(observations),"counts=",dict(counts),"out=",args.out)
    return 2 if args.strict and (counts["mismatch"] or counts["missing"]) else 0

if __name__=="__main__":
    sys.exit(main())
