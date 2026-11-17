> **2026-11-17 최종 판정: Entry5 PASS.** 원본 829/829 bytes/Git SHA와 JSON/PNG 정적 검사, C/F/D 교차감사 오차 0. [성공 Actions 실행](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/44079139796) · [독립 감사](G_ENTRY5_INDEPENDENT_RECOUNT.json) · [원격 SHA/행수/본문 검증](G_ENTRY5_REMOTE_READBACK.json). Entry6 허용·미착수, G 전체 G1~G6 최종 종료 0/6, 공식 JAR·게임 렌더 미인증.

# 1-2-G Entry5 — 원본 829개 직접 소스 감사

GitHub Actions 체크아웃의 Minecraft Java 1.21.11 사용자 추출 파일 bytes로 검증.
**Entry5 판정: PASS — 원본·선행 증거·독립·원격 게이트 통과**

## 원본 조사 수량
- 직접 파일 원본/해시: 829 / 829
- 모델 JSON: 379 / 379
- blockstate JSON: 265 / 265
- PNG 해시/디코드/RGBA: 185 / 185
- 모델 요소 675, face 2701 (원본 재계산)
- D 원문 선택: 1711, 서로 다른 참조 모델 513
- 선행 C PNG RGBA 일치 182 / C 외 G 신규 3
- mcmeta 31, 정적 애니메이션 메타 22
- 선행 F 시각 관찰 증거 연결 6 (이번 G의 신규 육안 관찰은 아님)
- 기록된 오류 0개

## 한계
- 공식 JAR 인증·게임 렌더·state registry·애니메이션 재생은 범위 외 미검증.
- E 특수 renderer, C 템플릿 미바인딩은 소관별로 계속 기록. PNG 내용 검증은 물체 정체/재질 확정이 아님.
- **전체 G 게이트 G1~G6는 계속 0/6이며 Entry6는 별도 실행에서 착수 가능.**
- A~F/v69 파일 변경 없음. G 6개 고정 Entry 중 5개 승인, 직접 본문 감사 **3,840/4,669 (82.24%)**, 잔여 **829**.

## 생성한 근거
G_ENTRY5_SOURCE_IDENTITY_829.csv, G_ENTRY5_MODEL_GEOMETRY_RECOUNT.csv, G_ENTRY5_D_ORIGINAL_OPTIONS.csv, G_ENTRY5_PNG_BINARY_AUDIT.csv, G_ENTRY5_ORIGINAL_FACES_*.csv, G_ENTRY5_INDEPENDENT_RECOUNT.json.

## 정적 감사 상세와 승인 범위
- **원본 829 파일:** 모델 JSON379(일반355 / E 특수24), blockstate JSON265, PNG185. 직접 원본 bytes와 Git SHA-1 재계산 829/829 일치, F 부모 상속·기하 및 C face/UV, D 상태 원문 교차 감사 통과.
- **모델:** elements **675**, face **2,701**. UV 명시 **1,576**/생략 **1,125**, PNG 결합 face **2,607**/템플릿 미바인딩 **94**. E 특수 모델 **24**는 원본 신원만 확인했고 실제 renderer는 미인증.
- **D 원본:** variants/multipart 모델 선택 **1,711**, 고유 참조 모델 경로 **513**, 조건·apply·선택 인덱스·x/y/uvlock/weight 명시 여부 선행 D와 일치. 실제 게임 상태 조립 시험은 아님.
- **PNG:** 총 **64,691 bytes**, SHA·PNG signature·Pillow full decode·RGBA SHA-256 전수 확인. C 과거 RGBA·치수·mode·알파 **182/182** 일치, C 밖 3개는 G 신규 검증으로만 인정. 메타데이터 sidecar 31개, 애니메이션 설정 22개 정적 판독. F 선행 첫 프레임 시각근거 6개는 신규 G 의미 확정이 아님.
- **미결정/범위 제한:** [G_ENTRY5_UNRESOLVED_SCOPE.csv](G_ENTRY5_UNRESOLVED_SCOPE.csv) 124행: 템플릿 미바인딩94, E renderer24, C 집합 밖 PNG3, F 시각 범위·런타임·애니메이션 각1. 원본 파일 손상이나 SHA 불일치 건수가 아니다.
- **워크플로 이력:** [최초 실행](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/44078991603)은 원본 감사 829 PASS였지만 잘못된 이전 파일명 G_ENTRY4_*로 증거 커밋이 실패했음. 수정 후 [전체 재실행](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/44079139796)은 원본검사·업로드·커밋 모두 성공.
- A~F/v69 원본·승인150/150·상위 완료1/5 불변. 원본은 사용자가 추출한 Minecraft Java 1.21.11 자산이며 공식 JAR 인증, 게임 엔진 renderer, 애니메이션 재생, 좀보이드 객체 정체, 마크 맵 생성은 이 검증에 포함되지 않음.
