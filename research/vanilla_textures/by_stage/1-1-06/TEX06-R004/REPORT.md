# TEX06-R004 — 아이템 모델 정의 8종·유광 6면 월드 방향 파생 검증

**날짜** 2026-11-13 · **고정 단계** 1-1-06 도기·유광도기 8개 · **기존 R001/R002/R003 원문 유지**, 공통 체크포인트 `v38` 유지.

## A/B — R003 이후 새로 찾은 사용자 추출본 정적 아이템 자료

사용자 직접 업로드 `1.21.11/assets/minecraft/items/`의 해당 **아이템 JSON 8개**를 실파일로 열어 JSON `model` 객체를 확인했다. 모두 `type=minecraft:model`, `model=minecraft:block/<texture_id>`로서 자기 블록 모델을 직접 참조. 다른 별도 모델 리소스를 증거 없이 가정하지 않는다.

미러 `InventivetalentDev/minecraft-assets` 고정 커밋 `7241a12cc2707abd7022f399c5d9033153e492e1`에서 대응 아이템 JSON **8개도 별도 직접 검사**했으며 **8/8 Git blob SHA 일치**. 파일 경로·해시·참조 대상은 `ITEM_MODEL_LEDGER.csv`. 이 **8개 신규 근거 파일**은 신규 텍스처 개수 8개가 아니라 **기존 고유 8종에 대한 아이템 단계 검증**이다.

## C/D — 기존 픽셀 결과 중복 방지

R001 2,048픽셀 명도·RGBA, R002 두 유광의 **2×2×256=512** 이미지 회전 조합, R003 사용자 PNG/정적 JSON 해시검증은 **그대로 계승**. R004에서 PNG를 새로 디코딩해 측정한 픽셀 **0**, 신규 고유 텍스처 **0**.

새 `FACING_EDGE_LOOKUP.csv`의 64개 facing 이음값은 R002 `EDGE_SEAM_PAIRWISE.csv` 원본 64개 수치에 *facing 레이블만 계산상 매핑*한 것이다. 독립 신규 RGB 분석이나 인게임 결과가 아니다.

## E1 — 원본 정적 JSON 6개 면을 4개 설치 방향에 기하학적으로 매핑

사용자 추출본 `template_glazed_terracotta.json`과 두 유광 `blockstates`를 다시 읽음. `+X=동쪽, +Y=위, +Z=남쪽` 좌표계와 오른손 +Y 회전 `Y90:(x,y,z)→(z,y,-x)`을 사용해 **2종 × 4 facing × 6면 = 48개의 월드 면 법선 대응 관계**를 직접 계산. 각 상태의 세계 6면이 모두 일대일 매핑인지 검증했다.

| facing / y° | 세계 북쪽 면←로컬(원본 UV°) | 동쪽 | 남쪽 | 서쪽 |
|---|---|---|---|---|
| south / 0° | north(90°) | east(180°) | south(270°) | west(0°) |
| west / 90° | east(180°) | south(270°) | west(0°) | north(90°) |
| north / 180° | south(270°) | west(0°) | north(90°) | east(180°) |
| east / 270° | west(0°) | north(90°) | east(180°) | south(270°) |

- 표의 괄호는 **원본 로컬 face의 UV rotation 선언값**이다. 이를 월드 화면상 최종 텍스처 회전값으로 오인하면 안 된다.
- `up`과 `down`의 출처 면은 모든 facing에서 동일하며, 원본 face UV 회전은 0°이다. 다만 모델 전체 Y 회전은 위에서 본 픽셀 방향에 영향을 줄 수 있다.
- 모든 행은 `WORLD_FACE_UV_MAPPING.csv`; 알고리즘/좌표계/출처 Git SHA는 `STATIC_MODEL_DERIVATION.json`.
- **게임 렌더러 자체의 UV 정점 변환/카메라 투영 실행은 하지 않았으므로 인게임 정적 검증이 아니다.**

## E2 — 아이템 모델과 설치된 유광 블록의 구조 차이

두 유광 item JSON은 블록 모델을 곧바로 참조하며, 설치 블록의 상태 키 `facing`은 item JSON 안에 없다. 반면 설치된 유광은 `facing=south→model_y 0°`, `west→90°`, `north→180°`, `east→270°`이다.

템플릿 모델에는 별도 `firstperson_righthand` display 변환(rotation=[0,135,0], scale=[0.4,0.4,0.4])도 있다. 따라서 **아이템 리소스와 설치 블록의 회전 입력 구조 차이**는 직접 확인됐지만, **실제 아이템이 특정 방향으로 어긋나 보이는지**는 게임 캡처 없이는 확정할 수 없다.

## D3 — 기존 R002 이음 지표를 검증할 facing 패널로 변환

상단 UV의 u→+X, v→+Z, 화면 위를 북(-Z)으로 둔 **조건부 상단 투영 가정**을 적용하면 `image_clockwise=(360-model_y)%360`. 이 계산은 **게임 실제 렌더 결과가 아니라 3D 좌표 가정에 따른 예측**이며, R002의 반대 투영 후보도 남긴다.

| 실게임 비교용 패널 | TL / TR / BL / BR | 기존 R002 4이음 RGB MAE | 동일 RGB 픽셀쌍 |
|---|---|---:|---:|
| black_A_right_hand | north / west / east / south | 4.770833 | 28/64 |
| black_B_opposite_projection | north / east / west / south | 23.302083 | 8/64 |
| white_A_right_hand | south / east / west / north | 2.145833 | 44/64 |
| white_B_opposite_projection | south / west / east / north | 89.447917 | 14/64 |

R002 최적 회전 배열의 기존 MAE **검정 4.770833, 흰색 2.145833**, RGB 완전 일치 쌍 **검정 28/64, 흰색 44/64**가 변환 뒤에도 일치함을 검산했다. 단 **동일 원장 수치를 재배열한 값**이므로 재계측한 것으로 집계하지 않는다.

`STATIC_FACING_COMPARISON.mcfunction`은 총 **4개의 2×2 비교 패널, 블록 16개**를 배치하는 **게임 내 실행용 텍스트 초안**이다. Minecraft 실제 환경에서 실행하지 않았으며 검증 화면도 수집하지 않았다.

## F — 인증 수준 (혼합 금지)

1. **사용자 제공 추출본**: PNG 8/8·모델/상태 8/8 기존 검수 유지 + **아이템 JSON 8/8 신규 검수**.
2. **기존 비공식 미러 교차**: 기존 파일 동등성 유지 + **아이템 JSON 8/8 신규 바이트 일치**.
3. **Mojang 공식 원본**: **0/8**. 원래 압축 client.jar SHA-1과 Mojang 공식 버전 메타데이터를 실제 대조하지 못함.
4. **인게임 정적 렌더**: **0/8**. 샘플 명령은 작성만 했고 실행/스크린샷 없음.

공식 서버에 대한 이 실행 환경의 DNS 접근 실패와 원본 압축 JAR의 부재로 3등급은 pending. 정적 모델/UV 기하 분석으로 3·4등급을 승격시키지 않는다.

## G — 저장/후속 연구

R004 신규 소스 파일 8, 신규 파생 world-face 매핑 48행, 기존 계측 재색인 64행. 신규 PNG 픽셀 계측 0, 고유 텍스처 누적 8 그대로.

**다음 `TEX06-R005`은 실제 Minecraft 정적 방향별 실화면 자료 또는 원본 압축 JAR SHA-1 인증 등 새 직접 근거가 있을 때만 생성.** 이전 버전 원문, 다른 재질 단계, 공통 `v38`을 건드리지 않는다. 애니메이션·PZ 변환·가구 3D 모델링은 계속 보류.
