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


# --- TEX04-R008 NEW AUDIT (prior R007 source check retained verbatim above) ---
from collections import Counter, defaultdict

def r008(root, out):
    main(root,out)   # R007 source SHA256/PNG CRC, global 73 inversions, 2295 shifts checked
    source={}
    for c in C:
        path=root/"assets/minecraft/textures/block"/(c+"_wool.png")
        with Image.open(path) as im:
            im.load()
            source[c]=np.asarray(im.convert("RGB"))
    enc={c:np.tensordot(rgb.astype(np.int64),np.array([2126,7152,722],dtype=np.int64),axes=([2],[0])) for c,rgb in source.items()}
    srgb={c:rgb.astype(float)/255 for c,rgb in source.items()}
    linear={c:np.where(v<=0.04045,v/12.92,((v+0.055)/1.055)**2.4) for c,v in srgb.items()}
    lin={c:np.tensordot(v,np.array([.2126,.7152,.0722]),axes=([2],[0])) for c,v in linear.items()}
    i,j=np.triu_indices(256,1)
    per={}; inversions={}
    for tag,data in [("encoded",enc),("linear",lin)]:
        rows=[]; details=[]
        for a,b in itertools.combinations(C,2):
            aa=data[a].ravel();bb=data[b].ravel()
            mul=(aa[i]-aa[j])*(bb[i]-bb[j])
            same=int((mul>0).sum());bad=int((mul<0).sum())
            ties=int((mul==0).sum())
            assert same+bad+ties==32640
            rows.append([a+"_wool",b+"_wool",same+bad,same,bad,ties])
            for k in np.flatnonzero(mul<0):
                p,q=int(i[k]),int(j[k])
                details.append([a+"_wool",b+"_wool",p%16,p//16,q%16,q//16])
        per[tag]=rows;inversions[tag]=details
        assert len(details)==73 and sum(r[2] for r in rows)==1130924
        assert sum(r[3] for r in rows)==1130851
    assert inversions["encoded"]==inversions["linear"]
    dual=[[e[0],e[1],*e[2:],*l[2:]] for e,l in zip(per["encoded"],per["linear"])]
    write(out,"DUAL_METRIC_36_COLOUR_PAIRS.csv",["texture_a","texture_b","encoded_comparable","encoded_concordant","encoded_inversions","encoded_ties","linear_comparable","linear_concordant","linear_inversions","linear_ties"],dual)
    levels={
        "G1":{(75,94,34),(75,94,35)},
        "G2":{(74,92,35),(74,92,36)}
    }
    pairs=defaultdict(set);positions=set();total=Counter()
    for a,b,x1,y1,x2,y2 in inversions["encoded"]:
        c1=tuple(map(int,source["green"][y1,x1]))
        c2=tuple(map(int,source["green"][y2,x2]))
        matches=[name for name,lv in levels.items() if {c1,c2}==lv]
        assert len(matches)==1
        group=matches[0];total[group]+=1
        pairs[(group,x1,y1,x2,y2)].add(a if b=="green_wool" else b)
        positions.update({(x1,y1),(x2,y2)})
    assert total=={"G1":27,"G2":46} and len(pairs)==16 and len(positions)==14
    coord_rows=[]
    for (group,x1,y1,x2,y2),other_colors in sorted(pairs.items()):
        rgb1=source["green"][y1,x1]
        rgb2=source["green"][y2,x2]
        coord_rows.append([group,x1,y1,x2,y2,len(other_colors),"|".join(sorted(other_colors)),"|".join(map(str,rgb1)),"|".join(map(str,rgb2))])
    write(out,"INVERSION_GROUPED_16_COORD_PAIRS.csv",["group","x1","y1","x2","y2","color_pair_reversals","other_colors","green_rgb_p1","green_rgb_p2"],coord_rows)
    levelrows=[]
    for group, colors in levels.items():
        for red,grn,blu in sorted(colors):
            ys,xs=np.where(np.all(source["green"]==[red,grn,blu],axis=2))
            pos=sorted(zip(xs.tolist(),ys.tolist()),key=lambda t:(t[1],t[0]))
            levelrows.append([group,red,grn,blu,len(pos),"|".join(f"{x}:{y}" for x,y in pos)])
    write(out,"GREEN_RGB_4_LEVELS.csv",["group","r","g","b","pixel_count","coordinates_x_colon_y"],levelrows)
    at_positions=[]
    for x,y in sorted(positions,key=lambda p:(p[1],p[0])):
        for c in C:
            red,grn,blu=map(int,source[c][y,x])
            at_positions.append([x,y,c+"_wool",red,grn,blu,int(enc[c][y,x]),f"{float(lin[c][y,x]):.12f}"])
    assert len(at_positions)==126
    write(out,"RGB_AT_14_POSITIONS_9_COLORS.csv",["x","y","texture_id","r","g","b","encoded_y_times_10000","linear_relative_y"],at_positions)
    result={"source_png_rechecked":9,"new_unique_png":0,"global_position_discordance_both_metrics":73,"metric_inversion_coordinate_identity":True,"green_level_pairs":2,"distinct_green_rgb_levels":4,"unique_positions":14,"unique_position_pairs":16,"G1_source_position_pairs":9,"G1_color_pair_inversions":27,"G2_source_position_pairs":7,"G2_color_pair_inversions":46,"new_rgb_audit_rows":126,"ingame_static_verified":0}
    (out/"R008_CHECK.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("TEX04-R008",json.dumps(result,ensure_ascii=False))

if __name__=="__main__":
    if len(sys.argv)!=3:raise SystemExit("python REPRODUCE_R008.py /path/to/1.21.11 output_dir")
    r008(Path(sys.argv[1]),Path(sys.argv[2]))
