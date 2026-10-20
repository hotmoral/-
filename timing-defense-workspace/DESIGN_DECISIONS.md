# Timing Defense — Design Decisions

## Core combat
- Primary input is timing, not free movement.
- One-square rhythm: `X → X → X → X+Y`.
- Fourth attack is charged/heavy and must feel substantially stronger.
- P×P on heavy = CRITICAL.
- Tap-anywhere remains the intended control model.

## Class roles
The classes solve different combat problems rather than converging to identical DPS.

### Knight
Generalist / stable frontline / penetration / strong heavy.
Should be consistently useful without owning a specialist benchmark.

### Rogue
Fast multihit / crit / high-HP normal execution.
- No same-target dagger hit cap.
- Repeated impacts are core to class feel.
- Boss dagger damage scalar starting value: `0.70`.

### Tank
Knockback / wall protection / battlefield control.
- Explicit team-specialist.
- Fresh-run solo Stage-10 parity is not required.
- Future permanent/meta stats may make solo completion practical.
- Boss knockback scalar starting value: `0.40`.

### Archer
Straight-line penetration / rear-target access / long-range pressure.
- Arrow continues only on its current trajectory.
- Only hitboxes intersecting that line may be penetrated.
- No homing, retargeting or automatic next-target chaining.

### Mage
Area damage / dense-pack deletion / chained explosions.
Should become stronger with density, not a top single-target boss killer.

## Balance philosophy
Do not normalize all classes to equal DPS or equal solo clear rate.
Evaluate by role:
- Rogue: durable-normal TTK.
- Archer: line-pack clear / rear pressure.
- Mage: dense-cluster clear.
- Tank: wall preservation / control / team utility.
- Knight: general-purpose consistency.

## Player mastery
Simulation reference:
- Average = N25 / G55 / P20.
- Skilled = N10 / G50 / P40 plus modestly faster commitment.

Skilled is treated as an attainable learned-player state, not an extreme expert state. Strong Average→Skilled improvement is desirable and must not automatically trigger nerfs.

## EXP philosophy
- EXP remains tied to timing attack results/events.
- Faster-killing classes are not compensated simply because they perform fewer attacks and therefore may level more slowly.
- Different growth pace is accepted as part of overall run balance unless a concrete progression failure appears later.
- Passive auto-attacks, if enabled, do **not** grant EXP.

## Balance-change governance
Simulation is diagnostic first.

Required order:
`model/simulate → identify cause or model artifact or intentional specialization → report → discuss → explicit decision → live patch`

A large measured gap never self-authorizes a balance change.

---

# Encounter-pressure philosophy

## Pressure families
- `S` Swarm — temporary high-count pressure.
- `E` Elite/Heavy — one/few unusually durable threats.
- `X` Special/Mixed — speed, flight, shield, split or other disruptive compositions.

`X` is the primary co-op scaling language. `S` and `E` are time-separated spike tools.

## Stage grammar
A stage may use one, two or all three pressure families. Do **not** force S+E+X into every stage.

A 50-stage tier receives identity through:
- 1/2/3-pattern stage proportions,
- S/E/X frequency,
- internal pair/triple ratios,
- early/mid/late/final timing,
- formation geometry,
- duration/intensity,
- overlap frequency.

Higher tier does not automatically mean more active pattern types. A high tier may return to focused 1-pattern stages with much stronger intensity.

Three-pattern stages remain a minority globally so they retain a chaos/event identity.

## Geometry is gameplay data
- line pressure creates Archer opportunities,
- dense cluster creates Mage opportunities,
- durable anchors create Rogue opportunities,
- split/special leakage creates Tank opportunities,
- awkward transitions preserve Knight generalist value.

## Concrete recipe candidate after v6
See `PRESSURE_RECIPES_V1.md`.

### Swarm burst counts
- S-line: 2P/3P/4P = `8 / 11 / 14`.
- S-cluster: `7 / 10 / 13`.
- S-scatter: `9 / 12 / 16`.

Do not solve 4-player difficulty by dumping 20–30 ordinary enemies into every spike.

### Special/mixed scaling
Additional players primarily add role-bearing anchors and disruptive composition:
- extra SHIELD / BRUTE anchors,
- more RUNNER / FLYER pressure,
- split geometry,
- event-budget density.

Avoid one flat global all-monster HP multiplier.

### Elite durability
Treat E as an **effective durability budget**, not permission to create one absurd health bar.
Distribute the budget through moderate HP, armor, an extra durable target and type/timing composition.

### Readability envelope
Current candidate structural calibration across 250 prototype stages per team-size model keeps approximately:
- 2P P95 4-second spawn burst ≈ 11,
- 3P ≈ 15,
- 4P ≈ 18.

This is an authoring/reference envelope, not a permanent engine cap. Exceptional chaos stages may deliberately exceed it after human visual testing.

---

# Auto-attack direction — approved concept, numbers not frozen

Purpose: let the player briefly read the battlefield without combat going completely idle, while timing remains the overwhelmingly dominant source of power.

Candidate first experiment from v8:
- passive/basic attack every ~2.0 s,
- raw damage around `40` (40% of no-skill NORMAL timing hit),
- no crit/proc-crit,
- no skill trigger,
- no charge generation,
- no PERFECT combo contribution,
- no EXP,
- minimal/zero knockback.

Do not compensate enemy HP 1:1 for the full passive contribution. The passive system must create a small amount of real breathing room.

Current leading test envelope:
- auto = 40 / 2.0 s,
- ordinary-monster HP compensation ≈ +8% candidate,
- boss/elite compensation evaluated separately.

These are test values only, not frozen production balance.

---

# Consecutive PERFECT combo — approved direction

## Counter rule
- Only PERFECT increments combo.
- GOOD / NORMAL / MISS reset combo to zero.
- Attacks 1–3 can each add +1.
- Heavy X and heavy Y can each add +1.
- Therefore a fully PERFECT 1→4 sequence adds **5 combo**.
- Combo is **unbounded**: 20, 30, 40, 50+ remain valid.
- Reaching a milestone never consumes/resets the counter.
- Stage/shop downtime does not itself break combo; only a non-PERFECT timing judgment does, unless later explicitly changed.

## Psychological-pressure rule
The rising visible streak is itself part of the difficulty.

Do **not** secretly make timing harder at high combo:
- no shrinking PERFECT window,
- no sweep acceleration,
- no hidden accuracy penalty.

The intended tension is: the player sees a valuable 20/30/40 streak, becomes increasingly conscious of what can be lost, and is more likely to make a genuine input mistake.

## Visual escalation
Candidate ladder:
- 1–4: small persistent number,
- 5–9: combo value begins appearing at the struck monster,
- 10–19: larger number/pulse,
- 20–29: stronger class-color impact feedback,
- 30+: maximum visual tier may plateau, but the numeric counter continues indefinitely.

## Mechanical reward
Mechanical reward values are not frozen.
Prefer milestone-triggered one-off class rewards over an indefinitely stacking permanent damage multiplier.

Test milestones:
- 5,
- 10,
- 20,
- 30,
- then every +10 while the counter continues.

Class reward language should preserve identity:
- Knight: extra blade/frontline break,
- Rogue: dagger burst,
- Tank: shockwave/protection,
- Archer: extra straight-line shot,
- Mage: secondary explosion.

See `BALANCE_SIM_REPORT_V8_AUTO_COMBO.md`.

---

## UI hierarchy
- Charge stack above Timing Square.
- Learned skill icons below Timing Square.
- EXP gauge immediately right of Timing Square.
- No permanent skill-name text beside EXP.
- Timing Square renders above monsters.
- Between timing attacks, the Timing Square should remain visible at reduced opacity instead of disappearing, so charge/location remain continuously readable.

## Team presentation
- AI teammates do not receive visible Timing Squares.
- AI internally receives timing results, EXP, levels and automatic class skill unlocks.
- AI progression is independent state, intended to be a closer stand-in for future human teammates.
- Four-character vertical spacing should be slightly wider than v0.16 so full silhouettes/weapons remain readable.

## Class color language
- Knight: gold / bright steel.
- Rogue: charcoal / silver / minimal red accent.
- Tank: blue / dark steel.
- Archer: green.
- Mage: purple.

The palette propagates through character clothing, weapons, projectiles, Timing Square, EXP gauge, skill icon and impact VFX.
