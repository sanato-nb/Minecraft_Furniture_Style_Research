# INT-4-H19 — V11 바닐라 침대 BED 블록 엔티티 타입 → BedRenderer 생성자 정확한 등록 명령 검증

## 1. 직계 출처와 연구 목적

- 직전 [H18 Draft PR #99](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/pull/99) head `995b508f7f0b76cf1be791de0d47e77f01f70648`를 부모로 하는 [H19 Draft PR #100](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/pull/100). `main`은 건드리지 않는다.
- 이미 검증한 역사 V11: Mojang Minecraft Java **1.21.11** 공식 클라이언트의 `bed.json` 일반 모델 요소/면 **0/0**, 실제 서버 머리/발 두 블록 상태 **2건**, 원본 AIR 2장/침대 2장 네이티브 F2 **4장**, AIR 대조 **0화면픽셀**과 침대 대 AIR **6,446화면픽셀**. 원본 실게임: [F11D Actions #45103243455](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45103243455).
- H18의 범위는 등록부에 `BedRenderer` 생성자 참조가 **존재**한다는 것까지였다. 이번 H19는 **정확한 `BlockEntityType.BED` 필드가 해당 생성자와 같은 등록 코드에서 연결되는지**를 추가 확인한다.

## 2. Mojang 공식 원본과 검사 결과

[H19 성공 Actions #45327234351](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45327234351), 분석 커밋 `d377b3cfd6e1e4dc6cbc401a4ab1a376d8070d4e`에서 원본 파일을 재다운로드하고 JDK 21 `javap -c -p -v` 검증.

| 검증 | 원본 직접 확인 |
|---|---|
| Mojang 1.21.11 공식 version JSON SHA1 | `a969d96978af7b52dba8df44e177f48ec4ebe0d8` |
| 공식 client JAR SHA1 | `ba2df812c2d12e0219c489c4cd9a5e1f0760f5bd` |
| 공식 client JAR SHA256 | `1473c9489ac50fda3c435049a76a70d61a10b8610db27f5ba9d8756b686cd3bd` |
| 해당 version.json에 묶인 client mappings SHA1 | `031a68bebf55d824f66d6573d8c752f0e1bf232a` |
| 합성 opcode/부정대조 회귀시험 | **13/13 통과** |
| 실제 Mojang 클래스 파일 `BlockEntityType.BED` 플래그 | **ACC_PUBLIC, ACC_STATIC, ACC_FINAL** |
| 구별되는 유효한 BED 등록 명령열 | **1개** |
| 신규 게임 실행 / 새 F2 | **0회 / 0장** |

Mojang ProGuard 매핑의 필드 선언에는 수식어가 없으므로, 매핑에서 정확한 원본 필드명 `BED`와 난독화 필드 `z`를 확인한 다음 **별도로 공식 classfile**에서 세 플래그를 검사했다. 가짜 매핑의 동명이인 필드·오류 타입·중복 필드·다른 bootstrap·다른 엔티티 타입·다른 생성자·등록 호출 부재는 실패 처리한다.

## 3. 실제 등록 바이트코드의 연결

| 코드 주소 (PC) | 명령 | 공식 원본의 대상 |
|---:|---|---|
| **193** | `getstatic` | `eld.z:Leld;` = 매핑된 `BlockEntityType.BED` |
| **196** | `invokedynamic` | `InvokeDynamic #17:create:()Lhrj;` |
| **201** | `invokestatic` | `a:(Leld;Lhrj;)V` = 블록 엔티티 타입과 렌더러 팩토리를 받는 등록 명령 |

`BootstrapMethods #17`가 가리키는 실제 메서드 핸들은 **`REF_newInvokeSpecial hrf.<init>`**, 즉 Mojang 매핑상 `BedRenderer` 생성자다. `hrk`는 `BlockEntityRenderers`, `eld`는 `BlockEntityType`, `hrf`는 `BedRenderer`의 이 릴리스에서의 난독화 클래스 이름이다.

이번 조사에서 **동일한 명령열에 원본 BED 타입 필드 조회, 침대 렌더러 생성자 팩토리, 타입+팩토리 등록 호출이 순서대로 등장한다는 사실**을 확인했다. 이는 단순한 클래스 상수풀 존재 증거보다 강하며, H18에서 미확정으로 표시했던 정확한 등록 연결을 좁은 정적 범위에서 해결한다.

## 4. 재현 가능성 및 원본 보존

- 검증 코드: `src/mcfr/int4_h19_v11_bed_registry_opcode.py`.
- 회귀시험: `tests/knowledge/test_int4_h19_v11_bed_registry_opcode.py` — **13개**.
- 재현 Actions: `.github/workflows/integration-int4-h19-v11-bed-registry-opcode.yml`.
- 기존 H18 원장을 반드시 재열람·SHA 대조한 뒤 H19 출처 검증 수행.
- [파생 분석 아티팩트 #14890322728](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45327234351/artifacts/14890322728): 직접 재다운로드해 ZIP CRC 정상, ZIP SHA256 `c118def09b72f9a4e3b44b677ee013b629d36845a49d8d3b62fe61b75f064bd1`. 내부 파생 원본 감사 JSON SHA256 `ff1f3233a969aa6751a3817623511d2ea0663e94144d17fadb9efd2d7e953ed2`.
- 영구 원장: `project/integration/INT4_H19_V11_BED_TYPE_RENDERER_REGISTRATION_RESULT_V1.json`. 공식 JAR·클래스 매핑 전체·소스코드·원본 바이트코드/텍스처를 Git에 저장하지 않고 파생 참조와 정확한 해시만 기록한다.

## 5. 완료와 남은 연구 경계

**H19 범위 통과:** 원본 Mojang 1.21.11 `BlockEntityType.BED` 정적 필드 → 특정 `BedRenderer.<init>` bootstrap #17 → 등록 코드 순서가 정확히 확인됨. [최종 Git 원장 대 공식 원본 전체 재계산 Actions #45327458960](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45327458960)에서도 **13/13 단위시험, 공식 원본 해시, BED 등록 코드, 파생 JSON 원장 전 필드 1:1 일치 검증 모두 성공**했다.

**아직 미승인:** 이전 실게임 V11 F2 촬영 중 **실제 JVM BedRenderer.render 호출 계측**(이번에는 새로운 게임 실행 없음), BedRenderer 생성 모델의 개별 파트 3D 기하·면별 UV 좌표, 원본 텍셀 → GPU 출력 화면 픽셀의 일대일 인과, 게임플레이 수면·파괴·충돌, 가구 의미·학습 및 재배포 권리.

**전체 게이트 보존:** H03 `HOLD`, H05 `CONDITIONAL`, F70 기존 증거 조건부 **70/70**, 무조건 **0/70**, H8 범위 6 PASS·1 조건부·1 보류, INT5 의미 승인 0, INT6 AI학습·재배포 권리 승인 0. **H19의 좁은 원본 소스 검증 성공은 INT-4 전체 완료를 의미하지 않는다.**
