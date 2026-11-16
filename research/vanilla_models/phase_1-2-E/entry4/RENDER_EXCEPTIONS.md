# 1-2-E 원본 예외 분류 86개

`E_RENDER_EXCEPTIONS_86.csv`는 고정 모집단 86개 각각의 원본 SHA, 일반 요소 부재, D 참조 건수 및 소스 선언 유형을 기록한다. 모든 경로에 `UNVERIFIED_RUNTIME_RENDERER`를 유지한다. 이름만으로 블록 엔티티나 특수 엔진 구현을 확정하지 않는다.

`UNRESOLVED.csv`는 86개 각각의 실제 renderer 경로에 필요한 후속 근거(공식 클라이언트 연결 또는 인게임 렌더)를 기록한다. 이것은 E의 **소스 예외 분류 완료 경계**로 관리하며 엔진 실행 인증을 뜻하지 않는다. `air.json`의 `missingno`는 제공 원본 PNG가 없고 `block.json`·`thin_block.json`은 D에서 직접 선택하지 않는 표시 템플릿이다. 나머지 particle PNG 역시 실제 보이는 표면으로 단정할 수 없다.
