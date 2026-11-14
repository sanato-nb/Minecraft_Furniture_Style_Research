# v45 — 1-2-A 역사 연구 SHA 교차 확장 + 아카시아 선반 원본 7모델 검증

> **2026-11-14 KST** · 사용자 제공 Minecraft Java 1.21.11 추출본 · 작업 시작 main `1d851a539f926177f5cf68300c844a799dadbd23`. v1–v44 자료는 삭제·덮어쓰기 없이 보존.

## 1. v44와 구분되는 이번 실제 작업

- v44의 P1 544행 원장과 110개 기존 정확한 SHA 연결은 **그대로 계승**하고 별도 `v45/01_P1_544_MODEL_VERIFICATION_LEDGER.csv`로 확장했다. 544개 모델 개별 행에서 새 검증 상태, 기존 근거 계승, 보류를 분리한다.
- v44에서 선택했던 역사 연구 CSV 17개와 **중복되지 않는 v5~v34 연구 CSV 86개를 실제 열어** `SHA/hash/blob/git` 컬럼의 40자리 Git blob SHA를 v44 P1 원본 SHA와 비교했다. 파일별 경로/Git blob SHA와 검사 방법은 `06_HISTORICAL_86_CSV_SHA_SCAN.csv`에 고정. **이것은 아직 모든 Markdown/JSON 서술형 기록을 해석한 연구가 아니며**, SHA 없는 이름 참조까지 누락됐다고 판정하지 않는다.
- 추가로 복원한 이전 연구 증거: [v30 기존 원본 기록](../v30/08_anvil_three_leaf_top_texture_overrides.csv)의 **`chipped_anvil.json`, `damaged_anvil.json`** 두 개가 동일 `models/block` 원본 경로 및 SHA로 연결된다. `anvil.json`은 이전 v44와 중복이므로 재계산하지 않는다. 이 **2개는 과거 증거 회수**, 이번에 새롭게 원본 기하 실측한 모델이 아니다.

## 2. 신규 직접 소스 검사: 아카시아 선반 7 leaf

원본 `1.21.11/assets/minecraft/models/block/acacia_shelf*.json` 7개를 직접 열고 v44 P1 SHA와 **7/7 동일**함을 확인했다. 대상은 기본, center, inventory, left, right, unconnected, unpowered.

- 7개 leaf 모두 `elements` 직접 선언 **0개**. 부모는 각각 `template_shelf_body/center/inventory/left/right/unconnected/unpowered`.
- leaf 슬롯 `textures.all=minecraft:block/acacia_shelf`, `textures.particle=minecraft:block/stripped_acacia_log`. particle는 원본 면 텍스처 `#all` 사용과 구별한다.
- 부모 템플릿 원본 JSON **7개 재열람 / SHA 7개 일치**. **v38에서 이미 분석한 오크 선반과 완전히 동일한 템플릿 원본 SHA**, 따라서 새로운 원형 연구 실적은 **0개**로 분리한다. 재사용한 부모의 선언 기하는 총 **11 elements, 원본 명시 UV face 38, 암시 UV face 0, 0두께 요소 5, 회전 요소 0, cullface 면 23**. 이는 7 leaf의 별도 원본 선언 38면이 아니라 *기존 템플릿 공유 구조*다.
- 원본 `1.21.11/assets/minecraft/blockstates/acacia_shelf.json` SHA `b622ec8a2c3755ce2fdbfb1dc44cf9017902924c`를 읽어 **multipart 규칙 24개** 확인. `facing 4 × powered 2 × side_chain 4 = 32` 파생 정적 조합을 평가해 **각 조합에서 본체+전면 2모델**, 총 **64 상태별 모델 적용**이 나옴을 검증. inventory leaf는 world multipart 적용 모델이 아님.
- 원본 `uvlock` 키는 24규칙에서 **부재**; false가 명시되었다고 변환하지 않는다. 면 UV는 부모 원본 명시값이며 **이번 새 PNG RGBA·텍셀 직접 측정 0건**. 실제 게임 렌더/엔진 상태·컬링 미검증.

## 3. 중복 제거 후 현행 상태

| 구분 | v44 | v45 |
|---|---:|---:|
| P1 후보 전체 | 544 | 544 |
| P1 SHA 연결 모델 (원본 경로 기준 고유) | 110 | **119** |
| 위 검사 범위에서 SHA 미연결 | 434 | **425** |
| 추가 역사 연구 CSV SHA필드 확인 | — | **86파일** |
| 이전 연구에서 새로 회수한 연결 | — | **2모델** |
| 이번 새 원본 leaf JSON 검사 | 0 | **7모델** |
| 새로운 선반 기하 원형 | — | **0개 (v38 부모 재사용)** |
| 신규 원본 PNG 픽셀 실측 | 0 | **0개** |
| 1-2 전체 기하·UV·상태·PNG 완료율 | 미산정 | **미산정** |

`110 + 2 + 7 = 119`은 **원본 SHA 근거가 있는 고유 모델 수**일 뿐 모든 기하·UV·blockstate 심층 연구를 마친 수가 아니다. 425개도 미분석 확정 수가 아니라 현재 조사한 근거에서의 SHA 미연결 수량이다.

## 4. 증거 및 다음 작업

- [544행 모델별 상태 원장](01_P1_544_MODEL_VERIFICATION_LEDGER.csv)
- [9개 신규 연결 증거](02_NEW_EVIDENCE_LINKS_9.csv)
- [아카시아 leaf 7개](03_ACACIA_LEAVES.csv)
- [부모 템플릿 7개 검증](04_PARENT_TEMPLATE_VERIFICATION.csv)
- [원본 multipart 24개와 파생 32개 조합](05_ACACIA_MULTIPART_AND_STATES.json)
- [추가 86 CSV SHA 필드 감사](06_HISTORICAL_86_CSV_SHA_SCAN.csv)
- [미해결/오탐 원장](07_ISSUES.csv)
- [검증 요약](SUMMARY.json) · [다음 채팅 인계](NEXT_CHAT_HANDOFF.md)

**미검증:** v5~v43의 남은 서술형 Markdown·JSON의 근거/이름 참조 전수 연결, 원본 PNG 픽셀 샘플링, 특수 렌더러·게임 엔진 동작. 자산 비교 키는 `(asset_type, full_source_path, git_blob_sha)`. v43의 `chiseled_bookshelf`와 `oak_shelf`의 모델 vs blockstate 이름 충돌 **2건 정정 상태 유지**.

**프로젝트 상위 완료 1/5 유지.** 1-1 바닐라 텍스처 v42의 승인 소스 150/150 완료 유지. 공식 압축 client.jar 인증·인게임 렌더 실증은 이번 단계 필수 완료 조건에서 제외됐으며, 실제 수행하지 않았다. 실제 Minecraft 가구 제작 및 Project Zomboid 변환은 시작하지 않았다.
