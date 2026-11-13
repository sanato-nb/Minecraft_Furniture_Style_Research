#!/usr/bin/env python3
"""Check an owned Minecraft Java 1.21.11 client.jar. The source file bytes
and official whole-JAR SHA-1 are two separate tests. No JAR is redistributed.

python VERIFY_CLIENT_JAR.py --jar /path/to/1.21.11.jar --ledger ../TEX07-R003/SOURCE_LEDGER.csv --output evidence.json
"""
import argparse
import csv
import hashlib
import json
import pathlib
import sys
import urllib.parse
import urllib.request
import zipfile

MANIFEST = "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"
VERSION = "1.21.11"
ALLOWED_HOSTS = {"piston-meta.mojang.com", "launchermeta.mojang.com"}

def metadata_get(url):
    u = urllib.parse.urlparse(url)
    if u.scheme != "https" or u.hostname not in ALLOWED_HOSTS:
        raise ValueError("Non-Mojang metadata URL refused: " + url)
    req = urllib.request.Request(url, headers={"User-Agent": "MC-Texture-Source-Audit/1.0"})
    with urllib.request.urlopen(req, timeout=15) as response:
        return json.load(response)

def official_client_info():
    manifest = metadata_get(MANIFEST)
    entry = next((x for x in manifest.get("versions", []) if x.get("id") == VERSION), None)
    if entry is None:
        raise ValueError("Version absent from Mojang manifest")
    doc = metadata_get(entry["url"])
    if doc.get("id") != VERSION:
        raise ValueError("Version JSON mismatch")
    info = doc["downloads"]["client"]
    if len(info["sha1"]) != 40 or not isinstance(info["size"], int):
        raise ValueError("Incomplete official SHA-1 or size")
    return {"sha1": info["sha1"].lower(), "size": info["size"], "metadata_url": entry["url"]}

def whole_file_sha1(path):
    h = hashlib.sha1()
    n = 0
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
            n += len(chunk)
    return h.hexdigest(), n

def git_blob_sha1(data):
    return hashlib.sha1(("blob %d\0" % len(data)).encode("ascii") + data).hexdigest()

def audit(args):
    r = {"version": VERSION, "original_JAR_authentication": "PENDING",
         "extracted_file_comparison": "PENDING", "entries": [], "metadata_manifest": MANIFEST}
    official = None
    if args.offline:
        r["metadata_error"] = "--offline: official metadata not accessed"
    else:
        try:
            official = official_client_info()
            r["mojang_metadata"] = official
        except Exception as e:
            r["metadata_error"] = type(e).__name__ + ": " + str(e)
    measured, size = whole_file_sha1(args.jar)
    r["measured_jar_sha1"] = measured
    r["measured_jar_size"] = size
    if official is not None:
        r["mojang_sha1_equal"] = measured == official["sha1"]
        r["mojang_size_equal"] = size == official["size"]
        r["original_JAR_authentication"] = (
            "OFFICIAL_AUTHENTICATED" if r["mojang_sha1_equal"] and r["mojang_size_equal"]
            else "FAILED_OFFICIAL_ARTIFACT_CHECK")
    with args.ledger.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 31:
        raise ValueError("Expected exactly 31 R003 source ledger rows")
    with zipfile.ZipFile(args.jar) as archive:
        for row in rows:
            path = row["mirror_repo_path"]
            expected = row["source_git_blob_sha1"].lower()
            try:
                digest = git_blob_sha1(archive.read(path))
                r["entries"].append({"path": path, "actual_git_blob_sha1": digest,
                                      "expected_git_blob_sha1": expected, "match": digest == expected})
            except KeyError:
                r["entries"].append({"path": path, "match": False, "error": "missing from JAR"})
    r["extracted_file_comparison"] = (
        "31_OF_31_MATCH" if all(x["match"] for x in r["entries"]) else "MISMATCH")
    r["official_and_ledger_fully_verified"] = (
        r["original_JAR_authentication"] == "OFFICIAL_AUTHENTICATED"
        and r["extracted_file_comparison"] == "31_OF_31_MATCH")
    if args.output:
        args.output.write_text(json.dumps(r, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in r.items() if k != "entries"}, indent=2, ensure_ascii=False))
    return 0 if r["official_and_ledger_fully_verified"] else 2

if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--jar", type=pathlib.Path, required=True)
    p.add_argument("--ledger", type=pathlib.Path, required=True)
    p.add_argument("--output", type=pathlib.Path)
    p.add_argument("--offline", action="store_true", help="Do not fetch official metadata; never mark authenticated")
    args = p.parse_args()
    try:
        sys.exit(audit(args))
    except Exception as e:
        print(type(e).__name__ + ": " + str(e), file=sys.stderr)
        sys.exit(3)
