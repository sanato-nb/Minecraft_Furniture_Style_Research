"""Measure the fixed comparison set in one static geometry/UV schema."""
import argparse
from collections import Counter, defaultdict
import csv
from fractions import Fraction
import hashlib
from itertools import product
import json
import lzma
from pathlib import Path
import runpy
from statistics import median
import sqlite3
from zipfile import ZipFile

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parents[1]
A_DIR = HERE.parent/'A'
PHASE13 = RESEARCH/'phase_1-3'
PHASE14 = RESEARCH/'phase_1-4'
GEOM = runpy.run_path(str(PHASE13/'E/compare_furniture.py'))
MATERIAL = runpy.run_path(str(PHASE14/'entry03/compare_materials.py'))
UV = MATERIAL['UV']
PNG = UV['FIRST']
A = runpy.run_path(str(A_DIR/'verify_scope.py'))
DIRECTIONS = {'up':(0,2), 'down':(0,2), 'east':(2,1), 'west':(2,1),
              'north':(0,1), 'south':(0,1)}
SAMPLED = {'STATIC_RECT','ANIMATED_FRAME_RECTS'}
APP = ('case','rule_index','option_index')
MEASURES = ('pixels','alpha_zero','alpha_partial','visible_rgb','visible_luma_mean','visible_luma_stddev',
            'visible_luma_span','top_rgb','rgba_sha256')


def rows(path):
    opener = lzma.open if path.suffix == '.xz' else open
    with opener(path,'rt',encoding='utf-8',newline='') as file:
        yield from csv.DictReader(file)


def save(path, records):
    opener = lzma.open if path.suffix == '.xz' else open
    with opener(path,'wt',encoding='utf-8',newline='') as file:
        writer=csv.DictWriter(file,fieldnames=list(records[0]),lineterminator='\n')
        writer.writeheader()
        writer.writerows(records)


def key(row, columns=APP):
    return tuple(str(row[k]) for k in columns)


def group(records, columns):
    output=defaultdict(list)
    for row in records:
        output[key(row,columns)].append(row)
    return output


def base_application(case, cohort, minecraft, category, block, state, rule, option, model, provider,
                     x, y, uvlock, weight, status):
    return dict(case=case,cohort=cohort,minecraft=minecraft,category=category,block=block,
                state=state,rule_index=rule,option_index=option,model=model,provider=provider,
                x=x,y=y,uvlock=int(uvlock),weight=weight,geometry_status=status)


def mod_evidence():
    scope={r['case']:r for r in rows(A_DIR/'MOD_CASE_SCOPE.csv')}
    identities={key(r):r for r in rows(PHASE13/'E/CATEGORY_EVIDENCE.csv')}
    with sqlite3.connect(':memory:') as db:
        db.deserialize(lzma.decompress((PHASE13/'F/furniture_research.sqlite.xz').read_bytes()))
        weights={(case,str(rule),str(option)):weight for case,rule,option,weight in db.execute(
            'SELECT sample_id,rule_index,option_index,weight FROM sample_option JOIN option USING(state_id,rule_index,option_index)')}
    options={}
    for r in rows(PHASE14/'entry04/1-5_TEXTURE_UV_HANDOFF.csv'):
        a=identities[key(r)]
        s=scope[r['case']]
        assert (r['model_sha'],r['provider_sha'],r['state_sha'])==(a['model_sha'],a['provider_sha'],a['state_sha'])
        options[key(r)]=base_application(r['case'],r['mod'],s['minecraft'],r['category'],r['state_id'],
            s['assignment'],r['rule_index'],r['option_index'],r['model_key'],r['provider_key'],
            int(r['x']),int(r['y']),int(r['uvlock']),weights[key(r)],'STATIC_SOURCE')
        options[key(r)].update(state_path=a['state_path'],state_sha=r['state_sha'],
                               model_path=a['model_path'],model_sha=r['model_sha'],
                               provider_path=a['provider_path'],provider_sha=r['provider_sha'],
                               model_hash_kind='SHA256' if r['mod']=='MACAW' else 'GIT_BLOB_SHA1')
    queue={r['texture_id']:r for r in rows(PHASE13/'F/1-3_TEXTURE_UV_HANDOFF.csv')}
    sizes={r['texture_id']:r for r in rows(PHASE14/'entry02/TEXTURE_UV_COUNTS.csv.xz')}
    elements=[]
    case_rule={(k[0],k[1]):k for k in options}
    assert len(case_rule)==len(options)
    for r in rows(PHASE13/'E/E_ELEMENT_EVIDENCE.csv'):
        k=case_rule[r['case'],r['rule_index']]
        assert r['model_key']==options[k]['model']
        elements.append(dict(case=k[0],rule_index=k[1],option_index=k[2],element_index=r['element_index'],
                             local_size=r['local_size'],zero_axes=r['zero_axes'],
                             assembly_bbox=r['assembly_bbox'],faces=int(r['faces'])))
    faces=[]
    for r in rows(PHASE14/'entry03/SAMPLE_FACES.csv.xz'):
        k=key(r)
        assert r['model_key']==options[k]['model']
        texture=queue[r['texture_id']]
        frame=sizes[r['texture_id']]
        assert r['texture_sha']==texture['source_sha']==frame['source_sha']
        width,height,count=(int(frame[n]) for n in ('frame_width','frame_height','frame_count'))
        assert r['status'] not in SAMPLED or count==int(r['region_frame_count'])
        faces.append(new_face(k,r['element_index'],r['direction'],r['slot'],r['resource_id'],texture['path'],
                              r['texture_sha'],texture['source_hash_kind'],(width,height*count),(width,height),count,
                              r['uv'],r['uv_method'],r['uv_rotation'],r['cullface'],r['tintindex'],
                              r['density_u'],r['density_v'],r['status'],r['pixel_box'],{n:r[n] for n in MEASURES}))
    frames=[]
    for r in rows(PHASE14/'entry03/SAMPLE_ANIMATION_FRAMES.csv'):
        frames.append(frame_row(key(r),r['element_index'],r['direction'],r['frame'],r['pixel_box'],r))
    return list(options.values()),elements,faces,frames


def new_face(application,index,direction,slot,resource,path,sha,kind,sheet,frame,count,uv,method,rotation,
             cull,tint,density_u,density_v,status,box,measures):
    return dict(zip(APP,application),element_index=index,direction=direction,slot=slot,
                resource_id=resource,png_path=path,png_sha=sha,png_hash_kind=kind,
                sheet_width=sheet[0],sheet_height=sheet[1],frame_width=frame[0],frame_height=frame[1],
                png_frames=count,uv=uv,uv_method=method,uv_rotation=rotation,cullface=cull,tintindex=tint,
                density_u=density_u,density_v=density_v,status=status,pixel_box=box,**measures)


def frame_row(application,index,direction,frame,box,measures):
    return dict(zip(APP,application),element_index=index,direction=direction,frame=frame,pixel_box=box,
                **{n:measures[n] for n in MEASURES})


def transformed_element(element, x, y):
    start,end=element['from'],element['to']
    extent=tuple(abs(b-a) for a,b in zip(start,end))
    corners=list(product(*zip(start,end)))
    rot=element.get('rotation',{})
    if rot.get('angle'):
        corners=[GEOM['rotate'](v,rot['origin'],rot['axis'],rot['angle'],rot.get('rescale',False)) for v in corners]
    for axis, angle in (('x',x),('y',y)):
        if angle:
            corners=[GEOM['rotate'](v,(8,8,8),axis,-angle) for v in corners]
    return extent,GEOM['bounds'](corners)


def vanilla_evidence(jar_file):
    provenance={r['path']:r for r in rows(A_DIR/'VANILLA_SOURCE_PROVENANCE.csv')}
    expected=json.loads((A_DIR/'A_SCOPE_AUDIT.json').read_text())['vanilla']['official_client_jar_sha1']
    assert hashlib.sha1(jar_file.read_bytes()).hexdigest()==expected
    applications,elements,faces,frames=[],[],[],[]
    metadata={}
    with ZipFile(jar_file) as jar:
        names=frozenset(jar.namelist())
        def read(path):
            data=jar.read(path)
            assert A['git_blob'](data)==provenance[path]['git_blob_sha1'],path
            return data
        images={}
        for r in rows(A_DIR/'VANILLA_CONTROL_OPTIONS.csv'):
            app=(r['control'],r['rule_index'],r['option_index'])
            x,y=map(int,(r['x'],r['y']))
            applications.append(base_application(r['control'],'VANILLA','1.21.11',r['categories'],r['block'],
                r['properties'],r['rule_index'],r['option_index'],r['model_path'],r['geometry_provider'],
                x,y,int(r['uvlock']),int(r['weight']),r['scope']))
            applications[-1].update(state_path=r['state_path'],state_sha=r['state_git_blob_sha1'],
                                    model_path=r['model_path'],model_sha=r['model_git_blob_sha1'],
                                    provider_path=r['geometry_provider'],provider_sha=r['provider_git_blob_sha1'],
                                    model_hash_kind='GIT_BLOB_SHA1')
            if not r['geometry_provider']:
                assert r['control']=='V11'
                continue
            provider=json.loads(read(r['geometry_provider']),parse_float=Fraction)
            textures={}
            for path in reversed(r['parent_chain'].split('|')):
                textures.update(json.loads(read(path)).get('textures',{}))
            first=len(faces)
            for index,e in enumerate(provider['elements']):
                size,box=transformed_element(e,x,y)
                elements.append(dict(zip(APP,app),element_index=index,local_size=UV['packed'](size),
                                     zero_axes='|'.join(axis for axis,value in zip('xyz',size) if not value),
                                     assembly_bbox=GEOM['fmt'](box),faces=len(e['faces'])))
                for side,face in sorted(e['faces'].items()):
                    resource=PNG['resolve'](face['texture'],textures)
                    path='assets/'+resource.replace(':','/textures/')+'.png'
                    if path not in images:
                        body=read(path)
                        im,*_=PNG['decode_png'](body)
                        sidecar=path+'.mcmeta'
                        meta=jar.read(sidecar) if sidecar in names else None
                        row=dict(path=path,source_hash_kind='SHA256',source_sha=hashlib.sha256(body).hexdigest())
                        sources={path:body,sidecar:meta}
                        crops,animation=UV['png_frames'](row,sources.get,None)
                        images[path]=(im.size,crops,row['source_sha'])
                        if animation:
                            metadata[sidecar]=dict(path=sidecar,sha256=hashlib.sha256(meta).hexdigest(),
                                                   frame_count=len(crops),frametime=animation.get('frametime',1),
                                                   interpolate=animation.get('interpolate',False))
                    sheet,crops,sha=images[path]
                    assert list(sheet)==json.loads(r['texture_dimensions'])[path]
                    method='EXPLICIT' if 'uv' in face else 'DEFAULT'
                    uv=tuple(map(Fraction,face['uv'])) if method=='EXPLICIT' else UV['default_uv'](e['from'],e['to'],side)
                    rotation=face.get('rotation',0)
                    axes=DIRECTIONS[side][::-1] if rotation in (90,270) else DIRECTIONS[side]
                    width,height=crops[0].size
                    density=tuple(str(Fraction(abs(uv[i+2]-uv[i])*pixels,16*size[axis])) if size[axis] else ''
                                  for i,(axis,pixels) in enumerate(zip(axes,(width,height))))
                    status,pixel_box,stats=UV['measure_region'](crops,uv)
                    packed_box=UV['packed'](pixel_box) if pixel_box else ''
                    observed=[MATERIAL['color_stats'](crop,pixel_box) for crop in crops] if stats else []
                    assert [o['rgba_sha256'] for o in observed]==[s[-1] for s in stats]
                    assert all((o['alpha_zero'],o['alpha_partial'],o['visible_rgb'])==s[:2]+(s[3],)
                               for o,s in zip(observed,stats))
                    faces.append(new_face(app,index,side,face['texture'],resource,path,sha,'SHA256',sheet,(width,height),
                                          len(crops),UV['packed'](uv),method,rotation,face.get('cullface',''),
                                          face.get('tintindex',''),*density,status,packed_box,
                                          observed[0] if observed else dict.fromkeys(MEASURES,'')))
                    if len(observed)>1:
                        frames.extend(frame_row(app,index,side,i,packed_box,o) for i,o in enumerate(observed))
            assert len(faces)-first==int(r['faces'])
    assert len(applications)==22 and len(elements)==55 and len(faces)==234
    return applications,elements,faces,frames,[v for _,v in sorted(metadata.items())]


def enclosing(elements):
    if not elements:
        return None
    boxes=[tuple(map(float,r['assembly_bbox'].split('|'))) for r in elements]
    axes=list(zip(*boxes))
    return tuple(min(a) for a in axes[:3])+tuple(max(a) for a in axes[3:])


def summary(applications,elements,faces):
    e_groups=group(elements,APP)
    f_groups=group(faces,APP)
    for r in applications:
        ek=e_groups[key(r)]
        fk=f_groups[key(r)]
        box=enclosing(ek)
        assert sum(e['faces'] for e in ek)==len(fk)
        r.update(elements=len(ek),faces=len(fk),zero_thickness_elements=sum(bool(e['zero_axes']) for e in ek),
                 assembly_bbox=GEOM['fmt'](box) if box else '',
                 span_blocks=GEOM['fmt'](v/16 for v in GEOM['span'](box)) if box else '')
    case_elements=group(elements,('case',))
    case_faces=group(faces,('case',))
    outcomes=[]
    for (case,),apps in group(applications,('case',)).items():
        app=apps[0]
        ef=case_elements[case,]
        ff=case_faces[case,]
        box=enclosing(ef)
        states=Counter(f['status'] for f in ff)
        observed=[f for f in ff if f['status'] in SAMPLED]
        density=[Fraction(f[a]) for f in observed for a in ('density_u','density_v') if f[a]!='']
        outcomes.append(dict(case=case,cohort=app['cohort'],minecraft=app['minecraft'],category=app['category'],
                             block=app['block'],applications=len(apps),elements=len(ef),faces=len(ff),
                             bbox=GEOM['fmt'](box) if box else '',
                             span_blocks=GEOM['fmt'](v/16 for v in GEOM['span'](box)) if box else '',
                             zero_thickness_elements=sum(bool(e['zero_axes']) for e in ef),
                             min_positive_local_thickness_blocks=str(min(v for e in ef for v in UV['vector'](e['local_size']) if v>0)/16) if ef else '',
                             default_uv_faces=sum(f['uv_method']=='DEFAULT' for f in ff),
                             explicit_uv_faces=sum(f['uv_method']=='EXPLICIT' for f in ff),
                             uvlock_declared_faces=sum(len(f_groups[key(a)]) for a in apps if a['uvlock']),
                             status_counts=json.dumps(states,sort_keys=True),
                             faces_measured=len(observed),
                             faces_with_first_frame_alpha_zero=sum(int(f['alpha_zero'])>0 for f in observed),
                             faces_with_first_frame_alpha_partial=sum(int(f['alpha_partial'])>0 for f in observed),
                             density_axis_median=str(median(density)) if density else '',
                             faces_at_density_1x1=sum(f['density_u']==f['density_v']=='1' for f in observed)))
    return outcomes


def main(jar, out):
    mod=mod_evidence()
    vanilla=vanilla_evidence(jar)
    applications,elements,faces,frames=[a+b for a,b in zip(vanilla[:4],mod)]
    cases=summary(applications,elements,faces)
    previous={r['case']:r for r in rows(PHASE13/'E/E_SAMPLE_METRICS.csv')}
    for case in cases:
        if case['case'] in previous:
            old=previous[case['case']]
            assert (case['bbox'],case['elements'],case['faces'])==(old['bbox'],int(old['effective_elements']),int(old['effective_faces']))
    assert (len(cases),len(applications),len(elements),len(faces))==(62,74,390,1844)
    assert len({key(r,APP+('element_index','direction')) for r in faces})==len(faces)
    assert len({key(r,APP+('element_index','direction','frame')) for r in frames})==len(frames)
    out.mkdir(parents=True,exist_ok=True)
    for name,data in (('CASES.csv',cases),('APPLICATIONS.csv',applications),('ELEMENTS.csv',elements),
                      ('FACES.csv.xz',faces),('ANIMATION_FRAMES.csv.xz',frames),('VANILLA_MCMETA.csv',vanilla[4])):
        save(out/name,data)
    result={}
    for name,subset in (('vanilla',vanilla[:4]),('mod',mod)):
        app,elem,side,frame=subset
        result[name]=dict(applications=len(app),elements=len(elem),faces=len(side),
                          face_status=dict(Counter(r['status'] for r in side)),
                          uv_methods=dict(Counter(r['uv_method'] for r in side)),animation_frame_rows=len(frame),
                          cases_with_static_geometry=len({r['case'] for r in elem}))
    encoded=json.dumps(dict(status='PASS',**result),indent=2,sort_keys=True)+'\n'
    (out/'B_AUDIT.json').write_text(encoded,encoding='utf-8')
    print(encoded)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--jar',required=True,type=Path)
    parser.add_argument('--out',required=True,type=Path)
    a=parser.parse_args()
    main(a.jar,a.out)
