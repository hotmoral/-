# Timing Defense — P5 Rogue Dagger Storm Broad-Cleanup Breakpoint V0.1

Date: 2026-10-23 KST  
Status: **DIRECTIONAL BREAKPOINT CONFIRMED / IDENTITY GUARD ADDED / NO NUMERICAL FREEZE / NO PRODUCTION CHANGE**

Depends on:
- `91_P4D1_LV31_POWER_FANTASY_AND_STAGE46_MASTERY_GATE_APPROVED_CONTRACT_V0_1.md`
- `129_P5_CLASS_IDENTITY_RADAR_INVARIANT_GATE_V0_1.md`
- `131_P5_CLASS_IDENTITY_FIRST_DIRECTIONAL_RESULT_V0_1.md`
- `data/p5_class_identity_refinement_fixture_v0_1.json`

## 1. Current approved semantic remains

Dagger Storm:
- many real daggers;
- same target may absorb all remaining daggers while alive;
- after target death, remaining daggers may deterministically retarget to the nearest valid target;
- no same-target cap;
- no recursive proc tree.

This document does **not** remove retargeting or add a hidden target cap.

## 2. Breakpoint

Working dagger raw before shop:

```text
600 * 0.45 = 270
```

Diagnostic GRUNT HP:

```text
320
```

With the current P5 ATK mapping, one dagger reaches GRUNT one-shot at approximately:

```text
BALANCED atk8       -> shop scale >= 0.289352
ATTACK_HEAVY atk9   -> shop scale >= 0.257202
ROLE_AWARE Rogue10  -> shop scale >= 0.231481
```

Current common diagnostic center `0.40` is above all three thresholds.

At that point:

```text
one dagger kills one GRUNT
-> remaining dagger retargets
-> next GRUNT dies
-> repeated serial cleanup
```

A 16-dagger single-target execution package can therefore behave like practical broad-wave cleanup even though each projectile is still technically single-target.

## 3. Why this matters

Radar identity:

```text
Rogue: CRIT 5 / AGI 5 / PEN 1 / AOE 1
```

The problem is not that Dagger Storm can finish a wounded nearby enemy.
The problem is if late-run shop growth routinely converts the entire 16-dagger package into a one-dagger-per-body wave sweeper.

## 4. Identity guard

Add the following P5/P4-D2 guard:

```text
ROGUE_STORM_SINGLE_DAGGER_ORDINARY_ONESHOT_NOT_ROUTINE
```

Interpretation:
- under the intended late-run shop envelope, a fresh ordinary GRUNT-like body should not routinely require only one storm dagger;
- Dagger Storm should still annihilate durable targets through repeated hits;
- deterministic retargeting after death remains allowed;
- no exact max distinct-target count is frozen yet.

## 5. Repair order

If this guard fails in the integrated run:

1. inspect per-dagger damage × shop-ATK interaction;
2. inspect ordinary-monster HP breakpoints across the actual late roster;
3. inspect realized distinct-target count per storm;
4. only then consider changing storm coefficients;
5. do not remove approved retarget semantics as the first repair.

## 6. Current classification

```text
ROGUE_CORE_MULTIHIT_IDENTITY = PRESERVED
ROGUE_DURABLE_EXECUTION_IDENTITY = PRESERVED
ROGUE_BROAD_WAVE_CLEANUP_BREAKPOINT = CONFIRMED_DIRECTIONALLY
ROGUE_GRUNT_ONESHOT_WATCH = HIGH
RETARGET_SEMANTIC_CHANGE_AUTHORIZED = NO
NUMERICAL_FREEZE = NO
```
