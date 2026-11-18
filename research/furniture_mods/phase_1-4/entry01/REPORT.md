# 1-4 가구 모드 텍스처·UV 분석 · 첫 회차

2026-11-18 KST. 입력은 1-3 종료 커밋 `37778f58cc61c28a0ab1937612f044705194f153`의 [F 인계 원장](../../phase_1-3/F/1-3_TEXTURE_UV_HANDOFF.csv)과 [정규화 SQLite](../../phase_1-3/F/furniture_research.sqlite.xz)다. 고정 원본을 다시 열어 PNG를 전수 디코딩하고 v24 의자 39종의 상속 UV를 원본 JSON과 대조했다.

| 검증 범위 | 첫 회차 결과 |
|---|---|
| 신규 후보 PNG 원본 SHA·디코딩 | **1,996/1,996**. Another Furniture 1,036, Handcrafted 885, Macaw 18, 바닐라 참조 57 |
| 의자 우선 PNG | 신규 19개, 선행 비교용 5개. 총 24개 SHA 일치 |
| 의자 모델·면 UV | leaf 모델 39개와 부모 템플릿 2개 원본 SHA 일치. 상속 면 **1,794/1,794**의 PNG 영역을 실측 |
| 신규 PNG 후보가 적용되는 모델 면 인스턴스 | **533,647개** 중 첫 회차 실측 456개, 나머지 533,191개 |
| 경로 미확정·선언 전용 | 고정 Another Git에서 해당 이름의 PNG 경로가 없는 8건. 면에 미적용된 슬롯 77건은 인계 상태 유지 |

## 측정과 관찰

- PNG 원본 SHA와 무결성을 검증하고, 크기·원본 비트 심도·색상 유형·불투명/완전 투명/부분 알파 수·가시 RGB 색 수·빈도 상위 RGBA를 기록했다. PNG 975개에 완전 투명 픽셀이 있었고, 2개에는 부분 알파도 있었다. `.png.mcmeta`에서 애니메이션 선언을 찾은 4개는 전체 PNG 시트의 픽셀 통계만 계산했다.
- 의자 면에서는 부모 원형에 선언된 UV, 회전, leaf의 텍스처 슬롯 덮어쓰기를 원문과 대조했다. UV 0~16을 PNG 픽셀 좌표로 변환하고 시작값을 내림, 끝값을 올림한 반개구간 사각형을 표본으로 사용했다. 축 반전과 UV 회전은 원장에 유지했다. 사각형의 색상·알파 통계는 픽셀 분포를 나타낸다. UV 반전은 273개, 면 UV 회전은 117개, 투명 픽셀을 포함한 영역은 78개다.
- PNG와 UV 영역의 알파별 픽셀 수 및 가시 RGB 색 수는 Pillow 디코딩 결과에서 Python 히스토그램과 NumPy 집계가 모두 일치했다. 면 인스턴스는 각 모델에 적용되는 면의 수이며, 반복 상속되는 UV가 포함된다. 게임 엔진의 재질 합성·필터링·렌더링은 이번 측정 범위 밖이다.
- 원본 PNG 및 모드 모델 파일은 첨부하지 않았다. 과거 PNG 175개와 면 RGBA 4,113건은 선행 실측으로 유지했다. 비교용 PNG 5개는 신규 1,996건에서 제외했다.

## 원장과 후속 작업

- [PNG 픽셀 원장](1-4_PNG_PIXEL_LEDGER.csv.gz), [의자 UV 원장](1-4_CHAIR_UV_LEDGER.csv.gz), [신규 후보 UV 작업 원장](1-4_NEW_UV_QUEUE.csv.gz), [원본 경로 예외](1-4_SOURCE_EXCEPTIONS.csv), [집계](1-4_ENTRY01_AUDIT.json)
- 다음 회차는 `texture_id + UV 사각형`이 같은 면의 픽셀 계산을 재사용하면서 모델별 면 연결을 보존한다. 기본 UV, 범위 밖 UV, 넓이 0, 애니메이션 프레임의 별도 판정과 8개 경로 예외가 남아 있다. 이 단계의 전체 종료 판정은 보류한다.

## 재현

Python 3.11 이상, Pillow, NumPy, Git이 필요하다. Another Furniture·Handcrafted는 [G 원본 재집계](../../phase_1-3/G/G_SOURCE_RECOUNT.json)의 고정 Git 커밋을 포함하는 체크아웃을 사용한다. JAR 폴더는 공식 Macaw 배포 파일을 `macaw.jar`로, Mojang의 고정 클라이언트 파일을 `1.21.1.jar`와 `1.21.11.jar`로 준비한다. 원본 해시는 [G 원본 재집계](../../phase_1-3/G/G_SOURCE_RECOUNT.json)와 [C 기하 감사](../../phase_1-3/C/C_AUDIT.json)에 있다.

```sh
python research/furniture_mods/phase_1-4/entry01/measure.py --repo . \
  --af AF_GIT --hc HC_GIT --jars JAR_DIR --out OUTPUT_DIR
```
