# 하네스 검수 2·3·4 보완 — 사용 및 재현

대상: (2) 모델 구조 분석, (3) 운영 연구 DB 인계, (4) 근거/API 정책 강제. 기존 역사 자료는 보존한다.

## 2. 모델 JSON 심층 정적 분석

새 모듈 **mcfr.model_analysis**는 등록된 단일 JSON 모델의 부모 체인, JSON SHA256, 상속 텍스처, 별칭 순환, 요소별 from/to와 회전, 면별 명시 UV·UV 회전·cullface, 누락 및 외부 부모를 보고한다. 기존 검증 엔진의 해시·JSON 최상위 키 검사에서 한 단계 확장한 읽기 전용 분석기다.

Python 3.12, 등록된 DB, 원본 디렉터리 또는 고정 JAR/ZIP가 필요하다. 저장소 루트에서:

~~~sh
export PYTHONPATH=src
python -m mcfr.model_analysis \
  --db /path/to/research.sqlite \
  --release minecraft-java-1.21.11-git \
  --source . \
  --asset 1.21.11/assets/minecraft/models/block/acacia_shelf_unconnected.json
~~~

모드는 해당 릴리스 키와 검증 가능한 JAR 경로, JAR 내부 모델 경로를 지정한다.
- PASS: 카탈로그 해시와 정적 JSON 구조를 해석할 수 있음.
- PARTIAL: 부모·텍스처가 미해결, 미등록 디렉터리 부모, 순환 또는 정적 요소 부재.
- 한계: 암묵적 UV 투영, 인게임 블록 상태 변환, 커스텀 렌더러, 실제 텍스처 픽셀은 분석하지 않는다. 모드 JAR가 외부 바닐라 부모를 포함하지 않을 때는 PARTIAL로 남긴다.
- 결과는 직접 DB 원장을 덮어쓰지 않으며, 필요하면 --out으로 로컬 JSON 보고서를 작성한다.

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
