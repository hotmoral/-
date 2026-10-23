# Timing Defense — P6 Encounter-Family Rotation & Tank Objective Attribution Result V0.1

Date: 2026-10-24 KST  
Status: **P6-A DIAGNOSTIC COMPLETE / ENCOUNTER-FAMILY ROTATION CONFIRMED / TANK MASTERY-PACKAGE WATCH ISOLATED / NO NUMERICAL FREEZE / NO PRODUCTION CHANGE**

Depends on:
- `150_P6_STAGE46_47_FIRST_CAUSAL_CONVERGENCE_RESULT_V0_1.md`
- `147_ENCOUNTER_COMPOSITION_CLASS_RESPONSE_MATRIX_V0_1.md`
- `135_P5_CLASS_IDENTITY_GROUP_DIRECTIONAL_CLOSURE_V0_1.md`
- `132_P5_TANK_CONTROL_CLEAR_PARETO_DIRECTION_V0_1.md`
- `91_P4D1_LV31_POWER_FANTASY_AND_STAGE46_MASTERY_GATE_APPROVED_CONTRACT_V0_1.md`
- `88_P4C1_LV26_STRUCTURAL_SKILL_APPROVED_CONTRACT_V0_1.md`

Production gameplay remains unchanged and unauthorized.

---

## 1. Plain-language result

The approved P6-A question is answered:

> Does the apparent class power order rotate when the encounter family changes while player-power, mastery, shop and run-state semantics are held fixed?

**Yes.**

The current Stage46–47 dense/aligned pressure is not a neutral class-power ranking surface.
Changing only the encounter family materially rotates the class ordering without changing class scalars.

Reference Stage46–47 BALANCED baseline from P6-S1:

```text
Mage 19/20
Archer 19/20
Rogue 9/20
Knight 7/20
Tank 2/20
```

20-seed alternate-family confirmation:

```text
DURABLE_DISTRIBUTED
Knight 20/20
Mage   20/20
Archer 20/20
Rogue  17/20
Tank    3/20

CHARGER_CONTROL_SCREENED
Knight 20/20
Archer 20/20
Rogue  18/20
Mage   18/20
Tank    3/20
```

Therefore:

```text
CLASS_RANKING_IS_ENCOUNTER_FAMILY_DEPENDENT = CONFIRMED
CURRENT_DENSE_ALIGNED_RANKING != UNIVERSAL_CLASS_POWER_ORDER
```

This strengthens the existing encounter-opportunity framework and argues against equalizing classes from one late pressure recipe.

---

## 2. Execution evidence

Temporary branch:
`timing-defense-workspace-temp-p6-pressure-family`

### 5-seed family preflight
Informative final preflight run:
```text
40023824300
```
Exact-byte repeat PASS.
SHA256:
```text
b7f8c1a3886985f334d1f635b9f1fd579732a510d0c80249c04c01a0596fed80
```

Preflight descriptive ordering:
```text
BASELINE_DENSE_ALIGNED      Mage > Archer > Rogue > Knight > Tank
DURABLE_DISTRIBUTED         Knight > Mage > Archer > Rogue > Tank
CHARGER_CONTROL_SCREENED    Knight > Archer > Rogue > Mage > Tank
```

### 20-seed confirmation
Run:
```text
40023996992
```
Commit:
```text
3d15a68b882e10676115ebf753ea44eacce1e78a
```
Exact-byte repeat PASS.
SHA256:
```text
cfc653db6a8a033e625b8222c45b5d5332a72ade26540e4879e71fce57851e85
```

Screen:
- BALANCED shop fixed;
- SKILLED_V2_CENTRAL;
- 20 deterministic seeds;
- five classes;
- Stage46→47;
- persistent judgment/combo/charge;
- Heavy X/Y;
- P×P-only Lv31 final;
- STAGE_SETTLED;
- wall current/max/absolute deficit carry;
- normal right-edge entry;
- current class and monster anchors;
- no production values changed.

Baseline was not rerun because P6-S1 already had 20-seed BALANCED authority.

---

## 3. Family normalization boundary

The alternate families were diagnostic compositions, not production Stage authoring.
They were intentionally given gross effective-HP/contact-wall budgets near the current baseline while changing body count, role mix and geometry.

Stage46 gross diagnostic budgets:

```text
BASELINE_DENSE_ALIGNED
126 bodies / effective HP 50,175 / nominal contact-wall 11,670

DURABLE_DISTRIBUTED
75 bodies / effective HP 48,000 / nominal contact-wall 10,350

CHARGER_CONTROL_SCREENED
80 bodies / effective HP 49,600 / nominal contact-wall 11,200
```

This does not make the families numerically equivalent.
It only prevents interpreting the rotation as the trivial result of replacing the baseline with a tiny low-pressure packet.

No packet is adopted as Tier1 content.

---

## 4. Tank remained the exception

Across the three tested surfaces:

```text
BASELINE              2/20
DURABLE_DISTRIBUTED   3/20
SCREENED_CHARGER      3/20
```

Yet ALL_PERFECT retained a clear path in every tested Tank control.

This required a separate source-fidelity and package-attribution check before any scalar conclusion.

### 4.1 Aftershock source-fidelity mismatch found

Approved Lv26 semantics define the Aftershock Zone center as:

```text
authoritative primary Ground Impact location
```

The diagnostic runner instead appended the zone after knockback and used the target's post-push `x` position.

A temporary fidelity-corrected runner moved the zone center back to the pre-push impact location.

Result on SCREENED_CHARGER, 20 skilled seeds:

```text
SOURCE_CURRENT       3/20, Stage46 mean wall loss ~1507.6
FIDELITY_CORRECTED   3/20, Stage46 mean wall loss ~1502.1
```

So:

```text
AFTERSHOCK_CENTER_MISMATCH = REAL DIAGNOSTIC FIDELITY DEFECT
AFTERSHOCK_CENTER_MISMATCH != PRIMARY_TANK_FAILURE_CAUSE
```

This does not claim a production bug; the mismatch was in the planning diagnostic runner.

### 4.2 Existing Tank defensive/control components are functional

Corrected-runner paired ablations, SCREENED_CHARGER:

```text
FULL CORRECTED        3/20, Stage46 wall loss ~1502
NO PUSH               2/20, +244 wall loss
NO ALL BARRIERS       2/20, +172 wall loss
NO LV31 BARRIER       2/20,  +63 wall loss
NO AFTERSHOCK SLOW    3/20,  +59 wall loss
NO IRON WALL          2/20,  +50 wall loss
```

Run:
```text
40024651146
```
Exact-byte repeat PASS.
SHA256:
```text
fd0a2be4880fd76f00b7db44af5d9ae450bd9b78db0aae6c6362f1188c72603c
```

Interpretation:
- push materially protects the wall;
- barriers materially protect the wall;
- Iron Wall materially protects the wall;
- Aftershock slow has a smaller but measurable effect;
- the problem is not that Tank's defensive kit is absent or inert.

---

## 5. Existing Tank 0.20 / 0.25 / 0.30 bracket does not repair the boundary

The already-authorized diagnostic bracket from doc132 was rerun on the Aftershock-corrected runner.

Run:
```text
40024845146
```
Exact-byte repeat PASS.
SHA256:
```text
b0b36d4e2a1e1471ba0601bcf526e675a563c3f5efb22e78b8863a479a3a709f
```

### SCREENED_CHARGER
```text
0.20 -> 2/20, Stage46 wall loss ~1675, maxActive ~24.3
0.25 -> 3/20, Stage46 wall loss ~1502, maxActive ~22.3
0.30 -> 3/20, Stage46 wall loss ~1462, maxActive ~20.9
```

### DURABLE_DISTRIBUTED
```text
0.20 -> 3/20, Stage46 wall loss ~1590, maxActive ~24.9
0.25 -> 3/20, Stage46 wall loss ~1464, maxActive ~23.3
0.30 -> 3/20, Stage46 wall loss ~1363, maxActive ~22.2
```

ALL_PERFECT cleared every tested coefficient/family control.

Therefore:

```text
TANK_0P20_0P30_SHOCKWAVE_SCALAR = MATERIAL_FOR_BACKLOG/RESERVE
TANK_0P20_0P30_SHOCKWAVE_SCALAR != PRIMARY_CURRENT_COMPLETION_BOUNDARY
```

Do not select 0.30 merely to raise the current clear rate.
No Tank scalar is frozen.

---

## 6. Refined Tank causal classification

Current evidence supports the following chain:

```text
Tank intentionally low removal
-> live backlog accumulates
-> push / slow / Iron Wall / barriers delay or absorb pressure
-> survival becomes disproportionately dependent on sufficiently frequent
   P×P Absolute Barrier battlefield reset windows
-> central-skilled P×P frequency often cannot reset backlog before wall collapse
-> all-perfect retains a clear path
```

This is consistent with prior factor isolation where forcing Heavy P×P while keeping ordinary central judgments removed the Stage46–47 failure surface across all classes.

The current watch is therefore not:

```text
"Tank control is broken"
```

and not:

```text
"0.25 must be increased"
```

It is:

```text
TANK_MASTERY_PACKAGE_TO_OBJECTIVE_CONVERSION_WATCH
```

The product question later is whether Tank is intended to be this disproportionately dependent on P×P final-package frequency in the late mastery band while still advertising control/wall-protection identity.
That is a design decision, not something this diagnostic may silently repair.

---

## 7. P6-A closure

The approved A objective is complete enough to stop additional family microtuning.

Closed conclusions:

```text
ENCOUNTER_FAMILY_ROTATES_CLASS_RESULTS = YES
DENSE_ALIGNED_BASELINE_IS_NOT_NEUTRAL = YES
CLASS_EQUALIZATION_FROM_ONE_PACKET = REJECTED
TANK_CONTROL/DEFENSE_COMPONENTS_FUNCTIONAL = YES
AFTERSHOCK_CENTER_DIAGNOSTIC_MISMATCH = REAL_BUT_NONPRIMARY
0.20/0.25/0.30_TANK_SCALAR = NOT_PRIMARY_COMPLETION_REPAIR
```

Open watch:
```text
TANK_MASTERY_PACKAGE_TO_OBJECTIVE_CONVERSION_WATCH
```

No exact encounter quota, Tier1 family distribution, Tank scalar, P×P rate or class buff/nerf is approved.

---

## 8. Next approved work boundary

Per the user-approved sequence:

```text
P6-A encounter-opportunity convergence
-> P6-B progression-relevant shop / timing-event / EXP / skill-reach feedback
-> Tier count + monster availability candidate
-> exact Tier1 authoring later
```

Proceed to P6-B without changing Tank numbers.
Carry the Tank mastery-package watch forward so later progression/player-power convergence does not accidentally hide it.
