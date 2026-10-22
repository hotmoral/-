# Timing Defense — Legacy Evidence Map

Date: 2026-10-22 KST  
Status: **EVIDENCE INDEX / NO NUMERICAL AUTHORIZATION**

## 1. 목적

레거시 구조자료가 과거 문서/코드/현재 contract를 혼동하지 않도록, 주요 근거의 상태와 사용 범위를 정리한다.

## 2. 현재 구조 권위

### MONSTER_CAPABILITY_CONTRACT_V1.md
Status: `CURRENT_FROZEN_STRUCTURE`

사용:
- 9종 ordinary roster
- 각 archetype의 primary role/state-machine
- no hard class lockout
- no manual-target assumption
- server authority requirement

사용하지 않음:
- production HP/speed/reward 수치 freeze
- final Tier introduction point
- final Stage composition

### PLAYER_SKILL_AUTHORITY_REVIEW_2026-10-22.md
Status: mixed authority map

- Lv6: `CURRENT_FROZEN_STRUCTURE + CURRENT_AUTHORITATIVE`
- Lv11/16/21: `LEGACY_IMPLEMENTED_REFERENCE` / exact parity candidate
- Lv26: `DESIGNED_NOT_AUTHORITATIVE`
- Lv31: `OPEN_DECISION`

50-stage late calibration 시 skill reach와 결합해서 다시 검토해야 한다.

### DESIGN_DECISIONS.md
Status: current design direction

유효 구조:
- timing-primary input
- visible target / target-wait integrity
- class role identities
- pregame flow
- lobby settings direction
- Stage intro

기존 S/E/X section은 이 corpus에서 production encounter taxonomy로는 superseded 처리한다.

## 3. 사용자 직접 확정 구조 — 2026-10-22

Status: `USER_CONFIRMED_STRUCTURE`

### 독립 class Tier progression
각 직업이 별도로 Tier를 깨 나감.

### 50 Stage Tier star result
- fail 1~19 = 0★
- fail 20~39 = 1★
- fail 40~49 = 2★
- clear 50 = 3★

### 별 합산과 공용 영구 성장
- `직업 x Tier` 최대 3★
- 5직업이 T1 모두 3★면 총 15★
- 누적 별 수에 따라 모든 직업 공용 permanent stat 자동 획득

현재 live canonical 문서에서 이 구조가 명시적으로 정리되어 있지 않았으므로 본 corpus에서 최초 구조화한다.

## 4. Legacy implemented flow

### v0.20 / V020_IMPLEMENTATION_REPORT.md
Status: `LEGACY_IMPLEMENTED_REFERENCE`

유효 근거:
- Stage intro
- visible-target turn gating
- no empty-turn EXP
- active turn completion integrity
- target-wait does not break combo

### v0.22 / V022_LOBBY_IMPLEMENTATION_REPORT.md
Status: `LEGACY_IMPLEMENTED_REFERENCE`

유효 근거:
- nickname -> class -> play setting -> run/team waiting
- five classes
- SOLO/TEAM, AI, TEAM method, Tier UI

한계:
- 당시 Tier는 사실상 Tier1 prototype UI
- per-class Tier progression 저장 구조는 확인되지 않음

### v0.31~v0.35 multiplayer reports/source
Status: `LEGACY_IMPLEMENTED_REFERENCE` + 일부 current architecture predecessor

유효 근거:
- room create/join
- P1~P4
- READY/host START
- reconnect session recovery
- authoritative shared combat evolution
- Stage clear -> team shop -> READY/NEXT -> next Stage

### V035_RECONNECT_SHOP_STAGE2_REPORT.md
특히 다음이 실제 구현 reference:
- Stage1 clear -> shop
- per-human coin/upgrades server authority
- all-human READY
- host NEXT STAGE
- Stage2 synchronized start

그러나 50-stage production에서 shop이 매 Stage 필요한지는 `OPEN_DECISION`.

## 5. Legacy campaign recipe

### Old Stage 1~10
Status: `SUPERSEDED` as production campaign, retained as regression/history

기존 prototype:
- 10 Stage
- stage별 spawn target/gap
- Stage5/10 boss
- GRUNT/RUNNER/BRUTE/SHIELD/FLYER 점진 혼합

현재 의미:
- 초기 combat feel/reference
- 일부 Stage1~3 regression fixture

현재 의미가 아닌 것:
- final campaign schedule
- final boss cadence
- final Tier length

## 6. TIER_PRESSURE_GRAMMAR_V1.md
Status: `LEGACY_ANALYSIS_REFERENCE`

유효 아이디어:
- 50-stage Tier
- Tier identity
- one/two/three-pattern variation
- timing-window bias
- geometry distribution
- anti-repetition
- higher difficulty != every Stage maximum complexity

현재 superseded 부분:
- S/E/X가 production top-level taxonomy라는 가정
- exact T1~T5 prototype distributions
- exact prototype names/count/order

## 7. PRESSURE_RECIPES_V1.md
Status: `LEGACY_ANALYSIS_REFERENCE`

유효 아이디어:
- 2/3/4-player composition scaling
- short-window density를 readability 핵심 지표로 사용
- global HP inflation보다 composition/event scaling 우선

현재 superseded 부분:
- 5종 roster만 사용
- S/E/X recipe ID
- 당시 exact recipe count를 현재 9종 roster production 값으로 재사용

## 8. v0.16 skill implementation

Status: `LEGACY_IMPLEMENTED_REFERENCE`

유효:
- Lv11/16/21 exact formulas 복구 가능
- current server parity 후보

주의:
- 현재 9종 monster와 50-stage pacing을 고려해 parity 적용 후 재시뮬레이션 필요
- Lv26/31은 자동 복원 대상이 아님

## 9. v0.18 combo/passive

Status: mixed

일부 개념은 이후 current contract/N3로 재검토 또는 재구현됨.
과거 v0.18 전체를 한 덩어리 authority로 취급하지 않는다.

## 10. 현재 가장 큰 canonical gap

이 corpus 작성 전 흩어져 있거나 빠져 있던 상위 구조:
- class-independent Tier progression
- star result and best-star persistence
- GlobalStarTotal
- automatic account-wide permanent stats
- 9-monster production encounter taxonomy
- frontline/screening-aware encounter authoring
- 50 Stage star-boundary pacing
- account progression까지 포함한 simulation plan

## 11. Supersession rule

새 corpus 문서가 과거 분석물을 지운다는 뜻은 아니다.

규칙:
- historical evidence는 보존
- 구조가 충돌하면 현재 frozen contract > user-confirmed current structure > legacy implemented reference > legacy analysis
- 숫자는 별도 explicit freeze 없이는 승격하지 않음
- live implementation truth는 실제 source/server를 다시 검증

## 12. 다음 evidence audit

향후 추가할 항목:
- legacy source의 stage plan 상세
- v022 Tier UI/state exact recovery
- v031~35 lobby/reconnect/shop state machine
- result/retry/end-run flow
- persistence/local storage 범위
- boss prototype behavior
- run reset semantics

추가 audit 결과는 이 index에 상태를 붙여 통합한다.
