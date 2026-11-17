# Minecraft Java 1.21.11 — 1-2-G 최종 종료 보고서

**2026-11-17 · 최종 판정: `G_COMPLETE_SOURCE_CROSS_STAGE_CONSISTENCY_SCOPE` (PASS 6/6).**

이 판정은 **사용자가 추출한 원본 Minecraft Java 1.21.11 소스의 A~F 출처·모델·blockstate·PNG·예외·스타일 증거 교차 일치**에만 적용한다. 공식 배포 JAR, 실제 게임 엔진 렌더·상태 레지스트리·애니메이션 재생, 좀보이드 개별 가구 정체 확정, Minecraft 맵 생성 완료 판정이 아니다.

## 직접 검증한 고정 모집단

| 자산 유형 | 파일 수 | 원본 bytes·Git SHA |
|---|---:|---|
| block model JSON | 2,390 | 2,390/2,390 |
| blockstate JSON | 1,168 | 1,168/1,168 |
| block texture PNG | 1,111 | 1,111/1,111 |
| **합계** | **4,669** | **4,669/4,669** |
| `.mcmeta` 원본 JSON (분모 밖) | 99 | 99/99 |

모델/B·C·F 기하 요소 **5,689**, face **23,090**(UV 명시 **18,808** / 키 생략 **4,282**; PNG 결합 face **21,590** / 템플릿 미바인딩 **1,500**). heavy_core 정정 **6면**은 기존 정정 근거와 대조했고 과거 원본에 덮어쓰지 않았다.

D 블록 상태 **1,168**: 원문 모델 옵션 **7,592**, 정적 문법 상태 **9,193**, 상태별 모델 옵션 적용 **19,440**, D 직접 모델 **2,136** / 미직접 **254**, E 모델 참조 **84** / 미참조 템플릿 **2**로 독립 재집계가 일치했다.

PNG **1,111개** 모두 원본을 재개방하고 Git SHA를 검산했다. 기존 C의 RGBA 검증 **1,073개**와 C 집합 밖 신규 G PNG **38개**를 구분했다. 메타데이터 sidecar **99개** 중 기존 C 연결 기록 **97개**는 소스 SHA와 일치했다. F3의 기존 시각 관찰은 **PNG 첫 프레임 332개·접촉시트 8장**, 모델과 PNG 직접 연결 **340개**, 미연결 모델 **38개**, 애니메이션 첫 프레임 범위 **16개**로 선행 관찰 증거로만 인정했다.

## 6회차 직접 원본 감사

| 회차 | 모델 | blockstate | PNG | 합계 | 최종 단계 판정 |
|---|---:|---:|---:|---:|---|
| Entry1 | 150 | 12 | 185 | 347 | PASS |
| Entry2 | 494 | 96 | 185 | 775 | PASS |
| Entry3 | 495 | 265 | 185 | 945 | PASS |
| Entry4 | 494 | 265 | 185 | 944 | PASS |
| Entry5 | 379 | 265 | 185 | 829 | PASS |
| Entry6 | 378 | 265 | 186 | 829 | PASS |
| **합계** | **2,390** | **1,168** | **1,111** | **4,669** | **6/6** |

각 회차별 원본 JSON·PNG는 직접 검증했고, 마지막 [전체 원본 별도 실행](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/44090818527)에서도 **4,669개 원본 bytes·Git SHA**를 독립적으로 다시 계산했다. 오류 **0건**, 모집단 중복·누락 **0건**. Entry6 [원본 실행](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/44089873718)도 성공했다.

## G1~G6 계약 종료 게이트

| Gate | 판정 | 근거 |
|---|---|---|
| **G1** 원본 경로·신원 | PASS | 타입·path·SHA 4,669/4,669, sidecar 99 |
| **G2** 모델·face·기하 | PASS | B/C/F 모델 2,390, E86, 요소 5,689, face 23,090, heavy_core 6면 |
| **G3** 상태·모델 조립 | PASS | D 1,168개/옵션 7,592/정적 상태 9,193/옵션 적용 19,440 |
| **G4** PNG·선행 시각 | PASS | PNG1,111/C1,073/G신규38, .mcmeta99, F3 PNG332·접촉시트8 |
| **G5** 예외·기존 자료 보호 | PASS | E 특수 renderer 미인증86, 템플릿 미바인딩1,500 등 단위 구분, A~F/v69 기존 파일 무변경 |
| **G6** 전체 독립·원격 검증 | PASS | 6회 전수 재집계, GitHub Actions 원본 재해시 4,669개, 원격 SHA/행수/본문 재검증 |

**중요한 F 선행 출처 공백:** `sculk_mirrored`, `stone_mirrored`의 공통 부모 `cube_mirrored.json`에 대해 기존 F parent_chain·geometry_provider SHA가 **2모델·4필드 공란**이었다. G에서 실제 원본 SHA `38f44bda128d10a5e09614e5ac155c956237681e`를 새로 계산해 [전용 보완 원장](../entry6/G_ENTRY6_PROVENANCE_GAPS.json)에 기록했다. 기존 F가 SHA를 이미 검증했다고 소급 주장하거나 F 원장을 수정하지 않는다. 두 모델의 소스 교차감사 완료와 과거 출처 공백 보존은 양립한다.

## 결과물과 검증 재현

- [최종 6게이트 판정 JSON](G_FINAL_EXIT_AUDIT.json)
- [독립 모집단·G1~G5 전제 재집계](G_GLOBAL_INDEPENDENT_RECOUNT.json)
- [전체 4,669개 원본 SHA 원장](G_FINAL_SOURCE_SHA_4669.csv)
- [99개 sidecar SHA 원장](G_FINAL_MCMETA_99.csv)
- [GitHub 원격 원본 SHA·행수 예비 검산](G_GLOBAL_PRE_FINAL_REMOTE_READBACK.json)
- [최종 보고·상태 파일 원격 재조회](G_FINAL_REMOTE_READBACK.json) — 최종 커밋 후 생성
- [Entry6 보고서](../entry6/G_ENTRY6_REPORT.md) / [한계 252행](../entry6/G_ENTRY6_UNRESOLVED_SCOPE.csv)

기존 A~F/v69 원본 파일과 이전 승인 **150/150**, 상위 완료 단계 **1/5**는 그대로 보존한다. Entry7 자동 생성 없음.

## G 이외 후속 단계

**1-2 전체 종료 여부**는 이 G 소스 감사 PASS와 **별개의 최종 심사**로 분리한다. 현 단계에서 전체 1-2 완료/모드 가구·마인크래프트 맵 구현 완료를 자동 승인하지 않는다. 사용자 추출 바닐라 원본 A~G 연구를 다음 설계의 출처 기반으로 재사용하되, 좀보이드 TMX·타일셋 의미·다칸 가구·Minecraft 렌더·모드 구현은 별도 근거와 검증이 필요하다.
