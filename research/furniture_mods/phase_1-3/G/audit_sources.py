"""고정 원본과 B·F 원장의 경로, 해시, 집계를 대조한다."""
import argparse
from collections import Counter, defaultdict
import csv
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import tarfile
import zipfile


def rows(path):
    opener = gzip.open if path.suffix == '.gz' else open
    with opener(path, 'rt', encoding='utf-8-sig', newline='') as file:
        return list(csv.DictReader(file))


def json_file(path):
    return json.loads(path.read_bytes())


def git(repo, *args):
    return subprocess.check_output(['git', '-C', str(repo), *args])


def blob(data):
    return hashlib.sha1(f'blob {len(data)}\0'.encode() + data).hexdigest()


def git_files(repo, pin):
    with subprocess.Popen(['git', '-C', str(repo), 'archive', pin], stdout=subprocess.PIPE) as process:
        with tarfile.open(fileobj=process.stdout, mode='r|') as archive:
            for item in archive:
                if item.isfile():
                    yield item.name, archive.extractfile(item).read()
        if process.wait():
            raise RuntimeError(f'git archive failed for {pin}')


def read_original(mod, ns, files, digest, ledger, textures, code):
    actual = {}
    texture_count = 0
    code_count = 0
    for path, data in files:
        if path in textures:
            assert digest(data) == textures[path], path
            texture_count += 1
        if (mod, path) in code:
            assert code[mod, path] == (digest(data), len(data)), path
            code_count += 1
        marker = f'assets/{ns}/'
        if marker not in path or not path.endswith('.json'):
            continue
        family, _, rel = path.split(marker,1)[1].partition('/')
        if family not in ('models', 'blockstates') and not (mod=='MACAW' and family=='items'):
            continue
        row = ledger[path]
        actual_sha = digest(data)
        body = json.loads(data)
        assert path not in actual and isinstance(body, dict), path
        assert (row['mod_id'],row['family'], row['asset_id'], row['sha'], int(row['bytes']),row['parse']) == (
            mod,family,ns+':'+rel.removesuffix('.json'),actual_sha,len(data),'STRICT_JSON'), path
        if family == 'models':
            els = body.get('elements', [])
            assert (row['parent'],int(row['own_elements']),int(row['own_faces'])) == (
                body.get('parent',''),len(els),sum(len(e['faces']) for e in els)), path
        actual[path] = (family, actual_sha)
    assert actual.keys() == ledger.keys(), mod
    assert len({(r['family'],r['asset_id']) for r in ledger.values()}) == len(ledger), mod
    assert texture_count == len(textures)
    assert code_count == sum(m == mod for m,_ in code)
    return actual


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('af','hc','source-dir','out'):
        parser.add_argument('--'+name,type=Path,required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[4]
    phase = root/'research/furniture_mods/phase_1-3'
    b, c, f = (phase/n for n in ('B','C','F'))
    bv = b/'source_verification'
    registry = {r['mod_id']:r for r in rows(b/'SOURCE_REGISTRY.csv')}
    pinned_macaw = json_file(bv/'B_SOURCE_BODY_AUDIT.json')['macaw']
    version = json_file(args.source_dir/'macaw-version.json')
    project = json_file(args.source_dir/'macaw-project.json')
    macaw_data = (args.source_dir/'macaw.jar').read_bytes()
    primary, = [r for r in version['files'] if r['primary']]
    assert version['id']==pinned_macaw['version_id'] and version['project_id']==project['id']==pinned_macaw['project_id']
    assert version['game_versions']==pinned_macaw['minecraft'] and version['loaders']==pinned_macaw['loaders']
    assert version['version_number']==pinned_macaw['mod_version']
    assert project['license']['id']==pinned_macaw['distribution_license']
    assert primary['url']==pinned_macaw['url'] and len(macaw_data)==primary['size']==pinned_macaw['bytes']
    for alg in ('sha1','sha256','sha512'):
        observed=hashlib.new(alg,macaw_data).hexdigest()
        assert observed == pinned_macaw[alg]
        if alg in primary['hashes']:
            assert observed == primary['hashes'][alg]
    textures = rows(f/'1-3_TEXTURE_UV_HANDOFF.csv')
    disposition = Counter(r['disposition'] for r in textures)
    assert len({(r['resource_id'], r['minecraft']) for r in textures})==len(textures)==2256
    assert disposition=={'PNG_UV_CANDIDATE':1996,'PRIOR_RGBA_SHA_MATCH':175,'DECLARED_SLOT_ONLY':77,'SOURCE_EXCEPTION':8}
    texture_paths = defaultdict(dict)
    for row in textures:
        if row['source_sha']:
            source,path,sha=(row[k] for k in ('source_id','path','source_sha'))
            assert texture_paths[source].setdefault(path,sha)==sha
        else:
            assert row['disposition']=='SOURCE_EXCEPTION' and not row['path']
    for row in rows(f/'F_PRIOR_RGBA_LEDGER.csv'):
        path=root/row['ledger_path']
        assert blob(path.read_bytes())==row['ledger_blob_sha']
        prior_rows=rows(path)
        if prior_rows and 'newly_sampled' in prior_rows[0]:
            prior_rows=[r for r in prior_rows if r['newly_sampled']=='1']
        assert len(prior_rows)==int(row['rows_recounted']), path
    code = {(r['mod'],r['path']):(r['hash'],int(r['bytes'])) for r in rows(c/'C_CODE_SHA_INDEX.csv')}
    assert Counter(mod for mod,_ in code)=={'AF':89,'HC':86,'MACAW':53}
    code_entries=rows(b/'B_JAVA_KOTLIN_SOURCE_INDEX.csv')
    assert {(r['mod_id'],r['source_path']):(r['git_blob_sha'],int(r['bytes'])) for r in code_entries}=={
        k:v for k,v in code.items() if k[0]!='MACAW'}
    ledgers={}
    for mod in ('AF','HC','MACAW'):
        source_rows=rows(bv/f'B_{mod}_SOURCE_BODIES.csv.gz')
        ledgers[mod]={r['path']:r for r in source_rows}
        assert len(ledgers[mod])==len(source_rows)
    observed={}
    source_records={}
    for mod,repo,version_key,mc_key,ns in (
        ('AF',args.af,'mod_version','minecraft_version','another_furniture'),
        ('HC',args.hc,'version','minecraftVersion','handcrafted'),
    ):
        r=registry[mod]
        pin=r['source_pin']
        assert git(repo,'rev-parse',pin+'^{tree}').decode().strip()==r['source_tree_sha']
        lic=git(repo,'show',pin+':'+r['license_path'])
        assert blob(lic)==r['license_blob_sha']
        assert b'MIT' in lic and b'all rights reserved' in lic.lower()
        props=dict(line.split('=',1) for line in git(repo,'show',pin+':gradle.properties').decode().splitlines()
                   if '=' in line and not line.lstrip().startswith('#'))
        props={k.strip():v.strip() for k,v in props.items()}
        assert props[version_key]==r['mod_version_pinned'] and props[mc_key]==r['mc_version_pinned']
        source_records[mod]={'pin':pin,'tree':r['source_tree_sha'],'mod_version':props[version_key],
                             'minecraft':props[mc_key],'license_sha':blob(lic),'license_record':r['license_terms']}
        observed[mod]=read_original(mod,ns,git_files(repo,pin),blob,ledgers[mod],texture_paths[mod],code)

    with zipfile.ZipFile(args.source_dir/'macaw.jar') as archive:
        names=archive.namelist()
        assert len(names)==len(set(names))==pinned_macaw['zip_entries']
        assert archive.testzip() is None
        meta=json.loads(archive.read('fabric.mod.json'))
        assert meta['id']=='mcwfurnitures' and meta['version']==pinned_macaw['mod_version']
        assert meta['license']==pinned_macaw['mod_metadata_license']
        assert meta['depends']['minecraft'].lstrip('~') in version['game_versions']
        assert hashlib.sha256(archive.read(pinned_macaw['embedded_license_name'])).hexdigest()==pinned_macaw['embedded_license_sha256']
        observed['MACAW']=read_original('MACAW','mcwfurnitures',
                                        ((path,archive.read(path)) for path in names if not path.endswith('/')),
                                        lambda body:hashlib.sha256(body).hexdigest(),ledgers['MACAW'],texture_paths['MACAW'],code)
    source_records['MACAW']={k:pinned_macaw[k] for k in ('version_id','project_id','mod_version','minecraft','loaders','url',
                             'sha1','sha256','sha512','distribution_license','mod_metadata_license','embedded_license_sha256')}
    for ver,m in json_file(c/'C_AUDIT.json')['vanilla_sources'].items():
        jar=args.source_dir/(ver+'.jar')
        assert (hashlib.sha1(jar.read_bytes()).hexdigest(),jar.stat().st_size)==(m['sha1'],m['size'])
        with zipfile.ZipFile(jar) as archive:
            for path, sha in texture_paths['MC'+ver].items():
                assert hashlib.sha256(archive.read(path)).hexdigest()==sha
    a=phase/'A'
    legacy=rows(a/'A_INPUT_MANIFEST.csv')
    assert len(legacy)==len({r['repo_path'] for r in legacy})==195
    for r in legacy:
        data=(root/r['repo_path']).read_bytes()
        assert (blob(data),len(data))==(r['git_blob_sha'],int(r['bytes'])),r['repo_path']
    previous=rows(a/'A_LATEST_MAIN_SOURCE_REHASH_20261118.csv')
    assert len(previous)==len({r['source_path'] for r in previous})==431
    for r in previous:
        mod=r['group'].split('_',1)[0]
        sha=observed[mod][r['source_path']][1]
        assert sha==r['expected_blob_sha']==r['computed_blob_sha'],r['source_path']
    code_refs=set()
    for r in rows(phase/'D/D_CODE_EVIDENCE.csv'):
        for ref in (r['registration_source']+'|'+r['code_sources']).split('|'):
            if not ref:
                continue
            path,sha=ref.rsplit('@',1)
            if (r['mod'],path) not in code and path.endswith('.class'):
                with zipfile.ZipFile(args.source_dir/'1.21.1.jar') as archive:
                    assert hashlib.sha256(archive.read(path)).hexdigest()==sha, path
            else:
                assert code[r['mod'],path][0]==sha, path
            code_refs.add((r['evidence_grade'],path,sha))
    scope=defaultdict(list)
    for mod,assets in observed.items():
        for path,(family,sha) in assets.items():
            kind=path.split('/models/',1)[1].split('/',1)[0] if family=='models' else family
            scope[mod,family,kind].append(sha)
    expected={(r['mod_id'],r['family'],r['resource_kind']):(int(r['direct_verified_paths']),int(r['distinct_paths']),int(r['distinct_hashes']))
              for r in rows(bv/'B_FIXED_THREE_SOURCE_SCOPE.csv')}
    assert {k:(len(v),len(v),len(set(v))) for k,v in scope.items()}==expected
    queue=rows(b/'ENTRY_QUEUE.csv')+rows(bv/'B_MACAW_ENTRY_QUEUE.csv')
    paths_by_entry=defaultdict(list)
    for ledger in ledgers.values():
        for r in ledger.values():
            paths_by_entry[r['entry_id']].append(r['path'])
    for r in code_entries:
        paths_by_entry[r['entry_id']].append(r['source_path'])
    assert len(queue)==len({r['entry_id'] for r in queue})==len(paths_by_entry)==137
    for r in queue:
        paths=paths_by_entry[r['entry_id']]
        assert len(paths)==len(set(paths))==int(r['file_count']),r['entry_id']
        assert {r['start_source_path'],r['end_source_path']}<=set(paths),r['entry_id']
    families=Counter(family for assets in observed.values() for family,_ in assets.values())
    assert families=={'models':16572,'blockstates':1158,'items':716}
    result={'status':'PASS','source_records':source_records,'families':families,'code_paths':len(code_entries),
            'A_historical_research_blobs':len(legacy),'A_prior_source_paths_crosschecked':len(previous),
            'macaw_classes':53,'distinct_D_code_references':len(code_refs),'queue_batches':len(queue),
            'scope':[dict(mod=k[0],family=k[1],kind=k[2],paths=len(v),distinct_content_hashes=len(set(v))) for k,v in sorted(scope.items())],
            'texture_dispositions':disposition,'texture_rows_rehashed':sum(bool(r['source_sha']) for r in textures),
            'unique_texture_paths_per_source':{k:len(v) for k,v in sorted(texture_paths.items())},
            'pixel_measurements':0,'errors':[]}
    args.out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__ == '__main__':
    main()
