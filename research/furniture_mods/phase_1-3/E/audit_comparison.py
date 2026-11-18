"""E 결과의 키·합산·선행 원장 연결과 반례를 독립적으로 대조한다."""
import argparse
from collections import Counter, defaultdict
import csv
import gzip
import json
import math
from pathlib import Path


def read(path):
    opener = gzip.open if path.suffix == '.gz' else open
    with opener(path, 'rt', encoding='utf8', newline='') as source:
        return list(csv.DictReader(source))


def index(rows, fields):
    found = {tuple(row[f] for f in fields):row for row in rows}
    assert len(found) == len(rows), fields
    return found


def vec(text):
    return list(map(float,text.split('|')))


def close(a,b):
    assert all(math.isclose(x,y,abs_tol=2e-7) for x,y in zip(a,b,strict=True)), (a,b)


def main():
    args = argparse.ArgumentParser(description=__doc__)
    for name in ('c','d'):
        args.add_argument('--'+name,required=True,type=Path)
    args.add_argument('--out',default=Path(__file__).resolve().parent,type=Path)
    args = args.parse_args()
    out = args.out
    samples = index(read(out/'E_SAMPLE_METRICS.csv'),['case'])
    assert len(samples) == 47
    options = index(read(out/'CATEGORY_EVIDENCE.csv'),['case','rule_index','option_index'])
    assert len(options) == 52
    elements = index(read(out/'E_ELEMENT_EVIDENCE.csv'),['case','rule_index','element_index'])
    counts = Counter()
    application_faces = Counter()
    per_case = defaultdict(list)
    model = index(read(args.c/'mod_furniture_catalog.csv.gz'), ['model_key'])
    d = index(read(args.d/'MODEL_STATE_ASSEMBLY.csv.gz'),['mod','state_id','rule_index','option_index'])
    c = index(read(args.c/'mod_model_elements.csv.gz'),['source_key','element_index'])
    for (case,rule,element),r in elements.items():
        o = options[(case,rule,'0')]
        assert (r['provider_key'],r['model_key'])==(o['provider_key'],o['model_key'])
        orig = c[(r['provider_key'],element)]
        assert (r['faces'],r['zero_axes'],r['local_size']) == (orig['face_count'],orig['zero_axes'],orig['raw_size'])
        box = vec(orig['rotated_bbox'])
        corners = [tuple(box[i+3*((mask>>i)&1)]-8 for i in range(3)) for mask in range(8)]
        # 90도 정수 좌표 치환으로 AABB를 독립 계산한다.
        for _ in range((int(o['x'])%360)//90):
            corners = [(x,z,-y) for x,y,z in corners]
        for _ in range((int(o['y'])%360)//90):
            corners = [(-z,y,x) for x,y,z in corners]
        axes = list(zip(*corners))
        reference = [min(a)+8 for a in axes]+[max(a)+8 for a in axes]
        close(reference,vec(r['assembly_bbox']))
        counts[(case,rule)] += 1
        application_faces[(case,rule)] += int(r['faces'])
        per_case[case].append(r)
    assert len(elements)==335

    for (case,rule,opt),r in options.items():
        choice = d[(r['mod'],r['state_id'],rule,opt)]
        assert (r['model_key'],r['model_sha'],r['x'],r['y']) == (
            choice['model_key'],choice['model_source_sha'],choice['x'],choice['y'])
        c_row = model[(r['model_key'],)]
        assert r['provider_key']==c_row['geometry_source_key']
        assert counts[(case,rule)] == int(c_row['effective_elements'])
        assert application_faces[(case,rule)] == int(c_row['effective_faces'])
    for (key,),sample in samples.items():
        parts = per_case[key]
        boxes = list(zip(*(vec(r['assembly_bbox']) for r in parts)))
        box = [min(a) for a in boxes[:3]]+[max(a) for a in boxes[3:]]
        close(box,vec(sample['bbox']))
        size = [hi-lo for lo,hi in zip(box[:3],box[3:],strict=True)]
        close(size,vec(sample['width_height_depth']))
        close([v/16 for v in size],vec(sample['width_height_depth_blocks']))
        assert int(sample['effective_elements']) == len(parts)
        assert int(sample['effective_faces']) == sum(int(r['faces']) for r in parts)
        assert all(0<=float(sample[f])<=100 for f in ('front_fill_pct','side_fill_pct','top_fill_pct'))

    part_groups = read(out/'E_PART_GROUPS.csv')
    for row in part_groups:
        for element in row['element_indices'].split('|'):
            assert (row['case'],row['rule_index'],element) in elements
    for a,b in [('S06','S07'),('S20','S21'),('S39','S40'),('S44','S45')]:
        assert samples[(a,)]['geometry_assembly_sha']==samples[(b,)]['geometry_assembly_sha']
    selected = {r['case']:r for r in options.values()}
    for a,b in [('S06','S07'),('S20','S21'),('S39','S40')]:
        assert selected[a]['texture_resource_ids'] != selected[b]['texture_resource_ids']
    assert int(samples[('S43',)]['effective_elements']) == int(samples[('S42',)]['effective_elements']) + 1
    assert samples[('S43',)]['bbox']==samples[('S42',)]['bbox']
    assert elements[('S43','7','1')]['zero_axes']=='y'
    assert samples[('S01',)]['width_height_depth']==samples[('S02',)]['width_height_depth']
    close([0,0,-9,0,0,-9],[b-a for a,b in zip(vec(samples[('S01',)]['bbox']),vec(samples[('S02',)]['bbox']))])
    assert selected['S03']['model_id'].endswith('/birch_1')
    assert selected['S04']['model_id'].endswith('/spruce_1')
    with (out/'E_INDEPENDENT_AUDIT.json').open('w',encoding='utf8') as f:
        json.dump(dict(status='PASS',cases=len(samples),model_applications=len(options),
                       element_bounds_checked=len(elements),part_groups_linked=len(part_groups),
                       texture_rotation_and_state_counterexamples_reproduced=True,
                       silhouette_summary_range_checked=True,errors=[]),f,indent=2)
        f.write('\n')


if __name__ == '__main__':
    main()
