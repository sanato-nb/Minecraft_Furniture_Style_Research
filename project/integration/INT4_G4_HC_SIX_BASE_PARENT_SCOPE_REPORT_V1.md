# INT-4-G4 Handcrafted 기초 모델 6개 원본 부모·자식 경로 감사

고정 HC Git 8d21d166 원본 JSON 6개를 직접 열어 Git blob SHA를 검증함.
6개 모두 block/block 부모 및 display.gui 변환값을 정의하고, 자체 elements는 없음.
이 결과는 일반 블록 JSON 입체 요소 없음이 렌더 불량을 증명하지 않음을 보여준다.
과거 1-3-C 부모 체인 16,572행과 D 옵션 78,456행을 출처 해시 확인 후 재개방해 해당 base의 자손·정적 선택을 계산.

| HC 모델 | 직접 자식 | 전체 하위 모델 | D 선택 하위 모델 | 판정 |
|---|---:|---:|---:|---|
| HC1 handcrafted:block/base/bed_block | 8 | 1427 | 1408 | VERIFIED_HC_BASE_DISPLAY_PARENT_WITH_STATIC_D_SELECTED_DESCENDANTS |
| HC2 handcrafted:block/base/bench_block | 12 | 1537 | 1512 | VERIFIED_HC_BASE_DISPLAY_PARENT_WITH_STATIC_D_SELECTED_DESCENDANTS |
| HC3 handcrafted:block/base/chair_block | 1 | 199 | 187 | VERIFIED_HC_BASE_DISPLAY_PARENT_WITH_STATIC_D_SELECTED_DESCENDANTS |
| HC4 handcrafted:block/base/couch_block | 6 | 1425 | 1408 | VERIFIED_HC_BASE_DISPLAY_PARENT_WITH_STATIC_D_SELECTED_DESCENDANTS |
| HC5 handcrafted:block/base/phantom_trophy_block | 1 | 2 | 1 | VERIFIED_HC_BASE_DISPLAY_PARENT_WITH_STATIC_D_SELECTED_DESCENDANTS |
| HC6 handcrafted:block/base/statue_trophy_block | 6 | 12 | 6 | VERIFIED_HC_BASE_DISPLAY_PARENT_WITH_STATIC_D_SELECTED_DESCENDANTS |

**원래 A HOLD는 변경하지 않았고, 이번 G4는 부모 템플릿의 정적 소스 역할만 평가한 것입니다.**
자바/아이템/렌더러 선택·라이브 베이크 UV·기능·의미·재배포 권리의 승인은 없음.
G/H 최종 종료 승인 0, INT5 및 INT6 권리 승인 0.

