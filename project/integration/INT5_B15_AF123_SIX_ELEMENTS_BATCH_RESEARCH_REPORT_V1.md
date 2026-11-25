# INT-5-B15 — AF123 미검증 원본 6요소 한 번에 배치 검증

## 목적과 직계

- 직계: [B14 Draft PR #126](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/pull/126) head `b026233f61b5d9231aa9bdf988dd3d5f526bf673`
- 별도 B15 브랜치: `work/int5-b15-af123-six-original-elements-batch-f2-20261125`
- 이 작업의 **명령 단위는 여섯 요소를 하나의 CI 워크플로에서 검증**하는 것. 요소 하나마다 사용자 요청이나 PR을 만들지 않는다.
- 기존 H/INT-4 및 INT-5 B1~B14의 원본 파일, Git `main`, 다른 모드의 원본 JAR/PNG는 수정하거나 병합하지 않는다.

## 1. 기존 B3 원본 소스에서 선정한 6개

| 원본 아이디 | 원본 요소 인덱스 | 원본 면 수 | 역할 단서(확정 의미 아님) | 사전 상태 |
|---|---:|---:|---|---|
| AF123/AF1394/0 | 0 | 5 | LEG_OR_LOWER_POST | 단독 렌더 인과 미검증 |
| AF123/AF1394/1 | 1 | 5 | LEG_OR_LOWER_POST | 단독 렌더 인과 미검증 |
| AF123/AF1394/2 | 2 | 5 | LEG_OR_LOWER_POST | 단독 렌더 인과 미검증 |
| AF123/AF1394/3 | 3 | 5 | LEG_OR_LOWER_POST | 단독 렌더 인과 미검증 |
| AF123/AF1394/5 | 5 | 4 | LOWER_FRAME | 단독 렌더 인과 미검증 |
| AF123/AF1394/6 | 6 | 4 | LOWER_FRAME | 단독 렌더 인과 미검증 |

기존 이미 실험한 AF123 요소 4·7·8·9를 재실험 성공률에 중복 계산하지 않는다. 역할명은 원본 텍스처/기하 자료에서 도출한 **가설**이며 실제 다리·프레임 기능 승인으로 승격하지 않는다.

## 2. 실제 실행과 안전한 원본 대조

- Minecraft Java **1.21.1 Fabric**, 공식 Another Furniture **Fabric 4.0.2** JAR SHA1 `c2f992081bdc4795ed6d87771a3b5f7c71103785`만 사용한다. 연구 Git 4.0.3과 배포판 4.0.2가 바이트 동일하다고 가정하지 않는다.
- 정식 `acacia_10_tucked` 자식 모델은 원래 공유 부모 `template/chair_tucked`의 **10요소/46면**을 상속한다. 각 CI 작업은 단 하나의 지정 요소만 제외한 **9요소/(46−그 요소 면수)면**을 **자식 JSON 하나에만** 임시 오버라이드한다.
- B3 45요소 원장과 출시판 실제 parent/child Git blob, ZIP CRC, JAR의 원본 SHA, 원본 JSON/텍스처/모든 다른 멤버의 바이트 동일성 대조를 강제한다. 임시 변형 JAR·제삼자 원본 리소스는 절대 Git/아티팩트로 내보내지 않는다.
- 정상 블록 `another_furniture:acacia_chair[facing=north,tucked=true,variant=10]` 및 앞쪽 **상단 oak slab 지지**를 유지한다. 원본 B4 실게임 기준 네이티브 F2 8장(아티팩트 `14982648778`, ZIP SHA256 `4a50c784ecc7499546e5f4a23ef2b8de08a0d6fd8899cafc7b885a071d575e35`)을 각 작업에서 정확히 재검사한다.
- **한 GitHub Actions의 6개 병렬 매트릭스 작업**은 각각 새 Fabric 게임을 열어 남/북 카메라에서 `chair+slab → slab only → chair+slab 복원 → air` 신규 F2 8장, 의자/슬랩 서버 상태 16쌍, PNG/로그 SHA를 생성한다. 기존 B4와는 독립 게임 세션이다.
- 의자 변경 응답, 반복 A와 A', 변형 전후 슬랩/air 음성대조, 시간 드리프트, 원래 전경 밖 변화를 각각 판정한다. 픽셀 변화 0일 경우 화면 미검출로 보존하며 자동 PASS로 승격하지 않는다.

## 3. 산출 및 실행

- 배치 스크립트: `src/mcfr/int5_b15_af123_six_element_batch_f2.py`
- 런타임 진입: `python -m mcfr.runtime int5-b15-af123-batch-f2 --index <0,1,2,3,5,6> --version 1.21.1 ...`
- 정적/음성 회귀시험: `tests/knowledge/test_int5_b15_af123_six_element_batch_f2.py` (11개)
- 원본 실게임 Actions: `.github/workflows/integration-int5-b15-af123-six-element-batch-f2.yml`
- 매 작업 아티팩트: 원본 F2 PNG, client.log, SHA manifest 및 `INT5_B15_ELEMENT_NATIVE_F2_AUDIT_V1.json`. 수정된 JAR은 아티팩트에 포함하지 않음.

## 4. 승인 경계 및 검증 결과 기록

**주의: CI의 독립 검증이 끝나기 전에는 B15 여섯 요소의 실제 게임 성공/픽셀 수치를 주장하지 않는다.**

- 시작 시점의 45요소 중 **실게임 단일요소 렌더 인과 검증 9/45**, 남은 36요소.
- B15 여섯 요소가 모두 실제 PASS라면 최대 15/45이며, 반응 0·CI 실패·음성대조 불일치는 각 요소별 보류한다. **6개를 자동으로 성공 수에 더하지 않는다.**
- B14의 원본 외형/색상/요소 대응을 참조하지만, 개별 요소 픽셀 반응은 원본 GPU face→pixel **독점 소유권이 아님**. 기능·재질·스타일 의미 승인 0/45, INT6 AI 학습/재배포 승인 0.
- INT-4 모델링 전용 70/70의 범위 한정 종료와 별개로 구 엄격 **H03 HOLD**, **H05 CONDITIONAL**, **F70 무조건 PASS 0/70**를 유지한다.
- 이번 작업은 AF123 같은 게임/모드 버전/의자 구성을 묶은 배치이며, **Macaw 1.21.11**의 source index0은 별도 공식 원본·카메라/렌더 근거를 마련한 다른 배치에서 처리해야 한다.

검증 후 GitHub Actions 각 작업 ID·결론·아티팩트·픽셀·최종 누적 수치를 별도로 기록한다.
