# INT-4 H23 — R06 물 표면 애니메이션 통제 실험 최종 연구 보고

## 판정과 직계 출처

H22 Draft #104의 69/70 모델링 계약 V4를 계승한다. 마지막 조건부 위험 질문 R06을 공식 원본과 프레임 고정 대조군의 실제 Minecraft F2 비교로 해결했다. **별도 모델링 연구 계약 V5는 역사 모델 62/62, 위험 질문 8/8, 합산 검토 단위 70/70 범위 통과**. 기존 엄격한 F70 승인, H03/H05, INT5/INT6는 변경하지 않는다.

## 공식 원본 및 통제 변수

- Minecraft Java 1.21.11, Macaw's Furniture Fabric 3.4.2 공식 JAR SHA256 `e55d7a78b878043af82875cb8738941b0bba1a3c77652dea3d75a434dbba1a0e`.
- 역사 S43 `mcwfurnitures:oak_kitchen_sink[facing=north,water=true]`, 동일 위치·카메라의 실제 클라이언트 두 세션.
- H22 출처: 물 표면 element 1 UP, UV [1,2,13,11], rotation 0. 원본 water_still.png 16×512, 32개 서로 다른 16×16 프레임 및 32개 서로 다른 선택 UV 영역. PNG SHA256 `d5d63ddd36311d6b064123750715fe551fbeccb5cb1f677ef93027e9305791de`.
- 원본 .mcmeta SHA256 `e9b8025fde1b09b0a4d2a38427b04f98f28a593045be6d177eb2b29164c872b0`, animation frametime 2. 실험용 임시 JAR에서 해당 .mcmeta 1개만 frames=[0]으로 고정. 나머지 모든 uncompressed ZIP 멤버 바이트 일치, PNG·모델·클래스 변경 없음. 임시 JAR SHA256 `16c0562bb972c7d8c2a19ddd79748b715593833f1931d9c26bfa7d4300cef301`. 원본 및 변형 JAR을 Git에 저장하지 않음.

## 실제 실행 및 독립 재검증

[실게임 Actions #45339878802](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45339878802) 성공. 원본 3장, 고정 대조군 3장, 실제 정확 서버 상태 6회. 각 PNG 1024×684. 실제 시간 간격 원본 10.636/10.367초, 고정 10.367/10.379초.

| RGB24 비교 | 원본 물 변화 | 고정 물 변화 | 원본/고정 싱크 비수면 및 돌 대조 |
|---|---:|---:|---:|
| T0/T1 | 0 | 0 | 0/0 |
| T0/T2 | 17 | 0 | 0/0 |
| T1/T2 | 10 | 0 | 0/0 |

원본 변화 17/10픽셀은 양쪽 이미지 모두 청색 물 픽셀이다. 각 화면 물 영역의 청색 픽셀 778개 유지. 두 세션 간 싱크 비수면 및 돌 바닥 대조도 RGB24 변화 0. 기존 F11E 원본 세 장의 22/8/9 변화는 별도 역사 근거로 보존한다. 실제 원본 애니메이션을 고정했을 때 선택된 수면의 관측 변화가 사라진다는 제한된 인과 증거를 얻었다.

[원본 F2·로그 artifact 14895158453](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45339878802/artifacts/14895158453), ZIP SHA256 `7064033b712cbc8bd7b1e50ccd08da1c5710524bdb0d20516d9d5f86c7ddd912`. [별도 독립 재열람 CI #45340359660](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45340359660)에서 실제 6 PNG와 로그 SHA·CRC, 픽셀 분석, 영구 H23 JSON 재계산 일치 및 V5 생성 통과. [파생 artifact 14896285844](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45340359660/artifacts/14896285844). 합성 회귀시험 4/4 성공 #45339987452.

## 완료 원장과 승인 경계

- `INT4_H23_R06_ANIMATION_CONTROL_RESULT_V1.json` 실제 통제 결과.
- `INT4_F70_MODELING_CONTRACT_CASE_REVIEW_V5.csv`, `INT4_F70_MODELING_CONTRACT_SUMMARY_V5.json`: V4 → R06만 범위 통과 및 새 F2 표시. 기존 F2 참조 및 69개 다른 행 보존.
- 역사 모델 62/62 및 위험 질문 8/8. 총 70개 서로 다른 검토 단위 범위 통과, 조건부 0, 보류 0. 이 분모는 모든 Minecraft/모드 모델 총량이 아니다.
- 기존 엄격 F70 무조건 0/70, H03 HOLD, H05 CONDITIONAL, INT5 의미 승인 0, INT6 AI 학습·재배포 권리 승인 0 그대로.
- 원래 F11E F2의 정확한 애니메이션 프레임 번호, GPU 개별 texel 대응, RGB24 미만 변화 부재, 전체 게임플레이, 물리 기능, 모든 방향/상태, 전체 모드 버전 및 권리 승인을 주장하지 않는다.
- Draft PR #105, main 미병합. 향후 새 모델 연구 및 통합 검토는 별도 분모와 승인 기준으로 관리한다.
