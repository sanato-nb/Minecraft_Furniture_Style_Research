# 전역 v41 — 1-1 전체 11단계 최신 연구 통합 갱신

> 2026-11-14 KST · ID: `INT-1-1-20261114-01` · 원본 HEAD: `8c4d40d27537a08a18926840836534aa91f0132a`.

## 핵심 통합 결과

- **11/11개 재질 단계·150/150개 고유 텍스처 ID** 모두 통합 원장에 포함. v4 원본 ID·경로·SHA256과 **150/150 정확히 일치**, 누락·중복 0.
- **소스 기반 연구 완료 판정: 132/150(88%), 10/11개 단계.** 미완료는 **1-1-01 목재·원목 18개**. 이는 소스 범위 연구 완료율이며 전체 프로젝트의 5개 상위 과제는 **0/5** 그대로.
- **석재·벽돌 고정 통합 버전 갱신: `TEX02-R015 → TEX02-R017`.** 기존 v40의 R015 고정 완료 0/17에서 R017 근거의 완료 17/17로 변경. 나머지 10개 독립 단계 참조·해시는 v40 그대로.
- **v39 및 v40은 보존하고 새 v41 파일로 기록**. 이번에 실제 PNG/모델을 재측정한 추가 분석은 **0건**, 기존 단계 R016·R017 근거를 후속 통합에 정식 반영했을 뿐.

## 석재·벽돌 최신 연구를 통합한 근거

- [TEX02-R017 원본 보고서](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R017/REPORT.md) · [SUMMARY](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R017/SUMMARY.json).
- 원본 고정 PNG 17개에 아틀라스 보조 상부 PNG 2개가 추가로 참조되나, **150개 고정 분모에 2개를 추가하지 않음**.
- 원본 모델 JSON 19개·부모 JSON 7개, 블록상태 모델 선택 선언 31개, 모델면→스프라이트 경로 186개 연결, 미해결 0개.
- R016은 17개 블록의 원본 Java 클래스 및 등록 경로 기반 렌더 시드 상속을 확인; R017은 아틀라스 선언·원본 loader 클래스 경로를 확인. 두 결과 모두 **소스 기반 검증**이며 Minecraft 렌더러 실행/인게임 화면 관측은 아님.
- `STATE.json` Git blob `1626a2041bc599fa9b79a0c5c63c4686e6c4a372`, R017 보고서 blob `55fc7d3083364c71b3a7b5e8e88d2cc76a881570`, SUMMARY blob `989b4be1d3793f97f448607a0db8170cf6fb11f0`로 고정. 기존 R015/R016/R017 개별 릴리스 내용은 수정하지 않음.

## 단계별 소스 연구 판정

| 단계 | 재질 | 원본 PNG | v41에 고정된 독립 버전 | 소스 연구 완료 |
|---|---|---:|---|---:|
| 1-1-01 | 목재·원목 | 18 | [TEX01-R008](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-01/TEX01-R008/REPORT.md) | 0/18 |
| 1-1-02 | 석재·벽돌 | 17 | [TEX02-R017](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R017/REPORT.md) | 17/17 |
| 1-1-03 | 금속·금속부품 | 16 | [TEX03-R008](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-03/TEX03-R008/REPORT.md) | 16/16 |
| 1-1-04 | 직물·양털 | 9 | [TEX04-R009](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-04/TEX04-R009/REPORT.md) | 9/9 |
| 1-1-05 | 유리 | 6 | [TEX05-R008](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-05/TEX05-R008/REPORT.md) | 6/6 |
| 1-1-06 | 도기·유광도기 | 8 | [TEX06-R008](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-06/TEX06-R008/REPORT.md) | 8/8 |
| 1-1-07 | 콘크리트·색면 | 7 | [TEX07-R008](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-07/TEX07-R008/REPORT.md) | 7/7 |
| 1-1-08 | 복합·기능면 | 21 | [TEX08-R008](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-08/TEX08-R008/REPORT.md) | 21/21 |
| 1-1-09 | 토양·지면 | 9 | [TEX09-R008](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-09/TEX09-R008/REPORT.md) | 9/9 |
| 1-1-10 | 잎·식생 | 8 | [TEX10-R014](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-10/TEX10-R014/REPORT.md) | 8/8 |
| 1-1-11 | 목재·구조부품 | 31 | [TEX11-R013](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-11/TEX11-R013/REPORT.md) | 31/31 |
| **합계** | **11개 분류** | **150** | | **132/150** |

## 범위 및 완료 판정

- **통합 파일 등록률 150/150(100%)**와 **소스 연구 완료율 132/150(88%)**는 서로 다른 수치다. 잔여 목재·원목 18개는 단계 자체에서 아직 완료 판정되지 않았음.
- Mojang 공식 `client.jar` 전체 SHA 인증과 실게임 런타임·인게임 검증은 최신 사용자 정책에서 **필수 완료조건 제외**. 인증에 성공했다거나 실제 게임에서 렌더링을 관측했다는 주장은 하지 않음.
- 애니메이션 원본 소스 분석은 9개 단계에서 재개, **1-1-02 및 1-1-10은 최신 단계 상태상 보류**. 프레임 메타데이터·정적 상태 끝점을 실제 런타임 움직임으로 오인하지 않음.
- 기존 v4 150종 픽셀/해시 기록, v39 10단계 133종, v40 전체 150종 및 모든 TEX 연구 릴리스는 그대로 보존. 저작권 있는 원본 PNG·class 파일은 이번 v41에 다시 업로드하지 않음.
- Project Zomboid 맵 변환이나 실제 3D 가구 제작은 본 연구 통합 범위가 아님.

## 산출물
[단계별 원장](STAGE_INTEGRATION_LEDGER.csv) · [150종 개별 원장](TEXTURE_150_SCOPE_LEDGER.csv) · [SHA/버전 스냅샷](MANIFEST.json) · [검증 결과](VALIDATION.json) · [다음 연구 인수인계](CONTINUATION.md).
