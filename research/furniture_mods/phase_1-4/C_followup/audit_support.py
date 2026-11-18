"""Reconcile UV exception groups and independently check source support by cell overlap."""
from collections import Counter
import csv
from fractions import Fraction
import json
import lzma
from pathlib import Path

HERE = Path(__file__).resolve().parent


def rows(path):
    opener = lzma.open if path.suffix == '.xz' else open
    with opener(path,'rt',encoding='utf-8',newline='') as stream:
        yield from csv.DictReader(stream)


def cells(lo, hi, size):
    lo, hi = sorted((lo,hi))
    inside_lo, inside_hi = max(Fraction(0),lo), min(Fraction(16),hi)
    if inside_lo>inside_hi:
        return []
    point = inside_lo==inside_hi
    result=[]
    for i in range(size):
        a,b=Fraction(i*16,size),Fraction((i+1)*16,size)
        if (a<=inside_lo<=b if point else max(a,inside_lo)<min(b,inside_hi)):
            result.append(i)
    return result


def main():
    prior = {(r['texture_id'],r['uv'],r['reason']):int(r['face_instances'])
             for r in rows(HERE.parent/'entry02/UV_EXCEPTIONS.csv')
             if r['reason'] in ('ZERO_UV_AREA','OUTSIDE_TEXTURE_UV')}
    observed_groups={}
    outcomes=Counter()
    frame_keys=set()
    for row in rows(HERE/'UV_SOURCE_SUPPORT.csv.xz'):
        key=(row['texture_id'],row['uv'],row['original_status'])
        count=int(row['face_instances'])
        assert key in prior and prior[key]==count
        frame=(key,row['frame'])
        assert frame not in frame_keys
        frame_keys.add(frame)
        if key not in observed_groups:
            outcomes[row['outcome']]+=count
        assert observed_groups.setdefault(key,row['outcome'])==row['outcome']
        u0,v0,u1,v1=map(Fraction,row['uv'].split('|'))
        x=cells(u0,u1,int(row['frame_width']))
        y=cells(v0,v1,int(row['frame_height']))
        if not x or not y:
            assert not row['pixel_box'] and not row['rgba_sha256']
            assert row['outcome']=='NO_PINNED_SPRITE_INTERSECTION'
            continue
        assert tuple(map(int,row['pixel_box'].split('|')))==(min(x),min(y),max(x)+1,max(y)+1)
        assert sum(int(row[k]) for k in ('transparent','partial_alpha','opaque'))==len(x)*len(y)
        assert len(bytes.fromhex(row['rgba_sha256']))==32
    assert set(prior)==set(observed_groups)
    summary=json.loads((HERE/'SUMMARY.json').read_text())
    assert outcomes==summary['pixel_support_counts']
    assert summary['supplemental_source_support_faces']==sum(outcomes.values())-outcomes['NO_PINNED_SPRITE_INTERSECTION']
    slots=Counter()
    for row in rows(HERE/'SLOT_CHILD_CONTEXT.csv.xz'):
        assert row['direct_blockstate_selection']=='0'
        assert bool(int(row['bound_child_models']))==(row['outcome']=='BOUND_CHILD_CONTEXT')
        slots[row['outcome']]+=int(row['face_instances'])
    assert slots==summary['unbound_face_contexts']
    missing=list(rows(HERE/'MISSING_TEXTURE_RELEASE_CHECK.csv'))
    assert len(missing)==8 and all(all(row[k]=='0' for k in
        ('pinned_git_exists','fabric_402_exists','neoforge_403_exists')) for row in missing)
    assert sum(int(row['face_instances']) for row in missing)==summary['unchanged_missing_png_faces']
    total=summary['original_full_rect_samples']+sum(outcomes.values())+sum(slots.values())+summary['unchanged_missing_png_faces']
    assert total==summary['fixed_faces']
    print(json.dumps(dict(status='PASS',verified_uv_groups=len(observed_groups),
        verified_frame_rows=len(frame_keys),verified_face_total=total),indent=2))


if __name__=='__main__':
    main()
