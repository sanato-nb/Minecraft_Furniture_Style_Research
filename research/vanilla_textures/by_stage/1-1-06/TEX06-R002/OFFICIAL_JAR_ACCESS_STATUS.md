# TEX06-R002 — 공식 자산 접근 시도 및 분리된 증거 등급

- 목표: Java **1.21.11** 공식 Mojang client.jar에서 직접 8종 텍스처를 추출해 비공식 미러 SHA-256과 비교.
- 배포 메타데이터의 표준 출발점: https://piston-meta.mojang.com/mc/game/version_manifest_v2.json
- 2026-11-13 조회한 **PrismLauncher가 복제한** 버전 매니페스트(`PrismLauncher/meta-upstream/mojang/version_manifest_v2.json`, Git blob SHA `ca1a480811400bd5b55ab0ffa6bcddfa7e25bc20`)의 `id=1.21.11` 표본: `sha1=812ee7fdfdf648bb872f7a1dca33718de4e786b4`, version JSON URL `https://piston-meta.mojang.com/v1/packages/812ee7fdfdf648bb872f7a1dca33718de4e786b4/1.21.11.json`. 이 정보는 GitHub 복제본에서 확인한 **참조**이지 여기서 직접 Mojang HTTPS 응답을 검증한 것이 아니다. 메타데이터 SHA는 재배포/수정될 수 있으므로 향후 실검증 시 **당일 공식 매니페스트**에서 다시 조회.
- 제3자 링크가 가리키는 Mojang 클라이언트 객체: `https://piston-data.mojang.com/v1/objects/ba2df812c2d12e0219c489c4cd9a5e1f0760f5bd/client.jar`. SHA1 추정(객체 키): `ba2df812c2d12e0219c489c4cd9a5e1f0760f5bd`. **실제 파일 해시를 읽은 값 아님.**
- 시도: 실행 환경에서 Mojang API DNS/HTTP 접근 및 29MB급 JAR 다운로드가 실패. 그러므로 다운로드 성공/인증 완료라는 기록 없음.
- 준비 스크립트 `VERIFY_OFFICIAL_1_21_11.py`는 표준 Python 라이브러리로 공식 manifest->version metadata의 SHA1->로컬 JAR SHA1/크기->JAR 내부 PNG 8종 SHA256 / 모델·상태 의미를 비교한다. **스크립트 문법 및 도움말/무인자 경로만 테스트**. 공식 JAR로 실행하지 못함. 사용자 보유 JAR을 외부로 업로드하지 않는다.
- 사용: 자신의 컴퓨터에서 로컬 게임 파일 경로를 확인하고 `python VERIFY_OFFICIAL_1_21_11.py "경로/1.21.11.jar"`; 결과 JSON과 SHA가 검증되면, 그 결과를 별도 `TEX06-R003`에 기록. 게임 파일 자체를 공개 저장소에 올리지 말 것.
- 게임 내부 Facing/UV 정적 캡처 및 픽셀 대조는 별도 작업이며, JAR 파일 인증이 완료돼도 `ingame_static_verified`는 자동 true가 되지 않는다.
