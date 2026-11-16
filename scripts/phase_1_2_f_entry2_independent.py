"""Independent source/geometry/visual/D option crosscheck for F Entry2."""
import csv,json,hashlib,collections
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[1];B=R/'research/vanilla_models/phase_1-2-F/entry2'
def rows(name):
 with (B/name).open(newline='') as f:return list(csv.DictReader(f))
def sha(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def modelpath(ref):
 a=ref.split(':',1);return f'1.21.11/assets/{a[0] if len(a)==2 else "minecraft"}/models/{a[-1]}.json'
q=rows('F_ENTRY2_QUEUE_494.csv');m=rows('STYLE_OBSERVATIONS.csv');e=rows('F_GEOMETRY_ELEMENTS.csv');p=rows('F_PNG_DIRECT_VISUAL_OBSERVATIONS.csv');d=rows('F_D_ORIGINAL_RULE_CHOICES.csv');g=rows('F_GEOMETRY_FEATURES.csv');t=rows('F_TEXTURE_VISUAL_EVIDENCE.csv');a=rows('F_ASSEMBLY_LINKS.csv')
assert len(q)==len(m)==len(g)==len(t)==len(a)==494 and len({x['source_path'] for x in q})==494
assert len(p)==303 and len({x['png_path'] for x in p})==303 and len(d)==1092
M={x['model_path']:x for x in m};E=collections.defaultdict(list)
for x in e:E[x['model_path']].append(x)
assert set(M)=={x['source_path'] for x in q}
models=general=special=visual=unbound=elements=face=uv_exp=uv_abs=0
for x in q:
 path=x['source_path'];raw=(R/path).read_bytes();assert sha(raw)==x['git_blob_sha']==M[path]['model_sha'];leaf=json.loads(raw);seen=set();cur=leaf;chain=[]
 while True:
  curpath=path if not chain else modelpath(chain[-1]['parent_ref']);assert curpath not in seen;seen.add(curpath)
  r=(R/curpath).read_bytes();cur=json.loads(r);chain.append({'path':curpath,'sha':sha(r),'parent_ref':cur.get('parent'),'own_elements':len(cur.get('elements',[]))})
  if not cur.get('parent'):break
 assert chain==json.loads(M[path]['parent_chain_json']);prov=next((z for z in chain if z['own_elements']),None)
 if x['E_exception_owned']=='YES':
  special+=1;assert not prov and M[path]['element_count']=='N/A' and M[path]['runtime_renderer']=='UNVERIFIED_RUNTIME_RENDERER'
 else:
  general+=1;assert prov and prov['path']==M[path]['geometry_provider_path'] and prov['sha']==M[path]['geometry_provider_sha']
  src=json.loads((R/prov['path']).read_text())['elements'];assert len(src)==len(E[path])==int(M[path]['element_count'])
  elements+=len(src);faces=[f for el in src for f in el.get('faces',{}).values()];n=len(faces)
  assert n==int(M[path]['face_count'])==int(x['C_geometry_faces_prior']);face+=n
  uv=sum('uv' in f for f in faces);assert uv==int(M[path]['UV_explicit'])==int(x['C_uv_explicit_faces_prior']);uv_exp+=uv;uv_abs+=n-uv
  assert sum(any(abs(el['to'][i]-el['from'][i])<=1 for i in range(3)) for el in src)==int(M[path]['thin_elements'])
  assert sum('rotation' in el for el in src)==int(M[path]['rotated_elements'])
  for j,el in enumerate(src):
   z=E[path][j];assert json.loads(z['from_json'])==el['from'] and json.loads(z['to_json'])==el['to'] and json.loads(z['rotation_json'])==el.get('rotation')
   assert json.loads(z['face_keys_json'])==sorted(el.get('faces',{})) and int(z['face_count'])==len(el.get('faces',{}))
   assert int(z['face_UV_explicit'])==sum('uv' in f for f in el.get('faces',{}).values())
 paths=json.loads(M[path]['source_PNG_paths_json']);visual+=bool(paths);unbound+=not bool(paths)
 assert bool(paths)==(M[path]['F_PNG_first_frame_observed']=='YES_SOURCE_FIRST_FRAME')
 assert M[path]['F_status']=='F_ENTRY2_SOURCE_STYLE_ACCEPTED_WITH_EXPLICIT_LIMITS'
 assert (x['D_direct_model_selected']=='YES')==(int(M[path]['D_original_rule_choices'])>0)
 models+=1
assert (models,general,special,elements,face,uv_exp,uv_abs,visual,unbound)==(494,447,47,1944,7131,5986,1145,467,27)
for i,x in enumerate(p):
 raw=(R/x['png_path']).read_bytes();im=Image.open(R/x['png_path']);im.load()
 assert sha(raw)==x['png_sha'] and (im.width,im.height)==(int(x['width']),int(x['height']))
 assert x['F_visual_first_frame_observed']=='YES' and x['contact_index']==str(i)
 assert (B/x['contact_sheet']).exists()
D={}
for x in d:
 bp=x['blockstate_path'];assert sha((R/bp).read_bytes())==x['blockstate_sha'];obj=D.setdefault(bp,json.loads((R/bp).read_text()))
 rules=[('VARIANT',str(k),v) for k,v in obj['variants'].items()] if 'variants' in obj else [('MULTIPART',json.dumps(part.get('when',{}),sort_keys=True),part['apply']) for part in obj['multipart']]
 ri=int(x['rule_index']);ai=int(x['alternative_index']);kind,cond,app=rules[ri];opt=(app if isinstance(app,list) else [app])[ai]
 assert (kind,cond,modelpath(opt['model']))==(x['rule_kind'],x['condition'],x['model_path'])
 for key in ('x','y','uvlock','weight'):
  assert x[key+'_present']==str(key in opt)
  assert x[key]==str(opt[key]) if key in opt else x[key]==''
assert len(D)==len({x['blockstate_path'] for x in d})
assert len(rows('F_UNRESOLVED.csv'))==74
out={'schema':'F_ENTRY2_INDEPENDENT_SOURCE_STYLE_AUDIT/v1','baseline_main':'9c771b684859a444bcd29fc36a023299c3a954f0','queue_original_JSON_and_SHA':models,'general_geometry':general,'E_source_exceptions':special,'parent_chain_and_geometry_provider_rechecked':models,'applied_elements':elements,'applied_faces_equal_prior_C':face,'UV_key_explicit':uv_exp,'UV_key_absent':uv_abs,'PNG_unique_original_SHA_dimension_first_frame_checked':len(p),'models_with_source_PNG_visual_evidence':visual,'unbound_template_visual_limit':unbound,'D_original_model_rule_options':len(d),'D_original_blockstate_paths':len(D),'D_direct_model_count':sum(x['D_direct_selected']=='YES' for x in m),'D_not_direct_model_count':sum(x['D_direct_selected']=='NO' for x in m),'E_runtime_renderer_verified':0,'explicit_unresolved_rows':74,'Entry2_source_style_accepted':494,'F_cumulative_source_style_accepted':644,'F_remaining':1746,'mismatches':0,'pass':True,'Entry2_complete':False,'F_complete':False}
(B/'F_ENTRY2_INDEPENDENT_AUDIT.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(out,ensure_ascii=False,indent=2))
