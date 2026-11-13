# TEX10-R012 데이터셋 복원 방법

GitHub의 BASE_RGBA_ZLIB_B64.txt 및 MIP_RGBA_ZLIB_B64.txt는 **zlib을 적용한 raw RGBA byte stream을 base64 문자열로 저장한 텍스트**이다. 복구할 때 UTF-8에서 줄바꿈을 제외하고 디코드한다.

```python
import base64, zlib, hashlib, json
from pathlib import Path
layout = json.loads(Path('DATASET_LAYOUT.json').read_text())
for section in ('base', 'mip'):
    meta = layout[section]
    contents = Path(meta['file']).read_text().strip()
    data = zlib.decompress(base64.b64decode(contents))
    assert len(data) == meta['decoded_total_bytes']
    assert hashlib.sha256(data).hexdigest() == meta['raw_SHA256']
    Path(section.upper() + '_RGBA.bin').write_bytes(data)
```

원본 텍스처 순서는 `DATASET_LAYOUT.json`의 `order`이다. `base`는 1개당 16×16×4 = 1024 bytes, `mip`는 1개당 L1(8×8×4=256) → L2(4×4×4=64) → L3(2×2×4=16) → L4(1×1×4=4), 총 340 bytes. 픽셀은 좌에서 우로, 행은 위에서 아래로, 채널은 RGBA이다.

이 파일은 **원본 TextureUtil/NativeImage 및 MipmapHelper 바이트코드를 참고한 Python 정적 재현 결과**이다. 원본 Mojang JVM 코드의 직접 실행, 실제 게임 화면, GPU 결과의 byte-for-byte 인증이 아니다.
