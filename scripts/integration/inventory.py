"""INT-0/INT-1: reproducible, read-only Git-tree inventory of historical research.

Pinned to main@176f7f...: newly created integration files and the extracted
Minecraft 1.21.11 source tree are deliberately outside this file manifest.
This indexes Git paths/mode/blob IDs/sizes; it does NOT prove pixel, runtime,
or model-semantic correctness.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import csv
import io
import json
from pathlib import Path
import subprocess
import sys

BASELINE = "176f7f34de2336eb7984c4734e97b6eb156c19f4"
ROOT = Path(__file__).resolve().parents[2]
SCOPES = (
    ".github", "data", "docs", "handoff", "harness", "inbox", "project",
    "registry", "research", "scripts", "src", "tests",
    ".gitignore", "AGENTS.md", "FILE_MANIFEST_SHA256.csv", "HANDOFF.md",
    "PROGRESS.md", "README.md", "README_2026-11-19.md",
    "SOURCES_AND_LIMITS.md", "UPLOAD_GUIDE.md", "requirements.txt",
)
HEADER = ("source_commit", "stage", "role", "path", "git_mode", "git_blob_sha1", "bytes")


def stage(path: str) -> str:
    if path.startswith(("research/vanilla_textures/", "docs/vanilla_texture_1-1/")):
        return "1-1"
    if path.startswith(("research/vanilla_models/", "docs/vanilla_models_1-2/")):
        return "1-2"
    for index in ("1-3", "1-4", "1-5"):
        if path.startswith(f"research/furniture_mods/phase_{index}/"):
            return index
    if path.startswith("docs/furniture_mods_1-3/"):
        return "1-3"
    if path.startswith("docs/furniture_mods_1-4/"):
        return "1-4"
    if path.startswith("docs/furniture_compare_1-5/"):
        return "1-5"
    if path.startswith(("research/historical/", "docs/archive/")):
        return "HISTORICAL"
    if path.startswith(("src/", "scripts/", "tests/", "harness/", ".github/", "project/", "registry/")):
        return "HARNESS"
    return "CROSS_OR_OTHER"


def role(path: str) -> str:
    name = path.rsplit("/", 1)[-1].lower()
    if name.endswith((".sqlite", ".sqlite.xz", ".db", ".db.xz")):
        return "SQLITE"
    if name.endswith((".csv", ".csv.gz", ".csv.xz", ".tsv", ".tsv.gz", ".tsv.xz")):
        return "TABLE"
    if name.endswith((".png", ".jpg", ".jpeg", ".webp", ".gif")):
        return "IMAGE"
    if name.endswith((".py", ".java", ".kt", ".sh", ".ps1", ".bat")):
        return "CODE"
    if name.endswith(".json"):
        return "JSON"
    if name.endswith(".md"):
        return "DOCUMENT"
    if name.endswith((".sql", ".yml", ".yaml", ".toml", ".ini")):
        return "SCHEMA_OR_CONFIG"
    return "OTHER"


def inventory(repo: Path = ROOT, baseline: str = BASELINE) -> list[dict[str, str]]:
    command = ["git", "-C", str(repo), "ls-tree", "-r", "-l", "-z", baseline, "--", *SCOPES]
    raw = subprocess.check_output(command)
    result = []
    for record in raw.split(b"\x00"):
        if not record:
            continue
        meta, path = record.split(b"\t", 1)
        mode, kind, sha, size = meta.decode("ascii").split()
        source_path = path.decode("utf-8")
        if kind != "blob":
            raise ValueError(f"Unexpected non-blob entry: {source_path}")
        if source_path.startswith("1.21.11/"):
            raise ValueError("Original resource extraction must not be mixed into research inventory")
        result.append({
            "source_commit": baseline,
            "stage": stage(source_path), "role": role(source_path),
            "path": source_path, "git_mode": mode,
            "git_blob_sha1": sha, "bytes": size,
        })
    result.sort(key=lambda item: item["path"])
    paths = [item["path"] for item in result]
    if len(set(paths)) != len(paths):
        raise ValueError("Duplicate paths in Git tree inventory")
    return result


def render(rows: list[dict[str, str]]) -> str:
    output = io.StringIO(newline="")
    writer = csv.DictWriter(output, fieldnames=HEADER, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue()


def overview(rows: list[dict[str, str]]) -> dict:
    by_sha = defaultdict(list)
    for row in rows:
        by_sha[row["git_blob_sha1"]].append(row["path"])
    return {
        "schema": "MCFR_INT1_GIT_TREE/v1",
        "baseline_commit": rows[0]["source_commit"] if rows else None,
        "file_count": len(rows),
        "total_git_blob_bytes": sum(int(row["bytes"]) for row in rows),
        "by_stage": dict(sorted(Counter(row["stage"] for row in rows).items())),
        "by_role": dict(sorted(Counter(row["role"] for row in rows).items())),
        "same_blob_sha_groups": sum(len(paths) > 1 for paths in by_sha.values()),
        "scope": "research/docs/project/data/handoff/registry/scripts/src/tests/harness/inbox/.github/root docs",
        "excluded": ["1.21.11/ source extraction (managed by H2 source catalog; not included in INT-1 historical research artifact manifest)"],
        "verification_level": "GIT_TREE_METADATA_ONLY",
    }


def validate_references(rows: list[dict[str, str]], integration_dir: Path) -> dict:
    found = {row["path"] for row in rows}
    for filename, fields in (
        ("EVIDENCE_MAP.csv", ("path",)),
        ("DEPENDENCY_MAP.csv", ("source", "target")),
    ):
        path = integration_dir / filename
        with path.open(encoding="utf-8-sig", newline="") as file:
            refs = list(csv.DictReader(file))
        bad = [(name, row.get(name)) for row in refs for name in fields if row.get(name) not in found]
        if bad:
            raise ValueError(f"{filename}: missing pinned paths: {bad[:10]}")
    return {"evidence_map": "ALL_PATHS_IN_PINNED_TREE", "dependencies": "ALL_PATHS_IN_PINNED_TREE"}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", default=BASELINE)
    parser.add_argument("--manifest", type=Path, default=ROOT / "project/integration/SOURCE_MANIFEST.csv")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="Compare checked-in manifest and reference links")
    mode.add_argument("--write", action="store_true", help="Write a newly generated snapshot explicitly")
    args = parser.parse_args(argv)
    rows = inventory(ROOT, args.baseline)
    content = render(rows)
    if args.write:
        args.manifest.parent.mkdir(parents=True, exist_ok=True)
        args.manifest.write_text(content, encoding="utf-8", newline="")
    elif args.manifest.read_text(encoding="utf-8") != content:
        raise SystemExit("INT-1 manifest differs from the pinned Git tree")
    checks = validate_references(rows, args.manifest.parent)
    print(json.dumps({**overview(rows), **checks}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
