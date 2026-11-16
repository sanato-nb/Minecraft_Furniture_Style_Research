"""Fix the 86-model E queue against B/C source identities and D usage."""
import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'research/vanilla_models/phase_1-2-E'


def blob(raw):
    return hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()


def rows(path):
    with (ROOT / path).open(newline='') as file:
        return list(csv.DictReader(file))


def model_path(ref):
    x = ref.split(':', 1)
    return f'1.21.11/assets/{x[0] if len(x)==2 else "minecraft"}/models/{x[-1]}.json'


def main():
    cpath = 'research/vanilla_models/phase_1-2-C/C_FIXED_SCOPE_2390.csv'
    bpath = 'research/vanilla_models/phase_1-2-B/entry10/B_SCOPE_2390_STATUS.csv'
    dpath = 'research/vanilla_models/phase_1-2-D/D_FIXED_SCOPE_1168.csv'
    c = rows(cpath)
    b = {r['full_source_path']: r for r in rows(bpath)}
    d = rows(dpath)
    assert len(c) == len(b) == 2390 and len(d) == 1168
    e = [r for r in c if r['C_assignment'] == 'E_EXCEPTION']
    assert len(e) == 86 and Counter(x['B_first_owner_scope'] for x in e) == {'E_FIRST_P1_30_DEFERRED': 30, 'B_FIRST_2360': 56}
    usage = defaultdict(lambda: {'blockstates': set(), 'options': 0})
    for s in d:
        raw = (ROOT/s['source_path']).read_bytes()
        assert blob(raw) == s['git_blob_sha']
        value = json.loads(raw)
        apps = value['variants'].values() if 'variants' in value else (x['apply'] for x in value['multipart'])
        for app in apps:
            for opt in (app if isinstance(app, list) else [app]):
                p = model_path(opt['model'])
                usage[p]['blockstates'].add(s['source_path'])
                usage[p]['options'] += 1
    first = sorted((x for x in e if x['B_first_owner_scope'].startswith('E_FIRST')), key=lambda x:x['full_source_path'])
    rest = sorted((x for x in e if x['B_first_owner_scope'] == 'B_FIRST_2360'), key=lambda x:x['full_source_path'])
    cohorts = [('ENTRY1', first), ('ENTRY2', rest[:28]), ('ENTRY3', rest[28:])]
    assert [len(x) for _, x in cohorts] == [30, 28, 28]
    BASE.mkdir(exist_ok=True)
    out = BASE/'E_FIXED_SCOPE_86.csv'
    fields = ['entry','entry_row','model_path','model_git_sha','priority','B_owner_scope','B_geometry_status','B_scope_sha','C_scope_sha','C_exception_owner','D_blockstate_paths_count','D_rule_option_refs','D_blockstate_paths_json','status']
    with out.open('w', newline='') as file:
        w = csv.DictWriter(file,fields,lineterminator='\n');w.writeheader()
        for entry, cohort in cohorts:
            for i, r in enumerate(cohort, 1):
                p = r['full_source_path']
                assert p in b and b[p]['git_blob_sha'] == r['git_blob_sha'] == blob((ROOT/p).read_bytes())
                assert r['C_exception_owner'] == '1-2-E'
                w.writerow({'entry':entry,'entry_row':i,'model_path':p,'model_git_sha':r['git_blob_sha'],
                    'priority':r['priority'],'B_owner_scope':r['B_first_owner_scope'],
                    'B_geometry_status':r['B_geometry_source_status'],'B_scope_sha':blob((ROOT/bpath).read_bytes()),
                    'C_scope_sha':blob((ROOT/cpath).read_bytes()),'C_exception_owner':r['C_exception_owner'],
                    'D_blockstate_paths_count':len(usage[p]['blockstates']),'D_rule_option_refs':usage[p]['options'],
                    'D_blockstate_paths_json':json.dumps(sorted(usage[p]['blockstates']),ensure_ascii=False),
                    'status':'ASSIGNED_NOT_E_INSPECTED'})
    assert len(rows(str(out.relative_to(ROOT)))) == 86
    audit={'schema':'E_FIXED_SCOPE_AUDIT/v1','baseline_head':'5ef795f4d0b24ae5535d6c9411a5f092ba35e6ac',
           'C_scope_sha':blob((ROOT/cpath).read_bytes()),'B_scope_sha':blob((ROOT/bpath).read_bytes()),
           'D_scope_sha':blob((ROOT/dpath).read_bytes()),'E_queue_sha':blob(out.read_bytes()),
           'C_exception_models':86,'B_E_first':30,'B_no_general_geometry':56,
           'D_referenced_E_models':sum(bool(usage[x['full_source_path']]['blockstates']) for x in e),
           'D_unreferenced_E_models':[x['full_source_path'] for x in e if not usage[x['full_source_path']]['blockstates']],
           'entry_model_counts':{'ENTRY1':30,'ENTRY2':28,'ENTRY3':28,'ENTRY4_AUDIT':0},
           'unique_model_paths':86,'path_SHA_mismatch':0,'entry5_allowed':False,'pass':True}
    (BASE/'E_FIXED_SCOPE_AUDIT.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(audit,ensure_ascii=False,indent=2))


if __name__ == '__main__':
    main()
