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
Always fetch live remote first. Current key chain:
- `02_TIER_SYSTEM.md`
- `04_MONSTER_ENCOUNTER_MODEL.md`
- `16_MASTER_CAMPAIGN_PROGRESSION_SPINE_V0_1.md`
- `70_SYSTEM_DEPENDENCY_AND_CALIBRATION_ORDER_REVIEW_V0_1.md`
- `72_RUN_STATE_LIFECYCLE_APPROVED_CONTRACT_V0_1.md`
- `76_TEN_STAGE_PERSISTENT_RUN_KERNEL_APPROVED_CONTRACT_V0_1.md`
- `79_P4_EXP_AND_PLAYER_POWER_SPINE_APPROVED_CONTRACT_V0_1.md`
- `85_P4B_R2_APPROVED_ROUTING_CONTRACT_V0_1.md`
- `111_P4E_PROVISIONAL_PLAYER_POWER_SPINE_CLOSURE_WITH_EXP_WATCHES_V0_1.md`
- `116_P5_RUN_COIN_SHOP_A2_APPROVED_STRUCTURAL_CONTRACT_V0_1.md`
- `135_P5_CLASS_IDENTITY_GROUP_DIRECTIONAL_CLOSURE_V0_1.md`
- `144_P5_P6_PERSISTENT_STATE_FIDELITY_BRIDGE_RESULT_V0_1.md`
- `147_ENCOUNTER_COMPOSITION_CLASS_RESPONSE_MATRIX_V0_1.md`
- `149_P6_FORMAL_ENTRY_AND_FIRST_CAUSAL_SLICE_AUTHORIZATION_V0_1.md`
- `150_P6_STAGE46_47_FIRST_CAUSAL_CONVERGENCE_RESULT_V0_1.md`
- `151_P6_ENCOUNTER_FAMILY_ROTATION_AND_TANK_OBJECTIVE_ATTRIBUTION_RESULT_V0_1.md`
- **latest:** `152_P6_SHOP_ATK_EXP_OPPORTUNITY_BIDIRECTIONAL_FEEDBACK_RESULT_V0_1.md`
- active plan `data/system_dependency_calibration_order_v0_37.yaml`

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
P5 mastery reinterpretation = COMPLETE
P5->P6 fidelity bridge = EXACT TEMP PASS
P5 entry charge/combo primary-cause checks = CLOSED
Stage48 local packet tuning = PAUSED
P6 = FORMALLY ENTERED / USER APPROVED
P6-S1 causal convergence = COMPLETE
P6-A encounter-family rotation = COMPLETE
P6-B1 shop-ATK -> EXP-opportunity attribution = COMPLETE
CURRENT = P6-B2 SKILL-REACH PROPAGATION METHOD DECISION GATE
Tier count / monster unlock ladder / exact Tier1 roster = DEFERRED UNTIL P6 CONVERGENCE
Tier1 exact Stage1-50 authoring = NOT STARTED
production = UNCHANGED / UNAUTHORIZED
```

No class/monster/shop/EXP/P×P/Stage scalar, armored packet, Stage48 packet, exact Tier count, Tier1 roster or monster unlock ladder is frozen.

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

Important design/content/numerical/phase adoption requires user approval.
Diagnostic/instrumentation/fidelity work may proceed independently when gameplay semantics do not change.

Run continuity remains authoritative:
- wall current/max/absolute deficit persists;
- level/EXP/coin/shop ranks persist;
- combo persists unless non-PERFECT breaks it;
- charge persists;
- Heavy X->Y resolves before transition;
- Stage advance requires `STAGE_SETTLED`;
- Stage-local enemies/transients do not carry.

---

# Class identity / radar authority

Player-facing radar remains `CHARACTER_PROFILE_RADAR_V1.md`:

```text
Knight  ATK4 CRIT2 AGI3 KNOCK3 PEN4 AOE2
Rogue   ATK2 CRIT5 AGI5 KNOCK1 PEN1 AOE1
Tank    ATK2 CRIT1 AGI1 KNOCK5 PEN1 AOE3
Archer  ATK3 CRIT2 AGI4 KNOCK1 PEN5 AOE2
Mage    ATK4 CRIT2 AGI2 KNOCK1 PEN1 AOE5
```

The radar is a readability/identity graphic, not literal hidden coefficients.

User clarification now authoritative for interpretation:

```text
Tank = control / defense / wall-protection specialist
Tank low monster-removal capability = intentional weakness, not by itself a balance defect
Tank kill/clear parity with damage classes = NOT required
```

Current Tank watch is therefore narrow:

```text
TANK_CONTROL_DEFENSE_TO_OBJECTIVE_PROTECTION_WATCH
```

P6-A already demonstrated that Tank push, barriers, Aftershock slow and Iron Wall materially protect the wall.
Do not use low Tank kill throughput alone as justification for an ATK buff.

Keep `SURVIVAL != CLEAR`, no hard lockout, no automatic class buff/nerf from one encounter family.

---

# P6-A closed encounter-family result

P6-A confirmed that apparent class order rotates with encounter family.

20-seed central-skilled through-family endpoint:

```text
BASELINE dense/aligned
Mage 19 / Archer 19 / Rogue 9 / Knight 7 / Tank 2

durable/distributed
Knight 20 / Mage 20 / Archer 20 / Rogue 17 / Tank 3

screened-CHARGER control family
Knight 20 / Archer 20 / Rogue 18 / Mage 18 / Tank 3
```

Therefore:

```text
CLASS_RANKING_IS_ENCOUNTER_FAMILY_DEPENDENT
CURRENT_DENSE_PACKET != UNIVERSAL_CLASS_POWER_RANKING
```

Tank attribution also closed the easy explanations:
- Aftershock diagnostic zone-center mismatch was real but non-primary;
- push/barrier/slow/Iron Wall all function and reduce wall loss;
- shockwave `0.20 / 0.25 / 0.30` did not materially repair completion.

With the user's radar clarification, this is not treated as a Tank damage-balance blocker.

---

# P6-B1 shop / EXP-opportunity result

Temp branch:
```text
timing-defense-workspace-temp-p6-shop-exp-opportunity
```
Temp head after summary tooling:
```text
7d83360da97cf0add2256c0b391d1dac7e9cd9a6
```

Main attribution run:
```text
40029402035
SHA256 83b5e1630231fb38426ae878cd3f2b6e7f3cd99894a44bac8416d0f23d614788
exact-byte repeat PASS
```

Cumulative summary run:
```text
40029618307
SUCCESS
```

Paired design:
```text
20 SKILLED_V2_CENTRAL seeds × 5 classes × ATK_OFF/ATK_ON
+ all-PERFECT controls
Stage46 -> Stage49
BALANCED FORT/DEF held fixed
only shop ATK component isolated
```

Skilled Stage49 completion:
```text
ATK_OFF 17/100
ATK_ON  48/100
survival promotions 31
regressions 0
```

Clean cumulative self-damping among the 17 pairs that survive through49 in both variants:
```text
root actions ~-4.19%
provisional XP_CREDIT ~-3.89%
```

Survival-promoted cohort (31 pairs):
```text
root actions ~+68.66%
provisional XP_CREDIT ~+70.38%
```

Interpretation:

```text
shop ATK
├─ faster removal within a survived Stage
│  -> fewer valid timing actions
│  -> less EXP opportunity
└─ prevents failure / extends progression
   -> later Stages become reachable
   -> more total timing actions / EXP opportunity
```

Thus:

```text
SHOP_ATK_TO_EXP_FEEDBACK = BIDIRECTIONAL / OUTCOME-CONDITIONED
MONOTONIC "MORE SHOP POWER -> LESS EXP" ASSUMPTION = REJECTED
```

Do not treat the all-pairs positive net as per-Stage EXP acceleration; it is largely survival-extension exposure.
Do not project the late clean ~4% compression linearly across Stage1-45.

---

# P4/P6 progression authority boundary

P4 pure per-valid-turn EXP remains a **provisional diagnostic baseline**, not final EXP authority.
Heavy X+Y remains one EXP award.
Final EXP routing was deferred under approved R2.

P4-B historical evidence showed skill-power-driven action-opportunity divergence can materially move common skill windows.
However the reproducibility audit found:
- historical P4-B result JSON exists;
- P4-B report exists;
- P4-A runner/validator exists;
- **no dedicated reproducible P4-B propagation runner is retained in the historical canonical tree**.

Therefore P6-B2 may not silently fabricate an exact Lv31 shift using:
- nominal shop ATK%;
- late-run ~4% compression;
- old median action ratios;
- or a flat class/Tier correction.

---

# Tier / campaign authoring boundary

User-approved order remains:

```text
P6 convergence
-> constrain Tier monster availability / unlock order
-> author exact Tier1 Stage1-50
```

Current monsters and armored proxy remain diagnostic vocabulary, not final T1 roster.
Exact Tier count, exact unlock ladder and exact Tier1 roster remain OPEN.

---

# Current decision gate — P6-B2

Question:

> What bounded reproducible method should estimate Stage1-45 shop-history × skill-power × combat-opportunity × EXP × skill-reach before exact T1 Stage1-50 authoring?

Candidate methods, **not yet adopted**:

### A — rebuild a bounded P4-B-style synthetic combat-feedback runner, then inject P5 stage-by-stage shop trajectories
- preserves current dependency ordering;
- closest continuity with prior P4 evidence;
- requires an explicit reconstruction/fidelity contract because the old runner was not retained.

### B — author a provisional full Stage1-50 combat fixture first and run actual shop/EXP jointly
- more direct chronology;
- risks pre-empting the approved P6 -> Tier/unlock -> exact T1 authoring order.

### C — defer exact skill-reach propagation until later exact authoring
- avoids synthetic assumptions;
- leaves P6 progression convergence open before Tier/unlock work.

No B2 method has been selected.
No new EXP rule, shop coefficient, class scalar, Tank scalar or production gameplay value is authorized.