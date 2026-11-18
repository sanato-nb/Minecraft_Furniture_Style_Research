# 1-3-F 재현 및 다음 G

## DB 사용

```sh
xz -dc furniture_research.sqlite.xz > furniture_research.sqlite
sqlite3 furniture_research.sqlite "PRAGMA integrity_check; PRAGMA foreign_key_check;"
```

`model.model_key`는 C의 안정 키이며 `source_id`로 모드 버전, Minecraft 버전, 원본 고정 식별자 및 해시 방식을 조회한다. 원본 참조에 쓰는 SHA와 원본을 고정하는 SHA를 `asset_hash_kind`, `pin_kind`로 구분한다. `geometry.provider_key`와 `lineage`에서 상속 원형을 찾는다. `effective_face_texture`는 원형 요소·면과 모델별 슬롯의 바인딩을 연결한다. 요소의 회전과 D 상태 선택의 회전은 각각 `element`와 `option`에 있다. UV는 C에서 계산한 값이며 `uv_declared`로 원문 선언 여부를 확인한다.

`texture`의 고유키는 해당 고정 모집단의 리소스 ID와 Minecraft 버전이다. `face_instances`는 상속 모델별 적용 수이므로 고유 면 수와 다르다. `SOURCE_EXCEPTION` 8개는 1-4에서 경로를 우선 확인하고, `DECLARED_SLOT_ONLY` 77개는 실제 적용 근거를 확보한 경우에 측정 범위를 검토한다. `PRIOR_RGBA_SHA_MATCH`는 파일 SHA와 기존 원장을 연결한 상태다.

기존 원장 기준으로 `F_1-5_COMPARISON_CANDIDATES.csv`의 상태·규칙·옵션 키를 D에 조인한다. [E 반례 원장](../E/EXCEPTIONS.md)의 상태 표본 ID와 함께 검토한다.

## 재생성

Python 3.11 이상과 Git, SQLite의 역직렬화 지원이 필요하다. 원본 고정 식별자와 확보 경로는 [B 종료 보고서](../B/source_verification/B_SOURCE_EXIT_REPORT.md), [C 재현 문서](../C/C_NEXT.md)에 있다. 연구 Git 저장소에 E 종료 커밋의 트리와 그 입력 파일을 준비한다. C 폴더는 `analyze_geometry.py`, 바닐라 폴더는 고정된 `1.21.1.jar`와 `1.21.11.jar`를 포함한다.

```sh
python build_handoff.py --repo RESEARCH_REPO --prior FURNITURE_MODS_DIR \
  --b B_SOURCE_VERIFICATION_DIR --c C_DIR --d D_DIR --e E_DIR \
  --af AF_GIT --hc HC_GIT --macaw MACAW_JAR --vanilla VANILLA_JAR_DIR --out OUTPUT_DIR
python audit_handoff.py --b B_SOURCE_VERIFICATION_DIR --c C_DIR --d D_DIR --e E_DIR --out OUTPUT_DIR
```

G는 A~F 고정 근거, C/D 예외와 F 인계 범위를 재집계하고 M1~M6를 각각 심사한다. F 시점의 상위 승인 수는 0/6이다.
