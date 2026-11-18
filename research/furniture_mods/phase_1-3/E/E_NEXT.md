# 다음 단계 1-3-F

E는 9개 가구 유형의 대표 상태 47개를 고정 원본으로 비교했다. F에서 B·C·D·E 원장의 키를 연결하고 1-4 텍스처·UV 및 1-5 구조 비교 인계 데이터를 정리한다.

- CATEGORY_EVIDENCE.csv의 model_key 및 provider_key를 C와 조인한다. mod,state_id,rule_index,option_index는 D의 모델 선택 키다. 바닐라 형상 제공자는 C_VANILLA_PARENTS.csv에서 조인한다.
- 상태별 적용 요소, 형상 제공자, 회전을 포함한 구조 서명, 텍스처 바인딩을 보존한다. 열린 서랍과 닫힌 서랍, 쿠션 설정, 조리대 타입은 같은 형상을 공유할 수 있다.
- E의 비교와 미확인 항목은 1-5 후보에 포함한다. 미검증 PNG·UV 후보는 기존 v24/1-4 실측 기록과 대조한다. E의 실화소·게임 렌더 검증 건수는 0이다.
- 1-3 A~E 완료. F와 G가 남았으며 M1~M6 최종 통과는 0/6이다.

## 재현

Python 3.10 이상으로 비교와 검산을 실행한다.

```sh
python compare_furniture.py --af AF_GIT --hc HC_GIT --macaw MACAW_JAR --mc1211 MINECRAFT_1_21_1_JAR --c C_DIR --d D_DIR
python audit_comparison.py --c C_DIR --d D_DIR
```

두 명령에서 --out 생략 시 스크립트 폴더에 저장한다. 입력은 C·D 원장과 고정 원본이다. 표본은 E_SAMPLE_SELECTION.csv, 기하를 보고 정리한 부품 후보는 E_PART_GROUPS.csv에 있다. 구조 서명은 기하 제공자의 순서 보존 요소·면 지문과 상태 x/y의 조합이므로 재질·UV 결과의 동일성을 뜻하지 않는다.
