# 1-1-08 복합·기능면 인수인계 — 현재 TEX08-R003

> 2026-11-13 · 다음 버전 **TEX08-R004** · 대상 PNG 21개 고정 · 통합 v38 그대로 · R001/R002/R003 불변 파일 정책 유지.

## 원본 출처 (사용자 확인 사항)
사용자가 직접 Minecraft Java 1.21.11 `client.jar`을 압축 해제해 GitHub에 올린 [`1.21.11/` 폴더](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/tree/main/1.21.11)를 **1차 리소스 분석 기준**으로 사용한다. 과거 [비공식 추출 미러](https://github.com/InventivetalentDev/minecraft-assets/tree/1.21.11)를 **2차 해시 교차검증 기준**으로만 사용한다. 압축 해제된 사용자 소스 ≠ Mojang JAR 전체 SHA1 인증 ≠ 실제 인게임 검증.

## R003 추가 원본 확인 (기존 실측 중복 금지)
- 추출본 **77 고유 파일 Git blob SHA 검사:** PNG21 + 보조 PNG1 + blockstate JSON16 + 모델 JSON39, 누락 0.
- R001/R002에 기존 비교 해시가 있는 **71개 전부 일치**. 모델 추가 6종(통 개폐/화로·훈연기·용광로 lit 상태/벌통 honey/chiseled 책장 base)은 추출본에서 확인했지만 기존 미러 비교 범위로 세지 않음.
- 실제 파일 파싱: blockstates JSON 16종 (variants73, multipart52), 모델 JSON 10종, PNG binary header 7종 (대상6 + 보조1), signature 및 IHDR 16×16 확인.
- 새 RGBA/UV/애니메이션 픽셀 실측 **0회**. 기존 R001/R002 보고서 누적값 그대로.
- **공식 Mojang `client.jar` 압축본 SHA1 인증 0/21**, **인게임 정적 UV 0/21**; 언제나 별도로 보류 기록.

## 파일 / 새 채팅 재개
- [R001 불변 결과](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/tree/main/research/vanilla_textures/by_stage/1-1-08/TEX08-R001)
- [R002 불변 결과](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/tree/main/research/vanilla_textures/by_stage/1-1-08/TEX08-R002)
- [R003 새 결과](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/tree/main/research/vanilla_textures/by_stage/1-1-08/TEX08-R003): `REPORT.md`, `SOURCE_LEDGER.csv`, `BLOCKSTATE_DIRECT_READ.csv`, `MODEL_DIRECT_READ.csv`, `PNG_HEADER_DIRECT_READ.csv`, `SUMMARY.json`.
- 차기 R004 전에 이 [STATE.json](STATE.json) 및 HEAD 커밋 재조회, 버전·blob SHA·R004 존재 유무 확인, 이전 릴리스 불변.
- 변경 허용: **오직** 이 단계 `STATE.json`, `HANDOFF.md`, 그리고 신규 `TEX08-R004/` 결과. 다른 단계/루트 `HANDOFF.md`, `PROGRESS.md`, `handoff/STATE.json`, v38 변경 금지.
- A–G 계속. 정적 소스·모델·UV·색상·블록 상태만; **애니메이션 프레임/움직임 보류**. Project Zomboid 변환과 실제 가구 3D 제작 제외.
