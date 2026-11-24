# INT-4-H18 — Minecraft Java 1.21.11 바닐라 V11 침대 공식 BedRenderer 바이트코드 출처 검증

## 1. 연구 위치 및 이전 증거
- 직계 원본 연구: [INT-4-H17 Draft PR #98](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/pull/98) head `2552cb59ea04763f3b9a7e369ec7c97d4555027a`; 이번 [H18 Draft PR #99](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/pull/99)는 #98 head 브랜치에서 분기했으며 `main`을 병합하지 않았다.
- 목표는 **바닐라 특수 렌더링의 공식 렌더러 클래스·등록부 연결 조사**다. 일반 JSON 모델에 요소가 0개라는 이유로 '침대가 없는 모델'이라고 오판하는 경로를 차단하는 데 목적이 있다.
- 고정 선행 증거: `project/integration/INT4_F11D_V11_WHITE_BED_REAL_F2_SOURCE_V1.json`, 실제 [F11D V11 Actions #45103243455](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45103243455). 공식 모델 0요소·0면, 실게임 서버 머리/발 상태 2건, AIR F2 2장 + 침대 F2 2장, 빈 화면 대조 **0픽셀**, 침대 대비 **6,446픽셀**.
- 앞선 H03/H05 보고서는 이 자료만으로 Java 메서드 직접 호출을 확정하지 않았으며, 그 근거 경계를 유지한다.

## 2. 최신 원본 소스 독립 확인
[H18 성공 GitHub Actions #45324711008](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45324711008), 소스 커밋 `0ca0e94f1a19772ca3d5cbd5cac928e8a7194600`.

| 검사 | 직접 결과 |
|---|---|
| Mojang 1.21.11 버전 JSON SHA1 | `a969d96978af7b52dba8df44e177f48ec4ebe0d8` 통과 |
| 공식 클라이언트 SHA1 | `ba2df812c2d12e0219c489c4cd9a5e1f0760f5bd` 통과 |
| 공식 클라이언트 SHA256 | `1473c9489ac50fda3c435049a76a70d61a10b8610db27f5ba9d8756b686cd3bd` 통과 |
| 공식 `client_mappings` SHA1 | `031a68bebf55d824f66d6573d8c752f0e1bf232a` 통과 |
| 실행 환경 | JDK 21 `javap -v -c -p`로 원본 컴파일 classfile 재열람 |
| 회귀시험 | **10/10 통과** |
| 모델 `bed.json`의 일반 요소/면 | **0/0** 및 원본 Git blob SHA1 일치 |
| 새로운 Minecraft 실게임 실행·F2 촬영 | **0회 / 0장** |

## 3. 공식 Mojang 클래스 매핑과 등록부 연결

| 공식 명칭 | 실제 확인된 클라이언트 클래스 |
|---|---|
| `net.minecraft.client.renderer.blockentity.BedRenderer` | `hrf.class` |
| `net.minecraft.client.renderer.blockentity.BlockEntityRenderers` | `hrk.class` |
| `net.minecraft.client.renderer.blockentity.BlockEntityRenderDispatcher` | `hrh.class` |
| `BedRenderState` | `hsk` |
| `BedBlockEntity` | `ekx` |
| `BlockEntityType` | `eld` |
| `BedSpecialRenderer` (아이템 특수 모델 경로) | `ijx` |

- `BlockEntityRenderers`의 실제 클래스 상수풀에서 **`hrf` 소유자 관련 참조 5줄**을 확인했다. 포함된 참조 유형은 `Class`, `Methodref`, `REF_newInvokeSpecial hrf.<init>` 메서드 핸들이다. 이는 **침대 전용 렌더러 생성자에 대한 컴파일된 등록부 참조가 실제로 존재**한다는 정적 증거다.
- `BedRenderer` 원본 바이트코드는 `BedRenderState`(obf `hsk`)와 관련 클래스 참조 **32줄**, `BedBlockEntity`(obf `ekx`) 참조 **18줄**, `BlockEntityType`(obf `eld`) 참조 **4줄**을 포함한다. 동일 원본 클래스에서 `BedSpecialRenderer`(obf `ijx`) 직접 참조는 **0줄**이다. 이는 아이템/블록 렌더링 모든 경로의 배제를 뜻하지 않는다.
- 원본 클래스 전체를 Git에 저장하지 않고, 제한된 소유자 식별·매핑·해시만 기록한다.
- 정적 `javap` 출력 해시: `BedRenderer 5ddf796ac8a055331c079909df76f68208ef22fbea916796e6ef351af7905a44`, `BlockEntityRenderers abd98a24b265345ee88e88581f1f1ac62e31c2b0735ca211a7f6a9b75d3b9f7e`, `BlockEntityRenderDispatcher 95393de2216f7042e02368382bad65295cbbc8603d5fb89e9de9c99b21e6b78c`.

## 4. 아티팩트와 재현성
- 원본 Mojang 클라이언트·매핑은 GitHub runner의 임시 경로에서만 다운로드하여 정확한 SHA를 검사했다.
- [파생 분석 아티팩트 #14889091838](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45324711008/artifacts/14889091838) ZIP SHA256 `b446a87566ca7232fb4a2f128c5d9b374e06f9d9b0eef8b1bb64b1e171df4f32`; 별도 내려받아 **ZIP CRC 확인 성공**. 원본 JAR/매핑/전체 `javap` 디스어셈블은 아티팩트에 포함하지 않았다.
- 재현용 소스: `src/mcfr/int4_h18_v11_bed_renderer_bytecode.py`; 회귀시험 `tests/knowledge/test_int4_h18_v11_bed_renderer_bytecode.py`; Actions `.github/workflows/integration-int4-h18-v11-mojang-bedrenderer-bytecode.yml`.
- 영구 지식 원장: `project/integration/INT4_H18_V11_BED_RENDERER_STATIC_BYTECODE_SOURCE_V1.json`. 원본 경로·SHA·공식 클래스·코드 참조·이전 F2 출처와 승인 범위를 고정한다.
- 첫 Actions에서 잘못 구성된 합성 테스트 픽스처로 10개 중 2개가 실패했고, 시험용 SHA와 ZIP 대조 데이터를 바로잡은 뒤 최종 성공. 공식 원본 바이트코드는 처음 성공한 실행에서만 통과로 취급한다.

## 5. 확인과 미확정의 구분
**확정한 좁은 사실:** Mojang 공식 1.21.11 클라이언트는 `BedRenderer` 클래스와 독립 렌더러 등록부를 갖고, 등록부의 컴파일된 상수풀에 해당 렌더러 생성자 메서드 핸들 참조가 존재한다. 역사 V11의 공식 `bed.json` 일반 요소/면은 0이고, 원본 Minecraft F2에서는 두 부분 침대 외형이 관찰됐다.

**아직 확정하지 않은 부분:** 이전 V11 F2 촬영 순간의 **실제 JVM BedRenderer 메서드 호출 기록**, `BlockEntityType.BED` 정확한 정적 등록 명령 한 줄과 생성자 연계의 코드 위치 단위 재대조, BedRenderer 내부 메시 파트별 정확한 3D 지오메트리 및 UV 원장, 원본 텍셀→GPU 화면 픽셀 인과. 정적 호출/등록 근거를 동적 호출로 승격하지 않는다.

후속 H18 확장은 원본 매핑의 `BlockEntityType.BED` 필드와 등록 메서드 호출의 구체적 bytecode 위치를 독립 확인하거나, 연구 목적상 꼭 필요한 최소 계측 시나리오만 선택한다. 침대 수면·파괴·충돌이나 모든 게임 상호작용을 모델링 연구의 필수조건으로 확대하지 않는다.

**종료 게이트 보존:** H03 `HOLD` / H05 `CONDITIONAL`; F70 70/70 조건부·**무조건 0/70**; H 범위통과 6/8·조건부 1/8·보류 1/8, INT5 의미 승인 0, INT6 AI학습·재배포 권리 승인 0, `main` 미병합.
