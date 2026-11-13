#!/usr/bin/env python3
"""TEX08-R002 official client.jar offline resource auditor.

Requires a locally supplied Minecraft 1.21.11 client JAR and online access
to Mojang's HTTPS version manifest. Neither uploads nor redistributes JAR data.
A successful SHA-1 match to Mojang launcher metadata authenticates the
downloaded JAR artifact under that metadata, not an in-game render test.
"""
import argparse
import hashlib
import json
import pathlib
import urllib.request
import zipfile

VERSION = "1.21.11"
MANIFEST_URL = "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"

def digest(data, algo="sha1"):
    return hashlib.new(algo, data).hexdigest()

def fetch(url):
    if not url.startswith("https://piston-meta.mojang.com/"):
        raise ValueError("Only Mojang piston-meta HTTPS metadata URLs are allowed")
    with urllib.request.urlopen(url, timeout=40) as response:
        return response.read()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jar", required=True, type=pathlib.Path)
    ap.add_argument("--ledger", required=True, type=pathlib.Path,
                    help="TEX08-R001 SOURCE_LEDGER.csv path")
    args = ap.parse_args()
    import csv
    with args.ledger.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 21, "Stage ledger must contain exactly 21 items"
    manifest = json.loads(fetch(MANIFEST_URL))
    matches = [v for v in manifest["versions"] if v["id"] == VERSION and v["type"] == "release"]
    assert len(matches) == 1, "No unique official 1.21.11 release"
    v = matches[0]
    metadata_bytes = fetch(v["url"])
    assert digest(metadata_bytes) == v["sha1"], "Mojang metadata SHA1 mismatch"
    metadata = json.loads(metadata_bytes)
    assert metadata["id"] == VERSION
    entry = metadata["downloads"]["client"]
    jar_bytes = args.jar.read_bytes()
    jar_sha1 = digest(jar_bytes)
    assert len(jar_bytes) == entry["size"], "JAR size differs from Mojang metadata"
    assert jar_sha1 == entry["sha1"], "JAR SHA1 differs from Mojang metadata"
    checks = []
    with zipfile.ZipFile(args.jar) as jar:
        assert jar.testzip() is None, "Corrupted ZIP/JAR member"
        for row in rows:
            file_path = row["source_path"]
            actual_sha = digest(jar.read(file_path), "sha256")
            checks.append({"texture_id": row["texture_id"], "source_path": file_path,
                           "official_jar_texture_sha256": actual_sha,
                           "matches_R001_mirror": actual_sha == row["sha256_recomputed"]})
    result = {
        "game_version": VERSION, "manifest_url": MANIFEST_URL,
        "metadata_sha1_verified": True, "jar_sha1_verified": True,
        "client_jar_sha1": jar_sha1, "client_jar_size": len(jar_bytes),
        "official_jar_files_checked": len(checks),
        "matching_mirror_sha256_count": sum(x["matches_R001_mirror"] for x in checks),
        "ingame_static_verified": False,
        "records": checks,
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if not all(x["matches_R001_mirror"] for x in checks):
        raise SystemExit("At least one 1.21.11 JAR PNG differs from the R001 mirror")

if __name__ == "__main__":
    main()
