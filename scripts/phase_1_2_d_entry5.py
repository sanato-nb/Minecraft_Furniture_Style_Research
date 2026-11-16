"""Rebuild Entry5 rows 1-265 from the checked-in 1.21.11 source."""
import csv
import hashlib
import itertools
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'research/vanilla_models/phase_1-2-D/entry5'
PREFIX = 'D_ENTRY5_265'
SOURCE = '5febebb97207ecee724725c272eefe2ea9c83481'


def blob(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def read_csv(path):
    with (ROOT / path).open(newline='') as f:
        return list(csv.DictReader(f))


def write_csv(name, rows, columns):
    with (OUT / (PREFIX + '_' + name + '.csv')).open('w', newline='') as f:
        w = csv.DictWriter(f, columns, lineterminator='\n')
        w.writeheader()
        w.writerows(rows)


def write_json(name, obj):
    (OUT / (PREFIX + '_' + name + '.json')).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')


def model_path(ref):
    ns, sep, name = ref.partition(':')
    if not sep:
        ns, name = 'minecraft', ns
    return f'1.21.11/assets/{ns}/models/{name}.json'


def options(apply):
    values = apply if isinstance(apply, list) else [apply]
    assert values and all(isinstance(v, dict) and 'model' in v for v in values)
    return values


def conditions(when, domain):
    if isinstance(when, dict):
        for key, value in when.items():
            if key in ('OR', 'AND'):
                for child in value:
                    conditions(child, domain)
            else:
                domain[key].update(str(value).split('|'))


def matches(when, state):
    if not when:
        return True
    if 'OR' in when:
        return any(matches(x, state) for x in when['OR'])
    if 'AND' in when:
        return all(matches(x, state) for x in when['AND'])
    return all(str(state.get(key)) in str(value).split('|') for key, value in when.items())


def state_key(state):
    return ','.join(f'{key}={state[key]}' for key in sorted(state)) or '<empty>'


def main():
    queue_path = 'research/vanilla_models/phase_1-2-D/entry5/D_ENTRY5_QUEUE_265.csv'
    queue = read_csv(queue_path)
    assert len(queue) == 265
    assert blob((ROOT / queue_path).read_bytes()) == '0eb5b45e83ee83a8321f4b31eba69562560e2a99'
    chosen = queue
    assert len(chosen) == 265 and Path(chosen[0]['source_path']).name == 'oak_fence.json'
    assert Path(chosen[-1]['source_path']).name == 'short_dry_grass.json'
    cbase = 'research/vanilla_models/phase_1-2-C/'
    cscope = 'research/vanilla_models/phase_1-2-C/C_FIXED_SCOPE_2390.csv'
    scope = {r['full_source_path']: r for r in read_csv(cscope)}
    assert len(scope) == 2390 and blob((ROOT / cscope).read_bytes()) == '6aacb4cba3fa445fffe9f19ba8691df6494a4fa6'
    # The C source evidence is the authoritative model path/SHA crosswalk.
    models = {}
    faces = defaultdict(list)
    slots = defaultdict(list)
    pngs = {}
    for entry in range(1, 6):
        base = cbase + f'entry{entry}/'
        for r in read_csv(base + 'MODEL_SOURCE_EVIDENCE.csv'):
            p = r['leaf_path']
            assert p not in models
            models[p] = (entry, r)
        for r in read_csv(base + 'FACE_UV_EVIDENCE.csv'):
            faces[r['leaf_path']].append(r)
        for r in read_csv(base + 'TEXTURE_BINDINGS.csv'):
            slots[r['leaf_path']].append(r)
        for r in read_csv(base + 'PNG_RGBA_EVIDENCE.csv'):
            p = r['png_path']
            if p in pngs:
                assert pngs[p]['png_sha'] == r['png_sha'] and pngs[p]['rgba_sha256'] == r['rgba_sha256']
            pngs[p] = r
    c_scope_sha = '6aacb4cba3fa445fffe9f19ba8691df6494a4fa6'
    b_scope_sha = '1c4a44bce97603215e8026a0bf5a2f61f2075756'
    model_refs, rules, states, summaries, snapshots = set(), [], [], [], []
    status = []
    for idx, row in enumerate(chosen, 1):
        path = row['source_path']
        raw = (ROOT / path).read_bytes()
        sha = blob(raw)
        assert sha == row['expected_git_blob_sha'], path
        data = json.loads(raw)
        assert ('variants' in data) ^ ('multipart' in data), path
        block = Path(path).stem
        snapshots.append({'queue_row': idx, 'path': path, 'git_blob_sha': sha, 'json_text': raw.decode('utf-8')})
        rule_defs = list(data['variants'].items()) if 'variants' in data else [(part.get('when', {}), part['apply']) for part in data['multipart']]
        group = 'variants' if 'variants' in data else 'multipart'
        for ri, (key, apply) in enumerate(rule_defs):
            for ai, option in enumerate(options(apply)):
                ref = option['model']
                mp = model_path(ref)
                model_refs.add(mp)
                rules.append({'queue_row': idx, 'blockstate_path': path, 'blockstate_sha': sha, 'rule_type': group,
                              'rule_index': ri, 'variant_key': key if group == 'variants' else '',
                              'multipart_when_json': json.dumps(key, ensure_ascii=False, separators=(',', ':')) if group == 'multipart' else '',
                              'alternative_index': ai, 'alternative_count': len(options(apply)), 'model_ref': ref,
                              'model_path': mp, **{f'{k}_explicit': k in option for k in ('x', 'y', 'uvlock', 'weight')},
                              **{f'{k}_value': option.get(k) for k in ('x', 'y', 'uvlock', 'weight')},
                              'raw_apply': json.dumps(option, ensure_ascii=False, separators=(',', ':'))})
        state_inputs = []
        if group == 'variants':
            state_inputs = [(key or '<empty>', [ri], 'source_variant_rule_' + str(ri)) for ri, (key, _) in enumerate(rule_defs)]
            domain = {}
        else:
            domain = defaultdict(set)
            for key, _ in rule_defs:
                conditions(key, domain)
            for key, values in domain.items():
                if values == {'true'}:
                    values.add('false')
                elif values == {'false'}:
                    values.add('true')
            keys = sorted(domain)
            assert len(keys) <= 16
            size = 1
            for k in keys:
                size *= len(domain[k])
            assert size <= 4096, (path, size)
            for vals in itertools.product(*(sorted(domain[k]) for k in keys)):
                state = dict(zip(keys, vals))
                hit = [i for i, (when, _) in enumerate(rule_defs) if matches(when, state)]
                state_inputs.append((state_key(state), hit, 'multipart_condition_domain_synthetic'))
        option_count = 0
        for key, hits, origin in state_inputs:
            expanded = []
            for ri in hits:
                for ai, option in enumerate(options(rule_defs[ri][1])):
                    expanded.append({'rule_index': ri, 'alternative_index': ai, 'alternative_count': len(options(rule_defs[ri][1])),
                                     'model_ref': option['model'], 'model_path': model_path(option['model']),
                                     **{f'{k}_explicit': k in option for k in ('x', 'y', 'uvlock', 'weight')},
                                     **{f'{k}_value': option.get(k) for k in ('x', 'y', 'uvlock', 'weight')}})
            option_count += len(expanded)
            states.append({'state_id': block + '|' + key, 'blockstate_path': path, 'blockstate_sha': sha,
                           'property_key': key, 'state_origin': origin, 'conditions_domain_only': True,
                           'matched_rules': hits, 'model_options': expanded, 'game_state_registered': 'UNVERIFIED'})
        summaries.append({'queue_row': idx, 'block': block, 'path': path, 'git_blob_sha': sha, 'source_type': group,
                          'rules': len(rule_defs), 'rule_choice_rows': sum(len(options(a)) for _, a in rule_defs),
                          'syntactic_candidates': len(state_inputs), 'syntactic_cases_matched': sum(bool(h) for _, h, _ in state_inputs),
                          'model_option_applications': option_count,
                          'property_domain_json': json.dumps({k: sorted(v) for k, v in domain.items()}, sort_keys=True, ensure_ascii=False),
                          'property_registry_verified': False, 'source_sha_valid': True})
        status.append({'queue_row': idx, 'path': path, 'expected_git_sha': sha, 'observed_git_sha': sha,
                       'original_JSON_read': True, 'source_JSON_valid': True, 'status': 'D3_SOURCE_AND_STATIC_ASSEMBLY_VERIFIED'})
    assert len(status) == 265 and len({s['state_id'] for s in states}) == len(states)
    unknown = [p for p in sorted(model_refs) if p not in models and not (ROOT / p).exists()]
    assert not unknown, unknown
    crosswalk = []
    for p in sorted(model_refs):
        raw = (ROOT / p).read_bytes()
        sha = blob(raw)
        assert p in scope and sha == scope[p]['git_blob_sha'], p
        if p in models:
            assert scope[p]['C_assignment'] != 'E_EXCEPTION', p
            entry, prior = models[p]
            assert sha == prior['leaf_sha'], p
            ff = faces[p]
            crosswalk.append({'model_path': p, 'model_git_sha': sha, 'C_entry': f'ENTRY{entry}',
                              'C_source_evidence_path': cbase + f'entry{entry}/MODEL_SOURCE_EVIDENCE.csv',
                              'C_scope_sha': c_scope_sha, 'B_scope_sha': b_scope_sha, 'E_owned': False,
                              'C_applied_faces': len(ff), 'C_png_bound_faces': sum(bool(r['png_path']) for r in ff),
                              'C_template_unbound_faces': sum(not r['png_path'] for r in ff),
                              'C_explicit_UV_faces': sum(r['uv_type'] == 'explicit_source' for r in ff),
                              'C_no_UV_key_faces': sum(r['uv_type'] != 'explicit_source' for r in ff),
                              'C_texture_slot_rows': len(slots[p]), 'D_new_BC_face_or_PNG_measurements': 0})
        else:
            assert scope[p]['C_assignment'] == 'E_EXCEPTION' and scope[p]['C_exception_owner'] == '1-2-E', p
            crosswalk.append({'model_path': p, 'model_git_sha': sha, 'C_entry': 'E_EXCEPTION',
                              'C_source_evidence_path': '', 'C_scope_sha': c_scope_sha, 'B_scope_sha': b_scope_sha,
                              'E_owned': True, 'C_applied_faces': 0, 'C_png_bound_faces': 0, 'C_template_unbound_faces': 0,
                              'C_explicit_UV_faces': 0, 'C_no_UV_key_faces': 0, 'C_texture_slot_rows': 0,
                              'D_new_BC_face_or_PNG_measurements': 0})
    # Verify every referenced PNG against the original C manifest, not merely the C CSV.
    linked_pngs = set()
    texture_links = []
    for p in sorted(model_refs & models.keys()):
        entry, _ = models[p]
        for r in slots[p]:
            texture_links.append({'model_path': p, 'model_git_sha': blob((ROOT / p).read_bytes()), 'slot': r['slot'],
                                  'resolved_texture': r['resolved_texture'], 'binding_status': r['status'],
                                  'C_binding_file': cbase + f'entry{entry}/TEXTURE_BINDINGS.csv',
                                  'C_binding_blob_sha': blob((ROOT / (cbase + f'entry{entry}/TEXTURE_BINDINGS.csv')).read_bytes()),
                                  'D_new_PNG_RGBA_decoded': 0})
        for face in faces[p]:
            png = face['png_path']
            if png:
                assert png in pngs and blob((ROOT / png).read_bytes()) == pngs[png]['png_sha'], png
                linked_pngs.add(png)
    maprows = {r['model_path']: r for r in crosswalk}
    links = []
    for s in states:
        for o in s['model_options']:
            m = maprows[o['model_path']]
            links.append({'state_id': s['state_id'], 'blockstate_path': s['blockstate_path'], 'blockstate_sha': s['blockstate_sha'],
                          'rule_index': o['rule_index'], 'alternative_index': o['alternative_index'], 'model_path': o['model_path'],
                          'model_git_sha': m['model_git_sha'], 'E_owned': m['E_owned'], 'C_entry': m['C_entry'],
                          'C_source_evidence_path': m['C_source_evidence_path'], 'C_applied_faces_preexisting': m['C_applied_faces'],
                          'D_new_BC_or_RGBA_credit': 0})
    write_csv('SOURCE_STATUS', status, list(status[0]))
    write_csv('RULES', rules, list(rules[0]))
    write_csv('SUMMARY', summaries, list(summaries[0]))
    write_csv('MODEL_BC_CROSSWALK', crosswalk, list(crosswalk[0]))
    write_csv('TEXTURE_C_LINKS', texture_links, list(texture_links[0]))
    write_csv('STATE_MODEL_BC_LINKS', links, list(links[0]))
    with (OUT / (PREFIX + '_STATES.jsonl')).open('w') as f:
        for s in states:
            f.write(json.dumps(s, ensure_ascii=False, separators=(',', ':')) + '\n')
    for start in range(0, len(snapshots), 16):
        write_json(f'ORIGINAL_BATCH{start // 16 + 1:02}_16', {'schema': 'D_ENTRY5_ORIGINAL/v1',
                    'baseline_head': SOURCE, 'queue_rows': [snapshots[start]['queue_row'], snapshots[min(start + 15, len(snapshots) - 1)]['queue_row']],
                    'sources': snapshots[start:start + 16]})
    audit = {'schema': 'D_ENTRY5_AUDIT/v1', 'baseline_head': SOURCE, 'queue_sha': blob((ROOT / queue_path).read_bytes()),
             'queue_rows': [1, 265], 'source_SHA_and_JSON_pass': len(status), 'source_types': {kind: sum(x['source_type'] == kind for x in summaries) for kind in ('variants', 'multipart')},
             'rule_choice_rows': len(rules), 'syntactic_state_candidates': len(states), 'state_model_options': len(links),
             'unique_models': len(crosswalk), 'C_direct_models': sum(not x['E_owned'] for x in crosswalk),
             'E_owned_models': sum(x['E_owned'] for x in crosswalk), 'C_prior_faces': sum(x['C_applied_faces'] for x in crosswalk),
             'C_prior_slots': len(texture_links), 'C_prior_png_paths_sha_checked': len(linked_pngs),
             'game_registered_states_verified': False, 'official_JAR_authenticated': False, 'runtime_renderer_verified': False}
    write_json('AUDIT', audit)
    print(json.dumps(audit, indent=2))


if __name__ == '__main__':
    main()
