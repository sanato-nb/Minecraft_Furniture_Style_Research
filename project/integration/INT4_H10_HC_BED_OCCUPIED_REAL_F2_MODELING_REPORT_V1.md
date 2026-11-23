# INT-4-H10 완료 — Handcrafted 침대 점유상태별 실제 모델·F2 시각 검증

## 모델링 연구 결론

**실제 Fabric Minecraft 1.21.1 클라이언트**에서 Handcrafted 4.0.3 `oak_fancy_bed`의 `foot` 모델을 **같은 좌표·같은 카메라**에서 `occupied=false`, `occupied=true`, `air` 순서로 렌더링·F2 촬영하고 서버 로그 상태를 독립 재검증했다.

- 실제 원본: [GitHub Actions 45166482002](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45166482002), [7개 아티팩트 파일 #14815016375](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45166482002/artifacts/14815016375).
- 원본 ZIP SHA256 `eaf49eb7cebb9b16975693e7c874ae7647f04a52a1c0c1cc3c18318a3b83ccaa`; ZIP CRC 검사 통과.
- 원본 런의 SHA256: `client.log` `41ac3770f2bb67ebac8d6f854e042e47ebe93f8cf781c2b198686642512ff0fe`.
- 각 시점 게임 명령 `/execute if block`에서 정확히 `occupied=false`, `occupied=true`, `minecraft:air`를 서버가 각각 확인했다.
- 네이티브 F2 **1024×684 PNG 3개**와 같은 런의 원본 서버 로그, 원본 모델·부모 모델 Git SHA를 독립 감사했다. 3개 F2는 별도 Actions 원본 ZIP에 보존하고 원본 PNG/JAR을 Git 커밋하지 않았다.
- 촬영 카메라 `-15.5 122.3 45.5 180 20` 동일. 창작 모드 잠자기·기상·아이템 사용·파괴 기능 테스트는 수행하지 않았다.

## 정량적 원본 F2 변화

| 실제 게임 화면 비교 | RGB 채널 최대차 `>=24` 픽셀 수 |
|---|---:|
| `occupied=false` ↔ `occupied=true` | **2,097** |
| `occupied=false` ↔ `air` | **7,830** |
| `occupied=true` ↔ `air` | **7,578** |

검사 영역은 원본 전체 1024×684 중 `x=350..674, y=275..619`이다. 실제 PNG를 별도 독립 재열람해 `false↔true` 전체 2,097픽셀의 변화 경계가 `x=477..546, y=403..461`에 집중됐음을 확인했다. 차이 픽셀의 2,091개(약 99.7%)는 `false↔air` 또는 `true↔air` 전경 차이 마스크에도 포함된다. 따라서 **화면 전체 밝기 변화로만 설명되는 결과는 아니며** 침대가 표시되는 위치에서 렌더 차이가 관찰됐다고 제한적으로 기록한다.

단, 차이 픽셀의 정확한 모델 요소/면/텍스처 UV 번호를 역추적한 것은 아니다. 같은 카메라·실제 상태·원본 소스 일치라는 근거가 있어도 **GPU의 어떤 화소가 특정 UV 면에서 나왔는지**는 별도 문제다.

## 원본 모델 선택과 시각 결과의 연결

| 검증 | `occupied=false` | `occupied=true` |
|---|---|---|
| 원본 블록 | `handcrafted:oak_fancy_bed` | 동일 |
| 점유 속성 | `false` | `true` |
| 리프 모델 | `oak_fancy_bed_single_white_foot` | `oak_fancy_bed_single_white_foot_occupied` |
| 부모 모델 | `fancy_bed/bed_single` | `fancy_bed/bed_single_occupied` |
| 모델 요소 | 12개 | 14개 |
| 모델 면 | 72개 | 84개 |
| 원본 연구 Git vs 런타임 JAR JSON | 동일 | 동일 |
| 실제 서버 정확 상태 | 통과 | 통과 |
| 실제 네이티브 F2 | 통과 | 통과 |

원본 모델 요소/면/UV의 변경 내역은 `INT4_H10_OCCUPIED_SINGLE_FOOT_FOUR_ELEMENT_CHANGES_V1.csv`(4행), `INT4_H10_OCCUPIED_SINGLE_FOOT_24_SOURCE_FACE_UV_V1.csv`(24행), `INT4_H10_OCCUPIED_SINGLE_FOOT_FACE_UV_SOURCE_AUDIT_V1.json`으로 증거 출처를 분리했다.

## 재현성과 실패 이력

- 새 F2 실제 게임·독립 감사 [run 45166482002](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45166482002): 원본 소스/배포 JAR 검사, Minecraft 실행, 서버 정확 상태 확인, 원본 3 PNG SHA 및 화면 대비 독립 검증 **통과**. 마지막 Git 자동 푸시 단계만 브랜치 동시 커밋으로 **non-fast-forward 실패**.
- 위 run의 [원본 ZIP #14815016375](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45166482002/artifacts/14815016375)에서 감사 JSON 전체를 복원하여 `project/integration/INT4_H10_OCCUPIED_FOOT_REAL_CLIENT_SOURCE_AUDIT_V1.json`으로 커밋했다. 원본 artifact 감사 파일과 GitHub 저장 파일의 Git blob SHA **`b4e4639259f687c145f1766a2656346705e89027`이 완전히 동일**.
- 원본 4요소·24 UV 감사를 수행한 [run 45166104848](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45166104848)도 모델 SHA/CSV/결정론 검사까지 통과했고 자동 푸시에서만 실패했다. 결과 3개를 원본 ZIP에서 복원하여 각 Git blob SHA **3/3 일치** 확인 후 별도 커밋.
- 구형 H10 설치 환경이 지연된 [run 45163855384](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45163855384)은 환경 단계에서 보류되어 있으며, 실제 게임 모델 검증 실패의 근거로 삼지 않는다.

## 연구 단계별 판정

- **H10 한정 모델 형상·화면 변화**: **실제 게임 원본 재현 통과**. 의미는 동일 카메라·정확 서버 상태·원본 소스 모델과 가시 픽셀 차이 존재.
- **면별 GPU 픽셀↔UV 대응**: 미승인. 원본 24 UV 좌표는 문서화했지만 실시간 렌더 얼굴 인과는 독립 입증되지 않음.
- **F70 기존 조건부** 70/70, 최종 무조건 승인 0: 본 H10 실험은 원본 연구 S37의 **새 점유 true 파생 상태**를 추가로 비교하는 것이며 기존 필수 F70 사례 하나를 무단 최종 통과로 올리지 않음.
- **H03** HOLD, **H05** CONDITIONAL, H 전체 종료 0, INT5 부품 의미·INT6 학습 및 재배포권 승인 0 유지.
- 새로운 모델링 연구에서는 수면·기상·파괴 기능 전체를 필수 검증으로 추가하지 않는다.
