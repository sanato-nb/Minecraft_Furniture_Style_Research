# 1-2-E Entry3 — B-first 나머지 28개 원본 조사

**2026-11-16 KST · 시작 main `5ce75365683e285e91706c10f69dec07ea9b0a9d` · Minecraft Java 1.21.11 추출 원본.**

고정 배정표의 Entry3 **28/28개** JSON 본문·Git SHA를 직접 검사했다. E 누적 **86/86개 원본 조사**, 미조사 0. 이번 모델 모두 자체 `elements`가 없고 `thin_block.json`의 부모 `block/block.json`에도 `elements`가 없다. 27개에는 `textures.particle`만 있으며 그중 `pitcher_crop_top_stage_0`~`2`의 세 모델은 `ambientocclusion`도 선언한다. `thin_block.json`은 particle 없이 `display`와 부모만 가진 D 미참조 템플릿이다.

| 근거 | Entry3 결과 |
|---|---:|
| 원본 JSON 본문·SHA | 28개 |
| 직접 부모 선언 / 자체·상속 요소 | 1 / 0·0 |
| particle 슬롯 선언 / 미선언 템플릿 | 27 / 1 |
| 고유 particle PNG SHA·RGBA | 23개 (item 경로 10개) |
| C 기존 PNG RGBA 일치 | 13개 |
| D 모델 선택 참조 | 40건·30경로 |
| 실제 런타임 renderer 인증 | 0개 |

원본 snapshot과 모델별 선언, PNG 해시·RGBA, D 참조를 `E_ENTRY3_*` 원장에 기록했다. 별도 검사기가 **모델 28개 본문/SHA, 고유 PNG 23개 SHA/RGBA, D 참조 40건**을 원본에서 재계산해 불일치 0으로 통과했다. particle PNG를 가시 표면이나 특수 renderer 형상으로 단정하지 않으며 `UNVERIFIED_RUNTIME_RENDERER`를 유지한다.

**게이트:** E1 고정 분모 PASS; E2 원본 조사 86/86; E3 소스 증거와 미인증 렌더 경계 기록. **E4 전체 86개 종합·원격 종료 감사 대기**, 따라서 E 전체는 아직 미완료. A/B/C/D·v69, 승인150/150 및 상위 1/5 보존.
