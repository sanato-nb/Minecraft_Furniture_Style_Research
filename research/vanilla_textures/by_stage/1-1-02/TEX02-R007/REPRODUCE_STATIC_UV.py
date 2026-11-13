#!/usr/bin/env python3
"""Static source UV projection / seams, not Minecraft engine renderer. Requires Pillow."""
import argparse,csv,json,io,math,hashlib,zlib
from pathlib import Path
from PIL import Image
NAMES="stone cobblestone stone_bricks deepslate_bricks polished_andesite bricks tuff_bricks granite polished_granite diorite polished_diorite andesite deepslate deepslate_tiles blackstone polished_blackstone chiseled_stone_bricks".split()
BASE={"down":((0,-1,0),(1,0,0),(0,0,-1)),"up":((0,1,0),(1,0,0),(0,0,1)),"north":((0,0,-1),(-1,0,0),(0,-1,0)),"south":((0,0,1),(1,0,0),(0,-1,0)),"west":((-1,0,0),(0,0,1),(0,-1,0)),"east":((1,0,0),(0,0,-1),(0,-1,0))}
FACES={v[0]:k for k,v in BASE.items()}
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def rot(v,x,y):
 a=tuple(v)
 for _ in range(x%360//90):a=(a[0],-a[2],a[1])
 for _ in range(y%360//90):a=(-a[2],a[1],a[0])
 return a
def get(root,part,name):
 p=root/'assets/minecraft'/part/(name+'.json')
 return json.loads(p.read_text(encoding='utf-8'))
def model(root,name):
 p='block/'+name;seen=set();chain=[]
 while p:
  assert p not in seen;seen.add(p)
  j=get(root,'models',p);chain.append((p,j));p=j.get('parent','').replace('minecraft:','')
 textures={};els=None
 for _,j in reversed(chain):
  textures.update(j.get('textures',{}))
  if 'elements' in j:els=j['elements']
 assert len(els)==1 and els[0]['from']==[0,0,0] and els[0]['to']==[16,16,16]
 return els[0]['faces'],textures,'>'.join(k for k,_ in chain)
def texture(t,ts):
 while t.startswith('#'):t=ts[t[1:]]
 return t
def run(root,out):
 out.mkdir(parents=True,exist_ok=True);rows=[];north={}
 for tex in NAMES:
  for prop,val in get(root,'blockstates',tex)['variants'].items():
   for idx,entry in enumerate(val if isinstance(val,list) else [val]):
    mod=entry['model'].split('/')[-1];x=int(entry.get('x',0));y=int(entry.get('y',0))
    specs,texslots,chain=model(root,mod)
    for face,(n,u,v) in BASE.items():
     fs=specs[face];uv=fs.get('uv');assert uv is None or uv==[16,0,0,16]
     mirrored=uv is not None
     world=FACES[rot(n,x,y)];_,wu,wv=BASE[world]
     u2=rot(tuple(-i for i in u) if mirrored else u,x,y);v2=rot(v,x,y)
     U=(dot(u2,wu),dot(u2,wv));V=(dot(v2,wu),dot(v2,wv))
     corners=[]
     for a,b in [(-8,-8),(8,-8),(8,8),(-8,8)]:
      corners.extend([8+a*U[0]+b*U[1],8+a*V[0]+b*V[1]])
     assert set(corners)<={0,16}
     r={'texture_id':tex,'prop':prop,'index':idx,'model':mod,'x':x,'y':y,'local_face':face,'world_face_math':world,'source_texture_png':texture(fs['texture'],texslots).split('/')[-1]+'.png','source_uv':'explicit_U_reverse' if mirrored else 'implicit_auto_uv_assumed','screen_U_x':U[0],'screen_U_y':U[1],'screen_V_x':V[0],'screen_V_y':V[1],'det':U[0]*V[1]-U[1]*V[0],'top_left_u':corners[0],'top_left_v':corners[1],'top_right_u':corners[2],'top_right_v':corners[3],'bottom_right_u':corners[4],'bottom_right_v':corners[5],'bottom_left_u':corners[6],'bottom_left_v':corners[7],'model_parent_chain':chain,'not_ingame':True}
     rows.append(r)
     if world=='north':north[(tex,prop,idx)]=(r,U,V)
 assert len(rows)==186 and len(north)==31
 def csvwrite(file,items):
  with (out/file).open('w',newline='',encoding='utf8') as f:
   w=csv.DictWriter(f,fieldnames=list(items[0]));w.writeheader();w.writerows(items)
 csvwrite('FACE_UV_WORLD_CORNERS.csv',rows)
 pngs={}
 def load(name):
  if name not in pngs:
   raw=(root/'assets/minecraft/textures/block'/name).read_bytes()
   assert raw[:8]==bytes.fromhex('89504e470d0a1a0a')
   k=8
   while k<len(raw):
    n=int.from_bytes(raw[k:k+4],'big');t=raw[k+4:k+8];b=raw[k+8:k+8+n];c=int.from_bytes(raw[k+8+n:k+12+n],'big')
    assert zlib.crc32(t+b)&0xffffffff==c;k+=12+n
    if t==b'IEND':break
   assert k==len(raw)
   img=Image.open(io.BytesIO(raw)).convert('RGBA');assert img.size==(16,16)
   pngs[name]=img
  return pngs[name]
 def render(row,U,V):
  img=load(row['source_texture_png']);res=Image.new('RGBA',(16,16))
  for iy in range(16):
   for ix in range(16):
    a=ix-7.5;b=iy-7.5
    u=math.floor(8+a*U[0]+b*U[1]);v=math.floor(8+a*V[0]+b*V[1]);res.putpixel((ix,iy),img.getpixel((u,v)))
  return res
 edgerows=[]
 for tex,prop,n in [('stone','',4),('deepslate','axis=x',4),('deepslate','axis=y',4),('deepslate','axis=z',4),('bricks','',1),('stone_bricks','',1),('deepslate_bricks','',1)]:
  candidates=[(north[tex,prop,i][0],render(*north[tex,prop,i])) for i in range(n)]
  for left,A in candidates:
   for right,B in candidates:
    for direc in ['east_to_west','south_to_north']:
     pairs=[(A.getpixel((15,z)),B.getpixel((0,z))) if direc=='east_to_west' else (A.getpixel((z,15)),B.getpixel((z,0))) for z in range(16)]
     total=sum(abs(a[c]-b[c]) for a,b in pairs for c in range(3));mismatch=sum(any(a[c]!=b[c] for c in range(3)) for a,b in pairs)
     edgerows.append({'texture_group':tex,'property':prop,'left_variant_index':left['index'],'right_variant_index':right['index'],'left_source_png':left['source_texture_png'],'right_source_png':right['source_texture_png'],'world_face':'north','direction':direc,'rgb_diff_sum':total,'mean_abs_rgb':f'{total/48:.6f}','edge_pixels_mismatched':mismatch,'pixel_pairs':16,'rgb_channel_differences':48,'projection_is_mathematical_hypothesis':True,'not_ingame':True})
 assert len(edgerows)==134
 csvwrite('SOURCE_PROJECTED_NORTH_FACE_SEAMS.csv',edgerows)
 print('Projected',len(rows),'model faces and',len(edgerows),'hypothetical pixel seams; game render NOT verified.')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();run(a.root,a.out)
