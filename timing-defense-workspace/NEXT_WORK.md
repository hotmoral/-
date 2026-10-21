# Timing Defense — Next Work Boundary

Updated: 2026-10-21 KST

## Closed migration gates
1. Cloudflare Durable Objects viability PoC — **PASS**
2. v0.31/v0.32 waiting-room parity — **PASS**
3. v0.33 authoritative Stage 1 parity — **PASS**
4. v0.34 render smoothing / remote projectile parity — **PASS**
5. v0.35 reconnect / Team Shop / Stage 2 parity — **PASS**

Exact preserved v0.35 baseline:
- HEAD `b8cb477b47bb8a38f6ab06452c5a9cf0bf26d69d`
- branch `timing-defense-cloudflare-v035-pass-20261021`
- health `0.35-cf.7`

## Explicit user decisions
### N1 — APPROVED / IMPLEMENTED
Restore exact legacy timing EXP:
NORMAL 8 / GOOD 12 / PERFECT 18 / HEAVY 10 / HEAVY+ 14 / GREAT 18 / SUPER 23 / CRITICAL 28.

### N2 — APPROVED / IMPLEMENTED
Restore exact legacy AI stage damage multiplier:
`1 + (stage - 1) * 0.035`.

### N3 — DEFERRED, MANDATORY FUTURE DISCUSSION
N3 is the experimental combo-milestone extra-attack system. It is **not discarded**.
It must not be silently ported, removed, frozen or rebalanced. A separate explicit discussion/decision is required later.

## Active slice — v0.36 Slice A
Status: **CF.3 AUTOMATED VALIDATION CANDIDATE DEPLOYED TO WATCHED BRANCH / PUBLIC SUITE RUN PENDING**

Implementation branch:
- `timing-defense-cloudflare-v036-lv6-authority`
- HEAD `458d468f68c95c569ff57f1e2fd5a4bd20d21e4a`

Cloudflare watched branch:
- `timing-defense-cloudflare-do-poc`
- HEAD `abb2d428df546c257181278ba6bd0814e0471c93`
- loader/cache generation `cf0363`

Expected health:
- version `0.36-cf.3`
- `n1: legacy-heavy-xp-restored`
- `n2: legacy-ai-stage-damage-scaling-restored`
- `n3: deferred-explicit-discussion-required`

### Slice A implementation scope
- Stage 1–2 only; no Stage 3.
- N1 exact EXP parity.
- N2 exact AI stage-damage parity.
- authoritative Lv6 consequences for all five human classes.
- action/cast identity and secondary-hit metadata.
- Rogue +55 ms / 55% authoritative second dagger.
- Tank +30% authoritative knockback.
- Archer strict-line two-target 52% penetration.
- Mage three-target 50% nearby splash.
- cf.2 hardening: remove Rogue's legacy local network secondary mutator; make new secondary VFX obey reconnect event floor.

## Validation policy — CHANGED
Do not require manual phone verification for exact numerical/class consequences.

Read:
- `CLOUDFLARE_V036_AUTOMATED_VALIDATION_2026-10-21.md`

Automated layers:
1. `GET /api/diagnostics/v036-slice-a`
   - actual patched `TimingDefenseRoom.prototype` deterministic self-test,
   - N1/N2, all five Lv6 boundaries, duplicate seq, Stage1->Shop->Stage2.
2. `/v036-client-selftest.html`
   - executes actual `v036-lv6-authority.js` in a controlled browser fixture,
   - Rogue local secondary mutation block,
   - reconnect event-floor / duplicate-VFX checks.
3. `/v036-multiclient-sim.html`
   - one browser tab creates two real WebSocket clients against deployed Durable Object,
   - READY/START, shared Stage1, authoritative Rogue secondary, stale seq, resume floor, reconnect same slot/run, shared Shop, Stage2 synchronization.
4. `/v036-validation-suite.html`
   - one-click aggregate of all three layers.

The model-side network environment cannot access the public `workers.dev` host, so the public suite itself must be launched from a normal browser. This is one automated run, not manual class-by-class gameplay.

## Remaining Slice A gate
Do **not** start Stage 3 yet.

First:
1. public `/api/health` -> `0.36-cf.3`,
2. `/v036-validation-suite.html` -> aggregate **PASS**,
3. only then one short real-device smoke test for actual Samsung/Chrome rendering/touch behavior:
   - current asset loads,
   - timing touch responds,
   - no obvious duplicate projectile/flicker/visual corruption,
   - Stage1 -> Shop -> Stage2 visibly usable.

Exact EXP/damage/knockback/target selection are owned by the automated suite, not by visual inspection.

Only after these gates PASS may Slice B start.

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
- READY/host/reconnect/shop/result/event-volume verification,
- automated multi-client harness should be extended before asking for manual repeated play.

### Later bounded groups
- Stage 4: SHIELD / armor,
- Stage 5–6: boss + FLYER + authoritative Y geometry,
- Stage 7–9: mixed-roster stress,
- Stage 10: final boss/final result,
- Lv11/16/21 authority with forced-level automated tests before natural progression depends on them.

## Deferred UX item
Responsive safety across heterogeneous phone sizes/aspect ratios remains intentionally deferred. Handle later as a shared responsive-safety layer, not per-device patches.

## Frozen governance
No unapproved numerical change. Numerical work must continue to follow:
`implement/test -> measure -> classify -> report -> discuss -> explicit decision -> patch/freeze`.
