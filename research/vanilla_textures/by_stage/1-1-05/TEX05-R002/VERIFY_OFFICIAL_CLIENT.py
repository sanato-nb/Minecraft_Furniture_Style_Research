#!/usr/bin/env python3
"""Authenticate official Minecraft 1.21.11 client.jar before auditing glass assets.
Does not download or republish the game JAR. Requires a user-supplied local JAR.
"""
import argparse
import hashlib
import json
from pathlib import Path
from urllib.request import urlopen
from zipfile import ZipFile

VERSION = '1.21.11'
MANIFEST = 'https://piston-meta.mojang.com/mc/game/version_manifest_v2.json'
EXPECTED_PNG = {
    'glass': 'cb89c706dce86eac3123cef087d359b5f23098b658a468fb91662b4a9922bcd0',
    'red_stained_glass': '4520f85fee79972191217d623c8b38522cacf74cb7c71113c0a6240d3b1f2ad2',
    'black_stained_glass': '62c705812949f0372dcc2fa82a5d89f7028ba1d9b3bd38765613e344f34f5b1c',
    'blue_stained_glass': '7d6cfe98ddc5d975b3bcf5f9cffc008f90db94d5d981ef440f7b68e8267ae247',
    'green_stained_glass': 'dc82be445bd9c7cf158bd57651d51bfef400310f2ad4937fe1e5b1c60b4f5916',
    'white_stained_glass': '2d4504957fa123a6e9f35d93e05f94fb053ec213541f01fcecbc0097eaa5df75',
}

def get(url):
    if not url.startswith('https://piston-meta.mojang.com/'):
        raise RuntimeError('Refusing unexpected metadata host: '+url)
    with urlopen(url, timeout=30) as response:
        return response.read()

def verify(path):
    data = json.loads(get(MANIFEST))
    entry = next(v for v in data['versions'] if v['id'] == VERSION and v['type'] == 'release')
    version_bytes = get(entry['url'])
    version_sha1 = hashlib.sha1(version_bytes).hexdigest()
    if version_sha1 != entry['sha1']:
        raise RuntimeError('Official Mojang version JSON SHA1 differs from manifest')
    metadata = json.loads(version_bytes)
    if metadata['id'] != VERSION:
        raise RuntimeError('Version ID differs from requested release')
    client = metadata['downloads']['client']
    local = path.read_bytes()
    jar_sha1 = hashlib.sha1(local).hexdigest()
    if jar_sha1 != client['sha1'] or len(local) != client['size']:
        raise RuntimeError('Supplied client.jar does not match official metadata SHA1+size')
    source = []
    with ZipFile(path) as jar:
        if jar.testzip() is not None:
            raise RuntimeError('Invalid JAR ZIP CRC')
        for name, expected in EXPECTED_PNG.items():
            rel = 'assets/minecraft/textures/block/' + name + '.png'
            found = hashlib.sha256(jar.read(rel)).hexdigest()
            source.append({'texture_id':name,'jar_png_path':rel,'sha256':found,
                           'matches_previous_mirror':found == expected})
    return {'version':VERSION,'official_manifest_url':MANIFEST,'official_version_json_sha1':version_sha1,
            'official_client_sha1':client['sha1'],'local_client_sha1':jar_sha1,
            'local_jar_size':len(local),'official_client_jar_authenticated':True,
            'png_assets_checked':len(source),'png_mirror_byte_matches':sum(x['matches_previous_mirror'] for x in source),
            'in_game_render_verified':False,'files':source}

def main():
    a=argparse.ArgumentParser()
    a.add_argument('--client-jar',type=Path,help='Locally installed original Minecraft 1.21.11 client.jar')
    arg=a.parse_args()
    if not arg.client_jar:
        print(json.dumps({'status':'pending','official_jar_verified':False,
                          'reason':'No local client.jar supplied; no download attempted'},indent=2))
        return
    try:
        print(json.dumps(verify(arg.client_jar),ensure_ascii=False,indent=2))
    except Exception as exc:
        print(json.dumps({'status':'pending_or_failed','official_jar_verified':False,'error':str(exc)},indent=2))
        raise SystemExit(2)

if __name__ == '__main__':
    main()
