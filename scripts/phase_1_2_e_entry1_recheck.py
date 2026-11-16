"""Independent E1 snapshot, PNG and D reference audit."""
import csv
import hashlib
import io
import json
from collections import Counter
from pathlib import Path

from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'research/vanilla_models/phase_1-2-E/entry1'


def sha(raw):return hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()


def rows(p):
    with p.open(newline='') as f:return list(csv.DictReader(f))


def model_path(ref):
    if ':' in ref:ns,name=ref.split(':',1)
    else:ns,name='minecraft',ref
    return f'1.21.11/assets/{ns}/models/{name}.json'


def main():
    queue=rows(ROOT/'research/vanilla_models/phase_1-2-E/E_FIXED_SCOPE_86.csv')
    assigned=[x for x in queue if x['entry']=='ENTRY1']
    source=rows(BASE/'E_ENTRY1_MODEL_SOURCE.csv')
    snapshots=json.loads((BASE/'E_ENTRY1_ORIGINAL_30.json').read_text())['sources']
    pngs=rows(BASE/'E_ENTRY1_PARTICLE_PNG_UNIQUE.csv')
    links=rows(BASE/'E_ENTRY1_D_BLOCKSTATE_LINKS.csv')
    assert len(queue)==86 and len(assigned)==len(source)==len(snapshots)==30 and len(pngs)==25
    for a,s,t in zip(assigned,source,snapshots):
        p=a['model_path'];raw=(ROOT/p).read_bytes()
        assert p==s['model_path']==t['path'] and raw.decode()==t['json_text']
        assert sha(raw)==a['model_git_sha']==s['model_sha']==t['sha']
        d=json.loads(raw)
        assert set(d)=={'textures'} and set(d['textures'])=={'particle'}
        ref=d['textures']['particle'];path='1.21.11/assets/minecraft/textures/'+ref.split(':')[-1]+'.png'
        assert path==s['particle_png_path']
    for r in pngs:
        path=r['png_path'];raw=(ROOT/path).read_bytes();image=Image.open(io.BytesIO(raw));image.load();rgba=image.convert('RGBA').tobytes()
        assert sha(raw)==r['png_sha'] and hashlib.sha256(rgba).hexdigest()==r['rgba_sha256']
        assert (image.width,image.height)==(int(r['width']),int(r['height']))
    occurrences=Counter()
    for path in (ROOT/'1.21.11/assets/minecraft/blockstates').glob('*.json'):
        data=json.loads(path.read_text());apps=data['variants'].values() if 'variants' in data else (x['apply'] for x in data['multipart'])
        for app in apps:
            for opt in (app if isinstance(app,list) else [app]):
                key=(model_path(opt['model']),str(path.relative_to(ROOT)),opt['model'])
                occurrences[key]+=1
    ledger=Counter((x['model_path'],x['blockstate_path'],x['model_ref']) for x in links)
    for a in assigned:
        p=a['model_path'];expected={k:v for k,v in occurrences.items() if k[0]==p};observed={k:v for k,v in ledger.items() if k[0]==p}
        assert expected==observed and sum(expected.values())==int(a['D_rule_option_refs'])
    report={'schema':'E_ENTRY1_INDEPENDENT_RECHECK/v1','model_source_body_and_SHA':30,'particle_PNG_SHA_RGBA':25,
            'D_model_rule_references_recomputed':sum(ledger.values()),'E_queue_rows':86,'mismatches':0,'pass':True,
            'special_renderer_runtime_verified':False,'E_whole_stage_complete':False}
    (BASE/'E_ENTRY1_INDEPENDENT_RECHECK.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))


if __name__=='__main__':main()
