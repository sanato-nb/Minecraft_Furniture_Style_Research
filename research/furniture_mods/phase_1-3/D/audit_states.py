"""원문 선택 순서·모델 조인·조합을 생성기와 다른 방식으로 재검산한다."""
import argparse
from collections import Counter, defaultdict
from itertools import product
import json
from pathlib import Path
import zipfile

from analyze_states import HERE, load_inputs, read_rows


def group(rows):
    result = defaultdict(list)
    for row in rows:
        result[(row['mod'], row['state_id'])].append(row)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for arg in ('af', 'hc', 'macaw', 'version', 'project', 'b', 'c', 'mc1211', 'mc12111'):
        parser.add_argument('--' + arg, required=True, type=Path)
    parser.add_argument('--out', default=HERE, type=Path)
    args = parser.parse_args()
    states, models = load_inputs(args)
    model_lookup = {(m['mod'], m['model_id']): m for m in models}
    c_missing = {r['model_key'] for r in read_rows(args.c / 'C_EXCEPTIONS.csv.gz')
                 if r['status'] == 'PARENT_MISSING'}
    states_out = group(read_rows(args.out / 'D_BLOCKSTATES.csv'))
    rules_out = group(read_rows(args.out / 'D_STATE_RULES.csv.gz'))
    options_out = group(read_rows(args.out / 'MODEL_STATE_ASSEMBLY.csv.gz'))
    multipart_out = group(read_rows(args.out / 'D_MULTIPART_ASSEMBLIES.csv.gz'))
    properties_out = group(read_rows(args.out / 'D_PROPERTY_DOMAINS.csv.gz'))
    assert set(states_out) == set(rules_out) == set(options_out) == set(states)
    assert set(multipart_out) == {k for k, (_, data) in states.items() if 'multipart' in data}
    assert set(properties_out) <= set(states)

    checks = Counter()
    expected_exceptions = set()
    with zipfile.ZipFile(args.mc1211) as vanilla:
        for key, (source, body) in states.items():
            mod, state_id = key
            state, = states_out[key]
            assert (state['source_sha'], state['path']) == (source['sha'], source['path'])
            variant = 'variants' in body
            if variant:
                native = [(i, selector, dict(term.split('=') for term in selector.split(',') if term), choice)
                          for i, (selector, choice) in enumerate(body['variants'].items())]
            else:
                native = [(i, str(i), part.get('when', {}), part['apply'])
                          for i, part in enumerate(body['multipart'])]
            assert len(native) == len(rules_out[key]) == int(state['rule_count'])
            expected_options = []
            property_values = defaultdict(set)
            for (i, selector, condition, choice), rule in zip(native, rules_out[key], strict=True):
                assert (i, selector, condition) == (int(rule['rule_index']), rule['source_selector'],
                                                    json.loads(rule['condition']))
                members = choice if type(choice) is list else [choice]
                assert (len(members), 'array' if type(choice) is list else 'object') == (
                    int(rule['options']), rule['apply_form'])
                for k, v in condition.items():
                    assert k not in ('AND', 'OR') and '!' not in v and '|' not in v, (key, condition)
                    property_values[k].add(v)
                expected_options.extend((i, j, option) for j, option in enumerate(members))
            assert len(expected_options) == int(state['option_count'])
            for (i, j, original), row in zip(expected_options, options_out[key], strict=True):
                expected = {'model': row['model_ref']}
                keys = row['explicit_fields'].split('|') if row['explicit_fields'] else []
                for field in keys:
                    expected[field] = row[field] == 'true' if field == 'uvlock' else int(row[field])
                assert (i, j, original) == (int(row['rule_index']), int(row['option_index']), expected)
                assert int(row['x_mod_360']) == int(row['x']) % 360
                assert int(row['y_mod_360']) == int(row['y']) % 360
                namespace, separator, suffix = original['model'].rpartition(':')
                model_id = (namespace if separator else 'minecraft') + ':' + suffix
                assert model_id == row['model_id']
                if (mod, model_id) in model_lookup:
                    model = model_lookup[(mod, model_id)]
                    assert row['reference_status'] == 'LOCAL'
                    assert (row['model_key'], row['model_path'], row['model_source_sha']) == (
                        model['model_key'], model['path'], model['source_hash'])
                    assert row['geometry_status'] == model['geometry_status']
                    assert row['model_key'] not in c_missing
                elif mod == 'AF' and model_id.startswith('minecraft:'):
                    import hashlib
                    path = 'assets/minecraft/models/' + suffix + '.json'
                    assert row['reference_status'] == 'VANILLA_JAR' and row['model_path'] == path
                    assert hashlib.sha256(vanilla.read(path)).hexdigest() == row['model_source_sha']
                else:
                    assert row['reference_status'] == 'UNRESOLVED_MODEL_REF'
                    assert (state_id, model_id) == ('another_furniture:unused/white_awning',
                                                     'another_furniture:block/awning/white_double')
                    expected_exceptions.add((key, i, j, 'UNRESOLVED_MODEL_REF'))
                if state_id in ('another_furniture:birch_chair', 'another_furniture:spruce_chair'):
                    if native[i][1] == 'facing=south,tucked=false,variant=3':
                        assert suffix == 'block/chair/' + state_id.split(':')[1].split('_')[0] + '_1'
                        expected_exceptions.add((key, i, j, 'PRIOR_CHAIR_VARIANT_3_POINTS_TO_1'))
                checks['references_' + row['reference_status']] += 1
            assert {r['property']: set(r['observed_values'].split('|')) for r in properties_out[key]} == property_values
            if variant:
                terms = [frozenset(condition.items()) for _, _, condition, _ in native]
                full = set(term for term in terms if len(term) == len(property_values))
                partial = [term for term in terms if len(term) < len(property_values)]
                assignments = gaps = overlaps = 0
                for values in product(*property_values.values()):
                    setting = frozenset(zip(property_values, values, strict=True))
                    match_count = (setting in full) + sum(term <= setting for term in partial)
                    assignments += 1
                    gaps += match_count == 0
                    overlaps += match_count > 1
                assert (assignments, gaps, overlaps) == tuple(int(state['variant_observed_domain_'+ val])
                    for val in ('assignments', 'gaps', 'overlaps'))
                checks.update(variant_assignments=assignments, variant_gaps=gaps, variant_overlaps=overlaps)
            else:
                domains = {k: {'true', 'false'} if v <= {'true', 'false'} else v for k, v in property_values.items()}
                actual = {frozenset(json.loads(r['observed_domain_assignment']).items()):
                          r['selected_rule_indices'] for r in multipart_out[key]}
                expected = {}
                for values in product(*domains.values()):
                    setting = frozenset(zip(domains, values, strict=True))
                    selected = [str(i) for i, _, condition, _ in native if condition.items() <= setting]
                    expected[setting] = '|'.join(selected)
                assert actual == expected
                assert len(actual) == len(multipart_out[key]) == int(state['multipart_assignments'])
                checks['multipart_assignments'] += len(actual)
            checks.update(states=1, rules=len(native), options=len(expected_options))

    exception_rows = read_rows(args.out / 'D_EXCEPTIONS.csv')
    assert len(expected_exceptions) == len(exception_rows) == 6
    assert expected_exceptions == {((r['mod'], r['state_id']), int(r['rule_index']),
                                    int(r['option_index']), r['category']) for r in exception_rows}
    summary = {'status': 'PASS', **dict(checks), 'exception_rows': len(exception_rows),
               'C_missing_parent_model_keys': len(c_missing), 'C_missing_parent_model_keys_directly_selected': 0,
               'input_reader_shared': True, 'runtime_tested': False, 'errors': []}
    (args.out / 'D_INDEPENDENT_AUDIT.json').write_text(json.dumps(summary, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
