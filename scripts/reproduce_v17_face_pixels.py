#!/usr/bin/env python3
"""Independently verify v17 source-PNG RGBA face samples with Pillow.

Usage: python scripts/reproduce_v17_face_pixels.py /path/to/Handcrafted
The checkout must be the original author's commit
8d21d1665916850c3fa3bdaf1370c50ec2ca7035. Does not fetch/repost assets.
Requires Pillow: python -m pip install Pillow.
"""
import argparse
import csv
import hashlib
import io
import json
from collections import Counter
from pathlib import Path

from PIL import Image

DATA = Path(__file__).resolve().parents[1] / "research/furniture_mods/v17"


def read_csv(name):
    with (DATA / name).open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def key(row):
    return row["leaf"], row["element_index"], row["face"]


def git_sha(blob):
    return hashlib.sha1(f"blob {len(blob)}\0".encode() + blob).hexdigest()


def sample(image, row):
    x0, y0, x1, y1 = [int(row[k]) for k in ("pixel_x0", "pixel_y0", "pixel_x1", "pixel_y1")]
    assert 0 <= x0 <= x1 <= image.width and 0 <= y0 <= y1 <= image.height
    area = (x1 - x0) * (y1 - y0)
    visible = transparent = partial = red = green = blue = 0
    colors = set()
    for y in range(y0, y1):
        for x in range(x0, x1):
            r, g, b, a = image.getpixel((x, y))
            if a == 0:
                transparent += 1
            else:
                visible += 1
                red += r
                green += g
                blue += b
                colors.add((r, g, b, a))
                if a < 255:
                    partial += 1
    assert visible + transparent == area
    status = (
        "zero_uv_area" if area == 0
        else "sampled_fully_transparent" if visible == 0
        else "sampled_all_opaque" if transparent == 0 and partial == 0
        else "sampled_partial_alpha" if partial
        else "sampled_mixed_opaque_transparent"
    )
    return {
        "rect_texels": area, "visible_texels": visible,
        "transparent_texels": transparent, "partial_alpha_texels": partial,
        "visible_rgba_colors": len(colors), "status": status,
        "mean_visible_r": round(red / visible, 2) if visible else None,
        "mean_visible_g": round(green / visible, 2) if visible else None,
        "mean_visible_b": round(blue / visible, 2) if visible else None,
    }


def verify(upstream):
    all_rects = read_csv("handcrafted_16_leaf_face_rects_786.csv")
    recorded = read_csv("face_pixel_samples_784.csv")
    mod_rects = [r for r in all_rects if r["namespace"] == "handcrafted"]
    assert len(all_rects) == 786 and len(mod_rects) == len(recorded) == 784
    expected = {key(row): row for row in recorded}
    assert len(expected) == 784

    images = {}
    statuses = Counter()
    counters = Counter()
    for face in mod_rects:
        name = face["png_name"]
        saved = expected[key(face)]
        if name not in images:
            path = upstream / "common/src/main/resources/assets/handcrafted/textures/block" / (name + ".png")
            content = path.read_bytes()
            assert git_sha(content) == face["png_sha"], name
            image = Image.open(io.BytesIO(content))
            image.load()
            images[name] = image.convert("RGBA")
        image = images[name]
        assert image.size == (int(face["png_width"]), int(face["png_height"]))
        assert saved["png_name"] == name and saved["png_sha"] == face["png_sha"]
        for k in ("pixel_x0", "pixel_x1", "pixel_y0", "pixel_y1"):
            assert saved[k] == face[k], (name, k)
        measured = sample(image, face)
        for k in ("rect_texels", "visible_texels", "transparent_texels",
                  "partial_alpha_texels", "visible_rgba_colors"):
            assert int(saved[k]) == measured[k], (key(face), k)
        assert saved["status"] == measured["status"], key(face)
        for k in ("mean_visible_r", "mean_visible_g", "mean_visible_b"):
            if measured[k] is None:
                assert saved[k] == ""
            else:
                assert abs(float(saved[k]) - measured[k]) <= 0.015, (key(face), k)
        statuses[measured["status"]] += 1
        for k in ("rect_texels", "visible_texels", "transparent_texels", "partial_alpha_texels"):
            counters[k] += measured[k]

    summary = json.loads((DATA / "v17_pixel_region_summary.json").read_text(encoding="utf-8"))["totals"]
    assert len(images) == summary["distinct_textures"] == 24
    assert statuses == Counter(summary["sample_statuses"])
    assert counters["rect_texels"] == summary["sampled_texel_uses"] == 41290
    assert counters["visible_texels"] == summary["opaque_texel_uses"] + summary["partial_alpha_texel_uses"]
    assert counters["transparent_texels"] == summary["transparent_texel_uses"] == 9625
    assert counters["partial_alpha_texels"] == summary["partial_alpha_texel_uses"] == 0
    print("PASS: 24 original PNG SHA checks, 784 face pixel rectangles, 41,290 texel uses")
    print("Limit: source image face UV regions verified, not game visibility, culling or lighting.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("upstream_handcrafted_dir", type=Path)
    verify(parser.parse_args().upstream_handcrafted_dir)
