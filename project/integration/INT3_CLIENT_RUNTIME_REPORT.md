# INT-3 / Minecraft 실제 클라이언트 의자 16방향 검증

**완료 범위:** 고정 PR #32의 연구 모델 4종과 그 원본 블록상태 방향 16개를 실제 Java Edition Fabric 클라이언트에서 게임 내 블록으로 배치하고, 각 상태의 서버 판정을 확인한 후 **Minecraft F2 기능으로 1024×684 원본 PNG 16장을 실제 촬영**했다.

## 실제 성공한 GitHub Actions

- [실제 Fabric 클라이언트 촬영 2개 버전 전부 통과 — Actions #44894353504](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/44894353504)
- **Minecraft 1.21.1 (Fabric 0.18.4): 12/12** — Another Furniture 의자 AF121 4개 방향, 접힌 의자 AF123 4개 방향, Handcrafted 의자 HC11210 4개 방향.
- **Minecraft 1.21.11 (Fabric 0.18.4): 4/4** — Macaw 의자 MACAW67 4개 방향.
- 각 게임/모드 설치는 기존 `mcfr.runtime`의 공식 클라이언트 SHA와 Modrinth JAR SHA를 사용한다. CI에서 공식 Minecraft 서버가 생성한 **별도 새 평지 월드**를 클라이언트 전용 저장소에 복사하고, 실제 `/setblock`과 `/execute if block`을 실행한다.
- `client.log`의 서버 실행 상태 `MCFR_CHAIR_STATE_...=PASS`를 확인한 경우에만 F2 촬영을 증거로 집계했다. 원본 자료 및 사용자 게임 월드 수정 없음.
- 16 PNG 전부 원본 F2 출력이며 크기 1024×684, 파일 단위 SHA-256 검증 완료. 데이터/클라이언트 조립 그림과 구별.

## 실증에서 드러난 두 가지 중요한 제약

**1. Another Furniture 소스 버전 차이:** 실제 실행에 설치된 AF 4.0.2의 `acacia_chair` 원본 JAR 블록상태 Git blob SHA-1은 `3a806533856f169a502373bda43a76eeabc1e689`이고, PR #32 연구 Git 4.0.3의 SHA-1 `37643398d7a49fdcfc6f2308ca04c13fb0b43aed`와 다르다. 이 차이를 조용히 무시하지 않았다. **이번에 촬영한 8개 AF 상태의 정확한 모델 리소스와 y 회전만** 실행 JAR 자체를 열어 직접 확인하고 게임 상태 PASS를 받았다. AF 릴리스 전체 88개 옵션이 연구 원본 4.0.3과 동일하다고 인증하지 않는다.

**2. 접힌 의자 지지 조건:** 최초 실행에서 AF123 `tucked=true` 네 방향이 게임의 블록상태 검사에 실패했고 자동으로 `tucked=false`가 됐다. [AnotherFurniture 원본 ChairBlock](https://github.com/crispytwig/AnotherFurniture/blob/57eb624cbb7f408d43398c7434b0d38d312cb55d/common/src/main/java/com/starfish_studios/another_furniture/block/ChairBlock.java) 의 `updateShape` 및 [TuckableBlock](https://github.com/crispytwig/AnotherFurniture/blob/57eb624cbb7f408d43398c7434b0d38d312cb55d/common/src/main/java/com/starfish_studios/another_furniture/util/block/TuckableBlock.java)의 `canTuckUnderBlockInfront`를 확인했다. 의자 앞면에 **바닐라 상단 반블록**을 지지대로 배치하자 4개 모두 `tucked=true` 상태 검증을 통과했다. 실험에 필요했던 지지 블록이 사진에 보이므로 단독 모델 진단 이미지와 직접 픽셀 동일성을 주장하면 안 된다.

## 촬영된 16방향과 원본 소스

| 게임 | 모델 | 방향 | 원본 상태 회전 y | 실제 스크린샷 |
|---|---|---|---|---:|
| 1.21.1 | AF121 — acacia_1 | 북·동·남·서 | 0·90·180·270° | 4 |
| 1.21.1 | AF123 — acacia_10_tucked | 북·동·남·서 | 0·90·180·270° | 4 |
| 1.21.1 | HC11210 — warped_chair_black | 북·동·남·서 | 0·90·180·270° | 4 |
| 1.21.11 | MACAW67 — acacia_chair | 북·동·남·서 | **90·180·270·0°** | 4 |

최종 총괄 접촉시트에서 16개 화면 모두 의자 형태를 수동 관찰했으나, 이는 **모델이 화면에 나타난다는 확인**일 뿐 실제 baked mesh·UV 아틀라스 정확도, 모델 부품 역할/충돌/실제 착석 기능 및 저작권/AI 학습 허가를 검증한 것이 아니다.

## 증거 파일과 재실행 방법

- `src/mcfr/chair_runtime_fixture.py`: 원본 블록상태/모델 선택의 지문을 확인하고 16방향 데이터팩 및 공식 바닐라 테스트 월드 생성. AF123용 지지 블록은 원본 코드와 실 게임 동작 근거로만 추가.
- `src/mcfr/chair_runtime_capture.py`: 기존 클라이언트 런처 재사용, 서버 상태 PASS, F2 PNG 완전성·화소 크기·SHA 추적.
- `src/mcfr/runtime.py`: 기존 장기 연구 하네스 CLI에 `chair-capture`만 추가.
- `.github/workflows/integration-int3-runtime-chairs.yml`: 1.21.1과 1.21.11 두 버전의 Java 21·Fabric 실제 Xvfb 클라이언트 캡처. Actions 아티팩트 `int3-real-fabric-client-chair-1.21.1` (PNG 12 + 로그 + JSON) / `int3-real-fabric-client-chair-1.21.11` (PNG 4 + 로그 + JSON) **45일 보존**.
- [16개 F2 스크린샷별 원본 상태/해시/제한 범위 JSON](INT3_CLIENT_RUNTIME_16_F2_EVIDENCE.json). 재현 가능한 소스/런타임 SHA 및 버전별 리포트 확인 가능.
- [PR #32 원본 PNG·UV 16방향 진단 이미지](INT3_CHAIR_16_TEXTURED_POSE_SUMMARY.json)와 실제 F2를 비교하는 오프라인 접촉시트/갤러리/16개 진단↔실게임 병렬 뷰를 별도 검수 묶음으로 제공. **관찰 카메라·투영·조명·배경이 다르기 때문에 픽셀 차이 수치로 합격 판정하지 않는다.**

보조 시각 검토 접촉시트 SHA-256: `05e1ec75549dd5ad6c7ea6558d68a14aee8112efd22abecfba383b848c24eaf8`. 시각 검수 CSV SHA-256: `370be6c25cb1ca0c430c0cfa8d34a04ad9efc810c494df7df6b8e823f8a19426`.

## 완료/보류 기준

- **검증 완료:** 고정 4개 모델/16개 방향을 실제 게임에 배치, 서버가 16/16 소스 상태 확인, 실제 클라이언트 F2 PNG 16/16, 각 이미지 SHA, 출처 연결, Macaw 90° 기준.
- **근거 제한:** AF 4.0.2 대 연구 4.0.3의 전체 blockstate blob 불일치. 이 검증의 AF 범위는 선택 8개 케이스뿐.
- **검증 보류:** 진단 렌더와 16개 실제 게임 화면의 정밀 baked mesh/UV lock/렌더 픽셀 일치, 역할·재질·스타일의 공식 확정, 게임 내 착석 기능·충돌의 해당 16상태 실측, 제삼자 자산의 AI 학습·재배포 권리.
- **원본 보호:** 원본 Minecraft/모드 JAR·PNG·JSON 본문, 사용자 게임월드, 이전 H2 연구 DB를 변경하지 않고 별도 임시 월드만 사용. Draft PR, `main` 자동 병합 금지.

**이번 단계의 최종 판정은 실제 Minecraft 클라이언트 F2와 서버 상태 검증 성공(16/16)이며, AI 가구 제작의 재료·스타일·기능 최종 완성 판정은 아니다.**
