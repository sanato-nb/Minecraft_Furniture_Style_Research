# TEX09-R003 — 사용자 제공 Minecraft 1.21.11 추출본 직접 재검증

검증일: 2026-11-13. **담당 단계 1-1-09 / 토양·지면 고정 9종**. 이 보고서는 이전 `TEX09-R001`·`TEX09-R002`의 결과를 보존하고, 새로 제공받은 `1.21.11/` 추출본에서 직접 검증하지 않았던 출처 공백만 보완한다. 전역 `v38`은 변경하지 않는다.

## 새 출처와 4가지 증거 수준

- **사용자 제공 추출본:** `https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/tree/main/1.21.11`. 사용자가 Minecraft Java 1.21.11 JAR에서 직접 압축을 해제해 업로드했다고 설명함. 실제 GitHub의 파일 바이트·JSON은 직접 읽어 확인했지만 **원래 JAR 파일 자체는 이번 검사에서 확보하지 못함**.
- **비공식 미러 교차 검사:** `https://github.com/InventivetalentDev/minecraft-assets/tree/1.21.11/` 경로가 동일한 항목을 별도로 읽어 blob SHA와 바이트/JSON을 비교했다.
- **Mojang 공식 원본 인증:** **미검증**. 전체 `client.jar` 실파일 SHA-1 및 Mojang 공식 메타데이터와의 직접 검산 기록이 없다. 사용자 추출본의 파일 이름·해시 일치만으로 달성되지 않는다.
- **인게임 정적 렌더:** **미검증**. 게임 실행 장면, 바이옴 색상, 눈·주변 블록 및 조명은 본 환경에서 확인하지 않았다.

## A: 기존 연구와 대상 대조
최신 `STATE.json`의 9개 아이템과 v4 `SHA-256`, R001 `SOURCE_LEDGER.csv`, R002 모델 구조 및 회전 원장을 확인했다. 이번 새 자료는 9개 타깃 PNG, 9개 선택 blockstate, 9개 실제 선택 모델, 8개 상속/상태/대체 모델, 5개 주변 보조 PNG로 **40개 고유 소스 파일**. 이 중 **정확한 담당 PNG 표본 수는 여전히 9개**이며, 보조 PNG 5개는 별도 완료량이 아니다.

## B: 사용자 추출본 PNG 실제 바이너리 점검
GitHub `fetch_file`(base64)에서 확보한 **사용자 `1.21.11/`의 9개 대상 바이너리**를 base64로 디코딩하고 바이트 수준 **SHA-256을 독립 계산**했다. 9/9 모두 R001 미러·v4 측정 SHA-256과 정확히 일치. PNG signature, IHDR(16×16), 청크 단위 CRC32, IEND와 남는 데이터 여부를 확인: **9/9 정상**. Git blob SHA-1도 비공식 미러의 동일 상대 경로와 **9/9 동일**. 합계 PNG 원본 바이트: **2,198**, 대상 픽셀: **2,304**.

**주의:** 픽셀별 RGBA 재디코드와 평균 명도/시각 비교는 이미 R001에서 동일한 바이트에 대해 수행했다. R003에서 새롭게 측정했다고 중복 계산하지 않고, **소스 바이트가 동일하므로 R001의 결과를 사용자 추출본에도 전이 가능한 근거**로만 취급한다. R001·R002 CSV 수정/초기화 없음.

## C / D1·D2: 소스 동등성에 기초한 기존 정량 근거 유지
R001의 RGBA·명도·알파 9종 및 R002의 회전 이음새 69개 시뮬레이션은 변경하지 않았다. 9개 타깃 PNG가 바이너리 동일이므로 당시 **원본 소스 이미지 측정값**은 사용자 추출본에서도 일치한다. 다만 **인게임의 UV 랜덤 선택·바이옴 틴트·조명까지 같다는 인증은 아니다**.

## D3 / E: 사용자 제공 blockstate 9개, 모델 17개 직접 JSON 확인
선택 blockstate **9/9**, 실제 선택 리프 모델 **9/9**, 상속/눈상태/비선택 대체 모델 **8/8**을 `1.21.11/assets/minecraft`에서 직접 JSON 파싱했다. 해당 26개 JSON은 모두 기존 미러와 **Git blob SHA-1 및 JSON 의미 동일**. `MODEL_BLOCKSTATE_LINKAGE.csv`와 `SOURCE_LEDGER.csv`에 경로별 sha를 보존한다.

- `dirt`, `coarse_dirt`, `rooted_dirt`, `mud`, `packed_mud`, `gravel`은 `cube_all` 계열의 여섯 면 동일 텍스처 경로. `dirt`, `rooted_dirt`는 blockstate상 회전 Y=0/90/180/270 후보.
- `mud_bricks`의 실제 blockstate는 **일반 `mud_bricks` 모델이 아닌 `mud_bricks_north_west_mirrored`**을 선택한다. 상속된 `cube_north_west_mirrored`에서 북/서 face가 `uv:[16,0,0,16]`을 사용한다. 이는 사용자 추출본 JSON도 동일하며 R001/R002의 UV 출처가 지지된다.
- `grass_block`의 `snowy=false` 위쪽 면 `tintindex:0`; 투명 측면 overlay 4면도 `tintindex:0`가 선언되어 있다. `snowy=true`는 `grass_block_snow` 모델을 선택하고 상속된 `cube_bottom_top`에 별도 tintindex 선언은 없다.
- `podzol`의 `snowy=false`는 `podzol_top`과 `podzol_side`를 참조하며 상단에 tintindex 선언은 없다. `snowy=true`에서는 **`grass_block_snow` 모델을 참조**한다는 사실을 사용자 제공 blockstate에서 확인했다.
- 5개 **참조 전용 PNG** (`grass_block_side`, `grass_block_side_overlay`, `grass_block_snow`, `podzol_side`, `colormap/grass.png`)도 사용자 파일/미러 blob이 5/5 일치한다. `colormap/grass.png`는 256×256 RGB PNG로 존재하지만 **인게임 생물군계 색상 산정·적용 RGB는 확인하지 못함**. 이들은 고정 9개 분석 완료량에 포함하지 않음.

## F: 검증 경계
- 사용자 제공 추출본의 9개 타깃 PNG: **직접 바이너리 SHA/CRC 확인 9/9**.
- 선택 모델 및 상태 18개 JSON + 지원 템플릿 8개: **직접 열람/파싱 26/26**, 미러와 byte-equal 26/26.
- 보조 PNG 5개: **출처/바이트 동일성 5/5**, 타깃 표본에서 제외.
- Mojang 공식 client.jar 실파일과 SHA-1 공식 메타데이터 동시 직접 대조: **0/9**.
- 인게임 정적 렌더/색상/눈/주변 블록 확인: **0/9**.
- 애니메이션·프레임·키프레임 조사, Project Zomboid 변환, 실제 가구 제작: 사용자 보류/범위 제외 유지.

## G: 저장·인수인계
- `SOURCE_LEDGER.csv` 총 **40행**: 9타깃 PNG + 9 blockstate JSON + 9 선택 모델 JSON + 8 지원 모델 JSON + 5 참조 PNG. 경로, 비교 대상, Git blob 및 검증 종류 보존.
- `MODEL_BLOCKSTATE_LINKAGE.csv` **9행**: 블록별 실제 선택 모델, 회전, UV/tint 관련 정적 근거.
- `SUMMARY.json` 및 `REPORT.md`; 최신 단계 전용 `STATE.json`, `HANDOFF.md` 갱신.
- R001/R002 불변, 통합 프로젝트 `v38` 및 타 재질 단계 미수정.
- 다음 후보 버전 **`TEX09-R004`**은 매번 GitHub `STATE.json`과 파일 SHA를 다시 확인한 후 사용할 것.

**검증 대상 로컬 소스 기준:** `1.21.11/`은 GitHub에 존재하는 **사용자 제공 추출 디렉터리**다. 원본 JAR 파일 전체가 존재하거나 SHA-1 인증되었다는 주장을 하지 않는다.
