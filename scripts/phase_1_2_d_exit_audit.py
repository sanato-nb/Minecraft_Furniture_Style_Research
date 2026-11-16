"""Cross-check the immutable six-entry blockstate population and prior evidence."""
import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'research/vanilla_models/phase_1-2-D'


def sha(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def rows(path):
    with path.open(newline='') as file:
        return list(csv.DictReader(file))


def records(path):
    return [json.loads(line) for line in path.read_text().splitlines()]


def source_snapshots():
    result = []
    b = BASE
    result.extend(json.loads((b/'entry1/D_ORIGINAL_12_SOURCE_SNAPSHOT.json').read_text())['samples'])
    for p in sorted((b/'entry2').glob('D_ORIGINAL_SOURCE_BATCH*_16.json')):
        result.extend(json.loads(p.read_text())['entries'])
    for p in sorted((b/'entry3').glob('D_ENTRY3_SUBBATCH1_ORIGINAL_BATCH*_8.json')):
        result.extend(json.loads(p.read_text())['sources'])
    for p in sorted((b/'entry3').glob('D_ENTRY3_REMAINING_217_ORIGINAL_BATCH*_16.json')):
        result.extend(json.loads(p.read_text())['sources'])
    for entry in (4, 5, 6):
        for p in sorted((b/f'entry{entry}').glob(f'D_ENTRY{entry}_265_ORIGINAL_BATCH*_16.json')):
            result.extend(json.loads(p.read_text())['sources'])
    return result


def source_data(item):
    path = item.get('source_path', item.get('path'))
    claimed = item.get('source_git_sha', item.get('git_blob_sha', item.get('expected_sha')))
    body = item.get('raw_json', item.get('json_text'))
    return path, claimed, body


def source_options(data):
    declarations = data.get('variants', {}).items() if 'variants' in data else ((x.get('when', {}), x['apply']) for x in data['multipart'])
    for _, app in declarations:
        for choice in (app if isinstance(app, list) else [app]):
            yield choice['model']


def model_path(ref):
    parts = ref.split(':', 1)
    return '1.21.11/assets/' + (parts[0] if len(parts) == 2 else 'minecraft') + '/models/' + parts[-1] + '.json'


def state_rows():
    b = BASE
    first = rows(b/'entry1/D_STATE_ASSEMBLY.csv')
    second = records(b/'entry2/D_STATE_ASSEMBLY.jsonl')
    paths = [b/'entry3/D_ENTRY3_SUBBATCH1_48_STATES.jsonl', b/'entry3/D_ENTRY3_REMAINING_217_STATES.jsonl']
    paths += [b/f'entry{n}/D_ENTRY{n}_265_STATES.jsonl' for n in (4, 5, 6)]
    return [first, second] + [records(p) for p in paths]


def main():
    fixed = rows(BASE/'D_FIXED_SCOPE_1168.csv')
    assert len(fixed) == 1168
    by_path = {r['source_path']: r for r in fixed}
    assert len(by_path) == 1168
    assigned = Counter(r['entry'] for r in fixed)
    assert assigned == {'ENTRY1': 12, 'ENTRY2': 96, 'ENTRY3': 265, 'ENTRY4': 265, 'ENTRY5': 265, 'ENTRY6': 265}
    snapshots = source_snapshots()
    assert len(snapshots) == 1168
    checked, source_choices = {}, {}
    for item in snapshots:
        path, claimed, body = source_data(item)
        assert path in by_path and path not in checked
        actual = (ROOT/path).read_bytes()
        assert body.encode() == actual and sha(actual) == claimed == by_path[path]['git_blob_sha'], path
        data = json.loads(body)
        assert ('variants' in data) != ('multipart' in data), path
        checked[path] = data
        source_choices[path] = Counter(source_options(data))
    assert set(checked) == set(by_path)
    rule_files = [BASE/'entry1/D_SOURCE_RULES.csv', BASE/'entry2/D_SOURCE_RULES.csv',
                  BASE/'entry3/D_ENTRY3_SUBBATCH1_48_RULES.csv', BASE/'entry3/D_ENTRY3_REMAINING_217_RULES.csv']
    rule_files += [BASE/f'entry{n}/D_ENTRY{n}_265_RULES.csv' for n in (4, 5, 6)]
    rule_count = 0
    ledger_choices = defaultdict(Counter)
    for file in rule_files:
        for r in rows(file):
            rule_count += 1
            ledger_choices[r['blockstate_path']][r['model_ref']] += 1
    assert set(ledger_choices) == set(checked)
    assert all(ledger_choices[p] == source_choices[p] for p in checked)
    states = state_rows()
    assert [len(v) for v in states] == [380, 884, 319, 1560, 1804, 2303, 1943]
    scope_file = ROOT/'research/vanilla_models/phase_1-2-C/C_FIXED_SCOPE_2390.csv'
    scope = {r['full_source_path']: r for r in rows(scope_file)}
    assert len(scope) == 2390
    # Every model option in every state resolves to the same C/E identity, without
    # counting a C face or PNG as newly measured D evidence.
    model_refs, option_total, state_ids = set(), 0, set()
    for group in states:
        for state in group:
            path = state['blockstate_path']
            assert path in checked and state['blockstate_sha'] == by_path[path]['git_blob_sha']
            state_id = state['state_id']
            assert state_id not in state_ids
            state_ids.add(state_id)
            if 'model_options_json' in state:
                opts = json.loads(state['model_options_json'])
            elif 'simultaneous_model_groups' in state:
                opts = [o for g in state['simultaneous_model_groups'] for o in g['alternatives']]
            else:
                opts = state['model_options']
            assert len(opts) == int(state.get('model_option_count', len(opts)))
            for opt in opts:
                path_model = model_path(opt['model_ref'])
                assert path_model == opt['model_path'] and opt['model_ref'] in source_choices[path]
                assert path_model in scope
                model_refs.add(path_model)
                option_total += 1
    model_sha = {p: sha((ROOT/p).read_bytes()) for p in model_refs}
    assert all(model_sha[p] == scope[p]['git_blob_sha'] for p in model_refs)
    e_owned = sum(scope[p]['C_assignment'] == 'E_EXCEPTION' for p in model_refs)
    # Provenance and independent checks are per Entry; no stage closure before
    # the final remote readback has checked the newly written result.
    checks = [BASE/'entry1/D_ENTRY1_INDEPENDENT_SOURCE_AUDIT.json', BASE/'entry2/D_ENTRY2_INDEPENDENT_SOURCE_AUDIT.json',
              BASE/'entry3/D_ENTRY3_SUBBATCH1_48_INDEPENDENT_RECHECK.json', BASE/'entry3/D_ENTRY3_REMAINING_217_INDEPENDENT_RECHECK.json']
    checks += [BASE/f'entry{n}/D_ENTRY{n}_265_INDEPENDENT_RECHECK.json' for n in (4, 5, 6)]
    independent = [json.loads(p.read_text()) for p in checks]
    assert independent[0]['E1_direct_original_blockstate_json'] == 12
    assert independent[0]['E1_original_blob_sha_mismatch'] == independent[0]['independent_state_mismatch'] == 0
    assert all(x.get('pass', False) for x in independent[1:])
    assert all((BASE/f'entry{n}/D_ENTRY{n}_REMOTE_READBACK.json').exists() for n in (1, 2, 3, 4, 5))
    result = {'schema': 'D_SOURCE_EXIT_AUDIT/v1', 'fixed_scope_paths': len(fixed), 'source_snapshots_body_SHA_reverified': len(checked),
              'source_paths_duplicate_or_missing': 0, 'six_entry_counts': dict(assigned), 'source_rule_option_rows': rule_count,
              'syntactic_state_rows': len(state_ids), 'state_option_instances': option_total,
              'distinct_model_paths_C_or_E_sha_verified': len(model_refs), 'distinct_E_exception_model_paths': e_owned,
              'independent_entry_checks_pass': len(independent), 'entry1_to_entry5_remote_readbacks_present': 5,
              'D1': 'PASS', 'D2': 'PASS_SOURCE_JSON_AND_RULES', 'D3': 'PASS_STATIC_SYNTAX_DOMAIN_ONLY',
              'D4': 'PASS_MODEL_C_E_PATH_SHA_SCOPE', 'D5': 'PENDING_ENTRY6_REMOTE_READBACK',
              'official_JAR_authenticated': False, 'game_state_registry_verified': False, 'runtime_render_verified': False,
              'whole_D_complete': False}
    path = BASE/'entry6/D_ENTRY6_PRE_REMOTE_EXIT_AUDIT.json'
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
