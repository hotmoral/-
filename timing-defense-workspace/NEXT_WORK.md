# Timing Defense — Next Work Boundary

Updated: 2026-10-21 KST

## Closed migration gates
1. Cloudflare Durable Objects viability PoC — **PASS**
2. v0.31/v0.32 waiting-room parity — **PASS**
3. v0.33 authoritative Stage 1 parity — **PASS**
4. v0.34 render smoothing / remote projectile parity — **PASS**
5. v0.35 reconnect / Team Shop / Stage 2 parity — **PASS**
6. v0.36 Slice A N1/N2 + Lv6 authority — **PASS**
7. v0.37 Slice B Stage 3 + BRUTE — **PASS**

Exact v0.37 Slice B full-PASS checkpoint:
- branch `timing-defense-cloudflare-v037-slice-b-pass-20261021`
- HEAD `08af6e1e9f399ad13369990dcc452f012ddda1fa`

## N3 product decision — APPROVED / FROZEN CONTRACT
Option B is approved.

Frozen N3 contract:
- triggers at 5 / 10 / 20 / 30 and every +10 after 30,
- exact theoretical max raw-equivalent budgets 60 / 90 / 150 / 210,
- preserve class-specific burst geometry,
- no EXP / charge / combo increment / crit / recursive skill proc,
- normal damage/kills/kill-coin attribution,
- armor and frozen boss scalars remain applicable,
- N3 generic knockback uses NORMAL-equivalent semantics rather than accidental tier escalation,
- Tank may retain its normal class knockback advantage.

N3 is approved but **not yet enabled in combat**. Slice C event delivery must close first.

## Active slice — v0.38 Slice C / larger-party event kernel
Implementation branch:
- `timing-defense-cloudflare-v038-slice-c-event-kernel`

Goals:
- remove dependence on public `events.slice(-24)`,
- retain up to 512 authoritative events,
- per-WebSocket monotonic cursor,
- explicit `event-gap` rather than silent loss,
- preserve reconnect/event-floor historical replay suppression,
- validate 3H / 4H / 2H+2AI / 3H+1AI,
- Stage 4 remains blocked,
- N3 remains disabled during this slice.

### cf.1 validation failure — classified / fixed before further testing
The first deployed v0.38 validation suite failed immediately in SERVER diagnostics with:
`TypeError: Cannot read properties of undefined (reading 'push')`.

Cause:
- v0.38 replaced `TimingDefenseRoom.prototype.event`,
- the replacement assumed `run.events` already existed,
- production `makeRun()` initializes `events: []`, but some older deterministic regression mocks create a minimal run without `events`,
- therefore the new event function broke the v0.36/v0.37 regression harness before Slice C tests could run.

Fix in cf.2:
- `event()` now normalizes missing `run.events` to `[]`,
- missing/invalid `nextEventId` is derived from the current retained tail,
- production behavior is unchanged for normally initialized runs,
- diagnostics/health version bumped to `0.38-cf.2`.

This failure is classified as a **validation/kernel robustness defect**, not evidence of gameplay-state corruption.

## Validation gate
Do not start Stage 4 or N3 implementation yet.

Run the deployed v0.38 suite after health shows `0.38-cf.2`.
It must pass:
- v0.36 server/client regression,
- v0.37 Stage 3 regression,
- event-history/cursor/gap deterministic tests,
- 3H,
- 4H including host reconnect,
- 2H+2AI,
- 3H+1AI,
- READY/START,
- Stage 1 -> Team Shop -> Stage 2,
- monotonic event IDs,
- no silent event loss across >24-event burst,
- no unexpected event-gap.

After automated PASS:
- one short Samsung Browser simulated-peer render/input smoke only,
- then preserve a Slice C PASS checkpoint,
- then implement N3 authority as its own bounded slice,
- Stage 4 follows only after that placement is respected.

## Later
- Stage 4 SHIELD / armor,
- Stage 5–6 boss + FLYER + authoritative Y geometry,
- Stage 7–9 mixed-roster stress,
- Stage 10 final boss/result,
- Lv11/16/21 authority with forced-level automated tests before natural progression depends on them.

## Deferred UX
Responsive safety across heterogeneous phone sizes/aspect ratios remains deferred. Handle later as a shared responsive-safety layer, not per-device patches.

## Frozen governance
No unapproved numerical change. Numerical work must continue to follow:
`implement/test -> measure -> classify -> report -> discuss -> explicit decision -> patch/freeze`.
