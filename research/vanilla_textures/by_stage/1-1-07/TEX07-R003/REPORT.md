# TEX07-R003 — 사용자 제공 1.21.11 JAR 추출본 직접 검증

Minecraft Java 1.21.11 / 2026-11-13 / 범위 **1-1-07 콘크리트·색면 7종**. 본 릴리스는 과거 미러 픽셀 연구를 새로 세지 않고, 사용자 제공 출처의 **실제 파일 및 교차출처 검증**에만 신규 성과를 기록한다.

## 출처 및 네 가지 독립 증거 수준

1. **사용자 제공 JAR 추출본 직접 검증 — 7/7 텍스처, 관련 31/31 파일.** 사용자가 자신의 Java 1.21.11 JAR을 직접 압축 해제해 업로드했다고 제공한 [저장소의 1.21.11/](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/tree/main/1.21.11)에서 실제 PNG 및 JSON을 조회했다. 재현용 고정 소스 커밋: `2a43897b8f605b4e0c96a272bca476ee6b70058e`. 직접 압축 해제했다는 사실은 사용자 진술이며 그 자체로 공식 원본 인증이 아니다.
2. **기존 비공식 미러 교차검증 — 31/31 파일 동일.** `InventivetalentDev/minecraft-assets`, ref `1.21.11`의 대응 PNG 7개, 블록상태 JSON 7개, 블록 모델 JSON 7개, 아이템 JSON 7개, 공통 부모 JSON 3개를 별도로 직접 조회해 Git blob SHA-1과 파일 내용을 비교했다. 전부 일치. `SOURCE_LEDGER.csv`에 31개 경로 및 해시 기록.
3. **Mojang 공식 원본 인증 — 0/7 미완료.** 압축 해제된 항목이 미러와 일치해도 원래 공식 `client.jar` 전체 파일의 SHA-1 및 Mojang 버전 메타데이터와 검증했다는 뜻이 아니다. 압축 파일 내 메타데이터, 순서, 헤더 등의 정보가 없으므로 추출 파일만으로 원래 JAR SHA-1을 신뢰성 있게 도출할 수 없다.
4. **인게임 정적 렌더 검증 — 0/7 미완료.** 게임 구동/실제 장면 캡처는 이번 작업에 없음. 애니메이션 분석은 보류.

## A/B — PNG 실물·교차 파일 무결성

사용자 제공 7개의 `assets/minecraft/textures/block/<color>_concrete.png`를 GitHub Base64로 읽고 실제 이진 바이트로 디코딩, SHA-256을 직접 계산한 뒤 기존 R001/R002/v4 SHA-256 및 미러 파일 실제 바이트와 비교: **7/7 정확히 일치**. PNG 서명, `IHDR` 16×16, indexed PNG color type 3, `PLTE`, `IDAT`, `IEND`, 모든 청크의 CRC32, IEND 뒤 추가 바이트 0건을 직접 검사: **7/7 통과**. 팔레트 엔트리 수: white 6, black 4, red 6, blue 4, green 5, yellow 10, gray 3. `PNG_CROSS_HASHES.csv`는 신규 원본 쪽에서 독립 계산한 실제 SHA-256과 길이·무결성 7행을 기록.

## C/D — 기존 결과 유지 및 중복 방지

R001의 1,792 RGBA 화소, 평균 RGB·명도·채도, R002의 팔레트 빈도 38행·반복 이음매 검사 7건·21쌍 CIEDE2000 계산은 **사용자 제공 PNG가 기존 PNG와 바이트 동일함이 증명되어 그대로 적용 가능**하다. 그러나 이번 단계가 기존 픽셀 통계를 또 신규 실측했다고 기록하지 않는다. 색면의 가구 적용은 가설이며 실제 가구 모델링/제작은 수행하지 않는다.

## E — 사용자 추출본의 원본 모델 체인·UV 직접 확인

- 사용자 폴더의 `blockstates/<color>_concrete.json` 7개: `variants[""]` 1개 → `minecraft:block/<color>_concrete`.
- `models/block/<color>_concrete.json` 7개: `parent=minecraft:block/cube_all`; `textures.all=minecraft:block/<color>_concrete`.
- `items/<color>_concrete.json` 7개: `model.type=minecraft:model`, `model.model=minecraft:block/<color>_concrete`.
- `models/block/cube_all.json`은 `block/cube`를 부모로 하며 `particle`과 여섯 면을 `#all`에 연결함.
- `models/block/cube.json`은 `block/block` 부모 아래 원소 한 개 `[0,0,0]`→`[16,16,16]`와 여섯 면 `down/up/north/south/east/west`를 선언하고 `cullface`를 지정. 숫자 `uv` 필드는 각 면에 **없음**.
- `models/block/block.json`은 기본 렌더 display 설정 모델이다.

따라서 7색×6면=**42면**, 명시된 숫자 UV **0면**, 기본 큐브 풀페이스로부터 파생한 UV `[0,0,16,16]` **42면**. 이 구조는 정적 JSON 소스상 사실이며 실제 게임 렌더 결과가 아님. `STATIC_MODEL_CHAIN.csv`에서 각 색의 참조 경로를 확인할 수 있다.

## G — 저장과 다음 과제

새로운 결과 `SOURCE_LEDGER.csv` 31건, `PNG_CROSS_HASHES.csv` 7건, `STATIC_MODEL_CHAIN.csv` 7건, `SUMMARY.json`, 본 `REPORT.md`를 **TEX07-R003 신규 디렉터리에 추가**한다. 기존 R001/R002 파일·보고서·SHA·커밋은 변경하지 않는다. 단계 `HANDOFF.md`와 `STATE.json`만 갱신. 글로벌 `v38`은 그대로.

다음 독립 단계는 **TEX07-R004**. 원본 `client.jar` 전체와 공식 Mojang 버전 메타데이터를 확보할 경우 JAR SHA-1 인증을 별도 진행하고, Minecraft 실행/실제 정적 장면이 있어야 인게임 검증을 진행할 수 있다. 애니메이션 보류, 좀보이드 변환과 실제 가구 3D 모델 제작 제외.
