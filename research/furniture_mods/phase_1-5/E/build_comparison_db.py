"""Build the normalized comparison database and phase-2 evidence handoff."""
import argparse
import csv
import hashlib
import json
import lzma
from pathlib import Path
import sqlite3
import subprocess

HERE=Path(__file__).resolve().parent
PHASE=HERE.parent
ROOT=HERE.parents[3]
P13_DB=PHASE.parent/'phase_1-3/F/furniture_research.sqlite.xz'
BASELINE='85f2336a59c09b5507b9cca31f8d5c030795a608'
TABLES={
    'study_case':'B/CASES.csv',
    'application':'B/APPLICATIONS.csv',
    'element':'B/ELEMENTS.csv',
    'face':'B/FACES.csv.xz',
    'face_frame':'B/ANIMATION_FRAMES.csv.xz',
    'finding':'C/CROSS_CATEGORY_FINDINGS.csv',
    'parent_exception':'D/PARENT_EXCEPTIONS.csv',
    'state_exception':'D/STATE_EXCEPTIONS.csv',
    'texture_exception':'D/TEXTURE_EXPOSURE.csv',
    'runtime_check':'D/RUNTIME_CHECKS.csv',
}
EXTRA=(
    'A/MOD_CASE_SCOPE.csv','A/VANILLA_CONTROL_OPTIONS.csv','A/VANILLA_SOURCE_PROVENANCE.csv',
    'B/VANILLA_MCMETA.csv','C/CATEGORY_COVERAGE.csv','D/STATIC_COUNTEREXAMPLES.json',
)
EXPECTED={
    'study_case':62,'application':74,'application_source':221,'element':390,'face':1844,'face_frame':109,
    'category':9,'finding':21,'parent_exception':48,'state_exception':6,'texture_exception':85,
    'runtime_check':10,'phase2_handoff':21,'phase_gate':3,'source_artifact':18,
}


def csv_rows(path):
    opener=lzma.open if path.suffix=='.xz' else open
    with opener(path,'rt',encoding='utf-8',newline='') as f:
        return list(csv.DictReader(f))


def write_csv(path,records):
    with path.open('w',encoding='utf-8',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(records[0]),lineterminator='\n')
        writer.writeheader()
        writer.writerows(records)


def git_blob(body):
    return hashlib.sha1(f'blob {len(body)}\0'.encode()+body).hexdigest()


def record_sources(db):
    sources=[PHASE/p for p in (*TABLES.values(),*EXTRA)]+[ROOT/'handoff/STATE.json',P13_DB]
    manifest={}
    for path in sorted(sources):
        name=path.relative_to(ROOT).as_posix()
        body=subprocess.check_output(['git','-C',ROOT,'show',BASELINE+':'+name])
        if path.name!='STATE.json':
            assert body==path.read_bytes(),name
        manifest[name]=body
        db.execute('INSERT INTO source_artifact VALUES (?,?,?,?,?)',
                   (name,BASELINE,git_blob(body),hashlib.sha256(body).hexdigest(),len(body)))
    return json.loads(manifest['handoff/STATE.json'])


def insert_rows(db,table,records):
    columns=db.execute(f'PRAGMA table_info({table})').fetchall()
    names=[col[1] for col in columns]
    def values(r):
        for _,name,kind,required,_,_ in columns:
            value=r[name if name!='case_id' or name in r else 'case']
            if kind=='INTEGER':
                yield int(value) if value not in ('',None) else None
            else:
                yield (None if value=='' else value) if not required and name=='case_id' else value
    db.executemany(f"INSERT INTO {table} ({','.join(names)}) VALUES ({','.join('?' for _ in names)})",
                   (tuple(values(r)) for r in records))


def main(out):
    out.mkdir(parents=True,exist_ok=True)
    raw={table:csv_rows(PHASE/path) for table,path in TABLES.items()}
    case_info={r['case']:r for r in raw['study_case']}
    versions={r['case']:r['mod_version'] for r in csv_rows(PHASE/'A/MOD_CASE_SCOPE.csv')}
    for row in raw['study_case']:
        row['mod_version']=versions.get(row['case'])
    with sqlite3.connect(':memory:') as sources:
        sources.deserialize(lzma.decompress(P13_DB.read_bytes()))
        model_origins={r[0]:r[1:] for r in sources.execute('''
            SELECT model_key,m.source_id,m.path,m.sha,s.asset_hash_kind,s.minecraft
            FROM model m JOIN source s ON s.id=m.source_id
        ''')}
    with sqlite3.connect(':memory:') as db:
        db.executescript((HERE/'schema.sql').read_text())
        state=record_sources(db)
        categories=sorted({t for r in raw['study_case'] for t in r['category'].split('|')})
        db.executemany('INSERT INTO category VALUES (?)',((c,) for c in categories))
        insert_rows(db,'study_case',raw['study_case'])
        db.executemany('INSERT INTO case_category VALUES (?,?)',
                       ((r['case'],c) for r in raw['study_case'] for c in r['category'].split('|')))

        assets={}
        hashes={}
        def asset(scope,version,path,kind,algorithm,sha):
            k=scope,version,path
            assert len(sha)=={'SHA256':64,'GIT_BLOB_SHA1':40}[algorithm] and int(sha,16)>=0
            if k not in assets:
                assets[k]=(db.execute('INSERT INTO asset(source_scope,minecraft,path,kind) VALUES (?,?,?,?)',
                                      (*k,kind)).lastrowid,kind)
            asset_id,prior_kind=assets[k]
            assert prior_kind==kind,(k,prior_kind,kind)
            hk=asset_id,algorithm
            if hk not in hashes:
                db.execute('INSERT INTO asset_hash VALUES (?,?,?)',(*hk,sha))
                hashes[hk]=sha
            assert hashes[hk]==sha,(k,algorithm)
            return asset_id

        for r in csv_rows(PHASE/'A/VANILLA_SOURCE_PROVENANCE.csv'):
            aid=asset('VANILLA','1.21.11',r['path'],r['kind'],'SHA256',r['sha256'])
            asset('VANILLA','1.21.11',r['path'],r['kind'],'GIT_BLOB_SHA1',r['git_blob_sha1'])
            db.executemany('INSERT INTO control_asset VALUES (?,?)',((c,aid) for c in r['controls'].split('|')))
        for r in csv_rows(PHASE/'B/VANILLA_MCMETA.csv'):
            asset('VANILLA','1.21.11',r['path'],'ANIMATION_METADATA','SHA256',r['sha256'])

        insert_rows(db,'application',raw['application'])
        for r in raw['application']:
            for role,kind in (('state','BLOCKSTATE'),('model','MODEL'),('provider','MODEL')):
                path=r[role+'_path']
                if not path:
                    assert r['case']=='V11' and role=='provider'
                    continue
                scope,version,algorithm=r['cohort'],r['minecraft'],r['model_hash_kind']
                if role in ('model','provider') and scope!='VANILLA':
                    scope,source_path,source_sha,algorithm,version=model_origins[r[role]]
                    assert (path,r[role+'_sha'])==(source_path,source_sha)
                    if scope.startswith('MC'):
                        scope='VANILLA'
                aid=asset(scope,version,path,kind,algorithm,r[role+'_sha'])
                db.execute('INSERT INTO application_source VALUES (?,?,?,?,?)',
                           (r['case'],r['rule_index'],r['option_index'],role,aid))
        for r in raw['face']:
            case=case_info[r['case']]
            scope='VANILLA' if r['resource_id'].startswith('minecraft:') else case['cohort']
            r['png_asset_id']=asset(scope,case['minecraft'],r['png_path'],'PNG',r['png_hash_kind'],r['png_sha'])
        for table in ('element','face','face_frame','finding','parent_exception','state_exception','texture_exception','runtime_check'):
            insert_rows(db,table,raw[table])
        for r in raw['finding']:
            db.executemany('INSERT INTO finding_case VALUES (?,?)',
                           ((r['finding_id'],c) for c in r['cases'].split('|')))
        for r in raw['runtime_check']:
            cases=r['cases_or_scope'].split('|')
            if all(c in case_info for c in cases):
                db.executemany('INSERT INTO runtime_case VALUES (?,?)',((r['test_id'],c) for c in cases))
            else:
                assert not set(cases)&case_info.keys() and r['test_id'] in ('R09','R10')
        for path,record in sorted(json.loads((PHASE/'D/STATIC_COUNTEREXAMPLES.json').read_bytes())['sources'].items()):
            scope=record['source']
            version='1.21.11' if scope=='MC1.21.11' else '1.21.1'
            kind=('CODE' if path.endswith('.java') else 'BLOCKSTATE' if '/blockstates/' in path else
                  'ITEM_DEFINITION' if '/items/' in path else 'MODEL')
            asset('VANILLA' if scope=='MC1.21.11' else scope,version,path,kind,record['hash_kind'],record['sha'])

        notes={r['finding_id']:r for r in csv_rows(HERE/'review_conditions.csv')}
        assert len(notes)==len(raw['finding']) and notes.keys()=={r['finding_id'] for r in raw['finding']}
        handoff=[]
        for r in raw['finding']:
            ident=r['finding_id']
            note=notes[ident]
            disposition=('SCOPE_LIMIT_ONLY' if r['classification']=='UNVERIFIED_OR_COUNTEREXAMPLE'
                         else 'CANDIDATE_REQUIRES_REVIEW')
            db.execute('INSERT INTO phase2_handoff VALUES (?,?,?)',(ident,disposition,note['review_condition']))
            if note['runtime_checks']:
                db.executemany('INSERT INTO handoff_runtime VALUES (?,?)',
                               ((ident,t) for t in note['runtime_checks'].split('|')))
            handoff.append(dict(**r,disposition=disposition,runtime_checks=note['runtime_checks'],
                                review_condition=note['review_condition']))

        assert state['phase_1_5_execution']['pending_parent_closure']==[
            '1-2 whole-stage separate review','1-4-F independent exit audit']
        assert not state['phase_1_4_execution']['phase_complete']
        db.executemany('INSERT INTO phase_gate VALUES (?,?,?,?)',(
            ('1-2_OVERALL','PENDING','docs/vanilla_models_1-2/1-2_STAGE_EXIT_SEPARATE_REVIEW.md','전체 종료 별도 심사'),
            ('1-4-F','PENDING','handoff/STATE.json','1-4 독립 종료 감사'),
            ('1-5-F','PENDING','docs/furniture_compare_1-5/1-5_DETAILED_EXECUTION_PLAN.md','1-5 자체 독립 종료 감사'),
        ))
        for table,total in EXPECTED.items():
            assert db.execute(f'SELECT count(*) FROM {table}').fetchone()==(total,),table
        assert db.execute('PRAGMA integrity_check').fetchall()==[('ok',)]
        assert not db.execute('PRAGMA foreign_key_check').fetchall()
        counts={table:db.execute(f'SELECT count(*) FROM {table}').fetchone()[0] for table, in
                db.execute("SELECT name FROM sqlite_schema WHERE type='table' ORDER BY name").fetchall()}
        db.commit()
        db.execute('VACUUM')
        (out/'comparison.sqlite.xz').write_bytes(lzma.compress(db.serialize()))
    write_csv(out/'PHASE2_HANDOFF.csv',handoff)
    encoded=json.dumps(dict(status='PASS',baseline=BASELINE,table_rows=counts,foreign_key_errors=0,
                            runtime_checks_executed=0),indent=2,sort_keys=True)+'\n'
    (out/'E_AUDIT.json').write_text(encoded,encoding='utf-8')
    print(encoded)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',required=True,type=Path)
    main(parser.parse_args().out)
