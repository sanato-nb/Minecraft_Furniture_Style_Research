# v61 — Minecraft Java 1.21.11 바닐라 가마솥 11개 P1 모델, 가변 내용물 높이, UV·PNG 원본 분석

> 연구 날짜 2026-11-14 KST · 시작 `main` `17d2fa985431efb208b21d2958fd3c0a5e8253ff` · 1-2-A의 원본 연구만 진행; 실제 가구 제작 또는 좀보이드 맵 변환은 하지 않았다.

## 1. 정밀 원본 재확인 범위 및 비중복 기준

P1 544개 모델 경로/Git blob SHA가 이미 연결된 v60 **544행×279열** 증거 원장에서, v53 새175·v57 16·v58 27·v59 35·v60 14와 겹치지 않는 **기존 11개 P1 신원**을 실제 Minecraft 1.21.11 추출 원본 JSON과 SHA로 다시 조회했다. 신규 신원 링크=0. 조사 대상: `cauldron` 1, `template_cauldron_full/level1/level2` 3, `water_cauldron_full/level1/level2` 3, `lava_cauldron` 1, `powder_snow_cauldron_full/level1/level2` 3.

원본 11개 JSON·경로·blob SHA를 `00A_ORIGINAL_CAULDRON_MODELS_11.json`에 저장. 네 original blockstate와 두 original png.mcmeta는 `00B_`에 보존했다. 원본 PNG 7종 파일 식별 경로·Git blob SHA·IHDR 및 Pillow 실측은 `00C_`.

## 2. own 대 inherited 원본 3D geometry

| 지표 | 출처 기반 집계 |
|---|---:|
| 직접 조회한 기존 P1 모델 | **11** |
| own `elements` | **55** |
| own 선언 faces | **235** |
| 부모 상속 적용 elements | **153** |
| 부모 상속 적용 faces | **648** |
| 원본 face.uv 명시 | **0** |
| `uv` 원본 누락 (엔진 암시 규칙 미인증) | **648** |
| 원본 PNG 경로+Git SHA로 해결된 face references | **645** |
| 독립 abstract parent의 `#content` 미해결 faces | **3** |
| inherited `tintindex:0` 내용물 top face refs | **10** |
| cullface face refs | **352** |
| 0두께 요소/회전 요소 | **0 / 0** |

빈 기본 가마솥 `cauldron.json`은 13 요소·58면. 내용물 공유 템플릿 3종은 각각 14 요소·59면(본문 13 요소 + 내용물 요소 1). 자식 7모델은 self elements가 없고 해당 템플릿 `elements`을 상속하면서 내용물 종류를 `#content` 텍스처 경로로 지정한다. 원본 면 CSV `02_ORIGINAL_FACE_EVIDENCE_648.csv`에는 모든 원본 face 텍스처 슬롯·부모 SHA·content `tintindex`·cullface와 결측 `uv`를 보존했다.

**중요:** 모든 648면이 원본에서 명시 UV가 없다. 계산 가능한 값은 오직 **엔진 암시 UV의 확인되지 않은 후보**이며, 실제 UV 좌표/반전/회전 공식은 이 회차에서 인증하지 않았다. 따라서 모든 645개 PNG 경로 해결 면을 원본 실화소 면별 완성으로 계상하지 않는다.

## 3. 내용물 top surface가 바뀌는 정확한 위치

공통 content 요소의 원본 `from:[2,4,2]`; `to`는 `level1=[14,9,14]`, `level2=[14,12,14]`, `full=[14,15,14]`. 표면은 `up: {texture:"#content", tintindex:0}`. **실제 내용물의 표현 범위와 높이 유효성은 JSON 좌표의 진술**이며 런타임 fluid 시뮬레이션/게임내 tint 검증은 아니다.

원본 `blockstates/cauldron.json` 기본 1 variant, `water_cauldron.json`의 레벨1/2/3 3 variant, `lava_cauldron.json`의 기본 1, `powder_snow_cauldron.json` 3 variant: 합계 **4파일, 8 variant source refs** 정적 직접 대조. 이 중 내용물 7모델의 `y=9/12/15`과 원본 상태가 일치. 기록 `03_BLOCKSTATE_4_VARIANTS_8_STATIC_AUDIT.json`.

## 4. 원본 PNG 진위·Pillow·애니메이션 선언

정확히 대응하는 PNG **7개**의 원본 GitHub 파일 경로 및 Git blob SHA를 재조회했다. PNG IHDR를 원본 바이너리 헤더에서 확인했다. 이 중 `cauldron_side`, `cauldron_top`, `cauldron_bottom`, `cauldron_inner`, `powder_snow` PNG 5개는 실제 원본 바이너리에서 Git SHA1을 재계산하여 **5/5 일치**, SHA256과 Pillow RGBA 전 5×16×16 = **1,280픽셀**을 직접 복원하여 **alpha255 1,008 / alpha0 272**, 나머지 부분 alpha 0. `cauldron_top`의 원본 알파0 100, `cauldron_bottom`의 알파0 172. 원본 PNG 단위 소스 검증이지 648면의 실제 엔진 sampling 결과가 아니다.

`water_still.png` 원본 **16×512 = 32개의 정사각형 밴드**, `lava_still.png` 원본 **16×320 = 20개의 밴드**임을 직접 PNG IHDR에서 읽었다. 대응 `.png.mcmeta` 2개 원본을 읽어 각각 `frametime=2` 선언 확인, 용암은 원본 38개 프레임 순서 `0→19→1`(되돌아오는 경로를 포함)를 선언. **이 두 애니메이션 PNG의 전체 RGBA 픽셀을 실제 Pillow로 디코딩하지 않았고, 프레임별 비교나 실제 게임 프레임 출력도 검증하지 않았다.** 그러므로 정지 PNG 5개 실측과 애니메이션 2개 IHDR/메타데이터 근거는 서로 다른 확신 수준으로 저장했다.

## 5. 이번 회차에서 가능한 가구 스타일 관찰

- 동일한 용기 외곽(13요소) + 내용물 위 표면(추가1요소) 형태로 여러 상태를 표현한다.
- 채움 단계가 달라지면 x/z 영역 `2..14`는 유지되고 y top 위치가 9→12→15로 달라진다.
- 원본 지정된 `#content` 텍스처만 물/용암/가루눈에 따라 다르며 원본 `tintindex` 선언은 확인되지만 출력 색은 게임 엔진 인증을 거치지 않았다.
- cauldron top/bottom PNG는 원본 자체에 투명 픽셀을 포함한다. 이 결과를 면 가림/알파 테스트 런타임으로 오해하면 안 된다.

## 6. 원장 보존·제약

v60 원장 **544행×279열 → v61 544행×297열**. 이전 279개 컬럼 × 544개 데이터행 **151,776 셀 값 전부 동일**; v61의 18개 신규 열은 11개 선택 모델에만 근거 추가. P1 모델 경로+Git SHA **544/544 기존 식별 연결**이며 전체 기하·UV·PNG·렌더러 완료 의미가 아니다. v53 new175/v57 16/v58 27/v59 35/v60 14와 새로 중복되지 않는 11개를 계상; 나머지 cohort 외부 **266개 P1**은 과거 근거가 이미 있을 수 있으므로 무조건 미검증이라고 부르지 않는다.

공식 Minecraft 1.21.11 클라이언트 엔진 암시 UV/tint/culling/animation, 특수 렌더러 14건 (shulker13+skull1), 전체 과거 의미론 통합은 여전히 남아 있다. 재현 스크립트 `REPRODUCE_CAULDRON_V61.py`는 저장했지만 전체 체크아웃에 대한 end-to-end 실행은 하지 않았음. **1-1 승인150/150**, 상위 **1/5 완료**, **1-2-A/1-2 진행 중·실질 완료율 미산정** 유지. 가구 제작과 Project Zomboid 변환 금지.

다음 채팅 시작 전 `NEXT_CHAT_HANDOFF.md`, `SUMMARY.json`, `VALIDATION_POST_RESEARCH_COMMIT.json`부터 새 `main` HEAD에서 검증하라.
