"""Launch a pinned, offline Fabric client and record the actual 1.21.1 atlas."""
from argparse import ArgumentParser
import csv
import json
import os
from pathlib import Path
import runpy
import subprocess
import tempfile
from zipfile import ZipFile, ZIP_DEFLATED

HERE = Path(__file__).resolve().parent
PHASE = HERE.parent
PREPARE = runpy.run_path(str(PHASE.parent/'phase_1-3/runtime_actions/run_probe.py'))['prepare']


def targets(path):
    with (PHASE/'entry04/TEXTURE_EXCEPTION_REVIEW.csv').open() as f:
        missing = {r['resource_id'] for r in csv.DictReader(f) if r['finding'].startswith('MISSING')}
    with (PHASE/'entry04/ALTERNATE_ASSET_CANDIDATES.csv').open() as f:
        candidates = {'another_furniture:'+r['candidate_path'].split('/textures/',1)[1].removesuffix('.png')
                      for r in csv.DictReader(f)}
    sprites = sorted(missing|candidates|{'minecraft:missingno','minecraft:block/iron_block',
                                          'another_furniture:block/service_bell'})
    controls = ['another_furniture:'+name for name in ('oak_chair','service_bell','stone_tombstone',
                                                        'stone_gravestone','white_tablecloth','tablecloth')]
    data = [f'SPRITE\t{name}' for name in sprites]
    data += [f'{kind}\t{name}' for kind in ('BLOCK','ITEM') for name in controls]
    path.write_text('\n'.join(data)+'\n',encoding='utf-8')


def main():
    parser=ArgumentParser(description=__doc__)
    for name in ('work','output','client-cache','ecj'):
        parser.add_argument('--'+name,type=lambda arg:Path(arg).resolve(),required=name in ('work','output'))
    parser.add_argument('--display')
    args=parser.parse_args()
    args.work.mkdir(parents=True,exist_ok=True)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    run, client, assets, index, libs = PREPARE('1.21.1',args.work,args.client_cache)
    loader = next(path for path in libs if path.name=='fabric-loader-0.18.4.jar')
    game = run/'probe_game'
    (game/'options.txt').write_text('renderDistance:2\nmaxFps:30\nguiScale:1\n',encoding='utf-8')
    with tempfile.TemporaryDirectory() as directory:
        classes = Path(directory)
        compiler = ['javac','--release','21'] if not args.ecj else ['java','-jar',str(args.ecj),'-21','-proc:none']
        subprocess.run([*compiler,'-cp',str(loader),'-d',str(classes),str(HERE/'AtlasProbe.java')],check=True)
        jar_path = game/'mods/research-atlas.jar'
        with ZipFile(jar_path,'w',ZIP_DEFLATED) as jar:
            for f in classes.rglob('*.class'):
                jar.write(f,f.relative_to(classes))
            jar.writestr('fabric.mod.json',json.dumps({'schemaVersion':1,'id':'research_atlas_probe',
                'version':'1.0.0','environment':'client','entrypoints':{'client':['research.AtlasProbe']},
                'depends':{'fabricloader':'>=0.18.4','fabric-lifecycle-events-v1':'*'}}))
    request=run/'atlas-targets.tsv'
    targets(request)
    args.output.unlink(missing_ok=True)
    env={**os.environ,'LIBGL_ALWAYS_SOFTWARE':'1','ALSOFT_DRIVERS':'null'}
    command=['java','-Xmx3G','-XX:ActiveProcessorCount=4',f'-Dresearch.output={args.output}',
             f'-Dresearch.targets={request}','-cp',os.pathsep.join(map(str,[client,*libs])),
             'net.fabricmc.loader.impl.launch.knot.KnotClient','--username','RenderAudit','--version','1.21.1',
             '--gameDir',str(game),'--assetsDir',str(assets),'--assetIndex',index,'--accessToken','0',
             '--width','640','--height','480']
    if args.display:
        env['DISPLAY']=args.display
    else:
        command=['xvfb-run','-a',*command]
    try:
        with args.output.with_suffix('.log').open('w') as log:
            subprocess.run(command,cwd=game,env=env,stdout=log,stderr=subprocess.STDOUT,check=True,timeout=240)
    finally:
        jar_path.unlink(missing_ok=True)
    if not args.output.exists():
        raise RuntimeError('The client exited without an atlas report')


if __name__=='__main__':
    main()
