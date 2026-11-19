"""Start the pinned game client and write renderer/model observations for 1-5."""
from argparse import ArgumentParser
import csv
import json
import os
from pathlib import Path
import runpy
import subprocess
import tempfile
from zipfile import ZIP_DEFLATED, ZipFile

HERE=Path(__file__).resolve().parent
PHASE=HERE.parent
PREPARE=runpy.run_path(str(PHASE.parent/'phase_1-3/runtime_actions/run_probe.py'))['prepare']


def input_rows(path):
    with path.open(encoding='utf-8',newline='') as stream:
        return list(csv.DictReader(stream))


def targets(version):
    entries=[('BLOCK',r['case'],r['state_id'],r['assignment']) for r in input_rows(PHASE/'A/MOD_CASE_SCOPE.csv')
             if r['minecraft']==version]
    if version=='1.21.1':
        for lab,wood in [('S03', 'birch'),('S04','spruce')]:
            entries.append(('BLOCK',lab+'_VAR1',f'another_furniture:{wood}_chair','facing=south;tucked=false;variant=1'))
        for level in (1,2,3):
            for lit in ('false','true'):
                entries.append(('BLOCK',f'LAMP_{level}_{lit}','another_furniture:white_lamp',
                                f'base=true;facing=north;lit={lit};level={level}'))
        entries.extend(('BLOCK','REG_'+name,'another_furniture:'+name,'')
                       for name in ('unused/white_awning','stone_tombstone','service_bell'))
        entries.extend(('ITEM','ITEM_'+name,identifier,'') for name,identifier in (
            ('TOMBSTONE','another_furniture:stone_tombstone'),('BELL','another_furniture:service_bell'),
            ('HAMMER','another_furniture:furniture_hammer'),('WHITE_CUSHION','handcrafted:white_cushion')))
    else:
        vanilla={}
        for r in input_rows(PHASE/'A/VANILLA_CONTROL_OPTIONS.csv'):
            vanilla[r['control']]=('BLOCK',r['control'],'minecraft:'+r['block'],
                ';'.join(f'{k}={v}' for k,v in sorted(json.loads(r['properties']).items())))
        entries.extend(vanilla.values())
        entries.extend((('ITEM','ITEM_WHITE_BED','minecraft:white_bed',''),
                        ('BLOCK','V11_FOOT','minecraft:white_bed','facing=north;part=foot;occupied=false'),
                        ('BLOCK','V11_HEAD','minecraft:white_bed','facing=north;part=head;occupied=false')))
        for case in ('V01','V08','S35','S36'):
            _,_,block,ass=next(r for r in entries if r[1]==case)
            entries.append(('BLOCK',case+'_EAST',block,ass.replace('facing=north','facing=east')))
        entries.append(('BLOCK','V03_EAST','minecraft:oak_fence','east=true;north=false;south=false;west=false'))
    for r in input_rows(PHASE/'D/TEXTURE_EXPOSURE.csv'):
        if r['minecraft']==version:
            entries.append(('SPRITE','T'+r['texture_id'],r['resource_id'],''))
    return entries


def main():
    parser=ArgumentParser(description=__doc__)
    parser.add_argument('--version',required=True,choices=('1.21.1','1.21.11'))
    for arg in ('work','output','client-cache','ecj'):
        parser.add_argument('--'+arg,type=lambda name:Path(name).resolve(),required=arg in ('work','output'))
    parser.add_argument('--display')
    parser.add_argument('--keep-open',action='store_true')
    parser.add_argument('--exposure',action='store_true',
                        help='check item and break-particle textures after joining a test world')
    a=parser.parse_args()
    a.work.mkdir(parents=True,exist_ok=True)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    run,client,assets,index,libs=PREPARE(a.version,a.work,a.client_cache)
    game=run/'probe_game'
    (game/'options.txt').write_text('renderDistance:4\nsimulationDistance:5\nmaxFps:30\nguiScale:2\n',encoding='utf-8')
    loader=next(f for f in libs if f.name=='fabric-loader-0.18.4.jar')
    jar=game/'mods/research-comparison.jar'
    with tempfile.TemporaryDirectory() as tmp:
        classes=Path(tmp)
        compiler=['javac','--release','21'] if a.ecj is None else ['java','-jar',str(a.ecj),'-21','-proc:none']
        subprocess.run([*compiler,'-cp',str(loader),'-d',tmp,str(HERE/'ComparisonProbe.java')],check=True)
        with ZipFile(jar,'w',ZIP_DEFLATED) as z:
            for f in classes.rglob('*.class'):
                z.write(f,f.relative_to(classes))
            z.writestr('fabric.mod.json',json.dumps({'schemaVersion':1,'id':'research_comparison_probe',
                'version':'1.0.0','environment':'client','entrypoints':{'client':['research.ComparisonProbe']},
                'depends':{'fabricloader':'>=0.18.4','fabric-lifecycle-events-v1':'*'}}))
    requests=run/'comparison-targets.tsv'
    requests.write_text(''.join('\t'.join(row)+'\n' for row in targets(a.version)))
    env={**os.environ,'LIBGL_ALWAYS_SOFTWARE':'1','ALSOFT_DRIVERS':'null'}
    cmd=['java','-Xmx2G','-XX:ActiveProcessorCount=4',f'-Dresearch.mc={a.version}',
         f'-Dresearch.keep_open={str(a.keep_open).lower()}',
         f'-Dresearch.exposure={str(a.exposure).lower()}',f'-Dresearch.output={a.output}',
         f'-Dresearch.targets={requests}','-cp',os.pathsep.join(map(str,[client,*libs])),
         'net.fabricmc.loader.impl.launch.knot.KnotClient','--username','RenderAudit','--version',a.version,
         '--gameDir',str(game),'--assetsDir',str(assets),'--assetIndex',index,'--accessToken','0',
         '--width','1024','--height','684']
    if a.display:
        env['DISPLAY']=a.display
    else:
        cmd=['xvfb-run','-a',*cmd]
    a.output.unlink(missing_ok=True)
    try:
        with a.output.with_suffix('.log').open('w') as log:
            subprocess.run(cmd,cwd=game,env=env,stdout=log,stderr=subprocess.STDOUT,check=True,
                           timeout=600 if a.keep_open else 240)
    finally:
        jar.unlink(missing_ok=True)
    if not a.output.is_file():
        raise RuntimeError('Client exited without writing actual engine results')


if __name__=='__main__':
    main()
