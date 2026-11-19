"""Check the 1-2 stage review against the pinned Git tree, client and replays."""
from argparse import ArgumentParser
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path
import re
import subprocess
from zipfile import ZipFile

from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
VANILLA = HERE.parent
BASE = "b2960c684f8e48ef3b413d408853cfd8a96d7746"
JAR_SHA1 = "ba2df812c2d12e0219c489c4cd9a5e1f0760f5bd"
G = VANILLA / "phase_1-2-G/final"
E = VANILLA / "phase_1-2-E/followup"
F = VANILLA / "phase_1-2-F/followup"
COUNTS = {"BLOCK_MODEL_JSON": 2390, "BLOCKSTATE_JSON": 1168, "BLOCK_TEXTURE_PNG": 1111}


def git(*args):
    return subprocess.check_output(["git", "-C", str(ROOT), *args])


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def rows(path):
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        result = list(reader)
    assert len(set(reader.fieldnames)) == len(reader.fieldnames)
    assert all(None not in r and None not in r.values() for r in result)
    return result


def tree_hashes(prefix):
    paths = {}
    for line in git("ls-tree", "-r", "-z", BASE, "--", prefix).decode().strip("\0").split("\0"):
        meta, name = line.split("\t", 1)
        paths[name] = meta.split()[2]
    return paths


def source_identity(jar):
    with jar.open("rb") as stream:
        assert hashlib.file_digest(stream, "sha1").hexdigest() == JAR_SHA1
    source = rows(G / "G_FINAL_SOURCE_SHA_4669.csv")
    metadata = rows(G / "G_FINAL_MCMETA_99.csv")
    assert Counter(r["type"] for r in source) == COUNTS and len(metadata) == 99
    identity = [(r["path"], r["sha"], int(r["bytes"])) for r in source]
    identity += [(r["mcmeta_path"], r["git_sha"], int(r["bytes"])) for r in metadata]
    assert len({r[0] for r in identity}) == len(identity)
    assert all(r["source_sha_match"] == "True" for r in source)
    tree = tree_hashes("1.21.11/assets/minecraft")
    with ZipFile(jar) as zipfile:
        for path, expected, size in identity:
            raw = zipfile.read(path.removeprefix("1.21.11/"))
            actual = hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()
            assert len(raw) == size and actual == expected == tree[path], path
    return {r["path"]: r["sha"] for r in source if r["type"] == "BLOCK_MODEL_JSON"}


def compare_abcdf(models):
    specs = (
        ("phase_1-2-B/entry10/B_SCOPE_2390_STATUS.csv", "full_source_path"),
        ("phase_1-2-C/entry5/C_SCOPE_2390_FINAL_STATUS.csv", "source_path"),
        ("phase_1-2-F/F_FIXED_SCOPE_2390.csv", "source_path"),
    )
    for name, column in specs:
        ledger = rows(VANILLA / name)
        assert len(ledger) == 2390
        assert {r[column]: r["git_blob_sha"] for r in ledger} == models
        assert Counter(row["priority"] for row in ledger) == {"P1": 544, "P2": 1039, "P3": 807}
    d = load(VANILLA / "phase_1-2-D/entry6/D_FINAL_CLOSURE.json")
    assert d["whole_D_complete"] and d["source_paths_duplicate_or_missing"] == 0
    assert (d["fixed_scope_paths"], d["syntactic_state_rows"], d["state_option_instances"]) == (1168, 9193, 19440)


def verify_e(models, replay):
    results = rows(E / "E_RUNTIME_OUTCOMES_86.csv")
    plan = rows(E / "E_FIXTURE_PLAN_86.csv")
    log = (E / "E_RUNTIME_LOG_EXCERPT.txt").read_text()
    matches = {}
    for time, name in re.findall(r"^\[([0-9:]+)\] .* EF_MATCH_([a-z0-9_]+)$", log, flags=re.M):
        matches.setdefault(name, time)
    outcome = Counter(r["outcome"] for r in results)
    summary = load(E / "E_RUNTIME_SUMMARY.json")
    assert len(results) == len(plan) == 86
    assert outcome == summary["observations"]
    assert set(matches) == {r["model"] for r in results if r["state"]}
    for expected, actual in zip(plan, results, strict=True):
        assert all(actual[key] == value for key, value in expected.items())
        assert actual["state_readback"] == matches.get(actual["model"], "")
        assert models[f"1.21.11/assets/minecraft/models/block/{actual['model']}.json"] == actual["model_sha"]
        assert (E / actual["screenshot"]).is_file()
    for name, expected in summary["screenshot_evidence_sha256"].items():
        shot = E / "evidence" / name
        assert hashlib.sha256(shot.read_bytes()).hexdigest() == expected
        with Image.open(shot) as image:
            image.verify()
    assert len(matches) == summary["confirmed_runtime_states"] == 84
    assert (replay / "E-replayed/E_FIXTURE_PLAN_86.csv").read_bytes() == (E / "E_FIXTURE_PLAN_86.csv").read_bytes()
    return dict(models=len(results), confirmed_states=len(matches), outcomes=dict(outcome),
                prior_screenshots_verified=len(summary["screenshot_evidence_sha256"]))


def compare_replay(replay):
    final = load(G / "G_FINAL_EXIT_AUDIT.json")
    assert final["G_complete"] and all(g["status"] == "PASS" for g in final["gates"].values())
    names = ("G_GLOBAL_INDEPENDENT_RECOUNT.json", "G_FINAL_SOURCE_SHA_4669.csv", "G_FINAL_MCMETA_99.csv")
    for name in names:
        assert (G / name).read_bytes() == (replay / G.relative_to(ROOT) / name).read_bytes(), name
    recap = load(G / names[0])
    assert not recap["source_stage_errors"] and all(c["pass_"] for c in recap["all_subgate_checks"])
    files = sorted(p.name for p in F.glob("F3_*") if p.suffix in {".csv", ".json"})
    assert len(files) == 6
    for name in files:
        assert (F / name).read_bytes() == (replay / "F-replayed" / name).read_bytes(), name
    return (len(recap["all_subgate_checks"]), len(names), len(files))


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--jar", type=Path, required=True)
    parser.add_argument("--replay", type=Path, required=True)
    options = parser.parse_args()
    models = source_identity(options.jar)
    compare_abcdf(models)
    e = verify_e(models, options.replay)
    g_checks, g_files, f_files = compare_replay(options.replay)
    f = load(F / "F3_FOLLOWUP_SUMMARY.json")
    print(json.dumps(dict(status="PASS_FIXED_1_2_SOURCE_SCOPE", baseline=BASE,
        client_jar_sha1=JAR_SHA1, asset_identity=COUNTS, mcmeta_sidecars=99,
        shared_model_keys_B_C_F=len(models), P1_priority_models=544, E=e,
        F=dict(replayed_files=f_files, animation_textures=f["animation_textures"],
               source_frames=f["source_frame_cells"], playback_steps=f["playback_steps"]),
        G=dict(replayed_files=g_files, reproduced_checks=g_checks, previously_approved_gates=6)),
        ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
