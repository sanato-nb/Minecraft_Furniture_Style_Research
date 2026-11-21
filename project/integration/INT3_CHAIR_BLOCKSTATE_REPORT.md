# INT-3 / 원본 의자 블록상태 방향·회전 및 텍스처 적용 16방향 감사

**범위:** Minecraft Furniture Style Research 고정 연구 자료 INT-3; 선행 [PR #31](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/pull/31)의 AF/HC/Macaw 의자 4종 229면 원본 PNG·UV 진단 렌더와 비교해 **블록상태의 원본 모델 선택·회전(y)을 실제 조사했다.**

## 결과의 신뢰 경계

- **PASS:** 모드 원본 3개 블록상태 JSON의 바이너리 SHA 및 228개 모델 선택 규칙과 이전 1-3-F state/rule/option 원장 사이의 차이 **0**.
- **PASS:** 선택한 4개 의자 자식 모델을 북/동/남/서로 배치할 때 지정되는 원본 상태의 모델 ID/회전과 16개 기하 AABB가 소스 기반 계산으로 재현.
- **PASS:** 이미 PR #31에서 통과한 8개 원본 PNG·229면 UV·모델/부모 SHA 검사기를 재사용해, 4×4 **16개 방향에 실제 PNG 픽셀을 붙인 정사영 진단 렌더** 생성.
- **NOT VERIFIED:** 실제 Minecraft 클라이언트의 모델 베이크, UV lock 처리, GPU 아틀라스, ambient occlusion, 빛/투명도·컬러 tint, 렌더 순서, 부품의 사용 기능, 충돌, 외부 모드의 라이선스/AI 훈련 허용. 진단 렌더가 게임 스크린샷과 같다는 주장은 하지 않는다.

## 원본 전수검수 숫자

| 원본 블록상태 | 원본 상태 키 = 모델 선택 옵션 | 서로 다른 소스 모델 | 방향별 y |
|---|---:|---:|---|
| Another Furniture: `another_furniture:acacia_chair` | **88** | 22 | 0/90/180/270° 각 22 |
| Handcrafted: `handcrafted:warped_chair` | **136** | 17 | 0/90/180/270° 각 34 |
| Macaw: `mcwfurnitures:acacia_chair` | **4** | 1 | 0/90/180/270° 각 1 |
| **합계** | **228** | 블록별 중복 제외 | **228/228 원장 일치** |

각 상태의 모델 target, `x`, `y`, `uvlock`, `weight`, 상태 selector 및 원본 해시를 **직접 읽고** 이전 1-3-F의 동일 원본 `state / rule / option`과 대조했다. `x=0`, `uvlock=false`인 사례만 확인되었다.

### 원본에서 발견한 예외 — 자동수정 금지

Another Furniture 고정 원본의 `facing=south,tucked=false,variant=3`은 모델 `another_furniture:block/chair/acacia_1`을 참조한다. 같은 `variant=3,tucked=false`의 북/동/서는 `acacia_3`을 참조한다.

원본의 **동일한 1개 속성 조합 내 모델 대상 불일치**를 확인했으며, 4방향 모두의 그룹을 구성하는 **4행을 검토 범위로 기록**했다. 예외가 네 번 발생했다는 뜻이 아니다. 원본의 의도적인 재사용인지 오탈자인지는 미확정. 기존 연구 DB와 새 원본 대조에서는 **228개 중 내용 불일치 0**이며, 자동으로 `acacia_3`으로 수정하지 않았다.

### 원본 모델 선택·방향 범위

| 선택한 자식 | 원본의 해당 모델 선택 옵션 수 | 검증에 사용한 방향별 기본 상태 | 원본 `y` 순서 (북·동·남·서) |
|---|---:|---|---|
| AF121 — acacia_1 | 5 | variant=1,tucked=false (variant=3 남쪽의 참조 1행이 추가됨) | 0·90·180·270 |
| AF123 — acacia_10_tucked | 4 | variant=10,tucked=true | 0·90·180·270 |
| HC11210 — warped_chair_black | 8 | color=black,waterlogged=false | 0·90·180·270 |
| MACAW67 — acacia_chair | 4 | facing만 명시된 상태 | **90·180·270·0** |

부모 요소 좌표와 단위 블록 중심 `(8,8,8)`을 기준으로 `y` 회전을 적용해 4×4 **16개 소스 기하 자세**를 계산했다. 기존 1-3-F `geometry`의 원본 제공자·face 수(46/46/78/59)를 먼저 검증한다. Y축 360도 폐쇄성이 확인되며, 이 검사는 **블록상태 y 값으로 회전한 기하 근거**이지 Minecraft 런타임의 baked vertex 검사로 간주하지 않는다.

원본 AABB는 0~16 단위 내부에만 있지는 않다. 특히 AF123 tucked는 방향에 따라 한 축이 약 -7~23까지 나가며, HC11210는 Y 상단 약 27.946723이다. 이것은 원본 모형의 시각 배치 범위이고, 충돌 박스·여러 블록 점유·실제 게임 기능이라고 자동 해석하지 않는다.

## 사용한 증거 및 재현성

- `scripts/integration/audit_int3_chair_blockstates.py`: 고정 원본 3종 JSON을 소스 SHA로 다시 확인하고 **228개 상태 전체**를 F 원장에 전수 대조. 원본 이상 연결을 그대로 기록. 네 자식의 16개 회전 AABB.
- `scripts/integration/render_int3_chair_direction_previews.py`: PR #31의 원본 PNG와 UV 모델 감사·정사영 렌더를 재사용, **4×4 텍스처 적용 관찰 이미지** 생성.
- `scripts/integration/render_int3_textured_chairs.py`: 기존 코드에 블록상태 `y` 회전 선택지만 추가. 회전 0인 원래 PR #31의 이미지·229면 SHA 결과는 변경되지 않게 유지.
- `project/integration/INT3_CHAIR_BLOCKSTATE_SOURCE_SUMMARY.json`: 블록별 소스/회전 분포, 검토 그룹, 고정 전수 CSV·16방향 CSV SHA-256.
- `project/integration/INT3_CHAIR_16_TEXTURED_POSE_SUMMARY.json`: 16방향 텍스처 진단 이미지·위치/원본 해시/범위 설명·결과 SHA-256.
- [원본 블록상태와 16개 방향 모델 진단 최초 성공 CI #44888595540](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/44888595540).
- CI 아티팩트 `int3-original-chair-blockstate-direction-evidence`: 모든 228개 원본 상태 모델 선택 기록 CSV, 16개 회전 기하 CSV, 원본 이미지 픽셀을 응용한 진단 4×4 PNG, 16개 그림 추적 CSV 및 JSON 2종. **원본 PNG/JAR/모델 JSON 파일 자체는 재배포하지 않음**.

소스 선택 옵션 원장 CSV SHA-256 `3c2a79abdb528f04d1dc42d9c06970fd77d9adda802700f14d3fb2749bcdcdad`. 16개 기하 자세 CSV SHA-256 `a5452e9a8b1fe2741654d4f74dd2aaec1f09bc9554659a55b997b86abc238e98`. 16방향 텍스처 진단 PNG SHA-256 `9860fdd3df57f95a774ed00f0bc7770535b720e040ec476ca58602f0dfc04073`.

## 다음 검증 경로

1. **실제 마인크래프트 클라이언트에서 모드 3종 로드 후 각 상태의 화면 자료 확보**: 방향/외형·렌더링 효과를 진단 16방향과 나란히 비교.
2. 런타임 기반 bbox·UV lock/tint/AO 검증. 소스상의 리소스나 텍스처 이름을 재료·스타일의 물리적 증거로 승격시키지 않음.
3. 연구 저장소의 미확정 역할 45건·비교 후보 14건을 이 블록상태 출처·회전 근거와 연결, 검수 완료 전 규칙으로 확정하지 않음.
4. 외부 원본 자산의 권리 검토 및 향후 **새로 작성한 가구만을 사용한 생성 PoC**를 별도로 진행.

**판정:** 원본 블록상태 228/228 일치 및 16/16 방향의 소스 기하·PNG 진단 재현 통과. 실제 게임 클라이언트 렌더·가구 기능/재료/스타일·AI 학습 승인 범위는 아직 보류.
