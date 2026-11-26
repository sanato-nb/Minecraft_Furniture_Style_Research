# INT-5-B21 — Another Furniture 원본 요소5 단독 렌더·요소6 양성대조 실게임 연구

2026-11-26 KST · B20 Draft PR #132 head `ddd22cb579ceb7fc5b6219896d97c21e56c7daa4`에서 신규 분기. B19 기존 네 방향 원본 제거 화면 반응 43/45, AF 요소5 두 건 0픽셀 및 B20 양쪽 X 좌표 정렬 후 0픽셀 사실을 그대로 보존.

## 목표
- 원본 가구 전체에서는 제거해도 4방향 이미지 변화가 없었던 `AF121/AF1393/5`, `AF123/AF1394/5` 두 원본 요소가, **다른 9개 형상을 제거한 단독 모델에서는 나타나는가**를 검증한다.
- **원본 요소6 자체만 남긴 가구**를 양성대조로 사용한다. 요소6은 B15/B16에서 원본 제거 시 한정 화면 변화가 확인됐던 독립 요소다.
- **요소5의 원본 좌표와 UV 및 텍스처면을 고정하고 faces만 빈 맵으로 바꾼 모델**을 무면 음성대조로 사용한다. `elements=[]`는 Minecraft 부모 모델 상속으로 환원될 수 있으므로 사용하지 않는다.
- 요소5 단독 원본과 X endpoint만 정렬한 단독 개입을 따로 비교한다. B20 전체 가구에서 0픽셀이었다는 사실을 강제로 새 모델에 이식하지 않는다.

## 버전·원본 제한
- 공식 `another_furniture-fabric-4.0.2.jar`, Minecraft 1.21.1 Fabric, B19/B20에 고정된 원본 parent/child Git blob·JAR SHA·ZIP CRC 확인.
- 정확히 자식 모델 하나만 임시 수정. 원본 10 요소/46면과 source5 4면을 먼저 고정 검산하며, 원본 parent·텍스처 참조·블록상태·나머지 JAR 구성원과 제작자의 실제 출시 배포판은 변경하지 않는다.
- AF121 기본 `north` 의자 및 독립 variant3 대조·AIR, AF123 유효 `tucked=true` + 윗반블록, `slab_only`·AIR 상태를 재사용한다.

## 네 개의 실제 Minecraft 클라이언트 세션

| 세션 | 자식 JSON의 `elements` | 역할 | 카메라×상태 |
|---|---|---|---|
| `no_faces_5` | 요소5 하나(0 face) | 동일 geometry지만 quad 없는 음성대조 | 남·북·동·서 × 4 |
| `original_5` | 요소5 원본만 4 face | 기존 원본 요소5 단독 화면 응답 | 남·북·동·서 × 4 |
| `normalized_5` | 요소5만 X 양끝 정렬, UV/face 동일 | 역방향 X 가시성 조건 분리 | 남·북·동·서 × 4 |
| `positive_6` | 원본 요소6만 4 face | 게임이 단일 요소 렌더를 할 수 있는지 양성대조 | 남·북·동·서 × 4 |

각 세션마다 동일한 최초 월드 스냅샷 복원. 표적마다 실제 게임 4세션·F2 PNG 64장·정확 서버 의자 상태 64회(접힌 의자 추가 지지 슬랩64회). 총 두 대상 **8게임 세션·128장 예상**. CI에서 원본 PNG SHA256·client.log SHA256·서버 blockstate 마커·동일 프레임 전후·시간 A/A·타 모델과 AIR 음성대조를 독립 확인한다.

## 실험 판정의 분리

- `VISIBLE_ORIGINAL_SOURCE5_ONLY_NOT_VISIBLE_IN_FULL_MODEL`: 원본 요소5 단독화 시 실화소가 생기면 전체 원본에선 동일 변화가 0이었던 범위를 고려해 **조립체 맥락상 가림/겹침과 양립**. 가림이 배타적 원인이라는 확증은 아님.
- `ONLY_NORMALIZED_SOURCE5_VISIBLE_IN_ISOLATION`: 원본 단독 0, 정렬 단독 유의미한 화면 변화. 정렬의 조건부 영향만 인정.
- `ORIGINAL_AND_NORMALIZED_SOURCE5_NOT_VISIBLE_EVEN_ISOLATED`: 요소6 양성대조는 통과했는데 원본·정렬 요소5 모두 0. 해당 게임 상태·카메라의 단독 모델 F2 미검출; **원인을 확정하거나 요소가 불필요하다고 판단하지 않음**.
- `CONDITIONAL_FAILED_...`: 양성 대조가 0이거나 시간·동일 월드 대조가 불안정할 때는 인과 결론을 승인하지 않음.

## 코드·증거
- `src/mcfr/int5_b21_af_source5_isolation_four_view_f2.py` — 원본 고정·네 disposable 1-element child JAR·4 client capture·독립 F2 감사.
- `tests/knowledge/test_int5_b21_af_source5_isolation_four_view_f2.py` — 13개 원본/개입/반증/보류 구분 테스트.
- `.github/workflows/integration-int5-b21-af-source5-isolation-positive6-four-view-f2.yml` — 모델별 병렬 실제 Minecraft CLI·F2 테스트·감사·아티팩트.
- `src/mcfr/runtime.py` — B21 CLI, 월드·원본 모델·모드 설치·게임 캡처 연계.

**실제 GitHub Actions가 통과하고 공식 F2 아티팩트를 재개봉하기 전에는 검출 여부를 보고서에 확정하지 않는다.** GitHub에 원본 JAR·텍스처·시험용 patched JAR 파일을 배포하지 않는다.

## 보존해야 하는 엄격 경계
- 기존 B19 원본 **43/45 한정 화면 개입 반응**, 원본 요소별 시험 **45/45** 그대로.
- 원본 source face/UV 배타적 GPU 픽셀 귀속 0, 가구 부품의 물리적 역할·재질·스타일 기능 승인 0/45, 제3자 AI 학습·재배포 권리 승인 0.
- `H03 HOLD`, `H05 CONDITIONAL`, 엄격 F70 무조건 승인 `0/70`. Draft PR, main 미병합.

## CI 실행·감사 로그
실행 URL, 실제 exit code, 원본 ZIP SHA, 새 PNG 픽셀/양성·음성대조 수치, 실패 시 원인과 재실행을 뒤에 추가할 것. **현재 상태: 실게임 결과 미확정**.

## 최초 실제 CI 진행 기록

- [GitHub Actions #45744806918](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45744806918), 실행 코드 head `5872807b89f30966e35ba96378f65bf8d7665752`.
- AF121_5 및 AF123_5 두 개 병렬 작업 모두 원본/단독/양성·음성대조 회귀시험 **PASS**, 공식 Minecraft 1.21.1 월드 생성 **PASS**.
- 중간 점검 시 두 작업 모두 **4개 Fabric 실게임 세션/모델, 64장 네이티브 F2 촬영 실행 중**. 완료 run/로그/ZIP/이미지 독립 검수 없이는 요소 5의 화면 응답 여부를 확정하지 않는다.
- 이후 재확인에서 실제 최종 성공 또는 실패를 이력으로 보존하고, B19 한정 인과 43/45·의미 승인 0/45·권리 미승인을 바꾸지 않는다.
