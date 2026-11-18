"""Trace exceptions to pinned originals and record the runtime evidence still needed."""
import argparse
from collections import Counter
import csv
import gzip
import hashlib
from itertools import product
import json
import lzma
from pathlib import Path
import runpy
import sqlite3
import subprocess
from zipfile import ZipFile

HERE=Path(__file__).resolve().parent
FURNITURE=HERE.parents[1]
P13=FURNITURE/'phase_1-3'
P14=FURNITURE/'phase_1-4'
B=HERE.parent/'B'
ROTATE=runpy.run_path(str(P13/'E/compare_furniture.py'))['rotate']


def rows(path):
    opener={'.gz':gzip.open,'.xz':lzma.open}.get(path.suffix,open)
    with opener(path,'rt',encoding='utf-8',newline='') as file:
        return list(csv.DictReader(file))


def write(path,records):
    with path.open('w',encoding='utf-8',newline='') as file:
        writer=csv.DictWriter(file,fieldnames=list(records[0]),lineterminator='\n')
        writer.writeheader()
        writer.writerows(records)


def digest(body):
    return hashlib.sha256(body).hexdigest()


def blob(body):
    return hashlib.sha1(f'blob {len(body)}\0'.encode()+body).hexdigest()


def git(repo,pin,path):
    return subprocess.check_output(['git','-C',repo,'show',pin+':'+path])


def path_for_model(resource):
    namespace,path=resource.split(':')
    return f'assets/{namespace}/models/{path}.json'


def classify_inputs(args,out):
    with sqlite3.connect(':memory:') as db:
        db.deserialize(lzma.decompress((P13/'F/furniture_research.sqlite.xz').read_bytes()))
        pins=dict(db.execute('SELECT id,pin FROM source'))
        catalog={r[0]:r[1:] for r in db.execute('SELECT model_key,source_id,resource_id,path,sha FROM model')}
        refs={r[1] for r in catalog.values() if r[0]=='AF'}
        sample_keys={r[0] for r in db.execute(
            'SELECT model_key FROM sample_option JOIN option USING(state_id,rule_index,option_index)')}
        reachable={r[0] for r in db.execute('SELECT DISTINCT model_key FROM option WHERE model_key IS NOT NULL')}
        sample_lineage=sample_keys|{r[0] for r in db.execute('''
            SELECT ancestor_key FROM lineage JOIN (
                SELECT DISTINCT model_key FROM sample_option JOIN option USING(state_id,rule_index,option_index)
            ) USING(model_key)
        ''')}
        state_lineage=reachable|{r[0] for r in db.execute(
            'SELECT DISTINCT ancestor_key FROM lineage JOIN option USING(model_key)')}
        missing_tex=list(db.execute('''
            SELECT t.id,m.model_key,m.resource_id,s.slot,s.face_count,
                   (SELECT count(*) FROM option o WHERE o.model_key=m.model_key)
            FROM texture t JOIN model_slot s ON s.texture_id=t.id JOIN model m USING(model_key)
            WHERE t.path IS NULL ORDER BY t.id,m.model_key,s.slot
        '''))
        options={(s,r,o):(m,u,x,y) for s,r,o,m,u,x,y in db.execute('''
            SELECT state.state_id,rule_index,option_index,model_key,unresolved_target,x,y
            FROM option JOIN state ON state.id=option.state_id
        ''')}
        assert db.execute("SELECT count(*) FROM option WHERE unresolved_target IS NOT NULL").fetchone()[0]==4

    af_tree=set(subprocess.check_output(['git','-C',args.af,'ls-tree','-r','--name-only',pins['AF']]).decode().splitlines())
    assert digest(args.macaw.read_bytes())==pins['MACAW']
    assert hashlib.sha1(args.mc1211.read_bytes()).hexdigest()==pins['MC1.21.1']
    assert hashlib.sha1(args.mc12111.read_bytes()).hexdigest()==pins['MC1.21.11']
    parents=[]
    with ZipFile(args.macaw) as macaw, ZipFile(args.mc1211) as mc:
        macaw_paths=set(macaw.namelist())
        vanilla_paths=set(mc.namelist())
        for r in rows(P13/'C/C_EXCEPTIONS.csv.gz'):
            if r['status']!='PARENT_MISSING':
                continue
            key=r['model_key']
            source,resource,path,sha=catalog[key]
            assert source==r['mod'] and resource==r['model_id']
            body=git(args.af,pins['AF'],path) if source=='AF' else macaw.read(path)
            assert (blob(body) if source=='AF' else digest(body))==sha
            raw=json.loads(body)['parent']
            ref=raw if ':' in raw else 'minecraft:'+raw
            assert ref==r['detail']
            expected=path_for_model(ref)
            assert expected not in (vanilla_paths if source=='AF' else macaw_paths)
            note='assets/minecraft/models/block/lantern.json' if ref=='minecraft:lantern' else ''
            assert not note or note in vanilla_paths
            parents.append(dict(mod=source,model_key=key,model_resource=resource,model_path=path,model_sha=sha,
                                declared_parent=ref,raw_parent=raw,missing_exact_path=expected,alternate_path_hint=note,
                                direct_state_option=int(key in reachable),state_lineage=int(key in state_lineage),
                                sample_lineage=int(key in sample_lineage)))
    assert len(parents)==48 and not any(r['state_lineage'] or r['sample_lineage'] for r in parents)

    state_exceptions=[]
    for r in rows(P13/'D/D_EXCEPTIONS.csv'):
        body=git(args.af,pins['AF'],r['path'])
        assert blob(body)==r['source_sha']
        option=json.loads(body)['variants'][r['source_selector']]
        assert option['model']==r['model_id']
        k=(r['state_id'],int(r['rule_index']),int(r['option_index']))
        db_model,db_missing,x,y=options[k]
        assert (x,y)==(option.get('x',0),option.get('y',0))
        if r['category']=='UNRESOLVED_MODEL_REF':
            assert db_missing==r['model_id'] and db_model is None and r['model_id'] not in refs
            assert not any(path.endswith('/'+path_for_model(r['model_id'])) for path in af_tree)
            case=''
        else:
            assert db_model==r['model_key'] and db_missing is None
            case,= [a['case'] for a in rows(B/'APPLICATIONS.csv')
                    if a['model']==db_model and a['state']==r['source_selector'].replace(',',';')]
        state_exceptions.append(dict(case=case,state_id=r['state_id'],state_path=r['path'],state_sha=r['source_sha'],
                                     selector=r['source_selector'],rule_index=r['rule_index'],option_index=r['option_index'],
                                     model_ref=r['model_id'],model_key=db_model or '',finding=r['category']))
    assert len(state_exceptions)==6

    versions={r['case']:r['minecraft'] for r in rows(B/'CASES.csv')}
    sample_resources=Counter((r['resource_id'],versions[r['case']]) for r in rows(B/'FACES.csv.xz')
                             if r['case'].startswith('S'))
    texture_versions={r['texture_id']:r['minecraft'] for r in rows(P13/'F/1-3_TEXTURE_UV_HANDOFF.csv')}
    textures=[]
    for r in rows(P14/'entry04/TEXTURE_EXCEPTION_REVIEW.csv'):
        missing=r['finding'].startswith('MISSING_')
        if missing:
            namespace,relative=r['resource_id'].split(':')
            exact=f'/assets/{namespace}/textures/{relative}.png'
            assert not any(path.endswith(exact) for path in af_tree)
            bound=[item for item in missing_tex if item[0]==int(r['texture_id'])]
            assert sum(item[4] for item in bound)==int(r['face_instances'])
            assert not any(item[5] for item in bound)
        version=texture_versions[r['texture_id']]
        sampled=sample_resources[r['resource_id'],version]
        assert sampled==0
        alternate=sum(n for (resource,other),n in sample_resources.items()
                      if resource==r['resource_id'] and other!=version)
        textures.append(dict(**r,minecraft=version,sampled_model_face=sampled,other_version_sample_faces=alternate))
    assert sum(r['finding'].startswith('MISSING_') for r in textures)==8 and len(textures)==85
    write(out/'PARENT_EXCEPTIONS.csv',parents)
    write(out/'STATE_EXCEPTIONS.csv',state_exceptions)
    write(out/'TEXTURE_EXPOSURE.csv',textures)
    return pins,parents,state_exceptions,textures


def original_counterexamples(args,pins,out):
    apps={r['case']:r for r in rows(B/'APPLICATIONS.csv') if r['case'] in {'S37','S38','S44','S45'}}
    sources={}
    def verified(repo,source,path,expected=None):
        body=git(repo,pins[source],path)
        sha=blob(body)
        assert expected is None or sha==expected,path
        sources[path]={'source':source,'sha':sha,'hash_kind':'GIT_BLOB_SHA1'}
        return body
    foot,head=(apps[k] for k in ('S37','S38'))
    bodies={}
    for r in (foot,head):
        state=json.loads(verified(args.hc,'HC',r['state_path'],r['state_sha']))
        vals=dict(i.split('=') for i in r['state'].split(';'))
        choice,=[item for selector,item in state['variants'].items() if dict(i.split('=') for i in selector.split(','))==vals]
        assert choice['model']=='handcrafted:block/'+Path(r['model_path']).stem
        model=json.loads(verified(args.hc,'HC',r['model_path'],r['model_sha']))
        assert r['provider_path'].endswith('/'+path_for_model(model['parent']))
        bodies[r['case']]=json.loads(verified(args.hc,'HC',r['provider_path'],r['provider_sha']))['elements']
    hc_code='common/src/main/java/earth/terrarium/handcrafted/common/blocks/FancyBedBlock.java'
    placement=verified(args.hc,'HC',hc_code,'eb9fc2de73f4d7111bcf9a6b8335a667569445e9').decode()
    assert 'pos.relative(direction)' in placement and 'part == BedPart.FOOT ? direction : direction.getOpposite()' in placement

    def vertices(element,dz):
        corners=list(product(*zip(element['from'],element['to'])))
        rot=element.get('rotation',{})
        if rot.get('angle'):
            corners=[ROTATE(v,rot['origin'],rot['axis'],rot['angle'],rot.get('rescale',False)) for v in corners]
        return sorted((round(x,7),round(y,7),round(z+dz,7)) for x,y,z in corners)

    head_shape,=bodies['S38']
    coincident=[i for i,item in enumerate(bodies['S37']) if vertices(item,0)==vertices(head_shape,-16)]
    assert len(bodies['S37'])==12 and coincident==[11]
    af_code='common/src/main/java/com/starfish_studios/another_furniture/registry/AFBlocks.java'
    code=verified(args.af,'AF',af_code,'380e721488f3f0cd0a717291a185a5a938ed237d').decode()
    assert 'new LampBlock(DyeColor.WHITE, Properties.lamp)' in code
    assert 'blockState.getValue(BlockStateProperties.LIT) ? (blockState.getValue(ModBlockStateProperties.LEVEL_1_3) * 5) : 0' in code
    level_code='common/src/main/java/com/starfish_studios/another_furniture/block/properties/ModBlockStateProperties.java'
    assert 'IntegerProperty.create("level", 1, 3)' in verified(args.af,'AF',level_code).decode()
    faces=rows(B/'FACES.csv.xz')
    left,right=({(r['element_index'],r['direction']):r for r in faces if r['case']==case} for case in ('S44','S45'))
    assert left.keys()==right.keys() and all(left[k]['png_sha']==right[k]['png_sha'] for k in left)
    lamp_changes=[list(k) for k in sorted(left) if left[k]['uv']!=right[k]['uv']]
    assert len(lamp_changes)==4 and all(left[tuple(k)]['rgba_sha256']!=right[tuple(k)]['rgba_sha256'] for k in lamp_changes)
    with ZipFile(args.mc12111) as jar:
        body={}
        for p in ('blockstates/white_bed','models/block/bed','items/white_bed'):
            path='assets/minecraft/'+p+'.json'
            data=jar.read(path)
            sources[path]={'source':'MC1.21.11','sha':digest(data),'hash_kind':'SHA256'}
            body[p]=json.loads(data)
        assert body['blockstates/white_bed']['variants']['']['model']=='minecraft:block/bed'
        bed=body['models/block/bed']
        assert 'elements' not in bed and set(bed['textures'])=={'particle'}
        item=body['items/white_bed']['model']
        assert item['type']=='minecraft:special' and item['model']['type']=='minecraft:bed'
    report={'pinned_inputs':pins,'sources':sources,'hc_bed_north_head_offset':[0,0,-16],
            'hc_bed_coincident_foot_elements':coincident,'hc_bed_vertex_count':len(vertices(head_shape,-16)),
            'vanilla_world_bed_json':'PARTICLE_ONLY','vanilla_inventory_bed':'SPECIAL_BED_DECLARATION',
            'af_lamp_changed_local_faces':lamp_changes,'af_lamp_static_emission':{'unlit':0,'lit_levels':[5,10,15]},
            'uvlock_declared_applications':sum(r['uvlock']=='1' for r in rows(B/'APPLICATIONS.csv')),
            'cullface_declared_face_instances':sum(bool(r['cullface']) for r in faces),
            'tint_declared_face_instances':sum(r['tintindex']!='' for r in faces),
            'in_game_tests_run':0}
    (out/'STATIC_COUNTEREXAMPLES.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    return report


def main(args):
    out=args.out
    out.mkdir(parents=True,exist_ok=True)
    pins,parents,state,tex=classify_inputs(args,out)
    details=original_counterexamples(args,pins,out)
    result=dict(status='PASS_STATIC_REVIEW',missing_parent_models=len(parents),
                missing_parent_targets=dict(Counter(r['declared_parent'] for r in parents)),
                unresolved_state_options=sum(not r['model_key'] for r in state),
                verified_variant_counterexamples=sum(bool(r['case']) for r in state),
                missing_png_textures=sum(r['finding'].startswith('MISSING_') for r in tex),
                declared_only_textures=sum(not r['finding'].startswith('MISSING_') for r in tex),
                missing_png_model_faces=sum(int(r['face_instances']) for r in tex),
                missing_png_item_model_faces=sum(int(r['item_model_faces']) for r in tex),
                texture_exception_sample_faces=sum(r['sampled_model_face'] for r in tex),
                checked_static_counterexample_input_paths=len(details['sources']),
                in_game_tests_run=0)
    encoded=json.dumps(result,indent=2,sort_keys=True)+'\n'
    (out/'D_AUDIT.json').write_text(encoded)
    print(encoded)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for name in ('af','hc','macaw','mc1211','mc12111','out'):
        p.add_argument('--'+name,type=Path,required=True)
    main(p.parse_args())
