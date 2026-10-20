# Timing Defense — Next Work Boundary

## Current boundary after live v0.16 + v7

Do **not** change numerical balance merely because a class looks strong or weak in the new build.

Required governance:
`implement/observe → classify implementation defect vs specialization vs real balance issue → report → discuss → explicit decision → numerical patch`

## Current live state
- Public version: **v0.16**
- URL: `https://timing-defense-v011.onrender.com/v016.html`
- Live source HEAD: `b8b823742bd5fb16026090045cd347feb0f9275e`
- Render deploy: `dep-dbbb6pom7kps73ebd0eg` / LIVE

Implemented:
- Lv6 / Lv11 / Lv16 / Lv21 for all five classes,
- six-slot HUD reserving Lv6/11/16/21/26/31,
- boss dagger scalar 0.70,
- boss knockback scalar 0.40,
- Mage Lv16 center-excluding Resonance,
- Tank Lv11 -10% wall damage,
- Tank Lv16 80/3s refresh-only shield,
- class-specific Lv21 heavy transformations,
- **Archer launch-line locking with no off-line retarget after launch**.

## Closed implementation defect
Initial v0.16 allowed generic `nearestMonster()` retarget after an Archer target died, which could bend Lv21 side arrows. This violated the frozen straight-line rule and was fixed before v7 interpretation.

Fix commit:
`b8b823742bd5fb16026090045cd347feb0f9275e`

This was not a balance patch.

---

# v7 exact-formula result now available

See:
- `BALANCE_SIM_REPORT_V7_V016_EXACT.md`
- `combat_exact_v016.py`

Final/formula-corrected campaign-bound volume: 12,300 runs.

Lv21 pressure bound:
- 2P Average/Skilled = 100 / 100%,
- 3P = 81.6 / 96.4%,
- 4P = 52.8 / 73.6%.

T4 Crossfire remains hardest:
- 3P 63.3 / 89.3%,
- 4P 33.0 / 59.0%.

Durable-normal targeted TTK still gives Rogue the intended win:
- Rogue 20.54 / 15.92 s Average/Skilled,
- Archer 25.44 / 19.76,
- Knight 33.45 / 25.14,
- Mage 39.98 / 31.31,
- Tank 42.67 / 33.47.

No numerical rebalance is authorized.

Watch items only:
- Archer broad Lv21 campaign throughput,
- 2P saturation,
- Mage-vs-Archer dense-pack separation,
- future true-human teammate cadence.

---

# Immediate next execution slice

## 1. Human/device/browser v0.16 playtest
Check implementation/readability only:
- page loads and plays normally,
- six skill slots fit target landscape sizes,
- Lv11/Lv16/Lv21 unlock and execute for all classes,
- Archer arrow path stays visually straight when off-line enemies are nearby,
- Tank shield absorbs, refreshes and expires after 3 s,
- Rogue Lv21 5-dagger heavy preserves separate repeated impacts,
- Mage Resonance visibly excludes the original center target,
- Lv21 signature VFX remain readable under dense enemy overlap.

## 2. Fix defects only
Examples of valid immediate fixes:
- wrong target selection,
- missing skill proc,
- UI overlap,
- incorrect timer/expiry,
- VFX obscuring Timing Square,
- formula mismatch against frozen implementation spec.

Examples that require discussion first:
- class damage buffs/nerfs,
- boss resistance changes,
- EXP changes,
- pressure recipe count/HP changes.

## 3. After implementation/readability closure
Resume pressure calibration using exact v7 formulas and targeted real-play evidence.

Only then decide whether the next major feature block should be:
- Lv26/Lv31 signature skills,
- wider 50-stage tier authoring,
- multiplayer synchronization/economy work,
- or permanent/meta-stat progression.

---

# Accepted encounter state remains unchanged
Pressure grammar:
- S = Swarm,
- E = Elite/Heavy,
- X = Special/Mixed.

Rules:
- X is the main co-op scaling language,
- S/E are timed spikes,
- 1/2/3-pattern stages are all valid,
- all three families are not required every stage,
- higher tier does not automatically mean more active pattern types,
- geometry/timing/internal ratios are gameplay data.

Current candidate Swarm bursts:
- line 2P/3P/4P = 8 / 11 / 14,
- cluster = 7 / 10 / 13,
- scatter = 9 / 12 / 16.

Current candidate P95 4-second spawn density:
- 2P ≈ 11,
- 3P ≈ 15,
- 4P ≈ 18.

Do not retune these solely from v7 simulation values.

## Still not frozen
- literal final E HP/armor package,
- final X hardened multipliers,
- exact stage duration,
- final tier number/names/order,
- multiplayer shop/economy ownership,
- duplicate-class policy,
- true human multiplayer cadence/network behavior,
- sync DUO/TRIPLE/FULL rules,
- Lv26/Lv31 coefficients.
