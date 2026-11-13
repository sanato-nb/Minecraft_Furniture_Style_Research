#!/usr/bin/env python3
"""TEX02-R009: inspect user-provided 1.21.11 .class and blockstates.
Local bytecode-structure check, not Minecraft execution or in-game UV verification.
No third-party packages. --root points to the extracted 1.21.11 directory.
"""
import argparse,csv,hashlib,json,struct
from pathlib import Path
CLASS_SHA={
"hqi.class":"5b64584e8cc09a8db90f802e0021bc0533e81ab1",
"hqc.class":"17d6188210d69bbebb560a043396bb8eeedd6045",
"hqc$b.class":"7cf58ffc0114cf9c90c275317697da0834e5d8a1",
"g.class":"f4883aaac8f997dceb60b8f5e9a076e7a16c6fef",
"ioc.class":"6063a49dabf4cda7816dc570babd1a1b2e57e6e0",
"i.class":"c8ce4192ed4ba9f567d9e2f0ccc15a61d1d9b29e",
"e.class":"f1e3848cc8d112cad31e01d6ac2eb536a1d0e328",
"ilp.class":"076a9076dd3aaaf92265a78f07e05addad0449bc",
"hqd.class":"ce8dfb96595fcd4a4a92120d3b3abf8548fc1303",
"hoa.class":"6841dfb26d63d166dac1d261c78805e00dfb2fc2",
"hoa$a.class":"776c249d3ed2490e1968894a1ea5fd0a2c681a02",
"hoa$b.class":"1eaad856846155a63bbd56c3ff895fc73150dde7",
}
BLOCKS="stone cobblestone stone_bricks deepslate_bricks polished_andesite bricks tuff_bricks granite polished_granite diorite polished_diorite andesite deepslate deepslate_tiles blackstone polished_blackstone chiseled_stone_bricks".split()
class ClassFile:
 def __init__(self,data):
  self.data=data;self.pos=0
  assert self.get(4)==0xCAFEBABE
  self.minor=self.get(2);self.major=self.get(2);count=self.get(2)
  self.cp=[None]*count;i=1
  while i<count:
   t=self.get(1)
   if t==1:v=self.read(self.get(2)).decode('utf8','replace')
   elif t in (3,4):v=self.get(4)
   elif t in (5,6):
    self.cp[i]=(t,self.read(8));i+=2;continue
   elif t in (7,8,16,19,20):v=self.get(2)
   elif t in (9,10,11,12,17,18):v=self.get(2),self.get(2)
   elif t==15:v=self.get(1),self.get(2)
   else:raise ValueError(f'constant pool tag {t}')
   self.cp[i]=(t,v);i+=1
  self.access=self.get(2);self.cls=self.get(2);self.parent=self.get(2)
  for _ in range(self.get(2)):self.get(2)
  for _ in range(self.get(2)):
   self.get(2);self.get(2);self.get(2)
   for __ in range(self.get(2)):
    self.get(2);self.read(self.get(4))
  self.methods={}
  for _ in range(self.get(2)):
   self.get(2);name=self.ref(self.get(2));desc=self.ref(self.get(2));code=b''
   for __ in range(self.get(2)):
    tag=self.ref(self.get(2));payload=self.read(self.get(4))
    if tag=="Code":
     n=int.from_bytes(payload[4:8],'big');code=payload[8:8+n]
   self.methods[name,desc]=code
 def read(self,n):
  a=self.data[self.pos:self.pos+n]
  assert len(a)==n
  self.pos+=n;return a
 def get(self,n):return int.from_bytes(self.read(n),'big')
 def ref(self,i):
  t,x=self.cp[i]
  if t==1:return x
  if t in (7,8,16,19,20):return self.ref(x)
  if t in (9,10,11):return self.ref(x[0])+'.'+self.ref(x[1])
  if t==12:return self.ref(x[0])+':'+self.ref(x[1])
  return str(x)
 def getmethod(self,name,desc):return self.methods[name,desc]
def pcref(cls,code,offset):
 assert code[offset] in (0xb2,0xb4,0xb6,0xb7,0xb8,0xb9)
 return cls.ref(int.from_bytes(code[offset+1:offset+3],'big'))
def verify(root,out):
 classes={}
 for name,sha in CLASS_SHA.items():
  binary=(root/name).read_bytes()
  got=hashlib.sha1(b'blob '+str(len(binary)).encode()+b'\x00'+binary).hexdigest()
  assert got==sha,(name,got)
  classes[name]=ClassFile(binary)
  assert classes[name].major==65
 bakery=classes['hqi.class'];quad=next(v for (name,desc),v in bakery.methods.items() if name=='a' and len(v)==184)
 vertex=next(v for (name,desc),v in bakery.methods.items() if name=='a' and len(v)==181)
 assert "hqc.d:" in pcref(bakery,quad,1)
 assert quad[8]==0xc7 and "hqi.a:" in pcref(bakery,quad,15)
 assert "ioc.b:" in pcref(bakery,quad,24)
 assert "ioc.a:" in pcref(bakery,quad,76)
 assert "hqi.a:" in pcref(bakery,quad,88)
 assert "hqd.a:" in pcref(bakery,vertex,32)
 assert "i.c:" in pcref(bakery,vertex,58)
 assert "hqc.a:" in pcref(bakery,vertex,67)
 assert "hqc.b:" in pcref(bakery,vertex,78)
 assert "e.a:" in pcref(bakery,vertex,82)
 assert "org/joml/Matrix4fc.transformPosition:" in pcref(bakery,vertex,119)
 assert "ilp.a:" in pcref(bakery,vertex,166)
 assert "ilp.b:" in pcref(bakery,vertex,173)
 assert "hdr.a:" in pcref(bakery,vertex,176)
 g=classes['g.class'].getmethod('b','(I)I')
 assert len(g)==9 and g[0]==0x1b and g[-4:]==bytes.fromhex('60 07 70 ac')
 h=classes['hqc$b.class']
 assert h.getmethod('a','(I)F')==bytes.fromhex('1b 99 00 08 1b 04 a0 00 0a 2a b4 00 18 a7 00 07 2a b4 00 1c ae')
 assert h.getmethod('b','(I)F')==bytes.fromhex('1b 99 00 08 1b 06 a0 00 0a 2a b4 00 1a a7 00 07 2a b4 00 1e ae')
 stateclasses=classes['ioc.class']
 assert stateclasses.getmethod('b','(Liz;)Lorg/joml/Matrix4fc;')[:1]==b'\xb2'
 assert stateclasses.getmethod('a','(Liz;)Lorg/joml/Matrix4fc;')[:1]==b'\xb2'
 blockRows=[]
 for id in BLOCKS:
  path=root/'assets/minecraft/blockstates'/f'{id}.json'
  j=json.loads(path.read_text(encoding='utf8'))
  for prop,variants in j['variants'].items():
   for index,item in enumerate(variants if isinstance(variants,list) else [variants]):
    blockRows.append({'block_id':id,'variant_index_in_block':index,'property':prop,
                      'explicit_uvlock_key_present': 'uvlock' in item})
 assert len(blockRows)==31 and not any(x['explicit_uvlock_key_present'] for x in blockRows)
 out.mkdir(parents=True,exist_ok=True)
 with (out/'BLOCKSTATE_UVLOCK_CHECK.csv').open('w',newline='',encoding='utf8') as f:
  w=csv.DictWriter(f,fieldnames=blockRows[0].keys());w.writeheader();w.writerows(blockRows)
 corners=[]
 for name,uv in [('auto_cube_full',(0,0,16,16)),('mirror_cube_explicit',(16,0,0,16))]:
  u1,v1,u2,v2=uv
  for rot in range(4):
   for original in range(4):
    index=(original+rot)%4
    u=u1 if index in (0,1) else u2
    v=v1 if index in (0,3) else v2
    corners.append(dict(rectangle=name,rotation_index=rot,input_corner=original,
                     selected_corner=index,u=u,v=v,normalized_u=u/16,normalized_v=v/16))
 assert len(corners)==32
 with (out/'UV_CORNER_ALGORITHM_REGEN.csv').open('w',newline='',encoding='utf8') as f:
  w=csv.DictWriter(f,fieldnames=corners[0].keys());w.writeheader();w.writerows(corners)
 print(json.dumps(dict(verified_source_classes=len(classes),
  blockstate_variants=len(blockRows),declared_uvlock_keys=0,
  quad_uv_algorithm_corner_evaluations=len(corners),in_game_verified=0),indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--root',required=True,type=Path);p.add_argument('--out',required=True,type=Path)
 a=p.parse_args();verify(a.root,a.out)
