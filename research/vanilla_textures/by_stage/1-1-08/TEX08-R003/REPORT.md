# TEX08-R003 — 사용자 제공 1.21.11 JAR 추출본 원본 출처 정정 및 4단계 증거 분리

**날짜:** 2026-11-13. **범위:** 1-1-08 복합·기능면, 고정 PNG 21개. 전체 연구 버전 v38, R001/R002 불변.

## 핵심 결론

사용자가 직접 Minecraft Java Edition **1.21.11 client.jar을 압축 해제해 업로드했다고 밝힌** `1.21.11/` 폴더를 **1차 분석 원본**으로 채택한다. 이 진술과 **Mojang 공식 배포 JAR의 무결성 인증**은 구별한다.

| 증거 수준 | 확인 결과 |
|---|---|
| (1) 사용자 제공 추출본 확인 | Git tree의 **77개 고유 파일 경로/원본 blob SHA**: 목표 PNG 21 + 보조 PNG 1 + blockstate JSON 16 + 모델 JSON 39. 누락 0. |
| (2) 비공식 미러와 교차 검증 | 기존 R001/R002에 기록된 **71개 파일 해시 모두 동일**: PNG 21 + 보조 1 + blockstate 16 + 기존 모델 33. 불일치 0. 모델 6개는 기존 원장에 없으므로 교차검증 수에 **미포함**. |
| (3) Mojang 공식 JAR 인증 | **0/21 — 미검증.** 기존 JAR 압축본 전체 SHA1과 Mojang 메타데이터 실제 결합 대조 없음. |
| (4) 인게임 정적 렌더 확인 | **0/21 — 미검증.** 실제 Minecraft 실행·화면 관측 없음. |

Git blob SHA 동일은 각 파일 **바이트 동일성의 근거**이나, 동일하다는 사실만으로 공식 JAR 전체 SHA1을 인증하지 않는다. 원래 JAR을 압축 해제한 폴더에서 공식 JAR SHA1을 다시 계산할 수도 없다. `META-INF` 파일 존재만으로도 원본 유통 경로를 인증할 수 없다.

## A — 기존 실적을 보존한 새로운 출처 연결

원본 GitHub: https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/tree/main/1.21.11

추출본 `assets/minecraft/`의 Git tree SHA1:
- `textures/block`: `9a7172896d4a28b405b990733d51b77dcb50930c` (트리 엔트리 **1,210**).
- `blockstates`: `7a36f7d757e62aa61ee61aebcd8d5689bc462a8d` (트리 엔트리 **1,168**).
- `models/block`: `57eb7fbc4d0af0e931a04de94b4b6a766242d36e` (트리 엔트리 **2,390**).

이 숫자는 전체 폴더 **경로 모집단 규모이지 검수 완료 수가 아니다**. 해당 트리 중 77개만 이번 단계의 실제 출처 존재/파일 SHA 검사 대상이다.

R001 `SOURCE_LEDGER.csv`의 21 PNG, R001 `MODEL_UV_EVIDENCE.csv` 62면 원장에서 유일한 모델 15개, R001 `CHISELED_SLOT_UV.csv`의 슬롯 자식 12/템플릿 6, R002 `BLOCKSTATE_AUDIT.csv` 16개, R002 정적 보조 `barrel_top_open`까지 **기존 기록의 71 고유 해시를 전부 사용자 추출본에 연결**했다.

## B·C — 추출본 PNG 파일 검증, 이전 픽셀 재측정 불필요

사용자 추출본의 **21/21 표본 PNG Git blob SHA1**이 과거 미러와 바이트 동일성을 확인했다. 이번에는 그중 6개 + 보조 PNG 1개, 총 **7개 원본 PNG 바이너리를 GitHub에서 직접 불러 Base64 디코드**하여 PNG signature 및 첫 IHDR 청크, 16×16, bit depth 8, PNG 색형식 3을 확인했다. 각 바이트 길이와 출처 SHA는 `PNG_HEADER_DIRECT_READ.csv`에 기록했다.

**신규 RGBA 색상/휘도/알파 픽셀 측정 = 0.** 이전 R001에서 수행한 원본 미러 21 PNG 5,376픽셀 및 CRC·Adler·RGBA, R002의 정적 diff 결과를 다시 수행하지 않았고 새 실적에 중복 합산하지 않았다. 나머지 PNG 15개의 이번 증거 수준은 **Git 트리 SHA·기존 미러 SHA 동등성**으로 표시하며 직접 바이너리 재해독으로 부풀리지 않는다.

## D·E — 추출본 상태 JSON 16개 및 모델 JSON 추가 직접 검증

- 추출본 blockstates JSON **16/16 파일을 직접 읽고 JSON 파싱**해 합계 **73 variants + 52 multipart 규칙**을 확인. `barrel`은 12개 = closed6/open6, `beehive`는 honey_level 0..4:20 / 5:4, `chiseled_bookshelf`는 base 4 + 슬롯 조건 48(occupied24/empty24)이다. 일부 base 규칙에 `uvlock` 지정이 있으나 실제 렌더 방향 검증은 하지 않았다.
- R001 모델 실적 62 source-face 기록의 고유 모델 **33개**(leaf15, child12, template6)는 추출본 SHA가 모두 일치.
- 모델 6개 추가: `barrel_open`, `furnace_on`, `smoker_on`, `blast_furnace_on`, `beehive_honey`, `chiseled_bookshelf` 본체. 이들은 **이전 단계 모델 원장 밖의 '상태 선택 모델' 소스 확인**이며 미러 비교한 71개에 넣지 않았다. 사용자 추출본 모델 고유 출처 확인 총 **39종**.
- 실제 모델 파일을 **10개 골라 원본 JSON을 직접 파싱**: `barrel_open`은 `#top=barrel_top_open`, `beehive_honey`는 `#front=beehive_front_honey` 및 particle=`beehive_side`; `enchanting_table`은 측면 네 개 각각 명시 UV `[0,4,16,16]`; `template_chiseled_bookshelf_slot_top_left`는 명시 UV `[0,0,6,8]`; `chiseled_bookshelf` base는 별도 1 element/5 face 확인. 소스 목록 및 관측 슬롯은 `MODEL_DIRECT_READ.csv`에 저장.
- `smoker_on`과 `blast_furnace_on`에서 front 텍스처 **경로 문자열만** 확인했고, 프레임·키프레임·움직임을 **전혀 분석하지 않았다**.
- 신규 UV texel 측정 0. R001 62 source face 및 R002 13,056 texel-uses는 **이전 기록으로 보존**, 이번 추출본 교차검증 성과와 합산하지 않는다.

## F — 두 미완료 인증

(3) 공식 원본 배포: **원래 `client.jar`의 전체 SHA1 + Mojang 공식 버전 메타데이터 비교 미시행, 인증 0/21**. R002에 저장한 `VERIFY_OFFICIAL_CLIENT.py`는 향후 압축본을 확보할 경우 사용하며 이번에 실행 성공한 것으로 기록하지 않는다.

(4) Minecraft 실행: **게임 인게임 정적 표시·UVlock·회전·컬링·조명·particle 시각 검증 0/21**.

## G — 단계별 불변 기록

기존 `R001`, `R002` 원본 보고서/CSV/JSON/커밋을 수정·삭제·초기화하지 않았다. 신규 결과는 이 `TEX08-R003/` 아래에 `SOURCE_LEDGER.csv` (77 고유 경로), `BLOCKSTATE_DIRECT_READ.csv` (16), `MODEL_DIRECT_READ.csv` (10), `PNG_HEADER_DIRECT_READ.csv` (7), `SUMMARY.json`로 보존. 게임 원본 PNG/JSON/클래스/JAR 바이너리를 연구 산출물에 새로 복제하지 않았다.

차기 단계 `TEX08-R004`. 앞으로 사용자 제공 `1.21.11/`을 우선 분석하고 미러는 대조용으로만 사용한다. **애니메이션 연구 보류**, Project Zomboid 변환/3D 가구 제작 금지. 다른 단계 및 루트 체크포인트 변경 금지.
