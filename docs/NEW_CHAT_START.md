# 새로운 ChatGPT 채팅 시작 — 최신 v44

> **현재 GitHub v44:** 1-2-A [544개 모델 SHA 근거 1차 검수](../research/vanilla_models/v44/REPORT.md) 완료, **A 전체는 미완료**. 다음 연구는 나머지 v5~v43 증거 파일 중복 재조정. [1-2 현재 인수인계](vanilla_models_1-2/CURRENT_STATUS.md) · [전용 새 채팅 안내](vanilla_models_1-2/NEW_CHAT_START.md).


> **1-2 연구 최신 문서:** [진행 상태](vanilla_models_1-2/CURRENT_STATUS.md) · [연구 계획](vanilla_models_1-2/WORK_PLAN.md) · [별도 새 채팅 지시서](vanilla_models_1-2/NEW_CHAT_START.md). 이후 작업은 이 인수인계를 사용하고 기존 v38 28 leaf 기준 설명을 최신으로 취급하지 말 것.

> **전역 최신 연구 v43 · 2026-11-14:** [1-2 crafter 원본 4 leaf / 48 source variants / 24 상속 face 연결, v36 SHA 유형 오탐 2건](research/vanilla_models/v43/REPORT.md). v35~v43 선택 회차 직접 leaf **28+4=32**, P1 544는 후보 분모이며 v5~v34 전체 역사 검수 완료는 아님. **1-1 v42의 150/150 완료 및 상위 세부과제 1/5 상태는 유지**. 아래 v42/v38의 '현재' 문구는 역사적 스냅샷. 공식 JAR/인게임 실증 미실시.


> **[전체 프로젝트 최신 진행도](CURRENT_PROJECT_STATUS.md)** · 1-1 완료(150/150), 다음은 1-2. 본 프롬프트 실행 전 GitHub 라이브 상태를 확인한다.

**완료:** 1-1 바닐라 재질·텍스처 소스 연구 **11/11단계·150/150종**. [정본](vanilla_texture_1-1/CURRENT_STATUS.md) · [독립 감사](../research/vanilla_textures/audits/2026-11-14_v42_scope_verification/REPORT.md) · [전체 상태](../handoff/STATE.json). **1단계 세부과제 1/5 완료**.

## 다음 채팅에 복사할 실행 지시

```text
Minecraft Furniture Style Research를 GitHub 최신 연구에서 이어가라.
저장소: https://github.com/sanato-nb/Minecraft_Furniture_Style_Research

1. handoff/STATE.json, HANDOFF.md, PROGRESS.md를 실시간 조회하여 최신 버전과 실제 완료 범위를 확인하라.
2. docs/vanilla_texture_1-1/CURRENT_STATUS.md와 research/vanilla_textures/audits/2026-11-14_v42_scope_verification/REPORT.md를 읽고, 1-1 선정 150종 소스 연구 결과를 완료 자료로 계승한다. 기존 PNG/UV/TEX 릴리스를 신규 분석으로 중복 계상하지 않는다.
3. 이번 목표는 1-2 바닐라 3D 모델 JSON, UV, blockstate 연구의 실제 남은 검증을 진행하는 것이다. v34~v38의 P1 544후보, 실제 조사 28 leaf 등 기존 모델 분석을 먼저 대조하여 누락된 근거만 조사하라.
4. 공식 압축 JAR 인증 및 인게임 렌더/런타임 검증은 사용자 지시로 필수 범위에서 제외했으나 검증 성공한 것으로 쓰면 안 된다. 1.21.11/ 사용자 제공 추출본의 소스 근거와 모델 해석·추론은 구분한다.
5. 애니메이션 소스 보류/재개 상태는 각 단계 최신 STATE를 따른다. 과거 v38의 전면 보류 문구를 현행 지시로 취급하지 않는다.
6. 새로운 실제 연구 증거가 있으면 GitHub HEAD를 재확인하고 신규 릴리스와 전역 인수인계를 갱신하라. 기존 v39~v42와 TEXnn-Rxxx 파일은 보존한다.
7. 실제 3D 가구 제작과 Project Zomboid 변환은 지금의 연구 범위가 아니다.

1-2의 기존 증거와 미확인 부분을 먼저 조사하고 실제 분석으로 진행하라.
```

[이전 v38~v41 시작문 보관](archive/NEW_CHAT_START_PRE_V42.md)
