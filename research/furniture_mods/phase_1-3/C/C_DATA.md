# 1-3-C 원장 사용법

gzip 파일의 내용은 UTF-8 CSV다. `model_key`는 C 원장 내부 조인 키다. 같은 파일의 영구 식별은 모드·고정 원본·경로·SHA를 사용한다.

| 원장 | 내용 |
|---|---|
| `mod_furniture_catalog.csv.gz` | 모델 1행당 원본 신원, 회차, 적용 요소의 출처, 자체·상속 개수, AABB, 재질·UV 집계 |
| `MODEL_PARENT_CHAINS.csv.gz` | 모델별 선언 부모, `chain_keys`의 부모 순서와 종단 상태 |
| `mod_model_elements.csv.gz` | 선언 요소의 좌표, 피벗, 회전, 두께, 경계 제한, 가장 가까운 요소와 간격 |
| `MODEL_FACES.csv.gz` | 선언 요소와 면 방향별 텍스처 슬롯, UV 선언, 회전·컬링·tint |
| `PARTS.csv.gz` | 선언 요소별 기하 분류, 기하와 슬롯으로 판정한 후보 부품, 근거 등급 |
| `C_GEOMETRY_REUSE.csv` | 형상 선언의 적용 경로 수와 순서를 보존한 좌표·회전·면 방향 지문 |
| `C_VANILLA_PARENTS.csv` | 원장에 연동한 바닐라 부모의 버전·경로·SHA-256 |
| `C_EXCEPTIONS.csv.gz` | 부모·생성 아이템·정적 요소 없음·텍스처 슬롯 예외 |
| `C_CODE_SHA_INDEX.csv` / `C_CODE_EVIDENCE.csv` | 코드와 클래스의 해시 원장 및 Handcrafted 각도·좌표 Mixin과 Crockery 렌더러의 근거 파일 |

`geometry_source_key`를 요소 원장의 `source_key`로 조인한다. 바닐라 키는 별도 원장에 있다. 좌표 셀이 `|`로 구분된다. AABB 순서는 xmin, ymin, zmin, xmax, ymax, zmax다. 모델 해시는 AF/HC Git blob SHA-1, Macaw는 JAR 엔트리 SHA-256이다. 코드도 같은 기준을 따른다.

## 재현

[공식 Macaw JAR](https://modrinth.com/mod/macaws-furniture/version/xhmciaUD), 두 원저자 Git 저장소의 고정 커밋, Mojang 메타데이터와 클라이언트 JAR 두 버전을 준비한다. 입력 버전·SHA는 `C_AUDIT.json`에 있다. 바닐라 폴더에는 `1.21.1.json`, `1.21.1.jar`, `1.21.11.json`, `1.21.11.jar`를 둔다. B의 `source_verification/B_SOURCE_REMOTE_READBACK.json`에서 `records`의 `path,git_blob_sha` 두 열을 헤더가 있는 CSV로 내보낸다.

```sh
python analyze_geometry.py --af af_repo --hc hc_repo --macaw macaw.jar \
  --b ../B --remote-record b_remote_record.csv --vanilla vanilla --out .
python audit_geometry.py --out . --b ../B
```
