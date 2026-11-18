"""1-3-F 고정 원본의 정규화 DB와 1-4·1-5 인계 원장을 생성한다."""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
import lzma
from pathlib import Path
import sqlite3
import subprocess
import sys
import zipfile

HERE = Path(__file__).resolve().parent
BASE = '0897168655cd575075a44556e53e4a22e0d0fbc0'
ROOT = 'research/furniture_mods/'
PHASE = ROOT + 'phase_1-3/'
NS = {'AF':'another_furniture', 'HC':'handcrafted', 'MACAW':'mcwfurnitures'}
VERSIONS = {'AF':'4.0.3', 'HC':'4.0.3', 'MACAW':'3.4.2'}
ORIGIN = {'AF':'https://github.com/crispytwig/AnotherFurniture',
          'HC':'https://github.com/terrarium-earth/Handcrafted',
          'MACAW':'https://modrinth.com/mod/macaws-furniture/version/xhmciaUD'}
PRIOR_PNG = [
    ('AF','v19/another_texture_53_png_source_manifest.csv','texture','sha',None,53),
    ('AF','v21/another_new_14_png_unique_source_metrics.csv','texture','source_sha',None,14),
    ('AF','v22/shutter_43_png_original_source_manifest.csv','texture','source_git_sha','newly_sampled',42),
    ('AF','v23/new_42_png_first_measured_in_v23.csv','texture','git_sha',None,42),
    ('HC','v13/handcrafted_png_12_pixel_metrics.csv','name','sha',None,12),
    ('HC','v16/handcrafted_12_new_png_pixel_metrics.csv','name','upstream_blob_sha',None,12),
]
PRIOR_FACE = [('HC','v17/face_pixel_samples_784.csv',784),
              ('AF','v19/another_804_face_actual_rgba.csv',804),
              *[('AF',f'v21/new_38_leaf_rgba_faces_batch_{i}_of_4.csv',n)
                for i,n in enumerate((238,727,207,20),1)],
              ('AF','v22/shutter_214_face_uv_original_rgba.csv',214),
              ('AF','v23/new_51_leaf_all_1119_face_actual_rgba.csv',1119)]


def git(repo, *args):
    return subprocess.check_output(['git','-C',str(repo),*args])


def tree(repo, pin):
    return {path:metadata.split()[2] for metadata,path in (
        r.split('\t',1) for r in git(repo,'ls-tree','-r','-z',pin).decode().split('\0') if r)}


def optional(value):
    return value or None


def lookup(rows, field):
    return {r[field]:r for r in rows}


def group(rows, field):
    result = defaultdict(list)
    for r in rows:
        result[r[field]].append(r)
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for name in ('repo','prior','b','c','d','e','af','hc','macaw','vanilla'):
        p.add_argument('--'+name, type=Path, required=True)
    p.add_argument('--out',type=Path,default=HERE)
    a = p.parse_args()
    sys.dont_write_bytecode = True
    sys.path.insert(0,str(a.c.resolve()))
    from analyze_geometry import (PINS, MC_CLIENT_SHA1, archive_paths, face_slot, hash_data,
                                  read_csv, write_csv, normalize)
    a.out.mkdir(parents=True,exist_ok=True)
    manifest = {}
    baseline = tree(a.repo,BASE)

    def verified(file, remote_path):
        observed = hash_data(file.read_bytes(),True)
        assert observed == baseline[remote_path], remote_path
        manifest[remote_path] = observed
        return file

    def read(stage,name):
        local = getattr(a,stage.lower()) / name
        return read_csv(verified(local,PHASE+stage+'/'+name))

    prior = {}
    prior_summary = []
    for mod,file,resource_col,sha_col,filter_col,expected in PRIOR_PNG:
        ledger = ROOT+file
        rows = read_csv(verified(a.prior/file,ledger))
        found = 0
        for line,row in enumerate(rows,2):
            if filter_col and row[filter_col]!='1':
                continue
            identifier = row[resource_col] if ':' in row[resource_col] else NS[mod]+':block/'+row[resource_col]
            key = (identifier,PINS[mod][1])
            assert key not in prior, key
            prior[key] = (ledger,manifest[ledger],line,row[sha_col])
            found += 1
        assert found==expected
        prior_summary.append((mod,'PNG',ledger,manifest[ledger],found))
    for mod,file,expected in PRIOR_FACE:
        ledger = ROOT+file
        rows = read_csv(verified(a.prior/file,ledger))
        assert len(rows)==expected, (file,len(rows))
        prior_summary.append((mod,'FACE_RGBA',ledger,manifest[ledger],len(rows)))
    assert len(prior)==175 and sum(r[-1] for r in prior_summary if r[1]=='FACE_RGBA')==4113

    b_models, b_states = {}, {}
    for mod in NS:
        name = f'B_{mod}_SOURCE_BODIES.csv.gz'
        docs = read_csv(verified(a.b/name,PHASE+'B/source_verification/'+name))
        for r in docs:
            key = mod,r['path']
            if r['family']=='models':
                b_models[key] = r
            if r['family']=='blockstates':
                b_states[key] = r
    catalog = lookup(read('C','mod_furniture_catalog.csv.gz'),'model_key')
    assert len(catalog)==len(b_models)==16572
    chains = lookup(read('C','MODEL_PARENT_CHAINS.csv.gz'),'model_key')
    c_parents = lookup(read('C','C_VANILLA_PARENTS.csv'),'source_key')
    geometry_rows = read('C','mod_model_elements.csv.gz')
    c_parts = {(r['source_key'],r['element_index']):r for r in read('C','PARTS.csv.gz')}
    face_rows = read('C','MODEL_FACES.csv.gz')
    selected_states = read('D','D_BLOCKSTATES.csv')
    code_by_state = {(r['mod'],r['state_id']):r for r in read('D','CONNECTION_RULES.csv')}
    rules = read('D','D_STATE_RULES.csv.gz')
    options = read('D','MODEL_STATE_ASSEMBLY.csv.gz')
    e_cases = read('E','E_SAMPLE_METRICS.csv')
    e_options = read('E','CATEGORY_EVIDENCE.csv')
    e_groups = read('E','E_PART_GROUPS.csv')
    chair_rows = read_csv(verified(a.prior/'v24/chair_remaining_39_original_json_geometry_audit.csv',
                                  ROOT+'v24/chair_remaining_39_original_json_geometry_audit.csv'))
    verified(a.e/'EXCEPTIONS.md',PHASE+'E/EXCEPTIONS.md')
    assert len(chair_rows)==39
    chair_set = {r[c] for r in chair_rows for c in ('texture_bottom','texture_seat','texture_back')}
    assert len(chair_set)==24

    db_path = a.out/'furniture_research.sqlite'
    db_path.unlink(missing_ok=True)
    db = sqlite3.connect(db_path)
    db.executescript((HERE/'schema.sql').read_text())
    put = db.executemany
    put('INSERT INTO source VALUES (?,?,?,?,?,?,?)',[(m,VERSIONS[m],mc,pin,
        'GIT_COMMIT_SHA1' if m!='MACAW' else 'JAR_SHA256',
        'GIT_BLOB_SHA1' if m!='MACAW' else 'SHA256',ORIGIN[m]) for m,(pin,mc) in PINS.items()]+[
        ('MC'+v,v,v,sha,'JAR_SHA1','SHA256','https://piston-meta.mojang.com/mc/game/version_manifest_v2.json')
        for v,sha in MC_CLIENT_SHA1.items()])
    model_source_rows, bodies, local_png = [], {}, {}
    for mod,(pin,mc) in PINS.items():
        model_rows = [r for r in catalog.values() if r['mod']==mod]
        wanted = {r['path'] for r in model_rows}
        if mod!='MACAW':
            upstream = getattr(a,mod.lower())
            original_tree = tree(upstream,pin)
            content = archive_paths(upstream,pin,wanted)
            png_entries = [(p,sha) for p,sha in original_tree.items() if p.endswith('.png')]
        else:
            assert hash_data(a.macaw.read_bytes())==pin
            with zipfile.ZipFile(a.macaw) as z:
                content = {path:z.read(path) for path in wanted}
                png_entries = [(p, None) for p in z.namelist() if p.endswith('.png')]
        for path,sha in png_entries:
            marker = f'assets/{NS[mod]}/textures/'
            if marker not in path:
                continue
            rid = NS[mod]+':'+path.split(marker,1)[1].removesuffix('.png')
            local_png.setdefault(rid,[]).append((mod,path,sha))
        for r in model_rows:
            doc = b_models[mod,r['path']]
            raw = content[r['path']]
            assert (r['model_id'],r['source_hash'],len(raw)) == (
                doc['asset_id'],doc['sha'],int(doc['bytes']))
            assert hash_data(raw,mod!='MACAW')==r['source_hash']
            model_source_rows.append((r['model_key'],mod,r['model_id'],r['path'],r['source_hash'],
                                      'FIXED_MOD_JSON',optional(r['entry']),r['geometry_status']))
            bodies[r['model_key']] = json.loads(raw)
    put('INSERT INTO model VALUES (?,?,?,?,?,?,?,?)',model_source_rows)

    vanilla = {}
    for version,sha in MC_CLIENT_SHA1.items():
        path = a.vanilla/(version+'.jar')
        assert hashlib.sha1(path.read_bytes()).hexdigest()==sha
        vanilla[version] = zipfile.ZipFile(path)
    ext_choices = {(r['model_id'],r['model_path'],r['model_source_sha']) for r in options
                   if r['reference_status']=='VANILLA_JAR'}
    external_model = {}
    aux_rows = []
    for key,r in c_parents.items():
        aux_rows.append((key,r['minecraft'],r['model_id'],r['path'],r['sha256']))
    for i,(rid,path,sha) in enumerate(sorted(ext_choices),1):
        external_model[rid] = f'DV{i}'
        aux_rows.append((f'DV{i}','1.21.1',rid,path,sha))
    for key,ver,rid,path,sha in aux_rows:
        raw = vanilla[ver].read(path)
        assert hash_data(raw)==sha
        bodies[key] = json.loads(raw)
        db.execute('INSERT INTO model VALUES (?,?,?,?,?,?,?,?)',(key,'MC'+ver,rid,path,sha,'VANILLA_EVIDENCE',None,'AUXILIARY'))
    put('INSERT INTO geometry VALUES (?,?,?,?,?,?)',[(key,optional(r['geometry_source_key']),
        chains[key]['terminal_status'],chains[key]['terminal_ref'],int(r['effective_elements']),int(r['effective_faces']))
        for key,r in catalog.items()])
    put('INSERT INTO lineage VALUES (?,?,?)',[(key,i,node) for key,line in chains.items()
        for i,node in enumerate(line['chain_keys'].split('|'))])
    put('INSERT INTO element VALUES (?,?,?,?,?,?,?,?,?,?,?)',[
        (r['source_key'],int(r['element_index']),r['source_from'],r['source_to'],r['pivot'],r['axis'],
         float(r['angle']),int(r['rescale']),r['rotated_bbox'],c_parts[r['source_key'],r['element_index']]['candidate_part'],
         c_parts[r['source_key'],r['element_index']]['evidence']) for r in geometry_rows])
    put('INSERT INTO face VALUES (?,?,?,?,?,?,?,?,?)',[(r['source_key'],int(r['element_index']),r['direction'],
         r['texture_slot'],r['uv'],int(r['uv_declared']),int(r['uv_rotation']),r['cullface'],r['tintindex']) for r in face_rows])

    slot_rows, texture_keys, referenced_chairs = [], set(prior), set()
    face_frequency = {k:Counter(r['texture_slot'] for r in val) for k,val in group(face_rows,'source_key').items()}
    chair_models = {r['model_ref']:r for r in chair_rows}
    for key,r in catalog.items():
        bindings = {}
        for node in reversed(chains[key]['chain_keys'].split('|')):
            bindings.update(bodies[node].get('textures',{}))
        frequencies = face_frequency.get(r['geometry_source_key'],Counter())
        found = Counter()
        face_resources = set()
        for slot in sorted(set(frequencies)|{'#'+t for t in bindings}):
            status,rid = face_slot(slot,bindings)
            tk = (rid,r['minecraft']) if rid else None
            instance_count = frequencies[slot]
            if tk:
                texture_keys.add(tk)
                if instance_count:
                    face_resources.add(rid)
            found[status] += instance_count
            slot_rows.append((key,slot,tk,status,instance_count))
        assert (found['RESOURCE_ID'],found['SLOT_UNBOUND'],found['SLOT_CYCLE']) == (
            int(r['faces_resolved']),int(r['faces_unbound']),int(r['faces_slot_cycle']))
        assert face_resources == set(filter(None,r['texture_resource_ids'].split('|')))
        if r['mod']=='AF' and r['model_id'] in chair_models:
            old = chair_models[r['model_id']]
            assert r['source_hash']==old['git_blob_sha'] and len(frequencies)==3
            assert face_resources == {old[c] for c in ('texture_bottom','texture_seat','texture_back')}
            referenced_chairs.add(r['model_id'])
    assert len(referenced_chairs)==39

    ids, texture_data, historical = {}, {}, []
    with zipfile.ZipFile(a.macaw) as mac:
        for i,(rid,mc) in enumerate(sorted(texture_keys),1):
            tk = rid,mc
            ids[tk] = i
            candidates = local_png.get(rid,[])
            source = path = sha = None
            if len(candidates)==1:
                source,path,sha = candidates[0]
                if source=='MACAW':
                    sha = hash_data(mac.read(path))
                status = 'PINNED_MOD_PNG'
            elif candidates:
                status = 'AMBIGUOUS_RESOURCE_ROOT'
            elif rid.startswith('minecraft:'):
                candidate = 'assets/minecraft/textures/'+rid.split(':',1)[1]+'.png'
                z = vanilla[mc]
                if candidate in z.NameToInfo:
                    source,path,sha = 'MC'+mc,candidate,hash_data(z.read(candidate))
                    status = 'PINNED_VANILLA_PNG'
                else:
                    status = 'MISSING_VANILLA_PNG'
            else:
                status = 'MISSING_MOD_PNG' if rid.split(':')[0] in NS.values() else 'EXTERNAL_NAMESPACE'
            data = (i,rid,mc,source,status,path,sha)
            texture_data[tk] = data
            if tk in prior:
                record = prior[tk]
                assert status=='PINNED_MOD_PNG' and sha==record[-1], (tk,sha,record)
                historical.append((i,*record))
    put('INSERT INTO texture VALUES (?,?,?,?,?,?,?)',texture_data.values())
    put('INSERT INTO prior_texture VALUES (?,?,?,?,?)',historical)
    put('INSERT INTO model_slot VALUES (?,?,?,?,?)',[(key,slot,ids.get(tk),status,n)
        for key,slot,tk,status,n in slot_rows])

    state_keys = {}
    for i,r in enumerate(selected_states,1):
        mod,sid = r['mod'],r['state_id']
        state_keys[mod,sid] = i
        assert (sid,r['source_sha']) == (b_states[mod,r['path']]['asset_id'],b_states[mod,r['path']]['sha'])
        c = code_by_state[mod,sid]
        db.execute('INSERT INTO state VALUES (?,?,?,?,?,?,?,?)',(i,mod,sid,r['path'],r['source_sha'],r['kind'],
                   optional(c['evidence_id']),c['classification']))
    assert len(state_keys)==len(b_states)==1158
    put('INSERT INTO rule VALUES (?,?,?,?,?)',[(state_keys[r['mod'],r['state_id']],int(r['rule_index']),
        r['source_selector'],r['condition'],r['apply_form']) for r in rules])
    put('INSERT INTO option VALUES (?,?,?,?,?,?,?,?,?,?,?)',[(state_keys[r['mod'],r['state_id']],int(r['rule_index']),
        int(r['option_index']),optional(r['model_key']) or external_model.get(r['model_id']),r['reference_status'],
        r['model_id'] if r['reference_status']=='UNRESOLVED_MODEL_REF' else None,int(r['x']),int(r['y']),
        int(r['uvlock']=='true'),int(r['weight']),r['explicit_fields']) for r in options])
    sample_keys = {r['case']:state_keys[r['mod'],r['state_id']] for r in e_cases}
    put('INSERT INTO sample VALUES (?,?,?,?,?,?,?,?)',[(r['case'],r['category'],sample_keys[r['case']],r['state'],
        r['bbox'],float(r['front_fill_pct']),float(r['side_fill_pct']),float(r['top_fill_pct'])) for r in e_cases])
    put('INSERT INTO sample_option VALUES (?,?,?,?)',[(r['case'],sample_keys[r['case']],int(r['rule_index']),
        int(r['option_index'])) for r in e_options])
    selected_provider = {(r['case'],r['rule_index']):r['provider_key'] for r in e_options}
    put('INSERT INTO sample_part VALUES (?,?,?,?,?,?)',[(r['case'],int(r['rule_index']),
        selected_provider[r['case'],r['rule_index']],int(i),r['part_candidate'],r['basis'])
        for r in e_groups for i in r['element_indices'].split('|')])
    put('INSERT INTO exception VALUES (?,?,?,?)',[
        ('C',r['model_key'],r['status'],r['detail']) for r in read('C','C_EXCEPTIONS.csv.gz')]+[
        ('D',f"{r['state_id']}/{r['rule_index']}/{r['option_index']}",r['category'],r['detail'])
        for r in read('D','D_EXCEPTIONS.csv')])

    db.commit()
    tables = [r[0] for r in db.execute("SELECT name FROM sqlite_schema WHERE type='table' ORDER BY name")]
    counts = {t:db.execute(f'SELECT count(*) FROM {t}').fetchone()[0] for t in tables}
    assert counts['option']==counts['rule']==78456 and counts['sample_option']==52
    assert list(db.execute('PRAGMA integrity_check')) == [('ok',)]
    assert not list(db.execute('PRAGMA foreign_key_check'))
    assert db.execute('SELECT count(*) FROM effective_face_texture').fetchone()[0]==sum(
        int(r['effective_faces']) for r in catalog.values())==592312
    used, declared_only = Counter(), Counter()
    for _,_,tk,_,count in slot_rows:
        if tk:
            used[tk] += count
            declared_only[tk] += count==0
    handoff_rows = []
    for tk,record in texture_data.items():
        i,rid,mc,source,status,path,sha = record
        old = prior.get(tk)
        scope = 'V24_CHAIR' if mc=='1.21.1' and rid in chair_set else ''
        disposition = ('PRIOR_RGBA_SHA_MATCH' if old else
                       'SOURCE_EXCEPTION' if 'PINNED' not in status else
                       'PNG_UV_CANDIDATE' if used[tk] else 'DECLARED_SLOT_ONLY')
        handoff_rows.append((i,rid,mc,source or '',status,path or '',sha or '',used[tk],declared_only[tk],scope,disposition,
                    old[0] if old else '',old[1] if old else '',old[2] if old else '',
                    'GIT_BLOB_SHA1' if source in ('AF','HC') else 'SHA256' if sha else ''))
    chair_overlap = chair_set & {rid for rid,mc in prior if mc=='1.21.1'}
    assert all(texture_data[rid,'1.21.1'][4]=='PINNED_MOD_PNG' for rid in chair_set)
    best = [(r['case']+'/'+r['rule_index']+'/'+r['option_index'],r['case'],r['category'],r['mod'],
             r['state_id'],r['rule_index'],r['option_index'],r['model_key'],r['model_sha'],
             r['provider_key'],r['geometry_sha'],r['x'],r['y'],'E_FIXED_STATIC_SAMPLE',
             r['state_sha'],r['provider_sha'],r['uvlock'],r['texture_resource_ids'],r['d_code_evidence']) for r in e_options]
    source_index = [(key,mod,rid,path,sha,PINS[mod][0],PINS[mod][1],VERSIONS[mod],
                     'GIT_BLOB_SHA1' if mod!='MACAW' else 'SHA256',entry or '',grade)
                    for key,mod,rid,path,sha,_,entry,grade in model_source_rows]
    write_csv(a.out/'MODEL_SOURCE_INDEX.csv.gz','model_key mod resource_id source_path source_sha source_pin minecraft mod_version hash_kind entry_id evidence_grade',source_index)
    write_csv(a.out/'1-3_TEXTURE_UV_HANDOFF.csv','texture_id resource_id minecraft source_id texture_status path source_sha face_instances non_face_slot_count priority disposition previous_ledger previous_ledger_blob_sha previous_ledger_line source_hash_kind',handoff_rows)
    write_csv(a.out/'F_PRIOR_RGBA_LEDGER.csv','mod evidence_unit ledger_path ledger_blob_sha rows_recounted',prior_summary)
    write_csv(a.out/'F_1-5_COMPARISON_CANDIDATES.csv','candidate_id sample_id category mod state_id rule_index option_index model_key model_sha provider_key geometry_sha x y evidence_grade state_sha provider_sha uvlock texture_resource_ids d_code_evidence',best)
    write_csv(a.out/'F_V24_CHAIR_PNG.csv','resource_id pinned_path source_sha prior_rgba_status prior_ledger disposition',
              [(rid,texture_data[rid,'1.21.1'][5],texture_data[rid,'1.21.1'][6],
                'SHA_MATCH' if rid in chair_overlap else 'NONE_IN_151',
                prior[rid,'1.21.1'][0] if rid in chair_overlap else '',
                'REFERENCE_PRIOR_RGBA' if rid in chair_overlap else 'QUEUE_1_4')
               for rid in sorted(chair_set)])
    result = dict(status='PASS',base_commit=BASE,counts=counts,fixed_mod_models=len(catalog),
                  model_original_sha_rechecked=len(catalog),effective_face_instances=592312,
                  v24_chair_models=len(referenced_chairs),v24_png_paths=len(chair_set),v24_prior_covered=len(chair_overlap),
                  v24_queued_for_1_4=len(chair_set-chair_overlap),historical_png=len(historical),historical_face_rgba=4113,
                  texture_resource_status=dict(Counter(r[4] for r in texture_data.values())),
                  texture_disposition=dict(Counter(r[10] for r in handoff_rows)),deduplicated_resource_version_keys=len(texture_keys),
                  new_png_pixel_checks=0,new_face_rgba_checks=0,foreign_key_errors=0,integrity_check='ok',input_blob_shas=manifest)
    db.execute('VACUUM')
    db.close()
    with lzma.open(a.out/'furniture_research.sqlite.xz','wb',preset=6) as compressed:
        compressed.write(db_path.read_bytes())
    db_path.unlink()
    (a.out/'DB_VALIDATION.json').write_text(json.dumps(result,indent=2)+'\n')
    for archive in vanilla.values():
        archive.close()
    print(json.dumps({k:v for k,v in result.items() if k!='input_blob_shas'},indent=2))


if __name__ == '__main__':
    main()
