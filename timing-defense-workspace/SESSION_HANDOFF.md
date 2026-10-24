# Timing Defense — Session Handoff

Updated: 2026-10-24 KST

## 0. Recovery rule — mandatory
Always fetch live remote first. Never reconstruct current state from chat, memory, copied SHA, or an old handoff paragraph. Live GitHub canonical state wins.

The user must not have to re-explain project state, dependency ordering or reasoning method.

---

# 1. Mandatory read/check order
1. live `timing-defense-workspace` HEAD
2. `PROJECT_STATUS.md`
3. `NEXT_WORK.md`
4. active `legacy-game-structure/data/system_dependency_calibration_order_v0_41.yaml`
5. `legacy-game-structure/138_SESSION_BOOTSTRAP_COGNITIVE_REVIEW_AMENDMENT_V0_1.md`
6. `legacy-game-structure/70_SYSTEM_DEPENDENCY_AND_CALIBRATION_ORDER_REVIEW_V0_1.md`
7. `legacy-game-structure/156_P6_STRUCTURAL_CLOSURE_WITH_WATCHES_V0_1.md`
8. `legacy-game-structure/157_TIER_STRUCTURE_AND_MONSTER_AVAILABILITY_CANDIDATE_REVIEW_V0_1.md`
9. Tier authority as needed: `02`, `03`, `04`, `16`, `19`, `21`, `22`, `25`, `31`, `45`
10. current production/harness heads
11. only then exact evidence for the user-approved next unit

Do not rerun closed work merely because a new session started.

---

# 2. Mandatory cognition sequence

```text
Tier / Stage purpose
-> monster availability / novelty
-> encounter family / composition / formation / chronology / geometry
-> class identity / radar promise
-> skill state
-> run-state persistence
-> mastery / judgment model
-> shop/economy
-> timing-action count / EXP / skill-reach feedback
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

Campaign-authoring order:

```text
Tier availability
-> monster vocabulary
-> encounter-family availability
-> class-opportunity envelope
-> exact Stage composition
```

---

# 3. Approval rule
Important design/content/numerical/work-boundary/methodology/phase decisions must not be silently applied.

Approval is required before:
- adopting exact Tier count;
- adopting monster availability/unlock ladder;
- adopting exact Tier1 roster;
- exact Tier1 Stage1-50 authoring;
- class buff/nerf;
- P×P/judgment probability change;
- shop numerical freeze;
- EXP rule change;
- new monster adoption;
- production gameplay change.

P6 structural closure is already user-approved and must not be reopened without a concrete contradiction/new-source trigger.

---

# 4. Branch checkpoints

Planning/canonical:
- `timing-defense-workspace`
- always re-fetch live HEAD

Production:
- `timing-defense-cloudflare-do-poc`
- verified pre-current-work HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- gameplay/numerical changes unauthorized

Calibration harness:
- `timing-defense-skilled-v2-harness-v01`
- verified pre-current-work HEAD `063a9ac9986ba9a8028beb31a5b4c733c9bfa863`

P6-B2 fresh-forward temp:
- `timing-defense-workspace-temp-p6-b2-fresh-forward`
- final head `5093a151142090d58c0e1d26f52cdbee43653542`
- planning/diagnostic evidence only
- do not promote automatically

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
P5->P6 fidelity bridge = EXACT TEMP PASS
P6 = USER_APPROVED STRUCTURAL CLOSED WITH WATCHES
Tier structure / monster availability candidate review = COMPLETE
CURRENT = USER DECISION ON TIER PACKAGE
exact Tier count = OPEN
exact monster availability/unlock ladder = OPEN
exact Tier1 roster = OPEN
Tier1 Stage1-50 authoring = NOT STARTED
production = UNCHANGED / UNAUTHORIZED
```

---

# 6. P6 closure — preserve exactly

Source:
`156_P6_STRUCTURAL_CLOSURE_WITH_WATCHES_V0_1.md`

Closure means causal structure is sufficiently converged for the next campaign constraint layer.
It does not mean numerical convergence.

Preserve:
- encounter-family rotation is material;
- one late class ranking is not universal power ranking;
- Tank is control/defense/objective-protection specialist and does not need kill parity;
- shop ATK can reduce same-stage timing opportunity but increase total opportunity by preventing failure;
- pure per-root-action provisional EXP creates class progression divergence pressure;
- fresh-forward magnitude is watched, not production-authoritative;
- final EXP semantics remain OPEN and route to P10R.

Active watches:
```text
FRESH_FORWARD_ABSOLUTE_MAGNITUDE_WATCH
TANK_CONTROL_DEFENSE_TO_OBJECTIVE_PROTECTION_WATCH
TEMP_BRANCH_PUSH_TRIGGERS_HARNESS_CLOUDFLARE_BUILD_WATCH
```

---

# 7. Tier candidate review — current decision package

Source:
`157_TIER_STRUCTURE_AND_MONSTER_AVAILABILITY_CANDIDATE_REVIEW_V0_1.md`

## A — Compact 4 Tier — RECOMMENDED / NOT ADOPTED
```text
T1 G/R/B
T2 +SH/F
T3 +C/SP
T4 +SUP/SI
T5+ future expansion
```

Reasons:
- novelty density `3/2/2/2` is strong;
- class-role audit already shows five-class opportunities can be authored;
- 4 Tiers already create 20 class×Tier records / 1000 successful Stage floor / 60 max stars before retries;
- P6 found no structural reason requiring a fifth Tier;
- T4 SUPPORTER+SIEGER risk is a WATCH, not FAIL.

T4 guardrail:
```text
SUPPORTER isolated teach/mix
-> SIEGER isolated teach/mix
-> combined support/siege later
-> no first teach in Stage41-50
```

## B — Split 5 Tier — VALID FALLBACK / NOT ADOPTED
```text
T1 G/R/B
T2 +SH/F
T3 +C/SP
T4 +SUP
T5 +SI
```
Use if combined T4 later fails readability/role-expression.

## C — Extended 6 Tier — STRUCTURALLY POSSIBLE / NOT RECOMMENDED CURRENTLY
Current roster would become `3/2/1/1/1/1`, adding large campaign/meta volume with thin late novelty.

---

# 8. Tier1 roster candidate

Preferred, not adopted:
```text
GRUNT / RUNNER / BRUTE
```

Why:
- baseline + tempo + durability are clean foundational problems;
- five-class opportunity can be generated by formation/cadence/geometry;
- avoids advanced stateful/backline mechanics during onboarding;
- preserves six current monsters as later-Tier novelty.

`G/R` alone is too narrow as current default.
`G/R/B/SH` spends too much onboarding novelty and weakens T2.

---

# 9. Current user decision gate

Ask/resolve only this package:

```text
Initial Tier count = 4
T1 = GRUNT / RUNNER / BRUTE
T2 adds SHIELD / FLYER
T3 adds CHARGER / SPLITTER
T4 adds SUPPORTER / SIEGER
T5+ reserved for future monster expansion
```

If approved:
next work is **Tier identity / novelty budget / encounter-family availability / introduction-window / class-opportunity / role-expression constraints**.

Do not jump straight to exact Stage1-50.

If rejected:
identify the rejected dimension and compare only that dimension to B/C or another bounded alternative.
Do not reopen P6 by default.

---

# 10. Fixed guards

```text
LIVE REMOTE WINS
NO REPEAT OF CLOSED PROBES WITHOUT TRIGGER
P6 CLOSED WITH WATCHES
NO EXACT TIER/ROSTER ADOPTION WITHOUT USER APPROVAL
MONSTER AVAILABILITY BEFORE EXACT STAGE COMPOSITION
NO EXACT STAGE1-50 AUTHORING YET
NO HARD CLASS LOCKOUT
SURVIVAL != CLEAR
TANK LOW REMOVAL IS INTENTIONAL
NO FLAT SHOP->EXP MULTIPLIER
FINAL EXP ROUTING = P10R
NO P×P PATCH TO FIT CONTENT
NO PRODUCTION GAMEPLAY CHANGE WITHOUT APPROVAL
```

---

# 11. Session-close quality gate
Before handoff:
1. re-fetch live canonical HEAD;
2. verify production/harness unchanged unless explicitly authorized;
3. separate evidence from adopted semantics/values;
4. keep active plan/status/next/handoff synchronized;
5. explain simply before technical detail;
6. stop at current user decision gate.
