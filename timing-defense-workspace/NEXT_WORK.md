# Timing Defense — Next Work Boundary

Updated: 2026-10-24 KST

## Live recovery
Before work:
1. fetch live `timing-defense-workspace` HEAD;
2. read `PROJECT_STATUS.md`;
3. read `SESSION_HANDOFF.md`;
4. read active `legacy-game-structure/data/system_dependency_calibration_order_v0_38.yaml`;
5. read `152_P6_SHOP_ATK_EXP_OPPORTUNITY_BIDIRECTIONAL_FEEDBACK_RESULT_V0_1.md`;
6. read **latest** `153_P6_B2_P4B_RECONSTRUCTION_FIDELITY_BOUNDARY_RESULT_V0_1.md`;
7. read P4 chain `79`, `81`, `85`, `111` and P5 shop chain `116`, `118`, `119`, `123`, `124` before any new progression runner;
8. only then open exact source/evidence for a user-approved next unit.

Do not rerun closed P6-A/B1 or repeat P6-B2 reconstruction archaeology without a concrete new source trigger.

---

# Current phase

```text
P6 = FORMALLY ENTERED / USER APPROVED
P6-S1 = COMPLETE
P6-A = COMPLETE
P6-B1 = COMPLETE
P6-B2 historical reconstruction method A = USER APPROVED / EXECUTED / FIDELITY GATE FAIL
CURRENT = POST-RECONSTRUCTION METHODOLOGY DECISION GATE
Tier count / monster unlock ladder / exact T1 roster = DEFERRED UNTIL P6 CONVERGENCE
production = UNCHANGED / UNAUTHORIZED
```

---

# Tank identity guard

```text
Tank ATK2 CRIT1 AGI1 KNOCK5 PEN1 AOE3
```

Tank is a control/defense/wall-protection specialist. Low removal by itself is not a defect and kill parity is not required.
Active watch:
`TANK_CONTROL_DEFENSE_TO_OBJECTIVE_PROTECTION_WATCH`

Do not tune Tank ATK from dense-wave clear-rate equality pressure.

---

# Closed P6-B1 result

```text
shop ATK
├─ same survived path: faster removal -> fewer timing actions / EXP opportunity
└─ failure prevention: later-stage access -> more total timing actions / EXP opportunity
```

Main run `40029402035`, exact repeat PASS.
Same-path cumulative through49: root actions ~-4.19%, provisional XP ~-3.89%.
Survival-promotion cohort: root actions ~+68.66%, provisional XP ~+70.38%.

Never use a flat monotonic shop->EXP multiplier.

---

# Closed P6-B2 historical reconstruction result

User-approved method A required historical fidelity before P5 shop injection.

Best recovered propagation mode:
```text
GLOBAL_STAGE_BOUNDARY
run 40033665060
SHA256 af4bb68afa10e6cef4f8e1f8102defb824c1d710e013a48aac82c269eee675ea
exact-byte repeat PASS
```

Predeclared gate:
```text
within ±1 Stage >= 90%
mean abs error <= 0.75
max abs error <= 3
```

Held-out 120-point result:
```text
exact 85/120
within ±1 Stage 115/120 = 95.83%
mean abs error 0.354
max error 4
GATE FAIL
```

Per-recipe reconstruction was worse and is rejected.

Therefore:
```text
DO NOT relax the gate
DO NOT reverse-fit E01-E20 response values
DO NOT inject P5 shop into the failed recovered-old-P4B model
DO NOT claim exact Lv31 Stage shift from this approximation
```

The old P4-B runner/per-recipe map is not recoverable from current sources without target-fitting.

---

# CURRENT USER DECISION REQUIRED

## Recommended — FRESH_FORWARD_P6

Stop reconstructing the lost P4-B implementation. Build a new bounded forward progression runner from **current surviving authority**:

```text
P4-A synthetic multi-Tier Stage opportunity corpus
+ current run-state lifecycle
+ current skill semantics by milestone
+ SKILLED_V2_CENTRAL judgment process
+ P5 stagewise shop economy trajectory
+ explicitly labeled diagnostic shop-effect anchors
```

Validate independently against:
```text
P3 early Lv6 behavior
P4-B archived direction/envelope
P6-B1 late shop/EXP bidirectional response
class/encounter identity guards
```

Purpose:
- answer the actual P6 question now;
- produce a maintainable forward model instead of pretending a lost provisional runner is exact authority;
- preserve approved ordering before exact Tier1 authoring.

Required safeguards if approved:
1. write a fresh-forward fidelity/authority contract first;
2. no old P4-B milestone targets used for coefficient fitting;
3. separate within-stage self-damping from survival-extension;
4. shop effect coefficients remain diagnostic unless separately approved;
5. actual timing-action count drives provisional EXP;
6. Heavy X+Y remains one EXP award;
7. no final EXP/shop numeric freeze;
8. stop again before Tier/unlock adoption if a design decision appears.

## Alternative — accept failed global approximation
Not recommended. It knowingly violates the predeclared max-error gate.

## Alternative — defer exact skill reach
Safe but leaves P6 progression convergence open until concrete Tier authoring.

**FRESH_FORWARD_P6 is recommended but not adopted until user approval.**

---

# Operational watch

`TEMP_BRANCH_PUSH_TRIGGERS_HARNESS_CLOUDFLARE_BUILD_WATCH`

A P6-B2 temp push exposed a Cloudflare harness build check; it failed and no successful deployment was observed. Minimize further temp pushes and verify production/harness heads at boundaries.

---

# Fixed guards

```text
LIVE REMOTE WINS
SOURCE/SIMULATOR FIDELITY BEFORE BALANCE INTERPRETATION
DO NOT RELAX PREDECLARED GATES AFTER RESULTS
DO NOT REVERSE-FIT LOST HISTORICAL MODEL
SKILLED_V2_CENTRAL FIXED FOR CURRENT CAUSAL COMPARISONS
HEAVY X+Y = ONE EXP AWARD
STAGE_SETTLED REQUIRED
WALL DEFICIT / COMBO / CHARGE PERSIST
SURVIVAL != CLEAR
TANK LOW REMOVAL IS INTENTIONAL
NO FLAT SHOP->EXP MULTIPLIER
NO LINEAR STAGE1-45 PROJECTION FROM LATE B1 RESULT
NO P×P PATCH TO FIT CONTENT
NO EXACT TIER1 ROSTER/UNLOCK ASSUMPTION
NO PRODUCTION GAMEPLAY CHANGE WITHOUT APPROVAL
```