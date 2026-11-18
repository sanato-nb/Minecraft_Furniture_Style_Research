"""기존 A/B 연구 원장 재집계. 원저자 bytes 신규 검증을 주장하지 않는다."""
import csv
import hashlib
import io
import json
import subprocess
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
A = ROOT / 'research/furniture_mods/phase_1-3/A'
B = A.parent / 'B'
HEAD = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
errors = []
inputs = {}

def blob(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()

def read(path):
    data = path.read_bytes()
    rel = path.relative_to(ROOT).as_posix()
    remote = subprocess.check_output(['git', 'rev-parse', HEAD + ':' + rel], cwd=ROOT, text=True).strip()
    inputs[rel] = {'git_blob_sha': remote, 'computed_blob_sha': blob(data), 'bytes': len(data)}
    check(remote == blob(data), '입력 blob 불일치: ' + rel)
    return data.decode('utf-8-sig')

def rows(path):
    result = list(csv.DictReader(io.StringIO(read(path))))
    inputs[path.relative_to(ROOT).as_posix()]['csv_rows'] = len(result)
    return result

def check(ok, message):
    if not ok:
        errors.append(message)

manifest = rows(A / 'A_INPUT_MANIFEST.csv')
for r in manifest:
    data = (ROOT / r['repo_path']).read_bytes()
    check(blob(data) == r['git_blob_sha'] and len(data) == int(r['bytes']), '선행파일 무결성: ' + r['repo_path'])
check(len(manifest) == 195 and len({r['prior_version'] for r in manifest}) == 14, '195파일/14버전')
leaf = rows(A / 'A_ANOTHER_204_PRIOR_CROSSWALK.csv')
cohorts = dict(Counter(r['cohort'] for r in leaf))
check(cohorts == {'v18':33,'v21':38,'v22':43,'v23':51,'v24':39}, '모델 코호트')
leaf_index = {r['normalized_source_path']:r for r in leaf}
check(len(leaf_index) == len(leaf) == 204, '모델 중복/누락')
prior_indexes = {}
for r in leaf:
    p = r['source_ledger']
    if p not in prior_indexes:
        prior_indexes[p] = {v['source_path']:v for v in rows(ROOT/p)}
    old = prior_indexes[p].get(r['source_path'], {})
    sha = old.get('source_sha') or old.get('original_author_model_git_sha') or old.get('git_blob_sha')
    check(sha == r['source_sha'] == r['A_original_blob_sha'], '선행 모델 SHA 연결: ' + r['source_path'])
    check((old.get('parent') or old.get('parent_template')) == r['parent_ref'], '부모 선언 연결: ' + r['source_path'])
states = rows(A / 'A_ANOTHER_22_BLOCKSTATES.csv')
templates = rows(A / 'A_ANOTHER_69_TEMPLATES.csv')
chairs = rows(A / 'A_CHAIR_39_RELATIONS.csv')
hc = rows(A / 'A_HANDCRAFTED_PRIOR_SCOPE.csv')
issues = rows(A / 'A_UNRESOLVED.csv')
tindex = {r['template_ref']:r for r in templates}
check(len(tindex) == len(templates) == 69, '템플릿69')
check(sum(r['v18_selected'] == 'true' for r in templates) == 30, 'v18 템플릿 부분집합30')
check(len(states) == len({r['source_path'] for r in states}) == 22, '상태22')
check(sum(int(r['model_apply_records']) for r in states) == 1188, '상태 적용1188')
check(len(chairs) == 39 and len({r['source_path'] for r in chairs}) == 39, '의자39')
for r in chairs:
    parent = tindex[r['parent_template']]
    check(r['source_path'] in leaf_index and r['source_sha'] == leaf_index[r['source_path']]['source_sha'], '의자 leaf 연결')
    check(r['parent_sha'] == parent['source_sha'] and int(r['inherited_elements']) == int(parent['own_elements']) and int(r['inherited_faces']) == int(parent['own_faces']), '의자 상속 연결')
chair_counts = dict(Counter(r['parent_template'].rsplit('/',1)[-1] for r in chairs))
check(chair_counts == {'chair':19,'chair_tucked':20}, '의자 부모 분할')
hc_counts = dict(Counter(r['record_type'] for r in hc))
check(hc_counts.get('AUTHORED') == 120 and hc_counts.get('GENERATED_LEAF') == 16, 'HC 선행 분모')
af_models = rows(B/'B_MODEL_INVENTORY_AF.csv')
hc_authored = rows(B/'B_MODEL_INVENTORY_HC_AUTHORED.csv')
hc_generated = [r for p in sorted(B.glob('B_MODEL_INVENTORY_HC_GENERATED_*.csv')) for r in rows(p)]
bs_inventory = rows(B/'B_BLOCKSTATE_INVENTORY.csv')
new_states = [r for p in sorted(B.glob('B_AF_STATES_DIRECT_*.csv')) for r in rows(p)]
hc_direct = [r for p in sorted(B.glob('B_HC_AUTHORED_DIRECT_*.csv')) for r in rows(p)]
hc16 = rows(B/'B_HC_PRIOR_GENERATED_16_DIRECT.csv')
queue = rows(B/'ENTRY_QUEUE.csv')
check(len(af_models) == 1629 and len(hc_authored) == 121 and len(hc_generated) == 12273, 'B 모델 모집단')
check(len({(r['mod_id'],r['source_path']) for r in af_models+hc_authored+hc_generated}) == 14023, 'B 모집단 중복')
check(len(bs_inventory) == 444 and len(queue) == 109, 'B 상태/회차')
check(len(new_states) == 155 and len({r['source_path'] for r in states+new_states}) == 177, 'A+B 상태 집합')
check(all(r['upstream_tree_sha'] == r['fetch_sha'] == r['independent_original_blob_sha'] and r['sha_status'] == 'PASS' for r in new_states), 'B 상태 증거 SHA')
check(len(hc_direct) == 121 and all(r['tree_blob_sha'] == r['remote_blob_sha'] == r['independent_blob_sha'] for r in hc_direct), 'HC121 증거 SHA')
check(len(hc16) == 16 and all(r['A_prior_sha'] == r['fetch_original_sha'] == r['independent_original_sha'] for r in hc16), 'HC16 증거 SHA')
exceptions = rows(B/'B_AF_155_REF_EXCEPTIONS.csv')
state = json.loads(read(ROOT/'handoff/STATE.json'))
check(state['phase_1_3_A_execution']['gates_passed'] == 7 and not state['phase_1_3_B_execution']['completed'], '현행 상태')
result = {
    'schema':'CURRENT_SNAPSHOT_LEDGER_RECHECK/v1','date_kst':'2026-11-18','baseline_main':HEAD,
    'scope':'저장소 원장·연구파일 bytes·Git blob SHA 재집계; 원저자 JSON 신규 수집 아님',
    'original_upstream_bytes_newly_read_this_run':0,'new_models_discovered':0,
    'A_status_preserved':'A_PRIOR_EVIDENCE_RECONCILIATION_PASS','A_gates':{'passed':7,'total':7},
    'M_gates':{'passed':0,'total':6},'prior_files_checked':len(manifest),
    'prior_bytes':sum(int(r['bytes']) for r in manifest),'cohorts':cohorts,
    'A_counts':{'leaf':len(leaf),'states':len(states),'templates':len(templates),'chairs':len(chairs),
                'chair_elements':sum(int(r['inherited_elements']) for r in chairs),
                'chair_face_instances':sum(int(r['inherited_faces']) for r in chairs),'handcrafted_record_types':hc_counts},
    'B_counts':{'AF_model_paths':len(af_models),'HC_authored_paths':len(hc_authored),'HC_generated_paths':len(hc_generated),
                'all_model_paths':len(af_models+hc_authored+hc_generated),'states':len(bs_inventory),'entries':len(queue),
                'AF_direct_states_prior_A_plus_B':177,'HC_direct_model_evidence':len(hc_direct)+len(hc16),
                'HC_generated_unread':len(hc_generated)-len(hc16),'AF_model_unread':len(af_models)-len(leaf)-len(templates)},
    'B_reference_exceptions':exceptions,'planning_status_snapshot_is_not_current_execution_state':True,
    'input_files':inputs,'errors':errors,'result':'PASS' if not errors else 'FAIL'
}
out = A/'A_CURRENT_SNAPSHOT_RECHECK_20261118.json'
out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k != 'input_files'},ensure_ascii=False,indent=2))
raise SystemExit(bool(errors))
