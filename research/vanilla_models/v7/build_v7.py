#!/usr/bin/env python3
"""Builds a source-derived, selected-case vanilla multipart study v7.
Inputs: previously verified v6 SQLite + source observations recorded from the GitHub
connector for Minecraft Java Edition 1.21.11. It DOES NOT access game PNGs,
include copyrighted original model JSON, simulate game lighting, or assert full
Minecraft blockstate parity.
"""
from pathlib import Path
import sqlite3, json, csv, math, shutil, zipfile, hashlib
from collections import Counter
BASE=Path('/mnt/data')
OUT=BASE/'MC_vanilla_models_study_07'/'results'; OUT.mkdir(parents=True,exist_ok=True)
DB=OUT/'MC_Furniture_Style_Stage1_Research_v7.sqlite'
V6=BASE/'MC_vanilla_models_study_06'/'results'/'MC_Furniture_Style_Stage1_Research_v6.sqlite'
assert V6.is_file()
with sqlite3.connect(V6) as old, sqlite3.connect(DB) as new: old.backup(new)
REPO='https://github.com/InventivetalentDev/minecraft-assets/blob/1.21.11/assets/minecraft/'
SOURCE_STATES={
'oak_fence':'394851e1883d0bda305aa0b47b04b0e04716200a',
'cobblestone_wall':'ea2f67611565e206b85127251000594a4961101c',
'iron_bars':'37dfb9912c3d0123ce5f02f518da95070457437d',
'glass_pane':'d8f2900fd938b657359d8f6043904a76ec4da545',
'oak_shelf':'404c901695218478e0bc1df86b4c66538d118f56',
'oak_fence_gate':'872298ceb4c98e135aa951c57f142bcdd5e227e0',
'oak_stairs':'c20e7ef6c86dd57238f39cd51fc6b0c5bcc5b079',
'chiseled_bookshelf':'0c9b22b91093c4dfe3510a9a6aebe291df491e39'}
# Named models and parent template evidence (git blob SHA-1 from connector metadata).
MODEL_EVIDENCE={
'cobblestone_wall_post':('template_wall_post','7f47c03ff1834b840cff3ad017005692cd511dfe'),
'cobblestone_wall_side':('template_wall_side','f0eabd2b3a05eb78aedcfee14442007fdd8c2d78'),
'cobblestone_wall_side_tall':('template_wall_side_tall','d6f6625626ad01d6059db8ad1fa8088c3f80f278'),
'template_wall_post':('', 'c1c40e47e8d68d780da5a76cc7060ab61115b020'),
'template_wall_side':('', '301854c84411925511e45e977b448290a8d25956'),
'template_wall_side_tall':('','379a9e3cc92fab32b1247fc4e9af0781406a17cc'),
'iron_bars_post_ends':('template_bars_post_ends','a55271818fff1c4dc0ffeaa8a4ed6f342daa4874'),
'iron_bars_post':('template_bars_post','ac60ebe007ad230ae787c35e825f8e49615e43ed'),
'iron_bars_cap':('template_bars_cap','a2475f5e65927d52ea4c7bfe7c31cfff88cd9de1'),
'iron_bars_cap_alt':('template_bars_cap_alt','992c38e8ae793d5a9bc2bbca0b02a42ff317063a'),
'iron_bars_side':('template_bars_side','044bb4f0d693be164eba203f23a611dfbbaa1838'),
'iron_bars_side_alt':('template_bars_side_alt','1f0d7f92917881c9c66c6a57605ddd9fc2e6c444'),
'template_bars_post_ends':('','0e5871ac3d93bb2c7b000389c15c3c3f3f8cf85b'),
'template_bars_post':('','0f8c67c7f4150b02e9d2f3319d93b157d75e4c9c'),
'template_bars_cap':('','2c6279ce6cd1f25b6cfe15c8922165abbafa60c8'),
'template_bars_cap_alt':('','da342ff8f046103905480baddb66626b24da3a3d'),
'template_bars_side':('','66dbc1d7125939f3681d822e937614f2a513fdb5'),
'template_bars_side_alt':('','552424402eb36fc83e67f774deaae60e5711075c'),
'glass_pane_post':('template_glass_pane_post','6067b6a8c3c70b9b7ff28083c52503f644f9fdf7'),
'glass_pane_side':('template_glass_pane_side','0b03be05ea9da571c4666cf3692a630f2b927166'),
'glass_pane_side_alt':('template_glass_pane_side_alt','e8bd700f967c06b5ecf354a193b23c042c2a0442'),
'glass_pane_noside':('template_glass_pane_noside','dc01ef00458fcc1bd8a2d67dc90a71de0b7a1232'),
'glass_pane_noside_alt':('template_glass_pane_noside_alt','f0151c1baec3f69494b6760e2044ee585242b674'),
'template_glass_pane_post':('','54d7fa88ca46715fc7b77cdcc0118243c3948ebb'),
'template_glass_pane_side':('','fae06dcc6d4104788afc63cff079f2dfe56949eb'),
'template_glass_pane_side_alt':('','82d0e98e023182e6647a2f79717a4c70436f87b5'),
'template_glass_pane_noside':('','af16ff940878e9ace04595bc7026524f938bb64a'),
'template_glass_pane_noside_alt':('','771d694208bb99b37894a2e796323defe1a62b69'),
'oak_fence_gate':('template_fence_gate','74e6c4455979380a5c9c61b2a315a98209c9d1d2'),
'oak_fence_gate_open':('template_fence_gate_open','c3e37495f0e3c51668346fd9c54a43c4e036dfe5'),
'oak_fence_gate_wall':('template_fence_gate_wall','9c2c0f39ad50323c9f773ec2b79035d1658b0e5a'),
'oak_fence_gate_wall_open':('template_fence_gate_wall_open','2b5151791c57122cc38c7f8c6486ec42c1fb906b'),
'template_fence_gate':('','b1a090fa31c8d0cc6c2a135d706c5770805b3697'),
'template_fence_gate_open':('','af2062a116d5ed4c217035e43cede40d68c4534c'),
'template_fence_gate_wall':('','7b301338dc7f1edf8cd4c2e343ce8ffee141bb55'),
'template_fence_gate_wall_open':('','6fddae61c8f024c91717035ca77ccf324b4c96df'),
'oak_shelf_unconnected':('template_shelf_unconnected','f7e0246635a353d0e16784ad1445a4c8e6685e2a'),
'oak_shelf_left':('template_shelf_left','f93de7bab0f31486dc88528dd30f9991d06c1c66'),
'oak_shelf_center':('template_shelf_center','81892d5c8594124365625adfcffe321d4b9403f1'),
'oak_shelf_right':('template_shelf_right','8d21a41bfe2b341c45d4d94bb780b61ea8e5d2'),
'template_shelf_unconnected':('','3b82ae61468d0c2c15ea475a55a6e7b0d25864d2'),
'template_shelf_left':('','ecb099d693d75318303452a96a34d4a6ca4e83'),
'template_shelf_center':('','20b1449c2607d2f79c32b10d9a493b6b9cf8238b'),
'template_shelf_right':('','5e58b7f2c9c4a6ded052b3854a216de89b249201'),
'chiseled_bookshelf':('','a9bda72e10095343fb80de2bc4654212a1dc6834'),
'chiseled_bookshelf_occupied_slot_top_left':('template_chiseled_bookshelf_slot_top_left','85331c01dedeb9d94a1dde20212e93705acdead1'),
'chiseled_bookshelf_empty_slot_top_mid':('template_chiseled_bookshelf_slot_top_mid','19f44bc16e3f638acc0c79990bd80b4d3a0e8204'),
'template_chiseled_bookshelf_slot_top_left':('','da9fc59136a95d14a3fbe5eb363564b8fa45bf36'),
'template_chiseled_bookshelf_slot_top_mid':('','25cc8308d67d6223d455f6fca170a936208139fa'),
'template_chiseled_bookshelf_slot_top_right':('','077f1276e833d2d58f6e86ae590bfd3899717c91'),
'template_chiseled_bookshelf_slot_bottom_left':('','f224a1e88c819aa824c4cbe871f2b13a158a15ef'),
'template_chiseled_bookshelf_slot_bottom_mid':('','a1c54d921e6568eea038e0eac82d6bcaf136eff1'),
'template_chiseled_bookshelf_slot_bottom_right':('','5acdabdfa5ed0815ad7c0c588f19cea8dd5e8644'),
}
# Distilled geometry extracted from source model templates, not original game assets.
# Every primitive: [from_xyz, to_xyz]. Zero-thickness planes are intentional.
GEO={
'oak_fence_post':[[[6,0,6],[10,16,10]]],
'oak_fence_side':[[[7,12,0],[9,15,9]],[[7,6,0],[9,9,9]]],
'cobblestone_wall_post':[[[4,0,4],[12,16,12]]],
'cobblestone_wall_side':[[[5,0,0],[11,14,8]]],
'cobblestone_wall_side_tall':[[[5,0,0],[11,16,8]]],
'iron_bars_post_ends':[[[7,.001,7],[9,.001,9]],[[7,15.999,7],[9,15.999,9]]],
'iron_bars_post':[[[8,0,7],[8,16,9]],[[7,0,8],[9,16,8]]],
'iron_bars_cap':[[[8,0,8],[8,16,9]],[[7,0,9],[9,16,9]]],
'iron_bars_cap_alt':[[[8,0,7],[8,16,8]],[[7,0,7],[9,16,7]]],
'iron_bars_side':[[[8,0,0],[8,16,8]],[[7,0,0],[9,16,7]],[[7,.001,0],[9,.001,7]],[[7,15.999,0],[9,15.999,7]]],
'iron_bars_side_alt':[[[8,0,8],[8,16,16]],[[7,0,9],[9,16,16]],[[7,.001,9],[9,.001,16]],[[7,15.999,9],[9,15.999,16]]],
'glass_pane_post':[[[7,0,7],[9,16,9]]],
'glass_pane_side':[[[7,0,0],[9,16,7]]],
'glass_pane_side_alt':[[[7,0,9],[9,16,16]]],
'glass_pane_noside':[[[7,0,7],[9,16,9]]],
'glass_pane_noside_alt':[[[7,0,7],[9,16,9]]],
'oak_shelf':[[[0,0,13],[16,16,16]],[[0,0,11],[16,4,13]],[[0,12,11],[16,16,13]]],
'oak_shelf_unpowered':[[[0,4,13],[16,12,13]]],
'oak_shelf_unconnected':[[[0,4,13],[16,12,13]]],
'oak_shelf_left':[[[0,4,13],[16,12,13]]],
'oak_shelf_center':[[[0,4,13],[16,12,13]]],
'oak_shelf_right':[[[0,4,13],[16,12,13]]],
'chiseled_bookshelf':[[[0,0,0],[16,16,16]]],
'oak_stairs':[[[0,0,0],[16,8,16]],[[8,8,0],[16,16,16]]],
'oak_stairs_inner':[[[0,0,0],[16,8,16]],[[8,8,0],[16,16,16]],[[0,8,8],[8,16,16]]],
}
GEO['oak_fence_gate']=[[[0,5,7],[2,16,9]],[[14,5,7],[16,16,9]],[[6,6,7],[8,15,9]],[[8,6,7],[10,15,9]],[[2,6,7],[6,9,9]],[[2,12,7],[6,15,9]],[[10,6,7],[14,9,9]],[[10,12,7],[14,15,9]]]
GEO['oak_fence_gate_wall_open']=[[[0,2,7],[2,13,9]],[[14,2,7],[16,13,9]],[[0,3,13],[2,12,15]],[[14,3,13],[16,12,15]],[[0,3,9],[2,6,13]],[[0,9,9],[2,12,13]],[[14,3,9],[16,6,13]],[[14,9,9],[16,12,13]]]
SLOTS={
 'top_left':[[10,8,0],[16,16,0]],'top_mid':[[5,8,0],[10,16,0]],'top_right':[[0,8,0],[5,16,0]],
 'bottom_left':[[10,0,0],[16,8,0]],'bottom_mid':[[5,0,0],[10,8,0]],'bottom_right':[[0,0,0],[5,8,0]]
}
for key,volume in SLOTS.items():
 for status in ['occupied','empty']: GEO[f'chiseled_bookshelf_{status}_slot_{key}']=[volume]
# Source-derived conditional selection rules for selected examples, not full copied JSON.
RULES={}
def add(b,entry,when,model,y=0,x=0,uvlock=False): RULES.setdefault(b,[]).append(dict(entry=entry,when=when,model=model,y=y,x=x,uvlock=bool(uvlock)))
add('oak_fence',0,{},'oak_fence_post')
for i,d in enumerate('north east south west'.split(),1):add('oak_fence',i,{d:'true'},'oak_fence_side',90*(i-1),uvlock=True)
add('cobblestone_wall',0,{'up':'true'},'cobblestone_wall_post')
for idx,typ in enumerate(['low','tall']):
 for j,d in enumerate('north east south west'.split()): add('cobblestone_wall',1+idx*4+j,{d:typ},'cobblestone_wall_side'+('_tall' if typ=='tall' else ''),j*90,uvlock=True)
add('iron_bars',0,{},'iron_bars_post_ends')
add('iron_bars',1,{d:'false' for d in 'east north south west'.split()},'iron_bars_post')
for i,d in enumerate('north east south west'.split(),2):
 when={z:('true' if z==d else 'false') for z in 'east north south west'.split()}
 add('iron_bars',i,when,'iron_bars_cap' if d in ['north','east'] else 'iron_bars_cap_alt',90 if d in ['east','west'] else 0)
for i,d in enumerate('north east south west'.split(),6):add('iron_bars',i,{d:'true'},'iron_bars_side' if d in ['north','east'] else 'iron_bars_side_alt',90 if d in ['east','west'] else 0)
add('glass_pane',0,{},'glass_pane_post')
for i,d in enumerate('north east south west'.split(),1):add('glass_pane',i,{d:'true'},'glass_pane_side' if d in ['north','east'] else 'glass_pane_side_alt',90 if d in ['east','west'] else 0)
# false directions have specialized cap UV and rotation; exact source entry mapping.
for i,d,name,y in [(5,'north','glass_pane_noside',0),(6,'east','glass_pane_noside_alt',0),(7,'south','glass_pane_noside_alt',90),(8,'west','glass_pane_noside',270)]:add('glass_pane',i,{d:'false'},name,y)
for fi,d in enumerate('north east south west'.split()):
 add('oak_shelf',fi,{'facing':d},'oak_shelf',fi*90)
 add('oak_shelf',fi+4,{'facing':d,'powered':'false'},'oak_shelf_unpowered',fi*90)
 for k,key in enumerate(['unconnected','left','center','right']): add('oak_shelf',fi+8+4*k,{'facing':d,'powered':'true','side_chain':key},'oak_shelf_'+key,fi*90)
for fi,d in enumerate('north east south west'.split()):
 add('chiseled_bookshelf',fi*13,{'facing':d},'chiseled_bookshelf',fi*90,uvlock=True)
 for si,slot in enumerate(SLOTS):
  for v in [True,False]:
   # 1 based indices; each slot has occupied, empty state in source
   entry=fi*13+1+si*2+(0 if v else 1)
   add('chiseled_bookshelf',entry,{'facing':d,f'slot_{si}_occupied':str(v).lower()},f'chiseled_bookshelf_{"occupied" if v else "empty"}_slot_{slot}',fi*90)
# Variant entries from observed GitHub blockstate JSON. Order of fields is irrelevant for key matching.
VARIANTS={
('oak_fence_gate','closed_north'): [('oak_fence_gate',0,180,True)],
('oak_fence_gate','open_east_wall'): [('oak_fence_gate_wall_open',0,270,True)],
('oak_stairs','straight_north'): [('oak_stairs',0,270,True)],
('oak_stairs','inner_east'): [('oak_stairs_inner',0,270,True)],
}
SCENARIOS={
'oak_fence': [('isolated',dict(north=False,east=False,south=False,west=False)),('east',dict(north=False,east=True,south=False,west=False)),('north_east',dict(north=True,east=True,south=False,west=False))],
'cobblestone_wall':[('isolated',dict(up=True,north='none',east='none',south='none',west='none')),('low_north',dict(up=True,north='low',east='none',south='none',west='none')),('low_n_tall_e',dict(up=True,north='low',east='tall',south='none',west='none')),('no_post_east_tall',dict(up=False,north='none',east='tall',south='none',west='none'))],
'iron_bars':[('isolated',dict(north=False,east=False,south=False,west=False)),('north_only',dict(north=True,east=False,south=False,west=False)),('north_east',dict(north=True,east=True,south=False,west=False))],
'glass_pane':[('isolated',dict(north=False,east=False,south=False,west=False)),('north_only',dict(north=True,east=False,south=False,west=False)),('north_east',dict(north=True,east=True,south=False,west=False))],
'oak_shelf':[('inactive_north',dict(facing='north',powered=False,side_chain='unconnected')),('active_center_east',dict(facing='east',powered=True,side_chain='center')),('active_left_south',dict(facing='south',powered=True,side_chain='left'))],
'oak_fence_gate':[('closed_north',dict(facing='north',in_wall=False,open=False)),('open_east_wall',dict(facing='east',in_wall=True,open=True))],
'oak_stairs':[('straight_north',dict(facing='north',half='bottom',shape='straight')),('inner_east',dict(facing='east',half='bottom',shape='inner_left'))],
'chiseled_bookshelf':[('mixed_north',dict(facing='north',slot_0_occupied=True,slot_1_occupied=False,slot_2_occupied=False,slot_3_occupied=True,slot_4_occupied=False,slot_5_occupied=True))]
}
EXPECT={('oak_fence','isolated'):1,('oak_fence','east'):2,('oak_fence','north_east'):3,('cobblestone_wall','isolated'):1,('cobblestone_wall','low_north'):2,('cobblestone_wall','low_n_tall_e'):3,('cobblestone_wall','no_post_east_tall'):1,('iron_bars','isolated'):2,('iron_bars','north_only'):3,('iron_bars','north_east'):3,('glass_pane','isolated'):5,('glass_pane','north_only'):5,('glass_pane','north_east'):5,('oak_shelf','inactive_north'):2,('oak_shelf','active_center_east'):2,('oak_shelf','active_left_south'):2,('oak_fence_gate','closed_north'):1,('oak_fence_gate','open_east_wall'):1,('oak_stairs','straight_north'):1,('oak_stairs','inner_east'):1,('chiseled_bookshelf','mixed_north'):7}
# End-to-end independently recorded expected model selections from connector-side evaluation.
EXPECTED_PICKS={
('oak_fence','north_east'):['oak_fence_post','oak_fence_side','oak_fence_side'],
('cobblestone_wall','low_n_tall_e'):['cobblestone_wall_post','cobblestone_wall_side','cobblestone_wall_side_tall'],
('iron_bars','north_only'):['iron_bars_post_ends','iron_bars_cap','iron_bars_side'],
('iron_bars','north_east'):['iron_bars_post_ends','iron_bars_side','iron_bars_side'],
('glass_pane','isolated'):['glass_pane_post','glass_pane_noside','glass_pane_noside_alt','glass_pane_noside_alt','glass_pane_noside'],
('oak_shelf','active_center_east'):['oak_shelf','oak_shelf_center'],
('chiseled_bookshelf','mixed_north'):['chiseled_bookshelf','chiseled_bookshelf_occupied_slot_top_left','chiseled_bookshelf_empty_slot_top_mid','chiseled_bookshelf_empty_slot_top_right','chiseled_bookshelf_occupied_slot_bottom_left','chiseled_bookshelf_empty_slot_bottom_mid','chiseled_bookshelf_occupied_slot_bottom_right']}

def matched(rule,props):return all(str(props.get(k)).lower()==str(v).lower() for k,v in rule.items())
def rotated_bounds(lo,hi,rx,ry):
 # Blockstate model transforms about block center, aligned to 90 degree for all 21 cases.
 # Convert each of 8 original bbox corners; round to exact nearest integer when possible.
 xrad=math.radians(rx); yrad=math.radians(ry)
 points=[]
 for a in (lo[0],hi[0]):
  for b in (lo[1],hi[1]):
   for c in (lo[2],hi[2]):
    x,y,z=a-8,b-8,c-8
    y,z=y*math.cos(xrad)-z*math.sin(xrad), y*math.sin(xrad)+z*math.cos(xrad)
    x,z=x*math.cos(yrad)+z*math.sin(yrad),-x*math.sin(yrad)+z*math.cos(yrad)
    points.append([x+8,y+8,z+8])
 return [[round(min(p[k] for p in points),6) for k in range(3)],[round(max(p[k] for p in points),6) for k in range(3)]]

def j(o):return json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':'))
with sqlite3.connect(DB) as con:
 con.executescript('''
 CREATE TABLE IF NOT EXISTS connected_sources_v7 (path TEXT PRIMARY KEY, git_blob_sha1 TEXT NOT NULL, version TEXT, validation TEXT, url TEXT);
 CREATE TABLE IF NOT EXISTS connected_geometry_v7 (model TEXT PRIMARY KEY, parent_template TEXT, source_sha1 TEXT, primitive_count INTEGER, primitive_boxes_json TEXT, observation TEXT);
 CREATE TABLE IF NOT EXISTS assembly_cases_v7 (block TEXT, case_id TEXT, props_json TEXT, source_blockstate_sha1 TEXT, selection_kind TEXT, applied_model_count INTEGER, primitive_count INTEGER, zero_thickness_primitive_count INTEGER, bounds_from_json TEXT, bounds_to_json TEXT, method TEXT, PRIMARY KEY(block,case_id));
 CREATE TABLE IF NOT EXISTS assembly_parts_v7 (block TEXT, case_id TEXT, part_ordinal INTEGER, selected_model TEXT, source_rule_ordinal TEXT, x_rotation INTEGER, y_rotation INTEGER, uvlock INTEGER, primitive_count INTEGER, from_rotated_json TEXT, to_rotated_json TEXT, PRIMARY KEY(block,case_id,part_ordinal));
 CREATE TABLE IF NOT EXISTS assembly_primitives_v7 (block TEXT, case_id TEXT, part_ordinal INTEGER, primitive_ordinal INTEGER, model TEXT, unrotated_from_json TEXT, unrotated_to_json TEXT, rotated_from_json TEXT, rotated_to_json TEXT, zero_thickness INTEGER, PRIMARY KEY(block,case_id,part_ordinal,primitive_ordinal));
 CREATE TABLE IF NOT EXISTS research_limits_v7 (issue TEXT PRIMARY KEY, detail TEXT, status TEXT);
 ''')
 for b,sha in SOURCE_STATES.items():
  p=f'assets/minecraft/blockstates/{b}.json';url=REPO+f'blockstates/{b}.json'
  con.execute('INSERT OR REPLACE INTO connected_sources_v7 VALUES (?,?,?,?,?)',(p,sha,'java_1.21.11','GitHub_connector_JSON_read',url))
  con.execute('INSERT OR REPLACE INTO sources VALUES (?,?,?,?,?)',(p,sha,url,'blockstate','GitHub_connector_read_2026-11-12'))
 for n,(parent,sha) in MODEL_EVIDENCE.items():
  p=f'assets/minecraft/models/block/{n}.json';url=REPO+f'models/block/{n}.json'
  con.execute('INSERT OR REPLACE INTO connected_sources_v7 VALUES (?,?,?,?,?)',(p,sha,'java_1.21.11','GitHub_connector_JSON_read',url))
  con.execute('INSERT OR REPLACE INTO sources VALUES (?,?,?,?,?)',(p,sha,url,'model','GitHub_connector_read_2026-11-12'))
 for n,boxes in GEO.items():
  parent,sha=MODEL_EVIDENCE.get(n,('',None))
  if not sha:
   row=con.execute('SELECT github_blob_sha1 FROM sources WHERE path=?',(f'assets/minecraft/models/block/{n}.json',)).fetchone()
   sha=row[0] if row else None
  con.execute('INSERT INTO connected_geometry_v7 VALUES (?,?,?,?,?,?)',(n,parent,sha,len(boxes),j(boxes),'direct_or_parent_inherited_geometry; zero-thickness allowed'))
 for b,cases in SCENARIOS.items():
  for case,p in cases:
   selected=[]
   if b in RULES:
    for rule in RULES[b]:
     if matched(rule['when'],p):selected.append(rule)
   else:
    for idx,(name,x,y,uvlock) in enumerate(VARIANTS[(b,case)]):selected.append(dict(model=name,x=x,y=y,uvlock=uvlock,entry=f'variant_{idx}'))
   assert len(selected)==EXPECT[(b,case)],(b,case,len(selected))
   assert [r['model'] for r in selected]==EXPECTED_PICKS.get((b,case),[r['model'] for r in selected]),(b,case,selected)
   total=zero=0; bounds=[]
   for pi,r in enumerate(selected):
    model=r['model'];boxes=GEO.get(model)
    assert boxes,('missing geometry',model)
    bxs=[]
    for ei,(lo,hi) in enumerate(boxes):
     a,c=rotated_bounds(lo,hi,r['x'],r['y']);bxs.append((a,c));zero_dims=int(any(abs(hi[k]-lo[k])<1e-9 for k in range(3)))
     zero+=zero_dims;total+=1;bounds.append((a,c))
     con.execute('INSERT INTO assembly_primitives_v7 VALUES (?,?,?,?,?,?,?,?,?,?)',(b,case,pi,ei,model,j(lo),j(hi),j(a),j(c),zero_dims))
    a=[min(lo[k] for lo,hi in bxs) for k in range(3)];c=[max(hi[k] for lo,hi in bxs) for k in range(3)]
    con.execute('INSERT INTO assembly_parts_v7 VALUES (?,?,?,?,?,?,?,?,?,?,?)',(b,case,pi,model,str(r['entry']),r['x'],r['y'],int(r['uvlock']),len(boxes),j(a),j(c)))
   mn=[min(lo[k] for lo,hi in bounds) for k in range(3)];mx=[max(hi[k] for lo,hi in bounds) for k in range(3)]
   con.execute('INSERT INTO assembly_cases_v7 VALUES (?,?,?,?,?,?,?,?,?,?,?)',(b,case,j(p),SOURCE_STATES[b],'multipart' if b in RULES else 'variants',len(selected),total,zero,j(mn),j(mx),'state_condition_evaluated; blockstate x/y 90degree pivot=8; geometry from resolved templates; NOT actual rendered screenshot'))
 limits={
 'L01':'공식 Mojang client.jar와 JSON/PNG 바이트 대조 미수행: 현재 비공식 GitHub 에셋 기준',
 'L02':'선택한 상태 21개 조건 평가이며 모든 가능한 조합의 게임 중 런타임 상태 생성 규칙까지 검증한 것은 아님',
 'L03':'게임 내 조명, biome tint, AO, 재질/반투명 합성, 2면 셰이딩, 실제 렌더링 테스트 미수행',
 'L04':'UVlock=true는 상태값만 기록; 면 노멀 및 텍스처 픽셀 회전을 계산해 렌더러와 교차검증하지 않음',
 'L05':'blockstate rotation AABB는 직접 형상 정의에 대한 단순 기하학 변환이며 collision shape 아님',
 'L06':'Special renderer(상자/침대/표지판)와 모드 가구 에셋 분석 미시작'
 }
 for issue,desc in limits.items():con.execute('INSERT INTO research_limits_v7 VALUES (?,?,?)',(issue,desc,'OPEN'))
 con.commit()
 assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
 # verify no orphans, expected 21 cases
 assert con.execute('select count(*) from assembly_cases_v7').fetchone()[0]==21
 assert con.execute('select count(*) from assembly_parts_v7').fetchone()[0]==sum(EXPECT.values())
 assert con.execute('select count(*) from assembly_primitives_v7').fetchone()[0]==con.execute('select sum(primitive_count) from assembly_cases_v7').fetchone()[0]
 cases_rows=con.execute('SELECT block,case_id,props_json,selection_kind,applied_model_count,primitive_count,zero_thickness_primitive_count,bounds_from_json,bounds_to_json FROM assembly_cases_v7 ORDER BY block,case_id').fetchall()
 parts_rows=con.execute('SELECT block,case_id,part_ordinal,selected_model,source_rule_ordinal,x_rotation,y_rotation,uvlock,primitive_count,from_rotated_json,to_rotated_json FROM assembly_parts_v7 ORDER BY block,case_id,part_ordinal').fetchall()
 prim_rows=con.execute('SELECT * FROM assembly_primitives_v7 ORDER BY block,case_id,part_ordinal,primitive_ordinal').fetchall()
 sources_rows=con.execute('SELECT * FROM connected_sources_v7 ORDER BY path').fetchall()
 geo_rows=con.execute('SELECT * FROM connected_geometry_v7 ORDER BY model').fetchall()
 def csv_dump(name,headers,rows):
  p=OUT/name
  with p.open('w',encoding='utf-8-sig',newline='') as f:
   wr=csv.writer(f);wr.writerow(headers);wr.writerows(rows)
  return p
 csv_dump('01_v7_상태별_최종조립_21사례.csv',['block','case_id','props_json','selection_kind','model_parts','geometry_elements','zero_thickness_elements','bound_min','bound_max'],cases_rows)
 csv_dump('02_v7_선택모델_부품별.csv',['block','case_id','part_order','model','source_rule_index','x_rot','y_rot','uvlock','element_count','bound_min','bound_max'],parts_rows)
 csv_dump('03_v7_회전요소_좌표.csv',['block','case_id','part_order','element_index','model','source_from','source_to','rotated_from','rotated_to','zero_thickness'],prim_rows)
 csv_dump('04_v7_원본경로_해시.csv',['path','git_blob_sha1','version','check','url'],sources_rows)
 csv_dump('05_v7_모델별_구조정의.csv',['model','parent_template','sha1','elements','boxes_json','note'],geo_rows)
 stats={
 'source_repo':'InventivetalentDev/minecraft-assets','source_tag':'1.21.11',
 'case_count':len(cases_rows),'case_block_types':len(set(r[0] for r in cases_rows)),
 'model_part_instances':len(parts_rows),'geometry_element_instances':len(prim_rows),
 'plane_instances':sum(r[-1] for r in prim_rows),
 'models_with_geometry':len(geo_rows),
 'source_evidence_entries':len(sources_rows),
 'prior_texture_samples':con.execute('select count(*) from texture_stats_v4').fetchone()[0],
 'prior_model_files':con.execute('select count(*) from models').fetchone()[0]+con.execute('select count(*) from model_additions_v6').fetchone()[0],
 'prior_blockstate_files':con.execute('select count(*) from blockstates').fetchone()[0]+con.execute('select count(*) from state_additions_v6').fetchone()[0],
 'cumulative_source_paths':con.execute('select count(*) from sources').fetchone()[0],
 'official_jar_crosschecks':0,
 'ingame_render_verifications':0,
 'v7_verification':'selected scenario matches independently calculated GitHub connector evaluations; SQLite integrity+zip CRC checked'
 }
 (OUT/'06_v7_통계_검증현황.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2),encoding='utf-8')
 # Progress docs
 md=f'''# 마인크래프트 바닐라 3D v7 — 연결 상태·부품 조립 분석

- 기준: **Java Edition 1.21.11** 비공식 추출 에셋, [InventivetalentDev GitHub](https://github.com/InventivetalentDev/minecraft-assets/tree/1.21.11/assets/minecraft)
- 계승: v6 SQLite(기존 150종 텍스처, 모델 파일 68, 블록상태 23, UV 면 90)
- 오늘 신규 분석: **8가지 블록 유형, {stats['case_count']}개 상태 사례, 선택 모델 {stats['model_part_instances']}개 인스턴스, 기하 요소 {stats['geometry_element_instances']}개 인스턴스**
- 이번 조사에서 직접 확인한 근거 메타데이터: **{stats['source_evidence_entries']}개 원본 경로/해시 기록**. v6와 중복 포함.
- 누적 DB 출처 경로: **{stats['cumulative_source_paths']}개**. 텍스처 150종은 v4의 분석 통계만 계승했으며 공식 JAR 대조 미수행.

## 1. 상태별 최종 모델 선택 (실측과 계산)

| 블록 상태 사례 | 선택 모델 수 | 합산 직육면체/평면 요소 수 | 설명 |
|---|---:|---:|---|
'''
 showcase=[('oak_fence','isolated','독립 울타리 기둥'),('oak_fence','north_east','북·동 울타리 2방향 연결'),('cobblestone_wall','low_n_tall_e','낮은 북쪽 벽 + 높은 동쪽 벽'),('iron_bars','north_only','단방향 연결과 끝마감'),('iron_bars','north_east','2방향 연결, 끝마감 변경'),('glass_pane','isolated','고립 유리판도 cap 평면 포함'),('oak_shelf','active_center_east','동쪽 방향, 작동 중, 가운데 연결'),('oak_fence_gate','open_east_wall','담장 연결 상태의 열린 문'),('oak_stairs','inner_east','안쪽 코너 계단 3요소'),('chiseled_bookshelf','mixed_north','6개 슬롯에 대해 각각 면 선택')]
 lookup={(r[0],r[1]):r for r in cases_rows}
 for b,c,note in showcase:
  r=lookup[(b,c)];md+=f'| `{b}` / `{c}` | {r[4]} | {r[5]} | {note} |\n'
 md+='''
**주의:** 적용 모델 수와 직육면체 수는 다르다. 예를 들어 철창의 모델은 하나가 2~4개의 평면으로 이루어져 있고, 끌로 조각한 책장은 앞면에 겹쳐지는 슬롯 표시가 포함된다. 기하 요소 수는 실제 게임의 픽셀 수나 면 삼각형 개수와 다르다.

## 2. 실제 조건부 조립에서 확인한 특징

1. **울타리**: 기둥이 기본으로 들어가고 `north/east/south/west=true`인 방향의 연결 부품이 각각 추가된다.
2. **담장**: `up=true`일 때 기둥을 넣고, 방향별 `low` 또는 `tall` 연결 부품이 서로 다른 높이로 추가된다.
3. **철창**: 중앙의 위/아래 끝면 부품은 항상 존재하고, 네 방향이 모두 끊기면 독립 기둥 2평면을 추가한다. 한 방향만 연결되면 `cap`과 `side`가 같이 선택된다.
4. **유리판**: `post` 외에 연결 방향의 `side` 또는 끊긴 방향의 `noside`를 적용한다. 모델 선택 5개가 동일해도 실제 가시 면은 다르다.
5. **선반**: 모든 방향에 기본 본체를 배치하고, `powered`와 `side_chain` 상태에 따라 추가로 1개의 정면 평면을 선택한다. 32×32 텍스처에서 UV를 재사용하는 사례와 연결된다.
6. **끌로 조각한 책장**: 본체 1개에 여섯 슬롯마다 `occupied` 또는 `empty`인 얇은 평면을 선택한다. 부분적 텍스처 교체를 매번 완전한 3D 모델로 다시 제작하지 않는다.
7. **계단/울타리문**: `variants`에서는 해당 상태에 맞는 모델을 **하나** 골라 회전한다. 계단의 최종 기하 구성은 직선형 2요소, 안쪽 모서리형 3요소다.

## 3. 모델 좌표와 UV의 분리

- blockstate `x`,`y`: 모델 자체를 중심(8,8,8) 기준으로 회전. 90도 배수인 이번 사례 21건의 요소별 회전 후 AABB 계산.
- JSON 모델 `element`의 `from/to`: 회전 전 요소 상자, 물리 충돌 정보가 아님.
- 모델 면의 `faces.*.uv`: 해당 면이 텍스처 이미지의 어느 위치를 참조할지 결정. `uvlock=true`는 별도로 기록했으나 텍스처 픽셀 자체의 최종 회전·광원은 계산하지 않았다.
- 두께 0인 판형 요소도 모델을 구성하는 **한 개 요소**로 기록했다. 이들을 양산 가능한 가구의 법칙이라고 단정하지 않는다.

## 4. 검증과 미완료

- 21개 상태 사례의 모델 선택/회전은 GitHub 원본 조건을 읽어 별도로 평가한 결과와 대조하고, 코드에서 선택 모델 수·대표 선택 모델 순서를 검증.
- 기존 v6를 SQLite 백업한 뒤 신규 테이블 추가: 원본과 구버전 표를 덮어쓰지 않음.
- SQLite integrity_check 통과, CSV·ZIP 재검사.
- **미완료:** Mojang 공식 `client.jar`와 직접 SHA 비교, 실제 게임에서 조명·UVlock·상태 렌더 검증, 모델 카탈로그 전체 전수 확인, 특수 렌더 대상, 가구 모드 분석.

## 5. 다음 분석

- 대표 블록의 방향별 면 텍스처 UV 회전 규칙 심화, `uvlock`/Face-UV를 인게임 화면과 대조할 수 있는 검수 사례 축적
- 바닐라 JSON 모델과 특수 렌더 구분 정리(상자/침대/표지판)
- 02단계 대상의 대표성·완료 기준을 확정한 다음 03단계 가구 모드 모델 실측으로 이동

### 파일

`01` 상태별 조립 CSV, `02` 선택 모델 CSV, `03` 회전 후 요소 CSV, `04` 근거 경로 CSV, `05` 모델 구조 CSV, `06` 검증 JSON, 누적 SQLite, v7 재현 스크립트.

**저작권 유의:** 원본 게임 JSON이나 PNG 파일 자체를 번들에 포함하지 않는다. 출처와 측정 수치만 보존.
'''
 (OUT/'00_v7_연결형_조립분석_보고서.md').write_text(md,encoding='utf-8')
 progress=f'''# 마인크래프트 가구 모델링 학습 — v7 진행도 (2026-11-12)

| 단계 | 현황 | 정량 근거 | 완료 판단 |
|---|---|---|---|
| 01 바닐라 재질·텍스처 | 150/150 표본 수집·측정 달성 | v4 계승, 공식 JAR 대조 0/150 | **표본만 100%**, 최종 검증 보류 |
| 02 바닐라 모델·UV·상태 | v7 진행 중 | v6 68모델·23상태·UV 90면 계승 + v7 21개 조립 사례, {stats['geometry_element_instances']}개 요소 인스턴스 | 전수/특수렌더/인게임 미완료; 퍼센트 미부여 |
| 03 가구 모드 모델 | 미시작 | 0 | 미완료 |
| 04 가구 모드 텍스처·UV | 미시작 | 0 | 미완료 |
| 05 바닐라와 모드 비교 검증 | 미시작 | 0 | 미완료 |

**단계 확정 완료 0/5개, 진행 중 2/5개, 미시작 3/5개.** 원본 에셋과 독립 검증 대조가 끝나기 전에는 01 전체를 최종 완료로 처리하지 않는다.

현재 02의 퍼센트는 정확한 분모(필수 모델과 상태 범위)가 확정되지 않았으므로 계산하지 않았다. 모드 모델 분석과 좀보이드 가구 제작은 실시하지 않음.
'''
 (OUT/'07_v7_학습_진행도.md').write_text(progress,encoding='utf-8')
 (OUT/'README.md').write_text('# v7 연구 데이터\n\n이 패키지는 v6 연구 DB를 계승한 선택 블록상태 분석 자료입니다. PNG나 원본 Minecraft 모델 JSON은 포함하지 않습니다. 01~05 CSV 및 SQLite는 공개된 GitHub 추출 에셋에서 관찰한 21개 사례를 파생한 수치 자료이며 게임 전체의 조합을 뜻하지 않습니다.\n',encoding='utf-8')
# We distribute the script as text for reproducibility (all extraction snapshots are derived observations).
shutil.copy2(Path(__file__),OUT/'build_v7.py')
archive=BASE/'마크_바닐라3D분석_v7_연결형조립_21사례.zip'
with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=8) as z:
 for p in sorted(OUT.iterdir()):
  if p.is_file(): z.write(p,arcname='MC_vanilla_models_study_07/results/'+p.name)
with zipfile.ZipFile(archive) as z:
 assert z.testzip() is None
 assert len(z.namelist())==len([p for p in OUT.iterdir() if p.is_file()])
with sqlite3.connect(DB) as c:
 assert c.execute('pragma integrity_check').fetchone()[0]=='ok'
print('OUTPUT',archive)
print('STATS',json.dumps(stats,ensure_ascii=False,indent=2))
print('CASES',[(x[0],x[1],x[4],x[5]) for x in cases_rows])
