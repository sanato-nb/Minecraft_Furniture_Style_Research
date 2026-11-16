"""Direct source-oriented F Entry2 P1 morphology, C image, D assembly study."""
import csv,glob,json,hashlib,collections,colorsys
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[1];B=R/'research/vanilla_models/phase_1-2-F/entry2';B.mkdir(exist_ok=True)
def sha(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def read(p):
 with Path(p).open(newline='') as f:return list(csv.DictReader(f))
def write(p,rows,fields=None):
 with Path(p).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields or list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
def modelpath(ref):
 a=ref.split(':',1);return f'1.21.11/assets/{a[0] if len(a)==2 else "minecraft"}/models/{a[-1]}.json'
def pngpath(ref):
 a=ref.split(':',1);return f'1.21.11/assets/{a[0] if len(a)==2 else "minecraft"}/textures/{a[-1]}.png'
q=read(B/'F_ENTRY2_QUEUE_494.csv');assert len(q)==494 and len({x['source_path'] for x in q})==494 and all(x['priority']=='P1' for x in q)
Q={x['source_path']:x for x in q}
bgeom={x['full_source_path']:x for x in read(R/'research/vanilla_models/phase_1-2-B/entry10/MODEL_GEOMETRY_ALL_2360.csv')}
cb=collections.defaultdict(list);cf=collections.defaultdict(list)
for f in sorted(glob.glob(str(R/'research/vanilla_models/phase_1-2-C/entry*/TEXTURE_BINDINGS.csv'))):
 for x in read(f):
  if x['leaf_path'] in Q:cb[x['leaf_path']].append(x)
for f in sorted(glob.glob(str(R/'research/vanilla_models/phase_1-2-C/entry*/FACE_UV_EVIDENCE.csv'))):
 for x in read(f):
  if x['leaf_path'] in Q:cf[x['leaf_path']].append(x)
# Parse original blockstate bodies from the fixed D scope, for all 494 target models.
D=collections.defaultdict(list);dscope=read(R/'research/vanilla_models/phase_1-2-D/D_FIXED_SCOPE_1168.csv')
for item in dscope:
 p=item['source_path'];raw=(R/p).read_bytes();assert sha(raw)==item['git_blob_sha'];obj=json.loads(raw)
 rules=[('VARIANT',str(k),v) for k,v in obj['variants'].items()] if 'variants' in obj else [('MULTIPART',json.dumps(z.get('when',{}),sort_keys=True),z['apply']) for z in obj['multipart']]
 for ri,(kind,condition,app) in enumerate(rules):
  options=app if isinstance(app,list) else [app]
  for ai,opt in enumerate(options):
   m=modelpath(opt['model'])
   if m not in Q:continue
   D[m].append({'model_path':m,'model_sha':Q[m]['git_blob_sha'],'blockstate_path':p,'blockstate_sha':item['git_blob_sha'],'rule_kind':kind,'rule_index':ri,'condition':condition,'alternative_index':ai,'alternative_count':len(options),
    'x_present':'x' in opt,'x':opt.get('x',''),'y_present':'y' in opt,'y':opt.get('y',''),'uvlock_present':'uvlock' in opt,'uvlock':opt.get('uvlock',''),'weight_present':'weight' in opt,'weight':opt.get('weight',''),
    'source_grade':'F_ORIGINAL_BLOCKSTATE_CHOICE_STATIC'})
assert sum(bool(D[x['source_path']]) for x in q)==446
choices=[r for x in q for r in D[x['source_path']]];write(B/'F_D_ORIGINAL_RULE_CHOICES.csv',choices)
models=[];geoms=[];faces=[];png_usage=collections.defaultdict(set);issues=[]
for x in q:
 p=x['source_path'];raw=(R/p).read_bytes();assert sha(raw)==x['git_blob_sha'];obj=json.loads(raw)
 chain=[];cur=obj;seen=set()
 while True:
  cp=p if not chain else modelpath(chain[-1]['parent_ref']);assert cp not in seen;seen.add(cp)
  rr=(R/cp).read_bytes();d=json.loads(rr);chain.append({'path':cp,'sha':sha(rr),'parent_ref':d.get('parent'),'own_elements':len(d.get('elements',[]))})
  if not d.get('parent'):break
 assert len(chain)<30
 provider=next((r for r in chain if r['own_elements']),None)
 es=json.loads((R/provider['path']).read_text())['elements'] if provider else []
 is_e=x['E_exception_owned']=='YES';assert is_e==(not bool(es));assert (x['D_direct_model_selected']=='YES')==bool(D[p])
 if is_e:
  assert x['C_assignment']=='E_EXCEPTION'
 else:
  b=bgeom[p];assert b['git_blob_sha']==x['git_blob_sha'] and b['geometry_provider_path']==provider['path'] and b['geometry_provider_sha']==provider['sha']
  assert json.loads(b['parent_chain_paths'])==[r['path'] for r in chain]
  assert int(b['effective_element_instances'])==len(es)
 dims=[];zero=thin=rot=inv=outside=face_count=uv_exp=0
 for ei,e in enumerate(es):
  f,t=e['from'],e['to'];delta=[abs(t[i]-f[i]) for i in range(3)];dims.append(delta)
  zero+=any(v==0 for v in delta);thin+=any(v<=1 for v in delta);rot+='rotation' in e;inv+=any(t[i]<f[i] for i in range(3));outside+=any(v<0 or v>16 for v in f+t)
  face_count+=len(e.get('faces',{}));uv_exp+=sum('uv' in face for face in e.get('faces',{}).values())
  geoms.append({'model_path':p,'model_sha':x['git_blob_sha'],'provider_path':provider['path'],'provider_sha':provider['sha'],'element_index':ei,'from_json':json.dumps(f),'to_json':json.dumps(t),'axis_thickness_json':json.dumps(delta),'rotation_json':json.dumps(e.get('rotation')),'face_keys_json':json.dumps(sorted(e.get('faces',{}))),'face_count':len(e.get('faces',{})),'face_UV_explicit':sum('uv' in z for z in e.get('faces',{}).values()),'zero_thickness':any(v==0 for v in delta),'thin_le_1':any(v<=1 for v in delta)})
 if not is_e:
  assert face_count==int(x['C_geometry_faces_prior'])==len(cf[p]);assert uv_exp==int(x['C_uv_explicit_faces_prior'])
  assert face_count-uv_exp==int(x['C_uv_implicit_faces_prior'])
  assert int(bgeom[p]['effective_face_declaration_refs'])==face_count
  assert int(bgeom[p]['zero_thickness_elements'])==zero and int(bgeom[p]['rotated_elements'])==rot
 bbox=([min(min(e['from'][i],e['to'][i]) for e in es) for i in range(3)],[max(max(e['from'][i],e['to'][i]) for e in es) for i in range(3)]) if es else None
 extent=[bbox[1][i]-bbox[0][i] for i in range(3)] if bbox else None
 exact=len(es)==1 and es[0]['from']==[0,0,0] and es[0]['to']==[16,16,16] and not es[0].get('rotation')
 tags=['E_SOURCE_EXCEPTION'] if is_e else ['AXIS_ALIGNED_CUBOIDS']+(['EXACT_FULL_CUBE'] if exact else [])+(['THIN_ELEMENT'] if thin else [])+(['ZERO_THICKNESS'] if zero else [])+(['MULTI_ELEMENT'] if len(es)>1 else [])+(['ROTATED_ELEMENT'] if rot else [])+(['INVERTED_OR_OUTSIDE_16'] if inv or outside else [])
 primary='SPECIAL_RENDER_SOURCE' if is_e else 'STRICT_FULL_CUBE' if exact else 'ROTATED_GEOMETRY' if rot else 'MULTI_ELEMENT_GEOMETRY' if len(es)>1 else 'THIN_OR_ZERO_THICKNESS' if thin else 'OTHER_SIMPLE_CUBOID'
 textures=set()
 for row in cb[p]:
  if row['resolved_texture'] and row['status']=='resolved':textures.add(pngpath(row['resolved_texture']))
 for row in cf[p]:
  if row['png_path']:textures.add(row['png_path'])
 if is_e:
  ref=obj.get('textures',{}).get('particle')
  if ref and ref!='minecraft:missingno':textures.add(pngpath(ref))
 for pp in textures:
  if (R/pp).exists():png_usage[pp].add(p)
  else:issues.append({'model_path':p,'model_sha':x['git_blob_sha'],'issue':'DECLARED_PNG_NOT_IN_EXTRACT','evidence':pp,'status':'OPEN_SOURCE_ASSET_MISSING'})
 pngs=sorted(pp for pp in textures if (R/pp).exists())
 if not pngs:issues.append({'model_path':p,'model_sha':x['git_blob_sha'],'issue':'UNBOUND_OR_MISSING_PNG','evidence':'C bindings and E particle checked','status':'EXPLICIT_VISUAL_LIMIT'})
 if is_e:issues.append({'model_path':p,'model_sha':x['git_blob_sha'],'issue':'E_RUNTIME_RENDERER_UNVERIFIED','evidence':'E source-only exception','status':'OUT_OF_F_SOURCE_RUNTIME_SCOPE'})
 if primary=='STRICT_FULL_CUBE':transfer='단일 16³ 몸체의 외곽은 기하, 보이는 면 무늬는 PNG 후보로 분리한다.'
 elif primary=='THIN_OR_ZERO_THICKNESS':transfer='얇은 판/전면 장식 후보. 원본 0두께 면의 실제 양면 가시는 미검증이다.'
 elif primary=='MULTI_ELEMENT_GEOMETRY':transfer='여러 직육면체를 지지대·틀·단차 후보로 재사용한다. 원본 물체의 가구 기능은 추정하지 않는다.'
 elif primary=='ROTATED_GEOMETRY':transfer='회전 요소를 작은 대각 장식 또는 교차 판 후보로 활용한다. 축/각도는 원본에 한한다.'
 elif primary=='OTHER_SIMPLE_CUBOID':transfer='전체 블록보다 낮거나 좁은 단일 부피를 상판·받침 후보로 쓴다.'
 else:transfer='일반 elements가 없어 형태 이식 불가. particle 이미지는 실제 렌더 표면 근거가 아니다.'
 models.append({'model_path':p,'model_sha':x['git_blob_sha'],'F_queue_index':x['F_queue_index'],'priority':'P1','source_json_direct':'YES','parent_chain_json':json.dumps(chain,ensure_ascii=False),'geometry_provider_path':provider['path'] if provider else '','geometry_provider_sha':provider['sha'] if provider else '',
  'E_exception':is_e,'element_count':len(es) if not is_e else 'N/A','face_count':face_count if not is_e else 'N/A','UV_explicit':uv_exp if not is_e else 'N/A','UV_key_absent':face_count-uv_exp if not is_e else 'N/A',
  'bbox_min_json':json.dumps(bbox[0]) if bbox else '','bbox_max_json':json.dumps(bbox[1]) if bbox else '','bbox_extent_json':json.dumps(extent) if extent else '',
  'axis_thickness_json':json.dumps(dims),'zero_elements':zero if not is_e else 'N/A','thin_elements':thin if not is_e else 'N/A','rotated_elements':rot if not is_e else 'N/A','inverted_elements':inv if not is_e else 'N/A','outside_elements':outside if not is_e else 'N/A',
  'tags':'|'.join(tags),'primary_archetype':primary,'source_PNG_paths_json':json.dumps(pngs),'F_PNG_first_frame_observed':'PENDING_CONTACT_REVIEW' if pngs else 'NO_BOUND_SOURCE_PNG',
  'C_prior_binding_rows':len(cb[p]),'C_prior_face_rows':len(cf[p]),'D_direct_selected':x['D_direct_model_selected'],'D_original_rule_choices':len(D[p]),'D_blockstate_paths_json':json.dumps(sorted({d['blockstate_path'] for d in D[p]})),
  'furniture_transfer_hypothesis':transfer,'runtime_renderer':'UNVERIFIED_RUNTIME_RENDERER' if is_e else 'NOT_INGAME_TESTED','F_status':'SOURCE_GEOMETRY_AND_D_RECHECKED_VISUAL_PENDING'})
write(B/'F_MODEL_SOURCE_STATUS.csv',models)
write(B/'F_GEOMETRY_ELEMENTS.csv',geoms,fields=['model_path','model_sha','provider_path','provider_sha','element_index','from_json','to_json','axis_thickness_json','rotation_json','face_keys_json','face_count','face_UV_explicit','zero_thickness','thin_le_1'])
# Sourced PNG palette metrics; human visual observations supplied in a later reviewed contact-sheet pass.
pngrows=[]
for p,owners in sorted(png_usage.items()):
 raw=(R/p).read_bytes();im=Image.open(R/p);im.load();w,h=im.size;frame=im.convert('RGBA').crop((0,0,w,min(w,h)));px=list(frame.get_flattened_data());visible=[c[:3] for c in px if c[3]>0];hist=collections.Counter(visible);alpha=collections.Counter(c[3] for c in px)
 dominant=hist.most_common(1)[0][0] if hist else None
 pngrows.append({'png_path':p,'png_sha':sha(raw),'width':w,'height':h,'first_frame_visible_pixels':len(visible),'first_frame_transparent_pixels':alpha[0],'first_frame_partial_alpha_pixels':sum(n for a,n in alpha.items() if 0<a<255),'first_frame_unique_RGB':len(hist),'dominant_RGB':json.dumps(dominant),'models_linked':len(owners),'observed_visual_note':'PENDING_HUMAN_CONTACT_SHEET_REVIEW','image_evidence_status':'SOURCE_PIXEL_DECODED_NOT_YET_VISUALLY_REVIEWED'})
write(B/'F_TEXTURE_VISUAL_EVIDENCE.csv',pngrows)
write(B/'F_UNRESOLVED.csv',issues)
summary={'schema':'F_ENTRY2_SOURCE_FIRST_PASS/v1','baseline_head':'9c771b684859a444bcd29fc36a023299c3a954f0','entry2_assigned':494,'original_JSON_SHA_direct':len(models),'general_geometry':sum(x['E_exception']==False for x in models),'E_exception':sum(x['E_exception']==True for x in models),'elements':len(geoms),'faces':sum(x['face_count'] for x in geoms),'C_prior_face_rows':sum(len(cf[p]) for p in Q),'C_prior_binding_rows':sum(len(cb[p]) for p in Q),'D_original_rule_choices':len(choices),'D_direct_models':sum(bool(D[p]) for p in Q),'D_not_direct_models':sum(not D[p] for p in Q),'PNG_unique_direct_sha_RGBA_first_frame':len(pngrows),'visual_contact_review_complete':False,'Entry2_complete':False}
(B/'F_SOURCE_FIRST_PASS_AUDIT.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n');print(json.dumps(summary,ensure_ascii=False,indent=2))
