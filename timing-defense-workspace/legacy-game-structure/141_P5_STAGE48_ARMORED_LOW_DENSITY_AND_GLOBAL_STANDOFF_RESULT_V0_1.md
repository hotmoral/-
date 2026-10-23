# Timing Defense — P5 Stage48 Armored Low-Density / Global Standoff Result V0.1

Date: 2026-10-23 KST  
Status: **OBSERVED / DIAGNOSTIC RESULT / DECISION GATE / NO CANDIDATE ADOPTION / NO NUMERICAL FREEZE / NO PRODUCTION CHANGE**

Depends on:
- `137_P5_STAGE46_49_EXACT_EXECUTION_STAGE_SETTLED_BOUNDARY_RESULT_V0_1.md`
- `139_P5_STAGE48_SIEGER_PROTECTION_TIME_DIAGNOSTIC_V0_1.md`
- `140_P5_STAGE48_THREE_AXIS_COMPARISON_DECISION_GATE_V0_1.md`
- `129_P5_CLASS_IDENTITY_RADAR_INVARIANT_GATE_V0_1.md`
- `72_RUN_STATE_LIFECYCLE_APPROVED_CONTRACT_V0_1.md`
- `76_TEN_STAGE_PERSISTENT_RUN_KERNEL_APPROVED_CONTRACT_V0_1.md`
- `138_SESSION_BOOTSTRAP_COGNITIVE_REVIEW_AMENDMENT_V0_1.md`

Production remains unchanged and unauthorized for gameplay/numerical modification.

---

## 0. Plain-language result

The user proposed an important refinement:

> If only 2–3 armored-durable bodies are sent in front of SIEGER and their density is reduced, SIEGER should live longer, especially against Archer and Mage.

That direction is **partly confirmed**.

The decisive distinction is:

```text
LOWER SPATIAL DENSITY = useful
EXCESSIVE EARLY TEMPORAL SEPARATION = counterproductive
```

Keeping armored bodies close enough in time to SIEGER while separating their attack lines materially helps Archer and Knight. Sending them too early causes them to be consumed before SIEGER arrives.

However Mage remains special because its approved Lv31 bounded chain can select later live/unhit targets according to chronological live state. Spatial separation therefore does not protect SIEGER from Mage as strongly as it protects against Archer's strict-line penetration.

A hybrid diagnostic then showed that:

```text
limited armored low-density frontline
+ earlier SIEGER standoff
```

can create actual SIEGER firing in all five classes **inside Stage48**.

But applying the earlier standoff globally to SIEGER breaks Stage46–49 balance badly.
Therefore **global SIEGER standoff advancement is rejected as the current repair direction**.

The armored low-density axis remains promising and is not rejected.

---

## 1. UI stream error was not a repository rollback

During this work the user saw the ChatGPT UI message:

```text
메시지 스트림에 오류 발생
```

The live canonical GitHub branch was re-fetched afterwards and confirmed that the prior canonical writes persisted.
The error therefore did not roll back or corrupt the Timing Defense repository state.

The exact client/network/platform root cause cannot be proven from the screenshot alone; project evidence supports treating it as a response-stream/UI transport interruption rather than a repository/gameplay error.

---

## 2. Armored-candidate purpose — preserve this intent

`ARMORED_DURABLE_PROXY` originated as a diagnostic body, but the user clarified the broader design motivation for the armored/hardened axis:

1. late-game Mage/Archer can erase ordinary volume waves too quickly;
2. SIEGER needs enough protected role time to become meaningful;
3. a limited heavy frontline/elite/hardened package may address both without globally nerfing Mage/Archer.

This is **design intent**, not approval of a tenth ordinary monster or of the old proxy values.

The old repeated proxy Stage48 packet remains rejected.

---

## 3. Low-density temporal/spatial diagnostic

Temporary run:

```text
run id 39960227005
```

The existing proxy anchor was retained only as a diagnostic upper-bound body:

```text
HP 1600
armor multiplier 0.55
knockResist 0.65
speed 0.04
wall 160
```

No class/monster/shop value was adopted or changed.

### Finding: sending the bodies too early is counterproductive

Previous two-body reference:

```text
armored t=6.0 / t=7.0
SIEGER t=8.0
```

Representative SIEGER lifetime after spawn:

```text
Knight 2.325 s
Rogue 2.350 s
Tank   5.700 s
Archer 6.825 s
Mage   7.200 s
```

When the armored bodies were sent much earlier and spread farther in time, Mage and Archer did not improve; several cases regressed.

Cause:
- the lead armored body becomes attackable earlier;
- it is partially/fully consumed before SIEGER arrives;
- temporal separation reduces simultaneous density but also destroys the intended protection handoff.

Therefore:

```text
LOW_DENSITY != SEND_ESCORTS_ARBITRARILY_EARLY
```

---

## 4. Spatial-density isolation result

Temporary run:

```text
run id 39960432880
```

Timing was kept near the SIEGER arrival while only the band geometry was spread.

### Two-body reference

```text
armored: t6 band -1
a​rmored: t7 band +1
SIEGER:  t8 band +2
```

### Two-body spatial low-density

```text
armored: t6 band -2
armored: t7 band  0
SIEGER:  t8 band +2
```

SIEGER lifetime/death position changed approximately:

```text
Knight: 2.325 s / x~0.815 -> 4.575 s / x~0.730
Rogue:  2.350 s / x~0.814 -> 2.350 s / x~0.814
Tank:   5.700 s / x~0.745 -> 5.700 s / x~0.745
Archer: 6.825 s / x~0.613 -> 9.075 s / x~0.512
Mage:   7.200 s / x~0.596 -> 7.200 s / x~0.596
```

This strongly confirms the user's geometry hypothesis for Archer and also materially helps Knight.

Mage does not gain the same protection because Mage's approved package is not a simple straight-line collision model.

---

## 5. Why Mage behaves differently

The current approved/provisional Mage Lv31 structure supports a bounded final chain after Arcane Collapse.
Its chronological target semantics can select live enemies not already hit by the package, including targets that become live later in the sequence when eligible.

Observed Stage48 evidence included SIEGER taking damage almost immediately after spawn in some dense three-body cases, consistent with an already-running delayed Mage package/chain reaching the new live target.

Therefore:

```text
ARCHER SCREENING PROBLEM = strongly geometry/line sensitive
MAGE SCREENING PROBLEM = geometry + chronological package/chain sensitive
```

Changing Mage's chain semantics silently is not authorized and would reopen an approved class package.

---

## 6. Hybrid diagnostic fidelity defect found and fixed

First hybrid run:

```text
run id 39960854218
```

was internally inconsistent: prior death-position evidence showed SIEGER surviving past x=0.78 in some classes, yet the hybrid run reported zero windups.

Root cause was diagnostic code, not gameplay:

1. STAGE_SETTLED fixed-schedule hook was installed on the current `SIMULATE` function;
2. standoff sensitivity then dynamically rebuilt and replaced `SIMULATE`;
3. the new function had a fresh globals namespace whose `build_integrated_schedule` did not contain the fixed-schedule hook;
4. the intended armored/SIEGER packet could therefore be lost/fall back during the Stage-settled path.

Fix:
- rebuild threshold-specific `SIMULATE`;
- install the fixed Stage-owned authored schedule hook directly into that exact rebuilt function's globals;
- assert the actual Stage48 schedule equals the expected schedule.

Corrected run:

```text
run id 39961261476
```

All corrected rows reported:

```text
scheduleMatchesExpected = true
```

The invalid first hybrid result must not be used for balance interpretation.

---

## 7. Corrected Stage48 hybrid result

Formation A — two armored bodies, spatially separated:

```text
armored t6.0 band -2
armored t7.0 band  0
SIEGER  t8.0 band +2
```

At standoff x=0.78:

```text
Knight 2 shots
Rogue  0 shots
Tank   1 shot
Archer 2 shots
Mage   2 shots
```

At standoff x=0.82:

```text
Knight 2 shots
Rogue  0 shots (1 windup)
Tank   2 shots
Archer 3 shots
Mage   2 shots
```

Formation B — three armored bodies, spatially separated:

```text
armored t5.25 band -2
armored t6.25 band  0
armored t7.25 band -1
SIEGER  t8.00 band +2
```

At standoff x=0.78:

```text
Knight 1 shot
Rogue  1 shot
Tank   2 shots
Archer 2 shots
Mage   0 shots (1 windup)
```

At standoff x=0.82:

```text
Knight 2 shots
Rogue  1 shot
Tank   2 shots
Archer 2 shots
Mage   1 shot
```

This was the first bounded Stage48 packet in this search to produce actual SIEGER firing for all five classes.

But this is **not enough to adopt x=0.82**, because standoff is a monster-wide property unless a separate rule is approved.

---

## 8. Stage46→49 global-standoff consistency replay

Temporary full-chain run:

```text
run id 39961496878
```

Method:
- Stage48 uses the three-body spatial low-density single protected pulse above;
- wall deficit carries across Stages;
- every Stage drains to `STAGE_SETTLED`;
- four representative shop profiles × five classes = 20 cases per threshold;
- Tank uses diagnostic center 0.25 only;
- SIEGER standoff threshold is applied globally across Stage46–49.

### Control x=0.38

```text
20 / 20 settle through Stage49
0 buried
Stage48 SIEGER shots across all classes = 0
```

This remains too weak for intended Stage48 SIEGER expression, but it preserves the current chain.

### Global x=0.78

```text
13 / 20 settle through Stage49
7 buried
```

Aggregate Stage48 SIEGER shots by class across four representative profiles:

```text
Knight 5
Rogue  4
Tank   8
Archer 8
Mage   0
```

Total Stage46–49 SIEGER shots become very large for some classes, especially Tank and Archer.
Stage49 becomes a major failure point.

### Global x=0.82

```text
8 / 20 settle through Stage49
12 buried
```

Aggregate Stage48 SIEGER shots by class across four profiles:

```text
Knight 8
Rogue  4
Tank   8
Archer 8
Mage   4
```

Stage48 role expression is better, but Stage46/47 wall attrition and Stage49 pressure become excessive.

Representative failures include:
- Knight profiles losing large wall reserve before Stage48 and some burying in Stage49;
- Archer profiles repeatedly burying in Stage49;
- Tank often generating extremely high SIEGER shot counts in Stage49 because its intentionally low removal throughput allows the SIEGER group to remain active;
- Mage often survives but receives materially more wall pressure.

Therefore:

```text
GLOBAL_STANDOFF_X_0_78 = NOT ADMISSION READY
GLOBAL_STANDOFF_X_0_82 = REJECT AS CURRENT REPAIR DIRECTION
```

The exact numeric standoff remains unfrozen.
This does not freeze x=0.38 either; it only rejects the large global advancement as the current repair.

---

## 9. Three-axis comparison after the new evidence

### A. Existing BRUTE/SHIELD only

Pros:
- simplest;
- no roster/mechanic expansion.

Cons:
- insufficient protected time;
- repeatedly failed to create SIEGER role uptime in tested families;
- does not address late Mage/Archer volume-erasure strongly enough.

Current classification:

```text
INSUFFICIENT AS PRIMARY REPAIR
```

### B. Limited armored/hardened frontline axis

Pros:
- materially extends SIEGER life, especially against Archer;
- directly addresses the user's broader late-game volume-erasure concern;
- can be limited to small counts rather than repeated proxy spam;
- preserves the possibility of class asymmetry instead of globally nerfing Mage/Archer.

Cons:
- old proxy numbers are not production-ready;
- too many or badly timed armored bodies can worsen Mage interaction;
- does not by itself reach the current x=0.38 siege line reliably;
- exact identity remains open: elite recipe, hardened variant, temporary state, or another bounded mechanism.

Current classification:

```text
MOST PROMISING CURRENT EXPLORATION AXIS
NOT YET SUFFICIENT / NOT ADOPTED
```

### C. Global SIEGER standoff advancement

Pros:
- very effective at making SIEGER fire in Stage48.

Cons:
- global property changes Stage46/47/49 as well;
- x=0.78 and 0.82 create severe cross-stage overpressure;
- conflicts with Stage46 power-revelation / Stage47 recovery intent;
- especially dangerous for Tank because low removal throughput turns repeated SIEGER uptime into extreme shot counts.

Current classification:

```text
REJECT AS CURRENT GLOBAL REPAIR DIRECTION
```

### D. Buff/resistance/skill-like monster mechanics

The user explicitly allows later consideration of:
- buffs;
- resistances;
- skill-like monster states.

These remain valid future design space but introduce additional coupling:
- class-skill interactions;
- penetration/AoE/knockback/control policy;
- readability/telegraphing;
- effect stacking;
- encounter authoring frequency;
- reward/economy;
- elite/boss distinction;
- server-authoritative state;
- future meta/multiplayer implications.

Therefore they remain **deferred until the simpler armored-frontline axis is exhausted or shown insufficient**.

---

## 10. Decision gate — do not silently adopt

The next important decision is now narrower:

> Should P5 Stage48 exploration adopt the **limited armored/hardened frontline axis as the primary working direction**, while keeping the global SIEGER standoff behavior unchanged for now and treating any buff/resistance mechanic as a later fallback?

Recommended answer from current evidence:

```text
YES — adopt the AXIS for further bounded design exploration,
NOT the old proxy monster,
NOT HP1600/armor0.55 as production values,
NOT the exact 2/3-body packet,
NOT x=0.78/0.82,
NOT a tenth ordinary monster yet.
```

If the user approves this exploration direction, the next bounded work should be:
1. keep SIEGER global standoff at the current diagnostic baseline while it remains unfrozen;
2. design a **limited late-game hardened-frontline envelope** rather than repeating the old proxy;
3. search the smallest stat/placement envelope that delays Archer/Mage volume erasure without burying Mage or creating a Knight hard counter;
4. test whether 2–3 hardened bodies can make Stage48 role pressure meaningful through durability/spacing alone;
5. only if that still cannot solve Mage chronology, then open a separate user-approved buff/resistance/elite-mechanic design gate;
6. after a promising Stage48 packet exists, replay Stage46→49 with STAGE_SETTLED and re-check class identities/shop/EXP feedback.

No step above authorizes production or numerical freeze.

---

## 11. Classification

```text
ARMORED_LOW_SPATIAL_DENSITY_CAUSAL = YES
EXCESSIVE_TEMPORAL_LEAD_CAUSAL_REPAIR = NO
MAGE_CHAIN_CHRONOLOGY_RELEVANT = YES
FIRST_HYBRID_RUN_VALID = NO
HYBRID_FIXED_SCHEDULE_FIDELITY = PASS
ARMORED3_SPATIAL_PLUS_X0_82_STAGE48_ALL_CLASS_ROLE_EXPRESSION = YES
GLOBAL_X0_78_CHAIN_ADMISSION = FAIL
GLOBAL_X0_82_CHAIN_ADMISSION = FAIL
GLOBAL_STANDOFF_ADVANCEMENT_PRIMARY_REPAIR = REJECT
LIMITED_ARMORED_HARDENED_FRONTLINE_AXIS = PROMISING_DECISION_GATE
BUFF_RESISTANCE_MECHANICS = OPEN_FUTURE_FALLBACK_NOT_YET_OPENED
NEW_MONSTER_OR_ELITE_APPROVED = NO
NUMERICAL_VALUE_FROZEN = NO
PRODUCTION_CHANGE = NONE
AWAITING_USER_DECISION = YES
```
