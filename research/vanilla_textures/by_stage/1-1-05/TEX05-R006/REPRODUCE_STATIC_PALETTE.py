#!/usr/bin/env python3
"""TEX05-R006 offline palette and 2x2 arithmetic proxy.
Run: python REPRODUCE_STATIC_PALETTE.py --repo-root /path/to/repo --out-dir /path/to/out
Requires Pillow. This does NOT execute Minecraft's renderer or mipmap generator.
"""
import argparse
import csv
import hashlib
import io
from collections import Counter
from pathlib import Path
from PIL import Image

EXPECTED = {
"glass":"cb89c706dce86eac3123cef087d359b5f23098b658a468fb91662b4a9922bcd0",
"red_stained_glass":"4520f85fee79972191217d623c8b38522cacf74cb7c71113c0a6240d3b1f2ad2",
"black_stained_glass":"62c705812949f0372dcc2fa82a5d89f7028ba1d9b3bd38765613e344f34f5b1c",
"blue_stained_glass":"7d6cfe98ddc5d975b3bcf5f9cffc008f90db94d5d981ef440f7b68e8267ae247",
"green_stained_glass":"dc82be445bd9c7cf158bd57651d51bfef400310f2ad4937fe1e5b1c60b4f5916",
"white_stained_glass":"2d4504957fa123a6e9f35d93e05f94fb053ec213541f01fcecbc0097eaa5df75",
}
def save(path, rows):
    with path.open("w", newline="", encoding="utf-8") as f:
        w=csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
def audit(root):
    palettes,proxies,stats=[],[],[]
    masks={}
    for name,sha in EXPECTED.items():
        path=root/"1.21.11/assets/minecraft/textures/block"/(name+".png")
        raw=path.read_bytes()
        assert hashlib.sha256(raw).hexdigest()==sha,name+" SHA mismatch"
        with Image.open(io.BytesIO(raw)) as image:
            assert image.size==(16,16)
            p=list(image.convert("RGBA").getdata())
        hist=Counter(p)
        for (r,g,b,a),count in sorted(hist.items(),key=lambda e:(e[0][3],e[0][:3])):
            palettes.append(dict(texture_id=name,r=r,g=g,b=b,a=a,pixel_count=count,png_sha256=sha))
        alpha=[q[3] for q in p]
        masks[name]=alpha
        nonzero=mixed=diffcount=0
        maxdiff=0.0
        for y in range(8):
            for x in range(8):
                block=[p[(2*y+dy)*16+(2*x+dx)] for dy in (0,1) for dx in (0,1)]
                asum=sum(q[3] for q in block)
                nonzero+=asum>0
                mixed+=len({q[3] for q in block})>1
                straight=[sum(q[c] for q in block)/4 for c in range(3)]
                weighted=[sum(q[c]*q[3] for q in block)/asum for c in range(3)] if asum else None
                delta=max(abs(v-w) for v,w in zip(straight,weighted)) if weighted else None
                diffcount+=delta is not None and delta>1e-10
                if delta is not None:maxdiff=max(maxdiff,delta)
                proxies.append(dict(texture_id=name,block_x=x,block_y=y,
                    alpha_mean=f"{asum/4:.6f}",
                    straight_rgb="|".join(f"{v:.6f}" for v in straight),
                    alpha_weighted_rgb="|".join(f"{v:.6f}" for v in weighted) if weighted else "undefined_alpha0",
                    max_abs_rgb_delta=f"{delta:.6f}" if delta is not None else "undefined_alpha0",
                    source="math_proxy_not_game_mipmap"))
        stats.append(dict(texture_id=name,source_png_sha256=sha,unique_rgba=len(hist),
            unique_rgb=len({q[:3] for q in p}),mean_alpha=f"{sum(alpha)/256:.6f}",
            proxy_total_2x2_blocks=64,proxy_nonzero_alpha=nonzero,proxy_mixed_alpha=mixed,
            proxy_rgb_diff_blocks=diffcount,proxy_max_rgb_channel_delta=f"{maxdiff:.6f}",
            ingame_verified=False))
    ref=masks["red_stained_glass"]
    assert all(masks[n]==ref for n in EXPECTED if n!="glass")
    assert len(palettes)==20 and len(proxies)==384 and len(stats)==6
    assert stats[0]["proxy_rgb_diff_blocks"]==32
    assert stats[0]["proxy_max_rgb_channel_delta"]=="79.500000"
    assert all(s["proxy_rgb_diff_blocks"]==0 for s in stats[1:])
    return palettes,proxies,stats
if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--repo-root",type=Path,required=True)
    parser.add_argument("--out-dir",type=Path,required=True)
    args=parser.parse_args()
    args.out_dir.mkdir(parents=True,exist_ok=True)
    palettes,proxies,stats=audit(args.repo_root)
    save(args.out_dir/"RGBA_PALETTE_20.csv",palettes)
    save(args.out_dir/"BOX_2X2_PROXY_384.csv",proxies)
    save(args.out_dir/"PROXY_SUMMARY_6.csv",stats)
    print("existing PNGs verified: 6; palette rows: 20; hypothetical 2x2 blocks: 384; in-game: 0")
