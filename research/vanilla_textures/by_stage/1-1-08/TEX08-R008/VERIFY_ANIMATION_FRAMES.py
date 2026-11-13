#!/usr/bin/env python3
"""TEX08-R008 static-source PNG animation validation; requires Pillow.

python VERIFY_ANIMATION_FRAMES.py --textures /path/to/1.21.11/assets/minecraft/textures/block

Does not run Minecraft or claim observed runtime interpolation.
"""
from pathlib import Path
import argparse,hashlib,json,struct,zlib
from PIL import Image

ROOT=Path(__file__).resolve().parents[5] if len(Path(__file__).resolve().parents)>5 else Path.cwd()
DEFAULT=ROOT/"1.21.11/assets/minecraft/textures/block"
SOURCES={
"smoker_front_on":("9509bf23aecb04b857c1aecc3f71dbb79f182f0a8977bba1d9129b949a4bb0d5","bc6ecfc46a8e49e7a8df9e22482a145efe49396f",16,48),
"blast_furnace_front_on":("5363eaaf29c6cfed922c05fd4df9eaa7ef52b2d78ca56affda9ebf45ba33215d","53ee5793bc50295a771e10818a5601a71fc285b0",16,32),
"smoker_front":("ce2bec2d026b954529024c4ead234a39932335cf5367ac0a71c380b055150795","50dcaadecb8bd99810b4cfa646d1712b9d631911",16,16),
"blast_furnace_front":("df580828cf9079059e167dc13b51713d8029cdcf0f0b20374367c71a805d7f62","0246e9f925c7a9ce72f7732a4cdd29dffad7e560",16,16),
"furnace_front_on":("a4ff7cbdc6502673e9a2d61472a15673f608e70cbfc7b325a9473819906c73b9","1db2e1076134aac365d16517fafe36e361d0fed1",16,16),
"furnace_front":("aae808f71f1bddf4a25592f7dd3d7f6e9b3adaa739502170766424f4eb6bf9c5","db854a715a9ab076946d274b30c2fb70a561c2da",16,16)
}
META={
"smoker_front_on":("09eaec921357aabdd2fef6603815130df7e764b0",3,4,False,43,[21,34,36],[105,106,105],["0ff8","0480","0990","1dd8","3ff4","1ff0"]),
"blast_furnace_front_on":("4894b537c138a0cd21e4d64f93ce7ce5206d629a",2,10,True,6,[6,6],[12,12],["0540","0540","0000","0000","0000","0000"])
}
def gitsha(raw):
 return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
def png_crc(raw):
 assert raw.startswith(b"\x89PNG\r\n\x1a\n")
 pos=8
 while pos<len(raw):
  n=struct.unpack(">I",raw[pos:pos+4])[0]
  part=raw[pos+4:pos+8+n]
  assert zlib.crc32(part)&0xffffffff==struct.unpack(">I",raw[pos+8+n:pos+12+n])[0]
  pos+=12+n
 assert pos==len(raw)
def changes(a,b):
 return sum(a.getpixel((x,y))!=b.getpixel((x,y)) for y in range(16) for x in range(16))
def validate(path):
 images={}
 for name,(sha,git,w,h) in SOURCES.items():
  raw=(path/(name+".png")).read_bytes()
  png_crc(raw)
  assert hashlib.sha256(raw).hexdigest()==sha,(name,"sha256")
  assert gitsha(raw)==git,(name,"Git blob")
  im=Image.open(path/(name+".png")).convert("RGBA")
  assert im.size==(w,h) and all(p[3]==255 for p in im.getdata()),name
  images[name]=im
 for name,(meta_git,count,ticks,interpolate,dynamic,cycle,off_diffs,masks) in META.items():
  raw=(path/(name+".png.mcmeta")).read_bytes()
  assert gitsha(raw)==meta_git
  obj=json.loads(raw)["animation"]
  assert obj["frametime"]==ticks and obj["interpolate"] is interpolate
  assert "frames" not in obj
  fr=[images[name].crop((0,16*i,16,16*(i+1))) for i in range(count)]
  assert len(set(hashlib.sha256(im.tobytes()).hexdigest() for im in fr))==count
  assert [changes(fr[i],fr[(i+1)%count]) for i in range(count)]==cycle
  off=images[name.removesuffix("_on")]
  assert [changes(off,im) for im in fr]==off_diffs
  mask=[]
  for y in range(16):
   v=sum(1<<x for x in range(16) if len({im.getpixel((x,y)) for im in fr})>1)
   mask.append(f"{v:04x}")
  assert mask[8:14]==masks and all(v=="0000" for v in mask[:8]+mask[14:])
  assert sum(int(v,16).bit_count() for v in mask)==dynamic
 assert changes(images["furnace_front"],images["furnace_front_on"])==36
 assert not (path/"furnace_front_on.png.mcmeta").exists()
 print("PASS: 6 original PNG SHA+CRC, 2 animation mcmeta, 5 real frames, changing pixels 43/6, loops 21/34/36 and 6/6, furnace static 36.")
if __name__=="__main__":
 parser=argparse.ArgumentParser()
 parser.add_argument("--textures",type=Path,default=DEFAULT)
 validate(parser.parse_args().textures)
