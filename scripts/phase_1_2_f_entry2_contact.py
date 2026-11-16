"""Reproducible first-frame contact sheets for F Entry2 source PNGs."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import csv,json
R=Path(__file__).resolve().parents[1];B=R/'research/vanilla_models/phase_1-2-F/entry2';OUT=B/'visual_contact';OUT.mkdir(exist_ok=True)
with (B/'F_TEXTURE_VISUAL_EVIDENCE.csv').open(newline='') as f:paths=[x['png_path'] for x in csv.DictReader(f)]
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',13)
for start in range(0,len(paths),48):
 canvas=Image.new('RGB',(1320,1020),'#ddd');draw=ImageDraw.Draw(canvas)
 for slot,p in enumerate(paths[start:start+48]):
  index=start+slot;x=slot%8*165;y=slot//8*170;im=Image.open(R/p);im.load();w,h=im.size
  for cy in range(y+4,y+132,10):
   for cx in range(x+4,x+156,10):
    if ((cx-x)//10+(cy-y)//10)%2:draw.rectangle((cx,cy,cx+9,cy+9),fill='#bbb')
  frame=im.convert('RGBA').crop((0,0,w,min(w,h)));frame.thumbnail((120,120),Image.Resampling.NEAREST)
  scale=max(1,min(120//max(1,frame.width),120//max(1,frame.height)));frame=frame.resize((frame.width*scale,frame.height*scale),Image.Resampling.NEAREST)
  canvas.paste(frame,(x+(165-frame.width)//2,y+4),frame)
  draw.text((x+3,y+135),f'{index:03d} {Path(p).stem[:19]}',font=font,fill='black')
  draw.text((x+3,y+151),f'{w}x{h}',font=font,fill='black')
 canvas.save(OUT/f'contact_{start//48+1:02d}.png')
(OUT/'index.json').write_text(json.dumps(paths,ensure_ascii=False,indent=2)+'\n')
print(len(paths),(len(paths)+47)//48)
