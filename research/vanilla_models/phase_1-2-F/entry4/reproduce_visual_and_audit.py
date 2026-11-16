import csv,json,hashlib
from pathlib import Path
from collections import Counter,defaultdict
R=Path(__file__).resolve().parents[4]; O=R/'research/vanilla_models/phase_1-2-F/entry4'
def load(n):return list(csv.DictReader(open(O/n)))
def save(n,rows):
 with open(O/n,'w',newline='') as f:
  w=csv.DictWriter(f,rows[0].keys());w.writeheader();w.writerows(rows)
def js(x):return json.dumps(x,ensure_ascii=False)
specific={
 'mangrove_trapdoor':'붉은 갈색 정사각 테두리의 중앙에 큰 원형 투명 영역이 보인다.',
 'oak_door_top':'갈색 외곽 틀 안에 네 칸의 투명 영역과 아래쪽 작은 회색 픽셀이 보인다.',
 'observer_front':'회색 사각 얼굴 같은 두 개의 어두운 칸이 보인다. 실제 기능은 이미지로 판정하지 않는다.',
 'observer_back_on':'어두운 사각 외곽 안쪽의 붉은 점이 보인다.',
 'scaffolding_top':'갈색 수직·수평 격자 사이에 작은 투명 칸들이 반복된다.',
 'scaffolding_side':'연갈색 사각 테두리 안이 넓게 투명하다.',
 'redstone_dust_dot':'투명 배경 위에 작은 흰색 점 모양 픽셀 무리가 보인다.',
 'tripwire':'투명 배경 위 가는 회색 점선 픽셀들이 이어진다.',
 'spruce_trapdoor':'갈색 세로 판과 중앙 가로 띠, 작은 밝은 구멍이 보인다.',
 'warped_trapdoor':'청록색 틀과 가운데 큰 투명 영역이 보인다.',
 'piston_top':'회갈색 외곽 안에 황갈색 가로·세로대가 격자를 만든다.',
 'target_top':'연한 바탕 위 붉은 동심 사각형과 중앙 점이 보인다.',
 'acacia_door_bottom':'갈색 수직 살 사이에 투명한 빈 공간이 보이며 하단에 어두운 가로 띠가 있다.',
 'bamboo_fence_gate':'연노란 가로대·기둥과 중앙의 투명한 두 칸이 보인다.',
 'bamboo_trapdoor':'연노란 외곽 틀과 중앙 격자, 투명한 작은 칸이 보인다.',
 'birch_trapdoor':'밝은 사각 테두리 안에 십자형 안쪽 선이 보인다.',
 'black_stained_glass':'회색 면 둘레에 짙은 테두리와 작은 대각 반사선이 보인다.',
 'black_stained_glass_pane_top':'거의 검은 세로 띠가 보인다.',
 'glass':'옅은 하늘색 경계와 대각 흰 반사선, 넓은 투명 영역이 보인다.',
 'iron_bars':'회색 수직 살과 가로 연결부 사이에 투명 영역이 보인다.',
 'ladder':'갈색 수직 지지대 두 개와 가로대가 반복되고 그 사이가 투명하다.',
 'dark_oak_door_bottom':'진한 갈색의 세로 홈과 작은 노란 돌출처럼 보이는 픽셀 무늬가 있다.',
 'copper_trapdoor':'주황색 틀과 십자형 내부 무늬, 투명한 네 모서리 영역이 보인다.',
 'mangrove_planks':'붉은 갈색 수평 판재 띠가 반복되고 줄마다 명암이 다르다.',
 'lever':'회색 작은 받침과 갈색 세로 막대가 투명 배경 위에 보인다.',
 'redstone_torch':'갈색 세로 줄 위 빨간 네모 광원 모양이 투명 배경에 보인다.'
}
png=load('F_PNG_PIXEL_DECODE_STATUS.csv');note={}
for i,row in enumerate(png):
 stem=Path(row['png_path']).stem
 obs=specific.get(stem,'첫 프레임에서 픽셀 색, 명암 경계와 반복 무늬 또는 알파 실루엣을 접촉 시트로 확인했다. 구체 재질과 실제 3D 렌더는 미판정.')
 row.update(observed_visual_note=obs,image_evidence_status='PNG_FIRST_FRAME_CONTACT_SHEET_VISUALLY_OBSERVED',contact_sheet=f'visual_contact/contact_{i//48+1:02}.png',contact_index=i)
 note[row['png_path']]=obs
save('F_PNG_DIRECT_VISUAL_OBSERVATIONS.csv',png)
sources=load('F_MODEL_SOURCE_STATUS.csv');vis=load('F_TEXTURE_VISUAL_EVIDENCE.csv');styles=load('STYLE_OBSERVATIONS.csv');unres=load('F_UNRESOLVED.csv')
unres=[r for r in unres if r['issue'] not in ('PNG_VISUAL_OBSERVATION_PENDING','SOURCE_TEXTURE_NOT_BOUND')]
for s,v,t in zip(sources,vis,styles):
 assert s['model_path']==v['model_path']==t['model_path']
 links=json.loads(v['F_original_PNG_paths_sha_json']); observed=bool(links)
 text='; '.join(f'{p}@{h}: {note[p]}' for p,h in links[:3]) if observed else '실제 바인딩 PNG가 없어 자체 색·패턴 외형은 판정 불가.'
 state='YES_SOURCE_FIRST_FRAME' if observed else 'NO_BOUND_TEXTURE'
 s.update(F_PNG_first_frame_observed=state,F_status='F_ENTRY4_SOURCE_STYLE_ACCEPTED_WITH_EXPLICIT_LIMITS')
 v.update(F_first_frame_direct_visual_observed=state,F_observed_first_PNG_note=text,detail_vs_geometry=('SOURCE_GEOMETRY_AND_FIRST_FRAME_TEXTURE_OBSERVED' if observed else 'UNBOUND_TEMPLATE_VISUAL_UNRESOLVED'),source_confidence='SOURCE_FIRST_FRAME_OR_EXPLICIT_UNBOUND_LIMIT')
 t.update(F_PNG_first_frame_observed=state,F_status='F_ENTRY4_SOURCE_STYLE_ACCEPTED_WITH_EXPLICIT_LIMITS',F_visual_vs_geometry=text)
 if not observed:unres.append(dict(model_path=s['model_path'],model_sha=s['model_sha'],issue='SOURCE_TEXTURE_NOT_BOUND',evidence='자체 또는 상속된 적용 면에서 실제 PNG 경로 미연결',status='SOURCE_LIMIT'))
save('F_MODEL_SOURCE_STATUS.csv',sources);save('F_TEXTURE_VISUAL_EVIDENCE.csv',vis);save('STYLE_OBSERVATIONS.csv',styles);save('F_UNRESOLVED.csv',unres)

# A second path through the original JSON checks source hashes and parent provider
# and compares independently counted faces to the earlier C queue, without using
# the feature rows as input for the source-side calculation.
q=load('F_ENTRY4_QUEUE_494.csv');g=load('F_GEOMETRY_FEATURES.csv');ass=load('F_ASSEMBLY_LINKS.csv');els=load('F_GEOMETRY_ELEMENTS.csv');ch=load('F_D_ORIGINAL_RULE_CHOICES.csv')
errors=[];seen=set();total=0
for i,(a,b,c,e) in enumerate(zip(q,sources,g,ass)):
 p=R/a['source_path']; raw=p.read_bytes(); h=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
 if h!=a['git_blob_sha'] or h!=b['model_sha'] or a['source_path'] in seen:errors.append(['identity',i])
 seen.add(a['source_path'])
 if any(x['model_path']!=a['source_path'] for x in (b,c,e)):errors.append(['alignment',i])
 chain=json.loads(b['parent_chain_json']); pp=next((R/z['path'] for z in chain if 'elements' in json.loads((R/z['path']).read_text())),None)
 rawj=json.loads(pp.read_text()) if pp else {}; figures=rawj.get('elements',[])
 if len(figures)!=int(c['element_count']) or sum(len(x.get('faces',{})) for x in figures)!=int(a['C_geometry_faces_prior']):errors.append(['geometry_or_C',i])
 total+=sum(len(x.get('faces',{})) for x in figures)
 if (int(e['D_original_rule_choices'])>0)!=(a['D_direct_model_selected']=='YES'):errors.append(['D',i])
 if sum(x['model_path']==a['source_path'] for x in ch)!=int(e['D_original_rule_choices']):errors.append(['Dcount',i])
 if any(x['provider_sha']!=c['geometry_provider_sha'] for x in els if x['model_path']==a['source_path']):errors.append(['provider',i])
 model_elements=[x for x in els if x['model_path']==a['source_path']]
 if len(model_elements)!=len(figures):errors.append(['element_count',i])
 for j,actual in enumerate(model_elements):
  src=figures[j]
  if json.loads(actual['from_json'])!=src['from'] or json.loads(actual['to_json'])!=src['to'] or json.loads(actual['rotation_json'])!=src.get('rotation'):
   errors.append(['element_coordinates_or_rotation',i,j])
 if figures:
  lows=[min(x['from'][k] for x in figures) for k in range(3)]
  highs=[max(x['to'][k] for x in figures) for k in range(3)]
  # The feature record uses extrema of both endpoints, retaining inverted coordinates.
  lows=[min(v for x in figures for v in (x['from'][k],x['to'][k])) for k in range(3)]
  highs=[max(v for x in figures for v in (x['from'][k],x['to'][k])) for k in range(3)]
  if json.loads(c['bbox_min_json'])!=lows or json.loads(c['bbox_max_json'])!=highs:errors.append(['bbox',i])
for x in png:
 raw=(R/x['png_path']).read_bytes()
 if hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()!=x['png_sha']:errors.append(['PNG_sha',x['png_path']])
for row in vis:
 for path,expected in json.loads(row['F_original_PNG_paths_sha_json']):
  raw=(R/path).read_bytes()
  if hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()!=expected:errors.append(['model_PNG_link',row['model_path'],path])
for x in ch:
 raw=(R/x['blockstate_path']).read_bytes()
 if hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()!=x['blockstate_sha']:errors.append(['blockstate_sha',x['blockstate_path']])
 rawj=json.loads(raw)
 if x['rule_kind']=='VARIANTS':
  rule=list(rawj['variants'].items())[int(x['rule_index'])]
  condition,opts=rule; opts=opts if isinstance(opts,list) else [opts]
 else:
  part=rawj['multipart'][int(x['rule_index'])]
  condition=json.dumps(part.get('when',{}),ensure_ascii=False,separators=(',',':'));opts=part['apply'];opts=opts if isinstance(opts,list) else [opts]
 option=opts[int(x['alternative_index'])]
 if condition!=x['condition'] or len(opts)!=int(x['alternative_count']) or not x['model_path'].endswith('/'+option['model'].split(':')[-1]+'.json'):
  errors.append(['D_original_rule',x['blockstate_path'],x['rule_index']])
 for key in ('x','y','uvlock','weight'):
  if str(key in option)!=x[key+'_present'] or (key in option and str(option[key])!=x[key]):errors.append(['D_key',x['blockstate_path'],x['rule_index'],key])
assert len(q)==494 and len(sources)==len(g)==len(ass)==len(styles)==494
summary={'queue':494,'identity_sha_and_parent_independent':494-len(errors),'geometry_face_count':total,'element_rows':len(els),'D_direct':sum(x['D_direct_selected']=='YES' for x in ass),'D_original_choices':len(ch),'PNG_first_frames_visually_observed':len(png),'model_with_linked_PNG':sum(bool(json.loads(v['F_original_PNG_paths_sha_json'])) for v in vis),'model_without_bound_PNG':sum(not json.loads(v['F_original_PNG_paths_sha_json']) for v in vis),'prior_C_face_sum':sum(int(x['C_geometry_faces_prior']) for x in q),'errors':errors,'entry4_source_style_status':'PASS' if not errors else 'FAIL','full_F_models_after_entry4':1633 if not errors else 1139,'F_complete':False,'runtime_renderer_authenticated':False}
(O/'F_ENTRY4_INDEPENDENT_AUDIT.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(summary)
