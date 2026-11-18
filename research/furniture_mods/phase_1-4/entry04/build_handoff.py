"""Build the 1-4 exception, provenance and 1-5 comparison database."""
import argparse
from collections import Counter, defaultdict
import csv
from fractions import Fraction
import gzip
import hashlib
import json
import lzma
from pathlib import Path
import re
import sqlite3
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
STAGE = HERE.parent
PHASE = STAGE.parent/'phase_1-3'
ENTRY02 = STAGE/'entry02'
ENTRY03 = STAGE/'entry03'


def rows(path):
    opener = {'.xz':lzma.open,'.gz':gzip.open}.get(path.suffix,open)
    with opener(path,'rt',encoding='utf-8',newline='') as stream:
        yield from csv.DictReader(stream)


def write(path, fields, records):
    opener = lzma.open if path.suffix=='.xz' else open
    with opener(path,'wt',encoding='utf-8',newline='') as stream:
        writer=csv.writer(stream,lineterminator='\n')
        writer.writerow(fields)
        writer.writerows(records)


def git_blob(body):
    return hashlib.sha1(f'blob {len(body)}\0'.encode()+body).hexdigest()


def vector(text):
    return tuple(map(Fraction,text.split('|')))


def verify_source_tree(repo, pin):
    data=subprocess.check_output(['git','-C',repo,'ls-tree','-r','-z',pin])
    tree={}
    for entry in data.decode().split('\0'):
        if entry:
            header,path=entry.split('\t',1)
            tree[path]=header.split()[2]
    return tree


def alternates(resource, tree):
    _, relative=resource.split(':')
    tail=relative.removeprefix('block/')
    expected='/assets/another_furniture/textures/'+relative+'.png'
    pngs=[path for path in tree if '/assets/another_furniture/textures/block/' in path and path.endswith('.png')]
    assert not any(path.endswith(expected) for path in pngs), resource
    alias={'chair/oak_bottom':'chair/bottom/oak','chair/oak_seat':'chair/seat/oak'}
    for path in pngs:
        local=path.split('/textures/block/',1)[1].removesuffix('.png')
        if local=='unused/'+tail:
            yield path,tree[path],'UNUSED_SUBDIRECTORY'
        elif local==alias.get(tail):
            yield path,tree[path],'REORDERED_PATH'
        elif tail=='chair/oak_back' and re.fullmatch(r'chair/back_\d+/oak',local):
            yield path,tree[path],'VARIANT_SPECIFIC_PATH'


def trace_exceptions(base, db, queue, af, out):
    pins=dict(base.execute('SELECT id,pin FROM source'))
    tree=verify_source_tree(str(af),pins['AF'])
    options=Counter(dict(base.execute('SELECT model_key,count(*) FROM option GROUP BY model_key')))
    slot_sql='''SELECT s.model_key,m.resource_id,m.path,m.sha,s.slot,s.face_count
                FROM model_slot s JOIN model m USING(model_key)
                WHERE s.texture_id=? ORDER BY s.model_key,s.slot'''
    summaries=[]
    evidence=[]
    bindings=[]
    for tid,r in sorted(queue.items()):
        if r['disposition'] not in {'SOURCE_EXCEPTION','DECLARED_SLOT_ONLY'}:
            continue
        records=base.execute(slot_sql,(tid,)).fetchall()
        face_count=sum(row[-1] for row in records)
        particles=sum(row[-2]=='#particle' for row in records)
        item_faces=sum(row[-1] for row in records if ':item/' in row[1])
        state_models={row[0] for row in records if options[row[0]]}
        state_faces=sum(row[-1]*options[row[0]] for row in records)
        if r['disposition']=='SOURCE_EXCEPTION':
            assert not r['path'] and not r['source_sha'] and r['resource_id'].startswith('another_furniture:')
            candidates=list(alternates(r['resource_id'],tree))
            for path, sha, rationale in candidates:
                body=subprocess.check_output(['git','-C',af,'show',pins['AF']+':'+path])
                assert body.startswith(b'\x89PNG\r\n\x1a\n') and git_blob(body)==sha
                evidence.append((tid,path,sha,rationale))
            conclusion='MISSING_FACE_PATH' if face_count else 'MISSING_DECLARATION_PATH'
            assert not state_models
        else:
            assert r['source_sha'] and not face_count
            conclusion='DECLARATION_WITH_PARTICLE' if particles else 'DECLARATION_WITHOUT_MODEL_FACE'
        assert face_count==int(r['face_instances'])
        assert sum(row[-1]==0 for row in records)==int(r['non_face_slot_count'])
        summaries.append((tid,conclusion,len(records),particles,face_count,state_faces,len(state_models),item_faces))
        bindings.extend((tid,*row,options[row[0]]) for row in records)
    assert len(summaries)==85
    db.executemany('INSERT INTO texture_exception VALUES (?,?,?,?,?,?,?,?)',summaries)
    db.executemany('INSERT INTO exception_slot VALUES (?,?,?,?,?,?,?,?)',bindings)
    db.executemany('INSERT INTO alternate_asset VALUES (?,?,?,?)',evidence)
    write(out/'TEXTURE_EXCEPTION_REVIEW.csv',
          ('texture_id','resource_id','finding','model_slots','particle_slots','face_instances',
           'blockstate_option_face_instances','models_with_direct_state_option','item_model_faces'),
          ((r[0],queue[r[0]]['resource_id'],*r[1:]) for r in summaries))
    write(out/'ALTERNATE_ASSET_CANDIDATES.csv',('texture_id','candidate_path','sha','basis'),evidence)
    return len(bindings),len(evidence)


def link_prior(base, db, queue, input_faces, out):
    history=[r for r in rows(PHASE/'F/F_PRIOR_RGBA_LEDGER.csv') if r['evidence_unit']=='FACE_RGBA']
    hc_path=ROOT/'research/furniture_mods/v17/handcrafted_16_leaf_face_rects_786.csv'
    hc={(r['leaf'],r['element_index'],r['face']):r for r in rows(hc_path)}
    models={(mod,resource):(key,sha) for key,mod,resource,sha in
            base.execute('SELECT model_key,source_id,resource_id,sha FROM model')}
    model_shas={key:sha for key,sha in base.execute('SELECT model_key,sha FROM model')}
    ns={'HC':'handcrafted','AF':'another_furniture'}
    requested=[]
    targets=set()
    for record in history:
        ledger=record['ledger_path']
        assert git_blob((ROOT/ledger).read_bytes())==record['ledger_blob_sha']
        old=list(rows(ROOT/ledger))
        assert len(old)==int(record['rows_recounted'])
        mod=record['mod']
        for index,r in enumerate(old,2):
            model,sha=models.get((mod,ns[mod]+':block/'+r['leaf']),('',None))
            key=model,r['element_index'],r['face']
            target=hc[r['leaf'],r['element_index'],r['face']] if mod=='HC' else r
            targets.add(key)
            requested.append((ledger,index,mod,key,sha,r,target))
    current={(r['model_key'],r['element_index'],r['direction']):r for r in rows(input_faces)
             if (r['model_key'],r['element_index'],r['direction']) in targets}
    region_keys={(r['texture_id'],r['uv']) for r in current.values() if r['status']=='STATIC_RECT'}
    regions={(r['texture_id'],r['uv']):r for path in sorted(ENTRY02.glob('UV_REGIONS_*.csv.xz'))
             for r in rows(path) if r['frame']=='0' and (r['texture_id'],r['uv']) in region_keys}
    result=[]
    for ledger,index,mod,key,sha,r,src in requested:
        observed=current.get(key)
        model,element,direction=key
        provider,tid,uv,rgba=None,None,None,None
        finding='MODEL_FACE_KEY_ABSENT'
        if observed:
            provider=observed['provider_key']
            tid=int(observed['texture_id']) if observed['texture_id'] else None
            uv=observed['uv']
            leaf_sha=src.get('leaf_sha') or src.get('original_leaf_sha')
            parent_sha=src.get('parent_sha') or src.get('original_template_sha') or src.get('parent_template_sha')
            texture_name=r['png_name'] if ':' in r['png_name'] else ns[mod]+':block/'+r['png_name']
            raw_uv=src.get('uv_raw') or src.get('original_uv') or src.get('source_uv')
            if mod=='HC':
                raw_uv='|'.join(src[k] for k in ('uv_u1','uv_v1','uv_u2','uv_v2'))
            sample=regions.get((str(tid),uv))
            if (leaf_sha,parent_sha)!=(sha,model_shas[provider]):
                finding='MODEL_OR_PROVIDER_SHA_DIFFERS'
            elif not tid or (texture_name,r['png_sha'])!=(queue[tid]['resource_id'],queue[tid]['source_sha']):
                finding='TEXTURE_ID_OR_SHA_DIFFERS'
            elif raw_uv and vector(raw_uv)!=vector(uv):
                finding='DECLARED_UV_DIFFERS'
            elif (int(r['face_uv_rotation']),int(r['uv_reversed'])) != (
                  int(observed['uv_rotation']),int(bool(int(observed['u_reversed']) or int(observed['v_reversed'])))):
                finding='FACE_ORIENTATION_DIFFERS'
            elif observed['status']=='ZERO_UV_AREA' and r['status']=='zero_uv_area':
                finding='BOTH_ZERO_UV_NO_PIXELS'
            elif sample is None or observed['status']!='STATIC_RECT':
                finding='STATIC_SAMPLE_UNAVAILABLE'
            else:
                box='|'.join(r[k] for k in ('pixel_x0','pixel_y0','pixel_x1','pixel_y1'))
                area=int(sample['opaque'])+int(sample['transparent'])+int(sample['partial_alpha'])
                if vector(box)!=vector(sample['pixel_box']):
                    finding='PIXEL_RECTANGLE_DIFFERS'
                elif tuple(int(r[k]) for k in ('rect_texels','transparent_texels','partial_alpha_texels','visible_texels')) != (
                        area,int(sample['transparent']),int(sample['partial_alpha']),area-int(sample['transparent'])):
                    finding='PIXEL_TOTALS_DIFFER'
                else:
                    finding='MATCHED_PRIOR_FACE_SOURCE_AND_RECT'
                    rgba=sample['rgba8_sha256']
        result.append((ledger,index,finding,model or None,provider,int(element),direction,tid,uv,rgba))
    assert len(result)==4113
    db.executemany('INSERT INTO prior_face VALUES (?,?,?,?,?,?,?,?,?,?)',result)
    write(out/'PRIOR_FACE_LINKS.csv.xz',('ledger','row','finding','model_key','provider_key','element_index',
                                      'direction','texture_id','uv','entry02_rgba_sha256'),result)
    return dict(Counter(r[2] for r in result))


def comparison(db, out):
    applications=list(rows(PHASE/'F/F_1-5_COMPARISON_CANDIDATES.csv'))
    db.executemany('INSERT INTO comparison_application VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)',(
        (r['sample_id'],r['rule_index'],r['option_index'],r['category'],r['mod'],r['state_id'],r['state_sha'],
         r['model_key'],r['model_sha'],r['provider_key'],r['provider_sha'],r['x'],r['y'],int(r['uvlock']=='true'))
        for r in applications))
    records=list(rows(ENTRY03/'SAMPLE_FACES.csv.xz'))
    db.executemany('INSERT INTO comparison_face VALUES (?,?,?,?,?,?,?,?,?,?,?,?)',(
        (r['case'],r['rule_index'],r['option_index'],r['element_index'],r['direction'],r['texture_id'] or None,
         r['uv'],r['status'],r['region_frame_count'],r['density_u'],r['density_v'],r['rgba_sha256'] or None)
        for r in records))
    sql='''SELECT a.case_id,a.rule_index,a.option_index,a.category,a.mod,a.state_id,a.state_sha,
                  a.model_key,a.model_sha,a.provider_key,a.provider_sha,a.x,a.y,a.uvlock,
                  count(*),sum(f.status='STATIC_RECT'),sum(f.status='ANIMATED_FRAME_RECTS'),
                  sum(f.status='ZERO_UV_AREA'),count(DISTINCT f.texture_id),
                  sum(t.resource_id LIKE 'minecraft:%' AND f.frames>0)
           FROM comparison_application a JOIN comparison_face f USING(case_id,rule_index,option_index)
           LEFT JOIN texture t ON t.id=f.texture_id GROUP BY a.case_id,a.rule_index,a.option_index
           ORDER BY a.case_id,a.rule_index,a.option_index'''
    handoff=db.execute(sql).fetchall()
    write(out/'1-5_TEXTURE_UV_HANDOFF.csv',('case','rule_index','option_index','category','mod','state_id','state_sha',
                                         'model_key','model_sha','provider_key','provider_sha','x','y','uvlock',
                                         'face_instances','static_faces','animated_faces','zero_uv_faces',
                                         'distinct_texture_ids','sampled_vanilla_faces'),handoff)
    assert len(handoff)==52 and len(records)==1610
    return len(handoff),len(records)


def main(args):
    out=args.out
    out.mkdir(parents=True,exist_ok=True)
    base=sqlite3.connect(':memory:')
    base.deserialize(lzma.decompress((PHASE/'F/furniture_research.sqlite.xz').read_bytes()))
    queue={int(r['texture_id']):r for r in rows(PHASE/'F/1-3_TEXTURE_UV_HANDOFF.csv')}
    with sqlite3.connect(':memory:') as db:
        db.executescript((HERE/'schema.sql').read_text())
        artifacts=[PHASE/'F'/name for name in ('furniture_research.sqlite.xz','1-3_TEXTURE_UV_HANDOFF.csv',
                                               'F_PRIOR_RGBA_LEDGER.csv','F_1-5_COMPARISON_CANDIDATES.csv')]
        artifacts += sorted(ENTRY02.glob('UV_REGIONS_*.csv.xz'))
        artifacts += [ENTRY02/'TEXTURE_UV_COUNTS.csv.xz',ENTRY03/'SAMPLE_FACES.csv.xz',
                      ROOT/'research/furniture_mods/v17/handcrafted_16_leaf_face_rects_786.csv']
        artifacts += [ROOT/r['ledger_path'] for r in rows(PHASE/'F/F_PRIOR_RGBA_LEDGER.csv') if r['evidence_unit']=='FACE_RGBA']
        db.executemany('INSERT INTO input_artifact VALUES (?,?)',(
            (p.relative_to(ROOT).as_posix(),hashlib.sha256(p.read_bytes()).hexdigest()) for p in artifacts))
        db.executemany('INSERT INTO texture VALUES (?,?,?,?,?,?,?,?)',(
            (tid,r['resource_id'],r['minecraft'],r['source_id'] or None,r['path'] or None,r['source_sha'] or None,
             r['source_hash_kind'] or None,r['disposition']) for tid,r in sorted(queue.items())))
        keys=('texture_id','frame_width','frame_height','frame_count','uv_regions','static','animated','zero_uv','outside_uv')
        db.executemany('INSERT INTO texture_uv_counts VALUES (?,?,?,?,?,?,?,?,?)',(
            tuple(r[k] for k in keys) for r in rows(ENTRY02/'TEXTURE_UV_COUNTS.csv.xz')))
        slot_count,alt_count=trace_exceptions(base,db,queue,args.af,out)
        prior=link_prior(base,db,queue,args.faces,out)
        apps,faces=comparison(db,out)
        assert db.execute('PRAGMA integrity_check').fetchone()==('ok',)
        assert db.execute('PRAGMA foreign_key_check').fetchall()==[]
        exception_counts=db.execute('''
            SELECT t.disposition,count(*),sum(e.face_instances),sum(e.item_model_faces),
                   sum(e.model_slots),sum(e.particle_slots),sum(e.blockstate_models),sum(e.blockstate_option_faces)
            FROM texture_exception e JOIN texture t ON t.id=e.texture_id GROUP BY t.disposition
        ''').fetchall()
        uv_counts=db.execute('SELECT count(*),sum(static_faces),sum(animated_faces),sum(zero_uv_faces),sum(outside_uv_faces) FROM texture_uv_counts').fetchone()
        db.commit()
        db.execute('VACUUM')
        (out/'research_texture_uv.sqlite.xz').write_bytes(lzma.compress(db.serialize()))
    summary_fields=('textures','faces','item_model_faces','model_slots','particle_slots',
                    'texture_model_pairs_with_state_options','blockstate_option_faces')
    audit=dict(texture_rows=len(queue),
               normalized_uv_counts=dict(zip(('textures','static_faces','animated_faces','zero_uv_faces','outside_uv_faces'),uv_counts)),
               exception_counts={r[0]:dict(zip(summary_fields,r[1:])) for r in exception_counts},
               model_faces_input_sha256=hashlib.sha256(args.faces.read_bytes()).hexdigest(),
               slot_rows=slot_count,candidate_asset_rows=alt_count,prior_face_findings=prior,
               comparison_applications=apps,comparison_faces=faces,integrity='ok',foreign_key_errors=0)
    encoded=json.dumps(audit,indent=2,sort_keys=True)+'\n'
    (out/'E_AUDIT.json').write_text(encoded)
    print(encoded)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for name in ('af','faces','out'):
        p.add_argument('--'+name,type=Path,required=True)
    main(p.parse_args())
