# Timing Defense — P4-D2 First-Pass Lv31 Power Envelope & Pressure Targets V0.1

Date: 2026-10-23 KST  
Status: **FIRST-PASS ANALYTIC FEEDBACK / NO NUMERICAL FREEZE / P4-D2 CONTINUES**

Authority:
- `91_P4D1_LV31_POWER_FANTASY_AND_STAGE46_MASTERY_GATE_APPROVED_CONTRACT_V0_1.md`
- `92_P4D2_LV31_MASTERY_POWER_AND_STAGE46_PRESSURE_PREFLIGHT_V0_1.md`

---

# 0. Purpose

Translate the newly approved `strong final skill + strong Stage46 pressure` philosophy into a bounded first-pass power envelope before exact late-stage authoring.

This document does not freeze any production coefficient.

---

# 1. Rogue Dagger Storm — first quantitative bracket

Legacy/parity Lv21 Blade Barrage package:

```text
1.00 + 4 × 0.45 = 2.80 root-basis coefficient
```

P4-D2 candidate Dagger Storm counts if each projectile starts from the provisional `0.45` continuity coefficient:

| Dagger count | package coefficient | vs Lv21 2.80 package | boss-effective coefficient at 0.70 scalar |
|---:|---:|---:|---:|
| 12 | 5.40 | 1.93× | 3.78 |
| 16 | 7.20 | 2.57× | 5.04 |
| 20 | 9.00 | 3.21× | 6.30 |

Interpretation:
- 12 already gives a meaningful final-milestone jump;
- 16 creates a very clear final-skill escalation without using the maximum candidate;
- 20 is a deliberately aggressive upper bracket for power-fantasy / pressure-capacity testing;
- deterministic retargeting reduces overkill waste, so realized wave-clear value may approach the package coefficient more closely than a same-target-only calculation.

**Working P4-D2 center remains 16.**

No count or per-dagger coefficient is frozen.

---

# 2. Rogue event-volume engineering boundary

Bounded worst-case projectile counts for a future same-time all-Rogue team stress probe:

```text
4 Rogues × 12 = 48 projectiles
4 Rogues × 16 = 64 projectiles
4 Rogues × 20 = 80 projectiles
```

These counts are not by themselves a design failure.
They define an explicit future performance/stress target.

If runtime pressure appears later, investigate event batching / representation / VFX pooling / network payload strategy before reducing the class fantasy.

---

# 3. Revised provisional Lv31 magnitude brackets

Proposal 90 used intentionally conservative first ranges. Under approved document 91, P4-D2 may test a stronger envelope while keeping each class's geometry distinct.

## Knight — Heaven-Splitting Slash
Structural template remains two broad corridor waves.

First-pass power bracket for the second wave:

```text
0.75 / 1.00 / 1.25 of root outgoing basis
```

Reason:
- a final `double wave` should not read like one real wave plus a faint echo;
- the bounded corridor and penetration ceiling preserve Knight/Archer separation even when both passes are strong.

Knockback remains a separate sensitivity axis; do not compensate weak damage solely with uncontrolled knockback.

## Rogue — Dagger Storm

```text
12 / 16 / 20 projectiles
working center 16
provisional per-projectile continuity anchor 0.45
```

Per-projectile coefficient may later move if 16 projectiles is visually right but damage is not.
Do not conflate projectile count with coefficient tuning.

## Tank — Absolute Barrier
Control-first identity remains.

First-pass shockwave damage bracket may broaden to:

```text
0.50 / 0.75 / 1.00 of root outgoing basis
```

Strong battlefield knockback / wall barrier remain the primary fantasy; full root damage is now an allowed sensitivity endpoint rather than an automatic rejection.
The Tank should reset impossible pressure through control, not become Mage-style repeated global DPS.

## Archer — Sky-Piercing Arrow
Unlimited strict-line target count is already the main power multiplier.

Start with:

```text
1.00 root basis per intersected target
```

If Stage46+ aligned-pressure probes still undersell the final fantasy, test a higher per-target coefficient only after checking that line depth/formation is not the real limiting factor.
Do not add arbitrary target caps.

## Mage — Arcane Collapse
Keep bounded three-stage fixed-circle structure plus one final chain generation.

First-pass per-stage coefficient bracket:

```text
0.55 / 0.75 / 1.00 of root outgoing basis
```

This permits deliberately spectacular cluster deletion while keeping recursion finite.
Radius and stage coefficient must be varied separately so that `large area` is not hidden inside raw damage.

---

# 4. Stage46+ pressure targets — behavior before numbers

Do not freeze a raw monster-stat multiplier yet.
First calibrate the desired backlog/reset behavior.

## Stage46 power-revelation target

Without Lv31:
- normal Lv26 clearing capacity should be lower than sustained encounter inflow/pressure;
- monster backlog should grow over successive cycles;
- intended skilled players who enter without Lv31 may be buried.

With Lv31 + successful P×P:
- one final-skill event should create an unmistakable pressure reset;
- the player should visibly regain battlefield space/time;
- the reset should not permanently trivialize the rest of the Stage.

## Stage47
- require repeated successful pressure resets;
- one missed reset creates serious backlog but may remain recoverable.

## Stage48–49
- make P×P/combo maintenance itself a survival problem;
- repeated missed resets should usually create a burial cascade;
- formation/monster-role composition should matter, not only raw health.

## Stage50
- Lv31 is necessary power but not sufficient mastery;
- final application should combine class kit, run growth, combo/timing and encounter reading.

---

# 5. New pressure metrics for later simulation

Exact P4-D2 simulation should record:

```text
backlog_before_final
backlog_after_final
pressure_reset_fraction
seconds_to_reaccumulate_pre_reset_pressure
lv26_only_backlog_slope
lv31_backlog_slope_between_resets
missed_pxp_recovery_probability
consecutive_missed_pxp_to_burial
wall_hp_delta_between_resets
role_expression_count_before_death
```

A useful conceptual metric is:

```text
pressure_reset_fraction = 1 - post_final_threat / pre_final_threat
```

Do not freeze the exact acceptance percentage until the current-roster combat probe exists.

---

# 6. First-pass verdict

`16` Rogue projectiles is a defensible center for P4-D2:
- clearly stronger than Lv21;
- materially below the 20-projectile aggressive bracket;
- explicit/finitely bounded;
- strong enough to justify a real Stage46 pressure-regime transition;
- preserves the class's defining visual/mechanical appeal.

The broader Lv31 package should now be tested as a **deliberate late-run power spike**, not normalized downward before encounter pressure is given a chance to respond.

P4-D2 remains active.
No production gameplay changes or final numerical freeze are authorized.
