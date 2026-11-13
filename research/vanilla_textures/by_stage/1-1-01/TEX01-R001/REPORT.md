# TEX01-R001 · 1-1-01 목재·원목 정적 텍스처 직접 검증

**기준**: 2026-11-13 · Minecraft Java 1.21.11 · 사용자 저장소 `1.21.11/assets/minecraft` 추출/미러 자산. **전역 v38 변경 없음**. 범위는 [STATE.json](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/stages/1-1-01/STATE.json)에 고정된 PNG **18개**. Mojang 공식 client.jar **미인증**, 게임 실행 정적 장면 **미검증**.

## A: v4 역사 자료 대조

기존 [v4 픽셀 원장](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/v4_150/01_누적150종_픽셀측정.csv)과 [150개 번호 원장](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/1-1_150_texture_numbered_task_ledger.csv), 본 단계 STATE의 18개 texture_id/path/SHA-256을 교차 대조했다. 18개 경로 중복 또는 v4 SHA 충돌 **0개**. 이 18개 역사적 실측을 신규 검사 횟수로 중복 집계하지 않는다.

## B: 원본 PNG 바이너리 무결성

GitHub `fetch_file(base64)`로 받은 **18개 바이너리**를 Python에서 독립 Base64 해제 및 SHA-256 재계산했다. v4에 기록된 SHA-256과 **18/18 일치**. 각 PNG 시그니처·모든 chunk CRC32(zlib.crc32)·IDAT zlib 압축 해제·Pillow `Image.verify()`·`convert("RGBA")` 해독도 **18/18 통과**. 소스 PNG는 모두 팔레트 모드 **P**, 각각 **16×16**. `SOURCE_LEDGER.csv`에 바이너리 SHA-256과 Git blob SHA-1을 다른 열로 남겼다. 바이너리 정합성은 Mojang JAR 공식 인증과 **별개**다.

## C: 실제 RGBA와 숫자 의미

총 **4,608개 RGBA** 실화소: 완전불투명 4,608, 알파0=0, 부분알파=0. 밝기 = 8비트 RGB 코드값의 `0.2126R+0.7152G+0.0722B` 평균 (실제 광량이나 게임 조명 아님). 채도 = RGB의 HSV `(max-min)/max` 평균. H/V 인접 대비 = 각각 x/y로 한 칸 떨어진 픽셀들의 채널별 절댓값 차이 평균. 경계 이음새 대비 = 왼쪽/오른쪽 끝, 위/아래 끝에서 대응하는 RGB 간 절댓값 차이 평균. `SOURCE_LEDGER.csv`는 이 값을 **18개 파일별** 보존하며 기존 v4 수치와 직접 재계측 수치가 일치한다.

9개 판자 PNG(`oak, spruce, birch, dark_oak, cherry, jungle, pale_oak, crimson, warped`의 `_planks`)는 팔레트 색을 첫 등장 순서로 치환했을 때 **16×16 색배치 인덱스 패턴이 동일**하다. `oak_log`와 `spruce_log` 역시 패턴 동일. 서로 다른 SHA/실제 색을 가진 파일이며 바이트 중복은 아니다.

## D1: 목재 판자·옆면·단면 (두 번째−첫 번째)

| 이미지 비교 | 평균 휘도 차이 | 평균 HSV 채도 차이 |
|---|---:|---:|
| oak_planks → oak_log | -45.9897 | +0.0148 |
| oak_planks → oak_log_top | -9.2546 | +0.0007 |
| spruce_planks → spruce_log | -47.9518 | +0.1407 |
| birch_planks → birch_log | +39.9553 | -0.3274 |
| oak_log → oak_log_top | +36.7351 | -0.0141 |
| oak_log → stripped_oak_log | +59.2673 | -0.0187 |

자작나무 껍질 옆면은 판자보다 밝아 **판자>원목 밝기라는 일괄 규칙이 반례**로 깨진다. oak_log_top은 oak_log 옆면보다 +36.7351 밝다. `spruce_log_top`, `birch_log_top`, `stripped_oak_log_top` 등의 **PNG 직접 색상 측정은 고정 18개 밖**이므로 하지 않았다. 이들에 대한 D1 전체 종별 비교는 부분 미완료로 남긴다. `D1_COMPARISONS.csv` 참조.

## D2: 무늬·반복 타일 경계

12개 `_planks`의 V/H 인접 RGB 변화 비율은 **3.0524–3.7203**으로 텍스처 **화면 좌표 기준 가로줄**이 우세하다. `oak_log`=0.2899, `spruce_log`=0.3008, `stripped_oak_log`=0.4908은 세로 결 성향. 반례: `birch_log`=2.0303은 껍질의 가로 얼룩이 강하므로 수치만으로 블록 축 판단 금지. `oak_log_top`=1.0003, `bamboo_mosaic`=0.9804는 혼합·격자 성향.

반복 경계 예: oak_planks L/R=12.5417, T/B=56.8333; bamboo_planks L/R=3.1875, T/B=33.2917; oak_log_top L/R=0, T/B=2. 모든 수치는 **원본 16×16 PNG의 RGB 경계 대비**이며 게임 조명/보간/실제 렌더링에서 이음새가 어떻게 보이는지 미검증.

## D3/E: 정적 JSON 모델면·텍스처 슬롯·UV 근거

GitHub 원본 **JSON 43개 직접 조회**: 블록상태 17개, 리프 모델 21개, 템플릿 부모 5개(`cube_all`, `cube_column`, `cube_column_horizontal`, `cube`, `block`). `SOURCE_JSON_SHA_MANIFEST.csv`에 **각 원본 Git blob SHA-1** 수록.

- 판자 12종 + `bamboo_mosaic` = **13개 블록**. blockstate 기본 variant → 같은 이름의 모델 → `cube_all` → `cube`; 여섯 면 `#all`을 같은 텍스처에 연결. cube 요소 좌표 [0,0,0]–[16,16,16]. 면에 `uv` 배열이 따로 없으므로 **16×16 implicit UV**이며 explicit UV라고 적지 않는다.
- 원목 측면 4종 `oak_log/spruce_log/birch_log/stripped_oak_log`: `axis=y` → `cube_column` → 위·아래 `#end` / 옆 4면 `#side`. `oak_log_top`은 oak_log `#end`에 직접 연결.
- `axis=x` → `*_horizontal` + blockstate **x=90,y=90**; `axis=z` → 같은 `*_horizontal` + **x=90**. `cube_column_horizontal`의 로컬 위쪽 면에는 **UV rotation=180°**가 원본 명시됨. 면 방향을 월드 공간에 사상하는 최종 엔진 렌더는 미검증.
- `MODEL_UV_FACE_MAP.csv`에 총 **150개 모델-로컬 면 참조**(13×6+4×3×6) 기록. 이 중 고정 18 PNG로 가는 **132개**, 이 단계에 포함하지 않은 나머지 세 종 단면 PNG 의존성 **18개**는 경로 관계만 기록(픽셀 분석/성과 집계에 불포함). 모델면 참조는 독립 PNG나 인게임 렌더 픽셀을 의미하지 않는다.
- 기존 전체 프로젝트 **v38**의 `oak_shelf`가 `stripped_oak_log`를 `#particle`로 쓰되 **선반 기하면에는 연결하지 않는다는 근거**는 보존한다. 이 단계에서 선반 모델을 신규 파일로 세지 않음.

## F: 미검증 영역 (완료라고 표현 금지)

**Mojang 공식 Java 1.21.11 client.jar 인증·내부 PNG 독립 검사: 0/18. 실제 Minecraft 인게임 정적 색/UV/면·이음새 검증: 0/18.** 사용자 저장소의 추출/미러에 있는 PNG가 v4 미러 SHA와 일치한다는 사실만 확인했다. 실제 엔진 셰이더·보간·컬링·월드 표면 UV 결과는 가정하지 않는다. `D1`도 다른 목재 종의 단면 검사는 고정 범위 밖이므로 부분 미완료.

애니메이션 프레임·키프레임·움직임 연구는 사용자 해제 지시까지 **전면 보류**(기존 기록 삭제 금지). Project Zomboid 변환과 가구 3D 모델 제작은 범위 밖.

## G: 저장물·독립 버전

이 불변 폴더의 `SOURCE_LEDGER.csv`(18 PNG 실측), `D1_COMPARISONS.csv`(6쌍), `MODEL_UV_FACE_MAP.csv`(150면), `SOURCE_JSON_SHA_MANIFEST.csv`(43 JSON), `SUMMARY.json`, `REPORT.md`가 최초 신규 결과. **단계의 정적 소스 실측 18개**와 **전체 A–G 공식 포함 검증 완료 0개**를 혼동하지 않는다. 다음 버전은 `TEX01-R002`; 공식 전체 버전 `v38` 유지.
