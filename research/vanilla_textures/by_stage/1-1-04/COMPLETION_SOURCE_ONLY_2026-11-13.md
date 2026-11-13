# 1-1-04 직물·양털 9종 — 정적 소스 연구 완료 기록

> **사용자 승인 범위에서 완료: YES** · 연구 최신 릴리스 **TEX04-R008** · 확인 날짜 **2026-11-13** · 기준 게임 소스 **사용자 제공 Minecraft Java 1.21.11 추출본** · 전역 과거 체크포인트 **v38 불변**.

## 정확한 완료 범위

본 완료 표시는 마인크래프트 **양털 9개 PNG와 해당 블록/아이템 정적 JSON 연결을 대상으로 한 소스 분석**만을 뜻한다.
소스의 명도·RGB·패턴·이음매·모델 상속·UV 근거와 무결성은 R001–R008 보고서에서 검증했다.
사용자 요청에 따라 **인게임 실행/스크린샷 및 Mojang 전체 JAR SHA1·공식 메타데이터 인증은 필수 완료 항목이 아니다.**

- PNG **9/9개**: `white, red, blue, black, green, yellow, purple, cyan, orange` `_wool.png`. 사용자 추출본의 원본 PNG 바이트를 SHA-256 및 PNG CRC로 재검사, 16×16 및 불투명 RGBA 확인.
- PNG에서 검사한 **고유 소스 픽셀 9×256=2,304개**. R001에서 계수한 원본을 R002–R008에서 반복 분석했으나 새로운 픽셀로 중복 합산하지 않았다.
- 정적 블록 연결 **9 leaf model JSON + 9 blockstate JSON + 3 공통 parent JSON**. 모델 상속 `cube_all → cube → block`, 정적 블록 면/텍스처 참조 **총 54면**은 기존 근거를 계승.
- 1.21.11 `assets/minecraft/items/<color>_wool.json`의 정적 아이템 모델 참조 **9개** 확인. 신규 고유 PNG/face를 의미하지 않는다.
- 색상별 RGB·명도·저대비 텍스처 패턴·정적 이음매 수학적 측정, D4 방향 비교, 색상쌍 인접 변화 부호, 전역 명도 순위, 2,295건 순환 자기상관, RGB 팔레트 반례는 각 릴리스에 출처와 해석 범위를 분리해 기록.
- 특히 R007의 명도 순위 역전 **73건**은 R008에서 초록 양털 RGB 두 그룹의 Blue 채널 1단계 차이로 귀속했고, encoded-RGB 및 linear-light 두 지표에서 같은 역전 위치를 확인.
- META-INF SHA-384 MANIFEST/SF 내부 일치성은 선행 보고서의 **내부 파일 해시 연결 증거**일 뿐, `MOJANGCS.RSA`의 암호학적 서명 인증 또는 **Mojang 공식 client.jar 인증 성공을 의미하지 않음**.

## 최종 단계별 체크리스트

| 단계 | 상태 | 근거 / 판정 |
|---|---|---|
| 1-1-04-A 기존 자료·출처 대조 | **완료** | 원본 9종과 레거시 계측 중복 대조 |
| 1-1-04-B 원본 PNG 무결성·해상도 | **완료(사용자 제공 추출본 범위)** | 9 PNG SHA256·CRC·16×16 판정. 공식 JAR 인증은 범위 제외 |
| 1-1-04-C RGBA·색상·밝기·패턴 | **완료** | 2,304 고유 원본 픽셀 계측 |
| 1-1-04-D 재질 특화 비교 D1–D3 | **완료(정적 소스·가설 구분)** | 양털 9색 RGB·명도·패턴 비교, 제작 응용의 사실/제안 분리. 가구 제작 자체는 대상 아님 |
| 1-1-04-E 모델 JSON·정적 UV | **완료(소스 상속/참조 검증)** | 9 leaf + 9 blockstates + 3 parents, 54 face 참조, 9 item models |
| 1-1-04-F Mojang 공식·실제 게임 검증 | **필수 제외** | 인게임 검증 기록 0/9, 공식 JAR 인증 0. 미검증이지 검증 성공은 아님 |
| 1-1-04-G 결과 저장·인수인계 | **완료** | R001–R008 각 보고서/CSV/코드, 현재 STATE/HANDOFF, 이 최종 완료 보고서 |

## GitHub에 보존된 불변 연구 보고서

- [TEX04-R001 보고서](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-04/TEX04-R001/REPORT.md)
- [TEX04-R002 보고서](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-04/TEX04-R002/REPORT.md)
- [TEX04-R003 보고서](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-04/TEX04-R003/REPORT.md)
- [TEX04-R004 보고서](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-04/TEX04-R004/REPORT.md)
- [TEX04-R005 보고서](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-04/TEX04-R005/REPORT.md)
- [TEX04-R006 보고서](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-04/TEX04-R006/REPORT.md)
- [TEX04-R007 보고서](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-04/TEX04-R007/REPORT.md)
- [TEX04-R008 보고서](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-04/TEX04-R008/REPORT.md)

완료 상태의 살아 있는 문서:
- [STATE.json](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/stages/1-1-04/STATE.json)
- [HANDOFF.md](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/stages/1-1-04/HANDOFF.md)
- [이 최종 완료 기록](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-04/COMPLETION_SOURCE_ONLY_2026-11-13.md)

## 제외·보류 / 진실성 기준

1. 실제 인게임 텍스처 샘플링·GUI·광원·셰이더·렌더링은 관찰하거나 검증했다고 주장하지 않는다. 사용자가 완료 필수 조건에서 제외했으므로 **0/9은 연구 미완료 판정 근거가 아니다**.
2. 전체 Mojang client.jar SHA-1/메타데이터와 PKCS7 RSA 실서명 검증은 성공으로 바꾸지 않는다. 필요한 문서 해시 연결과 공식 인증은 다르다.
3. 애니메이션, Project Zomboid 맵 변환, 실제 3D 가구 제작, 다른 1-1 분류는 이 완료 표시에 포함되지 않는다.
4. `docs/vanilla_texture_1-1/1-1-04_직물양털.md`의 옛 체크리스트는 **연구 시작 당시 계획 기록**이며, 최종 완료 판정은 이 문서와 최신 `STATE.json`/`HANDOFF.md`가 우선한다. 원래 계획 파일을 역사적으로 덮어쓰지 않는다.
5. **새 연구 근거가 없는 상태에서 R009를 발행하지 않는다.** 현재 `TEX04-R008`을 최종 연구 릴리스로 유지한다. 사용자가 추후 새 원본·질문을 제공하면 상태 재검사 후 별도 작업.

**최종 판정:** 사용자 승인 정적 소스 연구 필수 단계 A–E 및 G **완료**, F **명시적 범위 제외**. 이 연구는 사용자 기준으로 **종료**.
