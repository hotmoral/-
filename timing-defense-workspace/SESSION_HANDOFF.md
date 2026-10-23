# Timing Defense — Session Handoff

Updated: 2026-10-24 KST

## 0. Recovery rule — mandatory
Always fetch live remote first. Never reconstruct current state from chat, memory, copied SHA, or an old handoff paragraph. Live GitHub canonical state wins.

The user must not have to re-explain the factual project state, dependency ordering or reasoning method.

---

# 1. Mandatory read/check order
1. live `timing-defense-workspace` HEAD
2. `PROJECT_STATUS.md`
3. `NEXT_WORK.md`
4. active `legacy-game-structure/data/system_dependency_calibration_order_v0_38.yaml`
5. `legacy-game-structure/138_SESSION_BOOTSTRAP_COGNITIVE_REVIEW_AMENDMENT_V0_1.md`
6. `legacy-game-structure/70_SYSTEM_DEPENDENCY_AND_CALIBRATION_ORDER_REVIEW_V0_1.md`
7. `CHARACTER_PROFILE_RADAR_V1.md`
8. `legacy-game-structure/72_RUN_STATE_LIFECYCLE_APPROVED_CONTRACT_V0_1.md`
9. P4 progression chain: `79`, `81`, `85`, `111`
10. P5 shop chain: `116`, `118`, `119`, `123`, `124`
11. `legacy-game-structure/144_P5_P6_PERSISTENT_STATE_FIDELITY_BRIDGE_RESULT_V0_1.md`
12. `legacy-game-structure/151_P6_ENCOUNTER_FAMILY_ROTATION_AND_TANK_OBJECTIVE_ATTRIBUTION_RESULT_V0_1.md`
13. `legacy-game-structure/152_P6_SHOP_ATK_EXP_OPPORTUNITY_BIDIRECTIONAL_FEEDBACK_RESULT_V0_1.md`
14. **latest:** `legacy-game-structure/153_P6_B2_P4B_RECONSTRUCTION_FIDELITY_BOUNDARY_RESULT_V0_1.md`
15. current production/harness heads
16. only then exact source/evidence for a user-approved next unit

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

Do not relax predeclared fidelity gates after seeing results. Do not reverse-fit lost historical implementation to archived outputs.

---

# 3. Approval rule
Important design/content/numerical/work-boundary/methodology decisions must not be silently applied.

Approval is required before:
- adopting the post-reconstruction P6-B2 methodology;
- changing exact Stage pressure/content;
- class buff/nerf;
- P×P/judgment probability change;
- shop numerical freeze;
- EXP rule change;
- Tier count or monster availability/unlock ladder adoption;
- exact Tier1 roster / Stage1-50 authoring;
- new monster adoption;
- production gameplay change.

Diagnostic/instrumentation/fidelity work may proceed independently if gameplay semantics are unchanged and it stays within an already approved methodology.

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

P6-B1 temp:
- `timing-defense-workspace-temp-p6-shop-exp-opportunity`
- head `7d83360da97cf0add2256c0b391d1dac7e9cd9a6`

P6-B2 reconstruction temp:
- `timing-defense-workspace-temp-p6-b2-p4b-reconstruction`
- final matrix commit `730f58ebdc5325766267b8ce9a7e7a72bfe79038`
- no planning/production authority
- do not promote temp runners/workflows automatically

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
P6 = FORMALLY ENTERED / USER APPROVED
P6-S1 = COMPLETE
P6-A = COMPLETE
P6-B1 = COMPLETE
P6-B2 historical reconstruction method A = USER APPROVED / EXECUTED / FIDELITY GATE FAIL
CURRENT = P6-B2 POST-RECONSTRUCTION NEW METHODOLOGY DECISION GATE
Tier count / exact monster unlock ladder / exact T1 roster = DEFERRED UNTIL P6 CONVERGENCE
Tier1 Stage1-50 authoring = NOT STARTED
production = UNCHANGED / UNAUTHORIZED
```

---

# 6. User-approved campaign/P6 ordering

```text
P6 convergence first
-> then use P6 evidence to constrain Tier structure / monster unlock order
-> then author actual Tier1 Stage1-50 according to Tier availability rules
```

Do not pre-empt exact Tier authoring to solve the current progression-model gap.

---

# 7. Player-facing class identity — preserve

```text
Knight  ATK4 CRIT2 AGI3 KNOCK3 PEN4 AOE2
Rogue   ATK2 CRIT5 AGI5 KNOCK1 PEN1 AOE1
Tank    ATK2 CRIT1 AGI1 KNOCK5 PEN1 AOE3
Archer  ATK3 CRIT2 AGI4 KNOCK1 PEN5 AOE2
Mage    ATK4 CRIT2 AGI2 KNOCK1 PEN1 AOE5
```

Newest user clarification:

```text
Tank does not need high monster-removal.
Tank's role is control / defense / wall protection.
Low removal is intentional if that role works.
```

Active watch only:
`TANK_CONTROL_DEFENSE_TO_OBJECTIVE_PROTECTION_WATCH`

P6-A already showed Tank push, barriers, Aftershock slow and Iron Wall materially reduce wall pressure.
Do not seek damage/clear parity from one encounter family.

---

# 8. P6-B1 closed result

Run:
```text
40029402035
SHA256 83b5e1630231fb38426ae878cd3f2b6e7f3cd99894a44bac8416d0f23d614788
exact-byte repeat PASS
```

Stage49 skilled:
```text
ATK_OFF 17/100
ATK_ON  48/100
31 survival promotions
0 regressions
```

Same-path through49:
```text
root actions ~-4.19%
provisional XP_CREDIT ~-3.89%
```

Survival-promotion cohort:
```text
root actions ~+68.66%
provisional XP_CREDIT ~+70.38%
```

Causal form:
```text
shop ATK
├─ faster same-stage removal -> fewer timing actions / EXP opportunity
└─ failure prevention -> more later-stage timing actions / EXP opportunity
```

Therefore shop→EXP feedback is bidirectional and outcome-conditioned.

---

# 9. P6-B2 historical P4-B reconstruction — exact boundary

The user approved method A: rebuild old P4-B-style feedback runner, prove fidelity, then inject P5 shop.

The repository retains P4-B outputs but not its dedicated propagation runner or exact E01-E20 per-class/per-skill response map.

Untuned reconstruction probes were run. Do not repeat them without new source evidence.

Key runs:

```text
static preflight
run 40031831033
SHA256 6a0a58363378c106d717962111b30d1ec8987048cbf85be205591c3def4f64fc

existing Layer-A Lv6
run 40032022545
SHA256 f914e024e9584ad03bb283a7bd0e8745fbda1ba988ab03bb6ef793ce1500910e

SKILLED_V2 direct-reuse probe
run 40032590027
SHA256 73ef0ee4f3ca96ff85e77e3b8d409d83504957a762f14e11f0a222fde100a279

global envelope equivalence
run 40032994701
SHA256 7fe959498deba8c3e89b7eb7eb4efd4ddb57d0832e617fe43e2dae7ab44f10f4

final semantics matrix
run 40033665060
job 120687797781
commit 730f58ebdc5325766267b8ce9a7e7a72bfe79038
SHA256 af4bb68afa10e6cef4f8e1f8102defb824c1d710e013a48aac82c269eee675ea
exact-byte repeat PASS
```

Predeclared gate:
```text
within ±1 Stage >= 90%
mean abs error <= 0.75 Stage
max abs error <= 3 Stages
```

Best mode `GLOBAL_STAGE_BOUNDARY`:
```text
exact 85/120
within ±1 Stage 115/120 = 95.83%
mean abs error 0.354
max abs error 4
GATE FAIL
```

Reconstructed per-recipe modes were worse:
```text
immediate: 85.0% within ±1, max 5
Stage boundary: 87.5% within ±1, max 5
```

Therefore:
```text
OLD P4-B RUNNER = NOT RECOVERED
OLD EXACT PER-RECIPE RESPONSE MAP = NOT RECOVERABLE WITHOUT TARGET-FITTING
DO NOT RELAX GATE
DO NOT REVERSE-FIT
DO NOT INJECT P5 SHOP INTO FAILED RECOVERED MODEL
```

P4-B remains valid historical bounded evidence for direction/envelope, not executable exact authority.

---

# 10. Current user decision gate

Recommended next methodology:

## FRESH_FORWARD_P6
Build a new bounded Stage1-45 synthetic forward runner from current surviving authority:

```text
P4-A multi-Tier synthetic opportunity corpus
+ current run-state contract
+ current skill semantics
+ SKILLED_V2_CENTRAL
+ P5 stagewise shop economy trajectory
+ explicitly diagnostic shop-effect anchors
```

Independent validation:
```text
P3 early Lv6 behavior
P4-B archived direction/envelope
P6-B1 late shop-ATK bidirectional response
class/encounter identity guards
```

Safeguards:
1. fresh-forward fidelity/authority contract first;
2. do not fit coefficients to old P4-B milestone outputs;
3. separate same-stage self-damping from survival extension;
4. actual timing-action counts drive provisional EXP;
5. Heavy X+Y remains one award;
6. shop effect coefficients remain diagnostic unless separately approved;
7. no final EXP/shop numeric freeze;
8. stop before Tier/unlock adoption if a new design decision appears.

Alternatives:
- knowingly accept failed global approximation — not recommended;
- defer exact skill-reach until concrete Tier authoring.

**No post-reconstruction method is adopted until user approval.**

---

# 11. Operational watch

`TEMP_BRANCH_PUSH_TRIGGERS_HARNESS_CLOUDFLARE_BUILD_WATCH`

One P6-B2 temp push exposed a Cloudflare Workers build check for `timing-defense-skilled-v2-harness`; it failed. No successful deployment was observed and the harness Git branch was not changed.

Minimize temp pushes. Recheck production/harness heads at boundaries.

---

# 12. Fixed guards

```text
LIVE REMOTE WINS
SOURCE/SIMULATOR FIDELITY BEFORE BALANCE INTERPRETATION
NO REPEAT OF CLOSED PROBES WITHOUT TRIGGER
NO RELAXATION OF PREDECLARED GATES AFTER RESULTS
NO REVERSE-FITTING LOST HISTORICAL MODEL
HEAVY X+Y = ONE EXP AWARD
STAGE_SETTLED REQUIRED
WALL DEFICIT / COMBO / CHARGE PERSIST
SURVIVAL != CLEAR
NO HARD CLASS LOCKOUT
TANK LOW REMOVAL IS INTENTIONAL
NO FLAT SHOP->EXP MULTIPLIER
NO LINEAR STAGE1-45 PROJECTION FROM P6-B1 LATE RESULT
NO P×P PATCH TO FIT CONTENT
NO EXACT TIER1 ROSTER/UNLOCK ASSUMPTION
NO PRODUCTION GAMEPLAY CHANGE WITHOUT APPROVAL
```

---

# 13. Session-close quality gate
Before handoff:
1. re-fetch live canonical HEAD;
2. verify production/harness unchanged unless explicitly authorized;
3. separate evidence from adopted semantics/values;
4. keep active plan/status/next/handoff synchronized;
5. explain simply before technical detail;
6. stop at current user decision gate.
