#!/usr/bin/env python3
"""Offline verifier for v15: rederive model geometry numbers from research CSVs.

Requires only Python 3 standard library and THIS research repository.
It deliberately does not fetch or redistribute copyrighted JSON/PNG/JAR assets.
This script validates derived-record consistency, NOT official game rendering.
"""
from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from pathlib import Path
from statistics import median

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "research" / "furniture_mods"

def read_rows(rel: str) -> list[dict[str, str]]:
    with (MOD / rel).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))

def n(r: dict, key: str) -> int:
    return int(r[key])

def outside_bbox(text: str) -> tuple[bool, str] | None:
    if not text:
        return None
    bounds = text.split(";")
    if len(bounds) != 3:
        raise AssertionError("bbox should have exactly three axes")
    axes = []
    for axis, raw in zip("xyz", bounds):
        lo, hi = (float(z) for z in raw.split(":"))
        if lo < 0 or hi > 16:
            axes.append(axis)
    return bool(axes), "".join(axes)

def metrics_for_source(r: dict, mod: str) -> dict:
    if mod == "Handcrafted":
        name, category, element_count, face_count = r["n"], r["n"].split("/")[0], n(r,"els"), n(r,"faces")
        rotated, flat, bbox = n(r,"rot"), n(r,"flat"), r["a"]
        sha, path = r["sha"], r["path"]
    else:
        name, category, element_count, face_count = r["name"], r["name"].split("_")[0], n(r,"elements"), n(r,"faces")
        rotated, flat, bbox = n(r,"rotated"), n(r,"flat"), r["bbox"]
        sha, path = r["sha"], r["path"]
    assert 0 <= rotated <= element_count and 0 <= flat <= element_count
    assert 0 <= face_count <= 6 * element_count
    return dict(
        mod=mod, source_model=name, category=category, source_git_sha=sha, source_path=path,
        elements=element_count, declared_faces=face_count, possible_face_slots=6*element_count,
        undeclared_face_slots=6*element_count-face_count,
        rotated_elements=rotated, flat_elements=flat, bbox=bbox,
        bbox_eval=outside_bbox(bbox))

def main() -> None:
    hc = [metrics_for_source(r, "Handcrafted") for r in read_rows("v12/handcrafted_authored_120_total.csv")]
    af = [metrics_for_source(r, "Another Furniture") for r in read_rows("v11/template_metrics_69_total.csv")]
    assert len(hc) == 120 and len(af) == 69

    def aggregate(rows: list[dict]) -> dict:
        active = [r for r in rows if r["elements"] > 0]
        sm = lambda k: sum(r[k] for r in rows)
        vals = dict(
            models=len(rows), authored_nonempty_models=len(active), empty_models=len(rows)-len(active),
            element_total=sm("elements"), declared_face_total=sm("declared_faces"),
            possible_face_slots=sm("possible_face_slots"), face_slots_not_declared=sm("undeclared_face_slots"),
            rotated_elements=sm("rotated_elements"), flat_elements=sm("flat_elements"),
            models_with_rotation=sum(r["rotated_elements"]>0 for r in active),
            models_with_flat_elements=sum(r["flat_elements"]>0 for r in active),
            models_with_all_six_faces_declared=sum(r["declared_faces"]==r["possible_face_slots"] for r in active),
            models_with_partial_face_declarations=sum(r["declared_faces"]<r["possible_face_slots"] for r in active),
            nonempty_models_with_bbox_evidence=sum(r["bbox_eval"] is not None for r in active),
            nonempty_models_with_bbox_outside_0_16=sum(r["bbox_eval"] is not None and r["bbox_eval"][0] for r in active),
        )
        for axis in "xyz":
            vals[f"models_with_outside_bbox_{axis}"] = sum(
                r["bbox_eval"] is not None and axis in r["bbox_eval"][1] for r in active)
        vals["face_declaration_pct"]=round(100*vals["declared_face_total"]/vals["possible_face_slots"],2)
        vals["rotated_elements_share_pct"]=round(100*vals["rotated_elements"]/vals["element_total"],2)
        vals["flat_elements_share_pct"]=round(100*vals["flat_elements"]/vals["element_total"],2)
        vals["nonempty_rotated_model_pct"]=round(100*vals["models_with_rotation"]/len(active),2)
        vals["nonempty_bbox_outside_model_pct"]=round(100*vals["nonempty_models_with_bbox_outside_0_16"]/len(active),2)
        return vals

    recorded = json.loads((MOD/"v15/v15_geometry_summary.json").read_text(encoding="utf-8"))
    for mod, rows in [("Another Furniture",af),("Handcrafted",hc)]:
        actual=aggregate(rows)
        expected=next(d for d in recorded["totals"] if d["mod"]==mod)
        for key, value in actual.items():
            assert expected[key]==value, f"{mod}.{key}: {value} vs {expected[key]}"

    derived=read_rows("v15/model_geometry_derived_189.csv")
    by_key={(r["mod"],r["source_model"]):r for r in derived}
    assert len(derived)==len(by_key)==189
    for r in af+hc:
        d=by_key[(r["mod"],r["source_model"])]
        for key in ("elements","declared_faces","possible_face_slots","undeclared_face_slots","rotated_elements","flat_elements"):
            assert int(d[key]) == r[key], (r["source_model"], key)
        assert d["source_git_sha"]==r["source_git_sha"]
        assert d["source_path"]==r["source_path"]
        if r["bbox_eval"] is None:
            assert d["bbox_outside_0_16"]==""
        else:
            assert int(d["bbox_outside_0_16"]) == int(r["bbox_eval"][0])
            assert d["bbox_outside_axes"]==r["bbox_eval"][1]

    families=read_rows("v15/handcrafted_family_metrics_22.csv")
    groups=defaultdict(list)
    for r in hc: groups[r["category"]].append(r)
    assert len(families)==len(groups)==22
    for f in families:
        rows=groups[f["category"]]
        assert int(f["models"])==len(rows)
        assert int(f["elements"])==sum(r["elements"] for r in rows)
        assert int(f["rotated_elements"])==sum(r["rotated_elements"] for r in rows)
        assert int(f["flat_elements"])==sum(r["flat_elements"] for r in rows)
    for key, rel in [("Another Furniture","v13/another_png_12_pixel_metrics.csv"),("Handcrafted","v13/handcrafted_png_12_pixel_metrics.csv")]:
        px=read_rows(rel)
        assert len(px)==12
        ps=next(x for x in recorded["v13_sample_palette_supplement"] if x["mod"]==key)
        assert int(median([int(r["unique_rgba"]) for r in px])) == ps["unique_visible_rgba_median"]
        assert sum(int(r["partial"])>0 for r in px) == ps["textures_with_partial_alpha"]

    assert recorded["original_assets_directly_read_v15"]==0
    print("v15 verified: 69 AF + 120 Handcrafted models, 189 derived rows, 22 HC families, 24 prior PNG sample statistics")
    print("This verifies cross-record aggregation only; original game assets and rendering are not examined.")

if __name__=="__main__":
    main()
