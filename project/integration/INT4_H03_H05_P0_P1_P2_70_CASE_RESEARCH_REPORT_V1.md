# INT-4 H03·H05 — P0 6건 / P1 21건 / P2 43건 원본 독립 재개봉 및 최소 재시험 결과

## 결과 개요

- 상위 연구: **Minecraft Furniture Style Research**, 좀보이드 → 마인크래프트 맵의 3D 모델·상태 선택·원본 텍스처·UV·렌더링 구조 연구. 게임플레이 모든 기능·제3자 원본 자산 권한 심사를 모델링 확인과 혼동하지 않는다.
- 직계 기준: [기존 70개 잔여 검수 원장 Draft PR #96](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/pull/96), head `5f0eee2561745c5b9399bb36b07336025013db72`; 이번 결과 [Draft PR #97](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/pull/97)에 별도 기록. 원본 Git/기존 PR/`main` 미수정.
- **전 70개 사례 실제 파일 독립 재검수 PASS**, **필요한 추가 실게임 1회에서 S20/S21 북쪽 서랍 앞면 F2 2장·1,208픽셀 차이 PASS**. 따라서 '재촬영 70번' 또는 '재촬영 0번' 어느 쪽도 아니며, 원본 소스와 화면의 모순이 구체적으로 확인된 사례만 제한적으로 재시험했다.

## 1. P0·P1·P2 — 실제 원본 ZIP·PNG·로그 70개 재개봉

[실제 GitHub Actions #45250155300](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45250155300) **SUCCESS**, 관련 소스 commit `7921f08f5c3ee104b333551ed3137357d03e444e`.

| 독립 검증 범위 | 결과 | 주의 |
|---|---:|---|
| 원본 Actions ZIP 다시 다운로드 | **20/20** | 원본 ZIP SHA256·CRC 실제 바이트 검증 |
| 원본 게임 client.log SHA | **21/21** | 복수 실행분 로그 구분 |
| 네이티브 원본 PNG F2 SHA·PNG 포맷·1024×684 | **91/91** | 각 소스 아카이브의 원본 이미지 |
| 원본 F11F·H3·H6·분류표 사례 1:1 연결 | **70/70** | 출처 SHA·런/아티팩트 IDs·모델 조건 연결 |
| 기존 정성적 화면 관찰이 원장에 남은 사례 | **70/70** | 과거 관찰이 새 GPU/UV 검증이 되는 것은 아님 |
| 새로 승인된 전 사례 GPU 면·텍셀·프레임 인과 | **0건** | 증거 범위 구분 |

- 증거 수치 재검증: P0 **6** / P1 **21** / P2 **43**, H6 원본 문서에서 사례 ID+exact 같은 로그 줄 26, 캡처 JSON exact 상태 근거 있으나 사례 줄 없는 38, H6 대상 ID 수준 exact 구조가 없던 위험 시나리오 6. 마지막 6건은 H7 세부 상태 **21건**의 원본 서버 증거와 H8 R03 후속 증거를 별도 반영한다.
- 새로운 원본 재개봉 *감사 결과만* 보존한 아티팩트 [#14856211320](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45250155300/artifacts/14856211320), 다운로드 ZIP SHA256 `11cf9533e561f249e72b57f268c082341521b4f6bf0bbf1f29d18c9dc4cc2a2e` (CRC PASS). 제3자 원본 PNG/JAR/로그는 Git 및 이 결과 아티팩트에 포함하지 않는다.
- 전 70개 사례 별 보고서: `project/integration/INT4_H03_H05_P0_P1_P2_70_CASE_NEW_ARCHIVE_REAUDIT_V1.csv`. 사례별 출처와 `H03/H05` 상태를 그대로 보존한다.

## 2. P0 6건 — 원본 출처의 심사 결과

| 대상 | 검증 결과 | 남은 범위 | 이번 추가 게임 여부 |
|---|---|---|---|
| **V11** 바닐라 흰 침대 | 일반 JSON 모델 **0요소·0면**이지만 실제 원본 F2 **4장**, BED vs AIR **6,446픽셀** 차이. 특수 렌더링 경로 추적 대상임을 재확인 | 실제 `BedRenderer` Java 호출 부위·개별 렌더 경로는 instrument 미검증. 0요소를 빈 침대로 판정하지 않는다 | 없음 |
| **S20·S21** AF 서랍 | **옛 남동쪽 F2 해시 동일**. 실제 원본 공식 JAR에서 상태와 leaf 모델 분리, open 모델이 닫힌 모델 상속 + **`front` 텍스처만 교체**한다는 사실 확인. 이번 **북쪽 전면 카메라 실게임에서 1,208픽셀 차이 실측** | GPU 개별 면의 정확한 UV 텍셀 경로, 사용자의 클릭 열기/닫기 동작은 미승인 | **새 실제 게임 1회, F2 2장** |
| **R02** AF 방향별 모델 | 실제 원본 variant3 사방 및 variant1 두 대조, 원본 F2 6개, H11 구조 10요소·46면, 텍스처 바인딩 변경 12면·차이 영역 텍셀 54개 검토 | 모든 방향의 GPU 렌더 픽셀→UV 세부 인과와 전 버전 추론은 미승인 | 없음 |
| **R07** AF 남향 예외 | variant3 **south → acacia_1**, north/east/west → acacia_3 선택을 원본 런타임 JAR와 H11 모델 선택 목록으로 재확인; R02 네 장 **중복 사용** | 제작자 버그·의도 추론 불가, 픽셀별 인과 미승인 | 없음 |
| **R08** AF 소스·배포 비교 | 공식 Fabric 4.0.2와 Git 소스 빌드 Fabric 4.0.3의 **북향 variant1 대표 한 상태**는 원본 F2 완전 동일 | 전체 88상태·공식 4.0.3 NeoForge 실행/전체 릴리스 동등성 미검증 | 없음 |

### S20·S21 — 최초 동일 화면의 원인 범위를 실제 게임으로 좁힌 결과

- **원본 최초 게임:** 공식 Another Furniture 4.0.2 `another_furniture:oak_drawer[facing=north,open=false/true]` 정확한 서버 상태는 서로 다름. 구형 남동쪽 관찰 위치 `3.4 123.6 45.7 151 28`의 두 PNG는 SHA256 `02ee02a4b05d0d9877fc12debd214a96823cea734e56e7f60972bb72ff29f566`으로 **완전 일치**.
- **원본 모델 JAR 직접 검증:** closed `block/drawer/oak.json` vs open `block/drawer/oak_open.json`; 열린 모델은 닫힌 모델을 부모로 사용하면서 `front`만 `oak_front_open`으로 변경, 모양/상태는 기존 원본 기준 그대로. north로 향한 서랍의 전면이 구형 카메라에서 보이지 않을 가능성을 소스에서 확인.
- **필요한 최소 재시험:** [성공한 실제 게임 GitHub Actions #45251124211](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45251124211), 공식 Minecraft **Java 1.21.1 Fabric** + **변경하지 않은 AF 4.0.2 JAR SHA1 `c2f992081bdc4795ed6d87771a3b5f7c71103785`**. 실제 게임 실행 **1회**, 북쪽 새 관찰 위치 `0.5 122.3 35.5 0 20`, 원본 S20/S21 서버 exact-state **2/2**, 실제 F2 **2장**, 출처/카메라 단위시험 **6/6 성공**.
- 북쪽 전면 결과: 두 상태의 **1,208화면 픽셀 변화** (RGB 채널차 ≥24), 경계 **x481..542, y450..470**, 측정한 서랍 ROI 밖 변화 **0**. 실제 육안 관찰: 닫힘 상태는 전면 서랍 손잡이 두 개, 열림 상태는 상부 어두운 열린 칸과 하부 손잡이 하나.
- 새 S20 F2 SHA256 `d0dc361b8db7094b512ce7144866b736ef3e4341c9c034ba8bf013ec40327863`, S21 SHA256 `1499e0f81313cc9c0c60f8c4ff50899cb44cfd5972d1224f7fad11ea4f067045`; 원본 실제 로그 SHA `2394f757337f79173d5c71288e94e07ded1f8156fe08707d6537de668eabb01f`.
- 원본 F2/게임로그 아티팩트 [#14855721943](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45251124211/artifacts/14855721943), 별도 다운로드 ZIP SHA256 `5972c182837a766f1ee5515a1a1c895affcefb1d01d9ffbf1106aa9a327ae3ab`, CRC·PNG SHA 2장·클라이언트 로그 SHA·실제 상태 2건 재검증 성공. 원본 JAR/텍스처/게임 데이터는 Git에 업로드하지 않음.
- **판정:** 옛 화면의 동일성은 전 방향 동일함을 뜻하지 않는다. 북쪽 전면에서는 실제 모델·텍스처 차이가 보였음. 그러나 GPU UV 바리센트릭/텍셀 샘플 경로를 직접 추적하거나 플레이어가 클릭해 열었다고 주장하지 않는다. F 게이트 무조건 승인도 자동 부여하지 않는다.

## 3. P1 21건 — 구형 F2 재사용과 위험 증거 제약

**15개 재사용 원본 사례:** `S14 S15 S16 S17 S18 S19 S28 S29 S37 S38 S39 S40 S41 S42 S43`. 이 15개 모두 원본 ZIP·F2·client.log SHA를 새로 재열람했다. 이전 화면 관찰과 원본 상태/카메라/실행 버전의 범위를 보존하면서, **재사용 이미지가 독립 신규 실게임 실행이라는 주장은 배제**했다.

**나머지 6개:** `R01`은 대표 S10 근거만, `R03`는 기존 `setblock` 3단계와 별개로 H8 창작모드 실제 플레이어 설치·제거 F2를 확인한 범위만 수용; `R04`는 물 유무 정적 2상태, `R05`는 침대 설치·수면·기상과 파괴 **서로 다른 원본 게임 실행 2회**, `R06`은 동일 water=true 시간차 3F2(물 물리 승인 아님), `S22`는 과거 `GIT_BLOB_SHA1`이라고 적힌 실제 **64자 SHA256** 표기 오류(원본 CSV 보존).

**P1 결과:** 21/21 원본 파일·출처 연결 새 재검수 통과. 다른 기능·UV·동작을 정당화하지 않는 상태에서 **같은 범위 추가 게임 재시험 0건**.

## 4. P2 43건 — 바닐라 14·모드 29, 기존 원본 활용

- 바닐라 `V01 V02 V03 V04 V05 V06 V07 V08 V09 V10 V12 V13 V14 V15` **14개**.
- 모드 `S01 S02 S03 S04 S05 S06 S07 S08 S09 S10 S11 S12 S13 S23 S24 S25 S26 S27 S30 S31 S32 S33 S34 S35 S36 S44 S45 S46 S47` **29개**.
- **43/43** 원본 네이티브 F2·원본 아카이브/로그 SHA 재열람과 대상 1:1 연결 일치. 이전 F11F의 정성적 관찰 기록 유지; 이를 별도 새 사람 검수 또는 정확한 GPU UV 인과 통과로 승격하지 않음.
- 이 범위에서 대상 모델의 실제 원본 화면 파일 진위·출처 연결 모순을 새로 찾지 못했으므로 **동일 상태 반복 게임 실행 0건**. 향후 정확한 개별 면·텍셀·프레임 상태 인과가 필요한 사례만 별도 대조시험으로 좁힌다.

## 5. 단계 5 — 추가 실게임 시험의 결과와 다음 조건

| 추가 실게임 목적 | 검사 대상 | 이번 실행 결과 |
|---|---|---|
| 옛 동일 F2 이미지 vs 새 카메라 시야를 구분 | **S20·S21** | **1 실제 Fabric 실행 / F2 2장 / 전면 1,208픽셀 차이 확인** |
| R02/R07 원본 모델 선택 | 과거 F2+H11~H16 원장 | 반복 촬영 불필요 |
| R08 버전 대표 한 상태 | 이전 두 정식/소스빌드 F2 | 전체 버전 일반화 불가; 이번 새 실행 불필요 |
| P1/P2 동일 원본 사례 재촬영 | 64건 | 기존 원본 증거 재개봉; 동일 범위 추가 촬영 **0건** |

후속 실험 필요 여부는 **원본 서브모델의 면/UV 인과·Java 특수 렌더 경로·특정 화면 픽셀**의 확인 필요성이 분명해졌을 때 결정한다. 70개 사례 전체 게임 플레이/모든 상호작용 재실행을 INT-4 모델링 연구 필수 과제로 만들지 않는다.

## 6. 산출물과 최종 승인 경계

- 원본 독립 감사기 `scripts/integration/audit_int4_h03_h05_f70_original_reopen.py`, [전체 F70 70건 성공 Actions #45250155300](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45250155300).
- 사례별 새 원본 감사 70행 `project/integration/INT4_H03_H05_P0_P1_P2_70_CASE_NEW_ARCHIVE_REAUDIT_V1.csv`.
- P0/P1/P2 새 연구 검수 원장 `project/integration/INT4_H03_H05_P0_P1_P2_70_CASE_SOURCE_RECHECK_V1.json`.
- S20/S21 원본 JAR preflight + 실게임 F2 코드 `src/mcfr/int4_h03_h05_s20_s21_drawer_front.py`, 실제 카메라 F2 테스트 `tests/knowledge/test_int4_h03_h05_s20_s21_drawer_front.py`, 실게임 CI `.github/workflows/integration-int4-h03-h05-drawer-s20s21-front-real-f2.yml`.
- 새 실게임 원본 증거 `project/integration/INT4_H03_H05_S20_S21_REAL_NORTH_F2_RESULT_V1.json`. 본 한국어 검수 보고서.
- 모든 원본 제3자 이미지, JAR, 실제 게임 로그는 임시 Actions 보존 아티팩트에만 남기고 Git에는 연구 결과·출처·코드만 저장한다.

**원래 종료 기준 유지:** F70 조건부 70/70·**무조건 0/70**, H03 **HOLD**, H05 **CONDITIONAL**, H 범위 통과 6/8·조건부 1/8·보류 1/8. INT5 가구 부품 의미·INT6 원본 자산 AI 학습/재배포 권한 승인 **0**. 이번 성공은 *원본 출처 검증 범위와 특정 S20/S21 전면 가시성 문제를 해결한 것*이지 모든 GPU UV/Java 동적 렌더·F70 전체 무조건 완료를 뜻하지 않는다.
