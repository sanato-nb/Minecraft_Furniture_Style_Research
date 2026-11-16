"""Reviewed source first-frame visual evidence and furniture-transfer hypotheses for F2."""
import csv,json,collections
from pathlib import Path
R=Path(__file__).resolve().parents[1];B=R/'research/vanilla_models/phase_1-2-F/entry2'
def read(p):
 with (B/p).open(newline='') as f:return list(csv.DictReader(f))
def write(p,a):
 with (B/p).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(a[0]),lineterminator='\n');w.writeheader();w.writerows(a)
models=read('F_MODEL_SOURCE_STATUS.csv');pngs=read('F_TEXTURE_VISUAL_EVIDENCE.csv');assert len(models)==494 and len(pngs)==303
manual={
 'barrel_top_open':'갈색 테두리 안에 어두운 원형 영역이 보인다. 실제 입체 구멍은 이 이미지만으로 입증되지 않는다.',
 'bookshelf':'갈색 가로 칸 사이에 여러 색 책등처럼 보이는 작은 픽셀 무늬가 있다. 선반의 실제 깊이는 이미지로 알 수 없다.',
 'chiseled_bookshelf_empty':'갈색 가로 구획과 어두운 칸처럼 보이는 픽셀이 있다. 빈 입체 공간인지는 기하에서 따로 판단한다.',
 'crafting_table_front':'갈색 프레임 안에 작은 사각·격자 모양 픽셀이 보인다. 원본 큐브 면의 그래픽 디테일이다.',
 'cartography_table_top':'갈색 바탕에 둥근 선과 밝은 작은 사각 픽셀이 보인다. 실물 기능은 추정하지 않는다.',
 'cauldron_top':'어두운 테두리와 가운데 투명한 정방형 구멍 픽셀이 보인다. 실제 벽·바닥 부피는 모델 요소를 따로 확인한다.',
 'flower_pot':'갈색 테두리와 밝은 빈 중앙 픽셀이 보인다. 입체 깊이는 5요소 원본에서 따로 확인한다.',
 'furnace_front_on':'어두운 사각 틀 안에 밝은 주황·노랑 픽셀이 보인다. 실제 발광/상태는 엔진 미검증이다.',
 'lectern_front':'갈색 면의 일부에 작은 다색 픽셀 무늬가 보인다. 기울어진 상판은 별도 원본 요소의 회전에서 확인한다.',
 'loom_front':'세로선과 가로 띠가 반복된 픽셀 무늬가 보인다. 그 선들이 입체 기둥이라는 근거는 아니다.',
 'piston_side':'회색 프레임과 밝은 갈색 부분이 분리된 픽셀이 보인다. 실제 돌출 구조는 요소에서 판단한다.',
 'acacia_shelf':'32×32 이미지에 여러 가로 칸과 세로 테두리 픽셀이 보인다. 3요소 상속 기하와 별도 근거.',
 'lava_still':'16×320 애니메이션 원본 첫 16×16 프레임에 주황·노란 불규칙 무늬가 보인다. 뒷 프레임 미시각 검토.',
 'water_still':'16×512 애니메이션 원본 첫 16×16 프레임에 연한 회색·반투명 무늬가 보인다. 뒷 프레임 미시각 검토.',
 'black_shulker_box':'어두운 불투명 면과 주변 경계 픽셀이 보인다. 실제 상자 표면/움직임은 E 런타임 미확인.'}
for i,r in enumerate(pngs):
 name=Path(r['png_path']).stem
 r['contact_sheet']=f'visual_contact/contact_{i//48+1:02d}.png';r['contact_index']=i
 r['F_visual_first_frame_observed']='YES'
 r['visual_note']=manual.get(name,'접촉 시트에서 원본 첫 정방 프레임의 픽셀 색·알파·무늬를 직접 확인했다. 재질·물리 형상·게임 렌더는 여기서 확정하지 않는다.')
 r['image_grade']='ORIGINAL_PNG_FIRST_FRAME_VISUALLY_OBSERVED_NOT_GAME_RENDER'
write('F_PNG_DIRECT_VISUAL_OBSERVATIONS.csv',pngs)
png={r['png_path']:r for r in pngs}
features=[];tex=[];assembly=[];style=[]
for r in models:
 p=r['model_path'];e=r['E_exception']=='True';paths=json.loads(r['source_PNG_paths_json']);first=png[paths[0]] if paths else None
 if paths:r['F_PNG_first_frame_observed']='YES_SOURCE_FIRST_FRAME'
 else:r['F_PNG_first_frame_observed']='NO_UNBOUND_TEMPLATE'
 r['F_status']='F_ENTRY2_SOURCE_STYLE_ACCEPTED_WITH_EXPLICIT_LIMITS'
 r['F_visual_source_note']=f'{paths[0]}@{first["png_sha"]}: {first["visual_note"]}' if first else '자기 모델에 바인딩된 PNG가 없어 시각적 외형을 보류한다.'
 r['F_furniture_transfer_grade']='MODELING_HYPOTHESIS_SEPARATE_FROM_SOURCE_FACT'
 r['F_structure_reason']=('일반 elements 부재. E 원본 particle 선언은 형상 근거가 아니다.' if e else f'원본 provider {r["geometry_provider_path"]} 요소 {r["element_count"]}개, bbox {r["bbox_extent_json"]}, 0두께 {r["zero_elements"]}, 회전 {r["rotated_elements"]}개의 소스 좌표를 확인.')
 r['F_visual_vs_geometry']='PARTICLE_ONLY_NOT_RENDER_SURFACE' if e else 'SOURCE_GEOMETRY_PLUS_FIRST_FRAME_TEXTURE_VISUAL_NO_RUNTIME' if paths else 'SOURCE_GEOMETRY_ONLY_UNBOUND_TEXTURE_TEMPLATE'
 r['F_D_assembly_evidence']='ORIGINAL_BLOCKSTATE_RULES_STATIC' if int(r['D_original_rule_choices']) else 'NOT_DIRECT_D_SELECTED_ROLE_UNDETERMINED'
 style.append(r)
 features.append({k:r[k] for k in ['model_path','model_sha','geometry_provider_path','geometry_provider_sha','element_count','face_count','UV_explicit','UV_key_absent','bbox_min_json','bbox_max_json','bbox_extent_json','axis_thickness_json','zero_elements','thin_elements','rotated_elements','inverted_elements','outside_elements','tags','primary_archetype']})
 tex.append({'model_path':p,'model_sha':r['model_sha'],'C_prior_binding_rows':r['C_prior_binding_rows'],'C_prior_face_rows':r['C_prior_face_rows'],'F_original_PNG_paths_json':json.dumps(paths),'F_PNG_unique_count':len(paths),'F_first_frame_direct_visual_observed':r['F_PNG_first_frame_observed'],'F_observed_first_PNG_note':r['F_visual_source_note'],'detail_vs_geometry':r['F_visual_vs_geometry'],'source_confidence':'SOURCE_FIRST_FRAME_OR_EXPLICIT_UNBOUND_LIMIT','runtime_renderer_verified':False})
 assembly.append({'model_path':p,'model_sha':r['model_sha'],'D_direct_selected':r['D_direct_selected'],'D_original_rule_choices':r['D_original_rule_choices'],'blockstate_paths_json':r['D_blockstate_paths_json'],'source_grade':r['F_D_assembly_evidence'],'in_game_state_registry_verified':False})
source_status=[{k:r[k] for k in ['model_path','model_sha','F_queue_index','priority','source_json_direct','parent_chain_json','geometry_provider_path','geometry_provider_sha','E_exception','F_PNG_first_frame_observed','D_direct_selected','F_status']} for r in models]
write('F_MODEL_SOURCE_STATUS.csv',source_status);write('STYLE_OBSERVATIONS.csv',style);write('F_GEOMETRY_FEATURES.csv',features);write('F_TEXTURE_VISUAL_EVIDENCE.csv',tex);write('F_ASSEMBLY_LINKS.csv',assembly)
rules={'schema':'F_ENTRY2_SOURCE_STYLE_ARCHETYPES/v1','sample':494,'multi_label_nonexclusive':True,'thresholds':{'THIN_ELEMENT':'any axis absolute thickness <=1 source coordinate','ZERO_THICKNESS':'any axis exact zero','EXACT_FULL_CUBE':'one unrotated [0,0,0] to [16,16,16] element'},
 'primary_counts':dict(collections.Counter(x['primary_archetype'] for x in style)),'source_visual_scope':{'unique_PNG_first_frames_directly_reviewed':len(pngs),'models_with_bound_source_PNG':sum(bool(json.loads(x['source_PNG_paths_json'])) for x in style),'unbound_templates':sum(not json.loads(x['source_PNG_paths_json']) for x in style),'animated_later_frames_reviewed':False,'game_runtime_render_verified':False},
 'representatives':[{'kind':'full cube with texture detail','model':'bookshelf.json','source_geometry':'one unrotated [0,0,0] to [16,16,16] inherited cube','source_image':'bookshelf.png first frame shows colored small stripes in horizontal compartments','transfer_hypothesis':'surface artwork can communicate stored-item detail without element-level books','limit':'texture pattern does not prove individual 3D books'},
 {'kind':'frame and cavity','model':'cauldron.json','source_geometry':'13 source elements create a rim/wall structure','source_image':'cauldron_top.png has transparent central square','transfer_hypothesis':'a basin-like open frame can be modeled from narrow walls and a separate bottom','limit':'no game liquid or collision verification'},
 {'kind':'shelf body and atlas','model':'acacia_shelf.json','source_geometry':'three inherited elements with depth 5','source_image':'acacia_shelf.png 32x32 shows compartment outlines','transfer_hypothesis':'small 3D projection plus drawn compartment divisions may simplify a shelf','limit':'visible interior and actual item storage not verified'},
 {'kind':'small container construction','model':'flower_pot.json','source_geometry':'five source elements bbox 6x6x6','source_image':'flower_pot.png has outlined center','transfer_hypothesis':'separate narrow rim and walls for small decorative container','limit':'not a claim about game planting behavior'},
 {'kind':'single block surface treatment','model':'crafting_table.json','source_geometry':'one inherited full cube','source_image':'crafting_table_front.png has frame and grid pixels','transfer_hypothesis':'cabinet facade graphics can live on a cube face','limit':'grid is not an actual modeled cavity'},
 {'kind':'rotated surface support','model':'lectern.json','source_geometry':'three elements including a rotated element','source_image':'lectern_front.png has small contrasting details','transfer_hypothesis':'one inclined panel supported by a small stem and base','limit':'does not establish furniture function'},
 {'kind':'source exception','model':'black_shulker_box.json','source_geometry':'no general elements in source chain','source_image':'particle PNG has dark field with boundary pixels','transfer_hypothesis':'palette reference only','limit':'actual E renderer surface unknown'}]}
(B/'F_ARCHETYPE_RULES.json').write_text(json.dumps(rules,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'models':len(style),'PNG':len(pngs),'with_visual':rules['source_visual_scope']['models_with_bound_source_PNG'],'unbound':rules['source_visual_scope']['unbound_templates'],'primary':rules['primary_counts']},ensure_ascii=False))
