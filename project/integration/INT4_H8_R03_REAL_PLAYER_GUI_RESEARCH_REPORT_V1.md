# INT-4-H8 — R03 실제 GUI 플레이어 테이블 설치·제거 독립 검수

## 원본 실험
- [성공한 GitHub Actions #45151609933](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45151609933)에서 **공식 Minecraft Java 1.21.11 + Fabric + Macaw's Furniture 3.4.2** 새 폐기 월드를 생성하고 실제 GUI 입력을 수행했다.
- [원본 F2 3장·실제 클라이언트 로그 아티팩트 #14806817076](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45151609933/artifacts/14806817076). 원본 ZIP SHA256 `78c6b781ea74faf7805bf0d340987473d9ce5be3f9c2e198300b62b9923baa54`.
- 게임 플레이어의 핫바에 `mcwfurnitures:oak_table` 아이템을 선택시키고 **우클릭 버튼 3**으로 동쪽 테이블을 설치했다. 설치 전 centre.east=false/east=air, 설치 후 centre.east=true/east.west=true를 서버에서 확인했다.
- **좌클릭 버튼 1**로 같은 동쪽 테이블을 제거한 뒤 centre.east=false/east=air 상태 복귀를 실제 서버가 확인했다. 절차는 reset→join→remove **하나의 새로운 GUI 세션**에서 수행됐다.
- 모든 시점은 같은 게임 GUI에서 네이티브 F2 1024×684 PNG를 획득했으며, 원본 3개 PNG SHA와 클라이언트 로그 SHA를 실험기와 독립 검사기로 검증. 직접 시각 검토 결과 한 탁자 → 두 탁자 연결 → 한 탁자로 복귀.
- 초기 R03 원본 실험은 `/setblock`을 통해 인접 테이블을 놓았다. 이번 H8에서는 원본 데이터팩을 **초기 reset 및 읽기 전용 서버 검증**에만 사용하고 기존 `join/remove` 자동 설치 함수를 호출하지 않았다. 이는 **새로운 플레이어 아이템 조작 근거**이며 H7 단순 증거 재사용과 다르다.

## 실패 기록 보존
- 실행 #45150181295: 새 명령의 version/world/work 인자 등록 누락, 게임 입력 미실행.
- 실행 #45150969249: 플레이어 우클릭 설치/양방향 연결 성공, 제거 좌클릭은 조준이 상판 아래여서 실패. 원본 불완전 상태 로그·F2 아티팩트 보존.
- 실행 #45151601134: 촬영 코드와 회귀시험의 조준각 상수가 잠시 달라 테스트 실패.
- 최종 #45151609933: 상판을 향하도록 고도각 21° → 16° 변경 후 **동일 GUI 세션 설치→해제·F2 감사 성공**.

## 증거 해석 주의
- 복제해 재사용한 R03 구형 `summarize` 함수의 `player_item_placement_tested=false`와 `state_changed_after_adjacent_setblock=true`는 **과거 /setblock 전용 분류 규칙이 생성한 플래그**로, 새 H8의 입력 메커니즘을 나타내지 않는다. H8의 GUI 실험에서는 실제 X11 클릭 기록, 원본 서버 로그, 새 R03 감사의 `scope.player_creative_GUI_item_placement_verified=true`가 입력 검증 근거이다. 이 모순을 숨기거나 두 값을 동시에 플레이어 조작 판정에 적용하지 않는다.
- 실험은 **스크립트 기반 창작 모드 GUI 실제 클릭**이며 사람의 수동 설치나 서바이벌 모드 행동을 입증하지 않는다.
- **R03의 한 가지 새로운 실제 입력 경로**가 입증됐다고 해서 마크 가구 전체의 동적 기능, pixel-to-UV 인과, 전체 70개 원본 F 계약이 승인되는 것은 아니다.
- R01/R02/R04/R05/R07 및 R06/R08 기존 판정 불변. **F70 조건부 70/70·무조건 승인 0, H03 HOLD·H05 CONDITIONAL, H 최종 승인 0**.
- INT5 의미 승인/INT6 AI 학습 및 원본 재배포권 승인 0. 실제 게임 PNG·로그·JAR는 저장소에 커밋하지 않고 원본 SHA와 감사 메타데이터만 저장한다.

## 이어서 필요한 작업
- **R04**: 시간 간격을 둔 실제 게임 water=false↔true 전환 입력과 변화 원인 및 ROI/UV 분리. 기존 R06의 물 영역 프레임 차이만으로 유체 기능 승인 금지.
- **R05**: 한 게임 내 플레이어 침대 설치→수면→기상→파괴 전 과정을 4단계 실시간 관찰.
- **R07**: AF 연구 Git/실행 릴리스 모델 선택 차이의 원본 코드와 실행 JAR 원인을 재조사하고 제작자 의도는 별도 미승인.
- R03조차 서바이벌 모드/플레이어 키·시점 변화·UV 인과는 여전히 열려 있으며 H03/H05 종료 게이트를 최종 통과시키지 않는다.
