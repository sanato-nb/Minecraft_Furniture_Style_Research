# INT-5-B23+B24 — 여러 연구 묶음 실제 진행(원형 렌더 10실험 + 전수 45요소 의미·UV 근거)
작성 2026-11-26 KST · 부모 [B22 원형 source5+source6 실게임 PR #134](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/pull/134) · **한 번에 여러 독립 연구 작업을 처리하되 완료 수치와 승인 등급은 분리**.

## 1. 이미 확정된 증거에서 출발
- 공식 Minecraft 1.21.1 Fabric, Another Furniture 4.0.2 release SHA1 `c2f992081bdc4795ed6d87771a3b5f7c71103785`.
- B19 45/45 원본 요소 단독 제거 수행, 원본 전체 의자 화면에서 **43/45** 한정 픽셀 변화, AF121·AF123 source index5 각각 **4방향 0픽셀**.
- B20 전체 상속 전개/역방향 X 정렬은 4카메라 **0픽셀**. B21 원본5 단독은 실제로 가시. B22 원본5+6 pair는 원본6 단독 대비 AF121 **378/284/378/284**, AF123 **302/0/176/137** 픽셀 변화. 따라서 source6 하나만으로 원본5를 완전히 숨긴다고 주장할 수 없음.

## 2. B23: 5개 원본 가림 맥락을 10개 독립 CI 병렬 작업으로 일괄 실험
실험 target **AF121_5 + AF123_5**, 각 target마다 아래 **5개 컨텍스트**. 전체 **10개 CI job, 20개 실제 Fabric 클라이언트, 320장 네이티브 F2**, 각 클라이언트 남/북/동/서 4방향 × 원본의자 이전·음성대조·원본의자 복원·빈 의자/AF123 합법 윗반블록만 4상태.

| 맥락 ID | 별도 원본 부모 요소 구성 | 의미 연구에 대한 주의 |
|---|---|---|
| `legs_0_3` | 0,1,2,3 | 기존 B3의 `LEG_OR_LOWER_POST` 가설을 보존, 구조만 선택 |
| `seat_4` | 4 | 기존 B3의 `SEAT_LAYER` 가설을 보존 |
| `back_7_9` | 7,8,9 | `BACKREST_ASSEMBLY` 가설을 보존 |
| `front_0_4` | 0,1,2,3,4 | 다리 가설+좌판 가설의 원본 기하 결합 |
| `all_others` | 0,1,2,3,4,7,8,9 | 원본 10요소 **전체 의자 재구성과 5만 없는 9요소 모델**을 재현, B19 0픽셀의 재확인 |

모든 그룹에 원본 **index6 필수 포함**, 같은 조합에서 **index5 없이/원형 index5 포함** 두 독립 게임 client 비교. 원본 부모의 10요소/46면, source5 역방향 X·4면, source6 원래 4면, 각 선택 요소의 순서·face·UV·texture bind는 고정. disposable child JSON **한 JAR member만** 변경, 원본 부모와 나머지 ZIP 모든 리소스 그대로, 같은 공식 초기 월드 별도 복원. 원본 JAR/수정 JAR Git 업로드/배포 금지.

**코드:** `src/mcfr/int5_b23_multigroup_source5_context_f2.py`; **안전 회귀:** `tests/knowledge/test_int5_b23_multigroup_source5_context_f2.py`; **병렬 원본 CI:** `.github/workflows/integration-int5-b23-fivecontext-10job-batch-320-f2.yml`.

**엄격 판정:** 32장 F2·게임 로그 2·서버 의자32 (AF123은 합법 지지 반블록32) 원본 SHA와 실제 게임 로그 마커 일치, 원본 모델 전후 픽셀차 동등, 음성대조 0/A-A 시간변화 0/화면 기여 픽셀 의자 foreground 집합 밖 0. 양성 및 음성 결과를 모두 기록하고, 무효 반례는 CONDITIONAL. **음성 결과가 부품이 물리적으로 없거나 스타일·재질이 밝혀졌다는 의미는 아님**. 모든 잡 완료 후 독립 ZIP 10개를 재계산해 추가 판정 및 원장 반영.

## 3. B24: 의미 연구를 기다리지 않고 원본 45요소 전체를 동시에 재검수
기존 실증 파일을 **원본 그대로 직접 읽음**: `INT5_B3_45_PART_ROLE_TEXTURE_CUE_DECISIONS_V1.csv` 및 `INT5_B22_FOUR_MODEL_45_ELEMENT_STATUS_V1.csv`. 원본 4모델 **AF121 10/AF123 10/HC11210 13/MACAW67 12**, 45요소 총 **229 source faces**.

| 구분 | 확인된 B3 원본 개수 | 현재 증명 수준 |
|---|---:|---|
| `LEG_OR_LOWER_POST` | 16 | 역할 **가설** |
| `SEAT_LAYER` | 6 | 역할 **가설** |
| `LOWER_FRAME` | 7 | 역할 **가설** |
| `BACKREST_ASSEMBLY` | 16 | 역할 **가설** |
| 이름/콘트라스트가 구분되는 source texture cue | 10 | 역할 기능 증명이 아닌 **단서** |
| 공용 텍스처, 분별 역할 단서 없음 | 35 | **약한 단서** |

[45요소 부품별 증거·보류 이유 원장](INT5_B24_45_PART_ORIGINAL_SOURCE_ROLE_SEMANTICS_EVIDENCE_REVIEW_V1.csv)에 각 요소의 원본 텍스처 SHA, 가설, B19 개별 제거에 따른 원본 F2 반응, B21/B22 원형 검증, 누락된 필수 이미지·부품 의미·재질 및 권리 근거를 **원본 소스에서 독립 교차 표출**. 원본 AF 모델 소스 4.0.3 vs 실제 정식 클라이언트 4.0.2의 byte-equal 여부는 미검증 상태 유지.

**독립 코드:** `src/mcfr/int5_b24_role_evidence_batch.py`, `tests/knowledge/test_int5_b24_role_evidence_batch.py` 6개 음성/부당승인 검증, 별도 GitHub Actions `.github/workflows/integration-int5-b24-role-45part-independent-source-audit.yml`에서 원장을 재생성하고 Git에 커밋된 45개 행과 직접 비교.

## 4. 완료 정의
- B23: 10개 원본 CI 잡 및 두 target×5맥락 실제 PNG·log ZIP 원본 다운로드 CRC/SHA/게임 blockstates/각 4방향 픽셀 독립 재감사하고 원장 추가할 때만 해당 배치 **완료**.
- B24: 45부품·229면 전체 재생성 및 6개 반례시험+Git 커밋된 45행과 독립 CI 일치 시 **증거 범위 정리 완료**. **의미 승인 45/45라는 뜻은 아님**.
- 최종 INT5 연구: 부품 기능·재질·스타일 **0/45 승인 유지**, GPU 개별 face/UV 독점 픽셀 귀속 승인0, 제삼자 AI 학습/재배포 권리 승인0, H03 HOLD / H05 CONDITIONAL / 엄격 F70 무조건 0/70, `main` 병합 금지/stacked Draft PR 유지.

## 5. CI 상태 추적
- [B23 실게임 10-job Actions #45781317951](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45781317951) — **원본 320 F2 실험 실행**, 본 파일에 검증 전 결과 숫자를 넣지 않음.
- [B24 45-element 독립 CI](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions) — 최종 통과 전인 항목은 PASS로 승격하지 않음.

