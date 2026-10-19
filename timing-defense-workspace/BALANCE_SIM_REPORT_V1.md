# Timing Defense — Headless Balance Simulation Report v1

## Scope
- Core constants mirrored from current prototype: monster HP/speed/armor/wall damage, Stage 1–10 counts/gaps, timing damage tiers, EXP curve, knockback magnitudes.
- Proposed class skills simulated through Lv21 only (Lv6/11/16/21). Lv26/Lv31 are intentionally excluded.
- Rogue has **no same-target hit cap**. Boss dagger damage scalar = **0.70**.
- Boss knockback scalar = **0.40**.
- Shop/run upgrades are disabled in campaign mode in this first pass to isolate class kits. Campaign clear rate is therefore a difficulty warning, not final economy balance.
- Recommended role-tuning variant: Mage Lv16 second explosion becomes an outer-ring effect that excludes the original center target; Tank Lv11 wall reduction = 10%, Lv16 shield = 80 for 3 s (refresh, non-stacking).

## Monte Carlo volume
- Campaign: 5 classes × 4 timing profiles × 300 seeds = **6,000 runs**
- Role scenarios: 5 scenarios × 5 classes × 300 seeds = **7,500 runs**
- Sensitivity sweeps: dagger resistance + boss knockback = **3,360 runs**
- Total = **16,860 simulated runs**

## Lv21 role validation (Skilled timing profile)

| Scenario | Knight | Rogue | Tank | Archer | Mage | Expected winner | Result |
|---|---:|---:|---:|---:|---:|---|---|
| High-HP normal TTK (s) | 6.52 | 3.45 | 8.32 | 5.07 | 7.88 | Rogue | PASS |
| Boss TTK (s) | 31.24 | 25.51 | 42.22 | 24.68 | 38.84 | Archer | PASS |
| Straight-line pack clear (s) | 15.26 | 17.83 | 25.05 | 11.10 | 17.39 | Archer | PASS |
| Dense cluster clear (s) | 14.01 | 17.67 | 16.17 | 11.46 | 8.85 | Mage | PASS |
| Wall crisis damage taken | 856.60 | 807.50 | 624.14 | 759.10 | 745.50 | Tank | PASS |

Interpretation: Rogue deletes high-HP normal enemies; Archer owns straight-line penetration and narrowly leads boss TTK; Mage dominates dense clusters; Tank produces the lowest wall damage under pressure. Knight remains the generalist rather than winning a specialist benchmark.

## Rogue boss dagger sensitivity

| Boss dagger scalar | Rogue boss TTK (s) | Archer boss TTK (s) | Interpretation |
|---:|---:|---:|---|
| 0.60 | 30.17 | 24.82 | Rogue remains strong but not boss-best |
| 0.65 | 27.86 | 24.82 | Rogue remains strong but not boss-best |
| 0.70 | 25.94 | 24.82 | Rogue remains strong but not boss-best |
| 0.75 | 24.25 | 24.82 | Rogue overtakes Archer |
| 0.80 | 22.70 | 24.82 | Rogue overtakes Archer |
| 0.85 | 21.46 | 24.82 | Rogue overtakes Archer |
| 1.00 | 18.32 | 24.82 | Rogue overtakes Archer |

**0.70 is the preferred starting value.** At 0.75 Rogue begins to overtake Archer in this boss duel; at 0.65 Rogue falls notably farther back. 0.70 preserves every dagger hit and the multi-hit feel without making Rogue the default boss killer.

## Boss knockback sensitivity
At a 0.40 boss knockback scalar, Tank still visibly delays a pressure boss, but far less than unrestricted knockback. This keeps Tank control meaningful without trivializing boss approach.

## Corrections found by simulation
1. **Mage Lv16 echo needed role correction.** When the second explosion re-hit the original center target, Mage boss TTK was about 29 s, too strong for a crowd specialist. The recommended outer-ring echo excludes the original center target; Mage still wins the dense-cluster benchmark (~8.85 s) but boss TTK rises to ~38.84 s.
2. **Tank defense needed more separation.** The earlier 8% wall reduction + 60 shield was almost tied with Mage in wall-pressure damage. The recommended 10% reduction + 80 shield yields ~624 wall damage versus the next-best ~746, making Tank’s defensive role clear.
3. **Rogue same-target cap should remain removed.** Rogue kills the high-HP normal target fastest (~3.45 s), while 0.70 boss dagger resistance keeps boss TTK slightly behind Archer (~25.51 s vs ~24.68 s).

## Campaign warning
The no-shop Stage 1–10 campaign is intentionally harsh because all purchasable ATK/HP/DEF upgrades are disabled. Skilled-profile clear rates are therefore not final difficulty targets: Archer ~46%, Knight ~2%, Mage ~2%, Rogue/Tank ~0%. This shows the next simulator revision must include a deterministic standard shop policy before using campaign clear rates to tune solo viability or Stage difficulty.

## Recommended implementation boundary
- Lock Rogue boss dagger scalar at **0.70** and boss knockback scalar at **0.40** for the first playable skill patch.
- Keep Rogue unlimited same-target dagger hits.
- Use Mage Lv16 **outer-ring resonance** rather than a center re-hit.
- Use Tank Lv11 **-10% wall damage** and Lv16 **80 shield / 3 s**, refresh-only and non-stacking, as the next test values.
- Implement Lv6/11/16/21 first, rerun this automated suite against the implemented formulas, then proceed to Lv26/31.
