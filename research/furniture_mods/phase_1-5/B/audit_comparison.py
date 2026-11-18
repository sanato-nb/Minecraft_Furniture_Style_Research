"""Reconcile normalized rows with the preceding evidence and frame dimensions."""
from collections import Counter, defaultdict
import csv
import json
import lzma
from pathlib import Path

HERE=Path(__file__).resolve().parent
FURNITURE=HERE.parents[1]
KEY=('case','rule_index','option_index')
FACE_KEY=KEY+('element_index','direction')


def rows(path):
    opener=lzma.open if path.suffix=='.xz' else open
    with opener(path,'rt',encoding='utf-8',newline='') as file:
        return list(csv.DictReader(file))


def key(row,columns):
    return tuple(row[c] for c in columns)


def main():
    apps=rows(HERE/'APPLICATIONS.csv')
    elements=rows(HERE/'ELEMENTS.csv')
    face_rows=rows(HERE/'FACES.csv.xz')
    faces={key(r,FACE_KEY):r for r in face_rows}
    assert len(face_rows)==len(faces)==1844
    prior=rows(FURNITURE/'phase_1-4/entry03/SAMPLE_FACES.csv.xz')
    assert len(prior)==1610
    old_fields=('uv','uv_method','uv_rotation','status','density_u','density_v','pixel_box',
                'pixels','alpha_zero','alpha_partial','visible_rgb','rgba_sha256')
    for r in prior:
        now=faces[key(r,FACE_KEY)]
        assert key(now,old_fields+('png_sha',))==key(r,old_fields+('texture_sha',))
    vanilla=rows(HERE.parent/'A/VANILLA_CONTROL_OPTIONS.csv')
    vanilla_expected={(r['control'],r['rule_index'],r['option_index']):r for r in vanilla}
    source=Counter(r['state_path'] for r in apps if r['cohort']=='VANILLA')
    assert len(source)==14
    element_counts=Counter(key(r,KEY) for r in elements)
    face_counts=Counter(k[:3] for k in faces)
    for r in apps:
        k=key(r,KEY)
        assert (int(r['elements']),int(r['faces']))==(element_counts[k],face_counts[k])
        if r['cohort']=='VANILLA':
            old=vanilla_expected.pop(k)
            assert key(r,('elements','faces','model_path','x','y','uvlock','weight'))==key(
                old,('elements','faces','model_path','x','y','uvlock','weight'))
            assert r['model_sha']==old['model_git_blob_sha1']
    assert not vanilla_expected
    animation=defaultdict(dict)
    for row in rows(HERE/'ANIMATION_FRAMES.csv.xz'):
        k=key(row,FACE_KEY)
        n=int(row['frame'])
        assert n not in animation[k]
        animation[k][n]=row
    for k,row in faces.items():
        if not row['pixels']:
            assert row['status']=='ZERO_UV_AREA'
            continue
        x0,y0,x1,y1=map(int,row['pixel_box'].split('|'))
        assert 0<=x0<x1<=int(row['frame_width']) and 0<=y0<y1<=int(row['frame_height'])
        assert (x1-x0)*(y1-y0)==int(row['pixels'])
        assert 0<=int(row['alpha_zero'])+int(row['alpha_partial'])<=int(row['pixels'])
        if row['status']=='ANIMATED_FRAME_RECTS':
            periods=animation.pop(k)
            assert set(periods)==set(range(int(row['png_frames'])))
            assert all(r['pixel_box']==row['pixel_box'] and r['pixels']==row['pixels'] for r in periods.values())
            assert periods[0]['rgba_sha256']==row['rgba_sha256']
    assert not animation
    print(json.dumps(dict(status='PASS',applications=len(apps),elements=len(elements),faces=len(faces),
                          mod_face_rows_reconciled=len(prior),vanilla_applications_reconciled=len(vanilla),
                          animated_face_instances=sum(r['status']=='ANIMATED_FRAME_RECTS' for r in faces.values())),
                     sort_keys=True,indent=2))


if __name__=='__main__':
    main()
