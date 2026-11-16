"""Finish F Entry1 visual source and original blockstate-rule evidence."""
import csv,json,hashlib,colorsys,collections,statistics,shutil
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
B=ROOT/'research/vanilla_models/phase_1-2-F/entry1'
def sha(data):return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
def read(name):
 with (B/name).open(newline='') as f:return list(csv.DictReader(f))
def write(name,rows,fields=None):
 with (B/name).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields or list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
def refpath(ref):
 ns,x=ref.split(':',1) if ':' in ref else ('minecraft',ref)
 return f'1.21.11/assets/{ns}/models/{x}.json'
queue=read('F_ENTRY1_QUEUE_150.csv');style=read('STYLE_OBSERVATIONS.csv');slots=read('F_TEXTURE_C_SLOT_PNG_LINKS.csv')
assert len(queue)==len(style)==150
entry={r['source_path']:r for r in queue};assert set(entry)=={r['source_path'] for r in style}
by_model=collections.defaultdict(set)
for row in slots:
 if row['PNG_path']:by_model[row['model_path']].add(row['PNG_path'])
for q in queue:
 if q['E_exception_owned']=='YES':
  d=json.loads((ROOT/q['source_path']).read_text());particle=d.get('textures',{}).get('particle')
  if particle:by_model[q['source_path']].add('1.21.11/assets/minecraft/textures/'+particle.split(':')[-1]+'.png')
paths=sorted(set.union(*[v for v in by_model.values() if v]));index=json.loads((B/'visual_contact/index.json').read_text());assert paths==index and len(paths)==195
manual={
 'acacia_shelf':'32×32 원본 첫 면에서 가로 구획선과 세로 칸 구분이 보인다. 0두께 판 기하의 표면 무늬 후보.',
 'birch_shelf':'32×32 원본에서 칸 구획과 가로 선이 보인다. 판의 두께를 이 이미지로 증명하지 않는다.',
 'lantern':'투명 배경 위 발광색 중심과 어두운 테두리, 분리된 상부 고리 모양 픽셀을 관찰.',
 'copper_lantern':'48픽셀 높이 원본 첫 프레임에 투명 바탕과 몸체·고리 모양 픽셀이 보인다.',
 'cherry_trapdoor':'투명 구멍과 둘레 프레임 색이 보인다. 입체 깊이는 모델 요소에서 별도로 확인.',
 'birch_planks':'불투명한 밝은 가로 결 무늬가 보인다. 실제 물리 재질은 판단하지 않는다.',
 'jukebox_side':'불투명한 갈색 계열 격자 무늬가 보인다. 깊이 있는 홈 여부는 이미지로 단정하지 않는다.',
 'vault_front_on_ominous':'불투명한 외곽과 중앙 대비 무늬가 보인다. 모델의 역방향 내부면과 별도 근거.',
 'redstone_dust_line1':'투명 바탕 위 가느다란 밝은 선형 픽셀이 보인다.',
 'water_still':'16×512 애니메이션 PNG의 첫 16×16 프레임에서 푸른색 반투명 무늬를 관찰. 나머지 프레임 미시각 검토.',
 'purple_shulker_box':'첫 프레임은 보라 계열의 불투명 면과 경계 무늬. 실제 상자 형태는 E renderer 미검증.',
 'beehive_front_honey':'불투명한 면에 밝은 중앙 띠와 작은 대비 무늬가 보인다.',
}
visual=[];prior_sha={}
for row in slots:
 if row['PNG_path'] and row['PNG_SHA_C_prior']:
  p=row['PNG_path'];assert p not in prior_sha or prior_sha[p]==row['PNG_SHA_C_prior'];prior_sha[p]=row['PNG_SHA_C_prior']
for i,p in enumerate(paths):
 raw=(ROOT/p).read_bytes();im=Image.open(ROOT/p);im.load();rgba=im.convert('RGBA');w,h=im.size
 pix=list(rgba.crop((0,0,w,min(w,h))).get_flattened_data());opaque=[(r,g,b) for r,g,b,a in pix if a>0]
 hist=collections.Counter(opaque);alpha=collections.Counter(a for *_,a in pix)
 top=hist.most_common(1)[0][0] if hist else None
 if top:
  r,g,b=top;hh,ss,vv=colorsys.rgb_to_hsv(r/255,g/255,b/255)
  tone=('DARK_NEUTRAL' if vv<.25 else 'LIGHT_NEUTRAL' if vv>.82 else 'MID_NEUTRAL') if ss<.17 else ['RED','ORANGE','YELLOW','GREEN','CYAN','BLUE','PURPLE','MAGENTA'][int((hh*360+22.5)%360//45)]
 else:tone='NO_VISIBLE_PIXELS'
 note=manual.get(Path(p).stem,'첫 정방 프레임을 접촉시트에서 눈으로 확인했다. 아래 색·투명도·색상 수는 픽셀 계산값이며 물리 재질이나 게임 렌더 결과가 아니다.')
 visual.append({'png_path':p,'git_blob_sha':sha(raw),'C_prior_blob_sha':prior_sha.get(p,''),'C_sha_match':'YES' if p in prior_sha and sha(raw)==prior_sha[p] else 'NOT_IN_C_FACE_LEDGER_E_OR_OTHER',
  'width':w,'height':h,'visual_frame':'FIRST_SQUARE_FRAME_ONLY' if h>w else 'FULL_IMAGE','contact_sheet':f'visual_contact/contact_{i//48+1:02d}.png','contact_index':i,
  'first_frame_visible_pixels':len(opaque),'first_frame_transparent_pixels':alpha[0],'first_frame_partial_alpha_pixels':sum(n for a,n in alpha.items() if 0<a<255),
  'first_frame_unique_visible_RGB':len(hist),'dominant_RGB':json.dumps(top),'dominant_color_family_metric':tone,
  'observed_visual_note':note,'evidence_grade':'F_ORIGINAL_PNG_FIRST_FRAME_VISUALLY_OBSERVED_SOURCE_ASSET_ONLY'})
write('F_PNG_DIRECT_VISUAL_OBSERVATIONS.csv',visual)
assert all((B/'visual_contact'/f'contact_{i:02d}.png').exists() for i in range(1,6))
# Original D blockstate rule choices, distinct from syntactic state expansions.
links=read('F_D_STATE_MODEL_SOURCE_LINKS.csv');assert len(links)==1180
expected={x['source_path'] for x in queue};blockstates={x['blockstate_path'] for x in links};source_shas=collections.defaultdict(set)
for x in links:
 if x['blockstate_source_sha']:source_shas[x['blockstate_path']].add(x['blockstate_source_sha'])
choice=[]
for p in sorted(blockstates):
 raw=(ROOT/p).read_bytes();actual=sha(raw);assert len(source_shas[p])<=1 and (not source_shas[p] or source_shas[p]=={actual})
 d=json.loads(raw)
 if 'variants' in d:rules=[('VARIANT',str(k),v) for k,v in d['variants'].items()]
 else:rules=[('MULTIPART',json.dumps(part.get('when',{}),sort_keys=True),part['apply']) for part in d['multipart']]
 for ri,(kind,condition,apps) in enumerate(rules):
  for ai,opt in enumerate(apps if isinstance(apps,list) else [apps]):
   model=refpath(opt['model'])
   if model not in expected:continue
   choice.append({'model_path':model,'model_sha':entry[model]['git_blob_sha'],'blockstate_path':p,'blockstate_sha':actual,'rule_kind':kind,'rule_index':ri,'rule_condition':condition,'alternative_index':ai,'alternative_count':len(apps) if isinstance(apps,list) else 1,
    'x_key_present':'x' in opt,'x_value_if_present':opt.get('x',''),'y_key_present':'y' in opt,'y_value_if_present':opt.get('y',''),
    'uvlock_key_present':'uvlock' in opt,'uvlock_value_if_present':opt.get('uvlock',''),'weight_key_present':'weight' in opt,'weight_value_if_present':opt.get('weight',''),
    'source_grade':'F_ORIGINAL_BLOCKSTATE_RULE_DIRECT_READ_STATIC_NOT_RUNTIME'})
write('F_D_ORIGINAL_RULE_CHOICES.csv',choice)
choice_by_model=collections.defaultdict(list)
for x in choice:choice_by_model[x['model_path']].append(x)
link_by_model=collections.defaultdict(list)
for x in links:link_by_model[x['model_path']].append(x)
for p,ls in link_by_model.items():
 assert p in choice_by_model
 assert {x['blockstate_path'] for x in ls}<={x['blockstate_path'] for x in choice_by_model[p]}
# Persist source/visual/assembly model records, retaining all prior columns.
tex=read('F_TEXTURE_VISUAL_EVIDENCE.csv');assembly=read('F_ASSEMBLY_LINKS.csv');status=read('F_MODEL_SOURCE_STATUS.csv')
for r in tex:
 p=r['model_path'];pp=sorted(by_model[p]);r['F_direct_source_PNG_paths']=json.dumps(pp);r['F_direct_source_PNG_count']=len(pp)
 r['F_original_PNG_image_directly_seen']='true' if pp else 'false'
 r['F_texture_detail_style']='FIRST_FRAME_SOURCE_PNG_OBSERVED_NOT_RENDERED_SURFACE' if pp else 'NO_RESOLVED_PNG_IN_THIS_UNBOUND_TEMPLATE'
 r['F_style_confidence']='SOURCE_PIXEL_OBSERVED_GEOMETRY_COMPARE_LIMITED' if pp else 'EXPLICIT_UNBOUND_TEMPLATE_LIMITATION'
for r in assembly:
 p=r['model_path'];c=choice_by_model[p];r['F_D_original_rule_choices']=len(c)
 r['F_D_original_rule_kinds']=json.dumps(sorted({x['rule_kind'] for x in c}))
 r['F_D_original_x_explicit_choices']=sum(x['x_key_present'] for x in c)
 r['F_D_original_y_explicit_choices']=sum(x['y_key_present'] for x in c)
 r['F_D_original_uvlock_explicit_choices']=sum(x['uvlock_key_present'] for x in c)
 r['F_D_original_weight_explicit_choices']=sum(x['weight_key_present'] for x in c)
 r['F_D_original_source_status']='DIRECT_BLOCKSTATE_RULE_VERIFIED' if c else 'NOT_DIRECT_D_SELECTED_SOURCE_ROLE_UNDETERMINED'
for r in style:
 p=r['source_path'];q=entry[p];pp=sorted(by_model[p]);e=q['E_exception_owned']=='YES';c=choice_by_model[p]
 r['F_original_PNG_visual_observed']='YES_SOURCE_FIRST_FRAME' if pp else 'NO_UNBOUND_TEMPLATE'
 r['F_style_visual_status']='SOURCE_PNG_OBSERVED_WITH_E_RUNTIME_LIMIT' if e else 'SOURCE_PNG_OBSERVED' if pp else 'EXPLICIT_UNBOUND_TEMPLATE_NO_PNG'
 r['F_direct_source_PNG_count']=len(pp);r['F_direct_source_PNG_paths']=json.dumps(pp)
 r['material_appearance']='PIXEL_COLOR_ALPHA_PATTERN_OBSERVED_NO_PHYSICAL_MATERIAL_CLAIM' if pp else 'NO_BOUND_PNG_FOR_TEMPLATE'
 r['F_texture_detail_vs_geometry']='PARTICLE_IMAGE_NOT_RENDERER_SURFACE' if e else 'SOURCE_GEOMETRY_AND_PNG_FIRST_FRAME_COMPARED_NO_RUNTIME_RENDER' if pp else 'GEOMETRY_ONLY_UNBOUND_TEXTURE_TEMPLATE'
 r['F_D_assembly_status']='DIRECT_ORIGINAL_RULE_CHOICES_CHECKED' if c else 'NOT_DIRECT_D_SELECTED_ROLE_UNDETERMINED'
 r['D_original_state_model_rules_in_F']='DIRECT_SOURCE_RULE_READ' if c else 'NOT_DIRECT_SELECTED'
 r['F_record_status']='F_ENTRY1_SOURCE_STYLE_ACCEPTED_WITH_EXPLICIT_RENDER_OR_TEMPLATE_LIMIT'
 r['D_original_rule_choice_count_F']=len(c)
 r['furniture_reuse_pattern_claim_grade']='MODELING_HYPOTHESIS_GROUNDED_IN_SOURCE_GEOMETRY_AND_PNG_LIMITS'
for r in status:
 p=r['source_path'];r['visual_style_comparison']='PNG_FIRST_FRAME_SOURCE_OBSERVED' if by_model[p] else 'UNBOUND_TEMPLATE_NO_DIRECT_PNG'
 r['D_assembly_rule_recheck']='ORIGINAL_RULE_CHOICES_VERIFIED' if choice_by_model[p] else 'NOT_DIRECT_SELECTED'
 r['F_full_entry1_status']='ACCEPTED_SOURCE_SCOPE_WITH_EXPLICIT_LIMITS'
write('F_TEXTURE_VISUAL_EVIDENCE.csv',tex);write('F_ASSEMBLY_LINKS.csv',assembly);write('STYLE_OBSERVATIONS.csv',style);write('F_MODEL_SOURCE_STATUS.csv',status)
for r in slots:r['PNG_original_image_visual_observed_by_F']='YES_FIRST_FRAME' if r['PNG_path'] else 'NO_UNRESOLVED_BINDING'
write('F_TEXTURE_C_SLOT_PNG_LINKS.csv',slots)
issues=[]
for r in queue:
 p=r['source_path']
 if not by_model[p]:issues.append({'source_path':p,'git_blob_sha':r['git_blob_sha'],'owner':'F','issue':'UNBOUND_TEMPLATE_NO_RESOLVED_PNG','gate':'F3','source_evidence':'ORIGINAL_MODEL_AND_C_SLOT_RESOLUTION','needed':'CHILD_MODEL_TEXTURE_BINDING_IF_REUSED','status':'EXPLICIT_LIMIT_NOT_BLOCKING_ENTRY1_SOURCE_SCOPE'})
 if r['E_exception_owned']=='YES':issues.append({'source_path':p,'git_blob_sha':r['git_blob_sha'],'owner':'E_RUNTIME_FUTURE','issue':'SPECIAL_RENDERER_RUNTIME_UNVERIFIED','gate':'F3','source_evidence':'E_SOURCE_EXCEPTION_86','needed':'OFFICIAL_CLIENT_OR_INGAME_RENDER','status':'OUT_OF_F_SOURCE_SCOPE_UNVERIFIED'})
write('F_UNRESOLVED.csv',issues)
print(json.dumps({'queue':len(queue),'PNG_unique':len(visual),'PNG_linked_models':sum(bool(by_model[x['source_path']]) for x in queue),'unbound_templates':sum(not by_model[x['source_path']] for x in queue),'D_rule_choices':len(choice),'D_models':sum(bool(v) for v in choice_by_model.values()),'D_blockstates':len(blockstates),'unresolved':len(issues)},indent=2))
