#!/usr/bin/env python3
"""Compare an owned Minecraft client.jar (or extracted textures) to the 150-source hash manifest.

Usage:
  python verify_150_against_client.py --client-jar /path/to/1.21.11.jar --manifest 01_누적150종_픽셀측정.csv --output source_checks.csv
  python verify_150_against_client.py --assets-dir /path/to/assets/minecraft/textures/block --manifest 01_누적150종_픽셀측정.csv --output source_checks.csv

Only validates correspondence to the *unofficial mirror* hashes, not the authenticity of a user-supplied JAR.
"""
import csv,hashlib,zipfile,argparse,io
from pathlib import Path
from PIL import Image

def main():
    p=argparse.ArgumentParser()
    group=p.add_mutually_exclusive_group(required=True)
    group.add_argument('--client-jar',type=Path)
    group.add_argument('--assets-dir',type=Path)
    p.add_argument('--manifest',type=Path,required=True)
    p.add_argument('--output',type=Path,default=Path('source_checks.csv'))
    args=p.parse_args()
    with args.manifest.open(encoding='utf-8-sig',newline='') as f: rows=list(csv.DictReader(f))
    z=zipfile.ZipFile(args.client_jar) if args.client_jar else None
    findings=[]
    try:
        for r in rows:
            path=r['source_path']; file=(args.assets_dir/Path(path).name) if args.assets_dir else None
            try:
                b=z.read(path) if z else file.read_bytes()
                im=Image.open(io.BytesIO(b));im.verify()
                hashok=hashlib.sha256(b).hexdigest()==r['sha256']
                findings.append({'texture_id':r['texture_id'],'present':1,'png_decodes':1,'sha256_matches_mirror':int(hashok),'computed_sha256':hashlib.sha256(b).hexdigest(),'error':''})
            except Exception as exc:
                findings.append({'texture_id':r['texture_id'],'present':0,'png_decodes':0,'sha256_matches_mirror':0,'computed_sha256':'','error':str(exc)})
    finally:
        if z:z.close()
    with args.output.open('w',newline='',encoding='utf-8-sig') as f:
        columns=['texture_id','present','png_decodes','sha256_matches_mirror','computed_sha256','error'];w=csv.DictWriter(f,fieldnames=columns);w.writeheader();w.writerows(findings)
    matches=sum(x['sha256_matches_mirror'] for x in findings)
    print('Mirror-byte SHA matches:',matches,'/',len(rows))
    print('NOTE: Match only confirms the files in your supplied input equal the unofficial mirror. It does NOT by itself prove your input is an official, authenticated 1.21.11 client.jar.')
if __name__=='__main__':main()
