# -*- coding: utf-8 -*-
"""Create source-grounded analysis files for the Minecraft Java 1.21.11 vanilla 3D study.

Input facts are extracted from GitHub-connected reads of the specified 1.21.11
assets. This script makes derived summaries; it does not bundle Mojang's files.
"""
import json, csv, sqlite3, hashlib, shutil, zipfile, os
from collections import Counter
from pathlib import Path
import pandas as pd

BASE=Path('/mnt/data/MC_vanilla_models_study_05')
OUT=BASE/'results'; OUT.mkdir(exist_ok=True)
PREV=Path('/mnt/data/MC_vanilla_textures_study_04/results')
GITHUB='https://github.com/InventivetalentDev/minecraft-assets/blob/1.21.11/assets/minecraft'
# Geometry is unrotated cuboid extents in model coordinates. Absence may mean inherited
# from parent, or a non-geometry placeholder; do not treat it as an empty in-game block.
A={}
def add(name,parent=None,boxes=None,sha='',kind='named',textures=None,rotation=None):
    assert name not in A,name
    A[name]={'name':name,'parent':parent,'boxes':boxes,'sha':sha,'kind':kind,'textures':textures or {},'rotation':rotation or {}}

# 32 independently-read named model definitions.
add('oak_planks','cube_all',sha='3a21a3f2e75848ac905b6819ceeb40d1dbb3b39c',textures={'all':'oak_planks'})
add('oak_slab','slab',sha='f11ff8bad0b9faa4b6d1ef65c9a75ff2681a162a',textures={'top':'oak_planks','bottom':'oak_planks','side':'oak_planks'})
add('oak_stairs','stairs',sha='d959a5f2894e4fd0821d06b36c049aaa30c129ef',textures={'top':'oak_planks','bottom':'oak_planks','side':'oak_planks'})
add('oak_fence_post','fence_post',sha='e05dc4ae309d60b31488d6fb9d3793bf495c92f5',textures={'texture':'oak_planks'})
add('oak_fence_side','fence_side',sha='fe4ed99e0deb7af04f3494469d0b65a753e5a80e',textures={'texture':'oak_planks'})
add('oak_trapdoor_bottom','template_trapdoor_bottom',sha='a4dcb639f352a8a966d78bcdb487db1e30d5ed0d',textures={'texture':'oak_trapdoor'})
add('oak_door_bottom_left','door_bottom_left',sha='9cd5e6b232790ba57f98bea60b608ad2b87a8a2c',textures={'bottom':'oak_door_bottom','top':'oak_door_top'})
add('oak_shelf','template_shelf_body',sha='4b0f3db311717ef740c50638ea1d252256310180',textures={'all':'oak_shelf','particle':'stripped_oak_log'})
add('bookshelf','cube_column',sha='c095a7d7ebf88c0a72dc9131b64e3b4f5963aad8',textures={'end':'oak_planks','side':'bookshelf'})
add('chiseled_bookshelf_empty_slot_top_left','template_chiseled_bookshelf_slot_top_left',sha='2b9817062fbc51325526c1fd4b72cd8aadb06a30',textures={'texture':'chiseled_bookshelf_empty'})
add('barrel','cube_bottom_top',sha='cff930084d47d226817f274616d14f4b07c0a9d4',textures={'bottom':'barrel_bottom','side':'barrel_side','top':'barrel_top'})
add('crafting_table','cube',sha='aa056b15efba47ef049e029b560029a6b1e3be84',textures={'down':'oak_planks','north':'crafting_table_front','up':'crafting_table_top','others':'crafting_table_side'})
add('smithing_table','cube',sha='f7bcd3e1f5f740089ded6cc3627b8018e8a55c83',textures={'down':'smithing_table_bottom','north':'smithing_table_front','up':'smithing_table_top','others':'smithing_table_side'})
add('lectern','block',boxes=[([0,0,0],[16,2,16]),([4,2,4],[12,15,12]),([0.0125,12,3],[15.9875,16,16])],sha='a504fa96bc3c5c729adaaa015d927b8250a1bd63',textures={'base':'lectern_base','front':'lectern_front','sides':'lectern_sides','top':'lectern_top','bottom':'oak_planks'},rotation={'2':{'axis':'x','angle':-22.5,'origin':[8,8,8]}})
add('anvil','template_anvil',sha='dc9d2555669a31984f3d0e221f778ca170d7f533',textures={'top':'anvil_top'})
add('composter','block',boxes=[([0,0,0],[16,2,16]),([0,0,0],[2,16,16]),([14,0,0],[16,16,16]),([2,0,0],[14,16,2]),([2,0,14],[14,16,16])],sha='9650f777a58fe668b42ad8ad6d57a643121f5202',textures={'side':'composter_side','bottom':'composter_bottom','top':'composter_top'})
add('oak_stairs_inner','inner_stairs',sha='2850cc5807525b601911009a3f7b458ac9069cfe')
add('oak_stairs_outer','outer_stairs',sha='78644acd4c29f06771661f1dfe668c41237a6196')
add('oak_slab_top','slab_top',sha='d7adec0ee079a22a08bdd9adf0d982a4978b82b2')
add('oak_trapdoor_open','template_trapdoor_open',sha='e8b0bb3b205bdfde6b611cf9ecb45039294bf840')
add('oak_trapdoor_top','template_trapdoor_top',sha='34322d68e4b4e28539684a36205ee69535527950')
add('barrel_open','cube_bottom_top',sha='c7d013e7b442624011ab4a0bef8b4e9ac5570ea9',textures={'top':'barrel_top_open'})
add('stone_button','button',sha='42d1cc4d82c32212a3210a5abb68aa9ace225152',textures={'texture':'stone'})
add('ladder',None,boxes=[([0,0,15.2],[16,16,15.2])],sha='1b975e4d8d0d5d8b763d7065e9b451d8fa437bb9',textures={'texture':'ladder'})
for n in ('bed','chest','oak_sign'):
    add(n,None,sha='9406a8491ed2532d4878b0a91b16a0e5f8d93d80',textures={'particle':'oak_planks'})
add('flower_pot',None,boxes=[([5,0,5],[6,6,11]),([10,0,5],[11,6,11]),([6,0,5],[10,6,6]),([6,0,10],[10,6,11]),([6,0,6],[10,4,10])],sha='45c7a75b1e69ce35bf3bc76d794e1a922deccf53',textures={'flowerpot':'flower_pot','dirt':'dirt'})
add('button',None,boxes=[([5,0,6],[11,2,10])],sha='b3dc8a56eefa7de473cbde2afc6523f94f34e068')
add('button_pressed',None,boxes=[([5,0,6],[11,1.02,10])],sha='a4da58f6a3afbf515136901b03ef5690e351932c')
add('oak_pressure_plate','pressure_plate_up',sha='3fb5dd7c91d1c9de7e7938c5db23282a22840421')
add('oak_pressure_plate_down','pressure_plate_down',sha='06c4db73235c56a16e2a2898ebdcd57e4f2be44a')

# 23 directly-read template/parent model files, excluding one missing `stairs_inner` guess.
def tmpl(n,p=None,b=None,sha='',r=None):add(n,p,b,sha,kind='template',rotation=r)
tmpl('cube_all','cube',sha='fa2f9e776173224b2b523b8b537c695b921267f6')
tmpl('slab','block',[([0,0,0],[16,8,16])],sha='1eadc701d915521e782c1f8af4393a57732d4af2')
tmpl('stairs','block',[([0,0,0],[16,8,16]),([8,8,0],[16,16,16])],sha='986ce9c6ee85c488fcce0ef924eec6ed118e5f09')
tmpl('fence_post',None,[([6,0,6],[10,16,10])],sha='4f6a7438647518cf3c2aada17462be1260dd86d2')
tmpl('fence_side',None,[([7,12,0],[9,15,9]),([7,6,0],[9,9,9])],sha='7145349ba783848e35d4786db6bed22b77ff5e51')
tmpl('template_trapdoor_bottom','thin_block',[([0,0,0],[16,3,16])],sha='2b6c8daa974d26356b18f037b7fc16a237699136')
tmpl('door_bottom_left',None,[([0,0,0],[3,16,16])],sha='5eef3f89cbe3e1fff5bfbaacc65e34f5fa5776a1')
tmpl('template_shelf_body','block',[([0,0,13],[16,16,16]),([0,0,11],[16,4,13]),([0,12,11],[16,16,13])],sha='2f258411f5a049fcd96f274e1253fb9acdaa570d')
tmpl('cube','block',[([0,0,0],[16,16,16])],sha='1b9780b479aee527f79bde950656b82f1524128b')
tmpl('cube_column','cube',sha='358b9847efe8bb17811ef48eedd219d8c9b51499')
tmpl('cube_bottom_top','cube',sha='4c610597880f4593c7b6e62d7da0feb95dac5b8f')
tmpl('template_chiseled_bookshelf_slot_top_left',None,[([10,8,0],[16,16,0])],sha='da9fc59136a95d14a3fbe5eb363564b8fa45bf36')
tmpl('template_anvil','block',[([2,0,2],[14,4,14]),([4,4,3],[12,5,13]),([6,5,4],[10,10,12]),([3,10,0],[13,16,16])],sha='47a37763cc372fa5ad9f0f43719e246d6a5b16df')
tmpl('thin_block','block',sha='1adb58ab77ba14878221c894e8bef09921e1844f')
tmpl('block',None,sha='f9c72559950abcb186b8e3959e135c0f2d542bdf')
tmpl('inner_stairs',None,[([0,0,0],[16,8,16]),([8,8,0],[16,16,16]),([0,8,8],[8,16,16])],sha='364eff63e057a4abbb74d80f7d5297beba61f751')
tmpl('outer_stairs',None,[([0,0,0],[16,8,16]),([8,8,8],[16,16,16])],sha='03bbe420026b24edee44cab63ede4927933fbc55')
tmpl('slab_top',None,[([0,8,0],[16,16,16])],sha='e21eb9329d4f40244079424a14aa694a0577114e')
tmpl('template_trapdoor_open',None,[([0,0,13],[16,16,16])],sha='b301619c260a8ae7d03e85bfe2bc2bc0c90de835')
tmpl('template_trapdoor_top',None,[([0,13,0],[16,16,16])],sha='036aeb7b92c6ee94a9ccdcc7b54bb11ecf796532')
tmpl('pressure_plate_up','thin_block',[([1,0,1],[15,1,15])],sha='689fbe4f968231325862003e5730c845592250fb')
tmpl('pressure_plate_down',None,[([1,0,1],[15,.5,15])],sha='db6e6ba6c1b8dc4de78806dfbea2956d7f3978ad')
tmpl('template_shelf_unpowered','block',[([0,4,13],[16,12,13])],sha='ad5b6a3fc7c2256e2cab8f18a46a82e085511cec')

# 16 actual blockstate JSON files inspected. `entries` is JSON-key count, not #geometry variants.
B={}
def blockstate(n,mode,entries,sha,example):B[n]=dict(name=n,mode=mode,entries=entries,sha=sha,example=example)
blockstate('oak_planks','variants',1,'02780929635818fd6254fdab86ea7e97a6440331','"": oak_planks')
blockstate('oak_slab','variants',3,'c503f74caa7dff5713280041366e628f9a7f8449','type=bottom/double/top; double -> oak_planks')
blockstate('oak_stairs','variants',40,'c20e7ef6c86dd57238f39cd51fc6b0c5bcc5b079','facing × half × shape; straight/inner/outer models; rotations/uvlock')
blockstate('oak_fence','multipart',5,'394851e1883d0bda305aa0b47b04b0e04716200a','always post + when north/east/south/west=true side')
blockstate('oak_trapdoor','variants',16,'168faf128975a6e34c0cf2035a464058d94072d8','facing × half × open; model variants and rotations')
blockstate('oak_door','variants',32,'c739dec25fbb5b9a85f175ab18b9b230b4003011','facing × half × hinge × open')
blockstate('barrel','variants',12,'3ed4f4061207cfaa7860fbc67a6697d701ca22cb','facing six directions × open false/true')
blockstate('oak_shelf','multipart',24,'404c901695218478e0bc1df86b4c66538d118f56','facing, powered, block states, multiple conditional applications')
blockstate('red_bed','variants',1,'6577c90a27efb34a7099150253c0bf557d75214c','"": model block/bed (no elements)')
blockstate('chest','variants',1,'f78fa579cec93e6b0ce9ed44d7115bd125f57ee9','"": model block/chest (no elements)')
blockstate('oak_sign','variants',1,'b9f38f4f7f38680ed0656ce1d62f5d076bf24559','"": model block/oak_sign (no elements)')
blockstate('flower_pot','variants',1,'8a1ab93befbc6f0aec81bb781572b6f1a0880be0','"": model block/flower_pot')
blockstate('oak_pressure_plate','variants',2,'6ecbfbc5fd703b033e05ff61fa05bb96be2afc30','powered=false/true -> pressure_plate_up/down')
blockstate('stone_button','variants',24,'0fb70d99020834cf401a4594327249b5cf25f66f','face × facing × powered; pressed geometry differs')
blockstate('lectern','variants',4,'b6ec88be8a3c38277d976d9214502aeb908d2a74','four facing rotations')
blockstate('composter','multipart',9,'219eea9c2abecb3edfebac457e3feea4d2be0378','base model + contents conditional on level 1..8')

assert len([a for a in A.values() if a['kind']=='named'])==32
assert len([a for a in A.values() if a['kind']=='template'])==23
assert len(B)==16
assert len(A)==55

def resolve(name):
    visited=set(); cur=name;path=[]
    while cur is not None:
        if cur in visited:raise ValueError('parent cycle '+name)
        visited.add(cur); n=A.get(cur)
        if n is None:raise ValueError('missing '+cur+' for '+name)
        path.append(cur)
        if n['boxes'] is not None:return n['boxes'],path,n['rotation']
        cur=n['parent']
    return None,path,{}

def bbox(boxes):
    if not boxes:return None
    # NOTE: axis-aligned extents are calculated BEFORE element-local rotation.
    return [min(box[0][i] for box in boxes) for i in range(3)]+[max(box[1][i] for box in boxes) for i in range(3)]

def write_csv(fname,rows,cols):
    with (OUT/fname).open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=cols,extrasaction='ignore');w.writeheader();w.writerows(rows)

models=[]; elements=[]; sources=[]
for n,v in A.items():
    bx,chain,r=resolve(n)
    status=('JSON_particle_only_or_special_renderer_unverified' if bx is None else 'model_JSON_geometry_inherited' if len(chain)>1 and v['boxes'] is None else 'model_JSON_geometry_direct')
    bb=bbox(bx)
    url=f'{GITHUB}/models/block/{n}.json'
    models.append(dict(name=n,kind=v['kind'],parent=v['parent'] or '',parent_chain=' > '.join(chain),element_count=len(bx) if bx is not None else '',box_min_xyz=json.dumps(bb[:3]) if bb else '',box_max_xyz=json.dumps(bb[3:]) if bb else '',rotation_observed=int(bool(v['rotation'] or r)),texture_variables=json.dumps(v['textures'],ensure_ascii=False),geometry_status=status,github_blob_sha1=v['sha'],source_url=url))
    sources.append(dict(path=f'assets/minecraft/models/block/{n}.json',github_blob_sha1=v['sha'],source_url=url,source_type='model',read_status='GitHub_connector_read_2026-11-11'))
    for k,(lo,hi) in enumerate(bx or []):
        dims=[round(hi[i]-lo[i],4) for i in range(3)]
        elements.append(dict(model=n,element_index=k,origin_geometry_model=chain[-1],from_xyz=json.dumps(lo),to_xyz=json.dumps(hi),dimensions_xyz=json.dumps(dims),local_rotation=json.dumps((v['rotation'] or r).get(str(k),{})),note='Unrotated element dimensions; not collision shape'))
for n,v in B.items():
    sources.append(dict(path=f'assets/minecraft/blockstates/{n}.json',github_blob_sha1=v['sha'],source_url=f'{GITHUB}/blockstates/{n}.json',source_type='blockstate',read_status='GitHub_connector_read_2026-11-11'))
blockstates=[dict(name=v['name'],type=v['mode'],variant_or_multipart_entry_count=v['entries'],sample_behavior=v['example'],github_blob_sha1=v['sha'],source_url=f'{GITHUB}/blockstates/{n}.json') for n,v in B.items()]
assert len(sources)==71 and len(models)==55
assert next(z for z in models if z['name']=='oak_shelf')['element_count']==3
assert next(z for z in models if z['name']=='lectern')['element_count']==3
assert next(z for z in models if z['name']=='anvil')['element_count']==4
assert next(z for z in models if z['name']=='flower_pot')['element_count']==5
assert next(z for z in models if z['name']=='oak_stairs_inner')['element_count']==3
assert next(z for z in models if z['name']=='chest')['geometry_status'].startswith('JSON_particle')

write_csv('01_대표모델_구조55.csv',models,list(models[0]))
write_csv('02_모델요소_치수.csv',elements,list(elements[0]))
write_csv('03_블록상태_16.csv',blockstates,list(blockstates[0]))
write_csv('04_모델및블록상태_근거원장71.csv',sources,list(sources[0]))

# Carry forward the v4 quantitative record, not the original asset textures.
shutil.copy2(PREV/'01_누적150종_픽셀측정.csv',OUT/'05_v4계승_150종_픽셀측정.csv')
previous=pd.read_csv(OUT/'05_v4계승_150종_픽셀측정.csv')
assert len(previous)==150 and len(set(previous.texture_id))==150

# An independent database that can be joined to future mod studies.
db_path=OUT/'MC_Furniture_Style_Stage1_Research_v5.sqlite'
if db_path.exists():db_path.unlink()
conn=sqlite3.connect(db_path)
conn.execute('PRAGMA foreign_keys=ON')
conn.execute('CREATE TABLE sources (path TEXT PRIMARY KEY, github_blob_sha1 TEXT, source_url TEXT, source_type TEXT, read_status TEXT)')
conn.execute('CREATE TABLE models (name TEXT PRIMARY KEY, kind TEXT, parent TEXT, parent_chain TEXT, element_count INTEGER, box_min_xyz TEXT, box_max_xyz TEXT, rotation_observed INTEGER, texture_variables TEXT, geometry_status TEXT, github_blob_sha1 TEXT, source_url TEXT)')
conn.execute('CREATE TABLE elements (model TEXT, element_index INTEGER, origin_geometry_model TEXT, from_xyz TEXT, to_xyz TEXT, dimensions_xyz TEXT, local_rotation TEXT, note TEXT, PRIMARY KEY (model,element_index), FOREIGN KEY(model) REFERENCES models(name))')
conn.execute('CREATE TABLE blockstates (name TEXT PRIMARY KEY, type TEXT, variant_or_multipart_entry_count INTEGER, sample_behavior TEXT, github_blob_sha1 TEXT, source_url TEXT)')
conn.execute('CREATE TABLE texture_stats_v4 (texture_id TEXT PRIMARY KEY, family TEXT, source_url TEXT, sha256 TEXT, width INTEGER, height INTEGER, unique_rgb_visible INTEGER, mean_luma REAL, luma_std REAL, verification TEXT)')
conn.executemany('INSERT INTO sources VALUES (?,?,?,?,?)',[[r[k] for k in sources[0]] for r in sources])
for m in models:
    vals=[m[k] if m[k]!='' else None for k in list(models[0])]
    conn.execute('INSERT INTO models VALUES (?,?,?,?,?,?,?,?,?,?,?,?)',vals)
for e in elements:
    conn.execute('INSERT INTO elements VALUES (?,?,?,?,?,?,?,?)',[e[k] for k in elements[0]])
for b in blockstates:
    conn.execute('INSERT INTO blockstates VALUES (?,?,?,?,?,?)',[b[k] for k in blockstates[0]])
for r in previous.itertuples(index=False):
    conn.execute('INSERT INTO texture_stats_v4 VALUES (?,?,?,?,?,?,?,?,?,?)',(r.texture_id,r.family,r.source_url,r.sha256,r.width,r.height,r.unique_rgb_visible,r.mean_luma,r.luma_std,r.verification))
conn.commit(); integrity=conn.execute('PRAGMA integrity_check').fetchone()[0]
counts={tbl:conn.execute(f'SELECT count(*) FROM {tbl}').fetchone()[0] for tbl in ['sources','models','elements','blockstates','texture_stats_v4']};conn.close()
assert integrity=='ok' and counts['sources']==71 and counts['models']==55 and counts['blockstates']==16 and counts['texture_stats_v4']==150

major=[('참나무 반 블록','oak_slab'),('참나무 계단','oak_stairs'),('안쪽 모서리 계단','oak_stairs_inner'),('울타리 기둥','oak_fence_post'),('울타리 연결 부품','oak_fence_side'),('참나무 다락문 닫힘','oak_trapdoor_bottom'),('참나무 문 하단','oak_door_bottom_left'),('참나무 선반','oak_shelf'),('독서대','lectern'),('모루','anvil'),('화분','flower_pot'),('퇴비통','composter'),('참나무 압력판','oak_pressure_plate'),('누른 압력판','oak_pressure_plate_down')]
rows=[]
for ko,n in major:
    m=next(z for z in models if z['name']==n)
    lo=json.loads(m['box_min_xyz']);hi=json.loads(m['box_max_xyz']);
    rows.append(f"| {ko} | `{n}` | {m['element_count']} | `{tuple(round(hi[i]-lo[i],3) for i in range(3))}` |")
md='''# 바닐라 3D 구조 분석 v5 — 첫 모델링 분석 보고서

- 기준: Minecraft **Java Edition 1.21.11**
- 연구 원칙: 바닐라 → 가구 모드 → 공통 스타일 연구. **실제 좀보이드 가구 제작은 이 단계에서 제외**
- 원본 경로: [`InventivetalentDev/minecraft-assets` 1.21.11](https://github.com/InventivetalentDev/minecraft-assets/tree/1.21.11/assets/minecraft), *비공식 게임 에셋 추출 미러*
- 검증 근거: 연결된 GitHub의 개별 원본 모델 JSON과 블록 상태 JSON을 직접 읽어, 파일별 SHA-1(Git Blob SHA)을 기록한 파생 구조 데이터. 아래 수치는 설계 권장값이 아니라 **원본 관찰 수치**다.

## 1. 진행 상태

| 항목 | 실측·근거 상태 | 남은 검증 |
|---|---|---|
| 01 바닐라 재질·텍스처 | **150/150 경로** 기존 v4 계승, 표본 측정 목표 100% | 공식 client.jar의 150건 해시 대조 0/150, 인게임 렌더 0/150 |
| 02 바닐라 3D 모델 구조 | **이름 있는 모델 32개 + 부모/템플릿 23개 = 실제 JSON 55개 확인**, 블록 상태 JSON 16개 확인 | 완전한 전체 모델 목록·실제 렌더링·충돌 형태·아이템/엔티티 렌더링 연구 |
| 03 가구 모드 3D | 미착수 | 모드 에셋 및 라이선스 확보 |
| 04 가구 모드 텍스처·UV | 미착수 | 모드별 텍스처 원본 분석 |
| 05 바닐라/모드 비교 | 미착수 | 전 단계 근거 필요 |

**전체 5개 작업 확정 완료 수는 0/5개이고, 진행 중 2개다.** 02의 55개 모델 표본이 완료됐다는 뜻이지 바닐라 전체 모델 분석이 완료됐다는 뜻이 아니다.

## 2. 파악한 대표 구조 — 모델 좌표계 16단위 기준

> 외접 크기는 요소의 **로컬 회전을 적용하기 전**의 축 정렬 범위다. 특히 독서대의 실제 기울어진 상판 범위와 물리 충돌 범위는 이 표의 치수와 다를 수 있다.

| 모델 | 소스 키 | 직육면체 수 | 외접 크기 (X,Y,Z) |
|---|---|---:|---|
'''+ '\n'.join(rows)+''' 

### 2.1 바닐라 모델에서 직접 확인한 3가지 구조 방식

**A. 같은 정육면체 형상에 텍스처만 다르게 배정하기**

- `oak_planks` → `cube_all` → `cube` 부모 템플릿으로 이어지는 계층이다.
- `bookshelf` → `cube_column` → `cube`; 상단/하단에는 참나무 판자, 옆면에는 책장 텍스처를 배치한다.
- `barrel` → `cube_bottom_top` → `cube`; 위·옆·아래를 별개 PNG로 지정한다.
- `crafting_table` / `smithing_table`은 둘 다 전체 정육면체지만 면마다 다른 텍스처를 둔다.
- **확인한 사실:** 적은 메시 요소 수로도 면별 텍스처 배치를 달리해 사물의 정체를 구분한다.

**B. 간단한 직육면체들을 조합해 입체적인 실루엣 만들기**

- `oak_slab`은 16×8×16 바닥 하나, 일반 `oak_stairs`는 직육면체 2개다.
- `oak_stairs_inner`는 3개, `oak_stairs_outer`는 2개다. 모양별로 **새 모델/템플릿 선택**이 이루어진다.
- `oak_fence_post`는 4×16×4 기둥이고, `oak_fence_side`는 위·아래 가로대 2개다.
- `oak_shelf`는 벽 부착형 몸체와 위·아래 판을 포함해 3개 요소이며, `oak_shelf.png`는 앞선 v4에서 32×32로 확인되었다.
- `template_anvil`은 바닥·몸통·상단 등을 4개 요소로 조립한다.
- `flower_pot`, `composter`는 각각 5개 직육면체로 빈 공간을 표현한다.
- `lectern`은 3개 요소 중 상단 요소 하나에 X축 −22.5° 로컬 회전이 명시되어 있다.

**C. 블록 상태로 형태·부품·방향을 달리하기**

- `oak_stairs`: `facing`·`half`·`shape`의 조합으로 **40개 `variants` 키**를 정의하며 일반/안쪽/바깥쪽 모델 및 회전을 쓴다.
- `oak_door`: **32개 `variants` 키**로 방향·상하·경첩·열림 상태를 구분한다.
- `oak_trapdoor`: **16개 `variants` 키**로 방향·상하·열림 상태를 구분한다.
- `oak_fence`: **5개 `multipart` 규칙**을 이용해 기둥을 항상 두고 N/E/S/W가 연결되면 가로대를 추가한다.
- `oak_shelf`: **24개 `multipart` 규칙**은 방향·상태 등에 따라 부품 모델을 추가한다. 이 수는 모든 가능한 게임 상태 수나 한 번에 배치되는 직육면체 수가 아니다.
- `composter`: **9개 `multipart` 규칙**으로 기본 모델과 높이별 내부 내용을 나눈다.
- `barrel`: **12개 `variants` 키**로 여섯 방향과 열림 여부에 따라 다른 텍스처/모델 상태를 조합한다.

## 3. UV·모델·텍스처를 함께 봐야 하는 이유

- 모델 JSON의 `from`/`to`는 기하구조, `faces[].uv`와 `textures`는 실제 픽셀이 어디에 표시되는지 정의한다.
- 참나무 선반 `template_shelf_body`는 3개 요소가 **같은 32×32 PNG의 서로 다른 UV 구역**을 사용한다. 모델의 한 면이 32×32라는 뜻이 아니다.
- `template_trapdoor_bottom`은 16×3×16 요소를 쓰되, 옆면의 UV 높이는 윗면과 다르다.
- 오브젝트가 `elements: []`처럼 기하 구조를 직접 제공하지 않고 부모를 가진 경우, **부모 템플릿까지 추적하지 않으면 실제 요소 수가 0개라고 잘못 읽는다**.

## 4. 주의할 예외와 미확정 사항

**특수 렌더 구조:** 실제로 확인한 `block/bed`, `block/chest`, `block/oak_sign` 모델 JSON에는 `elements`가 없고 파티클 텍스처 참조만 있다. 따라서 일반 블록 모델 요소 수로 침대·상자·표지판의 **실제 게임 속 3D 형상**을 측정할 수 없다. 이들 객체의 렌더링 파이프라인과 실제 크기는 현재 *미검증*으로 보존한다.

**충돌 판정과 모델 요소 구분:** `from`/`to`는 그래픽 모델을 기술한다. 울타리의 통과 가능 영역, 상자의 충돌 상자, 누름판의 상호작용 등은 별도의 게임 상태/코드로 정의될 수 있으므로 여기서 추정하지 않는다.

**일부 템플릿 요소는 두께가 0:** 사다리 `ladder`와 조각 책장 슬롯 템플릿은 0 두께 평면 요소를 사용한다. 3D 텍스처를 붙이는 얇은 면이지 일반적인 부피가 있는 큐브로 볼 수 없다.

**원본 공식 검증:** 비공식 GitHub 미러에서 실제 JSON을 읽은 단계이며 사용자 로컬의 정품 Mojang `client.jar`와의 바이트·해시 대조를 수행하지 않았다. 게임 플레이 및 화면 관찰도 수행하지 않았다.

## 5. 아직 확정해서는 안 되는 규칙

- "의자 다리는 반드시 2픽셀이어야 한다" 같은 규범적인 결론은 아직 내리지 않는다.
- "가구는 큐브 3개가 적절하다"도 일반화하지 않는다. 이번 32개 이름 있는 모델은 임의 추출한 대표 표본이지 모든 바닐라 모델의 통계적 대표성을 확보한 것이 아니다.
- 저작권·라이선스가 확인되지 않은 Minecraft 모델 JSON·텍스처 PNG 원본은 배포 ZIP에 넣지 않았다.

## 6. 다음 단계

1. **02 계속:** 계단/울타리/문/선반을 대상으로 부모 상속뿐 아니라 면별 UV·회전·블록 상태에 따른 완성 조합을 복원해 실제 외관 차이를 검증한다.
2. `chest`, `bed`, `oak_sign` 특수 렌더링 구조는 일반 블록 JSON 분석과 구분한다.
3. **01의 보류:** 사용자의 정품 1.21.11 `client.jar`가 확보되면 150개 텍스처 SHA를 비교하고 게임 내 렌더를 따로 검증한다. 이 보류가 02에서 원본 JSON의 분석을 진행할 수 없다는 뜻은 아니다.
4. 02 구조 분석 근거가 늘어나면 03의 가구 모드 실제 모델 연구로 넘어간다.

## 7. 출처 및 재현

- [모델 원본 인덱스](https://github.com/InventivetalentDev/minecraft-assets/tree/1.21.11/assets/minecraft/models/block)
- [블록 상태 원본 인덱스](https://github.com/InventivetalentDev/minecraft-assets/tree/1.21.11/assets/minecraft/blockstates)
- 개별 71개 JSON 경로와 Git Blob SHA-1은 `04_모델및블록상태_근거원장71.csv`에 기록했다.
- 개별 모델의 부모 경로·실측 요소 치수·원본 참조가 `01_대표모델_구조55.csv`, `02_모델요소_치수.csv`에 있다.
- 기존 v4 텍스처 결과 150경로의 통계 CSV를 동일 바이트로 계승해, 새 SQLite DB에 결합했다.

**검증 상태:** JSON 구조 표본 판독 완료 / 공식 게임 파일 SHA·인게임 렌더 보류 / 2단계 규칙서 미작성.
'''
(OUT/'00_v5_3D_구조분석_보고서.md').write_text(md,encoding='utf-8')
progress='''# 학습 진행도 v5 (2026-11-11)

| 세부 작업 | 진행 상태 | 확인된 정량 근거 | 미완료 이유 |
|---|---|---|---|
| 01. 바닐라 재질·텍스처 | 표본 목표 100%, 검증 보류 | 150/150 경로 | 공식 client.jar 0/150, 인게임 0/150 |
| 02. 바닐라 3D 구조 | **진행 중** | 이름 있는 블록 모델 32개, 부모/템플릿 23개, 블록 상태 16개 → JSON 파일 71개 직접 열람 | UV 전체, 완성 상태별 합성, 특수 렌더·게임 검증 미완료 |
| 03. 가구 모드 모델 | 미시작 | 0 | 단계 02 분석 선행 |
| 04. 가구 모드 텍스처/UV | 미시작 | 0 | 단계 03 분석 선행 |
| 05. 바닐라/모드 비교 | 미시작 | 0 | 단계 03~04 분석 선행 |

**전체 5개 세부 작업 확정 완료 수: 0/5. 진행 중: 2/5.**

진행률은 임의 가중 평균으로 표기하지 않는다. 특히 01의 150/150=100%는 **표본 통계 수집 목표**일 뿐 01 최종 완료 아님. 02는 대표 모델 JSON을 71개 읽었으며 바닐라 전체 모델 수에 대한 완료율로 환산하지 않는다.
'''
(OUT/'06_학습_진행도_v5.md').write_text(progress,encoding='utf-8')
README=f'''# MC 바닐라 모델링 학습 v5

- 기존 150종 텍스처 통계 CSV 유지; 새로 실제 모델 JSON 55개/블록 상태 JSON 16개 분석.
- 원본 Minecraft 3D 모델 JSON/PNG는 포함되지 않음. 파생 통계, 출처, 기록만 수록.
- 핵심 보고서: `00_v5_3D_구조분석_보고서.md`
- SQL DB: `MC_Furniture_Style_Stage1_Research_v5.sqlite` (integrity_check = {integrity})
- 검증된 파일 레코드: {len(sources)}개, 요소 치수 레코드: {len(elements)}개.
- `build_v5.py`는 추출한 요약 데이터를 재집계하기 위한 코드. 원본 JSON을 재수집하지 않으며 라이브 Github API 접근 기능은 없음.
'''
(OUT/'README.md').write_text(README,encoding='utf-8')
shutil.copy2(BASE/'build_v5.py',OUT/'build_v5.py')
state={'version':'v5','date':'2026-11-11','edition':'Minecraft Java 1.21.11','prior_textures':150,'prior_textures_original_refetched':0,'new_named_models':32,'new_parent_templates':23,'new_blockstates':16,'total_source_json_read':71,'derived_element_rows':len(elements),'official_jar_textures_compared':0,'in_game_render_verified':0,'five_subtasks_finished':0,'five_subtasks_in_progress':2,'sqlite_integrity':integrity,'tables':counts,'note':'Representative model files only; do not mistake model file count or 150 textures for completion of the stage.'}
(OUT/'07_검증_상태.json').write_text(json.dumps(state,ensure_ascii=False,indent=2),encoding='utf-8')
zip_path=Path('/mnt/data/마크_가구모델링_바닐라3D분석_v5_근거71파일.zip')
with zipfile.ZipFile(zip_path,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=8) as z:
    for p in sorted(OUT.iterdir()):
        if p.is_file():z.write(p,arcname=p.name)
with zipfile.ZipFile(zip_path) as z:
    assert z.testzip() is None
print(json.dumps({'zip_path':str(zip_path),'zip_bytes':zip_path.stat().st_size,'sqlite_integrity':integrity,'table_counts':counts,'named_models':32,'templates':23,'blockstates':16,'element_rows':len(elements),'report':str(OUT/'00_v5_3D_구조분석_보고서.md')},ensure_ascii=False,indent=2))
