# 1-2-G Entry5 최종 PASS — Entry6 허용, **아직 미착수**

2026-11-17 기준 Minecraft Java 1.21.11 사용자 추출 자산. 고정 큐 **829 = 모델 JSON379 + blockstate JSON265 + PNG185**의 실제 원본 bytes/Git SHA를 다시 계산해 **829/829 PASS**. [GitHub Actions 전체 재실행](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/44079139796) **success**, [독립 감사](G_ENTRY5_INDEPENDENT_RECOUNT.json) 오류0, [원격 SHA/행수/내용 검산](G_ENTRY5_REMOTE_READBACK.json) PASS.

## 검증 근거
- 원본 모델 **379**: 일반 기하 **355**, E 특수 renderer 소관 **24**. E 24개는 원본 파일 신원만 직접 검증했고 게임 특수 렌더는 미인증. 부모 JSON 상속/F chain 및 C face 대조.
- 적용 기하 **675 elements / 2,701 faces**, 명시 UV **1,576**/생략 **1,125**, 연결 PNG face **2,607**, 템플릿 미바인딩 **94**. 미바인딩에 가상 PNG를 지정하지 않음.
- 원본 blockstate JSON **265**, D 원본 variants/multipart 선택 **1,711**, 고유 모델 경로 **513**. 선택 인덱스·조건·모델·apply·회전 x/y/uvlock/weight 명시 여부 재검산 오류0.
- 원본 PNG **185**, 총 **64,691 bytes**. 파일 SHA·PNG 시그니처·Pillow 전체 디코드·RGBA SHA256 PASS. C 과거 RGBA 검증 **182/182** 일치, C 바깥 3개는 G 신규 직접 검증으로만 인정. .mcmeta 원문 **31**·애니메이션 정적 설정 **22**, 실제 게임 재생 미시험. F 선행 시각 근거 **6**은 신규 G 육안 정체 검수 아님.
- [G_ENTRY5_UNRESOLVED_SCOPE.csv](G_ENTRY5_UNRESOLVED_SCOPE.csv) **124행** = 미바인딩94, E 특수 소관24, C 범위 밖 PNG3, F 기존 시각·공식 JAR/엔진·애니메이션 각1. SHA 불일치 124건이라는 뜻이 아님.
- 첫 실행 run 44078991603은 829개 소스 검사 성공 후 잘못된 G_ENTRY4 파일명으로 **증거 커밋 단계 실패**. 워크플로 경로 수정 후 run 44079139796 전체 재실행 성공. 최초 오류 이력 보존.

## 고정된 G 상태
- Entry1~5 승인 **5/6**, 직접 원본 내용 감사 **3,840/4,669 (82.24%)**, 잔여 **829개**.
- **G1~G6 전체 종료 게이트는 0/6**; 전체 1-2 및 최종 가구·마크 맵 생성 작업 미완료. Entry7 없음.
- A~F/v69 원본 파일 미수정, 기존 승인 150/150 및 상위 완료 1/5 유지.

## 다음 Entry6: 별도 실행에서만 착수
확정 큐 `research/vanilla_models/phase_1-2-G/entry6/G_ENTRY6_QUEUE_829.csv`의 **829개 = 모델 JSON378 + blockstate JSON265 + PNG186**만 처리한다. 원본 bytes/Git SHA, F/D/C/E 증거 교차, 모든 PNG 실제 픽셀, 기존 미결정 범위, 6 Entry 전체 중복·누락 및 마지막 G1~G6 독립 종료 감사까지 수행한다. Entry1~5의 선행 실적을 재실행 신규 실적으로 계산하지 않는다.

Entry6 원본 조사 PASS만으로 G 전체 완료 선언 금지. G 글로벌 6게이트 각각의 증거 및 독립 재집계·원격 SHA·행수·본문 검증을 완료했을 때만 종료를 허용한다. 공식 Minecraft JAR, 런타임 state registry, 애니메이션 재생, 좀보이드 객체 정체 및 실제 마인크래프트 맵 재현은 별도 인증 소관.
