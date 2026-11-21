# INT-2 4차 — 1-2-B 요소 원본 및 회전 AABB 수학적 독립 재검수

2026-11-21 · 원본 기준 `main@176f7f34de2336eb7984c4734e97b6eb156c19f4`.

**범위 판정: `PASS_B_ELEMENT_EVIDENCE_AND_DUAL_AABB_MATH`**.
[최초 전체 원본 실행](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/44859836398)에서 1.21.11 JSON 모델을 직접 다시 읽고, 기존 1-2-B 요소 원장 `ELEMENTS_P1_ALL.csv`/`P2_ALL.csv`/`P3_ALL.csv`의 전체 개별 행과 대조했다. 구 B 분석기를 임포트하거나 실행하지 않았다.

## 원본 요소 개별 대조

| 검증 지표 | 기존 1-2-B | 이번 직접 재산출 | 차이 |
|---|---:|---:|---:|
| 일반 정적 모델 / E 특수 범위 | 2,304 / 86 | 2,304 / 86 | 0 |
| 부모상속을 거친 적용 요소 | 5,689 | 5,689 | 0 |
| 5,689개별 B 근거(좌표/회전/face/부모 형상제공자) | 5,689 | **5,689 일치** | **0** |
| 적용 face | 23,090 | 23,090 | 0 |
| 로컬 rotation 선언 요소 | 1,548 | 1,548 | 0 |
| 0두께 요소 | 1,965 | 1,965 | 0 |
| 0~16 좌표 범위밖 요소 | 413 | 413 | 0 |
| 좌표 역전 요소 | 18 | 18 | 0 |

- B의 고정 파일 행 5,689개와 새로운 모델별 `(leaf_path, element_index)` 고유 키를 전수 비교했다.
- 원본에서 부모 경로를 따라 실제 `elements` 제공 모델을 확인하고 from/to, rotation, face, 부모 제공자를 비교했다.
- B가 원래 구분한 0두께/범위밖/좌표 역전은 **모두 불법이라고 단정할 오류가 아니다**. 실제 원본 선언 현상을 집계한 것이다.

## 회전 후 AABB 검산

회전 선언 요소 1,548개의 중심·모서리·회전 축·각도·pivot·rescale 값을 원본에서 읽었다. 동일한 수학적 회전 변환에 대해 두 가지 다른 경계 계산을 각각 수행했다.

1. 요소 박스의 8개 꼭짓점을 회전 변환한 뒤 축별 최솟값·최댓값 산출.
2. 요소 중심점/반크기를 회전 행렬로 변환하고, 회전 행렬의 절댓값과 반크기 벡터로 경계 직접 산출.

**1,548/1,548개에서 두 방식의 좌표 차이가 허용오차 1e-9 이내.** [회전요소별 1,548행 CSV](INT2_B_ROTATED_ELEMENTS.csv)에 원본 출처·회전·계산된 AABB·수학식 간 최댓값 오차를 기록했고, [기계 판독 총계](INT2_B_ROTATION_SUMMARY.json)에 집계했다.

**중요한 제한:** 두 방식은 *동일한 회전변환 가정*에 대한 수학적 상호 검산이다. Minecraft Java 런타임의 baked quad 구현·회전 rescale 세부 정책과 독립 비교한 것은 아니며, 게임 충돌 상자(VoxelShape)와 같다고 주장할 수 없다. 또한 blockstate x/y, uvlock, 아틀라스·조명·실제 렌더는 이번 범위 밖이다.

## 기록 및 재현

- [검사기](../../scripts/integration/audit_int2_rotation.py)
- [AABB 수학 회귀 테스트](../../tests/integration/test_int2_rotation.py)
- [검증 Actions](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/workflows/integration-int2-rotation.yml)
- `python scripts/integration/audit_int2_rotation.py --root . --out /tmp/int2-rotation`
- CI는 저장된 1,548행·집계 JSON을 새로 계산한 결과와 **바이트/필드 일치**까지 재검증한다.

기존 소스·B 역사 원장·1-1~1-5 연구 결과를 수정하지 않았다. 이번 수학 검산 성공은 AI 모델 훈련·모델링 능력 승인으로 승격되지 않는다.

**후속 INT-2:** 런타임 회전·상태 조립의 엔진 검증은 별도 경계로 남기고, 기존 가구 모드 1-3 정적 구조 원본의 독립 재감사로 넘어간다.
