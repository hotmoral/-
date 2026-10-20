# Timing Defense — Design Decisions

## Core combat
- Primary input is timing, not free movement.
- Rhythm: `X → X → X → X+Y`.
- Fourth attack is charged/heavy.
- P×P on heavy = CRITICAL.
- Tap-anywhere remains intended combat control.

## Target visibility / turn integrity
- Off-screen enemies cannot be targeted/damaged/rewarded.
- New timing turn starts only with a visible target.
- No visible target at next-turn boundary = Timing Square / AI / passive wait.
- Empty turns cannot generate EXP.
- A turn already started with a valid target is allowed to finish even if teammates remove the final enemy.
- Heavy X→Y may complete fully.
- Target-wait itself does not break PERFECT combo.

## Class roles
- Knight: stable generalist / frontline / penetration.
- Rogue: fast multihit / crit / durable-normal execution; no same-target dagger cap; boss dagger scalar `0.70`.
- Tank: team-specialist / knockback / wall protection; solo parity not required; boss knockback scalar `0.40`.
- Archer: strict straight-line penetration; no bending/homing/next-target chaining.
- Mage: density/AoE specialist.

Do not normalize all classes to identical DPS/solo clear. Role-specific benchmarks govern interpretation.

## Mastery / balance governance
- Average = N25 / G55 / P20.
- Skilled = N10 / G50 / P40 plus modestly faster commitment.
- Skilled is intentionally attainable.
- Simulation is diagnostic, not self-authorizing.
- Required order: `simulate/measure → classify cause → report → discuss → explicit decision → numerical patch`.

## EXP
- EXP is tied to valid timing events.
- Passive attacks grant no EXP.
- A valid already-started turn may still award EXP if its target disappears mid-turn.
- Every valid local EXP event should visibly produce `+EXP N` beside the EXP gauge.
- No separate lower-left EXP float.

---

# Passive attack — approved concept, coefficients not frozen
Purpose: preserve battlefield-reading bandwidth while timing attacks remain mandatory.

Current A/B:
- `40 raw / 2.0 s`
- no EXP / charge / crit / skill / combo
- minimal/zero knockback
- ordinary non-boss HP +10%

Do not compensate passive damage 1:1; some genuine breathing room is intended.

---

# Consecutive PERFECT combo
- PERFECT only increments.
- GOOD/NORMAL/MISS reset.
- Attacks 1–3 each +1; heavy X and Y each +1.
- Fully PERFECT 1→4 sequence = +5.
- Count is unbounded.
- Stage/shop/target-wait downtime does not break combo.
- No hidden high-combo timing difficulty increase.

Presentation:
- show from `1 COMBO!`,
- transient tilted punch popup near Timing Square,
- visual tiers 1–4 / 5–9 / 10–19 / 20–29 / 30+,
- visual intensity may cap at 30+, number never caps.

Current A/B reward:
- 5–9 +5%
- 10–19 +8%
- 20–29 +12%
- 30+ +15% cap
- milestone raw-equivalent 60 / 90 / 150 / 210 cap, repeated every +10 after 30 at max tier.

---

# Stage-start presentation
`STAGE N / READY → fade → START! + combat`.
While intro is active: no enemy progression, AI/passive attack or Timing Square input/sweep.

---

# Combat UI hierarchy
- Charge above Timing Square.
- Skill icons below.
- EXP gauge immediately right.
- `+EXP N` beside gauge on every valid gain.
- Timing judgment appears briefly **inside** Timing Square with tier-specific color/size/glow.
- Timing Square remains visible/paused between active turns.
- Combo pop appears only on PERFECT moments.
- Natural battlefield background replaces black grid.
- Debug/prototype statistics should not consume battlefield visibility.

### Rogue contrast rule
Rogue's charcoal/silver identity must remain readable over brighter natural scenery.
Combat HUD may use a stronger red/silver accent for Timing Square/charge pips without changing Rogue combat values.

---

# End-run contribution presentation
Rows follow top-to-bottom slot order.
Metrics:
- KILLS
- DMG
- COIN
- LV
- MAX COMBO

Each metric exposes rank: gold / silver / bronze / muted.
No forced global MVP.
Result board is centered and must preserve clear row spacing.
Local nickname may replace hard-coded `YOU`.

---

# Pre-game lobby / entry flow
Production-direction flow:
`nickname → character selection → play settings → run / team waiting → stage intro → combat`.

Battle screen is not a configuration menu. In-combat class switch and prototype TEAM/SPEED/RESET controls remain hidden.

## Character selection layout — v0.23 direction
Landscape uses three visual zones:
- **left fixed info:** class identity / role / play-style,
- **center:** only the character hero slides horizontally,
- **right fixed info:** six skill icons + selected full skill detail.

Navigation:
- explicit left/right arrows,
- horizontal swipe,
- smooth class change.

The user should perceive the character as the moving object; surrounding information updates in place.

## Character prototype art
Geometric/vector construction is acceptable during prototype stage, but class silhouette, clothing, weapon and equipment details must differ enough that identity is not carried by color alone.

## Skill-icon semantic rule — frozen direction
Icons must communicate mechanic by **shape + color**.
- Double/multiple attacks visibly use multiple blades/daggers/arrows.
- Penetration shows through-line/targets.
- Shield/guard uses defensive silhouette.
- Ground impact uses crack/impact language.
- Chain explosion uses linked blast nodes.
- Different skills in one class must not be generic recolors.

All six milestones `Lv6 / 11 / 16 / 21 / 26 / 31` should be visible in the roadmap. Selecting an icon exposes full skill name/level/description; core descriptions should not be ellipsized away.

## Play-setting interaction
For small fixed option sets, prefer visible buttons/segmented controls over dropdowns when faster on mobile.

Settings:
- SOLO / TEAM
- AI count/fill
- AI class
- AI position P2/P3/P4
- TEAM method FRIEND / LINK / RANDOM
- Tier

Defaults:
- SOLO
- no AI
- highest available tier (currently Tier1).

### TEAM slot rule — frozen direction
TEAM must reserve at least one slot for another human participant.
- SOLO may use AI 0–3.
- TEAM uses `AI FILL` and may use at most AI 0–2.
- TEAM +3 AI is invalid.

Human slots take conceptual priority over AI filler.

### AI selector readability
Avoid developer-only single-letter class controls when possible. Use a compact class glyph plus readable short label such as KNI/ROG/TNK/ARC/MAG.

## Networking truth boundary
FRIEND/LINK/RANDOM may exist as front-end states before backend completion, but UI must not falsely report a remote player connection.

Sequence:
1. waiting-room UX,
2. room authority/network transport,
3. real invite/link/random join,
4. reconnect/reconciliation.

AI-only/SOLO starts immediately.

---

# Encounter pressure
Pressure families:
- S Swarm
- E Elite/Heavy
- X Special/Mixed

Do not force all three into every stage. Tier identity comes from 1/2/3-pattern distribution, geometry, timing and intensity.

Current Swarm candidate bursts:
- line 2P/3P/4P = 8 / 11 / 14
- cluster = 7 / 10 / 13
- scatter = 9 / 12 / 16

Reference P95 4-second spawn density:
- 2P ≈ 11
- 3P ≈ 15
- 4P ≈ 18.

---

# Current implementation mapping
- v0.20: target turn-gating + READY.
- v0.21: natural battlefield + judgment/EXP cleanup + START + centered results.
- v0.22: nickname / class carousel / skill roadmap / button settings / AI lineup.
- v0.23: three-zone character selection, full skill detail, Rogue HUD contrast, robust every-gain EXP pop, TEAM human-slot reservation, AI selector/result layout polish.
- Next: v0.24 FRIEND/LINK/RANDOM waiting-room UX; actual networking remains separate.
