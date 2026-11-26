# INT-5 B31+B32+B33 — 21 원본 ZIP 독립 검증 · 45 텍스처 출처 · 조건부 원형 가림 교차 연구

- 검수일: **2026-11-26 (KST)**.
- 기존 누적 [Draft PR #137](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/pull/137) head `03447d5769cd04e3214abbab0914f360d811a8c7`에서 **새 독립 브랜치** `work/int5-b31-b32-b33-original21-texture-conditional-audit-20261126`를 분기한다. `main` 병합하지 않음.
- 연구는 바닐라 및 가구 모드의 3D 부품·원본 텍스처 출처/UV/블록상태·실제 렌더링 관찰 근거를 축적한다. 앉기·수면·파괴 등 불필요한 게임플레이 검증을 새 게이트로 추가하지 않는다.

## B31 — B27의 아직 이번 배치에서 직접 재다운로드하지 않았던 원본 21요소 실증 아티팩트

- [B27 전체 45요소 원장](INT5_B27_FULL_45_ORIGINAL_F2_SOURCE_VISUAL_SPATIAL_INDEPENDENT_EVIDENCE_V1.csv)의 `direct_visual_audit_batch=B27` **21행**을 원본 artifact ID/SHA별로 고정: AF121 **10개**, AF123 **10개**, HC11210 **쿠션12 1개**.
- 21개 GitHub Actions 실제 원본 ZIP을 별도로 **전부 다운로드**하여 파일별 ZIP SHA-256 대조 + ZIP CRC 검증 + 중복/부적절 경로 방지 + 실제 PNG의 1024×684 원본 F2 검증 + 내부 감사 JSON에서 직접 PNG 및 client.log SHA-256 대조. **21/21 ZIP, 실제 F2 176/176장, 로그 22/22개** 일치.
- 이 21개 작업에는 AF121/AF123 각각 8장 F2·로그1개씩, HC 원본 및 임시 수정 상태 각각 8장 F2·로그1개씩 포함. 실제 클라이언트 서버 JOIN 문자열도 기록됨.
- [GitHub Actions #45843425631](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45843425631) **B31 Job SUCCESS**. 독립 CI용 코드 `src/mcfr/int5_b31_remaining21_real_archive_audit.py`, 원본 21개 ID/SHA/result `INT5_B31_ORIGINAL_21_ZIP_176_NATIVE_F2_INDEPENDENT_VERIFIED_V1.json`. 성공 원본 감사 결과 아티팩트 **#15130505727** 직접 재다운로드·CRC·결과 수량 확인.
- 앞선 B26에서 이미 다른 날 직접 검수한 HC/Macaw 24요소 **384 원본 F2·48로그**와 B31 **176 F2·22로그**를 합산하면 전체 **45요소·560 F2·70로그**의 **서로 다른 배치에 걸친 실제 ZIP 독립 검수 이력**이 확보됨. 하지만 B31에서 45개 ZIP 전부를 다시 받았다고 말하지 않으며, 이미 보고된 B27 스크린 픽셀 변화 수치를 새로운 원본 모델 21개에 대해 재계산했다고 말하지 않음.
- 원본 모델을 임시로 격리해 기록한 인과와 개별 GPU face/UV 소유·역할 의미 확정은 별개이다. 원본 JAR, PNG, 파생 접촉시트는 Git에 새로 업로드하지 않음.

## B32 — 원본 텍스처 체크섬 및 런타임 버전 증거의 분리 검수

- B24 45부품 원본 `source_texture_cue`·`original_texture_source_hashes`와 B27 출처 45행을 재교차; 45부품·229면 출처 정합 유지.
- 원본 `source_texture_hashes`는 그룹 문자열 기준 **8그룹**, 그룹 안 공유되는 개별 SHA1/256 체크섬의 중복 제거 후 **8종**. 단일 원본 그룹에 SHA 2개를 기재한 사례가 있어 그룹 수를 체크섬 수에 단순 더하면 중복됨.
- 텍스처 단서 원장: generic/shared **35**, `ROLE_NAMED_ORIGINAL_SEAT_PNG` **2**, `ROLE_NAMED_ORIGINAL_BACK_PNG` **6**, `ROLE_NAMED_ORIGINAL_CUSHION_PNG` **1**, `UNIQUE_SOURCE_TEXTURE_CONTRAST_NO_ROLE_NAME` **1** → 고유 역할/대비 단서 후보 **10/45**. 후보는 물리 기능·재질·스타일 엄격 승인이 아님.
- 서로 다른 버전 출처 주의: AF 소스 `4.0.3`과 런타임 `4.0.2` 동일 바이트 미증명 **20개**, 부모 모델 JSON/블록상태 SHA 일치로 전체 런타임 동치 자동 주장 불가 **25개**.
- B32의 검사기는 단서 분류, SHA 형식, 출처 버전 caveat, 역할/권리 승인0 및 B24↔B27 부품별 `face_count`/role 가설 관계를 재검증. 정상적으로 통과한 결과는 `INT5_B32_45_ORIGINAL_TEXTURE_SOURCE_CAVEAT_VERIFIED_V1.json`.
- 실제 텍스처 이미지의 픽셀 색·재질은 **이 배치에서 새롭게 다운로드해 분석하지 않았으며**, 개별 원본 face/UV→GPU 픽셀 배타 소유를 재현했다고 주장하지 않음.

## B33 — 원본 전체 모델 음성 결과 vs 단일 생략 맥락의 조건부 반응

- [B23 10개 맥락·F2 320장 기록](INT5_B23_FULL10_CONTEXTS_320_REAL_F2_FINAL_INDEPENDENT_AUDIT_V1.json), [B27 45개 원형 렌더 원장](INT5_B27_FULL_45_ORIGINAL_F2_SOURCE_VISUAL_SPATIAL_INDEPENDENT_EVIDENCE_V1.csv), [B28 직접 재감사 B25 8조합·F2 256장](INT5_B28_B25_ALL8_ORIGINAL_ARTIFACTS_INDEPENDENT_FINAL_AUDIT_V1.json)을 1:1 교차.
- **AF121#5·AF123#5 원본 전체 모델**에서 남/북 원본 제거 시 화면 반응 0 유지, B23 `all_others`/ `front_0_4`의 남/북/동/서도 각각 `0/0/0/0` 유지.
- 다른 맥락: source6·source4 고정 상태에서 0/1/2/3 하나를 생략한 **8개 실험**, 반응 조건 **7/8**, 남북동서 32뷰 중 반응 **8뷰**, 변한 원본 F2 화면 픽셀 **합계 10개**. 모든 차이는 개별 화면에서 **1~2픽셀**이며, 실측 좌표 10개의 ROI·뷰별 개수와 시간/음성대조가 기록과 일치.
- **원본 전체 모델 무반응**과 **별도 일부 원본 요소 제거 맥락에서의 1~2픽셀 조건부 반응**은 논리적 충돌이 아님. 전경 가림의 조건부 시각 변화이지, 어떤 요소가 실제 다리인지·유일하게 가리는지·한 face/UV가 특정 픽셀을 독점하는지 판단할 증거는 아님.
- B33 보고 JSON `INT5_B33_ORIGINAL_SOURCE5_FULL_VS_8_CONTEXT_CONDITIONAL_AUDIT_V1.json`.

## 실제 병렬 CI 검증과 재현성

- 신규 GitHub workflow: `.github/workflows/integration-int5-b31-b32-b33-three-research-audits.yml`. B31 실물 ZIP 다운로드·SHA/CRC/F2/로그, B32 원본 텍스처/역할 출처, B33 원본 전체/조건부 맥락을 **3개 Job으로 병렬 실행**.
- 신규 회귀시험 `tests/knowledge/test_int5_b31_b32_b33_evidence_parallel.py` **9개**: 원본 누락·데이터 범위·SHA 형식 변조·가짜 소재 승인·B23 전체 모델 거짓 반응·B28 좌표 조작 등 실패하도록 설계.
- 초기 CI에서 (1) 불필요한 Pillow 정적 import, (2) 원본 체크섬 8그룹 내 중복된 해시 수를 9로 센 계산 오류 발견. 소스와 테스트를 수정한 후 [최종 CI #45843425631](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45843425631) **3/3 Job SUCCESS**. 첫 실패 시도를 성공으로 위장하지 않음.
- 실제 CI의 원본 감사 결과 아티팩트 [B31 #15130505727](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45843425631/artifacts/15130505727), [B32 #15130470773](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45843425631/artifacts/15130470773), [B33 #15129805306](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45843425631/artifacts/15129805306)를 **별도 다운로드**해 3개 모두 ZIP CRC 및 결과 필드의 수량을 확인했다. Git에는 원본 ZIP/PNG 대신 SHA·모델 인덱스·제한적 화면 좌표·감사 결과만 유지.

## 엄격 연구 승인 상태 (변경 없음)

| 심사 항목 | 결과 |
|---|---|
| B26+B31 합계 원본 F2 실제 ZIP 독립 검수 이력 | 45요소·560 F2·70 로그 |
| B27 한정된 원본 요소 제거 화면 반응 | 43/45 |
| B32 텍스처 단서 후보 | 10/45 (역할·재질·스타일 엄격 승인 아님) |
| B33 원본 전체 모델 source5 무반응 | AF121#5·AF123#5 |
| B33 생략 맥락 source5 화면 반응 | 7/8 조합, 누적 10픽셀 |
| 실물 부품 물리적 기능·재질·스타일 승인 | **0/45** |
| 개별 원본 GPU face/UV 배타 픽셀 소유 승인 | **0** |
| 제3자 원본 학습·재배포 권리 승인 | **0** |
| H03 | **HOLD** |
| H05 | **CONDITIONAL** |
| F70 무조건 최종 승인 | **0/70** |

후속 연구에서 역할 의미와 UV 귀속을 엄격 승격하려면 실제 원본 텍셀 및 face/UV와 실게임 장면의 반복 원본 근거를 추가로 확보해야 한다. **현 단계에서 새 정량 검사 성공만으로 엄격 의미 최종 승인 또는 AI 원본 학습·재배포 권리를 부여하지 않는다.**
