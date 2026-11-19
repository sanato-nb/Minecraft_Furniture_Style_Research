"""Independently reconcile the 1-4 exit evidence and verify pinned remote artifacts."""
from argparse import ArgumentParser
from collections import Counter
import csv
import gzip
from hashlib import sha1, sha256
import json
import lzma
from pathlib import Path
import sqlite3
import subprocess

HERE = Path(__file__).resolve().parent
PHASE = HERE.parent
ROOT = HERE.parents[3]
UPSTREAM = PHASE.parent/'phase_1-3/F'
BASE = 'c087fdaf2fffe078d168b04a791f557de35f38d8'
STAGES = {'A':'A','B':'entry01','C':'entry02','D':'entry03','E':'entry04',
          'C_followup':'C_followup','E_followup':'E_followup'}


def rows(path):
    opener = gzip.open if path.suffix == '.gz' else lzma.open if path.suffix == '.xz' else open
    with opener(path,'rt',encoding='utf-8-sig',newline='') as stream:
        yield from csv.DictReader(stream,delimiter='\t' if path.suffix=='.tsv' else ',')


def git(*args):
    return subprocess.check_output(['git','-C',str(ROOT),*args])


def remote_manifest(out):
    assert git('rev-parse',f'{BASE}^{{commit}}').decode().strip()==BASE
    relative = PHASE.relative_to(ROOT).as_posix()
    dependencies = [UPSTREAM.relative_to(ROOT).as_posix()+'/'+p for p in (
        '1-3_TEXTURE_UV_HANDOFF.csv','F_PRIOR_RGBA_LEDGER.csv','F_V24_CHAIR_PNG.csv',
        'F_1-5_COMPARISON_CANDIDATES.csv','furniture_research.sqlite.xz')]
    raw = git('ls-tree','-rlz',BASE,'--',relative,*dependencies)
    manifest = []
    for entry in raw.decode().strip('\0').split('\0'):
        record,path=entry.split('\t',1)
        _,kind,oid,size=record.split()
        assert kind=='blob'
        body=(ROOT/path).read_bytes()
        assert len(body)==int(size)
        assert sha1(f'blob {len(body)}\0'.encode()+body).hexdigest()==oid,path
        if path.endswith(('.csv','.csv.gz','.csv.xz','.tsv')):
            records=sum(1 for _ in rows(ROOT/path))
        else:
            records=''
        manifest.append((path,size,oid,sha256(body).hexdigest(),records))
    assert len(manifest)==75 and sum(r[0].startswith(relative+'/') for r in manifest)==70
    with (out/'REMOTE_INPUT_MANIFEST.csv').open('w',encoding='utf-8',newline='') as stream:
        writer=csv.writer(stream,lineterminator='\n')
        writer.writerow(('path','bytes','git_blob_sha1','sha256','data_rows'))
        writer.writerows(manifest)
    return len(manifest),sum(r[-1]!='' for r in manifest)


def replay_results(replay):
    counts={}
    for label,saved in STAGES.items():
        files=sorted((replay/label).iterdir())
        counts[label]=len(files)
        for p in files:
            reference=PHASE/saved/p.name
            assert reference.is_file() and p.read_bytes()==reference.read_bytes(),(label,p.name)
    assert counts=={'A':1,'B':5,'C':16,'D':8,'E':7,'C_followup':6,'E_followup':6},counts
    actual=replay/'ATLAS_REPLAY.tsv'
    assert actual.read_bytes()==(PHASE/'E_followup/ATLAS_RUNTIME.tsv').read_bytes()
    return counts,sha256(actual.read_bytes()).hexdigest()


def verify_png():
    queued={r['texture_id']:r for r in rows(UPSTREAM/'1-3_TEXTURE_UV_HANDOFF.csv')}
    assert len(queued)==2256 and len({(r['resource_id'],r['minecraft']) for r in queued.values()})==2256
    assert Counter(r['disposition'] for r in queued.values())=={
        'PNG_UV_CANDIDATE':1996,'PRIOR_RGBA_SHA_MATCH':175,'DECLARED_SLOT_ONLY':77,'SOURCE_EXCEPTION':8}
    count=Counter()
    pixels=0
    seen=set()
    for r in rows(PHASE/'entry01/1-4_PNG_PIXEL_LEDGER.csv.gz'):
        tid=r['texture_id']
        assert tid not in seen
        seen.add(tid)
        q=queued[tid]
        assert (r['computed_sha'],r['pinned_path'],r['hash_algorithm'])==(q['source_sha'],q['path'],q['source_hash_kind'])
        area=int(r['width'])*int(r['height'])
        assert area==sum(int(r[k]) for k in ('transparent','partial_alpha','opaque'))
        pixels+=area
        count[r['scope']]+=1
    assert len(seen)==2001 and count['NEW_CANDIDATE']==1996
    return len(queued),len(seen),pixels


def verify_uv(replay):
    face_keys=set()
    counts=Counter()
    model_faces=replay/'MODEL_FACES.csv.xz'
    for r in rows(model_faces):
        key=(r['model_key'],r['element_index'],r['direction'])
        assert key not in face_keys
        face_keys.add(key)
        counts[r['status']]+=1
    assert len(face_keys)==592312
    pixels=0
    region_frames=0
    for path in sorted((PHASE/'entry02').glob('UV_REGIONS_*.csv.xz')):
        for r in rows(path):
            u,v,x,y=map(int,r['pixel_box'].split('|'))
            area=(x-u)*(y-v)
            assert area==sum(int(r[k]) for k in ('transparent','partial_alpha','opaque'))
            pixels+=area
            region_frames+=1
    ordinary=counts['STATIC_RECT']+counts['ANIMATED_FRAME_RECTS']
    extra=json.loads((PHASE/'C_followup/SUMMARY.json').read_bytes())
    supplemented=extra['supplemental_source_support_faces']
    assert ordinary==511709 and supplemented==74260
    remainder=counts['SLOT_UNBOUND']+counts['MISSING_PINNED_PNG']+extra['pixel_support_counts']['NO_PINNED_SPRITE_INTERSECTION']
    assert remainder==6343 and ordinary+supplemented+remainder==len(face_keys)
    return dict(model_faces=len(face_keys),ordinary_rect_faces=ordinary,supplemental_faces=supplemented,
                faces_with_original_pixel_support=ordinary+supplemented,remaining_without_own_support=remainder,
                sampled_region_frame_rows=region_frames,sampled_region_frame_pixels=pixels,
                face_ledger_sha256=sha256(model_faces.read_bytes()).hexdigest())


def load_db(path):
    db=sqlite3.connect(':memory:')
    db.deserialize(lzma.decompress(path.read_bytes()))
    assert db.execute('PRAGMA integrity_check').fetchone()==('ok',),path
    assert not db.execute('PRAGMA foreign_key_check').fetchall(),path
    return db


def verify_databases():
    initial=load_db(PHASE/'entry04/research_texture_uv.sqlite.xz')
    updated=load_db(PHASE/'E_followup/research_texture_uv_runtime.sqlite.xz')
    tables=[name for name, in initial.execute("SELECT name FROM sqlite_master WHERE type='table'")]
    for table in tables:
        sql=f'SELECT * FROM "{table}" ORDER BY rowid'
        assert initial.execute(sql).fetchall()==updated.execute(sql).fetchall(),table
    counts={}
    checks={'texture':2256,'texture_exception':85,'prior_face':4113,'prior_zero_uv_support':176,
            'comparison_application':52,'comparison_face':1610,'missing_sprite_runtime':8,
            'alternate_sprite_runtime':16,'oak_chair_runtime_binding':176,'atlas_probe':217}
    for table,expected in checks.items():
        count,=updated.execute(f'SELECT COUNT(*) FROM "{table}"').fetchone()
        assert count==expected,table
        counts[table]=count
    fallback=updated.execute('SELECT COUNT(*) FROM missing_sprite_runtime WHERE runtime_sprite=?',
                             ('minecraft:missingno',)).fetchone()[0]
    active=updated.execute('SELECT COUNT(*) FROM alternate_sprite_runtime WHERE oak_states_using>0').fetchone()[0]
    assert fallback==8 and active==13
    linked=updated.execute('SELECT finding,COUNT(*) FROM prior_face GROUP BY finding').fetchall()
    assert dict(linked)=={'BOTH_ZERO_UV_NO_PIXELS':176,'MATCHED_PRIOR_FACE_SOURCE_AND_RECT':3937}
    assert updated.execute('SELECT COUNT(DISTINCT source_selector) FROM oak_chair_runtime_binding').fetchone()==(88,)
    assert updated.execute('SELECT COUNT(DISTINCT case_id) FROM comparison_application').fetchone()==(47,)
    links={(r['case'],r['rule_index'],r['option_index']):r for r in rows(PHASE/'entry04/1-5_TEXTURE_UV_HANDOFF.csv')}
    model_keys={(c,str(r),str(o)):(m,sha) for c,r,o,m,sha in
                updated.execute('SELECT case_id,rule_index,option_index,model_key,model_sha FROM comparison_application')}
    assert len(links)==counts['comparison_application'] and links.keys()==model_keys.keys()
    assert all((r['model_key'],r['model_sha'])==model_keys[k] for k,r in links.items())
    return counts,len(tables),fallback,active


def main():
    parser=ArgumentParser(description=__doc__)
    parser.add_argument('--replay',type=Path,required=True)
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    args.out.mkdir(parents=True,exist_ok=True)
    remote_files,remote_tables=remote_manifest(args.out)
    replay_counts,atlas_digest=replay_results(args.replay)
    texture_total,png_count,pixels=verify_png()
    uv=verify_uv(args.replay)
    db,preserved_tables,fallback,active=verify_databases()
    result=dict(status='PASS_PHASE_1_4_SOURCE_SCOPE',base_commit=BASE,
        remote_blob_files=remote_files,remote_csv_tsv_row_counts=remote_tables,
        exact_replayed_artifacts_by_stage=replay_counts,actual_runtime_replay_sha256=atlas_digest,
        handoff_unique_texture_ids=texture_total,redecoded_b_png_files=png_count,redecoded_b_png_pixels=pixels,
        uv=uv,sqlite_tables_verified=db,sqlite_original_tables_unchanged=preserved_tables,
        runtime_missing_fallback_ids=fallback,runtime_candidates_in_actual_chair=active)
    (args.out/'EXIT_AUDIT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n',encoding='utf-8')


if __name__=='__main__':
    main()
