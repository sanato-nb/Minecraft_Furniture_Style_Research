# -*- coding: utf-8 -*-
"""Stage-1 vanilla 3D study v6. Derived observations, not game assets.

Source: direct reads via connected GitHub from
 InventivetalentDev/minecraft-assets, ref=1.21.11 (2026-11-11).
Prior study v5 copied and extended. UV rows manually transcribed from fetched
model JSON; no claim of complete UV coverage is made.
"""
import csv, json, sqlite3, shutil, zipfile, hashlib, math, pathlib, collections, datetime
ROOT=pathlib.Path('/mnt/data/MC_vanilla_models_study_06')
OUT=ROOT/'results'; OUT.mkdir(parents=True,exist_ok=True)
PRIOR=pathlib.Path('/mnt/data/MC_vanilla_models_study_05/results/MC_Furniture_Style_Stage1_Research_v5.sqlite')
DB=OUT/'MC_Furniture_Style_Stage1_Research_v6.sqlite'
shutil.copy2(PRIOR,DB)
conn=sqlite3.connect(DB)
repo='https://github.com/InventivetalentDev/minecraft-assets/blob/1.21.11/assets/minecraft'

# New model files directly fetched from GitHub. Element counts are in source JSON
# or inherited through the named parent. Partial dimensions deliberately not extrapolated.
models_new=[
 ('cauldron',None,13,'788da3e1449187f15d820c0172f33b80f39620ca','direct','empty vessel with side walls, bottom and feet'),
 ('grindstone','block',5,'cc5e0f1f985fb58e381d8b2dd8c9fc1b8aef1532','direct','stone body and two paired supports'),
 ('stonecutter','block',2,'b89f0aaa1647332191fd685fd55633dbc8a879cb','direct','base plus zero-depth saw face'),
 ('lantern','template_lantern',4,'12970adc81a3bd51666060e8312b7ef4cf476930','inherited','crossed, rotated decorative planes'),
 ('lantern_hanging','template_hanging_lantern',4,'d047dcd004fa2d3bb374ae2c7f490587456b42b1','inherited','hanging variant'),
 ('end_rod','block',2,'aeb57d0b7929e2df4e2c2b47dc0ce571fd53de97','direct','slender light rod'),
 ('torch','template_torch',1,'7c6241d04d44dbaffcc87592470cbff2f82c0c8c','inherited','small upright flame support'),
 ('hopper',None,7,'ce9eb542c6ee3bd0a449183048fa5b6c090af550','direct','open container and downward spout'),
 ('hopper_side',None,7,'28d3dc65b758afdaf9eed61ba964b6575c5e8c8e','direct','open container and sideways spout'),
 ('template_lantern','block',4,'d54baf8db9aa52c0d828cb6047ea5aec21b8b341','direct','two cuboids plus two rotated planes'),
 ('template_hanging_lantern','block',4,'fb7ebb4d64e33bc0ab18aa568e273987a7c1cc9b','direct','hanging lantern cuboids/planes'),
 ('template_torch',None,1,'21ed11386517038d77683dcbec4f150e339d84c1','direct','2x10x2 cuboid'),
 ('oak_shelf_unpowered','template_shelf_unpowered',1,'0d536cc45ac2bc311ff1b1fc44651dbc43492c47','inherited','one state-dependent shelf face'),
]
states_new=[
 ('cauldron','variants',1,'9908cf5d4d631592e48fd436d4b90b3447fe3976'),
 ('grindstone','variants',12,'244481d0a87030158eccc80a2b6d37df6a8671b4'),
 ('stonecutter','variants',4,'c50b85fc73ee41725164b4226f858fb4300ef324'),
 ('lantern','variants',2,'00cb4380c57005b299665f3f78dfc1373d26cb51'),
 ('end_rod','variants',6,'0119a1a244b277aac6a27f75d92475828218b84d'),
 ('torch','variants',1,'7d14911ac2f30b0157e709a3d8cedecf253a032d'),
 ('hopper','variants',5,'be15ea37fe30021ad8356254154c912d436250ee'),
]
conn.executescript('''
CREATE TABLE IF NOT EXISTS model_additions_v6 (
 name TEXT PRIMARY KEY,parent TEXT,element_count INTEGER,sha1 TEXT,geometry_kind TEXT,source_url TEXT,evidence_note TEXT
);
CREATE TABLE IF NOT EXISTS state_additions_v6 (
 name TEXT PRIMARY KEY,state_mode TEXT,entry_count INTEGER,sha1 TEXT,source_url TEXT
);
CREATE TABLE IF NOT EXISTS uv_faces_v6 (
 source_geometry_model TEXT NOT NULL,element_index INTEGER NOT NULL,face TEXT NOT NULL,
 uv_json TEXT,texture_variable TEXT NOT NULL,face_rotation INTEGER NOT NULL DEFAULT 0,
 cullface TEXT,source_url TEXT NOT NULL,verification TEXT NOT NULL,
 PRIMARY KEY(source_geometry_model,element_index,face)
);
CREATE TABLE IF NOT EXISTS state_examples_v6 (
 block TEXT NOT NULL,state_key TEXT NOT NULL,selected_model TEXT NOT NULL,
 rotation_x INTEGER, rotation_y INTEGER, uvlock INTEGER, selection_kind TEXT NOT NULL,
 condition TEXT,source_url TEXT NOT NULL,
 PRIMARY KEY(block,state_key,selected_model,selection_kind)
);
CREATE TABLE IF NOT EXISTS research_issues_v6 (
 issue_id TEXT PRIMARY KEY, subject TEXT, status TEXT, notes TEXT
);
''')
for n,p,num,sha,kind,note in models_new:
 conn.execute('INSERT OR REPLACE INTO model_additions_v6 VALUES (?,?,?,?,?,?,?)',
  (n,p,num,sha,kind,repo+'/models/block/'+n+'.json',note))
 conn.execute('INSERT OR REPLACE INTO sources (path,github_blob_sha1,source_url,source_type,read_status) VALUES(?,?,?,?,?)',
  ('assets/minecraft/models/block/'+n+'.json',sha,repo+'/models/block/'+n+'.json','model','GitHub_connector_read_2026-11-11'))
for n,mode,count,sha in states_new:
 conn.execute('INSERT OR REPLACE INTO state_additions_v6 VALUES(?,?,?,?,?)',
  (n,mode,count,sha,repo+'/blockstates/'+n+'.json'))
 conn.execute('INSERT OR REPLACE INTO sources (path,github_blob_sha1,source_url,source_type,read_status) VALUES(?,?,?,?,?)',
  ('assets/minecraft/blockstates/'+n+'.json',sha,repo+'/blockstates/'+n+'.json','blockstate','GitHub_connector_read_2026-11-11'))

# Face evidence rows: all values below were directly checked against the 1.21.11
# GitHub connector source output, with 0-based element indexes.
# Compact format: face, uv (or None), #texture variable, rotation, cullface
S={}
def add(src,i, entries):
 S[(src,i)]=entries
# Blank UV means implicit calculated UV from geometry by Minecraft's model loader.
add('cube',0,[('down',None,'#down',0,'down'),('up',None,'#up',0,'up'),('north',None,'#north',0,'north'),('south',None,'#south',0,'south'),('west',None,'#west',0,'west'),('east',None,'#east',0,'east')])
add('stairs',0,[('down',[0,0,16,16],'#bottom',0,'down'),('up',[0,0,16,16],'#top',0,None),('north',[0,8,16,16],'#side',0,'north'),('south',[0,8,16,16],'#side',0,'south'),('west',[0,8,16,16],'#side',0,'west'),('east',[0,8,16,16],'#side',0,'east')])
add('stairs',1,[('up',[8,0,16,16],'#top',0,'up'),('north',[0,0,8,8],'#side',0,'north'),('south',[8,0,16,8],'#side',0,'south'),('west',[0,0,16,8],'#side',0,None),('east',[0,0,16,8],'#side',0,'east')])
add('inner_stairs',2,[('up',[0,8,8,16],'#top',0,'up'),('north',[8,0,16,8],'#side',0,None),('south',[0,0,8,8],'#side',0,'south'),('west',[8,0,16,8],'#side',0,'west')])
add('fence_side',0,[('down',[7,0,9,9],'#texture',0,None),('up',[7,0,9,9],'#texture',0,None),('north',[7,1,9,4],'#texture',0,'north'),('west',[0,1,9,4],'#texture',0,None),('east',[0,1,9,4],'#texture',0,None)])
add('fence_side',1,[('down',[7,0,9,9],'#texture',0,None),('up',[7,0,9,9],'#texture',0,None),('north',[7,7,9,10],'#texture',0,'north'),('west',[0,7,9,10],'#texture',0,None),('east',[0,7,9,10],'#texture',0,None)])
add('template_trapdoor_bottom',0,[('down',[0,0,16,16],'#texture',0,'down'),('up',[0,0,16,16],'#texture',0,None),('north',[0,16,16,13],'#texture',0,'north'),('south',[0,16,16,13],'#texture',0,'south'),('west',[0,16,16,13],'#texture',0,'west'),('east',[0,16,16,13],'#texture',0,'east')])
add('door_bottom_left',0,[('down',[16,13,0,16],'#bottom',90,'down'),('north',[3,0,0,16],'#bottom',0,'north'),('south',[0,0,3,16],'#bottom',0,'south'),('west',[0,0,16,16],'#bottom',0,'west'),('east',[16,0,0,16],'#bottom',0,None)])
add('template_shelf_body',0,[('east',[8,0,9.5,8],'#all',0,'east'),('south',[8,0,16,8],'#all',0,'south'),('west',[14.5,0,16,8],'#all',0,'west'),('up',[16,5,8,3.5],'#all',0,'up'),('down',[16,6,8,4.5],'#all',0,'down')])
add('template_shelf_body',1,[('north',[0,6,8,8],'#all',0,None),('east',[1.5,6,2.5,8],'#all',0,'east'),('west',[5.5,6,6.5,8],'#all',0,'west'),('up',[8,3.5,16,4.5],'#all',0,None),('down',[16,4.5,8,3.5],'#all',0,'down')])
add('template_shelf_body',2,[('north',[0,0,8,2],'#all',0,None),('east',[1.5,0,2.5,2],'#all',0,'east'),('west',[5.5,0,6.5,2],'#all',0,'west'),('up',[16,6,8,5],'#all',0,'up'),('down',[8,5,16,6],'#all',0,None)])
add('lectern',0,[('north',[0,14,16,16],'#base',0,'north'),('east',[0,6,16,8],'#base',0,'east'),('south',[0,6,16,8],'#base',0,'south'),('west',[0,6,16,8],'#base',0,'west'),('up',[0,0,16,16],'#base',180,None),('down',[0,0,16,16],'#bottom',0,'down')])
add('lectern',1,[('north',[0,0,8,13],'#front',0,None),('east',[2,16,15,8],'#sides',90,None),('south',[8,3,16,16],'#front',0,None),('west',[2,8,15,16],'#sides',90,None)])
add('lectern',2,[('north',[0,0,16,4],'#sides',0,None),('east',[0,4,13,8],'#sides',0,None),('south',[0,4,16,8],'#sides',0,None),('west',[0,4,13,8],'#sides',0,None),('up',[0,1,16,14],'#top',180,None),('down',[0,0,16,13],'#bottom',0,None)])
add('ladder',0,[('north',[0,0,16,16],'#texture',0,None),('south',[16,0,0,16],'#texture',0,None)])
add('flower_pot',4,[('down',[6,12,10,16],'#flowerpot',0,'down'),('up',[6,6,10,10],'#dirt',0,None)])
add('composter',0,[('up',None,'#inside',0,None),('down',None,'#bottom',0,'down')])
add('composter',1,[('up',None,'#top',0,'up'),('north',None,'#side',0,'north'),('south',None,'#side',0,'south'),('west',None,'#side',0,'west'),('east',None,'#side',0,None)])
add('template_anvil',3,[('down',[3,0,13,16],'#body',180,None),('up',[3,0,13,16],'#top',180,None),('north',[3,0,13,6],'#body',0,None),('south',[3,0,13,6],'#body',0,None),('west',[10,0,16,16],'#body',90,None),('east',[16,0,10,16],'#body',270,None)])

# Integrity: reject duplicate keys & invalid format. Each measurement references
# an already sourced geometry file from v5 and respects the element count.
source_sha={row[0].split('/')[-1][:-5]:row[1] for row in conn.execute("SELECT path,github_blob_sha1 FROM sources WHERE source_type='model'")}
model_counts={row[0]:row[1] for row in conn.execute('SELECT name,element_count FROM models')}
model_counts.update({n:num for n,p,num,sha,kind,note in models_new})
rows=[]
for (src,i),arr in S.items():
 assert src in source_sha and source_sha[src],src
 assert i>=0 and i<model_counts[src], (src,i)
 for face,uv,tex,rot,cull in arr:
  assert face in {'up','down','north','south','east','west'}
  assert uv is None or len(uv)==4
  assert rot in {0,90,180,270}
  assert tex.startswith('#')
  rows.append((src,i,face,json.dumps(uv),tex,rot,cull,repo+'/models/block/'+src+'.json','source_JSON_face_directly_read'))
conn.executemany('INSERT OR REPLACE INTO uv_faces_v6 VALUES(?,?,?,?,?,?,?,?,?)',rows)

# Selected exact blockstate examples. `condition` is the multipart `when` or a
# selected variants key. Distinct applications are not entire rendered states.
EX=[]
def ex(block,key,model,x=0,y=0,uv=False,mode='variants',condition=None):
 EX.append((block,key,model,x,y,int(uv),mode,condition,repo+'/blockstates/'+block+'.json'))
ex('oak_stairs','facing=east,half=bottom,shape=inner_left','oak_stairs_inner',0,270,True)
ex('oak_stairs','facing=east,half=bottom,shape=inner_right','oak_stairs_inner')
ex('oak_stairs','facing=east,half=bottom,shape=outer_left','oak_stairs_outer',0,270,True)
ex('oak_stairs','facing=east,half=bottom,shape=outer_right','oak_stairs_outer')
ex('oak_fence','always_post','oak_fence_post',mode='multipart',condition='always')
for cond,y in [('north',0),('east',90),('south',180),('west',270)]:
 ex('oak_fence','connection_'+cond,'oak_fence_side',0,y,True,mode='multipart',condition=cond+'=true')
ex('oak_slab','type=bottom','oak_slab')
ex('oak_slab','type=double','oak_planks')
ex('oak_slab','type=top','oak_slab_top')
ex('oak_trapdoor','facing=east,half=bottom,open=false','oak_trapdoor_bottom')
ex('oak_trapdoor','facing=east,half=bottom,open=true','oak_trapdoor_open',0,90)
ex('oak_door','facing=east,half=lower,hinge=left,open=false','oak_door_bottom_left')
ex('oak_door','facing=east,half=lower,hinge=left,open=true','oak_door_bottom_left_open',0,90)
ex('barrel','facing=down,open=false','barrel',180)
ex('barrel','facing=east,open=true','barrel_open',90,90)
for key,model,x,y in [('facing=down','end_rod',180,0),('facing=east','end_rod',90,90),('facing=north','end_rod',90,0),('facing=up','end_rod',0,0)]:
 ex('end_rod',key,model,x,y)
for key,model in [('hanging=false','lantern'),('hanging=true','lantern_hanging')]:ex('lantern',key,model)
for key,x,y in [('face=ceiling,facing=east',180,270),('face=floor,facing=north',0,0),('face=wall,facing=west',90,270)]:ex('grindstone',key,'grindstone',x,y)
for key,y in [('facing=east',90),('facing=north',0),('facing=south',180),('facing=west',270)]:ex('stonecutter',key,'stonecutter',0,y)
for key,model,y in [('facing=down','hopper',0),('facing=east','hopper_side',90),('facing=west','hopper_side',270)]:ex('hopper',key,model,0,y)
conn.executemany('INSERT OR REPLACE INTO state_examples_v6 VALUES(?,?,?,?,?,?,?,?,?)',EX)

issues=[
 ('I01','바닐라 텍스처 공식 client.jar 150건 해시 대조','pending','공식/로컬 client.jar 미제공. 비공식 1.21.11 미러만 확인됨'),
 ('I02','인게임 렌더 검수','pending','실제 Java 클라이언트/렌더 스크린샷을 통한 육안 대조 없음'),
 ('I03','02단계 전체 바닐라 모델 대표성','in_progress','실제 추출 모델 표본 분석이며 전체 바닐라 모델 전수조사가 아님'),
 ('I04','UV 전체 면 완전성','in_progress','uv_faces_v6는 선별 모델·면의 확인 기록임. 나머지 면은 미측정'),
 ('I05','부모모델 상속 텍스처 변수의 최종 PNG 해석','in_progress','부모 템플릿과 이름 있는 모델 조합 및 출력 PNG 연계를 일부 사례로 검증'),
 ('I06','특수 렌더 침대/상자/표지판','pending','기본 block model JSON은 particle-only; 엔티티/블록 엔티티 렌더를 별도 조사해야 함'),
 ('I07','가구 모드 비교 연구','not_started','03/04/05 작업은 아직 수행하지 않음'),
 ('I08','게임 버전 단일 기준','confirmed','비공식 추출 자산의 1.21.11 ref 고정; 공식 JAR 대조는 미완료'),
 ('I09','가구 규칙 확정','not_started','이번 1단계는 실측만; 2단계 규칙화는 별도 작업'),
]
conn.executemany('INSERT OR REPLACE INTO research_issues_v6 VALUES(?,?,?,?)',issues)
conn.commit()

# Produce additional useful joined database views of previous v5 data
conn.execute("""CREATE VIEW IF NOT EXISTS uv_audited_face_summary_v6 AS
 SELECT source_geometry_model, count(*) AS faces_recorded,
 count(DISTINCT element_index) AS elements_covered,
 sum(CASE WHEN uv_json='null' THEN 1 ELSE 0 END) AS implicit_uv_faces,
 count(DISTINCT texture_variable) AS texture_variables_used,
 sum(CASE WHEN face_rotation<>0 THEN 1 ELSE 0 END) AS rotated_face_uvs,
 sum(CASE WHEN cullface IS NOT NULL THEN 1 ELSE 0 END) AS culled_faces
 FROM uv_faces_v6 GROUP BY source_geometry_model""")
conn.execute("""CREATE VIEW IF NOT EXISTS all_model_inventory_v6 AS
 SELECT name,parent,element_count,geometry_status AS evidence_kind,source_url,'v5' AS batch
 FROM models UNION ALL SELECT name,parent,element_count,geometry_kind AS evidence_kind,source_url,'v6' AS batch
 FROM model_additions_v6""")
conn.execute("""CREATE VIEW IF NOT EXISTS all_blockstate_inventory_v6 AS
 SELECT name,type AS state_mode,variant_or_multipart_entry_count AS entry_count,source_url,'v5' AS batch
 FROM blockstates UNION ALL SELECT name,state_mode,entry_count,source_url,'v6' AS batch
 FROM state_additions_v6""")
conn.commit()

def writecsv(name,headers,data):
 with (OUT/name).open('w',newline='',encoding='utf-8-sig') as f:
  w=csv.writer(f);w.writerow(headers);w.writerows(data)
writecsv('01_v6_신규모델13개.csv',['name','parent','element_count','sha1','geometry_kind','source_url','evidence_note'],list(conn.execute('SELECT * FROM model_additions_v6 ORDER BY name')))
writecsv('02_v6_신규블록상태7개.csv',['name','state_mode','entry_count','sha1','source_url'],list(conn.execute('SELECT * FROM state_additions_v6 ORDER BY name')))
writecsv('03_v6_UV면별_실측.csv',['geometry_model','element_index','face','uv_json','texture_variable','face_rotation','cullface','source_url','verification'],list(conn.execute('SELECT * FROM uv_faces_v6 ORDER BY source_geometry_model,element_index,face')))
writecsv('04_v6_UV모델별_요약.csv',['geometry_model','faces_recorded','elements_covered','implicit_uv_faces','texture_variables_used','rotated_face_uvs','culled_faces'],list(conn.execute('SELECT * FROM uv_audited_face_summary_v6 ORDER BY source_geometry_model')))
writecsv('05_v6_블록상태_실제예시.csv',['block','state_key','selected_model','rotation_x','rotation_y','uvlock','selection_kind','condition','source_url'],list(conn.execute('SELECT * FROM state_examples_v6 ORDER BY block,state_key')))
writecsv('06_v6_검증보류항목.csv',['issue_id','subject','status','notes'],list(conn.execute('SELECT * FROM research_issues_v6 ORDER BY issue_id')))
writecsv('10_v6_누적_출처원장91.csv',['path','github_blob_sha1','source_url','source_type','read_status'],list(conn.execute('SELECT * FROM sources ORDER BY source_type,path')))
writecsv('11_v6_누적_모델목록68.csv',['model_name','parent','element_count','evidence_kind','source_url','batch'],list(conn.execute('SELECT * FROM all_model_inventory_v6 ORDER BY name')))
writecsv('12_v6_누적_상태목록23.csv',['name','state_mode','entry_count','source_url','batch'],list(conn.execute('SELECT * FROM all_blockstate_inventory_v6 ORDER BY name')))
counts={
 'previous_v5_sources':71,
 'v6_new_model_sources':len(models_new),
 'v6_new_state_sources':len(states_new),
 'cumulative_source_files':conn.execute('SELECT count(*) FROM sources').fetchone()[0],
 'v5_model_files':55,
 'v6_new_model_files':len(models_new),
 'cumulative_model_files':55+len(models_new),
 'v5_blockstate_files':16,
 'v6_new_blockstate_files':len(states_new),
 'cumulative_blockstate_files':16+len(states_new),
 'uv_sample_faces':conn.execute('SELECT count(*) FROM uv_faces_v6').fetchone()[0],
 'uv_sample_geometry_files':conn.execute('SELECT count(DISTINCT source_geometry_model) FROM uv_faces_v6').fetchone()[0],
 'uv_elements_covered':conn.execute('SELECT count(DISTINCT source_geometry_model||":"||element_index) FROM uv_faces_v6').fetchone()[0],
 'state_examples':conn.execute('SELECT count(*) FROM state_examples_v6').fetchone()[0],
 'texture_stats':conn.execute('SELECT count(*) FROM texture_stats_v4').fetchone()[0],
 'v5_geometry_element_rows':conn.execute('SELECT count(*) FROM elements').fetchone()[0]
}
assert counts['cumulative_source_files']==71+len(models_new)+len(states_new),counts
assert counts['uv_sample_faces']==len(rows)
assert counts['cumulative_model_files']==55+len(models_new)
assert counts['texture_stats']==150
assert conn.execute('PRAGMA integrity_check').fetchone()[0]=='ok'

# JSON for machine parsing and future continuation.
(OUT/'07_v6_검증및진행현황.json').write_text(json.dumps({
 'project':'Minecraft Furniture Style Study', 'edition':'Java 1.21.11',
 'research_scope':'stage1, vanilla 3D UV/structure; NOT PZ conversion',
 'counts':counts,
 'percent':{'vanilla_texture_sample':100,'stage02_overall':None,'stage1_total':None},
 'statuses':{'01_vanilla_texture':'sample_complete_official_jar_and_ingame_pending',
             '02_vanilla_3d':'in_progress',
             '03_mod_3d':'not_started',
             '04_mod_uv':'not_started',
             '05_comparison':'not_started'},
 'evidence_source':'GitHub connector direct read of public nonofficial extracted assets at tag 1.21.11',
 'independent_official_client_jar_verified':False,
 'ingame_screen_verified':False,
 'no_original_game_assets_bundled':True
},ensure_ascii=False,indent=2),encoding='utf-8')

# Quantitative demonstration of UV-to-PNG pixel conversion from an actual model:
# UV units are normalized to a 0..16 scale over image width/height (32x32 shelf).
# E.g. shelf north [0,6,8,8] -> pixel rectangle [0,12,16,16].
shelf_uv_pixel=[]
for (model,i),faces in S.items():
 if model!='template_shelf_body':continue
 for face,uv,tex,rot,cull in faces:
  if uv is None:continue
  shelf_uv_pixel.append([i,face,*uv,*[v*2 for v in uv],tex])
writecsv('08_v6_선반32px_UV픽셀대응.csv',
 ['element','face','u0_uv','v0_uv','u1_uv','v1_uv','u0_pngpx','v0_pngpx','u1_pngpx','v1_pngpx','texture_variable'],shelf_uv_pixel)

# Meaningful research note; do not mislabel the subset as full coverage.
report=f'''# 마인크래프트 바닐라 3D 학습 — v6 UV·상태별 구성 확장 분석

- 기준 게임: **Java Edition 1.21.11**
- 원본: [InventivetalentDev/minecraft-assets 1.21.11](https://github.com/InventivetalentDev/minecraft-assets/tree/1.21.11/assets/minecraft), 비공식 추출 에셋
- 범위: **학습 1단계 중 02 바닐라 3D 모델 구조 분석**. 좀보이드 가구 제작/규칙서 확정은 수행하지 않음.
- 데이터 상태: 연결된 GitHub에서 JSON을 직접 읽은 파생 수치. **공식 Mojang client.jar 해시 검증과 실제 게임 화면 검증은 미완료**.

## 1. 계승 및 신규 성과

| 근거 유형 | v5 | 이번 신규 | v6 누적 |
|---|---:|---:|---:|
| 실제 열람한 모델 JSON | 55 | {len(models_new)} | {55+len(models_new)} |
| 실제 열람한 블록 상태 JSON | 16 | {len(states_new)} | {16+len(states_new)} |
| 원본 경로·SHA 원장 총계 | 71 | {len(models_new)+len(states_new)} | {counts['cumulative_source_files']} |
| 텍스처 측정 기록 | 150 | 0 | 150 (v4 계승) |

이번 추가 결과는 UV 좌표를 **{counts['uv_sample_geometry_files']}개 기하구조 모델의 {counts['uv_elements_covered']}개 요소, {counts['uv_sample_faces']}개 면**에서 추출했고, **{counts['state_examples']}개의 상태 적용 예시**를 별도 기록했다. UV는 바닐라 전체 면 전수조사가 아니고 표본이다.

## 2. 3D와 UV의 역할 분리 — 원본에서 관찰한 사례

| 구조 | 원본에서 확인한 사실 | 관련 파일 |
|---|---|---|
| 정육면체 | `cube`는 부피 16×16×16, 6면의 `uv` 값을 생략하고 면별 텍스처 변수 사용 | `models/block/cube.json` |
| 계단 | `stairs`는 2개 직육면체, 정면 상·하 UV가 분리되어 서로 다른 범위를 사용 | `models/block/stairs.json` |
| 다락문 | `template_trapdoor_bottom`는 16×3×16, 상면 UV 16×16 범위와 측면 UV 16×3 범위를 별도 적용 | `models/block/template_trapdoor_bottom.json` |
| 선반 | `template_shelf_body`는 3개 요소, 같은 `#all` 텍스처를 15개 면별로 다른 UV 범위에 배치 | `models/block/template_shelf_body.json` |
| 독서대 | `lectern`은 3개 요소, 상단 로컬 회전 −22.5°, 일부 면 UV 회전 90°/180° | `models/block/lectern.json` |
| 사다리 | `ladder`는 Z=15.2의 0-두께 양면, 반대쪽 UV 가로 방향이 뒤집혀 있음 | `models/block/ladder.json` |
| 모루 | `template_anvil`는 상부 요소 `#top`, 측면은 `#body` 사용. 일부 면은 UV 90/270° 회전 | `models/block/template_anvil.json` |
| 화분 | 내부 바닥은 `#dirt`, 외부 테두리는 `#flowerpot`: 재질을 부품/면별 구분 | `models/block/flower_pot.json` |

**핵심 구분:** `element.rotation`은 3D 요소의 공간 회전, `faces[].rotation`은 텍스처 면의 UV 회전, `blockstates`의 `x`/`y`는 모델 배치 방향을 바꾼다. 이 셋은 서로 다른 값이므로 같은 열로 합치면 안 된다.

### 2.1 실제 32×32 PNG와 UV 좌표

v4에서 `oak_shelf.png`를 **32×32**로 측정했으며, v5에서 `oak_shelf`가 `template_shelf_body`를 상속하고 `#all`에 해당 PNG를 지정함을 확인했다. 일반 모델 UV는 0..16 좌표 척도를 사용하므로 **해당 32×32 이미지에서 UV 1단위는 이미지 2픽셀**에 해당한다. 예를 들어:

- 선반 `element 1`의 `north` UV `[0,6,8,8]` → PNG 상 픽셀 영역 `[0,12,16,16]`.
- 선반 `element 2`의 `north` UV `[0,0,8,2]` → `[0,0,16,4]`.
- UV가 역방향인 `[16,5,8,3.5]`도 오류로 취급하지 않고 방향 반전 정보 그대로 저장.

`08_v6_선반32px_UV픽셀대응.csv`에 선반 15면의 좌표를 추적했다. 좌표만으로 실제 게임 광원·색감·투명 렌더를 검증했다고 주장하지 않는다.

## 3. 바닐라의 형태 구성 확장

- 가마솥 `cauldron`: **13개 요소**, 테두리/바닥/발을 분리한 고부품 사례.
- 숫돌 `grindstone`: **5개 요소**, 지지대와 중앙 연마부를 분리.
- 석재 절단기 `stonecutter`: **2개 요소**이고 날 부분은 `from=[1,9,8]`, `to=[15,16,8]`로 두께 0인 양면 패널.
- 랜턴 `lantern`: `template_lantern`을 상속해 **4개 요소**, 중앙을 교차하는 장식용 평면은 Y축 45° 회전.
- 매달린 랜턴 `lantern_hanging`: 별도 부모 모델 `template_hanging_lantern`의 **4개 요소**.
- 깔때기 `hopper` / `hopper_side`: **각 7개 요소**, 출구 방향에 따라 다른 기하구조.
- 엔드 막대 `end_rod`: **2개 요소**, 방향은 상태 JSON에서 변경.
- 횃불 `torch`: `template_torch`를 상속한 **1개 요소**.

이 수치는 모델 JSON의 개별 `elements` 요소 개수이며, 일반화된 권장 큐브 개수가 아니다. 형태가 빈 원통처럼 보여도 실제로는 직육면체 벽을 나눠 놓을 수 있다.

## 4. 상태별 조립 예시

`blockstates`에는 단일 모델 `variants`와 여러 부품을 조건에 따라 겹쳐 쓰는 `multipart`가 존재한다. 이를 구분한 실측 예시는 `05_v6_블록상태_실제예시.csv`에 {counts['state_examples']}건 포함한다.

| 사례 | 확인된 조건 | 동작 |
|---|---|---|
| 계단 | `facing=east,half=bottom,shape=inner_left` | `oak_stairs_inner` + Y축 270°, `uvlock=true` |
| 울타리 | 항상 기둥 / `east=true` | 기둥 기본 + `oak_fence_side` 90° 회전 |
| 반 블록 | `type=double` | 반 블록 2개를 겹치는 게 아니라 전체 `oak_planks` 모델 선택 |
| 랜턴 | `hanging=false/true` | 일반/매달림 모델 선택 |
| 숫돌 | `face=ceiling,facing=east` | X축 180°, Y축 270° |
| 깔때기 | `facing=east` | `hopper_side` 모델 + Y축 90° |

`variant_or_multipart_entry_count`는 **JSON 항목의 수**이지 항상 독립 3D 모델의 수나 게임 내 유효 상태 전체 수는 아니다.

## 5. 연구를 완료로 처리하지 않은 근거

- **01 텍스처:** 150/150 표본 실측 완료. 공식 게임 `client.jar`와 해시 대조 **0/150**, 인게임 화면 직접 검증 **미실시**.
- **02 바닐라 3D:** {counts['cumulative_model_files']}개 모델 파일, {counts['cumulative_blockstate_files']}개 상태 파일, 선택된 {counts['uv_sample_faces']}면 UV 확인. 하지만 모델 전체 카탈로그·전체 면 UV·복합 상태 완성 모델 렌더 검증은 미완료.
- **03/04/05 모드·비교:** 아직 시작하지 않음.
- **특수 렌더:** 상자·침대·표지판은 보통의 JSON 직육면체 합계로 게임 외관을 판단할 수 없어 미확인 유지.

따라서 **1단계 전체 완료 0/5개, 진행 중 2/5개**다. 02 단계는 표본 목표 분모를 정하지 않았으므로 부정확한 퍼센트를 제시하지 않는다.

## 6. 다음 권장 분석

1. 대상 블록 상태에서 조건부 `multipart`를 실제로 평가해 최종 구성 요소 목록 만들기.
2. 3D 요소 회전과 면 UV 반전·회전을 동시에 계산해 케이스별 구조 검증.
3. 남은 대표 형태(벽, 연속형 블록, 투명 블록, 특수 렌더)의 원본 조사 확대.
4. 02가 충분히 쌓이면 03 가구 모드 공개 모델 구조 분석으로 이동.

**증거 파일:** `01~06 CSV`, `08 선반 UV-픽셀 대응 CSV`, `MC_Furniture_Style_Stage1_Research_v6.sqlite`, `07 검증및진행현황.json`. **게임 원본 에셋은 이 패키지에 포함하지 않음.**
'''
(OUT/'00_v6_UV상태별_확장분석보고서.md').write_text(report,encoding='utf-8')

progress=f'''# 학습 1단계 진행도 — v6 (2026-11-11)

| 세부 단계 | 상태 | 근거 수치 | 남은 작업 |
|---|---|---|---|
| 01 바닐라 재질·텍스처 | 표본 목표 달성 / 최종 검증 보류 | 150/150 텍스처 기록 (100% 표본) | 공식 JAR 대조 0/150, 인게임 확인 |
| 02 바닐라 3D 모델·상태 | 진행 중 | 모델 파일 {counts['cumulative_model_files']}, 상태 파일 {counts['cumulative_blockstate_files']}, UV 면 {counts['uv_sample_faces']}건 | 전수성/렌더/특수렌더 검증 |
| 03 가구 모드 3D | 미시작 | 0 | 모드 에셋 확보 |
| 04 가구 모드 텍스처·UV | 미시작 | 0 | 모드 UV 측정 |
| 05 바닐라·모드 비교 | 미시작 | 0 | 공통 축 비교 |

**확정 완료: 0/5개 · 진행 중: 2/5개 · 미시작: 3/5개.**

참고: 02의 파일/UV 면 개수는 **분석된 근거 개수**이지 02의 전체 작업 중 퍼센트가 아니다. 01 표본 100%는 공식 및 인게임 검증 완료를 뜻하지 않는다.
'''
(OUT/'09_v6_학습_진행도.md').write_text(progress,encoding='utf-8')

readme='''# Minecraft Vanilla Stage1 Research v6

Data-only research pack for Minecraft Java 1.21.11. Prior v5 SQLite carried over.
No original Mojang PNG / model JSON files included. Source URLs / Git Blob hashes
recorded in SQLite and CSV. The companion build_v6.py can rebuild from v5 database.

Major files: 00 report; 01/02 new models/states; 03/04 UV sample; 05 state
examples; 06 pending issues; 07 JSON progress; 08 shelf UV pixel coordinates;
09 MD progress; SQLite DB.

Important: UV only covers a selected set of faces and does not equal 3D render validation.
'''
(OUT/'README.md').write_text(readme,encoding='utf-8')
conn.close()
# Syntax test, database consistency, zip CRC
with sqlite3.connect(DB) as con:
 assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
 assert con.execute('SELECT count(*) FROM sources').fetchone()[0]==counts['cumulative_source_files']
 assert con.execute('SELECT count(*) FROM uv_faces_v6').fetchone()[0]==counts['uv_sample_faces']
 assert con.execute('SELECT count(*) FROM state_examples_v6').fetchone()[0]==counts['state_examples']
 assert con.execute('SELECT count(*) FROM texture_stats_v4').fetchone()[0]==150
 assert con.execute('SELECT count(*) FROM all_model_inventory_v6').fetchone()[0]==68
 assert con.execute('SELECT count(*) FROM all_blockstate_inventory_v6').fetchone()[0]==23

zip_path=pathlib.Path('/mnt/data/마크_가구모델링_바닐라3D분석_v6_UV상태_확장.zip')
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for p in sorted(OUT.iterdir()):
  if p.is_file():z.write(p,arcname='MC_vanilla_models_study_06/results/'+p.name)
with zipfile.ZipFile(zip_path) as z: assert z.testzip() is None
print(json.dumps({'counts':counts,'zip':str(zip_path),'zip_bytes':zip_path.stat().st_size,'DB':str(DB),'report':str(OUT/'00_v6_UV상태별_확장분석보고서.md')},ensure_ascii=False,indent=2))
