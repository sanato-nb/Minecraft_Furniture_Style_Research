"""Freeze the 1-5 comparison cohort against the vanilla JAR and 1-3/1-4 evidence."""
import argparse
from collections import Counter
import csv
import hashlib
import json
import lzma
from pathlib import Path
import sqlite3
import struct
from zipfile import ZipFile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
RESEARCH = HERE.parents[1]
PHASE13 = RESEARCH/'phase_1-3'
PHASE14 = RESEARCH/'phase_1-4'
G = ROOT/'research/vanilla_models/phase_1-2-G/final'
ASSETS = 'assets/minecraft/'
VERSION = '1.21.11'

# id, vanilla block, requested properties, relevant categories, comparison axis
CONTROL = (
    ('V01','oak_stairs',{'facing':'north','half':'bottom','shape':'straight'},'SEATING_CHAIR|SOFA_BENCH','STEPPED_PROFILE'),
    ('V02','oak_slab',{'type':'bottom'},'SMALL_TABLE|LARGE_TABLE|SOFA_BENCH','SLAB_THICKNESS'),
    ('V03','oak_fence',dict(north='true',south='false',east='false',west='false'),'SMALL_TABLE|LARGE_TABLE','CONNECTED_POST'),
    ('V04','oak_pressure_plate',{'powered':'false'},'SMALL_TABLE|LARGE_TABLE','THIN_PLATE'),
    ('V05','barrel',dict(facing='north',open='false'),'STORAGE','CONTAINER_FRONT_CLOSED'),
    ('V06','barrel',dict(facing='north',open='true'),'STORAGE','CONTAINER_FRONT_OPEN'),
    ('V07','bookshelf',{},'SHELVING','SHELF_SURFACE'),
    ('V08','chiseled_bookshelf',{'facing':'north',**{f'slot_{i}_occupied':str(i==0).lower() for i in range(6)}},
     'SHELVING','SIX_MULTIPART_SLOT_SURFACES'),
    ('V09','white_wool',{},'SEATING_CHAIR|SOFA_BENCH|BED','LIGHT_FABRIC_SURFACE'),
    ('V10','oak_planks',{},'SMALL_TABLE|LARGE_TABLE|STORAGE|SHELVING','WOOD_SURFACE'),
    ('V11','white_bed',{},'BED','SPECIAL_BED_RENDER_BOUNDARY'),
    ('V12','cauldron',{},'KITCHEN','EMPTY_CONTAINER'),
    ('V13','water_cauldron',{'level':'3'},'KITCHEN','CONTAINER_WITH_WATER_SURFACE'),
    ('V14','lantern',{'hanging':'false'},'LIGHT_DECOR','LIGHT_FIXTURE'),
    ('V15','flower_pot',{},'LIGHT_DECOR','DECORATIVE_CONTAINER'),
)


def csv_rows(path):
    with path.open(encoding='utf-8',newline='') as stream:
        return list(csv.DictReader(stream))


def json_bytes(value):
    return json.dumps(value,sort_keys=True,separators=(',',':'))


def write(path, records):
    with path.open('w',encoding='utf-8',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(records[0]),lineterminator='\n')
        writer.writeheader()
        writer.writerows(records)


def git_blob(data):
    return hashlib.sha1(f'blob {len(data)}\0'.encode()+data).hexdigest()


def compare(db,left,right):
    assert not db.execute(left+' EXCEPT '+right).fetchall()
    assert not db.execute(right+' EXCEPT '+left).fetchall()


def mod_scope(out):
    f_path=PHASE13/'F/furniture_research.sqlite.xz'
    e_path=PHASE14/'entry04/research_texture_uv.sqlite.xz'
    with sqlite3.connect(':memory:') as db:
        db.deserialize(lzma.decompress(e_path.read_bytes()))
        db.execute("ATTACH DATABASE ':memory:' AS frozen")
        db.deserialize(lzma.decompress(f_path.read_bytes()),name='frozen')
        left='''SELECT case_id,rule_index,option_index,model_key,model_sha,provider_key,provider_sha,
                       state_sha,x,y,uvlock FROM comparison_application'''
        right='''SELECT s.sample_id,s.rule_index,s.option_index,o.model_key,m.sha,g.provider_key,p.sha,
                        st.sha,o.x,o.y,o.uvlock FROM frozen.sample_option s
                 JOIN frozen.option o USING(state_id,rule_index,option_index)
                 JOIN frozen.state st ON st.id=s.state_id
                 JOIN frozen.model m ON m.model_key=o.model_key
                 JOIN frozen.geometry g ON g.model_key=m.model_key
                 JOIN frozen.model p ON p.model_key=g.provider_key'''
        compare(db,left,right)
        compare(db,'''SELECT case_id,rule_index,option_index,element_index,direction,texture_id
                      FROM comparison_face''',
                   '''SELECT so.sample_id,so.rule_index,so.option_index,f.element_index,f.direction,f.texture_id
                      FROM frozen.sample_option so JOIN frozen.option o USING(state_id,rule_index,option_index)
                      JOIN frozen.effective_face_texture f ON f.model_key=o.model_key''')
        rows=db.execute('''
            SELECT s.id,s.category,st.source_id,st.state_id,st.sha,s.assignment,
                   m.minecraft,m.version, count(DISTINCT printf('%d/%d',a.rule_index,a.option_index)),
                   count(f.direction),sum(f.status='STATIC_RECT'),sum(f.status='ANIMATED_FRAME_RECTS'),
                   sum(f.status='ZERO_UV_AREA')
            FROM frozen.sample s JOIN frozen.state st ON st.id=s.state_id
            JOIN frozen.source m ON m.id=st.source_id
            JOIN comparison_application a ON a.case_id=s.id
            JOIN comparison_face f USING(case_id,rule_index,option_index)
            GROUP BY s.id,s.category,st.source_id,st.state_id,st.sha,s.assignment,m.minecraft,m.version
            ORDER BY s.id
        ''').fetchall()
        cases=[dict(zip(('case','category','mod','state_id','state_sha','assignment','minecraft','mod_version',
                         'applications','faces','static_faces','animated_faces','zero_uv_faces'),r)) for r in rows]
        upstream=csv_rows(PHASE14/'entry04/1-5_TEXTURE_UV_HANDOFF.csv')
        assert len(upstream)==52
        assert len({(r['case'],r['rule_index'],r['option_index']) for r in upstream})==52
        for r in upstream:
            expected=db.execute('''
                SELECT model_key,model_sha,provider_key,provider_sha,state_sha,x,y,uvlock
                FROM comparison_application WHERE case_id=? AND rule_index=? AND option_index=?
            ''',(r['case'],r['rule_index'],r['option_index'])).fetchone()
            assert tuple(r[k] for k in ('model_key','model_sha','provider_key','provider_sha','state_sha','x','y','uvlock'))==tuple(map(str,expected))
            face_counts=db.execute('''
                SELECT count(*),sum(status='STATIC_RECT'),sum(status='ANIMATED_FRAME_RECTS'),sum(status='ZERO_UV_AREA')
                FROM comparison_face WHERE case_id=? AND rule_index=? AND option_index=?
            ''',(r['case'],r['rule_index'],r['option_index'])).fetchone()
            assert tuple(int(r[k]) for k in ('face_instances','static_faces','animated_faces','zero_uv_faces'))==face_counts
        assert len(cases)==47 and sum(r['applications'] for r in cases)==52 and sum(r['faces'] for r in cases)==1610
        assert len({r['category'] for r in cases})==9
        assert {r['mod'] for r in cases}=={'AF','HC','MACAW'}
        pin=db.execute("SELECT pin FROM frozen.source WHERE id='MC1.21.11'").fetchone()[0]
    write(out/'MOD_CASE_SCOPE.csv',cases)
    return cases,pin


def matches(condition,properties):
    if 'AND' in condition:
        return all(matches(part,properties) for part in condition['AND'])
    if 'OR' in condition:
        return any(matches(part,properties) for part in condition['OR'])
    assert all(key in properties for key in condition),condition
    return all(properties[key] in value.split('|') for key,value in condition.items())


def selections(doc,properties):
    if 'variants' in doc:
        for index,(key,value) in enumerate(doc['variants'].items()):
            rule=dict(part.split('=',1) for part in key.split(',')) if key else {}
            if matches(rule,properties) and rule.keys()==properties.keys():
                yield index,key,value
    else:
        for index,r in enumerate(doc['multipart']):
            if matches(r.get('when',{}),properties):
                yield index,json_bytes(r.get('when',{})),r['apply']


def local_resource(ref):
    if ':' in ref:
        namespace,ref=ref.split(':',1)
        assert namespace=='minecraft'
    return ref


def vanilla_scope(out,jar_path,jar_pin):
    raw=jar_path.read_bytes()
    assert hashlib.sha1(raw).hexdigest()==jar_pin
    g_manifest={r['path'].removeprefix(VERSION+'/'):r for r in csv_rows(G/'G_FINAL_SOURCE_SHA_4669.csv')}
    sources={}
    models=[]
    with ZipFile(jar_path) as jar:
        def read(path,kind,control):
            data=jar.read(path)
            hashed=git_blob(data)
            manifest=g_manifest[path]
            assert manifest['sha']==hashed and int(manifest['bytes'])==len(data),(path,manifest)
            source=sources.setdefault(path,dict(path=path,kind=kind,bytes=len(data),git_blob_sha1=hashed,
                                                 sha256=hashlib.sha256(data).hexdigest(),controls=set()))
            source['controls'].add(control)
            return data

        for control,block,properties,categories,axis in CONTROL:
            state=ASSETS+'blockstates/'+block+'.json'
            data=read(state,'BLOCKSTATE',control)
            doc=json.loads(data)
            chosen=list(selections(doc,properties))
            assert len(chosen)==({'V03':2,'V08':7}.get(control,1)),(control,chosen)
            for rule,condition,value in chosen:
                options=value if isinstance(value,list) else [value]
                for option_index,option in enumerate(options):
                    resource=local_resource(option['model'])
                    chain=[]
                    merged={}
                    leaf=ASSETS+'models/'+resource+'.json'
                    provider=''
                    elements=[]
                    while resource:
                        path=ASSETS+'models/'+resource+'.json'
                        assert path not in chain
                        chain.append(path)
                        body=json.loads(read(path,'MODEL',control))
                        if 'elements' in body and not provider:
                            provider=path
                            elements=body['elements']
                        merged=body.get('textures',{}) | merged
                        resource=local_resource(body.get('parent',''))
                    face_count=sum(len(e.get('faces',{})) for e in elements)
                    texture_paths=set()
                    for face in (f for e in elements for f in e['faces'].values()):
                        ref=face['texture']
                        used=set()
                        while ref.startswith('#'):
                            assert ref not in used and ref[1:] in merged,(control,ref,merged)
                            used.add(ref)
                            ref=merged[ref[1:]]
                        texture_paths.add(ASSETS+'textures/'+local_resource(ref)+'.png')
                    dims={}
                    for path in sorted(texture_paths):
                        png=read(path,'PNG',control)
                        assert png.startswith(b'\x89PNG\r\n\x1a\n')
                        dims[path]=struct.unpack('>II',png[16:24])
                    particle_only=''
                    if control=='V11':
                        particle_only=ASSETS+'textures/'+local_resource(merged['particle'])+'.png'
                        read(particle_only,'PNG',control)
                    models.append(dict(control=control,block=block,properties=json_bytes(properties),categories=categories,
                                       axis=axis,state_path=state,state_git_blob_sha1=sources[state]['git_blob_sha1'],
                                       rule_index=rule,condition=condition,option_index=option_index,
                                       model_path=leaf,model_git_blob_sha1=sources[leaf]['git_blob_sha1'],
                                       parent_chain='|'.join(chain),geometry_provider=provider,
                                       provider_git_blob_sha1=sources[provider]['git_blob_sha1'] if provider else '',
                                       elements=len(elements),faces=face_count,x=option.get('x',0),y=option.get('y',0),
                                       uvlock=int(option.get('uvlock',False)),weight=option.get('weight',1),
                                       texture_dimensions=json_bytes(dims),particle_only_path=particle_only,
                                       scope='STATIC_SOURCE' if elements else 'NO_ORDINARY_ELEMENTS'))
            assert (any(r['elements'] for r in models if r['control']==control))==(control!='V11')
    for r in sources.values():
        r['controls']='|'.join(sorted(r['controls']))
    old_options={}
    for ledger in sorted(G.parent.glob('entry*/G_ENTRY*_D_ORIGINAL_OPTIONS.csv')):
        for row in csv_rows(ledger):
            key=(row['blockstate_path'].removeprefix(VERSION+'/'),
                 int(row['rule_index']),int(row['alternative_index']))
            old_options[key]=row
    previous_match=0
    for model in models:
        key=(model['state_path'],model['rule_index'],model['option_index'])
        old=old_options.get(key)
        if old is not None:
            raw=json.loads(old['raw_apply_json'])
            assert old['sha']==model['state_git_blob_sha1']
            assert old['model_path'].removeprefix(VERSION+'/')==model['model_path']
            assert [raw.get(k,v) for k,v in (('x',0),('y',0),('uvlock',False),('weight',1))]==[
                model['x'],model['y'],model['uvlock'],model['weight']]
            previous_match += 1
    assert previous_match==11
    bed=next(row for row in models if row['control']=='V11')
    e_rows=ROOT/'research/vanilla_models/phase_1-2-E/entry1/E_ENTRY1_MODEL_SOURCE.csv'
    old_bed=next(row for row in csv_rows(e_rows) if row['model_path']==VERSION+'/'+bed['model_path'])
    assert (old_bed['model_sha'],old_bed['own_elements'],old_bed['particle_png_path'])==(
        bed['model_git_blob_sha1'],'0',VERSION+'/'+bed['particle_only_path'])
    write(out/'VANILLA_CONTROL_OPTIONS.csv',models)
    write(out/'VANILLA_SOURCE_PROVENANCE.csv',[sources[p] for p in sorted(sources)])
    return dict(controls=len(CONTROL),applications=len(models),sources=dict(Counter(r['kind'] for r in sources.values())),
                element_instances=sum(r['elements'] for r in models),face_instances=sum(r['faces'] for r in models),
                special_controls=[r['control'] for r in models if r['scope']=='NO_ORDINARY_ELEMENTS'],
                matching_prior_G_state_options=previous_match,official_client_jar_sha1=jar_pin)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--jar',required=True,type=Path)
    parser.add_argument('--out',required=True,type=Path)
    args=parser.parse_args()
    args.out.mkdir(parents=True,exist_ok=True)
    mod,pin=mod_scope(args.out)
    vanilla=vanilla_scope(args.out,args.jar,pin)
    assert {tag for _,_,_,categories,_ in CONTROL for tag in categories.split('|')}=={r['category'] for r in mod}
    result=dict(status='PASS',mod_cases=len(mod),mod_applications=sum(r['applications'] for r in mod),
                mod_faces=sum(r['faces'] for r in mod),mod_category_count=len({r['category'] for r in mod}),
                mod_face_disposition={k:sum(r[k] for r in mod) for k in ('static_faces','animated_faces','zero_uv_faces')},
                vanilla=vanilla)
    encoded=json.dumps(result,indent=2,sort_keys=True)+'\n'
    (args.out/'A_SCOPE_AUDIT.json').write_text(encoded,encoding='utf-8')
    print(encoded)


if __name__=='__main__':
    main()
