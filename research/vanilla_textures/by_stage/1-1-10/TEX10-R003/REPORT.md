# TEX10-R003 — 1-1-10 잎·식생: 사용자 제공 JAR 추출본 우선 적용 및 정적 리소스 연결 폐쇄 검증

> 날짜 2026-11-13 · **기존 R001/R002 결과는 보존** · 대상 PNG 8개 그대로 · 통합 체크포인트 `v38` 유지 · 애니메이션 조사 보류.

## 원본 우선순위·증거 신뢰도 정정

사용자는 저장소 [`1.21.11/`](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/tree/main/1.21.11)이 **직접 Minecraft Java Edition 1.21.11의 JAR을 압축 해제해 업로드한 자료**라고 명시했다. 이 사실은 **사용자의 출처 진술(user attestation)**이다. 이 추출본을 **1순위 분석 대상**으로 삼되, JAR 원본 바이트 자체나 Mojang 버전 메타데이터에서 공식 클라이언트 SHA-1을 검증한 것은 아니다.

별도 구분:
1. **사용자 제공 추출본 직접 검증:** 이번 채팅에서 `1.21.11/assets/minecraft/textures/block/` PNG **8개 Base64 실제 바이트를 다시 요청**, 동일 저장소 모델 JSON 8개·blockstates JSON 8개를 실제로 파싱, 공유 부모 모델 JSON 4개를 직접 파싱. **총 고유 경로 28개**를 확인. 저장소 PNG/모델/상태의 Git blob SHA가 기존 R001/R002 STATE 원장과 **각각 8/8 일치**, 부모 4개 SHA도 저장. 사용자 주장에 따른 출처와 파일 내용 직접 검증을 구분했다.
2. **기존 미러와 교차 검증:** R001에서 비공식 `InventivetalentDev/minecraft-assets` `1.21.11` 미러 PNG **8/8 Git blob 동일**을 이미 기록. 이는 **이전 R001 증거를 계승**한 것이며 R003 신규 미러 측정 8건으로 다시 합산하지 않는다. R003에서는 사용자 저장소의 PNG Git blob SHA가 R001 당시와 **8/8 변경 없음**을 확인.
3. **Mojang 공식 원본 인증:** **0/8 미완료**. 공식 `client.jar` 전체 SHA-1과 Mojang 공식 버전 JSON의 SHA-1 직접 대조 미수행. 추출본 파일·Git SHA-1·PNG SHA-256을 공식 클라이언트 JAR SHA-1과 혼동하지 않는다.
4. **인게임 검증:** **0/8 미완료**. 실제 Minecraft 1.21.11을 실행한 프레임·스크린샷·실시간 biome tint 검증은 이번 작업에서 수행하지 않았다.

## 새로 독립 확인한 B/E: 블록 상태 → 모델 → 부모 → 텍스처 완전 연결

이전에 이미 계산한 RGBA, 알파 마스크, 44 모델 선언 면, 덩굴 32 논리 조합은 **새 실측으로 중복 집계하지 않음**. 이번 릴리스의 신규 확인 포인트는 **사용자 제공 추출본의 실제 정적 파일 28개 참조 그래프가 끊김 없이 해석되는가**이다.

| 텍스처 | 직접 확인한 상속 부모 체인 | blockstates 정의 | 정적 모델 면 | 리소스 연결 |
|---|---|---:|---:|---|
| `oak_leaves` | oak_leaves → leaves → block | 1 기본 variant | 6 | OK |
| `spruce_leaves` | spruce_leaves → leaves → block | 1 기본 variant | 6 | OK |
| `birch_leaves` | birch_leaves → leaves → block | 1 기본 variant | 6 | OK |
| `mangrove_leaves` | mangrove_leaves → leaves → block | 1 기본 variant | 6 | OK |
| `azalea_leaves` | azalea_leaves → cube_all → cube → block | 1 기본 variant | 6 | OK |
| `moss_block` | moss_block → cube_all → cube → block | 1 기본 variant | 6 | OK |
| `vine` | vine | 10 multipart | 2 | OK |
| `flowering_azalea_leaves` | flowering_azalea_leaves → cube_all → cube → block | 1 기본 variant | 6 | OK |

- 잎 4종은 모두 모델 `parent: minecraft:block/leaves`, 그 위 `block/block`; `leaves` 부모의 큐브 6면 `#all`이 개별 잎 PNG를 가리킨다. **4개×6면의 24면**은 이전 R001 선언 면 계산에 포함된 것으로 새 산정이 아니다.
- 철쭉·이끼 3종은 `cube_all → cube → block`; `cube_all`의 **7개 텍스처 슬롯(particle/down/up/north/east/south/west)**이 `#all`로 정의되고, 각 자식의 `all`이 자신의 PNG로 수렴한다. `cube` 부모의 6면에 `tintindex` 미기재, face UV 미기재라는 원본 JSON 사실과 상속을 연결했다.
- 덩굴은 부모 없는 자체 모델 `model/vine.json`: `#vine` → `block/vine` 및 `particle: block/vine`; blockstates의 multipart 적용 모델 **10개 전부 `minecraft:block/vine`으로 참조 일치**. R002의 32 상태 진리표를 다시 새 결과로 합산하지 않음.
- 잎·철쭉·이끼 **7개**의 blockstates는 `variants: {"": {"model": ...}}` 형태의 **빈 문자열 단일 기본 변형**이다. 이는 JSON 파일에 개별 거리·영속·물 상태별 변형 항목이 없다는 뜻일 뿐, 런타임 물리 상태의 부재를 입증하지는 않는다.
- 이번 검증이 **8 PNG / 8 모델 / 8 blockstates / 공통 부모 모델 4개 = 고유 파일 경로 28개**의 직접 출처 확인과 리소스 경로 유효성 확인임을 명시한다. **새로운 연구 대상 텍스처 0개**, 새 RGBA 픽셀 수 **0**.

## A–G 대응 및 남은 일

- **A:** 저장소 사용자 추출본을 제1 출처로, R001 미러는 교차 증거로 재분류. 이전 레거시 값을 지우지 않음.
- **B:** 8개 PNG 현재 Git blob을 다시 확인하고, R001/R002의 직접 SHA-256/PNG CRC 결과를 변경 없이 계승.
- **C:** 기존 2,048 RGBA 픽셀 결과 재측정하지 않음.
- **D1–D3:** 기존 128줄 마스크, RGB 차분, tintindex·컷아웃 모델 분류를 그대로 유지. 새 tint RGB 관측 없음.
- **E:** 사용자 추출본 정적 리소스 참조 체인 직접 검증, 8개 각 모델 및 상태 SHA 재검사, 상속 부모 4개 재검사, 모든 정적 모델·텍스처 참조 연결 성공.
- **F:** Mojang SHA-1 인증, 인게임 실제 정적 확인 **모두 0/8**. 원본 `client.jar` 바이트와 실행 가능 게임 화면 부재로 계속 미완료.
- **G:** 이 보고서, [SOURCE_PROVENANCE_LEDGER.csv](SOURCE_PROVENANCE_LEDGER.csv), [RESOURCE_REFERENCE_CLOSURE.json](RESOURCE_REFERENCE_CLOSURE.json), [FOUR_AXIS_VERIFICATION.json](FOUR_AXIS_VERIFICATION.json), [SUMMARY.json](SUMMARY.json) 신규 R003 버전으로 별도 보존. 다른 단계, 루트 인수인계, 전역 `v38` 변경 금지.

## 근거와 범위

- 실측 출처는 사용자 제공 `1.21.11/` 경로의 현재 GitHub 파일 직접 조회. SHA는 파일을 SHA-256으로 다시 계산했다는 뜻이 아니라 **저장소 Git blob SHA-1로 현재 저장소 파일의 정체를 비교**한 기록. PNG의 독립 SHA-256은 R001/R002 기록을 그대로 인용했다.
- 상속·참조 연결 검증은 **게임 JSON의 정적 분석**이며 Mojang 공식 JAR의 무결성 또는 렌더/biome 결과가 아니다.
- 후속 독립 버전은 **TEX10-R004**로 예약; 새 검증 근거가 있는 경우에만 생성.
