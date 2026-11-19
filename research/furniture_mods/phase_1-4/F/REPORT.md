# 1-4-F 독립 종료 감사

**2026-11-19 KST · 통과 · 1-4 원본 텍스처·UV 연구 범위 종료 승인**

[고정 감사 기준 커밋](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/commit/c087fdaf2fffe078d168b04a791f557de35f38d8)의 A~E 원장을 새 작업 폴더에서 재생성했다. Git에 저장된 산출물 **49개**가 재현본과 바이트 단위로 일치했다. 1.21.1 Fabric 클라이언트를 별도로 실행해 **아틀라스 관측 217행**도 재현했다.

| 단계 | 결과 | 검산 범위 |
|---|---|---|
| A 인계 | PASS | 고정 텍스처 ID·버전 2,256개. 신규 1,996개, 선행 일치 175개, 선언 전용 77개, 원본 경로 누락 8개 |
| B 원본 PNG | PASS | 신규 1,996개와 대조용 5개를 고정 Git·JAR에서 재디코딩. 총 4,406,272화소의 알파별 합계와 원본 SHA 대조 |
| C 면·UV | PASS | 고유 면 키 592,312개. 사각형 실측 511,709면과 점·선·경계·부분 영역 보완 74,260면을 합쳐 원본 화소 근거 585,969면(98.93%). 기본 UV 검증과 영역·프레임 29,957행의 화소 합계 검산 |
| D 재질·배치 | PASS | 대표 상태 47개, 모델 적용 52행, 면 1,610행 및 바닐라 대조군 48면 재현 |
| E 예외·DB | PASS | 8개 ID의 `missingno` 폴백, 후보 16개 중 의자에 실제 쓰이는 13개, 의자 등록 상태 176개 및 고정 조건 88개 대조. SQLite 기존 테이블 9개 동일, 무결성 오류 및 외래키 오류 0건 |
| F 독립 종료 감사 | PASS | 원격 기준의 본문 75개, 그중 CSV·TSV 41개의 데이터 행 수 확인. 1-4-F 산출물과 진행표만 승인 커밋의 변경 대상 |

C의 원본 화소 근거가 없는 **6,343면**은 슬롯 미연결 6,202면, 원본 PNG 경로 누락 139면, 원본과 겹치지 않는 UV 2면이다. 슬롯 미연결 중 6,196면은 자식 모델에서 대응 텍스처 경로를 확인했다. 선행 면 4,113행은 동일 면·사각형 링크 3,937행과 영면적 176행으로 구분된다. 영면적 176행은 후속 C의 선 화소 172행·점 화소 4행과 연결돼 있다.

이번 종료는 [세부 실행계획](../../../../docs/furniture_mods_1-4/1-4_DETAILED_EXECUTION_PLAN.md)의 범위다. 전체 인게임 화소 비교, UV lock 적용 후 렌더, 조명·tint·필터링·애니메이션 타이밍과 실제 제작은 별도 업무다. E의 실제 참조 경로 재현은 Minecraft 1.21.1의 Another Furniture Fabric 4.0.2 기본 리소스 설정을 사용했다.

[독립 감사 집계](EXIT_AUDIT.json) · [원격 본문·SHA·행수 원장](REMOTE_INPUT_MANIFEST.csv)

## 1-5 인계

- [대표 상태의 텍스처·UV 인계표 52행](../entry04/1-5_TEXTURE_UV_HANDOFF.csv)
- [최신 연구 SQLite](../E_followup/research_texture_uv_runtime.sqlite.xz)
- [원본 화소 보완 원장](../C_followup/UV_SOURCE_SUPPORT.csv.xz)

## 재현

고정 원본 파일과 Git 체크아웃은 [B 재현 조건](../entry01/REPORT.md)을 따른다. [E 클라이언트 재현 절차](../E_followup/REPORT.md)에서 새 아틀라스 TSV를 생성하고, 저장소 루트에서 아래 명령을 실행한다. 감사 기준 커밋이 로컬 Git에 있어야 한다.

```sh
bash research/furniture_mods/phase_1-4/F/replay_exit.sh \
  AF_GIT HC_GIT JAR_DIR AF_FABRIC_402.jar AF_NEOFORGE_403.jar \
  NEW_ATLAS_TSV SCRATCH_DIRECTORY REPORT_DIRECTORY
```
