from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import csv,json
R=Path(__file__).resolve().parents[1];B=R/'research/vanilla_models/phase_1-2-F/entry1'
rows=list(csv.DictReader((B/'F_TEXTURE_C_SLOT_PNG_LINKS.csv').open())); paths=sorted({x['PNG_path'] for x in rows if x['PNG_path']})
for q in csv.DictReader((B/'F_ENTRY1_QUEUE_150.csv').open()):
 if q['E_exception_owned']=='YES':
  d=json.loads((R/q['source_path']).read_text());ref=d.get('textures',{}).get('particle')
  if ref: paths.append('1.21.11/assets/minecraft/textures/'+ref.split(':')[-1]+'.png')
paths=sorted(set(paths));print('all',len(paths));out=B/'visual_contact';out.mkdir(exist_ok=True)
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',13)
for page in range(0,len(paths),48):
 im=Image.new('RGB',(8*165,6*170),'#ddd');draw=ImageDraw.Draw(im)
 for slot,p in enumerate(paths[page:page+48]):
  idx=page+slot; x=slot%8*165;y=slot//8*170
  try:
   img=Image.open(R/p);img.load();w,h=img.size
   # animated strip: show first square frame only and the raw size in label
   frame=img.crop((0,0,w,min(h,w))).convert('RGBA');frame.thumbnail((120,120),Image.Resampling.NEAREST)
   frame=frame.resize((min(120,frame.width*max(1,120//max(1,frame.width))),min(120,frame.height*max(1,120//max(1,frame.height)))),Image.Resampling.NEAREST)
   for cy in range(y+4,y+132,10):
    for cx in range(x+4,x+156,10):
     if ((cx-x)//10+(cy-y)//10)%2:draw.rectangle((cx,cy,cx+9,cy+9),fill='#bbb')
   im.paste(frame,(x+(165-frame.width)//2,y+4),frame)
   name=Path(p).stem;draw.text((x+3,y+135),f'{idx:03d} {name[:19]}',font=font,fill='black');draw.text((x+3,y+151),f'{w}x{h}',font=font,fill='black')
  except Exception as e:print('ERR',p,e)
 im.save(out/f'contact_{page//48+1:02d}.png')
(out/'index.json').write_text(json.dumps(paths,indent=2))
