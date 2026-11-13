#!/usr/bin/env python3
"""Recompute TEX07-R006 source-only metrics on the user's extracted 1.21.11 folder.
Requires Python 3, Pillow and NumPy. No web or Minecraft runtime needed."""
import argparse, csv, hashlib, io, struct, zlib
from pathlib import Path
import numpy as np
from PIL import Image

COLORS = ("white","black","red","blue","green","yellow","gray")
COLUMNS = ["texture","user_png_git_sha1","sha256","png_size_bytes","png_chunk_count","mean_Y_709","Y_range","Y_std_population","luma_corr_wrap_x1","luma_corr_wrap_y1","best_nonzero_toroidal_corr","best_shift_dx","best_shift_dy","max_lr_seam_Y","max_tb_seam_Y","max_interior_adjacent_Y","lr_seam_pairs_gt_max_interior","tb_seam_pairs_gt_max_interior","identical_row_pairs","identical_column_pairs","unique_RGB","static_model_face_refs_inherited"]

def compute(path):
    b = path.read_bytes()
    assert b.startswith(b"\x89PNG\r\n\x1a\n"), path
    pos, chunks = 8, 0
    while pos < len(b):
        n = struct.unpack(">I",b[pos:pos+4])[0]
        typ=b[pos+4:pos+8]
        crc_expected=struct.unpack(">I",b[pos+8+n:pos+12+n])[0]
        assert zlib.crc32(b[pos+4:pos+8+n]) & 0xffffffff == crc_expected, (path,typ)
        pos += n+12
        chunks += 1
        if typ == b"IEND": break
    assert pos == len(b), path
    a=np.asarray(Image.open(io.BytesIO(b)).convert("RGBA"))
    assert a.shape == (16,16,4) and np.all(a[:,:,3] == 255), path
    rgb=a[:,:,:3].astype(float)
    y=np.tensordot(rgb,np.array([.2126,.7152,.0722]), axes=([2],[0]))
    cy=y-y.mean()
    var=np.mean(cy**2)
    def corr(dx,dy):
        z=np.roll(np.roll(cy,dx,axis=1),dy,axis=0)
        return float(np.mean(cy*z)/var) if var else 0.0
    shifts=[(corr(dx,dy),dx,dy) for dx in range(16) for dy in range(16) if (dx,dy)!=(0,0)]
    best=max(shifts)
    seams_x=np.abs(y[:,-1]-y[:,0])
    seams_y=np.abs(y[-1,:]-y[0,:])
    internal=np.r_[np.abs(np.diff(y,axis=1)).ravel(),np.abs(np.diff(y,axis=0)).ravel()]
    maxi=float(internal.max())
    pairs_row=sum(np.array_equal(rgb[i],rgb[j]) for i in range(16) for j in range(i+1,16))
    pairs_col=sum(np.array_equal(rgb[:,i],rgb[:,j]) for i in range(16) for j in range(i+1,16))
    sha1=hashlib.sha1(b"blob "+str(len(b)).encode()+b"\x00"+b).hexdigest()
    return [path.stem,sha1,hashlib.sha256(b).hexdigest(),len(b),chunks,
            round(float(y.mean()),6),round(float(np.ptp(y)),6),round(float(np.sqrt(var)),6),
            round(corr(-1,0),6),round(corr(0,-1),6),round(best[0],6),best[1],best[2],
            round(float(seams_x.max()),6),round(float(seams_y.max()),6),round(maxi,6),
            int(np.sum(seams_x>maxi)),int(np.sum(seams_y>maxi)),pairs_row,pairs_col,
            len(np.unique(rgb.reshape(-1,3),axis=0)),6]

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--root",required=True,help="Unzipped user's 1.21.11 folder")
    p.add_argument("--output",default="7_SPATIAL_NOISE_EDGE_AUDIT.csv")
    args=p.parse_args()
    folder=Path(args.root)/"assets/minecraft/textures/block"
    with open(args.output,"w",newline="",encoding="utf-8") as f:
        w=csv.writer(f,lineterminator="\n")
        w.writerow(COLUMNS)
        for c in COLORS: w.writerow(compute(folder/(c+"_concrete.png")))
    print("Wrote",args.output)
