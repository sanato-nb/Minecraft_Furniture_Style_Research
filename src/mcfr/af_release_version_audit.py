"""Compare pinned Another Furniture 4.0.2 JAR with fixed 4.0.3 research Git source.

Only asset metadata and diffs leave the scratch directory. The copyrighted
original JAR, JSON, model files and texture PNGs are NEVER checked into Git.
A byte difference alone is NOT evidence of geometry/UV change or role approval.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
import runpy
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from zipfile import ZipFile

from .chair_runtime_fixture import digest_bytes

ROOT = Path(__file__).resolve().parents[2]
UPSTREAM = "57eb624cbb7f408d43398c7434b0d38d312cb55d"
PREFIX = "assets/another_furniture/"
SOURCE_PREFIX = "common/src/main/resources/"
RESOURCE = "blockstates/acacia_chair.json"
EXPECTED_SOURCE_BLOB = "37643398d7a49fdcfc6f2308ca04c13fb0b43aed"
PINNED_PARENT_BLOBS = {
    "models/block/template/chair.json": "d9b64a818021f1a64b0cba13d16d18d6fea65d01",
    "models/block/template/chair_tucked.json": "ebcd7af6545ada207ad31720cb831b9ec5eb1dde",
}
RUNNING_JAR_NAME = "another_furniture-fabric-4.0.2.jar"
DIRS = ("north", "east", "south", "west")


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def model_path(resource):
    if not resource.startswith("another_furniture:block/"):
        return None
    tail = resource.split(":", 1)[1]
    if ".." in tail or tail.startswith("/"):
        raise ValueError("Invalid model source path")
    return "models/" + tail + ".json"


def fetch_research(relative):
    if not relative.startswith(("models/", "blockstates/")) or ".." in relative:
        raise ValueError("Invalid research file path")
    url = ("https://raw.githubusercontent.com/crispytwig/AnotherFurniture/"
           + UPSTREAM + "/" + SOURCE_PREFIX + PREFIX + relative)
    request = Request(url, headers={"User-Agent": "MCFR-source-pinned-release-audit/1.0"})
    try:
        with urlopen(request, timeout=35) as response:
            return response.read()
    except HTTPError as exc:
        if exc.code == 404:
            return None
        raise


def sha1(blob):
    return hashlib.sha1(blob).hexdigest()


def original_jar(work):
    # Reuse the existing runtime dependency pin and verified downloader.
    module = runpy.run_path(str(ROOT / "research/furniture_mods/phase_1-3/runtime_actions/run_probe.py"))
    mods = [item for item in module["MODS"]["1.21.1"]
            if item[0].split("/")[-1] == RUNNING_JAR_NAME]
    if len(mods) != 1:
        raise ValueError("Runtime pin for AF 4.0.2 changed or disappeared")
    locator, expected = mods[0]
    jar_path = work / RUNNING_JAR_NAME
    module["download"]("https://cdn.modrinth.com/data/" + locator, jar_path, expected)
    if sha1(jar_path.read_bytes()) != expected:
        raise ValueError("Original Modrinth AF 4.0.2 SHA-1 mismatch")
    return jar_path, expected


def compare_variant(src, jar):
    s, r = src["variants"], jar["variants"]
    rows = []
    for key in sorted(set(s) | set(r)):
        study, runtime = s.get(key), r.get(key)
        status = ("STUDY_ONLY" if runtime is None else
                  "RUNTIME_ONLY" if study is None else
                  "SAME" if canonical(study) == canonical(runtime) else
                  "CHANGED")
        rows.append({"selector": key, "status": status,
                     "study_model": study.get("model", "") if isinstance(study, dict) else "",
                     "runtime_model": runtime.get("model", "") if isinstance(runtime, dict) else "",
                     "study_y": study.get("y", 0) if isinstance(study, dict) else "",
                     "runtime_y": runtime.get("y", 0) if isinstance(runtime, dict) else "",
                     "study_rule": canonical(study) if study is not None else "",
                     "runtime_rule": canonical(runtime) if runtime is not None else ""})
    return rows


def effective(path, docs):
    # For the same namespaced model, parents supply elements, textures and
    # material settings. Minecraft built-in parents are outside comparison.
    chain = []
    seen = set()
    current = path
    while current is not None:
        if current in seen:
            raise ValueError("Circular parent chain " + current)
        seen.add(current)
        item = docs.get(current)
        if item is None:
            raise ValueError("Missing original parent model " + current)
        chain.append(item)
        current = model_path(item.get("parent", ""))
    chain.reverse()
    textures = {}
    elements = None
    render_type = None
    ao = None
    for item in chain:
        textures.update(item.get("textures", {}))
        if "elements" in item:
            elements = item["elements"]
        if "render_type" in item:
            render_type = item["render_type"]
        if "ambientocclusion" in item:
            ao = item["ambientocclusion"]
    if elements is None:
        raise ValueError("No original elements found for " + path)

    def resolved(slot):
        if not isinstance(slot, str):
            return slot
        seen_slots = set()
        while slot.startswith("#"):
            name = slot[1:]
            if name in seen_slots:
                return {"texture_cycle": name}
            seen_slots.add(name)
            if name not in textures:
                return {"unbound_texture_slot": name}
            slot = textures[name]
        return slot

    geometry = []
    uv = []
    bindings = []
    for element in elements:
        geometry.append({key: element[key] for key in ("from", "to", "rotation", "shade")
                         if key in element})
        uv.append({face: {key: data[key] for key in ("uv", "rotation") if key in data}
                   for face, data in sorted(element.get("faces", {}).items())})
        bindings.append({face: {"texture": resolved(data.get("texture")),
                                **{key: data[key] for key in ("tintindex", "cullface")
                                   if key in data}}
                         for face, data in sorted(element.get("faces", {}).items())})
    return {"geometry": geometry, "uv": uv, "face_bindings": bindings,
            "effective_textures": textures, "render_type": render_type,
            "ambientocclusion": ao, "element_count": len(elements),
            "face_count": sum(len(x.get("faces", {})) for x in elements)}


def write_csv(path, rows, columns):
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def audit(work, out):
    work.mkdir(parents=True, exist_ok=True)
    out.mkdir(parents=True, exist_ok=True)
    jar_path, jar_sha = original_jar(work)
    with ZipFile(jar_path) as zf:
        contents = set(zf.namelist())
        def runtime(relative):
            filename = PREFIX + relative
            return zf.read(filename) if filename in contents else None

        research_blockstate = fetch_research(RESOURCE)
        runtime_blockstate = runtime(RESOURCE)
        if not research_blockstate or not runtime_blockstate:
            raise ValueError("Pinned original 4.0.3 or 4.0.2 blockstate missing")
        if digest_bytes(research_blockstate, "GIT_BLOB_SHA1") != EXPECTED_SOURCE_BLOB:
            raise ValueError("4.0.3 source commit is not the pinned original blockstate")
        s = json.loads(research_blockstate.decode("utf-8-sig"))
        r = json.loads(runtime_blockstate.decode("utf-8-sig"))
        if set(s) != {"variants"} or set(r) != {"variants"}:
            raise ValueError("Unexpected nonstatic blockstate representation")
        variants = compare_variant(s, r)
        if len(s["variants"]) != 88 or len(variants) < 88:
            raise ValueError("Research 4.0.3 source option coverage incomplete")

        selected = [x for x in variants if
                    any(("facing=" + facing) in x["selector"] for facing in DIRS)
                    and (("tucked=false,variant=1" in x["selector"]) or
                         ("tucked=true,variant=10" in x["selector"]))]
        if len(selected) != 8 or any(x["status"] not in ("SAME", "CHANGED") for x in selected):
            raise ValueError("The eight earlier in-game AF states disappeared")

        targets = {entry["model"] for obj in (s, r)
                   for entry in obj["variants"].values()
                   if isinstance(entry, dict) and isinstance(entry.get("model"), str)}
        direct = {model_path(t) for t in targets}
        if None in direct:
            raise ValueError("Unexpected non-AF model target in chair options")
        queued = list(sorted(direct | set(PINNED_PARENT_BLOBS)))
        bytes_by_side = {"study": {}, "runtime": {}}
        docs = {"study": {}, "runtime": {}}
        missing = []
        while queued:
            path = queued.pop()
            if path in bytes_by_side["study"]:
                continue
            a, b = fetch_research(path), runtime(path)
            for side, blob in (("study", a), ("runtime", b)):
                bytes_by_side[side][path] = blob
                if blob is None:
                    missing.append({"side": side, "model": path})
                    continue
                try:
                    doc = json.loads(blob.decode("utf-8-sig"))
                except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                    raise ValueError(side + " model JSON invalid: " + path) from exc
                docs[side][path] = doc
                par = model_path(doc.get("parent", ""))
                if par is not None and par not in bytes_by_side["study"]:
                    queued.append(par)

        for path, expected in PINNED_PARENT_BLOBS.items():
            if digest_bytes(bytes_by_side["study"][path], "GIT_BLOB_SHA1") != expected:
                raise ValueError("Pinned 4.0.3 parent model SHA mismatch: " + path)

        models = []
        for path in sorted(bytes_by_side["study"]):
            a, b = bytes_by_side["study"][path], bytes_by_side["runtime"].get(path)
            models.append({
                "path": path, "kind": "STATE_TARGET" if path in direct else "PARENT",
                "study_blob_sha1": digest_bytes(a, "GIT_BLOB_SHA1") if a is not None else "",
                "runtime_blob_sha1": digest_bytes(b, "GIT_BLOB_SHA1") if b is not None else "",
                "byte_equal": a == b if a is not None and b is not None else None,
                "json_equal": docs["study"].get(path) == docs["runtime"].get(path)
                if a is not None and b is not None else None,
            })
        effective_rows = []
        for path in sorted(direct):
            try:
                left = effective(path, docs["study"])
                right = effective(path, docs["runtime"])
                effective_rows.append({
                    "model": path,
                    "geometry_equal": left["geometry"] == right["geometry"],
                    "uv_equal": left["uv"] == right["uv"],
                    "face_bindings_equal": left["face_bindings"] == right["face_bindings"],
                    "render_type_equal": left["render_type"] == right["render_type"],
                    "element_count_study": left["element_count"],
                    "element_count_runtime": right["element_count"],
                    "face_count_study": left["face_count"],
                    "face_count_runtime": right["face_count"],
                    "status": "FULLY_EVALUATED",
                })
            except ValueError as exc:
                effective_rows.append({"model": path, "status": "INCOMPLETE_PARENT_CHAIN",
                                       "diagnostic": str(exc)})
        summary = {
            "schema": "MCFR_INT3_AF402_AF403_COMPARISON/v1",
            "research": {"release": "4.0.3", "git_commit": UPSTREAM,
                         "blockstate_git_blob_sha1": EXPECTED_SOURCE_BLOB},
            "runtime": {"release": "4.0.2", "jar_name": RUNNING_JAR_NAME,
                        "jar_sha1": jar_sha,
                        "blockstate_git_blob_sha1":
                            digest_bytes(runtime_blockstate, "GIT_BLOB_SHA1")},
            "states": {"study": len(s["variants"]), "runtime": len(r["variants"]),
                       "union": len(variants),
                       "same": sum(x["status"] == "SAME" for x in variants),
                       "changed": sum(x["status"] == "CHANGED" for x in variants),
                       "study_only": sum(x["status"] == "STUDY_ONLY" for x in variants),
                       "runtime_only": sum(x["status"] == "RUNTIME_ONLY" for x in variants),
                       "previously_captured_eight_present_in_both": len(selected)},
            "models": {"direct_target_union": len(direct),
                       "all_with_transitive_parents": len(models),
                       "missing_source_assets": missing,
                       "byte_identical": sum(x["byte_equal"] is True for x in models),
                       "json_identical": sum(x["json_equal"] is True for x in models),
                       "evaluated": sum(x["status"] == "FULLY_EVALUATED" for x in effective_rows),
                       "geometry_changed": sum(x.get("geometry_equal") is False for x in effective_rows),
                       "uv_changed": sum(x.get("uv_equal") is False for x in effective_rows),
                       "face_bindings_changed": sum(x.get("face_bindings_equal") is False for x in effective_rows)},
            "boundary": {"part_roles_approved": 0, "runtime_game_screenshot_proven": False,
                         "material_style_approved": 0, "ai_training_rights_approved": 0,
                         "unmodified_original_research": True},
        }
        summary["status"] = ("COMPLETE_VERSION_DIFF_RECORDED_NOT_SEMANTIC_APPROVAL"
                             if not missing and summary["models"]["evaluated"] == len(direct)
                             else "INCOMPLETE_MISSING_OR_UNRESOLVED_SOURCE")
    write_csv(out / "blockstate_options.csv", variants,
              ["selector", "status", "study_model", "runtime_model",
               "study_y", "runtime_y", "study_rule", "runtime_rule"])
    write_csv(out / "model_json_sha.csv", models,
              ["path", "kind", "study_blob_sha1", "runtime_blob_sha1",
               "byte_equal", "json_equal"])
    write_csv(out / "model_effective_geometry_uv.csv", effective_rows,
              ["model", "status", "geometry_equal", "uv_equal", "face_bindings_equal",
               "render_type_equal", "element_count_study", "element_count_runtime",
               "face_count_study", "face_count_runtime", "diagnostic"])
    summary["evidence_sha256"] = {
        path.name: hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(out.glob("*.csv"))
    }
    (out / "AF_VERSION_COMPARISON.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    return summary


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--work", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    if args.output.exists():
        p.error("Specify a new output directory to avoid evidence overwrite")
    result = audit(args.work, args.output)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    if result["status"] != "COMPLETE_VERSION_DIFF_RECORDED_NOT_SEMANTIC_APPROVAL":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
