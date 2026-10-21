# Timing Defense — Cloudflare v0.40 Stage 4 SHIELD Preflight

Date: 2026-10-22 KST  
Status: **PREFLIGHT / EXACT LEGACY CONTRACT RECOVERED**

## Baseline
- prior full-PASS checkpoint: `timing-defense-cloudflare-v039-pass-20261022`
- exact baseline HEAD: `911dd67cf4bb4d704e050f8e3a92cb34c48deb3a`
- v0.39 N3 contract remains frozen and unchanged.

## Exact Stage 4 legacy encounter
Recovered directly from the legacy live source; no new numerical decision is required.

- count: **13**
- spawn gap: **940 ms**
- composition thresholds:
  - GRUNT: 36%
  - RUNNER: 26%
  - SHIELD: 20%
  - BRUTE: 18%

Equivalent type selection:
- `r < .36` -> GRUNT
- `.36 <= r < .62` -> RUNNER
- `.62 <= r < .82` -> SHIELD
- `.82 <= r` -> BRUTE

## Exact SHIELD contract
Legacy monster metadata:
- HP: **540**
- speed: **0.057**
- size: **1.08**
- wall damage: **120**
- knock resist: **0.62**
- armor multiplier: **0.72**
- kill reward: **10**

Armor semantics are multiplicative final incoming-damage reduction:
`actual = max(1, round(incomingDamage * 0.72))`.

This is equivalent to 28% reduction before the final integer damage is applied.

Existing approved stage HP rules remain unchanged:
- stage factor: `1 + (stage - 1) * 0.13`
- ordinary non-boss experiment: `x1.10`

Therefore Stage 4 ordinary HP values are:
- GRUNT: 489
- RUNNER: 252
- SHIELD: **826**
- BRUTE: 1376

## Integration audit findings
SHIELD already has an existing legacy visual silhouette in `drawMonsterShape()`.

However current Cloudflare combat metadata added incrementally through v0.36/v0.39 only enumerates monster types that were already reachable in Stages 1–3. Without Stage 4 compatibility work, SHIELD could fall back to GRUNT metadata in some Lv6/N3 geometry/knock calculations.

Required compatibility work for this slice:
1. add SHIELD `{knockResist:.62,size:1.08}` to v0.36 Lv6 geometry metadata;
2. add SHIELD `{knockResist:.62,size:1.08}` to v0.39 N3 geometry metadata;
3. give SHIELD exact server movement/wall/armor/reward authority instead of old unknown-type fallback;
4. keep BRUTE exact Stage 3+ behavior intact;
5. keep Stage 1–3 and N3 numerical contracts unchanged.

## Bounded v0.40 scope
Implement only Stage 4:
- Stage 3 Team Shop -> host NEXT -> Stage 4
- Stage 4 intro/combat
- exact 13/940 encounter and four-type roster
- SHIELD exact armor, movement, wall damage, knock resistance and reward
- Stage 4 clear -> Team Shop
- Stage 5 remains blocked

Out of scope:
- Stage 5 boss
- FLYER
- authoritative Y geometry changes
- Lv11/Lv16/Lv21 migration
- any numerical rebalance
- responsive-layout redesign

## Required deterministic/live validation
Server tests must cover at least:
- Stage 4 plan/count/gap/composition thresholds
- Stage 4 HP values
- SHIELD 0.72 armor rounding
- SHIELD reward/kill/contribution
- SHIELD movement and wall timing
- SHIELD base wall damage 120 and existing DEF reduction
- SHIELD knock resist 0.62
- Lv6 Archer/Mage geometry uses SHIELD size 1.08
- Tank Lv6 knockback uses SHIELD knock resist 0.62
- N3 geometry/knock metadata uses SHIELD exact values
- Stage 3 shop -> Stage 4
- Stage 4 -> shop
- Stage 5 blocked
- full v0.39 regression
- event-stream/larger-party regression

Live automation policy:
`code audit -> deterministic tests -> GitHub Actions Playwright/WebSocket validation -> minimal Samsung Browser visual/input smoke only if needed`.
