# TEX09-R002 — 토양·지면 9종 상태별 UV·반복 이음새 정적 보완 검증

검증일 2026-11-13 · 범위 **1-1-09 9종 고정** · 전역 `v38` 유지 · 사용자 지시 따라 애니메이션 전면 보류. R001 불변 상태 유지.

## A–C: 기확인 소스 재대조
R001에 저장한 비공식 `InventivetalentDev/minecraft-assets@1.21.11`의 9개 원본 PNG를 동일 작업 환경에서 다시 로드·SHA-256 검산, **9/9 동일**. 신규 PNG를 새로 확보한 건수는 **0**. 9종 원본은 16×16, 총 2,304 완전 불투명 화소이며 R001 측정 중복 집계하지 않음. R001 `REPORT.md`의 PNG 바이트 총합 부분에는 잘못 렌더링된 문자 `${bytes.reduce(...)}`가 그대로 남아 있으므로 이 릴리스에서 **실제 총합 2,198바이트**로 정정한다. 기존 R001 파일은 변경하지 않음.

## D2 — 게임 블록상태의 정적 회전 후보를 반영한 소스 시뮬레이션
블록상태 JSON상 `dirt`, `rooted_dirt`, `grass_block snowy=false`, `podzol snowy=false`는 모델 Y 회전 0/90/180/270을 가짐. 나머지 조사 대상 다섯 모델은 기본 0 고정. 각 16×16 소스 상단 패턴의 회전 조합에 대해 **69개 인접 타일 조합**을 분석했다(4종×16 + 5종×1). `Y=0.2126R+0.7152G+0.0722B`이며 좌우 인접 모델의 경계 열 간 절대차 평균 및 상하 모델의 경계 행 간 절대차 평균을 각 조합마다 보존했다. 이는 **컴퓨터에서 추출 PNG를 회전한 정적 텍셀 시뮬레이션**이지 실제 게임의 월드 난수·좌표·라이트·틴트의 재현이 아니다.

| texture_id | 정적 회전 후보 | 이웃 조합 | 좌우 경계 최소–평균–최대 (Y) |
|---|---|---:|---|
| `dirt` | 4 | 16 | 17.9565–24.6709–37.2587 |
| `coarse_dirt` | 1 | 1 | 26.9611–26.9611–26.9611 |
| `rooted_dirt` | 4 | 16 | 22.0569–27.5716–44.4328 |
| `mud` | 1 | 1 | 4.8107–4.8107–4.8107 |
| `packed_mud` | 1 | 1 | 9.3575–9.3575–9.3575 |
| `mud_bricks` | 1 | 1 | 10.5453–10.5453–10.5453 |
| `gravel` | 1 | 1 | 13.8381–13.8381–13.8381 |
| `grass_block_top` | 4 | 16 | 14.75–19.0156–26.5 |
| `podzol_top` | 4 | 16 | 4.6632–8.3821–10.8094 |

`mud_bricks`는 블록상태 자체에서는 단일 모델을 참조하지만 **모델의 북·서 faces가 [16,0,0,16] 수평 미러 UV**를 사용한다는 별개 사실을 확인. UV 미러링과 블록 전체 회전은 다른 변환임. `ROTATION_SEAM_PAIRS.csv`, `ROTATION_SUMMARY.csv`에는 각각 69행 및 9행 보존.

## D3 / E — 모델 요소 및 눈 상태를 포함한 면별 출처 분해
R001 54개 기본 큐브면 기록을 확장하여, 상태별 선택 모델의 **70개 렌더 면 선언**을 새로 분해(`STATIC_FACE_RESOLUTION_70.csv`). 9개 주요 블록의 기본 상태 54면 + 잔디 일반 상태 측면 overlay 4면 + 잔디/포드졸 snowy=true 모델 각 6면(12면) = **70면**. 이 숫자는 텍스처 70종 또는 고유 모델 70개가 아니라 **상태와 텍스처 슬롯을 중복 포함한 면 출처 행 수**다.

- `grass_block snowy=false`: 상단 `grass_block_top` 1면과 측면 `grass_block_side_overlay` 4면에 `tintindex=0`. 측면 기본 PNG는 `grass_block_side`; 하단 PNG는 `dirt`.
- `grass_block snowy=true`: `grass_block_snow -> cube_bottom_top` 모델을 사용하며 표면 슬롯 `grass_block_top`, 아래면 `dirt`, 옆면 `grass_block_snow`로 분리; **상속된 면에 tintindex 선언이 없다**. 이는 JSON의 사실만 말하며 게임 렌더 결과를 확정하지 않는다.
- `podzol snowy=false`: 위 `podzol_top`, 아래 `dirt`, 측면 `podzol_side`; inherited top tintindex 없음.
- `podzol snowy=true`: 이 미러의 blockstate가 `grass_block_snow` 모델을 참조해 위 `grass_block_top`을 사용하도록 적혀 있다. 원본 JSON 텍스트를 기준으로만 기록하며 게임 화면과 별도 검증 필요.
- 위 9종 외의 `grass_block_side_overlay`, `grass_block_side`, `grass_block_snow`, `podzol_side`는 **모델에서 참조하는 슬롯만 조사**했으며 원본 PNG 실측 9종에 더하지 않았다.

`mud_bricks`는 상속 경로 `mud_bricks_north_west_mirrored -> cube_north_west_mirrored_all -> cube_north_west_mirrored`을 추적해 **여섯 면 × 여섯 UV 좌표 = 36개 소스 픽셀 대응**을 새로 계산(`MUD_BRICKS_UV_PIXEL_SAMPLES.csv`). 예: 북쪽 face UV (0,0)은 원본 PNG 픽셀 (15,0)으로 이동. 남쪽 face (0,0)은 원본 (0,0) 유지. 각 위치의 실제 RGBA를 기존 SHA 확인 미러 PNG에서 표본 추출. **공식 게임 렌더된 UV 표본이라고 주장하지 않음.**

## F — Mojang 공식 client.jar 인증 미실시 (0/9)
실제 Mojang `piston-meta.mojang.com`, `piston-data.mojang.com`은 이 실행 환경에서 다운로드가 허용되지 않았다. 별도 제3자 `PrismLauncher/meta-launcher`의 캐시된 `net.minecraft/1.21.11.json`을 직접 열어, `client.jar` 예상 SHA-1을 `ba2df812c2d12e0219c489c4cd9a5e1f0760f5bd`, 크기를 `31,152,600`바이트, URL을 `https://piston-data.mojang.com/v1/objects/ba2df812c2d12e0219c489c4cd9a5e1f0760f5bd/client.jar`로 확인했다. 이것은 **공식 아티팩트의 위치/해시를 설명하는 제3자 캐시 메타데이터**이지 **실제 JAR 수신·해시 인증 아님**. `client.jar` 공식 SHA-1과 미러 PNG SHA-256을 동일시할 수도 없다.

보조적으로 `PrismLauncher/meta-upstream`의 `mojang/version_manifest_v2.json`에서 1.21.11 항목을 조회해 그 메타데이터 링크가 시점마다 변경됨을 확인. 공식 JAR을 얻으면 최종 `client.jar` 전체 SHA-1 검증 → 해당 JAR 내부 9 PNG SHA-256/CRC 대조 → 게임 정적 화면/바이옴 틴트/눈/인접 블록 확인 순서로 진행해야 한다.
**공식 JAR 인증 0/9, 실제 인게임 정적 화면 0/9**. 애니메이션 작업은 보류.

## G — 신규 산출물 / 인수인계
- `SOURCE_LEDGER.csv`: 9개 소스 PNG/모델·상태 SHA 연결, 공식 여부 표시
- `STATIC_FACE_RESOLUTION_70.csv`: 70면(잔디 오버레이/눈 상태 추가) texture slot, UV, tintindex 및 원본 RGB 표본
- `ROTATION_SEAM_PAIRS.csv`: 69개 이웃 회전 조합, `ROTATION_SUMMARY.csv`: 9종 요약
- `MUD_BRICKS_UV_PIXEL_SAMPLES.csv`: 36개 텍셀 UV 좌표/원본 RGBA
- `SUMMARY.json`: 신규·레거시 중복 구분, 공식 메타데이터 provenance, 잔여 미검증 범위
- 후속 번호 `TEX09-R003`는 현재 저장 직후 후보. **매번 STATE·HEAD 확인 후 진행**. 전체 공식 연구 버전은 `v38` 유지.

## 자료 근거
- 미러 `InventivetalentDev/minecraft-assets` GitHub ref `1.21.11` 소스 PNG / `models/block/*.json` / `blockstates/*.json`. SHA는 SOURCE_LEDGER와 R001 원장에 기록.
- https://github.com/PrismLauncher/meta-launcher/blob/master/net.minecraft/1.21.11.json (캐시 원본 모델 아님; 공식 client.jar URL 정보만)
- `TEX09-R001` 저장 산출물 원본 PNG SHA 및 픽셀 기록 재사용.
