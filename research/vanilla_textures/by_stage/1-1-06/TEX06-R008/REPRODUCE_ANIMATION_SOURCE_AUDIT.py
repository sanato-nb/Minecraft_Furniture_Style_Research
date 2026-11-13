#!/usr/bin/env python3
"""Reproduce TEX06-R008 source animation audit (Python standard library only).
Run from repository root containing 1.21.11/assets/minecraft.
Does NOT launch Minecraft or certify the official compressed client.jar.
"""
from pathlib import Path
import json
import struct
import zlib
ROOT=Path("1.21.11/assets/minecraft/textures/block")
TARGET_IDS=("terracotta","white_terracotta","orange_terracotta","blue_terracotta",
 "green_terracotta","yellow_terracotta","black_glazed_terracotta","white_glazed_terracotta")
CONTROLS={
 "water_still":(32,32,2,False),
 "lava_still":(20,38,2,False),
 "fire_0":(32,32,1,False),
 "sea_lantern":(5,5,5,False),
 "prismarine":(4,22,300,True)
}
def read_png(path):
 data=path.read_bytes()
 assert data[:8]==b"\x89PNG\r\n\x1a\n",path
 width,height=struct.unpack_from(">II",data,16)
 p=8;chunks=[]
 while p<len(data):
  length=struct.unpack_from(">I",data,p)[0]
  name=data[p+4:p+8]
  end=p+12+length
  assert end<=len(data),(path,"truncated PNG")
  assert (zlib.crc32(data[p+4:p+8+length])&0xffffffff)==struct.unpack_from(">I",data,p+8+length)[0],(path,name,"CRC failure")
  chunks.append(name.decode("ascii"))
  p=end
 assert p==len(data) and chunks[-1]=="IEND" and chunks[0]=="IHDR"
 return (width,height,chunks)
def get_control(name,expected):
 png=ROOT/(name+".png")
 meta=ROOT/(name+".png.mcmeta")
 w,h,chunks=read_png(png)
 assert h%w==0 and "acTL" not in chunks
 anim=json.loads(meta.read_text("utf-8"))["animation"]
 slots=h//w
 sequence=anim.get("frames",list(range(slots)))
 assert all(isinstance(s,int) or (isinstance(s,dict) and "index" in s) for s in sequence)
 indices=[s if isinstance(s,int) else s["index"] for s in sequence]
 assert all(0<=n<slots for n in indices)
 actual=(slots,len(sequence),anim.get("frametime",1),bool(anim.get("interpolate",False)))
 assert actual==expected,(name,actual,expected)
 return {"name":name,"dimensions":[w,h],"frame_slots":slots,
  "sequence_length":len(sequence),"frame_ticks":actual[2],"interpolate":actual[3]}
def main():
 target=[]
 for name in TARGET_IDS:
  w,h,chunks=read_png(ROOT/(name+".png"))
  assert (w,h)==(16,16),(name,w,h)
  assert "acTL" not in chunks,(name,chunks)
  assert not (ROOT/(name+".png.mcmeta")).exists(),name
  target.append(name)
 controls=[get_control(name,expected) for name,expected in CONTROLS.items()]
 assert len(target)==8 and len(controls)==5
 print(json.dumps({"static_target_textures":target,"animation_controls":controls},
   indent=2,ensure_ascii=False))
if __name__=="__main__":main()
