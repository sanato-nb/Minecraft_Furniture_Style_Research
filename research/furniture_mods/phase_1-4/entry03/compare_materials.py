"""Compare the fixed 1-3-E samples with measured static UV and original PNGs."""
import argparse
from collections import Counter, defaultdict
from contextlib import ExitStack
import csv
from fractions import Fraction
import hashlib
import json
import lzma
from pathlib import Path
import runpy
import sqlite3
from statistics import median
import zipfile

HERE = Path(__file__).resolve().parent
PHASE = HERE.parents[1] / 'phase_1-3'
ENTRY02 = HERE.parent / 'entry02'
UV = runpy.run_path(str(ENTRY02/'measure_uv.py'))
FIRST = UV['FIRST']
CONTROL_MODELS = ('oak_planks', 'stripped_oak_log', 'white_wool', 'bookshelf')
PAIRS = (
    ('S01','S02','chair_tuck'), ('S06','S07','chair_cushion'),
    ('S12','S13','table_connection'), ('S14','S15','multipart_table_legs'),
    ('S16','S17','table_connection'), ('S18','S19','table_connection'),
    ('S20','S21','drawer_open'), ('S28','S29','bookshelf_connection'),
    ('S30','S31','bench_back'), ('S33','S34','couch_corner'), ('S35','S36','couch_corner'),
    ('S37','S38','bed_foot_head'), ('S39','S40','counter_finish'),
    ('S42','S43','sink_water'), ('S44','S45','lamp_light'),
)
SAMPLED = {'STATIC_RECT','ANIMATED_FRAME_RECTS'}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read_csv(path):
    return UV['read_csv'](path)


def write(path, rows):
    opener = lzma.open if path.suffix == '.xz' else open
    with opener(path, 'wt', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def color_stats(image, box):
    crop = image.crop(box)
    pixels = list(crop.get_flattened_data() if hasattr(crop, 'get_flattened_data') else crop.getdata())
    colors = Counter((r,g,b) for r,g,b,a in pixels if a)
    lumas = {rgb:(2126*rgb[0]+7152*rgb[1]+722*rgb[2])/10000 for rgb in colors}
    n = sum(colors.values())
    mean = sum(lumas[rgb]*count for rgb,count in colors.items())/n if n else None
    variance = sum((lumas[rgb]-mean)**2*count for rgb,count in colors.items())/n if n else None
    best = sorted(colors, key=lambda rgb:(-colors[rgb],rgb))[:4]
    return {
        'pixels':len(pixels), 'alpha_zero':sum(a==0 for _,_,_,a in pixels),
        'alpha_partial':sum(0<a<255 for _,_,_,a in pixels), 'visible_rgb':len(colors),
        'visible_luma_mean':round(mean,4) if n else '',
        'visible_luma_stddev':round(variance**0.5,4) if n else '',
        'visible_luma_span':round(max(lumas.values())-min(lumas.values()),4) if n else '',
        'top_rgb': '|'.join(f'{bytes(rgb).hex()}:{colors[rgb]}' for rgb in best),
        'rgba_sha256':digest(crop.tobytes()),
    }


def controls(jars):
    output=[]
    for version, jar in jars.items():
        for name in CONTROL_MODELS:
            model_path=f'assets/minecraft/models/block/{name}.json'
            body=jar.read(model_path)
            leaf=json.loads(body)
            parent_path='assets/minecraft/models/'+leaf['parent'].split(':')[-1]+'.json'
            parent_body=jar.read(parent_path)
            parent=json.loads(parent_body)
            cube_path='assets/minecraft/models/'+parent['parent'].split(':')[-1]+'.json'
            cube_body=jar.read(cube_path)
            element,=json.loads(cube_body)['elements']
            assert element['from']==[0,0,0] and element['to']==[16,16,16]
            slots=parent['textures'] | leaf['textures']
            for direction,face in element['faces'].items():
                rid=FIRST['resolve'](face['texture'],slots)
                texture_path='assets/'+rid.replace(':','/textures/')+'.png'
                png=jar.read(texture_path)
                image, frame_count,*_=FIRST['decode_png'](png)
                assert frame_count==1 and texture_path+'.mcmeta' not in jar.namelist()
                uv=tuple(face['uv']) if 'uv' in face else UV['default_uv'](element['from'],element['to'],direction)
                assert uv==(0,0,16,16)
                output.append(dict(version=version, model_path=model_path, model_sha256=digest(body),
                                   parent_path=parent_path,parent_sha256=digest(parent_body),
                                   geometry_path=cube_path, geometry_sha256=digest(cube_body), side=direction,
                                   texture_path=texture_path,texture_sha256=digest(png),
                                   density_u=str(Fraction(image.width,16)),density_v=str(Fraction(image.height,16)),
                                   **color_stats(image,(0,0,image.width,image.height))))
    return output


def case_summary(source, face_rows, models, elements):
    frame0=[f for f in face_rows if f['status'] in SAMPLED]
    visible=[f for f in frame0 if f['visible_rgb']>0]
    density=[Fraction(f[key]) for f in frame0 for key in ('density_u','density_v') if f[key]]
    statuses=Counter(f['status'] for f in face_rows)
    frames=Counter(f['region_frame_count'] for f in frame0)
    direction_textures=defaultdict(set)
    for f in frame0:
        direction_textures[f['direction']].add(f['texture_id'])
    assert len(face_rows)==int(source['effective_faces'])
    assert len(elements)==int(source['effective_elements'])
    assert len(models)==int(source['model_applications'])
    return dict(case=source['case'],category=source['category'],mod=source['mod'],
                block=source['block'],state=source['state'],assembly_sha=source['geometry_assembly_sha'],
                geometry_providers='|'.join(sorted({m['provider_key'] for m in models})),
                model_applications=len(models),elements=len(elements),
                zero_thickness_elements=sum(bool(e['zero_axes']) for e in elements),
                sampled_faces=len(frame0),total_faces=len(face_rows),face_statuses=json.dumps(statuses,sort_keys=True),
                faces_with_alpha_zero=sum(f['alpha_zero']>0 for f in frame0),
                faces_with_alpha_partial=sum(f['alpha_partial']>0 for f in frame0),
                faces_fully_transparent=sum(f['alpha_zero']==f['pixels'] for f in frame0),
                sampled_texture_ids='|'.join(sorted({f['texture_id'] for f in frame0},key=int)),
                sampled_vanilla_texture_ids='|'.join(sorted({f['texture_id'] for f in frame0
                                                             if f['resource_id'].startswith('minecraft:')},key=int)),
                direction_texture_ids=';'.join(key+'='+','.join(sorted(ids,key=int))
                                               for key,ids in sorted(direction_textures.items())),
                distinct_texture_uv=len({(f['texture_id'],f['uv']) for f in frame0}),
                distinct_rgba_frame0=len({f['rgba_sha256'] for f in frame0}),
                median_visible_colors=median(f['visible_rgb'] for f in visible) if visible else '',
                median_visible_luma_stddev=round(median(f['visible_luma_stddev'] for f in visible),4) if visible else '',
                density_min=str(min(density)) if density else '',density_median=str(median(density)) if density else '',
                density_max=str(max(density)) if density else '',
                sampled_frames_per_face=json.dumps(frames,sort_keys=True))


def main(args):
    out=args.out
    out.mkdir(parents=True,exist_ok=True)
    e=PHASE/'E'
    cases=read_csv(e/'E_SAMPLE_METRICS.csv')
    applications=read_csv(e/'CATEGORY_EVIDENCE.csv')
    elements=read_csv(e/'E_ELEMENT_EVIDENCE.csv')
    queue={r['texture_id']:r for r in read_csv(PHASE/'F/1-3_TEXTURE_UV_HANDOFF.csv')}
    app_keys={(r['case'],r['rule_index'],r['option_index']) for r in applications}
    handoff={(r['sample_id'],r['rule_index'],r['option_index']):r
             for r in read_csv(PHASE/'F/F_1-5_COMPARISON_CANDIDATES.csv')}
    assert len(app_keys)==len(applications)==52 and app_keys==handoff.keys()
    assert len(cases)==47 and len(elements)==335
    model_keys={r['model_key'] for r in applications}
    faces=defaultdict(list)
    for face in xz_rows(args.faces) if args.faces.suffix=='.xz' else read_csv(args.faces):
        if face['model_key'] in model_keys:
            faces[face['model_key']].append(face)
    assert model_keys==faces.keys()
    sample_textures={f['texture_id'] for group in faces.values() for f in group if f['status'] in SAMPLED}
    target_uv={(f['texture_id'],f['uv']) for group in faces.values() for f in group if f['status'] in SAMPLED}
    regions=defaultdict(list)
    for path in sorted(ENTRY02.glob('UV_REGIONS_*.csv.xz')):
        for region in xz_rows(path):
            key=region['texture_id'],region['uv']
            if key in target_uv:
                regions[key].append(region)
    assert target_uv==regions.keys()
    origins=defaultdict(set)
    for tid in sample_textures:
        row=queue[tid]
        origins[row['source_id']].update((row['path'],row['path']+'.mcmeta'))
    with ExitStack() as stack:
        db=stack.enter_context(sqlite3.connect(':memory:'))
        db.deserialize(lzma.decompress((PHASE/'F/furniture_research.sqlite.xz').read_bytes()))
        pins=dict(db.execute('SELECT id,pin FROM source'))
        model_shas=dict(db.execute('SELECT model_key,sha FROM model'))
        sources={source:FIRST['archived'](repo,pins[source],origins[source]).get
                 for source,repo in (('AF',args.af),('HC',args.hc))}
        jars={}
        for source,name,algorithm in (('MACAW','macaw.jar','sha256'),('MC1.21.1','1.21.1.jar','sha1'),
                                      ('MC1.21.11','1.21.11.jar','sha1')):
            path=args.jars/name
            assert hashlib.new(algorithm,path.read_bytes()).hexdigest()==pins[source]
            jar=jars[source]=stack.enter_context(zipfile.ZipFile(path))
            keys=frozenset(jar.namelist())
            sources[source]=lambda path, archive=jar, names=keys: archive.read(path) if path in names else None
        images={tid:UV['png_frames'](queue[tid],sources[queue[tid]['source_id']],None)[0] for tid in sample_textures}
        vanilla=controls({key[2:]:jar for key,jar in jars.items() if key.startswith('MC')})

    measured={}
    for key,samples in sorted(regions.items()):
        tid,_=key
        evidence=[]
        for i,sample in enumerate(sorted(samples,key=lambda r:int(r['frame']))):
            assert int(sample['frame'])==i
            stats=color_stats(images[tid][i],tuple(map(int,sample['pixel_box'].split('|'))))
            assert stats['rgba_sha256']==sample['rgba8_sha256']
            assert (stats['alpha_zero'],stats['alpha_partial'],stats['visible_rgb'])==tuple(
                int(sample[field]) for field in ('transparent','partial_alpha','visible_rgb_colors'))
            evidence.append(dict(pixel_box=sample['pixel_box'],**stats))
        assert len(evidence)==len(images[tid])
        measured[key]=evidence

    elements_by_key={(r['case'],r['rule_index'],r['model_key'],r['element_index']):r for r in elements}
    detail=[]
    frame_detail=[]
    empty=dict(pixel_box='',pixels='',alpha_zero='',alpha_partial='',visible_rgb='',
               visible_luma_mean='',visible_luma_stddev='',visible_luma_span='',top_rgb='',rgba_sha256='')
    for app in applications:
        case,rule,option=(app[k] for k in ('case','rule_index','option_index'))
        model=app['model_key']
        assert app['provider_sha']==model_shas[app['provider_key']] and app['model_sha']==model_shas[model]
        assert all(app[k]==handoff[case,rule,option][k] for k in
                   ('model_key','model_sha','state_sha','provider_key','provider_sha','x','y','uvlock'))
        for f in faces[model]:
            idx,tid,uv=(f[k] for k in ('element_index','texture_id','uv'))
            assert f['provider_key']==app['provider_key']
            element=elements_by_key[case,rule,model,idx]
            texture=queue.get(tid,{})
            samples=measured.get((tid,uv),[]) if f['status'] in SAMPLED else []
            binding=dict(case=case,rule_index=rule,option_index=option,model_key=model,element_index=idx,
                         direction=f['direction'],texture_id=tid,uv=uv)
            detail.append(dict(**binding,provider_key=app['provider_key'],state_rotation_x=app['x'],
                               state_rotation_y=app['y'],state_uvlock=app['uvlock'],
                               part=element['c_part_candidate'],local_size=element['local_size'],
                               zero_thickness_axes=element['zero_axes'],slot=f['slot'],
                               resource_id=texture.get('resource_id',''),texture_sha=texture.get('source_sha',''),
                               status=f['status'],uv_method=f['uv_method'],uv_rotation=f['uv_rotation'],
                               u_reversed=f['u_reversed'],v_reversed=f['v_reversed'],tintindex=f['tintindex'],
                               cullface=f['cullface'],density_u=f['source_pixels_per_local_u'],
                               density_v=f['source_pixels_per_local_v'],region_frame_count=len(samples),
                               **(samples[0] if samples else empty)))
            if len(samples)>1:
                frame_detail.extend(dict(**binding,frame=i,**sample) for i,sample in enumerate(samples))
    def index(rows):
        groups=defaultdict(list)
        for row in rows:
            groups[row['case']].append(row)
        return groups
    all_faces,all_models,all_elements=map(index,(detail,applications,elements))
    summary=[case_summary(r,all_faces[r['case']],all_models[r['case']],all_elements[r['case']]) for r in cases]
    summary_by_case={r['case']:r for r in summary}
    comparisons=[]
    for a,b,kind in PAIRS:
        left,right=summary_by_case[a],summary_by_case[b]
        def matches(faces):
            return Counter((f['element_index'],f['direction'],f['texture_id'],f['uv'],f['rgba_sha256'])
                           for f in faces if f['status'] in SAMPLED)
        common=sum((matches(all_faces[a]) & matches(all_faces[b])).values())
        comparisons.append(dict(case_a=a,case_b=b,comparison=kind,
                                same_assembly=left['assembly_sha']==right['assembly_sha'],
                                elements_a=left['elements'],elements_b=right['elements'],
                                sampled_faces_a=left['sampled_faces'],sampled_faces_b=right['sampled_faces'],
                                texture_ids_a=left['sampled_texture_ids'],texture_ids_b=right['sampled_texture_ids'],
                                equal_index_direction_texture_uv_rgba_faces=common))
    assert len(detail)==sum(int(r['effective_faces']) for r in cases)
    assert len({(r['case'],r['rule_index'],r['option_index'],r['element_index'],r['direction']) for r in detail})==len(detail)
    category_summary=[]
    for category,mod in sorted({(r['category'],r['mod']) for r in summary}):
        subset=[r for r in summary if (r['category'],r['mod'])==(category,mod)]
        sample=[face for r in subset for face in all_faces[r['case']] if face['status'] in SAMPLED]
        category_summary.append(dict(category=category,mod=mod,cases='|'.join(r['case'] for r in subset),
                                     sample_states=len(subset),elements=sum(r['elements'] for r in subset),
                                     faces=sum(r['total_faces'] for r in subset),sampled_faces=len(sample),
                                     vanilla_png_faces=sum(f['resource_id'].startswith('minecraft:') for f in sample),
                                     faces_with_zero_alpha=sum(f['alpha_zero']>0 for f in sample),
                                     faces_with_partial_alpha=sum(f['alpha_partial']>0 for f in sample),
                                     density_1x1_faces=sum(f['density_u']==f['density_v']=='1' for f in sample),
                                     blank_faces=sum(f['pixels']==f['alpha_zero'] for f in sample)))
    write(out/'SAMPLE_FACES.csv.xz',detail)
    write(out/'CATEGORY_COMPARISON.csv',category_summary)
    write(out/'CASE_COMPARISON.csv',summary)
    write(out/'PAIRED_STATES.csv',comparisons)
    write(out/'VANILLA_CONTROLS.csv',vanilla)
    if frame_detail:
        write(out/'SAMPLE_ANIMATION_FRAMES.csv',frame_detail)
    result={'cases':len(summary),'applications':len(applications),'elements':len(elements),
            'face_instances':len(detail),'sample_face_status':dict(Counter(r['status'] for r in detail)),
            'distinct_sampled_texture_ids':len(sample_textures),
            'verified_texture_uv_regions':len(measured),'verified_region_frames':sum(map(len,measured.values())),
            'animated_sample_face_frames':len(frame_detail),'vanilla_control_faces':len(vanilla),
            'state_pairs':len(comparisons),'categories':len({r['category'] for r in summary}),
            'category_mod_rows':len(category_summary),
            'sampled_faces_using_vanilla_png':sum(r['vanilla_png_faces'] for r in category_summary),
            'sampled_faces_at_1x1_density':sum(r['density_1x1_faces'] for r in category_summary),
            'sampled_state_uvlock_face_instances':sum(f['state_uvlock']=='true' and f['status'] in SAMPLED for f in detail)}
    (out/'D_AUDIT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps(result))


def xz_rows(path):
    with lzma.open(path,'rt',encoding='utf-8',newline='') as stream:
        yield from csv.DictReader(stream)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ('af','hc','jars','faces','out'):
        parser.add_argument('--'+name,type=Path,required=True)
    main(parser.parse_args())
