#!/usr/bin/env python3
"""TEX04-R007 source-only audit. Requires numpy, Pillow.
python REPRODUCE_R007.py /path/to/1.21.11 /path/to/output
Outputs all 36 rank records, 73 inversion evidence rows and all 2295 toroidal shifts.
Does not authenticate official JAR or in-game rendering.
"""
import csv,io,hashlib,itertools,struct,sys,zlib
from pathlib import Path
import numpy as np
from PIL import Image
C=["white","red","blue","black","green","yellow","purple","cyan","orange"]
SHA=["70c9c9a9901d71ef9a5a89ea2cc4bc0d99ff5e65f733d1467da8b92f746107a5",
"07b48cec9b4610e908025807fb85fa686dd50f17918fa677ce655d28b3ba3464",
"2ca85a3e25a3ea9b0d8209edab2ab93f64e458d8c6baf8215536912159a6e2db",
"8cefbc855a4ff04f6125ded6a69e8bd21144802fc466b179665c8c0203daffd9",
"a2cd93d4bcead9b808d367fefa17081e12e5bd96ebff6993fc3d486422ecb9ad",
"cc77805bdc4ccb24d210ec65e304f1c367ae9e9ee0fed404ec99143bf62a2ef2",
"f8f5d7eb9145633d27d80c4c06a9a71e21eaea522c277f81a4d6d9e8fd60f0d9",
"68706949a22ed0877a42ddca38e5ec428039d52ff23e6614f2900e33cb759303",
"de3ec43fe8ca99026bdda3c036a964990e7d9b08c8b67690e2f975ddbdc5ff68"]
def write(out,name,header,rows):
    with (out/name).open("w",newline="",encoding="utf-8") as f:
        w=csv.writer(f);w.writerow(header);w.writerows(rows)
def load(root,c,sha):
    p=root/"assets/minecraft/textures/block"/(c+"_wool.png")
    b=p.read_bytes()
    assert hashlib.sha256(b).hexdigest()==sha and b[:8]==b"\x89PNG\r\n\x1a\n"
    i=8
    while i<len(b):
        assert i+12<=len(b)
        size=struct.unpack(">I",b[i:i+4])[0]; t=b[i+4:i+8]
        payload=b[i+8:i+8+size]
        assert len(payload)==size
        crc=struct.unpack(">I",b[i+8+size:i+12+size])[0]
        assert zlib.crc32(t+payload)&0xffffffff==crc
        i+=12+size
    assert i==len(b)
    im=Image.open(io.BytesIO(b));im.load()
    assert im.size==(16,16)
    a=np.array(im.convert("RGBA"))
    assert np.all(a[:,:,3]==255)
    return np.tensordot(a[:,:,:3].astype(np.int64),np.array([2126,7152,722]),axes=([2],[0]))
def main(root,out):
    out.mkdir(exist_ok=True,parents=True)
    Y={c:load(root,c,sha) for c,sha in zip(C,SHA)}
    i,j=np.triu_indices(256,1)
    ranks=[]; inverted=[]
    for a,b in itertools.combinations(C,2):
        A=Y[a].ravel();B=Y[b].ravel()
        dA=A[i]-A[j];dB=B[i]-B[j];mul=dA*dB
        good=int((mul>0).sum());bad=int((mul<0).sum());tied=int((mul==0).sum())
        assert good+bad+tied==32640
        ranks.append([a+"_wool",b+"_wool",32640,good+bad,good,bad,tied])
        for k in np.flatnonzero(mul<0):
            p,q=int(i[k]),int(j[k])
            inverted.append([a+"_wool",b+"_wool",p%16,p//16,q%16,q//16,int(A[p]),int(A[q]),int(B[p]),int(B[q])])
    write(out,"RANK_PAIRWISE_36.csv",["texture_a","texture_b","candidate","valid_both_nonzero","concordant","discordant","at_least_one_tie"],ranks)
    write(out,"RANK_INVERSION_73_EVIDENCE.csv",["a","b","x1","y1","x2","y2","a_y10000_1","a_y10000_2","b_y10000_1","b_y10000_2"],inverted)
    shifts=[];summary=[]
    for c in C:
        z=Y[c].astype(float);z-=z.mean()
        variance=(z*z).mean();results={}
        for dy in range(16):
            for dx in range(16):
                if dx==0 and dy==0:continue
                rho=float((z*np.roll(z,(dy,dx),axis=(0,1))).mean()/variance)
                results[dx,dy]=rho
                shifts.append([c+"_wool",dx,dy,round(rho,12)])
        best=max(results,key=results.get)
        summary.append([c+"_wool",best[0],best[1],round(results[best],12),255])
        assert best==(8,8)
        assert all(not np.array_equal(Y[c],np.roll(Y[c],(dy,dx),axis=(0,1))) for dx,dy in results)
    write(out,"TORUS_SHIFT_2295.csv",["texture_id","dx","dy","pearson"],shifts)
    write(out,"PERIODICITY_PER_COLOUR_9.csv",["texture_id","best_dx","best_dy","pearson","nonorigin_shifts"],summary)
    assert len(ranks)==36 and len(inverted)==73 and len(shifts)==2295
    assert sum(r[3] for r in ranks)==1130924 and sum(r[4] for r in ranks)==1130851
    assert sum(r[5] for r in ranks)==73
    assert len({tuple(r[2:6]) for r in inverted})==16
    assert all("green_wool" in r[:2] for r in inverted)
    print("9 existing source PNGs CRC+SHA256 rechecked; rank 1,175,040 candidates, 73 reversals; 2295 shifts. In-game 0/9.")
if __name__=="__main__":
    if len(sys.argv)!=3:raise SystemExit("python REPRODUCE_R007.py /path/to/1.21.11 output_dir")
    main(Path(sys.argv[1]),Path(sys.argv[2]))
