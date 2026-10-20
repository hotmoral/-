# Timing Defense — Project Status

Updated: 2026-10-20 KST

## Canonical locations
- Public repo: `hotmoral/-`
- Live source branch: `timing-defense-live-v011`
- Planning/balance/handoff branch: `timing-defense-workspace`
- Stable public prototype: `v0.15`
- Stable URL: https://timing-defense-v011.onrender.com/v015.html
- v0.16 source loader: `timing-defense-v011/v016.html`
- v0.16 source HEAD: `caa7e249f4b52aa3b6215ff2677b0c4973f3eb17`

## Deployment status
v0.16 source is implemented on the live branch, but at the last check Render still reported the v0.15 deployment as current. Render has `autoDeploy=yes`; no duplicate manual deploy was triggered. Do not call v0.16 publicly live until Render reports a deploy containing the v0.16 source HEAD or later.

## Core playable design
- Landscape timing-defense game.
- Fixed player near the left wall; monsters approach from the right.
- Timing rhythm: `X → X → X → X+Y`.
- NORMAL / GOOD / PERFECT; heavy outcomes HEAVY / HEAVY+ / GREAT / SUPER / CRITICAL.
- Classes: Knight / Rogue / Tank / Archer / Mage.
- Current Stage prototype: 1–10.
- Run EXP / level / coin / shop upgrades.
- Team controls currently support solo through +3 AI.

## Frozen class/progression decisions
- Archer penetration = true straight-line geometry only; no homing or automatic next-target chain.
- Tank = team-specialist; fresh-run solo parity is not required.
- Rogue same-target dagger hits remain uncapped.
- Boss dagger damage scalar = `0.70` starting value.
- Boss knockback scalar = `0.40` starting value.
- EXP remains tied to timing attack events/results.
- Faster clear does not receive compensating EXP merely because it generated fewer attacks.
- Simulation never self-authorizes a live balance patch.

## Player mastery reference
- Average = N25 / G55 / P20.
- Skilled = N10 / G50 / P40 plus modestly faster commitment.
- Skilled is an attainable learned-player state; strong Average→Skilled improvement is intended.

---

# v0.16 implementation state

v0.16 is layered on top of v0.15 and preserves v0.15 as rollback.

Files:
- `v016-core.js`
- `v016-ui.js`
- `v016-render.js`
- `v016.html`

Implemented automatic growth block:
`Lv6 / Lv11 / Lv16 / Lv21`

The HUD reserves all six milestones:
`Lv6 / Lv11 / Lv16 / Lv21 / Lv26 / Lv31`

### Knight
- Lv6 +12% blade-wave damage.
- Lv11 penetration: normal +1 target at 85%; heavy +2.
- Lv16 attacks containing PERFECT: +18% damage / +20% knockback.
- Lv21 heavy: +20% damage, larger signature wave, up to +3 penetrations.

### Rogue
- Lv6 second dagger 55%.
- Lv11 +6%p native crit.
- Lv16 PERFECT-containing attack shortens next recovery 390→312 ms.
- Lv21 heavy = 5 daggers total: 100% + 45%×4.
- Boss dagger scalar 0.70 applied without deleting hit events.

### Tank
- Lv6 knockback ×1.30.
- Lv11 wall incoming damage -10%.
- Lv16 PERFECT-containing attack refreshes 80 wall shield / 3 s / non-stack.
- Lv21 heavy Ground Impact = broad multi-target control + Tank heavy knockback ×2.0.
- Boss knockback scalar 0.40.

### Archer
- Lv6 up to 2 additional straight-line targets.
- Real line-projection/hit-corridor collision; no bend/retarget chain.
- Pre-Lv16 secondary penetration keeps the known 52% coefficient.
- Lv11 projectile speed +25% equivalent and base damage +10%.
- Lv16 PERFECT-containing attack ignores armor and preserves penetration damage.
- Lv21 heavy = 3 parallel arrows: 100% + 65% + 65%.

### Mage
- Lv6 splash 50%.
- Lv11 radius +35%, splash 60%.
- Lv16 PERFECT-containing attack: delayed ~180 ms Resonance at 55%, original center excluded.
- Lv21 heavy: +20% damage, radius ×1.6, larger/slower Greater Arcane Orb.

### UI/VFX
- single skill icon replaced by six-slot horizontal skill strip below Timing Square,
- newly unlocked slot pulses temporarily,
- no permanent skill-name text,
- Tank temporary shield HUD,
- Lv21 Knight/Tank/Mage signature heavy overlays.

Validation completed:
- Node syntax PASS for all three v0.16 JS patches,
- loader dependency check PASS,
- GitHub live branch confirmed at `caa7e249...`.

See `V016_IMPLEMENTATION_REPORT.md`.

---

# Encounter / simulation state

## v4 — team roles
- Tank defensive utility confirmed under pressure.
- Rogue durable-normal niche confirmed.
- Archer line vs Mage cluster distinction confirmed.
- Knight remains generalist/stabilizer.
- unscaled Stage 1–10 saturates with 3–4 players.

## v5 — Tier Pressure Grammar
Pressure families:
- S = Swarm,
- E = Elite/Heavy,
- X = Special/Mixed.

Across five 50-stage prototypes:
- 1-pattern 40.8%,
- 2-pattern 43.6%,
- 3-pattern 15.6%.

Tier identity is controlled by family mix, internal ratios, geometry, timing, intensity and overlap rather than forcing S+E+X every stage.

## v6 — concrete current-roster recipes
Candidate Swarm burst sizes:
- line 2P/3P/4P = 8 / 11 / 14,
- cluster = 7 / 10 / 13,
- scatter = 9 / 12 / 16.

Candidate P95 4-second spawn density:
- 2P ≈ 11,
- 3P ≈ 15,
- 4P ≈ 18.

X is the main co-op scaling language through role-bearing compositions. E is an effective durability budget, not a single absurd HP multiplier.

Files:
- `TIER_PRESSURE_GRAMMAR_V1.md`
- `PRESSURE_RECIPES_V1.md`
- `BALANCE_SIM_REPORT_V5_PRESSURE_GRAMMAR.md`
- `BALANCE_SIM_REPORT_V6_CONCRETE_RECIPES.md`

---

# Current next boundary
1. wait for / verify Render auto-deploy of v0.16,
2. public smoke test v0.16 for runtime/UI/mechanics defects,
3. fix implementation defects only — do not rebalance from first impressions,
4. extract exact v0.16 formulas back into the headless simulator,
5. rerun concrete pressure recipes for 2/3/4-player models,
6. report/discuss before numerical rebalance.

Still not frozen:
- final E HP/armor package,
- final X hardened values,
- final stage duration,
- human multiplayer cadence/network behavior,
- multiplayer shop/economy ownership,
- duplicate-class policy,
- sync bonus implementation,
- final tier count/names/order,
- Lv26/Lv31 exact coefficients.
