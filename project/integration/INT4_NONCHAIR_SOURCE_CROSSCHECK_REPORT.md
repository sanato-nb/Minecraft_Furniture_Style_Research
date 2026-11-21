# INT-4 — 비의자 가구의 실제 원본 구조·블록상태·텍스처 참조 교차검증

## 공식 단계 및 범위

본 회차는 INT-4 '연구 결과 간 교차 검증'이며, 기존 [PR #40](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/pull/40)의 부모 누락 48모델 정적 블록상태 **0/48 도달** 판정을 보존한다. 임의의 미사용 모델을 게임에 강제 배치하지 않고, 기존 1-5 연구에서 출처와 실제 선택 상태가 정해진 대표 **15개 사례·19개 모델 적용**을 직접 다시 열어 검증한다.

## 1-5 B/C에서 범위 고정

| 유형 | 대상 1-5 사례 | 원본 비교 질문 |
|---|---|---|
| 연결형 테이블 | S14, S15, S16, S17, S18, S19 | Another Furniture multipart의 상판·다리, Handcrafted 단일·중앙, Macaw 연결/단일 |
| 연결형 책장 | S28, S29 | Macaw 원본 bookshelf base/middle의 기하·면·텍스처 결합 |
| 침대 | S37, S38 | Handcrafted oak_fancy_bed 발/머리의 선택 모델·부모 기하 |
| 카운터 | S39, S40, S41 | Handcrafted calcite finish 1·2, Macaw 원본 counter |
| 주방 싱크 | S42, S43 | Macaw water=false/true의 기하 면 55→56 |

기존 C 비교 판정 중 **C06, C12, C16, C17, C18, C19**의 원본 사례 ID를 인용한다. C17은 원래 바닐라 V12/V13도 포함한 비교이므로, 이번에는 **S42/S43 모드측만 새로 재검증**하며 바닐라의 가마솥 비교 전체를 새 검증으로 표시하지 않는다.

## 실제 소스 교차 검증 범위

- \`scripts/integration/audit_int4_nonchair_source.py\`: 역사 1-5 B의 \`CASES.csv\`와 \`APPLICATIONS.csv\`에 있는 **74개의 전체 모델 적용**에서 위 19개 적용만 고정 선택.
- AF 연구 4.0.3 Git \`57eb624...\`, Handcrafted \`8d21d166...\`, Macaw Fabric 3.4.2 SHA-256 \`e55d7a78...\`; 관련 Minecraft 1.21.1/1.21.11 공식 JAR를 GitHub Actions 임시 영역에서 읽는다.
- 모든 선정 사례별 원본 blockstate \`variants\` / \`multipart\` 조건을 독립 평가. **원본 선택 규칙 순서, 조건 만족/원본 모델 ID, 선택 회전 x·y, uvlock·weight**를 역사 B 적용 원장과 비교.
- 실제 원본 모델·상속 제공자 JSON의 Git blob SHA-1(또는 JAR SHA-256)을 다시 계산. 상속된 요소/면 개수 및 면별 텍스처 슬롯 결합·PNG 원본 존재 여부를 별도로 기록.
- 각 비교쌍의 원본 모델 적용 수·요소·면 수 및 모델 SHA 변경 여부를 메타데이터 CSV 두 종에 보존. 원본 PNG/모델/JAR/아이템 저작물은 절대 Git·아티팩트에 포함하지 않음.
- \`tests/integration/test_int4_nonchair_source.py\`와 \`.github/workflows/integration-int4-nonchair-source.yml\`에서 회귀검증 및 실제 원본 재생성.

## 판정 경계

- 원본 블록상태가 해당 모델을 선택한다는 **소스 수준의 출처 확인**이지 실제 게임에서 모든 해당 상태가 쉽게 배치·유지되거나 GUI에서 동일 모습으로 렌더된다는 증거는 아니다.
- 원본 PNG 파일 **존재 여부**는 검사하지만 화소 RGBA와 GPU 렌더 색/광원, UV-Atlas bake, 애니메이션 프레임 타이밍은 아직 재검증하지 않는다. 본문 1-5의 역사 측정값을 신규 측정으로 승격하지 않는다.
- 싱크대 \`water=true\`의 원본 면 1개 증가 자체는 확인 가능하지만 실제 애니메이션 물결이 보인다는 의미는 아니다.
- INT-5 부품 의미·스타일 승인 0. INT-6 AI 학습/배포 라이선스 승인 0. INT-4 전체 종료 또는 INT-7 최종 감사 완료로 승격하지 않는다.

## 후속

원본 교차검증 결과에 따라 **실제 블록상태에서 도달 가능한** 테이블·책장·침대·싱크대 대표 상태의 게임 내 사용성과 F2 사진을 새 독립 실험으로 확인한다. 침대/연결형 테이블은 인접 블록 자동 상태 변경과 특수 렌더를 구분한 다음 실험 조건을 설계해야 한다.

**CI 결과가 통과하기 전에는 실제 소스 재확정 수치 및 예외 건수를 완성으로 기록하지 않는다.**
