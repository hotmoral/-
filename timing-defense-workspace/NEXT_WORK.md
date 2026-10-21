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

## Explicit numerical decisions
### N1 — APPROVED / IMPLEMENTED / AUTOMATED PASS
Exact legacy timing EXP restored:
NORMAL 8 / GOOD 12 / PERFECT 18 / HEAVY 10 / HEAVY+ 14 / GREAT 18 / SUPER 23 / CRITICAL 28.

### N2 — APPROVED / IMPLEMENTED / AUTOMATED PASS
Exact legacy AI stage damage multiplier restored:
`1 + (stage - 1) * 0.035`.

### N3 — DEFERRED, MANDATORY FUTURE DISCUSSION
Experimental combo-milestone extra attacks are **not discarded and not implemented** in Slice A.
Do not silently port, remove, freeze or rebalance N3. A separate explicit discussion/decision is mandatory later.

## Active slice — v0.36 Slice A
Status: **AUTOMATED VALIDATION PASS / FINAL SHORT DEVICE SMOKE PENDING**

Implementation branch:
- `timing-defense-cloudflare-v036-lv6-authority`
- latest implementation HEAD at automated-suite build: `458d468f68c95c569ff57f1e2fd5a4bd20d21e4a`

Cloudflare watched branch:
- `timing-defense-cloudflare-do-poc`
- exact tested HEAD `abb2d428df546c257181278ba6bd0814e0471c93`
- health generation `0.36-cf.3`
- loader/cache generation `cf0363`

Preserved automated-pass checkpoint:
- `timing-defense-cloudflare-v036-automation-pass-20261021`
- HEAD `abb2d428df546c257181278ba6bd0814e0471c93`

Read:
- `CLOUDFLARE_V036_AUTOMATION_PASS_2026-10-21.md`
- `CLOUDFLARE_V036_AUTOMATED_VALIDATION_2026-10-21.md`
- `CLOUDFLARE_V036_SLICE_A_DECISION_2026-10-21.md`
- `CLOUDFLARE_V036_SLICE_A_CANDIDATE_2026-10-21.md`

## Automated validation evidence — PASS
Public suite executed by the user in Samsung Browser:
- `SERVER · PASS · 10/10`
- `CLIENT · PASS · 4/4`
- `MULTICLIENT · PASS · 9/9`
- `FINAL · PASS`

The automated suite owns exact verification for:
- N1/N2,
- Knight +12% server damage,
- Rogue 55% delayed authoritative second dagger,
- Tank +30% authoritative knockback,
- Archer up to 2 strict-line 52% secondary hits,
- Mage up to 3 nearby 50% splash hits,
- primary/secondary action identity and hit indices,
- stale/duplicate `seq` rejection,
- Rogue local-network secondary gameplay mutation block,
- reconnect event-floor / no historical secondary-VFX replay,
- two real WebSocket clients sharing READY/START/combat/reconnect/Shop/Stage2.

Do **not** ask the user to manually re-check numerical values or all five classes on the phone.

## Only remaining Slice A gate
One short real-device game smoke test for things simulation cannot fully prove:
1. actual game page/assets load,
2. Timing Square touch responds,
3. no obvious duplicate projectile, stale VFX replay, flicker or visual corruption,
4. Stage 1 -> Team Shop -> Stage 2 remains visibly usable.

This is a UX/render/input smoke only, not a numerical validation session.

If smoke PASS:
- declare v0.36 Slice A full PASS,
- preserve exact full-PASS branch from tested deployment HEAD,
- synchronize `PROJECT_STATUS.md` and `SESSION_HANDOFF.md`,
- remove/disable candidate-only debug controls when no longer needed,
- then open Slice B.

## Slice B — Stage 3 only, two humans first
Do not start before Slice A full PASS.

Scope after PASS:
- Stage 2 clear -> Team Shop,
- host NEXT -> Stage 3,
- exact legacy Stage 3: 12 enemies / 980 ms / GRUNT 44% / RUNNER 34% / BRUTE 22%,
- authoritative BRUTE behavior,
- Stage 3 clear -> Team Shop,
- Stage 4 remains blocked.

## Following bounded slices
### Slice C — larger-party baseline
- 3 humans,
- 4 humans,
- 2 humans + 2 AI,
- 3 humans + 1 AI,
- extend automated multi-client harness before manual repeated play.

### Later bounded groups
- Stage 4: SHIELD / armor,
- Stage 5–6: boss + FLYER + authoritative Y geometry,
- Stage 7–9: mixed-roster stress,
- Stage 10: final boss/final result,
- Lv11/16/21 authority with automated forced-level tests before natural progression depends on them.

## Deferred UX item
Responsive safety across heterogeneous phone sizes/aspect ratios remains intentionally deferred. Handle later as a shared responsive-safety layer, not per-device patches.

## Frozen governance
No unapproved numerical change. Numerical work must continue to follow:
`implement/test -> measure -> classify -> report -> discuss -> explicit decision -> patch/freeze`.
