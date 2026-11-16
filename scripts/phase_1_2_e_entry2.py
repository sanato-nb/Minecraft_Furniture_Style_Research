"""Inspect B-first twenty-eight source models, particle assets and D references."""
import csv
import hashlib
import io
import json
from collections import defaultdict
from pathlib import Path

from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'research/vanilla_models/phase_1-2-E'
OUT=BASE/'entry2'


def blob(data):
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()


def csvrows(path):
    with (ROOT/path).open(newline='') as f:return list(csv.DictReader(f))


def write(name, rows, fields):
    with (OUT/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fields,lineterminator='\n');w.writeheader();w.writerows(rows)


def model_path(ref):
    x=ref.split(':',1)
    return f'1.21.11/assets/{x[0] if len(x)==2 else "minecraft"}/models/{x[-1]}.json'


def main():
    qpath='research/vanilla_models/phase_1-2-E/E_FIXED_SCOPE_86.csv'
    q=csvrows(qpath);first=[r for r in q if r['entry']=='ENTRY2'];assert len(q)==86 and len(first)==28
    dpath='research/vanilla_models/phase_1-2-D/D_FIXED_SCOPE_1168.csv'
    d=csvrows(dpath)
    png_inventory={r['source_path']:r for r in csvrows('research/vanilla_models/v34/03_inventory_1111_block_texture_png_paths_git_shas.csv')}
    c_png={}
    for e in range(1,6):
        p=f'research/vanilla_models/phase_1-2-C/entry{e}/PNG_RGBA_EVIDENCE.csv'
        for r in csvrows(p):
            assert r['png_path'] not in c_png or c_png[r['png_path']]['png_sha']==r['png_sha']
            c_png[r['png_path']]=r
    uses=defaultdict(list)
    for r in d:
        data=json.loads((ROOT/r['source_path']).read_text())
        apps=data['variants'].values() if 'variants' in data else (x['apply'] for x in data['multipart'])
        for app in apps:
            for opt in (app if isinstance(app,list) else [app]):
                uses[model_path(opt['model'])].append({'blockstate_path':r['source_path'],'blockstate_sha':r['git_blob_sha'],'model_ref':opt['model']})
    OUT.mkdir(exist_ok=True)
    models=[];snapshots=[];png_links=[];d_links=[];unique_png={}
    for r in first:
        p=r['model_path'];raw=(ROOT/p).read_bytes();source_sha=blob(raw)
        assert source_sha==r['model_git_sha']
        model=json.loads(raw);snapshots.append({'path':p,'sha':source_sha,'json_text':raw.decode()})
        assert isinstance(model,dict)
        # One E2 template has no texture declaration; its missing particle is
        # evidence, not a PNG lookup failure.
        tex=model.get('textures',{});particle=tex.get('particle')
        pngpath='1.21.11/assets/minecraft/textures/'+particle.split(':',1)[-1]+'.png' if particle and particle!='minecraft:missingno' else ''
        pngsha='';prior=None
        if pngpath:
            assert (ROOT/pngpath).exists()
            pngraw=(ROOT/pngpath).read_bytes();pngsha=blob(pngraw)
            if pngpath in png_inventory:assert pngsha==png_inventory[pngpath]['git_blob_sha']
            im=Image.open(io.BytesIO(pngraw));im.load();rgba=im.convert('RGBA').tobytes()
            prior=c_png.get(pngpath)
            if prior:assert prior['png_sha']==pngsha and prior['rgba_sha256']==hashlib.sha256(rgba).hexdigest()
            unique_png[pngpath]={'png_path':pngpath,'png_sha':pngsha,'width':im.width,'height':im.height,
                 'rgba_sha256':hashlib.sha256(rgba).hexdigest(),'C_prior_RGBA_evidence':bool(prior),
                 'v34_block_inventory_evidence':pngpath in png_inventory,
                 'opaque_pixels':sum(rgba[i+3]==255 for i in range(0,len(rgba),4)),
                 'transparent_pixels':sum(rgba[i+3]==0 for i in range(0,len(rgba),4)),
                 'partial_alpha_pixels':sum(0<rgba[i+3]<255 for i in range(0,len(rgba),4))}
        refs=uses[p];declared=set(json.loads(r['D_blockstate_paths_json']))
        assert declared=={x['blockstate_path'] for x in refs} and len(refs)==int(r['D_rule_option_refs'])
        for use in refs:d_links.append({'model_path':p,'model_sha':source_sha,**use})
        models.append({'entry_row':r['entry_row'],'model_path':p,'model_sha':source_sha,
            'B_owner_scope':r['B_owner_scope'],'parent_key_present':'parent' in model,'parent_ref':model.get('parent'),
            'elements_key_present':'elements' in model,'own_elements':len(model.get('elements',[])),
            'texture_keys_json':json.dumps(sorted(tex),ensure_ascii=False),
            'particle_ref':particle,'particle_png_path':pngpath,'particle_png_sha':pngsha,
            'particle_source_status':'SOURCE_PNG_VERIFIED' if pngpath else 'MISSINGNO_SENTINEL_NO_SOURCE_PNG' if particle=='minecraft:missingno' else 'NO_PARTICLE_DECLARATION',
            'D_blockstate_paths_count':len(declared),'D_rule_option_refs':len(refs),
            'geometry_source_verdict':'NO_GENERAL_ELEMENTS_IN_SOURCE_CHAIN' if 'parent' not in model and not model.get('elements') else 'REVIEW_REQUIRED',
            'renderer_path_grade':'UNVERIFIED_RUNTIME_RENDERER',
            'particle_not_visible_geometry':True})
        if pngpath:
            png_links.append({'model_path':p,'particle_png_path':pngpath,'particle_png_sha':pngsha,
                             'rgba_sha256':unique_png[pngpath]['rgba_sha256'],'C_prior_RGBA_evidence':bool(prior)})
    write('E_ENTRY2_MODEL_SOURCE.csv',models,list(models[0]))
    write('E_ENTRY2_PARTICLE_LINKS.csv',png_links,list(png_links[0]))
    write('E_ENTRY2_PARTICLE_PNG_UNIQUE.csv',list(unique_png.values()),list(next(iter(unique_png.values()))))
    write('E_ENTRY2_D_BLOCKSTATE_LINKS.csv',d_links,list(d_links[0]))
    (OUT/'E_ENTRY2_ORIGINAL_28.json').write_text(json.dumps({'schema':'E_ENTRY2_ORIGINAL_28/v1','sources':snapshots},ensure_ascii=False,indent=2)+'\n')
    audit={'schema':'E_ENTRY2_SOURCE_AUDIT/v1','baseline_head':'449fde4d747fce95cecb3570b170ff24e2484a99',
           'E_queue_sha':blob((ROOT/qpath).read_bytes()),'models_direct_JSON_SHA':len(models),
           'source_parent_present':sum(x['parent_key_present'] for x in models),
           'source_own_elements':sum(x['own_elements'] for x in models),
           'particle_only_models':sum(x['texture_keys_json']=='["particle"]' for x in models),
           'models_without_texture_declaration':sum(x['texture_keys_json']=='[]' for x in models),
           'missingno_sentinel_without_source_PNG':sum(x['particle_ref']=='minecraft:missingno' for x in models),
           'distinct_particle_PNG_source_SHA_and_RGBA':len(unique_png),
           'C_prior_particle_PNG_RGBA':sum(x['C_prior_RGBA_evidence'] for x in unique_png.values()),
           'item_texture_PNG_direct_SHA_RGBA':sum('/textures/item/' in x for x in unique_png),
           'D_blockstate_model_rule_refs':len(d_links),'D_distinct_blockstate_paths':len({x['blockstate_path'] for x in d_links}),
           'renderer_runtime_proven':0,'models_uninspected_in_E':28,'E_complete':False}
    (OUT/'E_ENTRY2_AUDIT.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(audit,ensure_ascii=False,indent=2))


if __name__=='__main__':main()
