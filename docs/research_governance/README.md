# Minecraft Furniture Style Research — 새 연구 운영 합의 및 인수인계

**기준일:** 2026-11-27  
**작업 흐름:** 기존 GitHub 역사 자료 보존 → 연구 설계 고정 → TV-001 기술 검증 → 기존 자료 품질 조사 → 바닐라 사전 조사 → 바닐라 본 연구 → 가구 모드별 독립 연구

이 폴더는 이전 대화에서 확정한 연구 방향·범위·데이터·작업환경·상태를 새 채팅에서도 이어서 활용하도록 만든 **통합 문서 색인**이다. 기존 main, 역사 문서 및 연구 원본을 직접 변경하지 않았다.

## 읽는 순서

1. **[전체 확정 사항 통합 기록](PROJECT_AGREEMENTS_2026-11-27_FULL.md)** — 사용자가 제공한 13개 장 전체 정리본을 원문 형태로 보존. 연구 목적·버전 정책·3개 사전 단계·14개 데이터 영역·검증·DB·하네스·작업환경·TV-001·향후 순서를 모두 포함한다.
2. **[연구 운영 계약 v0.6 — 합의 재구성](RESEARCH_CONTRACT_V0_6_RECONSTRUCTED.md)** — 사전 조사→상세 범위·계획 고정→실행→종료 심사, 범위 확장 금지, 증거·완료·보존 규칙을 추출한 작업용 문서.
3. **[연구 데이터 명세 v0.2 — 합의 재구성](DATA_SPEC_V0_2_RECONSTRUCTED.md)** — SQLite 중심 6개 개념 계층, 14개 데이터 연구 영역, 객관 데이터/추론 구분 및 AI 지식 색인.
4. **[TV-001 기술 검증 실행 계약 v1.1](../tech_validation/TV001_SCOPE_AND_EXECUTION_V1_1.md)** — 고정된 12개 사례·25개 오프라인 렌더링 및 독립 정확성 검증 기준.

## 실제 GitHub 실행 근거

- [TV-001 Draft PR #139](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/pull/139)
- [TV-001 성공한 GitHub Actions #45986960067](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45986960067)
- [25개 PNG·입력 매니페스트·체크포인트·로그 아티팩트](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45986960067/artifacts/15192365353)

**정확한 상태:** 12개 기본 사례 및 25개 PNG 생성·기본 검사는 통과했지만, 독립적인 형상·UV·상태 정확성 검증(T4)과 전체 종료 심사(T8)는 아직 미완료다. TV-001 전체 판정은 `PARTIAL`이며 연구 전수 완료가 아니다. Blockbench 웹 직접 조작과 유료 외부 AI API는 기본 연구 경로에서 제외한다.

## 문서 간 관계와 보존 원칙

- [전체 확정 사항 통합 기록](PROJECT_AGREEMENTS_2026-11-27_FULL.md)이 사용자 제공 자료의 원문 보존본이다. 원문에는 대화 화면에서 만들어진 외부 이미지 링크와 UI 표현도 포함되어 있을 수 있으며, 이는 연구 원본 데이터나 검증 근거가 아니다.
- v0.6과 v0.2 **재구성본**은 원문을 대화에서 재구성한 것으로, 이전 채팅에서 작성한 초안 문서의 바이트 단위 원본은 아니다. 이를 'GitHub에서 이전부터 존재한 원문'으로 오인하지 않는다.
- TV-001은 기존 PR 브랜치의 실제 스크립트·Actions가 포함된 실행 계약이며, 연구 범위를 임의 변경하지 않는다.
- 새 연구 정책과 일부 과거 README/상태 문서 사이에 차이가 있더라도 역사 자료를 임의 삭제·덮어쓰지 않는다. 기존 연구 완료 주장을 새 기준의 PASS로 자동 전환하지 않는다.
- **현재 이 문서들은 PR 브랜치에만 있으며 main에 병합되었다는 의미가 아니다.** 별도 검수·병합 여부는 이후 결정한다.

## 새 대화 시작 시 절차

1. 위 네 문서를 순서대로 확인한다.
2. PR #139의 현재 상태와 최신 CI 결과를 GitHub에서 직접 확인한다.
3. 기존 작업을 새로 구현하지 말고 부족한 범위만 찾아 이어간다.
4. 우선 **TV-001 T4 정확성 검증 → T8 전체 종료 심사**를 수행한다.
5. 그다음 기존 GitHub 자료 목록·품질 분류를 실시하고, 바닐라 연구를 위한 별도의 사전 조사·범위·계획을 잠근다.

## TV-001 T4/T8 종료 판정 (2026-11-28)

- [T4 독립 검증 및 T8 종료 심사 보고서](../../project/audits/tv001/TV001_T4_T8_CLOSURE_2026-11-28.md)
- [T4/T8 25개 렌더 증거 영구 요약 JSON](../../project/audits/tv001/T4_T8_2026-11-28_EVIDENCE_SUMMARY.json)
- [T4/T8 실제 성공 GitHub Actions #46032645107](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/46032645107)

**최신 종료 기록은 `CLOSED_PARTIAL`이다.** 25개 형상 투영 검사와 P06 투명 UV 방향성 검사를 통과했지만, `R03-inner`의 uvlock 미적용 및 전 면 텍셀 단위 독립 검증 부족으로 TV-001 전체 PASS는 아니다. 2026-11-27 작성 당시의 대화 정리본은 역사 기록으로 그대로 보존한다.
