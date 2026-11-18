"""배포 SQLite와 원장을 열어 B~E 키 집합, 선행 증거와 인계 후보를 대조한다."""
import argparse
from collections import Counter
import csv
import gzip
import hashlib
import json
import lzma
from pathlib import Path
import sqlite3


def read(path):
    opener = gzip.open if path.suffix=='.gz' else open
    with opener(path,'rt',encoding='utf-8-sig',newline='') as stream:
        return list(csv.DictReader(stream))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for name in ('b','c','d','e'):
        p.add_argument('--'+name,type=Path,required=True)
    p.add_argument('--out',type=Path,default=Path(__file__).resolve().parent)
    a = p.parse_args()
    out = a.out
    compressed = (out/'furniture_research.sqlite.xz').read_bytes()
    db = sqlite3.connect(':memory:')
    db.deserialize(lzma.decompress(compressed))
    assert db.execute('PRAGMA integrity_check').fetchall()==[('ok',)]
    assert db.execute('PRAGMA foreign_key_check').fetchall()==[]
    assert db.execute('PRAGMA quick_check').fetchall()==[('ok',)]

    b_models = set()
    for mod in ('AF','HC','MACAW'):
        for r in read(a.b/f'B_{mod}_SOURCE_BODIES.csv.gz'):
            if r['family']=='models':
                b_models.add((mod,r['asset_id'],r['path'],r['sha']))
    f_models = {(r['mod'],r['resource_id'],r['source_path'],r['source_sha'])
                for r in read(out/'MODEL_SOURCE_INDEX.csv.gz')}
    db_models = set(db.execute("SELECT source_id,resource_id,path,sha FROM model WHERE kind='FIXED_MOD_JSON'"))
    assert b_models==f_models==db_models and len(db_models)==16572

    index_metadata = {(r['model_key'],r['source_pin'],r['minecraft'],r['mod_version'],
                       r['hash_kind'],r['entry_id'],r['evidence_grade'])
                      for r in read(out/'MODEL_SOURCE_INDEX.csv.gz')}
    assert index_metadata == set(db.execute("""
        SELECT model_key, pin, minecraft, version, asset_hash_kind, COALESCE(entry_id,''), static_grade
        FROM model JOIN source ON source_id=source.id WHERE kind='FIXED_MOD_JSON'
    """))
    assert db.execute("SELECT count(*) FROM model WHERE kind='VANILLA_EVIDENCE'").fetchone()==(7,)

    model_geometry = {
        (r['model_key'],r['geometry_source_key'] or None,int(r['effective_elements']),int(r['effective_faces']))
        for r in read(a.c/'mod_furniture_catalog.csv.gz')}
    assert model_geometry == set(db.execute('SELECT model_key,provider_key,element_instances,face_instances FROM geometry'))
    assert not db.execute('''
        SELECT g.model_key FROM geometry g LEFT JOIN model_slot s USING(model_key)
        GROUP BY g.model_key HAVING g.face_instances != COALESCE(SUM(s.face_count),0)
    ''').fetchall()
    assert db.execute('SELECT count(*) FROM effective_face_texture').fetchone()==(592312,)

    db_state = set(db.execute('SELECT source_id,state_id,path,sha FROM state'))
    assert db_state=={(r['mod'],r['state_id'],r['path'],r['source_sha'])
                      for r in read(a.d/'D_BLOCKSTATES.csv')}
    db_rules = set(db.execute('''
        SELECT s.source_id,s.state_id,r.rule_index,r.selector,r.condition,r.form
        FROM state s JOIN rule r ON r.state_id=s.id
    '''))
    assert db_rules=={(r['mod'],r['state_id'],int(r['rule_index']),r['source_selector'],r['condition'],r['apply_form'])
                      for r in read(a.d/'D_STATE_RULES.csv.gz')}
    db_opts = set(db.execute('''
        SELECT s.source_id,s.state_id,o.rule_index,o.option_index,coalesce(m.resource_id,o.unresolved_target),
               o.target_status,o.x,o.y,o.uvlock,o.weight,o.explicit_fields
        FROM state s JOIN option o ON o.state_id=s.id LEFT JOIN model m ON m.model_key=o.model_key
    '''))
    assert db_opts=={(r['mod'],r['state_id'],int(r['rule_index']),int(r['option_index']),r['model_id'],
                     r['reference_status'],int(r['x']),int(r['y']),int(r['uvlock']=='true'),int(r['weight']),r['explicit_fields'])
                     for r in read(a.d/'MODEL_STATE_ASSEMBLY.csv.gz')}
    assert Counter(row[5] for row in db_opts)=={'LOCAL':78420,'VANILLA_JAR':32,'UNRESOLVED_MODEL_REF':4}
    assert not db.execute('''
        SELECT s.id FROM sample s JOIN sample_option o ON s.id=o.sample_id WHERE o.state_id!=s.state_id
    ''').fetchall()
    db_sample_opts = set(db.execute('''
        SELECT o.sample_id,o.rule_index,o.option_index,m.model_key
        FROM sample_option o JOIN option m USING(state_id,rule_index,option_index)
    '''))
    e_sample_opts = {(r['case'],int(r['rule_index']),int(r['option_index']),r['model_key'])
                     for r in read(a.e/'CATEGORY_EVIDENCE.csv')}
    candidates = read(out/'F_1-5_COMPARISON_CANDIDATES.csv')
    assert len({r['candidate_id'] for r in candidates})==len(candidates)==52
    assert db_sample_opts==e_sample_opts=={(r['sample_id'],int(r['rule_index']),int(r['option_index']),r['model_key'])
                                         for r in candidates}

    evidence_fields = ('category','mod','state_id','model_sha','provider_key','geometry_sha',
                       'x','y','state_sha','provider_sha','uvlock','texture_resource_ids','d_code_evidence')
    assert {r['candidate_id']:tuple(r[k] for k in evidence_fields) for r in candidates} == {
        '/'.join((r['case'],r['rule_index'],r['option_index'])):tuple(r[k] for k in evidence_fields)
        for r in read(a.e/'CATEGORY_EVIDENCE.csv')
    }
    assert db.execute('SELECT count(DISTINCT category) FROM sample').fetchone()==(9,)

    t = read(out/'1-3_TEXTURE_UV_HANDOFF.csv')
    assert len(t)==len({(r['resource_id'],r['minecraft']) for r in t})==2256
    projected = {tuple(r[k] for k in ('resource_id','minecraft','texture_status','path','source_sha')) for r in t}
    assert projected==set(db.execute("SELECT resource_id,minecraft,texture_status,coalesce(path,''),coalesce(sha,'') FROM texture"))
    assert db.execute('SELECT count(*) FROM prior_texture p JOIN texture t ON t.id=p.texture_id WHERE p.prior_sha=t.sha').fetchone()==(175,)
    chair = read(out/'F_V24_CHAIR_PNG.csv')
    assert Counter(r['disposition'] for r in chair)=={'QUEUE_1_4':19,'REFERENCE_PRIOR_RGBA':5}
    priority = {r['resource_id']:r for r in t if r['priority']=='V24_CHAIR'}
    assert len(priority)==24
    for row in chair:
        assert row['source_sha']==priority[row['resource_id']]['source_sha']
        assert priority[row['resource_id']]['disposition']==(
            'PNG_UV_CANDIDATE' if row['disposition']=='QUEUE_1_4' else 'PRIOR_RGBA_SHA_MATCH')
    prior = read(out/'F_PRIOR_RGBA_LEDGER.csv')
    distribution = Counter()
    for r in prior:
        distribution[r['mod'],r['evidence_unit']] += int(r['rows_recounted'])
    assert distribution=={('AF','PNG'):151,('HC','PNG'):24,('AF','FACE_RGBA'):3329,('HC','FACE_RGBA'):784}
    result = dict(status='PASS',archive_sha256=hashlib.sha256(compressed).hexdigest(),mod_models=len(db_models),
                  blockstates=len(db_state),rules=len(db_rules),options=len(db_opts),comparison_candidates=len(db_sample_opts),
                  effective_faces=592312,texture_records=len(t),chair_prior=5,chair_candidates=19,errors=[])
    (out/'F_INDEPENDENT_AUDIT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
