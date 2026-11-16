"""Independently reconcile Entry2 face, source, PNG and history rows."""
import csv
import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "research/vanilla_models/phase_1-2-C/entry2"


def rows(name):
    with (OUT / name).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    tree = subprocess.check_output(["git", "ls-tree", "-r", "HEAD"], cwd=ROOT, text=True)
    shas = {line.split("\t", 1)[1]: line.split()[2] for line in tree.splitlines()}
    models, faces, pngs, bindings = (rows(x) for x in (
        "MODEL_SOURCE_EVIDENCE.csv", "FACE_UV_EVIDENCE.csv", "PNG_RGBA_EVIDENCE.csv", "TEXTURE_BINDINGS.csv"))
    crosswalk, prior, unbound = (rows(x) for x in (
        "HISTORICAL_C_CROSSWALK_P1_544.csv", "SELECTED_P1_PRIOR_C_FIELDS.csv", "UNBOUND_TEMPLATE_EVIDENCE.csv"))
    selection = json.loads((OUT / "C_SELECTION.json").read_text())
    assert len(models) == len(selection["models"]) == len(set(selection["models"])) == 96
    assert {r["model"] for r in models} == set(selection["models"])
    assert len({r["geometry_path"] for r in models}) == 91
    for priority, count in (("P1", 24), ("P2", 36), ("P3", 36)):
        assert len({r["geometry_path"] for r in models if r["priority"] == priority}) == count
    with (OUT.parent / "entry1/MODEL_SOURCE_EVIDENCE.csv").open() as f:
        old = {r["model"] for r in csv.DictReader(f)}
    assert not old.intersection(selection["models"])
    by_model = {r["model"]: r for r in models}
    for r in models:
        assert shas[r["leaf_path"]] == r["leaf_sha"]
        chain = json.loads(r["parent_chain"])
        assert chain[0] == {"path": r["leaf_path"], "sha": r["leaf_sha"]}
        assert len({x["path"] for x in chain}) == len(chain)
        assert all(shas[x["path"]] == x["sha"] for x in chain)
        source = json.loads((ROOT / r["geometry_path"]).read_text())
        assert sum(len(e.get("faces", {})) for e in source["elements"]) == int(r["face_count"])
    assert len(faces) == sum(int(r["face_count"]) for r in models)
    assert len({(r["model"], r["element_index"], r["direction"]) for r in faces}) == len(faces)
    for r in faces:
        source = json.loads((ROOT / r["geometry_path"]).read_text())
        face = source["elements"][int(r["element_index"])]["faces"][r["direction"]]
        assert shas[r["geometry_path"]] == r["geometry_sha"]
        assert r["face_texture"] == face["texture"]
        assert r["uv_type"] == ("explicit_source" if "uv" in face else "implicit_source_absent")
        assert (json.loads(r["original_uv"]) if r["original_uv"] else None) == face.get("uv")
        if r["texture_status"] == "resolved":
            assert r["png_path"] in shas
    for r in pngs:
        assert shas[r["png_path"]] == r["png_sha"]
        with Image.open(ROOT / r["png_path"]) as im:
            rgba = im.convert("RGBA")
            pixels = list(rgba.get_flattened_data())
            alpha = Counter(p[3] for p in pixels)
            assert hashlib.sha256(rgba.tobytes()).hexdigest() == r["rgba_sha256"]
            assert (im.width, im.height) == (int(r["width"]), int(r["height"]))
            assert (alpha[0], alpha[255], sum(n for a, n in alpha.items() if 0 < a < 255)) == (
                int(r["transparent_pixels"]), int(r["opaque_pixels"]), int(r["partial_alpha_pixels"]))
    assert len(crosswalk) == 544 and len({r["source_path"] for r in crosswalk}) == 544
    assert len(prior) == 24
    v69 = {r["source_path"]: r for r in csv.DictReader((ROOT / "research/vanilla_models/v69/07_P1_544_EVIDENCE_LEDGER.csv").open())}
    assert all((r["source_path"] in v69 and v69[r["source_path"]]["source_git_blob_sha"] == r["source_sha"])
               for r in crosswalk)
    assert len(unbound) == 7 and sum(int(r["face_unbound_slot_count"]) for r in unbound) == 81
    assert all(int(r["direct_children_count"]) > 0 and shas[r["source_path"]] == r["source_sha"] for r in unbound)
    assert sum(r["texture_status"] != "resolved" for r in faces) == 81
    result = {"schema": "C_ENTRY2_INDEPENDENT_AUDIT", "base_head": selection["base_head"],
              "model_chains_vs_git_tree": len(models), "face_rows_vs_source": len(faces),
              "slot_binding_rows": len(bindings), "unique_geometry_providers_across_priorities": 91,
              "png_blob_and_RGBA_checked": len(pngs),
              "P1_v69_identity_crosswalk": len(crosswalk), "P1_selected_prior_field_details": len(prior),
              "unbound_template_models": len(unbound), "unbound_face_refs": 81,
              "overlap_with_entry1": 0, "result": "PASS",
              "limit": "C history field presence is not prior semantic certification; no engine implicit UV authentication"}
    (OUT / "C_ENTRY2_INDEPENDENT_AUDIT.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
