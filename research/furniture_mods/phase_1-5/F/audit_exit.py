"""Check regenerated 1-5 evidence against the pinned GitHub baseline."""
import argparse
from collections import Counter
import csv
import hashlib
import io
import json
import lzma
from pathlib import Path
import sqlite3
import subprocess

from PIL import Image

HERE = Path(__file__).resolve().parent
PHASE = HERE.parent
ROOT = HERE.parents[3]
BASELINE = "84842b0516af1aaa9a4dcc7b1fb73ee798b96f87"
VERSIONS = ("1.21.1", "1.21.11")
APP = ("case", "rule_index", "option_index")
ELEMENT = APP + ("element_index",)
FACE = ELEMENT + ("direction",)
REPLAY_FILES = {
    "A": ("A_SCOPE_AUDIT.json", "MOD_CASE_SCOPE.csv", "VANILLA_CONTROL_OPTIONS.csv", "VANILLA_SOURCE_PROVENANCE.csv"),
    "B": ("B_AUDIT.json", "CASES.csv", "APPLICATIONS.csv", "ELEMENTS.csv", "FACES.csv.xz",
          "ANIMATION_FRAMES.csv.xz", "VANILLA_MCMETA.csv"),
    "C": ("C_AUDIT.json", "CATEGORY_COVERAGE.csv", "CROSS_CATEGORY_FINDINGS.csv"),
    "D": ("D_AUDIT.json", "PARENT_EXCEPTIONS.csv", "STATE_EXCEPTIONS.csv", "STATIC_COUNTEREXAMPLES.json",
          "TEXTURE_EXPOSURE.csv"),
    "E": ("E_AUDIT.json", "PHASE2_HANDOFF.csv", "comparison.sqlite.xz"),
}
SUPPORT = (
    "docs/furniture_compare_1-5/1-5_DETAILED_EXECUTION_PLAN.md",
    "docs/vanilla_models_1-2/1-2_STAGE_EXIT_SEPARATE_REVIEW.md",
    "handoff/STATE.json",
    "research/vanilla_models/phase_1-2-G/final/G_FINAL_EXIT_AUDIT.json",
    "research/furniture_mods/phase_1-3/G/1-3_INDEPENDENT_EXIT_AUDIT.json",
    "research/furniture_mods/phase_1-3/E/E_SAMPLE_SELECTION.csv",
    "research/furniture_mods/phase_1-3/followup/C_ITEM_DISPLAY_READBACK.csv",
    "research/furniture_mods/phase_1-4/entry04/1-5_TEXTURE_UV_HANDOFF.csv",
    "research/furniture_mods/phase_1-4/F/EXIT_AUDIT.json",
)


def git(*args):
    return subprocess.check_output(["git", "-C", str(ROOT), *args])


def tabular(data, delim=","):
    reader = csv.DictReader(io.StringIO(data.decode("utf-8")), delimiter=delim)
    assert reader.fieldnames and len(reader.fieldnames) == len(set(reader.fieldnames))
    records = list(reader)
    assert all(None not in row and None not in row.values() for row in records)
    return records


def data(path):
    raw = (PHASE / path).read_bytes()
    if path.endswith(".xz"):
        raw = lzma.decompress(raw)
    return tabular(raw)


def keyed(records, *cols):
    index = {tuple(r[k] for k in cols): r for r in records}
    assert len(index) == len(records), cols
    return index


def compare_sources(jar):
    from zipfile import ZipFile
    records = data("A/VANILLA_SOURCE_PROVENANCE.csv")
    assert len(keyed(records, "path")) == 74
    with ZipFile(jar) as archive:
        for row in records:
            raw = archive.read(row["path"])
            assert len(raw) == int(row["bytes"])
            assert hashlib.sha256(raw).hexdigest() == row["sha256"]
            assert hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest() == row["git_blob_sha1"]
    return len(records)


def comparison_keys():
    mod = keyed(data("A/MOD_CASE_SCOPE.csv"), "case")
    vanilla = data("A/VANILLA_CONTROL_OPTIONS.csv")
    cases = keyed(data("B/CASES.csv"), "case")
    apps = keyed(data("B/APPLICATIONS.csv"), *APP)
    elements = keyed(data("B/ELEMENTS.csv"), *ELEMENT)
    faces = keyed(data("B/FACES.csv.xz"), *FACE)
    frames = keyed(data("B/ANIMATION_FRAMES.csv.xz"), *FACE, "frame")
    assert len(mod) == 47 and len({r["control"] for r in vanilla}) == 15
    assert cases.keys() == mod.keys() | {(row["control"],) for row in vanilla}
    assert [len(x) for x in (cases, apps, elements, faces, frames)] == [62, 74, 390, 1844, 109]
    assert all(k[:1] in cases for k in apps)
    assert all(k[:3] in apps for k in elements)
    assert all(k[:4] in elements for k in faces)
    assert all(k[:5] in faces for k in frames)
    counts = Counter(k[0] for k in apps)
    assert (counts["V03"], counts["V08"], counts["V11"]) == (2, 7, 1)
    mod_apps = sum(k[:1] in mod for k in apps)
    mod_faces = sum(k[:1] in mod for k in faces)
    assert (mod_apps, mod_faces) == (52, 1610)
    for parent, child, width, expected in (
        (cases, apps, 1, "applications"), (apps, elements, 3, "elements"),
        (elements, faces, 4, "faces"),
    ):
        counts = Counter(k[:width] for k in child)
        assert all(counts[k] == int(v[expected]) for k, v in parent.items())
    return dict(cases=len(cases), applications=len(apps), elements=len(elements),
                faces=len(faces), animation_frames=len(frames), mod_cases=len(mod),
                mod_applications=mod_apps, mod_faces=mod_faces)


def findings_and_exceptions():
    categories = keyed(data("C/CATEGORY_COVERAGE.csv"), "category")
    findings = keyed(data("C/CROSS_CATEGORY_FINDINGS.csv"), "finding_id")
    handoff = keyed(data("E/PHASE2_HANDOFF.csv"), "finding_id")
    limited = keyed(data("runtime_followup/LIMITED_FINDINGS.csv"), "finding_id")
    assert (len(categories), len(findings)) == (9, 21)
    assert all((r["category"],) in categories for r in findings.values())
    assert findings.keys() == handoff.keys()
    assert all(all(handoff[k][col] == value for col, value in row.items())
               for k, row in findings.items())
    assert limited.keys() == {k for k, row in findings.items()
                              if row["classification"] == "UNVERIFIED_OR_COUNTEREXAMPLE"}
    disposition = Counter(r["disposition"] for r in handoff.values())
    assert disposition == {"CANDIDATE_REQUIRES_REVIEW": 14, "SCOPE_LIMIT_ONLY": 7}
    parents = keyed(data("D/PARENT_EXCEPTIONS.csv"), "model_key")
    state = keyed(data("D/STATE_EXCEPTIONS.csv"), "state_id", "selector", "rule_index", "option_index")
    assert len(parents) == 48 and len(state) == 6
    assert sum(not r["model_key"] for r in state.values()) == 4
    exposure = keyed(data("D/TEXTURE_EXPOSURE.csv"), "texture_id")
    atlas = keyed(data("runtime_followup/ATLAS_READBACK.csv"), "texture_id")
    r10 = keyed(data("runtime_followup/R10_TEXTURE_DISPLAY.csv"), "texture_id")
    assert len(exposure) == len(atlas) == 85 and exposure.keys() == atlas.keys()
    assert sum(r["actual"] == "minecraft:missingno" for k, r in atlas.items()
               if exposure[k]["finding"].startswith("MISSING_")) == 8
    assert r10.keys() == {key for key, row in exposure.items() if row["finding"].startswith("DECLARATION_")}
    assert len(r10) == 77 and all(r["result"] == "VERIFIED" for r in r10.values())
    assert (sum(bool(r["observed_item_display_ids"]) for r in r10.values()),
            sum(bool(r["break_particle_blocks_and_counts"]) for r in r10.values())) == (58, 19)
    planned = keyed(data("D/RUNTIME_CHECKS.csv"), "test_id")
    actual = keyed(data("runtime_followup/RUNTIME_VERIFICATION.csv"), "test_id")
    assert planned.keys() == actual.keys() == {(f"R{i:02}",) for i in range(1, 11)}
    assert all(r["status"] == "PASS" and not r["remaining_conditions"] for r in actual.values())
    for row in data("runtime_followup/WORLD_READBACK.csv"):
        assert (row["test_id"],) in actual
        assert (PHASE / "runtime_followup" / row["evidence"]).is_file()
    return dict(categories=len(categories), findings=len(findings), parent_exceptions=len(parents),
                state_exceptions=len(state), textures=len(exposure), runtime_passed=len(actual),
                runtime_r10_verified=len(r10), handoff=dict(disposition))


def runtime_replay(work):
    results = {}
    for version in VERSIONS:
        for stub, replay in (("ENGINE_", "comparison-"), ("R10_ENGINE_", "R10-")):
            expected = lzma.decompress((PHASE / f"runtime_followup/{stub}{version}.tsv.xz").read_bytes())
            raw = (work / f"{replay}{version}.tsv").read_bytes()
            original, fresh = (tabular(b, "\t") for b in (expected, raw))
            for capture in (original, fresh):
                keyed(capture, "kind", "case", "key")
            if stub == "ENGINE_" and version == "1.21.1":
                changed = {"ITEM_HAMMER", "ITEM_WHITE_CUSHION"}
                def is_item_face(row):
                    return row["kind"] == "QUAD" and row["case"] in changed and row["key"].startswith("unculled/")
                assert [r for r in original if not is_item_face(r)] == [r for r in fresh if not is_item_face(r)]
                for case in changed:
                    signature = lambda rows: Counter(r["value"] for r in rows if is_item_face(r) and r["case"] == case)
                    assert signature(original) == signature(fresh), case
            else:
                assert raw == expected, (stub, version)
            results[f"{stub}{version}"] = {
                "rows": len(fresh), "sha256": hashlib.sha256(raw).hexdigest(), "byte_equal": raw == expected,
                "changed_ordinals": sum(a != b for a, b in zip(original, fresh, strict=True)),
            }
    return results


def remote_manifest(remote, output):
    assert git("rev-parse", remote).decode().strip() == BASELINE
    scope = PHASE.relative_to(ROOT).as_posix()
    tree = git("ls-tree", "-r", BASELINE, "--", scope, *SUPPORT).decode().splitlines()
    records = []
    for line in tree:
        entry, path = line.split("\t", 1)
        sha = entry.split()[2]
        raw = git("cat-file", "blob", sha)
        assert hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest() == sha
        local = ROOT / path
        if local.is_file() and path != "handoff/STATE.json":
            assert local.read_bytes() == raw, path
        logical = path.removesuffix(".xz")
        count = ""
        if logical.endswith((".csv", ".tsv")):
            decoded = lzma.decompress(raw) if path.endswith(".xz") else raw
            count = len(tabular(decoded, "\t" if logical.endswith(".tsv") else ","))
        records.append((path, sha, hashlib.sha256(raw).hexdigest(), len(raw), count))
    assert {r[0] for r in records}.issuperset(SUPPORT)
    with (output / "REMOTE_INPUT_MANIFEST.csv").open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, lineterminator="\n")
        writer.writerow(("path", "git_blob_sha1", "sha256", "bytes", "data_rows"))
        writer.writerows(records)
    return len(records), sum(row[-1] != "" for row in records)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--replay", required=True, type=Path)
    parser.add_argument("--vanilla", required=True, type=Path)
    parser.add_argument("--remote-ref", default="FETCH_HEAD")
    parser.add_argument("--out", type=Path, default=HERE)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    count = sum(map(len, REPLAY_FILES.values()))
    for stage, files in REPLAY_FILES.items():
        for file in files:
            assert (args.replay / stage / file).read_bytes() == (PHASE / stage / file).read_bytes(), (stage, file)
    with sqlite3.connect(":memory:") as db:
        db.deserialize(lzma.decompress((PHASE / "E/comparison.sqlite.xz").read_bytes()))
        assert db.execute("PRAGMA integrity_check").fetchall() == [("ok",)]
        assert not db.execute("PRAGMA foreign_key_check").fetchall()
    captures = list((PHASE / "runtime_followup/evidence").glob("*"))
    for path in captures:
        with Image.open(path) as image:
            image.verify()
    state = json.loads(git("show", f"{BASELINE}:handoff/STATE.json"))
    one_two_approved = state["phase_1_2_G_final_exit"]["whole_stage_1_2_exit_separately_reviewed_and_approved"]
    one_four = json.loads(git("show", f"{BASELINE}:{SUPPORT[-1]}"))
    assert one_four["status"] == "PASS_PHASE_1_4_SOURCE_SCOPE"
    result = dict(status="PASS_1_5_FIXED_COMPARISON_SCOPE", baseline=BASELINE,
                  vanilla_assets_rehashed=compare_sources(args.vanilla), comparison=comparison_keys(),
                  findings=findings_and_exceptions(), exact_static_replay_files=count, world_images_checked=len(captures),
                  runtime_captures=runtime_replay(args.replay), comparison_sqlite_integrity="ok",
                  prerequisite_1_4_f=one_four["status"], prerequisite_1_2_whole_approved=one_two_approved,
                  phase_1_closure="PENDING_1_2_WHOLE_REVIEW" if not one_two_approved else "ELIGIBLE_FOR_FINAL_REVIEW")
    result["remote_blobs"], result["remote_tabular_files"] = remote_manifest(args.remote_ref, args.out)
    (args.out / "EXIT_AUDIT.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    main()
