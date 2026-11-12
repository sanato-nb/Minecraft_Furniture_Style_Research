#!/usr/bin/env python3
"""Minecraft Java 1.21.11 block texture analysis. No source PNGs distributed.

Usage examples:
  python analyze_vanilla.py --assets-dir path/to/assets/minecraft/textures/block --output results
  python analyze_vanilla.py --client-jar path/to/1.21.11.jar --output results

Supply a legitimately obtained client jar or extracted game assets yourself.
The input game's version is not auto-verified; set --version after checking it.
"""
from __future__ import annotations
import argparse, collections, csv, hashlib, io, json, math, zipfile
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

FAMILIES = {
    '목재': ['oak_planks', 'spruce_planks', 'birch_planks', 'dark_oak_planks', 'cherry_planks', 'mangrove_planks', 'oak_log_top', 'stripped_oak_log'],
    '석재·벽돌': ['stone', 'cobblestone', 'stone_bricks', 'deepslate_bricks', 'polished_andesite', 'bricks', 'tuff_bricks'],
    '금속': ['iron_block', 'copper_block', 'exposed_copper', 'oxidized_copper'],
    '직물': ['white_wool', 'red_wool', 'blue_wool'],
    '유리': ['glass', 'red_stained_glass'],
    '도기·색면': ['terracotta', 'white_terracotta', 'orange_terracotta'],
    '기타·가공면': ['white_concrete', 'black_concrete', 'crafting_table_front'],
}
LABELS={name:fam for fam,names in FAMILIES.items() for name in names}
SRC_ROOT='assets/minecraft/textures/block/'
COLS=['texture_id','family','edition','game_version','source_branch','source_path','source_url','sha256','width','height','pixels_total','visible_pixels','visible_pct','fully_opaque_pct','mean_alpha','unique_rgb_visible','dominant_rgb','dominant_pct_visible','median_rgb','mean_luma','luma_std','mean_saturation','adjacent_horizontal_delta','adjacent_vertical_delta','direction_ratio_vertical_over_horizontal','left_right_seam_delta','top_bottom_seam_delta','shannon_entropy_colors_bits','png_bytes','evidence_type','verification']

def pxstats(name,data,version):
    im=Image.open(io.BytesIO(data));im.load(); im=im.convert('RGBA')
    ar=np.asarray(im,dtype=np.uint8); rgb=ar[:,:,:3];alpha=ar[:,:,3]
    v=alpha>0; full=alpha==255
    pix=rgb[v]
    if pix.size==0: raise ValueError('entirely transparent: '+name)
    pal=collections.Counter(tuple(int(k) for k in p) for p in pix)
    dominant,count=pal.most_common(1)[0]
    n=len(pix)
    probs=np.array(list(pal.values()),dtype=float)/n
    ent=float(-(probs*np.log2(probs)).sum())
    med=np.median(pix,axis=0).astype(int)
    luma=(.2126*rgb[:,:,0]+.7152*rgb[:,:,1]+.0722*rgb[:,:,2]).astype(float)
    lo,hi=pix.min(axis=1),pix.max(axis=1)
    sat=(hi-lo)/np.maximum(hi,1)
    def avg_neighbor(axis):
        if axis=='x':
            a=rgb[:,:-1].astype(float);b=rgb[:,1:].astype(float); mask=v[:,:-1]&v[:,1:]
        else:
            a=rgb[:-1].astype(float);b=rgb[1:].astype(float);mask=v[:-1]&v[1:]
        if not mask.any():return None
        return float(np.abs(a-b).mean(axis=2)[mask].mean())
    def avg_seam(axis):
        if axis=='x':a=rgb[:,0].astype(float);b=rgb[:,-1].astype(float);mask=v[:,0]&v[:,-1]
        else:a=rgb[0].astype(float);b=rgb[-1].astype(float);mask=v[0]&v[-1]
        if not mask.any():return None
        return float(np.abs(a-b).mean(axis=1)[mask].mean())
    horiz=avg_neighbor('x');vert=avg_neighbor('y')
    fmt=lambda a: '#%02X%02X%02X'%tuple(int(x) for x in a)
    round4=lambda x: '' if x is None else round(float(x),4)
    return {
        'texture_id':name,'family':LABELS[name], 'edition':'Java', 'game_version':version,
        'source_branch':version,'source_path':SRC_ROOT+name+'.png',
        'source_url':f'https://github.com/InventivetalentDev/minecraft-assets/blob/{version}/{SRC_ROOT}{name}.png',
        'sha256':hashlib.sha256(data).hexdigest(), 'width':im.width, 'height':im.height,
        'pixels_total':int(alpha.size), 'visible_pixels':int(v.sum()),'visible_pct':round4(v.mean()*100),
        'fully_opaque_pct':round4(full.mean()*100), 'mean_alpha':round4(alpha.mean()),
        'unique_rgb_visible':len(pal),'dominant_rgb':fmt(dominant),'dominant_pct_visible':round4(count/n*100),
        'median_rgb':fmt(med), 'mean_luma':round4(luma[v].mean()),'luma_std':round4(luma[v].std()),
        'mean_saturation':round4(sat.mean()),
        'adjacent_horizontal_delta':round4(horiz),'adjacent_vertical_delta':round4(vert),
        'direction_ratio_vertical_over_horizontal':round4(vert/horiz if horiz and vert is not None else None),
        'left_right_seam_delta':round4(avg_seam('x')),'top_bottom_seam_delta':round4(avg_seam('y')),
        'shannon_entropy_colors_bits':round4(ent),'png_bytes':len(data),
        'evidence_type':'원본파일_확인','verification':'PIL_PNG_decode_ok',
    }, luma

def write_csv(path,rows,cols):
    with path.open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=cols,extrasaction='ignore');w.writeheader();w.writerows(rows)

def chart(rows,out):
    # Show summary statistics only, NOT copied original source pixels.
    width=1240;row_h=52;h=120+row_h*len(rows)
    img=Image.new('RGB',(width,h),'#f5f6f8');d=ImageDraw.Draw(img)
    font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',16) if Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf').is_file() else ImageFont.load_default()
    fontb=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',19) if Path('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf').is_file() else font
    d.text((22,20),'Minecraft Java 1.21.11 - sampled texture metrics (non-original visualization)',fill='#222c36',font=fontb)
    d.text((22,60),'Each stripe shows median RGB, unique visible RGB colors, and mean brightness. Original pixel layouts are NOT reproduced.',fill='#596675',font=font)
    for i,r in enumerate(rows):
        y=100+i*row_h
        if i%2==0:d.rectangle((8,y,width-9,y+row_h-2),fill='#e9edf1')
        d.text((20,y+12),r['texture_id'],fill='#28323d',font=font)
        d.rectangle((250,y+7,390,y+43),fill=r['median_rgb'],outline='#74797f',width=1)
        d.text((413,y+13),'colors: '+str(r['unique_rgb_visible']),fill='#293443',font=font)
        d.text((560,y+13),'brightness: '+str(round(float(r['mean_luma']),1)),fill='#293443',font=font)
        x0=800;scale=400/255;lum=float(r['mean_luma'])
        d.rectangle((x0,y+16,x0+400,y+31),fill='#d5dade')
        d.rectangle((x0,y+16,x0+lum*scale,y+31),fill='#536779')
    img.save(out)

def load_assets(input_dir,jar):
    if jar:
        with zipfile.ZipFile(jar) as z:
            for names in FAMILIES.values():
                for name in names:
                    path=SRC_ROOT+name+'.png'
                    try:yield name,z.read(path)
                    except KeyError:print('MISSING:',path)
    else:
        for names in FAMILIES.values():
            for name in names:
                p=input_dir/(name+'.png')
                if p.is_file():yield name,p.read_bytes()
                else:print('MISSING:',p)

def run():
    ap=argparse.ArgumentParser()
    inputs=ap.add_mutually_exclusive_group(required=True)
    inputs.add_argument('--assets-dir',type=Path)
    inputs.add_argument('--client-jar',type=Path)
    ap.add_argument('--version',default='1.21.11',help='Input assets must independently be verified to match this version')
    ap.add_argument('--output',type=Path,required=True)
    a=ap.parse_args();a.output.mkdir(parents=True,exist_ok=True)
    rows=[]; lum_arrays={}
    for name,data in load_assets(a.assets_dir,a.client_jar):
        try:
            row,l=pxstats(name,data,a.version); rows.append(row);lum_arrays[name]=l
        except Exception as exc: print('INVALID:',name,str(exc))
    order={name:i for i,name in enumerate(LABELS)};rows.sort(key=lambda r:order[r['texture_id']])
    write_csv(a.output/'05_픽셀통계.csv',rows,COLS)
    src_cols=['texture_id','family','edition','game_version','source_path','source_url','sha256','evidence_type','verification']
    write_csv(a.output/'04_원본_출처_목록.csv',rows,src_cols)
    summary=[]
    for family in FAMILIES:
        sub=[r for r in rows if r['family']==family]
        if not sub:continue
        summary.append({'family':family,'count':len(sub),'expected':len(FAMILIES[family]),'mean_unique_rgb':round(float(np.mean([r['unique_rgb_visible'] for r in sub])),2),'mean_luma':round(float(np.mean([r['mean_luma'] for r in sub])),2),'mean_luma_std':round(float(np.mean([r['luma_std'] for r in sub])),2),'mean_visible_pct':round(float(np.mean([r['visible_pct'] for r in sub])),2)})
    write_csv(a.output/'06_재질계열_집계.csv',summary,['family','count','expected','mean_unique_rgb','mean_luma','mean_luma_std','mean_visible_pct'])
    corr=[]
    names=['oak_planks','spruce_planks','birch_planks','dark_oak_planks','cherry_planks','mangrove_planks']
    for i,one in enumerate(names):
        for two in names[i+1:]:
            if one in lum_arrays and two in lum_arrays:
                p=float(np.corrcoef(lum_arrays[one].ravel(),lum_arrays[two].ravel())[0,1])
                corr.append({'texture_a':one,'texture_b':two,'luma_pearson_r':round(p,6),'interpretation':'same lightness pattern likely' if p>.97 else 'different lightness pattern'})
    write_csv(a.output/'09_목재무늬_상관분석.csv',corr,['texture_a','texture_b','luma_pearson_r','interpretation'])
    chart(rows,a.output/'08_색상_밝기_요약.png')
    (a.output/'00_summary.json').write_text(json.dumps({'source':'Minecraft Java 1.21.11 extracted asset mirror','source_url':'https://github.com/InventivetalentDev/minecraft-assets','count':len(rows),'groups':summary,'wood_correlations':corr},indent=2,ensure_ascii=False),encoding='utf-8')
    print('SUCCESS:',len(rows),'textures',len(summary),'families')

if __name__=='__main__':run()
