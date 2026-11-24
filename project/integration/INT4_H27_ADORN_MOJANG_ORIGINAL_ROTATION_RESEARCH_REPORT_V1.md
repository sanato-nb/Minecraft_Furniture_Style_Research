# INT-4 H27 — Adorn 7.6.1 / Mojang 1.21.11 원본 회전·꼭짓점 검증

## 1. 상위 단계와 증거 신원

H26 [Draft PR #108](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/pull/108), head d28e9c198b9e636b6fcb4922a8d3f9220e2be39a에서 분기한다. H26에서 확인한 기본 UV 107고유면/400상태별 면, Adorn 명시 UV 32고유면/256상태별 면, 바닐라 5 PNG를 보존하면서 **상태 방향 및 요소별 실제 Minecraft 회전 결과**만 새로 검사한다.

원본 고정 신원:
- Mojang 1.21.11 공식 manifest SHA-1: a969d96978af7b52dba8df44e177f48ec4ebe0d8.
- 공식 client JAR SHA-256: 1473c9489ac50fda3c435049a76a70d61a10b8610db27f5ba9d8756b686cd3bd.
- 공식 mappings SHA-256: 517799a8485e107e932dc1bd27c002b2d0b9207eb2396b685bcfe6c3321a9fbd.
- 공식 Adorn 7.6.1 Fabric JAR SHA-256: d431be4ee89d0d71b1ababedaa5275f478cfff5de94eba1165f5cd10d1b676d3.
- 부모 H26 JSON/CSV 원본 Git blob: e7dbb1c17e4fa9bd8f6b4cc7d09e0282c4c739ab / e722131593a883f713f300eefc8846b06f4766a7.
- 공식 JVM 라이브러리 55개 각 SHA-1 독립 검증. 원본 JAR·PNG·매핑 바이너리 파일은 이 저장소에 복제하지 않는다.

## 2. 컴파일된 원본 Mojang 코드 실제 호출

원본 mappings 및 bytecode에서 아래 클래스와 메서드의 정확 신원을 확인한 뒤, Java 21 격리 JVM에서 수정되지 않은 원본을 직접 호출했다.

1. Variant.SimpleModelState.asModelState → ModelState.transformation → Transformation.getMatrix로 X/Y/Z Quadrant 모델상태 회전 행렬 조회.
2. BlockElementRotation.SingleAxisRotation → BlockElementRotation.transform으로 필요한 요소의 실제 원본 회전 행렬 조회.
3. FaceBakery.BLOCK_MIDDLE 상수를 공식 클래스에서 직접 읽음.
4. 원본 FaceBakery.rotateVertexBy(Vector3f, Vector3fc, Matrix4fc)를 Reflection으로 실제 실행. **요소 회전 다음에 블록상태 회전**을 적용한다.
5. 모드 JAR에서 직접 읽은 from/to·회전 원점·축·각도와 21개 원본 상태 선택을 사용하고, 독립 Python 감사기로 출력 신원을 재정합한다.

시험기 Java 패키지는 원본 Mojang의 서명된 패키지와 충돌하지 않는 별도 mcfr.research를 사용한다. 검증 도중 발견한 Java 컴파일 의존성 문제, JVM 입력 ID 대소문자 문제, JSON float·정수형 표현과 CSV 표기 문제는 **원본 수식이나 원본 코드 변경 없이 시험기·원장 처리만 수정**했다.

## 3. 실제 검증 결과

| 항목 | 값 |
|---|---:|
| 공식 원본 Adorn 모델 | 5개 |
| 서로 다른 원본 모델 요소 | 29개 |
| 정확한 원본 블록상태 | 21개 |
| 상태별 선택 모델 적용 | 29회 |
| 상태별 원본 요소 적용 (중복 포함) | 136개 |
| 원본 Mojang 꼭짓점 변환 | **1,088개 (136 × 8)** |
| 철제 선반 요소별 -45도 회전 적용 | **8회 (2요소 × 4상태)** |
| 기존 H26 고유면 / 상태별 면 기록 | 139 / 656 유지 |
| 신규 실제 Minecraft 게임 실행 / F2 | 0 / 0 |

- 아카시아 커피 테이블 기본 상태는 요소 12개, 모델 좌표 전체 경계 최소 (0,0,0), 최대 (16,12,16).
- 철제 선반은 4방향 상태의 Y 회전 north=270도, east=0도, south=90도, west=180도를 사용한다. 선반 3개 요소 중 2개가 원본 JSON의 축 Z, 각도 -45도, 서로 다른 origin을 사용한다.
- 커피 제조기 16상태는 facing 4 × active 2 × has_mug 2 조합이며, 머그잔 없을 때 3요소, 있을 때 11요소(기본 3 + 머그 8)를 동일한 방향 상태 모델 회전으로 변환했다.

### 원본 JVM에서 계산된 철제 선반 회전 후 경계

단위는 **블록의 내부 모델 0~16 좌표 단위**이며 실제 게임의 충돌/히트박스 또는 관찰한 인게임 픽셀 범위가 아니다.

| 상태 | Y | 최소 XYZ | 최대 XYZ |
|---|---:|---|---|
| north | 270 | (0, 0.81802, 9) | (16, 6, 16.68198) |
| east | 0 | (-0.68198, 0.81802, 0) | (7, 6, 16) |
| south | 90 | (0, 0.81802, -0.68198) | (16, 6, 7) |
| west | 180 | (9, 0.81802, 0) | (16.68198, 6, 16) |

원본 요소 회전으로 인해 -0.68198보다 작은 모델 좌표 및 16.68198처럼 16보다 큰 좌표가 나온다. 따라서 모델의 원본 축정렬 from/to만으로 상태 회전 후 형상 범위를 확정하면 오류가 생긴다.

## 4. GitHub Actions 및 영구 산출물

- [H27 공식 Mojang 모델 회전 클래스 매핑 확인 성공](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45363152332).
- [H27 원본 FaceBakery.rotateVertexBy 실제 바이트코드 확인](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45363327228).
- [H27 실제 Mojang JVM 1,088꼭짓점 검증 성공](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45364287774).
- [H27 최종 영구 JSON·21행 CSV 독립 대조, 회귀시험 13/13 통과](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45364744909).
- Python 감사기: src/mcfr/int4_h27_adorn_mojang_rotation_vertices.py.
- 실제 JVM 원본 변환 호출기: tools/research/H27MojangElementStateRotationProbe.java.
- 개별 136요소 × 8 꼭짓점·Mojang 55개 라이브러리 SHA·21상태: project/integration/INT4_H27_ADORN_ORIGINAL_MOJANG_ROTATED_VERTICES_V1.json.
- 상태별 선택 모델·회전 각도·변환 후 경계 21행: project/integration/INT4_H27_ADORN_21_STATE_ROTATED_BOUNDS_V1.csv.
- 회귀·부정대조 13건: tests/knowledge/test_int4_h27_adorn_mojang_rotation_vertices.py.
- 전용 GitHub Actions: .github/workflows/integration-int4-h27-adorn-mojang-rotated-vertices.yml.

## 5. 명확한 한계와 승인 경계

**H27 검증 완료 범위는 원본 Mojang 모델상태·요소별 회전 및 1,088개 꼭짓점 변환이다.** 아직 원본 FaceBakery.bakeQuad 전체를 실행하여 쿼드의 winding/culling/uvlock/atlas/실제 픽셀을 검증한 것은 아니다. 이번 원본 21상태는 uvlock=false로 제한된다. 블록의 충돌체, 인게임 F2, GPU 렌더링, 모든 Adorn 모델 또는 다른 모드와의 모델 동등성을 검증했다고 주장하지 않는다.

H23의 **별도 모델링 F70 70/70 범위 완료 유지**. 기존 엄격 F70 무조건 0/70(조건부 70/70), **H03 HOLD**, **H05 CONDITIONAL**, INT5 가구 의미 승인 0, INT6 학습·재배포 권리 0. 원본 게임 실행 및 F2 0. main 변경/병합 없음.

후속 **H28**은 원본 FaceBakery.bakeQuad 및 sprite atlas에 필요한 의존성을 공식 소스에서 좁혀 실제 전체 쿼드를 검증하거나, 실제 Adorn 게임에서 최소 F2를 찍어 원본 회전 수치와 비교하는 연구로 분리한다.
