"""Reproduce the bounded 1-2-C Entry1 source inspection from the 1.21.11 tree."""
import csv
import hashlib
import json
import os
import subprocess
from collections import Counter
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "research/vanilla_models/phase_1-2-C/entry1"
ENTRY = os.environ.get("C_ENTRY", "entry1")
if ENTRY != "entry1":
    OUT = ROOT / f"research/vanilla_models/phase_1-2-C/{ENTRY}"
MODEL = ROOT / "1.21.11/assets/minecraft/models/block"
TEXTURE = ROOT / "1.21.11/assets/minecraft/textures"
B = ROOT / "research/vanilla_models/phase_1-2-B/entry10"
NAMES = (
    "cartography_table", "flower_pot", "oak_shelf_left", "soul_lantern",
    "acacia_button", "glass_pane_post", "oak_door_bottom_left", "stone_brick_stairs_inner",
    "acacia_leaves", "stone", "wheat_stage1", "fire_floor1",
)
if ENTRY != "entry1":
    NAMES = tuple(json.loads((OUT / "C_SELECTION.json").read_text())["models"])


def blob(path):
    return hashlib.sha1(b"blob " + str(path.stat().st_size).encode() + b"\0" + path.read_bytes()).hexdigest()


def relative(path):
    return str(path.relative_to(ROOT))


def write_csv(name, rows, fields):
    with (OUT / name).open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    ledger = {r["full_source_path"]: r for r in csv.DictReader((B / "B_SCOPE_2390_STATUS.csv").open())}
    cache = {r["path"]: r for r in json.loads((B / "SOURCE_JSON_CACHE_2360.json").read_text())["source_records"]}
    bindings, faces, pngs, evidence, unresolved = [], [], {}, [], []
    prior = set()
    for report in (ROOT / "research/vanilla_models").glob("v*/REPORT.md"):
        if report.is_file():
            body = report.read_text(encoding="utf-8", errors="replace")
            for name in NAMES:
                if name in body:
                    prior.add(name)

    for name in NAMES:
        leaf = MODEL / (name + ".json")
        lr = ledger[relative(leaf)]
        assert lr["B_first_owner_scope"] == "B_FIRST_2360"
        assert blob(leaf) == lr["git_blob_sha"]
        chain, visited = [], set()
        path = leaf
        while True:
            assert path not in visited, f"parent cycle: {path}"
            visited.add(path)
            source = json.loads(path.read_text(encoding="utf-8"))
            sha = blob(path)
            if relative(path) in cache:
                assert cache[relative(path)]["sha"] == sha
                assert cache[relative(path)]["source"] == source
            chain.append((path, sha, source))
            parent = source.get("parent")
            if not parent:
                break
            assert parent.startswith(("minecraft:block/", "block/")), (name, parent)
            path = MODEL / (parent.removeprefix("minecraft:block/").removeprefix("block/") + ".json")
            assert path.exists(), (name, parent)

        geometry = next(((p, sha, s) for p, sha, s in chain if "elements" in s), None)
        slots = {}
        for p, sha, source in reversed(chain):
            slots.update(source.get("textures", {}))
        def resolve(ref):
            trail, seen = [], set()
            while isinstance(ref, str):
                # 1.21.11 hqp.a(String) tests a slot key with or without a leading '#';
                # iog.a(hqp,String,...) falls back to a direct resource only if no slot exists.
                key = ref[1:] if ref.startswith("#") else ref
                if key not in slots:
                    if ref.startswith("#"):
                        return None, trail + [key], "missing_slot"
                    break
                if key in seen:
                    return None, trail + [key], "cycle"
                seen.add(key)
                trail.append(key)
                ref = slots[key]
            if not isinstance(ref, str):
                return None, trail, "invalid_texture_reference"
            if ":" not in ref:
                ref = "minecraft:" + ref
            return ref, trail, "resolved"

        for key, raw in sorted(slots.items()):
            value, trail, status = resolve("#" + key)
            bindings.append(dict(model=name, leaf_path=relative(leaf), leaf_sha=lr["git_blob_sha"],
                                 slot=key, raw_value=raw, resolved_texture=value or "",
                                 slot_chain=">".join(trail), status=status,
                                 defining_source_path=next(relative(p) for p, sha, src in chain if key in src.get("textures", {}))))
        nfaces = 0
        if geometry:
            gp, gsha, gs = geometry
            for ei, element in enumerate(gs["elements"]):
                for direction, face in element.get("faces", {}).items():
                    nfaces += 1
                    tex, trail, status = resolve(face.get("texture"))
                    png_path = None
                    if status == "resolved" and tex.startswith("minecraft:"):
                        png_path = TEXTURE / (tex.removeprefix("minecraft:") + ".png")
                        if not png_path.exists():
                            status = "missing_png"
                        else:
                            key = relative(png_path)
                            if key not in pngs:
                                with Image.open(png_path) as im:
                                    rgba = im.convert("RGBA")
                                    counts = Counter(a for *_, a in rgba.get_flattened_data())
                                    pngs[key] = dict(png_path=key, png_sha=blob(png_path), width=im.width,
                                                     height=im.height, mode=im.mode, rgba_sha256=hashlib.sha256(rgba.tobytes()).hexdigest(),
                                                     opaque_pixels=counts[255], transparent_pixels=counts[0],
                                                     partial_alpha_pixels=sum(v for a, v in counts.items() if 0 < a < 255),
                                                     unique_alpha_values=len(counts))
                    if status != "resolved":
                        unresolved.append(dict(model=name, issue=status, ref=str(face.get("texture"))))
                    faces.append(dict(model=name, priority=lr["priority"], leaf_path=relative(leaf),
                                      leaf_sha=lr["git_blob_sha"], geometry_path=relative(gp), geometry_sha=gsha,
                                      element_index=ei, direction=direction, face_texture=face.get("texture", ""),
                                      slot_chain=">".join(trail), resolved_texture=tex or "", texture_status=status,
                                      png_path=relative(png_path) if png_path and png_path.exists() else "",
                                      uv_type="explicit_source" if "uv" in face else "implicit_source_absent",
                                      original_uv=json.dumps(face.get("uv"), ensure_ascii=False) if "uv" in face else "",
                                      face_rotation_original=face.get("rotation", ""),
                                      uv_x_reversed=bool("uv" in face and face["uv"][0] > face["uv"][2]),
                                      uv_y_reversed=bool("uv" in face and face["uv"][1] > face["uv"][3]),
                                      cullface_original=face.get("cullface", ""),
                                      element_from=json.dumps(element.get("from")), element_to=json.dumps(element.get("to"))))
        evidence.append(dict(model=name, priority=lr["priority"], leaf_path=relative(leaf), leaf_sha=lr["git_blob_sha"],
                             parent_chain=json.dumps([dict(path=relative(p), sha=sha) for p, sha, src in chain], ensure_ascii=False),
                             geometry_path=relative(geometry[0]) if geometry else "",
                             geometry_sha=geometry[1] if geometry else "", face_count=nfaces,
                             prior_v_report_name_mention=name in prior,
                             prior_note="name mention only; not a claim of prior C-complete evidence" if name in prior else "no report name mention found"))

    write_csv("FACE_UV_EVIDENCE.csv", faces, list(faces[0]))
    write_csv("TEXTURE_BINDINGS.csv", bindings, list(bindings[0]))
    write_csv("PNG_RGBA_EVIDENCE.csv", sorted(pngs.values(), key=lambda r:r["png_path"]), list(next(iter(pngs.values()))))
    animation_metadata = []
    for key in sorted(pngs):
        meta = ROOT / (key + ".mcmeta")
        if meta.exists():
            animation_metadata.append(dict(png_path=key, mcmeta_path=relative(meta),
                                           mcmeta_sha=blob(meta), source_bytes=meta.stat().st_size,
                                           interpretation="source_file_only_animation_timing_not_authenticated"))
    if ENTRY not in ("entry1", "entry2"):
        write_csv("PNG_MCMETA_SOURCE.csv", animation_metadata,
                  ["png_path", "mcmeta_path", "mcmeta_sha", "source_bytes", "interpretation"])
    write_csv("MODEL_SOURCE_EVIDENCE.csv", evidence, list(evidence[0]))
    write_csv("UNRESOLVED.csv", unresolved, ["model", "issue", "ref"])
    summary = dict(schema=f"C_{ENTRY.upper()}_SOURCE_AUDIT", base_head=os.environ.get("C_BASE_HEAD", "73571a9e1ab791e6ded46b6a01a1aae04fc8ffaf"),
                   model_count=len(evidence), priorities=dict(Counter(r["priority"] for r in evidence)),
                   applied_face_count=len(faces), explicit_source_faces=sum(r["uv_type"] == "explicit_source" for r in faces),
                   implicit_source_absent_faces=sum(r["uv_type"] == "implicit_source_absent" for r in faces),
                   binding_rows=len(bindings), png_paths=len(pngs),
                   png_rgba_pixels=sum(r["width"]*r["height"] for r in pngs.values()),
                   unresolved_rows=len(unresolved), prior_report_name_mentions=len(prior),
                   verification="local Git blob SHA agrees with B ledger and cache; PNG Git blob and decoded RGBA SHA recorded; no game renderer authentication")
    if ENTRY not in ("entry1", "entry2"):
        summary["png_mcmeta_source_paths"] = len(animation_metadata)
    (OUT / f"C_{ENTRY.upper()}_AUDIT.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
