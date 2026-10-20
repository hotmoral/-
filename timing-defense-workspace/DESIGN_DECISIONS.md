# Timing Defense — Design Decisions

## Core combat
- Primary input is timing, not free movement.
- One-square rhythm: `X → X → X → X+Y`.
- Fourth attack is charged/heavy and must feel substantially stronger.
- P×P on heavy = CRITICAL.
- Tap-anywhere remains the intended control model.

## Target visibility / turn-boundary integrity
- A monster may be targeted/damaged only after its aim point enters the visible viewport.
- Spawning beyond the right edge does not make an enemy targetable.
- Local, AI, passive, pierce and AoE damage obey the same visibility rule.
- Unseen/off-screen kills must not award rewards.
- Attack input must not force-spawn an invisible target.

### Timing-turn gating
- A **new** Timing Square turn starts only while a valid visible enemy exists.
- If no visible target exists at the next-turn boundary, the square pauses in a waiting state and does not sweep.
- Passive and AI attacks also wait rather than attacking empty space or generating progression.
- Empty timing turns must not generate EXP.

### In-progress turn continuity
Once a timing turn begins with a visible target, that whole turn is locked as valid.

If the final visible target disappears because of AI/passive/team damage while the needle is moving:
- do **not** cancel or snap-stop the current turn,
- normal X may still be tapped,
- fourth-attack X must still be allowed to continue into Y,
- the full X→Y sequence may finish,
- that already-valid turn may still resolve its normal timing judgment/EXP,
- only the following turn waits if no target is visible.

Reason: cancelling mid-turn due to teammate kills can look like latency, dropped input, or an unresponsive Timing Square.

Target-wait itself does **not** break PERFECT combo. Only an actual non-PERFECT timing judgment breaks it.

Stage-clear/shop/final-clear transition should wait for an already-valid local timing turn to finish or naturally time out.

---

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
- EXP remains tied to valid timing attack results/events.
- Faster-killing classes are not compensated merely because they perform fewer attacks.
- Passive auto-attacks do **not** grant EXP.
- A turn that was valid when started may still grant its normal timing EXP if the target disappears during that same turn.
- A turn must not start solely to farm EXP while no visible target exists.

## Balance-change governance
Required order:
`model/simulate → identify cause/artifact/intentional specialization → report → discuss → explicit decision → live patch`

A large measured gap never self-authorizes a numerical change.

---

# Encounter-pressure philosophy

## Pressure families
- `S` Swarm — temporary high-count pressure.
- `E` Elite/Heavy — one/few unusually durable threats.
- `X` Special/Mixed — speed, flight, shield, split or other disruptive compositions.

`X` is the primary co-op scaling language. `S` and `E` are time-separated spike tools.

## Stage grammar
A stage may use one, two or all three pressure families. Do **not** force S+E+X into every stage.

A 50-stage tier gets identity through:
- 1/2/3-pattern proportions,
- S/E/X frequency,
- pair/triple ratios,
- early/mid/late/final timing,
- geometry,
- duration/intensity,
- overlap frequency.

Higher tier does not automatically mean more pattern types; focused one-pattern stages may return with much stronger intensity.

## Concrete pressure candidates
- S-line 2P/3P/4P = `8 / 11 / 14`.
- S-cluster = `7 / 10 / 13`.
- S-scatter = `9 / 12 / 16`.

Current reference P95 four-second spawn density:
- 2P ≈ 11,
- 3P ≈ 15,
- 4P ≈ 18.

X carries most multiplayer scaling through role-bearing composition. E is an effective durability budget rather than one giant HP sponge.

---

# Auto-attack direction — approved concept, numbers not frozen

Purpose: let the player briefly read the battlefield without combat going completely idle while timing remains dominant.

Semantic rules:
- fires independently only while a valid visible combat target exists,
- no timing judgment,
- no crit/proc-crit,
- no skill trigger,
- no charge,
- no PERFECT combo contribution,
- no EXP,
- minimal/zero knockback.

Leading A/B candidate:
- passive = `40 raw / 2.0 s`,
- ordinary non-boss HP compensation = about `+10%`,
- bosses/elites calibrated separately.

Do not compensate passive damage 1:1; some real breathing room is intentional.

---

# Consecutive PERFECT combo

## Counter rule
- Only PERFECT increments.
- GOOD / NORMAL / MISS reset to zero.
- Attacks 1–3 can each add +1.
- Heavy X and heavy Y can each add +1.
- Fully PERFECT 1→4 sequence adds 5 combo.
- Counter is unbounded: 20 / 30 / 40 / 50+.
- Milestones never consume/reset the streak.
- Stage/shop/target-wait downtime does not itself break combo.

## Psychological-pressure rule
High visible streaks should make the player nervous naturally.
Do **not** secretly shrink the timing window, accelerate sweep speed, or apply hidden accuracy penalties at high combo.

## Presentation
- Show from `1 COMBO` so the player never has to count manually.
- Primary location is near Timing Square.
- Do not keep a permanent boxed HUD.
- Every PERFECT produces a short tilted punch/scale popup, then fade-out.
- Visual strength tiers: 1–4 / 5–9 / 10–19 / 20–29 / 30+.
- Visual intensity may cap at 30+, numeric count never caps.

## Mechanical reward candidate
Persistent timing bonus:
- 5–9 +5%
- 10–19 +8%
- 20–29 +12%
- 30+ +15% cap

Milestone follow-up:
- 5 small,
- 10 medium,
- 20 strong,
- 30 maximum,
- 40/50/60… repeat 30-tier power rather than scaling forever.

Current raw-equivalent A/B budgets:
`60 / 90 / 150 / 210 cap`.

Class reward language:
- Knight: extra blade/frontline break.
- Rogue: dagger burst.
- Tank: shockwave/protection.
- Archer: extra straight-line shot.
- Mage: secondary explosion.

---

# Stage-start presentation
Every stage should establish a clear boundary before play resumes.

Current approved flow:
`STAGE N / READY → fade out → combat begins`.

While stage-intro text is present:
- no enemy spawn/movement progression,
- no AI/passive attack,
- no Timing Square sweep/input.

Combo is preserved through the intro.

---

# End-run team contribution presentation

On clear/game over, show rows in actual top-to-bottom character-slot order:
1. local player,
2. teammate slot 2,
3. teammate slot 3,
4. teammate slot 4.

Current metric set:
- KILLS,
- DMG,
- COIN contribution,
- LV,
- MAX COMBO.

Every metric must make ranking obvious at a glance:
- 1st gold,
- 2nd silver,
- 3rd bronze,
- 4th muted.

Do not force one global MVP; different classes should visibly lead different categories.

---

# UI hierarchy
- Charge stack above Timing Square.
- Learned skill icons below Timing Square.
- EXP gauge immediately right of Timing Square.
- Combat judgment text sits beside EXP/right of Timing Square at smaller size; it must not overlap the square or combo pop.
- Timing Square renders above monsters.
- Between active attacks the square remains visible at reduced opacity.
- While waiting for a visible target, the square remains visibly paused rather than disappearing.
- Combo popup appears only at PERFECT moments near the Timing Square.
- Stage-start message is large and centered.
- Prototype test descriptors should not consume battlefield visibility.

## Team presentation
- AI teammates do not receive visible Timing Squares.
- AI internally receives timing results, EXP, levels and automatic skill unlocks.
- Four-character spacing should preserve full-body silhouettes and weapons.
- Current v0.20 candidate slot Y = `.265 / .425 / .585 / .745`, scale `.41`.
- Temporary prototype controls do not define the final production character area.

## Class color language
- Knight: gold / bright steel.
- Rogue: charcoal / silver / minimal red.
- Tank: blue / dark steel.
- Archer: green.
- Mage: purple.

Class color propagates through clothing, weapons, projectiles, Timing Square, EXP, skill icons and impact VFX.
