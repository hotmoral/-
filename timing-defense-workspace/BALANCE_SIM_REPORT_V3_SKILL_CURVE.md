# Timing Defense — Headless Balance Simulation v3: Average → Skilled Mastery Curve

Date: 2026-10-20 KST
Status: **REPORT ONLY — no playable/live balance values changed**

## Frozen decisions used by this run

- Archer penetration is **straight-line only**. No auto-retarget / homing / next-target chain.
- Tank is intentionally **team-specialized**. Poor fresh-run solo clear is not, by itself, a balance defect.
- EXP acquisition remains tied to timing attack results/events. Faster-killing classes are not compensated for performing fewer attacks.
- Rogue same-target dagger hits are unrestricted.
- Boss dagger damage scalar remains `0.70`.
- Boss knockback scalar remains `0.40`.
- No simulation result authorizes an automatic live patch. Report → discuss → decide → patch.

## Goal

Measure whether the transition from the current `Average` timing profile to the current `Skilled` profile produces a useful player-mastery curve rather than an arbitrary class-balance cliff.

### Endpoints

`Average`
- NORMAL 25%
- GOOD 55%
- PERFECT 20%
- normal attack cycle 1.14 s
- heavy attack cycle 1.68 s

`Skilled`
- NORMAL 10%
- GOOD 50%
- PERFECT 40%
- normal attack cycle 1.04 s
- heavy attack cycle 1.54 s

The full sweep linearly interpolates both timing accuracy and attack-cycle speed. A second diagnostic holds attack-cycle speed at Average values and improves accuracy only.

## Run volume

- 9-point Average→Skilled full sweep: 6,750 runs
- 9-point accuracy-only sweep: 6,750 runs
- targeted confirmation at 5 proficiency points, 500 seeds/class for Knight/Rogue/Archer/Mage: 10,000 runs
- Skilled accuracy-only confirmation, 1,000 seeds/class for Knight/Rogue/Archer/Mage: 4,000 runs
- **Total v3 analysis volume: 27,500 runs**

Role-aware shop policy is used throughout to avoid mixing the mastery question with shop-policy variation. The v2 report already established that the major class ordering is not a single shop-policy artifact.

---

# 1. Confirmed mastery curve

The table below uses the 500-seed/class targeted confirmation. `t` is progress from Average (`0.0`) to Skilled (`1.0`).

| t | PERFECT | NORMAL | Knight clear | Rogue clear | Archer clear | Mage clear |
|---:|---:|---:|---:|---:|---:|---:|
| 0.50 | 30.0% | 17.5% | 32.6% | 0.0% | 12.4% | 19.4% |
| 0.625 | 32.5% | 15.6% | 54.8% | 1.0% | 36.8% | 43.0% |
| 0.75 | 35.0% | 13.8% | 79.8% | 5.2% | 60.2% | 73.8% |
| 0.875 | 37.5% | 11.9% | 94.8% | 15.8% | 80.8% | 92.6% |
| 1.00 | 40.0% | 10.0% | 98.4% | 32.8% | 94.6% | 97.0% |

### Interpretation

For Knight, Archer and Mage, the curve is not flat and not random. There is a clear mastery band:

- Around PERFECT 30%: the player is still frequently failing the full run.
- Around PERFECT 32.5–35%: clear probability rises rapidly.
- Around PERFECT 37.5%: a competent learned player is already highly reliable on Knight/Mage and strong on Archer.
- At the defined Skilled endpoint (PERFECT 40%, NORMAL 10%): Knight/Archer/Mage are consistently strong.

This supports the desired design principle: **a player who learns the timing system can materially improve without requiring permanent-stat growth first.**

The transition is fairly steep, which is expected in a defense game because a small increase in kill speed can cross a threshold from "enemy reaches wall" to "enemy dies before wall".

---

# 2. Rogue remains a specialist rather than following the general solo curve

Rogue does not follow Knight/Archer/Mage's solo-clear curve:

- 30% PERFECT: 0% clear
- 35% PERFECT: 5.2%
- 37.5% PERFECT: 15.8%
- 40% PERFECT: 32.8%

This is consistent with the previously observed role split rather than evidence of a broken dagger model:

- Rogue remains strong against high-HP normal targets.
- Rogue remains weak against sustained late-run multi-enemy pressure.
- Boss dagger resistance stays at 0.70 and same-target multi-hit remains uncapped.

No Rogue patch is authorized by this result. If later co-op simulation shows that Rogue also lacks a useful team niche, that would be a separate balance issue.

---

# 3. Tank solo result is intentionally non-normative

Tank remains near 0% solo clear across this Average→Skilled sweep in the current fresh-run model.

Per the frozen design decision, this is **not treated as an automatic defect**:

- Tank is a team-specialist class.
- Tank's value is wall preservation, knockback and control rather than solo DPS parity.
- A future permanent-stat/meta-progression layer may eventually make solo completion practical.

Therefore no Tank damage/defense buff is proposed from v3.

The correct next validation for Tank is team-composition simulation, not forcing its solo curve to match damage classes.

---

# 4. Mastery is not only accuracy — cadence matters substantially

A separate diagnostic set the player to the same Skilled judgment probabilities (`N 10 / G 50 / P 40`) but kept attack-cycle speed at the Average values (`1.14 s / 1.68 s`). 1,000 seeds/class were used.

| Class | Full Skilled clear | Skilled accuracy + Average cadence |
|---|---:|---:|
| Knight | 98.4% | 59.9% |
| Rogue | 32.8% | 1.5% |
| Archer | 94.6% | 35.5% |
| Mage | 97.0% | 51.4% |

This is an important result.

The simulator's `Skilled` state means both:
1. the player hits GOOD/PERFECT more reliably, and
2. the player recognizes the timing window and commits the input somewhat faster.

The cadence difference is modest numerically (normal 1.14→1.04 s, heavy 1.68→1.54 s), but it has large campaign consequences because monster pressure is time-based.

This does **not** imply that attack speed should be buffed. It means the game naturally rewards becoming faster and more confident at the timing interaction in addition to becoming more accurate.

---

# 5. Lv21 visibility under the accepted EXP rule

Targeted 500-seed confirmation at the full Skilled endpoint:

| Class | Reach Lv21 by Stage 10 |
|---|---:|
| Knight | 96.4% |
| Rogue | 66.8% |
| Archer | 98.0% |
| Mage | 99.0% |

Rogue's lower reach is partly a consequence of earlier failures; class-specific attack count and kill efficiency also affect EXP pace.

This remains accepted under the current progression philosophy. EXP is not decoupled from timing attacks, and no compensatory EXP patch is proposed.

---

# 6. Decision from v3

The current mastery curve is **plausible and useful enough to continue with**. It provides real room for the player to grow from Average toward Skilled, and the Skilled endpoint is not an extreme expert-only profile.

No numerical live-game change is recommended from v3.

### Current interpretation

- Knight: healthy mastery response for a generalist.
- Archer: healthy mastery response once penetration is modeled as true straight-line geometry.
- Mage: healthy mastery response for a density specialist.
- Rogue: expected specialist tradeoff; evaluate in team context before considering changes.
- Tank: solo curve intentionally not used as the balance target; evaluate in team context.

## Next validation boundary

Before implementing balance changes from these reports, the highest-value next simulation is **team-composition / co-op role validation**, especially:

- whether Tank meaningfully improves team survival without making teams immortal,
- whether Rogue's high-HP-normal deletion creates a valuable team niche,
- whether Archer + Mage crowd-clearing overlap is excessive,
- whether Knight remains a useful generalist in mixed teams,
- 2-player / 3-player / 4-player class combinations under identical seeded waves.

This next step remains simulation/report-only until its results are discussed.
