"""Audit selected Minecraft 1.21.11 texture animation sources with Pillow."""
import argparse
import csv
import hashlib
import io
import json
import zipfile
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[5]
SOURCE = ROOT / "1.21.11"
TEXTURES = ROOT / "research/vanilla_textures"
REVISIONS = {"1-1-02": "TEX02-R018", "1-1-10": "TEX10-R015"}
CONTROLS = {"1-1-02": "water_still", "1-1-10": "kelp"}
TARGET_COUNTS = {"1-1-02": 17, "1-1-10": 8}
JAR_SHA1 = "ba2df812c2d12e0219c489c4cd9a5e1f0760f5bd"
BLOCK_TEXTURES = "assets/minecraft/textures/block/"


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def read_matching(jar, path):
    data = jar.read(path)
    if data != (SOURCE / path).read_bytes():
        raise ValueError(f"JAR and repository extraction differ: {path}")
    return data


def audit_png(jar, path, sample_type, item_id="", previous_sha=""):
    data = read_matching(jar, path)
    if previous_sha and sha256(data) != previous_sha:
        raise ValueError(f"Fixed ledger SHA-256 differs: {path}")
    sidecar = path + ".mcmeta"
    present = sidecar in jar.namelist()
    if present != (SOURCE / sidecar).is_file():
        raise ValueError(f"JAR and repository disagree on sidecar existence: {path}")
    metadata = read_matching(jar, sidecar) if present else b""
    sections = json.loads(metadata) if present else {}
    animation = sections.get("animation")
    if "animation" in sections and not isinstance(animation, dict):
        raise ValueError(f"Invalid animation section: {sidecar}")

    with Image.open(io.BytesIO(data)) as image:
        image.verify()
    with Image.open(io.BytesIO(data)) as image:
        rgba = image.convert("RGBA")
    width, height = rgba.size
    alpha_histogram = rgba.getchannel("A").histogram()
    row = {
        "sample_type": sample_type, "item_id": item_id, "source_path": path,
        "png_sha256": sha256(data), "fixed_ledger_sha256_match": bool(previous_sha),
        "width": width, "height": height, "decoded_pixels": width * height,
        "transparent_pixels": alpha_histogram[0],
        "opaque_pixels": alpha_histogram[255],
        "mcmeta_path": sidecar if present else "",
        "mcmeta_sha256": sha256(metadata) if present else "",
        "mcmeta_sections": ",".join(sorted(sections)),
        "mipmap_strategy": sections.get("texture", {}).get("mipmap_strategy", ""),
        "animation_declared": animation is not None,
    }
    frames = []
    if animation is not None:
        # Both selected controls use the verified 16-pixel sprite layout
        # and the default sequential frame order from frametime alone.
        if set(animation) != {"frametime"} or width != 16 or height % 16:
            raise ValueError(f"Unexpected control layout or metadata: {sidecar}")
        frame_time = animation["frametime"]
        if type(frame_time) is not int or frame_time < 1:
            raise ValueError(f"Invalid control frame time: {sidecar}")
        previous = None
        for index in range(height // 16):
            top = index * 16
            frame = rgba.crop((0, top, 16, top + 16))
            pixels = frame.get_flattened_data()
            frames.append({
                "source_path": path, "frame_index": index, "top_y": top,
                "duration_ticks": frame_time,
                "rgba_sha256": sha256(frame.tobytes()),
                "rgba_changed_from_previous": "" if previous is None else
                sum(first != second for first, second in zip(previous, pixels)),
            })
            previous = pixels
    return row, frames


def model_refs(value):
    if isinstance(value, dict):
        if "model" in value:
            yield value["model"]
        for child in value.values():
            yield from model_refs(child)
    elif isinstance(value, list):
        for child in value:
            yield from model_refs(child)


def animation_keys(value):
    if isinstance(value, dict):
        for key, child in value.items():
            if key in {"animation", "frames", "frametime", "interpolate"}:
                yield key
            yield from animation_keys(child)
    elif isinstance(value, list):
        for child in value:
            yield from animation_keys(child)


def audit_model_sources(jar, fixed):
    sources = {}
    paths = [f"assets/minecraft/blockstates/{row['texture_id']}.json" for row in fixed]
    while paths:
        path = paths.pop()
        if path in sources:
            continue
        data = read_matching(jar, path)
        content = json.loads(data)
        keys = set(animation_keys(content))
        sources[path] = {"path": path, "sha256": sha256(data),
                         "animation_keys": ",".join(sorted(keys))}
        refs = list(model_refs(content))
        if "parent" in content:
            refs.append(content["parent"])
        for ref in refs:
            namespace, sep, model = ref.partition(":")
            if not sep:
                namespace, model = "minecraft", namespace
            paths.append(f"assets/{namespace}/models/{model}.json")
    return [sources[path] for path in sorted(sources)]


def write_csv(path, rows):
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=rows[0], lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def audit_stage(jar, stage, fixed, output):
    if len(fixed) != TARGET_COUNTS[stage] or len({row["source_path"] for row in fixed}) != len(fixed):
        raise ValueError(f"Invalid fixed denominator for {stage}")
    rows = [
        audit_png(jar, row["source_path"], "fixed", row["item_id"], row["v4_source_sha256"])[0]
        for row in fixed
    ]
    if stage == "1-1-02":
        prior = TEXTURES / "by_stage/1-1-02/TEX02-R017/MODEL_FACE_SPRITE_BINDINGS_186.csv"
        with prior.open(encoding="utf-8", newline="") as stream:
            sprites = {row["expected_original_png"].removeprefix("1.21.11/")
                       for row in csv.DictReader(stream)}
        fixed_paths = {row["source_path"] for row in rows}
        rows.extend(audit_png(jar, path, "linked_face")[0] for path in sorted(sprites - fixed_paths))
    control, frames = audit_png(jar, BLOCK_TEXTURES + CONTROLS[stage] + ".png", "control")
    if len(frames) < 2 or len({row["rgba_sha256"] for row in frames}) < 2:
        raise ValueError(f"Positive control did not detect changing frames for {stage}")

    models = audit_model_sources(jar, fixed)
    fixed_rows = [row for row in rows if row["sample_type"] == "fixed"]
    summary = {
        "revision": REVISIONS[stage],
        "fixed_pngs_checked": len(fixed_rows),
        "fixed_pngs_16x16": sum((row["width"], row["height"]) == (16, 16) for row in fixed_rows),
        "fixed_pixels_redecoded": sum(row["decoded_pixels"] for row in fixed_rows),
        "fixed_png_sha256_matches": sum(row["fixed_ledger_sha256_match"] for row in fixed_rows),
        "fixed_mcmeta_present": sum(bool(row["mcmeta_path"]) for row in fixed_rows),
        "fixed_dark_cutout_sidecars": sum(row["mipmap_strategy"] == "dark_cutout" for row in fixed_rows),
        "fixed_animation_declarations": sum(row["animation_declared"] for row in fixed_rows),
        "linked_face_pngs_checked": len(rows) - len(fixed_rows),
        "linked_face_animation_declarations": sum(row["animation_declared"] for row in rows[len(fixed_rows):]),
        "blockstate_json_checked": sum("/blockstates/" in row["path"] for row in models),
        "model_json_checked": sum("/models/" in row["path"] for row in models),
        "json_with_animation_keys": sum(bool(row["animation_keys"]) for row in models),
        "positive_control_sprite": CONTROLS[stage],
        "positive_control_frames": len(frames),
        "positive_control_unique_rgba_frames": len({row["rgba_sha256"] for row in frames}),
        "positive_control_cycle_ticks": sum(row["duration_ticks"] for row in frames),
        "in_game_render_observations": 0,
        "jar_sha1": JAR_SHA1,
    }
    output.mkdir(parents=True, exist_ok=True)
    write_csv(output / "TEXTURE_ANIMATION_AUDIT.csv", [*rows, control])
    write_csv(output / "BLOCKSTATE_MODEL_AUDIT.csv", models)
    write_csv(output / "POSITIVE_CONTROL_FRAMES.csv", frames)
    (output / "SUMMARY.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--jar", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    with args.jar.open("rb") as stream:
        if hashlib.file_digest(stream, "sha1").hexdigest() != JAR_SHA1:
            raise ValueError("Client JAR differs from the pinned 1.21.11 SHA-1")
    with (TEXTURES / "1-1_150_texture_numbered_task_ledger.csv").open(encoding="utf-8-sig", newline="") as stream:
        ledger = list(csv.DictReader(stream))
    with zipfile.ZipFile(args.jar) as jar:
        for stage, revision in REVISIONS.items():
            audit_stage(jar, stage, [row for row in ledger if row["work_id"] == stage], args.output / stage / revision)


if __name__ == "__main__":
    main()
