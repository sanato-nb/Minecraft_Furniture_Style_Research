# Minecraft Furniture Style Research v51 — 1-2-A 이어가기

1. GitHub `main` 최신 HEAD → `handoff/STATE.json` → `research/vanilla_models/v51/REPORT.md` / `SUMMARY.json` / 544행 `01_P1_544_EVIDENCE_LEDGER.csv` 순으로 확인. v50 이전 '최신' 표시보다 v51 이후 기록 우선.
2. P1 **544개 경로**, 원본 path+SHA 근거 연결 **335개**, 검사한 증거에서 미연결 **209개**. 이 둘은 전체 geometry+UV+PNG+blockstate+renderer 완료율이 아니다. 자산 식별은 `(asset_type, full_source_path, git_blob_sha)`.
3. v51 새 직접 원본 P1 SHA 연결 **54경로**: jungle/mangrove/pale_oak/warped 선반28, moss/pale_moss carpet5, 이전 미연결 P1 부모 carpet1, 가마솥/템플릿10, 발광 블록10. v50 281→v51 335. 과거 연구 '완전 미존재' 보증이 아니라 기존 선택적 근거에서 신규 직접 소스 검증이라는 뜻.
4. 고유 원본 직접 선언 **44 elements / 185 faces**: cauldron templates 3×14요소/59면=42요소/177암시UV면, carpet 1요소/6명시UV면, mossy_carpet_side 1개의 0두께 요소/2명시 UV면. 재사용한 v49 선반 부모 7종 11요소/38면은 신규 원형 수에 더하지 않는다.
5. 원본 부모를 leaf에 적용한 **826건 면 적용** = 선반152, 카펫24, 가마솥590, 발광60. 명시 UV 소스 176건/암시 UV 소스 650건. 고유 원본 선언 185면과 혼합 금지. 템플릿 단독 사용 기준 미해결 texture slot 면 **11건**은 자식 override를 확인하기 전 leaf 오류로 확정 금지.
6. original blockstates **15파일, variants 21건, multipart110규칙** (선반96 + pale_moss14), 선반 4종 파생 정적 **128조합/256모델 적용**. 54개 중 직접 world model reference45, template/inventory 등9. 런타임 유효성 증거 아님.
7. **PNG 바이너리 접근 제한**: original redstone_lamp.png file fetch에서 UnicodeDecodeError(텍스트 해석). 신규 PNG RGBA 픽셀 분석 0; 원본 PNG 바이트를 확보할 수 있는 접근 방법이 생기면 원본 SHA/좌표/alpha 및 암시UV 별도 실측. PNG를 보지 않고 '픽셀 검증'으로 보고 금지.
8. 다음 단계: v51 미연결209에서 초/초케이크 색상 변형, 셜커 상자, 거북알/픽클/레드스톤 토치 등을 소스 경로+SHA와 기존 기하/상태 근거에 교차 대조. 새로운 기하 분석과 부모 재활용을 구분. 충분한 증거 확보 후 v52로 새 커밋, 이후 최신 HEAD 재검증.
9. 기존 v1~v51 보존. 1-2-A 및 1-2 진행 중, 완료율 미산정. **1-1 승인 150/150 완료 / 상위 1/5 완료** 유지, 마인크래프트 실제 가구 모델링·PZ 변환 금지.
