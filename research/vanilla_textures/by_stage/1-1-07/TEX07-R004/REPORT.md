# TEX07-R004 — 내부 버전 서명·정적 면 플래그·아이템 표시 변환 점검

Minecraft Java 1.21.11 / 2026-11-13 / 담당 **1-1-07 콘크리트·색면 정확히 7종**. 신규 원본 PNG 0개, 중복 RGB/색차 계측 0개. R001–R003 결과를 그대로 보존한다.

## 1. 사용자 제공 소스 우선 / 버전 내부 일치성 (신규 출처 항목 1개)

사용자 제공 `1.21.11/version.json`을 실제 읽었다. 검증 대상 고정 소스 커밋: `2a43897b8f605b4e0c96a272bca476ee6b70058e`, Git blob SHA-1 `b49974d3ebd6cb73291d9e4c92d23b3192dadd66`.

| 필드 | 원본 JSON의 값 |
|---|---|
| id, name | `1.21.11`, `1.21.11` |
| world_version | `4671` |
| protocol_version | `774` |
| pack_version.resource_major/minor | `75` / `0` |
| pack_version.data_major/minor | `94` / `1` |
| java_version | `21` |
| build_time | `2025-12-09T12:20:42+00:00` |
| stable | `true` |

**범위:** 이는 추출본 **내부의 버전 일관성만** 보여 준다. 파일이 공식 Mojang JAR의 특정 전체 ZIP 바이트에서 유래했음을 증명하거나 서명/배포 해시를 인증하는 근거가 아니다. 공식 원본 인증 0/7 유지. 증거 파일 `SOURCE_VERSION_METADATA.json`.

## 2. E — 정적 모델 면의 세부 선언: 새 플래그 감사

사용자 제공 추출본 `assets/minecraft/models/block/cube_all.json`, `cube.json`, `block.json`, 7개의 `<color>_concrete.json`을 고정 커밋에서 직접 재조회. R003에서 이미 판정한 7색×6면=42면 사실을 **새 모델 수/새 UV 검증 수로 합산하지 않는다**.

- `cube_all`은 6면/particle 텍스처 슬롯을 모두 `#all`에 연결한다.
- `cube`의 `[0,0,0]`→`[16,16,16]` 원소는 `down/up/north/south/west/east` 6면에 각각 **정확히 같은 방향의 `cullface`를 명시**. 6/6면 템플릿 검사 통과, 7색에 상속되어 42/42 선언 추적.
- `cube`의 6면 모두 **`uv`, `rotation`, `tintindex`, `shade`를 명시하지 않음**. 이는 해당 JSON 필드가 없다는 뜻이며, 그 필드의 인게임 기본값이나 실제 컬링/조명 효과가 증명됐다는 뜻이 아님.
- 7개 색상별 `models/block/<color>_concrete.json`에는 `display`, `elements`, `ambientocclusion`, `gui_light`를 개별 덮어쓴 항목 **0개**. 각 색별 슬롯 `textures.all`만 연결.
- 풀큐브 기본 UV `[0,0,16,16]` 42건은 R001/R003과 동일한 **기하학적 파생**, 원본에 수치로 명시된 UV는 0건. 면별 출처와 필드 부재는 `42_STATIC_FACE_FLAGS.csv`.

**주의:** `cullface`의 존재는 정적 모델의 선언이다. 실제 게임에서 이웃 블록의 차폐 판단이 어떤 장면에서 발생하는지 측정한 결과가 아니다.

## 3. E — 7개 공유 표시 상황 및 정적 GUI 조명 선언

공통 `models/block/block.json`에서 **`gui_light="side"` 및 표시 변환 7개**를 직접 추출했다. 표시는 `gui`, `ground`, `fixed`, `on_shelf`, `thirdperson_righthand`, `firstperson_righthand`, `firstperson_lefthand`. 각 변환의 원본 rotation/translation/scale을 `7_DISPLAY_CONTEXTS.csv`에 기록했다.

7색은 모두 부모 체인을 공유하며 개별 색 모델의 `display` override는 **0/7**. 따라서 7색 모델에서 공통으로 **상속 가능한 원본 설정**임을 알 수 있다. 7개 컨텍스트를 각 색에 7회 복제해서 49개의 독립 실험으로 계산하지 않는다. `block.json`에는 `ambientocclusion` 명시도 없으며, 엔진의 기본 동작을 PNG 소스만으로 확정하지 않는다. 게임 화면 조명·GUI 투영·선반 배치 렌더는 미확인.

## 4. F — Mojang 공식 JAR 인증 차단과 재현 도구

공식 메타데이터 주소 `https://piston-meta.mojang.com/mc/game/version_manifest_v2.json` 및 `piston-data.mojang.com`에 접속을 시도했지만 현 실행 환경의 DNS 해석 실패로 다운로드/전체 SHA-1 검증을 수행할 수 없었다. 공식 `client.jar` 바이트·원본 메타데이터가 없어 **공식 인증 0/7**, Minecraft 런타임/정적 스크린샷 없어 **인게임 0/7**.

보조 도구 `VERIFY_CLIENT_JAR.py`를 함께 저장했다. **사용자가 소유한 JAR을 자신의 PC에서** 검사할 때 사용하도록 Mojang 공식 manifest와 버전 JSON 조회, 파일 전체 SHA-1+크기 대조를 하고, R003 `SOURCE_LEDGER.csv`의 31개 JAR 엔트리를 SHA-1 Git blob 식으로 비교한다. 공식 메타데이터를 얻지 못하면 엔트리 31개가 모두 일치해도 **PENDING**으로 남도록 설계했다.

사용 예시:

```bash
python VERIFY_CLIENT_JAR.py --jar "/path/to/1.21.11.jar" --ledger "../TEX07-R003/SOURCE_LEDGER.csv" --output "jar_evidence.json"
```

`--offline`은 출처 대비만 확인하므로 어떤 경우에도 공식 인증으로 표시하지 않는다. Python 표준 라이브러리만 사용. 로컬 프로토타입은 Python 구문 검사 및 31개 가짜 ZIP 멤버 테스트에서 31/31 항목 일치와 공식 **PENDING**이 독립적으로 유지됨을 확인했으나, 실제 Minecraft `client.jar`를 검사한 시험은 **미수행**. 원본 JAR 자체를 GitHub에 재배포하지 않는다.

## 5. A–G 및 인수인계

- A/B/C/D는 R001–R003 기계 검수 결과를 유지한다. R004에서 새로운 PNG별 해시나 통계 측정으로 이중 계산하지 않음.
- E는 **새로운 선언 필드 감사**(6면 템플릿, 42 상속 면, 7 공유 display 컨텍스트, 내부 version.json)만 추가.
- F는 공식 배포 인증 0/7, 실제 인게임 정적 검증 0/7 보류. 애니메이션 분석 전면 보류.
- G: 신규 `REPORT.md`, `SUMMARY.json`, `SOURCE_VERSION_METADATA.json`, `42_STATIC_FACE_FLAGS.csv`, `7_DISPLAY_CONTEXTS.csv`, `VERIFY_CLIENT_JAR.py`. 이 단계 전용 `STATE.json`, `HANDOFF.md`만 갱신.
- 글로벌 체크포인트 **v38 변경 없음**, 다른 단계 및 R001/R002/R003 문서·CSV 변경 없음. 가구 3D 제작과 PZ 변환 불실시.
- 다음 번호 **TEX07-R005**. 실제 `client.jar` 확보와 공식 manifest SHA 비교, 인게임 정적 장면 확보만 남은 핵심 물리 검증.
