#!/usr/bin/env python3
"""Reproduce TEX01-R007 4 log side/end comparisons from user-extracted 1.21.11 assets.
Usage: python REPRODUCE_D1_SIDE_END.py /path/to/repository
Requires Python 3, numpy, Pillow. Source-only measurements, not game render.
"""
import base64, csv, hashlib, io, sys, zlib
from pathlib import Path
import numpy as np
from PIL import Image

root=Path(sys.argv[1] if len(sys.argv)>1 else '.')
species=('oak','spruce','birch','stripped_oak')
expected_sha={
'oak_log':'61735859c9c9ea82601191a77c6f256d93619cbaf7cad998a3ed5762877a34e6',
'oak_log_top':'a520800a833ea0c6214481245ab40397aa0c08b4ffc909046dac266386f9fc01',
'spruce_log':'a87a55ec454cb682934666bdf864dbd7fab4a561415f76834f3c53bb75bf0ba9',
'spruce_log_top':'8583ff5fc439af8bbc108bef5d71e947fb1655734dadd9470478d8d26ca3900b',
'birch_log':'81f2e40265758846858019a6b65b7617a205ac654dd2854b8b6cd31426e7c930',
'birch_log_top':'85f362f5c269af976a6b3dcea4130404b58687a7bbd963bc8c743a05817c8382',
'stripped_oak_log':'a0beb15ad3d8223308d5b36a3ee9c3b9c2b5ed9b4fadc7c5bdbc69823dfb1bc2',
'stripped_oak_log_top':'00aadf60b3de1d23bbcbb1659b4183b42b74350216c7b45c3c706ba34fd498a7'}
def load(name):
 raw=(root/'1.21.11/assets/minecraft/textures/block'/ (name+'.png')).read_bytes()
 assert raw[:8]==b'\x89PNG\r\n\x1a\n'
 assert hashlib.sha256(raw).hexdigest()==expected_sha[name],name
 pos=8;crc_count=0
 while pos<len(raw):
  length=int.from_bytes(raw[pos:pos+4],'big')
  assert (zlib.crc32(raw[pos+4:pos+8+length])&0xffffffff)==int.from_bytes(raw[pos+8+length:pos+12+length],'big')
  pos+=12+length;crc_count+=1
 assert pos==len(raw) and crc_count==4
 rgba=np.asarray(Image.open(io.BytesIO(raw)).convert('RGBA'))
 assert rgba.shape==(16,16,4) and bool((rgba[:,:,3]==255).all())
 return rgba[:,:,:3].astype(np.int16)

def Y(x):return .2126*x[:,:,0]+.7152*x[:,:,1]+.0722*x[:,:,2]
def S(x):
 a=x.astype(float);high=np.max(a,axis=2);low=np.min(a,axis=2)
 return np.divide(high-low,high,out=np.zeros_like(high),where=high>0)
def hv(x):
 a=x.astype(float)
 h=np.abs(a[:,1:]-a[:,:-1]).mean();v=np.abs(a[1:]-a[:-1]).mean()
 return h,v,v/h
out=[]
for n in species:
 a=load(n+'_log');b=load(n+'_log_top')
 ash,bsh=hv(a),hv(b)
 vals=[n,n+'_log',n+'_log_top',
  float(Y(a).mean()),float(Y(b).mean()),float(Y(b).mean()-Y(a).mean()),
  float(Y(a).std()),float(Y(b).std()),float(S(a).mean()),float(S(b).mean()),
  float(S(b).mean()-S(a).mean()),len(np.unique(a.reshape(-1,3),axis=0)),len(np.unique(b.reshape(-1,3),axis=0)),
  *ash,*bsh,float(np.abs(a-b).mean()),int(np.all(a==b,axis=2).sum()),
  int(np.any(b!=np.rot90(b,2),axis=2).sum())]
 out.append(vals)
 print(n,'side Y',round(vals[3],4),'end Y',round(vals[4],4),'delta',round(vals[5],4),'rot180 changed',vals[-1])
print('checked PNGs',2*len(species),'new supplemental PNGs',3,'new unique source texels',3*256)
