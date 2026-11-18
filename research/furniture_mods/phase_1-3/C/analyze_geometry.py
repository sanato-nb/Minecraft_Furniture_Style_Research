"""1-3-C: B 원장으로 원문을 고정하고 정적 모델 상속과 형상을 분석한다."""
import argparse
import csv
import gzip
import hashlib
import io
import itertools
import json
import math
import subprocess
import tarfile
import zipfile
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

PINS = {
    'AF': ('57eb624cbb7f408d43398c7434b0d38d312cb55d', '1.21.1'),
    'HC': ('8d21d1665916850c3fa3bdaf1370c50ec2ca7035', '1.21.1'),
    'MACAW': ('e55d7a78b878043af82875cb8738941b0bba1a3c77652dea3d75a434dbba1a0e', '1.21.11'),
}
MC_CLIENT_SHA1 = {'1.21.1': '30c73b1c5da787909b2f73340419fdf13b9def88', '1.21.11': 'ba2df812c2d12e0219c489c4cd9a5e1f0760f5bd'}
VANILLA_ANGLES = {-45, -22.5, 0, 22.5, 45}
BUILTIN = {'minecraft:builtin/generated', 'minecraft:builtin/entity', 'minecraft:builtin/missing'}
CHAIRS = {
    ('AF', 'another_furniture:block/template/chair'): [[0,1,2,3],[4],[7,8,9],[5,6]],
    ('AF', 'another_furniture:block/template/chair_tucked'): [[0,1,2,3],[4],[7,8,9],[5,6]],
    ('HC', 'handcrafted:block/chair/chair'): [[0,1,7,8],[6,12],[2,9,10,11],[3,4,5]],
    ('MACAW', 'mcwfurnitures:block/parent/chair'): [[2,3,4,5],[0,11],[1,6,7,8,9,10],[]],
}


def hash_data(data, git_blob=False):
    if git_blob:
        return hashlib.sha1(f'blob {len(data)}\0'.encode() + data).hexdigest()
    return hashlib.sha256(data).hexdigest()


def read_csv(path):
    opener = gzip.open if path.suffix == '.gz' else open
    with opener(path, 'rt', encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))


def write_csv(path, columns, rows):
    if path.suffix == '.gz':
        with path.open('wb') as target, gzip.GzipFile(filename='', mode='wb', fileobj=target, mtime=0) as compressed:
            with io.TextIOWrapper(compressed, encoding='utf-8', newline='') as f:
                writer = csv.writer(f, lineterminator='\n')
                writer.writerow(columns.split())
                writer.writerows(rows)
    else:
        with path.open('w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(columns.split())
            writer.writerows(rows)


@dataclass(frozen=True)
class Model:
    key: str
    mod: str
    mc: str
    ident: str
    path: str
    sha: str
    entry: str
    body: dict


def archive_paths(repo, pin, paths):
    raw = subprocess.check_output(['git', '-C', str(repo), 'archive', pin])
    with tarfile.open(fileobj=io.BytesIO(raw)) as arc:
        found = {m.name: arc.extractfile(m).read() for m in arc if m.name in paths}
    assert found.keys() == paths
    return found


def normalize(ref):
    return ref if ':' in ref else f'minecraft:{ref}'


def fmt(vector):
    return '|'.join(f'{value:.8f}'.rstrip('0').rstrip('.') if abs(value) >= 1e-8 else '0' for value in vector)


def rotated_point(point, pivot, axis, angle, rescale):
    shifts = [p - o for p, o in zip(point, pivot)]
    i, j = {'x': (1, 2), 'y': (2, 0), 'z': (0, 1)}[axis]
    c, s = math.cos(math.radians(angle)), math.sin(math.radians(angle))
    scale = 1 / c if rescale else 1
    shifts[i], shifts[j] = scale * (c * shifts[i] - s * shifts[j]), scale * (s * shifts[i] + c * shifts[j])
    return [p + o for p, o in zip(shifts, pivot)]


def bounds(points):
    axes = list(zip(*points))
    return tuple(min(a) for a in axes) + tuple(max(a) for a in axes)


def union(boxes):
    return bounds([corner for box in boxes for corner in (box[:3], box[3:])]) if boxes else ()


def outside(box):
    return bool(box and any(v < -1e-8 or w > 16 + 1e-8 for v, w in zip(box[:3], box[3:])))


def separation(a, b):
    gaps = [max(a[i] - b[i+3], b[i] - a[i+3]) for i in range(3)]
    return math.hypot(*(max(0, x) for x in gaps)) if any(x > 0 for x in gaps) else max(gaps)


def geometry(model):
    result = []
    for element in model.body.get('elements', []):
        a, b = element['from'], element['to']
        assert len(a) == len(b) == 3 and all(math.isfinite(v) for v in a + b)
        points = list(itertools.product(*zip(a, b)))
        raw = bounds(points)
        rot = element.get('rotation')
        ortho = raw
        if rot and rot['angle']:
            assert not rot.get('rescale') or abs(rot['angle']) in (22.5, 45)
            ortho = bounds([rotated_point(point, rot['origin'], rot['axis'], rot['angle'], rot.get('rescale', False))
                            for point in points])
        result.append((element, raw, ortho))
    return result


def face_slot(reference, textures):
    seen = set()
    while reference.startswith('#'):
        name = reference[1:]
        if name in seen:
            return 'SLOT_CYCLE', ''
        seen.add(name)
        if name not in textures:
            return 'SLOT_UNBOUND', ''
        reference = textures[name]
    return 'RESOURCE_ID', normalize(reference)


def exceeds_vanilla_size(element):
    return any(v < -16 or v > 32 for v in element['from'] + element['to'])


def classify_element(element):
    widths = [abs(a-b) for a, b in zip(element['from'], element['to'])]
    ordered = sorted(widths)
    if not ordered[0]:
        return 'PLANE' if ordered[1] else 'DEGENERATE'
    if ordered[0] * 4 <= ordered[1]:
        return 'SLAB'
    if ordered[1] * 2 <= ordered[2]:
        return 'ELONGATED'
    return 'SOLID'


def load_models(args):
    source_dir = args.b / 'source_verification'
    remote = read_csv(args.remote_record)
    remote_by_name = {Path(r['path']).name: r for r in remote}
    for name in (f'B_{mod}_SOURCE_BODIES.csv.gz' for mod in PINS):
        blob = (source_dir / name).read_bytes()
        assert hash_data(blob, True) == remote_by_name[name]['git_blob_sha']
    code_index = read_csv(args.b / 'B_JAVA_KOTLIN_SOURCE_INDEX.csv')
    all_models, code = {}, {}
    evidence = []
    for mod, repo in (('AF', args.af), ('HC', args.hc), ('MACAW', None)):
        pin, mc = PINS[mod]
        rows = [r for r in read_csv(source_dir / f'B_{mod}_SOURCE_BODIES.csv.gz') if r['family'] == 'models']
        code_rows = [r for r in code_index if r['mod_id'] == mod]
        paths = {r['path'] for r in rows} | {r['source_path'] for r in code_rows}
        if mod == 'HC':
            paths |= {'common/src/main/resources/handcrafted-common.mixins.json',
                      'fabric/src/main/resources/fabric.mod.json',
                      'neoforge/src/main/resources/META-INF/neoforge.mods.toml'}
        if repo:
            source = archive_paths(repo, pin, paths)
            for r in code_rows:
                p = r['source_path']
                assert hash_data(source[p], True) == r['git_blob_sha']
                code[(mod, p)] = (r['git_blob_sha'], source[p])
        else:
            assert hash_data(args.macaw.read_bytes()) == pin
            with zipfile.ZipFile(args.macaw) as archive:
                source = {p: archive.read(p) for p in paths}
                for p in sorted(n for n in archive.namelist() if n.endswith('.class')):
                    data = archive.read(p)
                    assert data[:4] == b'\xca\xfe\xba\xbe'
                    code[(mod, p)] = (hash_data(data), data)
        for i, r in enumerate(rows, 1):
            p, ident = r['path'], r['asset_id']
            data = source[p]
            assert hash_data(data, bool(repo)) == r['sha'] and int(r['bytes']) == len(data), p
            body = json.loads(data)
            own = body.get('elements', [])
            assert len(own) == int(r['own_elements'])
            assert sum(len(e['faces']) for e in own) == int(r['own_faces'])
            assert body.get('parent', '') == r['parent']
            token = (mod, ident)
            assert token not in all_models
            all_models[token] = Model(f'{mod}{i}', mod, mc, ident, p, r['sha'], r['entry_id'], body)
        if mod == 'HC':
            for p in sorted(paths):
                if p.endswith(('BlockElementMixin.java','handcrafted-common.mixins.json','fabric.mod.json',
                               'neoforge.mods.toml','CrockeryRenderer.java','/HandcraftedClient.java')):
                    data = source[p]
                    evidence.append((mod, p, hash_data(data, True), len(data)))
    return all_models, code, evidence


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('af','hc','macaw','b','remote-record','vanilla','out'):
        parser.add_argument('--'+name, required=True, type=Path)
    args = parser.parse_args()
    out = args.out
    dataset, code, evidence = load_models(args)
    assert Counter(model.mod for model in dataset.values()) == {'AF':1629,'HC':12394,'MACAW':2549}
    mc = {}
    jar_evidence = {}
    auxiliary = {}
    for version in ('1.21.1','1.21.11'):
        jar = args.vanilla / (version+'.jar')
        record = json.loads((args.vanilla/(version+'.json')).read_text())
        info = record['downloads']['client']
        assert hashlib.sha1(jar.read_bytes()).hexdigest() == info['sha1'] == MC_CLIENT_SHA1[version] and jar.stat().st_size == info['size']
        jar_evidence[version] = {key:info[key] for key in ('sha1','size','url')}
        mc[version] = zipfile.ZipFile(jar)

    def find(model, ident):
        namespace, rel = ident.split(':', 1)
        if namespace != 'minecraft':
            return dataset.get((model.mod, ident))
        token = (model.mc, ident)
        if token not in auxiliary:
            path = f'assets/minecraft/models/{rel}.json'
            try:
                data = mc[model.mc].read(path)
            except KeyError:
                return None
            version_tag = model.mc.replace('.','')
            auxiliary[token] = Model(f'V{version_tag}-{len(auxiliary)+1}', 'VANILLA', model.mc,
                                     ident, path, hash_data(data), '', json.loads(data))
        return auxiliary[token]

    def chain(model):
        nodes = []
        seen = set()
        item = model
        while item is not None:
            if item.key in seen:
                return nodes, 'PARENT_CYCLE', item.ident
            nodes.append(item)
            seen.add(item.key)
            raw = item.body.get('parent')
            if not raw:
                return nodes, 'ROOT', ''
            ident = normalize(raw)
            if ident in BUILTIN:
                return nodes, 'BUILTIN', ident
            item = find(model, ident)
            if item is None:
                return nodes, 'PARENT_MISSING', ident

    def counts_for(elements):
        return len(elements), sum(len(e['faces']) for e, _, _ in elements)

    catalog, chains, exceptions, providers, refs, texture_metrics = [], [], [], Counter(), defaultdict(set), defaultdict(Counter)
    provider_stats = {}
    effective_stats = Counter()
    chain_stats = Counter()
    static = {}
    for model in dataset.values():
        lineage, end, terminal = chain(model)
        chain_stats[(model.mod,end)] += 1
        keys = [m.key for m in lineage]
        for parent in keys[1:]:
            refs[parent].add(model.key)
        for node in lineage:
            if node.key not in static:
                static[node.key] = geometry(node)
        own = static[model.key]
        provider = next((node for node in lineage if static[node.key]), None)
        applied = static[provider.key] if provider else []
        textures = {}
        for node in reversed(lineage):
            textures.update(node.body.get('textures', {}))
        source_kind = ('LOCAL' if provider else 'NONE')
        if provider and provider.mod == 'VANILLA':
            source_kind = 'VANILLA'
        if terminal == 'minecraft:builtin/generated':
            source_kind = 'GENERATED_ITEM_RUNTIME'
        if end in ('PARENT_MISSING','PARENT_CYCLE') or terminal in ('minecraft:builtin/entity','minecraft:builtin/missing'):
            source_kind = 'UNRESOLVED_PARENT' if not provider else 'PARTIAL_OWN_OR_LOCAL_GEOMETRY'
            exceptions.append((model.mod,model.key,model.ident,'PARENT',end,terminal))
        if source_kind == 'GENERATED_ITEM_RUNTIME':
            exceptions.append((model.mod, model.key, model.ident,'GEOMETRY','GENERATED_ITEM_RUNTIME',terminal))
        raw, turned = (union([r[index] for r in applied]) for index in (1,2))
        own_size, own_faces = counts_for(own)
        effective_size, effective_faces = counts_for(applied)
        if provider:
            providers[provider.key] += 1
            provider_stats[provider.key] = (effective_size, effective_faces)
        effective_stats[(model.mod,source_kind)] += 1
        angle_override = sum(e.get('rotation', {}).get('angle', 0) not in VANILLA_ANGLES for e,_,_ in applied) if model.mc == '1.21.1' else 0
        size_override = sum(exceeds_vanilla_size(e) for e,_,_ in applied) if model.mc == '1.21.1' else 0
        if source_kind == 'NONE':
            exceptions.append((model.mod,model.key,model.ident,'GEOMETRY','NO_EXPLICIT_ELEMENTS_IN_CHAIN',''))
        uv_present = sum('uv' in face for e,_,_ in applied for face in e['faces'].values())
        slot_faces = Counter(face['texture'] for e,_,_ in applied for face in e['faces'].values())
        tex_counts = Counter()
        bound = {}
        for slot, freq in sorted(slot_faces.items()):
            status, material = face_slot(slot, textures)
            tex_counts[status] += freq
            bound[slot] = [material,status,freq]
        if tex_counts['SLOT_UNBOUND'] or tex_counts['SLOT_CYCLE']:
            exceptions.append((model.mod,model.key,model.ident,'TEXTURE_BINDING','SLOT_UNRESOLVED',
                               '|'.join(slot for slot,v in bound.items() if v[1]!='RESOURCE_ID')))
        texture_metrics[model.mod].update(tex_counts)
        # BBox, counts and references are analysis data. Texture asset bytes are not redistributed.
        catalog.append((model.key,model.mod,model.mc,model.ident,model.path,model.sha,model.entry,
                        source_kind,provider.key if provider else '',own_size,own_faces,
                        effective_size-own_size,effective_faces-own_faces,effective_size,effective_faces,
                        fmt(raw),fmt(turned),fmt(b-a for a,b in zip(turned[:3],turned[3:])),
                        int(outside(raw)),int(outside(turned)),uv_present,effective_faces-uv_present,
                        tex_counts['RESOURCE_ID'],tex_counts['SLOT_UNBOUND'],tex_counts['SLOT_CYCLE'],
                        '|'.join(sorted(set(v[0] for v in bound.values() if v[0]))),angle_override,size_override))
        chains.append((model.key, model.ident, model.body.get('parent',''), '|'.join(keys), end, terminal,
                       len(keys)-1))
    for jar in mc.values():
        jar.close()
    all_by_key = {m.key:m for m in itertools.chain(dataset.values(),auxiliary.values())}
    assert len(all_by_key) == len(dataset)+len(auxiliary)
    all_elements, all_faces, parts = [], [], []
    element_stats = defaultdict(Counter)
    for key, elements in sorted(static.items()):
        model = all_by_key[key]
        selected = CHAIRS.get((model.mod,model.ident), [])
        manual_roles = {i: role for role, indices in zip(
            ('LEG_OR_LOWER_POST','SEAT_LAYER','BACKREST_ASSEMBLY','LOWER_FRAME'), selected) for i in indices}
        if selected:
            assert set(manual_roles) == set(range(len(elements)))
        for i, (e,raw,turn) in enumerate(elements):
            dims = [abs(a-b) for a,b in zip(e['from'],e['to'])]
            zero = ''.join(k for k,d in zip('xyz',dims) if d==0)
            rev = ''.join(k for k,a,b in zip('xyz',e['from'],e['to']) if a>b)
            gaps = [(separation(turn,z[2]),j) for j,z in enumerate(elements) if i!=j]
            nearest = min(gaps, key=lambda x:(max(0,x[0]),abs(x[0]),x[1])) if gaps else None
            rot = e.get('rotation',{})
            angle = rot.get('angle',0)
            stats = element_stats[model.mod]
            stats['source_elements'] += 1
            stats['faces'] += len(e['faces'])
            stats['zero_thickness'] += bool(zero)
            stats['reverse_axis'] += bool(rev)
            stats['rotation_nonzero'] += bool(angle)
            stats['outside_raw'] += outside(raw)
            stats['outside_element_rotated'] += outside(turn)
            stats['nonvanilla_1_21_1_angles'] += model.mc=='1.21.1' and angle not in VANILLA_ANGLES
            stats['outside_vanilla_1_21_1_coordinate_limit'] += model.mc=='1.21.1' and exceeds_vanilla_size(e)
            for near, j in gaps:
                if i < j:
                    stats['aabb_pairs'] += 1
                    stats['aabb_contact_or_overlap'] += near <= 1e-8
            all_elements.append((model.key,i,fmt(e['from']),fmt(e['to']),fmt(rot.get('origin',[])),
                                 rot.get('axis',''),angle,int(rot.get('rescale',False)),fmt(raw),fmt(turn),
                                 fmt(dims),zero,rev,int(outside(raw)),int(outside(turn)),
                                 nearest[1] if nearest else '',round(nearest[0],8) if nearest else '',
                                 len(e['faces']),int(model.mc=='1.21.1' and angle not in VANILLA_ANGLES),
                                 int(model.mc=='1.21.1' and exceeds_vanilla_size(e))))
            for face, prop in sorted(e['faces'].items()):
                uv = prop.get('uv',[])
                all_faces.append((model.key,i,face,prop['texture'],fmt(uv),int(bool(uv)),
                                  prop.get('rotation',0),prop.get('cullface',''),prop.get('tintindex','')))
            slots = '|'.join(sorted({f['texture'] for f in e['faces'].values()}))
            parts.append((model.key,i,classify_element(e),manual_roles.get(i,'UNDETERMINED'),
                          'GEOMETRY_AND_FACE_SLOTS' if i in manual_roles else 'GEOMETRY_ONLY',
                          slots,fmt(dims),fmt((raw[j]+raw[j+3])/2 for j in range(3))))
    def geometry_signature(key):
        topology = []
        for e, _, _ in static[key]:
            r = e.get('rotation', {})
            rotation = [r['origin'], r['axis'], r['angle'], bool(r.get('rescale', False))] if r.get('angle', 0) else []
            # 순서 및 면 방향은 보존하고 재질과 UV는 형상 지문에서 제외한다.
            topology.append([e['from'],e['to'],rotation,sorted(e['faces'])])
        return hash_data(json.dumps(topology,separators=(',',':')).encode())

    families = [(key, all_by_key[key].ident, providers[key], provider_stats[key][0], provider_stats[key][1],
                 geometry_signature(key)) for key in sorted(providers)]
    external = [(m.key,m.mc,m.ident,m.path,m.sha) for m in auxiliary.values()]
    codes = [(mod,path,sha,len(data)) for (mod,path),(sha,data) in sorted(code.items())]
    file_tables = {
        'mod_furniture_catalog.csv.gz': ('model_key mod minecraft model_id path source_hash entry geometry_status geometry_source_key own_elements own_faces inherited_elements inherited_faces effective_elements effective_faces raw_bbox rotated_bbox rotated_size outside_raw outside_rotated faces_explicit_uv faces_implicit_uv faces_resolved faces_unbound faces_slot_cycle texture_resource_ids elements_nonvanilla_1_21_1_angle elements_outside_vanilla_1_21_1_coord_limit', catalog),
        'MODEL_PARENT_CHAINS.csv.gz': ('model_key model_id declared_parent chain_keys terminal_status terminal_ref depth',chains),
        'mod_model_elements.csv.gz': ('source_key element_index source_from source_to pivot axis angle rescale raw_bbox rotated_bbox raw_size zero_axes reversed_axes outside_raw outside_rotated nearest_element rotated_aabb_signed_gap face_count nonvanilla_1_21_1_angle outside_vanilla_1_21_1_coord_limit',all_elements),
        'MODEL_FACES.csv.gz': ('source_key element_index direction texture_slot uv uv_declared uv_rotation cullface tintindex',all_faces),
        'PARTS.csv.gz': ('source_key element_index geometry_type candidate_part evidence texture_slots size center',parts),
        'C_EXCEPTIONS.csv.gz': ('mod model_key model_id category status detail',exceptions),
        'C_VANILLA_PARENTS.csv': ('source_key minecraft model_id path sha256',external),
        'C_GEOMETRY_REUSE.csv': ('source_key model_id effective_model_count elements faces ordered_geometry_sha256',families),
        'C_CODE_SHA_INDEX.csv': ('mod path hash bytes',codes),
        'C_CODE_EVIDENCE.csv': ('mod path hash bytes',evidence),
    }
    for name,(cols,rows) in file_tables.items():
        write_csv(out/name, cols, rows)
    assert sum(r[13] for r in catalog) == sum(f[2]*f[3] for f in families)
    assert sum(r[14] for r in catalog) == sum(f[2]*f[4] for f in families)
    model_by_mod = Counter(m.mod for m in dataset.values())
    totals = {
        'schema':'MOD_FURNITURE_C_GEOMETRY/v1','pinned_sources':PINS,'vanilla_sources':jar_evidence,
        'model_paths':model_by_mod,'all_model_paths':len(dataset),'direct_model_file_hash_matches':len(dataset),
        'vanilla_dependency_paths':len(auxiliary),'code_and_class_paths':Counter(r[0] for r in codes),
        'chain_terminals':{'|'.join(k):v for k,v in sorted(chain_stats.items())},
        'geometry_status':{'|'.join(k):v for k,v in sorted(effective_stats.items())},
        'elements_by_source_mod':element_stats,'models_with_nonempty_elements':sum(bool(r[9]) for r in catalog),
        'model_paths_with_effective_static_elements':sum(bool(r[13]) for r in catalog),
        'model_paths_with_no_static_elements_or_unresolved':sum(not r[13] for r in catalog),
        'models_with_nonvanilla_1_21_1_angles':sum(bool(r[26]) for r in catalog),
        'models_outside_vanilla_1_21_1_coordinate_limit':sum(bool(r[27]) for r in catalog),
        'effective_elements':sum(r[13] for r in catalog),'effective_faces':sum(r[14] for r in catalog),
        'element_provider_keys':len(families),'distinct_ordered_geometry_signatures':len({r[5] for r in families}),'parent_keys_reused':len(refs),
        'texture_slot_status_faces':texture_metrics,'measured_part_candidate_elements':sum(r[3]!='UNDETERMINED' for r in parts),
        'exception_records':len(exceptions),'counts_by_exception':{'|'.join(k):v for k,v in Counter((r[0],r[3],r[4]) for r in exceptions).items()},
        'rows_by_file':{k:len(v[1]) for k,v in file_tables.items()},
        'raw_assets_published':0,'runtime_verified':False,
    }
    (out/'C_AUDIT.json').write_text(json.dumps(totals,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(totals,ensure_ascii=False,indent=2))


if __name__ == '__main__':
    main()
