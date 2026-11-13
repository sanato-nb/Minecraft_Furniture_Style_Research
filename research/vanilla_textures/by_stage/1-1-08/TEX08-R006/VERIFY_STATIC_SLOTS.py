#!/usr/bin/env python3
"""Recheck TEX08-R006 from the user-extracted 1.21.11/ files. Requires Pillow."""
import hashlib,json,struct,zlib
from pathlib import Path
from PIL import Image
base=Path(__file__).resolve().parents[5]/"1.21.11/assets/minecraft"
names=["top_left","top_mid","top_right","bottom_left","bottom_mid","bottom_right"]
shas={"chiseled_bookshelf_empty":"a756e5f993f698a566b73b24c0610b9832781d4a5f20358f38442b77d028841d","chiseled_bookshelf_occupied":"a314c81a2dd8c3f14bec2428a0252322e6b37e95810d56316ac23c938540fb4e"}
imgs=[]
for name,expected in shas.items():
 p=base/"textures/block"/(name+".png");d=p.read_bytes()
 assert hashlib.sha256(d).hexdigest()==expected
 assert d[:8]==b"\x89PNG\r\n\x1a\n"
 off=8
 while off<len(d):
  length=struct.unpack(">I",d[off:off+4])[0]
  blob=d[off+4:off+8+length]
  assert zlib.crc32(blob)&0xffffffff==struct.unpack(">I",d[off+8+length:off+12+length])[0]
  off+=12+length
 assert off==len(d)
 im=Image.open(p).convert("RGBA");assert im.size==(16,16)
 assert all(im.getpixel((x,y))[3]==255 for y in range(16) for x in range(16))
 imgs.append(im)
a,b=imgs
areas=[];diffs=[];covered=set()
for s in names:
 m=json.loads((base/"models/block"/("template_chiseled_bookshelf_slot_"+s+".json")).read_text())
 e=m["elements"][0];assert e["from"][2]==e["to"][2]==0
 assert list(e["faces"])==["north"] and m["textures"]["particle"]=="#texture"
 x0,y0,x1,y1=e["faces"]["north"]["uv"]
 r={(x,y)for y in range(y0,y1)for x in range(x0,x1)}
 assert not r&covered;covered|=r
 areas.append((x0,y0,x1,y1))
 diffs.append(sum(a.getpixel(p)!=b.getpixel(p) for p in r))
assert len(covered)==256 and diffs==[25,29,24,29,25,24]
assert sum(diffs)==156
signatures=set()
for mask in range(64):
 result=Image.new("RGBA",(16,16))
 for i,(x0,y0,x1,y1) in enumerate(areas):
  src=b if mask&(1<<i) else a
  result.paste(src.crop((x0,y0,x1,y1)),(x0,y0))
 signatures.add(hashlib.sha256(result.tobytes()).hexdigest())
assert len(signatures)==64
data=json.loads((base/"blockstates/chiseled_bookshelf.json").read_text())
assert len(data["multipart"])==52
def m(when,props):
 if "AND" in when:return all(m(x,props)for x in when["AND"])
 if "OR" in when:return any(m(x,props)for x in when["OR"])
 return all(str(props[k]) in str(v).split("|") for k,v in when.items())
count=0
for facing,rot in [("north",0),("east",90),("south",180),("west",270)]:
 for mask in range(64):
  p={"facing":facing,**{"slot_"+str(i)+"_occupied":str(bool(mask&(1<<i))).lower() for i in range(6)}}
  chosen=[rule["apply"] for rule in data["multipart"] if m(rule["when"],p)]
  assert len(chosen)==7 and all(rule.get("y",0)==rot for rule in chosen)
  assert sum(rule["model"]=="minecraft:block/chiseled_bookshelf" for rule in chosen)==1
  for i,s in enumerate(names):
   expected="minecraft:block/chiseled_bookshelf_"+("occupied" if mask&(1<<i) else "empty")+"_slot_"+s
   assert sum(rule["model"]==expected for rule in chosen)==1
  count+=1
assert count==256
print("PASS: two static PNGs CRC+SHA, 156 RGBA diffs, 6 UV slots, 64 distinct atlas hashes, 256 model selections")
