# Timing Defense — Session Handoff

Updated: 2026-10-24 KST

## 0. Recovery rule — mandatory
Always fetch the live remote first. Never reconstruct current state from chat, memory, copied SHA, or an old handoff paragraph. Live GitHub canonical state wins.

The user must not have to re-explain the factual project state, dependency ordering or reasoning method.

---

# 1. Mandatory read/check order
1. live `timing-defense-workspace` HEAD
2. `PROJECT_STATUS.md`
3. `NEXT_WORK.md`
4. active `legacy-game-structure/data/system_dependency_calibration_order_v0_37.yaml`
5. `legacy-game-structure/138_SESSION_BOOTSTRAP_COGNITIVE_REVIEW_AMENDMENT_V0_1.md`
6. `legacy-game-structure/70_SYSTEM_DEPENDENCY_AND_CALIBRATION_ORDER_REVIEW_V0_1.md`
7. `CHARACTER_PROFILE_RADAR_V1.md`
8. `legacy-game-structure/72_RUN_STATE_LIFECYCLE_APPROVED_CONTRACT_V0_1.md`
9. P4 progression chain: `79`, `81`, `85`, `111`
10. P5 shop chain: `116`, `118`, `119`, `123`, `124`
11. `legacy-game-structure/144_P5_P6_PERSISTENT_STATE_FIDELITY_BRIDGE_RESULT_V0_1.md`
12. `legacy-game-structure/147_ENCOUNTER_COMPOSITION_CLASS_RESPONSE_MATRIX_V0_1.md`
13. `legacy-game-structure/149_P6_FORMAL_ENTRY_AND_FIRST_CAUSAL_SLICE_AUTHORIZATION_V0_1.md`
14. `legacy-game-structure/150_P6_STAGE46_47_FIRST_CAUSAL_CONVERGENCE_RESULT_V0_1.md`
15. `legacy-game-structure/151_P6_ENCOUNTER_FAMILY_ROTATION_AND_TANK_OBJECTIVE_ATTRIBUTION_RESULT_V0_1.md`
16. **latest:** `legacy-game-structure/152_P6_SHOP_ATK_EXP_OPPORTUNITY_BIDIRECTIONAL_FEEDBACK_RESULT_V0_1.md`
17. current production/harness heads
18. only then exact source/evidence for the user-approved next unit

Do not rerun closed work merely because a new chat/session started.

---

# 2. Mandatory cognition sequence

```text
Tier / Stage purpose
-> monster availability / novelty
-> encounter family / composition / formation / chronology / geometry
-> class identity / player-facing radar promise
-> skill state
-> run-state persistence
-> mastery / judgment model
-> shop/economy
-> attack count / EXP / skill-reach feedback
-> target order / objective pressure
-> STAGE_SETTLED / wall carry
-> later-stage consequences
-> Tier unlock / meta / multiplayer impact
```

Root-cause order:

```text
source/simulator fidelity
-> lifecycle/state
-> encounter composition/geometry/chronology
-> class/package semantics
-> shop/feedback
-> exact scalar last
```

Use the smallest bounded probe that distinguishes the cause. Deep review does not mean repeating closed work.

---

# 3. Approval rule
Important design/content/numerical/work-boundary decisions must not be silently applied.

Approval is required before:
- adopting a new P6-B2 progression propagation methodology;
- changing exact Stage pressure/content;
- class buff/nerf;
- P×P/judgment probability change;
- shop numerical freeze;
- EXP rule change;
- selecting/adopting Tier count or monster availability/unlock ladder;
- exact Tier1 roster / Stage1-50 authoring;
- armored/hardened/new-monster adoption;
- Stage48/49 packet adoption;
- production gameplay change.

Diagnostic/instrumentation/fidelity work may proceed independently if gameplay semantics are unchanged.

---

# 4. Branch checkpoints

Planning/canonical:
- `timing-defense-workspace`
- always re-fetch live HEAD

Production:
- `timing-defense-cloudflare-do-poc`
- last verified `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- v0.45 SIEGER FULL PASS
- gameplay/numerical changes unauthorized

Calibration harness:
- `timing-defense-skilled-v2-harness-v01`
- last verified `063a9ac9986ba9a8028beb31a5b4c733c9bfa863`

P6-B1 temp branch:
- `timing-defense-workspace-temp-p6-shop-exp-opportunity`
- latest known temp HEAD `7d83360da97cf0add2256c0b391d1dac7e9cd9a6`
- no planning/production authority
- do not promote temp runner/workflows automatically

P6 fidelity temp base:
- `timing-defense-workspace-temp-p5p6-fidelity`
- latest relevant base `0c334efed0af8ddcdef4eb93c34146ecfa7dadf5`

Other temp branches remain historical diagnostic evidence only.

---

# 5. Current exact phase

```text
P0 = PASS_WITH_WATCHES
P1 = USER_APPROVED_STRUCTURAL_COMPLETE
P2 = USER_APPROVED_STRUCTURAL_COMPLETE
P3 = STRUCTURAL_PASS_COMPLETE
P4 = PROVISIONAL_STRUCTURAL_COMPLETE_WITH_WATCHES
P5 A2 shop = USER APPROVED
P5 class identity group = DIRECTIONALLY CLOSED
P5 mastery reinterpretation = COMPLETE
P5->P6 fidelity bridge = EXACT TEMP PASS
entry charge/combo primary-cause checks = CLOSED
Stage48 local tuning = PAUSED
P6 = FORMALLY ENTERED / USER APPROVED
P6-S1 = COMPLETE
P6-A encounter-family convergence = COMPLETE
P6-B1 shop ATK -> EXP opportunity attribution = COMPLETE
CURRENT = P6-B2 PROGRESSION PROPAGATION METHOD DECISION GATE
Tier count / exact monster unlock ladder / exact T1 roster = DEFERRED UNTIL P6 CONVERGENCE
Tier1 Stage1-50 authoring = NOT STARTED
production = UNCHANGED / UNAUTHORIZED
```

---

# 6. User-approved campaign/P6 ordering
The user explicitly chose:

```text
P6 convergence first
-> then use P6 evidence to constrain Tier structure / monster unlock order
-> then author actual Tier1 Stage1-50 according to Tier availability rules
```

Do not return to exact Tier/unlock authoring before P6 is resolved unless the user changes direction.

Stable campaign philosophy:
- T1 starts with a limited monster subset;
- higher Tiers add new roles;
- returning monsters gain new composition/formation/cadence meanings;
- current monsters + temporary armored proxy are diagnostic vocabulary, not final T1 roster.

---

# 7. Player-facing class identity — preserve

Approved radar:

```text
Knight  ATK4 CRIT2 AGI3 KNOCK3 PEN4 AOE2
Rogue   ATK2 CRIT5 AGI5 KNOCK1 PEN1 AOE1
Tank    ATK2 CRIT1 AGI1 KNOCK5 PEN1 AOE3
Archer  ATK3 CRIT2 AGI4 KNOCK1 PEN5 AOE2
Mage    ATK4 CRIT2 AGI2 KNOCK1 PEN1 AOE5
```

Critical newest user clarification:

```text
Tank does not need to kill monsters well.
Tank's role is control / defense / wall protection.
If that role functions, low removal is sufficient/intentional.
```

Therefore:
- low Tank removal alone is NOT a defect;
- Tank clear-rate parity is NOT required;
- do not propose a Tank ATK buff from dense-wave results;
- active watch is only `TANK_CONTROL_DEFENSE_TO_OBJECTIVE_PROTECTION_WATCH`.

P6-A evidence already shows Tank push, barriers, Aftershock slow and Iron Wall materially reduce wall pressure.

Keep `SURVIVAL != CLEAR`.

---

# 8. User difficulty interpretation — preserve
The user considers current central-skilled late-segment completion around the mid-40% range plausibly appropriate when all-PERFECT retains a clear path.

Therefore:
```text
DO NOT default to raising global skilled completion.
DO NOT infer class scalar imbalance from one specialty-biased encounter family.
```

No exact percentage is frozen.

---

# 9. Closed P6-A finding

20-seed central-skilled outcome by encounter family:

```text
BASELINE dense/aligned
Mage 19 / Archer 19 / Rogue 9 / Knight 7 / Tank 2

durable/distributed
Knight 20 / Mage 20 / Archer 20 / Rogue 17 / Tank 3

screened CHARGER
Knight 20 / Archer 20 / Rogue 18 / Mage 18 / Tank 3
```

Conclusion:

```text
CLASS_RANKING_IS_ENCOUNTER_FAMILY_DEPENDENT
CURRENT_DENSE_CLASS_ORDER != UNIVERSAL_CLASS_POWER_ORDER
```

Tank component attribution:
- Aftershock center mismatch corrected: non-primary;
- no push worsens wall loss;
- no barrier worsens wall loss;
- no Lv31 barrier worsens wall loss;
- no Aftershock slow worsens wall loss;
- no Iron Wall worsens wall loss;
- shockwave `0.20/0.25/0.30` does not materially change completion boundary.

Interpret with the radar identity above, not as a damage-balance defect.

---

# 10. Closed P6-B1 finding

Purpose:
measure the incremental late-run shop-ATK effect on actual timing-action opportunity and provisional XP_CREDIT without inventing a flat conversion formula.

Execution:

```text
run 40029402035
job 120673610122
exact-byte repeat PASS
SHA256 83b5e1630231fb38426ae878cd3f2b6e7f3cd99894a44bac8416d0f23d614788
```

Cumulative summary:

```text
run 40029618307
job 120674332432
SUCCESS
```

Paired design:

```text
20 SKILLED_V2_CENTRAL seeds × 5 classes × ATK_OFF/ATK_ON
+ all-PERFECT controls
Stage46-49
BALANCED FORT/DEF fixed
ATK component only
Heavy X+Y = one root-action EXP award
```

Skilled through49:

```text
ATK_OFF 17/100
ATK_ON  48/100
survival promotions 31
regressions 0
```

Clean cumulative same-path cohort, both variants through49:

```text
17 pairs
root actions ~-4.19%
provisional XP_CREDIT ~-3.89%
```

Survival-promotion cohort:

```text
31 pairs
root actions ~+68.66%
provisional XP_CREDIT ~+70.38%
```

Causal result:

```text
shop ATK
├─ faster same-stage removal -> fewer timing actions -> less EXP opportunity
└─ improved survival/progression -> later-stage access -> more total EXP opportunity
```

Therefore:

```text
SHOP_ATK_TO_EXP_FEEDBACK = BIDIRECTIONAL / OUTCOME-CONDITIONED
```

Never reduce this to:
```text
more shop power = always less EXP
```

Do not project late-run ~4% clean compression across Stage1-45.
Do not map nominal ATK% linearly to action-count reduction.

---

# 11. P4 historical reproducibility audit

P4-B result data commit:
```text
c32dfd9dd45eaeec01ab53ea0cdafc3fd6233c7c
```

Historical canonical tree contains:
- P4-B result JSON;
- P4-A runner + validator;
- P3 kernel;
- older combat/role simulators.

It does **not** contain a dedicated reproducible P4-B propagation runner.
The next commit added the report only.

Therefore exact Lv31 reach cannot be reconstructed by guessing the missing model from result tables.

---

# 12. Current P6-B2 decision gate

Goal:

```text
Stage1-45
shop history
× skill power
× combat opportunity
× EXP
× skill-reach timing
```

must be estimated with a bounded reproducible method before exact Tier1 authoring if P6 progression convergence is to close now.

### A — recommended
Rebuild a bounded P4-B-style synthetic combat-feedback runner, then inject P5 stage-by-stage shop trajectories.

Required safeguards if approved:
1. write a reconstruction/fidelity contract first;
2. reproduce old P4-B known anchors before new shop conclusions;
3. use current authoritative skill semantics where available;
4. use actual simulated timing-action counts, not a flat multiplier;
5. preserve SKILLED_V2 and Heavy-one-award EXP semantics;
6. inject actual P5 diagnostic stage-by-stage shop trajectories;
7. classify survival-extension separately from within-stage self-damping;
8. no final EXP/shop numeric freeze;
9. stop before Tier/unlock or exact T1 authoring.

### B — not recommended now
Build provisional full Stage1-50 combat fixture first.
More direct, but risks pre-empting approved dependency order and effectively authoring T1 too early.

### C — not recommended unless user wants to defer
Carry the feedback watch forward until later exact authoring.
No synthetic assumption, but P6 progression convergence remains open.

**No B2 method is adopted yet. User approval is required.**

---

# 13. Fixed guards

```text
LIVE REMOTE WINS
P6 FORMAL ENTRY IS APPROVED
SKILLED_V2_CENTRAL STAYS FIXED FOR CURRENT DIAGNOSTICS
HEAVY X+Y = ONE EXP AWARD
STAGE_SETTLED REQUIRED
WALL DEFICIT / COMBO / CHARGE PERSIST
NO MID-FIELD POP-IN
SURVIVAL != CLEAR
NO HARD CLASS LOCKOUT
TANK LOW REMOVAL IS INTENTIONAL
NO TANK DAMAGE BUFF FROM CLEAR-RATE EQUALITY PRESSURE
NO FLAT SHOP->EXP MULTIPLIER
NO LINEAR STAGE1-45 PROJECTION FROM LATE B1 RESULT
NO P×P PROBABILITY PATCH TO FIT CONTENT
NO ARMORED PROXY ADOPTION
NO EXACT TIER1 ROSTER/UNLOCK ASSUMPTION
NO PRODUCTION GAMEPLAY CHANGE WITHOUT APPROVAL
```

---

# 14. Session-close quality gate
Before handoff:
1. re-fetch live canonical HEAD;
2. verify production/harness unchanged unless explicitly authorized;
3. separate evidence from adopted semantics/values;
4. sync status/next/handoff/active dependency plan when boundary changes;
5. do not repeat closed P6-A/B1 without source/simulator trigger;
6. explain simply before technical detail;
7. stop at the current user decision gate.