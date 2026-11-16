"""Independent source and provenance reconciliation for the fixed Entry3 batch."""
import csv
import hashlib
import json
import subprocess
from collections import Counter, defaultdict
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "research/vanilla_models/phase_1-2-C"
OUT = BASE / "entry3"


def csvrows(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    tree = subprocess.check_output(["git", "ls-tree", "-r", "HEAD"], cwd=ROOT, text=True)
    git = {line.split("\t", 1)[1]: line.split()[2] for line in tree.splitlines()}
    manifest = {r["full_source_path"]: r for r in csvrows(BASE / "C_FIXED_SCOPE_2390.csv")}
    selection = json.loads((OUT / "C_SELECTION.json").read_text())
    models = csvrows(OUT / "MODEL_SOURCE_EVIDENCE.csv")
    faces = csvrows(OUT / "FACE_UV_EVIDENCE.csv")
    bindings = csvrows(OUT / "TEXTURE_BINDINGS.csv")
    pngs = csvrows(OUT / "PNG_RGBA_EVIDENCE.csv")
    mcmeta = csvrows(OUT / "PNG_MCMETA_SOURCE.csv")
    unresolved = csvrows(OUT / "UNRESOLVED.csv")
    templates = csvrows(OUT / "UNBOUND_TEMPLATE_EVIDENCE.csv")
    history = csvrows(OUT / "SELECTED_P1_PRIOR_C_FIELDS.csv")
    previous = set()
    prior_png = set()
    for name in ("entry1", "entry2"):
        previous.update(r["leaf_path"] for r in csvrows(BASE / name / "MODEL_SOURCE_EVIDENCE.csv"))
        prior_png.update(r["png_path"] for r in csvrows(BASE / name / "PNG_RGBA_EVIDENCE.csv"))
    assert len(models) == 732 and len(selection["models"]) == 732
    assert not previous.intersection(r["leaf_path"] for r in models)
    assert Counter(r["priority"] for r in models) == {"P1": 155, "P2": 332, "P3": 245}
    assert {r["leaf_path"] for r in models} == {r["path"] for r in selection["source_path_sha"]}
    for r in models:
        entry = manifest[r["leaf_path"]]
        assert entry["C_assignment"] == "ENTRY3" and entry["git_blob_sha"] == r["leaf_sha"]
        chain = json.loads(r["parent_chain"])
        assert len(chain) == len({x["path"] for x in chain})
        assert chain[0] == {"path": r["leaf_path"], "sha": r["leaf_sha"]}
        assert all(git[x["path"]] == x["sha"] for x in chain)
        assert git[r["geometry_path"]] == r["geometry_sha"]
    declared = {}
    for r in models:
        geometry = json.loads((ROOT / r["geometry_path"]).read_text())
        n = sum(len(e.get("faces", {})) for e in geometry["elements"])
        assert n == int(r["face_count"])
        declared[r["model"]] = (geometry, r)
    assert len(faces) == sum(int(r["face_count"]) for r in models) == 7317
    assert len({(r["model"], r["element_index"], r["direction"]) for r in faces}) == 7317
    for r in faces:
        g, model = declared[r["model"]]
        face = g["elements"][int(r["element_index"])]["faces"][r["direction"]]
        assert r["geometry_path"] == model["geometry_path"] and r["geometry_sha"] == model["geometry_sha"]
        assert r["face_texture"] == face["texture"]
        assert r["uv_type"] == ("explicit_source" if "uv" in face else "implicit_source_absent")
        assert (json.loads(r["original_uv"]) if r["original_uv"] else None) == face.get("uv")
        assert r["face_rotation_original"] == (str(face["rotation"]) if "rotation" in face else "")
        if r["texture_status"] == "resolved":
            assert r["png_path"] in git and r["resolved_texture"].startswith("minecraft:")
        else:
            assert r["texture_status"] == "missing_slot"
    assert len(bindings) == 2802
    assert len(pngs) == 574 and len({r["png_path"] for r in pngs}) == 574
    for r in pngs:
        assert git[r["png_path"]] == r["png_sha"]
        with Image.open(ROOT / r["png_path"]) as im:
            rgba = im.convert("RGBA")
            count = Counter(v[3] for v in rgba.get_flattened_data())
            assert hashlib.sha256(rgba.tobytes()).hexdigest() == r["rgba_sha256"]
            assert (im.width, im.height) == (int(r["width"]), int(r["height"]))
            assert (count[0], count[255], sum(n for a, n in count.items() if 0 < a < 255)) == (
                int(r["transparent_pixels"]), int(r["opaque_pixels"]), int(r["partial_alpha_pixels"]))
    assert len(mcmeta) == 46 and all(git[r["mcmeta_path"]] == r["mcmeta_sha"] for r in mcmeta)
    assert all(r["png_path"] + ".mcmeta" == r["mcmeta_path"] for r in mcmeta)
    counts = Counter(r["model"] for r in unresolved)
    assert len(unresolved) == 427 and len(counts) == len(templates) == 50
    assert all(r["issue"] == "missing_slot" for r in unresolved)
    assert {r["model"] for r in templates} == set(counts)
    assert all(git[r["source_path"]] == r["source_sha"] and int(r["unbound_face_refs"]) == counts[r["model"]]
               and int(r["direct_children"]) > 0 and git.get(r["example_child"]) for r in templates)
    v69 = {r["source_path"]: r for r in csvrows(ROOT / "research/vanilla_models/v69/07_P1_544_EVIDENCE_LEDGER.csv")}
    assert len(history) == 155 and all(v69[r["source_path"]]["source_git_blob_sha"] == r["source_sha"] for r in history)
    result = {"schema": "C_ENTRY3_INDEPENDENT_AUDIT", "baseline_remote_head": selection["base_head"],
              "fixed_manifest_leaf_sha_and_parent_chains": 732, "applied_faces_recomputed": 7317,
              "explicit_uv": sum(r["uv_type"] == "explicit_source" for r in faces),
              "implicit_uv_key_absent": sum(r["uv_type"] == "implicit_source_absent" for r in faces),
              "binding_rows": len(bindings), "png_blob_and_RGBA_redecoded": len(pngs),
              "png_new_vs_entry1_2": len({r["png_path"] for r in pngs} - prior_png),
              "cumulative_unique_png": len({r["png_path"] for r in pngs} | prior_png),
              "mcmeta_source_sha_checked": len(mcmeta), "template_unbound_faces": len(unresolved),
              "template_models_with_children": len(templates), "P1_v69_identity_and_columns": len(history),
              "Entry1_2_leaf_overlap": 0, "result": "PASS",
              "limits": "Source-level UV and full PNG sheets only; historic field values not independently certified as C-complete; engine implicit UV and animation playback unverified."}
    (OUT / "C_ENTRY3_INDEPENDENT_AUDIT.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
