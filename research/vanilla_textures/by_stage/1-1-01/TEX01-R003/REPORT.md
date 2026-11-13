# TEX01-R003 — 1-1-01 사용자 제공 JAR 추출본 원본 출처 및 PNG IHDR 신규 검사

2026-11-13. 18개 고정 목재·원목. R001/R002 불변. 전체 v38 변경 없음.

## A 출처 교정 / 검증 네 구분

**사용자 진술:** 저장소 `1.21.11/`은 본인이 직접 Minecraft Java Edition 1.21.11 client JAR을 압축 해제해 GitHub에 올린 추출본이다. 이 사용자 제공 추출본을 연구의 우선 원본으로 인정한다. 그러나 JAR 전체가 Mojang 공식 배포 바이너리와 일치한다는 인증은 별도이다.

R001 보고서에서 `mirror/extracted`로 혼재 표기한 18 PNG와 정적 JSON 43개는 실제로 사용자 저장소 `1.21.11/assets/minecraft/` 파일을 직접 읽은 결과였다. 이 사실을 **새 보고서로 정정**하며 기존 결과/커밋은 수정하지 않는다.

1. **사용자 제공 추출본 검증:** R001 PNG 18/18 SHA-256/PNG CRC32/IDAT/RGBA 직접 검사 및 JSON 43개 정적 모델 연결. R003에 GitHub 바이너리 18개 SHA1(blob)·크기·PNG 헤더 다시 검사.
2. **미러 교차 검증:** 기존 v4의 **기록된** SHA-256과 R001의 PNG SHA-256 18/18 일치. 하지만 별도의 비공식 미러 **원본 바이너리를 이번에 직접 비교한 0건**은 엄격히 구분.
3. **Mojang 공식 원본:** 공식 1.21.11 client.jar 전체 SHA-1·크기를 Mojang 원본 메타데이터와 직접 대조한 바 없어 인증 **0/18**.
4. **인게임 실제 렌더:** Minecraft 화면상 UV/조명/컬링 정적 결과 확인 **0/18**.

## B — 이번 신규 PNG IHDR 실측

GitHub `1.21.11/assets/minecraft/textures/block/`의 실제 PNG 18개를 Base64로 재조회하여 **시그니처·IHDR 16×16·indexed color type 3 및 현행 Git blob SHA/파일 크기가 R001과 18/18 일치**함을 직접 확인.

- PNG 팔레트 **인덱스 저장 비트 깊이 4**: `acacia_planks`, `oak_log`, `spruce_log`, `birch_log` = **4개**.
- PNG 팔레트 **인덱스 저장 비트 깊이 8**: 나머지 **14개**.
- 이 4/8비트는 PNG 인코딩의 팔레트 인덱스 비트 깊이로, 기존에 검증된 **RGBA 출력 채널 깊이**나 실제 Minecraft 렌더 품질과 다른 개념.
- R001 4,608 RGBA 픽셀, SHA256/CRC/색상 정량 검사 및 R002 72개 가상 이웃 회전 조건을 **신규 검사로 중복 계산하지 않음**.

## C/D/E — 이번 신규 버전 및 아틀라스 원본 JSON 근거

- 직접 읽은 사용자 추출본 `1.21.11/version.json`의 Git blob SHA1 `b49974d3ebd6cb73291d9e4c92d23b3192dadd66` → `id=1.21.11`, `name=1.21.11`, `java_version=21`, `world_version=4671`, `protocol_version=774`, `stable=true`.
- 직접 읽은 `1.21.11/assets/minecraft/atlases/blocks.json` SHA1 `541ce56ad0b09f258963dd2bf3e3cb6e786d2d79` → `{"type":"minecraft:directory","source":"block","prefix":"block/"}`. 고정 18개는 **정적 경로 규칙상** `textures/block/`에 속함. 인게임 실제 GPU 아틀라스 생성·렌더는 미검증.
- 이 메타 JSON 2개는 **기존 R001의 고유 43 모델/블록상태 JSON과 다른 범주**. R001 모델 로컬 150면, D1 6쌍, D2 원본 이음새, R002 72 가상 회전 경계 실측과 11 JSON 재검사도 모두 보존.

## F/G

공식 JAR 및 인게임 검사 미완료 그대로. R003 파일 `SOURCE_LEDGER.csv`·`EXTRACT_METADATA.json`·`SUMMARY.json`·`REPORT.md`는 **이번 출처 정정과 신규 IHDR/버전/아틀라스 확인만** 기록. 다음 전용 버전 `TEX01-R004`. 애니메이션, Project Zomboid 변환, 실제 가구 3D 제작 수행 안 함.
