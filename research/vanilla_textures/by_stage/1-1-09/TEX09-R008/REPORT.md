# TEX09-R008 — 보류 해제 후 1-1-09 토양·지면 애니메이션 메타데이터/프레임 실측

연구 일시: 2026-11-13. 저장소 `sanato-nb/Minecraft_Furniture_Style_Research`, 자료원: **사용자 제공 Minecraft Java 1.21.11 JAR 추출본 `1.21.11/`**. GitHub 현재 main에서 읽어 검사함. 사용자가 “보류한 애니메이션 하자”라고 명시하여 **이 단계의 애니메이션 분석 보류만 해제**한다. 다른 `1-1-xx` 단계의 보류 정책에는 영향을 주지 않는다.

## 1. 검수 범위와 방법
- 고정 9종: dirt, coarse_dirt, rooted_dirt, mud, packed_mud, mud_bricks, gravel, grass_block_top, podzol_top. 연결 검토용 보조 4종: grass_block_side, grass_block_side_overlay, grass_block_snow, podzol_side.
- **13개 실제 PNG를 각각 직접 base64로 읽고** PNG signature와 IHDR 가로·세로 정보를 확인했다. **13/13 전부 16×16, 파일 안에 2개 이상의 16×16 프레임을 세로로 적층하지 않음**. 이것은 이미지 구성 실측이다. R001~R007의 과거 RGB·CRC 통과 등을 신규 검사 수량으로 재계상하지 않는다.
- **13개 대응 `.png.mcmeta` 경로 각각을 GitHub main에서 직접 조회:** 13/13 `NOT_FOUND(404)`. 파일 부재는 **검사한 사용자 추출 폴더의 본 경로에 한정**되며 다른 리소스팩 또는 엔진 내부의 모든 동작을 부정하는 전역 증명은 아니다.
- 블록 상태 JSON 9개와 선택/보조 모델 JSON 10개를 재파싱; frame/frametime/animation 같은 시간 순서 키가 없음. 각자 `variants`의 모델 참조/회전 또는 `snowy` 조건을 가짐.

## 2. 고정 9 PNG 결론
| 범주 | 검사 대상 | PNG 모양 | `.png.mcmeta` | source animated frame set |
|---|---:|---|---|---|
| 토양·자갈·진흙·벽돌류 | 7종 | 전부 16×16 | 7종 모두 없음 | 0 |
| `grass_block_top`, `podzol_top` | 2종 | 둘 다 16×16 | 2종 모두 없음 | 0 |
| **고정 합계** | **9종** | **9/9 한 장짜리** | **0/9 존재** | **0/9** |

보조 4 PNG (`grass_block_side`, `grass_block_side_overlay`, `grass_block_snow`, `podzol_side`)도 모두 16×16·애니메이션 메타데이터 없음. 9개 대상 표본 수에 포함하지 않는다.

## 3. 정적 변형을 시간적 애니메이션으로 오분류하지 않기
- `blockstates/dirt.json`, `rooted_dirt.json` 등에 Y 0,90,180,270도의 모델 선택 배열이 존재한다. 이는 **정적 외형 방향 후보**이며 `frame` 간 이동이나 초당 회전 타이밍이 정의된 프레임 애니메이션이 아니다.
- `blockstates/grass_block.json`과 `podzol.json`에서 `snowy=false` 일반 모델 및 `snowy=true` `grass_block_snow` 선택은 **블록 상태에 따른 정적 모델 교체**다. 0→1→2 순서의 애니메이션 프레임이나 시간값을 규정하지 않는다.
- `grass_block` 모델의 `tintindex:0`과 측면 overlay 알파, grass colormap의 RGB는 색상·구성 데이터이지 PNG 프레임 전환 규칙이 아니다.
- 블록 세계 상태 변화(성장, 주변 환경에 따른 상태 변화), 바이옴/조명/외부 리소스팩 재정의와 **텍스처 `.png.mcmeta` 기반 시간 재생**은 개념을 구분한다. 게임 코드까지 역분석하지 않았으므로 모든 가능한 코드 기반 동작이 없다고 단정하지 않는다.

## 4. 동일 추출본의 실제 애니메이션 **양성 대조군** (고정 9종 범위 외 · 검출 방법 검증용)
| 원본 PNG | IHDR | 프레임 띠 수(세로/가로) | `.png.mcmeta`의 animation | 판정 |
|---|---|---:|---|---|
| `lava_still.png` | 16×320 | 20 | `frametime:2`, 명시 프레임 인덱스 38개 (순서 0..19..1) | 프레임 정의 있음 |
| `lava_flow.png` | 32×512 | 16 | `frametime:3`, frames 목록 없음 | 기본 프레임 순서로 쓰일 수 있는 세로 배열 + 메타데이터 |
| `fire_0.png` | 16×512 | 32 | 명시 프레임 32개 (16..31,0..15) | 프레임 정의 있음 |

양성 대조군의 실제 PNG 바이트와 대응 `.png.mcmeta` JSON을 열어 확인했다. `assets/minecraft/atlases/blocks.json`은 `minecraft:directory` source=`block`을 선언하지만 대상 개별 프레임 재생 시간표는 아니다. **양성 대조군 3종을 이 단계의 9종 연구 완료 수량에 더하지 않는다.**

## 5. 검증한 사실과 검증하지 않은 것
- **검증한 사실:** 해당 사용자 추출본의 대상 9종 및 보조 4종은 16×16 단일 PNG이며 인접 `.png.mcmeta` 13개가 없고, 대상 블록의 관련 blockstate/model JSON에도 프레임 스케줄이 없음. 동일한 소스에 `animation` 메타데이터를 가진 실제 애니메이션 텍스처 양성 대조군이 존재하므로 메타데이터 검사 방식이 애니메이션을 탐지할 수 있음을 확인.
- **검증하지 않은 사실:** 게임 엔진 내부 코드가 발생시키는 모든 상태 변화나 프로시저/셰이더 애니메이션, 외부 리소스팩 또는 모드의 오버라이드, 실제 화면 재생. 인게임 검증과 공식 Mojang JAR 인증은 1-1-09의 이전 사용자 지시로 요구 범위에서 제외되며, 검증 성공했다고 주장하지 않음.

## 6. 완료 판정 및 인수인계
- 새 근거: 13개 개별 `.png.mcmeta` 404 확인, 13개 실제 PNG IHDR 프레임 띠 검사, 9개 블록 상태·10개 모델의 시간 키 없음 확인, 3개 애니메이션 양성 대조군 실측. **소스 기반 프레임 애니메이션 해당 없음(0/9)**으로 판정하며 전체 마인크래프트 모든 애니메이션 부재 증명으로 확장하지 않는다.
- 파일: `TEXTURE_ANIMATION_AUDIT_13.csv` (13행), `BLOCKSTATE_MODEL_MOTION_AUDIT_9.csv` (9행), `POSITIVE_ANIMATION_CONTROLS_3.csv` (3행), `SOURCE_LEDGER.csv` (검사 출처 목록), `SUMMARY.json`, 본 `REPORT.md`.
- 이전 `TEX09-R001`~`R007` 원본 결과 불변. 전역 `v38`, 다른 단계와 루트 파일 불변. 본 단계만 **애니메이션 연구 보류 해제**. 다음 후보 `TEX09-R009`는 새 소스 증거가 확인될 때만 생성, 없으면 완료를 알리고 중단.
