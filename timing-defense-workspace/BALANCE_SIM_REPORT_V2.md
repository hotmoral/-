# Timing Defense — Headless Balance Simulation v2 Report

Date: 2026-10-20 KST
Status: **REPORT ONLY — no playable-game balance values changed**

## Scope

The v2 simulator adds the actual run-shop economy to the v1 headless campaign model:

- Stage 1–10 spawn counts/gaps
- current monster HP/speed/wall damage/armor/knock resistance
- timing damage and EXP tables
- XP curve `60 + 12 × (level - 1)`
- kill coin rewards
- stage-clear reward `55 + stage × 12`
- current shop costs and ranks
- ATK / CRIT / CRIT DMG / WALL HP / DEF / KNOCKBACK effects
- proposed Lv6 / Lv11 / Lv16 / Lv21 skill kits
- Rogue boss dagger scalar = `0.70`
- boss knockback scalar = `0.40`
- Mage Lv16 resonance excludes the original center target
- Tank Lv11 wall reduction = `10%`
- Tank Lv16 shield = `80 / 3 s / refresh, no stack`

No Lv26/Lv31 skill is included yet.

## Run volume

- Main v2 campaign matrix: 18,000 runs
  - 3 shop policies × 4 timing profiles × 5 classes × 300 seeds
- Archer line-geometry sensitivity: 18,000 runs
- Tank Lv6 width/collateral diagnostic: 3,600 targeted runs
- **Total deliberate v2 analysis volume: 39,600 runs**

Each class comparison reuses deterministic seed sets where possible.

## Shop policies

Three policies were tested to avoid drawing conclusions from one purchase strategy:

1. `balanced`: roughly even stat allocation.
2. `offense`: favors ATK/CRIT/CRIT DMG.
3. `role`: class-specific allocation (Tank favors HP/DEF/KNOCKBACK, Rogue favors crit, etc.).

The large class gaps described below persist across all three policies, so the ordering is not merely a shop-policy artifact.

---

# 1. Primary finding — role-aware shop, Skilled player

| Class | Stage 10 clear | Avg stage | Avg final wall HP | Avg wall hits | Avg final Lv | Boss TTK |
|---|---:|---:|---:|---:|---:|---:|
| Knight | 99.3% | 10.00 | 1213.9 | 7.51 | 21.20 | 17.53 s |
| Rogue | 32.0% | 9.58 | 141.7 | 15.50 | 21.30 | 20.80 s |
| Tank | 0.0% | 6.20 | 0 | 21.69 | 15.86 | — |
| Archer* | 100% | 10.00 | 1961.7 | 1.69 | 20.33 | 17.73 s |
| Mage | 98.0% | 9.99 | 1143.6 | 7.59 | 21.50 | 20.82 s |

`*` This Archer row uses the permissive v1/v2 penetration abstraction (next enemies by X). See geometry sensitivity below before treating the Archer result as a balance verdict.

### Interpretation

- Knight and Mage are close to stable solo clear at Skilled input.
- Rogue is viable deep into the run but frequently collapses at Stage 9–10.
- Tank fails much earlier, mostly Stage 5–7.
- Archer result is highly dependent on how "straight-line penetration" is defined.

Failure-stage diagnostic (500 additional comparable Skilled/role seeds):

- Rogue failures: Stage 7 = 4, Stage 8 = 29, Stage 9 = 151, Stage 10 = 146. Clear ≈34%.
- Tank failures: Stage 5 = 54, Stage 6 = 323, Stage 7 = 109, Stage 8 = 14. Clear = 0%.

This suggests Rogue is a late-run tuning issue, while Tank is a substantially earlier structural issue in the solo model.

---

# 2. Player-skill profile result — role-aware shop

Stage 10 clear rates:

| Input profile | Knight | Rogue | Tank | Archer* | Mage |
|---|---:|---:|---:|---:|---:|
| Novice | 0% | 0% | 0% | 0% | 0% |
| Average | 0% | 0% | 0% | 43.3%* | 0% |
| Skilled | 99.3% | 32.0% | 0% | 100%* | 98.0% |
| Expert | 100% | 99.7% | 7.7% | 100%* | 100% |

The novice/average campaign is currently very punishing in this solo headless model. This is a warning, not an automatic patch recommendation. AI teammates/multiplayer are not modeled here.

---

# 3. Archer geometry sensitivity — important unresolved semantic

The primary v2 model inherited the earlier simplification where Archer penetration can select the next enemies by forward X order even when their Y positions are not truly on the arrow line.

A stricter diagnostic was run:

- additional pierce target must be within approximately `|ΔY| <= 0.075` of the original arrow line
- Lv11 projectile-speed bonus does not artificially reduce the attack-cycle time in this diagnostic

### Role-aware result

| Profile | Permissive penetration | Strict line penetration |
|---|---:|---:|
| Average clear | 43.3% | **0%** |
| Skilled clear | 100% | **94.7%** |
| Skilled avg wall HP | 1961.7 | **923.3** |
| Skilled boss TTK | 17.73 s | **20.29 s** |

Conclusion: **Archer's apparent campaign dominance is highly sensitive to penetration geometry.**

Therefore Archer should NOT be nerfed from the permissive simulation result alone. Before v0.16, the semantic must be frozen:

- true geometric straight-line collision, or
- assisted/auto-chain penetration.

The original role description ("straight-line penetration") points toward real line/path collision, but this should be decided explicitly rather than silently inferred.

---

# 4. Tank width sensitivity — Tank weakness is not explained only by one missing abstraction

The v2 main model treats Lv6 `Impact Wave+ width +30%` primarily as knockback width/feel and does not grant automatic collateral damage until the Lv21 broad shockwave.

To test whether this alone explains Tank's poor campaign result, hypothetical Lv6 collateral variants were run. These are **diagnostics, not proposed skill values**.

Hypothesis: after the primary hit, up to 2 nearby enemies receive collateral damage if they are close to the impact lane.

| Lv6 collateral | Average clear | Skilled clear | Expert clear |
|---|---:|---:|---:|
| 0% (main model) | 0% | 0% | 7.7% |
| 35% | 0% | 1% | 99.3% |
| 50% | 0% | 2% | 100% |
| 70% | 0% | 13% | 100% |
| 100% | 0% | 48% | 100% |

Even an unrealistically generous 100% collateral interpretation only raises Skilled Tank clear to ~48% in this model.

Conclusion: **Tank's early solo failure is not safely explained away by the Lv6 width abstraction.** It requires discussion before any numbers are changed.

Possible causes to discuss later (not patch decisions):

- Tank's role may be balanced for teams rather than true solo.
- Stage 5–7 pressure may exceed what defensive mitigation can compensate for without enough damage throughput.
- Wall defense value may need different evaluation in solo vs co-op.
- Tank's early wave may need a more explicit crowd-control mechanic rather than raw damage.

---

# 5. Skill unlock timing

Role-aware, Skilled profile (main v2 model):

| Class | Lv6 | Lv11 | Lv16 | Lv21 |
|---|---:|---:|---:|---:|
| Knight | Stage 2 | Stage 4 | Stage ~6.85 | 97.7% reach, ~Stage 10 |
| Rogue | Stage 2 | Stage ~4.05 | Stage ~6.78 | 70% reach, ~Stage 9.42 |
| Tank | Stage 2 | Stage 4 | 55.3% reach, ~Stage 6.04 | **0%** |
| Archer* | Stage 2 | Stage ~4.63 | Stage ~7.15 | 34% reach, Stage 10 |
| Mage | Stage 2 | Stage ~4.03 | Stage ~6.64 | 99.3% reach, ~Stage 9.91 |

Strict-line Archer diagnostic changes Lv21 reach to ~99% at ~Stage 9.97 because the class clears less quickly and therefore performs more timing attacks.

This exposes an important systemic effect:

> EXP is awarded per timing attack/result, so a class that kills faster can perform fewer attacks and therefore level more slowly.

That is not necessarily wrong, but it means combat efficiency and skill-unlock speed are inversely coupled. This should be an explicit design decision before using Lv21 visibility as a balance target.

For the Average profile, most classes do not naturally reach Lv21 within the current Stage 1–10 campaign at all.

---

# 6. Shop-policy robustness

At Skilled input, changing between balanced / offense / role-aware purchasing did not remove the major ordering:

- Archer / Knight / Mage remain the strongest campaign performers.
- Rogue remains much weaker in full-run survival than in its high-HP-normal specialty.
- Tank remains the weakest solo campaign performer by a large margin.

Therefore the main gaps cannot be dismissed as one bad automatic shopping rule.

---

# 7. What is NOT concluded

No gameplay patch should be made from this report alone.

Specifically, this report does **not** conclude that:

- Archer must be nerfed.
- Tank must receive a specific buff.
- Rogue boss dagger scalar 0.70 must change.
- EXP curve must change.
- Stage difficulty must change.

The report identifies where human design decisions are now required.

## Discussion items before any v0.16 balance patch

1. **Archer penetration semantics** — true line collision vs assisted chaining.
2. **Tank solo expectation** — should Tank be independently Stage-10 viable, or intentionally team-specialized?
3. **Average-player target** — should an Average solo player be expected to clear Stage 10, or only reach a particular stage?
4. **EXP philosophy** — keep EXP per timing attack (efficient classes level more slowly), or eventually decouple some progression from attack count?
5. **Lv21 visibility in Stage 1–10** — is Lv21 intended to be a late-prototype preview or something most competent players should reliably see?

Until those are decided, **no numerical gameplay changes are recommended.**
