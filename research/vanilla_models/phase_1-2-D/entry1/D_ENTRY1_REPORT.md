# Minecraft Java 1.21.11 · 1-2-D Entry1 blockstate 원본 조사 결과

**2026-11-16** · 착수 HEAD `96dbd5b6859e91efd5c8693469ae759927abd65c`, 고정 범위 커밋 `035b1def567b4ccd538c144bb5a30d467d56328a`, 12 JSON 자료 커밋 `57e52f5e1cecfe3d1ce897e040f8c36ab5bb5a64`.

## 1. 확정 분모와 실제 조사
고유 원본 blockstate JSON 모집단 **1,168경로**를 `research/vanilla_models/phase_1-2-D/D_FIXED_SCOPE_1168.csv`의 6 Entry(12+96+265+265+265+265)에 고정했다. **원본 목록/트리 경로·SHA 1,168/1,168 대조는 신원 검사이며 JSON 내용 검토가 아니다.** 이번에 실물 원본 JSON을 직접 읽고 blob SHA를 확인한 **Entry1 12개**만 D 실조사 실적으로 센다. 잔여 **1,156개** 미실행.

`D_ORIGINAL_12_SOURCE_SNAPSHOT.json`에는 원본 12경로/파일 내용/Git SHA, `D_SOURCE_RULES.csv`에는 **167개의 규칙/모델 선택 옵션** 및 조건, `x`/`y`/`uvlock`/weight **키 존재와 값**을 구분 기록했다. `D_STATE_ASSEMBLY.csv`에는 **380개 정적 문법 상태**, 선택 모델 옵션 총 **1,972개**를 모델/회전/uvlock와 함께 기록했다.

| 파일 | 종류 | 규칙 | 정적 후보상태 | 선택 모델 옵션 합산 |
|---|---|---:|---:|---:|
| `brewing_stand` | multipart | 7 | 8 | 32 |
| `lantern` | variants | 2 | 2 | 2 |
| `oak_shelf` | multipart | 24 | 32 | 64 |
| `oak_door` | variants | 32 | 32 | 32 |
| `oak_fence_gate` | variants | 16 | 16 | 16 |
| `campfire` | variants | 8 | 8 | 8 |
| `chiseled_bookshelf` | multipart | 52 | 256 | 1792 |
| `cauldron` | variants | 1 | 1 | 1 |
| `heavy_core` | variants | 1 | 1 | 1 |
| `furnace` | variants | 8 | 8 | 8 |
| `piston` | variants | 12 | 12 | 12 |
| `stonecutter` | variants | 4 | 4 | 4 |

양조기는 병3 boolean **8상태**와 각 상태 본체+세자리 병/빈 모델 **4개**로, **v69 원본 연구에 이미 존재하는 원본 경로/SHA의 중복**이다. `oak_shelf`는 facing4×powered2×side_chain4=32후보에 기본모델·추가부품 규칙을 결합. `chiseled_bookshelf`는 facing4×occupied 6슬롯(2^6)=256후보에 본체+6부품을 결합했다. `oak_fence_gate`의 명시 `uvlock:true`, 조각책장 기본모델의 명시 `uvlock:true`와 슬롯 부품의 미명시를 구별한다. 회전/uvlock이 **키로 없는 경우는 명시된 0/false와 다르다.**

## 2. B/C 경로 SHA 연결 · 선행연구 재집계 금지
정적 상태 1,972개 선택 모델 참조가 가리키는 고유 모델 **49개/49개**를 1-2-C 최종 원장(경로 + Git blob SHA)와 연결; 연결 실패0. `D_MODEL_BC_CROSSWALK.csv`가 모델별 기존 C Entry·face·UV·texture 증거파일과 B 종료 원장 파일 경로/SHA를 기록한다. `D_STATE_MODEL_BC_LINKS.csv`가 1,972개 상태-모델 적용에 그 참조를 붙인다. `D_TEXTURE_C_LINKS.csv`는 C 기존 texture slot과 PNG 원본 경로/Git SHA/RGBA SHA를 연결한다.

이 **49개 고유 모델의 C 선행 face 460 = PNG 연결 460 + 자식템플릿 미바인딩 0**, 기존 C 텍스처 슬롯 근거 138행·연결 고유 PNG 32종은 **선행 자료의 재사용 수치**이다. D 신규 face/PNG 해석 및 PNG RGBA 새복호화0. C 전체의 23,090 face·PNG1,073은 그대로 C 실적이며 D에 중복 산입하지 않는다. `heavy_core`의 6면은 기존 Entry4의 옛 불해결이 아니라 **C Entry5 `HEAVY_CORE_FACE_ERRATUM.csv` 정정 반영** 수치(중복 생성0). 일반 elements 없는 56개 및 E-first 30개 특수기하는 E 담당; 이번 49개 직접 모델 참조에서는 E 소관 원장 대상 없음.

## 3. 독립 검산 및 정직한 한계
원본 JSON을 snapshot에서 **별도로 재파싱**하고 variants 키, multipart AND/OR 조건의 모델 선택 순서를 독립 계산해 **380/380 상태 일치**. 12 블록 원본 Git blob SHA 연결12/12, C 모델49/49, model source face 460=460+0. 원격 파일 SHA/행수/내용 재조회는 추가 감사 파일로 보존한다.

상태조합은 **JSON 조건에서 읽힌 속성값의 문법상 후보**다. 게임 속성 레지스트리의 진짜 유효상태, 회전 UV의 실시간 렌더, 공식 배포 JAR 인증, 게임 내 모델 표시, 애니메이션 동작은 **실행·인증하지 않았다**. C PNG를 D에서 재측정하지 않았다. Entry1 자체의 source 조건 감사만 통과했으며 **D 전체는 `D_IN_PROGRESS_ENTRY1`**. D1 범위·배정 PASS, D2/D3/D4는 12경로 조사만 부분완료, D5 전체 종료감사는 보류. 전체 완료 선언은 고정 Entry6의 D1~D5 전부 PASS에만 허용한다.

A=`A_COMPLETE_SOURCE_SCOPE`, B=`B_COMPLETE_SOURCE_GEOMETRY_SCOPE`, C=`C_COMPLETE_SOURCE_UV_TEXTURE_PNG_SCOPE`; v69 P1 544x393/review544x70, 승인150/150, 상위 단계1/5 모두 보존. 기존 A/B/C/v69/원장 파일 수정 없음.
