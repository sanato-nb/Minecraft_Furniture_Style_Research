#!/usr/bin/env python3
"""Reproduce TEX04-R002 from the nine local 1.21.11 mirror PNGs.
No network operations, no copyrighted PNG redistribution, no animation processing.
Optional JAR comparison alone does NOT authenticate metadata provenance.
"""
import argparse
import csv
import hashlib
import io
import itertools
import json
import zipfile
from pathlib import Path
import numpy as np
from PIL import Image
from scipy.stats import pearsonr, spearmanr

COLORS = ("white", "red", "blue", "black", "green", "yellow", "purple", "cyan", "orange")
SHA256 = dict(zip(COLORS, (
    "70c9c9a9901d71ef9a5a89ea2cc4bc0d99ff5e65f733d1467da8b92f746107a5",
    "07b48cec9b4610e908025807fb85fa686dd50f17918fa677ce655d28b3ba3464",
    "2ca85a3e25a3ea9b0d8209edab2ab93f64e458d8c6baf8215536912159a6e2db",
    "8cefbc855a4ff04f6125ded6a69e8bd21144802fc466b179665c8c0203daffd9",
    "a2cd93d4bcead9b808d367fefa17081e12e5bd96ebff6993fc3d486422ecb9ad",
    "cc77805bdc4ccb24d210ec65e304f1c367ae9e9ee0fed404ec99143bf62a2ef2",
    "f8f5d7eb9145633d27d80c4c06a9a71e21eaea522c277f81a4d6d9e8fd60f0d9",
    "68706949a22ed0877a42ddca38e5ec428039d52ff23e6614f2900e33cb759303",
    "de3ec43fe8ca99026bdda3c036a964990e7d9b08c8b67690e2f975ddbdc5ff68",
)))

def digest(data, alg="sha256"):
    return hashlib.new(alg, data).hexdigest()

def save_csv(path, rows):
    with path.open("w", encoding="utf-8", newline="") as f:
        w=csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("png_dir", type=Path)
    parser.add_argument("--output", type=Path, default=Path("."))
    parser.add_argument("--jar", type=Path)
    parser.add_argument("--version-json", type=Path)
    a=parser.parse_args()
    a.output.mkdir(parents=True, exist_ok=True)

    rgb={}; indices={}
    for name in COLORS:
        data=(a.png_dir/(name+"_wool.png")).read_bytes()
        assert digest(data)==SHA256[name], name+" original SHA mismatch"
        im=Image.open(io.BytesIO(data))
        assert im.mode=="P" and im.size==(16,16), name+" PNG dimensions/mode mismatch"
        alpha=np.asarray(im.convert("RGBA"))[:,:,3]
        assert np.all(alpha==255), name+" alpha mismatch"
        rgb[name]=np.asarray(im.convert("RGB"), dtype=np.float64)
        indices[name]=np.asarray(im, dtype=np.int16)

    luma={n:(v @ np.array([0.2126,0.7152,0.0722])).ravel()
          for n,v in rgb.items()}

    pairs=[]
    for first,second in itertools.combinations(COLORS,2):
        equal=int(np.count_nonzero(indices[first]==indices[second]))
        pairs.append(dict(pair_a=first+"_wool", pair_b=second+"_wool",
            spearman_luma=f"{spearmanr(luma[first],luma[second]).statistic:.8f}",
            pearson_luma=f"{pearsonr(luma[first],luma[second]).statistic:.8f}",
            palette_index_equal_pixels=equal,
            palette_index_equal_fraction=f"{equal/256:.8f}"))

    seams=[]
    for n in COLORS:
        im=rgb[n]
        h=float(np.abs(im[:,:-1,:]-im[:,1:,:]).mean())
        v=float(np.abs(im[:-1,:,:]-im[1:,:,:]).mean())
        lr=float(np.abs(im[:,0,:]-im[:,-1,:]).mean())
        tb=float(np.abs(im[0,:,:]-im[-1,:,:]).mean())
        seams.append(dict(texture_id=n+"_wool",
            horiz_adjacent=f"{h:.6f}",vertical_adjacent=f"{v:.6f}",
            left_right_seam=f"{lr:.6f}",top_bottom_seam=f"{tb:.6f}",
            lr_over_h=f"{lr/h:.6f}",tb_over_v=f"{tb/v:.6f}",
            sha256=SHA256[n]))

    save_csv(a.output/"PAIRWISE_COLOUR_PATTERN.csv",pairs)
    save_csv(a.output/"SEAM_REPEAT_AUDIT.csv",seams)
    report={
        "source_pixel_sha_checked":9,
        "pair_count":36,
        "spearman_min":min(float(x["spearman_luma"]) for x in pairs),
        "spearman_max":max(float(x["spearman_luma"]) for x in pairs),
        "lr_over_h_min":min(float(x["lr_over_h"]) for x in seams),
        "lr_over_h_max":max(float(x["lr_over_h"]) for x in seams),
        "official_jar_authenticated":False,
        "ingame_static_verified":False,
    }

    if a.jar or a.version_json:
        if not (a.jar and a.version_json):
            raise ValueError("Provide BOTH candidate JAR and version JSON")
        metadata=json.loads(a.version_json.read_text(encoding="utf-8"))
        assert metadata["id"]=="1.21.11"
        expected=metadata["downloads"]["client"]
        jar=a.jar.read_bytes()
        report["candidate_jar_sha1"]=digest(jar,"sha1")
        report["candidate_jar_matches_supplied_metadata"]=(
            digest(jar,"sha1")==expected["sha1"] and len(jar)==expected["size"])
        with zipfile.ZipFile(io.BytesIO(jar)) as z:
            report["candidate_jar_png_sha256_matches"]={
                n: digest(z.read(f"assets/minecraft/textures/block/{n}_wool.png"))==SHA256[n]
                for n in COLORS}
        # This tool does not establish whether the metadata JSON came from Mojang.
        report["official_jar_authenticated"]=False

    (a.output/"REPRODUCE_SUMMARY.json").write_text(
        json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
