#!/usr/bin/env python3
"""v7 SQLite -> v8: Minecraft Java 1.21.11 special & hybrid render evidence.
This reproduces packaged analysis from recorded observations.  GitHub source
SHA-1 identifiers were collected through live GitHub fetch calls on 2026-11-12.
It is NOT a replay of in-game rendering.  Original game asset bytes omitted.
"""
import csv, hashlib, io, json, os, re, sqlite3, zipfile
from pathlib import Path
from collections import Counter

ROOT=Path('/mnt/data')
WORK=ROOT/'MC_vanilla_models_study_08'
RESULT=WORK/'results'
RESULT.mkdir(parents=True,exist_ok=True)
PREV=ROOT/'마크_바닐라3D분석_v7_연결형조립_21사례.zip'
OLD='MC_vanilla_models_study_07/results/MC_Furniture_Style_Stage1_Research_v7.sqlite'
DB=RESULT/'MC_Furniture_Style_Stage1_Research_v8.sqlite'
with zipfile.ZipFile(PREV) as z:
    DB.write_bytes(z.read(OLD))

P='assets/minecraft/'
REPO='InventivetalentDev/minecraft-assets'
BRANCH='1.21.11'
def link(path):return f'https://github.com/{REPO}/blob/{BRANCH}/{path}'

# These are the JSONs examined via the connected GitHub file fetcher.  A single
# state may refer to a model shared across many blocks, so Sha may repeat.
# (block, classification, blockstate_sha1, model_name, model_sha1,
#  parent, resolved geometry elements, atlas, renderer, evidence explanation)
ROWS=[
('red_bed','SPECIAL','6577c90a27efb34a7099150253c0bf557d75214c','bed','9406a8491ed2532d4878b0a91b16a0e5f8d93d80','',0,'beds','BedBlockEntityRenderer','침대 HEAD/FOOT의 실제 3D 외형은 BER; JSON에는 particle만 기록'),
('chest','SPECIAL','f78fa579cec93e6b0ce9ed44d7115bd125f57ee9','chest','9406a8491ed2532d4878b0a91b16a0e5f8d93d80','',0,'chests','ChestBlockEntityRenderer','닫히거나 열리는 뚜껑, 단일/이중 상자 모델은 BER'),
('trapped_chest','SPECIAL','fd8d40b1972deddf609b991f851b71a35d5c3798','trapped_chest','9406a8491ed2532d4878b0a91b16a0e5f8d93d80','',0,'chests','ChestBlockEntityRenderer','비슷한 소유의 JSON(파티클)과 특수 상자 렌더 처리'),
('ender_chest','SPECIAL','8656aed71d3f2e90e6fde221cc0bbba74e823e01','ender_chest','ae6b33b2d0c399283351c2c97270e21ae4f7c6bb','',0,'chests','ChestBlockEntityRenderer','흑요석 파티클 정의와 실제 상자 렌더 모델은 별개'),
('oak_sign','SPECIAL','b9f38f4f7f38680ed0656ce1d62f5d076bf24559','oak_sign','9406a8491ed2532d4878b0a91b16a0e5f8d93d80','',0,'signs','SignBlockEntityRenderer','JSON 파티클 정의만 있고 나무 표지판과 텍스트는 별도 렌더'),
('oak_wall_sign','SPECIAL','b9f38f4f7f38680ed0656ce1d62f5d076bf24559','oak_sign','9406a8491ed2532d4878b0a91b16a0e5f8d93d80','',0,'signs','SignBlockEntityRenderer','벽 부착 표지판; JSON 모델 참조가 일반 표지판과 동일'),
('oak_hanging_sign','SPECIAL','b2c43dc30565df7450e5d82b9a1613ea1a8f325d','oak_hanging_sign','97f5acc2ba44bfd146fd1a8cfe1090d139a26074','',0,'signs','HangingSignBlockEntityRenderer','매다는 모양에 따른 특수 렌더; PNG는 signs/hanging 하위 디렉터리'),
('oak_wall_hanging_sign','SPECIAL','b2c43dc30565df7450e5d82b9a1613ea1a8f325d','oak_hanging_sign','97f5acc2ba44bfd146fd1a8cfe1090d139a26074','',0,'signs','HangingSignBlockEntityRenderer','벽 부착형 매달린 표지판'),
('shulker_box','SPECIAL','7248d53eae4b7699c076f04feee66d4054121b9a','shulker_box','7eb23421c9ccaf37874b279d17361706b2aa713d','',0,'shulker_boxes','ShulkerBoxBlockEntityRenderer','상자 속성 기반 특수 렌더; JSON은 파티클만'),
('white_shulker_box','SPECIAL','36973a4db98e49bffeb7ce35b3301a8637c3d838','white_shulker_box','3a9a58d33499a009e02f6c3d4dd712df0413798a','',0,'shulker_boxes','ShulkerBoxBlockEntityRenderer','색상별 재질 및 움직이는 몸체'),
('decorated_pot','SPECIAL','2aa0faf7bb6157870c9d09cb29f52ea1adf72f6a','decorated_pot','1456e72d8c368d6bacdc16f172dc2771784fa422','',0,'decorated_pot','DecoratedPotBlockEntityRenderer','도자기 조립과 장식은 기본 블록 JSON의 elements로 표현되지 않음'),
('enchanting_table','HYBRID','85aeab36af37efcca94f64c3b23aa9d5eb6266e0','enchanting_table','404ca9a3d28f77362a5597a4b0f0c2deaba6987c','block/block',1,'blocks','EnchantingTableBlockEntityRenderer','책상 본체 1요소 JSON + 위에 떠 있는 책 BER'),
('lectern','HYBRID','b6ec88be8a3c38277d976d9214502aeb908d2a74','lectern','a504fa96bc3c5c729adaaa015d927b8250a1bd63','block/block',3,'blocks','LecternBlockEntityRenderer','독서대 본체 3요소 JSON + 놓인 책 BER'),
('oak_shelf','HYBRID','404c901695218478e0bc1df86b4c66538d118f56','oak_shelf','4b0f3db311717ef740c50638ea1d252256310180','minecraft:block/template_shelf_body',3,'blocks','ShelfBlockEntityRenderer','선반 본체 3요소 + 상태에 따라 얇은 오버레이 + 보관 물품 BER'),
('bell','HYBRID','2af4b5dd2f1160d144385efe1df86d4f6f35b680','bell_floor','c2abfcbd5859121bf7c901822509b8c642ca9c14','',3,'blocks','BellBlockEntityRenderer','종의 설치 받침은 JSON, 종 몸체 움직임은 BER; floor형만 수치 집계'),
('barrel','JSON_ONLY','3ed4f4061207cfaa7860fbc67a6697d701ca22cb','barrel','cff930084d47d226817f274616d14f4b07c0a9d4','minecraft:block/cube_bottom_top',1,'blocks','','데이터를 저장하는 블록 엔티티지만 3D 외형은 일반 JSON 정육면체'),
('chiseled_bookshelf','JSON_ONLY','0c9b22b91093c4dfe3510a9a6aebe291df491e39','chiseled_bookshelf','a9bda72e10095343fb80de2bc4654212a1dc6834','block/block',1,'blocks','','본체 1요소 + 6개 슬롯에 multipart overlay, BER 없이 상태 기반 표시')]

# Atlases verified as actual version-specific atlas definitions, separate from
# the ordinary block atlas. source declarations are JSON, not the images.
ATLAS=[
('beds','d2e798a5e469c9b26e4e681c8062aec11fc848ea','entity/bed/','entity/bed'),
('chests','81a68b1cae693407b865d9c248870f7da3f54fb9','entity/chest/','entity/chest'),
('signs','1f34aaa1a133b15491c9844a583dcf8a9d76bf16','entity/signs/','entity/signs'),
('shulker_boxes','d4ecef71e8e365f0204ca18a44defc3b60e50fd9','entity/shulker/','entity/shulker'),
('decorated_pot','57356d9851bdcf43b0f21c698f1abc2f87c97740','entity/decorated_pot/','entity/decorated_pot'),
('blocks','541ce56ad0b09f258963dd2bf3e3cb6e786d2d79','block/','block'),
]

# Exact PNG IHDR dimensions, file length, and Git blob SHA from connector binary
# content (base64 decoded for header verification).  These are not SHA-256.
TEXTURES=[
('entity/bed/red.png','8ff0fb22f4a2b5e8a8593d227914576391aa0441',64,64,783,8,3),
('entity/bed/white.png','4b8e15c353428959a8e65a2e6b6f495e86708569',64,64,788,8,3),
('entity/bed/blue.png','a6ac300381be57ea059e5b0521e2e8ec242bf013',64,64,760,8,3),
('entity/bed/green.png','8a389fd11b024d2c8cbeac8ea541b5086e521cd5',64,64,777,8,3),
('entity/chest/normal.png','88afac2807f0fdc739a80ba41aac7173ccd16b9a',64,64,811,8,3),
('entity/chest/normal_left.png','15521925323176e06a507b3c2a5a1e6c105e06cc',64,64,838,8,3),
('entity/chest/normal_right.png','efe18c17a48066553aa25e4659e59a555fd6327f',64,64,873,8,3),
('entity/chest/ender.png','16025ae2249b64b5feaebee9e093b32c46bfa51e',64,64,712,8,3),
('entity/chest/trapped.png','ef78b7ec2ac696f9a47f61f301275f99232028d2',64,64,903,8,3),
('entity/signs/oak.png','35afd3dc77cd0f41701127690b19dd97e554fbf9',64,32,426,4,3),
('entity/signs/hanging/oak.png','b7fbbb639eae8df436f477f3031ba2b51674ef23',64,32,409,4,3),
('entity/signs/hanging/bamboo.png','e304f41682bb490022385bd4342886eb2499fd7b',64,32,449,4,3),
('entity/shulker/shulker.png','7abfb3a57d6f1920bc49dad636706f9ec5c9c3d5',64,64,1414,8,3),
('entity/shulker/shulker_purple.png','221a82042d99b3b77e99ddda29bcfafa2e59ff42',64,64,1056,8,3),
('entity/shulker/shulker_white.png','03473a59af65d7bbf028bd9a6d6a845f92b86b64',64,64,1085,8,3),
('entity/enchanting_table_book.png','ae861dc49572c2460dec3d4d54a1389e089ea2fa',64,32,305,8,3),
('entity/bell/bell_body.png','12d7795b5ec82866e87a46b3db0ed2761d1d781d',32,32,261,8,3),
('entity/decorated_pot/decorated_pot_base.png','e737e2850d48cdd2b087c335828872ae9b621da6',32,32,280,4,3),
('block/oak_planks.png','e5a15780171bdff340a8bab625c31d0891e8ba5e',16,16,195,8,3),
]

JAVADOC='https://maven.fabricmc.net/docs/yarn-1.21.11%2Bbuild.1/net/minecraft/client/render/block/entity/'
CLASS_DOCS={v[8]:JAVADOC+v[8]+'.html' for v in ROWS if v[8]}
VERSION_NOTE_URL='https://feedback.minecraft.net/hc/en-us/articles/46690753273997-Minecraft-Java-Edition-26-2'

cn=sqlite3.connect(DB)
cn.execute('PRAGMA foreign_keys=ON')
cn.executescript('''
CREATE TABLE IF NOT EXISTS special_block_evidence_v8 (
 block TEXT PRIMARY KEY, rendering_class TEXT NOT NULL,
 blockstate_path TEXT NOT NULL, blockstate_blob_sha1 TEXT NOT NULL,
 model_name TEXT NOT NULL, model_path TEXT NOT NULL, model_blob_sha1 TEXT NOT NULL,
 parent TEXT, base_primitive_count INTEGER NOT NULL,
 texture_atlas TEXT, renderer_class TEXT, renderer_reference_url TEXT,
 description_ko TEXT NOT NULL, evidence_grade TEXT NOT NULL,
 version TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS texture_atlases_v8 (
 atlas TEXT PRIMARY KEY, atlas_json_path TEXT NOT NULL, git_blob_sha1 TEXT NOT NULL,
 directory_prefix TEXT NOT NULL, source_directory TEXT NOT NULL,
 version TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS special_texture_metadata_v8 (
 texture_path TEXT PRIMARY KEY, git_blob_sha1 TEXT NOT NULL,
 width INTEGER NOT NULL, height INTEGER NOT NULL, file_bytes INTEGER NOT NULL,
 png_bit_depth INTEGER NOT NULL, png_color_type INTEGER NOT NULL,
 png_signature_checked INTEGER NOT NULL, version TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS rendering_conclusions_v8 (
 finding_id TEXT PRIMARY KEY, theme TEXT NOT NULL, finding_ko TEXT NOT NULL,
 evidence_paths_json TEXT NOT NULL, limitations_ko TEXT NOT NULL, grade TEXT NOT NULL
);
''')
for t in ('special_block_evidence_v8','texture_atlases_v8','special_texture_metadata_v8','rendering_conclusions_v8'):
    cn.execute('DELETE FROM '+t)

for block,typ,bs_sha,model,mod_sha,parent,primitives,atlas,renderer,desc in ROWS:
    bsp=f'{P}blockstates/{block}.json';mp=f'{P}models/block/{model}.json'
    cn.execute('INSERT INTO special_block_evidence_v8 VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
     (block,typ,bsp,bs_sha,model,mp,mod_sha,parent,primitives,atlas,renderer,CLASS_DOCS.get(renderer),desc,
      'A:JSON/atlas + B:Javadoc' if renderer else 'A:JSON/atlas + static model',BRANCH))
for atlas,sha,prefix,source in ATLAS:
    cn.execute('INSERT INTO texture_atlases_v8 VALUES (?,?,?,?,?,?)',
       (atlas,f'{P}atlases/{atlas}.json',sha,prefix,source,BRANCH))
for t,sha,w,h,n,bits,ct in TEXTURES:
    cn.execute('INSERT INTO special_texture_metadata_v8 VALUES (?,?,?,?,?,?,?,?,?)',
       (f'{P}textures/{t}',sha,w,h,n,bits,ct,1,BRANCH))

FINDINGS=[
('F01','SPECIAL','빈 블록 모델 JSON은 렌더링 모델 부재의 증거가 아니다. 침대/상자/표지판 등은 별도 BER/엔티티 모델을 사용한다.',
 ['models/block/bed.json','models/block/chest.json','models/block/oak_sign.json','atlases/beds.json','atlases/chests.json','atlases/signs.json'], 'BER 소스 코드를 직접 디컴파일하거나 인게임 화면을 비교하지 않았다.','A/B'),
('F02','HYBRID','마법 부여대/독서대/선반/종은 정적 본체와 별도 렌더 내용이 공존하는 사례다.',
 ['models/block/enchanting_table.json','models/block/lectern.json','models/block/oak_shelf.json','models/block/bell_floor.json'], '책·물품의 실제 프레임별 변환을 계산하지 않았다.','A/B'),
('F03','JSON_ONLY','블록 엔티티가 존재한다는 사실만으로 특수 렌더러가 필요하다고 판정하면 안 된다. 통/끌로 조각한 책장이 반례다.',
 ['models/block/barrel.json','models/block/chiseled_bookshelf.json','blockstates/chiseled_bookshelf.json'], '확인된 두 대상에 한정하며 전체 블록의 전수판정이 아니다.','A'),
('F04','TEXTURE_SCALE','특수 렌더용 텍스처는 64×64·64×32 등 여러 해상도를 활용하고, 일반 판자 표본은 16×16이다.',
 ['textures/entity/bed/red.png','textures/entity/chest/normal.png','textures/entity/signs/oak.png','textures/block/oak_planks.png'], 'PNG 헤더 확인만으로 UV 의미나 인게임 출력 색상까지 입증하지 않는다.','A'),
('F05','ATLAS','1.21.11은 beds/chests/signs/shulker_boxes/decorated_pot 등 별도 엔티티 atlas를 정의한다.',
 ['atlases/beds.json','atlases/chests.json','atlases/signs.json','atlases/shulker_boxes.json','atlases/decorated_pot.json'], '아틀라스에 나열된 폴더와 실제 최종 렌더 선택은 구분해야 한다.','A'),
('F06','VERSION','26.2에서 침대·표지판·매달린 표지판이 일반 블록 모델로 이관되었으므로, 1.21.11 연구 결과를 최신 버전에 그대로 일반화하면 안 된다.',
 ['models/block/bed.json','models/block/oak_sign.json','atlases/beds.json','atlases/signs.json'], '26.2 부분은 공식 릴리스 노트에 근거한다. 26.2 실제 JSON 파일은 본 연구에서 열지 않았다.','A/B'),
('F07','DESIGN','가구의 마인크래프트다움은 16x16 정적 모델만으로 정의되지 않는다. 정적·동적 외형과 버전을 함께 비교할 필요가 있다.',
 ['models/block/lectern.json','models/block/oak_shelf.json','atlases/blocks.json'], '이 문장은 연구 방향을 위한 해석으로 최종 제작 규칙이 아니다.','Inference')]
for k,theme,msg,paths,limit,grade in FINDINGS:
    cn.execute('INSERT INTO rendering_conclusions_v8 VALUES (?,?,?,?,?,?)',
            (k,theme,msg,json.dumps([P+x for x in paths],ensure_ascii=False),limit,grade))
cn.commit()
assert cn.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
assert cn.execute('SELECT COUNT(*) FROM texture_stats_v4').fetchone()[0]==150
assert cn.execute('SELECT COUNT(*) FROM assembly_cases_v7').fetchone()[0]==21
assert cn.execute('SELECT COUNT(*) FROM special_block_evidence_v8').fetchone()[0]==17
assert cn.execute('SELECT COUNT(*) FROM special_texture_metadata_v8').fetchone()[0]==19
assert cn.execute('SELECT COUNT(*) FROM texture_atlases_v8').fetchone()[0]==6
assert all(re.fullmatch('[0-9a-f]{40}',x[1]) for x in ATLAS)
assert all(re.fullmatch('[0-9a-f]{40}',x[1]) for x in TEXTURES)
assert all(re.fullmatch('[0-9a-f]{40}',r[2]) and re.fullmatch('[0-9a-f]{40}',r[4]) for r in ROWS)


def csv_save(path,head,rows):
    with open(path,'w',newline='',encoding='utf-8-sig') as f:
        w=csv.writer(f);w.writerow(head);w.writerows(rows)

csv_save(RESULT/'01_v8_17블록_렌더방식_근거.csv',
 ['block','render_mode','blockstate_path','blockstate_git_sha1','model_path','model_git_sha1','geometry_element_count','atlas','renderer','renderer_doc_url','observation','state','model_source_url'],
 [[b,k,f'{P}blockstates/{b}.json',s,f'{P}models/block/{m}.json',sh,c,at,rd,CLASS_DOCS.get(rd,''),d,BRANCH,link(f'{P}models/block/{m}.json')] for (b,k,s,m,sh,pa,c,at,rd,d) in ROWS])

csv_save(RESULT/'02_v8_19PNG_해상도_근거.csv',
 ['path','width','height','file_bytes','bit_depth','png_color_type','git_blob_sha1','url','note'],
 [[P+'textures/'+name,w,h,n,depth,color,sha,link(P+'textures/'+name),'PNG IHDR verified; alpha/compositing not analyzed'] for name,sha,w,h,n,depth,color in TEXTURES])

csv_save(RESULT/'03_v8_6아틀라스_정의.csv',
 ['name','path','git_blob_sha1','source_prefix','source_dir','source_url'],
 [[name,P+'atlases/'+name+'.json',sha,prefix,source,link(P+'atlases/'+name+'.json')] for name,sha,prefix,source in ATLAS])

csv_save(RESULT/'04_v8_17모델_유형요약.csv', ['mode','count','block_names'],
 [[mode,sum(x[1]==mode for x in ROWS),';'.join(x[0] for x in ROWS if x[1]==mode)] for mode in ('SPECIAL','HYBRID','JSON_ONLY')])

REPORT=f'''# 마인크래프트 1단계 연구 — v8 특수 렌더와 복합 가구의 구조

**연구 대상:** Minecraft Java Edition **1.21.11** (고정). **연구 범위:** 1단계 중 02. 바닐라 3D 모델 구조, 특별 사례. **분석일:** 2026-11-12.

## 1. 이번에 추가한 실측과 확인

- 지난 v7 SQLite DB(150종 텍스처 통계, 21개 상태별 조립 사례)를 그대로 계승하여 **17개 블록 유형을 재분류**했다.
- 분류: **SPECIAL(정적 JSON에 외형이 없음) {sum(r[1]=='SPECIAL' for r in ROWS)}개 / HYBRID(정적 모델+특수 요소) {sum(r[1]=='HYBRID' for r in ROWS)}개 / JSON_ONLY(정적 모델로 표현) {sum(r[1]=='JSON_ONLY' for r in ROWS)}개**.
- 공식이 아닌 **1.21.11 추출 에셋의 실제 blockstates/models/atlases JSON을 열어** Git blob SHA-1을 기록했다.
- 엔티티 계열 텍스처 **19개 PNG 헤더를 직접 확인**했고, **아틀라스 정의 6개**를 대조했다.
- 별도의 렌더러 클래스는 **Fabric Yarn 1.21.11 Javadoc**의 `BlockEntityRenderer` 계열에서 확인했다. 구현 코드나 런타임 화면을 디컴파일/실행한 것은 아니다.

## 2. 왜 모델 JSON이 비어 있는데 화면에는 입체 가구가 보일까?

블록 상태 정의가 모델 JSON을 가리키더라도, `models/block/bed.json`, `models/block/chest.json`, `models/block/oak_sign.json` 등은 `textures.particle`만 있고 `elements`가 없다. 따라서 이 JSON으로 계산된 직육면체 수는 **0개**이며, **게임 내 시각적인 침대·상자·표지판이 없다는 뜻이 아니다**.

`BedBlockEntityRenderer`, `ChestBlockEntityRenderer`, `SignBlockEntityRenderer` 클래스가 1.21.11 렌더링 계층에 존재한다. 침대는 `bedHead`/`bedFoot` 모델을 사용하며, 상자 렌더는 single/left/right 모델을 구분한다. 렌더러의 최종 자세·애니메이션 출력 검증은 아직 남았다.

이런 모델은 일반 JSON의 요소/면/UV 분석만 하면 구조를 놓치므로 **SPECIAL 분리**가 필요하다.

| 사례 | JSON 기본 기하 | 특수 요소 근거 | 텍스처 사례 |
|---|---:|---|---|
| 붉은 침대 | 0 | `BedBlockEntityRenderer` (머리·발 부분) | `entity/bed/red.png` **64×64** |
| 기본 상자 | 0 | `ChestBlockEntityRenderer` (단일·좌·우) | `entity/chest/normal.png` **64×64** |
| 참나무 표지판 | 0 | `SignBlockEntityRenderer` | `entity/signs/oak.png` **64×32** |
| 참나무 매달린 표지판 | 0 | `HangingSignBlockEntityRenderer` | `entity/signs/hanging/oak.png` **64×32** |
| 셜커 상자 | 0 | `ShulkerBoxBlockEntityRenderer` | `entity/shulker/shulker.png` **64×64** |
| 장식된 도자기 | 0 | `DecoratedPotBlockEntityRenderer` | `entity/decorated_pot/decorated_pot_base.png` **32×32** |

> 위 JSON 기하 수치는 고정된 정적 모델의 요소 수다. 게임 런타임의 다른 모델까지 0개라는 주장이 아니다.

## 3. 정적·동적 모델을 함께 사용하는 HYBRID 사례

| 사례 | 확인한 정적 요소 | 별도 렌더 내용 | 근거 |
|---|---:|---|---|
| 마법 부여대 | 1 | 위의 책 | `EnchantingTableBlockEntityRenderer` |
| 독서대 | 3 | 놓인 책 | `LecternBlockEntityRenderer` |
| 참나무 선반 | 3 (+조건별 평면) | 보관 아이템 | `ShelfBlockEntityRenderer.renderItem` |
| 종(바닥 설치형 받침) | 3 | 종 몸체 | `BellBlockEntityRenderer` |

**주의:** 정적 모델에 부분적 3D 구조가 있는 것과 동적 렌더러가 있는 것은 양립할 수 있다. 특히 선반의 기본 모델이 3개 요소라는 사실만으로, 선반에 놓인 아이템의 위치까지 표현했다고 결론내리면 안 된다.

## 4. 그렇지만 블록 엔티티 = 특수 3D 렌더는 아니다

**통**(`barrel.json`)은 부모 `cube_bottom_top`을 통해 16×16×16 큐브를 렌더한다. **끌로 조각한 책장**(`chiseled_bookshelf.json`)도 JSON 본체와 블록 상태의 **52개 multipart 조건**으로 책이 들어 있는 칸을 외형상 표시한다. 저장 공간/데이터를 가진 물체라는 사실과 렌더링 경로는 별개다.

## 5. 텍스처·UV 관련 발견

| 구분 | 이번 실제 PNG 헤더에서 확인한 해상도 | 오해하지 말 것 |
|---|---|---|
| 판자 표본 | 16×16 | 바닐라의 모든 텍스처가 16×16인 것은 아님 |
| 침대·상자 | 64×64 | PNG 크기는 모델 치수(64블록)를 뜻하지 않음 |
| 표지판·매달린 표지판 | 64×32 | 표지판 뒤쪽/앞쪽 텍스처의 UV 구성까지 이번 분석에서 역산한 것은 아님 |
| 종·도자기 일부 | 32×32 | 별도 아틀라스 여부와 텍스처 해상도는 다른 정보 |

**아틀라스:** 1.21.11의 `beds`, `chests`, `signs`, `shulker_boxes`, `decorated_pot`에서 각각 `entity/...`를 가리키는 directory source를 검증했다. `blocks`는 `block/` 경로를 포함한다.

## 6. 버전 경계 — 중요한 발견

**Java 26.2 릴리스 노트**는 **침대·표지판·매달린 표지판이 블록 모델을 사용하도록 전환**되고 `beds`, `signs` 아틀라스가 제거되었다고 명시한다. 따라서 **1.21.11에서 나온 JSON 중심 해석의 예외는 26.2에 그대로 적용되지 않는다.** 26.2의 실제 자산 JSON은 열지 않았으므로 이 차이는 공식 릴리스 설명에 근거한다.

- 1.21.11 자료: https://github.com/{REPO}/tree/{BRANCH}/assets/minecraft
- 1.21.11 Yarn 클래스 목록: {JAVADOC}package-summary.html
- 26.2 공식 릴리스 노트: {VERSION_NOTE_URL}
- 1.21.11 Fabric BER 가이드: https://github.com/FabricMC/fabric-docs/blob/main/versions/1.21.11/develop/blocks/block-entity-renderer.md

## 7. 검증 등급과 현재 제약

- **A(직접 관찰)**: 해당 버전 JSON 파일의 내용과 Git blob SHA, PNG header(width,height,bitdepth,colorType), 리소스 경로. **파일 자체를 패키지에 재배포하지 않았다**.
- **B(개발자 문서 근거)**: 1.21.11 Yarn Javadoc에 등재된 클래스·필드·메서드, 26.2 릴리스 노트.
- **추론**: 각 구조가 가구 스타일 학습에 주는 시사점은 아직 규칙이 아니다.
- **미완료**: 게임 설치본 `client.jar` 공식 직접 대조, 인게임 렌더 이미지/애니메이션 검사, BER의 실제 Java 구현 로직과 각 축의 UV 지도 재구성.

## 8. 다음 조사 순서

1. 1.21.11 BER 클래스 별 실제 `getTexturedModelData`/모델 파트 계층 구조 조사(가능한 경우 매핑·코드 자료 이용).
2. **같은 가구 유형의 인게임 외형과 모델의 일치** 확인(사용자 게임 스크린샷/실행본 제공 시).
3. 01과 02의 완료 조건 확정 후 03 가구 모드의 실제 `.json`/`.bbmodel` 샘플 분석으로 이동.

**이번 연구는 실제 좀보이드 가구를 제작하거나 모델링 룰북(2단계)을 확정하는 작업이 아니다.**
'''
(RESULT/'00_v8_특수렌더_정적동적_비교보고서.md').write_text(REPORT,encoding='utf-8')

progress=f'''# 1단계 학습 진행도 — v8 (2026-11-12)

| 계획서 항목 | 상태 | 실측·근거 |
|---|---|---|
| 01 바닐라 재질·텍스처 | 표본 완료 / 원본·인게임 검증 보류 | 150 / 150종 표본 |
| 02 바닐라 3D 모델 구조 | 진행 중 / 특수 렌더 예외 조사 | v7 연결 조립 21개 사례 계승 + v8 신규 17블록(11+4+2) |
| 03 가구 모드 3D | 미시작 | 0 모드 |
| 04 가구 모드 텍스처·UV | 미시작 | 0 모드 |
| 05 바닐라·모드 비교 | 미시작 | 비교 데이터 부족 |

**전체 단계 완료: 0/5**. 숫자 150/150은 텍스처 표본 측정 목표이고, 마인크래프트 전체 가구 모델링 학습 진도는 아니다.

### 이번 v8 추가분

- 1.21.11 블록 17개 렌더 경로 판정 (SPECIAL 11, HYBRID 4, JSON_ONLY 2)
- 실물 PNG 19개 파일 헤더 파싱/해상도·Git blob SHA 기록
- 아틀라스 JSON 정의 6개 대조
- v7 21개 상태 조립, 이전 150종 통계 보존 확인
- 버전 차이: 26.2에서 침대·표지판의 렌더링 방식이 변경되었으므로 별도 구분

### 남은 검증

- 공식 1.21.11 client.jar SHA 비교 미실시
- 실제 게임의 재질 tint/광원/UV·BER 애니메이션 미검증
- 02 전체 바닐라 모델 목록을 대상으로 한 전수 검수 미실시

### 다음 체크포인트

- 더 깊은 특수 렌더 지오메트리(침대·상자·표지판)의 실제 부품 구성/비율을 확인하고, 02 대표 샘플의 완료 기준을 고정한다.
'''
(RESULT/'05_v8_학습진행도.md').write_text(progress,encoding='utf-8')

cn.commit(); cn.execute('PRAGMA wal_checkpoint(TRUNCATE)')
stats={name:cn.execute(f'SELECT COUNT(*) FROM {name}').fetchone()[0] for name in ('texture_stats_v4','assembly_cases_v7','special_block_evidence_v8','texture_atlases_v8','special_texture_metadata_v8','rendering_conclusions_v8')}
cn.close()
validation={'database_integrity':'ok','base_db':'v7 preserved','version':'1.21.11','checkpoints':stats,
            'class_count':dict(Counter(r[1] for r in ROWS)),
            'sources':'GitHub assets extract + Yarn 1.21.11 Javadoc + Mojang 26.2 release notes',
            'checks':['each observed record uses git blob sha1','sqlite integrity_check','150 historical texture stats','21 historical assembly examples','PNG headers observed in connected GitHub base64 response'],
            'not_verified':['official client.jar byte/sha comparison','runtime rendering','implementation details of BER'],
            'published_material_contains_original_game_assets':False}
(RESULT/'06_v8_검증현황.json').write_text(json.dumps(validation,ensure_ascii=False,indent=2),encoding='utf-8')

readme='''# MC Vanilla 3D v8 (Java 1.21.11)\n\nResearch only; no original copyrighted Minecraft images/models redistributed.\n\n`00` Korean report, `01` per-block render evidence, `02` PNG metadata, `03` atlas sources, `04` category summary, `05` progress, `06` validations, cumulative SQLite, `build_v8.py` (the entire v8 build script).\n\nGit SHA-1 is Git blob ID, **not PNG SHA-256**.  Attached records are derived metadata from actual 1.21.11 repository files and 1.21.11 Yarn class metadata. No official Mojang client.jar hash verified.\n'''
(RESULT/'README.md').write_text(readme,encoding='utf-8')

with zipfile.ZipFile(ROOT/'마크_가구모델링_바닐라3D분석_v8_특수렌더_17블록.zip','w',compression=zipfile.ZIP_DEFLATED,compresslevel=8) as z:
    for f in RESULT.iterdir():
        if f.is_file(): z.write(f,arcname=f'{WORK.name}/results/{f.name}')
    z.write(__file__,arcname=f'{WORK.name}/results/build_v8.py')

with zipfile.ZipFile(ROOT/'마크_가구모델링_바닐라3D분석_v8_특수렌더_17블록.zip') as z:
    assert z.testzip() is None
    print('ZIP',z.filename, 'size',os.stat(z.filename).st_size, 'entries',len(z.namelist()))
print('SQLITE',DB.stat().st_size,'STATS',stats)
