#!/usr/bin/env python3
"""Reproduce TEX07-R007 from the user's extracted 1.21.11 folder.
Requires Python 3, NumPy, Pillow. No Minecraft runtime or network access."""
import argparse
import csv
import hashlib
from pathlib import Path
import numpy as np
from PIL import Image

COLORS = ("white", "black", "red", "blue", "green", "yellow", "gray")
B = 20000
BASE_SEED = 20261113
KEYS = [
"texture","source_sha256","rng_seed","permutations",
"observed_max_torus_corr","null_mean_max_corr","null_p95_max_corr",
"max_corr_exceedances","max_corr_empirical_p",
"observed_low_freq_energy_fraction","null_mean_low_freq_fraction",
"null_p95_low_freq_fraction","low_freq_exceedances","low_freq_empirical_p",
"max_corr_holm14_adjusted_p","low_freq_holm14_adjusted_p"
]
fy = np.fft.fftfreq(16)*16
fx = np.fft.fftfreq(16)*16
fmask = (np.abs(fy[:,None]) <= 2) & (np.abs(fx[None,:]) <= 2)
fmask[0,0] = False

def features(y):
    centered = y - y.mean(axis=(-2,-1), keepdims=True)
    spectrum = np.fft.fft2(centered,axes=(-2,-1))
    energy = np.abs(spectrum)**2
    corr = np.fft.ifft2(energy,axes=(-2,-1)).real
    corr /= np.sum(centered**2,axis=(-2,-1))[...,None,None]
    corr[...,0,0] = -np.inf
    max_shift_corr = np.max(corr,axis=(-2,-1))
    low_freq_share = np.sum(energy*fmask,axis=(-2,-1))/np.sum(energy,axis=(-2,-1))
    return max_shift_corr,low_freq_share

def calculate(texture_path,index):
    b = texture_path.read_bytes()
    rgba=np.asarray(Image.open(texture_path).convert("RGBA"))
    assert rgba.shape == (16,16,4)
    assert np.all(rgba[:,:,3] == 255)
    y = rgba[:,:,:3].astype(np.float64) @ np.array([.2126,.7152,.0722])
    observed = (float(features(y)[0]),float(features(y)[1]))
    rng = np.random.default_rng(BASE_SEED+index)
    exceedances=[0,0]
    simulations=[[],[]]
    for _ in range(B//1000):
        indices=np.argsort(rng.random((1000,256)),axis=-1)
        permuted=y.ravel()[indices].reshape(1000,16,16)
        generated=features(permuted)
        for j,vals in enumerate(generated):
            exceedances[j]+=int(np.count_nonzero(vals >= observed[j]-1e-13))
            simulations[j].append(vals)
    null0=np.concatenate(simulations[0])
    null1=np.concatenate(simulations[1])
    return dict(
      texture=texture_path.stem,source_sha256=hashlib.sha256(b).hexdigest(),
      rng_seed=BASE_SEED+index, permutations=B,
      observed_max_torus_corr=round(observed[0],9),
      null_mean_max_corr=round(float(null0.mean()),9),
      null_p95_max_corr=round(float(np.quantile(null0,.95)),9),
      max_corr_exceedances=exceedances[0],
      max_corr_empirical_p=round((1+exceedances[0])/(B+1),9),
      observed_low_freq_energy_fraction=round(observed[1],9),
      null_mean_low_freq_fraction=round(float(null1.mean()),9),
      null_p95_low_freq_fraction=round(float(np.quantile(null1,.95)),9),
      low_freq_exceedances=exceedances[1],
      low_freq_empirical_p=round((1+exceedances[1])/(B+1),9))

def holm_14(rows):
    allp=sorted((r[field],i,field) for i,r in enumerate(rows)
               for field in ("max_corr_empirical_p","low_freq_empirical_p"))
    running=0
    for j,(p,i,key) in enumerate(allp):
        running=max(running,p*(len(allp)-j))
        rows[i][key.replace("empirical_p","holm14_adjusted_p")] = round(min(1,running),9)

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--root",required=True,help="Path to extracted 1.21.11 folder")
    parser.add_argument("--output",default="7_PERMUTATION_SPATIAL_TESTS.csv")
    args=parser.parse_args()
    root=Path(args.root)/"assets/minecraft/textures/block"
    rows=[calculate(root/(color+"_concrete.png"),i) for i,color in enumerate(COLORS)]
    holm_14(rows)
    with open(args.output,"w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=KEYS)
        writer.writeheader()
        writer.writerows(rows)
    print("Wrote",args.output,"7 PNGs; 140000 permutations; 14 one-sided tests")
