# TEX03-R003 — 사용자 제공 1.21.11 JAR 추출본 직접 검증 및 기존 미러 비교

**범위** 1-1-03 금속·금속부품 / Minecraft Java 1.21.11 / 2026-11-13. 이전 릴리스 `TEX03-R001`·`TEX03-R002` 불변. 공통 `v38` 변경 없음.

## 출처 명칭 정정

사용자는 [GitHub 저장소의 `1.21.11/`](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/tree/main/1.21.11)을 **직접 1.21.11 클라이언트 JAR을 압축 해제해 올린 파일**이라고 명시했다. 이번에는 실제 이 폴더의 PNG 바이트와 JSON 문서를 직접 읽고 검증했다. `InventivetalentDev/minecraft-assets@1.21.11`는 이제 교차 검증용 비공식 미러다. 사용자 제공 추출본과 비공식 미러의 일치는 **공식 Mojang 배포본 자체의 인증이 아니다**.

직접 확인한 추출본 내부 `1.21.11/version.json` (Git blob SHA-1 `b49974d3ebd6cb73291d9e4c92d23b3192dadd66`): `id=1.21.11`, `world_version=4671`, `protocol_version=774`, `resource_major=75`. 이 값은 **추출본의 자체 기재 정보**이며 Mojang 공식 메타데이터와 인증된 결과는 아니다.

## A — 변경된 분석 범위

기존 고정 대상인 금속 텍스처 **16개**의 자료 출처를 사용자 제공 `1.21.11/`로 바꿔 대조했다. 직접 검증한 연결 파일은 **PNG 16개 + blockstate JSON 14개 + model JSON 39개 = 총 69개 고유 파일**. 기존의 v4/R001 PNG 픽셀 측정과 R002 모델 145면 분석을 신규 실측으로 **중복 집계하지 않았다**.

## B — 사용자 제공 PNG 파일 16개 실제 바이너리 확인

- `1.21.11/assets/minecraft/textures/block/`의 16개를 GitHub에서 **Base64 실제 파일로 가져와 디코딩**하고 신규 SHA-256을 직접 계산함.
- **16/16** PNG IHDR 16×16, PNG 시그니처, 모든 청크 경계 및 CRC 검사 통과.
- **16/16** 신규 SHA-256이 기존 R001 미러 PNG SHA-256과 정확히 일치. **16/16** Git Blob SHA-1도 기존 미러와 일치.
- 총 바이트 **3,176**. [`USER_PNG_BINARY_CROSSCHECK.csv`](USER_PNG_BINARY_CROSSCHECK.csv)에 파일별 256비트 해시, 160비트 Git Blob 해시, 크기, PNG 구조 증거 수록.

## C — 기존 팔레트/알파 측정의 재사용 여부

PNG 내용이 바이트 수준에서 일치하므로 기존 `TEX03-R001/SOURCE_LEDGER.csv`의 **총 4,096 RGBA 픽셀, 완전투명 321, 완전불투명 3,775, 중간 알파 0**과 각 색상 평균은 사용자 제공 해당 PNG에 적용될 수 있다. 단, R003에서 새롭게 4,096픽셀을 디코딩하거나 별도 픽셀 측정한 것으로 기록하지 않는다.

## D — 정적 상태 직접 확인

- `1.21.11/assets/minecraft/blockstates/`에서 해당 JSON **14/14 직접 수집·파싱**, 모두 이전 미러와 **Git Blob SHA-1 14/14 동일**.
- 총 **63개** 정적 `variants`를 확인함: 단순 10개 블록×1, heavy_core 1, anvil 방향 4, iron_trapdoor 16, iron_door 32.
- `iron_door` 상·하단, `iron_trapdoor` 열림/닫힘은 기존 모델 상태 구분을 그대로 재사용. 정적 상태 JSON은 애니메이션 또는 게임 내 시각 검증을 뜻하지 않음.
- [`USER_BLOCKSTATE_CROSSCHECK.csv`](USER_BLOCKSTATE_CROSSCHECK.csv)에 대상 모델 경로와 SHA/상태수 기록.

## E — 정적 모델 JSON 39개 직접 검증

- 각 blockstate가 지정한 **23개 고유 leaf 모델**, 이를 상속/연결하는 **16개 부모·템플릿 모델**을 사용자 제공 저장소에서 실제 JSON으로 읽음.
- 39/39개 모두 기존 1.21.11 미러의 대응 원문 **Git Blob SHA-1 일치**. 이 중 R002의 13개 모델 SHA 기록도 **13/13 재확인**.
- 모델 경로/부모/텍스처 매핑/면·요소 수를 [`USER_MODEL_JSON_CROSSCHECK.csv`](USER_MODEL_JSON_CROSSCHECK.csv)에 기록. 기존 145개의 템플릿 면 UV 알파 분석 결과를 이 해시 일치로 사용자 제공 추출본에도 적용할 수 있다.
- 예: **기존 R002 결과**인 heavy_core의 알파 64픽셀 미사용 UV, anvil_top의 PNG 투명 96픽셀 미사용, 철문/철다락문 판면·측면 차이는 그대로 유지하되 **R003의 신규 UV 145면 실측이라고 주장하지 않음**.

## F — 요구된 4가지 독립 검증 기준

| 검증 축 | 결과 | 구분 |
|---|---|---|
| ① 사용자 제공 JAR 추출본 실제 파일 검증 | **69개 파일 직접 확인** | PNG SHA256/CRC 16, 블록 상태 JSON 14, 모델 JSON 39 |
| ② 기존 비공식 미러와 교차 검증 | **69/69 Git Blob SHA-1 일치** | PNG는 별도 **16/16 SHA-256** 일치 |
| ③ Mojang 공식 JAR 무결성 인증 | **미완료 / 0** | 원본 client.jar 바이트 및 공식 버전 메타데이터 SHA-1과 대조하지 못함 |
| ④ 인게임 정적 렌더 검증 | **미완료 / 0** | 게임 실행, 동일 정적 장면 사진·화면 검증 없음 |

사용자 저장소에 JAR **추출 파일**이 있다는 사실과 Mojang 공식 **원본 client.jar 전체 SHA-1 인증**을 혼동하지 않는다. 정적 PNG/모델 JSON으로 광택·조명·실제 렌더 결과를 인증하지 않는다.

## G — 신규 불변 릴리스 및 다음 작업

- `USER_PNG_BINARY_CROSSCHECK.csv`: 새 출처 PNG 16개 직접 SHA256·PNG CRC·미러 해시 일치 원장
- `USER_BLOCKSTATE_CROSSCHECK.csv`: 블록 상태 JSON 14개(63 variants) 비교 원장
- `USER_MODEL_JSON_CROSSCHECK.csv`: leaf+연결 부모 모델 JSON 39개 비교 원장
- `VERIFICATION_TRACKS.json`: 위 4개 검증 축을 분리한 기계 판독 상태
- 이 `REPORT.md`, 해당 단계 전용 `STATE.json` 및 `HANDOFF.md`만 갱신. R001/R002, 타 단계, 공통 v38 불변.
- **다음 신규 버전: TEX03-R004**, 공식 JAR 원본 전체 SHA-1과 Mojang 공식 1.21.11 버전 메타데이터 대조 또는 인게임 정적 화면 증거가 있을 때만 인증 상태 변경.
- 애니메이션·키프레임·움직임 연구 **보류**. Project Zomboid 변환 및 실제 가구 3D 모델 제작 **범위 제외**.
