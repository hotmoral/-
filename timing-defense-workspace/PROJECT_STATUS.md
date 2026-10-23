# Timing Defense — Project Status

Updated: 2026-10-24 KST

## Production checkpoint
- branch `timing-defense-cloudflare-do-poc`
- last verified HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- v0.45 SIEGER FULL PASS
- production gameplay/numerical changes unauthorized

## Calibration harness checkpoint
- branch `timing-defense-skilled-v2-harness-v01`
- last verified HEAD `063a9ac9986ba9a8028beb31a5b4c733c9bfa863`
- unchanged by current planning/diagnostic work

## Canonical operating authority
Always fetch live remote first. Current key documents:
- `legacy-game-structure/02_TIER_SYSTEM.md`
- `legacy-game-structure/04_MONSTER_ENCOUNTER_MODEL.md`
- `legacy-game-structure/16_MASTER_CAMPAIGN_PROGRESSION_SPINE_V0_1.md`
- `legacy-game-structure/86_SESSION_RECOVERY_AND_CROSS_STAGE_REVIEW_PROTOCOL_V0_1.md`
- `legacy-game-structure/138_SESSION_BOOTSTRAP_COGNITIVE_REVIEW_AMENDMENT_V0_1.md`
- `legacy-game-structure/70_SYSTEM_DEPENDENCY_AND_CALIBRATION_ORDER_REVIEW_V0_1.md`
- `legacy-game-structure/72_RUN_STATE_LIFECYCLE_APPROVED_CONTRACT_V0_1.md`
- `legacy-game-structure/76_TEN_STAGE_PERSISTENT_RUN_KERNEL_APPROVED_CONTRACT_V0_1.md`
- `legacy-game-structure/91_P4D1_LV31_POWER_FANTASY_AND_STAGE46_MASTERY_GATE_APPROVED_CONTRACT_V0_1.md`
- `legacy-game-structure/116_P5_RUN_COIN_SHOP_A2_APPROVED_STRUCTURAL_CONTRACT_V0_1.md`
- `legacy-game-structure/135_P5_CLASS_IDENTITY_GROUP_DIRECTIONAL_CLOSURE_V0_1.md`
- `legacy-game-structure/137_P5_STAGE46_49_EXACT_EXECUTION_STAGE_SETTLED_BOUNDARY_RESULT_V0_1.md`
- `legacy-game-structure/142_P5_STAGE48_FODDER_CHAIN_AND_GLOBAL_STANDOFF_BOUNDARY_RESULT_V0_1.md`
- `legacy-game-structure/143_P5_SKILLED_V2_LATE_RUN_REINTERPRETATION_AND_P5_P6_FIDELITY_GATE_V0_1.md`
- `legacy-game-structure/144_P5_P6_PERSISTENT_STATE_FIDELITY_BRIDGE_RESULT_V0_1.md`
- `legacy-game-structure/145_P5_P6_STAGE46_47_ARMORED_MIDWAVE_REPLACEMENT_DIAGNOSTIC_V0_1.md`
- **latest:** `legacy-game-structure/146_P5_P6_ARMORED_PLACEMENT_AND_TIER_AUTHORING_BOUNDARY_V0_1.md`
- active dependency plan `legacy-game-structure/data/system_dependency_calibration_order_v0_33.yaml`

Live remote always wins over copied SHA, memory or chat.

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
P5→P6 persistent-state fidelity bridge = EXACT TEMP EXECUTION PASS
P5 entry charge/combo cause checks = CLOSED AS PRIMARY EXPLANATION
P5 Stage46/47 sparse-armored count/chronology/band diagnostics = COMPLETE
P5 armored coordinate micro-tuning = STOPPED TO AVOID PRE-AUTHORING OVERFIT
Stage48 local SIEGER packet tuning = PAUSED
CURRENT = ENCOUNTER-COMPOSITION CLASS-RESPONSE MATRIX DIAGNOSTIC
P6 = NOT FORMALLY STARTED / FORMAL START STILL REQUIRES USER APPROVAL
Tier1 exact 50-Stage authoring = NOT STARTED
production = UNCHANGED / UNAUTHORIZED
```

No Stage46/47 armored packet is approved.
No Stage48 packet is approved.
No armored/elite/new-monster identity is approved.
No SIEGER standoff value is frozen.
No Tank scalar is selected.
No class/monster/shop/EXP/P×P numerical value is frozen.
No exact Tier1 roster/unlock ladder is frozen.

---

# Mandatory operating method

Every material step checks:

```text
Tier/Stage purpose
-> monster availability / content role
-> encounter family / formation / chronology
-> class identity / skill behavior
-> run-state persistence
-> player mastery / judgment model
-> shop/economy
-> attack count / EXP / skill-reach feedback
-> target order / geometry
-> wall pressure / SIEGER exposure
-> STAGE_SETTLED
-> carried wall deficit
-> later-Stage consequences
-> downstream P6/meta/multiplayer impact
```

Repair/analysis order:

```text
source/simulator fidelity
-> lifecycle/state semantics
-> encounter composition / geometry / chronology
-> class/package semantics
-> shop/feedback
-> exact scalar tuning last
```

Important design/content/numerical/work-boundary decisions require user approval before adoption. Diagnostic/instrumentation work may proceed independently when gameplay semantics remain unchanged.

Do not rerun closed work without a concrete trigger.

---

# Stable structural truths

## Run continuity
Within one Tier attempt:
- Base HP/max, level/EXP, coin and shop ranks persist;
- combo persists across Stage/shop/target-wait unless a non-PERFECT timing judgment breaks it;
- charge persists across Stage/shop;
- an in-progress Heavy X→Y resolves before transition.

## Stage transition

```text
last authored spawn
+ zero live Stage-owned enemies
+ authorized effects drained
+ no unresolved delayed Stage transient
= STAGE_SETTLED
-> Stage clear/shop
-> reset Stage-local enemies/transients
-> next Stage
```

Wall current/max/absolute deficit persists; enemy instances do not.

## Class identity guards

```text
Knight  ATK4 CRIT2 AGI3 KNOCK3 PEN4 AOE2
Rogue   ATK2 CRIT5 AGI5 KNOCK1 PEN1 AOE1
Tank    ATK2 CRIT1 AGI1 KNOCK5 PEN1 AOE3
Archer  ATK3 CRIT2 AGI4 KNOCK1 PEN5 AOE2
Mage    ATK4 CRIT2 AGI2 KNOCK1 PEN1 AOE5
```

Keep:
- `SURVIVAL != CLEAR`;
- class clear rates need not be identical;
- Tank solo parity is not required;
- no hard class lockout;
- do not convert encounter-composition skew directly into class buff/nerf;
- no Stage46 nerf just to hide a P×P/Lv31 coupling effect;
- no P×P probability manipulation to make content fit;
- Rogue deterministic retarget is not the first repair axis.

---

# Tier availability / 50-Stage authoring authority

Active direction from `02_TIER_SYSTEM.md` and `16_MASTER_CAMPAIGN_PROGRESSION_SPINE_V0_1.md`:

```text
T1 = limited monster subset
higher Tier(s) = new monster archetype introductions
returning monsters = new formation/cadence/composition reinterpretation
current 9 ordinary monsters = foundation roster, not lifetime final roster
```

`09_TIER_LADDER_CANDIDATE_V0_1.md` contains an older proposal that T1 teaches all nine ordinary monsters by Stage29. That portion is now explicitly treated as:

```text
SUPERSEDED_LEGACY_CANDIDATE
NOT_ACTIVE_TIER_AVAILABILITY_AUTHORITY
```

Exact Tier count and exact unlock ladder remain open.

Current Stage46→49 diagnostics use the foundation 9-monster roster plus temporary proxy to learn mechanics. They are **not** final Tier1 authoring.

When exact Tier1 Stage1→50 authoring begins, order is:

```text
active monster availability ladder
-> T1 introduced/available/returning set
-> Tier novelty/identity
-> 50-Stage macro flow
-> exact frequency/count/composition/formation/cadence
```

---

# Mastery reinterpretation and fidelity bridge

Old P5 late-run runner effectively used ordinary PERFECT + successful Heavy P×P/CRITICAL, so old late-run survival is upper-tail evidence.

Central-skilled run `39968100989`:

```text
through Stage49 = 45/100
fail Stage46 = 26
fail Stage47 = 21
fail Stage48 = 0
fail Stage49 = 8
Knight 3 / Rogue 4 / Tank 2 / Archer 18 / Mage 18
```

Factor isolation `39968400953`:

```text
ordinary central + Heavy forced P×P -> 100/100 through47
ordinary PERFECT + Heavy central     -> 63/100
full central                         -> 58/100
```

Dominant sensitivity remains:

```text
REDUCED_PXP_LV31_FINAL_FREQUENCY
```

The fidelity bridge run `39971985538` combined persistent SKILLED_V2 state, combo, charge, combo damage, N3, Lv31 packages, P5 shop, right-edge combat, STAGE_SETTLED and carried wall deficit.

All-PERFECT:

```text
20/20 through Stage49
```

Central-skilled by entry charge:

```text
charge 0 -> 48/100
charge 1 -> 45/100
charge 2 -> 42/100
charge 3 -> 44/100
```

Stage46 failures were `23/100` for every entry charge.

Entry combo upper-bound run `39972649909`:

```text
combo 0  -> 48/100
combo 40 -> 48/100
```

Therefore entry charge/combo boundaries are not the primary explanation.

---

# User difficulty interpretation — current guidance, not freeze

The user judged the current central-skilled late-segment completion around the mid-40% range as plausibly appropriate because all-PERFECT retains a 100% path in the tested controls.

This means:

```text
DO NOT assume the global skilled clear rate must be raised.
FIRST ask whether class differences are caused by encounter composition.
```

`45%` is not an exact target or production freeze.

---

# Stage46/47 sparse armored diagnostic — COMPLETE

The existing `ARMORED_DURABLE_PROXY` was reused unchanged. It is still a diagnostic body, not an approved new monster.

## Count sensitivity — run `39976475153`

```text
BASELINE       A18 M18 R6 K5 T1 = 48/100
1 per Stage    A17 M17 R6 K5 T1 = 46/100
2 per Stage    A13 M15 R4 K5 T1 = 38/100
```

All-PERFECT: 5/5 classes through Stage49 for every variant.

Finding:
- one sparse body selectively trims the two strongest high-volume-clearing classes in this sample;
- two bodies become broad pressure and also hurt Rogue.

## Chronology sensitivity — run `39978274698`

```text
BASELINE  A18 M18 R6 K5 T1 = 48
EARLY     A16 M16 R6 K4 T1 = 43
MID       A17 M17 R6 K5 T1 = 46
LATE      A18 M16 R7 K5 T1 = 47
```

EARLY and MID both used band +2, so their difference is a chronology signal. Early insertion is too broad; midpoint is the cleanest directional center.

## Band sensitivity at MID — run `39978899281`

```text
BASELINE  A18 M18 R6 K5 T1 = 48
band -2   A16 M17 R6 K4 T1 = 44
band  0   A18 M17 R6 K5 T1 = 47
band +2   A17 M17 R6 K5 T1 = 46
```

All-PERFECT remained 5/5 in every variant.

Current reference only:

```text
one armored proxy
+ MID chronology
+ band +2
= cleanest tested selective diagnostic center
```

It is **not adopted content**.

Stop rule:

```text
DO NOT search finer proxy seconds/bands now.
Exact-coordinate search before real Tier authoring would overfit a temporary fixture.
```

---

# Stage48 evidence — parked, not discarded

User-approved exploration direction remains limited armored/hardened frontline + GRUNT-like cheap-target/fodder chronology.

Stable findings:
- real BRUTE/SHIELD-only screens did not buy enough SIEGER role time;
- spatial separation helps;
- excessive temporal lead can hurt;
- Mage chain chronology can reach later live targets;
- late GRUNT2 helps delay Mage access; GRUNT3 added little in tested band;
- SUPPORTER is secondary with phase risk;
- global SIEGER standoff movement is strongly disfavored as the primary repair.

No Stage48 packet is adopted.

---

# Current interpretation

The current evidence supports a broader causal model:

```text
SKILLED_V2 P×P frequency
× Lv31 package
× encounter family/composition
× formation/chronology/geometry
-> class-specific throughput/control/wall response
-> Stage outcome
```

High-volume clustered/aligned pressure naturally favors Mage/Archer identities. Sparse hardened bodies alter that response without requiring a class scalar change.

Therefore the next question is not “which class should be buffed?” but:

```text
which encounter families advantage/disadvantage each class,
and are those opportunities distributed intentionally across a Tier?
```

---

# Current work boundary

Active diagnostic:

**Encounter-composition class-response matrix**

Use existing evidence first for:
- FLOOD / high density;
- LINE / penetration;
- BULWARK / durable targets;
- control-sensitive pressure;
- protected SIEGE;
- chronology-sensitive Mage chain cases.

Goal:

```text
CLASS_NUMERIC_PROBLEM
vs
ENCOUNTER_COMPOSITION_ADVANTAGE
```

Only missing matrix cells should receive a new bounded simulation.

This diagnostic does not formally start P6.
Formal P6 Joint Run-Power Convergence still requires explicit user approval.

Do not begin exact Tier1 Stage1→50 authoring until the Tier availability/unlock ladder is explicitly selected.
