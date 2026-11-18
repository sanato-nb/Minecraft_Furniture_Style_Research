"""Audit the delivered database independently against CSVs and the pinned Git tree."""
from collections import Counter
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
KEY=('case','rule_index','option_index','element_index','direction')


def rows(path):
    opener=lzma.open if path.suffix=='.xz' else open
    with opener(path,'rt',encoding='utf-8',newline='') as f:
        return list(csv.DictReader(f))


def key(r,fields):
    return tuple(r[f] for f in fields)


def main():
    with sqlite3.connect(':memory:') as db:
        db.deserialize(lzma.decompress((HERE/'comparison.sqlite.xz').read_bytes()))
        assert db.execute('PRAGMA integrity_check').fetchall()==[('ok',)]
        assert not db.execute('PRAGMA foreign_key_check').fetchall()
        assert db.execute('PRAGMA user_version').fetchone()==(1,)
        inputs=db.execute('SELECT path,baseline_commit,git_blob_sha1,sha256,bytes FROM source_artifact').fetchall()
        for path,commit,blob,sha,size in inputs:
            body=subprocess.check_output(['git','-C',ROOT,'show',commit+':'+path])
            assert len(body)==size and hashlib.sha256(body).hexdigest()==sha
            assert hashlib.sha1(f'blob {len(body)}\0'.encode()+body).hexdigest()==blob

        source_rows=db.execute('''
            SELECT s.case_id,s.rule_index,s.option_index,s.role,a.path,h.digest
            FROM application_source s JOIN asset a USING(asset_id) JOIN asset_hash h USING(asset_id)
        ''').fetchall()
        source_index={}
        for case,rule,option,role,path,digest in source_rows:
            source_index.setdefault((case,str(rule),str(option),role),set()).add((path,digest))
        expected=rows(PHASE/'B/APPLICATIONS.csv')
        for r in expected:
            for role in ('state','model','provider'):
                path=r[role+'_path']
                if path:
                    assert (path,r[role+'_sha']) in source_index.pop((*key(r,KEY[:3]),role))
        assert not source_index and len(expected)==74
        assert db.execute('''
            SELECT a.source_scope,a.minecraft,h.algorithm
            FROM application_source s JOIN asset a USING(asset_id) JOIN asset_hash h USING(asset_id)
            WHERE s.case_id='S22' AND s.role='provider'
        ''').fetchall()==[('VANILLA','1.21.1','SHA256')]

        matched={}
        for record in db.execute('''
            SELECT f.case_id,f.rule_index,f.option_index,f.element_index,f.direction,a.path,
                   h.algorithm,h.digest,f.uv,f.status,f.pixel_box,f.rgba_sha256,f.pixels,f.alpha_zero,f.alpha_partial,
                   a.minecraft,c.minecraft
            FROM face f JOIN asset a ON a.asset_id=f.png_asset_id JOIN asset_hash h USING(asset_id)
            JOIN study_case c ON c.case_id=f.case_id
        '''):
            *row,png_version,case_version=record
            assert png_version==case_version
            k=tuple(map(str,row[:5]))
            matched.setdefault(k,set()).add(tuple('' if v is None else str(v) for v in row[5:]))
        faces=rows(PHASE/'B/FACES.csv.xz')
        fields=('png_path','png_hash_kind','png_sha','uv','status','pixel_box','rgba_sha256','pixels','alpha_zero','alpha_partial')
        for r in faces:
            assert key(r,fields) in matched.pop(key(r,KEY))
        assert len(faces)==1844 and not matched

        frame_db={tuple(map(str,r[:6])):r[6:] for r in db.execute(
            'SELECT case_id,rule_index,option_index,element_index,direction,frame,rgba_sha256,pixels FROM face_frame')}
        frames=rows(PHASE/'B/ANIMATION_FRAMES.csv.xz')
        for r in frames:
            assert frame_db.pop(key(r,KEY+('frame',)))==(r['rgba_sha256'],int(r['pixels']))
        assert len(frames)==109 and not frame_db

        handoff=rows(HERE/'PHASE2_HANDOFF.csv')
        findings={r['finding_id']:r for r in rows(PHASE/'C/CROSS_CATEGORY_FINDINGS.csv')}
        for r in handoff:
            ident=r['finding_id']
            old=findings.pop(ident)
            assert all(r[k]==v for k,v in old.items())
            assert db.execute('SELECT disposition,review_condition FROM phase2_handoff WHERE finding_id=?',(ident,)).fetchone()==(
                r['disposition'],r['review_condition'])
            assert set(r['cases'].split('|'))=={v for v, in
                db.execute('SELECT case_id FROM finding_case WHERE finding_id=?',(ident,))}
            assert set(filter(None,r['runtime_checks'].split('|')))=={v for v, in
                db.execute('SELECT test_id FROM handoff_runtime WHERE finding_id=?',(ident,))}
        assert not findings and len(handoff)==21
        dispositions=Counter(r['disposition'] for r in handoff)
        assert dispositions=={'CANDIDATE_REQUIRES_REVIEW':14,'SCOPE_LIMIT_ONLY':7}
        runtime=db.execute('SELECT status,count(*) FROM runtime_check GROUP BY status').fetchall()
        assert runtime==[('NOT_RUN',10)]
        pending=db.execute('SELECT gate_id FROM phase_gate WHERE status=\'PENDING\' ORDER BY gate_id').fetchall()
        assert pending==[('1-2_OVERALL',),('1-4-F',),('1-5-F',)]
    print(json.dumps(dict(status='PASS',input_artifacts_verified=len(inputs),applications_reconciled=len(expected),
                          face_rows_reconciled=len(faces),frame_rows_reconciled=len(frames),
                          handoff_dispositions=dispositions,confirmed_runtime_checks=0,
                          pending_gates=[r[0] for r in pending]),indent=2,sort_keys=True))


if __name__=='__main__':
    main()
