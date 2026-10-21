# Timing Defense — Cloudflare v0.36 Slice A Automated Validation PASS

Date: 2026-10-21 KST
Status: **AUTOMATED VALIDATION PASS / FINAL DEVICE SMOKE PENDING**

## Candidate under test
Cloudflare watched branch:
- `timing-defense-cloudflare-do-poc`
- HEAD `abb2d428df546c257181278ba6bd0814e0471c93`
- health generation `0.36-cf.3`
- loader/cache generation `cf0363`

Preserved automated-pass checkpoint:
- branch `timing-defense-cloudflare-v036-automation-pass-20261021`
- exact HEAD `abb2d428df546c257181278ba6bd0814e0471c93`

## Public validation evidence
User opened the deployed validation suite in Samsung Browser and supplied screenshot evidence showing:
- `SERVER · PASS · 10/10`
- `CLIENT · PASS · 4/4`
- `MULTICLIENT · PASS · 9/9`
- `FINAL · PASS`

The result panel also showed the expected cf.3 validation-suite identity and N1 HEAVY+ EXP example `xpGain: 14`.

## What the automated suite covers
### Server deterministic layer
- N1 exact timing EXP restoration,
- N2 exact AI stage damage scaling,
- Knight Lv6 +12% authority,
- Rogue Lv6 authoritative 55% delayed second dagger,
- Tank Lv6 +30% authoritative knockback,
- Archer Lv6 strict-line secondary penetration,
- Mage Lv6 authoritative splash,
- action identity / hit indices,
- stale/duplicate sequence rejection,
- Stage 1 -> Team Shop -> Stage 2 server transition.

### Client authority/presentation layer
- actual `v036-lv6-authority.js` exercised in controlled browser fixture,
- legacy Rogue local secondary gameplay mutation blocked in network mode,
- authoritative secondary VFX event-floor handling,
- historical Lv6 secondary VFX not replayed after resume,
- repeated snapshots do not duplicate secondary VFX.

### Real deployed multi-client layer
- two WebSocket clients against the deployed Durable Object,
- READY / START,
- shared Stage 1 state,
- authoritative Rogue secondary propagation,
- stale sequence rejection,
- resume event floor,
- reconnect to the same slot/run,
- shared Team Shop,
- shared READY / NEXT / Stage 2 synchronization.

## Numerical decisions represented
N1 — approved and implemented.
N2 — approved and implemented.
N3 — **not implemented; mandatory future discussion remains open**. Do not silently add, discard, freeze or rebalance combo-milestone extra attacks.

## Remaining Slice A gate
Do not repeat manual class-by-class numerical testing.

Only one short real-device game smoke remains, limited to browser/render/touch behavior the automated suite cannot fully prove:
- live game assets load,
- Timing Square touch input responds,
- no obvious duplicate projectile, stale VFX replay, flicker or visual corruption,
- Stage 1 -> Team Shop -> Stage 2 is visibly usable.

If that smoke passes, close v0.36 Slice A, preserve the exact PASS checkpoint, synchronize canonical status/handoff, then open Slice B: Stage 3 only.
