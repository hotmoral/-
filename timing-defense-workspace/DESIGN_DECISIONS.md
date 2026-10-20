# Timing Defense — Design Decisions

## Core combat
- Primary input is timing, not free movement.
- One-square rhythm: `X → X → X → X+Y`.
- Fourth attack is charged/heavy and must feel substantially stronger.
- P×P on heavy = CRITICAL.
- Tap-anywhere remains the intended combat control model.

## Target visibility / turn-boundary integrity
- A monster may be targeted/damaged only after its aim point enters the visible viewport.
- Spawning beyond the right edge does not make an enemy targetable.
- Local, AI, passive, pierce and AoE damage obey the same visibility rule.
- Unseen/off-screen kills must not award rewards.
- Attack input must not force-spawn an invisible target.

### Timing-turn gating
- A **new** Timing Square turn starts only while a valid visible enemy exists.
- If no visible target exists at the next-turn boundary, the square pauses and does not sweep.
- Passive and AI attacks wait too.
- Empty timing turns must not generate EXP.

### In-progress turn continuity
Once a timing turn begins with a visible target, that entire timing turn is locked as valid.
If the final visible target disappears due to AI/passive/team damage while the needle is moving:
- do not cancel/snap-stop the current turn,
- normal X remains tappable,
- fourth-attack X may continue into Y,
- the full X→Y sequence may finish,
- that already-valid turn may resolve normal judgment/EXP,
- only the following turn waits if no target is visible.

Reason: cancelling mid-turn because a teammate killed the target looks like lag, dropped input or an unresponsive Timing Square.

Target-wait does not break PERFECT combo. Stage-clear/shop/final-clear should wait for an already-valid local turn to finish or naturally time out.

---

## Class roles
Classes solve different combat problems rather than converging on identical DPS.

### Knight
Generalist / stable frontline / penetration / strong heavy.

### Rogue
Fast multihit / crit / high-HP normal execution.
- No same-target dagger hit cap.
- Boss dagger damage scalar starting value `0.70`.

### Tank
Knockback / wall protection / battlefield control.
- Explicit team-specialist.
- Fresh-run solo Stage-10 parity not required.
- Future permanent/meta stats may make solo completion practical.
- Boss knockback scalar starting value `0.40`.

### Archer
Straight-line penetration / rear-target access / long-range pressure.
- Arrow continues only on its current launch trajectory.
- Only hitboxes intersecting that line may be penetrated.
- No homing, bending or automatic next-target chaining.

### Mage
Area damage / dense-pack deletion / chained explosions.
Should become stronger with density, not become top single-target boss DPS.

## Balance philosophy
Do not normalize all classes to equal DPS or equal solo clear.
Evaluate by role:
- Rogue: durable-normal TTK.
- Archer: line-pack clear/rear pressure.
- Mage: dense-cluster clear.
- Tank: wall preservation/control/team utility.
- Knight: general-purpose consistency.

## Player mastery
Simulation references:
- Average = N25 / G55 / P20.
- Skilled = N10 / G50 / P40 plus modestly faster commitment.

Skilled is considered attainable. Strong Average→Skilled improvement is intended and does not self-authorize nerfs.

## EXP philosophy
- EXP remains tied to valid timing attack results/events.
- Faster-killing classes are not compensated merely because they perform fewer attacks.
- Passive auto-attacks do not grant EXP.
- A turn that was valid when started may grant normal EXP even if the target disappears during that same turn.
- No visible target = no new timing turn solely for EXP farming.

## Balance-change governance
Required order:
`model/simulate → identify intent/artifact/defect → report → discuss → explicit decision → numerical live patch`

A large measured gap never self-authorizes a balance change.

---

# Encounter-pressure philosophy

Pressure families:
- `S` Swarm
- `E` Elite/Heavy
- `X` Special/Mixed

`X` is the primary co-op scaling language. `S` and `E` are time-separated spike tools.

## Stage grammar
A stage may use one, two or all three pressure families. Do not force S+E+X into every stage.
A 50-stage tier gets identity through:
- 1/2/3-pattern proportions,
- S/E/X frequency,
- pair/triple ratios,
- early/mid/late/final timing,
- geometry,
- duration/intensity,
- overlap frequency.

Higher tiers do not automatically mean more simultaneous pattern types; focused one-pattern stages may return at much higher intensity.

Current concrete Swarm candidates:
- S-line 2P/3P/4P = `8 / 11 / 14`
- S-cluster = `7 / 10 / 13`
- S-scatter = `9 / 12 / 16`

Reference P95 four-second spawn density:
- 2P ≈ 11
- 3P ≈ 15
- 4P ≈ 18

X carries multiplayer scaling through role-bearing composition. E is an effective durability budget rather than one giant HP sponge.

---

# Passive basic attack — approved concept, coefficients not frozen
Purpose: let the player briefly inspect the battlefield without combat going completely idle while timing remains dominant.

Rules:
- only fires while a valid visible combat target exists,
- no timing judgment,
- no crit/proc crit,
- no skill trigger,
- no charge,
- no PERFECT combo,
- no EXP,
- minimal/zero knockback.

Leading A/B candidate:
- `40 raw / 2.0 s`
- ordinary non-boss HP +10%
- boss/elite compensation calibrated separately.

Do not compensate passive damage 1:1; some real breathing room is intentional.

---

# Consecutive PERFECT combo

## Counter
- PERFECT only increments.
- GOOD/NORMAL/MISS reset.
- attacks 1–3 each can add +1.
- heavy X and heavy Y each can add +1.
- fully PERFECT 1→4 sequence = +5 combo.
- count is unbounded: 20/30/40/50+.
- milestones do not consume/reset the streak.
- stage/shop/target-wait downtime does not break combo.

## Psychological pressure
High visible streaks should make the player nervous naturally.
Do not secretly shrink timing windows, accelerate sweeps or apply hidden accuracy penalties at high combo.

## Presentation
- show from `1 COMBO!`.
- near Timing Square.
- transient, slightly tilted punch/scale pop on each PERFECT; no permanent rectangular box.
- visual tiers 1–4 / 5–9 / 10–19 / 20–29 / 30+.
- visual intensity may cap at 30+, numeric count never caps.

## Mechanical A/B candidate
Persistent bonus:
- 5–9 +5%
- 10–19 +8%
- 20–29 +12%
- 30+ +15% cap

Milestone follow-up:
- 5 small
- 10 medium
- 20 strong
- 30 maximum
- 40/50/60… repeat 30-tier power.

Current raw-equivalent budgets: `60 / 90 / 150 / 210 cap`.

Class reward language:
- Knight: blade/frontline break.
- Rogue: dagger burst.
- Tank: shockwave/protection.
- Archer: straight-line shot.
- Mage: secondary explosion.

---

# Stage-start presentation
Approved flow:
`STAGE N / READY → fade out → combat begins + START!`

While STAGE/READY is present:
- no enemy progression,
- no AI/passive attack,
- no Timing Square sweep/input.

Combo is preserved.

---

# Combat UI hierarchy
- Charge stack above Timing Square.
- Learned skill icons below Timing Square.
- EXP gauge immediately right of Timing Square.
- EXP gain feedback beside gauge uses explicit `+EXP N`.
- No separate lower-left EXP floating message.
- Judgment result appears **inside Timing Square** as a very short impact-style pop.
- Result tiers use different size/color/glow; PERFECT/CRITICAL are more emphatic than GOOD/NORMAL.
- Pop must fade quickly enough not to obstruct the next sweep.
- Timing Square renders above monsters.
- Between attacks/waits, square remains visibly present/paused rather than disappearing.
- Combo pop stays near the square at PERFECT moments.
- Stage-start message is centered and prominent.
- Debug/prototype stats should not consume battlefield visibility.

## Battlefield background
The black/grid prototype background is no longer the product direction.
Use a restrained natural environment with enough tonal separation for:
- monsters,
- projectiles,
- character silhouettes,
- Timing Square.

Natural scenery should be atmospheric rather than highly detailed/competitive with combat.

---

# Team / character presentation
- AI teammates do not render Timing Squares.
- AI internally receives timing results, EXP, levels and automatic skills.
- Four-character spacing must preserve full-body silhouettes and weapons.
- Temporary prototype controls do not define the production battlefield layout.
- Class color language:
  - Knight gold/bright steel
  - Rogue charcoal/silver/red accent
  - Tank blue/dark steel
  - Archer green
  - Mage purple

---

# End-run contribution presentation
Rows follow top-to-bottom character order.
Current metrics:
- KILLS
- DMG
- COIN contribution
- LV
- MAX COMBO

Every metric must expose ranking at a glance:
- 1st gold
- 2nd silver
- 3rd bronze
- 4th muted

Do not force one global MVP; different roles should be socially legible through different category wins.
The results panel should be visually centered in the viewport.

---

# Pre-game lobby / entry flow — approved direction

Production-direction entry flow:
`nickname → character selection → play settings → run / team waiting → stage intro → combat`

The battle screen should not be used as a configuration menu. Old in-combat class-switch and TEAM/SPEED debug controls are removed from the production-facing flow.

## Nickname
- Player creates/enters a nickname before play.
- Reuse locally where possible.
- Later network identity rules can supersede local-only persistence.

## Character selection
Use a **horizontal card/carousel** presentation:
- one class prominently shown at a time,
- swipe left/right and explicit arrow controls,
- smooth slide motion,
- class role and play style visible,
- weapon/clothing silhouette strongly differentiated even with geometric prototype art,
- six-skill roadmap visible before selecting.

## Skill-icon semantic rule — frozen direction
Skill icons must communicate the mechanic through **shape + color**, not merely class color or generic numbered glyphs.

Examples:
- a double blade-wave mechanic should visibly contain two blade/slash forms,
- triple shot should visibly contain three arrows,
- penetrating shot should show a line passing through targets/plates,
- shield skills should read as shield/guard,
- ground impact should read as impact/crack,
- chain explosion should read as connected blast nodes.

Different skills in the same class should not all look like recolors of one symbol.
This rule applies to both lobby roadmap icons and future final HUD assets.

## Play-setting interaction
Dropdowns are not mandatory.
For small fixed choice sets on mobile, prefer **visible buttons / segmented controls** when faster and easier to understand.

Current intended settings:
- SOLO / TEAM
- AI count 0–3 in either mode where applicable
- AI class
- AI position P2/P3/P4
- TEAM method FRIEND / LINK / RANDOM
- TIER selection

Defaults:
- SOLO
- AI NONE
- highest unlocked/available tier

Currently only Tier1 exists, so Tier1 is both default and highest.

## Team networking truth boundary
FRIEND/LINK/RANDOM may be designed in the front-end before backend networking exists, but UI must not falsely imply a remote player joined.

Planned sequence:
1. waiting-room/invite/link/random UX,
2. actual room authority and network transport,
3. real friend/link/random join flow,
4. disconnect/rejoin/state reconciliation.

For AI-only/solo configurations, start immediately without waiting.

---

# Current implementation mapping
- v0.20: target turn-gating + stage READY.
- v0.21: natural battlefield + inside-square judgment + EXP cleanup + START + centered results.
- v0.22: nickname/class carousel/skill roadmap/button settings/AI lineup; real TEAM networking still pending.
