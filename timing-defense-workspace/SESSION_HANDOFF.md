# Timing Defense — Session Handoff

Updated: 2026-10-20 KST

## Canonical locations
- Public repository: `hotmoral/-`
- Planning / balance / handoff branch: `timing-defense-workspace`
- Live source branch: `timing-defense-live-v011`
- Current public prototype: **v0.16**
- Public URL: `https://timing-defense-v011.onrender.com/v016.html`
- Current live source HEAD: `b8b823742bd5fb16026090045cd347feb0f9275e`
- Current Render deploy: `dep-dbbb6pom7kps73ebd0eg` / LIVE

The workspace branch is canonical for design decisions, simulation interpretation and new-session recovery. The live branch remains separate.

---

# Frozen combat / progression decisions
- Knight: stable generalist / penetration / strong heavy.
- Rogue: multihit / crit / high-HP normal execution.
- Tank: team-specialist / knockback / wall protection / control; fresh-run solo parity not required.
- Archer: true straight-line geometry. **Trajectory locks at launch; no post-launch retarget/bending to off-line enemies.**
- Mage: density specialist / AoE / chained explosions.
- Rogue same-target dagger hits are uncapped.
- Boss dagger scalar = `0.70`.
- Boss knockback scalar = `0.40`.
- EXP remains tied to timing attack events/results.
- Faster clear does not receive compensating EXP merely for fewer attacks.

Player mastery reference:
- Average = N25 / G55 / P20.
- Skilled = N10 / G50 / P40 plus modestly faster commitment.
- Skilled is considered attainable; strong mastery improvement is intended.

Balance governance:
`measure/model → identify specialization/artifact/defect → report → discuss → explicit decision → numerical patch`

---

# Current playable implementation — v0.16

Files:
- `timing-defense-v011/v016-core.js`
- `timing-defense-v011/v016-ui.js`
- `timing-defense-v011/v016-render.js`
- `timing-defense-v011/v016.html`

v0.15 remains available as prior rollback page.

## Skill milestones implemented
Actual mechanics through:
`Lv6 / Lv11 / Lv16 / Lv21`

Six-slot HUD reserves:
`Lv6 / Lv11 / Lv16 / Lv21 / Lv26 / Lv31`

### Knight
- Lv6 +12% blade-wave damage.
- Lv11 normal +1 penetration at 85%; heavy +2.
- Lv16 PERFECT-containing attack: +18% damage / +20% knockback.
- Lv21 heavy +20% damage, larger wave, up to +3 penetrations.

### Rogue
- Lv6 second dagger 55%.
- Lv11 +6%p native crit.
- Lv16 PERFECT-containing attack: recovery 390→312 ms.
- Lv21 heavy = 5 daggers total: 100% + 45%×4.
- no same-target cap.
- boss dagger damage 70%.

### Tank
- Lv6 knockback ×1.30.
- Lv11 wall incoming damage -10%.
- Lv16 PERFECT-containing attack refreshes wall shield 80 / 3 s / non-stack.
- Lv21 Ground Impact broad multi-target heavy; Tank heavy knockback ×2.0.
- boss knockback 40%.

### Archer
- Lv6 up to 2 additional straight-line targets.
- pre-Lv16 secondary penetration coefficient 52%.
- Lv11 projectile speed +25% equivalent / base damage +10%.
- Lv16 PERFECT-containing attack ignores armor and preserves penetration damage.
- Lv21 heavy = three arrows 100% + 65% + 65%.
- final v0.16 line fix: launch path is locked; if original target disappears, only a hitbox intersecting the locked line can be hit.

### Mage
- Lv6 splash 50%.
- Lv11 radius +35%, splash 60%.
- Lv16 PERFECT-containing attack: delayed ~180 ms Resonance 55%, original center excluded.
- Lv21 heavy +20% damage, explosion radius ×1.6, larger/slower Greater Arcane Orb.

### HUD/VFX
- six-slot skill strip below Timing Square,
- new unlock pulse,
- no permanent skill-name text beside EXP,
- Tank shield HUD/VFX,
- Lv21 Knight/Tank/Mage signature overlays.

## Important implementation defect already closed
The first v0.16 version used geometric penetration but generic projectile fallback could retarget Archer to `nearestMonster()` after original target death. This could bend Lv21 arrows off-line.

Fixed in live commit:
`b8b823742bd5fb16026090045cd347feb0f9275e`

This was a semantics/implementation fix, not numerical rebalance.

## Deployment validation
- `node --check` PASS for v0.16 JS patches.
- final Archer-line core syntax PASS.
- loader dependency check PASS.
- Render deployment `dep-dbbb6pom7kps73ebd0eg` status LIVE at exact fix commit.

Direct visual/device browser inspection was not available in the current tool lane; Render LIVE proves publication/build, not final visual correctness.

See `V016_IMPLEMENTATION_REPORT.md`.

---

# Encounter / simulation history

## v4 — team role validation
- Tank defensive team value confirmed.
- Rogue durable-normal niche confirmed.
- Archer line vs Mage cluster distinction confirmed.
- Knight stabilizing generalist.
- old unscaled Stage 1–10 saturates with 3–4 players.

## v5 — Tier Pressure Grammar
Pressure families:
- S = Swarm,
- E = Elite/Heavy,
- X = Special/Mixed.

Across five 50-stage prototypes:
- 1-pattern 40.8%,
- 2-pattern 43.6%,
- 3-pattern 15.6%.

All three families are not forced into every stage. Tier identity also uses ratio, timing, geometry, intensity and overlap.

## v6 — concrete current-roster pressure recipes
Swarm candidate bursts:
- line 2P/3P/4P = 8 / 11 / 14,
- cluster = 7 / 10 / 13,
- scatter = 9 / 12 / 16.

Candidate P95 4-second spawn density:
- 2P ≈ 11,
- 3P ≈ 15,
- 4P ≈ 18.

X is the main co-op scaling language through role-bearing composition. E is an effective durability budget rather than one giant HP multiplier.

## v7 — latest: exact v0.16 formula re-run
Files:
- `BALANCE_SIM_REPORT_V7_V016_EXACT.md`
- `combat_exact_v016.py`

Final/formula-corrected volume:
- 12,300 campaign-bound runs,
- 50,000 durable-normal targeted duels,
- 20,000 static line/cluster trials.

### Fixed-level co-op pressure result
3P Average/Skilled:
- Lv6 36.2 / 50.7%,
- Lv11 49.6 / 68.0%,
- Lv16 55.6 / 77.8%,
- Lv21 **81.6 / 96.4%**.

4P:
- Lv6 22.7 / 33.0%,
- Lv11 33.3 / 42.7%,
- Lv16 33.7 / 49.3%,
- Lv21 **52.8 / 73.6%**.

2P is already near saturation in the current pressure/AI-bound model.

T4 Crossfire remains hardest at Lv21:
- 3P 63.3 / 89.3%,
- 4P 33.0 / 59.0%.

### Durable-normal role survives
Mean Lv21 high-HP-normal TTK Average/Skilled:
- Rogue **20.54 / 15.92 s**,
- Archer 25.44 / 19.76,
- Knight 33.45 / 25.14,
- Mage 39.98 / 31.31,
- Tank 42.67 / 33.47.

Rogue still owns the intended durable-normal niche.

### Geometry after Archer line lock
Average:
- line: Archer 16.53 vs Mage 21.40 s,
- dense cluster: Archer 20.03 vs Mage 19.71.

Skilled:
- line: Archer 12.16 vs Mage 15.53,
- dense cluster: Archer 15.08 vs Mage 15.59.

The line identity is strong. Dense-pack separation remains close and is a watch item only.

### v7 balance decision
**No numerical class rebalance authorized.**

Watch items only:
- Archer broad Lv21 campaign throughput,
- 2P saturation,
- real rendered Mage-vs-Archer dense-pack separation,
- real-human teammate cadence.

---

# Exact next work boundary

1. Human/device/browser playtest v0.16 for implementation/readability defects.
2. Verify six-slot HUD fit on target landscape sizes.
3. Visually verify Archer arrows remain straight with nearby off-line enemies.
4. Verify Tank shield refresh/3 s expiry.
5. Verify Mage Resonance visibly excludes original center target.
6. Verify Rogue repeated dagger impacts and Lv21 barrage readability.
7. Verify Lv21 signature VFX remain readable during dense S/X pressure.
8. Fix implementation defects only.
9. Report/discuss before any numerical balance change.

After visual/behavior defects close:
- resume exact co-op pressure calibration using v7 formulas,
- then decide whether to proceed first to Lv26/Lv31 or broader tier authoring.

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
11. `BALANCE_SIM_REPORT_V7_V016_EXACT.md`
12. `SIMULATION_METHOD.md`
13. `NEXT_WORK.md`

Older v1/v2/v3 reports remain available for numerical provenance and decision history.
