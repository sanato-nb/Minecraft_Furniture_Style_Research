# TEX02-R002 — 석재·벽돌 17종 정적 면 검증과 끝면 예외 확인

> 2026-11-13 · **1-1-02만 담당** · 전 단계 TEX02-R001 계승 · 전체 v38 그대로 · 애니메이션 보류.

## 이번 작업의 신규 범위와 검증 등급

1. Github `main`의 단계별 `STATE.json`에서 TEX02-R001 및 next TEX02-R002 확인. v4 원장 17종·TEX02-R001 PNG/RGBA 17종·model/blockstates 17종은 이전 연구 근거로 재사용하며 **신규 17종 완료라고 다시 계산하지 않음**.
2. GitHub 추출 미러 `InventivetalentDev/minecraft-assets`의 **pinned commit `7241a12cc2707abd7022f399c5d9033153e492e1`**에서 모델이 실제 참조하는 **`deepslate_top.png`, `blackstone_top.png` 보조 PNG 2종을 직접 가져와 독립 SHA-256, 원본 PNG 청크 CRC32, Pillow RGBA 픽셀 검증**. 출처는 Mojang 공식 JAR가 아닌 `unofficial_extraction_mirror`.
3. 원본 부모 JSON `cube.json`, `cube_all.json`, `cube_column.json`, `cube_mirrored.json`, `cube_column_mirrored.json`과 자식 모델/블록상태 연결을 대조. 이 단계 17종에 대해 면별 **102개 정적 `face→#slot→texture_path` 매핑**, 블록상태 **31개 JSON 배열 항목**을 별도 CSV에 보존.
4. 공식 버전 매니페스트/클라이언트 JAR 원본을 인증하지 못했으므로 **공식 인증 0/17, 인게임 정적 렌더 0/17** 유지. TEX02-R002은 부분 증거 릴리스이지 A–G 최종 완료가 아니다.

## 새 보조 PNG 실제 정량 결과 (17개 분모에 포함하지 않음)

| 모델 | end PNG | SHA-256 | bytes | opaque | mean Y | side mean Y | side와 동일 픽셀 | mean abs Y diff |
|---|---|---|---:|---:|---:|---:|---:|---:|
| deepslate | deepslate_top | `9f2f5e0a67b4a007244cf7064e09da7e693322cfd21b1884190bcd6b26e91aec` | 189 | 256/256 | 87.3605 | 80.3099 | 37/256 | 21.6362 |
| blackstone | blackstone_top | `9eb9bce7a27defc49dd8a2b2dc74f4c7710dc3bbcaa5108a6c1193c82922935d` | 193 | 256/256 | 38.1320 | 37.3047 | 37/256 | 18.5175 |

PNG 두 파일 모두 16×16/완전 불투명, `IHDR→PLTE→IDAT→IEND` 청크별 CRC 통과. `END_FACE_SUPPLEMENT.csv`에 파일 SHA-256·Git blob SHA·CRC32·정량 수치/출처를 구분했다.

관찰: `deepslate` end T/B 인접 블록(동일 PNG 반복 가정) seam 평균 Y=18.0063, 측면=13.0618; `blackstone` end L/R=17.6985, 측면=10.3085. **끝면과 측면은 시각적/화소적 동일 재료로 치환하면 오류**. 이는 텍스처 자체의 접합 지표이며 게임의 실제 벽면 접합·동적 셰이더 결과가 아니다.

## 면/UV 및 D3 검사 — 정적 모델 소스

- `cube_all` 15종의 `down/up/north/south/east/west` 여섯 면은 동일 `#all` 텍스처. 15×6=90개 기본 면 매핑.
- `cube_column`인 `deepslate`, `blackstone`의 각 4개 수직 면은 `#side`, 위아래 각 2개 면은 `#end`; 2×6=12개 기본 면 매핑. **총 102개**. 해당 부모는 `cube`를 상속하며 cube가 UV를 별도 명시하지 않으므로 기본 면 UV 상속이지 원본에 각 면 `uv:[0,0,16,16]`가 적힌 것은 아니다.
- `stone` 블록 상태: normal, mirrored, normal y=180, mirrored y=180 총 4개. Mirrored model은 `cube_mirrored_all`→`cube_mirrored`, 여섯 면에 **명시된 `uv:[16,0,0,16]`**, U 반전이 구조적으로 확인됨.
- `deepslate` 블록 상태: `axis=x/y/z` 각 4개로 총 12개 항목. 이 중 `axis=x`는 `x=90,y=90` 조합 **동일 표현 2회씩 반복**. 중복을 임의 삭제하지 않고 `BLOCKSTATE_VARIANTS.csv` 배열 인덱스 그대로 보존. `axis=y/z`는 미러와 `y=180` 회전 조합. **변형 합계: stone 4 + deepslate 12 + 다른 15종 각 1 = 31개.**
- 회전된 모델이 실제 월드 어떤 방향에서 어느 픽셀 쌍과 맞닿는지, 색상/조명/UVlock에 따라 결과가 어떻게 변하는지는 **인게임 정적 렌더 미검증**. `FACE_SOURCE_LEDGER.csv` 102개는 회전 이전의 **model-local face** 매핑이고, `BLOCKSTATE_VARIANTS.csv` 31개는 회전·미러 선언의 원문 추적이다. 102를 월드 렌더 검증 면 수로 오인하면 안 된다.

## 공식 검증 시도 및 한계 — F 보류

- 공개적으로 알려진 Mojang 메타데이터 경로 `https://piston-meta.mojang.com/mc/game/version_manifest_v2.json`와 버전별 `downloads.client` 정보를 확인하려 했으나 본 실행 환경은 직접 공식 도메인 요청에서 DNS 해석 불가/웹 접근 불가로 공식 `client.jar`를 취득하지 못함.
- 외부 GitHub 미러의 매니페스트 기록/제3자 다운로드 색인은 원본 Mojang 응답의 **대체 인증이 아니다**. 특정 SHA-1이 웹에 기재되어 있어도 이 채팅에서 JAR 바이트를 실제 해시하지 않았다.
- `VERIFY_OFFICIAL_JAR.py`는 공식 manifest→version JSON SHA-1→JAR SHA-1+size→ZIP의 단계 17개 텍스처 PNG SHA-256, 그리고 보조 끝면 2개를 확인하기 위한 **실행 가능한 오프라인 검사기**다. 현재 JAR 입력이 없어 실행 검증값은 없다. **이 스크립트 존재 자체가 공식 인증을 뜻하지 않는다.**

## 다음 작업 TEX02-R003

- 우선 Mojang HTTPS에서 다운로드된 신뢰할 수 있는 `manifest`, 1.21.11 version JSON, `client.jar`을 확보하고 검사기를 실행. 해시와 실제 JAR PNG가 일치하는지 파일별 `official` 상태를 전환할 것.
- 실제 게임의 **정적** 같은 재질 옆면·끝면·90/180도 회전·미러 변형을 같은 조명에서 비교하고 좌/우·상/하 이음새를 검증. 인게임 렌더/조명은 현재 0건.
- 모든 검증은 `STATE.json`의 최신 번호/파일 SHA/HEAD를 읽고 충돌 없는 새 독립 경로에 저장. 기존 TEX02-R001 및 전체 `v38` 변경 금지. 애니메이션·Project Zomboid·가구 모델 제작 범위 밖.

### 재현성/출처

- 고정 17: [STATE](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/stages/1-1-02/STATE.json) / [TEX02-R001 보고서](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R001/REPORT.md)
- 미러 PNG: `https://github.com/InventivetalentDev/minecraft-assets/blob/7241a12cc2707abd7022f399c5d9033153e492e1/assets/minecraft/textures/block/deepslate_top.png`, 같은 경로의 `blackstone_top.png`
- Model/Blockstate: 동일 ref의 `assets/minecraft/models/block/*.json`, `assets/minecraft/blockstates/*.json`.
- 픽셀 Y=`0.2126R+0.7152G+0.0722B`; RGB/alpha/Pillow 디코드. Git blob SHA와 파일 SHA256은 별도.
