# TV-001 결함 보완 최종 심사 — 2026-11-28

**보완 작업 A–E 종료 / TV-001 전체 CLOSED_PARTIAL.** 본 연구 시작 아님.

기준: 기존 [보완 계획](TV001_CORRECTION_PLAN_2026-11-28.md), v1.1, 원본 main `176f7f34de2336eb7984c4734e97b6eb156c19f4`, 검증 코드 `18710783ebd4507dc908a4dad6adddd6cbbabc45`. 사례 12개, PNG 25개 유지.

## D. 실제 검증
- [렌더 회귀 #46120638219](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/46120638219), job 140904150444, artifact 15253965840: success.
- R03-inner 실제 Blender mesh: 15/15 면, 60/60 좌표쌍, 음성 대조군에서 변경 대상 11/11 면 불일치 검출. 고정 x=180/y=0/uvlock=true, 명시 UV/면 자체 회전 0에 한정.
- 기본 PNG 및 독립 실루엣 25/25, P06 방향성 PASS, 12→13→0 재개, T8 집계 회귀 14/14.
- [원본 바이트코드 #46120638204](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/46120638204) success, 14개 클래스. [기존 하네스 #46120638240](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/46120638240) success, 단위 테스트 28/28 및 H0/H1.

## E. T0 기존 기능 재사용 감사
v1.1의 T0는 모듈 재사용 검토이지 운영 DB 통합 구현을 요구하지 않는다. 네 소스 본문, Git blob 및 실제 단위 테스트 로그를 대조했다. 검토 4/4 완료, 통합은 미실행.
| 모듈 | 재사용 가능 | 한계 |
|---|---|---|
| research_db.py | release/asset/run registration, schema v4, transactions and read-only access | does not store complete new 14-area research knowledge; schema redesign deferred |
| research_engine.py | plan_run scope hash, incremental selection, directory/archive pin verification, source hashing | inspect_asset only JSON top-level keys and PNG IHDR, not a model/UV resolver or full image validation |
| source_jobs.py | 64-asset SQLite source checkpoints and identity validation, reopen/resume | source asset scans, not Blender output; cross-Job restoration not proven |
| visual_check.py | pinned single-frame RGBA PNG comparison, size and changed-pixel counts | requires independent comparable PNG; does not supply Minecraft ground truth |

## 종료 판정
| 단계 | 결과 |
|---|---|
| A | PASS |
| B | PASS (정적 원본 기준) |
| C | PASS (고정 R03 메시) |
| D | PASS (고정 회귀, 전면 정확성은 미검증) |
| E | 종료 심사 완료, CLOSED_PARTIAL |

T0 재사용 검토 PASS(통합 미검증), T1/T2/T3/T6/T7 기존 제한 범위 PASS, T4 PARTIAL, T5 범위 제외, T8 CLOSED_PARTIAL. 기존 자동 T8 로그는 T0 미통합과 UVLOCK 결함을 설명하는 과거 고정 문구가 남아 있으므로 실제 R03 수정 결과 및 T0 검토 판정은 본 심사로 구분한다. 기존 자동 로그 자체는 변경하지 않는다.

남은 한계: 25개 PNG 전체의 독립 텍셀 정확성 미검증, 다른 UV-lock 회전/형식 미지원, 서로 다른 Job 사이 재개 미검증. 모든 모델의 렌더링을 정확하다고 표시하지 않는다. 새 UV 검증은 별도 범위와 승인 대상. 운영 DB 통합/스키마 개편도 별도 단계. 다음은 기존 자료 품질 사전 조사, 범위 고정, 상세 계획 고정 순서다. 정확성이 확인되지 않은 렌더 결과에 근거한 디자인 확정은 금지한다.

[기계 판독 증거](TV001_CORRECTION_FINAL_EVIDENCE_2026-11-28.json). main 및 역사 자료 보존.
