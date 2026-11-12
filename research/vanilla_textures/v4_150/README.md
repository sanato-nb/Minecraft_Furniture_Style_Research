# 바닐라 텍스처 실측 누적 150종 · v4

**이 패키지는 Minecraft 게임 원본 텍스처 PNG를 포함하지 않는다.**

핵심 파일은 `11_누적150종_확장검증_보고서.md`와 `12_학습_진행도.md`.

`01_누적150종_픽셀측정.csv` = 이전 100종의 실측 기록을 계승하고 이번 50종을 실제 분석한 누적 기록.

게임 원본과 비교하려면 자신의 Minecraft Java 1.21.11 `client.jar` 또는 올바르게 추출한 PNG 파일을 확보하고 다음을 실행:

```bash
pip install pillow numpy
python verify_150_against_client.py --client-jar '/path/to/1.21.11.jar' --manifest '01_누적150종_픽셀측정.csv' --output verify.csv
python analyze_vanilla_150.py --client-jar '/path/to/1.21.11.jar' --output my_recomputed_stats
```

위 코드는 사용자가 제공한 파일과 **비공식 추출 미러의 해시가 일치하는지** 비교한다. 사용자 입력이 정식 게임 원본임을 자동으로 인증하지 않으므로, 파일 입수 출처를 별도로 확인해야 한다.

기존 v3 분석 코드를 보존하고 그 위에 신규 50종 목록을 추가하여 재실행할 수 있다. 코드 자체와 파생 통계/도표만 배포하며, 실제 텍스처/원본 게임 JSON은 넣지 않았다.
