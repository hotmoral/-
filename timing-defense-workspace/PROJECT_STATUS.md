# Timing Defense — Project Status

Updated: 2026-10-20 KST

## Canonical locations
- Public repo: `hotmoral/-`
- Live branch: `timing-defense-live-v011`
- Planning/balance/handoff branch: `timing-defense-workspace`
- Current playable prototype: **v0.17**
- Public play URL: `https://timing-defense-v011.onrender.com/v017.html`
- Current live source HEAD: `8f46b2460f0d16b6103e0f10bec0b5206aa93ae6`
- Current Render deploy: `dep-dbbc3emq1p3s73c29csg` / LIVE

## Current playable scope
- Landscape mobile/browser timing-defense prototype.
- Fixed player near left wall; monsters approach from right.
- Rhythm: `X → X → X → X+Y`.
- Judgments: NORMAL / GOOD / PERFECT plus HEAVY / HEAVY+ / GREAT / SUPER / CRITICAL.
- Classes: Knight / Rogue / Tank / Archer / Mage.
- Team controls: solo through +3 AI.
- Monsters: GRUNT / RUNNER / BRUTE / SHIELD / FLYER.
- Current playable Stage 1–10 prototype.
- Run-only EXP / level / coin / shop upgrades.
- Playable skill implementation reaches Lv21.

## Growth structure
Automatic skill unlocks:
`Lv6 / Lv11 / Lv16 / Lv21 / Lv26 / Lv31`

Implemented now:
`Lv6 / Lv11 / Lv16 / Lv21`

Lv21 is intentionally the first major fourth-attack transformation milestone. Lv26/Lv31 remain planned only.

## Frozen class / progression decisions
- Archer = true straight-line geometry; launch trajectory is fixed and cannot retarget off-line.
- Tank = team-specialist; fresh-run solo parity is not required.
- Rogue repeated dagger hits on the same target are uncapped.
- Boss dagger scalar = `0.70`.
- Boss knockback scalar = `0.40`.
- EXP remains tied to timing attack events/results.
- Faster clear does not receive compensating EXP merely because it generates fewer attacks.
- Simulation never self-authorizes a live numerical balance patch.

## Player mastery reference
- Average = N25 / G55 / P20.
- Skilled = N10 / G50 / P40 plus modestly faster commitment.
- Skilled is considered attainable; strong Average→Skilled improvement is intended.

---

# Current playable changes — v0.17

v0.17 intentionally avoids auto-attack/combo numerical balance changes and applies only the already-approved system/UX changes.

### AI teammate growth parity
AI teammates now internally carry:
- independent EXP,
- independent level,
- automatic Lv6/11/16/21 unlocks,
- internally simulated timing judgments,
- class skill behavior including Rogue barrage, Tank protection, Archer line mechanics and Mage burst/resonance.

No additional AI Timing Squares are rendered.

### Timing Square continuity
- After a timing input the square no longer disappears during projectile/recovery.
- It remains visible at reduced opacity (~42%) until the next active timing pass.
- Charge/location information therefore remains continuously anchored.

### Party spacing
- Four-character vertical spacing is widened slightly from v0.16.
- Character scale is preserved so the intent is more full-body/weapon readability rather than simply shrinking everyone.

Source files:
- `timing-defense-v011/v017-ux-ai.js`
- `timing-defense-v011/v017.html`

v0.16 remains available as rollback/reference.

---

# Simulation / design history

## v1 — role separation
Established the intended class-role split.

## v2 — Stage 1–10 + run shop
Resolved Archer straight-line semantics, Tank team specialization and EXP/attack-count coupling.

## v3 — mastery curve
Confirmed meaningful Average→Skilled improvement.

## v4 — team composition
Confirmed Tank defensive utility, Rogue durable-normal niche, Archer-line/Mage-density split and Knight generalist value.

## v5 — Tier Pressure Grammar
Future 50-stage tier grammar:
- `S` Swarm,
- `E` Elite/Heavy,
- `X` Special/Mixed.

Representative five-tier distribution:
- 1-pattern 40.8%,
- 2-pattern 43.6%,
- 3-pattern 15.6%.

## v6 — concrete pressure recipes
Candidate Swarm burst sizes:
- line 2P/3P/4P = `8 / 11 / 14`,
- cluster = `7 / 10 / 13`,
- scatter = `9 / 12 / 16`.

X remains the main co-op scaling language; E is an effective durability budget.

## v7 — exact v0.16 formula re-run
Key Lv21 clear bounds:
- 3P Average/Skilled = 81.6 / 96.4%,
- 4P = 52.8 / 73.6%.

Rogue retains best durable-normal TTK. Archer remains strongest on line geometry. No numerical class rebalance authorized.

Files:
- `BALANCE_SIM_REPORT_V7_V016_EXACT.md`
- `combat_exact_v016.py`

## v8 — latest: auto-attack + unbounded PERFECT combo diagnostic
Approved concept:
- passive basic attack creates limited battlefield-reading breathing room,
- timing remains the dominant damage/progression source,
- consecutive PERFECT combo is unbounded and resets only on non-PERFECT judgment,
- rising visible streak itself creates psychological pressure,
- no hidden timing-window/sweep-speed difficulty increase at high combo.

Leading first auto-attack test candidate:
- 40 raw damage / 2.0 s,
- no EXP / crit / charge / skill / combo,
- ordinary-monster HP compensation around +8% as a **test candidate**, not frozen value.

Baseline math:
- passive contribution ≈ 13.9% of Average timing DPS,
- 10.8% of Skilled,
- 8.8% of Expert.

At +8% ordinary HP, net pace remains slightly easier:
- Average about +5.5%,
- Skilled +2.6%,
- Expert +0.7%.

Combo rarity supports unlimited counting. In roughly 150 judgment opportunities:
- Skilled P40 reaches 5 combo ~60.9%, 10 combo ~0.8%, 20 essentially never,
- Expert P65 reaches 10 ~50.9%, 20 ~0.8%, 30 ~0.016%,
- Master-like P80 reaches 20 ~27.5%, 30 ~2.9%, 40 ~0.3%.

Mechanical milestone coefficients remain unfrozen. Visual escalation candidate: 5 / 10 / 20 / 30+, with the number continuing indefinitely.

See `BALANCE_SIM_REPORT_V8_AUTO_COMBO.md`.

---

# Current next boundary

1. Human/device playtest v0.17 for:
   - faded Timing Square readability,
   - slightly wider four-character spacing,
   - AI growth/skill behavior.
2. Fix implementation defects only.
3. Build the **auto-attack + combo experimental block** using v8 candidate values, but keep it as an explicitly testable balance slice.
4. Simulate conservative/medium/aggressive combo reward variants before freezing mechanical milestone rewards.
5. Compare no-timing / Average / Skilled / Expert survival and clear behavior.
6. Report/discuss before final monster-HP or reward coefficients are frozen.

## Still not frozen
- final auto-attack interval/damage,
- final HP compensation,
- exact combo milestone mechanical rewards,
- final E HP/armor package,
- final X hardened values,
- final stage duration,
- true human multiplayer cadence/network behavior,
- multiplayer shop/economy ownership,
- duplicate-class policy,
- sync-bonus implementation,
- final number/names/order of tiers,
- Lv26/Lv31 exact coefficients.
