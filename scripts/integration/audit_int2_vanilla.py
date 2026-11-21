"""INT-2 source-backed re-audit for 1-1 (150 PNGs) and 1-2 (4,768 assets).

Runs on a real checkout containing 1.21.11/. Reads official study ledgers;
never rewrites original research, models, or source assets.

Validation:
- Every 1-1 pinned PNG: raw SHA-256, Git blob SHA-1, PNG chunk CRCs,
  Pillow decode and RGBA statistics.
- Every 1-2 G ledger row: bytes, Git blob SHA-1, JSON syntax or full PNG
  decoding. The 99 sidecars are checked separately.
- G's cube_mirrored original-source correction: independently rechecked
  without backfilling the historic F record.

No claim is made about official JAR authenticity, in-game rendering,
complete model geometry correctness, material semantics or training rights.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
from collections import Counter
from pathlib import Path
import struct
import zlib

from PIL import Image

TEXTURE_LEDGER = ("research/vanilla_textures/integrations/"
                  "v42_INT-1-1-11steps_150_SOURCE_COMPLETE/TEXTURE_150_SCOPE_LEDGER.csv")
G_LEDGER = "research/vanilla_models/phase_1-2-G/final/G_FINAL_SOURCE_SHA_4669.csv"
SIDECAR_LEDGER = "research/vanilla_models/phase_1-2-G/final/G_FINAL_MCMETA_99.csv"
G_GAPS = "research/vanilla_models/phase_1-2-G/entry6/G_ENTRY6_PROVENANCE_GAPS.json"
PNG_HEADER = b"\x89PNG\r\n\x1a\n"
PNG_FIELDS = (
    "stage_id", "item_id", "texture_id", "path", "material_family", "bytes",
    "raw_sha256", "git_blob_sha1", "width", "height",
    "rgba_sha256", "pixels", "alpha_zero", "alpha_partial", "alpha_opaque",
    "unique_rgba", "chunk_count", "idat_count", "png_crc_failures", "status",
)


def _table(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def _source(root: Path, path: str) -> bytes:
    if not path.startswith("1.21.11/") or "\\" in path or ".." in Path(path).parts:
        raise ValueError(f"Unexpected source path: {path}")
    root_abs = root.resolve()
    source = (root_abs / path).resolve(strict=True)
    if not source.is_relative_to(root_abs / "1.21.11") or not source.is_file():
        raise ValueError(f"Source outside pinned checkout: {path}")
    return source.read_bytes()


def _blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\x00" + data).hexdigest()


def _strict_json(data: bytes, path: str):
    def pair_check(pairs):
        obj = {}
        for key, value in pairs:
            if key in obj:
                raise ValueError(f"{path}: duplicate JSON key {key}")
            obj[key] = value
        return obj
    return json.loads(
        data.decode("utf-8-sig"),
        object_pairs_hook=pair_check,
        parse_constant=lambda x: (_ for _ in ()).throw(ValueError(f"{path}: {x}")),
    )


def _png_crc(raw: bytes, path: str) -> tuple[int, int]:
    if not raw.startswith(PNG_HEADER):
        raise ValueError(f"{path}: PNG signature mismatch")
    at = len(PNG_HEADER)
    chunks, idats, ended = 0, 0, False
    while at < len(raw):
        if len(raw) - at < 12:
            raise ValueError(f"{path}: truncated PNG chunk")
        size = struct.unpack_from(">I", raw, at)[0]
        stop = at + 12 + size
        if stop > len(raw):
            raise ValueError(f"{path}: chunk extends past file")
        kind = raw[at + 4:at + 8]
        body = raw[at + 8:at + 8 + size]
        expected = struct.unpack_from(">I", raw, at + 8 + size)[0]
        calculated = zlib.crc32(kind + body) & 0xFFFFFFFF
        if expected != calculated:
            raise ValueError(f"{path}: {kind!r} PNG CRC mismatch")
        if chunks == 0 and (kind != b"IHDR" or size != 13):
            raise ValueError(f"{path}: missing/invalid initial IHDR")
        chunks += 1
        idats += int(kind == b"IDAT")
        at = stop
        if kind == b"IEND":
            if size != 0 or at != len(raw):
                raise ValueError(f"{path}: invalid final IEND/trailing bytes")
            ended = True
            break
    if not ended or idats == 0:
        raise ValueError(f"{path}: missing IEND/IDAT")
    return chunks, idats


def _image(raw: bytes, path: str) -> dict:
    chunks, idats = _png_crc(raw, path)
    with Image.open(io.BytesIO(raw)) as png:
        png.verify()
    with Image.open(io.BytesIO(raw)) as png:
        png.load()
        rgba = png.convert("RGBA")
        width, height = rgba.size
        payload = rgba.tobytes()
    alphas = payload[3::4]
    zero = alphas.count(0)
    full = alphas.count(255)
    count = width * height
    if len(payload) != count * 4:
        raise ValueError(f"{path}: decoded RGBA dimensions mismatch")
    return {
        "width": width, "height": height, "rgba_sha256": hashlib.sha256(payload).hexdigest(),
        "pixels": count, "alpha_zero": zero, "alpha_partial": count - zero - full,
        "alpha_opaque": full, "unique_rgba": len(set(payload[i:i+4] for i in range(0, len(payload), 4))),
        "chunk_count": chunks, "idat_count": idats, "png_crc_failures": 0,
    }


def audit(root: Path) -> tuple[list[dict], dict]:
    root = root.resolve()
    tex = _table(root / TEXTURE_LEDGER)
    g_rows = _table(root / G_LEDGER)
    sidecars = _table(root / SIDECAR_LEDGER)
    gaps = json.loads((root / G_GAPS).read_text(encoding="utf-8"))
    assert len(tex) == 150, f"v42 PNG denominator changed: {len(tex)}"
    assert len(g_rows) == 4669, f"G source denominator changed: {len(g_rows)}"
    assert len(sidecars) == 99, f"G sidecar denominator changed: {len(sidecars)}"
    assert len({r["item_id"] for r in tex}) == len({r["texture_id"] for r in tex}) == 150
    assert len({r["user_supplied_asset_path"] for r in tex}) == 150
    assert len({r["path"] for r in g_rows}) == 4669
    assert len({r["mcmeta_path"] for r in sidecars}) == 99

    g_by_path = {r["path"]: r for r in g_rows}
    png_rows = []
    stage_counts = Counter()
    for row in tex:
        path = row["user_supplied_asset_path"]
        assert path.startswith("1.21.11/assets/minecraft/textures/block/") and path.endswith(".png"), path
        raw = _source(root, path)
        sha256 = hashlib.sha256(raw).hexdigest()
        blob = _blob_sha(raw)
        if sha256 != row["v4_historical_sha256"]:
            raise AssertionError(f"{path}: v4 historical raw SHA-256 mismatch")
        if path not in g_by_path or blob != g_by_path[path]["sha"]:
            raise AssertionError(f"{path}: cross-stage 1-2 G blob SHA mismatch")
        metrics = _image(raw, path)
        png_rows.append({
            "stage_id": row["stage_id"], "item_id": row["item_id"],
            "texture_id": row["texture_id"], "path": path,
            "material_family": row["material_family"], "bytes": len(raw),
            "raw_sha256": sha256, "git_blob_sha1": blob, **metrics, "status": "PASS",
        })
        stage_counts[row["stage_id"]] += 1

    type_counts = Counter()
    model_parents = {}
    model_paths = set()
    g_sha_by_path = {}
    for row in g_rows:
        path = row["path"]
        raw = _source(root, path)
        kind = row["type"]
        blob = _blob_sha(raw)
        if len(raw) != int(row["bytes"]) or blob != row["sha"]:
            raise AssertionError(f"{path}: G raw bytes / Git SHA mismatch")
        if row["source_sha_match"] != "True":
            raise AssertionError(f"{path}: original G ledger reports mismatched source")
        if kind == "BLOCK_TEXTURE_PNG":
            _image(raw, path)
        elif kind in ("BLOCK_MODEL_JSON", "BLOCKSTATE_JSON"):
            obj = _strict_json(raw, path)
            if not isinstance(obj, dict):
                raise AssertionError(f"{path}: JSON root must be object")
            if kind == "BLOCK_MODEL_JSON":
                model_paths.add(path)
                parent = obj.get("parent")
                if parent is not None:
                    if not isinstance(parent, str):
                        raise AssertionError(f"{path}: parent must be a string")
                    model_parents[path] = parent
        else:
            raise AssertionError(f"Unexpected G type: {kind}")
        type_counts[kind] += 1
        g_sha_by_path[path] = blob
    required = {"BLOCK_MODEL_JSON": 2390, "BLOCKSTATE_JSON": 1168, "BLOCK_TEXTURE_PNG": 1111}
    if dict(type_counts) != required:
        raise AssertionError(f"Unexpected G source type distribution: {dict(type_counts)}")

    animation_counter = Counter()
    for row in sidecars:
        path = row["mcmeta_path"]
        raw = _source(root, path)
        if _blob_sha(raw) != row["git_sha"] or len(raw) != int(row["bytes"]):
            raise AssertionError(f"{path}: sidecar SHA/size mismatch")
        obj = _strict_json(raw, path)
        if not isinstance(obj, dict):
            raise AssertionError(f"{path}: .mcmeta JSON root is not object")
        animated = "animation" in obj
        if animated != (row["animated"] == "True"):
            raise AssertionError(f"{path}: animation flag disagreement")
        animation_counter["animated" if animated else "not_animated"] += 1

    parent = "1.21.11/assets/minecraft/models/block/cube_mirrored.json"
    affected = {
        "1.21.11/assets/minecraft/models/block/sculk_mirrored.json",
        "1.21.11/assets/minecraft/models/block/stone_mirrored.json",
    }
    if gaps.get("count") != 4 or len(gaps.get("records", [])) != 4:
        raise AssertionError("G provenance gap count changed")
    if {r["model"] for r in gaps["records"]} != affected:
        raise AssertionError("G provenance gap affected models changed")
    if any(r["parent"] != parent or r["G_recomputed_original_git_blob_sha"] != g_sha_by_path[parent] for r in gaps["records"]):
        raise AssertionError("G parent correction hash differs from independently rehashed bytes")
    for path in affected:
        declared = model_parents.get(path, "")
        if not declared.endswith("cube_mirrored"):
            raise AssertionError(f"{path}: unexpected parent: {declared}")

    # Static links are descriptive only; unresolved references may be built-ins
    # or runtime generated and must not be interpreted as confirmed errors.
    summary = {
        "audit_schema": "MCFR_INT2_VANILLA_SOURCE_v1",
        "baseline_commit": "176f7f34de2336eb7984c4734e97b6eb156c19f4",
        "scope_1_1": {
            "source_png": len(png_rows), "stage_counts": dict(sorted(stage_counts.items())),
            "raw_sha256_matches": len(png_rows), "cross_g_blob_matches": len(png_rows),
            "png_crc_and_full_rgba_decode_pass": len(png_rows),
            "total_decoded_pixels": sum(int(x["pixels"]) for x in png_rows),
            "total_alpha_zero": sum(int(x["alpha_zero"]) for x in png_rows),
            "total_alpha_partial": sum(int(x["alpha_partial"]) for x in png_rows),
            "total_alpha_opaque": sum(int(x["alpha_opaque"]) for x in png_rows),
            "newly_verified": "RAW_SHA256_PNG_CRC_RGBA",
            "not_verified": ["material_semantic_classification", "ingame_rendering", "official_client_JAR_authenticity"],
        },
        "scope_1_2": {
            "source_files_rehashed": len(g_rows), "by_type": dict(sorted(type_counts.items())),
            "png_full_crc_and_decode": type_counts["BLOCK_TEXTURE_PNG"],
            "json_parsed": type_counts["BLOCK_MODEL_JSON"] + type_counts["BLOCKSTATE_JSON"],
            "sidecars_rehashed_json_parsed": len(sidecars),
            "sidecar_animation_counts": dict(sorted(animation_counter.items())),
            "models_declaring_parent": len(model_parents),
            "G_provenance_gap_records_independently_rechecked": len(gaps["records"]),
            "not_verified": ["all_inherited_geometry", "UV_accuracy", "blockstate_render_selection", "official_JAR_sha", "ingame_behavior"],
        },
        "overall_status": "PASS_SOURCE_BINARY_AND_JSON_SCOPE",
        "ai_training_approval": "NOT_GRANTED",
    }
    return png_rows, summary


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args()
    rows, summary = audit(args.root)
    args.out.mkdir(parents=True, exist_ok=True)
    csv_path = args.out / "INT2_1_1_PNG_REAUDIT.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=PNG_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    (args.out / "INT2_VANILLA_SOURCE_SUMMARY.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print("INT2_SUMMARY_JSON:" + json.dumps(summary, ensure_ascii=False, sort_keys=True))
    print("INT2_CSV_BEGIN")
    print(csv_path.read_text(encoding="utf-8"), end="")
    print("INT2_CSV_END")


if __name__ == "__main__":
    main()
