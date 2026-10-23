# Timing Defense — Project Status

Updated: 2026-10-24 KST

## Production / harness
- production branch `timing-defense-cloudflare-do-poc`
- verified production HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- v0.45 SIEGER FULL PASS
- production gameplay/numerical changes unauthorized
- calibration harness `timing-defense-skilled-v2-harness-v01`
- verified harness HEAD `063a9ac9986ba9a8028beb31a5b4c733c9bfa863`
- both unchanged during P6-B2 fresh-forward work

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
- `150_P6_STAGE46_47_FIRST_CAUSAL_CONVERGENCE_RESULT_V0_1.md`
- `151_P6_ENCOUNTER_FAMILY_ROTATION_AND_TANK_OBJECTIVE_ATTRIBUTION_RESULT_V0_1.md`
- `152_P6_SHOP_ATK_EXP_OPPORTUNITY_BIDIRECTIONAL_FEEDBACK_RESULT_V0_1.md`
- `153_P6_B2_P4B_RECONSTRUCTION_FIDELITY_BOUNDARY_RESULT_V0_1.md`
- `154_P6_B2_FRESH_FORWARD_P6_AUTHORITY_AND_FIDELITY_CONTRACT_V0_1.md`
- **latest:** `155_P6_B2_FRESH_FORWARD_P6_PROGRESSION_FEEDBACK_RESULT_V0_1.md`
- active plan `data/system_dependency_calibration_order_v0_40.yaml`

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
P6-B2 historical P4-B reconstruction = COMPLETE / FIDELITY GATE FAIL / DO NOT REVERSE-FIT
P6-B2 FRESH_FORWARD_P6 = DIAGNOSTIC COMPLETE / PASS WITH ABSOLUTE MAGNITUDE WATCH
CURRENT = P6 CLOSURE SYNTHESIS / USER DECISION PENDING
Tier count / monster unlock ladder / exact Tier1 roster = DEFERRED UNTIL USER-APPROVED P6 CLOSURE
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
Legitimate discrete chronology exceptions must be reported rather than hidden.
Important design/content/numerical/methodology/phase adoption requires user approval.

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

Tank remains a control / defense / wall-protection specialist.
Low removal is an intentional limitation, not by itself a defect.
Active watch: `TANK_CONTROL_DEFENSE_TO_OBJECTIVE_PROTECTION_WATCH`.

Fresh-forward Tank's earlier provisional EXP reach is interpreted as **timing-opportunity retention**, not as evidence for a damage buff/nerf.

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

One late packet is not universal class-power authority.

---

# Closed P6-B1 result

Main run:
```text
40029402035
SHA256 83b5e1630231fb38426ae878cd3f2b6e7f3cd99894a44bac8416d0f23d614788
exact-byte repeat PASS
```

Same-path cumulative through49:
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

---

# Closed P6-B2 historical reconstruction result

Best recovered approximation:
```text
GLOBAL_STAGE_BOUNDARY
run 40033665060
SHA256 af4bb68afa10e6cef4f8e1f8102defb824c1d710e013a48aac82c269eee675ea
exact-byte repeat PASS
```

Predeclared fidelity gate failed only on max error:
```text
within ±1 Stage 115/120 = 95.83%
mean abs error 0.354 Stage
max error 4 Stages (required <=3)
GATE FAIL
```

Therefore:
```text
OLD_P4B_DEDICATED_RUNNER = NOT RECOVERED
DO NOT RELAX GATE
DO NOT REVERSE-FIT
DO NOT INJECT SHOP INTO FAILED RECOVERED MODEL
```

---

# Closed P6-B2 FRESH_FORWARD_P6 result

Contract written before execution:
`154_P6_B2_FRESH_FORWARD_P6_AUTHORITY_AND_FIDELITY_CONTRACT_V0_1.md`.

Result:
`155_P6_B2_FRESH_FORWARD_P6_PROGRESSION_FEEDBACK_RESULT_V0_1.md`.

Temp execution:
```text
branch timing-defense-workspace-temp-p6-b2-fresh-forward
head 5093a151142090d58c0e1d26f52cdbee43653542
final run 40039163053
job 120705885236
SUCCESS
result SHA256 80c920d4e2c3982b6a5562768ed4b37f87e2f41703077e46ae8e3cf9d411c6d4
exact-byte repeat PASS
```

Validation:
```text
invariant failures = 0
early Lv6 directional gate = PASS all five classes
survival claim = false
```

Isolated same-entered-Stage ATK pairs:
```text
240 pairs
ATK_OFF root actions 1982
ATK_ON  root actions 1750
-11.7053%
```

One reported chronology exception exists:
```text
Archer / T3_CENTRAL / Stage30 / Lv21 / seed307
5 -> 6 root actions
```
Cause: earlier SPLITTER death inserts children into live targeting order and can consume remaining penetration slots. Production capability ordering supports this as a legitimate discrete chronology effect.

Structural conclusion:
```text
PURE_PER_ROOT_ACTION_EXP_CLASS_PROGRESSION_DIVERGENCE = RECONFIRMED
SHOP_ATK_SAME_STAGE_SELF_DAMPING = RECONFIRMED
GLOBAL_SHOP_EXP_RELATION = STILL BIDIRECTIONAL / OUTCOME-CONDITIONED
TANK_FAST_PROGRESSION_SIGNAL = OPPORTUNITY RETENTION, NOT DAMAGE DEFECT
```

Magnitude warning:
Fresh runner reproduces P3 early-Lv6 **direction**, but offensive-class compression magnitude is materially stronger than historical P3.
Therefore:
```text
FRESH_FORWARD_ABSOLUTE_MAGNITUDE_WATCH = ACTIVE
```
Use fresh-forward for causal direction and accumulation, not exact production Stage reach.

---

# EXP routing remains unchanged

User-approved R2 remains authoritative:

```text
pure per-valid-turn EXP = provisional diagnostic baseline only
final EXP semantics = OPEN
hidden class/Tier EXP multipliers = NOT approved
P10 current-roster multiplayer scaling baseline
-> P10R mandatory EXP / multiplayer timebase reconvergence
```

Fresh-forward does not authorize an EXP rule change now.

---

# Current decision gate

Available evidence now supports a P6 closure synthesis, but the phase boundary itself is not silently adopted.

Decision to request from user:

```text
Accept current P6 causal convergence as sufficient structural closure?
YES -> next package is Tier-count / monster-availability / unlock-order candidate review
NO  -> identify a concrete unresolved P6 blocker and probe only that blocker
```

No exact Tier count, monster unlock ladder, Tier1 roster or Stage1-50 authoring begins before that decision.

---

# Operational watches

```text
TEMP_BRANCH_PUSH_TRIGGERS_HARNESS_CLOUDFLARE_BUILD_WATCH
FRESH_FORWARD_ABSOLUTE_MAGNITUDE_WATCH
```

Production and harness heads were rechecked after fresh-forward execution and remained unchanged.
