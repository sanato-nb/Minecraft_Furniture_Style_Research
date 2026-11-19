"""Reconcile the 8 missing references and 16 alternatives with live Fabric evidence."""
from argparse import ArgumentParser
from collections import Counter
import csv
from hashlib import sha1, sha256
import json
import lzma
from pathlib import Path
import sqlite3
from zipfile import ZipFile

HERE = Path(__file__).resolve().parent
PHASE = HERE.parent
E_DB = PHASE/'entry04/research_texture_uv.sqlite.xz'
F_DB = PHASE.parent/'phase_1-3/F/furniture_research.sqlite.xz'
UV_SUPPORT = PHASE/'C_followup/UV_SOURCE_SUPPORT.csv.xz'
MOD_SHA1 = 'c2f992081bdc4795ed6d87771a3b5f7c71103785'
AF = 'another_furniture:'
MISSING = 'minecraft:missingno'


def read_csv(path, delimiter=','):
    with path.open(encoding='utf-8',newline='') as stream:
        return list(csv.DictReader(stream,delimiter=delimiter))


def make_csv(path, fields, rows):
    with path.open('w',encoding='utf-8',newline='') as stream:
        writer=csv.writer(stream,lineterminator='\n')
        writer.writerow(fields.split())
        writer.writerows(rows)


def connect(path):
    db=sqlite3.connect(':memory:')
    db.deserialize(lzma.decompress(path.read_bytes()))
    db.execute('PRAGMA foreign_keys=ON')
    return db


def model_use(db, resource):
    return db.execute('''
        SELECT COUNT(DISTINCT s.model_key),COALESCE(SUM(s.face_count),0),
        COUNT(DISTINCT s.model_key) FILTER
            (WHERE EXISTS(SELECT 1 FROM option o WHERE o.model_key=s.model_key))
        FROM texture t JOIN model_slot s ON s.texture_id=t.id
        WHERE t.resource_id=? AND t.minecraft='1.21.1'
    ''',(resource,)).fetchone()


def candidate_bindings(db, resource):
    return db.execute('''
        SELECT m.resource_id,s.slot,s.face_count,
        (SELECT count(*) FROM option WHERE model_key=s.model_key)
        FROM texture t JOIN model_slot s ON s.texture_id=t.id
        JOIN model m ON m.model_key=s.model_key
        WHERE t.resource_id=? AND t.minecraft='1.21.1'
        ORDER BY 1,2
    ''',(resource,)).fetchall()


def assets_path(id):
    namespace,path=id.split(':',1)
    return f'assets/{namespace}/textures/{path}.png'


def git_blob(data):
    return sha1(f'blob {len(data)}\0'.encode()+data).hexdigest()


def main():
    parser=ArgumentParser(description=__doc__)
    for flag in ('atlas','fabric','out'):
        parser.add_argument('--'+flag,type=Path,required=True)
    args=parser.parse_args()
    args.out.mkdir(parents=True,exist_ok=True)
    e=connect(E_DB)
    f=connect(F_DB)
    assert sha1(args.fabric.read_bytes()).hexdigest()==MOD_SHA1
    runtime=read_csv(args.atlas,'\t')
    identity={(r['kind'],r['requested'],r['properties']) for r in runtime}
    assert len(identity)==len(runtime)
    sprites={r['requested']:r['sprite'] for r in runtime if r['kind']=='SPRITE'}
    assert sprites.get(MISSING)==MISSING and sprites.get('minecraft:block/iron_block')=='minecraft:block/iron_block'
    oak=[r for r in runtime if r['kind']=='BLOCK' and r['requested']==AF+'oak_chair']
    assert oak and all(r['status']=='BAKED' and r['quad_sprites'] for r in oak)
    quad_use=Counter(s for row in oak for s in row['quad_sprites'].split('|'))
    assert not quad_use[MISSING]
    item=[r for r in runtime if r['kind']=='ITEM' and r['requested']==AF+'stone_tombstone']
    assert len(item)==1 and item[0]['status']=='NOT_REGISTERED'
    bell={r['sprite'] for r in runtime if r['kind']=='BLOCK' and r['requested']==AF+'service_bell' and r['status']=='BAKED'}
    assert bell=={AF+'block/service_bell'}
    item_bell={r['sprite'] for r in runtime if r['kind']=='ITEM' and r['requested']==AF+'service_bell' and r['status']=='BAKED'}
    assert item_bell=={'minecraft:block/iron_block'}

    missing,candidates,bindings,chair_state_refs=[],[],[],[]
    with ZipFile(args.fabric) as jar:
        names=set(jar.namelist())
        atlas_files={p for p in names if p.startswith('assets/') and '/atlases/' in p and p.endswith('.json')}
        assert not atlas_files,atlas_files
        model_docs={p:json.loads(jar.read(p)) for p in names
                    if p.startswith('assets/another_furniture/models/') and p.endswith('.json')}
        declared=Counter(str(value) for model in model_docs.values() for value in model.get('textures',{}).values())
        for tid,resource,faces in e.execute('''
            SELECT x.texture_id,t.resource_id,x.face_instances
            FROM texture_exception x JOIN texture t ON t.id=x.texture_id
            WHERE x.finding LIKE 'MISSING%' ORDER BY x.texture_id
        '''):
            assert assets_path(resource) not in names and sprites[resource]==MISSING
            missing.append((tid,resource,faces,sprites[resource],'ORIGINAL_ID_FALLBACK'))
        for tid,path,pinned in e.execute('SELECT texture_id,path,sha FROM alternate_asset ORDER BY 1,2'):
            resource=AF+path.split('/textures/',1)[1].removesuffix('.png')
            actual_hash=git_blob(jar.read(assets_path(resource)))
            assert actual_hash==pinned
            models,faces,direct=model_use(f,resource)
            if direct:
                label='USED_IN_REGISTERED_OAK_CHAIR'
                assert quad_use[resource] and sprites[resource]==resource
            else:
                label='UNUSED_ALTERNATIVE'
                assert not declared[resource] and not quad_use[resource] and models==faces==0
            candidates.append((tid,path,resource,actual_hash,models,faces,direct,sprites[resource],quad_use[resource],label))
            bindings.extend(((resource,*row) for row in candidate_bindings(f,resource)))

    pinned_choices={}
    for selector,model in f.execute('''
        SELECT r.selector,m.resource_id FROM state s JOIN rule r ON r.state_id=s.id
        JOIN option o ON o.state_id=s.id AND o.rule_index=r.rule_index
        JOIN model m ON m.model_key=o.model_key WHERE s.state_id=? ORDER BY r.rule_index
    ''',(AF+'oak_chair',)):
        assert selector not in pinned_choices
        pinned_choices[selector]=model
    expected=[(dict(kv.split('=',1) for kv in selector.split(',')),selector,model)
              for selector,model in pinned_choices.items()]
    active={row[2] for row in candidates if row[-1]=='USED_IN_REGISTERED_OAK_CHAIR'}
    covered=set()
    for row in oak:
        properties=dict(kv.split('=',1) for kv in row['properties'].split(','))
        matches=[(selector,model) for cond,selector,model in expected
                 if all(properties.get(k)==v for k,v in cond.items())]
        assert len(matches)==1,(properties,matches)
        selector,model=matches[0]
        covered.add(selector)
        observed=set(row['quad_sprites'].split('|'))&active
        expected_sprites={sprite for sprite,ref,*_ in bindings if ref==model}
        assert observed==expected_sprites,(selector,model,observed,expected_sprites)
        chair_state_refs.append((row['properties'],selector,model,'|'.join(sorted(observed))))
    assert covered==set(pinned_choices)
    assert len(missing)==8 and sum(r[2] for r in missing)==139 and len(candidates)==16
    assert len(active)==13
    prior=dict(e.execute('SELECT finding,count(*) FROM prior_face GROUP BY finding'))
    assert prior=={'BOTH_ZERO_UV_NO_PIXELS':176,'MATCHED_PRIOR_FACE_SOURCE_AND_RECT':3937}
    declarations=e.execute("SELECT count(*) FROM texture_exception WHERE finding LIKE 'DECLARATION_%'").fetchone()[0]
    assert declarations==77

    table_defs={
        'missing_sprite_runtime':(
            'texture_id INTEGER PRIMARY KEY REFERENCES texture_exception, requested TEXT NOT NULL, '
            'face_instances INTEGER NOT NULL, runtime_sprite TEXT NOT NULL, outcome TEXT NOT NULL',
            'texture_id requested face_instances runtime_sprite outcome',missing),
        'alternate_sprite_runtime':(
            'texture_id INTEGER NOT NULL, candidate_path TEXT NOT NULL, sprite TEXT NOT NULL, git_blob_sha TEXT NOT NULL, '
            'model_bindings INTEGER, face_instances INTEGER, directly_selected_models INTEGER, atlas_result TEXT, '
            'oak_states_using INTEGER, outcome TEXT, PRIMARY KEY(texture_id,candidate_path), '
            'FOREIGN KEY(texture_id,candidate_path) REFERENCES alternate_asset(texture_id,path)',
            'texture_id candidate_path sprite git_blob_sha model_bindings face_instances directly_selected_models atlas_result oak_states_using outcome',candidates),
        'alternate_sprite_model_binding':(
            'sprite TEXT NOT NULL, model_resource TEXT NOT NULL, slot TEXT NOT NULL, face_instances INTEGER, '
            'direct_blockstate_options INTEGER, PRIMARY KEY(sprite,model_resource,slot)',
            'sprite model_resource slot face_instances direct_blockstate_options',bindings),
        'oak_chair_runtime_binding':(
            'runtime_state TEXT PRIMARY KEY, source_selector TEXT NOT NULL, source_model TEXT NOT NULL, '
            'runtime_candidate_sprites TEXT NOT NULL',
            'runtime_state source_selector source_model runtime_candidate_sprites',chair_state_refs),
    }
    for table,(schema,fields,data) in table_defs.items():
        e.execute(f'CREATE TABLE {table} ({schema})')
        e.executemany(f'INSERT INTO {table} VALUES ({",".join("?" for _ in data[0])})',data)
        make_csv(args.out/f'{table.upper()}.csv',fields,data)
    e.execute('CREATE TABLE atlas_probe(kind TEXT, requested TEXT, properties TEXT, status TEXT, '
              'sprite TEXT, quad_sprites TEXT, PRIMARY KEY(kind,requested,properties))')
    e.executemany('INSERT INTO atlas_probe VALUES (?,?,?,?,?,?)',
                  (tuple(r[k] for k in ('kind','requested','properties','status','sprite','quad_sprites')) for r in runtime))
    with lzma.open(UV_SUPPORT,'rt',encoding='utf-8',newline='') as stream:
        supports={(int(r['texture_id']),r['uv']):r for r in csv.DictReader(stream)
                  if r['frame']=='0' and r['outcome'] in ('LINE_SUPPORT','POINT_SUPPORT')}
    zero_support=[]
    for ledger,row,tid,uv in e.execute("""
        SELECT ledger_path,ledger_row,texture_id,uv FROM prior_face
        WHERE finding='BOTH_ZERO_UV_NO_PIXELS' ORDER BY ledger_path,ledger_row
    """):
        support=supports[tid,uv]
        zero_support.append((ledger,row,support['outcome'],support['pixel_box'],support['rgba_sha256']))
    zero_counts=Counter(r[2] for r in zero_support)
    assert zero_counts=={'LINE_SUPPORT':172,'POINT_SUPPORT':4}
    e.execute('CREATE TABLE prior_zero_uv_support(ledger_path TEXT NOT NULL, ledger_row INTEGER NOT NULL, '
              'outcome TEXT NOT NULL, source_pixel_box TEXT NOT NULL, frame0_rgba_sha256 TEXT NOT NULL, '
              'PRIMARY KEY(ledger_path,ledger_row), FOREIGN KEY(ledger_path,ledger_row) REFERENCES prior_face)')
    e.executemany('INSERT INTO prior_zero_uv_support VALUES (?,?,?,?,?)',zero_support)
    e.execute('CREATE TABLE followup_input(name TEXT PRIMARY KEY, sha256 TEXT NOT NULL)')
    e.executemany('INSERT INTO followup_input VALUES (?,?)',
                  ((name,sha256(path.read_bytes()).hexdigest()) for name,path in (
                    ('base_e_db',E_DB),('phase_1_3_f_db',F_DB),('c_uv_source_support',UV_SUPPORT),
                    ('runtime_probe',args.atlas),
                    ('another_furniture_4.0.2_fabric',args.fabric))))
    e.commit()
    assert e.execute('PRAGMA integrity_check').fetchone()==('ok',)
    assert not e.execute('PRAGMA foreign_key_check').fetchall()
    (args.out/'research_texture_uv_runtime.sqlite.xz').write_bytes(lzma.compress(e.serialize()))
    result=dict(missing_ids_with_engine_fallback=len(missing),missing_original_face_instances=sum(r[2] for r in missing),
        candidates=len(candidates),actual_oak_chair_textures=len(active),unused_alternatives=len(candidates)-len(active),
        unused_alternatives_present_in_atlas=sum(r[2]==r[7] for r in candidates if r[-1]=='UNUSED_ALTERNATIVE'),
        candidate_binding_rows=len(bindings),oak_registry_states=len(oak),oak_fixed_selectors_checked=len(covered),
        stone_tombstone_item_status=item[0]['status'],service_bell_block_particle=next(iter(bell)), service_bell_item_particle=next(iter(item_bell)),
        declaration_only_textures=declarations,prior_faces=prior, prior_zero_uv_source_support=zero_counts,db_integrity='ok')
    (args.out/'SUMMARY.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
