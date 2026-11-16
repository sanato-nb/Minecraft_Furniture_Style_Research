#!/usr/bin/env python3
"""F Entry6 original PNG first-frame audit. GitHub Actions runner reads repository source directly."""
import base64, csv, hashlib, io, json, os, subprocess, math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageStat

REPO=Path(__file__).resolve().parents[1]
ROOT=REPO/"research/vanilla_models/phase_1-2-F/entry6"
MANIFEST=ROOT/"F_ENTRY6_PNG_QUEUE_332.json"
OUT=ROOT/"visual_contact"
OUT.mkdir(parents=True,exist_ok=True)
manifest=json.loads(MANIFEST.read_text(encoding="utf-8"))
assert manifest["unique_png_count"]==332
raw=manifest["png_paths"]
records=[]
fnt=ImageFont.load_default()
for i,x in enumerate(raw,1):
    path=REPO/x["path"]
    assert path.is_file(), f"missing: {path}"
    sha=subprocess.check_output(["git","hash-object",str(path)],cwd=REPO,text=True).strip()
    assert sha==x["sha"], f"SHA: {path}: {sha} != {x['sha']}"
    with Image.open(path) as inp:
        rgba=inp.convert("RGBA")
        w,h=rgba.size
        full_hash=hashlib.sha256(rgba.tobytes()).hexdigest()
        assert full_hash==x["rgba_sha256"], f"RGBA mismatch: {path}: {full_hash}"
        frame=rgba.crop((0,0,w,min(h,w)))
        full_pixels=list(frame.getdata())
        opaque=[(r,g,b,a) for r,g,b,a in full_pixels if a>0]
        alpha_nonzero=sum(1 for p in full_pixels if p[3]>0)
        alpha_partial=sum(1 for p in full_pixels if 0<p[3]<255)
        frac=alpha_nonzero/len(full_pixels) if full_pixels else 0
        if opaque:
            mean=[round(sum(p[c] for p in opaque)/len(opaque),1) for c in range(3)]
        else: mean=[0,0,0]
        records.append(dict(index=i,path=x["path"],source_git_sha=x["sha"],source_RGBA_SHA256=x["rgba_sha256"],full_width=w,full_height=h,first_frame_width=w,first_frame_height=min(h,w),alpha_covered=round(frac,5),partly_transparent_pixels=alpha_partial,approx_frame_count=math.ceil(h/w) if w else 0,avg_visible_RGB=str(mean),first_frame_sha256=hashlib.sha256(frame.tobytes()).hexdigest()))
        # Store only first frame crop in memory as needed per contact sheet.
        sheet_index=(i-1)//42
        if (i-1)%42==0:
            canvas=Image.new("RGB",(7*180,6*156),(242,245,249))
            draw=ImageDraw.Draw(canvas)
        pos=(i-1)%42; col=pos%7; row=pos//7
        left=col*180; top=row*156
        draw.rectangle([left+2,top+2,left+176,top+153],outline=(160,172,190),width=1)
        # Checkerboard gives a real visual basis for detecting alpha holes.
        bg=Image.new("RGBA",(112,112),(242,242,242,255))
        bd=ImageDraw.Draw(bg)
        for y in range(0,112,16):
            for xx in range(0,112,16):
                if (xx//16+y//16)%2: bd.rectangle([xx,y,xx+15,y+15],fill=(207,213,222,255))
        # 112px preview from first frame with nearest pixel resampling
        pw,ph=frame.size
        z=min(112/max(pw,1),112/max(ph,1))
        sz=(max(1,round(pw*z)),max(1,round(ph*z)))
        big=frame.resize(sz,Image.Resampling.NEAREST)
        bg.alpha_composite(big,((112-sz[0])//2,(112-sz[1])//2))
        canvas.paste(bg.convert("RGB"),(left+32,top+18))
        label=f"{i:03d} "+path.name.replace(".png","")
        if len(label)>26: label=label[:25]+"~"
        draw.text((left+8,top+5),label,fill=(22,39,59),font=fnt)
        draw.text((left+8,top+133),f"{w}x{h} / alpha {int(frac*100)}%",fill=(43,58,77),font=fnt)
        if pos==41 or i==len(raw):
            index=sheet_index+1
            png=OUT/f"contact_{index:02d}.png"
            jpg=OUT/f"contact_{index:02d}.jpg"
            canvas.save(png,optimize=True)
            canvas.save(jpg,quality=83,optimize=True,subsampling=0)
            print(f"F3_SHEET_RESULT {index:02d} first={i-pos} last={i} jpeg_bytes={jpg.stat().st_size} png_sha256={hashlib.sha256(png.read_bytes()).hexdigest()}",flush=True)
            # Image content emitted as text in log, reassembled by authenticated connector.
            encoded=base64.b64encode(jpg.read_bytes()).decode("ascii")
            chunk=2400
            print(f"F3_IMAGE_START id={index:02d} chunks={math.ceil(len(encoded)/chunk)}",flush=True)
            for k in range(0,len(encoded),chunk):
                print(f"F3_IMAGE_CHUNK {index:02d} {k//chunk:04d} {encoded[k:k+chunk]}",flush=True)
            print(f"F3_IMAGE_END id={index:02d}",flush=True)
with (OUT/"F3_FIRST_FRAME_PIXEL_AUDIT.csv").open("w",encoding="utf-8",newline="") as f:
    wr=csv.DictWriter(f,fieldnames=list(records[0]));wr.writeheader();wr.writerows(records)
stats={"schema":"F3_ENTRY6_ORIGINAL_PNG_PIXEL_AUDIT/v1","texture_paths":len(records),"all_git_sha_match":True,"all_C_RGBA_SHA256_match":True,"unique_full_images":len(set(x["source_git_sha"] for x in records)),"images_have_visible_first_frame":sum(x["alpha_covered"]>0 for x in records),"fully_transparent_first_frame":sum(x["alpha_covered"]==0 for x in records),"partially_transparent_first_frame":sum(x["alpha_covered"]<1 for x in records),"animated_tall_png_count":sum(x["full_height"]>x["full_width"] for x in records),"original_image_visual_contact_sheets":math.ceil(len(records)/42),"not_claimed":"Game runtime renderer or per-model semantic identification"}
(OUT/"F3_PIXEL_AUDIT_SUMMARY.json").write_text(json.dumps(stats,indent=2)+"\n",encoding="utf-8")
print("F3_PIXEL_AUDIT_FINISHED "+json.dumps(stats,ensure_ascii=True),flush=True)
