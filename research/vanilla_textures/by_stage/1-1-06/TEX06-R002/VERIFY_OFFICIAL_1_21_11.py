#!/usr/bin/env python3
"""TEX06 user-side verification. Python 3.9+, stdlib only. Never uploads game files.
Usage: python VERIFY_OFFICIAL_1_21_11.py path/to/1.21.11.jar
Requires network access to Mojang manifest.
"""
import sys,json,hashlib,zipfile,urllib.request,pathlib
VERSION='1.21.11'
MANIFEST='https://piston-meta.mojang.com/mc/game/version_manifest_v2.json'
SHA256={
 'terracotta':'b2458267eac6b6f35d02990ee3244edf1f43fbe258bd6dfe15189cf2eaf42ae8',
 'white_terracotta':'9feeb13f19514ea58a5b6e942df7a8595330e61173f8d0a13c83b78acd1bd62e',
 'orange_terracotta':'3074d90b0a27d1c149df2f3eacc9c6895c4cc0548999f864146dc18f64bcab5a',
 'blue_terracotta':'99b4ec0a8a02a9d609d4987cbb7ba594a59f93c76b5fd98e3a1f12c2df1f9a70',
 'green_terracotta':'ffe10089bcef9873c74f18be35e605c5d035f472c06bf677746d39ff8a656c07',
 'yellow_terracotta':'7c00bf901f78ad628a06335d47310a6b18c1419243d4150e32cdf01d51bafca6',
 'black_glazed_terracotta':'214ce8ca46c60a42b8863655b3895aca839c7ef7cfa511a192dc1974a0ca2758',
 'white_glazed_terracotta':'cb1ebf9f3f3e93009ff4cab1b2b2b70d41fd87caa40c71942ae51996d12498b4'
}
def fetch_json_bytes(url):
 if not url.startswith('https://piston-meta.mojang.com/'):
  raise ValueError('Expected Mojang metadata HTTPS URL')
 with urllib.request.urlopen(url,timeout=30) as r:
  b=r.read(4*1024*1024+1)
 if len(b)>4*1024*1024:raise ValueError('Metadata size exceeded limit')
 return b,json.loads(b)
def hash_file(p):
 h=hashlib.sha1();n=0
 with open(p,'rb') as f:
  for block in iter(lambda:f.read(1024*1024),b''):
   h.update(block);n+=len(block)
 return h.hexdigest(),n
def main():
 if len(sys.argv)!=2:
  print('Usage: python VERIFY_OFFICIAL_1_21_11.py path/to/1.21.11.jar');return 2
 result={'version':VERSION,'official_jar_authenticated':False,'official_png_match_count':0,'official_model_blockstate_match_count':0,'ingame_static_verified':False,'source':'user_side_local_jar'}
 try:
  p=pathlib.Path(sys.argv[1]);manifest=fetch_json_bytes(MANIFEST)[1]
  rec=next(x for x in manifest['versions'] if x['id']==VERSION)
  data,meta=fetch_json_bytes(rec['url'])
  if hashlib.sha1(data).hexdigest()!=rec['sha1'] or meta['id']!=VERSION:raise ValueError('Version metadata SHA1 failed')
  official=meta['downloads']['client']
  sha1,n=hash_file(p)
  result.update({'manifest_sha1':rec['sha1'],'expected_jar_sha1':official['sha1'],'actual_jar_sha1':sha1,'jar_size':n})
  if sha1!=official['sha1'] or n!=official['size']:raise ValueError('client.jar SHA1 or size mismatch')
  result['official_jar_authenticated']=True
  with zipfile.ZipFile(p) as z:
   for name,expected in SHA256.items():
    b=z.read('assets/minecraft/textures/block/'+name+'.png')
    good=hashlib.sha256(b).hexdigest()==expected
    result['official_png_match_count']+=int(good)
    glazed='glazed' in name;slot='pattern' if glazed else 'all'
    model=json.loads(z.read('assets/minecraft/models/block/'+name+'.json'))
    states=json.loads(z.read('assets/minecraft/blockstates/'+name+'.json'))['variants']
    parent='minecraft:block/template_glazed_terracotta' if glazed else 'minecraft:block/cube_all'
    valid=model.get('parent')==parent and model.get('textures',{}).get(slot)=='minecraft:block/'+name
    if glazed:
     turns={'facing=east':270,'facing=north':180,'facing=south':0,'facing=west':90}
     valid=valid and set(states)==set(turns) and all(states[k].get('model')=='minecraft:block/'+name and states[k].get('y',0)==v for k,v in turns.items())
    else:valid=valid and set(states)=={''} and states[''].get('model')=='minecraft:block/'+name
    result['official_model_blockstate_match_count']+=int(valid)
  result['all_eight_match']=(result['official_png_match_count']==8 and result['official_model_blockstate_match_count']==8)
 except Exception as e:result['error']=type(e).__name__+': '+str(e)
 print(json.dumps(result,ensure_ascii=False,indent=2))
 return 0 if result.get('all_eight_match') else 1
if __name__=='__main__':sys.exit(main())
