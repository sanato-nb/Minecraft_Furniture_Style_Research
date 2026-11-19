"""H0 full tracked-file integrity and executable path-dependency audit.

Read-only: writes reports only under --out, never edits tracked sources.
"""
from __future__ import annotations

import argparse
from collections import Counter
import csv
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

CODE_SUFFIXES = {".py", ".js", ".sh", ".yml", ".yaml", ".java", ".sql", ".mcfunction"}
PATH_REF = re.compile(r"(?:research|scripts|docs|data|handoff|1\.21\.11|\.github)/[A-Za-z0-9가-힣_./-]+")
PIN = re.compile(r"(?:\bBASELINE\b|\bBASE\b\s*=|[a-f0-9]{40})")
GIT_DEP = re.compile(r"(?:ls-tree|rev-parse|git[\s,'\"]+show|HEAD:main|git push)")
ROOT_DEP = re.compile(r"(?:\.parents?\[|__file__|Path\.cwd\()")
MAIN_WRITE = re.compile(r"(?:HEAD:main|git push origin)")


def git_blob_digest(body: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(body)).encode() + b"\0" + body).hexdigest()


def indexed_paths(root: Path):
    payload = subprocess.check_output(["git", "-C", str(root), "ls-files", "-s", "-z"])
    for token in payload.split(b"\0"):
        if not token:
            continue
        meta, raw_path = token.split(b"\t", 1)
        mode, digest, stage = meta.decode("ascii").split(" ")
        yield mode, digest, int(stage), raw_path.decode("utf-8", "surrogateescape")


def compare_baseline(root: Path, baseline: str, indexed: dict) -> dict:
    commit = subprocess.check_output(
        ["git", "-C", str(root), "rev-parse", "--verify", "--end-of-options", f"{baseline}^{{commit}}"],
        text=True,
    ).strip()
    tree = subprocess.check_output(["git", "-C", str(root), "ls-tree", "-r", "-z", commit])
    original = {}
    for entry in tree.split(b"\0")[:-1]:
        metadata, raw_path = entry.split(b"\t", 1)
        mode, _, digest = metadata.decode("ascii").split()
        original[raw_path.decode("utf-8", "surrogateescape")] = (mode, digest)
    removed = sorted(original.keys() - indexed.keys())
    modified = sorted(path for path in original.keys() & indexed.keys() if original[path] != indexed[path])
    return {
        "commit": commit,
        "files": len(original),
        "added_count": len(indexed.keys() - original.keys()),
        "removed": removed,
        "modified": modified,
        "preserved_files": len(original) - len(removed) - len(modified),
    }


def run(root: Path, out: Path, baseline: str | None = None):
    root = root.resolve()
    out.mkdir(parents=True, exist_ok=True)
    paths = list(indexed_paths(root))
    comparison = None
    if baseline is not None:
        indexed = {path: (mode, digest) for mode, digest, stage, path in paths if stage == 0}
        comparison = compare_baseline(root, baseline, indexed)
    root_counts = {}
    suffix_counts = Counter()
    hashes = Counter()
    scan_records = []
    errors = []
    total_bytes = 0
    with (out / "H0_TRACKED_FILES.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(("path", "mode", "git_blob_sha1", "bytes", "sha256"))
        for mode, git_sha, stage, rel in paths:
            file = root / rel
            try:
                if stage != 0:
                    raise ValueError("Unmerged index stage")
                if mode == "120000":
                    body = os.readlink(file).encode("utf-8", "surrogateescape")
                else:
                    body = file.read_bytes()
                if git_blob_digest(body) != git_sha:
                    raise ValueError("Git blob SHA does not match working tree")
                sha256 = hashlib.sha256(body).hexdigest()
                writer.writerow((rel, mode, git_sha, len(body), sha256))
                total_bytes += len(body)
                first = rel.split("/", 1)[0]
                x = root_counts.setdefault(first, {"files": 0, "bytes": 0})
                x["files"] += 1
                x["bytes"] += len(body)
                suffix_counts[file.suffix.lower() or "(none)"] += 1
                hashes[git_sha] += 1
                if file.suffix.lower() in CODE_SUFFIXES and not rel.startswith("1.21.11/"):
                    content = body.decode("utf-8", errors="replace")
                    flags = []
                    if PIN.search(content):
                        flags.append("pinned_commit_or_hash")
                    if GIT_DEP.search(content):
                        flags.append("git_history_dependency")
                    if ROOT_DEP.search(content):
                        flags.append("cwd_or_file_relative")
                    if MAIN_WRITE.search(content):
                        flags.append("main_push_reference")
                    if "subprocess." in content or "runs-on:" in content:
                        flags.append("runtime_dependency")
                    scan_records.append({
                        "path": rel,
                        "git_blob_sha1": git_sha,
                        "flags": flags,
                        "path_literals": sorted(set(PATH_REF.findall(content)))
                    })
            except (OSError, ValueError) as exc:
                errors.append({"path": rel, "error": str(exc)})
    scan_records.sort(key=lambda x: x["path"])
    duplicate_counts = [n for n in hashes.values() if n > 1]
    failed = bool(errors or (comparison and (comparison["modified"] or comparison["removed"])))
    summary = {
        "status": "FAIL" if failed else "PASS",
        "source": "checked-out indexed working tree",
        "scope": "all tracked files: Git blob SHA-1 and SHA-256; static path scan outside extracted client assets",
        "scanned_code_suffixes": sorted(CODE_SUFFIXES),
        "baseline_comparison": comparison,
        "tracked_files": len(paths),
        "verified_files": len(paths) - len(errors),
        "total_bytes": total_bytes,
        "by_root": root_counts,
        "by_suffix": dict(sorted(suffix_counts.items())),
        "duplicate_git_blob_sha_groups": len(duplicate_counts),
        "duplicate_extra_paths": sum(n - 1 for n in duplicate_counts),
        "code_scanned": len(scan_records),
        "code_main_push_references": [x["path"] for x in scan_records if "main_push_reference" in x["flags"]],
        "errors": errors,
        "limitation": "Path references are candidate string literals, not proof of runtime dependency or link resolution."
    }
    (out / "H0_CODE_PATH_SCAN_FULL.json").write_text(json.dumps({
        "source": "read-only static scan of Git checkout",
        "records": scan_records
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (out / "H0_AUDIT_SUMMARY.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({k: summary[k] for k in (
        "status", "tracked_files", "verified_files", "code_scanned", "baseline_comparison",
        "duplicate_git_blob_sha_groups", "code_main_push_references", "errors"
    )}, ensure_ascii=False, indent=2))
    return 1 if failed else 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--baseline", help="Fail if any tracked path, mode, or blob from this commit differs")
    args = parser.parse_args(argv)
    return run(args.root, args.out, args.baseline)


if __name__ == "__main__":
    raise SystemExit(main())
