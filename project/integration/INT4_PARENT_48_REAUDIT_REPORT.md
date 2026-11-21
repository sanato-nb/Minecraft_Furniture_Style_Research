# INT-4 — 원본 부모 모델 누락 48경로 독립 재검증

## 연구 목적과 기존 증거

공식 INT-4의 **모델→부모→요소→면** 출처 체인을 확인한다. 종전 INT-2 고정 감사에서 16,572개 모드 모델 중 부모 누락 48경로(AF 랜턴 4, Macaw 책상 22·서랍 22), 정적 형상 없음·미해결 108경로가 기록됐다. 두 분류는 **Macaw 44개를 공유**하므로 서로 더하면 안 된다.

AF 랜턴 4개는 기존 감사에서 자체 모델 요소가 남은 부분 형상으로 분류했고, Macaw 44개는 자체 기하가 없는 경로로 분류했다. 이번 감사에서 원본을 직접 열어 해당 관계를 재검증한다.

## 실제 독립 수행

- `scripts/integration/audit_int4_parent_gaps.py`: 고정 AF Git 아카이브, Macaw 3.4.2 Fabric JAR, 공식 Mojang 1.21.1/1.21.11 JAR에서 48개 모델 JSON을 독립 개봉. 역사 1-3 B CSV의 경로·SHA·크기를 검증한다.
- 원본 `parent` 경로를 종료점까지 순서대로 추적. 자체 요소·면 개수, 실제 부모 존재/누락, 같은 이름의 다른 위치 파일(대체 가능성은 *미승인*)을 계산한다.
- `tests/integration/test_int4_parent_gaps.py`: 48·108·44 중복, 키 무결성, 실제/가상 부모 경로, 순환, JSON 중복 키의 회귀 검증.
- `.github/workflows/integration-int4-parent-gaps.yml`: 원본 해시를 고정하고 실제 Git ZIP·Macaw/Mojang JAR을 다운로드하여 전수 검사.
- 출력: `INT4_PARENT_48_ORIGINAL_CHAIN_RESULTS.csv`(경로별 48행), `INT4_PARENT_48_ORIGINAL_SUMMARY.json`(정적 관계/출처/범위/SHA).

## 확정과 보류의 분리

- 고정 소스의 부모 리소스가 실제로 없더라도 **해당 게임 내 가구가 보이지 않는다, 상호작용할 수 없다, 렌더가 깨졌다**고 단정하지 않는다. 실제 Minecraft baked 모델과 시각 결과는 별도로 검증해야 한다.
- 같은 basename의 다른 원본 파일이 있다고 해서 자동 대체하거나 과거 모델 JSON을 수정하지 않는다.
- 원본 48경로는 AI용 제작 자산 권리 승인과 무관하다. INT-5 의미 검증, INT-6 권리, INT-7 최종 감사는 미완료.
- 원본 JAR/ZIP/PNG/모델 본문은 아티팩트 및 Git 이력에 넣지 않고, 출처 경로·관찰 SHA·집계만 보존한다.
- 기존 원본 연구 31,242개 및 역사 인수인계, main은 변경하지 않는다.

## 재현

```bash
python -m unittest discover -s tests/integration -p 'test_int4_parent_gaps.py' -v
python scripts/integration/audit_int4_parent_gaps.py --root . \
  --af /tmp/af.zip --macaw /tmp/macaw.jar \
  --mc1211 /tmp/mc1211.jar --mc12111 /tmp/mc12111.jar \
  --out /tmp/int4-parent
```

실제 CI 결과가 확인되면 본 보고서에 실측 건수와 실행 SHA를 추가한다.

## GitHub Actions 실제 원본 독립 검수 결과 (2026-11-21)

[독립 원본 CI #44914040186](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/44914040186) **성공**, 오프라인 무결성·오류 주입 회귀테스트 **9/9 통과**.

| 검증 항목 | 실제 결과 |
|---|---:|
| 원본 B/JAR 모델 SHA와 바이트 길이 | **48/48 일치** |
| 기존 누락 부모 종단 재확인 | **48/48 실제 파일 누락** |
| 고유 누락 부모 식별자 | **3종** |
| AF 자체 요소·면 존재 경로 | **4** |
| Macaw 자체 요소 없는 경로 | **44** |
| 기존 'no static 108'과 중복 | **44** |
| 서로 다른 이름 같은 원본 다른 경로의 basename 후보 | **0** |
| 자동 부모 수정 | **0** |
| 실제 게임의 모델 깨짐·결함 판정 | **0** |
| 부품·스타일·AI 사용 권리 승인 | **0** |

### 실제 없었던 부모 경로

- `minecraft:lantern` → AF 랜턴 자식 4개, **원본 모델 자체 기하를 포함하지만 기본 부모는 없음**.
- `mcwfurnitures:block/parent/desk` → Macaw 책상 자식 22개, **원본 모델 자체 elements 없음**.
- `mcwfurnitures:block/parent/drawer_base` → Macaw 서랍 자식 22개, **원본 모델 자체 elements 없음**.

이 값은 JAR 자체에 포함된 모델 바이트, 실제 SHA 및 Mojang 클라이언트 참조를 대조해 얻었다. Macaw 44개가 실제 게임에서 보이지 않는다는 결론이 아님. 런타임 리소스 교체/자원팩/모델 동적 생성 가능성을 이 감사가 조사하지 않았으므로, **실제 F2 런타임 조사 필요**.

- Git의 보존 체크포인트: [INT4_PARENT_48_ORIGINAL_AUDIT_RESULT.json](INT4_PARENT_48_ORIGINAL_AUDIT_RESULT.json)
- 원본 48행 CSV SHA-256: `5d03ba00073a2db2a158e9ce654297beb1d48fa2ed52550030a7d32d5a2eb748`
- 최초 CI 아티팩트 `int4-parent-48-original-source-path-classification` (ID 14710324120), ZIP SHA-256 `d9d14584b9d2c4868205b492ed9c7cb0b02a03ed906aa338103d355d428c6f23`.
- 고정 결과가 바뀌면 재실행 CI는 체크포인트와 전체 생성 JSON 비교에서 실패하도록 구성했다.
- 후속: 원본 리소스 규칙/실제 클라이언트로 Macaw 대표 책상·서랍 및 AF 랜턴 **실제 화면과 런타임 동적 처리 여부** 검증. 원본 부모 파일을 추측해 새로 만들거나 과거 원장에 덮어쓰지 않음.

**이 작업은 INT-4의 일부 범위다. INT-4 전체 종료, INT-5 부품 역할 승인, INT-6 AI 학습 권한으로 확대하지 않는다.**
