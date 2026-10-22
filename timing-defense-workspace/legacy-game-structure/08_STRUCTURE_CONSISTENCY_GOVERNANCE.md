# Timing Defense — Structure Consistency Governance

Date: 2026-10-22 KST  
Status: **CORPUS GOVERNANCE / REQUIRED FOR EVERY STRUCTURAL CHANGE**

## 0. 목적

레거시 구조자료의 목적은 문서를 많이 만드는 것이 아니라, 최종 게임의 상위 구조를 구현 전에 충분히 닫아 싸게 발견 가능한 결함을 코드/밸런스 단계까지 끌고 가지 않는 것이다.

현재 중심 기준:
`16_MASTER_CAMPAIGN_PROGRESSION_SPINE_V0_1.md`

본질:

> 직업별 독립 Tier 진행과 교차 메타 성장 위에서, Tier×50 Stage의 캠페인 진행축이 신규 콘텐츠·player power·soft wall·monster availability를 일관되게 배치하고, deterministic simulation을 통과한 뒤에만 live 구현으로 승격한다.

---

# 1. Source priority

구조 충돌 시:
1. CURRENT_FROZEN_STRUCTURE
2. USER_CONFIRMED_STRUCTURE
3. DERIVED_INVARIANT
4. CURRENT_AUTHORITATIVE
5. LEGACY_IMPLEMENTED_REFERENCE
6. LEGACY_ANALYSIS_REFERENCE
7. OPEN_DECISION
8. SUPERSEDED

추가 상태:
- DESIGNED_NOT_AUTHORITATIVE

주의:
- old live code가 현재 campaign direction과 충돌하면 production design에서는 상위 구조가 우선한다.
- live 동작 설명은 실제 source authority를 따른다.
- explicit freeze 없는 수치는 production authority가 아니다.

---

# 2. Master dependency model

현재는 단순 직선 dependency보다 **Master Campaign Spine 중심 구조**를 사용한다.

```text
A. Core product premise
      ↓
B. MASTER CAMPAIGN PROGRESSION SPINE
      ├─ Tier count / novelty budget
      ├─ Monster availability / unlock ladder
      ├─ 50-Stage macro flow
      ├─ Run player-power windows
      ├─ Star/meta-power windows
      └─ Achievement progression envelope
               ↓
C. Encounter authoring
               ↓
D. Run economy / boss / multiplayer scaling
               ↓
E. Deterministic simulation
               ↓
F. Spine revision / explicit freeze
               ↓
G. Live implementation
```

완전 waterfall도, 무질서한 동시설계도 사용하지 않는다.
전체를 얕게 정렬한 뒤 단계적으로 깊게 내려간다.

후행 계층이 선행 계층을 편의상 바꾸면 안 된다.

예:
- 기존 T1 recipe 때문에 9종 전부를 T1에 넣지 않는다.
- simulator 편의를 위해 star boundary를 바꾸지 않는다.
- 기존 shop 구현 때문에 every-stage shop을 강제하지 않는다.
- old S/E/X tool 때문에 신규 taxonomy를 S/E/X로 되돌리지 않는다.

---

# 3. Required review lenses

모든 구조 변경은 다음 관점으로 검토한다.

## 3.1 Product purpose
- 이 변경이 campaign progression과 실제 플레이 선택에 기여하는가?
- 시스템 추가 자체가 목적이 되지 않았는가?

## 3.2 Internal consistency
- 용어/범위/off-by-one 충돌은 없는가?
- stored vs derived data drift가 없는가?

## 3.3 Cross-category
- Tier가 monster novelty와 맞는가?
- monster unlock이 skill reach와 겹쳐 learning overload를 만들지 않는가?
- star/achievement growth가 intended soft wall을 무력화하지 않는가?
- encounter 변경이 class opportunity/target order와 맞는가?

## 3.4 Player experience / novelty
- 새 Tier가 새로운 경험을 주는가?
- 한 Tier에 novelty가 과밀하지 않은가?
- later Tier가 단순 HP/count inflation으로 퇴행하지 않는가?
- 신규 monster가 학습 전에 고압으로 시험되지 않는가?

## 3.5 Combat truth
- free manual targeting을 가정하지 않는가?
- formation intent와 runtime frontmost target이 맞는가?
- penetration/AoE를 hard requirement로 만들지 않는가?

## 3.6 Difficulty calibration
- intended-entry SKILLED_V2 full-Tier clear rate가 기본적으로 60% 미만인가? (T1 exception 가능)
- clear-rate 기준을 과성장 replay account와 섞지 않았는가?
- class asymmetry를 허용하되 hard lockout은 없는가?

## 3.7 Economy / progression
- stars/achievements/shop/skills가 multiplicative runaway를 만들지 않는가?
- first-class와 later-class 차이가 의도된 soft-wall recovery 범위인가?
- dominant progression route가 생기지 않는가?

## 3.8 Future extensibility
- `monsterCount==9` 같은 하드코딩이 없는가?
- 신규 monster/Tier/taxonomy 추가가 가능한가?
- 현재 9종을 lifetime final roster로 오해하지 않는가?

## 3.9 Multiplayer
- solo spine을 왜곡하지 않는가?
- Tier eligibility/star credit exploit이 없는가?

## 3.10 Authority / implementation
- candidate를 live authority처럼 쓰지 않는가?
- server-authoritative state를 authoring metadata가 재정의하지 않는가?

## 3.11 Simulation
- 결과 재현 가능한가?
- 평균값만 보지 않고 fail histogram/tail/class variance/path dependence를 보는가?

## 3.12 Scope / cost
- 지금 필요 없는 수치까지 정밀화하지 않는가?
- 상위 전제가 열린 상태에서 하위 tuning을 과도하게 하지 않는가?

---

# 4. Cross-category decision gates

## G0 — Master Campaign Spine
연동:
- Tier count
- novelty budget
- monster unlock ladder
- 50-Stage macro flow
- run skill reach
- meta-power states
- difficulty target

G0가 닫히기 전 exact encounter count/cadence 확장은 중단 가능.

## G1 — Tier unlock
연동:
- Meta progression
- Lobby Tier selector
- Multiplayer eligibility
- Stars
- permanent pacing

## G2 — Permanent stat reward ladder
연동:
- Tier count
- max stars
- intended-entry power
- first/later class difficulty
- run economy
- class stat sensitivity

## G3 — Shop cadence
연동:
- Stage duration
- 50-stage run length
- coin income
- upgrade curve
- multiplayer READY/NEXT friction

## G4 — Skill reach / EXP curve
연동:
- 50-stage pacing
- Lv11/16/21 parity
- Lv26/31 contract
- monster difficulty
- novelty budget

## G5 — Boss/checkpoint
연동:
- Tier identity
- Stage macro flow
- star boundaries
- novelty budget
- reward cadence

## G6 — Multiplayer Tier progression
연동:
- eligibility
- star credit
- selected class
- AI fill
- scaling
- carry exploit

## G7 — Achievement reward graph
연동:
- soft-wall map
- star ladder
- class viability
- solo/AI/TEAM rules
- route reachability
- snowball

---

# 5. Resolved structural rules

## 5.1 Design band vs reward band
분리한다.

Reward:
- fail 1-19 -> 0★
- fail 20-39 -> 1★
- fail 40-49 -> 2★
- clear 50 -> 3★

## 5.2 Star computation

```text
if Stage50 clear: 3
else if failedStage >= 40: 2
else if failedStage >= 20: 1
else: 0
```

`bestStars = max(previous, attemptStars)`.

## 5.3 Shared Stage data
같은 Tier/Stage는 class별로 따로 authoring하지 않는다.
Class별 난도 차이는 soft-wall/meta progression 구조로 다룬다.

## 5.4 Monster availability
T1에서 9종 전체를 강제 teaching하지 않는다.
Tier 상승에 따라 신규 monster가 등장하는 것이 current user-confirmed direction이다.
현재 9종은 expandable registry다.

## 5.5 Skilled difficulty
T1 exception을 제외한 일반 Tier의 intended-entry `SKILLED_V2` full-clear probability는 기본적으로 60% 미만을 목표로 한다.
60%는 상한선이며 exact lower target은 Tier별로 추후 결정한다.

## 5.6 Target-order terminology
FRONT/MID/BACK은 aggro override가 아니라 authoring intent다.
Actual target은 runtime authority를 따른다.

---

# 6. Change protocol

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
- live-code impact
```

숫자는:

```text
candidate
 -> deterministic simulation
 -> failure classification
 -> sensitivity check
 -> report
 -> explicit user/product decision
 -> production freeze
 -> implementation
```

---

# 7. Handoff discipline

새 세션 복구:
1. live `timing-defense-workspace` HEAD
2. SESSION_HANDOFF.md
3. PROJECT_STATUS.md
4. NEXT_WORK.md
5. corpus README
6. `16_MASTER_CAMPAIGN_PROGRESSION_SPINE_V0_1.md`
7. 본 governance
8. active structure docs
9. source evidence as needed

Handoff 필수:
- canonical HEAD
- executable checkpoint
- active structure tranche
- closed/user-confirmed decisions
- candidate-only values
- parked/superseded candidates
- exact next boundary
- live-code/numeric change 여부

---

# 8. Stop conditions

다음이면 하위 계층으로 내려가지 않는다.
- Master Campaign Spine 자체가 불일치
- Tier count/monster unlock/skill reach가 서로 설명되지 않음
- 현재 roster를 9종 final로 하드코딩
- intended-entry skilled target 정의 불명확
- star/Tier/Stage boundary ambiguity
- schema가 구조를 표현하지 못함
- simulation nondeterministic
- candidate/frozen 혼동

---

# 9. Current exact next boundary

1. Tier count 4/5/6 비교
2. Tier별 novelty budget
3. 현재 9종 monster unlock ladder candidate
4. future monster expansion contract
5. Tier별 50-Stage macro flow
6. run skill-reach windows
7. meta-power P0/P1/P2/P3
8. SKILLED_V2 clear target envelope
9. Master Campaign Matrix static cross-audit
10. 그 뒤 encounter frequency/count/cadence로 재진입

기존 T1 micro-sim 확장은 이 G0 tranche가 닫힐 때까지 PARKED한다.
