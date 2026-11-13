#!/usr/bin/env python3
"""TEX02-R008. Verify 1.21.11 user-extracted FaceBakery default UV bytecode.
No Minecraft launch, rendering, Mojang official client.jar authentication, or external libraries.
"""
import argparse,struct,hashlib,json
from pathlib import Path

EXPECTED_SHA={
"hqi.class":"5b64584e8cc09a8db90f802e0021bc0533e81ab1",
"hqi$1.class":"237bb887fe196bc3d707a0f75ca5664c9baf8553",
"iz.class":"e820016d321253132b9f33de2da4b1b07f358e91"
}
EXPECTED={
"down":["from.x","(16-to.z)","to.x","(16-from.z)"],
"up":["from.x","from.z","to.x","to.z"],
"north":["(16-to.x)","(16-to.y)","(16-from.x)","(16-from.y)"],
"south":["from.x","(16-to.y)","to.x","(16-from.y)"],
"west":["from.z","(16-to.y)","to.z","(16-from.y)"],
"east":["(16-to.z)","(16-to.y)","(16-from.z)","(16-from.y)"]
}
DIRECTIONS=["down","up","north","south","west","east"]
class ClassFile:
 def __init__(self,data):
  self.data=data;self.pos=0
  assert self.get(4)==0xCAFEBABE
  self.minor=self.get(2);self.major=self.get(2)
  count=self.get(2);self.cp=[None]*count;i=1
  while i<count:
   tag=self.get(1)
   if tag==1:
    n=self.get(2);value=self.read(n).decode('utf-8','replace')
   elif tag==3:value=self.get(4)
   elif tag==4:value=struct.unpack('>f',self.read(4))[0]
   elif tag in (5,6):value=self.read(8);self.cp[i]=(tag,value);i+=2;continue
   elif tag in (7,8,16,19,20):value=self.get(2)
   elif tag in (9,10,11,12,17,18):value=(self.get(2),self.get(2))
   elif tag==15:value=(self.get(1),self.get(2))
   else:raise ValueError(f'constant_pool tag {tag}')
   self.cp[i]=(tag,value);i+=1
  self.flags=self.get(2);self.thisclass=self.get(2);self.superclass=self.get(2)
  n=self.get(2);self.read(2*n)
  self.fields=[]
  for _ in range(self.get(2)):
   flags=self.get(2);name=self.resolve(self.get(2));desc=self.resolve(self.get(2))
   self.skipattrs();self.fields.append((name,desc))
  self.methods={}
  for _ in range(self.get(2)):
   flags=self.get(2);name=self.resolve(self.get(2));desc=self.resolve(self.get(2))
   attrs={}
   for __ in range(self.get(2)):
    tag=self.resolve(self.get(2));size=self.get(4);payload=self.read(size)
    attrs[tag]=payload
   code=b''
   if 'Code' in attrs:
    content=attrs['Code']
    ncode=int.from_bytes(content[4:8],'big')
    code=content[8:8+ncode]
   self.methods[(name,desc)]=code
 def read(self,n):
  b=self.data[self.pos:self.pos+n]
  if len(b)!=n:raise ValueError('invalid classfile length')
  self.pos+=n;return b
 def get(self,n):return int.from_bytes(self.read(n),'big')
 def skipattrs(self):
  for _ in range(self.get(2)):self.get(2);self.read(self.get(4))
 def resolve(self,i):
  if not i:return None
  tag,x=self.cp[i]
  if tag==1:return x
  if tag in (7,8,16,19,20):return self.resolve(x)
  if tag in (9,10,11):return self.resolve(x[0])+'.'+self.resolve(x[1])
  if tag==12:return self.resolve(x[0])+':'+self.resolve(x[1])
  return x
def main(root):
 classes={}
 for name,sha in EXPECTED_SHA.items():
  data=(root/name).read_bytes()
  gitblob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\x00'+data).hexdigest()
  assert gitblob==sha,(name,gitblob)
  cls=ClassFile(data);assert cls.major==65
  classes[name]=cls
 cls=classes['hqi.class']
 desc='(Lorg/joml/Vector3fc;Lorg/joml/Vector3fc;Liz;)Lhqc$b;'
 code=cls.methods[('a',desc)]
 assert len(code)==302
 switch=code.index(b'\xaa')
 pad=(switch+4)&~3
 def i32(p):return struct.unpack_from('>i',code,p)[0]
 assert i32(pad+4)==1 and i32(pad+8)==6
 starts=[switch+i32(pad+12+4*i) for i in range(6)]
 assert starts==[58,98,132,178,218,258],starts
 result={}
 for j,start in enumerate(starts):
  st=[];i=start
  while True:
   op=code[i];i+=1
   if op==0xbb: i+=2;st.append("new")
   elif op==0x59:st.append(st[-1])
   elif op==0x2a:st.append("from")
   elif op==0x2b:st.append("to")
   elif op==0x12:
    v=cls.resolve(code[i]);i+=1;assert float(v)==16.
    st.append("16")
   elif op==0xb9:
    ref=(code[i]<<8)|code[i+1];i+=4
    method=cls.resolve(ref)
    v=st.pop()
    coordinate=method.split("Vector3fc.")[-1][0]
    assert coordinate in "xyz" and "Vector3fc." in method
    st.append(v+"."+coordinate)
   elif op==0x66:
    rhs=st.pop();lhs=st.pop();st.append("("+lhs+"-"+rhs+")")
   elif op==0xb7:
    i+=2;result[DIRECTIONS[j]]=st[-4:];break
   else:raise AssertionError(f'unexpected opcode 0x{op:x} at {i-1}')
 assert result==EXPECTED,(result,EXPECTED)
 # UV fallback: face.uv -> ifnonnull -> defaultFaceUV(from,to,Direction)
 bake=next(v for (n,d),v in cls.methods.items() if n=='a' and d.startswith('(Linw$a;'))
 assert len(bake)==184
 assert bake[0]==0x2d and cls.resolve(int.from_bytes(bake[2:4],'big')).startswith('hqc.d:')
 assert bake[8]==0xc7 and bake[15]==0xb8
 assert cls.resolve(int.from_bytes(bake[16:18],'big')).startswith('hqi.a:')
 # Synthetic case mapping, each of iz.a..iz.f is assigned switch case 1..6.
 switchcls=classes['hqi$1.class']
 init=next(v for (n,d),v in switchcls.methods.items() if n=='<clinit>')
 flds=[]
 for i in range(len(init)-8):
  if init[i]==0xb2 and init[i+3]==0xb2 and init[i+6]==0xb6 and init[i+9] in (0x04,0x05,0x06,0x07,0x08,0x10):
   fld=switchcls.resolve(int.from_bytes(init[i+4:i+6],'big'))
   if fld.startswith('iz.') and fld.endswith(':Liz;'):
    flds.append(fld)
 assert flds==['iz.'+ch+':Liz;' for ch in 'abcdef'],flds
 # Enum labels are also from the user's Java client iz.class.
 enumcls=classes['iz.class']
 names=[x[1] for x in enumcls.cp if x and x[0]==1]
 for name in ('DOWN','UP','NORTH','SOUTH','WEST','EAST'):assert name in names
 print(json.dumps({"source":"user 1.21.11 extracted client classfiles",
    "verified_classes":len(classes),"direction_count":len(result),
    "default_uv_cases":result,"full_cube_uv":[0,0,16,16],
    "default_uv_called_when_missing":True,"in_game_verified":False},
    indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser()
 p.add_argument('--root',type=Path,required=True,help='Path to user-extracted 1.21.11/ folder')
 a=p.parse_args();main(a.root)
