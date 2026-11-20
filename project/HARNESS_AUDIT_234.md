# 하네스 검수 2·3·4 보완 — 사용 및 재현

대상: (2) 모델 구조 분석, (3) 운영 연구 DB 인계, (4) 근거/API 정책 강제. 기존 역사 자료는 보존한다.

## 2. 기존 1-3-C 기반 공통 모델 분석

**별도 신규 `mcfr.model_analysis`는 제거했다.** `mcfr.geometry_engine`이 기존 역사 분석기 `research/furniture_mods/phase_1-3/C/analyze_geometry.py`의 함수를 직접 호출한다. 역사 1-3-C 코드·CSV·증거는 수정하지 않는다.

기존 1-3-C의 원본 `geometry`, `rotated_point`, `separation`, `classify_element`, `face_slot`, `hash_data` 함수로 회전 후 경계상자, 요소 간 AABB 접촉 거리, 형상 분류와 형상 지문을 계산한다. 공통 진입점은 H2 SQLite 등록·H3 원본 및 SHA 검증과 Vanilla/Mods 양쪽을 지원한다.

~~~sh
export PYTHONPATH=src
python -m mcfr.geometry_engine \
  --db /path/to/research.sqlite \
  --release minecraft-java-1.21.11-git \
  --source . \
  --asset 1.21.11/assets/minecraft/models/block/acacia_shelf_unconnected.json
~~~

모드는 해당 등록 릴리스 키·원본 디렉터리/JAR·모델 경로를 지정한다. 모드에 포함되지 않은 바닐라 부모를 연결하려면 같은 Minecraft 버전으로 **따로 등록된 Vanilla 원본**을 제공한다.

~~~sh
python -m mcfr.geometry_engine \
  --db /path/to/research.sqlite \
  --release my-mod-release \
  --source /path/to/mod.jar \
  --asset assets/mymod/models/block/chair.json \
  --vanilla-release minecraft-java-1.21.11-git \
  --vanilla-source /path/to/versioned/vanilla/source
~~~

- **PASS:** 부모 체인·정적 요소·텍스처 슬롯을 해석함. 암묵 UV 경고만 존재하는 경우도 포함한다.
- **PARTIAL:** 미해결 부모, 미등록 부모, 별칭 오류·순환 또는 정적 요소 부재 등으로 해석이 불완전함.
- **원본 검증:** 등록 자산 SHA, 등록된 JAR/ZIP 전체 해시를 검증한다. 중복 JSON 키, 비유한 좌표·각도를 거부한다.
- **한계:** 인게임 변환·실제 렌더링·픽셀 비교·커스텀 렌더러 및 암묵 UV 계산은 수행하지 않는다. 요소의 접촉은 메시 접촉이 아닌 회전 후 AABB 기준이다.
- **출력:** DB와 역사 원장을 변경하지 않는 읽기 전용 분석이며, 로컬 JSON 기록은 `--out`을 쓴다.

역사 연구의 **전체 배치 결과**를 재현할 때는 기존 1-3-C 스크립트를 그대로 사용한다. 새 공통 명령은 등록한 개별 모델의 재사용 가능한 온디맨드 분석 진입점이다.

## 3. 새 채팅/환경용 연구 상태 인계

**mcfr.handoff**는 SQLite의 일관된 백업과 메타데이터를 함께 저장한다.

~~~sh
export PYTHONPATH=src
python -m mcfr.handoff export --db /path/to/operational.sqlite --out /private/MCFR-handoff-001
python -m mcfr.handoff verify --input /private/MCFR-handoff-001
python -m mcfr.handoff restore --input /private/MCFR-handoff-001 --db /new/local/research.sqlite
~~~

내보낸 폴더에는 research.sqlite와 handoff.json(파일 SHA-256, 스키마 버전, 테이블 건수, 미완료 작업 건수, Git 커밋)이 있다. verify는 SHA·SQLite 무결성·외래키·테이블 건수를 검사하며, restore는 **기존 DB를 덮어쓰지 않는다.**

**보안 및 재개 한계:** SQLite에는 개인 경로와 AI 응답이 포함될 수 있다. 공개 GitHub/inbox/PR에 백업을 올리지 말고, 로컬 또는 접근 통제된 장소에 보관한다. 원본 파일 경로가 다른 PC에서 바뀌면 기록은 복원되어도 중단 작업은 자동 재개할 수 없다. 기존 원본은 별도로 확보해야 한다. 새로운 채팅에서 실제 복원을 수행하려면 이 로컬 DB에 접근 가능한 실행 환경 또는 전달받은 파일이 필요하다.

## 4. 설정 정책의 실제 실행 적용

harness/shared/config.json의 정책 두 개를 실제 명령에 연결했다.

- require_evidence=true: 일반 명령 mcfr.research_db register에서 **근거 파일 경로**가 필수다. manifest 최상위의 evidence_path 또는 각 assets 항목의 evidence_path로 지정하며, 저장소 내부에 존재하는 상대 파일 경로여야 한다. 파일명만 그럴듯한 허위 근거는 별도 수동 검수 대상이다. 기존 import-legacy·역사 재현 및 저수준 register_release() 호출은 이 CLI 게이트와 별개다.
- ai_api_enabled=false: H4 유료 API 전송을 기본 차단한다. 수동으로 의도한 한 번의 호출은 승인 해시와 키를 준비한 뒤 mcfr.workflow review-send REVIEW_ID --approve APPROVAL_SHA256 --enable-api로 실행한다. 기본 설정의 영구 변경 없이 해당 단건만 명시적 허용한다. API 비용이 발생할 수 있다.

일반 신규 등록 manifest 예시는 프로젝트의 기존 registry/legacy-releases.json 스키마를 따르되, 실제 제출에 대한 project/audits/ 아래의 근거 보고서를 만들고 다음 필드를 추가한다.

~~~json
{
  "evidence_path": "project/audits/EXAMPLE_REPORT.md",
  "release": {"release_key": "example", "profile": "mods", "target_id": "example",
              "version": "1.0", "minecraft_version": "1.21.11", "loader": "fabric",
              "pin_algorithm": "SHA256", "pin_digest": "<실제 SHA256>", "source": "<원본 출처>"},
  "assets": [{"source_path": "assets/example/models/block/example.json", "kind": "model",
              "resource_id": "example:block/example", "hash_algorithm": "SHA256",
              "digest": "<해당 파일 SHA256>"}]
}
~~~

예시 근거는 실제 파일이 아니므로 그대로 제출하면 등록이 거부된다. 별도 보고서의 존재뿐 아니라 내용·원본 링크·해시도 검수할 것.

## 테스트

~~~sh
PYTHONPATH=src python -m mcfr.foundation validate
PYTHONPATH=src python -m unittest discover -s tests/harness -p 'test_*.py' -v
~~~

추가 테스트는 부모 상속·UV·별칭, 원본 해시 변경, SQLite 백업 변조, 정책 차단을 다룬다. 이 보고서는 실시간 게임 실행이나 유료 API 응답 성공을 주장하지 않는다.
