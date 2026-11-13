# 전역 v39 — 1-1 바닐라 재질 10단계 통합, 1-1-02 석재·벽돌 제외

> 2026-11-13 KST · 고정 source commit `e20d1bef908bb5f3f5d3727a72513d3957a66b54` · 통합 식별자 `INT-1-1-20261113-01` · 이관 기준은 11개 독립 단계의 실제 GitHub STATE와 150개 v4 원장.

## 통합 범위 및 엄격한 해석

- **포함 10개 독립 분류: 133개 서로 다른 고정 `texture_id`.**
- **의도적으로 제외 1-1-02 석재·벽돌: 17개.** 독립 연구 현재 `TEX02-R015`의 기록·폴더·STATE/HANDOFF 그대로 보존. 기존 v4 역사적 150개 원장도 유지.
- **133/150은 연구 성과의 전체 완료율이 아니라 이번 "전역 통합"에 편입한 고정 파일명 수의 비율**. 이번 통합에서 원본 PNG를 새로 디코딩하거나 133개를 다시 분석한 것이 아니다. 새 직접 PNG 픽셀 계측 **0건**.
- 10개 단계의 기존 USER JAR 추출본 SHA/CRC·모델 JSON·UV 및 애니메이션 근거를 확인하고 각 독립 단계 `STATE.json` Git blob SHA를 스냅샷으로 고정. 최신 독립 REPORT 및 SUMMARY 파일은 **통합 직전 확인한 Git blob SHA와 경로**를 원장에 기록. 독립 `TEXnn-Rxxx` 버전은 바꾸지 않음.
- 최상위 연구 체크포인트 `v38 → v39` 업데이트는 **이 통합 작업의 버전**, 해당 단계들의 새 분석 릴리스가 아니다. 상위 1단계 5개 세부 과제 최종 완료 수 **0/5 유지**, 1-1 전체 최종 완료 판정은 **석재·벽돌 미통합으로 보류**.

## 통합 단계별 출처 (서로 다른 단위 합산 금지)

| 번호 | 재질 | 고정 PNG 수 | 마지막 연구 보고서 | 이관 핵심 근거 |
|---|---|---:|---|---|
| 1-1-01 | 목재·원목 | 18 | [TEX01-R008](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-01/TEX01-R008/REPORT.md) | 목재 고정 18 PNG, 132개 소스 모델 면 RGB 참조; 보조 애니메이션 PNG 4종·18프레임은 별도 범위 |
| 1-1-03 | 금속·금속부품 | 16 | [TEX03-R008](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-03/TEX03-R008/REPORT.md) | 금속 16 PNG, 63 정적 상태·406면; 금속 16종에 texture .mcmeta 없음, 개폐 정적 끝점 24쌍 |
| 1-1-04 | 직물·양털 | 9 | [TEX04-R009](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-04/TEX04-R009/REPORT.md) | 양털 9 PNG·2,304 RGBA·54 모델면; 대상 9종 애니메이션 정의 미발견 |
| 1-1-05 | 유리 | 6 | [TEX05-R008](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-05/TEX05-R008/REPORT.md) | 유리 6 PNG·1,536 RGBA, 컷아웃/투명 픽셀; 대상 6종 애니메이션 정의 미발견 |
| 1-1-06 | 도기·유광도기 | 8 | [TEX06-R008](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-06/TEX06-R008/REPORT.md) | 도기 8 PNG·48 정적 면 및 UV 회전; 대상 8종 애니메이션 정의 미발견 |
| 1-1-07 | 콘크리트·색면 | 7 | [TEX07-R008](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-07/TEX07-R008/REPORT.md) | 콘크리트 7 PNG, 색상/패턴/42 모델면; 대상 7종 애니메이션 정의 미발견 |
| 1-1-08 | 복합·기능면 | 21 | [TEX08-R008](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-08/TEX08-R008/REPORT.md) | 기능면 21 PNG/39 모델·8 상속 부모·143면; 모델 참조 texture52종 중 애니메이션 2종/5프레임은 별도 분모 |
| 1-1-09 | 토양·지면 | 9 | [TEX09-R008](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-09/TEX09-R008/REPORT.md) | 지면 9 PNG, 잔디 overlay·눈 측면·상태 JSON; 고정9+보조4 PNG 원본 애니메이션 정의 없음 |
| 1-1-10 | 잎·식생 | 8 | [TEX10-R014](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-10/TEX10-R014/REPORT.md) | 잎·식생 8 PNG, 알파/틴트/atlas-JVM loader 경로 분석; 원본 애니메이션 연구는 해당 단계의 최신 기록상 보류 |
| 1-1-11 | 목재·구조부품 | 31 | [TEX11-R013](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-11/TEX11-R013/REPORT.md) | 목재 구조부품 31 PNG, 127 leaf, 문·다락문·선반 544 정적 상태 및 528개 source 상태차 후보, 실제 런타임 모션 아님 |

## 검증의 경계와 현재 연구 정책

- **1차:** 사용자가 직접 Minecraft Java 1.21.11 설치 JAR을 풀어 `1.21.11/`로 올렸다고 밝힌 게임 리소스. 이전 비공식 추출 미러는 비교 자료. 사용자 제공 추출본과 Mojang 공식 배포 JAR SHA-1 인증은 서로 다름.
- **Mojang 공식 압축 JAR SHA-1 인증 및 실제 인게임 화면/런타임 인증은 최신 사용자 결정으로 필수 연구·완료 조건에서 제외**. 그러나 이를 성공적으로 인증하거나 인게임 화면을 관찰했다고 주장하지 않는다. 단계 STATE의 과거 실제 인게임 관찰은 모두 0이다.
- **애니메이션 소스 검증 재개:** 1-1-01/03/04/05/06/07/08/09/11의 9개 단계는 최신 사용자 요청에 따라 재개. **1-1-10 잎·식생은 최신 STATE에서 보류**이므로 재개로 간주하지 않는다. 프레임 PNG 실측과 실제 Minecraft 런타임 보간/애니메이션 관측은 별개.
- 소스 결과의 단위 구분: 애니메이션 보조 PNG·프레임, texture/material 슬롯, 모델 리프·부모, face×material 인스턴스, 블록 상태 정의/가능 조합, UUID 없는 PNG 원본 픽셀·재사용 UV 텍셀. **서로 다른 범주의 카운트를 더하지 않는다.**
- 원본 게임 에셋의 **저작권/공개 재배포 상태는 본 연구 통합으로 해결되지 않음**. 이번 산출물은 바이너리 PNG·JSON·class를 별도로 복제하지 않고 기존 근거 경로·해시·분석 요약만 담음.
- 단계별 자체 정의된 source-only 완료 판정은 그 작업만의 경계. 바닐라 전체 P1 조사·게임 렌더·모드 비교·2단계 가구 모델링 스타일 가이드가 완성됐다는 의미 아님. Project Zomboid 변환이나 실제 3D 가구 제작은 범위 제외.

## 감사 자료

- [STAGE_INTEGRATION_LEDGER.csv](STAGE_INTEGRATION_LEDGER.csv) — **11행**, 포함 10 + 제외 1, 독립 단계 고정 버전·SHA·source 근거
- [TEXTURE_133_SCOPE_LEDGER.csv](TEXTURE_133_SCOPE_LEDGER.csv) — **133행**, 파일 ID·경로·기존 SHA256·단계 소스 검증 상태
- [MANIFEST.json](MANIFEST.json) — 소스 메인 커밋, 각 단계 `STATE.json` blob SHA와 버전, 133/17 분모
- [CONTINUATION.md](CONTINUATION.md) — 제외된 1-1-02 및 향후 개별 릴리스 업데이트의 처리

**다음 작업:** 1-1-02는 별도 독립 채팅에서 계속 연구할 수 있지만 **사용자가 요청하기 전에는 이 통합에 포함하지 않는다**. 남은 10개에서 새 `TEXnn-Rxxx`가 생겨도 v39이 자동 갱신되지는 않으므로, 후속 집계는 별도 전역 버전에서 수행.
