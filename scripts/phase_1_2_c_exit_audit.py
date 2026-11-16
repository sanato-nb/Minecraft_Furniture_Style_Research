"""Independently audit the complete 1-2-C source scope before remote closure."""
import csv
import hashlib
import json
import re
import subprocess
from collections import Counter, defaultdict
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "research/vanilla_models/phase_1-2-C"
OUT = BASE / "entry5"


def rows(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def resolve(value, slots):
    seen = set()
    while True:
        key = value[1:] if value.startswith("#") else value
        if key in seen:
            return "cycle", ""
        if key not in slots:
            if value.startswith("#"):
                return "template_unbound", ""
            return "resolved", value if ":" in value else "minecraft:" + value
        seen.add(key)
        value = slots[key]


def main():
    tree = subprocess.check_output(["git", "ls-tree", "-r", "HEAD"], cwd=ROOT, text=True)
    git = {line.split("\t", 1)[1]: line.split()[2] for line in tree.splitlines()}
    original = rows(ROOT / "research/vanilla_models/phase_1-2-B/entry10/B_SCOPE_2390_STATUS.csv")
    assigned = rows(BASE / "C_FIXED_SCOPE_2390.csv")
    final = rows(OUT / "C_SCOPE_2390_FINAL_STATUS.csv")
    assert len(original) == len(assigned) == len(final) == 2390
    assert len({r["source_path"] for r in final}) == 2390
    by_path = {r["source_path"]: r for r in final}
    for b in original:
        path = b["full_source_path"]
        assert git[path] == b["git_blob_sha"] == by_path[path]["git_blob_sha"]
    count = Counter(r["C_assignment"] for r in final)
    assert count == {"ENTRY1": 12, "ENTRY2": 96, "ENTRY3": 732, "ENTRY4": 732, "ENTRY5": 732, "E_EXCEPTION": 86}
    all_model, all_face = {}, {}
    for entry in range(1, 6):
        folder = BASE / f"entry{entry}"
        for r in rows(folder / "MODEL_SOURCE_EVIDENCE.csv"):
            assert r["leaf_path"] not in all_model
            assert by_path[r["leaf_path"]]["C_assignment"] == f"ENTRY{entry}"
            assert git[r["leaf_path"]] == r["leaf_sha"]
            chain = json.loads(r["parent_chain"])
            assert chain[0] == {"path": r["leaf_path"], "sha": r["leaf_sha"]}
            assert len(chain) == len({x["path"] for x in chain})
            assert all(git[x["path"]] == x["sha"] for x in chain)
            all_model[r["leaf_path"]] = r
        for r in rows(folder / "FACE_UV_EVIDENCE.csv"):
            key = (r["leaf_path"], int(r["element_index"]), r["direction"])
            assert key not in all_face
            all_face[key] = (entry, r)
    assert len(all_model) == 2304 and len(all_face) == 23090
    assert sum(int(r["C_applied_faces"]) for r in final) == 23090
    assert sum(int(r["C_bound_png_face_refs"]) for r in final) == 21590
    status = Counter()
    for path, r in all_model.items():
        chain = json.loads(r["parent_chain"])
        sources = [(x["path"], json.loads((ROOT / x["path"]).read_text())) for x in chain]
        geometry_path, geometry = next((p, d) for p, d in sources if "elements" in d)
        assert geometry_path == r["geometry_path"] and git[geometry_path] == r["geometry_sha"]
        slots = {}
        for _, d in reversed(sources):
            slots.update(d.get("textures", {}))
        n = 0
        for ei, element in enumerate(geometry["elements"]):
            for direction, face in element.get("faces", {}).items():
                n += 1
                entry, saved = all_face[(path, ei, direction)]
                assert saved["geometry_path"] == geometry_path and saved["geometry_sha"] == r["geometry_sha"]
                assert saved["face_texture"] == face["texture"]
                assert (json.loads(saved["original_uv"]) if saved["original_uv"] else None) == face.get("uv")
                assert saved["uv_type"] == ("explicit_source" if "uv" in face else "implicit_source_absent")
                verdict, texture = resolve(face["texture"], slots)
                if verdict == "template_unbound":
                    assert saved["texture_status"] == "missing_slot"
                    status["template_unbound"] += 1
                elif path.endswith("/heavy_core.json"):
                    assert entry == 4 and saved["texture_status"] == "missing_png"
                    assert texture == "minecraft:block/heavy_core"
                    status["corrected_heavy_core"] += 1
                else:
                    assert verdict == "resolved" and saved["texture_status"] == "resolved"
                    assert saved["resolved_texture"] == texture
                    png_path = "1.21.11/assets/minecraft/textures/" + texture.removeprefix("minecraft:") + ".png"
                    assert saved["png_path"] == png_path and png_path in git
                    status["resolved_original"] += 1
        assert n == int(r["face_count"]) == int(by_path[path]["C_applied_faces"])
    assert status == {"resolved_original": 21584, "corrected_heavy_core": 6, "template_unbound": 1500}
    unbound = rows(OUT / "C_UNBOUND_TEMPLATE_ALL.csv")
    assert len(unbound) == len({r["source_path"] for r in unbound})
    assert sum(int(r["face_refs"]) for r in unbound) == 1500
    assert all(int(r["direct_children"]) > 0 and git[r["source_path"]] == r["source_sha"]
               and git.get(r["example_child"]) for r in unbound)
    correction = rows(OUT / "HEAVY_CORE_FACE_ERRATUM.csv")
    assert len(correction) == 6 and {r["direction"] for r in correction} == {"north", "south", "east", "west", "up", "down"}
    assert all(git[r["model_path"]] == r["model_sha"] and git[r["png_path"]] == r["png_sha"] for r in correction)
    assert all(git["1.21.11/hqp.class"] == r["client_slot_lookup_class_sha"] and
               git["1.21.11/iog.class"] == r["client_dispatch_class_sha"] for r in correction)
    bytecode = (OUT / "HEAVY_CORE_CLIENT_BYTECODE_EVIDENCE.txt").read_text()
    assert "java/util/Map.get" in bytecode and "java/lang/String.substring" in bytecode and "ifnull" in bytecode
    png = rows(OUT / "C_PNG_UNIQUE_ALL.csv")
    assert len(png) == len({r["png_path"] for r in png}) == 1073
    for r in png:
        assert git[r["png_path"]] == r["png_sha"]
        with Image.open(ROOT / r["png_path"]) as im:
            rgba = im.convert("RGBA")
            alpha = Counter(v[3] for v in rgba.get_flattened_data())
            assert hashlib.sha256(rgba.tobytes()).hexdigest() == r["rgba_sha256"]
            assert (im.width, im.height) == (int(r["width"]), int(r["height"]))
            assert alpha[0] == int(r["transparent_pixels"]) and alpha[255] == int(r["opaque_pixels"])
            assert sum(n for a, n in alpha.items() if 0 < a < 255) == int(r["partial_alpha_pixels"])
        if r["mcmeta_path"]:
            assert r["mcmeta_path"] == r["png_path"] + ".mcmeta" and git[r["mcmeta_path"]] == r["mcmeta_sha"]
    assert sum(bool(r["mcmeta_path"]) for r in png) == 97
    v69 = rows(ROOT / "research/vanilla_models/v69/07_P1_544_EVIDENCE_LEDGER.csv")
    history = rows(OUT / "C_HISTORICAL_P1_544_PROVENANCE.csv")
    assert len(history) == len(v69) == 544
    fields = [k for k in v69[0] if re.match(r"^v\d+_", k) and re.search(r"uv|texture|png|pixel|face_material", k, re.I)
              and not re.search(r"fully_|complete|certified|renderer|source_only", k, re.I)]
    hist_by_path = {r["source_path"]: r for r in history}
    for r in v69:
        path = r["source_path"]
        h = hist_by_path[path]
        assert git[path] == r["source_git_blob_sha"] == h["source_sha"]
        active = {k: r[k] for k in fields if r[k].strip() not in ("", "0", "false", "False", "no", "NO", "null", "None")}
        assert json.loads(h["prior_C_field_values_json"]) == active
        assert h["adopted_prior_C_semantics"] == "no_current_C_remeasures_source"
    protected = ["research/vanilla_models/v69/07_P1_544_EVIDENCE_LEDGER.csv",
                 "research/vanilla_models/v69/04_SOURCE_REVIEW_LEDGER_544.csv",
                 "research/vanilla_models/phase_1-2-A_completion/round1/A_ASSET_REGISTRY_4669.csv",
                 "research/vanilla_models/phase_1-2-B/entry10/B_SCOPE_2390_STATUS.csv"]
    assert all(subprocess.check_output(["git", "rev-parse", "HEAD:" + p], cwd=ROOT, text=True).strip() == git[p]
               for p in protected)
    audit = dict(schema="C_ENTRY5_INDEPENDENT_SOURCE_EXIT_AUDIT", baseline_remote_head="efedcdbee50d53ee9f4c7c5b7208d496fa07ed59",
                 model_identity_and_source_sha=2390, direct_models=2304, E_exceptions=86,
                 original_applied_faces=23090, explicit_uv_faces=sum(r[1]["uv_type"] == "explicit_source" for r in all_face.values()),
                 implicit_uv_key_absent_faces=sum(r[1]["uv_type"] == "implicit_source_absent" for r in all_face.values()),
                 resolved_face_refs_after_erratum=21590, verified_template_unbound_face_refs=1500,
                 corrected_heavy_core_face_refs=6, unexplained_face_refs=0,
                 unique_png_full_RGBA_and_git_sha=1073,
                 unique_png_pixels=sum(int(r["width"]) * int(r["height"]) for r in png),
                 mcmeta_sha_checked=97, v69_prior_P1_path_sha_and_field_values=544,
                 protected_files_unchanged_vs_HEAD=len(protected),
                 gates_before_remote_readback={"C1": "PASS_SOURCE_PROVENANCE", "C2": "PASS_SOURCE_FACE_SLOTS",
                                              "C3": "PASS_SOURCE_PNG_RGBA", "C4": "PENDING_REMOTE_READBACK"},
                 result="SOURCE_AUDIT_PASS_REMOTE_PENDING",
                 limits="No official-distribution JAR authentication, runtime rendering, implicit engine UV calculation, blockstate composition or animation playback claim.")
    (OUT / "C_ENTRY5_INDEPENDENT_SOURCE_EXIT_AUDIT.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(audit, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
