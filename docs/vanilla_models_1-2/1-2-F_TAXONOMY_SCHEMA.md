# 1-2-F 분류 체계 v1 — 관찰값·증거·미확인 구분

**상위 WORK_PLAN.md 1-2-F의 '큐브 대 얇은 평면', '입체 디테일 vs 텍스처 디테일', '면/요소/비례 분포'를 필수 축으로 정한다.** 결과 하나에 하나의 형태만 강제하지 않는다. **계획 정의이며 개별 2,390개에 아직 실제 판정을 적용하지 않았다.**

## 1. 축별 필드(독립 다중 레이블)
| 축 | 허용 기록·기준 | 금지 |
|---|---|---|
| **원본 역할** | `C_DIRECT_GEOMETRY`, `E_SOURCE_EXCEPTION`; D `DIRECT_SELECTED/NOT_DIRECT_SELECTED`; leaf/부모/템플릿은 F 원본 확인 후 보조 표식 | E86을 0-face 일반 큐브로 계산 |
| **기하 원형 태그** | `EXACT_FULL_CUBE`(unrotated 단일 0..16 요소), `AXIS_ALIGNED_CUBOIDS`, `THIN_ELEMENT`(해당 치수 1 이하; 0 별도), `ZERO_THICKNESS`, `MULTI_ELEMENT`, `ROTATED_ELEMENT`, `FRAME_OR_OPEN_STRUCTURE_CANDIDATE`, `INVERTED_OR_OUTSIDE_16`, `NONE_OR_UNVERIFIED`; **다중 허용** | 원본 도형 외 보이지 않는 면·실게임 형상 창작 |
| **수치** | B 실제 상속 적용 요소, 원본 from/to, 각 축 요소 크기, bbox 및 상대비(분모0 명시), zero-thickness, rotation 요소, 적용 face; min/median/max/분위수는 **독립 고유 모델** 기준 계산 | inherited face와 leaf 반복을 새 고유 face로 합산 |
| **UV·색감/재질** | C `EXPLICIT_UV/IMPLICIT_UV_KEY_ABSENT/MIXED`; slot·PNG SHA; 실제 픽셀 관찰이 있으면 알파/패턴/색감 후보 메모, 없으면 `NOT_VISUALLY_OBSERVED` | PNG 파일명만 보고 목재·유리·천 등 실제 재질 확정 |
| **디테일 담당** | `GEOMETRY_EVIDENCE`(요철/돌출을 요소로 확인), `TEXTURE_EVIDENCE`(PNG의 시각 디테일 직접 관찰), `MIXED`(양쪽 근거), `UNRESOLVED`; 실제 기하/텍스처 근거와 함께 판단 | face/element 개수만으로 텍스처 디테일 확정 |
| **방향·상태 조립** | D `VARIANT_ORIENTATION`, `MULTIPART_COMPOSITION`, `WEIGHTED_ALTERNATIVES`, `NOT_DIRECT_D_SELECTED`; x/y/uvlock 키의 **존재와 값** 개별 보존 | 원본 없는 기본 0/false를 선언된 값처럼 작성 |
| **가구 활용 후보** | `PANEL/SUPPORT/FRAME/SURFACE/SEATLIKE/CONTAINERLIKE/DOORLIKE/DECORATIVE/UNKNOWN` 등 **설계 표현 패턴**. 원형의 실제 물체 정체나 기계적 기능과 구분, 보수적 근거 작성 | 게임 속 실제 가구 종류, 수납 기능, 제작 가능성을 무근거 확정 |

- `EXACT_FULL_CUBE`는 적용 geometry provider의 원본 실제 요소 **한 개**, `from=[0,0,0]`, `to=[16,16,16]`, rotation 없음의 **정적 엄격 조건**. 다른 요소가 붙은 원형은 해당 tag 미적용.
- `THIN_ELEMENT`는 적용 element의 원본 축 치수 **어느 하나가 |to-from| ≤ 1**인 **비교·분포용 명시적 분류 기준**(마인크래프트 공식 'thin' 정의라고 하지 않음). `ZERO_THICKNESS`는 정확히 0. 단위는 모델 좌표 0~16이며 실제 마크 블록 높이/충돌 판정과 다르다.
- `FRAME_OR_OPEN_STRUCTURE_CANDIDATE` / `SEATLIKE` 같은 의미 태그는 **엄밀한 구조 기준 미제공 시 candidate**로 표기하고 이미지·모델 기하 증거와 근거 문장을 기록한다.
- 지오메트리 제공자가 없거나 E가 직접 담당하면 **기하 수치 null(미측정) 또는 not_applicable**과 검증 상태를 구분해 0 크기/0면 수라고 집계하지 않는다.
- `material_appearance_candidates`는 시각 관찰에 따른 *외형 후보*다. 실제 Minecraft block material·hardness 등 gameplay metadata가 아니다.

## 2. 출처·증거 등급 (분리 기록)
- `SOURCE_JSON_DIRECT`: F에서 해당 원본 본문 직접 열람, blob SHA/원본 증거 행 기록.
- `PRIOR_B_C_D_E_SOURCE_VERIFIED`: 해당 선행 검수의 증거 경로/SHA 재참조; F 신규 관찰 아님.
- `DETERMINISTIC_DERIVATION`: 원본 수치/조건에서 **재현 가능한** 계산(대조 알고리즘 명시).
- `PNG_VISUALLY_OBSERVED`: **원본 PNG를 실제 눈으로 확인**한 범위/대상. 이전 v69/1-1 선행 관찰은 별도 계승 표시.
- `STATIC_PREVIEW_INFERRED`: 원본 요소/PNG로 재구성한 정적 프리뷰 관찰, 엔진 내부 렌더 테스트와 구분.
- `MODELING_HYPOTHESIS`: 가구에 사용할 수 있을 법한 디자인 제안, **확정된 원본 사실과 분리**.
- `UNVERIFIED_OR_UNRESOLVED`: 증거 없음, E 런타임 특수 렌더·미인증 공식 JAR 포함.

한 행에 여러 등급이 공존할 수 있어 `geometry_evidence, UV_evidence, image_evidence, D_assembly_evidence, furniture_transfer_evidence`를 별도 작성한다.

## 3. 반드시 남길 산출물
- `STYLE_OBSERVATIONS.csv`: F 모델마다 정확히 1행, 증거 연결·다축 분류·source status·E 미확인.
- `F_GEOMETRY_FEATURES.csv`: 수치/요소·from/to/회전·bbox/비율·0두께/얇은 요소 근거; E는 해당 없음 표기.
- `F_TEXTURE_VISUAL_EVIDENCE.csv`: 원본 texture slot/PATH/SHA/PNG 근거; **실제로 관찰한 이미지**와 관찰하지 못한 이미지를 구별.
- `F_ASSEMBLY_LINKS.csv`: 해당 모델의 D blockstate·variant/multipart 참조 출처·회전/uvlock 원문.
- `F_ARCHETYPE_RULES.json`, `VANILLA_GEOMETRY_ARCHETYPES.md`: 원형 그룹·분포·원본 경로/SHA 기반 대표 예시·반례·가구 제작에 이전 가능한 규칙과 한계.
- `F_UNRESOLVED.csv`: 누락된 증거/계산/담당/차단 여부.

## 4. 감사 규칙
- 항상 **모델 경로·원본 SHA**로 연결. basename만으로 결합하지 않는다.
- 부모 템플릿 중복, 색상별 복제 및 blockstate 상태×모델 적용은 **고유 모델 분모와 별개**로 표시.
- 모든 대표 archetype에는 **원본 예시 최소 하나와 반례 또는 한계**를 명시한다. 시각 자료 확인이 안 되면 비교 주장 보류.
- `STYLE_OBSERVATIONS.csv`의 F 원본 직접 판독 2,390/2,390과 독립 재산정이 검증되기 전에는 **F 완료 불가**. E 소스 예외의 런타임 렌더 미인증은 미확인으로 소관 유지해도 원본 유형화 종료 가능.
