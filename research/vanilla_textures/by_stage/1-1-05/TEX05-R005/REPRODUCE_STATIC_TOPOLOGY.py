#!/usr/bin/env python3
"""TEX05-R005: offline analysis of six user-extracted Minecraft 1.21.11 PNGs.
Requires Pillow; run from anywhere: python REPRODUCE_STATIC_TOPOLOGY.py --repo-root /path/to/clone
Does NOT reproduce or claim Minecraft's actual mipmap pipeline or rendering.
"""
import argparse
import csv
import hashlib
import io
import struct
import sys
import zlib
from collections import Counter
from pathlib import Path
from PIL import Image

EXPECTED = {
    "glass": "cb89c706dce86eac3123cef087d359b5f23098b658a468fb91662b4a9922bcd0",
    "red_stained_glass": "4520f85fee79972191217d623c8b38522cacf74cb7c71113c0a6240d3b1f2ad2",
    "black_stained_glass": "62c705812949f0372dcc2fa82a5d89f7028ba1d9b3bd38765613e344f34f5b1c",
    "blue_stained_glass": "7d6cfe98ddc5d975b3bcf5f9cffc008f90db94d5d981ef440f7b68e8267ae247",
    "green_stained_glass": "dc82be445bd9c7cf158bd57651d51bfef400310f2ad4937fe1e5b1c60b4f5916",
    "white_stained_glass": "2d4504957fa123a6e9f35d93e05f94fb053ec213541f01fcecbc0097eaa5df75",
}
def png_chunks(data):
    assert data.startswith(b"\x89PNG\r\n\x1a\n")
    pos, chunks = 8, []
    while pos < len(data):
        n = int.from_bytes(data[pos:pos+4], "big")
        kind = data[pos+4:pos+8]
        payload = data[pos+8:pos+8+n]
        expected = int.from_bytes(data[pos+8+n:pos+12+n], "big")
        assert zlib.crc32(kind+payload) & 0xffffffff == expected, "PNG CRC mismatch"
        chunks.append((kind.decode(), n))
        pos += n+12
    assert pos == len(data) and chunks[-1][0] == "IEND"
    return chunks

def components4(mask):
    visited, sizes = set(), []
    for start, present in enumerate(mask):
        if not present or start in visited:
            continue
        visited.add(start)
        pending = [start]
        size = 0
        while pending:
            idx = pending.pop()
            size += 1
            x, y = idx % 16, idx // 16
            for nx, ny in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
                j = ny*16+nx
                if 0 <= nx < 16 and 0 <= ny < 16 and mask[j] and j not in visited:
                    visited.add(j)
                    pending.append(j)
        sizes.append(size)
    return sorted(sizes, reverse=True)

def analyze(repo):
    outer = set(range(16)) | set(range(240,256)) | {y*16 for y in range(16)} | {y*16+15 for y in range(16)}
    rows, masks = [], {}
    for name, sha in EXPECTED.items():
        rel = Path("1.21.11/assets/minecraft/textures/block") / (name + ".png")
        data = (repo / rel).read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        assert digest == sha, f"wrong input SHA: {rel}: {digest}"
        png_chunks(data)
        w, h, bit, coltype, _, _, _ = struct.unpack(">IIBBBBB", data[16:29])
        assert (w, h, bit) == (16, 16, 8)
        with Image.open(io.BytesIO(data)) as im:
            pixels = list(im.convert("RGBA").getdata())
            src_mode = im.mode
        alpha = [p[3] for p in pixels]
        threshold = 255 if name == "glass" else 155
        mask = [a >= threshold for a in alpha]
        masks[name] = mask
        components = components4(mask)
        avg = [sum(alpha[(2*y+dy)*16+2*x+dx] for dy in range(2) for dx in range(2))/4
               for y in range(8) for x in range(8)]
        border = sum(mask[i] for i in outer)
        assert sum(mask) == 65 and components == [60,1,1,1,1,1] and border == 60
        rows.append(dict(texture_id=name, sha256=digest, png_bytes=len(data),
                         png_color_type=coltype, png_bit_depth=bit, src_mode=src_mode,
                         alpha_hist=dict(Counter(alpha)), unique_rgba=len(set(pixels)),
                         alpha_threshold=threshold, high_alpha_pixels=sum(mask),
                         border_high_alpha=border, components4=str(components),
                         proxy_2x2_alpha_min=min(avg), proxy_2x2_alpha_max=max(avg),
                         proxy_2x2_alpha_unique=len(set(avg)), runtime_verified=False))
    ref = masks["glass"]
    assert all(all(a == b for a, b in zip(ref, m)) for m in masks.values())
    return rows

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[5])
    args=parser.parse_args()
    rows=analyze(args.repo_root)
    writer=csv.DictWriter(sys.stdout, fieldnames=list(rows[0]))
    writer.writeheader()
    for row in rows:
        writer.writerow(row)
if __name__ == "__main__":
    main()
