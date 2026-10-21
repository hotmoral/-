# Timing Defense — Next Work Boundary

Updated: 2026-10-21 KST

## Closed migration gates
1. Cloudflare Durable Objects viability PoC — **PASS**
2. v0.31/v0.32 real-game waiting-room parity — **PASS**
3. v0.33 authoritative Stage 1 parity — **PASS**
4. v0.34 render smoothing / remote projectile parity — **PASS**
5. v0.35 reconnect / Team Shop / Stage 2 parity — **PASS**

## v0.35 closure
Exact validated deployment:
- watched branch: `timing-defense-cloudflare-do-poc`
- HEAD: `b8cb477b47bb8a38f6ab06452c5a9cf0bf26d69d`
- health: `0.35-cf.7`
- preserved checkpoint: `timing-defense-cloudflare-v035-pass-20261021`
- report: `CLOUDFLARE_V035_PASS_2026-10-21.md`

Device-confirmed closure includes:
- Stage 1 authoritative multiplayer,
- Stage 1 -> Team Shop,
- authoritative purchase/coin/rank state,
- immediate shop `처리중…` feedback + duplicate-tap guard,
- shop READY gate,
- host-only NEXT STAGE,
- synchronized Stage 2 intro/start,
- Stage 2 Timing Square/input,
- Stage 2 authoritative GRUNT/RUNNER combat,
- remote human projectile visibility,
- bounded Stage 2 clear,
- authoritative result board,
- reconnect gate,
- Rogue CHARGE palette/flicker fix,
- remote human timing-projectile visual parity.

## Immediate next work — PRE-FLIGHT ONLY
Do **not** immediately implement Stage 3–10 or rebalance anything.

First recover and classify the contracts needed for the next migration slice:

### A. Stage 3–10 generalization audit
- enumerate existing `stagePlan` / monster composition / gap / scaling rules,
- separate already-frozen values from experimental values,
- identify any Stage-specific legacy assumptions that cannot simply be looped over,
- define server-authoritative state/events needed to generalize beyond Stage 2.

### B. Larger-party audit
- confirm 3–4 participant slot semantics,
- human + AI combinations,
- READY/host/reconnect behavior at larger party sizes,
- authoritative contribution/result behavior,
- projectile/event volume and presentation limits.

### C. Lv6+ multiplayer authority audit
For every class unlock consequence, classify as:
1. presentation-only,
2. client prediction + server confirmation,
3. server-authoritative combat consequence.

Do not port a skill effect until its ownership is explicit. Preserve the frozen class identities and exact legacy contracts where already defined.

### D. Preflight deliverable
Before coding, produce a bounded implementation slice with:
- scope,
- non-goals,
- exact reuse vs adapter vs replace classification,
- acceptance checks,
- rollback/checkpoint plan,
- device-validation matrix.

Only after this preflight is reviewed should implementation start.

## Deferred item
Responsive safety across heterogeneous phone screen sizes/aspect ratios is intentionally deferred. Review it later as a shared responsive-safety layer rather than per-device patches.

## Frozen governance
No numerical change to attack damage, monster HP, passive interval, combo coefficients, EXP, shop cost, knockback, stage count/gap or class balance without:
`implement/test -> measure -> classify -> report -> discuss -> explicit decision -> numerical patch/freeze`.
