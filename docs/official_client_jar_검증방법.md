# Minecraft Java 1.21.11 공식 client.jar 교차검증 도구 사용법

**현재 상태:** 도구 개발 및 합성 입력에 대한 단위 테스트는 통과했지만, 실제 Mojang 공식 `client.jar` 검증은 **아직 실행하지 않았습니다**.

## 1. 입력 파일

- [GitHub 연구 DB v8](../data/MC_Furniture_Style_Stage1_Research_v8.sqlite) 또는 v10으로 재구성한 SQLite
- 사용자가 **본인 PC에서 설치한 Minecraft Java 1.21.11 클라이언트 JAR**. 일반적인 Windows 설치에서는 `%APPDATA%\.minecraft\versions\1.21.11\1.21.11.jar`에 있을 수 있습니다. 런처·프로필에 따라 경로가 다릅니다.

**JAR을 GitHub에 업로드하지 마세요.** 기기에서 로컬 검사만 하면 됩니다.

## 2. 명령

```powershell
python scripts/verify_official_jar.py --jar "C:\Users\USERNAME\AppData\Roaming\.minecraft\versions\1.21.11\1.21.11.jar" --db "data\MC_Furniture_Style_Stage1_Research_v8.sqlite" --out "comparison.json"
```

경로의 `USERNAME`은 실제 사용자명으로 바꿔야 합니다. 종료 코드 0은 기본적으로 **도구가 실행되었다**는 뜻이며 모든 항목 일치를 보장하지 않습니다. 모든 항목 일치가 필요하면 `--strict`를 지정하세요.

## 3. 검사 범위

- `texture_stats_v4`의 바닐라 텍스처 **150개 PNG 파일**: JAR 내부의 원본 PNG를 읽어 SHA-256을 비교.
- `sources` 테이블의 모델·상태 JSON **148개 경로**: 파일 바이트를 읽어 Git blob SHA-1을 비교. 이 경로 수는 이전 체크포인트의 기록으로, 중복·누락 없이 전부가 존재하는지는 실제 출력 보고서를 봐야 합니다.
- 결과는 `match`, `missing`, `mismatch`로 분리해 JSON으로 저장하며 사용한 JAR 및 연구 DB 파일의 SHA-256도 기록합니다.

## 4. 해석 시 주의

- **모든 일치 ≠ 인게임 화면 검증 완료.** 바이옴 색 보정, 투명도, 모델의 최종 3D 렌더, 애니메이션 동작은 따로 검사해야 합니다.
- JSON이 재포맷되면 의미가 같아도 바이트 SHA는 다를 수 있습니다.
- 특수 렌더링 엔티티 모델 추출 JSON은 일반적으로 `client.jar` 내부 정적 에셋 경로에 그대로 있는 것이 아니므로 이 도구의 대상이 아닙니다.
- JAR 파일명만 보고 공식 배포본임이 증명되는 것은 아닙니다. 사용자가 실제 설치본과 버전을 확인해야 합니다.

## 5. 현재까지 기록된 결론

- **도구 사용 준비 완료**
- **합성 테스트 JAR 2개 자산의 일치 사례 단위테스트 통과**
- **Minecraft 1.21.11 공식 JAR 교차검증은 아직 미실시**
