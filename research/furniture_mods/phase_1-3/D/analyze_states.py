"""고정 원본 blockstate와 C단계 기하 원장을 연결한다."""
import argparse
from collections import Counter, defaultdict
import csv
import gzip
import hashlib
import io
import itertools
import json
import math
from pathlib import Path
import sys
import zipfile

HERE = Path(__file__).resolve().parent
MODS = {'AF': ('another_furniture', '1.21.1'), 'HC': ('handcrafted', '1.21.1'),
        'MACAW': ('mcwfurnitures', '1.21.11')}


def read_rows(path):
    opener = gzip.open if path.suffix == '.gz' else open
    with opener(path, 'rt', newline='', encoding='utf-8') as stream:
        return list(csv.DictReader(stream))


def write_rows(path, rows):
    buffer = io.StringIO(newline='')
    writer = csv.DictWriter(buffer, list(rows[0]), lineterminator='\n')
    writer.writeheader()
    writer.writerows(rows)
    data = buffer.getvalue().encode()
    path.write_bytes(gzip.compress(data, mtime=0) if path.suffix == '.gz' else data)


def compact(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'))


def load_inputs(args):
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(args.b))
    import verify_sources as b

    scope = {r['mod_id']: r for r in read_rows(args.b.parent / 'SOURCE_REGISTRY.csv')}
    models = read_rows(args.c / 'mod_furniture_catalog.csv.gz')
    states = {}
    for mod, (namespace, _) in MODS.items():
        index = read_rows(args.b / f'B_{mod}_SOURCE_BODIES.csv.gz')
        rows = [r for r in index if r['family'] == 'blockstates']
        assert {(r['path'], r['sha']) for r in index if r['family'] == 'models'} == {
            (r['path'], r['source_hash']) for r in models if r['mod'] == mod}
        if mod == 'MACAW':
            documents, _ = b.verify_macaw(args.macaw, json.loads(args.version.read_text()),
                                           json.loads(args.project.read_text()))
            data = {row['path']: (row['sha'], row['bytes'], row['asset_id'], body, row['parse'])
                    for row, body in documents if row['family'] == 'blockstates'}
        else:
            repo = getattr(args, mod.lower())
            pin = scope[mod]['source_pin']
            assert b.git(repo, 'rev-parse', pin + '^{tree}').decode().strip() == scope[mod]['source_tree_sha']
            listing = b.git(repo, 'ls-tree', '-lr', '-z', pin)
            tree = {}
            for entry in listing.split(b'\0'):
                if not entry:
                    continue
                meta, path = entry.decode().split('\t', 1)
                if f'/assets/{namespace}/blockstates/' in path and path.endswith('.json'):
                    _, kind, sha, size = meta.split()
                    assert kind == 'blob'
                    tree[path] = sha, int(size)
            blobs = dict(b.git_objects(repo, [sha for sha, _ in tree.values()]))
            data = {p: (sha, size, b.asset_id(p), *b.parse_asset(blobs[sha]))
                    for p, (sha, size) in tree.items()}
        assert len(rows) == len(data) and set(data) == {r['path'] for r in rows}
        for row in rows:
            sha, size, asset_id, body, parse = data[row['path']]
            assert (sha, str(size), asset_id, parse) == (row['sha'], row['bytes'], row['asset_id'], 'STRICT_JSON')
            states[(mod, asset_id)] = row, body
    assert len(states) == 1158 and len(models) == 16572
    return states, models


def variant_condition(key):
    if not key:
        return {}
    terms = [term.split('=', 1) for term in key.split(',')]
    assert all(len(term) == 2 and all(term) for term in terms)
    result = dict(terms)
    assert len(result) == len(terms)
    return result


def property_domains(condition, domains):
    for key, value in condition.items():
        if key in {'AND', 'OR'}:
            for member in value:
                property_domains(member, domains)
        else:
            domains[key].update(value.removeprefix('!').split('|'))


def condition_has_property(condition, prop):
    return prop in condition or any(condition_has_property(member, prop)
                                    for combinator in ('AND', 'OR')
                                    for member in condition.get(combinator, []))


def matches(condition, state):
    for key, value in condition.items():
        if key in {'AND', 'OR'}:
            combine = all if key == 'AND' else any
            matched = combine(matches(member, state) for member in value)
        else:
            matched = state[key] in value.removeprefix('!').split('|')
            if value.startswith('!'):
                matched = not matched
        if not matched:
            return False
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for arg in ('af', 'hc', 'macaw', 'version', 'project', 'b', 'c', 'mc1211', 'mc12111'):
        parser.add_argument('--' + arg, required=True, type=Path)
    parser.add_argument('--out', default=HERE, type=Path)
    args = parser.parse_args()
    states, models = load_inputs(args)
    by_model = {(r['mod'], r['model_id']): r for r in models}
    assert len(by_model) == len(models)
    parents = {r['model_key']: r['detail'] for r in read_rows(args.c / 'C_EXCEPTIONS.csv.gz')
               if r['status'] == 'PARENT_MISSING'}
    assert len(parents) == 48
    vanilla = {}
    jar_sha1s = {'1.21.1': '30c73b1c5da787909b2f73340419fdf13b9def88',
                 '1.21.11': 'ba2df812c2d12e0219c489c4cd9a5e1f0760f5bd'}
    for version, jar in [('1.21.1', args.mc1211), ('1.21.11', args.mc12111)]:
        assert hashlib.sha1(jar.read_bytes()).hexdigest() == jar_sha1s[version]
        with zipfile.ZipFile(jar) as z:
            vanilla[version] = {p.removeprefix('assets/minecraft/models/').removesuffix('.json'):
                                hashlib.sha256(z.read(p)).hexdigest()
                                for p in z.namelist()
                                if p.startswith('assets/minecraft/models/') and p.endswith('.json')}
    counts = defaultdict(Counter)
    ref_counts = defaultdict(Counter)
    rules_out, options_out, property_out, multi_out, exceptions, state_out = [], [], [], [], [], []
    for (mod, state_id), (source, data) in sorted(states.items()):
        version = MODS[mod][1]
        assert set(data) in ({'variants'}, {'multipart'})
        kind, = data
        if kind == 'variants':
            rules = [(key, variant_condition(key), value) for key, value in data[kind].items()]
            assert len({compact(c) for _, c, _ in rules}) == len(rules)
        else:
            rules = [(str(i), row.get('when', {}), row['apply']) for i, row in enumerate(data[kind])]
        prefix = dict(mod=mod, state_id=state_id)
        state_links = dict(path=source['path'], source_sha=source['sha'])
        domains, state_refs = defaultdict(set), Counter()
        option_total = 0
        for ordinal, (key, condition, choices) in enumerate(rules):
            property_domains(condition, domains)
            options = choices if isinstance(choices, list) else [choices]
            assert options
            option_total += len(options)
            rules_out.append(dict(**prefix, rule_index=ordinal, kind=kind, source_selector=key,
                                  condition=compact(condition), options=len(options),
                                  apply_form='array' if isinstance(choices, list) else 'object'))
            for index, option in enumerate(options):
                assert set(option) <= {'model', 'x', 'y', 'uvlock', 'weight'}
                ref = option['model']
                model_id = ref if ':' in ref else 'minecraft:' + ref
                x, y = option.get('x', 0), option.get('y', 0)
                uv, weight = option.get('uvlock', False), option.get('weight', 1)
                assert all(type(angle) is int and angle % 90 == 0 for angle in (x, y))
                assert type(uv) is bool and type(weight) is int and weight > 0
                model = by_model.get((mod, model_id), {})
                model_key = model.get('model_key', '')
                model_path = model.get('path', '')
                model_hash = model.get('source_hash', '')
                target_ns, target_path = model_id.split(':', 1)
                if model:
                    ref_status = 'LOCAL'
                elif target_ns == 'minecraft' and target_path in vanilla[version]:
                    model_path = f'assets/minecraft/models/{target_path}.json'
                    model_hash = vanilla[version][target_path]
                    ref_status = 'VANILLA_JAR'
                else:
                    ref_status = 'UNRESOLVED_MODEL_REF'
                missing_parent = parents.get(model_key, '')
                row = dict(**prefix, rule_index=ordinal, option_index=index, model_ref=ref, model_id=model_id,
                           x=x, y=y, x_mod_360=x % 360, y_mod_360=y % 360,
                           uvlock=str(uv).lower(), weight=weight,
                           explicit_fields='|'.join(k for k in ('x', 'y', 'uvlock', 'weight') if k in option),
                           reference_status=ref_status, model_key=model_key, model_path=model_path,
                           model_source_sha=model_hash, geometry_status=model.get('geometry_status', ''),
                           missing_parent=missing_parent)
                options_out.append(row)
                state_refs[ref_status] += 1
                counts[mod]['nonzero_x_mod_360'] += x % 360 != 0
                counts[mod]['nonzero_y_mod_360'] += y % 360 != 0
                counts[mod]['angles_outside_0_359'] += x != x % 360 or y != y % 360
                counts[mod]['uvlock_true'] += uv
                counts[mod]['nondefault_weight'] += weight != 1
                anomaly = ''
                if ref_status == 'UNRESOLVED_MODEL_REF':
                    anomaly = ref_status
                elif missing_parent:
                    anomaly = 'C_MISSING_PARENT_SELECTED'
                elif mod == 'AF' and state_id in ('another_furniture:birch_chair', 'another_furniture:spruce_chair') and key == 'facing=south,tucked=false,variant=3':
                    wood = state_id.split(':')[1].split('_')[0]
                    assert model_id == f'another_furniture:block/chair/{wood}_1'
                    anomaly = 'PRIOR_CHAIR_VARIANT_3_POINTS_TO_1'
                if anomaly:
                    exceptions.append(dict(**prefix, **state_links, rule_index=ordinal, option_index=index,
                                           source_selector=key, model_id=model_id, model_key=model_key,
                                           category=anomaly, detail=missing_parent or model_id))
        assert option_total == int(source['references'])
        assert state_refs['LOCAL'] == int(source['local_references'])
        assert state_refs['VANILLA_JAR'] == int(source['minecraft_external_references'])
        assert state_refs['UNRESOLVED_MODEL_REF'] == int(source['other_references'])
        ref_counts[mod].update(state_refs)
        for key, values in sorted(domains.items()):
            property_out.append(dict(**prefix, property=key, observed_values='|'.join(sorted(values)),
                                     rules_using_property=sum(condition_has_property(c, key) for _, c, _ in rules)))
        multi_count = 0
        variant_matches = Counter()
        if kind == 'variants':
            keys = sorted(domains)
            for _, condition, _ in rules:
                variant_matches.update(itertools.product(*(
                    [condition[k]] if k in condition else sorted(domains[k]) for k in keys)))
            variant_assignments = math.prod(len(domains[k]) for k in keys)
        else:
            variant_assignments = 0
        gaps = variant_assignments - len(variant_matches)
        overlaps = sum(count > 1 for count in variant_matches.values())
        assert gaps >= 0
        if kind == 'multipart':
            for values in domains.values():
                if values <= {'true', 'false'}:
                    values.update({'true', 'false'})
            keys = sorted(domains)
            for combo in itertools.product(*(sorted(domains[key]) for key in keys)):
                props = dict(zip(keys, combo, strict=True))
                matched = [i for i, (_, condition, _) in enumerate(rules) if matches(condition, props)]
                multi_out.append(dict(**prefix, observed_domain_assignment=compact(props),
                                      selected_rule_indices='|'.join(map(str, matched)),
                                      selected_rule_count=len(matched)))
                multi_count += 1
        state_out.append(dict(**prefix, **state_links, bytes=source['bytes'], kind=kind, rule_count=len(rules),
                              option_count=option_total, observed_properties='|'.join(sorted(domains)),
                              local=state_refs['LOCAL'], vanilla_jar=state_refs['VANILLA_JAR'],
                              unresolved=state_refs['UNRESOLVED_MODEL_REF'], multipart_assignments=multi_count,
                              variant_observed_domain_assignments=variant_assignments,
                              variant_observed_domain_gaps=gaps, variant_observed_domain_overlaps=overlaps))
        counts[mod].update(states=1, rules=len(rules), options=option_total,
                           multipart_assignments=multi_count, variant_observed_domain_assignments=variant_assignments,
                               variant_observed_domain_gaps=gaps, variant_observed_domain_overlaps=overlaps,
                               array_form_rules=sum(
                               isinstance(value, list) for _, _, value in rules))
        counts[mod][kind] += 1

    for name, rows in [('D_BLOCKSTATES.csv', state_out), ('D_STATE_RULES.csv.gz', rules_out),
                       ('MODEL_STATE_ASSEMBLY.csv.gz', options_out), ('D_PROPERTY_DOMAINS.csv.gz', property_out),
                       ('D_MULTIPART_ASSEMBLIES.csv.gz', multi_out), ('D_EXCEPTIONS.csv', exceptions)]:
        write_rows(args.out / name, rows)
    summary = dict(status='STATIC_SOURCE_SCOPE', states=len(states), rules=len(rules_out), options=len(options_out),
                   counts={mod: dict(c) for mod, c in counts.items()},
                   references={mod: dict(c) for mod, c in ref_counts.items()},
                   options_with_parent_missing=sum(bool(r['missing_parent']) for r in options_out),
                   selected_model_keys_with_parent_missing=len({r['model_key'] for r in options_out if r['missing_parent']}),
                   unresolved_options=sum(r['reference_status'] == 'UNRESOLVED_MODEL_REF' for r in options_out),
                   exception_counts=dict(Counter(r['category'] for r in exceptions)),
                   multipart_assignments=len(multi_out),
                   multipart_assignments_without_rules=sum(r['selected_rule_count'] == 0 for r in multi_out),
                   runtime_tested=False, whole_1_3_gates_recorded_pass=0)
    (args.out / 'D_AUDIT.json').write_text(json.dumps(summary, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
