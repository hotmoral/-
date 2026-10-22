# Timing Defense — Structure Consistency Governance

Date: 2026-10-22 KST  
Status: **CORPUS GOVERNANCE / REQUIRED FOR EVERY STRUCTURAL CHANGE**

## 0. 목적

레거시 구조자료의 목표는 문서를 많이 만드는 것이 아니라, 최종 게임의 상위 구조를 구현 전에 충분히 닫아 **싸게 발견할 수 있는 구조 결함을 코드·밸런스 패치 단계까지 끌고 가지 않는 것**이다.

본질은 다음 한 문장이다.

> 직업별 독립 Tier 진행과 계정 공용 별 성장 위에서, 50 Stage의 전투가 9종 몬스터와 클래스 역할을 이용해 읽을 수 있고 반복 가능하며 확장 가능한 난이도 곡선을 만들고, 이를 deterministic simulation으로 검증한 뒤에만 live 구현으로 승격한다.

이 문서는 위 본질에서 벗어나는 작업을 막는 governance다.

---

# 1. Source priority

구조 충돌 시 우선순위:

1. `CURRENT_FROZEN_STRUCTURE`
2. `USER_CONFIRMED_STRUCTURE`
3. 사용자 확정 구조에서 논리적으로 필수인 `DERIVED_INVARIANT`
4. `CURRENT_AUTHORITATIVE`
5. `LEGACY_IMPLEMENTED_REFERENCE`
6. `LEGACY_ANALYSIS_REFERENCE`
7. `OPEN_DECISION`
8. `SUPERSEDED`

주의:
- CURRENT_AUTHORITATIVE code가 오래된 campaign 구조를 구현하고 있어도, 현재 frozen/user-confirmed 상위 구조와 충돌하면 production campaign 설계에서는 상위 구조가 우선한다.
- 단, live 동작을 설명할 때는 실제 source authority를 왜곡하지 않는다.
- 수치는 별도 explicit freeze가 없으면 production authority로 승격하지 않는다.

## 공통 상태 enum

Corpus에서 허용하는 상태명:
- `CURRENT_FROZEN_STRUCTURE`
- `CURRENT_AUTHORITATIVE`
- `USER_CONFIRMED_STRUCTURE`
- `DERIVED_INVARIANT`
- `LEGACY_IMPLEMENTED_REFERENCE`
- `LEGACY_ANALYSIS_REFERENCE`
- `DESIGNED_NOT_AUTHORITATIVE`
- `OPEN_DECISION`
- `SUPERSEDED`

문서마다 임의의 유사 상태명을 만들지 않는다.

---

# 2. Dependency order

구조 작업은 아래 순서를 기본 dependency로 사용한다.

```text
A. Core product premise
   ↓
B. Meta progression
   ↓
C. Tier structure
   ↓
D. 50-Stage pacing
   ↓
E. Encounter taxonomy / monster roster
   ↓
F. Authoring data
   ↓
G. Run progression (EXP / skill / coin / shop)
   ↓
H. Team scaling / multiplayer progression
   ↓
I. Deterministic simulation
   ↓
J. Explicit freeze
   ↓
K. Live implementation
```

후행 계층이 선행 계층의 의도를 몰래 바꾸면 안 된다.
예:
- simulation 편의를 위해 별 경계를 바꾸지 않는다.
- 기존 shop 구현 때문에 50 Stage마다 shop을 자동 강제하지 않는다.
- 기존 S/E/X simulator가 있다는 이유로 신규 9종 taxonomy를 S/E/X에 맞추지 않는다.

---

# 3. Required review lenses

각 구조 변경마다 최소 다음 관점으로 검토한다.

## 3.1 Product-purpose lens
- 이 변경이 게임의 본질과 직접 연결되는가?
- 단순 시스템 추가 자체가 목적이 되어 있지 않은가?
- 플레이어가 실제로 체감하는 선택/진행/전투 문제를 개선하는가?

## 3.2 Internal-consistency lens
- 같은 용어가 다른 문서에서 다른 의미로 사용되지 않는가?
- 범위/경계/off-by-one이 모순되지 않는가?
- derived data와 stored data가 중복되어 drift할 여지가 없는가?

## 3.3 Cross-category lens
- Meta progression 변경이 Tier 난이도에 미치는 영향은?
- Tier 변경이 Stage/Encounter 빈도에 미치는 영향은?
- Encounter 변경이 class opportunity와 target order에 미치는 영향은?
- EXP/skill/shop 변경이 late-stage calibration을 무효화하지 않는가?
- multiplayer scaling이 solo progression 규칙을 왜곡하지 않는가?

## 3.4 Player-experience lens
- 신규 mechanic이 학습되기 전에 시험되고 있지 않은가?
- 반복 플레이에서 tutorial/저난도 구간이 과도하게 길지 않은가?
- 20/40/50 별 경계가 보상 cliff를 만들지 않는가?
- 난이도가 숫자 증가만으로 체감되지 않는가?

## 3.5 Combat-system lens
- free manual targeting을 가정하지 않는가?
- frontmost target order와 실제 formation이 일치하는가?
- penetration/AoE를 필수 해법으로 강제해 hard class lockout을 만들지 않는가?
- 9종 capability contract를 침범하지 않는가?

## 3.6 Economy/progression lens
- 영구 stat snowball이 과도하지 않은가?
- first-class와 later-class 난이도 차이가 허용 범위인가?
- run coin/shop 성장과 permanent growth가 곱연산 폭주를 만들지 않는가?
- 특정 class가 crit/knock/damage 등 공용 stat에서 과도하게 이득 보지 않는가?

## 3.7 Multiplayer lens
- 2/3/4인 scaling이 단순 HP inflation으로 퇴행하지 않는가?
- 서로 다른 Tier unlock 상태의 플레이어가 만났을 때 progression exploit이 생기지 않는가?
- 별 획득 귀속 규칙과 host Tier 선택 규칙이 충돌하지 않는가?

## 3.8 Implementation/authority lens
- 구조자료가 live에 이미 구현됐다고 오해될 표현이 없는가?
- legacy source의 수치를 production freeze처럼 쓰지 않는가?
- server-authoritative이어야 할 상태를 client authoring metadata로 결정하려 하지 않는가?

## 3.9 Simulation lens
- 결과를 재현할 수 있는가?
- 특정 평균값 하나로 구조 결함을 숨기지 않는가?
- fail histogram, tail risk, class variance, path dependence를 함께 보는가?

## 3.10 Scope/cost lens
- 지금 결정할 필요가 없는 문제까지 확장하고 있지 않은가?
- 이미 닫힌 문제를 근거 없이 반복 재검토하고 있지 않은가?
- 다음 의존 계층에 필요한 만큼만 정확하게 닫고 있는가?

---

# 4. Cross-category decision gates

다음 항목은 한 문서에서 단독 결정 금지.

## Gate G1 — Tier unlock
연동:
- Meta progression
- Lobby Tier selector
- Multiplayer eligibility
- Star acquisition
- permanent progression pacing

## Gate G2 — Permanent stat reward ladder
연동:
- max Tier count
- max stars
- first/fifth class difficulty
- run upgrade economy
- class coefficient sensitivity

## Gate G3 — Shop cadence
연동:
- Stage duration
- 50-stage run length
- run coin income
- run upgrade curve
- multiplayer READY/NEXT friction
- reconnect state

## Gate G4 — Skill reach / EXP curve
연동:
- 50-stage pacing
- Lv11/16/21 parity
- Lv26/31 contract
- monster difficulty
- class opportunity

## Gate G5 — Boss/checkpoint policy
연동:
- Stage 10/20/30/40/50 pacing
- star boundary
- ordinary encounter frequency
- boss capability composition
- run reward cadence

## Gate G6 — Multiplayer Tier progression
연동:
- host/join eligibility
- star credit
- selected class record
- AI fill
- difficulty scaling
- carry/boost exploit

---

# 5. Resolved structural ambiguities from first cross-audit

## 5.1 Design band vs star reward band
둘은 분리한다.

### Design bands
- Teach 1-9
- Checkpoint 10
- Expand 11-19
- Synthesis A 20-29
- Checkpoint 30
- Escalate 31-39
- Final Examination 40-49
- Final 50

### Reward bands
- fail on Stage 1-19 -> 0★
- fail on Stage 20-39 -> 1★
- fail on Stage 40-49 -> 2★
- clear Stage 50 -> 3★

Stage 30은 design checkpoint이지만 reward상 1★ 구간이다.
Stage 40-49는 design final-examination이면서 reward상 2★ 구간이다.

두 분류를 같은 enum으로 저장하지 않는다.

## 5.2 Star computation
정확한 입력은 `attempt outcome`이다.

```text
if tierCleared(Stage50): 3
else if failedStage >= 40: 2
else if failedStage >= 20: 1
else: 0
```

`bestStars[class][tier] = max(previous, attemptStars)`는 사용자 확정 구조에서 파생되는 `DERIVED_INVARIANT`다.
별 중복 파밍을 허용하지 않는다.

## 5.3 New mechanic introduction
Stage 40-49는 final-examination band이므로, Tier의 핵심 ordinary-monster capability를 **처음** 소개하는 구간으로 사용하지 않는 것을 기본 guardrail로 한다.
예외가 필요하면 명시적 authoring justification이 있어야 한다.

## 5.4 Target-order terminology
`FRONT/MID/BACK`은 고정 aggro slot이 아니다.
실제 target authority는 runtime X/validity 규칙을 따른다.
Formation depth는 예상/의도된 arrival and screening order를 표현하는 authoring metadata다.

---

# 6. Change protocol

구조 변경 하나마다 다음 기록을 남긴다.

```text
CHANGE
- problem
- proposed structural change
- source/status
- direct dependencies
- downstream dependencies
- contradictions checked
- simulation needed
- unresolved decisions
- live-code impact: none | future | authorized
```

## 숫자 변경
숫자는 다음 순서 없이는 live에 반영하지 않는다.

```text
candidate data
 -> deterministic simulation
 -> failure classification
 -> sensitivity check
 -> report
 -> user/product decision
 -> production freeze
 -> implementation
```

---

# 7. Handoff discipline

새 세션은 memory나 직전 채팅을 canonical로 간주하지 않는다.

필수 복구 순서:
1. live `timing-defense-workspace` HEAD 확인
2. `SESSION_HANDOFF.md`
3. `PROJECT_STATUS.md`
4. `NEXT_WORK.md`
5. `legacy-game-structure/README.md`
6. 본 governance
7. 현재 active 구조문서
8. 필요한 source evidence

Handoff에는 최소 다음을 기록한다.
- current canonical HEAD
- last validated executable checkpoint
- active structure tranche
- closed decisions
- open decisions
- candidate-only values
- exact next boundary
- files modified in tranche
- whether live code/numbers changed

작업 그룹이 끝날 때 위 항목을 canonical handoff에 동기화한다.

---

# 8. Stop conditions

다음 상황이면 다음 계층으로 진행하지 않는다.
- 같은 핵심 개념의 정의가 문서 간 불일치
- star/Tier/Stage boundary off-by-one ambiguity
- authoring schema가 구조문서의 필드를 표현하지 못함
- 새로운 encounter가 기존 archetype과 실제 tactical question이 동일함
- simulation에서 결과 재현 불가
- candidate와 frozen 값의 구분 불명확
- live 구현이 아직 product decision을 필요로 하는 상태

---

# 9. 현재 exact next boundary

1. 첫 cross-document inconsistency를 schema/document에 반영
2. Tier ladder candidate를 구조 수준에서 작성
3. T1의 9종 introduction/readiness rule을 정의
4. Tier별 pressure/archetype frequency를 아직 exact production 숫자가 아닌 candidate envelope로 작성
5. 이후 exact candidate dataset을 생성하여 first simulation tranche로 이동

이 순서를 벗어나 Lv11+ live 구현이나 production monster numeric patch로 이동하지 않는다.
