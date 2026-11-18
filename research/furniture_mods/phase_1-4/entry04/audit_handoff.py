"""Independently cross-check the 1-4-E database against the frozen 1-3 and C/D evidence."""
from collections import Counter
import csv
import hashlib
import json
import lzma
from pathlib import Path
import sqlite3

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
PHASE=HERE.parents[1]/'phase_1-3'


def read(path):
    loader=lzma.open if path.suffix=='.xz' else open
    with loader(path,'rt',encoding='utf-8',newline='') as stream:
        return list(csv.DictReader(stream))


def main():
    with sqlite3.connect(':memory:') as db:
        db.deserialize(lzma.decompress((HERE/'research_texture_uv.sqlite.xz').read_bytes()))
        assert db.execute('PRAGMA integrity_check').fetchall()==[('ok',)]
        assert not db.execute('PRAGMA foreign_key_check').fetchall()
        artifacts=db.execute('SELECT path,sha256 FROM input_artifact').fetchall()
        for path,sha in artifacts:
            assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==sha,path
        db.execute("ATTACH DATABASE ':memory:' AS f")
        db.deserialize(lzma.decompress((PHASE/'F/furniture_research.sqlite.xz').read_bytes()),name='f')
        def compare(left,right):
            assert not db.execute(left+' EXCEPT '+right).fetchall()
            assert not db.execute(right+' EXCEPT '+left).fetchall()
        compare('SELECT id,resource_id,minecraft,coalesce(path,\'\'),coalesce(sha,\'\') FROM main.texture',
                'SELECT id,resource_id,minecraft,coalesce(path,\'\'),coalesce(sha,\'\') FROM f.texture')
        compare('SELECT texture_id,model_key,slot,face_instances FROM exception_slot',
                'SELECT texture_id,model_key,slot,face_count FROM f.model_slot JOIN texture_exception USING(texture_id)')
        assert not db.execute('''
            SELECT 1 FROM texture_exception e JOIN main.texture t ON t.id=e.texture_id
            WHERE t.disposition='SOURCE_EXCEPTION' AND EXISTS (
                SELECT 1 FROM exception_slot s JOIN f.option o USING(model_key) WHERE s.texture_id=e.texture_id
            )
        ''').fetchall()
        compare('SELECT case_id,rule_index,option_index,model_key,x,y,uvlock FROM comparison_application',
                'SELECT sample_id,rule_index,option_index,model_key,x,y,uvlock FROM f.sample_option JOIN f.option USING(state_id,rule_index,option_index)')
        compare('SELECT case_id,rule_index,option_index,element_index,direction,texture_id FROM comparison_face',
                'SELECT s.sample_id,s.rule_index,s.option_index,f.element_index,f.direction,f.texture_id '
                'FROM f.sample_option s JOIN f.option o USING(state_id,rule_index,option_index) '
                'JOIN f.effective_face_texture f ON f.model_key=o.model_key')
        old_rows=read(HERE/'PRIOR_FACE_LINKS.csv.xz')
        assert len(old_rows)==4113
        match_counts=Counter(r['finding'] for r in old_rows)
        assert match_counts==dict(db.execute('SELECT finding,count(*) FROM prior_face GROUP BY finding'))
        c_status=Counter(json.loads((HERE.parent/'entry02/INDEPENDENT_AUDIT.json').read_bytes())['status_counts'])
        summed=db.execute('SELECT sum(static_faces),sum(animated_faces),sum(zero_uv_faces),sum(outside_uv_faces) FROM texture_uv_counts').fetchone()
        assert summed==tuple(c_status[k] for k in ('STATIC_RECT','ANIMATED_FRAME_RECTS','ZERO_UV_AREA','OUTSIDE_TEXTURE_UV'))
        assert db.execute('SELECT sum(face_instances) FROM texture_exception').fetchone()[0]==c_status['MISSING_PINNED_PNG']
        counts={k:db.execute(f'SELECT count(*) FROM {k}').fetchone()[0] for k in (
            'texture','texture_uv_counts','texture_exception','exception_slot','alternate_asset',
            'prior_face','comparison_application','comparison_face')}
        assert counts==dict(texture=2256,texture_uv_counts=2171,texture_exception=85,exception_slot=169,
                            alternate_asset=16,prior_face=4113,comparison_application=52,comparison_face=1610)
    print(json.dumps({'status':'PASS','source_artifact_hashes':len(artifacts),'table_rows':counts,
                      'prior_face_findings':match_counts,'foreign_key_errors':0},indent=2,sort_keys=True))


if __name__=='__main__':
    main()
