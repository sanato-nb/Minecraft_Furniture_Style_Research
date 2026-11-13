# TEX08-R004 — 사용자 추출본 39 모델·8 부모 체인의 정적 모델 전체 면/UV 검사

**2026-11-13 | 1-1-08 복합·기능면 | 대상 PNG 21개 그대로 | 전체 v38 불변**

## 핵심 결과와 모집단
- 1차 원본: 사용자가 JAR 압축 해제 후 GitHub에 업로드한 `1.21.11/assets/minecraft/models/block/` 및 blockstates. **Mojang 공식 JAR SHA1 인증을 했다는 뜻이 아니다.**
- R003에서 직접 파싱했던 **모델 10개를 재실적으로 가산하지 않고**, 이번에 그 밖의 **29개 leaf/template/child 모델 JSON을 실제로 새로 읽음**. 이 단계에서 관리하는 39개 소스 모델은 **39/39** 원본 JSON 직접 파싱 근거 보유.
- 별도 공통 부모 모델 JSON **8개를 새로 직접 읽어** 부모 상속을 실제 추적: `block`, `cube`, `cube_all`, `cube_bottom_top`, `cube_top`, `cube_column`, `orientable`, `orientable_with_bottom`. 직접 파싱된 부모 포함 고유 모델 JSON 경로 **47개**.
- 고정 대상 텍스처 21개와 무관한 재질도 전체 모델 face 해석에는 연결되지만 **21개 표본의 신규 PNG 실측으로 세지 않았다**. `MODEL_FACE_RESOLUTION.csv`에는 resolved texture path만 보존; 해당 범위 밖 PNG의 화소 검증은 수행하지 않았다.
- 모델 39개 × 유효 면은 **143 face-model rows** (명시 UV29, 부모 cube 유도/암시 UV114). 모든 UV 직사각형의 면적 합은 **32,512 texel-uses**, 단 **이것은 UV 지정 면적 합계이지 새로운 실제 PNG 픽셀 샘플링 결과가 아니다**. 후자의 신규 측정 건수 0.
- 모델 39에는 **슬롯 템플릿 6개가 별도 모델로 포함**되어 있어 child를 함께 세면 중복 소스 face 선언을 모델 단위로 다시 등장시킨다. 템플릿을 제외하면 렌더 대상으로 선택되는 **33 leaf 모델의 137 face-model rows**. 이는 blockstate 선택 상태 수나 고유 기하 면 수와 다르다.
- 모델 구성: `cube` 상속 19모델×6면=114, `enchanting_table` 직접 6면, `chiseled_bookshelf` 본체 직접 5면, 슬롯 템플릿 6면, 슬롯 자식 모델 12면. 기하/UV 출처를 각 face 행에 분리 기재.

## 부모 상속에 대한 추가 실증
- `cube.json`이 직접 선언한 유일한 요소는 `from=[0,0,0]`·`to=[16,16,16]`인 1개 육면체이며 6개 면의 `texture="#down/#up/#north/#south/#west/#east"`를 선언한다. 이 파일에는 명시 UV가 없다. **[0,0,16,16]은 상속 기하로부터 계산한 UV 유도**이고 직접 선언된 숫자와 구분해야 한다.
- `cube_all`은 여섯 면 및 particle을 `#all`로, `cube_column`은 측면/particle을 `#side`, 상·하단을 `#end`로, `cube_top`은 5면/particle을 `#side`와 윗면 `#top`으로 매핑한다.
- `cube_bottom_top`은 particle 및 4측면 `#side`, 아래 `#bottom`, 위 `#top`으로 연결. 따라서 `barrel_open`도 여전히 **측면/아래의 동일 기본 PNG를 재사용**하며 위만 `barrel_top_open`으로 교체한다.
- `orientable`은 `orientable_with_bottom`을 상속하면서 **`#bottom`을 `#top`으로 연결**한다. `orientable_with_bottom`은 최종 `cube` 상속으로 6면을 사용하고, 북쪽 `#front`, 동남서 `#side`, 위 `#top`, 아래 `#bottom`, particle `#front`를 연결한다. `beehive_empty`와 `beehive_honey`는 particle을 별도 `#side`로 **직접 override**한다.
- `enchanting_table`은 부모 `block/block`의 표시 프리셋만 상속하고 **자체 요소 [0,0,0]..[16,12,16]**을 선언, 위/아래 UV `[0,0,16,16]`, 네 측면 `[0,4,16,16]` 명시. 이 모델의 여섯 면을 전부 포함했기 때문에 R001의 **목표 텍스처에 대한 4측면 기록**과는 분모가 다르다.

## 끌로 조각한 책장: 새 슬롯 기하와 부모 particle 의미
- `chiseled_bookshelf` 본체는 [0,0,0]..[16,16,16] 1개 요소의 **east/south/west/up/down 5면만 선언**하며 **north 정면은 선언하지 않는다**. particle은 본체의 `#top`.
- 슬롯 템플릿은 각각 `z=0`의 **0두께 평면, 북쪽 단일 면, cullface=north**. 슬롯 UV는 6개가 위/아래 행에서 [0..6], [6..11], [11..16]의 폭으로 나뉜다.
- **기하 x와 PNG UV x가 반대 좌우 순서**로 정의됨: `top_left` geometry x10..16 ↔ UV x0..6, `top_mid` x5..10 ↔ UV x6..11, `top_right` x0..5 ↔ UV x11..16 (하단도 동일). 이는 소스 좌표의 대응이며 실제 화면 좌우 표시는 별도 렌더 검증 대상이다.
- 템플릿 6종은 `textures.particle="#texture"`를 **직접 선언**하고, 각각의 `empty/occupied` 자식 모델은 `#texture`를 실제 empty/occupied PNG로 바꾸는 방식으로 **particle 슬롯이 상속 해결된다**. 기존 R001/R002에서 “슬롯 overlay에 particle이 없다”로 쓴 표현은 **모델 JSON 선언 차원에서 부정확**하여 이번에 명시적으로 정정한다. 다만 최종 multipart 블록에서 실제 어떤 model particle이 우선 선택되는지는 인게임 미검증이므로 **그 효과까지 단정하지 않는다**.
- blockstates JSON에서 각 `facing=north/east/south/west`당 base 1규칙(`uvlock=true`) + 슬롯 `12`개 조건 규칙(`uvlock` 생략/false). Y 회전 0/90/180/270; 실제 상태 1개에서는 `base 1 + 선택된 slot children 6`을 적용. 이 규칙 개수 **52**는 R002/R003 검증 재사용이며 신규 상태 수로 더하지 않는다.

## 기존 A–G와 4단계 증거 경계
- **(1) 사용자 추출본:** 39단계 모델 JSON을 모두 직접 파싱(10종 R003 재사용 + 새 29종), 공통 부모 8 JSON 신규 직접 파싱; 143 face-model 정적 소스 연결표 작성.
- **(2) 미러 교차:** R003 기존 71/71 SHA 동일성을 그대로 보존. 이번에 별도 미러 다운로드/재픽셀 분석을 했다고 주장하지 않음.
- **(3) Mojang client.jar SHA1 및 공식 버전 metadata:** 아직 0/21, 미완료.
- **(4) Minecraft 실제 게임 정적 조명·uvlock·particle·렌더 관찰:** 아직 0/21, 미완료.
- **C 원본 PNG 신규 픽셀/알파 실측 0**, **애니메이션 분석 0**. R001–R003와 전체 v38 불변. PZ 변환/가구 3D 모델 제작도 미수행.

## 결과 파일
- `SOURCE_LEDGER.csv`: 39 모델 + 추가 부모 8의 SHA 및 읽기 상태
- `MODEL_INHERITANCE.csv`: 39 모델별 실제 parent, particle, effective face/UV 상태
- `MODEL_FACE_RESOLUTION.csv`: 143 모델-면별 선언 texture slot → 최종 참조 텍스처 해석, 좌표/UV/출처, 템플릿의 unresolved placeholder 구분
- `CHISELED_SLOT_GEOMETRY.csv`: 6개 zero-thickness 슬롯 면 좌표·UV·입자 선언과 양쪽 자식 SHA
- `CHISELED_FACING_UVLOCK.csv`: 4방향별 회전·본체 vs 슬롯 uvlock 설정
- `SUMMARY.json`: 중복 없는 신규 결과·미검증 상태

**차기 TEX08-R005**; 사용자 추출본 1차, 미러 2차. 새 분석은 자기 단계 신규 폴더에서만 수행.
