# TEX10-R008 — 잎·식생 8종 블록별 색상 공급자 추적과 덩굴 32상태 기하 대조

> 2026-11-13 · Java 1.21.11 사용자 추출본 `.class`/model JSON/blockstates JSON 정적 검증. **인게임 검증과 Mojang 전체 JAR SHA-1 인증은 사용자 정책상 제외**. 화면 캡처 없이 원본 소스 근거만으로 확인한 결과. R001–R007과 전역 v38, 타 단계 변경 없음.

## 가장 중요한 새 결론: 5종 틴트, 3종 비틴트 — 블록/아이템 틴트도 다르다

| texture_id | 모델 면 tintindex | 블록 색상 공급자 | 아이템 틴트 (R005 계승) |
|---|---|---|---|
| `oak_leaves` | 0 | 바이옴 foliage getter | #48B518 |
| `spruce_leaves` | 0 | #619961 | #619961 |
| `birch_leaves` | 0 | #80A755 | #80A755 |
| `mangrove_leaves` | 0 | 바이옴 foliage getter | #92C648 |
| `azalea_leaves` | 없음 | 없음(BlockColors 등록 없음) | 별도 constant 미선언 |
| `flowering_azalea_leaves` | 없음 | 없음(BlockColors 등록 없음) | 별도 constant 미선언 |
| `vine` | 0 | 바이옴 foliage getter | #48B518 |
| `moss_block` | 없음 | 없음(BlockColors 등록 없음) | 별도 constant 미선언 |

- **바이옴 잎색 3종**은 `oak_leaves`, `mangrove_leaves`, `vine`: `dzs` registry symbols `aK`, `aS`, `fN` 각각 `ggr.a()Lggr;`의 6종 공유 그룹에 포함 → `ggr.i` → `hns.b` lambda `hns.c(Biome)` → `dxo.d()` foliage getter. hns를 포함한 실제 1.21.11 `.class`의 `BootstrapMethods` 항목과 Code 명령어를 직접 대조.
- **고정 상수 2종**은 `spruce_leaves` `dzs.aL`→`ggr.k` `#619961`; `birch_leaves` `dzs.aM`→`ggr.j` `#80A755`. 이 고정 틴트는 R005 아이템 상수와 같으나, 참나무·맹그로브·덩굴 **아이템 고정 색상**은 **배치 블록 바이옴 foliage 색상**과 처리 계층이 다르다. 블록 색상을 아이템 상수로 대체하지 말 것.
- **미등록 3종**은 `azalea_leaves`, `flowering_azalea_leaves`, `moss_block`: registry symbols `dzs.aT`, `aU`, `ub`가 `ggr`의 BlockColors factory 등록 목록에 없음. 이 3종은 모델도 `cube_all→cube`를 상속하여 **6개 면에 tintindex 미선언**. `ggr.a(..., tintIndex)`는 provider 누락 시 `-1`을 반환하지만, **모델에 틴트가 없으므로** '임의 바이옴색으로 곱한다'는 모델 해석은 잘못임. '화면 최종 RGB'는 이 정적 근거만으로 확정하지 않는다.
- 나머지 확장 그룹으로 `jungle_leaves`, `acacia_leaves`, `dark_oak_leaves`도 같은 `ggr.i` 등록에 존재함을 확인했지만 **본 단계 표본 8종에 추가 계수하지 않음**.

## 원본 모델과 블록상태·UV 대조 (기존 증거 심화 검사)

- 4개 바이옴/고정 틴트 잎은 `block/leaves` 부모의 **6개 큐브 면 모두 tintindex 0**; 부모에는 각 면 `UV [0,0,16,16]`가 명시된다. 두 철쭉 잎과 이끼는 `cube_all→cube`의 **6개 큐브 면 tintindex 미선언**(UV는 면 기본값). 덩굴은 단일 원본 모델의 **2개 양면 면, z=0.8 평면**, north/south UV를 반대로 지정하고 두 면에 tintindex 0. **총 44개 원본 모델 면 관계**(24+18+2)로 R001의 UV 44행과 수량 대조됨. 개별 면의 최종 게임 조명은 포함되지 않는다.
- 7개 대상 블록은 블록상태 JSON에 빈 키 모델 variant 1개. 덩굴만 `multipart` **10규칙**이며 north/east/south/west/up **5개 불리언 상태 조합 2^5=32개**를 모두 독립 평가하였다.
- 덩굴 **모두 false 상태는 오히려 5개 평면**이 기본 fallback으로 선택된다. 다른 31 상태는 true인 방향만 선택. 32상태에 걸친 **모델 평면 적용 횟수 합 85, 양면 면 적용 합 170**. 이는 32개 다른 상태를 합산한 정적 수치지, 한 게임 프레임의 폴리곤 수가 아니다. plane 개수 분포: 1개 5상태, 2개 10상태, 3개 10상태, 4개 5상태, 5개 2상태.

## 원본 근거와 새 경로 수

- **신규 고유 소스 경로 2개**: `1.21.11/dzs.class` Git blob `b58e7153fb0cfbb47313c3a59dd7c8516ee3642c`와 `1.21.11/hns.class` Git blob `3764254251aadfd1549e5d155d48a43efd5d2194`.
- 기존 원본 경로 **21개 재활용·재조회**: 8개 대상 모델 JSON, 8개 blockstate JSON, 부모 모델 3, R007의 `ggr.class`/`dxo.class`. 원본 경로 Git blob SHA와 현재 트리를 모두 대조했다. 신규 고유 2개를 R003–R007 누적 **134개**에 더해 **136개**. 과거 `ggr.class`는 새 파일로 중복 계수하지 않고 **이번에는 registration factory 전체의 실제 그룹 및 메서드 bootstrap까지 새롭게 해석**한 것으로 기록.
- 사용자 제공 원본 `Biome` JSON 65와 R007 `BIOME_COLORMAP_LOOKUP_65.csv`를 재사용해 **65×8 = 520개 참조 행**을 생성. 각 행은 단일 바이옴이 가정된 **모델 틴트 인자**이고, 틴트 없는 블록은 공백으로 명시. 실제 좌표의 이웃 바이옴 보간, GPU 조명/알파/최종 화면색을 재현하지 않았음.
- 이번 새 대상 PNG 계측, RGB 디코드, raw SHA256 산출, 새 UV 면은 모두 **0**. R001 RGBA 2,048픽셀 및 R007 보조 3컬러맵 196,608 RGB 픽셀 위치를 계승하며 새 계측으로 중복 집계하지 않는다.

## R008 파일

`BLOCK_COLOR_PROVIDER_8.csv`, `CLASS_REGISTRATION_AUDIT.json`, `MODEL_FACE_AUDIT_8.csv`, `BIOME_TINT_REFERENCE_65x8.csv`, `VINE_MULTIPART_32.csv`, `REUSED_SOURCES_AUDIT.csv`, `SOURCE_LEDGER.csv`, `SUMMARY.json`, 이 `REPORT.md`.

## 미확인·연구 완료 판단 경계

- **완료된 정적 하위 질문**: 표본 8종의 모델·UV·틴트 인덱스, registry 이름과 BlockColors 공급자 적용 그룹, 덩굴 상태의 원본 정적 조합, R007의 바이옴 foliage default/명시 override.
- **정적 소스로 추가 해석 가능한 후보**: 실제 블록별 렌더 패스 선택과 밉맵 세부 알고리즘(현재 foliage 원본 metadata `dark_cutout`만 확인), 이웃 바이옴 틴트 보간 경로. 이는 기존 자료로 자동 완료 처리하지 않는다.
- **필수 조건에서 제외**: Minecraft 실제 실행/스크린샷/인게임 0/8 및 Mojang 공식 전체 client.jar SHA1 인증. 사용자에게 인게임 캡처 요구를 하지 않는다. 실제 최종 화면 RGB 검증 주장을 하지 않는다.
- **보류**: 애니메이션·흔들림, Project Zomboid 변환, 실제 가구 3D 모델 생성. 전역 v38 및 다른 단계·이전 R001–R007 불변.
