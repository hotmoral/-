# Timing Defense — Project Status

Updated: 2026-10-20 KST

## Canonical locations
- Public repo: `hotmoral/-`
- Live branch: `timing-defense-live-v011`
- Planning/balance/handoff branch: `timing-defense-workspace`
- Current playable prototype: **v0.16**
- Public play URL: `https://timing-defense-v011.onrender.com/v016.html`
- Current live source HEAD: `b8b823742bd5fb16026090045cd347feb0f9275e`
- Current Render deploy: `dep-dbbb6pom7kps73ebd0eg` / LIVE

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
- Playable skill implementation now reaches **Lv21**.

## Growth structure
Automatic skill unlocks:
`Lv6 / Lv11 / Lv16 / Lv21 / Lv26 / Lv31`

Implemented now:
`Lv6 / Lv11 / Lv16 / Lv21`

Lv21 is intentionally the first major fourth-attack transformation milestone. Lv26/Lv31 remain planned only.

## Frozen class / progression decisions
- Archer = true straight-line geometry. Final v0.16 projectiles lock trajectory at launch and cannot retarget off-line after launch.
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

# Simulation / design history

## v1 — role separation
Established the intended class-role split.

## v2 — Stage 1–10 + run shop
Resolved:
- Archer auto-chain model artifact → straight-line only,
- Tank solo weakness → accepted team specialization,
- EXP/attack-count coupling → retained.

## v3 — mastery curve
Confirmed meaningful Average→Skilled improvement.

## v4 — team composition
13,780 deliberate runs.

Findings:
- Tank real defensive value under pressure.
- Rogue disproportionate durable-normal kills.
- Archer line geometry vs Mage dense geometry distinction.
- Knight strong stabilizing generalist.
- old unscaled Stage 1–10 waves saturate at 3–4 players.

## v5 — Tier Pressure Grammar
Future 50-stage tier grammar:
- `S` Swarm,
- `E` Elite/Heavy,
- `X` Special/Mixed.

Across five representative 50-stage tiers:
- 1-pattern 40.8%,
- 2-pattern 43.6%,
- 3-pattern 15.6%.

All three families are not forced into every stage. Tier identity comes from family frequency, ratio, geometry, timing, intensity and overlap.

## v6 — concrete pressure recipes
Converted S/E/X into current-roster recipes.

Candidate Swarm burst sizes:
- line 2P/3P/4P = `8 / 11 / 14`,
- cluster = `7 / 10 / 13`,
- scatter = `9 / 12 / 16`.

X is the primary co-op scaling language. E is an effective durability budget rather than one giant HP bar.

Readability candidate P95 4-second spawn density:
- 2P ≈ 11,
- 3P ≈ 15,
- 4P ≈ 18.

## v0.16 implementation
Implemented Lv6/11/16/21 for all five classes plus six-slot skill HUD.

Important implementation correction:
- initial v0.16 penetration selection was geometric but generic projectile retarget could bend Archer arrows after target death,
- fixed at live commit `b8b823742...`,
- Archer now locks launch line and only collides with hitboxes on that line.

See `V016_IMPLEMENTATION_REPORT.md`.

## v7 — latest: exact v0.16 formula re-run
Final/formula-corrected analysis:
- 12,300 campaign-bound runs,
- 50,000 durable-normal targeted duels,
- 20,000 static geometry trials.

### Fixed-level co-op pressure bound
3P clear:
- Lv6 36.2 / 50.7% Average/Skilled,
- Lv11 49.6 / 68.0%,
- Lv16 55.6 / 77.8%,
- Lv21 **81.6 / 96.4%**.

4P clear:
- Lv6 22.7 / 33.0%,
- Lv11 33.3 / 42.7%,
- Lv16 33.7 / 49.3%,
- Lv21 **52.8 / 73.6%**.

2P is already near saturation in this recipe/AI-bound model.

T4 Crossfire remains hardest at Lv21:
- 3P 63.3 / 89.3%,
- 4P 33.0 / 59.0%.

### Durable-normal specialization survives
Mean Lv21 high-HP-normal TTK:
- Rogue 20.54 / 15.92 s Average/Skilled,
- Archer 25.44 / 19.76,
- Knight 33.45 / 25.14,
- Mage 39.98 / 31.31,
- Tank 42.67 / 33.47.

Rogue remains the intended durable-normal specialist despite lower full-wave clear.

### Geometry check after Archer lock
Average:
- line: Archer 16.53 s vs Mage 21.40,
- dense cluster: Archer 20.03 vs Mage 19.71.

Skilled:
- line: Archer 12.16 vs Mage 15.53,
- cluster: Archer 15.08 vs Mage 15.59.

Dense-pack separation is close and remains a watch item, not a patch decision.

### v7 balance decision
**No numerical class rebalance authorized.**

Watch only:
- Archer broad Lv21 campaign throughput,
- 2P saturation,
- exact Mage/Archer dense-pack separation on real rendered battlefield,
- future real-human teammate cadence.

See `BALANCE_SIM_REPORT_V7_V016_EXACT.md` and `combat_exact_v016.py`.

---

# Current next boundary

1. Human/device/browser playtest v0.16 for implementation/readability defects.
2. Check six-slot skill strip fit on target landscape sizes.
3. Visually verify Archer arrows remain straight with off-line enemies nearby.
4. Verify Tank shield refresh/3 s expiry and Mage Resonance center exclusion.
5. Verify Lv21 VFX remain readable under enemy overlap.
6. Fix implementation defects only.
7. Report/discuss before any numerical balance change.

After visual/behavior defects close:
- continue exact co-op pressure calibration using v7 formulas,
- then proceed toward Lv26/Lv31 signature skills and larger tier authoring.

## Still not frozen
- final E HP/armor package,
- final X hardened values,
- final stage duration,
- true human multiplayer cadence/network behavior,
- multiplayer shop/economy ownership,
- duplicate-class policy,
- sync-bonus implementation,
- final number/names/order of tiers,
- Lv26/Lv31 exact coefficients.
