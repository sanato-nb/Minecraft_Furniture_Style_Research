# TEX10-R012 — Minecraft 1.21.11 TextureUtil/NativeImage RGB 전처리 및 680개 full RGBA mip 정적 재계산

> 2026-11-13. **사용자 제공 1.21.11 원본**을 근거로 한 정적 연구. 인게임 검증은 사용자 정책에 따라 필수 조건에서 제외. 공식 Mojang 전체 JAR SHA-1도 제외(인증 성공 아님). Java JVM 실제 실행 결과와 byte-identical하다고 주장하지 않음.

## 1. 이번 새 원본 1차 소스 (누적 고유 경로 146→148)

- `1.21.11/com/mojang/blaze3d/platform/TextureUtil.class` — Git blob `848d481bd69d54c23b970d42227c0200ff2aacca`, JVM version 65. `solidify(Lfyh;)V` 359바이트 및 `fillEmptyAreasWithDarkColor(Lfyh;)V` 214바이트 명령어와 방향 배열 직접 검증.
- `1.21.11/fyh.class` (NativeImage) — Git blob `1396022da9cc9060e2c9ca27a30c6834f08139ce`, `a(II)I`(픽셀 읽기) 10바이트 및 `b(III)V`(픽셀 쓰기) 11바이트. 정수 ABGR와 정적 실험의 raw RGBA 파일 표현을 구분.
- R010 `ild.class`와 R011 `bel.class`, 앞서 재검증한 원본 PNG 8종은 **기존 측정 계승**이며 새 고유 소스에 합산하지 않음. 원본 8개 PNG SHA-256을 Python Pillow 이미지 디코드 전 재검증했다.

## 2. 원본 전처리 경로

**DARK_CUTOUT 잎 6종**: TextureUtil은 alpha가 0이 아닌 원본 픽셀 중 R+G+B 총합이 최소인 픽셀을 고른다. 동점이면 x-우선, y-다음 순회에서 먼저 나온 픽셀이 선택된다. 선택 색의 RGB 채널을 각각 정수 `(3*c)//4`로 계산해 α=0인 원본 픽셀에 넣는다. 알파는 0을 보존한다.

| 텍스처 | α=0 픽셀 | 선택한 최소 RGB | 채워 넣은 RGB |
|---|---:|---|---|
| `oak_leaves` | 84 | `#686468` | **`#4E4B4E`** |
| `spruce_leaves` | 96 | `#424242` | **`#313131`** |
| `birch_leaves` | 112 | `#706D70` | **`#545154`** |
| `mangrove_leaves` | 44 | `#4A4949` | **`#373636`** |
| `azalea_leaves` | 59 | `#3A4C26` | **`#2B391C`** |
| `flowering_azalea_leaves` | 51 | `#3A4C26` | **`#2B391C`** |

**덩굴(CUTOUT)**: `TextureUtil.solidify()`는 α>0 픽셀을 x-우선/y-다음 순서로 FIFO 큐에 넣고, 상하좌우 네 방향 **(우,좌,아래,위)** 순서로 최단 거리 BFS를 수행해 α=0 위치에 소스 RGB를 전파한다. 동거리 경쟁은 큐 삽입·방향 순서로 결정된다. 덩굴 투명 픽셀 **110개**의 최근접 소스 거리: **1칸 81개, 2칸 27개, 3칸 2개**.

**이끼(MEAN)**: 투명 픽셀이 없어 이 전처리 분기에서 RGB 변경이 발생하지 않음.

**실측 정적 결과**: 잎 6종 투명 RGB 위치 **446개** + 덩굴 **110개** = 원본 2,048 RGBA 위치 중 **556개 RGB 변경**; 8개 모두 alpha 변경 **0**, 원본 불투명 픽셀 RGB 변경 **0**. 정확한 사전/사후 비교 해시는 `SOURCE_PREPROCESS_8.csv`에 기록.

## 3. 32개 밉맵의 full RGBA 실험 결과

Python Pillow로 다시 읽은 원본 텍스처 8개에 위 전처리를 적용하고, R010 `ild` 및 R011 `bel`의 float32 gamma LUT·2×2 downsample·opacity coverage 보정 경로를 정적 구현했다.

- 각각 8×8(64), 4×4(16), 2×2(4), 1×1(1): **85×8=680개 파생 full RGBA 값**, 32개 이미지/레벨 산출.
- 이전 R011에서 **Python·JavaScript 독립 재구현으로 일치했던 alpha CRC32 32/32개**가 새 full RGBA 계산의 alpha 채널과도 일치.
- 8개 전처리 원본 16×16 base RGBA raw 데이터 합계 **8,192 bytes**, SHA256 `2e7396cbf6ee1039256a5cfc4a757d8b9332a5bd62416a714a90da6e31bc60b6`.
- 8×4 full mip RGBA raw 합계 **2,720 bytes**, SHA256 `d41e8edda12ebe1be8f00c96b46fabd261724af5a05d487bf3e14713e9b5f036`.
- raw RGBA를 zlib 압축한 뒤 base64로 인코딩한 **두 데이터셋**을 `BASE_RGBA_ZLIB_B64.txt`, `MIP_RGBA_ZLIB_B64.txt`에 보존. `DATASET_LAYOUT.json`에 8종 순서·레벨 순서·크기·복구 후 SHA를 기록. `REPRODUCE.md`에 Python 표준 라이브러리 복구 절차 제공.
- 미프 레벨 4의 1×1 `RGBA` 샘플을 `MIP_LEVEL4_RGB_8.csv`에, 원본 처리 전후 8개 SHA256을 `SOURCE_PREPROCESS_8.csv`에 제공.

## 4. 검증 경계

**원본 TextureUtil의 알고리즘/바이트코드는 직접 읽었으나, full RGBA 수치 계산 자체는 Python 포팅 재현**이다. Java JDK의 `Math.pow`, gamma LUT rounding, native NativeImage와 실제 게임 sprite atlas 입력을 직접 Java VM에서 호출해 바이트 비교하지 않았다. 그러므로 생성 680개 색상은 엄밀히 **source-guided experimental reconstruction**, 원본 마인크래프트의 검증된 실제 GPU 픽셀이라고 주장하지 않는다.

이번 신규 **원본 PNG 위치 0** (8개 기존 이미지만 재처리), **원본 고유 클래스 경로 2**. 8개 대상·기존 모델/블록상태/틴트 및 R009 렌더 레이어는 계승, 전역 v38/다른 단계/기존 TEX10-R001~R011 파일은 변경하지 않는다. 애니메이션·PZ→Minecraft 맵 변환·실제 가구 모델 제작은 계속 보류. 인게임 검증은 사용자 지시에 따라 의무에서 제외.

다음 실제 정적 연구의 핵심은 **원본 Java/JVM 직접 재생 또는 실제 sprite atlas 입력 데이터 확보를 통한 RGB byte-for-byte 교차 검증**으로, 이번 R012에서는 미완료로 명시한다.
