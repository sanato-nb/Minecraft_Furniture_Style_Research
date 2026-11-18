# 1-3-D 데이터 규격 및 재현

| 원장 | 키 및 연결 |
|---|---|
| D_BLOCKSTATES.csv | `mod,state_id`가 고유 키다. B의 blockstates 경로·SHA와 1:1이다. |
| D_STATE_RULES.csv.gz | `mod,state_id,rule_index`가 고유 키다. 원본의 variant 키 또는 0부터 시작하는 multipart 인덱스를 `source_selector`에 저장한다. 빈 condition은 명시 조건 없이 적용된다. |
| MODEL_STATE_ASSEMBLY.csv.gz | 규칙 키에 0부터 시작하는 `option_index`를 붙인다. 로컬 `model_key`를 C에 조인한다. 바닐라 대상은 공식 JAR 경로와 SHA-256이 기재된다. |
| D_PROPERTY_DOMAINS.csv.gz | `mod,state_id,property`가 고유 키다. 조건에 적힌 가능한 값을 기록했다. |
| D_MULTIPART_ASSEMBLIES.csv.gz | `mod,state_id,observed_domain_assignment`가 고유 키다. 매칭된 모든 규칙 인덱스를 원문 순서로 기재한다. |
| CONNECTION_RULES.csv | 상태당 한 행이다. `evidence_id`가 있는 상태는 등록 코드가 확인된 실제 블록 ID를 코드 근거에 연결한다. |
| D_CODE_EVIDENCE.csv | `evidence_id`가 고유 키다. Java 소스는 Git blob SHA-1, JAR class는 개별 SHA-256이다. |
| D_EXCEPTIONS.csv | 선택 키가 보존된다. 동일 누락 모델 ID가 서로 다른 조건에서 사용될 수 있다. |

`x,y`는 원본 선언 또는 값이 생략됐을 때 0이다. `x_mod_360,y_mod_360`은 양의 나머지다. `explicit_fields`로 명시된 기본값과 생략을 구분한다. `weight=1`, `uvlock=false`가 기본값이다. 회전의 적용 결과는 C 원장의 요소 회전과 별개다.

상태와 로컬 모델 해시는 B·C와 같은 규약을 따른다. Another·Handcrafted는 Git blob SHA-1, Macaw는 JAR 내부 바이트 SHA-256이다. 집계·CSV는 원래 JSON/PNG/JAR이나 역어셈블 전문을 포함하지 않는다.

Python 3.10+로 `analyze_states.py`와 `audit_states.py`에 동일 인자를 전달한다. `--b`는 B의 `source_verification` 경로이며 옆에 B의 `SOURCE_REGISTRY.csv`가 있어야 한다. `--c`는 C 원장 경로다. `--af`와 `--hc`에는 B에서 고정한 Git 객체를 가진 저장소, `--macaw --version --project`에는 Macaw JAR 및 Modrinth 배포·프로젝트 JSON, `--mc1211 --mc12111`에는 고정 버전의 공식 Minecraft 클라이언트 JAR을 전달한다. `--out`을 생략하면 스크립트 폴더에 저장된다.

코드 위치는 `javap -p -c -classpath <JAR> <class>`로 확인했다. Mojang 클라이언트 매핑의 SHA-1은 1.21.1 `2244b6f072256667bcd9a73df124d6c58de77992`, 1.21.11 `031a68bebf55d824f66d6573d8c752f0e1bf232a`이다. Macaw의 `BlockPos` 방향 호출은 Fabric intermediary 1.21.11 v2 매핑 JAR(SHA-256 `f45b9530d0becae596fd48743e3ee1733cc2cdc69128cdb7d8d3571de163ab87`)과 Mojang 매핑을 대조했다. [Fabric 매핑 배포본](https://maven.fabricmc.net/net/fabricmc/intermediary/1.21.11/intermediary-1.21.11-v2.jar)
