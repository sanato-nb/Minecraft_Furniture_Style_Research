"""Independent source, condition, and provenance readback for Entry4."""
import csv
import hashlib
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'research/vanilla_models/phase_1-2-D/entry4'
P = 'D_ENTRY4_265_'


def sha(b):
    return hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()


def csvrows(name):
    with (BASE / (P + name + '.csv')).open(newline='') as f:
        return list(csv.DictReader(f))


def predicate(node, props):
    if not node:
        return True
    tests = []
    for key, val in node.items():
        if key == 'AND':
            tests.append(all(predicate(sub, props) for sub in val))
        elif key == 'OR':
            tests.append(any(predicate(sub, props) for sub in val))
        else:
            tests.append(props.get(key) in str(val).split('|'))
    return all(tests)


def collect(node, domain):
    for key, val in node.items():
        if key in ('AND', 'OR'):
            for sub in val:
                collect(sub, domain)
        else:
            domain.setdefault(key, set()).update(str(val).split('|'))


def modelpath(ref):
    parts = ref.split(':', 1)
    return '1.21.11/assets/' + (parts[0] if len(parts) == 2 else 'minecraft') + '/models/' + parts[-1] + '.json'


def main():
    queue = list(csv.DictReader(open(BASE / 'D_ENTRY4_QUEUE_265.csv')))
    fixed = [r for r in csv.DictReader(open(ROOT / 'research/vanilla_models/phase_1-2-D/D_FIXED_SCOPE_1168.csv')) if r['entry'] == 'ENTRY4']
    assert len(fixed) == len(queue) == 265
    assert [(r['source_path'], r['git_blob_sha']) for r in fixed] == [(r['source_path'], r['expected_git_blob_sha']) for r in queue]
    got = csvrows('SOURCE_STATUS')
    assert len(got) == 265 and len(queue) == 265
    snapshot_sources = []
    for p in sorted(BASE.glob(P + 'ORIGINAL_BATCH*_16.json')):
        snap = json.loads(p.read_text())
        snapshot_sources.extend(snap['sources'])
    assert len(snapshot_sources) == 265
    state_rows = [json.loads(line) for line in (BASE / (P + 'STATES.jsonl')).read_text().splitlines()]
    by_source = {}
    for state in state_rows:
        by_source.setdefault(state['blockstate_path'], []).append(state)
    recomputed = 0
    alternatives = 0
    for idx, (q, record, snap) in enumerate(zip(queue, got, snapshot_sources), 1):
        name = q['source_path']
        b = (ROOT / name).read_bytes()
        assert name == record['path'] == snap['path']
        assert idx == int(record['queue_row']) == snap['queue_row']
        assert sha(b) == q['expected_git_blob_sha'] == record['observed_git_sha'] == snap['git_blob_sha']
        assert b.decode() == snap['json_text']
        raw = json.loads(snap['json_text'])
        if 'variants' in raw:
            declarations = list(raw['variants'].items())
            expected = [(k or '<empty>', [n]) for n, (k, _) in enumerate(declarations)]
        else:
            declarations = [(part.get('when', {}), part['apply']) for part in raw['multipart']]
            domain = {}
            for cond, _ in declarations:
                collect(cond, domain)
            for values in domain.values():
                if values in ({'true'}, {'false'}):
                    values.update({'true', 'false'})
            fields = sorted(domain)
            expected = []
            for vals in itertools.product(*(sorted(domain[k]) for k in fields)):
                props = dict(zip(fields, vals))
                label = ','.join(k + '=' + props[k] for k in fields) or '<empty>'
                expected.append((label, [i for i, (w, _) in enumerate(declarations) if predicate(w, props)]))
        actual = by_source[name]
        assert len(actual) == len(expected), name
        for state, (label, hits) in zip(actual, expected):
            assert state['property_key'] == label and state['matched_rules'] == hits, name
            source_options = []
            for i in hits:
                app = declarations[i][1]
                choices = app if isinstance(app, list) else [app]
                for j, opt in enumerate(choices):
                    source_options.append((i, j, len(choices), opt))
            assert len(state['model_options']) == len(source_options)
            for o, (i, j, count, src) in zip(state['model_options'], source_options):
                assert (o['rule_index'], o['alternative_index'], o['alternative_count']) == (i, j, count)
                assert o['model_ref'] == src['model'] and o['model_path'] == modelpath(src['model'])
                for field in ('x', 'y', 'uvlock', 'weight'):
                    assert o[field + '_explicit'] == (field in src) and o[field + '_value'] == src.get(field)
                alternatives += 1
            recomputed += 1
    links = csvrows('STATE_MODEL_BC_LINKS')
    cross = csvrows('MODEL_BC_CROSSWALK')
    scope_path = ROOT / 'research/vanilla_models/phase_1-2-C/C_FIXED_SCOPE_2390.csv'
    scope = {r['full_source_path']: r for r in csv.DictReader(scope_path.open())}
    assert len(links) == alternatives
    for r in cross:
        path = r['model_path']
        assert sha((ROOT / path).read_bytes()) == r['model_git_sha'] == scope[path]['git_blob_sha']
        assert (r['E_owned'] == 'True') == (scope[path]['C_assignment'] == 'E_EXCEPTION')
    report = {'schema': 'D_ENTRY4_INDEPENDENT_RECHECK/v1',
              'source_body_and_git_sha_rechecked': len(got), 'syntactic_candidates_recomputed': recomputed,
              'options_and_explicit_flags_recomputed': alternatives, 'model_scope_sha_and_owner_rechecked': len(cross),
              'queue_row_range': [1, 265], 'mismatches': 0, 'pass': True,
              'game_property_registry_verified': False, 'runtime_renderer_verified': False}
    (BASE / (P + 'INDEPENDENT_RECHECK.json')).write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
