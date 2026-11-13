# TEX02-R003 — 1-1-02 사용자 제공 Minecraft 1.21.11 JAR 추출본 우선 검증

- 분석 대상: **석재·벽돌 고정 17종** (새 고유 텍스처 0종), 날짜 2026-11-13.
- 사용자 제공 원본: [이 저장소의 1.21.11/](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/tree/2a43897b8f605b4e0c96a272bca476ee6b70058e/1.21.11) — 사용자가 `client.jar`를 직접 압축 해제해서 올렸다고 제공한 폴더. 연구에 사용한 Git commit: `2a43897b8f605b4e0c96a272bca476ee6b70058e`.
- 2차 교차 소스: [InventivetalentDev/minecraft-assets](https://github.com/InventivetalentDev/minecraft-assets/tree/7241a12cc2707abd7022f399c5d9033153e492e1), 과거 R001/R002 자료. **사용자 제공 추출본 자체를 Mojang 공식 JAR 인증으로 간주하지 않는다.**

## A/B 사용자 원본 직접 조회·바이너리 검증

`1.21.11/assets/minecraft/textures/block/<id>.png`의 고정 **17개 실제 바이너리**를 직접 읽어 SHA-256 계산, PNG signature·내부 청크 CRC32·IHDR 크기 측정: **17/17 모두 16×16·CRC 통과**. SHA-256은 파일마다 이전 v4/R001 기록과 완전 일치. Git blob SHA도 동일 경로의 기존 비공식 미러와 17/17 동일. `SOURCE_LEDGER.csv`는 이를 항목별로 기록하며 기록된 PNG SHA는 이번 사용자 파일에서 직접 계산한 값이다.

고정 범위 외 모델의 참조 끝면 PNG `deepslate_top.png`·`blackstone_top.png` 2개는 사용자 폴더에서 signature/CRC/16×16 확인, R002 미러와 Git blob SHA 2/2 일치. 이 두 파일의 SHA-256 및 RGBA 측정 기록은 **R002에서 바이트 동일성에 따라 승계**하며 이번 신규 SHA256/픽셀 측정으로 중복 산입하지 않는다. 결과는 `SUPPLEMENTAL_END_FACE_LEDGER.csv`.

## C/D1/D2 기존 RGB·명암·알파·연마/줄눈 결과 재사용

R001의 **17×16×16=4,352 RGBA 픽셀** 실측값, D1 에지·대비, D2 반복 경계·줄눈은 원본 17개 PNG가 사용자 추출본과 **바이트 동일**하므로 기존 값을 그대로 적용할 수 있다. **R003의 신규 RGBA 측정 픽셀은 0개**다. 이전 PNG 측정을 새 성과로 덧셈하지 않는다.

## D3/E 사용자 추출본 정적 JSON 및 UV

사용자 폴더에서 `models/block/<id>.json` **17개**, `blockstates/<id>.json` **17개**를 직접 읽어 JSON 파싱 및 Git blob SHA 검증, 모두 이전 미러와 **바이트 일치**. 관련 부모/미러 모델 `cube`, `cube_all`, `cube_column`, `cube_mirrored`, `cube_mirrored_all`, `cube_column_mirrored`, `stone_mirrored`, `deepslate_mirrored` **8개**도 직접 확인·미러와 동일. 합계 `MODEL_JSON_CROSSCHECK.csv` **42개 JSON 원장**.

이 같은 정적 소스에서 `cube_all` 15종은 6면 `#all`; `cube_column` 2종 `deepslate`, `blackstone`은 4개 측면 `#side`와 2개 끝면 `#end`를 사용한다. `cube_mirrored`의 명시적 `uv:[16,0,0,16]` 역시 사용자 추출본 원문과 동일하다. R002에 보존한 **기본 면 슬롯 102개·블록상태 31개 변형 기록**을 바이트 동일성으로 교차 검증한 것이며 이번에 102면/31개를 새로 측정한 것은 아니다.

## 별도 4단계 검증 상태

| 수준 | 이번 판정 |
|---|---|
| 1. 사용자 제공 JAR 추출본 | PNG SHA-256·CRC **17/17**, 모델 JSON **17/17**, blockstate JSON **17/17** 직접 검증 |
| 2. 기존 비공식 미러와 교차 | 고정 PNG 17 + 모델 17 + blockstate 17, 보조 PNG 2 + 공유/미러 모델 8 **Git blob 59/59 동일** |
| 3. Mojang 공식 `client.jar` SHA-1 + 공식 버전 메타데이터 | **0/17, 미검증**. 압축 해제 폴더만으로 원본 JAR 자체 SHA-1을 역산/공식 인증할 수 없음 |
| 4. 실제 인게임 정적 렌더 | **0/17, 미검증**. 게임 내 정적 스크린샷/렌더 없음 |

공식 인증과 인게임 렌더가 남아 있으므로 최종 A–G 완료는 **0/17**로 보수적 유지. 동적 애니메이션 프레임·키프레임·움직임 분석은 계속 보류.

## 다음 TEX02-R004

- 우선 사용자 제공 `1.21.11/` 추출본을 원본 분석의 1순위로 사용하고 미러는 검증용 보조 출처로만 활용.
- 가능하면 원본 압축된 `client.jar` 바이너리·Mojang 공식 manifest/version SHA-1 체인을 확보해 비교.
- 실제 Minecraft의 **정적** 모델 회전·UV 접합·광원 관찰을 통해 인게임 증거만 추가 인증.
- 기존 R001/R002 파일·원시 측정치 유지, 전체 `v38`, 다른 단계 손대지 않음. 연구 분모 17개, 실제 가구 3D 제작·Project Zomboid 변환·애니메이션은 작업 범위 밖.
