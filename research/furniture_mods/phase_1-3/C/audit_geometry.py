"""형상 원장의 관계와 회전 경계상자를 별도의 계산으로 검증한다."""
import argparse
import csv
import gzip
import json
import math
from collections import Counter, defaultdict
from pathlib import Path


def rows(path):
    op = gzip.open if path.suffix == '.gz' else open
    with op(path, 'rt', encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f))


def vec(value):
    return tuple(map(float, value.split('|'))) if value else ()


def verify_box(expected, actual):
    assert len(expected) == len(actual)
    assert all(math.isclose(x, y, rel_tol=0, abs_tol=5e-8) for x, y in zip(expected, actual)), (expected, actual)


def analytic_box(row):
    start, end = vec(row['source_from']), vec(row['source_to'])
    middle = [(x+y)/2 for x,y in zip(start,end)]
    radius = [abs(x-y)/2 for x,y in zip(start,end)]
    lo, hi = zip(*(sorted((x,y)) for x,y in zip(start,end)))
    verify_box(lo+hi, vec(row['raw_bbox']))
    angle = math.radians(float(row['angle']))
    if not angle:
        return lo + hi
    pivot = vec(row['pivot'])
    axis = 'xyz'.index(row['axis'])
    i = (axis+1)%3
    j = (axis+2)%3
    cos, sin = math.cos(angle), math.sin(angle)
    scale = 1/cos if int(row['rescale']) else 1
    u, v = middle[i]-pivot[i], middle[j]-pivot[j]
    middle[i] = pivot[i] + scale*(cos*u-sin*v)
    middle[j] = pivot[j] + scale*(sin*u+cos*v)
    a, b = radius[i], radius[j]
    radius[i] = scale*(abs(cos)*a+abs(sin)*b)
    radius[j] = scale*(abs(sin)*a+abs(cos)*b)
    return tuple(x-r for x,r in zip(middle,radius))+tuple(x+r for x,r in zip(middle,radius))


def normalized_parent(parent):
    return parent if not parent or ':' in parent else 'minecraft:'+parent


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out',type=Path,required=True)
    p.add_argument('--b',type=Path,required=True)
    args = p.parse_args()
    out = args.out
    catalog = rows(out/'mod_furniture_catalog.csv.gz')
    chains = {r['model_key']:r for r in rows(out/'MODEL_PARENT_CHAINS.csv.gz')}
    source_counts = {r['model_key']:r for r in catalog}
    parent_ids = {(r['model_key']):r['model_id'] for r in catalog}
    parent_ids.update({r['source_key']:r['model_id'] for r in rows(out/'C_VANILLA_PARENTS.csv')})
    assert len(catalog) == len(source_counts) == len(chains) == 16572
    pinnings = {}
    for mod in ['AF','HC','MACAW']:
        b_rows = rows(args.b/'source_verification'/f'B_{mod}_SOURCE_BODIES.csv.gz')
        for r in b_rows:
            if r['family']=='models':
                key = (mod,r['path'])
                assert key not in pinnings
                pinnings[key] = r
    assert len(pinnings)==len(catalog)
    elements = defaultdict(list)
    for r in rows(out/'mod_model_elements.csv.gz'):
        assert int(r['element_index'])==len(elements[r['source_key']])
        verify_box(analytic_box(r),vec(r['rotated_bbox']))
        elements[r['source_key']].append(r)
    faces = Counter((r['source_key'],r['element_index']) for r in rows(out/'MODEL_FACES.csv.gz'))
    parts = Counter((r['source_key'],r['element_index']) for r in rows(out/'PARTS.csv.gz'))
    assert set(faces) <= parts.keys()
    for key, shape in elements.items():
        for r in shape:
            i = r['element_index']
            assert faces[key,i]==int(r['face_count']) and parts[key,i]==1
    totals = Counter()
    for model in catalog:
        key = model['model_key']
        pin = pinnings[model['mod'],model['path']]
        chain = chains[key]
        assert (model['source_hash'],model['model_id'],model['entry']) == (pin['sha'],pin['asset_id'],pin['entry_id'])
        assert (model['own_elements'],model['own_faces'],chain['declared_parent'])==(pin['own_elements'],pin['own_faces'],pin['parent'])
        nodes = chain['chain_keys'].split('|')
        assert nodes[0]==key and len(set(nodes))==int(chain['depth'])+1
        for i, node in enumerate(nodes[:-1]):
            if node in chains:
                assert normalized_parent(chains[node]['declared_parent'])==parent_ids[nodes[i+1]]
        provider = next((n for n in nodes if elements.get(n)), '')
        assert model['geometry_source_key']==provider
        boxes = [vec(e['rotated_bbox']) for e in elements.get(provider,[])]
        extent = tuple(min(b[i] for b in boxes) for i in range(3))+tuple(max(b[i] for b in boxes) for i in range(3,6)) if boxes else ()
        verify_box(extent,vec(model['rotated_bbox']))
        a,b = int(model['effective_elements']),int(model['effective_faces'])
        assert a==len(boxes) and b==sum(int(r['face_count']) for r in elements.get(provider,[]))
        assert a==int(model['own_elements'])+int(model['inherited_elements'])
        assert b==int(model['own_faces'])+int(model['inherited_faces'])
        assert b==sum(int(model[k]) for k in ('faces_resolved','faces_unbound','faces_slot_cycle'))
        assert b==int(model['faces_explicit_uv'])+int(model['faces_implicit_uv'])
        totals.update({'effective_elements':a,'effective_faces':b,'models':1})
    audit = json.loads((out/'C_AUDIT.json').read_text())
    assert totals['effective_elements']==audit['effective_elements'] and totals['effective_faces']==audit['effective_faces']
    result = dict(status='PASS',model_path_sha_and_b_row_matches=len(catalog),parent_chains_checked=len(chains),
                  element_rotated_bbox_analytic_comparisons=sum(map(len,elements.values())),
                  effective_element_instances=totals['effective_elements'],effective_face_instances=totals['effective_faces'],
                  face_rows=sum(faces.values()),part_rows=sum(parts.values()),errors=[])
    (out/'C_INDEPENDENT_AUDIT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(result)


if __name__ == '__main__':
    main()
