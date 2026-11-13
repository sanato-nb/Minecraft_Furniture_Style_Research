#!/usr/bin/env python3
"""TEX02-R016: source-only registry/concrete-class/getSeed inheritance verifier.

Example (run where user-extracted Minecraft 1.21.11 files exist):
 python VERIFY_R016_BLOCK_SEED_INHERITANCE.py \
    --root ./1.21.11 \
    --r013-slots ./TEX02-R013/BLOCKSTATE_CHOICE_SLOTS_31.csv \
    --out ./r016_regenerated

Standard Python 3.9+; no external packages. Verifies original Git blob SHA,
.class constant pools, registered block literal positions and factory bytes,
LambdaMetafactory constructor references, seed method signatures, all 31
original model slots, and writes one 17-row source verification CSV.
Not an actual Minecraft runtime/model atlas/GPU rendering validation.
"""
import argparse
import csv
import hashlib
import struct
from collections import Counter
from pathlib import Path

SOURCES = {
 "dzs.class":"b58e7153fb0cfbb47313c3a59dd7c8516ee3642c",
 "dzq.class":"fab6c386693f88d28cc680ba8112bf0a2243ee16",
 "egl.class":"61424d1fe2efc6162c61c64e74a57f01c519d8f4",
 "eog.class":"bee52d0356520a1872a94b0a15b0c98ea5407154",
 "eog$a.class":"35c882743a59ae8d99fee1da9dfe0f21e8c6aa7c",
 "bgj.class":"89604a1a7dfc4e63be8bc0eb170352b59c7f5374"
}
SLOTS_SHA = "18f02c6f44fd18f2a522fca81b2f73ba7409f829"
SEED_METHOD = ("a", "(Leoh;Lis;)J")

def git_blob_sha(data):
 return hashlib.sha1(b"blob "+str(len(data)).encode("ascii")+b"\0"+data).hexdigest()

class JavaClass:
 def __init__(self,data):
  self.data=data
  self.p=0
  assert self.u4()==0xCAFEBABE
  self.minor=self.u2()
  self.major=self.u2()
  n=self.u2()
  cp=[None]*n
  i=1
  while i<n:
   t=self.u1()
   if t==1:
    length=self.u2()
    v=self.take(length).decode("utf-8","replace")
   elif t in (3,4):
    v=self.u4()
   elif t in (5,6):
    v=self.take(8)
    cp[i]=(t,v)
    i+=2
    continue
   elif t in (7,8,16,19,20):
    v=self.u2()
   elif t in (9,10,11,12,17,18):
    v=(self.u2(),self.u2())
   elif t==15:
    v=(self.u1(),self.u2())
   else:
    raise ValueError(("unsupported classfile CP tag",t,i))
   cp[i]=(t,v)
   i+=1
  self.cp=cp
  self.access=self.u2()
  self.name=self.ref(self.u2())
  self.superclass=self.ref(self.u2())
  for _ in range(self.u2()):
   self.u2()
  for _ in range(self.u2()):
   self.u2();self.u2();self.u2()
   for __ in range(self.u2()):
    self.u2();length=self.u4();self.take(length)
  self.methods=[]
  for _ in range(self.u2()):
   flags=self.u2()
   name=self.ref(self.u2())
   desc=self.ref(self.u2())
   code=b""
   for __ in range(self.u2()):
    attr=self.ref(self.u2())
    size=self.u4()
    payload=self.take(size)
    if attr=="Code":
     assert len(payload)>=8
     clen=struct.unpack(">I",payload[4:8])[0]
     code=payload[8:8+clen]
     assert len(code)==clen
   self.methods.append(dict(name=name,desc=desc,flags=flags,code=code))
  self.bootstrap=[]
  for _ in range(self.u2()):
   key=self.ref(self.u2())
   size=self.u4()
   payload=self.take(size)
   if key!="BootstrapMethods":
    continue
   at=0
   num=struct.unpack_from(">H",payload,at)[0]
   at+=2
   for __ in range(num):
    handle,numargs=struct.unpack_from(">HH",payload,at)
    at+=4
    args=list(struct.unpack_from(">"+("H"*numargs),payload,at)) if numargs else []
    at+=2*numargs
    self.bootstrap.append((handle,args))
   assert at==len(payload)
  assert self.p==len(self.data)
 def take(self,n):
  value=self.data[self.p:self.p+n]
  assert len(value)==n, ("truncated class",self.name if hasattr(self,"name") else "")
  self.p+=n
  return value
 def u1(self):return self.take(1)[0]
 def u2(self):return struct.unpack(">H",self.take(2))[0]
 def u4(self):return struct.unpack(">I",self.take(4))[0]
 def ref(self,i):
  ent=self.cp[i]
  assert ent is not None,(self.name if hasattr(self,"name") else "",i)
  tag,v=ent
  if tag==1:return v
  if tag in (7,8,16,19,20):return self.ref(v)
  if tag in (9,10,11):return self.ref(v[0])+"."+self.ref(v[1])
  if tag==12:return self.ref(v[0])+":"+self.ref(v[1])
  if tag==15:return "kind"+str(v[0])+":"+self.ref(v[1])
  if tag==18:return "bsm"+str(v[0])+":"+self.ref(v[1])
  return str(v)
 def method(self,name,desc):
  ms=[m for m in self.methods if m["name"]==name and m["desc"]==desc]
  assert len(ms)==1,(self.name,name,desc,len(ms))
  return ms[0]
 def has(self,name,desc):
  return any(m["name"]==name and m["desc"]==desc for m in self.methods)
 def string_cp(self,name):
  utf8=[i for i,c in enumerate(self.cp) if c and c==(1,name)]
  assert len(utf8)==1,(self.name,name,utf8)
  ids=[i for i,c in enumerate(self.cp) if c and c==(8,utf8[0])]
  assert len(ids)==1,(self.name,"ldc",name,ids)
  return ids[0]
 def lambda_constructor(self,indy_cp):
  tag,(bsm_index,nt_index)=self.cp[indy_cp]
  assert tag==18
  bm=self.bootstrap[bsm_index]
  return [self.ref(i) for i in bm[1] if self.ref(i).startswith("kind8:")]

def main(root,slot_file,out):
 cs={}
 for name,sha in SOURCES.items():
  data=(root/name).read_bytes()
  assert git_blob_sha(data)==sha,("original source changed",name)
  cs[name]=JavaClass(data)
 assert (cs["dzq.class"].name,cs["dzq.class"].superclass)==("dzq","eog")
 assert (cs["egl.class"].name,cs["egl.class"].superclass)==("egl","dzq")
 assert (cs["eog.class"].name,cs["eog.class"].superclass)==("eog","java/lang/Object")
 for sub in ("dzq.class","egl.class"):
  assert not cs[sub].has(*SEED_METHOD),("seed override found",sub)
 eog=cs["eog.class"]
 assert eog.method(*SEED_METHOD)["code"]==bytes.fromhex("2c b8 02 07 ad")
 assert cs["eog$a.class"].method("b","(Lis;)J")["code"]==bytes.fromhex(
   "2a b6 00 ff 2a b6 00 73 2b b6 02 74 ad")
 reg=cs["dzs.class"]
 assert reg.lambda_constructor(0x05C4)==["kind8:dzq.<init>:(Leog$d;)V"]
 assert reg.lambda_constructor(0x09FF)==["kind8:egl.<init>:(Leog$d;)V"]
 assert reg.method("a","(Ljava/lang/String;Leog$d;)Ldzq;")["code"]==bytes.fromhex(
   "2a ba 05 c4 00 00 2b b8 05 19 b0")
 assert reg.method("a","(Ljava/lang/String;Ljava/util/function/Function;Leog$d;)Ldzq;")["code"]==bytes.fromhex(
   "2a b8 05 d8 2b 2c b8 05 c6 b0")
 raw=slot_file.read_bytes()
 assert git_blob_sha(raw)==SLOTS_SHA
 with slot_file.open(newline="",encoding="utf-8") as src:
  slots=list(csv.DictReader(src))
 assert len(slots)==31
 counts=Counter(r["block"] for r in slots)
 assert len(counts)==17
 clinit=reg.method("<clinit>","()V")["code"]
 assert len(clinit)==40257
 rows=[]
 for name in counts:
  idx=reg.string_cp(name)
  pattern=bytes([0x13,idx>>8,idx&255])
  assert clinit.count(pattern)==1,("not unique",name)
  pc=clinit.index(pattern)
  special=name=="deepslate"
  if special:
   assert clinit[pc+3:pc+8]==bytes.fromhex("ba 09 ff 00 00")
  helper=0x0519 if special else 0x0991
  helper_pattern=bytes([0xB8,helper>>8,helper&255,0xB3])
  off=clinit.find(helper_pattern,pc+3,pc+100)
  assert off>=0,(name,"helper")
  field_idx=int.from_bytes(clinit[off+4:off+6],"big")
  field=reg.ref(field_idx)
  assert field.startswith("dzs.") and field.endswith(":Ldzq;")
  rows.append(dict(
   block_id=name,registry_pc=pc,registry_literal_cp=idx,
   block_class="egl" if special else "dzq",
   superclass_chain="egl->dzq->eog" if special else "dzq->eog",
   putstatic_field=field,
   source_model_slots=counts[name],
   original_class_method_seed_override_found=False,
   vanilla_default_position_seed_inherited=True,
   actual_game_renderer_observed=False
  ))
 assert len(rows)==17
 assert sum(r["block_class"]=="egl" for r in rows)==1
 assert sum(r["block_class"]=="dzq" for r in rows)==16
 assert sum(r["source_model_slots"] for r in rows)==31
 out.mkdir(parents=True,exist_ok=True)
 with (out/"R016_REGENERATED_REGISTRY_17.csv").open("w",newline="",encoding="utf-8") as sink:
  writer=csv.DictWriter(sink,list(rows[0]))
  writer.writeheader()
  writer.writerows(rows)
 print("VERIFIED: 6 original classes; 17/17 inherited render seed; "
       "31/31 model choice declarations; 0/17 in-game renders")
if __name__=="__main__":
 parser=argparse.ArgumentParser()
 parser.add_argument("--root",type=Path,required=True)
 parser.add_argument("--r013-slots",type=Path,required=True)
 parser.add_argument("--out",type=Path,required=True)
 args=parser.parse_args()
 main(args.root,args.r013_slots,args.out)
