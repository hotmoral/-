# Timing Defense — Balance Simulation v7: Exact v0.16 Formula Re-run

Date: 2026-10-20 KST  
Status: **REPORT ONLY — no numerical rebalance authorized**

## Purpose

Re-run the v6 concrete S/E/X pressure recipes after the first real Lv6/Lv11/Lv16/Lv21 implementation exists, using the coefficients actually implemented in v0.16 rather than the earlier approximate candidate model.

This pass also checked the implementation against frozen semantics before interpreting balance.

## Important implementation finding fixed before final v7 interpretation

The first v0.16 source correctly made *penetration selection* geometric, but inherited the old generic projectile behavior that retargeted `nearestMonster()` if the original target died before impact. That allowed Archer Lv21 side arrows to bend toward off-line enemies.

This was treated as an implementation defect, not a balance change.

Final v0.16 Archer behavior now:
- launch trajectory is locked,
- projectile does not bend or retarget after launch,
- if the original target disappears, the arrow only hits a live enemy whose hitbox intersects the locked line,
- subsequent penetration remains on that same line.

Fix commit: `b8b823742bd5fb16026090045cd347feb0f9275e`.

---

## Model boundary

The campaign-bound model intentionally remains conservative:
- one local human player uses the named Average/Skilled profile,
- other team slots use current live AI cadence/result quality and **do not** receive human Lv6–21 class skills,
- S/E/X recipes come from `PRESSURE_RECIPES_V1.md`,
- local class formulas mirror final v0.16 through Lv21,
- fixed-level snapshots are used instead of pretending the future full 50-stage progression/economy is already implemented.

Therefore these are **pressure bounds / skill-step diagnostics**, not final human-co-op clear-rate targets.

Implemented details now mirrored include:
- Knight: +12%, Lv11 85% penetration, Lv16 +18% PERFECT damage/+20% knockback, Lv21 +20% heavy and 3 extra penetrations.
- Rogue: 55% second dagger, +6%p native proc crit, exact 390→312 ms recovery reduction, Lv21 4×45% follow-ups.
- Tank: Lv6 knockback, Lv11 -10% wall damage, Lv16 80 shield with true 3 s expiry/refresh, Lv21 full-damage Ground Impact coverage and ×2 heavy knockback.
- Archer: +10%, projectile life ÷1.25, strict locked straight-line collision, pre-Lv16 52% secondary penetration, Lv16 armor-ignore/100% preserved penetration on PERFECT, Lv21 100/65/65 triple shot.
- Mage: 50→60% splash, +35% radius, 55% outer-ring Resonance with center exclusion, Lv21 +20% heavy / ×1.6 radius / slower orb.

---

# 1. Fixed-level skill-step result

## 3-player teams

| Local level | Average clear | Skilled clear |
|---|---:|---:|
| Lv6 | 36.2% | 50.7% |
| Lv11 | 49.6% | 68.0% |
| Lv16 | 55.6% | 77.8% |
| **Lv21** | **81.6%** | **96.4%** |

## 4-player teams

| Local level | Average clear | Skilled clear |
|---|---:|---:|
| Lv6 | 22.7% | 33.0% |
| Lv11 | 33.3% | 42.7% |
| Lv16 | 33.7% | 49.3% |
| **Lv21** | **52.8%** | **73.6%** |

2-player teams are already near saturation under this recipe envelope:
- Lv6 Average ≈99%, Skilled 100%,
- Lv11+ ≈100%.

### Interpretation

The main power step is clearly Lv21. That is directionally consistent with the design because Lv21 is deliberately the first major heavy-attack transformation milestone.

This is **not** sufficient evidence to nerf Lv21. Future real-human teammates will be stronger than the current AI-bound teammates, while future stage pressure/economy is not frozen yet.

---

# 2. Final Lv21 pressure bound after exact formula extraction

Stable rerun volume: 3,500 campaign-bound runs (5 deterministic seeds per matrix cell).

| Team | Average | Skilled | Avg final wall HP A/S |
|---|---:|---:|---:|
| 2P | 100.0% | 100.0% | 1862 / 1980 |
| 3P | **81.6%** | **96.4%** | 814 / 1377 |
| 4P | **52.8%** | **73.6%** | 510 / 886 |

T4 Crossfire remains the hardest prototype identity:
- 3P: Average 63.3%, Skilled 89.3%.
- 4P: Average 33.0%, Skilled 59.0%.

Mastery remains highly meaningful rather than being erased by multiplayer pressure.

---

# 3. Why v7 differs from the earlier v6 bound

Earlier v6 approximate Lv21 result:
- 3P = 88.4 / 94.9% Average/Skilled,
- 4P = 68.3 / 83.0%.

Final v0.16-formula bound:
- 3P = 81.6 / 96.4%,
- 4P = 52.8 / 73.6%.

The lower Average / 4P result is explainable by model corrections rather than a newly introduced nerf:
1. Rogue Lv16 now removes exactly 78 ms of recovery instead of incorrectly shortening the whole cycle by 20%.
2. Tank Lv16 shield actually expires after 3 seconds instead of persisting indefinitely in the old bound.
3. Tank has no invented non-heavy collateral damage before Ground Impact.
4. Knight extra heavy penetrations use the implemented 85% coefficient rather than full damage.
5. Archer pre-Lv16 penetrations use the live 52% coefficient and strict line geometry.
6. Archer triple arrows are now trajectory-locked instead of retargeting off-line enemies.

So v7 is a better formula-fidelity bound than v6.

---

# 4. Lv21 local-class campaign contribution signal

Additional distinct seeded role matrix: 2,500 campaign-bound runs.

## 3P Average local class clear
- Knight 86.7%
- Rogue 64.0%
- Tank 82.7%
- Archer 98.0%
- Mage 84.7%

## 3P Skilled
- Knight 98.0%
- Rogue 86.0%
- Tank 98.0%
- Archer 100.0%
- Mage 99.3%

## 4P Average
- Knight 58.0%
- Rogue 35.0%
- Tank 66.0%
- Archer 66.0%
- Mage 59.0%

## 4P Skilled
- Knight 68.0%
- Rogue 46.0%
- Tank 72.0%
- Archer 91.0%
- Mage 73.0%

These full-stage clear values must **not** be interpreted as equal-DPS targets. Rogue is expected to trade broad wave throughput for durable-normal specialization; Tank is expected to trade damage for wall/control value.

Archer's higher campaign throughput is a **watch item**, not a nerf decision. Geometry approximation, future human teammate behavior, exact authored tier distribution and real screen density still matter.

---

# 5. Durable-normal role check after real v0.16 formulas

50,000 targeted Lv21 durable-normal duels were run (5,000 seeds × 5 classes × 2 timing profiles) against the same high-HP normal target.

Mean TTK:

| Class | Average | Skilled |
|---|---:|---:|
| **Rogue** | **20.54 s** | **15.92 s** |
| Archer | 25.44 s | 19.76 s |
| Knight | 33.45 s | 25.14 s |
| Mage | 39.98 s | 31.31 s |
| Tank | 42.67 s | 33.47 s |

Rogue therefore still owns the intended high-HP normal-enemy niche despite having lower full-stage clear throughput.

No Rogue buff is supported by full-stage clear rate alone.

---

# 6. Archer vs Mage geometry re-check

After removing Archer retarget/bending, a simple Lv21 static-pack diagnostic produced:

### Average
- line pack: Archer 16.53 s vs Mage 21.40 s.
- dense cluster: Archer 20.03 s vs Mage 19.71 s.

### Skilled
- line pack: Archer 12.16 s vs Mage 15.53 s.
- dense cluster: Archer 15.08 s vs Mage 15.59 s.

The line identity is strong. Dense-cluster performance is much closer and is sensitive to coarse lane/radius abstraction, so this diagnostic does **not** justify a Mage buff or Archer nerf.

The important implementation result is that Archer no longer gains artificial off-line coverage from retargeting.

---

# 7. Run volume

Final/formula-corrected campaign-bound analysis:
- Lv6 snapshot: 2,100 runs.
- Lv11 snapshot: 2,100.
- Lv16 snapshot: 2,100.
- Lv21 stable snapshot: 3,500.
- independent Lv21 local-class role matrix: 2,500.
- **campaign-bound total: 12,300 runs.**

Additional targeted durable-normal validation:
- **50,000 duels.**

The static geometry diagnostic adds 20,000 class/profile/geometry trials but is treated separately because it is not a campaign run.

---

# 8. Balance decision

**No numerical class balance patch is recommended from v7.**

Supported:
- exact Lv6→21 implementation preserves a strong mastery response,
- Rogue durable-normal specialization survives,
- Tank remains valuable as pressure rises,
- strict Archer straight-line semantics are now implemented more faithfully,
- T4 remains the best current stress identity,
- Lv21 is a deliberately large milestone.

Watch items for later discussion, not automatic patching:
- Archer broad campaign throughput at Lv21,
- 2P saturation,
- final human-co-op pressure once human teammate cadence exists,
- exact Mage-vs-Archer dense-pack separation on the real rendered battlefield.

---

# 9. Next boundary

1. Public v0.16 device/browser playtest for visual/readability defects only.
2. Do not rebalance from first feel impressions; report first.
3. Validate skill-strip density and Lv21 VFX under actual overlap.
4. Validate straight Archer lines visually with off-line enemies nearby.
5. Validate Tank shield timing/expiry and Mage Resonance center exclusion by observation.
6. After implementation defects close, resume co-op pressure calibration using v7 formulas.
