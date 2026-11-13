#!/usr/bin/env python3
"""Independent PNG edge and alpha audit for TEX05-R002. No game runtime claims."""
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image

EXPECTED = {
    'glass': 'cb89c706dce86eac3123cef087d359b5f23098b658a468fb91662b4a9922bcd0',
    'red_stained_glass': '4520f85fee79972191217d623c8b38522cacf74cb7c71113c0a6240d3b1f2ad2',
    'black_stained_glass': '62c705812949f0372dcc2fa82a5d89f7028ba1d9b3bd38765613e344f34f5b1c',
    'blue_stained_glass': '7d6cfe98ddc5d975b3bcf5f9cffc008f90db94d5d981ef440f7b68e8267ae247',
    'green_stained_glass': 'dc82be445bd9c7cf158bd57651d51bfef400310f2ad4937fe1e5b1c60b4f5916',
    'white_stained_glass': '2d4504957fa123a6e9f35d93e05f94fb053ec213541f01fcecbc0097eaa5df75',
}

def inspect(root):
    results = []
    alpha_masks = {}
    for name, want in EXPECTED.items():
        src = root / (name + '.png')
        raw = src.read_bytes()
        sha = hashlib.sha256(raw).hexdigest()
        if sha != want:
            raise RuntimeError('SHA mismatch: ' + str(src))
        with Image.open(src) as img:
            if img.size != (16, 16):
                raise RuntimeError('16x16 expected: ' + str(src))
            pix = img.convert('RGBA')
            pixels = list(pix.getdata())
        xy = lambda x, y: pixels[y * 16 + x]
        lr = [(xy(0, y), xy(15, y)) for y in range(16)]
        tb = [(xy(x, 0), xy(x, 15)) for x in range(16)]
        mismatch_rgb = lambda pairs: sum(abs(a[k] - b[k]) for a, b in pairs for k in range(3))
        cross = lambda dx, dy: sum(xy(x,y)[3]!=xy(x+dx,y+dy)[3] for y in range(16-dy) for x in range(16-dx))
        hist = {str(a): sum(p[3]==a for p in pixels) for a in sorted({p[3] for p in pixels})}
        alpha_masks[name] = tuple(p[3] for p in pixels)
        results.append(dict(texture_id=name,sha256=sha,rgba_pixels=256,alpha_histogram=hist,
            lr_rgba_exact_matches=sum(a==b for a,b in lr),tb_rgba_exact_matches=sum(a==b for a,b in tb),
            lr_alpha_exact_matches=sum(a[3]==b[3] for a,b in lr),tb_alpha_exact_matches=sum(a[3]==b[3] for a,b in tb),
            lr_rgb_mae=mismatch_rgb(lr)/(16*3),tb_rgb_mae=mismatch_rgb(tb)/(16*3),
            alpha_horizontal_transitions=cross(1,0),alpha_vertical_transitions=cross(0,1)))
    dyed = [n for n in EXPECTED if n!='glass']
    assert all(alpha_masks[n] == alpha_masks[dyed[0]] for n in dyed)
    assert all((a==255) == (b in (155,163)) for a,b in zip(alpha_masks['glass'],alpha_masks[dyed[0]]))
    return {'stage':'1-1-05','target_count':6,'unique_pixel_count':1536,'source':'six_existing_extracted_mirror_pngs',
            'mirrors_sha_match':6,'stained_alpha_masks_identical':True,'clear_alpha_template_same_as_stained_outlines':True,
            'official_client_jar_authenticated':False,'ingame_static_render_verified':False,'results':results}

if __name__ == '__main__':
    arg=argparse.ArgumentParser()
    arg.add_argument('--png-dir',type=Path,required=True,help='Directory containing the six previously extracted PNG files')
    a=arg.parse_args()
    print(json.dumps(inspect(a.png_dir),ensure_ascii=False,indent=2))
