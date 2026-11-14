# 1-1 현재 완료 현황 — 정본 v42 (2026-11-14)

> **[전체 프로젝트 현재 진행도](../CURRENT_PROJECT_STATUS.md)** · 본 문서는 완료된 1-1 세부과제의 자료만 관리하며, 현재 다음 과제는 1-2다.

**Minecraft Java 1.21.11에서 지정한 텍스처 150개 / 재질 11개 분류의 승인된 소스 연구 완료 150/150.** 전역 상위 세부과제 완료는 **1/5**이며 1-2~1-5 연구는 별개다. 전체 블록 PNG 1,111종을 전수 분석했다는 주장이 아니다.

[v42 통합 보고서](../../research/vanilla_textures/integrations/v42_INT-1-1-11steps_150_SOURCE_COMPLETE/REPORT.md) · [150종 고유 ID 추적 원장](../../research/vanilla_textures/integrations/v42_INT-1-1-11steps_150_SOURCE_COMPLETE/TEXTURE_150_SCOPE_LEDGER.csv) · [단계 원장](../../research/vanilla_textures/integrations/v42_INT-1-1-11steps_150_SOURCE_COMPLETE/STAGE_INTEGRATION_LEDGER.csv) · [독립 재감사](../../research/vanilla_textures/audits/2026-11-14_v42_scope_verification/REPORT.md)

## 분류별 최종 연구

| 번호 | 분류 | 고정 PNG | 최종 버전 | 최신 근거 |
|---|---|---:|---|---|
| 1-1-01 | 목재·원목 | **18/18** | `TEX01-R008` | [STATE](stages/1-1-01/STATE.json) · [보고서](../../research/vanilla_textures/by_stage/1-1-01/TEX01-R008/REPORT.md) |
| 1-1-02 | 석재·벽돌 | **17/17** | `TEX02-R017` | [STATE](stages/1-1-02/STATE.json) · [보고서](../../research/vanilla_textures/by_stage/1-1-02/TEX02-R017/REPORT.md) |
| 1-1-03 | 금속·금속부품 | **16/16** | `TEX03-R008` | [STATE](stages/1-1-03/STATE.json) · [보고서](../../research/vanilla_textures/by_stage/1-1-03/TEX03-R008/REPORT.md) |
| 1-1-04 | 직물·양털 | **9/9** | `TEX04-R009` | [STATE](stages/1-1-04/STATE.json) · [보고서](../../research/vanilla_textures/by_stage/1-1-04/TEX04-R009/REPORT.md) |
| 1-1-05 | 유리 | **6/6** | `TEX05-R008` | [STATE](stages/1-1-05/STATE.json) · [보고서](../../research/vanilla_textures/by_stage/1-1-05/TEX05-R008/REPORT.md) |
| 1-1-06 | 도기·유광도기 | **8/8** | `TEX06-R008` | [STATE](stages/1-1-06/STATE.json) · [보고서](../../research/vanilla_textures/by_stage/1-1-06/TEX06-R008/REPORT.md) |
| 1-1-07 | 콘크리트·색면 | **7/7** | `TEX07-R008` | [STATE](stages/1-1-07/STATE.json) · [보고서](../../research/vanilla_textures/by_stage/1-1-07/TEX07-R008/REPORT.md) |
| 1-1-08 | 복합·기능면 | **21/21** | `TEX08-R008` | [STATE](stages/1-1-08/STATE.json) · [보고서](../../research/vanilla_textures/by_stage/1-1-08/TEX08-R008/REPORT.md) |
| 1-1-09 | 토양·지면 | **9/9** | `TEX09-R008` | [STATE](stages/1-1-09/STATE.json) · [보고서](../../research/vanilla_textures/by_stage/1-1-09/TEX09-R008/REPORT.md) |
| 1-1-10 | 잎·식생 | **8/8** | `TEX10-R014` | [STATE](stages/1-1-10/STATE.json) · [보고서](../../research/vanilla_textures/by_stage/1-1-10/TEX10-R014/REPORT.md) |
| 1-1-11 | 목재·구조부품 | **31/31** | `TEX11-R013` | [STATE](stages/1-1-11/STATE.json) · [보고서](../../research/vanilla_textures/by_stage/1-1-11/TEX11-R013/REPORT.md) |
| **합계** | **11개** | **150/150** | **v42** | |

## 검수 결과와 범위 한계

- **실제 GitHub 원본 블록 텍스처 디렉터리에서 150개 경로 모두 존재**, 단계별 증거 CSV의 Git blob SHA-1과 **150/150 일치**, 단계별 STATE/REPORT/SUMMARY Git blob 고정 SHA **33/33 일치**. 원장의 ID·경로·기록된 SHA256 불일치 0.
- 단, 독립 재감사에서는 PNG 바이너리 **150개를 재디코딩하여 SHA256·CRC·픽셀 계산을 전량 재실행하지는 않음**. 이 완료 판정은 기존 소스 연구 근거와 Git 파일 동일성 교차검증 범위다.
- 공식 Mojang 압축 JAR 인증 및 실제 인게임 렌더/런타임 동작 검증은 사용자 지시로 **필수 완료 조건에서 제외**되었고, 실제 검증 성공은 주장하지 않는다.
- 애니메이션 원본 소스는 9개 분류(01,03,04,05,06,07,08,09,11)에서 재개됐고, 02·10은 별도 보류. 게임상 움직임을 재현했다는 뜻이 아니다.
- v41의 목재·원목 0/18은 **낡은 완료 상태 수치로 인한 집계 오류**로서 기존 R001–R008 근거를 확인해 **18/18**으로 바로잡았다. 중복 신규 실측이나 새 TEX 버전은 생성하지 않았다.

## 과거 문서와 후속 작업

- `1-1-NN_재질.md` 11개는 **v38 최초 연구계획의 이력**. 문서에 남은 A–G/D1–D3 설명과 당시 v4 상태 문구는 지금 미완료 TODO가 아니다.
- v39(석재 제외 133종), v40(전종 150종 최초 통합), v41(석재 R017 갱신)은 **과거 연구 스냅샷**. 과거의 "최신", "0/5", "132/150"은 현재 값이 아니다.
- 다음 실제 과제는 **1-2 바닐라 모델 JSON·UV·blockstate 연구**. [새 채팅 시작](../NEW_CHAT_START.md) · [1-1 단계별 상태 바로가기](NEW_CHAT_LAUNCHER.md) · [전역 진행도](../../PROGRESS.md).
