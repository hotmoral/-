# Timing Defense — Project Status

Updated: 2026-10-24 KST

## Production / harness
- production branch `timing-defense-cloudflare-do-poc`
- last verified production HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- v0.45 SIEGER FULL PASS
- production gameplay/numerical changes unauthorized
- calibration harness `timing-defense-skilled-v2-harness-v01`
- last verified harness HEAD `063a9ac9986ba9a8028beb31a5b4c733c9bfa863`

## Canonical operating authority
Always fetch live remote first. Current key chain includes:
- `72_RUN_STATE_LIFECYCLE_APPROVED_CONTRACT_V0_1.md`
- `79_P4_EXP_AND_PLAYER_POWER_SPINE_APPROVED_CONTRACT_V0_1.md`
- `81_P4B_LV6_LV21_COMBAT_FEEDBACK_EXECUTION_REPORT_V0_1.md`
- `85_P4B_R2_APPROVED_ROUTING_CONTRACT_V0_1.md`
- `111_P4E_PROVISIONAL_PLAYER_POWER_SPINE_CLOSURE_WITH_EXP_WATCHES_V0_1.md`
- `116_P5_RUN_COIN_SHOP_A2_APPROVED_STRUCTURAL_CONTRACT_V0_1.md`
- `135_P5_CLASS_IDENTITY_GROUP_DIRECTIONAL_CLOSURE_V0_1.md`
- `144_P5_P6_PERSISTENT_STATE_FIDELITY_BRIDGE_RESULT_V0_1.md`
- `147_ENCOUNTER_COMPOSITION_CLASS_RESPONSE_MATRIX_V0_1.md`
- `150_P6_STAGE46_47_FIRST_CAUSAL_CONVERGENCE_RESULT_V0_1.md`
- `151_P6_ENCOUNTER_FAMILY_ROTATION_AND_TANK_OBJECTIVE_ATTRIBUTION_RESULT_V0_1.md`
- `152_P6_SHOP_ATK_EXP_OPPORTUNITY_BIDIRECTIONAL_FEEDBACK_RESULT_V0_1.md`
- **latest:** `153_P6_B2_P4B_RECONSTRUCTION_FIDELITY_BOUNDARY_RESULT_V0_1.md`
- active plan `data/system_dependency_calibration_order_v0_38.yaml`

Live remote wins over memory/chat/copied SHA.

---

# Current phase

```text
P0 = PASS_WITH_WATCHES
P1 = USER_APPROVED_STRUCTURAL_COMPLETE
P2 = USER_APPROVED_STRUCTURAL_COMPLETE
P3 = STRUCTURAL_PASS_COMPLETE / STAGE_SETTLED + persistent run-state authority
P4 = PROVISIONAL_STRUCTURAL_COMPLETE_WITH_WATCHES
P5 A2 shop = USER APPROVED
P5 class identity group = DIRECTIONALLY CLOSED
P5->P6 fidelity bridge = EXACT TEMP PASS
P6 = FORMALLY ENTERED / USER APPROVED
P6-S1 = COMPLETE
P6-A encounter-family rotation = COMPLETE
P6-B1 shop-ATK / EXP-opportunity attribution = COMPLETE
P6-B2 historical P4-B reconstruction method A = USER APPROVED / EXECUTED / FIDELITY GATE FAIL
CURRENT = P6-B2 POST-RECONSTRUCTION NEW METHOD DECISION GATE
Tier count / monster unlock ladder / exact Tier1 roster = DEFERRED UNTIL P6 CONVERGENCE
Tier1 exact Stage1-50 authoring = NOT STARTED
production = UNCHANGED / UNAUTHORIZED
```

No class/monster/shop/EXP/P×P/Stage scalar, exact Tier count, Tier1 roster or monster unlock ladder is frozen.

---

# Stable operating rules

```text
source/simulator fidelity
-> lifecycle/state
-> encounter composition / geometry / chronology
-> class/package semantics
-> shop/feedback
-> exact scalar last
```

Do not relax a predeclared fidelity gate after seeing results.
Do not reverse-fit a lost historical runner to archived outputs.
Important design/content/numerical/methodology adoption requires user approval.

---

# Class identity / Tank interpretation

Approved player-facing radar:

```text
Knight  ATK4 CRIT2 AGI3 KNOCK3 PEN4 AOE2
Rogue   ATK2 CRIT5 AGI5 KNOCK1 PEN1 AOE1
Tank    ATK2 CRIT1 AGI1 KNOCK5 PEN1 AOE3
Archer  ATK3 CRIT2 AGI4 KNOCK1 PEN5 AOE2
Mage    ATK4 CRIT2 AGI2 KNOCK1 PEN1 AOE5
```

User clarification:

```text
Tank = control / defense / wall-protection specialist
Tank low removal = intentional weakness, not by itself a defect
Tank kill/clear parity with damage classes = NOT required
```

Active Tank watch:
`TANK_CONTROL_DEFENSE_TO_OBJECTIVE_PROTECTION_WATCH`

P6-A already showed push/barriers/Aftershock slow/Iron Wall materially reduce wall pressure.

---

# Closed P6-A result

Class order rotates by encounter family.

```text
BASELINE dense/aligned:
Mage19 Archer19 Rogue9 Knight7 Tank2

durable/distributed:
Knight20 Mage20 Archer20 Rogue17 Tank3

screened CHARGER:
Knight20 Archer20 Rogue18 Mage18 Tank3
```

Therefore one late packet is not universal class-power authority.

---

# Closed P6-B1 result

Main run:
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

Same-path cumulative cohort, both variants through49:
```text
root actions ~-4.19%
provisional XP_CREDIT ~-3.89%
```

Survival-promotion cohort:
```text
root actions ~+68.66%
provisional XP_CREDIT ~+70.38%
```

Conclusion:

```text
SHOP_ATK_TO_EXP_FEEDBACK = BIDIRECTIONAL / OUTCOME-CONDITIONED
```

Do not project the late-run ~4% compression linearly across Stage1-45.

---

# P6-B2 historical reconstruction result

The user approved method A:

```text
rebuild bounded P4-B-style runner
-> prove historical fidelity first
-> only then inject P5 stagewise shop trajectory
```

The fidelity-first gate did its job.

Historical P4-B has:
- report;
- result JSON;
- archived all-20 class/skill action-response medians/ranges.

But repository history does **not** retain:
- the dedicated P4-B propagation runner;
- the exact E01-E20 × class × Lv6/11/16/21 response map.

Multiple untuned reconstruction families were tested.

Best final mode:
```text
GLOBAL_STAGE_BOUNDARY
run 40033665060
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

Best result across 120 held-out class×Tier×milestone P50 points:
```text
exact 85/120 = 70.83%
within ±1 Stage 115/120 = 95.83%
mean abs error 0.354 Stage
max abs error 4 Stages
GATE FAIL
```

Reconstructed per-recipe variants were worse:
```text
immediate:      85.0% within ±1 / max 5
Stage-boundary: 87.5% within ±1 / max 5
```

Therefore:

```text
OLD_P4B_DEDICATED_RUNNER = NOT RECOVERED
OLD_P4B_EXACT_PER_RECIPE_MAP = NOT RECOVERABLE WITHOUT TARGET-FITTING
GLOBAL_RESPONSE_ENVELOPE = STRONGLY SUPPORTED BUT NOT AN ACCEPTED EXACT REPLACEMENT
P5 SHOP INJECTION INTO RECOVERED OLD P4B = BLOCKED
```

The gate is not relaxed and the per-recipe map is not reverse-fit.

---

# What can still be used going forward

```text
P4-A synthetic 50-Stage opportunity corpus
P4-B archived class/skill response envelope and divergence direction
P3 early independent Lv6 behavior
current skill/run-state semantics
SKILLED_V2_CENTRAL
P5 stagewise shop economy trajectory
P6-B1 late shop/EXP paired attribution
```

The old P4-B runner itself is no longer treated as executable authority.

---

# Current decision gate

Recommended next methodology:

## FRESH_FORWARD_P6
Build a new reproducible Stage1-45 synthetic forward progression runner from current surviving authority rather than continuing archaeology of the lost P4-B runner.

Candidate inputs:
```text
P4-A multi-Tier synthetic opportunity corpus
+ current run-state contract
+ current skill semantics
+ SKILLED_V2_CENTRAL
+ P5 stagewise shop economy trajectory
+ explicit diagnostic shop-effect anchors
```

Independent validation boundaries:
```text
P3 early Lv6 signal
P4-B archived direction/envelope
P6-B1 late shop-ATK bidirectional behavior
class/encounter identity guards
```

This is a **new methodology choice**. It is recommended but not adopted until user approval.

Alternatives:
- accept the failed global approximation anyway — not recommended;
- defer exact skill-reach propagation until concrete Tier authoring.

---

# Operational watch

One P6-B2 temp push exposed a Cloudflare `Workers Builds: timing-defense-skilled-v2-harness` check. That check failed; no successful deployment was observed and the harness Git branch was not changed.

Carry:
`TEMP_BRANCH_PUSH_TRIGGERS_HARNESS_CLOUDFLARE_BUILD_WATCH`

Minimize temp pushes and recheck production/harness heads at work boundaries.

---

# Tier / campaign authoring boundary

User-approved order remains:

```text
P6 convergence
-> constrain Tier monster availability / unlock order
-> author exact Tier1 Stage1-50
```

Exact Tier count, unlock ladder and Tier1 roster remain OPEN.
