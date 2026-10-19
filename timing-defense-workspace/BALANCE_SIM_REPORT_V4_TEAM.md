# Timing Defense — Headless Balance Simulation v4: Team Composition / Co-op Role Validation

Date: 2026-10-20 KST  
Status: **REPORT ONLY — no playable/live balance values changed**

## Frozen rules used

- Archer penetration: straight-line only. No homing / retarget / next-target chaining.
- Tank: team-specialist; solo parity is not required.
- Rogue: no same-target dagger hit cap.
- Boss dagger scalar: 0.70.
- Boss knockback scalar: 0.40.
- EXP remains attack-result/event based.
- No simulation result authorizes an automatic live patch.

## Important modeling boundary

This v4 pass is a **role-isolation team model**, not a final multiplayer-economy model.

- All human team members use the same named timing profile in a comparison.
- Teammates attack independently; no sync-bonus system is modeled yet.
- Stage 1–10 uses the current prototype wave counts/gaps for the primary matrix.
- Run-shop upgrades are intentionally excluded here because multiplayer coin ownership / shop timing / shared-vs-individual purchase rules are not frozen.
- Therefore absolute clear-rate values should not be compared one-to-one with v2/v3 shop-enabled solo results.
- The useful outputs are composition ordering, marginal team contribution, role separation and saturation behavior.

## Deliberate v4 run volume

- 2-player unique-composition campaign confirmation: 3,600 runs.
- 3/4-player unique-composition campaign confirmation: 3,000 runs.
- Duplicate-class composition checks: 3,000 runs.
- Targeted 3-player contribution decomposition: 720 runs.
- Archer-vs-Mage geometry packs: 1,000 runs.
- High-pressure Lv21 role diagnostics: 1,920 runs.
- High-HP specialist diagnostic: 540 runs.
- **Total deliberate v4 analysis volume: 13,780 runs.**

# 1. Two-player campaign — current Stage 1–10 wave pressure

## Skilled profile

| Team | Stage 10 clear | Avg final wall HP |
|---|---:|---:|
| Knight + Mage | 100.0% | 1658 |
| Knight + Archer | 100.0% | 1632 |
| Knight + Rogue | 100.0% | 1509 |
| Archer + Mage | 100.0% | 1459 |
| Rogue + Mage | 100.0% | 1308 |
| Knight + Tank | 100.0% | 1268 |
| Rogue + Archer | 98.3% | 1101 |
| Tank + Mage | 96.1% | 865 |
| Tank + Archer | 93.9% | 720 |
| Rogue + Tank | 83.3% | 539 |

## Average profile

| Team | Stage 10 clear | Avg final wall HP |
|---|---:|---:|
| Knight + Mage | 56.7% | 250 |
| Knight + Rogue | 56.7% | 246 |
| Knight + Archer | 51.1% | 254 |
| Archer + Mage | 8.9% | 28 |
| Rogue + Archer | 7.8% | 19 |
| Rogue + Mage | 7.2% | 21 |
| Knight + Tank | 6.1% | 17 |
| Rogue + Tank | 0% | 0 |
| Tank + Archer | 0% | 0 |
| Tank + Mage | 0% | 0 |

Interpretation:
- Knight is a strong stabilizer/generalist in 2-player teams.
- Tank still pays a large DPS opportunity cost in 2-player fresh-run teams.
- That does not contradict the team-specialist decision, but it means Tank's value is expected to become clearer with more teammates or more severe wall pressure.

# 2. Three- and four-player saturation

With the **current unscaled Stage 1–10 wave**, team-size power quickly overwhelms encounter pressure.

## Average, 3 players
- 9 of 10 unique compositions reached 100% clear.
- The remaining `Rogue + Tank + Archer` reached 98%.
- Final wall HP still differentiates compositions, but clear rate mostly saturates.

## Skilled, 3 players
- Every unique composition reached 100% clear.
- Average final wall HP ranged roughly 1830–1940.

## Four players
- Every unique 4-player composition reached 100% clear at both Average and Skilled.
- At Skilled, all unique 4-player teams finished at effectively full wall HP.
- Even all-same-class 4-player teams reached 100% clear in this current-wave model.

**Conclusion:** the present Stage 1–10 wave is not a useful final balance target for 3–4 player co-op.  
This is not authorization to increase difficulty yet. It means **co-op pressure scaling must eventually be designed explicitly** before 3–4 player class balance can be judged from clear rate.

# 3. Tank team utility

At Lv21 under intentionally heavy wall-pressure diagnostics, replacing a DPS class with Tank often reduced total kills but reduced actual wall HP loss through:
- 10% wall-damage reduction,
- refreshed shield generation,
- knockback/control.

Using `Archer + Mage` as a fixed two-player core under hard diagnostic pressure:

| Third member | Mixed-pressure wall damage | High-HP-pressure wall damage | Line-pressure wall damage | Cluster-pressure wall damage |
|---|---:|---:|---:|---:|
| Knight | 2760 | 3386 | 4913 | 3835 |
| Rogue | 2840 | 3545 | 4938 | 3947 |
| **Tank** | **2811** | **3245** | **4533** | **3626** |

Tank generated roughly 1,150–1,330 shield points over these diagnostics.

Interpretation:
- Tank's role is visible once pressure is high enough that damage prevention matters.
- Tank does not simply make the team immortal.
- Tank often allows more enemies to reach the wall but for less net HP loss, which is consistent with a defensive/control class rather than a DPS class.
- No Tank buff is recommended from v4.

# 4. Rogue team niche

Rogue continues to claim a disproportionate share of durable-normal kills when present in 3-player teams.

Examples from Lv21 / Skilled targeted compositions:
- `Knight + Rogue + Mage`: Rogue took about **39%** of BRUTE/SHIELD kills.
- `Rogue + Archer + Mage`: Rogue took about **41%** of BRUTE/SHIELD kills.
- `Knight + Rogue + Tank`: Rogue took about **42%** of BRUTE/SHIELD kills.

Rogue is only one of three players, so this is a real specialization signal.

In a dedicated high-HP wave with `Archer + Mage` fixed:
- adding Knight: ~8.7 durable-normal kills by the added class,
- adding **Rogue: ~10.2** durable-normal kills,
- adding Tank: ~3.7.

Rogue does not maximize total team wave-clear throughput, but it preferentially finishes durable normal enemies. This supports the intended “that big normal enemy is mine” identity.

No Rogue change is recommended.

# 5. Archer + Mage overlap

A long horizontal line pack and a dense spatial cluster were tested separately at Lv21.

With an `Archer + Mage` pair:

| Geometry | Archer damage share | Mage damage share |
|---|---:|---:|
| Long straight line | **66.8%** | 33.2% |
| Dense cluster | 41.6% | **58.4%** |

This is a strong result.

- Archer wins when enemies are aligned but spatially separated along a trajectory.
- Mage wins when enemies are spatially dense.
- Their crowd-clear roles overlap enough to cooperate, but the geometric specialization remains distinct.

No Archer/Mage role redesign is indicated.

# 6. Knight generalist value

Knight repeatedly acts as the safest third member in current-wave 3-player comparisons.

Examples, Skilled:
- `Archer + Mage` core: adding Knight improved wall HP by about **+480**.
- `Rogue + Mage` core: adding Knight improved wall HP by about **+620**.
- `Rogue + Archer` core: Knight was the strongest third-member addition among the tested alternatives.

Knight therefore retains meaningful value without needing a unique extreme specialty.

# 7. Duplicate-class diagnostic

Duplicate stacking was checked because future multiplayer may allow repeated classes.

Notable 2-player Skilled results:
- Knight + Knight: 100% clear, ~1696 wall HP.
- Rogue + Rogue: 100%, ~1027.
- Archer + Archer: 99%, ~1253.
- Mage + Mage: 100%, ~1402.
- Tank + Tank: 24%, ~52.

At Average:
- **Knight + Knight reached ~93% clear**, much higher than mixed Knight pairs (~51–57%).
- Other same-class damage pairs were far less dominant.
- Tank + Tank remained poor.

This is a **flag, not a balance verdict**. The headless model currently approximates Knight Lv11 blade-wave penetration geometry before the real implementation exists, so the double-Knight result must be rechecked against the exact playable collision formula before any anti-stacking rule or Knight nerf is considered.

Four-player duplicate checks are not informative because the current Stage 1–10 wave is already saturated by four players.

# 8. v4 conclusions

### Supported
- Tank has measurable defensive team value under meaningful pressure.
- Rogue has measurable durable-normal execution value inside teams.
- Archer and Mage remain geometrically distinct.
- Knight is a useful generalist/stabilizer.

### Unresolved
1. **Co-op enemy-pressure scaling** for 2/3/4 humans is not designed yet.
2. **Double-Knight stacking** needs re-test after exact Lv11 penetration is implemented.
3. Multiplayer shop/economy ownership is not frozen, so v4 intentionally does not attempt final co-op economy balance.
4. Sync attacks / round IDs / DUO-TRIPLE-FULL SYNC bonuses are not part of this simulation yet.

### No live changes authorized
No class coefficient, boss resistance, EXP rule, Stage rule, or live prototype code should be changed from this report alone.

## Recommended discussion boundary

Before implementing co-op difficulty changes, decide the philosophy of team-size scaling:
- Should more players mainly create **more enemies**,
- **tougher enemies**,
- a mixture of count + HP,
- or mostly additional elite/special threats while ordinary enemies stay readable?

Only after that philosophy is agreed should a v5 co-op pressure model be calibrated.
