"""Reconcile the fixed C/D exceptions and compare release resources."""
import argparse
import csv
import gzip
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
B = ROOT / 'B/source_verification'
sys.path.insert(0, str(B))
from verify_sources import git, git_objects, item_model_refs

PINS = {'AF':'57eb624cbb7f408d43398c7434b0d38d312cb55d',
        'HC':'8d21d1665916850c3fa3bdaf1370c50ec2ca7035'}
NAMES = {'AF':'another_furniture','HC':'handcrafted','MACAW':'mcwfurnitures'}


def csv_rows(path):
    opener = gzip.open if path.suffix=='.gz' else open
    with opener(path, 'rt', encoding='utf-8-sig', newline='') as stream:
        return list(csv.DictReader(stream))


def write(path, rows):
    with path.open('w',encoding='utf-8',newline='') as stream:
        writer=csv.DictWriter(stream,rows[0].keys(),lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def data_for(mod, repo, installed, publication=None):
    rows=csv_rows(B/f'B_{mod}_SOURCE_BODIES.csv.gz')
    origin=dict(git_objects(repo,[r['sha'] for r in rows]))
    jar_names=set(installed.namelist())
    release_names=set(publication.namelist()) if publication else set()
    bodies, comparison={},[]
    for r in rows:
        rel='assets/'+r['path'].split('assets/',1)[1]
        data=origin[r['sha']]
        body=json.loads(data)
        bodies[r['asset_id']]=body
        runtime=installed.read(rel) if rel in jar_names else None
        published=publication.read(rel) if rel in release_names else None
        comparison.append(dict(mod=mod,path=rel,family=r['family'],runtime_binary_match=data==runtime,
                               runtime_json_match=runtime is not None and body==json.loads(runtime),
                               publication_json_match='' if publication is None
                               else published is not None and body==json.loads(published)))
    return bodies, comparison


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ('af-repo','hc-repo','af-runtime','af-publication','hc-runtime','macaw','vanilla1211','output'):
        parser.add_argument('--'+name,type=Path,required=True)
    args=parser.parse_args()
    args.output.mkdir(exist_ok=True,parents=True)
    sources={}
    compare=[]
    for mod,repo,runtime in (('AF',args.af_repo,args.af_runtime),('HC',args.hc_repo,args.hc_runtime)):
        with ZipFile(runtime) as jar:
            if mod=='AF':
                with ZipFile(args.af_publication) as release:
                    sources[mod], rows=data_for(mod,repo,jar,release)
            else:
                sources[mod], rows=data_for(mod,repo,jar)
        compare.extend(rows)
    compare_summary=[]
    for mod in ('AF','HC'):
        for family in ('models','blockstates'):
            rows=[r for r in compare if r['mod']==mod and r['family']==family]
            compare_summary.append(dict(mod=mod,family=family,source_rows=len(rows),
                runtime_byte_matches=sum(r['runtime_binary_match'] for r in rows),
                runtime_json_matches=sum(r['runtime_json_match'] for r in rows),
                official_af_403_json_matches=sum(r['publication_json_match'] is True for r in rows) if mod=='AF' else ''))
    notable_paths={'birch_chair','spruce_chair','oak_table','oak_bench','oak_shelf','oak_chair',
                   'oak_couch','oak_fancy_bed','unused/white_awning'}
    write(args.output/'RELEASE_COMPARISON.csv', compare_summary)
    write(args.output/'RUNTIME_RESOURCE_SAMPLES.csv',[r for r in compare if r['family']=='blockstates'
        and r['path'].split('/blockstates/',1)[1].removesuffix('.json') in notable_paths])

    with ZipFile(args.macaw) as jar, ZipFile(args.vanilla1211) as vanilla:
        assert hashlib.sha256(args.macaw.read_bytes()).hexdigest()=='e55d7a78b878043af82875cb8738941b0bba1a3c77652dea3d75a434dbba1a0e'
        jar_names=set(jar.namelist())
        types={r['asset_id']:json.loads(jar.read(r['path'])) for r in csv_rows(B/'B_MACAW_SOURCE_BODIES.csv.gz') if r['family']=='models'}
        sources['MACAW']=types
        item_refs=Counter(ref for p in jar_names if p.startswith('assets/mcwfurnitures/items/') and p.endswith('.json')
                          for ref in item_model_refs(json.loads(jar.read(p))))
        af_textures=set(git(args.af_repo,'ls-tree','-r','--name-only',PINS['AF']).decode().splitlines())
        hc_textures=set(git(args.hc_repo,'ls-tree','-r','--name-only',PINS['HC']).decode().splitlines())
        texture_names={'AF':af_textures,'HC':hc_textures,'MACAW':jar_names}

        selected=Counter(r['model_key'] for r in csv_rows(ROOT/'D/MODEL_STATE_ASSEMBLY.csv.gz'))
        templates=Counter(r['geometry_source_key'] for r in csv_rows(ROOT/'C/mod_furniture_catalog.csv.gz')
                          if int(r['effective_elements'])>0 and r['geometry_source_key']!=r['model_key'])
        parents=Counter((mod,b.get('parent')) for mod,models in sources.items() for b in models.values())
        affected=[]
        for row in csv_rows(ROOT/'C/C_EXCEPTIONS.csv.gz'):
            if row['category'] not in ('PARENT','GEOMETRY'):
                continue
            mod,key,ref=row['mod'],row['model_key'],row['model_id']
            body=sources[mod][ref]
            status=row['status']
            layers=[v for k,v in body.get('textures',{}).items() if k.startswith('layer')]
            for layer in layers:
                namespace,sep,path=layer.partition(':')
                assert sep and path
                filename=f'assets/{namespace}/textures/{path}.png'
                if namespace=='minecraft':
                    assert filename in vanilla.namelist(), filename
                else:
                    assert any(p.endswith(filename) for p in texture_names[mod]), filename
            if status=='PARENT_MISSING':
                namespace,model=row['detail'].split(':',1)
                filename=f'assets/{namespace}/models/{model}.json'
                if mod=='AF':
                    assert filename not in vanilla.namelist() and 'assets/minecraft/models/block/lantern.json' in vanilla.namelist()
                else:
                    assert filename not in jar_names
            affected.append(dict(mod=mod,model_key=key,model=ref,status=status,terminal=row['detail'],
                                 own_elements=len(body.get('elements',[])),direct_state_refs=selected[key],
                                 independent_item_definition_refs=item_refs[ref] if mod=='MACAW' else '',
                                 child_parent_refs=parents[mod,ref],used_as_geometry_provider=templates[key],
                                 source_png_layers='|'.join(layers)))
        write(args.output/'C_EXCEPTION_RECHECK.csv',affected)
        assert len(affected)==112 and sum(int(r['direct_state_refs']) for r in affected if r['status']=='PARENT_MISSING')==0
        assert sum(bool(r['source_png_layers']) for r in affected if r['status']=='GENERATED_ITEM_RUNTIME')==58
        assert sum(int(r['independent_item_definition_refs']) for r in affected
                   if r['status']=='PARENT_MISSING' and r['mod']=='MACAW')==0

    af=sources['AF']
    checked=[]
    for row in csv_rows(ROOT/'D/D_EXCEPTIONS.csv'):
        data=af[row['state_id']]
        selected_model=data['variants'][row['source_selector']]['model']
        assert selected_model==row['model_id']
        if row['category']=='UNRESOLVED_MODEL_REF':
            assert selected_model not in af
        else:
            assert data['variants']['facing=south,tucked=false,variant=1']==data['variants'][row['source_selector']]
        checked.append(row)
    assert len(checked)==6
    write(args.output/'D_EXCEPTION_RECHECK.csv',checked)


if __name__=='__main__':
    main()
