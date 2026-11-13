# TEX10-R011 — 실제 PNG 8종 재디코드·밉맵 4단계 알파 680셀 정적 재계산

> 2026-11-13 / Minecraft Java 1.21.11 사용자 추출본 정적 원본 연구. **인게임 검증 불필요(사용자 정책)**. 실제 Minecraft JVM/게임 실행과 byte-exact GPU 검증은 수행하지 않음. 기존 v38·타 세부 단계·R001–R010 변경 금지.

## 이번에 새롭게 계산·교차 검증한 내용

- 원본 PNG 8개를 GitHub에서 새로 읽어 16×16 RGBA로 Python Pillow 재디코드하고 **원시 PNG SHA-256 8개 전부 이전 R001/R002 기록과 일치**. 대상 개수 변경 없음. 새 파일의 고유 원본 경로는 `1.21.11/bel.class` **1개**; 이전 145→누적 146개. 기존 PNG 8개를 다시 디코드한 2,048화소는 **재검증**, 신규 고유 픽셀 원본 0.
- R010 `ild.class`에 있는 2×2 다운샘플, 4×4 bilinear opacity coverage 검사 및 5회 탐색 alpha correction 코드를 재해석하고, 이번 새 원본 `bel.class`의 ABGR α 추출/8→10bit gamma LUT·mean/dark alpha 경로를 교차 참조.
- 사용자 제공 8개 PNG 마스크(R002)로 시작해 각 16×16 입력을 **8×8(64) → 4×4(16) → 2×2(4) → 1×1(1)**로 정적 재계산. **1개당 85, 총 680개 새로운 *파생 알파값***을 `ALPHA_LEVELS_HEX_8.json`에 행·열 별 2자리 16진수로 저장.
- 독립 구현 2개: (1) Python Pillow/numpy.float32에서 실제 PNG RGBA 직접 읽기, (2) JavaScript Math.fround에서 R002의 알파 16행을 독립 재구성. **32/32 레벨 CRC32 일치**, 680바이트 합계 CRC32 `2171e3da`.
- **주의**: 이 일치는 Python/JavaScript *재구현끼리*의 확인이며 원본 Mojang Java 메서드 실행 비교/바이트 동일성 인증이 아니다. 680개는 **알파만** 보존하며, full RGBA의 원본 Java 출력 동등성은 미검증.

## 실제로 계산된 mip α 계층

| 텍스처 | 전략 | 원본 α=0 픽셀 | 계산 L1 (8×8) | L4 (1×1) α |
|---|---|---:|---|---|
| `oak_leaves` | DARK_CUTOUT | 84 | 64개 부분 알파 | 0x8e |
| `spruce_leaves` | DARK_CUTOUT | 96 | 64개 부분 알파 | 0x92 |
| `birch_leaves` | DARK_CUTOUT | 112 | 64개 부분 알파 | 0x8f |
| `mangrove_leaves` | DARK_CUTOUT | 44 | 64개 부분 알파 | 0x90 |
| `azalea_leaves` | DARK_CUTOUT | 59 | 64개 부분 알파 | 0x9e |
| `flowering_azalea_leaves` | DARK_CUTOUT | 51 | 64개 부분 알파 | 0x8f |
| `vine` | CUTOUT | 110 | 64개 부분 알파 | 0x8f |
| `moss_block` | MEAN | 0 | 64개 불투명 | 0xff |

- 6종 `DARK_CUTOUT` 잎과 덩굴 `CUTOUT`의 모델 기반 계산에서는 **L1–L4에서 595개 파생 픽셀이 전부 0<alpha<255**. 원본의 0/255 이진 알파와 구분된다. **이끼 MEAN의 파생 85개 픽셀은 전부 alpha=255**.
- 위 조건은 실험에 사용한 `mipmapLevels=4`·`alpha_cutoff_bias=0`·개별 16×16 입력이라는 제한하에서 나온 결과이다. 실제 게임 GPU 화면에서 그 값이 그대로 표시된다는 뜻이 아님.

## 원본 코드 해석과 재현 알고리즘

1. `bel.a([S)V`: 8-bit sRGB→10-bit linear LUT, `bel.a([B)V`: 10-bit linear→8-bit sRGB LUT. Java float32 수준의 산술/반올림 모델을 사용한다.
2. `DARK_CUTOUT`의 downsample α는 원본 `ild.a(IIII)I`와 같이 alpha=0 입력을 생략하고 살아남은 4개 입력의 linear 값을 합산한 뒤 4로 나눠 역변환한다. `CUTOUT` 및 `MEAN` 일반 α는 네 alpha 정수값 평균(버림)을 사용한다.
3. `ild.a(NativeImage,float,float)`: 좌우·상하 이웃 2×2 코너의 α를 4×4 보간 채점(총 16샘플)하고 임계값 0.5 초과 영역 비율 계산. 기준 원본 이미지의 해당 비율을 유지하도록 `ild.a(NativeImage,float,float,float)`의 제한된 5회 이분 탐색으로 스케일을 정한다. 픽셀별 최종 `clamp(alpha*scale+0+0.025,0,1)`.
4. 1×1단계에서 보간 cell 분모가 0이므로 Java float NaN 경계 조건은 구현상 추가 확인 포인트. 현재 실험에서는 최적 scale 기본 1.0을 유지했다.
5. `TextureUtil.solidify`와 `fillEmptyAreasWithDarkColor`의 RGB base-image 보정/최종 JAR byte-exact 비교는 이 연구의 **미확인**으로 별도 표시하며, alpha 배열만을 강하게 검증한다.

## 실제 산출 파일과 앞으로의 연구

- `ORIGINAL_PNG_REHASH_8.csv`: 원본 8개 raw SHA256·바이트 길이·블롭과 R002 비교
- `ALPHA_LEVELS_HEX_8.json`: **680개의 정적 파생 alpha**, 32개 각 수준 CRC32, float32 alpha coverage scale
- `MIP_ALPHA_METRICS_32.csv`: 8×4 각 크기/알파 영역/평균/CRC
- `BYTECODE_ALPHA_MATH_AUDIT.json`: 원본 두 클래스 메서드 근거 및 검증 한계
- `SOURCE_LEDGER.csv`, `SUMMARY.json` 및 이 보고서

**미확정 다음 후보**: 원본 Java `TextureUtil`과 실제 NativeImage/atlas 호출 맥락을 더 추적하여 alpha-only 결과를 진짜 원본 Java full RGBA 결과와 교차 검증. 인게임 캡처·애니메이션·실제 가구 모델링/PZ 변환은 사용자 정책 및 단계 범위로 제외/보류.
