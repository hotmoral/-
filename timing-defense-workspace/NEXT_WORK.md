# Timing Defense — Next Work Boundary

Updated: 2026-10-21 KST

## Closed migration gates
1. Cloudflare Durable Objects viability PoC — **PASS**
2. v0.31/v0.32 real-game waiting-room parity — **PASS**
3. v0.33 authoritative Stage 1 parity — **PASS**
4. v0.34 render smoothing / remote projectile parity — **PASS**
5. v0.35 reconnect / Team Shop / Stage 2 parity — **PASS**

Exact v0.35 validated checkpoint:
- HEAD `b8cb477b47bb8a38f6ab06452c5a9cf0bf26d69d`
- branch `timing-defense-cloudflare-v035-pass-20261021`
- health `0.35-cf.7`

## Post-v0.35 preflight — COMPLETE

Canonical audit:
- `CLOUDFLARE_POST_V035_PREFLIGHT_2026-10-21.md`

The preflight audited:
- exact legacy Stage 3–10 plans/compositions/gaps/scaling,
- BRUTE / SHIELD / FLYER and Stage 5/10 boss contracts,
- four-slot / human+AI room semantics,
- event-volume risk at 3–4 participants,
- Lv6–31 ownership classification,
- actual playable legacy skill boundary (Lv6/11/16/21),
- Stage-2-specific Cloudflare hardcoding that must be generalized,
- rollback/device matrix.

Important boundary:
- `TIER_PRESSURE_GRAMMAR_V1.md` and `PRESSURE_RECIPES_V1.md` remain candidate future encounter data and are **not** authorized as live Stage 3–10 replacement values.
- Lv26/Lv31 are design roadmap effects, not part of the current playable legacy skill authority baseline. Do not invent them during migration.

## Explicit numerical parity decision required before implementation

### N1 — Heavy-tier EXP mismatch
Legacy exact:
- NORMAL 8
- GOOD 12
- PERFECT 18
- HEAVY 10
- HEAVY+ 14
- GREAT 18
- SUPER 23
- CRITICAL 28

Current Cloudflare effectively uses:
- NORMAL 8
- GOOD 12
- PERFECT 18
- HEAVY 8
- HEAVY+ 8
- GREAT 12
- SUPER 18
- CRITICAL 28

Recommended classification: **parity defect; restore legacy exact table**.
Do not patch until explicitly approved because it changes deployed numerical behavior.

### N2 — AI stage damage scaling missing
Legacy AI damage multiplier:
`1 + (stage-1)*0.035`

Current Cloudflare AI uses unscaled `baseDamage(tier)`.

Recommended classification: **parity defect; restore exact legacy stage scaling**.
Do not patch until explicitly approved because it changes deployed numerical behavior.

### N3 — Combo milestone attacks
Legacy experimental v0.18 has extra milestone attack budgets; Cloudflare currently has only persistent combo percentage bonus.

Recommendation: **defer as a separate explicit decision** after event delivery is generalized. Do not silently add it to Stage 3 work.

## Next implementation after N1/N2 decision — Slice A only

Do **not** add Stage 3 yet.

Scope:
1. start from exact v0.35 PASS HEAD,
2. create a new implementation branch,
3. keep Stage 1–2 flow unchanged,
4. add generic server skill-authority primitives,
5. implement exact existing **Lv6** consequences for all five human classes,
6. add action/cast identity and secondary-hit event metadata,
7. keep local projectile prediction presentation-only,
8. API/forced-level tests for Lv5 vs Lv6,
9. Stage 1–2 multiplayer regression validation.

Lv6 authority targets:
- Knight: +12% server damage; size remains presentation.
- Rogue: second dagger 55%, same target allowed.
- Tank: +30% server knockback.
- Archer: strict-line penetration up to 2 additional targets, no seeking.
- Mage: 50% authoritative splash.

Non-goals:
- no Stage 3,
- no Lv11+,
- no Lv26/Lv31,
- no new pressure grammar,
- no party-size balance tuning,
- no responsive-safety work,
- no production anti-cheat/security redesign.

## Following bounded slices
Only after Slice A PASS:

### Slice B — Stage 3, two humans first
- Stage 2 clear -> Team Shop,
- NEXT -> Stage 3,
- exact legacy Stage 3: 12 enemies / 980 ms / G44-R34-B22,
- BRUTE authority,
- Stage 3 clear -> Team Shop,
- Stage 4 still blocked in this slice.

### Slice C — larger-party baseline
- 3 humans,
- 4 humans,
- 2 humans + 2 AI,
- 3 humans + 1 AI,
- READY/host/reconnect/shop/result/event-volume verification.

### Later bounded groups
- Stage 4: SHIELD / armor,
- Stage 5–6: boss + FLYER + authoritative Y geometry,
- Stage 7–9: mixed-roster stress,
- Stage 10: final boss/final result,
- Lv11/16/21 authority introduced with forced-level tests before natural progression relies on them.

## Deferred item
Responsive safety across heterogeneous phone sizes/aspect ratios remains intentionally deferred. Handle later as a shared responsive-safety layer, not per-device patches.

## Frozen governance
No numerical change to attack damage, monster HP, passive interval, combo coefficients, EXP, shop cost, knockback, stage count/gap or class balance without:
`implement/test -> measure -> classify -> report -> discuss -> explicit decision -> numerical patch/freeze`.
