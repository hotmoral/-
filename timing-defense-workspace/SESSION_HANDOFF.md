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
4. active `legacy-game-structure/data/system_dependency_calibration_order_v0_40.yaml`
5. `legacy-game-structure/138_SESSION_BOOTSTRAP_COGNITIVE_REVIEW_AMENDMENT_V0_1.md`
6. `legacy-game-structure/70_SYSTEM_DEPENDENCY_AND_CALIBRATION_ORDER_REVIEW_V0_1.md`
7. `CHARACTER_PROFILE_RADAR_V1.md`
8. `legacy-game-structure/72_RUN_STATE_LIFECYCLE_APPROVED_CONTRACT_V0_1.md`
9. P4 progression/R2 chain: `79`, `81`, `85`, `111`
10. P5 shop chain: `116`, `118`, `119`, `123`, `124`
11. `legacy-game-structure/144_P5_P6_PERSISTENT_STATE_FIDELITY_BRIDGE_RESULT_V0_1.md`
12. P6 causal chain: `150`, `151`, `152`, `153`
13. `legacy-game-structure/154_P6_B2_FRESH_FORWARD_P6_AUTHORITY_AND_FIDELITY_CONTRACT_V0_1.md`
14. **latest:** `legacy-game-structure/155_P6_B2_FRESH_FORWARD_P6_PROGRESSION_FEEDBACK_RESULT_V0_1.md`
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

Do not relax predeclared fidelity gates after seeing results.
Do not reverse-fit lost historical implementation to archived outputs.
Real discrete target/chronology exceptions must be reported rather than erased.

---

# 3. Approval rule
Important design/content/numerical/work-boundary/methodology/phase decisions must not be silently applied.

Approval is required before:
- declaring P6 structurally closed and moving to the next phase;
- adopting Tier count or monster availability/unlock ladder;
- exact Tier1 roster / Stage1-50 authoring;
- changing exact Stage pressure/content;
- class buff/nerf;
- P×P/judgment probability change;
- shop numerical freeze;
- EXP rule change;
- new monster adoption;
- production gameplay change.

Diagnostic/instrumentation/fidelity work may proceed independently only inside an already approved methodology and without gameplay-semantic changes.

---

# 4. Branch checkpoints

Planning/canonical:
- `timing-defense-workspace`
- always re-fetch live HEAD

Production:
- `timing-defense-cloudflare-do-poc`
- verified `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- v0.45 SIEGER FULL PASS
- gameplay/numerical changes unauthorized

Calibration harness:
- `timing-defense-skilled-v2-harness-v01`
- verified `063a9ac9986ba9a8028beb31a5b4c733c9bfa863`

P6-B2 reconstruction temp:
- `timing-defense-workspace-temp-p6-b2-p4b-reconstruction`
- final matrix commit `730f58ebdc5325766267b8ce9a7e7a72bfe79038`
- no planning/production authority

P6-B2 fresh-forward temp:
- `timing-defense-workspace-temp-p6-b2-fresh-forward`
- final head `5093a151142090d58c0e1d26f52cdbee43653542`
- final run `40039163053`
- result SHA256 `80c920d4e2c3982b6a5562768ed4b37f87e2f41703077e46ae8e3cf9d411c6d4`
- no planning/production authority
- do not promote temp runner/workflow automatically

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
P6-B2 historical reconstruction = COMPLETE / FIDELITY GATE FAIL / rejected as exact replacement
P6-B2 FRESH_FORWARD_P6 = DIAGNOSTIC COMPLETE / PASS WITH ABSOLUTE MAGNITUDE WATCH
CURRENT = P6 CLOSURE SYNTHESIS / USER DECISION PENDING
Tier count / exact monster unlock ladder / exact T1 roster = DEFERRED UNTIL USER-APPROVED P6 CLOSURE
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

The evidence for a closure synthesis now exists, but closure itself has not been silently adopted.

---

# 7. Player-facing class identity — preserve

```text
Knight  ATK4 CRIT2 AGI3 KNOCK3 PEN4 AOE2
Rogue   ATK2 CRIT5 AGI5 KNOCK1 PEN1 AOE1
Tank    ATK2 CRIT1 AGI1 KNOCK5 PEN1 AOE3
Archer  ATK3 CRIT2 AGI4 KNOCK1 PEN5 AOE2
Mage    ATK4 CRIT2 AGI2 KNOCK1 PEN1 AOE5
```

Tank does not need monster-removal parity.
Tank's role is control / defense / wall protection.
Low removal is intentional if that role works.
P6-A showed push, barriers, Aftershock slow and Iron Wall materially reduce wall pressure.

Fresh-forward Tank's earlier provisional EXP reach is a timing-opportunity-retention consequence, not evidence for a Tank damage change.

Active Tank watch:
`TANK_CONTROL_DEFENSE_TO_OBJECTIVE_PROTECTION_WATCH`

---

# 8. P6-B1 closed result

```text
shop ATK
├─ faster same-stage removal -> fewer timing actions / EXP opportunity
└─ failure prevention -> more later-stage timing actions / EXP opportunity
```

Main evidence:
```text
run 40029402035
same-path root actions ~-4.19%
same-path provisional XP ~-3.89%
survival-promotion root actions ~+68.66%
survival-promotion provisional XP ~+70.38%
```

Therefore shop→EXP feedback is bidirectional and outcome-conditioned.
Never use a flat global shop->EXP multiplier.

---

# 9. P6-B2 historical reconstruction boundary

The user-approved reconstruction method correctly stopped on fidelity failure.

Best recovered approximation:
```text
GLOBAL_STAGE_BOUNDARY
run 40033665060
within ±1 = 95.83%
mean abs error = 0.354
max error = 4 (gate required <=3)
GATE FAIL
```

Therefore:
```text
OLD P4-B RUNNER = NOT RECOVERED
DO NOT RELAX GATE
DO NOT REVERSE-FIT
DO NOT USE FAILED APPROXIMATION FOR SHOP PROPAGATION
```

Do not repeat this archaeology without concrete new source evidence.

---

# 10. P6-B2 fresh-forward exact result

The user then approved FRESH_FORWARD_P6.
The authority/fidelity contract was written before execution (`154`).

Final successful execution:
```text
branch timing-defense-workspace-temp-p6-b2-fresh-forward
head 5093a151142090d58c0e1d26f52cdbee43653542
run 40039163053
job 120705885236
SUCCESS
result SHA256 80c920d4e2c3982b6a5562768ed4b37f87e2f41703077e46ae8e3cf9d411c6d4
exact-byte repeat PASS
```

Fidelity:
```text
invariant failures = 0
early Lv6 directional gate = PASS all five
survival claim = false
```

Same-entered-Stage ATK test:
```text
240 pairs
root actions 1982 -> 1750
-11.7053%
```

One legitimate chronology exception:
```text
Archer / T3_CENTRAL / Stage30 / Lv21 / seed307
5 -> 6
```
Cause: higher ATK kills SPLITTER earlier, immediately spawned children enter the same root package's remaining penetration targeting, rear enemies survive, and one later root action is added.
Production capability ordering independently supports this chronology.

The first workflow failed because its validator incorrectly required zero such exceptions. The canonical contract had already said chronology exceptions must be reported. Only the validator was corrected; the runner output SHA remained exactly identical.
Do not describe this as relaxing a gate after results.

---

# 11. Fresh-forward causal conclusion

```text
offensive class skill / shop power
-> faster or broader removal
-> fewer later root timing actions
-> fewer provisional EXP awards
-> later skill acquisition
```

Therefore:
```text
PURE_PER_ROOT_ACTION_EXP_CLASS_PROGRESSION_DIVERGENCE = RECONFIRMED
SHOP_ATK_SAME_STAGE_SELF_DAMPING = RECONFIRMED
GLOBAL_SHOP_EXP_RELATION = BIDIRECTIONAL / OUTCOME-CONDITIONED
TANK_FAST_PROGRESSION_SIGNAL = OPPORTUNITY RETENTION, NOT DAMAGE DEFECT
```

This independently matches the structural direction of historical P4-B without fitting to its milestone outputs.

---

# 12. Magnitude watch — mandatory

Fresh-forward early-Lv6 direction matches P3, but offensive-class action-compression magnitude is much stronger than historical P3.

Carry:
`FRESH_FORWARD_ABSOLUTE_MAGNITUDE_WATCH`

Use fresh-forward for:
- causal topology;
- direction;
- accumulation/nonlinearity;
- structural progression divergence.

Do not promote:
- exact Stage reach;
- exact milestone delay;
- exact production EXP values;
- full campaign survival.

---

# 13. EXP routing remains R2

User-approved R2 is unchanged:

```text
pure per-valid-turn EXP = provisional diagnostic baseline only
final EXP semantics = OPEN
hidden class/Tier EXP multipliers = not approved
P10 current-roster multiplayer scaling baseline
-> P10R mandatory EXP / multiplayer timebase reconvergence
```

FRESH_FORWARD_P6 strengthens the existing watch but does not authorize changing EXP semantics now.

---

# 14. Current user decision gate

Recommended:

## P6 structural closure with watches
Interpretation:
- P6 has enough causal evidence to constrain the next campaign-authoring layer;
- this does not claim final EXP convergence;
- `FRESH_FORWARD_ABSOLUTE_MAGNITUDE_WATCH` stays active;
- P10R remains mandatory;
- no class/shop/EXP numerical change is adopted.

If approved, next package is **candidate review only**:
```text
Tier count
+ per-Tier monster availability
+ monster unlock order
+ exact Tier1 roster constraints
```

Do not immediately author Stage1-50 and do not adopt a Tier/unlock candidate without a separate user decision.

If P6 closure is not approved, identify one concrete remaining causal blocker and probe only that blocker.

---

# 15. Operational watches

```text
TEMP_BRANCH_PUSH_TRIGGERS_HARNESS_CLOUDFLARE_BUILD_WATCH
FRESH_FORWARD_ABSOLUTE_MAGNITUDE_WATCH
```

Production and harness were rechecked after fresh-forward and are unchanged.

---

# 16. Fixed guards

```text
LIVE REMOTE WINS
SOURCE/SIMULATOR FIDELITY BEFORE BALANCE INTERPRETATION
NO REPEAT OF CLOSED PROBES WITHOUT TRIGGER
NO RELAXATION OF PREDECLARED GATES AFTER RESULTS
REPORT REAL CHRONOLOGY EXCEPTIONS
NO REVERSE-FITTING LOST HISTORICAL MODEL
HEAVY X+Y = ONE EXP AWARD
STAGE_SETTLED REQUIRED
WALL DEFICIT / COMBO / CHARGE PERSIST
SURVIVAL != CLEAR
NO HARD CLASS LOCKOUT
TANK LOW REMOVAL IS INTENTIONAL
NO FLAT SHOP->EXP MULTIPLIER
NO P×P PATCH TO FIT CONTENT
NO EXACT TIER1 ROSTER/UNLOCK ASSUMPTION
NO PRODUCTION GAMEPLAY CHANGE WITHOUT APPROVAL
```

---

# 17. Session-close quality gate
Before handoff:
1. re-fetch live canonical HEAD;
2. verify production/harness unchanged unless explicitly authorized;
3. separate evidence from adopted semantics/values;
4. keep active plan/status/next/handoff synchronized;
5. explain simply before technical detail;
6. stop at current user decision gate.
