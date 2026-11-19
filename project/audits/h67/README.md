# H6~H7 통합·실전 검증 · Adorn

Adorn을 신규 연구 대상으로 등록하고 Minecraft 1.21.11용 Fabric 배포본 7.6.0과 7.6.1을 비교했다. 입력은 두 배포 파일의 공식 SHA-1·SHA-512와 로컬에 기록한 SHA-256, 파일 크기, 내부 Fabric의 모드 ID와 버전으로 고정했다. [7.6.0 배포](https://modrinth.com/mod/adorn/version/MwMpNgec) · [7.6.1 배포](https://modrinth.com/mod/adorn/version/tyOUUBLZ) · [입력 핀](ADORN_PINS.json)

## 결과

| 검증 흐름 | 결과 |
|---|---|
| H6 신규 등록과 재개 | 7.6.0 자산 4,340개 등록 및 검증. 64개에서 중단한 뒤 같은 작업 ID로 재개 |
| 입력 고정 업데이트 재현 | 공식 배포 메타데이터 스냅샷을 발표 순서로 입력해 `BASELINE → UPDATE_DETECTED → UNCHANGED` 확인 |
| H7 증분 연구 | 추가 0개, 바이트 변경 0개, 동일 2,837개, JAR에서 사라진 경로 1,503개. 재검사 선택은 0개였고 새 JAR의 핀 검사는 통과 |
| H7 처음부터 전수 검사 | `FRESH`로 7.6.1의 2,837개 모두 검사. 64개에서 중단한 뒤 재개했고 최종 실패 0개 |
| 바닐라 교차 비교 | 바닐라 4,768개와 Adorn 2,837개의 정적 관찰 지표 조합 51개 가운데 공통 10개 |
| 원본 텍스처 대조 | 사과 상자 `apple_crate.png`의 SHA-256과 16×16 픽셀 256개 일치 |
| AI 승인 검증 | 검토 요청 1건 준비, 잘못된 승인 해시 차단, 외부 전송 0회 |

각 회차의 완료 명령을 반복해도 실행 원장에 한 건만 저장된다. 운영 DB의 등록을 반복했을 때 추가 자산은 0개였다. [기계 판독 결과](RESULT.json)

사라진 경로는 모델 651개, 블록 상태 426개, 아이템 정의 426개다. 이 수치는 `assets/adorn/`의 모델·블록 상태·아이템 정의·PNG·PNG 메타데이터 경로에 한정한다. 게임 안에서 기능이 제거됐는지는 별도의 런타임 실험이 필요하다. 픽셀 비교는 JAR에서 직접 읽은 원본 텍스처 한 장의 결과다. Adorn 인게임 촬영과 유료 AI API 검증은 이 실행 범위에 포함되지 않았다.

## 재현

두 공식 JAR을 저장소 밖에 받은 뒤 저장소 루트에서 실행한다. Python 3.12 및 Pillow를 사용한다. 스크립트는 임시 작업 폴더에서 새 SQLite DB를 만든다. 출력에는 실행 시각이나 임의 실행 ID가 포함되지 않아 공개 결과와 바이트 단위 대조가 가능하다.

```sh
python scripts/migration/replay_h67.py \
  '/path/to/Adorn-7.6.0+1.21.11-fabric.jar' \
  '/path/to/Adorn-7.6.1+1.21.11-fabric.jar' > /tmp/h67-result.json
cmp /tmp/h67-result.json project/audits/h67/RESULT.json
```

[후속 런타임 검증](../adorn_runtime/README.md)에서 두 버전을 실행하고 최상위에서 사라진 1,503개를 조건부 오버레이의 동일 파일로 확인했다.
