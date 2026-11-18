# 1-4-E · 텍스처 예외, 연구 DB와 1-5 인계

1-4-D 종료 커밋 `1da87488d7d067cfb6fd202cc123b534a40683f0`을 기준으로 고정 블록상태의 모델 선택, 모델별 슬롯과 면, 앞선 화소 측정을 대조했다.

## 예외의 영향

| 대상 | 확인 결과 |
|---|---|
| 원본 경로 미확인 8건 | Another Furniture의 고정 Git 트리에서 정확한 PNG 경로 8건이 모두 없었다. 7건에 모델 면 139개가 연결되고, 나머지 1건은 파티클 슬롯 선언만 있었다. |
| 블록상태와 아이템 범위 | 고정 블록상태의 모델 선택 원장에서 경로 미확인 텍스처를 그대로 바인딩한 모델을 직접 선택하는 사례는 0건이다. 139면 중 12면은 `another_furniture:item/stone_tombstone`의 아이템 모델 면이다. 게임 내 등록·표시 여부는 별도 검증 범위다. |
| 대체 후보 16경로 | 의자 등받이 변형별 11개, 좌판·하부의 재배치 경로 2개, `unused/` 아래 식탁보와 묘비 경로 3개의 PNG 및 Git blob SHA를 확인했다. 정확한 리소스 참조가 확보될 때까지 8건의 예외를 유지한다. |
| 선언 전용 텍스처 77건 | 모델 면 연결 0건. 모델별 슬롯 149행은 `#layer0` 58행, `#particle` 91행이다. 이 중 블록상태에서 모델을 직접 선택하는 파티클 슬롯 38행이 있어 면 UV 집계와 별도로 보존했다. 아이템 레이어와 파티클의 런타임 효과는 별도 근거가 필요하다. |

[텍스처별 예외](TEXTURE_EXCEPTION_REVIEW.csv) · [대체 경로 후보](ALTERNATE_ASSET_CANDIDATES.csv)

## 선행 측정과 인계

선행 면 RGBA **4,113행**을 모델·기하 제공자 SHA, 요소·면 방향, PNG 리소스 ID 및 SHA, UV 회전·반전, 화소 사각형·알파 집계와 대조했다. **3,937행**은 C의 동일 면 근거에 연결했다. 이 링크가 가리키는 RGBA 지문은 C에서 새로 계산한 값이다. **176행**은 두 원장에서 모두 UV 면적이 0으로 확인되어 화소 지문 없이 기록했다. [선행 면 연결표](PRIOR_FACE_LINKS.csv.xz)

정규화 SQLite에는 텍스처 **2,256건**, 원본 경로와 면이 있는 텍스처의 UV 집계 **2,171건**, 예외 **85건**, 선행 면 연결 **4,113건**과 비교 표본 **52개 모델 적용·1,610면**이 들어 있다. 전체 모델·면 결합은 1-3-F DB, 화소 사각형과 프레임의 상세 측정은 C 분할 원장에 있다. DB의 `input_artifact` 테이블은 원본 입력 경로와 SHA-256을 기록한다. 독립 검산에서 SQLite 무결성 및 외래키 오류 0건, F 모델·면 키의 차이 0건을 확인했다.

- [SQLite DB 압축본](research_texture_uv.sqlite.xz) · [스키마](schema.sql) · [독립 검산](INDEPENDENT_AUDIT.json)
- [1-5 텍스처·UV 인계표](1-5_TEXTURE_UV_HANDOFF.csv) · [D 표본 비교](../entry03/REPORT.md)

## 재현

저장소 루트에서 C 재현 절차의 `--faces` 출력과 고정 Another Furniture Git 체크아웃을 지정한다.

```sh
entry=research/furniture_mods/phase_1-4/entry04
python "$entry/build_handoff.py" --af AF_GIT --faces MODEL_FACES.csv.xz --out "$entry"
python "$entry/audit_handoff.py"
xz -dk "$entry/research_texture_uv.sqlite.xz"
```

다음 1-4-F에서 A~E의 결과를 독립적으로 재계산하고 원격 저장본·예외 처리·기존 단계 경로를 검증한 뒤 전체 1-4 종료를 판정한다.
