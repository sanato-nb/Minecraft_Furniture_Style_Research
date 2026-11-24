# INT-4 H26 — Adorn 7.6.1의 Mojang 1.21.11 기본 UV와 바닐라 PNG 실제 원본 검증

## 연구 대상과 직계 출처

상위 단계: [H25 Draft PR #107](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/pull/107), 분기 기준 388e45b95c8f1f08710fad7b68c7b848ed64b916. H25에서 확인한 5개 Adorn 모델·21개 블록상태 중 미완으로 남은 **바닐라 외부 PNG 5종과 암묵 기본 UV 400면(21상태 중복 포함)**을 독립 검증한다.

검사한 공식 원본:
- Minecraft 1.21.11 version manifest SHA-1: a969d96978af7b52dba8df44e177f48ec4ebe0d8.
- Mojang 공식 client JAR SHA-256: 1473c9489ac50fda3c435049a76a70d61a10b8610db27f5ba9d8756b686cd3bd.
- Mojang 공식 client mappings SHA-256: 517799a8485e107e932dc1bd27c002b2d0b9207eb2396b685bcfe6c3321a9fbd.
- Adorn 공식 7.6.1 / 1.21.11 Fabric JAR SHA-256: d431be4ee89d0d71b1ababedaa5275f478cfff5de94eba1165f5cd10d1b676d3.
- H25 JSON·CSV의 Git blob: 5aefb171ab57d48aebba213ccedc8dbad268fbba / 762c6f0b6b650b9ac4e137486f886e037149124a.
- 원본 JVM 실행에 필요한 Mojang 공식 라이브러리 **55개를 각각 SHA-1 검증**했다. 원본 실행 파일·모드 JAR·이미지는 Git에 저장하지 않는다.

## 1. Mojang PNG 다섯 종류 직접 확인

1.21.11 자산 인덱스에서는 대상 블록 텍스처를 찾을 수 없으나, 실제 공식 client JAR 내부 assets/minecraft/textures/block 경로의 PNG 파일 5개를 직접 읽었다. 각각 PNG 파일 신원·SHA-256과 해상도 16×16을 확인했다.

| 텍스처 | 공식 Mojang 1.21.11 SHA-256 |
|---|---|
| acacia_log | cdf7c1971c2bb95e4ddfdb6b53bd0be69a341415e43030629bb4c72b339b83c1 |
| acacia_planks | 3f84918024e190f2767e03631d8c35b31fa5cd9235d7b114738224297dca6797 |
| iron_block | dafa9944ba49fe71958553eded50e87d7bea9c7410cfe568745989bede101c49 |
| orange_stained_glass | 136ad613ee1da3520bc980cc8376abd3cf1dddb886cf89eaf37820ca051711ab |
| stone | b5e10adc72442bfb257ce7ba0b9bbe36475a0c8cdfec89b80dc9517203ff3e9f |

이 5개 PNG가 필요한 선택 소스 모델 면은 21상태 합계 **120면(중복 포함)**이다. 원본 텍스처 바이트 확인은 게임의 GPU texel·화면 픽셀 인과 승인과 다르다.

## 2. 원본 FaceBakery.defaultFaceUV를 실제 JVM에서 호출

Mojang의 실제 공식 class mappings 및 바이트코드에서 원본 메서드를 확인했다.

- 원본 FaceBakery는 난독화 클래스 hqi, 기본 UV 메서드는 a(Vector3fc, Vector3fc, Direction).
- 방향 enum은 iz, 반환 UV 레코드는 hqc$b. 공식 매핑에서 DOWN·UP·NORTH·SOUTH·WEST·EAST가 각각 연결되는 정적 필드를 확인했다.
- 실제 FaceBakery의 bakeQuad는 face.uvs가 없으면 defaultFaceUV를 호출한다. 원본 classfile에서 이 연결을 확인했다.
- 순수 Java 시험기 H26MojangDefaultUvProbe.java는 서명된 Mojang 클래스와 기본 패키지가 충돌하지 않도록 별도 mcfr.research 패키지를 사용한다.
- 공식 Minecraft 클라이언트·55 라이브러리를 Java classpath에 배치하고, 수정하지 않은 원본 static defaultFaceUV를 Reflection으로 호출한다. 파이썬에서 동일 공식 자체를 실행했다고 거짓 주장하지 않는다.
- 입력은 Adorn 실제 릴리스 5개 모델의 from/to 좌표와 face 방향이다. 출력은 Mojang 메서드의 minU/minV/maxU/maxV 실제 반환값이다.
- 독립으로 기록한 H21 분수 기반 방향별 기본 UV 규칙과 반환값이 동일한지 각 면을 대조했다.

| 구분 | 원본 얼굴 면 기록 | 검증 |
|---|---:|---|
| 5개 모델에서 고유한 기본 UV 면 | 107 | **Mojang 원본 JVM 직접 호출 107/107 성공** |
| 5개 모델에서 Adorn에 명시된 UV 면 | 32 | 원본 모델 선언값 보존 |
| 고유 선택 소스 총면 | 139 | 두 방식 합계 일치 |
| 블록상태 21개, 모델 적용 29회에서 기본 UV | 400 | 원본 107개 기본 UV 면을 상태마다 정확하게 참조 |
| 같은 21개 상태에서 명시 UV | 256 | 선언값 재사용 |
| 21상태 총면 기록 | 656 | 중복 포함 400+256 |

이 검증 결과는 **모델 원본 위치계에서 면별 UV 사각형**이며, 바닐라 텍스처로 연결되는 120면의 PNG 출처도 확인됐다. 전체 bakeQuad, 요소의 rotation, blockstate facing, uvlock, sprite atlas, GPU 샘플링, 실제 F2 프레임을 검증했다고 주장하지 않는다.

## 3. 영구 산출물과 독립 재검증

- [공식 바이트코드·PNG 사전검증 성공](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45357899373).
- [Mojang 원본 기본 UV JVM 실검증 성공](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45358922428): 5 PNG, 107 원본 메서드 직접 호출, 21상태 400 기본 UV 원본 정합.
- 원본 입력과 수치 산출을 다시 계산하는 감사기: src/mcfr/int4_h26_adorn_mojang_default_uv.py.
- Mojang 원본 메서드만 호출하는 Java 시험기: tools/research/H26MojangDefaultUvProbe.java.
- 모델·면·UV·원본 이미지 SHA·55개 라이브러리 핀·21개 블록상태 집계: project/integration/INT4_H26_ADORN_MOJANG_DEFAULT_UV_RESULT_V1.json.
- 재사용 가능한 개별 면 139행 CSV: project/integration/INT4_H26_ADORN_139_ORIGINAL_SOURCE_FACE_UV_V1.csv.
- 회귀·부정대조 테스트: tests/knowledge/test_int4_h26_adorn_mojang_default_uv.py.
- 별도 GitHub Actions: .github/workflows/integration-int4-h26-adorn-mojang-uv.yml. 최신 CI에서 원본 메서드를 다시 호출해 저장 JSON·CSV를 비교한다.

## 4. 연구 완료 범위와 후속 필요사항

- 새 원본 모델의 의미 및 학습·배포 권리를 승인하지 않는다. 실제 Minecraft 신규 세션 **0**, 네이티브 F2 **0**.
- H23의 **모델링 전용 F70 70/70** 범위 완료 상태는 보존한다. 기존 엄격 F70 최종 무조건 승인 **0/70**, H03 **HOLD**, H05 **CONDITIONAL**, INT5 의미 0, INT6 AI 학습/재배포 권리 0을 유지한다.
- **H26 종료 범위**는 Adorn 5개 모델의 Mojang 원본 기본 UV 107개 직접 호출, 21상태별 기본 UV 400면 정합, 바닐라 원본 PNG 5개 SHA 검증이다.
- 다음 단계 H27은 전체 원본 quad bake(회전·UV lock·atlas 포함) 혹은 신중하게 선택한 Adorn 실게임 F2 최소 비교를 진행한다. 이번 139면 UV 좌표만으로 전체 실게임 외형이나 모드 간 동일성을 주장하지 않는다.
