#!/usr/bin/env python3
"""TEX02-R010: original classfile + 17 JSON static UVLOCK control flow.
Path is the user-extracted 1.21.11/ folder. No external libraries and NO game runtime.
Does NOT authenticate original Mojang jar metadata or client.jar SHA-1.
"""
import argparse,hashlib,json,csv
from pathlib import Path
EXPECTED_BLOBS={
"hqq$a.class":"7b52f239fcd9c4b2579b142e3c8a5174539bf0e0",
"hqq.class":"56e792cadab0839fe87c0d28cd41f5313a998515",
"inm.class":"672b186c8a8457082fec756114b443a48dc151d1",
"inm$a.class":"9ca92245d30e41cf4dfe239617ebbec94ad19974",
"ioc.class":"6063a49dabf4cda7816dc570babd1a1b2e57e6e0",
"hqi.class":"5b64584e8cc09a8db90f802e0021bc0533e81ab1",
}
BLOCKS="stone cobblestone stone_bricks deepslate_bricks polished_andesite bricks tuff_bricks granite polished_granite diorite polished_diorite andesite deepslate deepslate_tiles blackstone polished_blackstone chiseled_stone_bricks".split()
class ClassFile:
 def __init__(self,raw):
  self.raw=raw;self.pos=0
  assert self.readint(4)==0xCAFEBABE
  self.minor=self.readint(2);self.major=self.readint(2);n=self.readint(2)
  self.cp=[None]*n;i=1
  while i<n:
   t=self.readint(1)
   if t==1:v=self.read(self.readint(2)).decode('utf8','replace')
   elif t in (3,4):v=self.readint(4)
   elif t in (5,6):
    self.cp[i]=(t,self.read(8));i+=2;continue
   elif t in (7,8,16,19,20):v=self.readint(2)
   elif t in (9,10,11,12,17,18):v=self.readint(2),self.readint(2)
   elif t==15:v=self.readint(1),self.readint(2)
   else:raise ValueError(f'unknown constant pool tag {t}')
   self.cp[i]=(t,v);i+=1
  self.flags=self.readint(2);self.selfclass=self.ref(self.readint(2))
  self.superclass=self.ref(self.readint(2))
  self.interfaces=[self.ref(self.readint(2)) for _ in range(self.readint(2))]
  self.fields=[]
  for _ in range(self.readint(2)):
   acc=self.readint(2);name=self.ref(self.readint(2));desc=self.ref(self.readint(2))
   self.fields.append((acc,name,desc))
   self.skip_attrs()
  self.methods={}
  for _ in range(self.readint(2)):
   acc=self.readint(2);name=self.ref(self.readint(2));desc=self.ref(self.readint(2))
   code=None
   for __ in range(self.readint(2)):
    kind=self.ref(self.readint(2));payload=self.read(self.readint(4))
    if kind=="Code":
     sz=int.from_bytes(payload[4:8],"big");code=payload[8:8+sz]
   self.methods[(name,desc)]=code
 def read(self,n):
  v=self.raw[self.pos:self.pos+n]
  assert len(v)==n;self.pos+=n;return v
 def readint(self,n):return int.from_bytes(self.read(n),"big")
 def ref(self,i):
  if i==0:return ""
  t,v=self.cp[i]
  if t==1:return v
  if t in (7,8,16,19,20):return self.ref(v)
  if t in (9,10,11):return self.ref(v[0])+"."+self.ref(v[1])
  if t==12:return self.ref(v[0])+":"+self.ref(v[1])
  return str(v)
 def skip_attrs(self):
  for _ in range(self.readint(2)):
   self.readint(2);self.read(self.readint(4))
 def method(self,name,desc):return self.methods[(name,desc)]
def git_blob_sha(raw):
 return hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\x00'+raw).hexdigest()
def verify(root,out):
 src={}
 for f,sha in EXPECTED_BLOBS.items():
  raw=(root/f).read_bytes()
  assert git_blob_sha(raw)==sha,(f,git_blob_sha(raw))
  c=ClassFile(raw);assert c.major==65;src[f]=c
 codec=src['hqq$a.class']
 source_terms=[x[1] for x in codec.cp if x and x[0]==1]
 for t in ('uvlock','x','y','z'):assert t in source_terms
 code=codec.method('a','(Lcom/mojang/serialization/codecs/RecordCodecBuilder$Instance;)Lcom/mojang/datafixers/kinds/App;')
 # Codec.BOOL; "uvlock"; iconst_0; invokestatic optionalFieldOf
 assert bytes.fromhex('b2 00 9c 12 9e 03 b8 00 a4') in code
 assert codec.ref(156).startswith('com/mojang/serialization/Codec.BOOL')
 assert codec.ref(158)=='uvlock'
 assert 'optionalFieldOf' in codec.ref(164) or 'optionalFieldOf' in codec.ref(167)
 mk=codec.method('a','()Lioc;')
 assert mk==bytes.fromhex('2a b4 00 28 2a b4 00 2a 2a b4 00 2c b8 00 39 b8 00 3e 4c 2a b4 00 2e 99 00 0a 2b b6 00 40 a7 00 04 2b b0')
 assert codec.ref(62).startswith('inm.a:')
 assert codec.ref(64).startswith('inm.b:')
 assert src['inm.class'].interfaces==['ioc']
 assert ('b','(Liz;)Lorg/joml/Matrix4fc;') not in src['inm.class'].methods
 assert src['inm.class'].method('b','()Lioc;')==bytes.fromhex('2a b4 00 31 b0')
 assert src['inm$a.class'].interfaces==['ioc']
 wrap=src['inm$a.class'].method('b','(Liz;)Lorg/joml/Matrix4fc;')
 assert bytes.fromhex('b4 00 34') in wrap  # inverse face map in parent
 ioc=src['ioc.class']
 normal=ioc.method('b','(Liz;)Lorg/joml/Matrix4fc;')
 assert normal==bytes.fromhex('b2 00 12 b0')
 assert bytes.fromhex('bb 00 18 59 b7 00 1b b3 00 12') in ioc.method('<clinit>','()V')
 variant=src['hqq.class'].method('a','(Linw;)Lhqg;')
 assert variant==bytes.fromhex('2b 2a b4 00 37 2a b4 00 39 b6 00 58 b8 00 5d b0')
 quad=next(v for (n,d),v in src['hqi.class'].methods.items() if n=='a' and d.startswith('(Linw$a;'))
 assert bytes.fromhex('19 06 19 05 b9 00 4f 02 00') in quad
 rows=[]
 for block in BLOCKS:
  j=json.loads((root/'assets/minecraft/blockstates'/f'{block}.json').read_text(encoding='utf8'))
  for prop,vals in j['variants'].items():
   for idx,e in enumerate(vals if isinstance(vals,list) else [vals]):
    assert 'uvlock' not in e
    rows.append(dict(block=block,property=prop,variant_index=idx,model=e['model'],
       x=e.get('x',0),y=e.get('y',0),z=e.get('z',0),uvlock_key_present=False,
       effective_uvlock=False,modelstate='inm',uv_matrix='ioc.b identity',
       note='bytecode inferred, not game executed'))
 assert len(rows)==31
 from collections import Counter
 rotations=Counter((r['x'],r['y'],r['z']) for r in rows)
 assert rotations=={(0,0,0):19,(0,180,0):4,(90,90,0):4,(90,0,0):2,(90,180,0):2}
 out.mkdir(parents=True,exist_ok=True)
 with (out/'REGENERATED_EFFECTIVE_UVLOCK.csv').open('w',newline='',encoding='utf8') as f:
  w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
 print(json.dumps({'classfiles_sha_verified':len(src),
   'blockstate_jsons':len(BLOCKS),'variant_declarations':len(rows),
   'inferred_normal_modelstate_identity_uv_path':31,
   'game_render_verified':0},indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser()
 p.add_argument('--root',required=True,type=Path,help='User-extracted 1.21.11 directory')
 p.add_argument('--out',required=True,type=Path)
 a=p.parse_args();verify(a.root,a.out)
