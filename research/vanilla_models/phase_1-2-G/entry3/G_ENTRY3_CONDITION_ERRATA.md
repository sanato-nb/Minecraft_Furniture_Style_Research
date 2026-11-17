# 1-2-G Entry3 — D multipart 조건 정규화 검증 기록

- 발생: 최초 G_ENTRY3_INDEPENDENT_RECOUNT.json에서 945/945 원본 바이트·SHA와 PNG 185/185 RGBA 검증이 통과했으나 D multipart 조건 6건에서 `D_MULTIPART_CONDITION` 오류를 기록했다. 최초 Actions 결론은 failure이며 Entry3는 미승인 상태로 유지했다.
- 원본 재대조: cherry_fence, composter, copper_bars, crimson_fence, cyan_stained_glass_pane, dark_oak_fence의 `multipart[0]`에 `when` 필드가 없어서 새 G JSON의 조건 표현은 `null`. 반면 기존 D 원장 `D_ENTRY3_REMAINING_217_RULES.csv`는 해당 기본 규칙의 `multipart_when_json`을 `{}`로 기록하고 있었다.
- 의미: `when` 생략과 빈 객체 조건은 모두 **무조건 적용하는 기본 multipart 규칙**을 의미한다. 전후의 모델 참조, `apply` 원문, 옵션 인덱스, 명시 필드는 최초 실행부터 일치했다.
- 조치: G 독립 비교기의 조건 비교에서 `source when=null`과 `D when={}`의 이 1가지 동치만 허용하도록 수정했다. 다른 조건 표현이나 다른 `apply` 차이는 계속 오류로 남는다.
- 기존 D·A~F·v69 데이터는 **변경하지 않는다**. 최초 6건 오류 기록과 Actions 실패 이력은 보존하고 수정 후 전체 945개를 처음부터 재검증한다.
- 범위 제한: 조건 동치는 정적 JSON 의미에서의 대응이며 Minecraft 실제 state registry 또는 게임 엔진 렌더 검증이 아니다.
