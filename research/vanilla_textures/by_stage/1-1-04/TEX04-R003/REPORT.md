# TEX04-R003 — 사용자 제공 Minecraft 1.21.11 JAR 추출본 우선 전환 및 양털 9개 원본 대조

**일자:** 2026-11-13  
**작업 범위:** `1-1-04 직물·양털` 정확한 9개 텍스처만  
**새 근거:** 사용자 제공 GitHub `1.21.11/`의 **실제 9개 PNG + 9개 정적 모델 JSON + 9개 blockstate JSON + 3개 공통 모델 부모 JSON + version.json**.  
**버전:** `TEX04-R003` (독립), 기존 `R001/R002` 결과 및 전체 통합 `v38` **불변**.

## 가장 중요한 결론

1. 사용자 제공 `1.21.11/assets/minecraft/textures/block/`의 **양털 9개 실제 PNG를 GitHub로 직접 읽고 base64를 디코딩해 파일 내용의 SHA-256을 새로 계산했다. 모두 R001/v4 저장 SHA-256과 동일 (9/9)**. SHA-256 구현은 고정 시험 벡터 `abc`로 자체 검증했다.
2. 그 9개 PNG의 사용자 저장소 Git blob SHA와 `InventivetalentDev/minecraft-assets` (`1.21.11`) 미러의 개별 Git blob SHA가 각각 **9/9 완전 일치**. 각 원본 PNG 시그니처 및 4개 청크 `IHDR/PLTE/IDAT/IEND` CRC32 검사 통과. 16×16 palette color type 3, 크기 360~399 바이트. 따라서 R001/R002에서 측정한 원본 픽셀/알파/명도·채도·패턴을 **동일 바이트 기반으로 재사용 가능**.
3. 모델 leaf `models/block/{color}_wool.json` **9/9 읽고 부모 `minecraft:block/cube_all`, `textures.all` 대응 색상 확인**. `blockstates/{color}_wool.json` **9/9 읽고 `variants[""]`의 동일 색상 모델 연결 확인**. Git blob 비교에서 **9개 모델과 9개 blockstate 모두 미러와 일치**한다(블랙 모델의 R001 ledger 전사 오기 제외).
4. 사용자 제공 `cube_all.json` → `cube.json` → `block.json`의 공통 모델 상속도 직접 확인. `cube.json`은 from `[0,0,0]`, to `[16,16,16]` 정육면체에 up/down/north/south/east/west 6면을 사용하며 각 cullface·#face → #all → 색상 텍스처로 이어진다. **9×6=54개의 이미 존재하던 정적 면 참조**를 사용자 제공 JSON으로 새 교차 검사; 암시적 기본 UV는 0..16 전체 면(원본 PNG x0..15,y0..15). UV 배열은 `cube.json`에 **명시되어 있지 않다**. 54개의 별도 새로운 화면 실측을 의미하지 않음.
5. **비공식 미러 ↔ 사용자 제공 추출본** 간 **파일 동일성 확인은 Mojang 공식 원본 배포본 인증이 아님**. 전체 JAR 및 Mojang 제공 원본 버전 메타데이터가 부재하므로 공식 SHA-1 인증 0/9, 인게임 정적 렌더링 0/9 유지.

## A — 출처 범주 및 이력 대조

기준으로 [사용자가 직접 1.21.11 client.jar을 압축 해제해 업로드했다고 밝힌 저장소](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/tree/main/1.21.11)를 우선 읽었다. `1.21.11/version.json` 원본의 `id=1.21.11`, `world_version=4671`, `protocol_version=774`, `build_time=2025-12-09T12:20:42+00:00`을 확인했다. 이는 *추출본 내부 버전 표기*이며 Mojang에서 내려받은 JAR의 SHA-1 검증으로 간주하지 않는다.

`TEX04-R001/SOURCE_LEDGER.csv`의 기존 PNG SHA-256·Git blob·JSON 연결을 전부 교차 검사했고 `R002`의 36색쌍 상관 및 9개 이음매 기록은 재계산 성과로 중복 집계하지 않았다. 이 단계 고유 텍스처 분모는 **여전히 9개**.

## B — 사용자 제공 PNG의 실제 바이너리 실측·원본 비교

| 색상 | 파일 바이트 | SHA-256 (사용자 추출본 직접 재계산 = R001/v4) | Git blob / 미러 동일 |
|---|---:|---|---|
| white | 390 | `70c9c9a9901d71ef9a5a89ea2cc4bc0d99ff5e65f733d1467da8b92f746107a5` | 예 |
| red | 372 | `07b48cec9b4610e908025807fb85fa686dd50f17918fa677ce655d28b3ba3464` | 예 |
| blue | 381 | `2ca85a3e25a3ea9b0d8209edab2ab93f64e458d8c6baf8215536912159a6e2db` | 예 |
| black | 360 | `8cefbc855a4ff04f6125ded6a69e8bd21144802fc466b179665c8c0203daffd9` | 예 |
| green | 384 | `a2cd93d4bcead9b808d367fefa17081e12e5bd96ebff6993fc3d486422ecb9ad` | 예 |
| yellow | 398 | `cc77805bdc4ccb24d210ec65e304f1c367ae9e9ee0fed404ec99143bf62a2ef2` | 예 |
| purple | 399 | `f8f5d7eb9145633d27d80c4c06a9a71e21eaea522c277f81a4d6d9e8fd60f0d9` | 예 |
| cyan | 370 | `68706949a22ed0877a42ddca38e5ec428039d52ff23e6614f2900e33cb759303` | 예 |
| orange | 398 | `de3ec43fe8ca99026bdda3c036a964990e7d9b08c8b67690e2f975ddbdc5ff68` | 예 |

9개 모두 PNG 청크 CRC32 및 16×16 색인 컬러(color type 3) 검사 통과. **새로운 파일 해시/출처 진위검사이지 R001/R002 RGBA 2,304픽셀을 별도로 새 분석한 2,304픽셀로 다시 더하지 않음.**

## C·D — 기존 RGBA/색상/패턴 실측의 귀속 변경

사용자 제공 PNG와 미러 PNG가 각 색상에서 **정확히 동일 바이트**이므로 `R001` RGBA/명도/채도/잡음/이음매 및 `R002` 36색쌍 상관·팔레트 인덱스 분석은 **사용자 제공 자료에서도 파일 내용 기준 재현 가능한 근거**다. 다만 이번 R003의 새로운 연구량은 원본 출처 **9개 바이너리 직접 인증 + 9개 정적 모델 + 9개 blockstate의 독립 파일 검증**이다. R003에서 새 색상, 새 원본 픽셀, 새 36쌍 재측정을 수행했다고 중복 집계하지 않는다.

D1 팔레트 차이와 D2 방향성·경계 수치는 R001/R002로부터 계승. D3 쿠션/직물 응용은 가이드 가설이며 가구 구조·표면 물성의 게임 내부 확정 사실이 아니다.

## E — 사용자 추출본 정적 모델·블록 상태·UV 연결 확인

- 전체 직접 열람: 모델 leaf 9개, 블록상태 9개, 공통 부모 `cube_all`, `cube`, `block` 3개 = **정적 JSON 21개**, 그리고 별도 `version.json` 1개.
- 모델 연결: 단일 빈 variant 키 `""` → `minecraft:block/{color}_wool` → `minecraft:block/cube_all` → `block/cube` → `block/block`.
- 공통 `cube_all`이 여섯 면의 슬롯에 `#all`을 지정하고 색상 leaf가 `#all`에 연결된 텍스처를 지정한다. `cube`는 육면체 좌표와 각 면 texture/cullface, `block`은 display/gui transform을 정의한다.
- 각 면에 `uv` 명시가 없어 기본 full face implicit UV `[0,0,16,16]`를 적용하는 *정적 소스 기반 해석*. 54면에 대한 전용 대응 표 `USER_EXTRACT_54_FACE_UV_SOURCE_CHECK.csv` 저장.
- **R001 오기 발견:** `black_wool` 모델의 40자리 실제 Git blob은 `7fea63ff530cad3b51435e662daa2c4d6324bd8a`이나 R001의 `SOURCE_LEDGER.csv` 1행 및 `UV_FACE_LEDGER.csv`의 6면에서 끝 `a`가 누락된 **39자리 전사값** 사용. 사용자 추출본과 실제 미러 양쪽에서 올바른 40자리 값을 재확인. 모델 내용 자체는 동일하다. R001은 수정하지 않고 R003의 정오표 및 새 54면 표에서 바로잡았다.

## F — 서로 혼동하지 않는 네 가지 상태

| 상태 | 결과 | 인증 등급 |
|---|---|---|
| 사용자 제공 JAR 추출본 직접 검증 | PNG 9/9, 정적 모델/blockstate 9/9, 부모 JSON 확인 | `user_provided_extraction_checked` |
| 이전 미러와 SHA/내용 비교 | PNG 9/9, 모델 JSON 9/9, blockstate JSON 9/9 (블랙 모델 기록 오기 정정) | `mirror_binary_crosschecked` |
| Mojang 공식 배포 `client.jar` 전체 SHA-1 및 공식 메타데이터 | **미검증 0/9**. 단지 추출 파일이 있고 원본 JAR 전체가 없음 | `pending_official_jar` |
| 실제 게임 1.21.11 정적 렌더 | **미검증 0/9** | `pending_ingame_static` |

Git blob SHA-1·각 PNG 내용 SHA-256·Mojang 원본 JAR 전체 SHA-1은 서로 다른 지표다. 폴더의 `version.json`은 자체 표기이지 공식 인증 근거가 아니다.

## G — 저장 및 다음 채팅 인수인계

- `USER_EXTRACT_9_PNG_JSON_CROSSCHECK.csv` — 사용자 파일 경로, 실제 PNG SHA-256·Git blob SHA·기존 v4/mirror SHA·CRC·정적 JSON 9행.
- `USER_EXTRACT_54_FACE_UV_SOURCE_CHECK.csv` — R001 54행 보존·사용자 제공 모델/상속 재검증·블랙 모델 6행 SHA 정정.
- `ERRATA_R001_BLACK_WOOL_MODEL_SHA.md` — 수정 대상 7개 과거 필드 기록과 실제 올바른 SHA 비교, R001 불변 유지.
- `SOURCE_PROVENANCE_AND_FOUR_GATES.md` — 네 검증 축의 분리와 출처 등급.
- `SUMMARY.json` — 9개 직접 검증 9개 교차, 공식 0, 인게임 0 기계 판독 결과.
- `VERIFY_USER_EXTRACT.py` — 동일 JAR 추출 디렉터리를 가진 로컬 체크아웃의 SHA256/PNG CRC/JSON 상속을 검증하는 재현 스크립트.

**다음 `TEX04-R004`에서는 직접 받은 Mojang 공식 버전 JSON + 원본 `client.jar` 전체 SHA1/파일 크기 대조 및 내부 9 PNG·모델 대조를 우선 진행.** 실제 게임 정적 장면 증거가 없으면 그 상태도 보류. 기존 텍스처 9개 분석/UV 54면은 재반복하지 않으며, 애니메이션은 계속 중단한다. 다른 단계 및 프로젝트 루트/전역 `v38`는 수정하지 않았다.
