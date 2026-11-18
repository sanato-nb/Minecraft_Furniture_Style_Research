"""고정 C/D 원장과 원문에서 상태별 가구 기하를 검증하고 비교한다."""
import argparse
from collections import Counter, defaultdict
import csv
from functools import lru_cache
import gzip
import hashlib
from itertools import product
import json
import math
from pathlib import Path
import subprocess
import zipfile

HERE = Path(__file__).resolve().parent
NS = {'AF': 'another_furniture', 'HC': 'handcrafted', 'MACAW': 'mcwfurnitures'}
PINS = {'AF': '57eb624cbb7f408d43398c7434b0d38d312cb55d',
        'HC': '8d21d1665916850c3fa3bdaf1370c50ec2ca7035'}
LANG = {'AF': 'common/src/main/resources/assets/another_furniture/lang/en_us.json',
        'HC': 'common/src/main/generated/resources/assets/handcrafted/lang/en_us.json',
        'MACAW': 'assets/mcwfurnitures/lang/en_us.json'}
INPUTS = {
    'C/C_VANILLA_PARENTS.csv': '9fe27be8e403c5971111333fc39c23de138d4195',
    'C/C_GEOMETRY_REUSE.csv': 'fba1bdcdb14a03da352a5b290060708b53902be1',
    'C/PARTS.csv.gz': '933574ad09d388ec3261bda6eae7f985cd4dc3ff',
    'C/mod_furniture_catalog.csv.gz': '412470e5512b7af93f3c91e2db060612f72650e7',
    'C/mod_model_elements.csv.gz': '439c3d278c570749465b7a8c00493784dbe5b3b9',
    'D/CONNECTION_RULES.csv': 'e4d3e08eb5059a92b17fff2a8a171cc3e12ac768',
    'D/D_BLOCKSTATES.csv': '7079e6abec1bfd0c4a4a5e8c45861e5ceea1033d',
    'D/D_MULTIPART_ASSEMBLIES.csv.gz': '45ec8e6248acd8b8c9e0c36d5ffe1a8bf3f011ac',
    'D/D_STATE_RULES.csv.gz': '9a06279d4ec3cae2b648895151cfed567b93a95e',
    'D/MODEL_STATE_ASSEMBLY.csv.gz': '496d0273129828ec3e5e8f3c16f131aef7c9594c',
}
GRID = 64


def git_blob(data):
    return hashlib.sha1(f'blob {len(data)}\0'.encode() + data).hexdigest()


def rows(path):
    opener = gzip.open if path.suffix == '.gz' else open
    with opener(path, 'rt', encoding='utf-8', newline='') as source:
        return list(csv.DictReader(source))


def save(path, items):
    with path.open('w', encoding='utf-8', newline='') as target:
        writer = csv.DictWriter(target, list(items[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(items)


def group(items, key):
    result = defaultdict(list)
    for item in items:
        result[key(item)].append(item)
    return result


def vector(text):
    return tuple(float(v) for v in text.split('|'))


def fmt(values):
    return '|'.join(f'{v:.8f}'.rstrip('0').rstrip('.') if abs(v) > 1e-8 else '0' for v in values)


def rotate(point, pivot, axis, angle, rescale=False):
    i, j = {'x': (1, 2), 'y': (2, 0), 'z': (0, 1)}[axis]
    angle = math.radians(angle)
    c, s = math.cos(angle), math.sin(angle)
    p, q = point[i]-pivot[i], point[j]-pivot[j]
    factor = 1/c if rescale else 1
    v = list(point)
    v[i] = pivot[i] + (c*p-s*q)*factor
    v[j] = pivot[j] + (s*p+c*q)*factor
    return tuple(v)


def bounds(points):
    axes = list(zip(*points))
    return tuple(min(a) for a in axes) + tuple(max(a) for a in axes)


def span(box):
    return tuple(hi-lo for lo, hi in zip(box[:3], box[3:]))


def hull(points):
    points = sorted({tuple(round(x, 8) for x in point) for point in points})

    def half(ordered):
        curve = []
        for p in ordered:
            while len(curve) >= 2:
                a, b = curve[-2:]
                cross = (b[0]-a[0])*(p[1]-a[1]) - (b[1]-a[1])*(p[0]-a[0])
                if cross > 1e-12:
                    break
                curve.pop()
            curve.append(p)
        return curve
    if len(points) < 3:
        return []
    return half(points)[:-1] + half(reversed(points))[:-1]


def silhouette(solids, box, axes):
    i, j = axes
    x0, y0 = box[i], box[j]
    dx, dy = (box[i+3]-x0)/GRID, (box[j+3]-y0)/GRID
    assert dx > 0 and dy > 0
    masks = [0]*GRID
    for corners in solids:
        polygon = hull((p[i], p[j]) for p in corners)
        edges = list(zip(polygon, polygon[1:]+polygon[:1]))
        for r in range(GRID):
            y = y0 + (r+0.5)*dy
            intersections = [a[0]+(b[0]-a[0])*(y-a[1])/(b[1]-a[1])
                             for a, b in edges if min(a[1], b[1]) <= y < max(a[1], b[1])]
            if intersections:
                l, h = min(intersections), max(intersections)
                start = max(0, math.ceil((l-x0)/dx-0.5))
                end = min(GRID, math.floor((h-x0)/dx+0.5))
                if end > start:
                    masks[r] |= ((1 << (end-start))-1) << start
    filled = sum(mask.bit_count() for mask in masks)
    return round(100*filled/GRID**2, 4), hashlib.sha256(b''.join(m.to_bytes(GRID//8, 'little') for m in masks)).hexdigest()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for name in ('af', 'hc', 'macaw', 'mc1211', 'c', 'd'):
        p.add_argument('--'+name, required=True, type=Path)
    p.add_argument('--out', default=HERE, type=Path)
    args = p.parse_args()
    for key, digest in INPUTS.items():
        stage, file = key.split('/', 1)
        assert git_blob((getattr(args, stage.lower())/file).read_bytes()) == digest, key
    assert hashlib.sha1(args.macaw.read_bytes()).hexdigest() == '28f0929b6005bc28b1bde475579c13020420ae9f'
    arc = zipfile.ZipFile(args.macaw)
    assert hashlib.sha1(args.mc1211.read_bytes()).hexdigest() == '30c73b1c5da787909b2f73340419fdf13b9def88'
    vanilla = zipfile.ZipFile(args.mc1211)
    checked = {}

    @lru_cache(maxsize=None)
    def open_source(mod, path, expected=None):
        if mod in {'MACAW', 'MC1211'}:
            binary = (arc if mod == 'MACAW' else vanilla).read(path)
            sha = hashlib.sha256(binary).hexdigest()
        else:
            binary = subprocess.check_output(['git','-C',str(getattr(args, mod.lower())), 'show', PINS[mod]+':'+path])
            sha = git_blob(binary)
        assert expected is None or sha == expected, (mod,path)
        checked[(mod,path)] = sha
        return json.loads(binary), sha

    languages = {m: open_source(m, path) for m, path in LANG.items()}
    cases = rows(HERE/'E_SAMPLE_SELECTION.csv')
    selected_states = {(r['mod'],NS[r['mod']]+':'+r['block']) for r in cases}
    state_key = lambda r: (r['mod'],r['state_id'])
    states = {state_key(r):r for r in rows(args.d/'D_BLOCKSTATES.csv')}
    links = {state_key(r):r for r in rows(args.d/'CONNECTION_RULES.csv')}
    rules = group((r for r in rows(args.d/'D_STATE_RULES.csv.gz') if state_key(r) in selected_states), state_key)
    options = group((r for r in rows(args.d/'MODEL_STATE_ASSEMBLY.csv.gz') if state_key(r) in selected_states), state_key)
    multi = group((r for r in rows(args.d/'D_MULTIPART_ASSEMBLIES.csv.gz') if state_key(r) in selected_states), state_key)
    catalog = {r['model_key']:r for r in rows(args.c/'mod_furniture_catalog.csv.gz')}
    providers = {**catalog, **{r['source_key']:dict(model_key=r['source_key'], path=r['path'],
        source_hash=r['sha256'], mod='MC1211') for r in rows(args.c/'C_VANILLA_PARENTS.csv') if r['minecraft']=='1.21.1'}}
    elements = group(rows(args.c/'mod_model_elements.csv.gz'), lambda r:r['source_key'])
    part_lookup = {(r['source_key'],r['element_index']):r for r in rows(args.c/'PARTS.csv.gz')}
    fingerprints = {r['source_key']:r['ordered_geometry_sha256'] for r in rows(args.c/'C_GEOMETRY_REUSE.csv')}
    source_checks, samples, evidence, parts, profiles = set(), [], [], [], []
    case_solids = {}
    category = {(r['mod'],NS[r['mod']]+':'+r['block']):r['category'] for r in cases}
    source_bodies = {}

    for key in sorted(selected_states):
        mod, sid = key
        state = states[key]
        body, _ = open_source(mod,state['path'],state['source_sha'])
        source_bodies[key] = body
        kind = state['kind']
        raw_options = [v for v in body['variants'].values()] if kind == 'variants' else [r['apply'] for r in body['multipart']]
        for o in options[key]:
            group_options = raw_options[int(o['rule_index'])]
            raw = (group_options if isinstance(group_options, list) else [group_options])[int(o['option_index'])]
            assert (raw['model'],raw.get('x',0),raw.get('y',0),raw.get('uvlock',False),raw.get('weight',1)) == (
                o['model_ref'],int(o['x']),int(o['y']),o['uvlock']=='true',int(o['weight']))
        assert len(options[key]) == sum(len(value) if isinstance(value,list) else 1 for value in raw_options)
        used = {o['model_key'] for o in options[key]}
        ref_geometry = {k: fingerprints[catalog[k]['geometry_source_key']] for k in used}
        option_signature = lambda o: (ref_geometry[o['model_key']],o['x_mod_360'],o['y_mod_360'])
        if kind == 'multipart':
            sig_per_rule = {o['rule_index']:option_signature(o) for o in options[key]}
            assert len(sig_per_rule)==len(options[key])
            assembly_signatures = {tuple(sorted(sig_per_rule[i] for i in row['selected_rule_indices'].split('|') if i)) for row in multi[key]}
            checked_assignments = len(multi[key])
        else:
            ops_by_rule = group(options[key],lambda o:o['rule_index'])
            assembly_signatures = {tuple(sorted(option_signature(o) for o in members)) for members in ops_by_rule.values()}
            checked_assignments = int(state['variant_observed_domain_assignments'])
        profiles.append(dict(category=category[key],mod=mod,state_id=sid,source_path=state['path'],source_sha=state['source_sha'],
            loader_kind=kind,declared_rules=len(raw_options),model_options=len(options[key]),observed_assignments=checked_assignments,
            distinct_model_keys=len(used),distinct_providers=len({catalog[k]['geometry_source_key'] for k in used}),
            distinct_element_face_fingerprints=len(set(ref_geometry.values())),distinct_oriented_assembly_signatures=len(assembly_signatures),
            rotation_pairs='|'.join(','.join(pair) for pair in sorted({(r['x_mod_360'],r['y_mod_360']) for r in options[key]})),
            properties=state['observed_properties'],d_code_evidence=links[key]['evidence_id']))

    for case in cases:
        mod, block = case['mod'],case['block']
        key = mod,NS[mod]+':'+block
        state = states[key]
        body = source_bodies[key]
        translation_key = ('item' if mod == 'MACAW' else 'block')+'.'+NS[mod]+'.'+block
        lang, translation_sha = languages[mod]
        translation = lang[translation_key]
        setting = dict(s.split('=') for s in case['state'].split(';') if s)
        if state['kind'] == 'variants':
            selected = [str(i) for i,k in enumerate(body['variants']) if dict(t.split('=') for t in k.split(',') if t).items() <= setting.items()]
            assert len(selected)==1,case
        else:
            selected = [str(i) for i,r in enumerate(body['multipart']) if r.get('when',{}).items() <= setting.items()]
            assembly, = [r for r in multi[key] if json.loads(r['observed_domain_assignment']) == setting]
            assert assembly['selected_rule_indices'].split('|') == selected
        joined = [o for o in options[key] if o['rule_index'] in selected]
        assert len(joined)==len(selected) and joined,case
        rule_map = {r['rule_index']:r for r in rules[key]}
        solids, case_faces, zero_elements, geometry_options = [], 0, 0, []
        for option in joined:
            model = catalog[option['model_key']]
            provider = providers[model['geometry_source_key']]
            assert (model['path'],model['source_hash']) == (option['model_path'],option['model_source_sha'])
            source_view,_ = open_source(mod,model['path'],model['source_hash'])
            source_checks.add((mod,model['path']))
            shape,_ = open_source(provider['mod'],provider['path'],provider['source_hash'])
            source_checks.add((provider['mod'],provider['path']))
            original = shape['elements']
            sha = fingerprints[provider['model_key']]
            geometry_options.append((sha,int(option['x_mod_360']),int(option['y_mod_360'])))
            evidence.append(dict(case=case['case'],category=case['category'],mod=mod,translation=translation,
                translation_key=translation_key,translation_path=LANG[mod],translation_sha=translation_sha,
                state_id=key[1],state_path=state['path'],state_sha=state['source_sha'],rule_index=option['rule_index'],
                selector=rule_map[option['rule_index']]['source_selector'],option_index=option['option_index'],
                model_key=model['model_key'],model_id=model['model_id'],model_path=model['path'],model_sha=model['source_hash'],
                declared_parent=source_view.get('parent',''),provider_key=provider['model_key'],provider_mod=provider['mod'],provider_path=provider['path'],
                provider_sha=provider['source_hash'],geometry_sha=sha,x=option['x'],y=option['y'],uvlock=option['uvlock'],
                effective_elements=model['effective_elements'],effective_faces=model['effective_faces'],
                texture_resource_ids=model['texture_resource_ids'],
                d_code_evidence=links[key]['evidence_id']))
            original_bounds = []
            for i,(item,c) in enumerate(zip(original,elements[provider['model_key']],strict=True)):
                assert c['element_index']==str(i) and (tuple(item['from']),tuple(item['to'])) == (
                    vector(c['source_from']),vector(c['source_to']))
                corners = list(product(*zip(item['from'],item['to'],strict=True)))
                rot = item.get('rotation',{})
                if rot.get('angle'):
                    corners = [rotate(v,rot['origin'],rot['axis'],rot['angle'],rot.get('rescale',False)) for v in corners]
                box = bounds(corners)
                assert max(abs(a-b) for a,b in zip(box,vector(c['rotated_bbox']),strict=True))<1e-7
                original_bounds += corners
                for axis in ('x','y'):
                    angle = int(option[axis+'_mod_360'])
                    if angle:
                        corners = [rotate(v,(8,8,8),axis,-angle) for v in corners]
                solids.append(corners)
                face_count = len(item.get('faces',{}))
                assert face_count==int(c['face_count'])
                case_faces += face_count
                zero_elements += bool(c['zero_axes'])
                part = part_lookup[provider['model_key'],str(i)]
                bbox = bounds(corners)
                parts.append(dict(case=case['case'],rule_index=option['rule_index'],model_key=model['model_key'],
                    provider_key=provider['model_key'],element_index=i,local_size=c['raw_size'],
                    assembly_bbox=fmt(bbox),assembly_size=fmt(span(bbox)),faces=face_count,
                    texture_slots=part['texture_slots'],c_part_candidate=part['candidate_part'],c_part_evidence=part['evidence'],
                    zero_axes=c['zero_axes']))
            assert len(original)==int(model['effective_elements'])
            assert fmt(bounds(original_bounds))==model['rotated_bbox']
        box = bounds([v for solid in solids for v in solid])
        case_solids[case['case']] = solids
        assembled = hashlib.sha256(repr(sorted(geometry_options)).encode()).hexdigest()
        projections = [silhouette(solids,box,axes) for axes in [(0,1),(2,1),(0,2)]]
        samples.append(dict(**case,state_id=key[1],translation=translation,model_applications=len(joined),
            effective_elements=len(solids),effective_faces=case_faces,zero_thickness_elements=zero_elements,
            bbox=fmt(box),width_height_depth=fmt(span(box)),width_height_depth_blocks=fmt(v/16 for v in span(box)),
            front_fill_pct=projections[0][0],side_fill_pct=projections[1][0],
            top_fill_pct=projections[2][0],projection_mask_hashes='|'.join(p[1] for p in projections),
            geometry_assembly_sha=assembled))

    head_in_foot_frame = [[(x,y,z-16) for x,y,z in poly] for poly in case_solids['S38']]
    bed = case_solids['S37'] + head_in_foot_frame
    rounded_points = lambda poly: sorted(tuple(round(value,5) for value in point) for point in poly)
    bed_coincident_shapes = sum(rounded_points(poly)==rounded_points(head_in_foot_frame[0]) for poly in case_solids['S37'])
    assert bed_coincident_shapes==1
    bed_box = bounds([v for poly in bed for v in poly])
    assert fmt(bed_box)==next(r['bbox'] for r in samples if r['case']=='S37')
    lang_ids = {mod:{r['state_id'] for r in states.values() if r['mod']==mod and 'bed' in (
        lang.get(('item' if mod=='MACAW' else 'block')+'.'+NS[mod]+'.'+r['state_id'].split(':',1)[1],'').casefold().split())}
        for mod,(lang,_) in languages.items()}
    assert {m:len(v) for m,v in lang_ids.items()} == {'AF':0,'HC':11,'MACAW':0}
    for name, data in [('CATEGORY_EVIDENCE.csv',evidence),('E_SAMPLE_METRICS.csv',samples),('E_ELEMENT_EVIDENCE.csv',parts),
                        ('E_STATE_PROFILES.csv',profiles)]:
        save(args.out/name,data)
    result = {'status':'PASS_CURATED_STATIC_COMPARISON','categories':dict(Counter(r['category'] for r in samples)),
              'cases':len(samples),'sampled_state_files':len(profiles),'model_applications':len(evidence),
              'element_instances':len(parts),'unique_reopened_models_and_providers':len(source_checks),
              'reopened_source_paths_total':len(checked),'localized_bed_state_counts':{m:len(v) for m,v in lang_ids.items()},
              'bed_pair_north_head_offset':[0,0,-16],'bed_pair_bbox':fmt(bed_box),'bed_pair_element_applications':len(bed),
              'bed_pair_coincident_shapes':bed_coincident_shapes,
              'input_git_blob_shas':INPUTS,'grid':GRID,'runtime_verified':False,'model_images_rendered':False}
    (args.out/'E_AUDIT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
