# v66 — P1 원본 모델 JSON 직접판독 544/544 + v33 암시 UV 148면 및 v38 선반 38면·24규칙 독립 재검증

> 2026-11-15 KST · Minecraft Java 1.21.11 추출본 · 연구 시작 GitHub main `8368ecf760dc2f60c53f8943c5f021f3b3b9951d`. **1-2-A와 1-2는 진행 중.**

## 1. 기존 '역사 원본 SHA만 있음' 28개 모델을 실제 GitHub 원본 JSON으로 직접 재검증

v65 `04_SOURCE_REVIEW_LEDGER_544.csv`의 **v35~v63 원본 JSON 직접 판독 근거가 없고 선택 역사 원본 CSV 모델 SHA 행 근거만 있었던 28개 모델**을 새로 직접 열었다. **28개 모두 실제 원본 `1.21.11/assets/minecraft/models/block/*.json` Git blob SHA가 v65 P1 모델별 path+SHA와 일치**했고, JSON 파싱 후 자체 elements·faces·face UV 출처·zero-thickness·회전 요소와 parent 구조를 추출했다.

| v66 새 직접 재검토 범위 | 실측 |
|---|---:|
| 원본 JSON 파일 경로 | **28개** |
| 파일 자체 원본 elements | **37개** |
| 파일 자체 faces | **164면** |
| 파일 자체 명시 UV faces | **164면** |
| 파일 자체 UV 미지정 faces | **0면** |
| 두께0 원본 요소 | **10개** |
| 회전 원본 요소 | **8개** |
| **자체 element가 전혀 없는 모델** | **13개** |

상속 부모 기하 또는 특수 렌더러 영역의 모델도 포함되므로 **원본 자체 요소0 ≠ 실제 게임에서 물체가 없음**. 공식 엔진/인게임 런타임 검증이나 28개의 최종 상속 체인을 전부 인증한 건 아니다.

기존 **516개**의 v35~v65 누적 명시 직접 판독 경로에 이번 새 **28개 고유 경로**를 더해 **P1 544/544 모델 JSON의 실제 원본 경로+Git SHA 직접 조회 이력**을 확보했다. 모델 **신원 식별은 원래 544/544였으므로 신규 모델 신원 발견은 0개**. 544/544는 모델별 전체 기하·PNG·방향·게임 렌더 최종 확인 비율이 아니다.

증거: `00_DIRECT_SOURCE_PRIOR28_AGGREGATE.json`, `00_DIRECT_SOURCE_BATCH_1…4_PRIOR28.json` (원본 28 JSON, Git SHA, 요소·면·명시 UV와 부모 정보).

## 2. v33 — 12개 모델의 암시적 UV 148면을 원본과 독립 비교

과거 원본 CSV `research/vanilla_models/v33/02_twelve_model_148_inferred_uv_faces.csv`(Git SHA `e80591d98edacf2794ad8ebf37976ab6666843f0`)의 각 행을 cauldron·hopper·hopper_side·composter 및 contents1~7/ready 등 **12개 실제 원본 모델 JSON과 다시 대조**했다.

**148면의 원본 model SHA, element.from/to, 면 존재·방향, 원본 UV 키 없음, source texture slot/해결 경로, cullface, 회전, tint, UV 면적 및 방향별 기하 공식으로 계산한 UV 후보**를 행별 확인해 총 **10분야 × 148면 모두 일치**, 이 라운드 불일치0. `00_V33_12_MODELS_148_IMPLICIT_UV_RECHECK.json`에 원본 모델 SHA·행번호·원본 좌표·계산한 좌표·각 항목 결과를 저장.

**중요:** 148면은 실제 소스에 `uv` 필드가 **없다**. 여기 기록한 UV 사각형은 **원본 요소 좌표로 독립 계산한 후보**, Minecraft 엔진 자체의 암시 UV 계산 알고리즘을 실행해 인증한 결과가 아니다. 과거 v33 계산의 일관성 확인이지 148개가 공식 UV로 확정됐다는 뜻이 아님.

## 3. v38 — 선반 원본 명시 UV 38면·블록상태 24규칙·32정적 상태 검증

원본 `oak_shelf`와 관련 모델 leaf **7개**, parent template **7개**, 총 **14개 원본 모델 JSON SHA/내용**을 실제 열어 과거 `v38/02_oak_shelf_38_original_declared_faces_explicit_uv.csv`의 **38행 × 17검사 항목**을 독립 대조했다. leaf별 정확한 이름/원본 SHA, 부모 모델 SHA, from/to, source explicit face UV, 역방향 UV, cullface, zero thickness, 텍스처 슬롯, 이전 PNG 기록 SHA와 2배 해상도 UV 픽셀 경계·면적 계산 모두 일치. 잘못된 mismatch가 생기지 않도록 각 행의 `leaf_name`으로 leaf 모델 경로를 정확히 구분했다.

원본 `blockstates/oak_shelf.json`의 **24개 multipart 규칙**과 과거 v38 CSV 24행을 직접 대조해 오류 0. 정적인 `facing 4 × powered 2 × side_chain 4 = 32조합`에 원본 when 조건을 평가하면 **매 조합 본체1 + 덧붙임1 = source apply 2개**, 적용 원본 면 기록 **15+1=16면/상태(컬링 이전)**.

| 서로 다른 선반 소스 모델군 | 원본 명시 UV |
|---|---:|
| 본체 template_shelf_body | **15면** |
| 상태 덧붙임 template 5종 | **5면** |
| 인벤토리용 template_shelf_inventory | **18면** |
| **전체 과거 template 기록** | **38면** |

**특히 과거 38면은 월드에서 동시에 표시되는 38면이 아니다.** `template_shelf_inventory`의 18면은 blockstate 24개 규칙에 참조되지 않는다. 상태별 16면은 **엔진 컬링·실제 보이는 면 수·광원 처리 이전의 원본 apply 참조 면 합산**이다.

원본 `oak_shelf.png` **Git SHA `2dd79677605cdc90a3473931f6f6cdb66d423f7c`, IHDR 32×32** 직접 대조. 과거 v38 PNG 픽셀 표의 샘플 픽셀 수·UV 사각형 산술 검증은 했지만 **v66에서 원본 PNG RGBA 전체를 다시 Pillow로 픽셀 복호화하지 않았다**. 원본 마크 클라이언트/UVLOCK 런타임 검증하지 않음.

증거: `00_V38_OAK_SHELF_38_FACE_24_STATE_32_COMBINATIONS_RECHECK.json`, `01_ORIGINAL_SOURCE_FACE_CROSSCHECK_186.csv`, `02_OAK_SHELF_STATIC_32_STATES.csv`.

## 4. 실제 갱신 범위·과장 금지

- 총 **54개 서로 다른 기존 P1 원본 모델 JSON** 직접 재조회 = v33 12 + v38 14(leaf7+template7) + 과거 history-only28. 그중 신규 고유 직접 판독 등록 **28**, 기존 직접판독 26개는 재검증. 고유 P1 원본 모델 **544/544 직접 소스 파일 조회 이력 충족**, 신규 모델 식별0.
- 모델별 누적 P1 원장 **544행×337열 → 544행×351열**, v65 기존 **337×544=183,328 데이터셀 전부 값 보존**.
- 보조 모델별 source review **544행×37열 → 544행×48열**, 이전 **37×544=20,128 데이터셀 전부 보존**.
- v65의 과거 v5~v43 연구 **194파일 전부 원본 내용 재조회** 이력 그대로 유지. 과거 기록 전체 **의미론 검증 완료 아님**.
- 1-1 승인150/150 유지. 상위 5대 단계 중 1개 완료, **1-2-A와 1-2는 진행 중·실질 완료율 미산정**. 실제 마인크래프트 가구 모델 제작/좀보이드 맵 변환 작업 미착수.
- 특수 블록/블록 엔티티 렌더러 예외14, 암시 UV 엔진 공식, 상속/상태/PNG 전수 확인 등 **아직 해결할 항목은 남음**. 바닐라 원본 모델 JSON 조회 범위가 100%라고 그 다음 학습 단계까지 완료 선언 금지.

다음 작업과 제한사항은 `NEXT_CHAT_HANDOFF.md` 및 `08_OPEN_ISSUES.md`. 최종 연구/검증 커밋은 원격 readback 이후 `VALIDATION_POST_RESEARCH_COMMIT.json`에 기록.
