"""Prepare pinned Fabric clients, run the engine probe, and summarize its audit."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import csv
import gzip
import hashlib
import json
import math
import os
from pathlib import Path
import shutil
import subprocess
from urllib.parse import unquote
import zipfile

HERE = Path(__file__).resolve().parent
D = HERE.parent / 'D'
CLIENTS = {'1.21.1':'30c73b1c5da787909b2f73340419fdf13b9def88',
           '1.21.11':'ba2df812c2d12e0219c489c4cd9a5e1f0760f5bd'}
MODS = {
    '1.21.1': [
        ('ulloLmqG/versions/8xUs6Teu/another_furniture-fabric-4.0.2.jar','c2f992081bdc4795ed6d87771a3b5f7c71103785'),
        ('pJmCFF0p/versions/f0pKpUWd/handcrafted-fabric-1.21.1-4.0.3.jar','a9579fecd7ed429c282be21d5c921d220197acc6'),
        ('G1hIVOrD/versions/Hf91FuVF/resourcefullib-fabric-1.21-3.0.12.jar','cb67e1302b5116953f45556cc61dbcf40d986ecd'),
        ('P7dR8mSH/versions/5SwzqWUu/fabric-api-0.116.18%2B1.21.1.jar','584d303f646287ee6be059ecb2fc451255be9ee9')],
    '1.21.11': [
        ('dtWC90iB/versions/xhmciaUD/mcw-furniture-3.4.2-mc1.21.11fabric.jar','28f0929b6005bc28b1bde475579c13020420ae9f'),
        ('P7dR8mSH/versions/6qAuTtLR/fabric-api-0.141.6%2B1.21.11.jar','c98467cbbaf4d197377266795ae015f4130d65b6')]
}


def download(url, path, expected=None):
    def valid():
        return path.exists() and (expected is None or hashlib.sha1(path.read_bytes()).hexdigest() == expected)
    if valid():
        return path
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix+'.part')
    subprocess.run(['curl','-fLsS','--retry','3','--max-time','50',url,'-o',str(temporary)], check=True)
    temporary.replace(path)
    if not valid():
        raise ValueError(f'SHA-1 mismatch: {path}')
    return path


def batch(tasks):
    with ThreadPoolExecutor(10) as pool:
        list(pool.map(lambda job: download(*job), tasks))


def prepare(version, work, client_cache):
    run = work / version
    run.mkdir(parents=True, exist_ok=True)
    manifest_url = 'https://piston-meta.mojang.com/mc/game/version_manifest_v2.json'
    manifest = json.loads(download(manifest_url, work/'manifest.json').read_bytes())
    info = next(row for row in manifest['versions'] if row['id'] == version)
    model = json.loads(download(info['url'],run/'version.json',info['sha1']).read_bytes())
    source = model['downloads']['client']
    if source['sha1'] != CLIENTS[version]:
        raise ValueError('Unexpected Minecraft client SHA')
    client = download(source['url'],client_cache or run/'client.jar',source['sha1'])
    fabric = json.loads(download(
        f'https://meta.fabricmc.net/v2/versions/loader/{version}/0.18.4/profile/json',run/'profile.json').read_bytes())
    tasks, order = [], []
    for lib in model['libraries']:
        if any(token in lib['name'] for token in ('natives-windows','natives-macos','natives-linux-arm','natives-freebsd')):
            continue
        item = lib['downloads'].get('artifact')
        if item:
            local = work/'libs'/item['path']
            tasks.append((item['url'],local,item['sha1']))
            order.append(local)
    for lib in fabric['libraries']:
        group, artifact, value = lib['name'].split(':')
        ref = f"{group.replace('.','/')}/{artifact}/{value}/{artifact}-{value}.jar"
        local = work/'libs'/ref
        tasks.append((lib['url']+ref,local,lib.get('sha1')))
        order.append(local)
    for ref, sha in MODS[version]:
        name = unquote(ref.rsplit('/',1)[-1])
        tasks.append(('https://cdn.modrinth.com/data/'+ref,run/'probe_game/mods'/name,sha))
    batch(tasks)
    assets = work/'assets'
    index = model['assetIndex']
    asset_paths = json.loads(download(index['url'],assets/'indexes'/f"{index['id']}.json",index['sha1']).read_bytes())
    hashes = {row['hash'] for name,row in asset_paths['objects'].items() if '/sounds/' not in name}
    batch([(f'https://resources.download.minecraft.net/{sha[:2]}/{sha}',assets/'objects'/sha[:2]/sha,sha)
           for sha in sorted(hashes)])
    return run, client, assets, index['id'], order


def call_engine(args):
    run, client, assets, index, libraries = prepare(args.version,args.work,args.client_cache)
    classes = run/'probe_classes'
    classes.mkdir(exist_ok=True)
    loader = next(path for path in libraries if path.name=='fabric-loader-0.18.4.jar')
    compiler = ['javac','--release','21'] if args.ecj is None else ['java','-jar',str(args.ecj),'-21','-proc:none']
    subprocess.run([*compiler,'-cp',str(loader),'-d',str(classes),str(HERE/'StateProbe.java')],check=True)
    mod_file = run/'probe_game/mods/research-probe.jar'
    with zipfile.ZipFile(mod_file,'w',zipfile.ZIP_DEFLATED) as jar:
        for source in classes.rglob('*.class'):
            jar.write(source,source.relative_to(classes))
        jar.writestr('fabric.mod.json',json.dumps({
            'schemaVersion':1,'id':'research_state_probe','version':'1.0.0','environment':'client',
            'entrypoints':{'client':['research.StateProbe']},
            'depends':{'fabricloader':'>=0.18.4','fabric-lifecycle-events-v1':'*'}}))
    game = run/'probe_game'
    game.mkdir(exist_ok=True)
    (game/'options.txt').write_text('renderDistance:2\nmaxFps:30\nguiScale:1\n',encoding='utf-8')
    target = args.output/'ENGINE_STATES.tsv'
    target.unlink(missing_ok=True)
    command = [
        'java','-Xmx3G','-XX:ActiveProcessorCount=4',f'-Dresearch.mc={args.version}',
        f'-Dresearch.output={target}','-cp',os.pathsep.join(map(str,[client,*libraries])),
        'net.fabricmc.loader.impl.launch.knot.KnotClient','--username','RenderAudit',
        '--version',args.version,'--gameDir',str(game),'--assetsDir',str(assets),
        '--assetIndex',index,'--accessToken','0','--width','640','--height','480',
    ]
    env = {**os.environ,'LIBGL_ALWAYS_SOFTWARE':'1','ALSOFT_DRIVERS':'null'}
    if args.display is not None:
        env['DISPLAY'] = args.display
    else:
        command = ['xvfb-run','-a',*command]
    with (args.output/'engine.log').open('w',encoding='utf-8') as log:
        subprocess.run(command,env=env,stdout=log,stderr=subprocess.STDOUT,check=True,timeout=360)
    return target


def condition_matches(cond, state):
    for key, value in cond.items():
        if key in ('AND','OR'):
            results = [condition_matches(child,state) for child in value]
            if not (all(results) if key == 'AND' else any(results)):
                return False
        elif value.startswith('!'):
            if state.get(key) in value[1:].split('|'):
                return False
        elif state.get(key) not in value.split('|'):
            return False
    return True


def audit(version, target, output, ledger):
    namespaces = {'another_furniture','handcrafted'} if version == '1.21.1' else {'mcwfurnitures'}
    with (ledger/'D_BLOCKSTATES.csv').open(newline='',encoding='utf-8') as stream:
        expected = {r['state_id']:r for r in csv.DictReader(stream) if r['state_id'].split(':')[0] in namespaces}
    rules = {name:[] for name in expected}
    with gzip.open(ledger/'D_STATE_RULES.csv.gz','rt',newline='',encoding='utf-8') as stream:
        for row in csv.DictReader(stream):
            name = row['state_id']
            if name not in rules:
                continue
            if row['kind'] == 'variants':
                cond = dict(field.split('=',1) for field in row['source_selector'].split(',') if field)
            else:
                cond = json.loads(row['condition'] or '{}')
            rules[name].append((cond,int(row['options'])))
    seen, controls, empty, errors, issues, box_count, total, no_multipart = set(), {}, 0, 0, [], 0, 0, 0
    unique = set()
    with target.open(newline='',encoding='utf-8') as stream:
        for row in csv.DictReader(stream,delimiter='\t'):
            name, props, status, raw = (row[key] for key in ('block','properties','status','boxes'))
            identity = (name, props)
            if identity in unique:
                raise ValueError(f'Duplicate real state {identity}')
            unique.add(identity)
            boxes = [tuple(map(float,part.split(','))) for part in raw.split(';') if part]
            if name.startswith('minecraft:'):
                controls[name] = boxes
                continue
            total += 1
            seen.add(name)
            state = dict(field.split('=',1) for field in props.split(',') if field)
            if name in expected:
                hits = [n for cond,n in rules[name] if condition_matches(cond,state)]
                if expected[name]['kind'] == 'variants' and len(hits) != 1:
                    issues.append((name,props,'VARIANT_MATCH_COUNT',len(hits)))
                if expected[name]['kind'] == 'multipart' and not hits:
                    no_multipart += 1
                    issues.append((name,props,'NO_MULTIPART_RULE',0))
            if status != 'OK':
                errors += 1
                issues.append((name,props,status,''))
            empty += status == 'OK' and not boxes
            for box in boxes:
                if len(box)!=6 or not all(map(math.isfinite,box)) or any(a>=b for a,b in zip(box[:3],box[3:])):
                    raise ValueError(f'Invalid collision box: {name} {box}')
            box_count += len(boxes)
    if controls != {'minecraft:air':[], 'minecraft:stone':[(0.,0.,0.,1.,1.,1.)]} or not seen:
        raise ValueError('Invalid engine controls or empty registry')
    missing = sorted(expected.keys() - seen)
    extra = sorted(seen - expected.keys())
    with (output/'ENGINE_RULE_EXCEPTIONS.csv').open('w',newline='',encoding='utf-8') as stream:
        writer = csv.writer(stream)
        writer.writerow(['block','properties','reason','matches'])
        writer.writerows(issues)
    result = dict(minecraft=version, d_source_resources=len(expected), d_resources_in_registry=len(expected.keys()&seen),
                  source_resource_without_registry_block=missing, registry_blocks_without_d_resource=extra,
                  registry_block_types=len(seen), engine_registered_states=total,
                  empty_context_collision_ok=total-errors, collision_context_errors=errors, empty_shapes=empty,
                  collision_boxes=box_count, variant_match_issues=sum(r[2]=='VARIANT_MATCH_COUNT' for r in issues),
                  multipart_states_without_rules=no_multipart)
    (output/'SUMMARY.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    with target.open('rb') as inp, gzip.open(target.with_suffix('.tsv.gz'),'wb') as out:
        shutil.copyfileobj(inp,out)
    target.unlink()
    print(json.dumps(result,ensure_ascii=False,indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--version',choices=tuple(CLIENTS),required=True)
    parser.add_argument('--work',type=lambda value: Path(value).resolve(),required=True)
    parser.add_argument('--output',type=lambda value: Path(value).resolve(),required=True)
    parser.add_argument('--client-cache',type=lambda value: Path(value).resolve())
    parser.add_argument('--ecj',type=lambda value: Path(value).resolve())
    parser.add_argument('--display')
    args = parser.parse_args()
    args.work.mkdir(parents=True,exist_ok=True)
    args.output.mkdir(parents=True,exist_ok=True)
    target = call_engine(args)
    audit(args.version,target,args.output,D)


if __name__ == '__main__':
    main()
