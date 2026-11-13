#!/usr/bin/env python3
"""TEX04-R005 static source audit. Run: python REPRODUCE_R005.py /path/to/1.21.11
Requires numpy and Pillow. No game rendering or official JAR authentication."""
import csv, hashlib, io, json, struct, sys, zlib
from pathlib import Path
import numpy as np
from PIL import Image

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("1.21.11")
COLORS = ["white","red","blue","black","green","yellow","purple","cyan","orange"]
EXPECTED_SHA256 = {
  "white": "70c9c9a9901d71ef9a5a89ea2cc4bc0d99ff5e65f733d1467da8b92f746107a5",
  "red": "07b48cec9b4610e908025807fb85fa686dd50f17918fa677ce655d28b3ba3464",
  "blue": "2ca85a3e25a3ea9b0d8209edab2ab93f64e458d8c6baf8215536912159a6e2db",
  "black": "8cefbc855a4ff04f6125ded6a69e8bd21144802fc466b179665c8c0203daffd9",
  "green": "a2cd93d4bcead9b808d367fefa17081e12e5bd96ebff6993fc3d486422ecb9ad",
  "yellow": "cc77805bdc4ccb24d210ec65e304f1c367ae9e9ee0fed404ec99143bf62a2ef2",
  "purple": "f8f5d7eb9145633d27d80c4c06a9a71e21eaea522c277f81a4d6d9e8fd60f0d9",
  "cyan": "68706949a22ed0877a42ddca38e5ec428039d52ff23e6614f2900e33cb759303",
  "orange": "de3ec43fe8ca99026bdda3c036a964990e7d9b08c8b67690e2f975ddbdc5ff68"
}
w = np.array([0.2126, 0.7152, 0.0722])
def lum(rgb):
    return (rgb.astype(float) * w).sum(axis=-1)
def corr(a,b):
    return float(np.corrcoef(a.ravel(), b.ravel())[0,1])
def read_png(color):
    p=ROOT/"assets/minecraft/textures/block"/(color+"_wool.png")
    raw=p.read_bytes()
    assert hashlib.sha256(raw).hexdigest()==EXPECTED_SHA256[color], color+" SHA256 mismatch"
    assert raw[:8]==b"\\x89PNG\\r\\n\\x1a\\n"
    k=8
    while k<len(raw):
        n=struct.unpack(">I",raw[k:k+4])[0]; typ=raw[k+4:k+8]; v=raw[k+8:k+8+n]
        crc=struct.unpack(">I",raw[k+8+n:k+12+n])[0]
        assert (zlib.crc32(typ+v)&0xffffffff)==crc, (color,typ)
        k+=12+n
    im=Image.open(io.BytesIO(raw)); im.load()
    assert im.size==(16,16)
    rgba=np.asarray(im.convert("RGBA"))
    assert bool(np.all(rgba[:,:,3]==255))
    return np.asarray(im), rgba[:,:,:3]
png={c:read_png(c) for c in COLORS}
base=lum(png["white"][1])
D4={
    "identity":lambda a:a,"rotation90":lambda a:np.rot90(a,1),
    "rotation180":lambda a:np.rot90(a,2),"rotation270":lambda a:np.rot90(a,3),
    "flip_left_right":np.fliplr,"flip_top_bottom":np.flipud,
    "transpose":lambda a:a.T,"anti_transpose":lambda a:np.rot90(a.T,2)
}
def save(filename,header,rows):
    with open(filename,"w",newline="",encoding="utf-8") as f:
        t=csv.writer(f);t.writerow(header);t.writerows(rows)
colrows=[];d4rows=[];pairs=[]
for c in COLORS:
    idx,rgb=png[c]; yy=lum(rgb)
    X=np.column_stack((base.ravel(),np.ones(256)))
    fitted=np.stack([X@np.linalg.lstsq(X,rgb[:,:,k].ravel(),rcond=None)[0] for k in range(3)],axis=1)
    err=fitted-rgb.reshape(256,3)
    colour_fit=np.array([np.linalg.lstsq(X,rgb[:,:,k].ravel(),rcond=None)[0] for k in range(3)])
    h=np.diff(yy,axis=1);bh=np.diff(base,axis=1)
    v=np.diff(yy,axis=0);bv=np.diff(base,axis=0)
    hm=(h!=0)&(bh!=0);vm=(v!=0)&(bv!=0)
    assert np.all(np.sign(h[hm])==np.sign(bh[hm]))
    assert np.all(np.sign(v[vm])==np.sign(bv[vm]))
    colrows.append([c+"_wool",EXPECTED_SHA256[c],int((idx==png["white"][0]).sum()),round(corr(yy,base),8),round(float(np.sqrt(np.mean(err**2))),5),round(float(np.max(np.abs(err))),5),*[round(float(x),6) for x in colour_fit.ravel()],int(hm.sum()),int(vm.sum()),1.0,1.0])
    for k,trans in D4.items():
        d4rows.append([c+"_wool",k,round(corr(yy,trans(base)),8)])
for i,a in enumerate(COLORS):
    for b in COLORS[i+1:]:
        ia,ra=png[a];ib,rb=png[b]
        ya=lum(ra);yb=lum(rb)
        ah=np.diff(ya,axis=1);bh=np.diff(yb,axis=1)
        av=np.diff(ya,axis=0);bv=np.diff(yb,axis=0)
        hm=(ah!=0)&(bh!=0);vm=(av!=0)&(bv!=0)
        pairs.append([a+"_wool",b+"_wool",int((ia==ib).sum()),int(hm.sum()),int((np.sign(ah[hm])==np.sign(bh[hm])).sum()),int(vm.sum()),int((np.sign(av[vm])==np.sign(bv[vm])).sum())])
assert sum(x[3] for x in pairs)==7933 and sum(x[5] for x in pairs)==8471
assert all(x[3]==x[4] and x[5]==x[6] for x in pairs)
assert all(max([r for r in d4rows if r[0]==c+"_wool"],key=lambda r:r[2])[1]=="identity" for c in COLORS)
save("COLOR_SUBSTITUTION.csv",["texture_id","png_sha256","palette_index_positions_equal_to_white_256","luma_pearson_to_white","affine_rgb_rmse_0_255","affine_rgb_max_absolute_residual","R_slope","R_intercept","G_slope","G_intercept","B_slope","B_intercept","h_nonzero_gradient_pairs_to_white","v_nonzero_gradient_pairs_to_white","h_gradient_sign_concordance","v_gradient_sign_concordance"],colrows)
save("D4_ORIENTATION.csv",["texture_id","reference_white_wool_transform","pearson_luma"],d4rows)
save("PAIRWISE_GRADIENT_SIGNS.csv",["texture_a","texture_b","palette_indices_equal_positions","common_nonzero_horiz_adjacent_gradient_pairs","agreeing_horiz_gradient_signs","common_nonzero_vert_adjacent_gradient_pairs","agreeing_vert_gradient_signs"],pairs)
p=ROOT/"assets/minecraft"
cube=json.loads((p/"models/block/cube.json").read_text())
cube_all=json.loads((p/"models/block/cube_all.json").read_text())
assert cube_all["parent"]=="block/cube" and cube["parent"]=="block/block"
assert cube["elements"][0]["from"]==[0,0,0] and cube["elements"][0]["to"]==[16,16,16]
assert len(cube["elements"][0]["faces"])==6
for c in COLORS:
    leaf=json.loads((p/("models/block/"+c+"_wool.json")).read_text())
    bs=json.loads((p/("blockstates/"+c+"_wool.json")).read_text())
    assert leaf["parent"]=="minecraft:block/cube_all"
    assert leaf["textures"]["all"]=="minecraft:block/"+c+"_wool"
    assert bs["variants"]=={"":{"model":"minecraft:block/"+c+"_wool"}}
    assert all("uv" not in f and "rotation" not in f for f in cube["elements"][0]["faces"].values())
print("verified: 9 PNG, 36 spatial pair comparisons, 72 D4 comparisons, 9 static variant chains; game render NOT verified")
