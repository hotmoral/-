# Timing Defense — Next Work Boundary

Updated: 2026-10-21 KST

## Closed migration gates
1. Cloudflare Durable Objects viability PoC — **PASS**
2. v0.31/v0.32 waiting-room parity — **PASS**
3. v0.33 authoritative Stage 1 parity — **PASS**
4. v0.34 render smoothing / remote projectile parity — **PASS**
5. v0.35 reconnect / Team Shop / Stage 2 parity — **PASS**

Exact v0.35 preserved baseline:
- HEAD `b8cb477b47bb8a38f6ab06452c5a9cf0bf26d69d`
- branch `timing-defense-cloudflare-v035-pass-20261021`
- health `0.35-cf.7`

## Post-v0.35 preflight — COMPLETE
Read:
- `CLOUDFLARE_POST_V035_PREFLIGHT_2026-10-21.md`
- `CLOUDFLARE_V036_SLICE_A_DECISION_2026-10-21.md`
- `CLOUDFLARE_V036_SLICE_A_CANDIDATE_2026-10-21.md`

## Explicit user decisions
### N1 — APPROVED
Restore exact legacy timing EXP:
NORMAL 8 / GOOD 12 / PERFECT 18 / HEAVY 10 / HEAVY+ 14 / GREAT 18 / SUPER 23 / CRITICAL 28.

### N2 — APPROVED
Restore exact legacy AI stage damage multiplier:
`1 + (stage - 1) * 0.035`.

### N3 — DEFERRED, MANDATORY FUTURE DISCUSSION
N3 is the experimental combo-milestone extra-attack system. It is **not discarded**.
It must not be silently ported, removed, frozen or rebalanced. A separate explicit discussion/decision is required later.

## Active slice — v0.36 Slice A
Status: **IMPLEMENTED / WATCHED BRANCH TRIGGERED / LIVE & DEVICE VALIDATION PENDING**

Implementation branch:
- `timing-defense-cloudflare-v036-lv6-authority`
- HEAD `ce3ea7f168fce26f6e76556cd73fea9fb08dce99`

Cloudflare watched branch:
- `timing-defense-cloudflare-do-poc`
- HEAD `8b1e2890ea582bd1ddaeae89157a82500adf40a0`
- loader/cache generation `cf0362`

Expected health:
- version `0.36-cf.1`
- `n1: legacy-heavy-xp-restored`
- `n2: legacy-ai-stage-damage-scaling-restored`
- `n3: deferred-explicit-discussion-required`

Candidate test URL:
`https://timing-defense-do-poc.sktjsek.workers.dev/?v036debug=1&fix=cf0362`

### Implemented Slice A scope
- Stage 1–2 only; no Stage 3.
- N1 exact EXP parity.
- N2 exact AI stage-damage parity.
- authoritative Lv6 consequences for all five human classes.
- action/cast identity and secondary-hit metadata.
- scheduled Rogue second dagger (+55 ms).
- authoritative Archer line penetration and Mage splash target selection.
- remote/authoritative secondary skill presentation without client damage authority.
- host-only candidate debug level endpoint and `?v036debug=1` LV5/LV6 controls for differential tests.

Lv6 effects:
- Knight: +12% server damage; projectile size remains presentation.
- Rogue: 55% second dagger, same target allowed with nearest fallback.
- Tank: +30% server knockback.
- Archer: up to 2 strict-line additional hits at 52% damage.
- Mage: up to 3 nearby splash hits at 50% damage.

## Internal checks completed
- new server entry syntax PASS,
- new client authority/presentation syntax PASS,
- loader syntax PASS,
- isolated contract harness PASS for N1/N2 and all five Lv6 boundaries,
- watched execution files synchronized with implementation candidate; watched-only deployment marker retained.

These do not replace real Durable Object/device validation.

## Immediate validation gate
Do **not** start Stage 3 yet.

First:
1. confirm public `/api/health` reports `0.36-cf.1`,
2. validate N1 and N2 on real Durable Object state,
3. use host LV5/LV6 controls and verify all five class boundaries,
4. run two-human Stage 1–2 regression,
5. verify server is the only damage authority and local prediction does not double damage,
6. verify reconnect / Team Shop / Stage 2 result remain clean.

The model-side fetch environment cannot access the public `workers.dev` host, so public health confirmation must be made from the user browser/device.

Only after Slice A PASS may Slice B start.

## Following bounded slices
### Slice B — Stage 3, two humans first
- Stage 2 clear -> Team Shop,
- NEXT -> Stage 3,
- exact legacy Stage 3: 12 enemies / 980 ms / G44-R34-B22,
- BRUTE authority,
- Stage 3 clear -> Team Shop,
- Stage 4 remains blocked.

### Slice C — larger-party baseline
- 3 humans,
- 4 humans,
- 2 humans + 2 AI,
- 3 humans + 1 AI,
- READY/host/reconnect/shop/result/event-volume verification.

### Later bounded groups
- Stage 4: SHIELD / armor,
- Stage 5–6: boss + FLYER + authoritative Y geometry,
- Stage 7–9: mixed roster stress,
- Stage 10: final boss/final result,
- Lv11/16/21 authority with forced-level tests before natural progression depends on them.

## Deferred UX item
Responsive safety across heterogeneous phone sizes/aspect ratios remains intentionally deferred. Handle later as a shared responsive-safety layer, not per-device patches.

## Frozen governance
No unapproved numerical change. Numerical work must continue to follow:
`implement/test -> measure -> classify -> report -> discuss -> explicit decision -> patch/freeze`.
