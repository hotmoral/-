# Timing Defense — Session Handoff

Updated: 2026-10-20 KST

## Canonical locations
- Public repository: `hotmoral/-`
- Planning / balance / handoff branch: `timing-defense-workspace`
- Live source branch: `timing-defense-live-v011`
- Stable public prototype: `v0.15`
- Stable URL: https://timing-defense-v011.onrender.com/v015.html
- v0.16 source loader: `timing-defense-v011/v016.html`
- v0.16 live-branch HEAD: `caa7e249f4b52aa3b6215ff2677b0c4973f3eb17`

The workspace branch is canonical for design decisions, simulation interpretation and new-session recovery. The live branch is separate.

## Deployment status at handoff
v0.16 source is committed, but the latest observed Render deployment still points to v0.15 commit `4ce695f...`.

Render service:
- service: `srv-dbb1c9mi0phs73b5bao0`
- workspace: `tea-dba4s2ajnfac73ec91qg`
- branch: `timing-defense-live-v011`
- autoDeploy: `yes`

Because auto-deploy is enabled, no duplicate manual deploy was triggered. Do not claim v0.16 public-live until Render reports a deployment containing `caa7e249...` or later.

---

# Frozen combat / progression decisions
- Knight: stable generalist / penetration / strong heavy.
- Rogue: multihit / crit / high-HP normal execution.
- Tank: team-specialist / knockback / wall protection / control; fresh-run solo parity not required.
- Archer: true straight-line geometric penetration only; no homing/automatic next-target chaining.
- Mage: density specialist / AoE / chained explosions.
- Rogue same-target dagger hits are uncapped.
- Boss dagger scalar = `0.70` starting value.
- Boss knockback scalar = `0.40` starting value.
- EXP remains tied to timing attack events/results.
- Faster clear does not receive compensating EXP merely for fewer attacks.

Player mastery reference:
- Average = N25 / G55 / P20.
- Skilled = N10 / G50 / P40 plus modestly faster commitment.
- Skilled is considered attainable; strong mastery improvement is intended.

Balance governance:
`model/simulate → identify cause/artifact/specialization → report → discuss → explicit decision → live balance patch`

---

# v0.16 source implementation — completed

Files on live branch:
- `timing-defense-v011/v016-core.js`
- `timing-defense-v011/v016-ui.js`
- `timing-defense-v011/v016-render.js`
- `timing-defense-v011/v016.html`

v0.15 remains unchanged for rollback.

## Skill milestones implemented
Actual mechanics implemented through:
`Lv6 / Lv11 / Lv16 / Lv21`

Six-slot HUD reserves:
`Lv6 / Lv11 / Lv16 / Lv21 / Lv26 / Lv31`

### Knight
- Lv6 +12% blade-wave damage.
- Lv11 normal +1 penetration at 85%; heavy +2.
- Lv16 attacks whose actual timing inputs contain PERFECT: +18% damage / +20% knockback.
- Lv21 heavy +20% damage, larger wave, up to +3 penetrations.

### Rogue
- Lv6 second dagger 55%.
- Lv11 +6%p native crit.
- Lv16 PERFECT-containing attack: next recovery 390→312 ms.
- Lv21 heavy = 5 daggers total: 100% + 45%×4.
- no same-target cap.
- boss dagger damage 70%.

### Tank
- Lv6 knockback ×1.30.
- Lv11 wall incoming damage -10%.
- Lv16 PERFECT-containing attack refreshes wall shield 80 / 3 s / non-stack.
- Lv21 Ground Impact: broad nearby multi-target coverage; Tank heavy knockback ×2.0.
- boss knockback 40%.

### Archer
- Lv6 up to 2 additional penetration targets.
- actual line-projection + monster hit-corridor collision.
- no X-order chaining / no bending.
- secondary penetration before Precision uses the known live 52% coefficient.
- Lv11 projectile speed +25% equivalent / base damage +10%.
- Lv16 PERFECT-containing attack ignores armor and preserves penetration damage.
- Lv21 heavy = three parallel arrows 100% + 65% + 65%.

### Mage
- Lv6 splash 50%.
- Lv11 radius +35%, splash 60%.
- Lv16 PERFECT-containing attack schedules second 55% outer-ring Resonance after ~180 ms; original center excluded.
- Lv21 heavy +20% damage, explosion radius ×1.6, larger/slower Greater Arcane Orb.

### HUD/VFX
- single learned-skill icon replaced by horizontal six-slot strip below Timing Square.
- new unlock pulses temporarily.
- no permanent skill-name text beside EXP.
- Tank shield HUD/VFX added.
- Lv21 Knight/Tank/Mage heavy signature overlays added.

Validation completed:
- Node syntax PASS: `v016-core.js`, `v016-ui.js`, `v016-render.js`.
- loader dependency check PASS.
- live branch HEAD confirmed at `caa7e249...`.

See `V016_IMPLEMENTATION_REPORT.md`.

---

# Encounter / simulation history

## v4 — team role validation
- Tank defensive team value confirmed.
- Rogue durable-normal niche confirmed.
- Archer line vs Mage cluster distinction confirmed.
- Knight remains a stabilizing generalist.
- current unscaled Stage 1–10 saturates at 3–4 players.

## v5 — Tier Pressure Grammar
Pressure families:
- S = Swarm,
- E = Elite/Heavy,
- X = Special/Mixed.

Across five representative 50-stage tiers:
- 1-pattern 40.8%,
- 2-pattern 43.6%,
- 3-pattern 15.6%.

Higher tiers do not simply add more simultaneous pattern types; identity also comes from ratio, timing, geometry, intensity and overlap.

## v6 — concrete current-roster pressure recipes
Swarm candidate burst sizes:
- S-line 2P/3P/4P = 8 / 11 / 14,
- S-cluster = 7 / 10 / 13,
- S-scatter = 9 / 12 / 16.

P95 4-second spawn-density candidate:
- 2P ≈ 11,
- 3P ≈ 15,
- 4P ≈ 18.

X is the main co-op scaling language through role-bearing composition. E is an effective durability budget rather than one giant HP multiplier.

A conservative 7,000-run bound produced aggregate clear:
- 2P Average/Skilled = 100/100%,
- 3P = 88.4/94.9%,
- 4P = 68.3/83.0%.

An all-capable-human candidate-Lv21 upper bound still saturated near 100%, so final co-op difficulty was intentionally deferred until exact playable Lv11–21 existed. v0.16 now provides that exact source basis once runtime smoke validation closes.

Files:
- `TIER_PRESSURE_GRAMMAR_V1.md`
- `PRESSURE_RECIPES_V1.md`
- `BALANCE_SIM_REPORT_V5_PRESSURE_GRAMMAR.md`
- `BALANCE_SIM_REPORT_V6_CONCRETE_RECIPES.md`

---

# Exact next work boundary

1. Confirm Render auto-deploy of v0.16.
2. Public smoke test v0.16 for runtime/UI/mechanics defects.
3. Fix implementation defects only; do **not** tune class/stage numbers from first impressions.
4. Extract exact v0.16 formulas into the simulator.
5. Re-run the concrete S/E/X recipes under 2/3/4-player models.
6. Compare mastery response, role contribution, wall pressure, clear rate and suspicious windows.
7. Report/discuss before any numerical rebalance.

## Smoke-test checklist
- v0.16 loads without runtime errors.
- six skill slots fit target landscape sizes.
- Lv11/Lv16/Lv21 unlock and execute for all five classes.
- Archer penetration remains physically straight.
- Tank shield absorbs/refreshes/expires correctly.
- Rogue barrage preserves repeated hits.
- Mage Resonance excludes original center.
- Lv21 heavy VFX remains readable under overlap.

## Still unresolved
- final E HP/armor package,
- final X hardened values,
- final stage duration,
- real human multiplayer cadence/network behavior,
- multiplayer shop/economy ownership,
- duplicate-class policy,
- sync DUO/TRIPLE/FULL rules,
- final tier count/names/order,
- Lv26/Lv31 coefficients.

---

# New-session read order
1. `SESSION_HANDOFF.md`
2. `PROJECT_STATUS.md`
3. `V016_IMPLEMENTATION_REPORT.md`
4. `DESIGN_DECISIONS.md`
5. `SKILL_PLAN_LV6_31.md`
6. `TIER_PRESSURE_GRAMMAR_V1.md`
7. `PRESSURE_RECIPES_V1.md`
8. `BALANCE_SIM_REPORT_V4_TEAM.md`
9. `BALANCE_SIM_REPORT_V5_PRESSURE_GRAMMAR.md`
10. `BALANCE_SIM_REPORT_V6_CONCRETE_RECIPES.md`
11. `SIMULATION_METHOD.md`
12. `NEXT_WORK.md`

Older v1/v2/v3 reports remain available for numerical provenance and decision history.
