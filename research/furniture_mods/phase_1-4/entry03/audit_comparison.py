"""Check the comparison's face keys, source joins and aggregate denominators."""
from collections import Counter, defaultdict
import csv
import json
import lzma
from pathlib import Path
import sqlite3

HERE = Path(__file__).resolve().parent
PHASE = HERE.parents[1] / 'phase_1-3'


def rows(name):
    path = HERE/name
    opener = lzma.open if path.suffix == '.xz' else open
    with opener(path,'rt',encoding='utf-8',newline='') as stream:
        return list(csv.DictReader(stream))


def main():
    expected={}
    with sqlite3.connect(':memory:') as db:
        db.deserialize(lzma.decompress((PHASE/'F/furniture_research.sqlite.xz').read_bytes()))
        for row in db.execute('''
            SELECT s.id, so.rule_index,so.option_index,f.element_index,f.direction,
                   o.model_key,f.provider_key,f.slot,f.texture_id,o.x,o.y,o.uvlock,t.sha,
                   f.uv_rotation,f.uv_declared
            FROM sample s JOIN sample_option so ON so.sample_id=s.id AND so.state_id=s.state_id
            JOIN option o USING(state_id,rule_index,option_index)
            JOIN effective_face_texture f ON f.model_key=o.model_key LEFT JOIN texture t ON t.id=f.texture_id
        '''):
            key=tuple(map(str,row[:5]))
            assert key not in expected
            expected[key]=row[5:]
    detail=rows('SAMPLE_FACES.csv.xz')
    summary=rows('CASE_COMPARISON.csv')
    case_totals=defaultdict(Counter)
    sample_frames=Counter()
    for r in detail:
        key=tuple(r[field] for field in ('case','rule_index','option_index','element_index','direction'))
        values=tuple(r[field] for field in ('model_key','provider_key','slot','texture_id',
                                           'state_rotation_x','state_rotation_y','state_uvlock','texture_sha',
                                           'uv_rotation','uv_method'))
        model,provider,slot,tid,x,y,lock,sha,rotation,declared=expected.pop(key)
        assert values==(model,provider,slot,str(tid) if tid is not None else '',str(x),str(y),
                        str(bool(lock)).lower(),sha or '',str(rotation),'EXPLICIT' if declared else 'DEFAULT'),key
        case_totals[key[0]][r['status']]+=1
        if r['status']=='ANIMATED_FRAME_RECTS':
            sample_frames[key]=int(r['region_frame_count'])
        if r['pixels']:
            assert 0<=int(r['alpha_zero'])+int(r['alpha_partial'])<=int(r['pixels'])
            assert len(bytes.fromhex(r['rgba_sha256']))==32
    assert not expected and set(case_totals)=={r['case'] for r in summary}
    for r in summary:
        totals=case_totals[r['case']]
        assert totals==json.loads(r['face_statuses']) and sum(totals.values())==int(r['total_faces'])
        assert totals['STATIC_RECT']+totals['ANIMATED_FRAME_RECTS']==int(r['sampled_faces'])
    frames=defaultdict(set)
    for r in rows('SAMPLE_ANIMATION_FRAMES.csv'):
        key=tuple(r[field] for field in ('case','rule_index','option_index','element_index','direction'))
        frame=int(r['frame'])
        assert frame not in frames[key]
        frames[key].add(frame)
    assert {key:set(range(n)) for key,n in sample_frames.items()}==frames
    categories=rows('CATEGORY_COMPARISON.csv')
    assert sum(int(r['sample_states']) for r in categories)==len(summary)==47
    assert sum(int(r['faces']) for r in categories)==len(detail)==1610
    vanilla=defaultdict(dict)
    for r in rows('VANILLA_CONTROLS.csv'):
        key=r['model_path'],r['side']
        assert r['version'] not in vanilla[key]
        vanilla[key][r['version']]=r['texture_sha256'],r['rgba_sha256']
    assert len(vanilla)==24
    assert all(set(v)=={'1.21.1','1.21.11'} and len({item[1] for item in v.values()})==1 for v in vanilla.values())
    print(json.dumps({'status':'PASS','case_face_keys':len(detail),'cases':len(summary),
                      'category_mod_rows':len(categories),'animated_frame_rows':sum(map(len,frames.values())),
                      'vanilla_model_side_keys_reconciled_across_versions':len(vanilla)},
                     indent=2,sort_keys=True))


if __name__=='__main__':
    main()
