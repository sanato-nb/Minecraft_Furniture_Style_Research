# INT-5 B28+B29+B30 — 원본 F2 독립 재감사 · 45부품 증거 교차 연구 · GUI 네이티브 충돌 방어

- 검수일: 2026-11-26 (KST)
- 원본: 누적 [Draft PR #136](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/pull/136) head `360a1603747aa17367ab6124a8109ed647a06931`.
- 새 독립 작업 브랜치: `work/int5-b28-b29-b25-artifact-full45-cross-audit-20261126` (PR #136을 base로 하는 stacked Draft).
- 연구 내용은 3D 요소·원본 face/UV·PNG 텍셀과 실제 Minecraft F2의 화면 변화뿐. 침대/의자 상호작용 전체의 게임플레이 기능 성공을 연구 의미 최종 승인 조건에 추가하지 않음.
- `main` 미병합, 원본 모드 JAR/PNG/F2의 Git 사본 미커밋.

## B28 — B25 8개 원본 아티팩트/256 F2 직접 독립 재검수 **완료**

- [원본 실제 Minecraft 1.21.1 Fabric B25 8 Job Actions #45784956570](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45784956570)는 **8/8 SUCCESS**.
- 이 작업에서 8개 원본 GitHub Actions ZIP을 각각 실제로 다시 다운로드하고 새 환경에서 ZIP CRC/ZIP SHA-256 검증, 내부 네이티브 F2 **256/256** PNG SHA-256, 실제 Minecraft `client.log` **16/16** SHA-256, 원본 의자 정확 서버 상태 **256건**, 접힌 의자 윗반블록 추가 상태 **128건**을 재검증.
- 원본 ZIP 바이트 SHA, 실제 화면 RGB max-channel 차 `>24`, `ROI=(350,275,675,620)`을 이용해 4방향 원본 `source5` on/off 동일 장면을 다시 계산. 정상 반복 A/A, 다른 상태, 빈 화면 또는 윗반블록 음성대조, ROI 및 원본 전경 바깥 변화0.
- 재현 가능한 코드 `src/mcfr/int5_b28_aggregate_original_artifact_reaudit.py`, 기계 검수 결과 `INT5_B28_B25_ALL8_ORIGINAL_ARTIFACTS_INDEPENDENT_FINAL_AUDIT_V1.json`.
- 별도 [GitHub Actions #45822463051](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45822463051)에서 원본 ZIP **8개를 다시 다운로드**하고 별도 Python 프로세스로 전체 비교; B28/B29 **2/2 Job SUCCESS**, [B28 결과 아티팩트 #15118383060](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45822463051/artifacts/15118383060) 재다운로드·CRC·결과 수량 직접 확인.

| 원본 제거 index | AF121: 남/북/동/서 | AF123: 남/북/동/서 |
|---|---|---|
| 0 | 0/0/0/0 | 0/0/0/2 |
| 1 | 1/0/1/0 | 1/0/0/0 |
| 2 | 0/0/1/0 | 0/0/2/0 |
| 3 | 1/0/0/0 | 1/0/0/0 |

- 합계 **8조합 중 화면 비영(非零) 7조합, 32개 카메라 비교 중 비영 8개, 픽셀 변화 합계 10개**. 실제 바뀐 좌표·각 변형의 원본 ZIP SHA는 JSON 기록.
- 이는 해당 이미지·시점·일시·엄격 임계에서의 **한정된 미세 변화**. 1~2개 픽셀을 모델 의미·물리 다리 역할·유일 가림 원인·GPU 단일 면 소유의 확정 근거로 승격 금지. 이전 전체 원형 B19의 AF121/AF123 index5 화면 무변화 두 사례는 유지.

## B29 — B24↔B26↔B27 45요소/229면 증거 교차 감사 **완료**

- 기존 B24 45요소 원본 `source_element_index`/face/role 가설, B26 HC12+Macaw12 원본 F2 24개, B27 전체 45개 원본 F2 CSV를 각 원본 파일과 정확한 키로 교차 확인.
- B24 **45**, B26 **24**, B27 **45** 행; 중복/누락 모델·인덱스 없음; AF121 **10** + AF123 **10** + HC11210 **13** + MACAW67 **12** = **45** 원본 요소·**229** 원본 면.
- B24 역할 가설 수량: `LEG_OR_LOWER_POST 16`, `SEAT_LAYER 6`, `LOWER_FRAME 7`, `BACKREST_ASSEMBLY 16` (현실 기능 승인 아님); shared/generic texture cue **35**, 이름 또는 대비 질감 cue **10** (재질 승인 아님).
- B26의 24부품 남/북 픽셀 수, 원본 ZIP SHA 및 측면 반응 기록이 B27과 **24/24 일치**. B26 F2 기록 **384**, 로그 **48**. B27 전체 F2 기록 **560**, 로그 **70**, 원본 개별 요소 제거 화면 변화 **43/45**, 전체 원형에서 무변화 AF121#5·AF123#5 2개 유지.
- 재현 가능한 교차 검사기 `src/mcfr/int5_b29_full45_crossledger_audit.py`가 합계/원본 SHA/중복·누락·거짓 역할·권리 승인 반례 시 실패하도록 검사. 회귀시험 7건.
- [GitHub Actions #45822463051](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45822463051) B29 Job SUCCESS, [B29 JSON 아티팩트 #15117564106](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45822463051/artifacts/15117564106) 직접 재다운로드·CRC 확인.
- **범위 주의:** B29는 원본 45 ZIP 전체를 다시 다운로드한 조사가 아니라, *이미 원본에서 유래한 B24/B26/B27의 출처·상태·수치 교차 감사*다. B28의 실제 8 ZIP/256 F2 재감사와 분모 혼용 금지.

## B30 — 기존 INT-4 침대 원본 F2 CI 네이티브 장애 원인 직접 확인 및 최소 복구

- 최신 PR #136 head의 기존 [INT-4 실패 실행 #45788398894](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45788398894), `occupied-bed-exterior` Job #139800937992. 실패 원문: `Timed out waiting for both local clients joined`.
- 실패 원본 아티팩트 #15101088082 3개 실게임 `native/*.log` 재다운로드·CRC 확인: **BedObserver JVM의 `SIGBUS` 네이티브 충돌** (`ld-linux-x86-64.so.2`), 서버는 RenderAudit 1명만 실제 접속.
- 해당 실패 Job만 재실행한 **attempt #2**도 실패. 원본 아티팩트 #15116824787 직접 재다운로드·CRC 검사: 이번에는 BedObserver는 정상 접속했지만 **RenderAudit host 클라이언트가 `java.lang.UnsatisfiedLinkError: Failed to locate library: liblwjgl_opengl.so`**로 Minecraft 초기화 중 충돌. 따라서 '서버 접속이 느렸다'는 단순 timeout 진단은 불충분하고, **GUI 네이티브 초기화 실패**라는 재현 관찰이 명확하다. 두 충돌이 동일 내부 원인인지는 확정되지 않음.
- 모델링 자체와 무관한 GUI 기동 경쟁을 줄이기 위해 원래 두 클라이언트를 동시 생성하던 `src/mcfr/int4_bed_exterior.py`를 **RenderAudit GUI 실제 서버 JOIN 확인 → BedObserver GUI 실행·JOIN 확인** 순서로 수정. 개별 프로세스가 JOIN 전 종료하면 실제 종료코드·원본 클라이언트 로그 꼬리를 조기에 보고하고, 정상 종료·서버 state/동일 F2 검사 기준은 유지. 별도 기본 GUI/중간 과정 회귀시험 4개.
- **B30 최종 실게임 검증 성공**: 신규 PR #137 head `720e427d819b486187e6bc63cbacf583c25cd59e`의 [Actions #45823236922](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45823236922) `completed/success`. 기존 4개 Job이 모두 성공했고 `occupied-bed-exterior`도 실제 `native` + `uv_probe` 두 모드를 끝까지 실행.
- 성공 원본 아티팩트 [#15118718140](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45823236922/artifacts/15118718140)를 직접 재다운로드해 ZIP CRC 확인, ZIP SHA256 `64409343bae6c12f56e0ed4adbde0aed1def963087be5034a7e33d7b753896d8`, 원본 F2 PNG **14/14** SHA256 및 원본 서버·관찰자·호스트 로그 **6/6** SHA256 확인. 두 독립 실제 게임 세션 모두 `RenderAudit`와 `BedObserver` 정확 서버 접속 **4건** 확인.
- 별도 결과 `INT5_B30_NATIVE_FABRIC_BED_DOUBLE_CLIENT_STAGGERED_BOOT_FINAL_RESULT_V1.json` 보존. 원인 가설은 두 JVM 네이티브 초기화 동시 실행 경합이며 **한 번 성공으로 원인 유일성이나 미래 항상 성공을 증명하지 않는다**. 수면·파괴 등 모델링 무관 기능시험을 **새로 추가하지 않았고**, 기존 실제 F2/서버 상태 검증과 원본 로그를 덮어쓰지 않았다.

## 엄격 심사 경계

- **H03 HOLD, H05 CONDITIONAL, F70 무조건 0/70** 유지.
- 원본 45부품 실제 기능/재질/스타일 최종 승인 **0/45**, 개별 original GPU face/UV 배타 픽셀 귀속 **0**, 제3자 원본 자산 AI 학습·재배포 권리 승인 **0**.
- '실게임 F2 영상에 픽셀 차이가 있다'와 '실제 어떤 소재/가구 부품이다' 사이의 증거를 구분한다.
- 외부 파일 등 새 원본 ZIP/PNG는 Git에 넣지 않고 GitHub Actions에서 만료 아티팩트 및 원본 SHA로만 추적.
